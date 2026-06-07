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

### Fixed
- Self-recognition (§4b): event-anchored the last 4 `bonds` tropes so they confirm their own vignette,
  completing the arena (all 9) — `power_of_friendship` (Aids), `i_gave_my_word` (Honors),
  `conflicting_loyalty` (Commands), `like_brother_and_sister` (Aided + positive `[+Family(with)]`,
  dropping the closed-world `not()` spine). Corpus self-recognition **152 → 156/194 (78% → 80%)**.
  (Redo of the closed #26 on the v0.4.1 engine; recall still rides an event, with imply param threading
  generalizing the relation/role coverage.)
## [1.7.3] — 2026-06-07

### Changed
- **Prelude collective-agent ontology** (TIER 5/16, prelude `@version 1.16`) — wire the already-ratified
  collective vocabulary into a hierarchy: `imply Faction -> [Collective]`, `imply Institution -> [Collective]`,
  and a new `prop Nation` → `[Collective, Authority]` (the "what is a country" case). So a rule keyed on the
  broad `[+Collective]` now recognizes any `[+Faction]`/`[+Institution]`/`[+Nation]` entity (recognition
  coverage honors the imply on **engine ≥ 0.4.2**; parses fine on 0.4.1, so `engine_min` is unchanged).
  `Nation` only; `Movement`/`Organization` left unfounded until a trope reaches for them (promotion model).
  `[+Authority]` stays orthogonal (an individual holds it too). No trope changed; selfcheck steady 152/194.
- **STYLE §1 — "Choosing the entity kind"** — new guidance: pick `char`/`set`/`obj`/`concept` by what the
  entity *does* (agency / membership / inertness / idea). Organizations, factions, and countries are a
  `char` carrying `[+Collective]`/`[+Faction]`/`[+Nation]` — never a new entity kind (composition over
  classification). "What is a country?" → choose the facet (`char [+Nation]` / `set` / `concept`), mirroring
  the `realm: char|set|concept` typing.

## [1.7.2] — 2026-06-06

### Changed
- **Prelude opposition/alliance valence** (TIER 7, prelude `@version 1.15`) — sharpened-bond relations now
  thread the counterparty into the weaker base relation AND stamp the affective charge: `Adversary_Of`,
  `Enemy_Of`, `Nemesis_Of` → `[Rival_Of(other), Hostile]`; `Ally_Of` → `[Friendly]`. +2 relations
  (`Enemy_Of`, `Nemesis_Of`), +2 valence props (`Hostile`, `Friendly`). The three hostile relations are
  connotation-distinct author-facing names that normalize to the same core (a generic `Rival_Of` rule
  fires off any of them); a bare `[+Hostile]`/`[+Friendly]` still works when the counterparty is unnamed.
  `Adversary_Of` (previously a bare base, unused in the corpus) gains the imply with no behavior change.
  **Requires engine ≥ 0.4.1.**
- **Prelude royalty & rank** (TIER 16, prelude `@version 1.14`) — promote sovereign/noble rank from flat
  monadic props to **relations over a realm**, the threading pattern applied to governance. New base
  relations `Rules(realm)` and `Heir_To(realm)` bridge to the monadic standing (`Rules ⟹ [+Ruler]`,
  `Heir_To ⟹ [+Heir]`), so a generic ruler/heir rule fires off any rank. Rank relations thread the realm
  into the base relation and stamp standing + gender: King/Queen, Emperor/Empress, Lord/Lady, Duke/Duchess
  (→ `Rules` + `Royalty`/`Noble` + gender) and Prince/Princess (→ `Heir_To` + `Royalty` + gender — royal by
  birth, not ruling). +12 relations, +2 props (`Ruler`, `Noble`; founds the heavily-used inline `[+Ruler]`).
  `realm` is `char|set|concept` (a territory, a personified throne/empire, or an abstract polity/cause). A
  bare `[+Ruler] [+Royalty]` still works when the realm is unnamed (the corpus default, incl. collective
  rulers). **Requires engine ≥ 0.4.1.**
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
