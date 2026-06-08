# TropeLang corpus — map & worklist

What began as a flat "convert core tropes" list is now a **layered model of narrative**: a stack
of systems (modules that *simulate* a dynamic) with tropes riding on top (named patterns that
*recognize* an instance). This doc is the map of what exists and the forward worklist.

**How the work is steered**
- **drams** (`cargo run --quiet --example drams -- <story>`) is the EXACT (S3) metric — a **signal,
  not a requirement** (confidence when it moves, never pass/fail). It runs the engine over a story with
  the full trope overlay and counts which tropes actually **fire** and what encoded facts they bind;
  coverage follows firings, not imply-closure. The gap list is the conversion worklist. Eval targets:
  `examples/aragorn_fotr.trl`, `examples/mythbusters_water_heater.trl`. (The old `drams.py` proxy is retired.)
- **sim** (`tools/sim.py <scenario>`) forward-chains the real rule blocks — every system is run,
  not just written; it has caught real bugs (self-vengeance, the coup self-deposing, prepotency).
- **Sourcing**: definitions from allthetropes.org (the `source=` field); WebFetch 403s on the
  datacenter IP, so the search cache is used. Never TVTropes.
- **Variety**: vary story / medium / era **and the scale of stakes** — a toy's bedroom and a
  sundered nation are equally valid (see `[[trope-example-variety]]`). An over-epic vignette set is
  itself a gap.

**Legend:** `[x]` done · `[~]` partial (lives in a module/imply) · `[ ]` todo.

---

## Corpus metrics & self-recognition audit (2026-06 — re-measure before acting)

Snapshot at **204 tropes** (re-measure declaration counts before acting; the self-recognition drive added `verb Forsakes` to the prelude, `the_wizard` founds `prop Arcane` + `verb Casts` locally, and the `convert/high-profile-gaps` branch founds — all locally — `prop Lesson`/`state Edified` (an_aesop), `prop Villainous` (villain_protagonist), `prop Ensemble`/`SmartGuy`/`BigGuy`/`TheChick` (five_man_band), `prop Baseline`/`state Restored` (status_quo_is_god), `prop SeriesGoal`/`state Thwarted` (failure_is_the_only_option), `prop Clever`/`verb Blunders` (idiot_ball), and `prop Binary`/`verb Forges` (take_a_third_option)).

- **Founding / unfounded nodes:** inline (unfounded) tags down to **204** (from 291 at the start of the
  drive-down). Only `Plain`/`Faithful` recur (2× each, ambiguous — split before founding); the rest is
  one-off bespoke flavor. **Founding is effectively complete.**
- **drams (per-trope coverage × density):** coverage mean **22%** / median 19%; density mean **0.26×**;
  497 rule firings (mean 2.56/trope); only 2 zero-firing tropes (`dramatic_irony`, `fourth_wall`).
- **Self-recognition (the quality target): `204/204` (100%) — ✅ COMPLETE.** Every trope confirms its
  own vignette (started at 147/194). The §4b discriminator-binding worklist below is DONE — kept for
  provenance. Re-measure: `tropelang selfcheck trl/tropes/corpus.toml --corpus file://trl`.

**§4b worklist — ✅ DONE (provenance).** Recall keeps only `when:` EVENT patterns that name an `agent`;
a rule whose `when:` was pure static tags / `@rel` edges / `count()` (no agent-named `evt … [&Verb]`)
was never recalled → conf 0.00 on its own vignette. Fixed across every arena by anchoring the
discriminator on a narrative event and asserting the discriminating tags literally where the vignette
prose already states them (coverage re-checks literally), without over-firing siblings. Engine bumps
that mattered: **v0.4.2** coverage imply-closure (refined-relation coverage); **v0.4.3** enforces
binding-inequality at recognition (cleared the `Pincer_Attack` over-fire). Precision: `Finishing_Move`
tightened to the combination finisher (`&Pins` setup); remaining kindred overlaps (foil/gambit,
lancer/sidekick, trap/feint, redemption/sacrifice) left as defensible. Structural fixes: de-duplicated
the `FaceHeelTurn` rule, promoted `verb Forsakes` to the prelude, fixed scene/event name collisions.
See CHANGELOG `[Unreleased]` for the per-trope list.

