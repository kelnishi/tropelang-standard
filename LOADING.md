# Loading a corpus — editor/host contract (Phase C)

**Status: stub.** The contract the **Phase C editor** (`tropelang-site`) implements. Producer side:
[PUBLISHING.md](PUBLISHING.md). Engine spec: `19 §9`. This doc is the skeleton to drive that work — the
site repo fleshes out the implementation.

The job: turn a **corpus reference** (a URL, or a local folder) into a `load_corpus([{path, source}])`
call, gate compatibility, surface errors — for the three input forms.

## 0. Engine primitives (already shipped)
- **`load_corpus(files_json)`** — Phase A. Takes `[{path, source}]`, derives all metadata from
  `path` + `//` preamble. Returns `{ ok, count, errors }`.
- **`engine_version()`** — the engine/grammar version, for the `engineMin` gate (B.1 export).

## 1. The three input forms

### A. JSON bundle — a `corpus.json` (or channel/`resolve`) URL
1. Resolve to a `manifest.json`: a channel URL (`/:id/resolve?channel=…` or a channel file) → its
   `manifest`; or a direct `manifest.json`; or the sibling of a given `corpus.json`.
2. **engineMin gate** (§3).
3. Fetch `corpus.json`; **verify `sha256`** against the manifest.
4. `load_corpus(corpus.json)`.

Best for a *shared* corpus: one cached fetch + integrity.

### B. Tarball — a `.tar.gz` URL
1. Fetch → gunzip → untar in-browser.
2. Read `trl/tropes/corpus.toml` for `id`/`version`/`engine_min` → engineMin gate.
3. Collect every `trl/**/*.trl` into `[{path, source}]` (path = archive-relative `trl/…`).
4. `load_corpus`.

No `sha256`/manifest. Good for "fork and point" with no publish. **CORS caveat:** git archive endpoints
(e.g. `codeload.github.com`) may not send CORS headers — see §7.

### C. Naked files — a `corpus.toml` URL (or a local folder)
The editor assembles the bag by walking the repo from `corpus.toml` — no directory listing needed.
**`index.trl` is *not* a complete file list** (it imports tropes + the concepts index, not prelude /
ontology / modules), so the walk is: conventional roots + transitive import closure.
1. Fetch `corpus.toml`; parse `id`/`version`/`engine_min`, `tropes`, `index`. `root` = parent of
   `tropes`. **engineMin gate.**
2. Fetch the **conventional roots** (loaded by convention, not imported): `<root>/prelude.trl`,
   `<root>/ontology/verb_classes.trl`.
3. Fetch `index` (`index.trl`); seed a worklist with its `import "trl/…"` targets.
4. **Transitively** fetch every `import "trl/…"` target (dedupe; parse each fetched file for further
   imports). This closure reaches the concepts, the modules a trope pulls in, and all tropes.
5. Build `[{path, source}]` (path = `trl/`-relative); `load_corpus`.

Needs a **current `index.trl`** (the seed list) — keep it assembled (`tropelang assemble`; the `gate`
enforces it). This is the one non-trivial loader; prefer a **bundle** for anything shared.

### D. Binary bundle — a `corpus.trlb` URL

The **post-parse AST binary** (engine spec 24): each file's already-parsed AST + header metadata, so the
host loads it with **no lexing/parsing** — the fast path for an eval engine / game over a large corpus. It
ships beside `corpus.json` (same file set; `corpus.json` stays canonical) and is pinned in the manifest by
`trlb` / `trlbBytes` / `trlbSha256`.

1. Resolve to a `manifest.json` (as form A); **engineMin gate** (§3).
2. Fetch `corpus.trlb`; **verify `trlbSha256`**. It is uncompressed — rely on transport `gzip`/`br`
   (`Content-Encoding`); a browser `fetch` inflates transparently, or inflate a `.trlb.gz` via
   `DecompressionStream` before decoding.
3. Decode in-engine: `load_corpus_trlb(bytes)` (WASM) — the parse-skip peer of `load_corpus`. Layer
   further sources with `layer_corpus_trlb(bytes, strikes)`. A decoder rejects a `format_version` it
   doesn't know; that check is independent of the `engineMin` gate.

Best for a *shared, large* corpus where load latency matters. Falls back to form A (`corpus.json`) for any
host that hasn't adopted the binary path.

### Input detection (from a single URL/handle)
- a registry `id`, a channel/`resolve` URL, or `…/corpus.json` → **A**
- `….tar.gz` / `….tgz` → **B**
- `…/corpus.toml`, or a dropped local folder → **C**
- `…/corpus.trlb` → **D**

## 2. Load sequence (spec 19 §9.2)
channel `resolve` (short TTL) → `manifest` → **engineMin gate** → `corpus.json` (immutable, likely
edge/browser-cached) → verify `sha256` → `load_corpus` → on `{ ok:false }` surface `errors` and **keep
the prior corpus active**. Cache the bundle by `id/version` (immutable) for instant reloads; only the
channel pointer is re-fetched each load.

## 3. engineMin gate
If `semver(engineMin) > semver(engine_version())` → refuse to load (or load **read-only** with a clear
"needs a newer editor" warning). **Never silently mis-parse** a newer corpus. Source of `engineMin`: the
manifest (form A) or `corpus.toml`'s `engine_min` (forms B/C).

## 4. Discovery
- **Registry picker:** fetch `registry.json` → list (displayName, description, channels, `engineMin`,
  fork provenance). Selecting one stores `{ id, channel }`.
- **Add-by-URL:** accepts any of the three forms above, no gatekeeping — covers self-hosted corpora the
  registry doesn't list.

## 5. Export (archival)
From the in-memory `[{path, source}]`, reconstruct the `trl/…` tree → download as a folder (File System
Access API) or a `.tar.gz`/`.zip`. Round-trips with forms B/C.

## 6. Security
- The corpus is **DATA, not code** — `load_corpus` only lexes/parses. But the editor **renders** corpus
  prose/dialog: treat corpus text as **untrusted, escape on render** (the XSS surface).
- **CORS + HTTPS** required of the host; integrity via `sha256` (bundle) + HTTPS.
- A failed load leaves the previously loaded corpus active.

## 7. Open questions
- **Naked-mode enumeration:** transitive-import closure (this doc) vs. publishing a flat **file-list**
  artifact (`files.json`) for a trivial fetch-each. Start with closure; add a manifest if it proves
  fragile.
- **Tarball CORS:** `codeload.github.com` archives may lack CORS; may need a proxy, or fall back to the
  naked `corpus.toml` path. Confirm per host.
- **Browser cache:** CacheStorage vs IndexedDB, keyed by `id/version`.
- **Local editing tier:** form C from disk overlaps the editor's local/free buffers — unify the loader
  with the in-memory document store (editor-persistence plan).
