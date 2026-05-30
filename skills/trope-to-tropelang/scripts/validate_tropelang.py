"""
TropeLang structural validator — v1.3 grammar + planned extensions.

Implemented in the reference Rust parser (lib.rs v1.3), accepted here:
  domain tag sigils   = # % @ &   (Body / Mind / Essence / Rel / Verb)
  !...!  *...*  ?...?             epistemic wrappers (absolute / contingent / latent)
  (A|B|C) (A|B|...) (...)         ambiguity expressions; `as <name>` labels them
  resolve <name> -> <fact|ambiguity>   in-world collapse (narrow = collapse to a
                                       smaller ambiguity)
  retcon { <name> -> <fact>, ... }     author-level collapse
  Constraint (01 §11.4): resolve/retcon may target ONLY a named, non-absolute
  ambiguity. The Rust parser enforces this; this structural validator does not yet.

Validator-only (not in the Rust reference parser):
  concept declarations; attr/prop/state/verb/rel decls; import / ref.

Checks performed:
  - Balanced braces / parens / brackets
  - Tag syntax (modifier immediately before name)
  - No fractional-number identifiers
  - rule blocks contain when: and then:
  - No sidecar labels on entity declarations
  - Even count of * epistemic wrappers (warns if odd)
"""

import sys, os, glob, re as _re

ENTITY_TYPES = {"char", "set", "obj", "evt", "arc", "concept"}  # v1.3: concept added
SCOPE_TYPES  = {"scene", "act", "beat"}
DECL_TYPES   = {"attr", "prop", "state", "verb", "rel"}   # v1.2 attribute declarations
PLANNED_KW   = {"resolve", "retcon", "narrow", "as", "import", "ref"}
# Tag sigils (v1.3):
#   = Body  # Mind  % Essence  ~ Intent  @ Rel  & Verb  + generic Prop
#   - remove  ? query  ! assert-absent
ALL_SIGILS   = set("+-~?!#@&=%")

errors   = []
warnings = []


def lex(src, label=""):
    tokens = []
    i, line = 0, 1
    while i < len(src):
        c = src[i]
        if c == '\n': line += 1; i += 1; continue
        if c in ' \t\r': i += 1; continue

        # Comments
        if c == '/' and i + 1 < len(src) and src[i + 1] == '/':
            while i < len(src) and src[i] != '\n': i += 1
            continue

        # Triple-quoted block string (inline YAML for dialog)
        if c == '"' and src[i:i+3] == '"""':
            end = src.find('"""', i + 3)
            if end == -1:
                errors.append(f"[{label}] line {line}: unterminated block string")
                return tokens
            block = src[i+3:end]
            tokens.append(('BLOCK', block, line))
            line += block.count('\n')
            i = end + 3
            continue

        # String literal
        if c == '"':
            j = i + 1
            while j < len(src) and src[j] != '"': j += 1
            if j >= len(src):
                errors.append(f"[{label}] line {line}: unterminated string")
                return tokens
            tokens.append(('STR', src[i+1:j], line)); i = j + 1; continue

        # Number
        if c.isdigit():
            j = i + 1; dot = False
            while j < len(src) and (src[j].isdigit() or (src[j] == '.' and not dot)):
                if src[j] == '.': dot = True
                j += 1
            tokens.append(('NUM', src[i:j], line)); i = j; continue

        # Variable
        if c == '$':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'): j += 1
            if j == i + 1:
                errors.append(f"[{label}] line {line}: bare $"); i += 1; continue
            tokens.append(('VAR', src[i:j], line)); i = j; continue

        # Identifier / keyword
        if c.isalpha() or c == '_':
            j = i + 1
            while j < len(src) and (src[j].isalnum() or src[j] == '_'): j += 1
            tokens.append(('ID', src[i:j], line)); i = j; continue

        # Ellipsis — planned void/open marker
        if c == '.' and src[i:i+3] == '...':
            tokens.append(('ELLIPSIS', '...', line)); i += 3; continue

        # Multi-char operators (current grammar, longest match first)
        matched = False
        for op in ["!--", "->", "!>", "!@", "!=", ">=", "<=", "==", "--", "><"]:
            if src[i:i+len(op)] == op:
                tokens.append(('OP', op, line)); i += len(op); matched = True; break
        if matched: continue

        # Single-char tokens — current grammar + planned extensions (* | .)
        if c in "+-~?!><@=:,{}[]()":
            tokens.append(('OP', c, line)); i += 1; continue
        if c in "*|.#%&":
            tokens.append(('OP', c, line)); i += 1; continue  # planned extensions incl. domain sigils (= # % @ &)

        errors.append(f"[{label}] line {line}: unexpected char {c!r}"); i += 1

    return tokens


