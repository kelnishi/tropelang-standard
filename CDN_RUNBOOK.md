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

### 2. Create a least-privilege R2 token (S3 credentials)
R2 → **Manage R2 API Tokens** → **Create API Token**: permission **Object Read & Write**, scoped to the
**`tropelang-corpus`** bucket only. CI drives R2 over the **S3-compatible API** (not `wrangler r2 object`,
which rejects bucket-scoped tokens), so what you need from this screen is the pair it generates:
- **Access Key ID** → GitHub secret `R2_ACCESS_KEY_ID`
- **Secret Access Key** → GitHub secret `R2_SECRET_ACCESS_KEY`

Also record your **Account ID** (the S3 endpoint is `https://<account-id>.r2.cloudflarestorage.com`).
The Worker is deployed separately by you (`wrangler login` — step 5), so this token needs **no** Workers
Scripts / DNS permissions: it's R2-object-only on the one bucket.

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
  - `CLOUDFLARE_ACCOUNT_ID` — your account ID (used to build the R2 S3 endpoint URL).
  - `R2_ACCESS_KEY_ID` — the R2 token's Access Key ID (step 2).
  - `R2_SECRET_ACCESS_KEY` — the R2 token's Secret Access Key (step 2).

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
