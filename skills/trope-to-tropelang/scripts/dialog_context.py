#!/usr/bin/env python3
"""
TropeLang dialog interrogation tool (12_PRD_Dialog_and_Prose.md §9-10).

For every `dialog(...)` annotation in a .trl file, resolve its prose and surface the
graph facts that frame it — preconditions, motivations, postconditions, context — then
assemble a generation prompt (TRL slice + annotation + prose template).

Usage:
  python3 dialog_context.py <file.trl> [--prose-dir DIR] [--json]

The reference parser (lib.rs) owns the grammar; this tool is the author-facing
interrogation/prompt-assembly layer described in the PRD.
"""

import sys, os, argparse, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_tropelang import lex  # reuse the shared tokenizer

try:
    import yaml
except ImportError:
    yaml = None


# ---------------------------------------------------------------------------
# token helpers
# ---------------------------------------------------------------------------
def find_match(toks, i, open_v, close_v):
    """Index of the bracket closing the one at toks[i] (which must be `open_v`)."""
    depth = 0
    while i < len(toks):
        v = toks[i][1]
        if v == open_v:
            depth += 1
        elif v == close_v:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(toks) - 1


def parse_annotation(toks, i):
    """Parse a `dialog(...)` starting at the `dialog` token index i. Returns (fields, end)."""
    j = i + 1  # '('
    end = find_match(toks, j, "(", ")")
    f = {"kind": None, "src": None, "text": [], "inline": None,
         "inject": [], "context": [], "line": toks[i][2]}
    k = j + 1
    while k < end:
        key = toks[k][1]
        k += 1
        if k < end and toks[k][1] == "=":
            k += 1
        if key == "kind":
            f["kind"] = toks[k][1]; k += 1
        elif key == "src":
            f["src"] = toks[k][1]; k += 1
        elif key == "inline":
            f["inline"] = toks[k][1]; k += 1  # BLOCK token value (raw YAML)
        elif key == "text":
            if toks[k][1] == "[":
                m = find_match(toks, k, "[", "]")
                f["text"] = [t[1] for t in toks[k + 1:m] if t[0] == "STR"]
                k = m + 1
            else:
                f["text"] = [toks[k][1]]; k += 1
        elif key == "inject":
            m = find_match(toks, k, "[", "]")
            p = k + 1
            while p < m:
                if toks[p][0] in ("ID", "VAR") and p + 2 <= m and toks[p + 1][1] == "=":
                    f["inject"].append((toks[p][1], toks[p + 2][1])); p += 3
                else:
                    p += 1
                if p < m and toks[p][1] == ",":
                    p += 1
            k = m + 1
        elif key == "context":
            m = find_match(toks, k, "[", "]")
            f["context"] = [t[1] for t in toks[k + 1:m] if t[1] != ","]
            k = m + 1
        else:
            k += 1  # unknown field — skip its value
        if k < end and toks[k][1] == ",":
            k += 1
    return f, end


def rule_blocks(toks):
    """Each rule block with its source-line span and when:/then: lines."""
    blocks, i = [], 0
    while i < len(toks):
        if toks[i][0] == "ID" and toks[i][1] == "rule":
            name = toks[i + 1][1] if i + 1 < len(toks) else "?"
            j = i + 2
            while j < len(toks) and toks[j][1] != "{":
                j += 1
            end = find_match(toks, j, "{", "}")
            when_ln = then_ln = None
            depth = 0
            for k in range(j, end + 1):
                v = toks[k][1]
                if v == "{":
                    depth += 1
                elif v == "}":
                    depth -= 1
                elif toks[k][0] == "ID" and depth == 1 and v == "when":
                    when_ln = toks[k][2]
                elif toks[k][0] == "ID" and depth == 1 and v == "then":
                    then_ln = toks[k][2]
            blocks.append({"name": name, "start": toks[i][2], "end": toks[end][2],
                           "when": when_ln, "then": then_ln})
            i = end + 1
        else:
            i += 1
    return blocks


_BOUNDARY = {"{", "}", "="}
_BOUNDARY_KW = {"apply", "timeout_apply", "then", "triggers", "branches", "rule", "fork", "prompt"}