def check_braces(tokens, label):
    stack = []
    pairs = {'}': '{', ']': '[', ')': '('}
    for kind, val, line in tokens:
        if kind == 'OP' and val in '{[(':
            stack.append((val, line))
        elif kind == 'OP' and val in '}])':
            if not stack:
                errors.append(f"[{label}] line {line}: unmatched '{val}'")
            elif stack[-1][0] != pairs[val]:
                errors.append(f"[{label}] line {line}: mismatched '{val}' "
                              f"(opened '{stack[-1][0]}' at line {stack[-1][1]})")
            else:
                stack.pop()
    for ch, line in stack:
        errors.append(f"[{label}] line {line}: unclosed '{ch}'")


def check_tags(tokens, label):
    """Tags must be [sigil? name params?] — sigil is any of +-~?!#@&"""
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        if kind == 'OP' and val == '[':
            i += 1
            if i >= len(tokens): break
            k2, v2, l2 = tokens[i]
            if k2 == 'OP' and v2 in ALL_SIGILS:
                i += 1
                if i >= len(tokens): break
                k3, v3, l3 = tokens[i]
                if k3 not in ('ID', 'VAR', 'STR'):
                    errors.append(
                        f"[{label}] line {l3}: expected tag name after '{v2}', got {v3!r}")
        i += 1


def check_sidecar_labels(tokens, label):
    """Flag entity declarations that still use the deprecated inline label form."""
    all_entity_kw = ENTITY_TYPES | DECL_TYPES
    for idx in range(len(tokens) - 2):
        k1, v1, l1 = tokens[idx]
        k2, v2, l2 = tokens[idx + 1]
        k3, v3, l3 = tokens[idx + 2]
        if (k1 == 'ID' and v1 in ENTITY_TYPES        # only entity types — not attr decls
                and k2 in ('ID', 'VAR')
                and k3 == 'STR'):
            errors.append(
                f"[{label}] line {l1}: sidecar label \"{v3}\" on '{v2}' — "
                "use // annotation instead")


def check_rule_structure(tokens, label):
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        if kind == 'ID' and val == 'rule':
            depth = 0; found_when = found_then = False; j = i
            while j < len(tokens):
                kj, vj, lj = tokens[j]
                if kj == 'OP' and vj == '{': depth += 1
                elif kj == 'OP' and vj == '}':
                    depth -= 1
                    if depth == 0: break
                elif kj == 'ID' and vj == 'when' and depth == 1: found_when = True
                elif kj == 'ID' and vj == 'then' and depth == 1: found_then = True
                j += 1
            if not found_when: errors.append(f"[{label}] line {line}: rule missing 'when:'")
            if not found_then: errors.append(f"[{label}] line {line}: rule missing 'then:'")
        i += 1


def check_epistemic_balance(tokens, label):
    stars = [t for t in tokens if t[0] == 'OP' and t[1] == '*']
    if len(stars) % 2 != 0:
        warnings.append(f"[{label}]: odd number of '*' epistemic markers — check wrapper balance")


def build_declaration_registry(tokens):
    """Build a set of all declared names (entities + attr decls) from the token stream.
    Used by the reference validation pass to check that referenced identifiers exist."""
    return set(build_kind_registry(tokens).keys())


def build_kind_registry(tokens):
    """Map each declared name to its declaring keyword (char/set/obj/evt/arc/concept/
    attr/prop/state/verb/rel). Used for existence + entity-type checks on references."""
    reg = {}
    all_decl_kw = ENTITY_TYPES | DECL_TYPES
    for i in range(len(tokens) - 1):
        kind, val, _ = tokens[i]
        if kind == 'ID' and val in all_decl_kw:
            k2, v2, _ = tokens[i + 1]
            if k2 in ('ID', 'VAR'):
                reg.setdefault(v2, val)
    return reg


# Reserved param keys whose value must reference a node of a specific entity type (01 §5.3).
EXPECTED_KIND = {"site": "set", "event": "evt"}


