# TropeLang StoryCraft Guide

What effective storytelling looks like in TropeLang. This is the third layer of the
documentation stack:

| Layer | Document | Question it answers |
|-------|----------|---------------------|
| Mechanical | `tropelang grammar` (spec 01) | What is *legal*? |
| Protocol | `STYLE.md` | What is *well-formed*? |
| **Application** | **this guide** | What is *good storytelling*? |

A file can gate clean, follow every style rule, fire every trope it targets at
conf 1.00 — and still be a thin story. This guide is about the difference. It was
compiled from writing master narratives and auditing where they fell short.

---

## 1. The trope is the recognition, not the unit of composition

The single most tempting workflow for an agent is **trigger-first writing**: pick the
target tropes, look up each rule's `when:` clause, allocate one beat to deposit exactly
those facts, and move to the next trope. It works — every recognition fires — and it
produces a story shaped like a checklist.

The tell is structural: scenes with a single beat, each scene servicing exactly one
rule, characters who exist only as bundles of precondition tags.

❌ The scene exists to fire the rule:
```trl
scene the_button {
  beat 6 {
    evt the_ring [&Provokes(agent=the_doorbell, target=winston)]
    winston [+Enraged]
    // Berserk_Button → ✓ done, next trope
  }
}
```

✓ The scene is a dramatic unit; the trigger lands mid-progression:
```trl
scene the_button {
  beat 6 {
    // setup: the household at rest — the calm the button will shatter
    sam @ the_couch_corner
    winston @ the_window           // his post; the street is HIS street
    sam [#Doubting]                // carried in from the dog park — the armor already cracked
  }
  beat 7 {
    // turn: the provocation
    evt the_ring [&Provokes(agent=the_doorbell, target=winston)]
    winston [+Enraged]
    evt the_borkening [&Crushes(target=sam)]      // and the third crush lands on sam
    sam [#Frayed]                  // a new KIND of state — past doubt, before breaking
  }
  beat 8 {
    // consequence: the comfort, and the relationship that earns it
    evt the_scoop [&Embraces(agent=pat, target=winston)]
    winston [-Enraged]
    pat -- sam : "The look. The book. She bought the book."
  }
}
```

Same recognitions fire — `Berserk_Button`, `Cooldown_Hug`, the crush toward
`BreakTheHaughty` — but now they *emerge from* a scene with setup, turn, and
consequence, instead of being the scene.

**Rule of thumb: write the scene a director could shoot, then check which tropes it
fires. Not the reverse.** Use the trigger lookup (§9) to *aim* the drama, not to
replace it.

## 2. Beats progress; scenes develop

A beat is the engine's tick — the smallest unit of narrative time. A scene with one
beat is a scene where nothing *develops*; it states. Real scenes move through phases:

- **setup** — who is here, what they want, what they carry in from the last scene;
- **turn** — the event that changes something;
- **consequence** — the new state, the reaction, the cost.

That is 2–4 beats minimum. A single-beat scene is a deliberate effect — a smash cut,
a stinger, an insert — and should be the exception that reads as one.

The accretive log rewards this: state asserted in the beat it becomes true, retracted
(`[-Tag]`) in the beat it stops, intervals scoped per beat (`STYLE §7`). A one-beat
scene throws that machinery away — everything becomes simultaneous, and the engine
sees a tableau, not a progression.

## 3. Every beat does at least two jobs

Efficient storytelling braids threads. In any good scene, the A-plot moves *and* a
relationship shifts *and* a seed gets watered — simultaneously, in the same beats.
A scene that advances exactly one thing is a skipped opportunity the audience feels
as thinness.

Concretely, each beat should advance **at least two** of:

1. **Plot** — an `evt` that changes the situation;
2. **A relationship** — an edge asserted, relabeled, or severed (`a -- b : "…"`);
3. **A character state** — a tag accrued, a tag retracted, a transition between
   named conditions;
4. **A seed** — a latent `?…?` fact or named ambiguity referenced, complicated, or
   advanced toward its payoff;
5. **A place/thread token** — presence (`@`) that sets up a later scene.

When a beat does only one of these, either braid a second thread into it or merge it
into a neighboring beat.

## 4. Characters evolve between distinct states — no sliding spectra

**Avoid numbers.** TropeLang's numeric stats exist for the realtime-game bridge (HP,
AC, dice — the `^` arena); in a storytelling context an invented magnitude encodes
nothing. There is no unit of grief, no scale of pride. A `salience=6` that becomes
`salience=8` is false precision wearing the costume of development — the reader of
the graph learns only that the author typed a bigger number. (`STYLE §8` makes the
same call for qualitative `^` stats; it applies equally to author-side use of any
numeric slot.)

