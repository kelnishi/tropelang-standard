---
name: trope-to-tropelang
description: Converts narrative tropes from allthetropes.org, tvtropes.org, or plain-text descriptions into valid TropeLang structured text (current grammar; prelude v1.5) for LLM training data generation. Use this skill whenever the user asks to ingest, scrape, convert, or encode a trope into TropeLang format, or wants to generate TropeLang training examples from narrative descriptions. Also use it when the user gives a trope name and asks for a structured or code representation of it.
---

# Trope → TropeLang Converter

Converts a narrative trope into a canonical `.trl` file — a self-contained training example for a small LLM that will predict narrative outcomes and generate scenes.

The philosophy: every entity and beat is distilled to its symbolic bones. Identifiers are the canonical names. Human-readable display forms are annotations, not first-class syntax. A `.trl` file should read like Tamarian — compressed, referential, carrying the weight of the whole story in a few symbols.

Read `references/grammar.md` for full syntax. Read `references/examples.md` for worked examples at increasing complexity.

---

## Architecture & hardened agent rules (READ FIRST)

The corpus is a two-layer model; a converting agent must respect both.

- **Systems = modules** (`trl/modules/*.trl`) — each SIMULATES a dynamic via forward-chaining `rule`
  blocks (emotion, needs, persuasion, action_dynamics, the storytelling frameworks). Modules DECLARE
  vocabulary (`concept` / `verb` / `state`).
- **Tropes = riders** (`trl/tropes/*.trl`) — each RECOGNIZES an instance: an `imply Title -> [...]`,
  a recognition `rule`, and a concrete VIGNETTE. A trope IMPORTS the module(s) it rides and USES
  their vocabulary; it does NOT declare new `concept`/`verb`/`state`.

**Two registers** (why a "round-trip" can legitimately differ):
- **Log register** — entities, edges, tags, scenes, `imply`, `rule`, `assoc`. Round-trips
  byte-for-byte in the Rust reference. **Tropes live here and MUST round-trip.**
- **Library register** — `concept`/`verb`/`state`/`attr` declarations. Validator-only; does NOT
  round-trip in Rust by design. **Modules live here.** If a *trope* lands in library register, that's
  a smell: move the declared vocabulary into a module and `import` it.

**The acceptance gate — every file must pass before you return it:**
```bash
bash skills/trope-to-tropelang/scripts/gate.sh <file.trl>     # must print "── GATE PASS ──"
```
Checks preamble completeness (`@trope/@category/@source/@domain`), validator (no errors), round-trip
(`cargo run --quiet --example fidelity -- <file>` → `ok` for tropes), DRY, drams.

**Sim-test any recognition rule.** Forward-chain it on a concrete scenario and confirm it fires as
the prose claims — the sim has caught real logic bugs (self-vengeance; a coup deposing itself; a
two-phase arc collapsing into one). Run it AD HOC (load the rule file + a minimal scenario inline); do NOT edit the shared `tools/sim.py`.

**Never edit the registry.** `trl/tropes/index.trl` is rebuilt deterministically. Write ONE
self-contained trope file; do NOT touch `index.trl` (parallel agents collide on it). The coordinator
runs `cargo run --quiet --example assemble -- trl/tropes/corpus.toml` to regenerate imports and mint the concept entry — so carry full
preamble metadata, including `@domain` — the registry domain LABEL (one of those in use: `Narrative Mind Interpersonal Epistemic Political Social Psychological`; match the nearest cluster, e.g. relationships -> Interpersonal).

**Sourcing.** `https://allthetropes.org/wiki/<Trope>` via **WebSearch** — direct WebFetch 403s here,
so rely on the search cache. **Never tvtropes.org** (bot-blocked; respect it). Record the wiki URL in
`@source`.

**drams is a TROPE-overlay metric; frameworks are SCAFFOLDS.** A structural framework (a sequence of
steps/functions) gets only PRIVATE base implies — never imply its steps onto popular archetypes
(Mentor, Conflict, Reveal) to chase coverage; that pollutes the density of EVERY story using those
archetypes. After a module change, re-run drams on an UNRELATED eval (`examples/olympic_biopic.trl`)
and confirm it did not move. (Memory: `drams-framework-scaffold-rule`.)

**Stop and surface to the coordinator** when: changing category or register; the trope's
semantics/metaphor break down in the grammar; or the conversion would need a NEW module (a new
simulated dynamic) — module design is a judgment call, not autonomous.

