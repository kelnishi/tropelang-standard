# Worked Trope Mappings

Four complete examples in the updated `.trl` format. Each demonstrates: preamble, screenplay-annotated cast list, ontology, abstract rule, and a concrete vignette. All are valid against the current v1.1 grammar.

---

## 1. MacGuffin (simple rule)

**Laconic**: An object whose only narrative function is to be pursued and transferred — its actual nature is irrelevant.

**Modeling notes**: The MacGuffin pattern is purely about transfer of possession. Tags are applied retroactively when the transfer fires. No concrete character names needed in the abstract rule; the vignette instantiates it.

```trl
// @trope   MacGuffinDelivery
// @source  https://allthetropes.org/wiki/MacGuffin
// @version 1.1


// === CAST & LOCATIONS ===

// THE GIVER
char giver

// THE RECEIVER
char receiver

// THE ITEM
obj item


// === RULES & SCENES ===

rule MacGuffinDelivery {
  when:
    char $giver
    char $receiver
    obj $item
    $giver > $item
    $giver -- $receiver : "Meets"
    evt $transfer -> $receiver > $item
  then:
    $item [+MacGuffin]
    $receiver [+TheHero]
    $transfer [+CallToAdventure]
}

// --- concrete: Pulp Fiction ---

// VINCENT VEGA
char vincent [+Antagonist] [+Hired]

// BUTCH COOLIDGE
char butch [+Protagonist]

// INT. MARSELLUS WALLACE'S BRIEFCASE - UNKNOWN
obj briefcase [+MacGuffin] [+Glowing]

// THE DROP
evt handoff -> butch > briefcase : "Receives"

scene the_drop {
  beat 1 {
    vincent > briefcase
    vincent -- butch : "Meets"
  }
  beat 2 {
    handoff
    briefcase [+MacGuffin]
    butch [+TheHero]
    handoff [+CallToAdventure]
  }
}
```

---

## 2. Chekhov's Gun (two-rule arc)

**Laconic**: An object introduced early must be used meaningfully later; if it won't be used, don't introduce it.

**Modeling notes**: Requires two rules — setup (gun noticed, not yet used) and payoff (gun fired). An `arc` entity carries the obligation forward between beats. `not(...)` in the setup ensures the rule only fires when the item hasn't been used yet.

```trl
// @trope   ChekhovsGun
// @source  https://allthetropes.org/wiki/Chekhov%27s_Gun
// @version 1.1


// === CAST & LOCATIONS ===

// THE CHARACTER
char character

// THE ANYONE
char anyone

// THE ITEM
obj item [+Lethal]

// THE TRACKER ARC
arc tracker


// === RULES & SCENES ===

rule ChekhovsGun_Setup {
  when:
    scene $current
    obj $item [+Lethal]
    evt $intro -> $character > $item : "Notices"
    not ($item -> $anyone : "Used")
  then:
    arc $tracker
    $tracker > $item
    $tracker [+PendingPayoff(item=$item)]
}

rule ChekhovsGun_Fired {
  when:
    arc $tracker [+PendingPayoff(item=$item)]
    evt $action -> $character > $item : "Attacks"
  then:
    $tracker [-PendingPayoff]
    $tracker [+Resolved]
    $action [+DramaticClimax]
}

// --- concrete: No Country for Old Men ---

// ANTON CHIGURH
char anton [+Villain] [+Relentless]

// LLEWELYN MOSS
char llewelyn [+Protagonist]

// THE CATTLE GUN
obj cattle_gun [+Lethal] [+Pneumatic]

// INT. MOTEL ROOM - NIGHT
set motel [+Interior] [+Night]

arc cattle_gun_arc
cattle_gun_arc > cattle_gun

scene introduction {
  beat 1 {
    evt notice -> llewelyn > cattle_gun : "Notices"
    cattle_gun_arc [+PendingPayoff(item=cattle_gun)]
  }
}

scene payoff {
  beat 1 {
    anton @ motel
    evt attack -> anton > llewelyn : "Attacks"
    cattle_gun_arc [-PendingPayoff]
    cattle_gun_arc [+Resolved]
    attack [+DramaticClimax]
  }
}
```

---

## 3. Heel Face Turn (with subversion)

