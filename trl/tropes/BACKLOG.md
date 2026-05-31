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
- [ ] Frame Story
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
- [ ] Feint / Misdirection          (bait an action, punish the commitment)   ← **up next**
- [ ] Ambush / Surprise Attack      (strike from concealment → auto-expose)
- [ ] Last Stand / Hold the Line    (outnumbered defense that buys time at a cost)
- [ ] Sacrifice Play                (trade your position to save/enable an ally)
- [ ] Disarm / Counter              (turn an attacker's commitment against them)

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
