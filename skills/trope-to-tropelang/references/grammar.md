# TropeLang v1.3 Grammar Reference

**Status key**
- ✓ implemented in the reference Rust parser (lib.rs v1.1)
- ◎ planned — accepted by the Python validator, pending Rust parser update

---

## File structure

A `.trl` file has sections in this order:

```
// 1. PREAMBLE         — @directives
// 2. IMPORTS          — import / ref statements
// 3. DECLARATIONS     — attr / prop / state / verb / rel (prelude extensions)
// 4. CONCEPTS         — concept declarations (abstract graph nodes)
// 5. CAST & LOCATIONS — entity declarations with // annotations
// 6. IMPLY            — runtime ontological implications
// 7. RULES            — rule { when: ... then: ... }
// 8. SCENES           — scene / beat / act / arc blocks
```

### Preamble directives (✓ — comment convention)

```trl
// @title   My Story — Scene One
// @trope   HiddenIdentity, TheReveal
// @source  https://allthetropes.org/wiki/Hidden_Identity
// @version 1.2
// @no-prelude          // opt out of the standard library
```

### Annotations (✓ — comment convention)

Place a `//` comment on the line immediately above a declaration to provide its screenplay/human-readable display form:

```trl
// STRIDER / ARAGORN, SON OF ARATHORN
char aragorn [+Ranger]

// INT. THE PRANCING PONY — NIGHT
set prancing_pony [+Interior] [#Night]
```

**Do not use sidecar labels** — the grammar allows `char aragorn "Aragorn"` but this format deprecates it. Display forms belong in `//` annotations only.

---

## Import system ◎

```trl
import "trl/prelude.trl"               // bring all attrs, props, states, verbs, rels into scope
import "tolkien/entities.trl"          // bring entity declarations into scope
import "tropes/hidden_identity.trl"    // bring rules into scope

ref aragorn from "tolkien/entities.trl"   // selective — one entity only
ref Hobbit  from "tolkien/races.trl"      // selective — one attr only
```

`import` brings `attr`, `prop`, `state`, `verb`, `rel`, entity declarations, and `imply` statements into scope. `rule` and `scene` blocks are not imported. `ref` imports a single named declaration.

The prelude (`trl/prelude.trl`) is in scope automatically unless `// @no-prelude` is set.

---

## Declaration forms

### Entity types (✓ except `concept` ◎)

Entities are the nodes of the graph. All declarations may have a `//` annotation above them and zero or more tags.

```trl
char    name [tags...]   // character / person
obj     name [tags...]   // physical object
evt     name [tags...]   // event / story beat
set     name [tags...]   // setting / location
arc     name [tags...]   // narrative arc
concept name [tags...]   // abstract entity — idea, force, theme, condition  ◎
```

`scene`, `act`, `beat` are also valid node types in pattern position (when not followed by `{`).

**`concept` declarations** ◎

Concepts are abstract graph nodes — things that have no physical form but that characters, events, and relationships can be directed toward. Every concept must be declared before use; no floating string references.

```trl
// The state of not achieving an intended goal.
// Often precedes growth, revelation, or collapse. May be temporary or permanent.
concept failure      [%Timeless] [+Inevitable]

// The condition of being left without support, connection, or witness.
concept abandonment  [%Timeless] [#Painful]

// An internalized code that governs conduct; may conflict with survival or desire.
concept honor        [%Timeless] [+Aspirational] [+Fragile]
```

The `//` annotation above a concept is its **definition** — a natural-language description that makes the concept self-contained. Per the Darmok principle, TropeLang must not require cultural knowledge: if you reference it, you define it.

Concepts may be:
- Targets of `[~Intent]` tags: `gollum [~Desires(target=power)]`
- Endpoints of edges: `power -- corruption : "Leads To"`
- Matched in rule patterns: `char $c [~Devoted_To(target=honor)]`
- Tagged with any prelude attribute: `concept freedom [%Timeless] [+Paradoxical]`

### Attribute types ◎

Attribute declarations define the vocabulary used in tags. All inherit from the meta-hierarchy using `+` in declarations.

```trl
attr Name [+Parent]             // meta-hierarchy node — the type system itself
prop Name [+Group]              // stable entity attribute (adjective / noun)
state Name [+Group]             // mutable condition — added and removed by rules
verb  Name(param, ...) [+Group] // action descriptor — what an event does
rel   Name(param, ...) [+Group] // relationship type — how entities connect via edges
```

