# Corpus CDN — provisioning & operations runbook

How the standard corpus is published to `corpus.tropelang.com` (spec 19 Phase B.2). The corpus is a
**data artifact fetched at runtime** — a corpus edit reaches users by republishing this bundle, never by
redeploying the site.

## Architecture (what's in this repo)

| Piece | File | Role |
|---|---|---|
| Corpus metadata | `trl/tropes/corpus.toml` | `id`, `version`, `engine_min`, display fields → the manifest |
| Worker | `worker/` | fronts R2: cache headers, CORS, channel `resolve` (spec 19 §6.2) |
| Publish pipeline | `.github/workflows/publish.yml` | tag-triggered; bundles + uploads an **immutable** version |
| Promote pipeline | `.github/workflows/promote.yml` | mirrors channel pointers; moves `stable` (no rebuild) |
| Registry generator | `scripts/gen-registry.mjs` + `scripts/sync-registry.sh` | builds `registry.json` |
| Channel pointers | `channels/*.json` | the **mutable** pointers; committed = source of truth, mirrored to R2 |

**Immutability:** `/:id/:version/**` is write-once (cached forever at the edge). A change is always a
**new version**; promotion/rollback only repoints a channel.

---

## One-time provisioning (Cloudflare — only you can do this)

### 1. Create the R2 bucket
Cloudflare dashboard → R2 → **Create bucket** → name **`tropelang-corpus`** (matches `worker/wrangler.toml`
and `R2_BUCKET` in the workflows). No public access — the Worker is the only read path.

### 2. Create a least-privilege API token
R2 → **Manage API Tokens** (or My Profile → API Tokens → Create Token). Scope it to **just what publish
needs** (spec 22 §6.4):
- **Workers R2 Storage** → **Edit**, restricted to the **`tropelang-corpus`** bucket — object read/write.
- **Workers Scripts** → **Edit** (so `wrangler deploy` can publish the Worker).
- Account → **Workers Routes / DNS Edit** for the `tropelang.com` zone (custom-domain route).

Record the token value and your **Account ID** (R2 sidebar / dashboard URL).

### 3. DNS / zone
The `tropelang.com` zone must be in this Cloudflare account. `worker/wrangler.toml` declares a
**custom-domain route** `corpus.tropelang.com`; `wrangler deploy` creates the DNS record. (If you prefer a
`workers.dev` subdomain for testing first, drop the `routes` block and deploy.)

---

## One-time provisioning (GitHub — only you can do this)

### 4. The `production` environment (the security boundary)
Repo → Settings → Environments → **New environment** → **`production`**:
- **Required reviewers:** add yourself. Every publish/promote then waits for your one-click approval —
  even though the trigger is a tag/merge, the Cloudflare credential is unreachable until you approve.
- **Deployment branches:** limit to `main` + tags if desired.
- **Environment secrets:**
  - `CLOUDFLARE_ACCOUNT_ID` — your account ID.
  - `CLOUDFLARE_API_TOKEN` — the token from step 2.

> These live in the **environment**, not repo-wide, so no other workflow (and no fork PR) can reach them.

### 5. Deploy the Worker
```sh
cd worker
npx wrangler deploy        # uses CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID from your shell env
```
Verify: `curl -i https://corpus.tropelang.com/registry.json` (404 until the first publish — that's fine;
it proves the Worker + route are live).

### 6. Engine CLI release (prerequisite)
`publish.yml` pins **`CLI_TAG: cli-v0.4.0`** — the engine release whose `tropelang bundle` emits the full
spec-19 manifest. Tag/publish that release in the engine repo first (the `release-cli` workflow), so the
prebuilt binary exists at that tag.

---

## Operating it

### Publish a new version
1. Edit the corpus; bump **`version`** in `trl/tropes/corpus.toml` (point/minor/major per the content
   change). Keep `engine_min` honest if you used newer grammar.
2. Merge to `main` (the no-secret `gate` runs on the PR).
3. Tag it: `git tag corpus-v<version> && git push origin corpus-v<version>` (the tag version **must**
   match `corpus.toml`).
4. `publish.yml` runs → **approve** the `production` deployment → it bundles, **refuses if the version
   already exists**, uploads the immutable bundle, mirrors channels, regenerates `registry.json`.
   It does **not** move `stable`.

### Promote / rollback (point users at a version)
Edit `channels/standard.stable.json` → set `version` + `manifest` to an **already-published** version →
PR → merge. `promote.yml` mirrors it to R2 and regenerates the registry. Within ~30 s (the channel TTL)
every consumer serves it. Rollback = point back at a prior version (still immutable in R2).

### Verify
```sh
curl -i https://corpus.tropelang.com/registry.json                       # discovery (max-age=60)
curl -i https://corpus.tropelang.com/standard/resolve?channel=stable     # → the pinned manifest
curl -i https://corpus.tropelang.com/standard/1.7.0/corpus.json          # immutable (max-age=1y)
```

---

## Security invariants (do not break)
- **Never** add `pull_request`/`pull_request_target` to `publish.yml`/`promote.yml`, and never share a job
  with the no-secret `gate`. The CF credential lives only in the `production` environment.
- The token is **least-privilege** (one bucket + the Worker) and the environment is **fail-closed** behind
  a required reviewer — so a merged-then-bad change is a *new version + a channel repoint*, never an
  in-place overwrite.
- The Worker is **read-only** (GET/HEAD/OPTIONS); CI is the only writer.

## Notes / v1 scope
- **Channel source of truth is the repo** (`channels/`), mirrored to R2 — a deliberate, more-auditable
  choice over spec 19 §4.3's "R2-only mutable" (you get git history + PR review on every promotion).
- **One corpus (standard).** Forks self-host per spec 19 §8 (run `tropelang bundle`, upload the two files
  anywhere). A multi-corpus registry in this repo just adds more `channels/*.json` + `corpus.toml`s.
- `publish.yml`'s `--expect-tropes 191` is the same count tripwire as `gate.yml`; bump both when the corpus
  grows.
