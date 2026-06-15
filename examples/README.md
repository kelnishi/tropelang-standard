# Example stories

Standalone **story** files (`.trl`) — narratives, not tropes. Each carries a cast, scenes, beats, and
events but **no `rule`**: they exist to be read by the engine's `drams` tool, which overlays the full trope
corpus and reports which tropes actually **fire** on the story.

```sh
tropelang drams examples/theogony_succession.trl          # coverage signal
tropelang shape examples/theogony_succession.trl --corpus file://trl   # the tropes recognized
```

Each story does `import "trl/tropes/index.trl"`, so it is self-contained: it pulls in the whole vocabulary
and the trope overlay at once.

## Why these stories — the culture-balance set

The corpus's worked examples (trope vignettes and the engine's eval stories) lean **Western and
secular/Christian-adjacent** — Star Wars, Shakespeare, comic books. That makes one culture read as the
unmarked *default* and everything else as the exception. These stories deliberately ground the **same
recognizable patterns** in different religious and mythological traditions, so no single culture is the
baseline. (Phase 1 of the culture initiative — see `trl/tropes/BACKLOG.md`.)

| Story | Tradition | Patterns it exercises |
|---|---|---|
| `theogony_succession.trl` | Greek (Hesiod's *Theogony*) | the usurping heir, the self-fulfilling prophecy, the hidden child who returns to claim the throne |
| `the_passion.trl` | Christian (the Gospels) | the trusted intimate who betrays, the willing sacrifice for others, death and resurrection |
| `amaterasu_and_the_cave.trl` | Shinto (the *Kojiki*) | the sibling's offense, the god who withdraws, the clever lure (laughter and a mirror) that restores the world |

All three draw on **public-domain** source material.

### A note on coverage

The Greek and Christian stories fire a healthy spread of tropes; the Shinto story fires fewer. That gap is
*informative*, not a defect — the corpus underserves a withdrawal-and-restoration myth shape that isn't
foregrounded in Western story. It is exactly the kind of signal that drives later phases of the initiative
(diversifying vignettes; adding myth-grounded tropes such as a dying-and-rising god or a psychopomp).