In declarations, `+` always means "is-a" (inheritance). The new sigils (`#`, `@`, `&`) are for usage only.

**Examples:**
```trl
attr Kinship              [+Kind]
prop Mortal               [+Ontological]
state Grieving            [+Psychological]
verb Betrayed(other)      [+Interpersonal]
rel Parent_Of(child)      [+Kinship]
```

---

## Tag sigils ◎

Tags attach attributes to entities, events, or edges. The sigil encodes the **ontological domain** of the attribute — what kind of thing it is — so the reader knows immediately without consulting the declaration.

### The seven sigils

| Sigil | Domain | Used for |
|---|---|---|
| `[=Name]` | Body / Physical | vital, embodied, material attributes |
| `[#Name]` | Mind / Psychological | cognitive, emotional, inner-life attributes |
| `[%Name]` | Essence / Ontological | fundamental nature; what something IS at its deepest level |
| `[~Name]` | Intent / Directed | psychological orientation *toward* a target (entity or concept) |
| `[@Name]` | Rel / Structural | bilateral bond between two graph nodes |
| `[&Name]` | Verb / Action | descriptor on event nodes — what this event does |
| `[+Name]` | Prop / Generic | narrative, social, spatial attributes that don't fit body/mind/essence |

```trl
char eleanor [+Elder] [%Mortal]               // generic prop; essence prop
eleanor [=Ill] [=Wounded]                     // body attributes
eleanor [#Grieving] [#Devoted]                // mind attributes
eleanor [%Fallen]                             // essence — what she has become
eleanor [~Fears(target=abandonment)]          // directed toward a concept
eleanor [@Parent_Of(child=ruth)]              // structural bond
evt ceremony [&Initiated(into=the_order)]     // verb on an event
```

**The Darmok principle applies to targets:** every identifier used as a `[~Intent]` target must be a declared graph node — a `char`, `obj`, `evt`, `set`, `arc`, or `concept`. Quoted strings are not valid targets.

```trl
// WRONG — floating string
eleanor [~Fears(target="being forgotten")]

// RIGHT — declared concept
concept being_forgotten [%Timeless] [#Painful]
eleanor [~Fears(target=being_forgotten)]
```

### Mutation operators (✓)

These work on any tag regardless of sigil. The domain type is inferred from the declaration.

| Operator | Meaning |
|---|---|
| `[=Name]` / `[#Name]` / etc. | Add (sigil = add + domain) |
| `[-Name]` | Remove — domain inferred from declaration |
| `[?Name]` | Query / test presence |
| `[!Name]` | Assert absent |

```trl
frodo [=Alive]          // add body attribute Alive
frodo [-Alive]          // remove Alive — type inferred: body
frodo [?Knows]          // test: does frodo have Knows?
frodo [!Dead]           // assert frodo does not have Dead
```

### Parameters (✓)

```trl
[+DeadlyFear(target="Snakes")]
[+MotivatedBy(emotion="Grief", source="Uncle Owen")]
[@Parent_Of(child=ruth)]
[&Betrayed(other=frodo)]
[+Lineage(id=dunedain, hidden=true)]
```

Param values: strings `"text"`, numbers `42`, booleans `true`/`false`, variables `$x`, identifiers, lists `[a, b]`.

### Variable tags (✓ — in rule patterns)

```trl
rule TriggerFear {
  when:
    char $c [+DeadlyFear(target=$threat)]
    obj $o [+$threat]                       // variable as tag name
    $c [#Afraid]
  then:
    $c [#Panicking]
}
```

The sigil before `$var` signals the expected type:
```trl
char $elder [+Elder]              // expect a prop
$elder [#Grieving]                // expect a state
char $x [@Parent_Of(child=$y)]    // expect a rel binding
evt $e [&Betrayed(other=$z)]      // expect a verb
```

---

## Edge operators (✓)

Edges express structural relationships between entities.

| Operator | Meaning |
|---|---|
| `>` | Possession / control / dominance |
| `!>` | No longer possesses |
| `--` | Neutral bond / relationship |
| `!--` | Bond severed |
| `->` | Event causes / involves (causal chain) |
| `@` | Presence at location or scene |
| `!@` | Departure / absence |
| `><` | Symmetric conflict / mutual action |