Character development is a walk through **named, qualitatively distinct states** —
asserted in the beat each becomes true, retracted in the beat it stops:

✓ Pride doesn't shrink; it shatters in stages, each a different *kind* of state:
```trl
scene the_shedding  { beat 3 { … sam [+Defensive]                } }  // the joke armor goes on
scene the_herding   { beat 5 { … sam [-Defensive]  sam [#Doubting] } }  // the armor cracks
scene the_breaking  { beat 8 { … /* BreakTheHaughty derives [+Humbled] [+Teachable] */ } }
```

Each transition is an event the story can witness, a fact a rule can read, a moment a
director could shoot. "Slightly more humiliated" is none of those things.

**Where modules require numbers, treat them as enums and quarantine them.** Some
corpus rules mechanically compare numeric slots (the needs-module Inversion behind
`Determinator` reads `rank`/`salience`). Two cases:

- `rank` in `needs.trl` is a *defined ordinal* — it indexes Maslow's named rungs
  (1 = physiological … 4 = esteem …). It is an enum wearing a number. Always comment
  the rung name; never invent intermediate values.
- `salience` has no defined scale. Its only meaningful content is the *relation* the
  rule reads (`$hs > $bs` — which drive grips harder). Write the minimal pair that
  encodes that qualitative relation, **once**, as the module-required trigger payload
  — and never vary it over time as if it measured something.

If a character fact carries a number the corpus never compares, delete the number.

## 5. Tend your seeds

Planting is cheap; the style guide already says to front-load latent facts and named
ambiguities. The storytelling failure is **plant-and-forget**: a seed asserted in the
preamble and touched exactly once more, at the payoff. The graph then contains a
setup and a resolution with no middle — and the payoff is unearned everywhere except
in the comments.

Between planting and payoff, **re-touch every seed at least once**:

