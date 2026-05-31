# Core Tropes — conversion backlog

A curated list of foundational ("core") tropes to encode in `trl/tropes/`, worked **one at a
time**. This is the *forward* plan; the *measured* plan is the drams gap — `drams.py <story>`
shows which facts a real story leaves uncovered, and `corpus_reuse.py` shows what to reuse.
Converge the two.

**Status:** `[x]` converted · `[~]` partial (lives in a module/imply) · `[ ]` todo.
Vignettes must vary by story / medium / era — no franchise monoculture (see `SKILL.md`).

## Cast & character roles
- [x] The Protagonist            (Universal)
- [x] The Antagonist             (Universal)
- [x] The Deuteragonist          (Universal)
- [x] The Hero                   (Universal)
- [x] The Mentor                 (Universal)
- [ ] The Sidekick
- [ ] The Love Interest
- [ ] The Foil
- [ ] The Narrator
- [ ] Anti-Hero
- [ ] The Trickster
- [ ] The Big Bad

## Conflict
- [x] Conflict — the engine (vs Man / Self / Nature / Society / Fate)   (Omnipresent)
- [ ] Rivalry
- [~] The Dilemma                 (`philosophy.trl` → `MoralDilemma`)

## Plot structure & arc
- [x] Three-Act Structure        (Universal)
- [x] The Hero's Journey         (system — `trl/modules/heros_journey.trl`)
- [x] Call to Adventure          (Universal)
- [x] Refusal of the Call        (Universal)
- [ ] In Medias Res
- [~] The Climax                 (concept `climax` defined in `freytags_pyramid.trl`)
- [x] Frame Story                 (S14 levels — `frame_story.trl`: Frankenstein, 3 canon planes nested)
- [ ] Cliffhanger