**Laconic**: A villain switches allegiance and joins the heroes, usually through a moment of moral awakening.

**Modeling notes**: Two rules — the genuine turn and the faked turn (long con). `past` in the subversion rule checks whether a foreshadowing clue existed earlier. The `!--` / `--` pair severs the enmity bond and replaces it. Concrete vignette uses Zuko's arc from Avatar, split across two scenes.

```trl
// @trope   HeelFaceTurn
// @source  https://allthetropes.org/wiki/Heel_Face_Turn
// @version 1.1


// === CAST & LOCATIONS ===

// PRINCE ZUKO
char zuko [+Heel] [+Path_Corruption]

// AANG
char aang [+TheHero] [+InMortalDanger]

// PRINCESS AZULA
char azula [+Villain]

// INT. THE CRYSTAL CATACOMBS - NIGHT
set catacombs [+Interior] [+Underground] [+Night]

// INT. THE WESTERN AIR TEMPLE - DAY
set air_temple [+Interior] [+Ruined] [+Day]

// ZUKO'S REDEMPTION ARC
arc redemption


// === ONTOLOGY ===

imply Heel -> [Villain, Antagonist, Untrustworthy]
imply Face -> [Ally, Trustworthy, Redeemed]


// === RULES & SCENES ===

rule Trope_HeelFaceTurn {
  when:
    char $turncoat [+Heel]
    char $hero [+TheHero] [+InMortalDanger]
    $turncoat -- $hero : "Enemies"
    evt $moment -> $turncoat @ $hero : "Witnesses"
    not ($turncoat [+Face])
  then:
    $turncoat [-Heel]
    $turncoat [+Face]
    $turncoat [+Path_Redemption]
    $turncoat !-- $hero : "Enemies"
    $turncoat -- $hero : "Uneasy Allies"
    $moment [+RedemptionArc]
    surface_global(title="A Change of Heart", description="$turncoat has switched sides!")
}

rule Trope_HeelFaceTurn_Faked {
  when:
    char $infiltrator [+Heel] [+Face] [+Path_Redemption]
    char $hero [+TheHero]
    evt $reveal -> $infiltrator > $hero : "Betrays"
    scene $current [+Endgame]
    past scene $earlier {
      evt $signal -> $infiltrator @ char $handler : "Secret Contact"
    }
  then:
    $infiltrator [-Face]
    $infiltrator [-Path_Redemption]
    $infiltrator [+Path_Corruption]
    $infiltrator -- $hero : "Enemies"
    $reveal [+LongCon]
    surface_global(title="It Was All a Lie", description="$infiltrator was never truly redeemed.")
}

// --- concrete: Avatar - Zuko's Arc ---

scene catacombs_choice {
  beat 1 {
    zuko @ catacombs
    aang @ catacombs
    zuko -- aang : "Enemies"
    evt choice -> zuko @ aang : "Witnesses"
    zuko [+Status_AtCrossroads]
  }
  beat 2 {
    evt betrayal -> zuko > azula : "Sides With"
    redemption [+PendingPayoff(item=zuko)]
  }
}

scene air_temple_turn {
  beat 1 {
    zuko @ air_temple
    aang @ air_temple
    evt turn -> zuko @ aang : "Offers Help"
    zuko [-Heel]
    zuko [+Face]
    zuko [+Path_Redemption]
    zuko !-- aang : "Enemies"
    zuko -- aang : "Uneasy Allies"
    redemption [-PendingPayoff]
    redemption [+Resolved]
    turn [+RedemptionArc]
  }
}
```

---

## 4. The Mentor's Death (unique rule + fork)

**Laconic**: The wise guide is killed, forcing the hero to act independently and catalyzing their transformation.

**Modeling notes**: `unique: true` — the mentor dies once. A `fork` captures the hero's response (vengeful vs. resolute), which is the trope's most narratively rich moment and prime training signal for outcome prediction. Tags on the hero encode which path was chosen.