Re-measure self-recognition deterministically:
```sh
tropelang selfcheck trl/tropes/corpus.toml --corpus file://trl     # ratio + count
# per-trope: shape each file, check its own rule name confirms at 1.00 (loop over trl/tropes/**/*.trl)
```

**Failures by arena — ✅ ALL 47 CLEARED** (the snapshot that was, kept for provenance): bonds 9/13 ·
character 13/30 · conflict 10/34 · structure 5/17 · epistemic 4/27 · death 3/15 · power 2/9 · arc 1/22.
- **bonds:** ✅ **DONE — all 9** (event-anchored recall + relation/positive coverage). `found_family`
  (Accepts) · `love_triangle`/`star_crossed_lovers`/`unrequited_love` (Loves) · `sibling_rivalry`
  (Challenged) · `power_of_friendship` (Aids) · `i_gave_my_word` (Honors) · `conflicting_loyalty`
  (Commands) · `like_brother_and_sister` (Aided + positive `[+Family(with)]`).
  NOTE (v0.4.1 imply param threading): recall threads refined relations into their base class
  (`Brother_Of`→`Sibling_Of`), so a rule keyed on the base fires across gendered variants — but the
  phase-2 **coverage re-check is literal**, so a refined-only vignette confirms at ~0.62 (a "relevant"
  Possible) unless it also carries the base tag. This is the lever for the role archetypes next.
- **character roles:** `the_protagonist` `the_antagonist` `the_mentor` `the_foil` `the_lancer`
  `the_sidekick` `the_deuteragonist` `the_everyman` `the_paragon` `the_love_interest` `the_big_bad`
  `the_trickster`(0.81) `determinator`.
- **conflict:** `finishing_move` `feint` `the_trap` `the_duel` `heroic_second_wind` `decapitated_army`
  `achilles_heel`(0.81) `david_versus_goliath`(0.75) `combat_pragmatist`(0.62) `pyrrhic_victory`(0.62).
- **structure/epistemic/death/power/arc:** `cliffhanger` `conflict` `macguffin` `the_climax`
  `three_act_structure` · `dramatic_irony` (**no rule at all** — recognizes nothing) `hidden_identity`
  `open_secret` `the_mole`(0.50) · `defiant_to_the_end` `together_in_death` `redemption_equals_death`(0.75)
  · `full_circle_revolution` `smear_campaign` · `face_heel_turn`.

---

## High-profile coverage (the conversion worklist — updated each PR)

The forward target: convert the **allthetropes high-profile gaps** (Tropes of Legend / Omnipresent /
Universal + the cast & plot-structure indexes). This is the live ledger — **every conversion PR updates
it** (the finalize step in `CONVERSION_BOT.md`). The *recipe* for re-running the review (corpus inventory
vs. the indexes, archive access) lives in `CONVERSION_BOT.md`; the *state* lives here.

**Corpus: 256 tropes · self-recognition 256/256 (100%).** (Re-measure: `tropelang selfcheck
trl/tropes/corpus.toml --corpus file://trl`.)

