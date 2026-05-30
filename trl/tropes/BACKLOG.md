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
- [ ] The Climax
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

## Storytelling systems & frameworks (`trl/modules/`)
Higher-level structures that *organize* tropes — name + sequence the stages, link the beats.
- [x] The Hero's Journey / Monomyth   (Campbell — `heros_journey.trl`)
- [ ] Freytag's Pyramid               (exposition / rising / climax / falling / dénouement)   ← **up next**
- [ ] Dan Harmon's Story Circle       (the 8-step you/need/go/search/find/take/return/change)
- [ ] Save the Cat beat sheet         (Blake Snyder, 15 beats)
- [ ] The Seven Basic Plots           (Booker)
- [ ] Propp's Morphology              (31 narrative functions)
- [ ] Kishōtenketsu                   (4-act, no central conflict — East Asian)

## Recommended order (simple building blocks first)
1. ~~Conflict~~ ✓ — the engine that Protagonist + Antagonist create.
2. ~~The Hero~~ ✓ / ~~The Mentor~~ ✓ — core cast well underway.
3. ~~Call to Adventure~~ ✓ / ~~Three-Act Structure~~ ✓ — the spine of plot.
4. ~~Chekhov's Gun~~ ✓ / ~~Red Herring~~ ✓ — promoted from `foreshadowing.trl`'s imply to full tropes.
5. **Next:** finish the cast (Sidekick, Foil, Love Interest, Narrator…) or the remaining journey beats (The Climax, The Hero's Journey), then converge with the drams gap on the eval stories.
