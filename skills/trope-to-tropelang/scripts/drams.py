#!/usr/bin/env python3
"""
drams — the trope-coverage metric, reported as `density over coverage` (e.g. 1.85 over 90).

  density  D — trope-touches per fact, shown as a MULTIPLE (depth; unbounded — a rich
               database reads each beat through several tropes, so it climbs past 1.0)
  coverage C — % of a story's facts explained by >=1 database trope (breadth; <= 100%)

A story is a set of facts (here: tag-applications) in its .trl encoding — the story
described in isolation. Each database trope that matches explains the facts it binds — the
overlay. This tool computes the cheap PROXY (the exact metric runs the S3 evaluation engine): a fact
is "touched" by a trope when the trope's PATTERN — its `imply` expansion + abstract rule —
  references any concept in the fact's IMPLY CLOSURE (so a [+Heir_of_Isildur] fact is covered by
  a trope about Royalty, not only by exact-tag echoes),
NOT its concrete vignette — references that fact's tag. (Excluding the vignette stops a
same-world example from inflating coverage by coincidence.) The uncovered facts are the
GAP — the prioritized worklist of tropes still to convert.

The database is the imply-defined tropes in trl/modules + trl/tropes (the overlay), NOT the
prelude/concepts (the base vocabulary a story is written in).

Usage:
  python3 drams.py <story.trl>            # density over coverage + the gap
  python3 drams.py <story.trl> --json
See specs/00_Architecture_Overview.md §6.7.
"""

import sys, os, json, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_tropelang import lex, tag_usages, imply_decls


def _match(toks, i, opn, cls):
    depth = 0
    while i < len(toks):
        v = toks[i][1]
        if v == opn:
            depth += 1
        elif v == cls:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(toks) - 1


def pattern_tags(toks):
    """The tags that define a trope's PATTERN — its `imply` (LHS + components) and the tags
    inside its abstract `rule` blocks. The concrete vignette (top-level cast + scene facts)
    is EXCLUDED, so coverage reflects what a trope structurally explains, not what story its
    example happens to borrow vocabulary from."""
    tags = set()
    for lhs, _, comps in imply_decls(toks):
        tags.add(lhs)
        tags.update(comps)
    i = 0
    while i < len(toks):
        if toks[i][0] == 'ID' and toks[i][1] == 'rule':
            j = i + 1
            while j < len(toks) and toks[j][1] != '{':
                j += 1
            if j < len(toks):
                end = _match(toks, j, '{', '}')
                tags |= set(tag_usages(toks[j:end + 1]))
                i = end + 1
                continue
        i += 1
    return tags


def corpus_root(start):
    """Locate the trl/ corpus root from a story that may live outside it (e.g. examples/)."""
    d = os.path.dirname(os.path.abspath(start))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, 'prelude.trl')):
            return d
        if os.path.isdir(os.path.join(d, 'trl', 'tropes')):
            return os.path.join(d, 'trl')
        d = os.path.dirname(d)
    return None


def trope_db(root, exclude_abs):
    """tag -> set of trope titles whose source references it (the overlay vocabulary)."""
    tag_to_tropes = {}
    for sub in ('modules', 'tropes'):
        for f in sorted(glob.glob(os.path.join(root, sub, '*.trl'))):
            if os.path.abspath(f) == exclude_abs or os.path.basename(f) == 'index.trl':
                continue
            toks = lex(open(f).read(), f)
            titles = [lhs for lhs, _, _ in imply_decls(toks)]
            if not titles:
                continue
            for tag in pattern_tags(toks):     # pattern only — the vignette is excluded
                tag_to_tropes.setdefault(tag, set()).update(titles)
    return tag_to_tropes


# Generic structural tags that should NOT, on their own, grant coverage — almost every trope's
# `imply` ends in one, so crediting them would make everything trivially "covered".
GENERIC = {"Narrative", "Structure", "Abstract", "Kind"}


def imply_map(root, story_toks):
    """tag -> the tags it implies (its components), pooled from every `imply` in the corpus AND
    the story. Lets a story fact be expanded along its archetype chain so coverage credits
    CONCEPTUAL explanation — a `[+Heir_of_Isildur]` fact, which implies `[Royalty, Destined]`, is
    explained by a trope about Royalty — not only exact-tag echoes."""
    imap = {}
    def add(toks):
        for lhs, _, comps in imply_decls(toks):
            imap.setdefault(lhs, set()).update(comps)
    if root:
        for sub in ('modules', 'tropes'):
            for f in sorted(glob.glob(os.path.join(root, sub, '*.trl'))):
                if os.path.basename(f) == 'index.trl':
                    continue
                add(lex(open(f).read(), f))
    add(story_toks)
    return imap


def closure(tag, imap):
    seen, stack = set(), [tag]
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        stack.extend(imap.get(t, ()))
    return seen


def measure(path):
    toks = lex(open(path).read(), path)
    root = corpus_root(path)
    db = trope_db(root, os.path.abspath(path)) if root else {}
    all_titles = {t for s in db.values() for t in s}
    imap = imply_map(root, toks)            # for conceptual (imply-closure) coverage

    facts = covered = touches = 0
    gap = {}
    for tag, info in tag_usages(toks).items():
        n = len(info['lines'])              # ~ applications of this tag
        # a fact is explained if ANY concept in its imply-closure is referenced by a trope
        touching = set()
        for ct in closure(tag, imap):
            if ct not in GENERIC:
                touching |= db.get(ct, set())
        t = len(touching)                   # distinct database tropes that explain it
        facts += n
        touches += t * n
        if t:
            covered += n
        else:
            gap[tag] = n
    C = covered / facts if facts else 0.0
    D = touches / facts if facts else 0.0
    return {
        "file": path, "facts": facts, "covered": covered,
        "coverage": C, "density": D, "db_tropes": len(all_titles),
        "gap": dict(sorted(gap.items(), key=lambda kv: -kv[1])),
    }


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("-")]
    if not files:
        print("usage: drams.py <story.trl> [--json]")
        sys.exit(2)
    r = measure(files[0])
    if as_json:
        print(json.dumps(r, indent=2))
        return
    if r["db_tropes"] == 0:
        print(f"drams — {r['file']}: no trope database found "
              "(run from within the repo so the corpus is discoverable).")
        return
    print(f"drams — {r['file']}")
    print(f"  {r['density']:.2f} over {round(r['coverage']*100)}   (density ×, coverage %)")
    print(f"  {r['facts']} facts | {r['covered']} covered | database: {r['db_tropes']} tropes")
    if r["gap"]:
        top = list(r["gap"].items())[:18]
        shown = ", ".join(f"{t}({n})" for t, n in top)
        more = "" if len(r["gap"]) <= 18 else f"  (+{len(r['gap'])-18} more)"
        print(f"  gap — uncovered facts (conversion worklist): {shown}{more}")


if __name__ == "__main__":
    main()
