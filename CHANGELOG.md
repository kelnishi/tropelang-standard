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