```trl
// @trope   MentorDeath
// @source  https://allthetropes.org/wiki/Mentor_Occupational_Hazard
// @version 1.1


// === CAST & LOCATIONS ===

// THE HERO
char hero [+TheHero] [+Mentored] [+Alive]

// THE MENTOR
char mentor [+Mentor] [+Alive]

// THE VILLAIN
char villain [+Villain]

// EXT. THE THRESHOLD - NIGHT
set threshold [+Exterior] [+Night] [+Liminal]


// === ONTOLOGY ===

imply Mentor -> [Ally, AuthorityFigure, Knowledgeable, Mortal]


// === RULES & SCENES ===

rule Trope_MentorDeath {
  unique: true
  when:
    char $hero [+TheHero] [+Mentored]
    char $mentor [+Mentor] [+Alive]
    char $villain [+Villain]
    $mentor -- $hero : "Guides"
    evt $sacrifice -> $mentor > $villain : "Confronts"
    beat + 1 {
      not ($mentor [+Alive])
    }
  then:
    $mentor [-Alive]
    $mentor [+Fallen]
    $hero [-Mentored]
    $hero [+Path_Independent]
    $sacrifice [+HeroicSacrifice]
    fork(
      target = $hero
      duration = 20
      ui_text = "Your mentor is gone. What drives you now?"
      branches = {
        "Rage (Vengeful)" : {
          triggers = [ ui_click(1) ]
          apply = {
            $hero [+Archetype_Avenger]
            $hero -- $villain : "Sworn Enemy"
          }
        }
        "Purpose (Resolute)" : {
          triggers = [ ui_click(2) ]
          apply = {
            $hero [+Archetype_Champion]
            $hero [+Path_Heroic]
          }
        }
      }
      timeout_apply = {
        $hero [+Status_Grief_Stricken]
      }
    )
    surface_global(title="The Mentor Falls", description="$mentor is gone. $hero stands alone.")
}

// --- concrete: Star Wars - A New Hope ---

// LUKE SKYWALKER
char luke [+TheHero] [+Mentored] [+Alive]

// OBI-WAN KENOBI
char obiwan [+Mentor] [+Alive]

// DARTH VADER
char vader [+Villain]

// INT. DEATH STAR CORRIDOR - NIGHT
set death_star_corridor [+Interior] [+Night] [+Hostile]

obiwan -- luke : "Guides"

scene death_star_duel {
  beat 1 {
    obiwan @ death_star_corridor
    vader @ death_star_corridor
    luke @ death_star_corridor
    evt duel -> obiwan >< vader : "Lightsaber Duel"
  }
  beat 2 {
    evt sacrifice -> obiwan > vader : "Lets Go"
    obiwan [-Alive]
    obiwan [+Fallen]
    luke [-Mentored]
    luke [+Path_Independent]
    sacrifice [+HeroicSacrifice]
  }
}
```

## Stats & a combat round (`^`) — Game-Master mode

Stat declarations, a logged roll, a harness-computed check outcome, a threshold
rule, and — deliberately — a canonical out-of-range value (goblin HP driven to
`-2`, below the implicit `min` of `0`; the engine accepts it and `DropsAtZero`
fires, no clamping).

```trl
// @title   Goblin Ambush — combat round
// @version 1.3

stat HP [+Vital]
stat AC [+Defense]
verb Rolled(dice, result)     [+Mechanical]
verb Check(stat, dc, outcome) [+Mechanical]

char tharion [+Protagonist] [+Fighter]
tharion [^HP(cur=24, max=30)]
tharion [^AC=18]

char goblin [+Antagonist] [+Minion]
goblin [^HP(cur=7, max=7)]
goblin [^AC=15]

// a combatant brought to 0 or below drops — stat-vs-literal threshold
rule DropsAtZero {
  when:
    char $c [^HP <= 0]
  then:
    $c [#Downed]
    surface(target=$c, message="goes down")
}

scene round_1 {
  beat 1 {
    // harness rolled the attack, compared total vs goblin AC 15 -> hit
    evt swing -> tharion >< goblin : "Greataxe"
    swing [&Rolled(dice="1d20", result=17)]
    swing [&Check(stat="attack", dc=15, outcome="hit")]
    // harness computed 7 - 9 = -2 and wrote the concrete value; -2 is below
    // min=0 but canonical — the engine does not clamp; DropsAtZero then matches
    goblin [^HP = -2]
  }
}
```
