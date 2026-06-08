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

### Added
- **The Wizard** (Character Archetypes) — https://allthetropes.org/wiki/Wizard_Classic
  (The Tempest, Prospero — the wielder of arcane power, distinct from the Mentor by the casting itself.
  Founds the genre seed-vocabulary it reaches for, locally per the promotion model: `prop Arcane` and
  `verb Casts(spell)`.)
- **Love Dodecahedron** (Relationships / Romance) — https://allthetropes.org/wiki/Love_Dodecahedron
  (A Midsummer Night's Dream — the four-heart chain that does not close; strictly more tangled than the
  Love Triangle, with the four-distinct constraint enforced at recognition on engine ≥ 0.4.3). Corpus
  **194 → 196 tropes**; self-recognition steady at **196/196 (100%)**.
- **An Aesop** (Morality / Audience Reactions) — https://allthetropes.org/wiki/An_Aesop
  (Aesop's "The Tortoise and the Hare" — the author frames the tale's events `as=moral` and the audience
  is EDIFIED; a rhetoric-layer payoff distinct from Tear Jerker's pathos. Founds `prop Lesson` and
  `state Edified` locally per the promotion model.)
- **Big Good** (Relationships / Cast) — https://allthetropes.org/wiki/Big_Good
  (Transformers, Optimus Prime vs. Megatron — the bright mirror of the Big Bad; the `[+Leader]` who
  `[&Opposes]` the `[+Mastermind]`, the leadership discriminator parting it from a plain brave hero.)
- **Villain Protagonist** (Character Roles / Villains) — https://allthetropes.org/wiki/Villain_Protagonist
  (Macbeth — the story's `[+Central]` driver who commits genuine villainy; the conjunction on one
  character, distinct from the rough Anti-Hero. Founds `prop Villainous` locally.)
- **Five-Man Band** (Cast / Ensemble) — https://allthetropes.org/wiki/Category:Five-Man_Band
  (Gatchaman / G-Force — the first ENSEMBLE-structure trope: recognition rides the co-presence of five
  distinct complementary roles bound to one mission, with ten distinctness clauses enforced at
  recognition on engine ≥ 0.4.3. Founds the cast vocabulary `prop Ensemble`/`SmartGuy`/`BigGuy`/`TheChick`.)
  Corpus **196 → 200 tropes**; self-recognition steady at **200/200 (100%)**.
- **Status Quo Is God** (Narrative Devices) — https://allthetropes.org/wiki/Status_Quo_Is_God
  (Seinfeld, "no hugging, no learning" — the author imposes a return to the [+Baseline] premise, the Snap
  Back, so nothing carries over. Founds `prop Baseline` + `state Restored`.)
- **Failure Is the Only Option** (Narrative Devices) — https://allthetropes.org/wiki/Failure_Is_the_Only_Option
  (Wile E. Coyote vs. the Road Runner — the hero pursues a [+SeriesGoal] the author denies for the
  premise's sake; the win that can never land. Founds `prop SeriesGoal` + `state Thwarted`.)
- **Idiot Ball** (Plotting Devices) — https://allthetropes.org/wiki/Idiot_Ball
  (Prometheus, the biologist petting the alien — a [+Clever] character handed a plot-driven `[&Blunders]`
  lapse; recognized by the competence/foolishness contrast. Founds `prop Clever` + `verb Blunders`.)
- **Take a Third Option** (Plotting Devices) — https://allthetropes.org/wiki/Take_a_Third_Option
  (Kirk and the Kobayashi Maru — the hero `[&Rejected]` the [+Binary] dilemma itself and `[&Forges]` an
  unorthodox third way; the rejection binds the fork on an event role so the discriminator can't float
  free. Founds `prop Binary` + `verb Forges(option)`.)
  Corpus **200 → 204 tropes**; self-recognition steady at **204/204 (100%)**.
- **Character Development** (Characterization Tropes / Mechanics of Writing) — https://allthetropes.org/wiki/Character_Development
  (Pride and Prejudice, Elizabeth Bennet — the UMBRELLA transformation trope: a [+Dynamic] character
  `[&Changes]` by experience. The contrastive [+Dynamic] discriminator keeps the umbrella distinct from
  its axis-specific instances (Coming of Age / Took a Level in Badass / Redemption), which tag
  [+Innocent]/[+Weak] instead — verified non-over-firing both ways. Founds `prop Dynamic` + `verb Changes`.)
- **Title Drop** (Title Tropes) — https://allthetropes.org/wiki/Title_Drop
  (A Streetcar Named Desire, Blanche DuBois — a character `[&Utters]` a [+Titular] phrase that is the
  work's own title; the title bound on the event role parts it from any other charged line. Founds
  `prop Titular` + `verb Utters(phrase)`.)
- **Genre Savvy** (Metafiction / Genre Awareness) — https://allthetropes.org/wiki/Genre_Savvy
  (Scream, Randy's rules — a [+GenreLiterate] character `[&Anticipates]` a [+Convention], genre-sourced
  foreknowledge; distinct from Breaking the Fourth Wall (no audience address) and Dramatic Irony (here
  the character knows). Founds `prop GenreLiterate`/`prop Convention` + `verb Anticipates(convention)`.)
  Corpus **204 → 207 tropes**; self-recognition steady at **207/207 (100%)**.
- **Damsel in Distress** (Characters As Device / Love Interests) — https://allthetropes.org/wiki/Damsel_in_Distress
  (Perseus and Andromeda — a [+Captive] [+Helpless] character is the TARGET of a `[&Rescues]`; the
  distress tags bound on the rescue's target part it from the rescuer-side tropes (Big Damn Heroes /
  The Cavalry recognize the arrival) and from a rescue of an able ally. Founds `prop Captive`/`prop
  Helpless` + `verb Rescues(target)`.)