def annotated_event(toks, dlg_i):
    """The evt a dialog trails, if any. Scans back at bracket-depth 0 (so `=` inside tag
    params doesn't count): an `evt <name>` reached cleanly means attached; hitting a block
    boundary first means the dialog is a standalone action (e.g. inside a fork apply)."""
    depth = 0
    k = dlg_i - 1
    while k >= 0:
        kind, v, ln = toks[k]
        if v in ("]", ")"):
            depth += 1
        elif v in ("[", "("):
            depth -= 1
        elif depth == 0:
            if v == "evt":
                return (toks[k + 1][1] if k + 1 < len(toks) else "?"), ln
            if v in _BOUNDARY or (kind == "ID" and v in _BOUNDARY_KW):
                return None, None
        k -= 1
    return None, None


def apply_blocks(toks):
    """Spans of `apply = { … }` / `timeout_apply = { … }` blocks (for branch-local scope)."""
    out = []
    for i in range(len(toks) - 2):
        if toks[i][0] == "ID" and toks[i][1] in ("apply", "timeout_apply"):
            j = i + 1
            if j < len(toks) and toks[j][1] == "=":
                j += 1
            if j < len(toks) and toks[j][1] == "{":
                end = find_match(toks, j, "{", "}")
                out.append((i, end, toks[j][2], toks[end][2]))
    return out


_SCOPE_KW = {"scene", "act", "beat", "arc"}


def scope_blocks(toks):
    """Temporal scope blocks (scene/act/beat/arc with a `{ … }` body) and their spans.
    Nested beats are captured too, so a dialog's innermost enclosing moment can be found."""
    out, i = [], 0
    while i < len(toks):
        if toks[i][0] == "ID" and toks[i][1] in _SCOPE_KW:
            j = i + 1
            name = None
            if j < len(toks) and toks[j][0] in ("ID", "VAR", "NUM", "STR"):
                name = toks[j][1]; j += 1
            if j < len(toks) and toks[j][1] == "{":
                end = find_match(toks, j, "{", "}")
                out.append({"kind": toks[i][1], "name": name,
                            "open_idx": j, "close_idx": end,
                            "open_line": toks[j][2], "close_line": toks[end][2]})
                i = j + 1  # descend into the body to catch nested beats
                continue
        i += 1
    return out


def intent_lines(toks, var):
    """Source lines where `var` carries an intent tag `[~...]` (its motivations)."""
    out = []
    for k in range(len(toks) - 2):
        if (toks[k][0] == "VAR" and toks[k][1] == var
                and toks[k + 1][1] == "[" and toks[k + 2][1] == "~"):
            out.append(toks[k][2])
    return sorted(set(out))


# ---------------------------------------------------------------------------
# prose resolution
# ---------------------------------------------------------------------------
# Non-text fields a dialog node may carry for synthesis (beyond `text`).
_NODE_FIELDS = ("speaker", "addressee", "cue", "tone", "motivation", "kind")


def node_fields(node):
    """Normalize a YAML dialog node into the fields the tool surfaces."""
    text = node.get("text", [])
    if isinstance(text, str):
        text = [text]
    out = {"text": text}
    for key in _NODE_FIELDS:
        out[key] = node.get(key)
    return out


def resolve_node(f, prose_dir):
    """Return (node_fields, error) for a dialog from `src`, `inline`, or `text`."""
    if f["src"]:
        if "#" not in f["src"]:
            return None, f"src {f['src']!r} missing '#path'"
        fname, path = f["src"].split("#", 1)
        full = os.path.join(prose_dir, fname)
        if yaml is None:
            return None, "PyYAML not installed (pip install pyyaml)"
        if not os.path.exists(full):
            return None, f"file not found: {full}"
        node = yaml.safe_load(open(full)) or {}
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return None, f"path '{path}' not found in {fname}"
            node = node[part]
        if not isinstance(node, dict):
            return None, f"node '{path}' is not a mapping"
        return node_fields(node), None
    if f["inline"]:
        if yaml is None:
            return None, "PyYAML not installed (pip install pyyaml)"
        try:
            node = yaml.safe_load(f["inline"]) or {}
        except yaml.YAMLError as e:
            return None, f"inline YAML error: {e}"
        if not isinstance(node, dict):
            return None, "inline YAML is not a mapping"
        return node_fields(node), None
    # bare inline prose
    return node_fields({"text": f["text"]}), None


