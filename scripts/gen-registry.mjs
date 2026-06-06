#!/usr/bin/env node
// Generate registry.json (spec 19 §4.4) from the committed channel pointers + the manifests present
// locally under dist/. Pure: reads files only — the workflow is responsible for making every
// channel-pointed manifest available under dist/ first (built this run, or pulled from R2).
//
// Usage: node scripts/gen-registry.mjs [channelsDir=channels] [distDir=dist] [out=dist/registry.json]
// Env:   CORPUS_BASE_URL (default https://corpus.tropelang.com), BUILT_AT (default now, for determinism)

import { readFileSync, readdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const channelsDir = process.argv[2] || "channels";
const distDir = process.argv[3] || "dist";
const outFile = process.argv[4] || "dist/registry.json";
const BASE_URL = (process.env.CORPUS_BASE_URL || "https://corpus.tropelang.com").replace(/\/+$/, "");

// 1. channels/<id>.<channel>.json → { id: { channel: version } }
const channels = {};
for (const f of existsSync(channelsDir) ? readdirSync(channelsDir) : []) {
  if (!f.endsWith(".json")) continue;
  const ptr = JSON.parse(readFileSync(join(channelsDir, f), "utf8"));
  (channels[ptr.id] ||= {})[ptr.channel] = ptr.version;
}

// 2. dist/**/manifest.json → { "id/version": manifest }
const manifests = {};
(function walk(dir) {
  for (const e of existsSync(dir) ? readdirSync(dir, { withFileTypes: true }) : []) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name === "manifest.json") {
      const m = JSON.parse(readFileSync(p, "utf8"));
      if (m.id && m.version) manifests[`${m.id}/${m.version}`] = m;
    }
  }
})(distDir);

// 3. one registry entry per corpus; metadata from its stable (else any) channel's manifest
const corpora = [];
for (const [id, chans] of Object.entries(channels)) {
  const repVer = chans.stable || Object.values(chans)[0];
  const m = manifests[`${id}/${repVer}`];
  if (!m) {
    console.warn(`gen-registry: no manifest for ${id}@${repVer} under ${distDir} — emitting a minimal entry`);
  }
  corpora.push({
    id,
    displayName: m?.displayName || id,
    description: m?.description || "",
    author: m?.author ?? null,
    tags: m?.tags || [],
    homepage: m?.homepage ?? null,
    channels: chans,
    engineMin: m?.engineMin || null,
    base: m?.base ?? null,
    url: `${BASE_URL}/${id}/`,
  });
}
corpora.sort((a, b) => a.id.localeCompare(b.id));

const registry = {
  schema: 1,
  generatedAt: process.env.BUILT_AT || new Date().toISOString(),
  corpora,
};
writeFileSync(outFile, JSON.stringify(registry, null, 2) + "\n");
console.log(`gen-registry: ${corpora.length} corpora → ${outFile}`);
