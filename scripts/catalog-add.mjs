#!/usr/bin/env node
// Upsert a just-published version into a corpus version catalog (/<id>/versions.json) — the engine-aware
// discovery index (spec 19). Append-only: existing entries and their `yanked` flags are preserved (the
// immutable bundles never change, so the catalog only grows). Pure: reads files, writes the merged catalog;
// the workflow owns fetching the current catalog from R2 and uploading the result.
//
// Usage: node scripts/catalog-add.mjs <manifest.json> <catalog.json|-> <out.json>
//   manifest  the just-published version's manifest (has id, version, engineMin, sha256, …)
//   catalog   existing versions.json, or "-" / a missing / empty file for the first publish
//   out       merged catalog to write (the workflow uploads this to <id>/versions.json)

import { readFileSync, writeFileSync, existsSync } from "node:fs";

const [mfPath, catPath, outPath] = process.argv.slice(2);
if (!mfPath || !catPath || !outPath) {
  console.error("usage: catalog-add.mjs <manifest.json> <catalog.json|-> <out.json>");
  process.exit(2);
}

const m = JSON.parse(readFileSync(mfPath, "utf8"));
if (!m.id || !m.version) { console.error("catalog-add: manifest missing id/version"); process.exit(1); }

let cat = { schema: 1, id: m.id, versions: [] };
if (catPath !== "-" && existsSync(catPath)) {
  const raw = readFileSync(catPath, "utf8").trim();
  if (raw) { cat = JSON.parse(raw); cat.schema ??= 1; cat.id ??= m.id; cat.versions ??= []; }
}

const entry = {
  version: m.version,
  engineMin: m.engineMin ?? null,                                   // the floor: usable iff engineMin <= engine
  manifest: `/${m.id}/${m.version}/manifest.json`,
  bundle: `/${m.id}/${m.version}/${m.bundle || "corpus.json"}`,
  sha256: m.sha256 ?? null,
  bytes: m.bytes ?? null,
  tropeCount: m.tropeCount ?? null,
  builtAt: m.builtAt ?? null,
  yanked: false,                                                    // never auto-selected once true
};

// Upsert by version; a re-publish must never silently un-yank a withdrawn version.
const prior = cat.versions.find((v) => v.version === m.version);
if (prior && prior.yanked) entry.yanked = true;
cat.versions = cat.versions.filter((v) => v.version !== m.version);
cat.versions.push(entry);

// Newest-first by semver (numeric components, stable string fallback).
const key = (v) => v.version.split(".").map((n) => parseInt(n, 10) || 0);
cat.versions.sort((a, b) => {
  const x = key(a), y = key(b);
  return (y[0] - x[0]) || (y[1] - x[1]) || (y[2] - x[2]) || b.version.localeCompare(a.version);
});

writeFileSync(outPath, JSON.stringify(cat, null, 2) + "\n");
console.log(`catalog-add: ${m.id}@${m.version} → ${cat.versions.length} versions`);
