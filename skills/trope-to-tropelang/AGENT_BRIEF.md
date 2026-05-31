# Conversion agent brief

You convert **one** trope into a self-contained `trl/tropes/<name>.trl` file. The coordinator
integrates it (registry, promotion, commit). Read `SKILL.md` first — this is the operational checklist.

## Task
1. **Source** the assigned trope from allthetropes.org via **WebSearch** (never tvtropes; WebFetch 403s
   here). Pull the laconic, setup (→`when:`), payoff (→`then:`), participants, subversions.
2. **Find the module(s) it rides.** A trope RECOGNIZES an instance of a dynamic some `trl/modules/*.trl`
   already SIMULATES (emotion, needs, persuasion, action_dynamics, power, reputation, prophecy,
   common_knowledge, the frameworks…). `import` them and USE their vocabulary. Do NOT declare new
   `concept`/`verb`/`state` — that's a module's job (a trope that does is in the wrong register).
3. **Draft** the file: full preamble (`@trope/@category/@source/@domain/@version 1.3` + laconic),
   imports, `assoc` lateral links, `imply Title -> [...]`, the recognition `rule`, and a CONCRETE
   VIGNETTE from a real story. Vary story/medium/era/stakes — do not reuse a franchise already common
   in the corpus (check existing vignettes; e.g. avoid stacking LotR).
4. **DRY.** Reuse existing corpus tags/concepts rather than reinvent. Run
   `python3 skills/trope-to-tropelang/scripts/corpus_reuse.py <file>` and consolidate genuine duplicates
   (keep distinct specificity).
5. **Self-check — both must pass:**
   - `bash skills/trope-to-tropelang/scripts/gate.sh <file>` → `── GATE PASS ──`
   - **Sim the rule AD HOC — do NOT edit `tools/sim.py`** (shared file; parallel agents collide). Run an
     inline check that loads your trope's own rule file and a minimal scenario, e.g.:
     ```bash
     python3 - <<'PY'
     import sys,os; sys.path.insert(0,'tools'); import sim
     r=sim.load_rules('trl/tropes/<name>.trl')           # + any module it rides
     sim.simulate(r, sim.parse_scenario("""<minimal char + beat scenario>"""), "<name>")
     PY
     ```
     Confirm the rule fires and produces the claimed facts; fix the rule if it misfires (the sim is the
     truth test). The coordinator decides whether to persist a permanent scenario.

## Hard rules
- **Write exactly ONE new file: `trl/tropes/<name>.trl`.** Do NOT edit `index.trl`, `tools/sim.py`,
  or any other shared file — parallel agents must not collide. The coordinator runs `tools/regen_index.py`.
- A trope is **log register** and MUST round-trip (`cargo run --quiet --example fidelity -- <file>` → `ok`).
- Don't use `: "label"` on a tag statement — labels are only for edges (`a -> b : "x"`). Use `//` comments.
- **Stop and return WITHOUT finishing** (flag it to the coordinator) if: the trope needs a NEW module
  (a new simulated dynamic); it changes category/register; or its semantics don't fit the grammar.
  Module design and category jumps are coordinator calls.

## Return
The new file path + 3 lines: which module(s) it rides, the gate/sim result, its drams line, and any
stop-and-surface flag. Keep the file; the coordinator commits.
