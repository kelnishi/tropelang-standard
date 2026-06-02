# TropeLang Authoring Style Guide

Best practices for writing `.trl` — narratives, trope vignettes, modules. The grammar (`specs/01`)
tells you what is *legal*; this guide tells you what is *good*.

**The governing idea: a TropeLang file is an accretive log.** Like the game log it mirrors, it grows by
accumulation — entities and facts are laid down and never deleted, only reinterpreted (the soft-state,
never-delete store; `specs/04`, `specs/14 §6`). Write to that grain.

---

## 1. Front-load the cast — declare every entity ahead of use

Declare every entity — `char` / `obj` / `set` / `evt` / `arc` / `concept` — in a block at the **top of
the file**, before the temporal log that uses it. A reference that appears before its declaration is a
paper cut for the parser, for the validator (which flags undeclared referents), and for the reader.

**The firm rule:** nothing in the temporal log (a `scene` / `beat` / `act`) may name an entity not yet
declared. An entity that springs into being mid-story — used in a beat, never introduced — is the
defect this guide exists to kill. Even an entity the story only *points at* from the future belongs up
front: a foreshadowing omen's `[&Foreshadows(event=the_fall)]`, a Chekhov's gun, a planted twist —
declare the referent at the top (a bare `evt the_fall`) and let it *occur* later (§3). **The advisory:**
within the setup block itself, prefer to declare a bare entity before any sibling's tag names it
(declare `char polynices` before `antigone [@LoyalTo(faction=polynices)]`) — declarations first, then
the cross-referencing relationships (§4). A forward reference to a sibling *inside* the setup block is a
minor nit, not a defect; the whole block is read as a unit before the timeline begins.

Sweep a file (or the corpus) with `skills/trope-to-tropelang/scripts/audit_declare_ahead.py` — it
separates SEVERE (temporal-log) hits from advisory (intra-setup) ones.

❌ The forgery springs into being mid-swap, never introduced:
```trl
scene the_swap {
  beat 1 {
    evt the_substitution [&Swaps(agent=vale, decoy=the_forgery, real=the_nightingale)]
  }
}
```
✓ Declared with its siblings, up front, so the swap *uses* a thing the reader already met:
```trl
// THE OBJECTS
obj the_nightingale [+MacGuffin] [+Coveted]    // the watched prize
obj the_ledger      [+MacGuffin]               // the real prize
obj the_forgery     [+Counterfeit]             // the decoy that takes the bird's place at the swap
```

## 2. Write accretively — build the palette early, even loosely

Don't declare only what the next beat needs. **Lay out the whole table of pieces before you play.**
Front-load the cast, the objects, the places, the abstractions — generously, even things whose payoff
is far off or still uncertain. This mirrors the game log (which accretes state continuously), and it
pays the author back: a rich, pre-declared palette is a set of tools to reach for as the story turns.
An `obj the_locket` declared in scene one costs nothing and may become the whole third act.

> The cost of an unused declaration is one line. The cost of a *missing* one is a story you have to
> stop and scaffold mid-sentence.

## 3. Move ambiguous → concrete at your own pace

The accretive style's real gift: **you can declare a thing before you know what it means.** Plant it
now, commit later, with the tools the language gives you (`specs/01 §11`):

- **Latent facts** `?…?` — present in the graph, surfaced to no one. Seed the real motive, the hidden
  traitor, the loaded gun at the top — `?vale [~Pursues(goal=justice)]?` — and surface it at the turn.
- **Ambiguity** `*( A | B | … ) as name*` — a fact that is *one of these, or something not yet named*.
  Declare the open question; collapse it when the story decides.
- **`resolve name -> concrete`** — the in-world moment a planted ambiguity becomes fact.

Declare `obj the_box` with no role; let scene four `resolve` it into the murder weapon or the red
herring. Uncertainty is a first-class material — declare it early and sharpen it at your own pace.

## 4. The shape of a file

```trl
// @title / @source / @version …            preamble (comments)
import "trl/modules/index.trl"               imports

<<heist>>                                    home plane (S14), if leveled — the cast lives here

// ===== CAST =====       char declarations, with their standing tags
// ===== OBJECTS / SETS = obj / set declarations (places, things, MacGuffins, decoys)
// ===== ARCS / CONCEPTS  arc declarations; concept references
// ===== SEEDS =========  latent ?…? / ambiguous *(…)* facts planted up front

arc the_score [+Heist]                       the temporal log: arc ▸ act ▸ scene ▸ beat,
act the_mark { scene the_appraisal { … } }   in READING ORDER (it is the timeline)
```
Declarations first, the timeline second. Everything the timeline names already exists above it.

## 5. Naming & tags