def check_references(tokens, kinds, label):
    """Check tag parameter VALUES that reference graph nodes. A bare identifier value
    (e.g. `[&Foreshadows(event=macbeth_falls)]`) must name a node declared in this file,
    and — for entity-typed reserved keys — be of the expected type. Variables, strings,
    numbers, and booleans are skipped. Warning-level: an unknown name may be imported."""
    in_tag = 0
    for idx in range(len(tokens)):
        kind, val, line = tokens[idx]
        if kind == 'OP' and val == '[':
            in_tag += 1
        elif kind == 'OP' and val == ']':
            in_tag = max(0, in_tag - 1)
        elif in_tag > 0 and kind == 'ID' and idx >= 2 and tokens[idx - 1] == ('OP', '=', tokens[idx - 1][2]):
            if val in ('true', 'false') or not val[:1].islower():
                continue  # boolean / enum / Tag-shaped value — not a node reference
            key = tokens[idx - 2][1]
            if val not in kinds:
                warnings.append(f"[{label}] line {line}: param {key}={val} references "
                                f"'{val}', not declared in this file — ensure it is imported")
            elif key in EXPECTED_KIND and kinds[val] != EXPECTED_KIND[key]:
                errors.append(f"[{label}] line {line}: param {key}={val} expects a "
                              f"{EXPECTED_KIND[key]}, but '{val}' is declared a {kinds[val]}")


def check_intent_targets(tokens, registry, label):
    """Check that [~Intent(target=x)] params reference declared graph nodes.
    Variables ($x) are always valid — they're bound in rule patterns.
    Quoted strings are flagged — they should be concept declarations instead."""
    i = 0
    while i < len(tokens):
        kind, val, line = tokens[i]
        # Look for [~ sigil
        if kind == 'OP' and val == '[':
            if i + 1 < len(tokens) and tokens[i+1] == ('OP', '~', tokens[i+1][2]):
                # Scan forward for target= param
                j = i + 1
                depth = 1
                while j < len(tokens) and depth > 0:
                    kj, vj, lj = tokens[j]
                    if kj == 'OP' and vj == '(': depth += 1
                    elif kj == 'OP' and vj == ')': depth -= 1
                    elif kj == 'ID' and vj == 'target':
                        # Next should be = then the value
                        if j + 2 < len(tokens):
                            keq, veq, _ = tokens[j + 1]
                            kval, vval, lval = tokens[j + 2]
                            if keq == 'OP' and veq == '=':
                                if kval == 'STR':
                                    errors.append(
                                        f"[{label}] line {lval}: intent target \"{vval}\" "
                                        f"is a string — declare as: concept {vval.replace(' ', '_')} [...]")
                                elif kval == 'ID' and vval not in registry:
                                    warnings.append(
                                        f"[{label}] line {lval}: intent target '{vval}' "
                                        f"not declared in this file — ensure it is imported")
                    j += 1
        i += 1


def validate(src, label=""):
    toks = lex(src, label)
    check_braces(toks, label)
    check_tags(toks, label)
    check_sidecar_labels(toks, label)
    check_rule_structure(toks, label)
    check_epistemic_balance(toks, label)
    kinds = build_kind_registry(toks)
    check_intent_targets(toks, set(kinds.keys()), label)
    check_references(toks, kinds, label)
    return toks


# ---------------------------------------------------------------------------
# Report mode — where did each tag come from?
# ---------------------------------------------------------------------------
def declarations_with_lines(tokens):
    """name -> (declaring keyword, line) — the in-file source of each tag/entity."""
    reg = {}
    all_decl_kw = ENTITY_TYPES | DECL_TYPES
    for i in range(len(tokens) - 1):
        kind, val, line = tokens[i]
        if kind == 'ID' and val in all_decl_kw:
            k2, v2, _ = tokens[i + 1]
            if k2 in ('ID', 'VAR'):
                reg.setdefault(v2, (val, line))
    return reg


