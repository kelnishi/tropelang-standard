# TropeLang Standard Corpus

The canonical TropeLang corpus — the **publishable unit** and the **fork template** for a custom corpus.
Recognized by the [TropeLang engine](https://github.com/kelnishi/TropeLang); served to editors at
**https://corpus.tropelang.com**.

## How to use this repo

### 1. Load this corpus into an editor
Point a TropeLang editor at any one of these — all three resolve to the same corpus
(see **[PUBLISHING.md](PUBLISHING.md)** for the format spec):

- **Published bundle** *(recommended)* — a `corpus.json` URL. The standard corpus:
  `https://corpus.tropelang.com/standard/resolve?channel=stable`. One cached fetch, `sha256`-checked.
- **Tarball** — a `.tar.gz` archive URL of this repo (or a fork); fetched and unpacked client-side.
- **Naked files** — a **`corpus.toml`** URL, e.g.
  `https://raw.githubusercontent.com/kelnishi/tropelang-standard/main/trl/tropes/corpus.toml`. The editor
  reads it, follows `index.trl`, and pulls each `.trl` relative to it. No build step.

### 2. Fork & publish your own corpus
Zero infra — GitHub Pages, no Cloudflare, no secrets. Three steps, then every push republishes:

1. **Fork** this repo. In your fork, enable **Settings → Actions**, and set **Settings → Pages → Source →
   "GitHub Actions"**.
2. **Edit** `trl/tropes/corpus.toml` (set your own `id`, bump `version`) and add / edit / `strike` tropes
   under `trl/`.
3. **Push to `main`** → `pages.yml` bundles and deploys to `https://<you>.github.io/<repo>/`. Point an
   editor at that (per §1). Or skip publishing entirely and point the editor at your fork's raw
   `corpus.toml` (naked-files mode).

Other platforms (GitLab, Netlify, S3, …) and the full contract are in **[PUBLISHING.md](PUBLISHING.md)** —
it's just `tropelang bundle` + CORS-served static files.

### 3. Author / contribute tropes
Install the engine CLI (prebuilt binary), then work from the repo root (the CLI loads the corpus by URL):
```sh
curl -fSL https://github.com/kelnishi/tropelang-standard/releases/latest/download/tropelang-x86_64-linux \
  -o ~/.local/bin/tropelang && chmod +x ~/.local/bin/tropelang

tropelang gate trl/tropes/<bucket>/<name>.trl    # preamble · validates · round-trips · DRY · drams
tropelang assemble trl/tropes/corpus.toml        # regenerate trl/tropes/index.trl after add/remove
tropelang shape <file> --why                     # recognition provenance
```
Open **Issues** (trope requests, corrections) and **PRs** (new tropes, founding fixes). CI gates every PR
with no secrets; see `skills/trope-to-tropelang/SKILL.md` for the full conversion workflow.

## What's essential vs. helper
- **`trl/`** — **the corpus**. Prelude, ontology, modules, concepts, tropes, and `trl/tropes/corpus.toml`.
  **The only thing required to publish**, and the only thing a consumer loads. A fork starts here.
- `skills/trope-to-tropelang/` — the conversion skill: an **authoring helper**, *not* part of the
  publishable corpus.
- `STYLE.md` · `trl/tropes/BACKLOG.md` — authoring conventions + the trope worklist.
- `worker/` · `.github/workflows/{publish,promote}.yml` — the upstream's Cloudflare publish path (see
  *Maintaining*, below); forks ignore these and use `pages.yml` (§2).

The override/strike fork model is in engine spec `19`; the repo cleave is spec `22`.

## Maintaining the standard corpus (upstream only)
This repo publishes to **corpus.tropelang.com** (Cloudflare R2 + the Worker in `worker/`). Forks need
none of this — they use `pages.yml` (§2).

- **Publish a version:** run the **Release** action (Actions → *Release* → `point`/`minor`/`major`). It
  opens a bot-authored PR that bumps `version`, syncs `--expect-tropes` to the live count, and rolls up
  `CHANGELOG [Unreleased]`. **Approve + merge** → `auto-tag.yml` tags `corpus-v<version>` → `publish.yml`
  bundles + uploads the immutable version + regenerates the registry → **approve the `production`
  deployment**. (It does **not** move `stable`.) Manual fallback: bump `corpus.toml` + `--expect-tropes`,
  merge, then `git tag corpus-v<version> && git push origin corpus-v<version>`.
- **Promote / rollback:** edit `channels/standard.stable.json` to an already-published version → merge.
  `promote.yml` repoints within ~30 s (the channel TTL); rollback points back at a prior, still-immutable
  version.
- **Verify:** `curl -i https://corpus.tropelang.com/registry.json` (and `/standard/resolve?channel=stable`).
- **Infra:** R2 bucket `tropelang-corpus`; deploy the Worker with `cd worker && npx wrangler deploy`. The
  `production` environment (required reviewer) holds `CLOUDFLARE_ACCOUNT_ID` + `R2_ACCESS_KEY_ID` +
  `R2_SECRET_ACCESS_KEY` — a bucket-scoped R2 token used over the S3 API. The `publish.yml` / `promote.yml`
  headers document the security model.