- **snake_case** entity ids (`the_salt_gate`, `the_pact`); **CamelCase** tag names (`PendingPayoff`).
- **The definite article is meaning-bearing, not noise.** `hero` (common noun) → `Hero` (concept) →
  `TheHero` (definite archetype) is a three-tier signal, and `The X` is sometimes a distinct concept
  (`TheSublime` ≠ sublime, `TheOther` ≠ other). So `TheX` and `X` are **two symbols** — the resolver
  never strips the article. When they truly are the same trope under two names, link them deliberately
  with `alias TheX -> X`. Before minting a `TheX`/`X` trope, check the corpus for the other form first
  (S13 §6.1).
- **Sigils:** `+` prop · `-` remove · `#` status · `@` rel · `~` intent · `&` event verb · `=`/`%`
  domain facets · and the epistemic *wrappers* `!…!` / `*…*` / `?…?`.
- **Reserved param keys** carry meaning to the engine — use them: `agent`, `target`, `site` (a set),
  `event` (an evt), `as` (an alias). A scene/act/beat is itself a taggable entity (`scene s [+Endgame]`).
- **Reference a concept in lowercase; CamelCase is for tags.** Concepts are lowercase abstract nouns
  (`concept corruption`, `concept honor`). Reference them lowercase *everywhere* — param values
  (`goal=justice`) **and** imply components (`imply DecadentCourt -> [corruption, Power]`). CamelCase
  names are props / states / attrs / roles (`[+Corrupted]`, `[+Protagonist]`, `Power`). A CamelCase
  concept reference (`[… Corruption …]`) will **not** resolve to `concept corruption` — casing is
  meaning-bearing. (Legacy CamelCase concept refs are bridged in `concepts/concept_aliases.trl`; prefer
  the lowercase form in new code.)

### Where a new tag lives — declare it, don't strand it

A name that doesn't resolve reads **broken (red)** in the IDE. That is a signal, not a bug: either the
name belongs in shared vocabulary (declare it) or it is one-off color (leave it). Route it:

- **Universal** — any story could use it (`Pursues`, `Imperiled`, `Vengeful`, `Hurt`): the **prelude**.
- **Domain dynamics** — a system one scale up (siege / heist / reputation / persuasion / …): the
  **module** declares the vocabulary, **and its own rule outputs**. A `[+Overcommitted]` a rule
  *produces* must be a `state Overcommitted` in that module, or it reads broken.
- **Abstract theme** (`corruption`, `atonement`, `tragedy`): the **concepts library**, lowercase.
- **One-off story flavor** (`Blooded`, this host's `Aurochs` totem): leave it **bespoke**. A red tag is
  the honest mark that it is not shared vocabulary — don't promote color to the corpus.
- Before coining, **check it doesn't already exist** — both article forms (`Siege`/`TheSiege`), the
  lowercase concept form (`corruption`). Reuse or `alias` rather than mint a duplicate.

## 6. Epistemic discipline

| Tier | Form | Use it for |
|------|------|------------|
| Absolute | `!S!` | narrator ground truth, immutable — a death, a revealed fact. Use sparingly. |
| Asserted | `S` | the default — what is true on this plane, now. |
| Contingent | `*S*` | true-but-perspective-dependent; collapses under `perspective(observer)`. |
| Latent | `?S?` | present, unsurfaced — the seam `perspective` cuts along. **Plant early, surface late.** |

A `non_canon` plane cannot mint an `!absolute!` fact (`specs/14 §8`).

## 7. Temporal hygiene

- The temporal spine is `scene ▸ beat`; **the beat is the finest unit** (the engine ticks per beat).
- Assert a state in the beat it becomes true; **retract `[-Tag]` in the beat it stops** — the engine
  scopes a tag's interval `[assert, retract)`, so don't pre-net a state to "off" by asserting then
  removing it in the same breath.
- Reading order *is* time: `past scene {}` / `future scene {}` and `as_of` all read the file top-down.

## 8. Vignettes: trigger, don't hardcode

For a trope vignette (a concrete example riding a recognition rule): assert the **trigger facts** the
rule's `when` reads, and let the engine **derive** the recognition's outputs. Hand-asserting a rule's
conclusions (`$x [+TheTrope]`, `$v [+Defeated]`) makes the example *look* right while the rule never
fires — and a hardcoded output can even *block* the rule (a `[+Resolved]` failing a `not(Resolved)`,
a `[+Pivotal]` failing a `not(Pivotal)`). **Show the cause; let the engine prove the effect** — then
`cargo run --example eval -- <file>` shows the recognition firing.

## 9. S14 levels: home plane, loud crossings

- Declare a node on its **home plane** (the cast lives on the canon mainline, e.g. `<<heist>>`).
- Reference a node from another plane via a **loud crossing** `<<home|name>>` — never a bare silent
  reference. A plane change is always visible in the source (`specs/14 §7`).

## 10. Validate

Every file should:
- `gate` clean — preamble ✓, validates ✓, round-trips ✓ (`skills/trope-to-tropelang/scripts/gate.sh`);
- carry no undeclared referents (front-load — §1); and, for a story,
- fire the recognitions it means to (`cargo run --quiet --example eval -- <file>`).

The two master narratives in `narratives/` are the worked references — read them alongside this guide.
