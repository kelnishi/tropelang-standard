# Changelog

All notable changes to the **TropeLang Standard Corpus**. Format follows
[Keep a Changelog](https://keepachangelog.com/); each version is the corpus `version` in
`trl/tropes/corpus.toml`, published immutably as `corpus-v<version>`.

**Adding an entry** — every PR that changes `trl/tropes/**` appends one line per trope under
`## [Unreleased]`, generated from the trope's preamble:

```
- **<TropeName>** (<category>) — <source>
```

Use **Added** for new tropes, **Changed** for re-foundings/edits, **Removed** for strikes. At release the
maintainer moves `[Unreleased]` under a new `## [x.y.z] — <date>` heading and tags `corpus-v<x.y.z>`.
(The published GitHub Release also gets an auto-generated add/remove diff vs the previous version.)

## [Unreleased]

### Changed
- **Prelude kinship lattice + divine parentage** (TIER 6 / TIER 17, prelude `@version 1.13`) — extend
  the threading pattern to the rest of the kin lattice and to myth, all single parameterized `imply`s:
  - Kinship (→ conservative bases, no blood-parentage claimed where there is none): Nephew/Niece (→
    `Kin_Of` + gender), Cousin (→ `Kin_Of`, ungendered), the six in-laws (→ `Kin_Of` + gender),
    Godfather/Godmother and Stepfather/Stepmother (→ `Guardian_Of` + gender), Stepson/Stepdaughter (→
    `Ward_Of` + gender), Stepbrother/Stepsister (→ `Kin_Of` + gender). +17 relations.
  - Mythological: Demigod_Of (→ `Child_Of` + `Divine` + `Mortal_Born`), Scion_Of (→ `Descendant_Of` +
    `Divine`), Avatar_Of (→ `Emanation_Of` + `Divine`). +3 relations. The divine entity threads into the
    base relation; the holder is stamped divine. (Heracles, Perseus, an avatar of a god, …)
  - Exercises the renamed-slot thread form (`Guardian_Of(ward=godchild)`, `Descendant_Of(anc=ancestor)`,
    `Emanation_Of(source=deity)`) where a base relation's param name differs from the head param.
- **Prelude gendered kinship** (TIER 6) — Father/Mother, Son/Daughter, Brother/Sister, Husband/Wife,
  Grandfather/Grandmother, Uncle/Aunt: each one parameterized `imply` (threading) that refines its base
  relation (the bound `other`/`child`/… flows through) and tags the holder's gender
  (`Masculine`/`Feminine`). Replaces a derivation rule per refinement. **Requires engine ≥ 0.4.1**
  (`engine_min` bumped; prelude `@version 1.12`).

### Fixed
- Self-recognition (§4b): anchored 5 `bonds` tropes' recognition on an EVENT role so they confirm their
  own vignette — `found_family` (Accepts), `love_triangle` / `star_crossed_lovers` / `unrequited_love`
  (Loves), `sibling_rivalry` (Challenged). Replaced `unrequited_love`'s closed-world `not([~Loves])`
  with positive evidence (the beloved loves a third + the lover shown `[+Pining]`), which also removed an
  over-match on `star_crossed_lovers`. Per review: `found_family` now models **acceptance + recognition**
  (mutual `[@Bonded_To]` + an `Accepts` event, not mere protection), and `sibling_rivalry` keeps the
  **bidirectional** kin+rival bond (both siblings) alongside the event anchor. Corpus self-recognition
  **147 → 152/194 (76% → 78%)**.

### Changed
- Founded `verb Accepts(other)` (taking another in as one's own — belonging) in `prelude.trl` (→ **1.11**),
  for found-family-style bonds where acceptance, not protection, is the defining act.
- Founded the remaining unfounded tail in `prelude.trl` (→ **1.10**): props `Betrayer`, `Leader`,
  `Sympathetic`, `TrueRescue`, `RealPerson`, `Pass`, `Field`, `City`; states `Triumphant`, `Refused`,
  `Reluctant`, `Corrupted`, `CrossedTheHorizon`, `Status_Numb`; verbs `Recalls`, `Predicts`, `Atones`.
  Resolves ~35 more inline-invented refs across the arc, conflict, epistemic, non-fiction & character
  tropes (corpus inline total now 204, down from 291 at the start of the drive-down). What remains is the
  ambiguous pair `Plain`/`Faithful` (double meanings, left inline) plus a tail of genuinely one-off
  flavor tags. No trope changed; selfcheck steady at 147/194.
- Founded the diegetic / narration / narrative-role vocabulary in `prelude.trl` (→ **1.9**): props
  `Narrator`, `Spectator`, `Canon`, `RealEvent`, `Detective`, `Invincible`, `Oppressive`, `Vehicle`,
  `Treacherous(toward)`, `Family(with)`; relations `Bonded_To`/`Sundered_From`; verb `Wakes`. Resolves
  ~32 previously inline-invented refs across the diegetic, non-fiction, epistemic, and bonds tropes. No
  trope changed; selfcheck steady at 147/194.
- Founded the Chekhov's-Gun planting/payoff vocabulary in `prelude.trl` (→ **1.8**): `Payoff(item)`,
  `Introduces`, `Uses`, `Fired`, `Pivotal`, `Mundane`, `Endgame`. Resolves ~20 previously inline-invented
  refs across the `chekhovs_*` family and `foreshadowing`/`the_reveal`/`karma_houdini`. No trope changed;
  selfcheck steady at 147/194.

## [1.7.1] — 2026-06-06

### Added
- **The Drifter** (Character Tropes) — https://allthetropes.org/wiki/The_Drifter
- **The Sales Pitch** (Oratory / Persuasion) — https://en.wikipedia.org/wiki/Sales_pitch
- **Mercy Kill** (Death Tropes) — https://allthetropes.org/wiki/Mercy_Kill

## [1.7.0] — 2026-06-06
### Added
- Initial published corpus — **191 tropes** across the character, conflict, epistemic, structure,
  rhetoric, and relationship domains, plus the prelude, ontology, concept library, and modules.
- Founded the reused trope super-types as prelude TIER-0 `attr`s (the founding sweep).
- Public-domain dedication (**CC0-1.0**); served at `https://corpus.tropelang.com`.