**Edge syntax:**
```trl
lhs op rhs [: "label"] [tags...]

// Examples:
luke > lightsaber                            // possession
luke -- obiwan : "Apprentice"               // bond with label
evt duel -> obiwan >< vader : "Final"       // causal chain
frodo @ prancing_pony                        // presence
frodo !@ shire                               // departed
```

**Causal chain pattern:**
```trl
evt $e -> $agent > $target : "Label"
// event $e involves $agent acting on $target
```

---

## Scope blocks (✓)

```trl
arc "The Heist" {
  scene "Setup" {
    beat 1 {
      char alice [+Thief]
    }
    beat 2 {
      evt breach -> alice > vault
    }
  }
}
```

Scope names: identifiers, numbers, or quoted strings.

**Convention:** declare entities at the top level; keep scope blocks flat (references and edges only, no multi-tag declarations inside beats).

---

## Ontological implications (✓)

```trl
imply Sword    -> [Weapon, Sharp, Melee]
imply Mentor   -> [Ally, AuthorityFigure]
imply Hobbit   -> [SmallFolk, Resilient, Earthy]
```

Runtime: when an entity has the LHS tag, it implicitly also has all RHS tags. Distinct from `attr` inheritance (static typing). Use `imply` for runtime inference; use declaration inheritance (`[+Parent]`) for the type hierarchy.

---

## Rules (✓)

```trl
rule RuleName {
  unique: true             // optional — fires at most once globally
  when:
    // pattern conditions
  then:
    // actions
}
```

### Conditions (✓)

```trl
char $hero [+TheHero]               // entity with tag
$hero -- $mentor : "Guides"         // edge condition
not ($hero [#Dead])                 // negation
not ($hero -- $villain : "Trusts")  // negated edge
count(char $v [#Hostile]) >= 3      // quantifier
beat + 2 { $hero [#Wounded] }       // N beats later
past scene $s { evt $e -> ... }     // historical lookup
$hero != $mentor                    // inequality
$hero == $chosen                    // equality
```

### Actions (✓)

```trl
$hero [+TheHero]                    // add prop
$hero [#Transformed]                // add state
$hero [-Grieving]                   // remove state
$hero -- $mentor : "Guides"         // create edge
$hero !-- $enemy : "Friends"        // sever edge
print "Message"                     // log output
surface(id="x", title="T", description="D", reward_xp=100)
surface_global(title="T", description="D")
surface(target=$char, message="M")
surface(target=[$p1, $p2], message="M")
foreach char $p in $group { ... }
foreach char $p (where $p != $hero) { ... }
```

---

## Epistemic wrappers ✓

Wrap any statement to declare its epistemic status. The wrapper is the outermost decoration.

| Wrapper | Level | Meaning |
|---|---|---|
| `!statement!` | Absolute | Narrator ground truth — incontestable, survives any perspective slice |
| `statement` | Asserted | Default — narrator says it is true |
| `*statement*` | Contingent | True but interpretation is perspective-dependent |
| `?statement?` | Latent | In the graph but unsurfaced — no character is aware |

```trl
!aragorn [+Heir_of_Isildur]!           // absolute — cannot be retconned
aragorn [+Alias(name="Strider")]       // asserted — narrator truth, default
*aragorn [+Trustworthy]*               // contingent — some characters read it differently
?aragorn -- arwen : "Betrothed"?       // latent — nobody in this scene knows

// Composition: absolute AND latent — definitely true, currently hidden
!?aragorn [+Heir_of_Isildur]?!        // (outer wrapper wins for serialization)
```

---

## Ambiguity expressions ✓

Mark facts that are genuinely unresolved — not just hidden, but unknown even to the narrator.

```trl
// Closed — exactly one of these is true
(player_a [+Trustworthy] | player_a [+Dangerous])

// Semi-open — one of these, or something not yet named
(item [+Bribe] | item [+Gift] | ...)

// Tentative — might be this; alternatives unnamed
(player_c [@Witness_To(encounter)])

// Void — something is ambiguous here; no candidates yet
(...)
```

