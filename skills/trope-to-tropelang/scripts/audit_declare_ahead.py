#!/usr/bin/env python3
"""Audit .trl files for declare-ahead violations (STYLE.md §1).

Two severities:
  SEVERE   — an entity is referenced inside a scene/beat/act (the temporal log) before it is
             declared. This is the the_forgery case: a thing springs into being mid-story, never
             introduced. These should always be fixed (declare it up front, plant it as a seed).
  ADVISORY — an entity is referenced in the SETUP block (before any scene) before its own
             declaration line — typically a character's relationship tag naming a sibling/object
             declared a few lines below. Benign (the setup block is read as a unit), but tidier to
             declare bare entities first, then assert cross-referencing relationships (STYLE §4).

Usage:  python3 audit_declare_ahead.py [path ...]      (default: trl/tropes/*.trl + narratives/*.trl)
"""
import re, glob, sys

DECL  = re.compile(r'^\s*(char|obj|set|evt|arc|concept)\s+([a-z_]\w*)')
SCENE = re.compile(r'^\s*(scene|beat|act)\b.*\{')

def strip(line):
    return re.sub(r'"[^"]*"', '', line.split('//', 1)[0])

def audit(path):
    lines = open(path).read().splitlines()
    depth_at, depth = [], 0
    for l in lines:
        depth_at.append(depth)
        s = l.strip()
        if SCENE.match(l):       depth += 1
        elif s == '}' and depth: depth -= 1
    decls = {}
    for i, l in enumerate(lines, 1):
        m = DECL.match(l)
        if m and m.group(2) not in decls:
            decls[m.group(2)] = i
    severe, advisory = [], []
    for name, dline in decls.items():
        for i in range(dline - 1):
            if re.search(r'(?<![\w$])' + re.escape(name) + r'\b', strip(lines[i])):
                (severe if depth_at[i] > 0 else advisory).append((name, i + 1, dline))
                break
    return severe, advisory

def main(argv):
    paths = argv or sorted(glob.glob('trl/tropes/*.trl')) + sorted(glob.glob('narratives/*.trl'))
    nsev = nadv = 0
    for f in paths:
        if f.endswith('index.trl'):
            continue
        sev, adv = audit(f)
        nsev += len(sev); nadv += len(adv)
        if sev:
            print(f"  SEVERE   {f.split('/')[-1]}: " +
                  ", ".join(f"{n} (used@{r} in a scene, declared@{d})" for n, r, d in sev))
        if adv:
            print(f"  advisory {f.split('/')[-1]}: " +
                  ", ".join(f"{n} ({r}->{d})" for n, r, d in adv))
    print(f"\n  {nsev} severe (temporal-log), {nadv} advisory (intra-setup-block)")
    return 1 if nsev else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
