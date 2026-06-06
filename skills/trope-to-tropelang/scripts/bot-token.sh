#!/usr/bin/env bash
# Mint a short-lived (<=1h) GitHub App *installation* token for the TropeLang Conversion Bot.
#
# Why this exists: an automated conversion run must open its PRs under a NON-HUMAN identity that
# is distinct from the human reviewer. GitHub forbids approving your own PR, so if the bot authored
# as a person, that person could never approve it. A bot-authored PR can be reviewed + approved by
# a human maintainer normally. See ./../../../CONVERSION_BOT.md.
#
# Inputs (environment):
#   CONVERSION_APP_ID          - the App's numeric App ID (Settings -> Developer settings -> GitHub Apps)
#   CONVERSION_APP_PRIVATE_KEY - the App's PEM private key, EITHER the inline text (-----BEGIN...-----)
#                                OR a path to the .pem file
#   CONVERSION_REPO            - owner/repo to scope the token to (default: kelnishi/tropelang-standard)
#
# Output: prints ONLY the installation token to stdout. Typical use:
#   export GH_TOKEN="$(skills/trope-to-tropelang/scripts/bot-token.sh)"
#   # git + gh now act as the bot identity; the token auto-expires within the hour.
#
# Dependencies: bash, openssl, curl, python3 -- all present in a standard workspace.
#               No jq, no PyJWT, no extra installs. The token is scoped to exactly
#               contents:write + pull_requests:write on the one repo (least privilege).
set -euo pipefail

: "${CONVERSION_APP_ID:?set CONVERSION_APP_ID to the numeric App ID}"
: "${CONVERSION_APP_PRIVATE_KEY:?set CONVERSION_APP_PRIVATE_KEY to the PEM (inline text or a file path)}"
REPO="${CONVERSION_REPO:-kelnishi/tropelang-standard}"

# Resolve the private key: a file path is used in place; inline PEM is spilled to a locked-down temp file.
keyfile=""
cleanup() { [ -n "$keyfile" ] && rm -f "$keyfile"; }
trap cleanup EXIT
if [ -f "$CONVERSION_APP_PRIVATE_KEY" ]; then
  KEY="$CONVERSION_APP_PRIVATE_KEY"
else
  keyfile="$(mktemp)"; chmod 600 "$keyfile"
  printf '%s\n' "$CONVERSION_APP_PRIVATE_KEY" > "$keyfile"
  KEY="$keyfile"
fi

# base64url with no padding/newlines -- portable across LibreSSL (macOS) and OpenSSL (Linux).
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }

# --- 1. Build a 9-minute App JWT (GitHub caps exp at 10m; back-date iat 60s for clock skew). ---
now=$(date +%s)
header='{"alg":"RS256","typ":"JWT"}'
payload="{\"iat\":$((now - 60)),\"exp\":$((now + 540)),\"iss\":\"${CONVERSION_APP_ID}\"}"
unsigned="$(printf '%s' "$header" | b64url).$(printf '%s' "$payload" | b64url)"
sig="$(printf '%s' "$unsigned" | openssl dgst -sha256 -sign "$KEY" -binary | b64url)"
jwt="${unsigned}.${sig}"

gh_api() {
  # gh_api <bearer> <curl-args...>
  curl -fsS \
    -H "Authorization: Bearer $1" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "${@:2}"
}

# --- 2. Find this repo's installation id (the App must be installed on the repo). ---
inst_id="$(gh_api "$jwt" "https://api.github.com/repos/${REPO}/installation" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')" || {
    echo "bot-token: could not read installation for ${REPO} -- is the App installed on it?" >&2
    exit 1
  }

# --- 3. Exchange the JWT for a repo-scoped, least-privilege installation token. ---
repo_name="${REPO#*/}"
gh_api "$jwt" -X POST "https://api.github.com/app/installations/${inst_id}/access_tokens" \
  -d "{\"repositories\":[\"${repo_name}\"],\"permissions\":{\"contents\":\"write\",\"pull_requests\":\"write\"}}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["token"])'