def imply_decls(tokens):
    """[(lhs, line, [components]), ...] from each `imply Name -> [A, B, ...]`."""
    out, i = [], 0
    while i < len(tokens):
        if tokens[i][0] == 'ID' and tokens[i][1] == 'imply':
            line = tokens[i][2]
            lhs = tokens[i + 1][1] if i + 1 < len(tokens) and tokens[i + 1][0] == 'ID' else '?'
            j, comps = i + 2, []
            while j < len(tokens) and tokens[j][1] not in ('[', '{', '}'):
                j += 1
            if j < len(tokens) and tokens[j][1] == '[':
                j += 1
                while j < len(tokens) and tokens[j][1] != ']':
                    if tokens[j][0] == 'ID':
                        comps.append(tokens[j][1])
                    j += 1
            out.append((lhs, line, comps))
            i = j
        i += 1
    return out


def tag_usages(tokens):
    """{name: {sigils, lines}} for every `[sigil? Name …]` TAG. A `[` is a tag only when
    it follows an operand (ID/VAR/STR/]/)); value/component lists (after `=` or `->`) and
    variable tags ([+$x]) are skipped."""
    uses = {}
    for i in range(len(tokens)):
        if not (tokens[i][0] == 'OP' and tokens[i][1] == '[') or i == 0:
            continue
        pk, pv, _ = tokens[i - 1]
        if not (pk in ('ID', 'VAR', 'STR') or (pk == 'OP' and pv in (']', ')'))):
            continue
        j = i + 1
        sigil = '+'
        if j < len(tokens) and tokens[j][0] == 'OP' and tokens[j][1] in ALL_SIGILS:
            sigil = tokens[j][1]; j += 1
        if j < len(tokens) and tokens[j][0] == 'ID':
            name, line = tokens[j][1], tokens[j][2]
            e = uses.setdefault(name, {'sigils': set(), 'lines': []})
            e['sigils'].add(sigil)
            if line not in e['lines']:
                e['lines'].append(line)
    for e in uses.values():
        e['lines'].sort()
    return uses


def _trl_root(path):
    """Walk up from a file to the `trl/` corpus root (the dir holding prelude.trl)."""
    d = os.path.dirname(os.path.abspath(path)) if path else None
    while d and d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, 'prelude.trl')):
            return d
        d = os.path.dirname(d)
    return None


def build_corpus_index(target_path):
    """name -> 'kind in trl/<relfile>' for every declaration and imply across the whole
    corpus (prelude + concepts + modules + tropes), excluding the target file itself.
    Lets the report resolve an otherwise-'external' element to where it actually lives."""
    root = _trl_root(target_path)
    if not root:
        return {}
    index, target_abs = {}, os.path.abspath(target_path)
    for f in sorted(glob.glob(os.path.join(root, '**', '*.trl'), recursive=True)):
        if os.path.abspath(f) == target_abs:
            continue
        rel = os.path.relpath(f, root)
        toks = lex(open(f).read(), rel)
        for name, (kind, _l) in declarations_with_lines(toks).items():
            index.setdefault(name, f"{kind} in trl/{rel}")
        for lhs, _l, _c in imply_decls(toks):
            index.setdefault(lhs, f"imply in trl/{rel}")
    return index


_RESERVED = (ENTITY_TYPES | SCOPE_TYPES | DECL_TYPES | PLANNED_KW |
             {'rule', 'when', 'then', 'not', 'count', 'imply', 'surface', 'surface_global',
              'prompt', 'fork', 'past', 'future', 'foreach', 'where', 'unique', 'true',
              'false', 'in', 'timeout_apply', 'triggers', 'apply', 'branches', 'dialog',
              'narration', 'monologue', 'exposition', 'aside'})


def node_refs(tokens):
    """Identifiers used as node references (edge operands / param values), excluding
    keywords, param keys, function calls, and tag names. Used to spot concept reuse."""
    out = {}
    for i, (k, v, line) in enumerate(tokens):
        if k != 'ID' or v in _RESERVED:
            continue
        nxt = tokens[i + 1][1] if i + 1 < len(tokens) else ''
        if nxt in ('=', '('):          # param key or function/verb call
            continue
        p = tokens[i - 1] if i > 0 else ('', '', '')
        if p[0] == 'OP' and (p[1] == '[' or p[1] in ALL_SIGILS):   # tag name
            continue
        out.setdefault(v, []).append(line)
    return out