def fill(line, inject):
    for sym, val in inject.items():
        line = line.replace("{" + sym + "}", val)
    return line


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
def slice_lines(src_lines, a, b, exclude=None):
    """Source lines [a, b], dropping bare `when:`/`then:` headers and an excluded span."""
    a = max(1, a); b = min(len(src_lines), b)
    ex0, ex1 = exclude or (None, None)
    out = []
    for n in range(a, b + 1):
        if ex0 is not None and ex0 <= n <= ex1:
            continue
        line = src_lines[n - 1].rstrip()
        bare = line.strip()
        if bare in ("when:", "then:", "{", "}") or bare.startswith("//") or not bare:
            continue
        if bare.replace(" ", "") in ("apply={", "timeout_apply={"):
            continue
        out.append(line)
    return out


def interrogate(path, prose_dir):
    src = open(path).read()
    src_lines = src.splitlines()
    toks = lex(src, os.path.basename(path))
    rules = rule_blocks(toks)
    applies = apply_blocks(toks)
    scopes = scope_blocks(toks)

    items = []
    for i, t in enumerate(toks):
        if t[0] == "ID" and t[1] == "dialog" and i + 1 < len(toks) and toks[i + 1][1] == "(":
            f, end_i = parse_annotation(toks, i)
            span = (f["line"], toks[end_i][2])  # the dialog annotation's own line range
            evt_name, _ = annotated_event(toks, i)
            rule = next((r for r in rules if r["start"] <= f["line"] <= r["end"]), None)
            apply_blk = next((ab for ab in applies if ab[0] < i < ab[1]), None)
            inject = dict(f["inject"])

            # prose + non-text synthesis context (speaker / cue / tone / …)
            node, err = resolve_node(f, prose_dir)
            node = node or {}
            text, motivation, ykind = node.get("text"), node.get("motivation"), node.get("kind")
            cues = {key: fill(node[key], inject) for key in ("speaker", "addressee", "cue", "tone")
                    if node.get(key)}

            # motivations from participants' intent tags
            motiv_lines = []
            for _, v in f["inject"]:
                if v.startswith("$"):
                    motiv_lines += intent_lines(toks, v)
            motiv_lines = sorted(set(motiv_lines))

            # Enclosing temporal scope (when the dialog lives in a scene, not a rule).
            scope_blk = None
            if not rule:
                encl = [s for s in scopes if s["open_idx"] < i < s["close_idx"]]
                scope_blk = max(encl, key=lambda s: s["open_idx"]) if encl else None
            scope_name = f"{scope_blk['kind']} {scope_blk['name'] or ''}".strip() if scope_blk else None

            # Preconditions: rule `when`, else the co-present facts earlier in the beat.
            if rule:
                pre = slice_lines(src_lines, rule["when"], rule["then"] - 1)
                pre_label = f"rule {rule['name']} when"
            elif scope_blk:
                pre = slice_lines(src_lines, scope_blk["open_line"] + 1, span[0] - 1)
                pre_label = f"{scope_name} (earlier in beat)"
            else:
                pre, pre_label = [], None

            # Postconditions: fork branch apply, else rule `then`, else later facts in the beat.
            if apply_blk:
                post = slice_lines(src_lines, apply_blk[2], apply_blk[3], exclude=span)
                post_label = "branch apply" if evt_name is None else None
            elif rule:
                post = slice_lines(src_lines, rule["then"], rule["end"] - 1, exclude=span)
                post_label = f"rule {rule['name']} then"
            elif scope_blk:
                post = slice_lines(src_lines, span[1] + 1, scope_blk["close_line"] - 1)
                post_label = f"{scope_name} (later in beat)"
            else:
                post, post_label = [], None

            items.append({
                "line": f["line"], "kind": f["kind"] or ykind or "dialog",
                "event": evt_name,
                "source_desc": (f["src"] if f["src"]
                                else "inline YAML" if f["inline"]
                                else f"inline text {f['text']}"),
                "inject": f["inject"], "context": f["context"],
                "rule": rule["name"] if rule else scope_name,
                "preconditions": pre, "pre_label": pre_label,
                "postconditions": post, "post_label": post_label,
                "motivation_lines": [src_lines[n - 1].strip() for n in motiv_lines],
                "yaml_motivation": fill(motivation, inject) if motivation else None,
                "cues": cues,
                "prose": [fill(x, inject) for x in (text or [])],
                "error": err,
            })
    return items


