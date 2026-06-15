# Engine report — story-time predicates (`before`/`after`) are inert at recognition

**Engine:** tropelang CLI **0.8.0** (the S23 story-time release)
**Corpus:** standard, `file://trl`
**Pipelines exercised:** `tropelang validate`, `tropelang shape … --corpus file://trl`, `tropelang selfcheck`
**Status:** blocking — story-time ordering cannot be used as a trope discriminator. The six time-travel
tropes built on it (PR #78, held) self-recognize at 1.00 but the recognition is spurious.

---

## 1. Summary

`before($a, $b)` / `after($a, $b)` story-time predicates (and chron ordering generally) **parse and
validate, but are not evaluated by the recognition pipeline** (`shape` / `selfcheck`). A rule whose `when:`
block contains a story-time predicate recognizes **identically** whether the ordering holds, is reversed, or
no `chron` exists in the story at all. Recognition rests entirely on the entity/event patterns; the
story-time clause is silently ignored.

Net effect: a rule cannot key on "deed precedes its outcome", "the act lies later than the existence it
unmakes", a `[+Loop]` cycle, or a chron fork. Story-time is currently an authoring / `drams` concern only.

---

## 2. Expected mechanics

Author-facing model (as documented for S23):

- `chron m1 ~> m2 ~> m3` declares in-world succession between **markers**; `~~` co-presence; `[+Loop]` a
  cycle on a marker; comma-separated chains a **fork** (`chron p ~> a, p ~> b`).
- `@@ marker` anchors a scene / entity / event to a story-time position.
- In a rule `when:` block, `before($a, $b)` should hold **iff** `$a`'s story-time position strictly precedes
  `$b`'s under the chron order (presumably three-valued: false / unknown for incomparable branch tips or
  unordered loop members). `after` is the mirror.
- **Recognition should treat `before`/`after` as gating predicates**: a candidate binding whose operands do
  not satisfy the ordering under the story's chron must be **rejected**.

So `Stable_Time_Loop` (a deed `before` the outcome it produces, over a `[+Loop]`) should recognize **only**
stories whose chron actually places the deed before the outcome; a story with no chron, or the reverse
ordering, should **not** match.

---

## 3. Observed behavior (failing)

### 3a. Minimal isolated rule — `before(e1, e2)` does not gate

Rule (identical in both stories below):

```trl
import "trl/concepts/index.trl"
verb Acts(on) [+Temporal]
rule R_Order {
  when:
    char $a
    evt  $e1 [&Acts(agent=$a, on=$x)]
    evt  $e2 [&Acts(agent=$a, on=$y)]
    before($e1, $e2)
  then:
    $e1 [+StableTimeLoop]
}
```

**Story A — forward (`before(e1,e2)` is TRUE):**
```trl
chron earlier ~> later
char a
obj x obj y
scene s1 @@ earlier { beat 1 { evt e1 [&Acts(agent=a, on=x)] } }
scene s2 @@ later   { beat 1 { evt e2 [&Acts(agent=a, on=y)] } }
```

**Story B — reversed (`before(e1,e2)` is FALSE; e1 is anchored later, e2 earlier):**
```trl
chron earlier ~> later
char a
obj x obj y
scene s1 @@ later   { beat 1 { evt e1 [&Acts(agent=a, on=x)] } }
scene s2 @@ earlier { beat 1 { evt e2 [&Acts(agent=a, on=y)] } }
```

Both produce an **identical** recognition set — `R_Order conf 1.00` in each:

```
$ tropelang shape A.trl --corpus file://trl      $ tropelang shape B.trl --corpus file://trl
▸ A.trl — 6 recognitions                          ▸ B.trl — 6 recognitions
    R_Order              conf 1.00                     R_Order              conf 1.00
    …                                                  …
```

Expected: A fires, **B does not**. Observed: both fire.

### 3b. The shipped corpus rule fires with NO chron at all

