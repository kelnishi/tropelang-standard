# TropeLang Standard Corpus

The canonical TropeLang corpus — the **publishable unit** and the **template** for a custom corpus.
Recognized by the [TropeLang engine](https://github.com/kelnishi/TropeLang); served to the editor as a
runtime bundle (spec 19).

## What's essential vs. helper
- **`trl/`** — **the corpus**. Prelude, ontology, modules, concepts, tropes, and `trl/tropes/corpus.toml`.
  **This is the only thing required to publish**, and the only thing a consumer loads. A fork starts here.
- `skills/trope-to-tropelang/` — the conversion skill: an **authoring helper**, *not* part of the
  publishable corpus.
- `STYLE.md` · `trl/tropes/BACKLOG.md` — authoring conventions + the trope worklist.

## Authoring
Install the engine CLI, then work from the repo root (the CLI loads the corpus by URL — `--corpus file://trl`):
```sh
cargo install tropelang-cli          # release
# cargo install --git https://github.com/kelnishi/TropeLang tropelang-cli   # pre-release

tropelang gate trl/tropes/<bucket>/<name>.trl    # preamble · validates · round-trips · DRY · drams
tropelang assemble trl/tropes/corpus.toml        # regenerate trl/tropes/index.trl after add/remove
tropelang shape <file> --why                     # recognition provenance
```
See `skills/trope-to-tropelang/SKILL.md` for the full conversion workflow.

## Fork your own corpus
Copy `trl/tropes/corpus.toml`, set `base` to this repo's standard, point `tropes` at your tree, and add
`strike = [...]` to drop inherited tropes. The override/strike model is in engine spec `19`; the cleave is
spec `22`.

## Publishing (Phase 4)
A tagged release runs `tropelang bundle trl/tropes/corpus.toml` and publishes the immutable
`corpus.json` + `manifest.json` to the CDN, behind a review-gated environment (the CF deploy credential
is never exposed to PR code). See the publish workflow.

## Contributing
Open Issues (trope requests, corrections) and PRs (new tropes, founding fixes). CI gates every PR with
no secrets; a maintainer reviews via CODEOWNERS.