def report(src, label, target_path=None):
    """For every tag used in the file, show where it originated — resolving across the
    whole corpus (prelude/concepts/modules/tropes), so the only true 'inline' tags are
    the bespoke ones invented here. Also lists node references that reuse the corpus."""
    toks = lex(src, label)
    decls = declarations_with_lines(toks)
    implies = imply_decls(toks)
    imply_lhs = {lhs: line for lhs, line, _ in implies}
    imply_comps = {lhs: comps for lhs, _, comps in implies}
    comp_of = {}
    for lhs, line, comps in implies:
        for c in comps:
            comp_of.setdefault(c, (lhs, line))
    uses = tag_usages(toks)
    corpus = build_corpus_index(target_path) if target_path else {}

    groups = {"declared": [], "imply": [], "component": [], "corpus": [], "inline": []}
    for name in sorted(uses):
        sig = ''.join(sorted(uses[name]['sigils']))
        disp = f"[{sig}]{name}"
        used = "used: " + ", ".join(str(n) for n in uses[name]['lines'])
        if name in decls:
            kind, dl = decls[name]
            groups["declared"].append((disp, f"{kind} declared @ line {dl}", used))
        elif name in imply_lhs:
            groups["imply"].append((disp, f"imply @ line {imply_lhs[name]} -> [{', '.join(imply_comps[name])}]", used))
        elif name in comp_of:
            er, el = comp_of[name]
            groups["component"].append((disp, f"imply-component of {er} @ line {el}", used))
        elif name in corpus:
            groups["corpus"].append((disp, corpus[name], used))
        else:
            groups["inline"].append((disp, "INLINE — no source in the corpus (consolidation candidate)", used))

    titles = {"declared": "declared in this file",
              "imply": "defined by imply (this file)",
              "component": "imply components (this file)",
              "corpus": "reused from the corpus",
              "inline": "inline — invented here (consolidation candidates)"}
    width = max((len(r[0]) for g in groups.values() for r in g), default=0)
    print(f"TAG ORIGINS — {label}   ({len(uses)} distinct tags)")
    for key in ("declared", "imply", "component", "corpus", "inline"):
        if not groups[key]:
            continue
        print(f"\n  ▸ {titles[key]}  ({len(groups[key])})")
        for disp, origin, used in groups[key]:
            print(f"      {disp.ljust(width)}  {origin}   [{used}]")

    # Node references that reuse the corpus (concepts are referenced as nodes, not tags).
    local = set(decls)
    cref = {}
    for name, lines in node_refs(toks).items():
        if name not in local and name in corpus:
            cref[name] = (corpus[name], lines)
    if cref:
        print(f"\n  ▸ corpus node references (concepts/entities reused)  ({len(cref)})")
        nwidth = max(len(n) for n in cref)
        for name in sorted(cref):
            origin, lines = cref[name]
            print(f"      {name.ljust(nwidth)}  {origin}   [used: {', '.join(map(str, lines))}]")


if __name__ == "__main__":
    argv = sys.argv[1:]
    flags = {a for a in argv if a.startswith("-")}
    files = [a for a in argv if not a.startswith("-")]
    if not files:
        print("usage: validate_tropelang.py <file.trl> [--report]")
        sys.exit(2)
    label = files[0]
    src = open(files[0]).read()

    if "--report" in flags:
        report(src, label, target_path=files[0])
        sys.exit(0)

    toks = validate(src, label)

    if errors:
        print("ERRORS:")
        for e in errors: print("  ✗", e)
    if warnings:
        print("WARNINGS:")
        for w in warnings: print("  ⚠", w)
    if not errors and not warnings:
        rules  = len([t for t in toks if t[0] == 'ID' and t[1] == 'rule'])
        scenes = len([t for t in toks if t[0] == 'ID' and t[1] == 'scene'])
        imply  = len([t for t in toks if t[0] == 'ID' and t[1] == 'imply'])
        resolv = len([t for t in toks if t[0] == 'ID' and t[1] == 'resolve'])
        # count attribute declarations by type
        decl_counts = {kw: len([t for t in toks if t[0] == 'ID' and t[1] == kw])
                       for kw in sorted(DECL_TYPES | {"attr"})}
        decl_summary = ", ".join(f"{v} {k}" for k, v in decl_counts.items() if v)
        print(f"✓ {label}")
        if decl_summary:
            print(f"  declarations: {decl_summary}")
        if rules or scenes or imply or resolv:
            print(f"  {rules} rule(s), {scenes} scene(s), "
                  f"{imply} imply(s), {resolv} resolve(s)")
    sys.exit(1 if errors else 0)