A story with no `chron` and no `@@` anchors — i.e. no story-time structure whatsoever:

```trl
import "trl/concepts/index.trl"
char trav
obj out
scene s1 { beat 1 { evt d [&Causes(agent=trav, outcome=out)] } }
```

recognizes the real corpus rule:

```
$ tropelang shape t4.trl --corpus file://trl
▸ t4.trl — 2 recognitions
    Stable_Time_Loop     conf 1.00
```

`Stable_Time_Loop`'s `when:` is `char $t; obj $o; evt $d [&Causes(agent=$t, outcome=$o)]; before($d,$o)`.
With no chron present, `before($d,$o)` cannot be true under any reasonable semantics — yet the rule matches.
This is the discriminator collapsing to the bare `[&Causes]` event.

### 3c. Full test matrix (rule of §3a / §3b)

| Case          | Story-time setup                                  | `before` truth | Expected | Observed |
|---------------|---------------------------------------------------|----------------|----------|----------|
| forward       | e1 @@earlier, e2 @@later (`chron earlier ~> later`)| true           | FIRE     | FIRE     |
| reversed      | e1 @@later, e2 @@earlier                           | false          | NO FIRE  | **FIRE** |
| single-marker | both events @@earlier                              | vacuous        | NO FIRE  | FIRE     |
| no-chron      | no `chron`, no `@@`                                | undefined      | NO FIRE  | FIRE     |

All four fire. The **reversed** and **no-chron** rows are the proof: `before` is not consulted.

---

## 4. Likely cause (hypothesis for the engine agent)

The recognition matcher (recall → coverage) appears to build candidate bindings from the **entity / tag /
edge / event** clauses of `when:` and then **drop / no-op** any clause it doesn't recognize as one of those
shapes — story-time predicates (`before`/`after`, and presumably any chron-order constraint) fall through and
are never applied as filters. `validate` accepts them (they parse), so the gap is purely in the
recognition evaluator, not the grammar.

---

## 5. Reproduction

```sh
# engine 0.8.0, from the corpus repo root
tropelang shape A.trl --corpus file://trl   # forward  — R_Order fires (correct)
tropelang shape B.trl --corpus file://trl   # reversed — R_Order STILL fires (bug)
tropelang shape t4.trl --corpus file://trl  # no chron — Stable_Time_Loop fires (bug)
```
(A.trl / B.trl / t4.trl = the three snippets above.)

---

## 6. Impact & ask

- **Impact:** story-time ordering is unusable as a recognition discriminator. The chron / `@@` / `[+Loop]` /
  fork structure an author writes is invisible to `shape` / `selfcheck`, so any trope whose identity is
  *structural in time* (stable loop, grandfather paradox, branching timeline, …) cannot be recognized; its
  rule collapses to whatever bespoke event verb it happens to carry, over-firing on non-time-travel stories.
- **Ask:** make `before` / `after` (and chron order: `~>`, `[+Loop]`, `~~`, the fork) **evaluable as
  recognition gates** — reject candidate bindings that violate the ordering under the story's chron.

### Open questions for the engine team
1. Are `before`/`after` intended to gate **recognition** (`shape`/`selfcheck`), or only the `sim` / `drams`
   forward-chain path? (If the latter, that should be documented, and trope recognition needs a different
   story-time primitive.)
2. How does a bound operand acquire its story-time position for predicate evaluation — inherited from the
   enclosing `scene @@ marker`, or only from an explicit `@@` on the operand itself? (In §3a the events
   inherit position from their scene's `@@`; if inheritance isn't implemented, that may be the root cause.)
3. What are the intended three-valued semantics for `before`/`after` across a **fork** (incomparable branch
   tips) and a **`[+Loop]`** (mutually reachable markers)?
4. Should a `before`/`after` whose operands have **no** resolvable story-time position evaluate to false
   (reject) rather than pass? (§3b suggests it currently passes.)
