---
name: trope-to-tropelang
description: Converts narrative tropes from allthetropes.org, tvtropes.org, or plain-text descriptions into valid TropeLang v1.1 structured text for LLM training data generation. Use this skill whenever the user asks to ingest, scrape, convert, or encode a trope into TropeLang format, or wants to generate TropeLang training examples from narrative descriptions. Also use it when the user gives a trope name and asks for a structured or code representation of it.
---

# Trope → TropeLang Converter

Converts a narrative trope into a canonical `.trl` file — a self-contained training example for a small LLM that will predict narrative outcomes and generate scenes.

The philosophy: every entity and beat is distilled to its symbolic bones. Identifiers are the canonical names. Human-readable display forms are annotations, not first-class syntax. A `.trl` file should read like Tamarian — compressed, referential, carrying the weight of the whole story in a few symbols.

Read `references/grammar.md` for full syntax. Read `references/examples.md` for worked examples at increasing complexity.

---

## Workflow

### 1. Acquire the trope

Fetch raw wikitext — cleaner than JS-rendered HTML:

| Source | URL pattern |
|---|---|
| allthetropes.org | `https://allthetropes.org/wiki/<TropeName>?action=raw` |
| tvtropes.org | `https://tvtropes.org/pmwiki/pmwiki.php/Main/<TropeName>` |

`?action=raw` returns plain MediaWiki markup with no JS dependency. Extract:
- **Laconic definition** — one-line summary at the top or in a "Laconic" subpage
- **Setup** — preconditions; what must already be true
- **Payoff** — what the trope produces when it fires
- **Participants** — character roles, objects, locations, events in the pattern
- **Subversions/inversions** — alternate resolutions (feeds `fork`/`prompt` branches)

If the domain is unreachable, fall back to general narrative knowledge.

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

### 3. Structure the output file

A `.trl` file has four sections in order:

```
// === PREAMBLE ===
// @trope   TropeName
// @source  https://...
// @version 1.1

// === CAST & LOCATIONS ===
// (top-level entity declarations with // annotations)

// === ONTOLOGY ===
// (imply statements)

// === RULES & SCENES ===
// (rule blocks, then scene/beat vignettes)
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
python3 scripts/validate_tropelang.py <file>.trl --report
```
Resolves each tag across the whole corpus (prelude + concepts + modules + tropes) into:
declared here / defined by imply / **reused from the corpus** / **inline — invented here**.
The inline group is the consolidation worklist. Concepts are referenced as *nodes*, so the
report's "corpus node references" section is where concept reuse shows up.

**Get reuse candidates for the inline tags:**
```bash
python3 scripts/corpus_reuse.py <file>.trl          # deterministic name shortlist
python3 scripts/corpus_reuse.py <file>.trl --json   # inline tags + corpus vocab, for an agent
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

After generating output, save it and run:

```bash
python3 scripts/validate_tropelang.py output.trl            # validate
python3 scripts/validate_tropelang.py output.trl --report   # tag origins (reuse vs inline)
```

Checks: balanced braces, tag syntax, no fractional identifiers, `when:`/`then:` in every
rule, no sidecar labels, and reference existence/type (param values must name a declared
node; `event=`/`site=` must match entity type). Then consolidate (see above).

---

## Reference files

- `references/grammar.md` — complete syntax reference (✓ = in the Rust parser, ◎ = validator-only)
- `references/examples.md` — worked trope mappings
- `scripts/validate_tropelang.py` — structural validator + `--report` tag-origin mode (Python 3, no deps)
- `scripts/corpus_reuse.py` — consolidation assist: inline tags + corpus vocab, `--json` for an agent
- `scripts/dialog_context.py` — interrogates `dialog(...)` annotations (preconditions / motivations / postconditions / context)
