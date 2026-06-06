#!/usr/bin/env bash
# Prepare a corpus release: bump the version, sync the publish self-check count to the live trope count,
# and roll up the changelog. Used by .github/workflows/release.yml; runnable locally too. Prints the new
# version to stdout (nothing else goes to stdout). Requires the `tropelang` CLI on PATH.
#
# Usage: scripts/cut-release.sh <point|minor|major|X.Y.Z>
set -euo pipefail

arg="${1:?usage: cut-release.sh <point|minor|major|X.Y.Z>}"
toml="trl/tropes/corpus.toml"
changelog="CHANGELOG.md"
publish=".github/workflows/publish.yml"

cur=$(grep -E '^version' "$toml" | head -1 | cut -d'"' -f2)
[ -n "$cur" ] || { echo "cut-release: no version in $toml" >&2; exit 1; }

# Resolve the new version from a bump keyword or an explicit X.Y.Z.
case "$arg" in
  major|minor|point|patch)
    IFS=. read -r MA MI PA <<< "$cur"
    case "$arg" in
      major) MA=$((MA + 1)); MI=0; PA=0;;
      minor) MI=$((MI + 1)); PA=0;;
      *)     PA=$((PA + 1));;
    esac
    new="$MA.$MI.$PA";;
  [0-9]*.[0-9]*.[0-9]*) new="$arg";;
  *) echo "cut-release: bad version/bump '$arg' (want point|minor|major|X.Y.Z)" >&2; exit 1;;
esac
[ "$new" != "$cur" ] || { echo "cut-release: new version equals current ($cur)" >&2; exit 1; }

# 1. bump corpus.toml version
sed -i.bak -E "s/^(version[[:space:]]*=[[:space:]]*\").*(\")/\1${new}\2/" "$toml" && rm -f "$toml.bak"

# 2. sync --expect-tropes to the live effective count (assemble also refreshes the index; a no-op if in sync)
count=$(tropelang assemble "$toml" | sed -nE 's/.* ([0-9]+) effective tropes.*/\1/p' | head -1)
[ -n "$count" ] || { echo "cut-release: could not read the effective trope count" >&2; exit 1; }
sed -i.bak -E "s/--expect-tropes [0-9]+/--expect-tropes ${count}/" "$publish" && rm -f "$publish.bak"

# 3. roll up CHANGELOG: insert a dated heading right after [Unreleased] (its current body rolls under it)
if ! grep -q '^## \[Unreleased\]' "$changelog"; then
  echo "cut-release: no '## [Unreleased]' heading in $changelog" >&2; exit 1
fi
date=$(date -u +%Y-%m-%d)
awk -v ver="$new" -v d="$date" '
  /^## \[Unreleased\]/ && !done { print; print ""; print "## [" ver "] — " d; done=1; next }
  { print }
' "$changelog" > "$changelog.tmp" && mv "$changelog.tmp" "$changelog"

echo "cut-release: $cur → $new (expect-tropes $count, changelog rolled up)" >&2
echo "$new"