**Converted batches (done):**
- `convert/high-profile-gaps` (#38) — An Aesop · Big Good · Villain Protagonist · Five-Man Band ·
  Status Quo Is God · Failure Is the Only Option · Idiot Ball · Take a Third Option.
- `convert/character-development-batch` (#42) — Character Development · Title Drop · Genre Savvy.
- `convert/damsel-redshirt-snarker` (#44) — Damsel in Distress · Red Shirt · Deadpan Snarker.
- `convert/quest-villaindeath-wth-hero` (#45) — The Quest · Disney Villain Death · What the Hell, Hero?
- `convert/bondvillain-raceclock-father` (#47) — Bond Villain Stupidity · Race Against the Clock ·
  I Am Your Father.
- `convert/plotcoupon-jbyam-timebomb` (#48) — Plot Coupon · Just Between You and Me · Time Bomb.
- `convert/backfromdead-bigkiss-ace` (#49) — Back from the Dead · The Big Damn Kiss · The Ace.
- `convert/rysspeech-premortem-bittersweet` (#50) — Pre-Mortem One-Liner · The Reason You Suck Speech · Bittersweet Ending.
- `convert/berserkbutton-defeatfriend-boast` (#51) — Berserk Button · Defeat Means Friendship · Badass Boast.
- `convert/seven-villainy-bonds-batch` (#52, 7) — Well-Intentioned Extremist · Sacrificial Lion · Evil Chancellor · Mook · The Man Behind the Man · Fire-Forged Friends · Trash Talk.
- `convert/seven-archetypes-batch` (#53, 7) — Lovable Rogue · Sacrificial Lamb · Downer Ending · Calling Your Attacks · Cooldown Hug · The Purge · Hannibal Lecture.
- `convert/rhetoric-scales-batch` (#54, 7) — **Rhetoric push, scene/act/arc mix**: Armor-Piercing Question · Lampshade Hanging · Aside Glance (scene) · Talking the Monster to Death · Patrick Stewart Speech (act) · Strawman Political · Audience Surrogate (arc).
- `convert/loaded-meaning-batch` (this PR, 7) — **ground-level loaded-meaning tropes** (object/action/behavior gets meaning from legend/religion/anime/chivalry/comedy/myth/ritual): Only the Chosen May Wield · Holy Halo · Tsundere · Throwing Down the Gauntlet · Spit Take · Red String of Fate · Pinky Swear.

**Remaining gaps (archive-verified; the next-batch candidates):**
- [ ] Mood Whiplash · [ ] Idiot Plot · [ ] Crapsack World (each harder to event-anchor —
  tonal/structural/setting; design the discriminator carefully).
- [ ] (re-run the coverage recipe against the live high-profile indexes for fresh candidates — the
  archive dump exposes `/page`, `/search`, `/titles`, `/exists`).
- Smaller leftovers: further Love Triangle variants · "Within a Frame Story" · the cross-repo eval-side
  drams gap (below) · the low-value fantastic-species framing.

**Suggested next batch:** re-run the coverage recipe against the live indexes for a fresh, varied trio.
The remaining logged gaps (Mood Whiplash / Idiot Plot / Crapsack World) each need an event-anchored
discriminator worked out first (tonal/structural/setting), so pair at most one with two clean fresh finds.

---

## Systems (the modules in `trl/modules/`)
Each is a forward-chaining dynamic that tropes ride on.

- **Psychology** — `emotion_dynamics` (appraisal→emotion→motivation→threads) · `motivation_dynamics`
  (desire→pursuit→outcome) · `needs` (Maslow's 8 rungs + **prepotency and its inversion**, scale-
  invariant) · `five_stages_of_grief`
- **Tactics** — `action_dynamics` (conflict & cooperation verbs: strike/guard/exploit/finisher ·
  pin/cover/improvise/bar · feint/ambush/sacrifice · hold/reinforce/riposte)
- **Epistemic** — `prophecy` · `common_knowledge` (mutual↔common) · `theory_of_mind` · `cognitive_biases`
- **Social / political** — `power_dynamics` (coalition·legitimacy·revolution) · `reputation` (status
  as common belief)
- **Rhetoric** — `rhetoric` (the author↔audience layer: framing-dependent appraisal · curiosity gap ·
  **audience investment** · authorial override). Non-fiction = this **minus** override-of-outcome.
- **Oratory / persuasion** — `persuasion` (the speaker↔audience layer: **ethos / logos / pathos** →
  belief-change → call-to-action). Rhetoric cultivates ATTENTION and EMOTION; persuasion goes for
  CONVICTION — moving the room from belief A to belief B, then to action.
- **Storytelling frameworks** — `heros_journey` · `freytags_pyramid` · `story_circle` · `save_the_cat`
  · `booker_seven_plots` · `philosophy`
- **Language feature** — S14 diegetic levels (`specs/14`), implemented in the reference parser.

---

## Open worklist by arena
Done tropes are summarized; **todo** is the actionable list.

### Cast & character roles
Done: Protagonist · Antagonist · Deuteragonist · Hero · Mentor · Sidekick · Foil · Big Bad ·
Paragon · Everyman.
- [x] The Love Interest — `the_love_interest` (Genji)
- [x] The Narrator — `the_narrator` (S14, agent-converted)
- [x] Anti-Hero — `anti_hero` (Man with No Name)
- [x] The Trickster — `the_trickster` (Anansi)
- [x] The Drifter — `the_drifter` (Shane; the rootless [+Stranger] who Protects a town then Departs)

### Character relationships (the dyad/triad)
Done: The Rival · Unrequited Love · Found Family · Enemies to Lovers · Love Triangle ·
Star-Crossed Lovers · Mentor & Student.
- [x] Love Dodecahedron — `love_dodecahedron` (A Midsummer Night's Dream; the open four-heart chain)
- [ ] further Love Triangle variants (Love Pentagon, Triang Relations)
- [x] Sibling Rivalry — `sibling_rivalry` (Mufasa/Scar)  ·  [x] Like Brother and Sister — `like_brother_and_sister`

### Character change & arcs
Done (psychology arena): Heel/Face Turn · Revenge · Despair Event Horizon · Survivor's Guilt.
- [x] Redemption Arc (The Atoner — guilt discharged by costly amends) — `redemption_arc`
- [x] Fall From Grace (Start of Darkness — the two-phase slide) — `fall_from_grace`
- [x] Coming of Age (Bildungsroman — innocence traded for maturity) — `coming_of_age`
- [x] Mercy Kill (the [+Compassion] read of &Slays — a loved one spared a worse end) — `mercy_kill` (Of Mice and Men)

### Identity / worldbuilding (drams-flagged)
Done: Hidden Identity · Rightful King Returns · The Chosen One · Unreliable Narrator.
- [x] Secret Legacy — `secret_legacy` (Percy Jackson)
- [x] the Mage/Wizard — `the_wizard` (Prospero; founds the [+Arcane] + [&Casts] magic seed-vocabulary, locally)
- [~] the Wanderer/Ranger — covered in spirit by `the_drifter` (Shane: [+Stranger] who Protects then Departs)
- [ ] fantastic-species framing (`Hobbit`,`Elf`,`Dunedain` — low general value; consider eval re-encode instead)

### Plot structure & devices
Done: Three-Act · Call to Adventure · Refusal · Foreshadowing · The Reveal · Hope Spot ·
Chekhov's Gun · Red Herring · Cliffhanger · Frame Story.
- [x] Plot Twist · [x] Flashback · [x] In Medias Res — `in_medias_res` · [x] MacGuffin — `macguffin`
- [~] The Climax (concept in `freytags_pyramid`)  ·  [x] The Dilemma — `the_dilemma` (Sophie's Choice)

### Diegetic-level devices (S14)
Done: Frame Story · Dream Sequence · Fourth Wall · Dream Within a Dream · Show Within a Show ·
Or Was It a Dream? · Unreliable Narrator.
- [x] Reality Bleed — `reality_bleed` (the §7 leak)  ·  [ ] Within a Frame Story

### Epistemic arenas
Done: Self-Fulfilling Prophecy · Prophecy Twist · Common Knowledge · Emperor's New Clothes ·
Open Secret · Cassandra Truth · The Gambit · Tomato Surprise · Dramatic Irony.
- [x] Tomato in the Mirror — `tomato_in_the_mirror` (Oedipus)

### Specific actions (tactics)
Done: Finishing Move · Bar the Door · Improvised Weapon · Feint · Ambush · Heroic Sacrifice ·
Last Stand · The Cavalry · Counter.
- [x] Trap — `the_trap` · [x] Pincer — `pincer_maneuver` · [x] Pyrrhic Victory — `pyrrhic_victory`  (agent-converted)

### Collective / political
Done: Klingon Promotion · Full-Circle Revolution · Divide and Conquer · The Coup · Praetorian
Guard · Decadent Court · We Have Reserves · The Duel.
- [x] Smear Campaign (serialised slander → common belief) — `smear_campaign`

### Rhetoric — author, audience & attention
Done: Rule of Funny · Rule of Cool · Deus Ex Machina · Cliffhanger · Foregone Conclusion ·
Human Interest Story (the investment capability).
- [x] Rule of Drama — `rule_of_drama`
- [x] The Pratfall — `pratfall` · [x] Tear Jerker — `tear_jerker`  ·  [x] crafted Spectacle — `spectacle`

### Oratory / persuasion (the speaker↔audience arena — opened by `persuasion`)
Rhetoric holds attention; persuasion goes for CONVICTION. The speaker collapses author-and-figure
(direct address — the Host, persuading), and the goal is belief-change + a call to action. One
module unlocks a whole category of real-world forms:
- [x] the Persuasive Speech / TED Talk (the ethos/logos/pathos spine + call to action) — `persuasion`
- [x] the Courtroom Summation (logos + pathos before a jury; the burden of proof) — `courtroom_summation` (Atticus Finch)
- [x] the Rousing Speech (St. Crispin's Day — honest pathos-only, fear→resolve) — `rousing_speech`
- [x] the Reasonable-Doubt gate / Rogue Juror (burden of proof defeats persuasion) — `rogue_juror`
- [x] the Stump Speech (campaign address; a candidate wins a crowd's allegiance + vote) — `stump_speech` (Chisholm '72)
- [x] the Sales Pitch (persuasion for a sale) — `sales_pitch` (Mad Men's 'Carousel'; self-interested seller, the call to BUY)
- [x] the Debate (adversarial persuasion; rebuttal unseats, the audience swings) — `the_debate`
- [x] Propaganda / the Big Lie (ethos & pathos + repetition vs logos; entrenchment) — `propaganda`

### Non-fiction storytelling (the corpus handles it at ~71%)
Reality narrativized with the same grammar; the gap is the non-fiction *forms*.
Done: The Host / Presenter · Putting It to the Test · Based on a True Story.
- [x] Talking Head — `talking_head`  ·  [x] Reenactment — `reenactment`
- [x] Mockumentary — `mockumentary` (the form's fiction inversion)

### Storytelling frameworks
Done: Hero's Journey · Freytag · Story Circle · Save the Cat · Booker's Seven Plots.
- [x] Propp's Morphology (31 functions + 7 dramatis personae) — `propp`
- [x] Kishōtenketsu (4-act, conflict-FREE — proven: the conflict machinery stays idle) — `kishotenketsu`

---

## drams gap (the measured forward target)
NOTE: the eval-story fixtures live **engine-side, not in this repo**, and use the contingency/`resolve`
grammar (`*(…|…) as x*`, `resolve … -> …`) that the **shipped CLI `drams`/`eval` cannot parse** (only
the engine-internal `drams` example handles them; the latent `?(…)?` form does parse) — so measuring and
verifying these is a cross-repo, engine-internal task. PREPARED FIX for the Aragorn kingship facts (the
"cover for free via Royalty" one-liner): add to `examples/aragorn_fotr.trl`'s ontology —
`imply Rightful_King_of_Gondor -> [Heir_of_Isildur]` and `imply Exile_Who_Refuses_Crown -> [Heir_of_Isildur]`
(`Heir_of_Isildur` already implies `Royalty`, so both reach it transitively). The remaining uncovered
facts, in priority order:
- **fantasy** (`aragorn_fotr`): `Hobbit`, `Chieftain_of_the_Dunedain`, `Dangerous`, `Kingly_Bearing`,
  `Ranger`, `Dunedain`, `Wizard`, `Maiar`, `Elf`, `Halfelven` — mostly fantastic species/roles (low
  general value); `Rightful_King_of_Gondor`/`Exile_Who_Refuses_Crown` would cover *for free* if the
  eval story implied them to `Royalty` (a one-line eval fix, not new tropes).
- **non-fiction** (`mythbusters`): `Host`, `Experiments`, `Escalates`, `Confirmed` — the non-fiction
  forms above.

## Unfounded-node drive-down — measured from the committed corpus

The forward target = the highest-frequency **inline-invented tags** across `trl/tropes/**` — the red
tags the corpus references but does not declare. **Measure it deterministically** (not from the stale
notes below) by aggregating `tropelang report <file> --json` → `inline_tags` over every trope:

```sh
for f in $(git ls-files 'trl/tropes/**/*.trl' | grep -v index.trl); do tropelang report "$f" --json; done \
  | jq -r '.inline_tags[]' | sort | uniq -c | sort -rn   # frequency-ranked unfounded nodes
```

**Founded so far.** The 1.7.0 sweep declared most of the old P1 list (`Pursues`, `Trusted`, `Exposed`,
`Redeemed`, `Survivor`, `Coveted`), and `LoyalTo` + `Avenges` are already `rel`s in the prelude (the
corpus just uses different param keys — tolerated). The **1.8** round founded the **Chekhov's-Gun
planting/payoff** cluster (`Payoff(item)`, `Introduces`, `Uses`, `Fired`, `Pivotal`, `Mundane`,
`Endgame`). The **1.9** round founded the **diegetic / narration / role cluster** (the next densest):
`Narrator`, `Spectator`, `Canon`, `RealEvent`, `Detective`, `Invincible`, `Oppressive`, `Vehicle`,
`Treacherous(toward)`, `Family(with)`, and the relations `Bonded_To`/`Sundered_From` + the verb `Wakes`
— ~32 occurrences turned green across the diegetic, non-fiction, epistemic, and bonds tropes. (Rules
stay in the tropes; only vocabulary founded — no new module.)

The **1.10** round ground down the remaining 2–3× tail: props `Betrayer(of)`, `Leader`, `Sympathetic`,
`TrueRescue`, `RealPerson`, `Pass`, `Battlefield`, `City`; states `Triumphant`, `Refused`, `Reluctant`,
`Corrupted`, `CrossedTheHorizon`, `Status_Numb`; verbs `Recalls`, `Predicts`, `Atones`.

**The drive-down is essentially complete** — corpus inline (unfounded) total is now **204**, down from
**291** at the start. Re-measure with the command above before any further founding; what remains is:
- `Plain` and `Faithful` (2× each) — **ambiguous** (plain truth vs. open plain; loyal vs. accurate).
  Left inline deliberately; found them only by *splitting* the two senses into distinct names.
- A long tail of genuinely one-off bespoke flavor tags (`KeyserSoze`, `Pawn`, `Phantom`, `Unmasked`, …)
  — keep broken per the closed-vocabulary decision unless one recurs and earns promotion.

With founding exhausted **and self-recognition complete (100%)**, the forward target is **converting
new tropes** — the **allthetropes high-profile coverage gaps**. The live worklist, done batches, and
next-batch candidates are tracked in **"High-profile coverage" at the top of this file** (updated every
PR); the review *recipe* (how to run it, archive access) is in `CONVERSION_BOT.md`.

### Domain libraries & structural tropes (done — kept for provenance)
- **P2 domain vocab:** `modules/siege.trl` + `modules/heist.trl` declare the siege/military and
  heist/crime sets (Besieger/Rampart/…; Grifter/Counterfeit/…).
- **P3 structural tropes:** [x] **Heist** (`conflict/tactics/heist.trl`, Antwerp 2003) · [x] **Siege**
  (`conflict/war/siege.trl`, Orléans 1429). NOTE: a thin pre-existing `the_siege.trl` (Masada) coexists
  — coordinator to decide coexist vs. fold/`alias TheSiege -> Siege`.
