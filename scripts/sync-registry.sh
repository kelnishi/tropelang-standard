#!/usr/bin/env bash
# Mirror the committed channel pointers to R2, ensure every channel-pointed manifest is available
# locally, regenerate registry.json, and upload it. Shared by publish.yml (after a version upload) and
# promote.yml (channel-only change). Idempotent. Never touches immutable /:id/:version/ objects.
#
# Uses the R2 S3-compatible API (so a bucket-scoped R2 token works — wrangler's account-level object API
# rejects bucket-scoped tokens). Env: R2_BUCKET, R2_S3_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
# AWS_DEFAULT_REGION=auto; BUILT_AT + CORPUS_BASE_URL pass through to gen-registry.
set -euo pipefail
: "${R2_BUCKET:?set R2_BUCKET}"
: "${R2_S3_ENDPOINT:?set R2_S3_ENDPOINT}"

s3_put() { aws s3api put-object --endpoint-url "$R2_S3_ENDPOINT" --bucket "$R2_BUCKET" --key "$1" --body "$2" --content-type application/json >/dev/null; }
s3_get() { aws s3api get-object --endpoint-url "$R2_S3_ENDPOINT" --bucket "$R2_BUCKET" --key "$1" "$2" >/dev/null; }

shopt -s nullglob
for f in channels/*.json; do
  id=$(jq -r .id "$f")
  ver=$(jq -r .version "$f")

  # The channel-pointed manifest must be available locally for registry metadata. If this run didn't
  # build it (a promote-only run), pull it from R2. If it isn't published yet (first-publish bootstrap,
  # or a pointer ahead of its bundle), warn + skip — gen-registry emits a minimal entry rather than
  # failing the whole job.
  if [ ! -f "dist/$id/$ver/manifest.json" ]; then
    mkdir -p "dist/$id/$ver"
    if ! s3_get "$id/$ver/manifest.json" "dist/$id/$ver/manifest.json" 2>/dev/null; then
      echo "sync-registry: WARN $id@$ver is not published yet — skipping its registry metadata"
      rmdir "dist/$id/$ver" 2>/dev/null || true
    fi
  fi

  # Mirror the (mutable) pointer to R2.
  s3_put "$f" "$f"
done

node scripts/gen-registry.mjs channels dist dist/registry.json
s3_put "registry.json" "dist/registry.json"
echo "sync-registry: registry.json regenerated + uploaded"
