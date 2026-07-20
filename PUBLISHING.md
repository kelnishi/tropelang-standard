# Publishing a TropeLang corpus

A corpus is consumed by the editor/engine as a **bag of files** — `[{ "path", "source" }, …]`, exactly
what the engine's `load_corpus()` takes. "Publishing" just means making that bag fetchable. There's a
turnkey GitHub path and a platform-neutral contract underneath it; both produce the same thing.

---

## Quickstart — fork & publish on GitHub Pages (no Cloudflare, no secrets)

Three steps, then every push republishes:

1. **Fork** this repo. In your fork: **Settings → Actions** → enable workflows, and **Settings → Pages →
   Source → "GitHub Actions"**.
2. **Edit the corpus** — `trl/tropes/corpus.toml` (set your own `id`, bump `version`) and add / edit /
   `strike` tropes under `trl/`.
3. **Push to `main`.** `pages.yml` bundles your corpus and deploys it to
   `https://<you>.github.io/<repo>/`. Point the editor there.

The channel pointer and `registry.json` are **derived from `corpus.toml`** — you never hand-edit
`channels/`. (The Cloudflare workflows here are upstream-only; your fork ignores them.)

---

## The contract (any platform)

A published corpus is the output of one command hosted as static files:

```
tropelang bundle trl/tropes/corpus.toml --out <dir>/<id>/<version>
# → <dir>/<id>/<version>/corpus.json     the bundle ([{path,source}], canonical, sha256-stable)
# → <dir>/<id>/<version>/corpus.trlb     post-parse AST binary (engine spec 24) — the fast-load form
# → <dir>/<id>/<version>/manifest.json   spec-19 metadata (id, version, engineMin, sha256, trlbSha256, …)
```

`corpus.trlb` is the same file set as `corpus.json`, pre-parsed, so an eval engine / game loads it with no
parsing (~2.7× smaller uncompressed; pinned by `trlbSha256`). `corpus.json` stays canonical/human-readable;
serve both. It is uncompressed — let the host apply `gzip`/`br` transport compression.

Host that under a base URL, optionally alongside:
```
<base>/<id>/<version>/corpus.json        # immutable — cache forever
<base>/<id>/<version>/corpus.trlb        # immutable — the binary fast-load bundle (a standard artifact: the upstream pipeline + the Worker always publish/serve it)
<base>/<id>/<version>/manifest.json      # immutable
<base>/channels/<id>.<channel>.json      # mutable pointer: { id, channel, version, manifest, updatedAt }
<base>/registry.json                     # optional discovery index (scripts/gen-registry.mjs)
```

**Three requirements, and they're the only platform-specific part:**
- **HTTPS.**
- **CORS** — the editor fetches cross-origin, so responses need `Access-Control-Allow-Origin: *` (or the
  editor's origin). GitHub Pages and `raw.githubusercontent.com` send this already; most static hosts
  (Netlify, Cloudflare Pages, S3+CloudFront, GitLab Pages) let you add it.
- **Immutability** for `/<id>/<version>/**` — never overwrite a published version; a change is a new
  version. Promotion = repoint a channel.

`tropelang bundle` is a standalone binary — it runs in any CI (GitHub Actions, GitLab CI, Bitbucket
Pipelines, …) or locally. The GitHub Actions + Pages workflow (`.github/workflows/pages.yml`) is **one
implementation** of this contract; on another platform, run the same `bundle` step in your CI and serve
the files from your host. The Cloudflare Worker (`worker/`) the upstream uses adds tuned cache headers +
a channel `resolve` route — an optimization, not a requirement.

---

## What the editor will load

The editor accepts a corpus in **three forms** — pick the lowest-effort one for your case. All three
reduce to the same `load_corpus([{path, source}])`:

| Form | URL you give the editor | Best for |
|---|---|---|
| **JSON bundle** | a published **`corpus.json`** (this contract) | a shared / production corpus — one cached fetch + `sha256` integrity |
| **Tarball** | a **`.tar.gz`** of the repo / `trl/` tree (e.g. a GitHub/GitLab archive URL) | "fork and point" with **no publish step** — one fetch, unpacked client-side |
| **Naked files** | a **`corpus.toml`** URL (raw git, or a local file) | point straight at a fork's raw repo, or a local folder — zero build |

How **naked files** works: you hand the editor the `corpus.toml` URL (e.g.
`https://raw.githubusercontent.com/<you>/<fork>/main/trl/tropes/corpus.toml`). The editor reads it,
follows its `index` (`index.trl` — the assembled list of every file), and fetches each `.trl` **relative
to the `corpus.toml`** — assembling the bag client-side. No bundle, no publish. (A local folder is the
same flow, opened from disk.) It needs a **current `index.trl`**, since that's the file list the editor
walks — keep it assembled (`tropelang assemble`, which the `gate` enforces).

Notes:
- `corpus.toml` carries `id` / `version` / `engine_min`, so the **`engineMin` compatibility gate works in
  all three forms**. The **JSON bundle** additionally carries a `sha256` over the canonical bundle for
  integrity; the tarball and naked forms don't.
- One cached fetch (bundle) vs. many small fetches (naked) — prefer the **bundle** for a corpus you
  *share*; naked/tarball are ideal for dev, preview, and "just fork and point."
- The editor reconstructs the `trl/…` tree from the `path` fields in every form, and can **export back**
  to a directory or tarball for archival.

The consumer side of this — how the editor resolves and loads each form — is specced in
**[LOADING.md](LOADING.md)** (Phase C).

---

## Versioning
- `version` in `corpus.toml` is the corpus's own number (independent of the engine). Bump it per change:
  content edit = point, new arena/capability = minor, structural break = major.
- `engine_min` is the minimum engine that can parse your corpus — raise it only when you adopt newer
  grammar. The editor refuses a corpus whose `engineMin` exceeds its bundled engine.
