# Corpus discovery & engine-aware version selection

A client should never have to guess version numbers or assume "newest = needs the newest engine."
Everything below is served from the CDN (`https://corpus.tropelang.com`, backed by R2). All three documents
are JSON with a `schema` field.

## The three documents

| URL | Mutability | Purpose |
|-----|-----------|---------|
| `/registry.json` | mutable | Entry point: lists every corpus, its curated `channels`, and its catalog URL. |
| `/<id>/versions.json` | append-only | **Catalog**: every *published* version of a corpus + its `engineMin`. |
| `/<id>/<version>/manifest.json` | immutable | One published version (sha256, tropeCount, `engineMin`, bundle path). |

### `registry.json`
```json
{
  "schema": 1,
  "generatedAt": "2026-06-06T23:28:50Z",
  "corpora": [
    {
      "id": "standard",
      "channels": { "stable": "1.7.2" },
      "engineMin": "0.4.1",
      "versions": "https://corpus.tropelang.com/standard/versions.json",
      "url": "https://corpus.tropelang.com/standard/"
    }
  ]
}
```
`channels.stable` is the **curated, recommended** live version (moved by the *Promote Stable and Sync*
action). `engineMin` here is *stable's* floor. For anything more than "give me the recommended latest,"
read the catalog.

### `/<id>/versions.json` (the catalog)
```json
{
  "schema": 1,
  "id": "standard",
  "versions": [
    { "version": "1.7.2", "engineMin": "0.4.1", "manifest": "/standard/1.7.2/manifest.json",
      "bundle": "/standard/1.7.2/corpus.json", "sha256": "…", "tropeCount": 194,
      "builtAt": "2026-06-06T23:28:50Z", "yanked": false },
    { "version": "1.7.1", "engineMin": "0.4.0", "…": "…", "yanked": false }
  ]
}
```
- **Append-only**: a version is added when its immutable bundle is *deployed* (regardless of whether it is
  later promoted to `stable`). Entries are sorted newest-first.
- `engineMin` — the version is runnable iff `engineMin ≤ your engine version`.
- `yanked` — a withdrawn version (e.g. a bad release). The bundle stays immutable in R2, but `yanked: true`
  removes it from selection. Never auto-selected.

## Client resolution

Given your engine version `E` (e.g. `0.4.0`), pick a corpus version like this:

```
resolve(E, id):
  reg     = GET /registry.json
  corpus  = reg.corpora.find(id)
  stable  = corpus.channels.stable
  catalog = GET corpus.versions                       # /<id>/versions.json

  # Default policy — "newest the engine supports, never ahead of curated stable":
  candidates = catalog.versions.filter(v =>
                 !v.yanked
                 && semver(v.engineMin) <= semver(E)
                 && semver(v.version)   <= semver(stable))
  return maxBySemver(candidates)                       # null ⇒ engine too old even for the oldest published
```

This is the case that motivated the catalog: when `stable = 1.7.2` (needs `0.4.1`) and your engine is
`0.4.0`, you **step down** to `1.7.1` (needs `0.4.0`) — the newest compatible version that doesn't exceed
the curated pointer — instead of failing.

Policy variants (same catalog):
- **Recommended latest** (no pinning): just use `corpus.channels.stable`; only fall back to the catalog if
  `stable`'s `engineMin > E`.
- **Bleeding edge**: drop the `version ≤ stable` clause to take the newest compatible *available* version,
  even before it is promoted to `stable`.
- **Pinned**: fetch a specific `/<id>/<version>/manifest.json` directly; verify `engineMin ≤ E` and `sha256`.

Always verify the chosen version's `sha256` after downloading the bundle.

## Yanking a version

The catalog is the only mutable record of a published version, so withdrawing one is a catalog edit, not a
delete (bundles are immutable):

1. Fetch `/<id>/versions.json` from R2, set `"yanked": true` on the offending entry, upload it back
   (`--cache-control no-cache`).
2. If `stable` points at the yanked version, run **Promote Stable and Sync** naming a prior good version to
   move clients off it.

(A re-publish of the same version number is refused by the deploy immutability guard, and `catalog-add.mjs`
preserves an existing `yanked` flag regardless — a withdrawn version cannot be silently un-yanked.)
