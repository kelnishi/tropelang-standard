#!/usr/bin/env python3
"""
Corpus reuse / consolidation assist.

For a target .trl, isolate the elements it invented INLINE (tags + node references with
no source anywhere in the corpus) and propose existing corpus elements they could be
consolidated to. DRY: every element a story can reuse instead of reinventing makes the
corpus easier to build on — and lets later systems collapse overlapping narratives.

Two layers:
  • deterministic shortlist — name-similarity matches (case-fold / substring / token
    overlap). Cheap, high-precision, but blind to meaning.
  • agent hand-off — `--json` emits the inline elements + the corpus vocabulary as a task
    an LLM agent can run to find SEMANTIC equivalents the name match misses
    (e.g. inline [+Imperiled] ~ concept `dread` / prelude [#Afraid]).

Usage:
  python3 corpus_reuse.py <file.trl>            # human-readable suggestions
  python3 corpus_reuse.py <file.trl> --json     # assist task for an agent
"""

import sys, os, json, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_tropelang import (
    lex, tag_usages, node_refs, declarations_with_lines, imply_decls,
    build_corpus_index, _RESERVED,
)


def tokens_of(name):
    """Split a tag/concept name into lowercase word tokens (snake_case + CamelCase)."""
    parts = re.split(r'[_\s]+', name)
    words = []
    for p in parts:
        words += re.findall(r'[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+', p) or [p]
    return [w.lower() for w in words if w]


def similarity(a, b):
    """Cheap name similarity in [0,1]: exact-fold, containment, or token Jaccard."""
    la, lb = a.lower(), b.lower()
    if la == lb:
        return 1.0
    if la in lb or lb in la:
        return 0.85
    ta, tb = set(tokens_of(a)), set(tokens_of(b))
    if ta and tb and (ta & tb):
        return len(ta & tb) / len(ta | tb)
    return 0.0


def inline_elements(path):
    """(inline_tags, corpus) — tags used here that have no source anywhere in the corpus
    (and aren't defined locally or by an imply). These are the consolidation candidates."""
    toks = lex(open(path).read(), path)
    local = set(declarations_with_lines(toks))
    implied = {lhs for lhs, _, _ in imply_decls(toks)}
    for _, _, comps in imply_decls(toks):
        implied.update(comps)
    corpus = build_corpus_index(path)
    tags = sorted(n for n in tag_usages(toks)
                  if n not in local and n not in implied and n not in corpus)
    return tags, corpus


def shortlist(name, corpus, k=3):
    """Top-k corpus names by similarity (>0), as (corpus_name, source, score)."""
    scored = [(cn, corpus[cn], similarity(name, cn)) for cn in corpus]
    scored = [s for s in scored if s[2] > 0.0]
    scored.sort(key=lambda s: -s[2])
    return scored[:k]


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("-")]
    if not files:
        print("usage: corpus_reuse.py <file.trl> [--json]")
        sys.exit(2)
    path = files[0]
    tags, corpus = inline_elements(path)

    if as_json:
        # An assist task for an agent: find semantic equivalents the name match missed.
        print(json.dumps({
            "file": path,
            "inline_tags": tags,
            "instruction": ("For each inline tag, name the closest existing corpus element "
                            "it could be consolidated to (or null if none fits). Prefer "
                            "prelude states/props for condition tags, and concept nodes "
                            "for things a character feels/seeks. Return {inline: corpus|null}."),
            "corpus_vocabulary": corpus,
        }, indent=2))
        return

    print(f"CONSOLIDATION ASSIST — {path}")
    print(f"  {len(tags)} inline tag(s); corpus vocabulary: {len(corpus)} elements\n")
    if not tags:
        print("  nothing inline — fully consolidated against the corpus.")
        return
    print("  ▸ inline tags (name-similarity shortlist; precision-only)")
    for name in tags:
        cands = shortlist(name, corpus)
        if cands:
            hint = "; ".join(f"{cn} ({src.split(' in ')[0]}, {score:.2f})"
                             for cn, src, score in cands)
            print(f"      {name:22} ~ {hint}")
        else:
            print(f"      {name:22}   no name match — needs a semantic pass")
    print("\n  Name match misses meaning. For semantic equivalents, hand off to an agent:")
    print(f"      python3 {os.path.basename(__file__)} {path} --json   # -> agent")


if __name__ == "__main__":
    main()