def render(items, path):
    if not items:
        print(f"(no dialog annotations in {path})")
        return
    for d in items:
        print("─" * 78)
        head = f"● {path}:{d['line']}  kind={d['kind']}"
        head += f"  event={d['event']}" if d["event"] else "  (fork branch / standalone)"
        print(head)
        print(f"  prose source: {d['source_desc']}")
        if d["error"]:
            print(f"  !! {d['error']}")
        for n, line in enumerate(d["prose"], 1):
            print(f"     [{n}] {line}")
        if d["cues"]:
            print("  synthesis context: " + ", ".join(f"{k}={v!r}" for k, v in d["cues"].items()))
        if d["inject"]:
            print("  inject:  " + ", ".join(f"{k}={v}" for k, v in d["inject"]))
        if d["context"]:
            print("  context: " + ", ".join(d["context"]))

        print("  ── preconditions" + (f" ({d['pre_label']}):" if d["pre_label"] else " (standalone):"))
        for line in d["preconditions"] or ["     (none)"]:
            print(f"     {line.strip()}")
        print("  ── motivations:")
        for line in d["motivation_lines"] or (["     (no intent tags on participants)"]):
            print(f"     {line}")
        if d["yaml_motivation"]:
            print(f"     yaml: {d['yaml_motivation']}")
        print("  ── postconditions" + (f" ({d['post_label']}):" if d["post_label"] else ":"))
        for line in d["postconditions"] or ["     (none)"]:
            print(f"     {line.strip()}")

        print("  ── generation prompt:")
        prompt = assemble_prompt(d)
        for line in prompt.splitlines():
            print(f"     {line}")
    print("─" * 78)


def assemble_prompt(d):
    """TRL slice + annotation + prose template -> one generation prompt."""
    out = []
    subject = f"event '{d['event']}'" if d["event"] else "this moment"
    out.append(f"Write {d['kind']} for {subject}.")
    if d["preconditions"]:
        out.append("Preconditions (true at this moment):")
        out += [f"  - {l.strip()}" for l in d["preconditions"] if l.strip()]
    if d["motivation_lines"] or d["yaml_motivation"]:
        out.append("Motivations:")
        out += [f"  - {l}" for l in d["motivation_lines"]]
        if d["yaml_motivation"]:
            out.append(f"  - {d['yaml_motivation']}")
    if d["postconditions"]:
        out.append("This moment then causes:")
        out += [f"  - {l.strip()}" for l in d["postconditions"] if l.strip()]
    if d["cues"]:
        out.append("Delivery:")
        out += [f"  - {k}: {v}" for k, v in d["cues"].items()]
    if d["context"]:
        out.append("Context (who perceives/understands what): " + ", ".join(d["context"]))
    if d["prose"]:
        out.append("Template (fill any remaining {slots}; pick one variant if several):")
        out += [f"  | {l}" for l in d["prose"]]
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Interrogate TropeLang dialog annotations.")
    ap.add_argument("file")
    ap.add_argument("--prose-dir", default=".", help="directory holding the prose YAML files")
    ap.add_argument("--json", action="store_true", help="emit structured JSON instead of a report")
    args = ap.parse_args()

    items = interrogate(args.file, args.prose_dir)
    if args.json:
        print(json.dumps(items, indent=2))
    else:
        render(items, args.file)
    sys.exit(0)