**Variety.** Vary story / medium / era AND scale of stakes across vignettes; never stack one
franchise (a toy's bedroom and a sundered nation are equally valid). Memory: `trope-example-variety`.

---

## Workflow

### 1. Acquire the trope

Source from **allthetropes.org** via **WebSearch** (`<Trope> trope <facets> allthetropes`, optionally
`allowed_domains:["allthetropes.org"]`). Direct WebFetch 403s from this environment, so the search
result snippets / cache are the reliable channel. **Never tvtropes.org** — it is bot-blocked and we
respect that. Record the wiki URL in `@source`. Extract:
- **Laconic definition** — one-line summary at the top or in a "Laconic" subpage
- **Setup** — preconditions; what must already be true (→ the `when:`)
- **Payoff** — what the trope produces when it fires (→ the `then:`)
- **Participants** — character roles, objects, locations, events in the pattern
- **Subversions/inversions** — alternate resolutions (feeds `fork`/`prompt` branches)

If search is unreachable, fall back to general narrative knowledge, but say so.

### 2. Map trope mechanics to TropeLang primitives

| Trope concept | TropeLang construct |
|---|---|
| Character role | `char $x [+Archetype]` |
| Object with narrative function | `obj $item [+MacGuffin]` |
| Triggering event | `evt $e -> $agent > $target : "Label"` |
| Location / setting | `set $place [+Interior] [+Night]` |
| Narrative arc | `arc $a` |
| Must be true | condition in `when:` |
| Must NOT be true | `not(...)` in `when:` |
| Effect / result | mutation in `then:` |
| Temporal structure | `beat N { }` / `scene name { }` |
| Player choice | `prompt(...)` or `fork(...)` |
| Counting occurrences | `count(...) >= N` |
| Historical state | `past scene $s { }` |
| Ontological cluster | `imply TropeName -> [Tag1, Tag2]` |
| Numeric attribute (HP, AC, score) | `stat Name [+Group]`; on an entity `$e [^Stat(cur=…, max=…)]` |
| Threshold trigger | comparison in `when:` — `char $c [^Stat <= N]` |
| Dice roll / check | concrete logged event — `evt $e [&Rolled(dice="…", result=N)]` / `[&Check(stat="…", outcome="…")]` |

### 3. Structure the output file

A `.trl` file has four sections in order:

```
// === PREAMBLE ===
// @trope    TropeName
// @category <Category, from the wiki>
// @source   https://allthetropes.org/wiki/TropeName
// @domain   Narrative          @domain is a bare label: Narrative|Mind|Interpersonal|Epistemic|Political|Social|Psychological (no trailing comment)
// @version  1.3
//
// Laconic (per the wiki): <one-line definition>. FRONTIER: <what new capability it adds, if any>.

// === IMPORTS & ASSOCIATIONS ===
// import the module(s) this trope rides; assoc for lateral links

// === ONTOLOGY ===
// (imply Title -> [...]  — private/archetype components)

// === ABSTRACT RULE ===
// (the recognition rule — sim-test it)

// === CONCRETE VIGNETTE: <Story Title> (medium, era) ===
// (entity declarations + scene/beat instantiation; vary story/medium/era/stakes)
```

**The cast & locations section is a symbol table.** Each entity gets a `//` annotation on the line above it carrying its screenplay display form. Identifiers are short and symbolic; the annotation is what a renderer uses for human output:

```
// JIMMY FONG
char jimmy [+Protagonist] [+Skilled]

// INT. GOLDEN PALACE RESTAURANT - NIGHT
set golden_palace [+Interior] [+Night]

// THE BRIEFCASE
obj briefcase [+MacGuffin]
```

For entities with many tags, use a multi-line TagMut immediately below the declaration — this is the current idiom until block form is added to the grammar:

```
// DETECTIVE MILLS
char mills [+Antagonist] [+Authority]
mills [+Path_Corruption] [+Compromised]
mills [+MotivatedBy(reason="Ambition")]
```

**Scene blocks stay flat.** Entities are declared at top level and only referenced inside scenes. This keeps nesting depth bounded:

```
scene standoff {
  beat 1 {
    jimmy @ golden_palace
    mills @ golden_palace
    jimmy > briefcase
    mills -- jimmy : "Suspects"
  }
}
```

**For `set` entities**, encode the screenplay header components as tags:
- `[+Interior]` or `[+Exterior]`
- `[+Night]`, `[+Day]`, `[+Dawn]`, `[+Dusk]`
- Additional atmosphere: `[+Raining]`, `[+Crowded]`, etc.

The `//` annotation carries the human form (`INT. LOCATION - TIME`); the tags carry the machine-readable form. Both are present.

### 4. Generate both the abstract rule and a concrete vignette

**Abstract rule** — captures the trope pattern for matching:
```
rule TropeName {
  when:
    // pattern with $variables
  then:
    // mutations, surface calls
}
```

**Concrete vignette** — shows the trope instantiated in a specific story:
```
// --- concrete: [Story Title] ---
// (entity declarations specific to this instance)

scene scene_name {
  beat 1 { ... }
  beat 2 { ... }
}
```

If the trope has a meaningful subversion, add `rule TropeName_Subverted` or use `fork`/`prompt` to branch the outcome.

**Vary the source story and format.** Across conversions, draw vignettes from a *variety* of stories, media, and eras — film, TV, novel, play, myth, game, comic — and do not lean on one franchise (e.g. several LotR examples in a row). Prefer an example that also sharpens the trope's nuance (a villain-protagonist for The Protagonist, a *non-villain* antagonist for The Antagonist). A monoculture of examples narrows the corpus and skews the drams eval set.

**Capture the connective detail in code, not the laconic.** As much of the trope's errata as the source gives — what it imparts, risks, catalyzes, pairs with — should be *code*, so evaluators and embeddings can follow real connections (the laconic is for human readers only). Use the right construct:
- **`imply`** for hierarchy (the tag's broader components — normative, matched).
- **edges** (`--` `->` `@` `><`) for concrete story-graph relationships (normative, matched).
- **`assoc Subject -> [target : "relation", …]`** for lateral thematic links (optional, redundancy-allowed metadata; *not* matched — for discovery/embeddings). e.g. `assoc mentor -> [wisdom : "imparts", death : "occupational hazard"]`.
- **`import "file"`** to make a dependency on another file's nodes explicit in code, not a `@uses` comment.

TropeLang is not strictly hierarchical — bidirectional/lateral links are encouraged. See `the_mentor.trl` as the worked example.

### 5. Format the output

Return a `.trl` fenced code block with a brief annotation:

```
**[TropeName]** — [laconic definition]

Modeling notes: [1–3 sentences on key choices]

\```trl
[output]
\```
```

---

## Corpus reuse & consolidation (DRY)

A conversion should reuse what the corpus already defines, not reinvent it. The denser the
corpus, the more overlapping narratives can later be collapsed onto shared elements. After
drafting, run the reuse assist and consolidate.

**See where every tag comes from:**
```bash
cargo run --quiet --example report -- <file>.trl
```
Resolves each tag across the whole corpus (prelude + concepts + modules + tropes) into:
declared here / defined by imply / **reused from the corpus** / **inline — invented here**.
The inline group is the consolidation worklist. Concepts are referenced as *nodes*, so the
report's "corpus node references" section is where concept reuse shows up.

**Get reuse candidates for the inline tags:**
```bash
cargo run --quiet --example report -- <file>.trl --reuse          # deterministic name shortlist
cargo run --quiet --example report -- <file>.trl --reuse --json   # inline tags + corpus vocab, for an agent
```
Name-matching is precision-only — it misses meaning (`[+Imperiled]`, `[&OffersEscape]`).
Hand the `--json` task to an agent for meaning-level matches.

**Consolidation rules** — how the agent (and the author) decide each inline element:
- **DRY only if absolutely the same.** Consolidate to a corpus element only when they mean
  the *same thing*. A loose association is not enough.
- **Convert flavor.** A word that is *primarily flavor* for an existing plain meaning →
  reuse the corpus element. (e.g. inline `[+FalseDawn]` → prelude `[+Deceptive]`.)
- **Keep different specificity.** If the inline element sits at a *different level of
  specificity*, keep it. (e.g. `[+Inferno]` is more specific than `[+Dangerous]`; `[+Saved]`
  ≠ socio-political `[+Liberated]`.) Never consolidate away meaning.
- **Titles get their own entries.** A trope's title and the proper nouns from the source
  (works, characters, places) may warrant their own declarations / `imply`, so later
  references can be **rehydrated** — resolved back to the full element they name.

Inlining an existing element is not illegal, but consolidate it when it's absolutely the
same. Reuse is the default; invention is for what the corpus genuinely lacks.

### Promotion to the core library

Consolidation is *local* (reuse what already exists). Promotion is *global* — moving an
element INTO the shared corpus so every future trope reuses it. As tropes accumulate, take
the time to review what has earned promotion:

- A **tag or concept that recurs across multiple tropes**, or is a fundamental primitive,
  → promote to `trl/prelude.trl` (the core). Bump the prelude's `@version` — it's a core
  capability change. (e.g. `attr Trope` was promoted once a trope category existed.)
- A **trope title** → give it a canonical entry in `trl/tropes/index.trl` (reusing an
  existing concept if one matches its meaning), so references **rehydrate** to its
  definition + provenance. Source proper-nouns (works, characters) can get the same
  treatment when they need to be referenced across tropes.
- Don't promote on thin evidence (a single use). Promote when the reuse is real and the
  element is genuinely shared vocabulary — otherwise leave it local.

## Naming conventions

- **Identifiers**: short, lowercase, `snake_case` — `jimmy`, `golden_palace`, `the_briefcase`. These are the Tamarian proper nouns; keep them lean.
- **`//` annotations**: screenplay display form — `JIMMY FONG`, `INT. GOLDEN PALACE - NIGHT`, `THE BRIEFCASE`. No quotes needed in the comment.
- **Rule names**: `PascalCase` — `MacGuffinDelivery`, `HeelFaceTurn`, `ChekhovsGun_Fired`
- **Variables**: `$camelCase` or `$snake_case` — `$hero`, `$magic_item`
- **Tags**: `+PascalCase` — archetypes, states, paths, plot functions (see `references/grammar.md`)
- **Edge labels**: short plain-English strings — `"Trusts"`, `"Draws Weapon"`, `"Hands Off"`
- **`unique: true`**: use when the trope fires at most once globally

**Do not use sidecar labels** — the current grammar allows `char luke "Luke Skywalker"` but this format demotes that string to a `//` annotation. Identifiers are canonical; display strings are annotations only.

---

## Quality checklist

- Every `$variable` in `then:` was bound in `when:`
- No sidecar labels (`char name "Label"` form is banned)
- Every top-level entity has a `//` annotation above it
- `set` entities have `[+Interior]`/`[+Exterior]` and time-of-day tags
- Tags: `[+Name]` — modifier immediately before name, no space
- Params: `key=value` inside parens — `[+Fear(target="Snakes")]`
- Scene blocks contain only flat references and edges, no multi-line TagMuts
- No fractional numbers in identifiers — use `[+Mod(factor=0.5)]`
- String literals always double-quoted
- `imply` used when the trope introduces an ontological cluster

---

## Grammar notes (current limitations)

Two features discussed in the format design are **not yet in the grammar**:

- **`##` doc-comments**: The lexer only supports `//`. Use `//` for all annotations now. `##` is the planned future syntax that will make annotations a distinct token the parser can associate with the following declaration.
- **Entity block form** (`char luke { [+TheHero] }`): Not yet supported — `{` after a non-scope entity type is a parse error. Use a TagMut on the following line(s) instead.

Both are pending grammar updates to lib.rs.

---

## Self-validation

After generating output, save it and run the acceptance gate — it bundles the checks below and must
print `── GATE PASS ──`:

```bash
bash skills/trope-to-tropelang/scripts/gate.sh output.trl   # the gate (preamble/validate/round-trip/DRY/drams)
cargo run --quiet --example report -- output.trl   # tag origins (reuse vs inline) — DRY worklist
cargo run --quiet --example fidelity -- output.trl          # round-trip alone (ok | library-register | FAIL)
```

Checks: balanced braces, tag syntax, no fractional identifiers, `when:`/`then:` in every
rule, no sidecar labels, and reference existence/type (param values must name a declared
node; `event=`/`site=` must match entity type). Then consolidate (see above).

---

## Reference files

- `references/grammar.md` — complete syntax reference (✓ = in the Rust parser, ◎ = validator-only)
- `references/examples.md` — worked trope mappings
- `examples/validate.rs` (`cargo run --example validate`) — structural validator (Rust reference / LSP backend)
- `examples/report.rs` (`cargo run --example report [-- --reuse [--json]]`) — tag origins + consolidation assist
- `scripts/dialog_context.py` — interrogates `dialog(...)` annotations (preconditions / motivations / postconditions / context)
- `cargo run --example drams -- <file>` — the exact (S3) coverage metric, `density over coverage` (specs/00 §6.7); a SIGNAL not a gate; the gap list is the conversion worklist