**Naming for later resolution:**
```trl
(item [+Bribe] | item [+Gift] | ...) as item_nature
?(player_b [+DoubleAgent] | player_b [+Innocent]) as b_loyalty?
```

**Composing with epistemic wrappers:**
```trl
*(aragorn [+Trustworthy] | aragorn [+Dangerous] | ...)* as strider_nature
?(...)? as aragorn_kingship                            // latent void
!(player_c [@Witness_To(enc)] | player_c [#Oblivious])!  // absolute but unresolved
```

**Pipe `|` is terminal-free:** branches are separated by `|`; `...` (if present) is always last.

---

## Resolution ✓

> **Normative constraint (parser-enforced).** `resolve` / `retcon` may target **only a
> named ambiguity** (`( … ) as <name>`). Collapsing a non-ambiguity, or an ambiguity
> wrapped `!…!` (absolute facts are immutable), is a `grammar` validation error. `retcon`
> exists to settle ambiguities, not to rewrite arbitrary past facts. See `01 §11.4`.

### In-world disambiguation — `resolve`

Inside a scene beat: a narrative event collapses a named ambiguity.

```trl
scene gandalf_letter {
  beat 1 {
    evt read -> frodo @ letter
    resolve strider_nature -> aragorn [+Trustworthy]
    resolve strider_intent -> aragorn -- frodo : "Will Guide Safely"
    frodo [-Perceives(target=aragorn, as=strider)]
    frodo [+Knows(target=aragorn)]
  }
}
```

`resolve` can collapse to a concrete fact OR narrow to a smaller ambiguity:
```trl
resolve aragorn_kingship -> *(aragorn [+Rightful_King] | aragorn [+Exile] | ...)*
// void → semi-open: candidates emerge but aren't yet settled
```

### Author retcon — `retcon`

Outside scenes: author goes back across books/files and collapses earlier ambiguities.

```trl
// @retcons book_1.trl
retcon {
  item_nature    -> item [+Warning]
  b_loyalty      -> player_b [+DoubleAgent]
  c_saw_meeting  -> player_c [#Oblivious]     // new reading — not in original candidates
}
```

`retcon` can introduce readings not listed in the original ambiguity (if the expression was semi-open or void). Closed expressions `(A | B | C)` require choosing from the listed alternatives.

---

## Player interaction (✓)

### `prompt` — player chooses an interpretation

```trl
prompt(
  target   = $witness
  question = "What did you see?"
  choices  = {
    "An alliance." : {
      $a -- $b : "Allies"
    }
    "A betrayal." : {
      $a [+Path_Corruption]
    }
  }
)
```

### `fork` — timed, triggered by in-world events

```trl
fork(
  target   = $player
  duration = 15
  ui_text  = "The clock is ticking..."
  branches = {
    "Intervene" : {
      triggers = [ evt $act -> $player > $enemy ]
      apply    = { $player [+Stance_Decisive] }
    }
    "Wait" : {
      triggers = [ ui_click(2) ]
      apply    = { $player [#Hesitant] }
    }
  }
  timeout_apply = {
    $player [#Paralyzed]
  }
)
```

---

## Identity and perception pattern ◎

The canonical way to model hidden identity and perspective disambiguation:

```trl
// Identity layer — top level, narrator truth
char aragorn [+Alias(name="Strider")]
aragorn [+Heir_of_Isildur]              // true regardless of who knows

// Perception layer — in scene, on the observer
frodo [+Perceives(target=aragorn, as=strider)]
*(aragorn [+Trustworthy] | aragorn [+Dangerous] | ...) as strider_nature*

// Disambiguation event
resolve strider_nature -> aragorn [+Trustworthy]
frodo [-Perceives(target=aragorn, as=strider)]
frodo [+Knows(target=aragorn)]
```

**Identity** lives at the top level (narrator ground truth, unchanged by character beliefs).
**Perception** lives in scene blocks as contingent or ambiguous facts on the *observer*, not the observed.

---

## Canonical form rules (✓ — serializer)

- Two-space indent inside blocks
- Tags serialized without space between modifier and name: `[+Name]`, `[#Name]`
- Edge chains on one line when short: `evt e -> agent > target : "Label"`
- `not (inner)` always parenthesized
- Commas between statements are optional; canonical form omits them
- `//` comments preserved in source, stripped during parsing