- reference the ambiguity from a beat (`*winston [+Tyrant]*` from the herding
  incident's perspective — the contingent reading that keeps the question alive);
- deepen the latent fact (`?sam [~Pursues(goal=second_corgi)]?` can acquire
  a contingent sibling mid-story: sam lingering on the breeder's page *again*);
- let a character act in a way only explicable by the seed — the graph shows the
  cause when the resolve lands.

**Plant seeds prospectively, not just retrospectively.** When writing from scratch, you won't
always know where a payoff beat falls before you write it. Plant the seed at the moment you
introduce the element anyway — `?entity [~Verb]?` is a forward promise to yourself, not just
a declaration of existing ambiguity. A seed without a payoff is easier to find and fix than a
payoff without a seed that the engine can't trace.

A seed that is never watered should either get a middle touch or be cut.

## 6. Encode the story; comment the annotation

The `//` layer is invisible to the engine, to drams, and to recognition. If a story
moment matters — the forty minutes of barking, the eleven apologized-to strangers —
it must exist as an **encoded fact**: an event, an edge, a state change, a presence.
The comment annotates *why* the fact is there; it never substitutes for it.

The test: delete every comment, then re-read the file as the engine sees it. Whatever
vanished from the story was never in it.

## 7. Read drams as an editorial report

`tropelang drams <file>` measures density × coverage: how much of what you encoded
participates in a recognized pattern. Two editorial readings:

- **The gap list is your dead-threads report.** Every uncovered fact is something
  you declared that no pattern ever picked up: an unused presence edge, a
  relationship that never figured in a recognition, a gauge asserted once. Each one
  is either a thread to *develop* (braid it into more beats until a rule covers it)
  or a declaration to *cut*. A long gap list with single-beat scenes means the
  structure is thin, not that the corpus is missing tropes.
- **Score by revision, not by target.** A first structural draft landing ~0.4 is
  normal; braiding threads and adding intra-scene progression should *raise* it,
  because the new facts participate in the patterns already firing. If a revision
  adds facts and the score *drops*, you added decoration, not story.

Free recognitions are the reward signal for real structure: a properly built
crush-and-relief arc earns `TraumaCongaLine_Broken` without targeting it; the
character on the floor surrounded by consequences earns `HeroicBSOD`. When unplanned
tropes fire at high confidence, the structure is genuinely load-bearing. (Inspect the
sub-1.00 strays too — a `MamaBear($guardian=the_vacuum)` at 0.50 is harmless noise,
but a wrong-way binding at 0.75 may mean a discriminator is leaking.)

## 8. Know the recognizer's grain (and write with it)

Recognition is shape-based and has mechanical limits that *constrain plotting*. Found
so far, the hard way:

- **Shared-verb binding resolves by coverage, not file order** (engine ≥ 0.7.4). When two
  rules trigger on the same verb (e.g. two tropes both keyed on `&Crushes`), the recognizer
  binds each to the event whose entities best satisfy *its* discriminator — so two tropes
  whose discriminators sit on *different entities* but ride the *same verb* both fire from one
  file (recognition matches `eval` here). The corollary: this works **because** discriminators
  are contrastive (next bullet) — make them so and the right event binds itself. (Pre-0.7.4
  engines bound the first matching event with no backtrack, so such tropes were mutually
  exclusive; only give competing beats distinct verbs if you must target an older engine.)
- **The discriminator must ride a bound event role** (`STYLE §8`); static tags on
  entities no event binds are invisible to coverage. When braiding threads (§3),
  make sure each trope's distinguishing entity is named in a role of its trigger
  event — a braid that moves the discriminator off the event un-fires the trope.
- **Sibling vignettes cross-fire.** If your scene is structurally a cousin of another
  trope in the same family, expect it in the suggestions at ≤0.75. That's correct
  behavior — only investigate when a cousin confirms at 1.00.

Debug with bisection: when an expected trope is silent, reproduce its trigger in a
minimal file, confirm it fires alone, then add back the story's other facts until it
goes quiet. The last addition is the collision.

## 9. The workflow, revised

**Before step 1 — inventory the source.** For an adaptation or a known story, do one pass
of the material as plain notes: props, gags, character quirks, motifs, the moment a
relationship shifts, every callback. The encoding pass fires on more tropes and compresses
fewer scenes when the inventory exists. Skipping this step produces premature beat
compression — you fold three story moments into one beat and the evidence that would fire
recognition is silently lost.

1. **Premise and cast first.** Who wants what; what stands in the way; what the
   audience should carry away. Pick the *spine* trope (the one the story IS) and
   3–6 supporting tropes at other scales (character, bond, structure, meta).
2. **Look up the triggers** for every target — read the actual `rule` blocks, note
   the precondition tags the cast must carry and the verbs the beats must contain.
   If two targets share a verb, give them **contrastive** discriminators on the
   entities they care about (§8), so recall binds each to its own event.
3. **Outline scenes as dramatic units** — setup/turn/consequence, 2–4 beats each,
   each scene braiding ≥2 threads. Place the trigger events where the drama puts
   them, not in dedicated trope-beats. Use the full **`arc ▸ act ▸ scene ▸ beat`**
   spine: acts (and the arc) are first-class, *taggable* scopes the engine sees and
   recognizes over — not formatting. Group scenes into acts that carry a turn, and
   tag the arc itself when the story-as-a-whole is part of what a trope reads.

   **Sketch all beat labels before writing the header.** The outline reveals what is
   cross-scene vocabulary (recurring characters, the main MacGuffin, chron markers) vs.
   scene-local (a single-beat prop, a throwaway set). That scan determines what belongs
   in the file header vs. what should be declared inline at the top of its beat
   (`STYLE §10`). Writing the header before the outline inverts the dependency and
   produces a registry of every prop the author imagined — most of which get no log
   footprint.
4. **Draft. Then verify three ways:**
   `validate` (legal) → `suggest` (the targets fire, at full confidence, with the
   *right bindings*) → `drams` (coverage; read the gap list).

   **Check three defects per scene as you finish it**, not at file end: (a) `concept`
   where `char [+Collective]` is correct — if the entity takes edges, accretes tags, or
   anchors a seed, it is a `char` (`STYLE §1`); (b) double `resolve` — a second resolve
   of the same ambiguity name is a defect, not a confirmation (`STYLE §3`); (c) inline
   declarations buried after `evt` lines in the same block — declarations lead the block
   (`STYLE §10`). These compound across a long file; catching them per-scene costs nothing.
5. **Revise against the gap list** — develop or cut every dead thread; deepen
   gauges; water seeds. Re-run drams; the score should rise.
6. **Prose pass last.** `dialog(inline="""…""")` annotations on the events that
   carry voice — the graph is the structure, the prose is the performance. The
   annotations are transparent to recognition, so this pass cannot break the
   structure (re-run `suggest` once to confirm).

---

*Companion documents: `tropelang grammar` for the language, `STYLE.md` for authoring
protocol. The worked narratives this guide was distilled from used corpus `standard`
1.8.0, CLI 0.7.2. Cold-start workflow notes (`§5`, `§9`) added from corpus `standard`
1.9.0 narrative work.*
