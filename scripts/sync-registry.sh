#!/usr/bin/env bash
# Mirror the committed channel pointers to R2, ensure every channel-pointed manifest is available
# locally, regenerate registry.json, and upload it. Shared by publish.yml (after a version upload) and
# promote.yml (channel-only change). Idempotent. Never touches immutable /:id/:version/ objects.
#
# Env: R2_BUCKET (required), CLOUDFLARE_ACCOUNT_ID + CLOUDFLARE_API_TOKEN (for wrangler), BUILT_AT,
#      CORPUS_BASE_URL (passed through to gen-registry).
set -euo pipefail
: "${R2_BUCKET:?set R2_BUCKET}"

wr() { npx --yes wrangler@3 "$@"; }

shopt -s nullglob
for f in channels/*.json; do
  id=$(jq -r .id "$f")
  ver=$(jq -r .version "$f")

  # The channel-pointed manifest must be available locally for registry metadata. If this run didn't
  # build it (a promote-only run), pull it from R2 — it must already be published (fail-closed).
  if [ ! -f "dist/$id/$ver/manifest.json" ]; then
    mkdir -p "dist/$id/$ver"
    wr r2 object get "$R2_BUCKET/$id/$ver/manifest.json" --file "dist/$id/$ver/manifest.json"
  fi

  # Mirror the (mutable) pointer to R2.
  wr r2 object put "$R2_BUCKET/$f" --file "$f" --content-type application/json
done

node scripts/gen-registry.mjs channels dist dist/registry.json
wr r2 object put "$R2_BUCKET/registry.json" --file dist/registry.json --content-type application/json
echo "sync-registry: registry.json regenerated + uploaded"
