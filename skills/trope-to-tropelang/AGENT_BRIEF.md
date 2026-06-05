# Conversion agent brief

You convert **one** trope into a self-contained `.trl` file under a **functional bucket**:
`trl/tropes/<bucket>/<name>.trl` (e.g. `conflict/tactics/`, `arc/fall/`, `epistemic/reveal/`). The
coordinator tells you the bucket when assigning the trope, and integrates it (registry, promotion,
commit). If no bucket was given, pick the closest one from `trl/tropes/README.md` and flag your choice.
Read `SKILL.md` first — this is the operational checklist.

## Task
0. **Check it doesn't already exist.** Before creating, `grep -rE "imply (The)?<Name>" trl/tropes` for
   **both** article forms (and obvious synonyms). The definite article is meaning-bearing (`TheX` ≠ `X`
   in general — S13 §6.1), so a broken `[+Siege]` does NOT prove there's no `TheSiege`. If a match
   exists, reconcile with a deliberate `alias` (or extend it) — do NOT mint a duplicate.
1. **Source** the assigned trope from allthetropes.org via **WebSearch** (never tvtropes; WebFetch 403s
   here). Pull the laconic, setup (→`when:`), payoff (→`then:`), participants, subversions.
2. **Find the module(s) it rides.** A trope RECOGNIZES an instance of a dynamic some `trl/modules/*.trl`
   already SIMULATES (emotion, needs, persuasion, action_dynamics, power, reputation, prophecy,
   common_knowledge, the frameworks…). `import` them and USE their vocabulary. Do NOT declare new
   `concept`/`verb`/`state` — that's a module's job (a trope that does is in the wrong register).
3. **Draft** the file: full preamble (`@trope/@category/@source/@domain/@version 1.3` + laconic),
   imports, `assoc` lateral links, `imply Title -> [...]`, the recognition `rule`, and a CONCRETE
   VIGNETTE from a real story. Tie the trope's DISCRIMINATOR (what sets it apart from its family) to an
   EVENT role so recognition binds it, and have the vignette's bound entity overtly carry the tag the
   rule checks — SKILL.md §4b (otherwise it over-fires on every cousin). Vary story/medium/era/stakes —
   do not reuse a franchise already common in the corpus (check existing vignettes; e.g. avoid stacking
   LotR). Follow **`STYLE.md`** —
   especially: **(§1) declare the vignette cast ahead of use** (char/obj/set/evt in a block before the
   scenes), and **(§8) the vignette TRIGGERS the rule, it does not hardcode its conclusions** — assert
   only the `when` trigger facts and let the engine DERIVE the `then` outputs. Hand-asserting an output
   (`$x [+TheTrope]`, a `[+Resolved]`/`[+Pivotal]`) makes the example look right while the rule never
   fires — and often *blocks* it (a `not(Resolved)` clause fails).
4. **DRY.** Reuse existing corpus tags/concepts rather than reinvent. Run
   `cargo run --quiet --example report -- <file> --reuse` and consolidate genuine duplicates
   (keep distinct specificity).
5. **Self-check — both must pass:**
   - `bash skills/trope-to-tropelang/scripts/gate.sh <file>` → `── GATE PASS ──`
   - **The recognition must FIRE on your vignette under the real engine:**
     `cargo run --quiet --example eval -- trl/tropes/<bucket>/<name>.trl` → your rule appears under "rules fired"
     and its outputs under "derived facts" (NOT hand-asserted in the vignette). If it doesn't fire, the
     vignette isn't triggering the rule — fix the triggers, don't paper over it by asserting the output.
   - **The recognition must be SPECIFIC, not just fire** (SKILL.md §4b):
     `cargo run --quiet --example shape -- trl/tropes/<bucket>/<name>.trl --why` → your trope confirms, and
     its distinguishing tag shows as a satisfied COVERAGE line on the bound entity. The discriminator that
     separates this trope from its family must ride an EVENT role (`subject=`/`to=`/`agent=`/`target=`) so it
     binds — a distinguishing tag on an unbound var is invisible and the trope over-fires on every cousin at
     1.00. If your trope has siblings (reveals, betrayals, recognitions), confirm a sibling's vignette does
     NOT confirm yours at 1.00.
   - **Sim the rule AD HOC — do NOT edit `tools/sim.py`** (shared file; parallel agents collide). Run an
     inline check that loads your trope's own rule file and a minimal scenario, e.g.:
     ```bash
     python3 - <<'PY'
     import sys,os; sys.path.insert(0,'tools'); import sim
     r=sim.load_rules('trl/tropes/<bucket>/<name>.trl')  # + any module it rides
     sim.simulate(r, sim.parse_scenario("""<minimal char + beat scenario>"""), "<name>")
     PY
     ```
     Confirm the rule fires and produces the claimed facts; fix the rule if it misfires (the sim is the
     truth test). The coordinator decides whether to persist a permanent scenario.

## Hard rules
- **Write exactly ONE new file: `trl/tropes/<bucket>/<name>.trl`.** Do NOT edit `index.trl`, `tools/sim.py`,
  or any other shared file — parallel agents must not collide. The coordinator runs the corpus assembler
  (`cargo run --quiet --example assemble -- trl/tropes/corpus.toml`).
- A trope is **log register** and MUST round-trip (`cargo run --quiet --example fidelity -- <file>` → `ok`).
- Don't use `: "label"` on a tag statement — labels are only for edges (`a -> b : "x"`). Use `//` comments.
- **Stop and return WITHOUT finishing** (flag it to the coordinator) if: the trope needs a NEW module
  (a new simulated dynamic); it changes category/register; or its semantics don't fit the grammar.
  Module design and category jumps are coordinator calls.

## Return
The new file path + 3 lines: which module(s) it rides, the gate/sim result, its drams line, and any
stop-and-surface flag. Keep the file; the coordinator commits.
