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

### Character relationships (the dyad/triad)
Done: The Rival · Unrequited Love · Found Family · Enemies to Lovers · Love Triangle ·
Star-Crossed Lovers · Mentor & Student.
- [ ] The Love Triangle's darker forms (Love Dodecahedron, Triang Relations variants)
- [x] Sibling Rivalry — `sibling_rivalry` (Mufasa/Scar)  ·  [ ] Like Brother and Sister

### Character change & arcs
Done (psychology arena): Heel/Face Turn · Revenge · Despair Event Horizon · Survivor's Guilt.
- [x] Redemption Arc (The Atoner — guilt discharged by costly amends) — `redemption_arc`
- [x] Fall From Grace (Start of Darkness — the two-phase slide) — `fall_from_grace`
- [x] Coming of Age (Bildungsroman — innocence traded for maturity) — `coming_of_age`

### Identity / worldbuilding (drams-flagged)
Done: Hidden Identity · Rightful King Returns · The Chosen One · Unreliable Narrator.
- [x] Secret Legacy — `secret_legacy` (Percy Jackson)
- [ ] role archetypes: the Wanderer/Ranger, the Mage/Wizard (covers `Ranger`,`Wizard` gap facts)
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
- [x] The Pratfall — `pratfall` · [x] Tear Jerker — `tear_jerker`  ·  [ ] crafted Spectacle

### Oratory / persuasion (the speaker↔audience arena — opened by `persuasion`)
Rhetoric holds attention; persuasion goes for CONVICTION. The speaker collapses author-and-figure
(direct address — the Host, persuading), and the goal is belief-change + a call to action. One
module unlocks a whole category of real-world forms:
- [x] the Persuasive Speech / TED Talk (the ethos/logos/pathos spine + call to action) — `persuasion`
- [x] the Courtroom Summation (logos + pathos before a jury; the burden of proof) — `courtroom_summation` (Atticus Finch)
- [x] the Rousing Speech (St. Crispin's Day — honest pathos-only, fear→resolve) — `rousing_speech`
- [x] the Reasonable-Doubt gate / Rogue Juror (burden of proof defeats persuasion) — `rogue_juror`
- [x] the Stump Speech (campaign address; a candidate wins a crowd's allegiance + vote) — `stump_speech` (Chisholm '72)
- [ ] the Sales Pitch (persuasion for a sale)
- [x] the Debate (adversarial persuasion; rebuttal unseats, the audience swings) — `the_debate`
- [x] Propaganda / the Big Lie (ethos & pathos + repetition vs logos; entrenchment) — `propaganda`

### Non-fiction storytelling (the corpus handles it at ~71%)
Reality narrativized with the same grammar; the gap is the non-fiction *forms*.
Done: The Host / Presenter · Putting It to the Test · Based on a True Story.
- [x] Talking Head — `talking_head`  ·  [ ] Reenactment
- [x] Mockumentary — `mockumentary` (the form's fiction inversion)

### Storytelling frameworks
Done: Hero's Journey · Freytag · Story Circle · Save the Cat · Booker's Seven Plots.
- [x] Propp's Morphology (31 functions + 7 dramatis personae) — `propp`
- [x] Kishōtenketsu (4-act, conflict-FREE — proven: the conflict machinery stays idle) — `kishotenketsu`

---

## drams gap (the measured forward target)
The remaining uncovered facts on the eval stories, in priority order — the worklist that actually
moves coverage:
- **fantasy** (`aragorn_fotr`): `Hobbit`, `Chieftain_of_the_Dunedain`, `Dangerous`, `Kingly_Bearing`,
  `Ranger`, `Dunedain`, `Wizard`, `Maiar`, `Elf`, `Halfelven` — mostly fantastic species/roles (low
  general value); `Rightful_King_of_Gondor`/`Exile_Who_Refuses_Crown` would cover *for free* if the
  eval story implied them to `Royalty` (a one-line eval fix, not new tropes).
- **non-fiction** (`mythbusters`): `Host`, `Experiments`, `Escalates`, `Confirmed` — the non-fiction
  forms above.

## Broken-ref drive-down — current masters (links-first)

Driven by what the master narratives actually reference but the corpus does not yet declare (scan:
`links().tags` with `known=false` over `narratives/` + corpus). Resolving these is what turns red tags
green in the IDE. Two masters, two domains. Priority order = frequency × reusability.

**P1 — generic vocabulary (prelude candidates).** Universal, not domain-specific; belong in `prelude.trl`:
- `Pursues` (82, intent), `Avenges` (rel), `Trusts`/`Trusted`, `LoyalTo`, `Exposed`, `Redeemed`,
  `Coveted`, `Secured`, `Lifted`, `Authentic`, `Overcommitted`, `Demands`, `Opens`, `Held`, `Burns`,
  `Withdraws`. Decide prelude vs. concept per term; `Pursues` is the single biggest win.

**P2 — domain vocabulary libraries (declare, not convert).** Reusable across any story in the domain:
- **Siege / military** (`the_salt_gate`): `Besieger`/`Besieged`/`Besieging`, `Siege`, `Fortress`,
  `Rampart`, `Chokepoint`, `Inner_Gate`, `Sally_Door`, `Belfry`, `Salt_Rich`, roles `Warlord`/`Soldier`/
  `Sergeant`/`Veteran`/`Quartermaster`/`Commander`/`ReliefCommander`/`Champion`/`Defender`/`Army`, verbs
  `Encircles`/`Bombards`/`Breaches`/`Sallies`/`Battered`/`Stunned`/`Steadfast`/`Galled`. → a
  `concepts/`+`modules/` military set.
- **Heist / crime** (`the_lacquer_nightingale`): roles `Grifter`/`Hacker`/`Collector`/`InsideOperator`/
  `Mark`, `RealTarget`/`Counterfeit`/`Offstage`/`Artisan`/`Wronged`, verbs `Swaps`/`Disables`/`Feints`/
  `Endears`. → a crime/caper set.

**P3 — structural tropes (convert).** The masters *demonstrate* these tropes, yet they don't exist:
- [x] **Heist** — `tropes/conflict/tactics/heist.trl` riding `modules/heist.trl` (Antwerp 2003 vignette).
- [x] **Siege** — `tropes/conflict/war/siege.trl` riding `modules/siege.trl` (Orléans 1429 vignette).
      NOTE: a thin pre-existing `the_siege.trl` (`imply TheSiege`, Masada) now coexists — coordinator
      to decide coexist vs. fold/`alias TheSiege -> Siege`.

P2 progress: `modules/siege.trl` + `modules/heist.trl` declare the bulk of each master's domain
vocabulary (Besieger/Rampart/…; Grifter/Counterfeit/…). Remaining P1 prelude candidates still broken:
`Pursues` (biggest), `Avenges`, `LoyalTo`, `Trusted`, `Exposed`, `Redeemed`, `MadeBy`, `Survivor`.

Keep genuinely bespoke flavor tags (one-off character descriptors) broken per the closed-vocabulary
decision unless promoted here.