## Setup, payoff & devices
- [x] Foreshadowing               (Omnipresent)
- [x] The Reveal                  (Omnipresent)
- [x] Hope Spot                   (Omnipresent)
- [x] Chekhov's Gun               (Omnipresent — promoted from foreshadowing's imply)
- [x] Red Herring                 (Omnipresent — promoted from foreshadowing's imply)
- [ ] Plot Twist
- [ ] MacGuffin                   (cf. skill example `MacGuffinDelivery`)
- [~] Dramatic Irony              (`theory_of_mind.trl`)
- [ ] Flashback
- [x] Unreliable Narrator         (FRONTIER — first corpus use of S14 diegetic levels: a non_canon
                                    narration plane vs the reality plane; The Usual Suspects)
- [x] Dream Sequence              (S14 lifecycle — `dream_sequence.trl`: a non_canon dream that
                                    dissolves to LATENT on waking; Link's Awakening)
- [x] Breaking the Fourth Wall    (S14 outward crossing — `fourth_wall.trl`: a character reaches OUT
                                    to the audience plane; Ferris Bueller)
- [x] Dream Within a Dream        (S14 deep nesting — `dream_within_a_dream.trl`: 4 stacked non_canon
                                    planes + the kick; Inception)
- [x] Show Within a Show          (S14 inner-fiction-loops-back — `show_within_a_show.trl`: a non_canon
                                    play mirrors a canon crime to expose it; Hamlet's Mousetrap)
- [x] Or Was It a Dream?          (S14 levels × §11 ambiguity — `or_was_it_a_dream.trl`: a dream-residue
                                    leaves an uncollapsed (real|dream) ambiguity; Coleridge's flower)

## Character change & arcs
- [ ] Coming of Age
- [ ] Heel Face Turn              (cf. skill example `HeelFaceTurn`)
- [ ] Redemption Arc
- [ ] Fall From Grace

## Relationships
- [ ] Found Family
- [ ] Star-Crossed Lovers
- [ ] Mentor and Student

## Psychological systems & emotion threads (`trl/modules/` + tropes)
Code that *simulates/estimates* emotional response as threads progress — appraisal,
motivation, and state transitions — general enough to compose arbitrary emotional arcs.
- [x] Emotion Dynamics             (system — `emotion_dynamics.trl`: appraisal → emotion → motivation → threads)
- [x] Revenge                      (trope — rides the vengeance thread)
- [x] Despair Event Horizon        (trope — irreversible hope → despair crossing; dark mirror of Hope Spot)
- [x] Five Stages of Grief         (system — `five_stages_of_grief.trl`: staged denial → … → acceptance thread)
- [x] Heel Face Turn / Face Heel Turn   (paired trope — `heel_face_turn.trl`: alignment reversal riding the appraisal layer)
- [x] Survivor's Guilt / Trauma    (trope — `survivors_guilt.trl`: S8 imprint → trigger → catharsis/repression; self-directed blame)
- [x] Motivation / goals system    (system — `motivation_dynamics.trl`: desire → pursuit → attainment/obsession/abandonment; determination is the hinge)

## Specific actions — conflict & cooperation (`trl/modules/` + tropes)
Event-level tactics: what a character actually DOES in a contested moment — the layer a game
mechanic maps onto. Rides `action_dynamics.trl` (strike/guard/exploit/finisher · pin/cover/
improvise/bar). All sim-runnable (`tools/sim.py finisher_combo | bar_door | improvised`).
- [x] Action Dynamics system        (`action_dynamics.trl`: the verbs of conflict & cooperation)
- [x] Finishing Move                (trope — combination finisher; Naruto + Shikamaru vs Hidan)
- [x] Bar the Door                  (trope — deny access / buy time; Jesse's RV vs Hank)
- [x] Improvised Weapon             (trope — indirect attack; Henry Jones' umbrella → gulls → plane)
- [x] Feint / Misdirection          (`feint.trl` — Bait → Punish_Overcommit; Hannibal at Cannae)
- [x] Ambush / Surprise Attack      (`ambush.trl` — Spring_Ambush bypasses guard; Teutoburg Forest)
- [x] Heroic Sacrifice / Sacrifice Play (`heroic_sacrifice.trl` — giver [+Fallen], ally [+Saved]; Sydney Carton)
- [x] Last Stand / Hold the Line    (`last_stand.trl` — Hold_The_Line: count(strikes)≥3 → BoughtTime+Fallen; Thermopylae)
- [x] The Cavalry                   (`the_cavalry.trl` — Reinforcement → [+Relieved], which spares the held line; Vienna 1683)
- [x] Disarm / Counter              (`counter.trl` — Riposte: let them commit, turn it back → [+Defeated]; Musashi vs Kojiro)

## Epistemic arenas (`trl/modules/` + tropes)
Knowledge, belief, and truth as first-class dynamics — beyond the narrator truth-tiers.
- [x] Prophecy / Foreknowledge      (system — `prophecy.trl`: foretell → ?latent? fate → !absolute!)
- [x] Self-Fulfilling Prophecy      (trope — the avoidance seals the fate; Oedipus)
- [x] Prophecy Twist                (trope — §11 ambiguity collapses the unforeseen way; Macbeth)
- [x] Common Knowledge             (system — `common_knowledge.trl`: mutual → common via the public utterance)
- [x] The Emperor's New Clothes    (trope — the spoken resolution: the child makes it common, the fiction collapses)
- [x] Open Secret                  (trope — the unspoken resolution: a tacit pact, never made common; Discworld's Carrot)
- [x] Cassandra Truth              (`cassandra_truth.trl` — true foresight that can't propagate; inverse of common knowledge; Troy)
- [x] The Gambit / Batman Gambit   (`the_gambit.trl` — a plan built on predicting others' behaviour; weaponized ToM; Code Geass)
- [x] Tomato Surprise              (`tomato_surprise.trl` — a fact withheld from the audience, surfaced; latent→absolute; Pale Fire)
- [ ] Dramatic Irony (full)        (promote from `theory_of_mind.trl`)   ← **up next**
- [ ] Tomato in the Mirror         (the PROTAGONIST learns the recontextualizing fact)

## Collective / political scale (`trl/modules/` + tropes)
The supra-individual arena — the [%Political] domain. Power as common knowledge of the right to
rule; coalitions, legitimacy, defection, revolution. Rides `power_dynamics.trl`.
- [x] Power Dynamics system        (`power_dynamics.trl`: pledge/coalition · legitimacy · revolution · usurp · divide)
- [x] Klingon Promotion            (take a rank by killing its holder; Commodus / Gladiator)
- [x] Full-Circle Revolution       (the deposers become the deposed; Animal Farm)
- [x] Divide and Conquer           (keep rivals from uniting — inverse of coalition; Jay Gould)
- [ ] The Coup                     (seize the state apparatus, not just the throne)   ← **up next**
- [ ] Praetorian Guard             (the kingmakers who make and unmake rulers)
- [ ] Decadent Court               (the rot inside legitimate power)
- [ ] We Have Reserves             (the callous arithmetic of mass force)
- [ ] Reputation / Honor system    (status as a social-epistemic quantity)

## Storytelling systems & frameworks (`trl/modules/`)
Higher-level structures that *organize* tropes — name + sequence the stages, link the beats.
- [x] The Hero's Journey / Monomyth   (Campbell — `heros_journey.trl`)
- [x] Freytag's Pyramid               (Freytag — `freytags_pyramid.trl`; defines `climax` et al.)
- [x] Dan Harmon's Story Circle       (system — `story_circle.trl`: the 8-step closed loop; order/chaos halves, two threshold crossings)
- [x] Save the Cat beat sheet         (system — `save_the_cat.trl`: the 15 beats with page-target params, on the three-act spine)
- [x] The Seven Basic Plots           (system — `booker_seven_plots.trl`: plot-TYPE taxonomy wired to corpus mechanisms; 7-story gallery)
- [ ] Propp's Morphology              (31 narrative functions)
- [ ] Kishōtenketsu                   (4-act, no central conflict — East Asian)

## Recommended order (simple building blocks first)
1. ~~Conflict~~ ✓ — the engine that Protagonist + Antagonist create.
2. ~~The Hero~~ ✓ / ~~The Mentor~~ ✓ — core cast well underway.
3. ~~Call to Adventure~~ ✓ / ~~Three-Act Structure~~ ✓ — the spine of plot.
4. ~~Chekhov's Gun~~ ✓ / ~~Red Herring~~ ✓ — promoted from `foreshadowing.trl`'s imply to full tropes.
5. **Next:** finish the cast (Sidekick, Foil, Love Interest, Narrator…) or the remaining journey beats (The Climax, The Hero's Journey), then converge with the drams gap on the eval stories.