- **Red Shirt** (Death Tropes / Cast Filler) — https://allthetropes.org/wiki/Red_Shirt
  (Star Trek's landing party — an [+Expendable] nobody `[&Slays]`-ed to prove the menace; expendability
  bound on the victim parts it from every significant-death trope (loved one / willing hero / main).
  Founds `prop Expendable`/`prop Lethal`.)
- **Deadpan Snarker** (Character Archetypes / Character Flaw Index) — https://allthetropes.org/wiki/Deadpan_Snarker
  (The Big Sleep, Philip Marlowe — a [+Sardonic] character `[&Quips]` a deflating wisecrack; the standing
  temperament anchored on the act of snarking (cf. Title Drop's act-by-utterance) parts it from a
  villain's Motive Rant / Breaking Speech. Founds `prop Sardonic` + `verb Quips(at)`.)
  Corpus **207 → 210 tropes**; self-recognition steady at **210/210 (100%)**.

### Fixed
- Self-recognition (§4b): event-anchored the last 4 `bonds` tropes so they confirm their own vignette,
  completing the arena (all 9) — `power_of_friendship` (Aids), `i_gave_my_word` (Honors),
  `conflicting_loyalty` (Commands), `like_brother_and_sister` (Aided + positive `[+Family(with)]`,
  dropping the closed-world `not()` spine). Corpus self-recognition **152 → 156/194 (78% → 80%)**.
  (Redo of the closed #26 on the v0.4.1 engine; recall still rides an event, with imply param threading
  generalizing the relation/role coverage.)
- Self-recognition (§4b): event-anchored recall + literal phase-2 coverage (STYLE §8) carried the
  remaining arenas — character roles, conflict, epistemic, death, power, structure — to full coverage:
  corpus self-recognition **156 → 194/194 (80% → 100%)** on the v0.4.2 engine. Each trope re-founded
  below now recalls and confirms its own vignette. Pattern: anchor the rule on a narrative `[&Verb]`
  event that names an `agent` (recall keys on the agent), and assert the discriminating tags literally
  where the vignette prose already states them (coverage re-checks literally, not via derivation).
  Incidental fixes: de-duplicated the `FaceHeelTurn` rule (it had been defined in both `face_heel_turn`
  and `heel_face_turn`); promoted `verb Forsakes` to the prelude (`ontology/verb_classes.trl` already
  classed it Betray); named the `agent` on `Reveals`/`Strikes` where a rule keyed on them; fixed
  scene/event name collisions (`the_edict`, `the_struggle`). Precision: tightened `Finishing_Move` to
  the combination finisher (now requires the ally's `[&Pins]` setup, per its own title/laconic),
  clearing its ≥0.9 co-fires on solo-kill vignettes (David Versus Goliath, Achilles' Heel, Combat
  Pragmatist: **1.00 → 0.50**). The `Pincer_Attack` over-fire — a recognition-time gap where `$x != $z`
  was honored at eval but not at shape recall — is resolved by **engine cli-v0.4.3**, which enforces
  binding-inequality at recognition: its ≥0.9 co-fires on single-attacker vignettes (David Versus
  Goliath, Achilles' Heel, Combat Pragmatist, Determinator, You Shall Not Pass, Last Stand, Zerg Rush)
  are gone, while it still self-confirms its own two-attacker vignette and selfcheck holds 194/194. Any
  remaining ≥0.9 overlaps are defensible kindred tropes (foil/gambit, lancer/sidekick, trap/feint,
  redemption/sacrifice, last-stand/you-shall-not-pass).

### Changed
- **The Protagonist** (Universal Tropes) — https://allthetropes.org/wiki/The_Protagonist
- **The Antagonist** (Universal Tropes) — https://allthetropes.org/wiki/The_Antagonist
- **The Deuteragonist** (Universal Tropes) — https://allthetropes.org/wiki/Deuteragonist
- **The Mentor** (Universal Tropes) — https://allthetropes.org/wiki/Mentors
- **The Sidekick** (Relationships / Cast) — https://allthetropes.org/wiki/Sidekick
- **The Big Bad** (Relationships / Cast) — https://allthetropes.org/wiki/Big_Bad
- **The Love Interest** (Relationships / Romance) — https://allthetropes.org/wiki/Love_Interest
- **The Everyman** (Cast / Character) — https://allthetropes.org/wiki/Everyman
- **The Paragon** (Cast / Character) — https://allthetropes.org/wiki/The_Paragon
- **The Foil** (Characterization / Relationships) — https://allthetropes.org/wiki/Foil
- **The Lancer** (Characterization / Relationships) — https://allthetropes.org/wiki/The_Lancer
- **The Trickster** (Character Archetypes) — https://allthetropes.org/wiki/The_Trickster
- **Determinator** (Heroic Spirit / Willpower) — https://allthetropes.org/wiki/Determinator
- **Achilles' Heel** (Combat Tropes) — https://allthetropes.org/wiki/Achilles%27_Heel
- **David Versus Goliath** (Combat Tropes) — https://allthetropes.org/wiki/David_Versus_Goliath
- **Finishing Move (Combination Finisher)** (Combat / Action) — https://allthetropes.org/wiki/Finishing_Move
- **Heroic Second Wind** (Heroic Spirit / Comeback) — https://allthetropes.org/wiki/Heroic_Second_Wind
- **The Duel (Duel to the Death · Affair of Honor)** (Social / Conflict) — https://allthetropes.org/wiki/Duel_to_the_Death
- **Combat Pragmatist (Dirty Fighting · Anti-Honor Fighter)** (Conflict / Tactics) — https://allthetropes.org/wiki/Combat_Pragmatist
- **Feint (Defensive Feint Trap)** (Conflict / Tactics) — https://allthetropes.org/wiki/Defensive_Feint_Trap
- **Pyrrhic Victory** (Conflict / Tactics) — https://allthetropes.org/wiki/Pyrrhic_Victory
- **The Trap (Lured into a Trap)** (Conflict / Tactics) — https://allthetropes.org/wiki/Lured_into_a_Trap
- **Decapitated Army** (Military and Warfare) — https://allthetropes.org/wiki/Decapitated_Army
- **Dramatic Irony** (Epistemic / Narrative Devices) — https://allthetropes.org/wiki/Dramatic_Irony
- **Hidden Identity (Secret Identity)** (Identity / Epistemic) — https://allthetropes.org/wiki/Secret_Identity
- **Open Secret** (Epistemic / Social) — https://allthetropes.org/wiki/Open_Secret
- **The Mole** (Spy Fiction / Betrayal) — https://allthetropes.org/wiki/The_Mole
- **Defiant to the End** (Characterization / Death) — https://allthetropes.org/wiki/Defiant_to_the_End
- **Redemption Equals Death** (Death Tropes) — https://allthetropes.org/wiki/Redemption_Equals_Death
- **Together in Death** (Death Tropes) — https://allthetropes.org/wiki/Together_in_Death
- **Full-Circle Revolution** (Political / Power) — https://allthetropes.org/wiki/Full-Circle_Revolution
- **Smear Campaign (Malicious Slander)** (Social / Reputation) — https://allthetropes.org/wiki/Malicious_Slander
- **Cliffhanger** (Rhetoric / Suspense) — https://allthetropes.org/wiki/Cliff_Hanger
- **Conflict** (Omnipresent Tropes) — https://allthetropes.org/wiki/Conflict
- **MacGuffin** (Plot Devices) — https://allthetropes.org/wiki/MacGuffin
- **The Climax** (Story Structure) — https://allthetropes.org/wiki/Climax
- **Three-Act Structure** (Universal Tropes) — https://allthetropes.org/wiki/Three_Act_Structure
- **Face Heel Turn** (Character Development / Alignment) — https://allthetropes.org/wiki/Face_Heel_Turn
- **Heel Face Turn** (Character Development / Alignment) — https://allthetropes.org/wiki/Heel_Face_Turn
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
