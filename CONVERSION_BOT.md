# Conversion bot — identity & runbook

How an automated [`trope-to-tropelang`](skills/trope-to-tropelang/) run submits corpus PRs to
`tropelang-standard` under a dedicated bot identity, so a human still reviews and approves them.

## The identity rule (why this exists)

`main` is protected by a ruleset requiring **1 approving review** before merge. GitHub will not
let an account approve its own PR. Therefore:

> The conversion bot must **author** PRs under an identity that is **not** the human who approves them.

- ❌ Bot authenticates as a person → that person can never approve → every merge needs an admin
  *bypass*, so the review gate never actually runs.
- ✅ Bot authenticates as a **GitHub App** → PRs are authored by `…[bot]` → a human maintainer
  approves and merges normally, review gate intact.

The automated quality bar is the **`gate` workflow** (`.github/workflows/gate.yml`): it runs
`tropelang gate` on every changed `.trl` with no secrets and a read-only token. The human approval
on top is an editorial spot-check, not a line-by-line validation.

## One-time setup

### 1. Create the App (account owner, in the browser — once)

**Settings → Developer settings → GitHub Apps → New GitHub App**

| Field | Value |
| --- | --- |
| **Name** | `TropeLang Conversion Bot` (App names are globally unique; adjust if taken) |
| **Homepage URL** | `https://github.com/kelnishi/tropelang-standard` |
| **Webhook → Active** | **unchecked** (this App only mints tokens; it receives no events) |
| **Repository permissions → Contents** | **Read and write** (push the conversion branch) |
| **Repository permissions → Pull requests** | **Read and write** (open the PR) |
| **Repository permissions → Metadata** | Read-only (mandatory, auto-selected) |
| *(everything else)* | **No access** — do **not** grant Workflows, Administration, or Secrets |
| **Where can this App be installed?** | **Only on this account** |

Keep this App **separate from the release App** (`RELEASE_APP_ID`): least privilege — the
conversion bot can open PRs but cannot publish releases, and the release App cannot push branches
or open PRs.

After **Create GitHub App**:
- note the **App ID** (top of the App's settings page);
- **Generate a private key** → downloads a `.pem`. Store it as a secret; **never commit it.**

### 2. Install it on the corpus repo (once)

On the App page → **Install App** → install on `kelnishi` → **Only select repositories** →
`tropelang-standard`. That single install is what `bot-token.sh` looks up.

### 3. Give the workspace its credentials

The Claude Code workspace that runs conversion needs these in its environment (workspace secret
store / env — **not** in git):

```sh
export CONVERSION_APP_ID="<the App ID>"
export CONVERSION_APP_PRIVATE_KEY="$(cat /secure/path/conversion-bot.pem)"   # inline PEM, or a path
# export CONVERSION_REPO="kelnishi/tropelang-standard"   # default; override only for a fork
```

`CONVERSION_APP_PRIVATE_KEY` accepts either the inline PEM text or a path to the `.pem`.

## Per-run flow (what the bot does)

```sh
# 0. Mint a short-lived, repo-scoped token (contents+PR write only; auto-expires within the hour).
export GH_TOKEN="$(skills/trope-to-tropelang/scripts/bot-token.sh)"

# 1. Branch off main (no base-tracking), do the conversion, gate locally.
git switch -c convert/<batch-name> --no-track origin/main
#    ...run the trope-to-tropelang skill to add/edit trl/ tropes...
skills/trope-to-tropelang/scripts/gate.sh trl/tropes/<path>/<new_trope>.trl   # local pre-flight

# 2. Commit + push as the bot (x-access-token + the installation token = bot authorship).
git -c user.name="tropelang-conversion-bot[bot]" \
    -c user.email="<bot-user-id>+tropelang-conversion-bot[bot]@users.noreply.github.com" \
    commit -am "Convert <batch-name>"
git push "https://x-access-token:${GH_TOKEN}@github.com/kelnishi/tropelang-standard.git" \
    HEAD:refs/heads/convert/<batch-name>

# 3. Open the PR (authored by the bot because GH_TOKEN is the installation token).
gh pr create --repo kelnishi/tropelang-standard --base main \
    --head convert/<batch-name> --title "Convert <batch-name>" --body "..."
```

The PR *author* is the bot regardless of commit authorship (it follows the token that calls the
create-PR API). Setting the commit `user.name/email` to the bot is cosmetic but keeps the history
attributed; find `<bot-user-id>` once via
`gh api users/tropelang-conversion-bot[bot] --jq .id` (the `[bot]` suffix is literal).

## Guardrails

- **Don't push after approval.** The ruleset has `dismiss_stale_reviews_on_push: true` — a late
  commit nukes the human's approval and re-blocks. Land fixups as a fresh PR, not a follow-up push.
- **One batch per PR.** Keep PRs reviewable; the gate runs per changed `.trl`.
- **The token is least-privilege and short-lived** — it can't touch workflows, releases, or repo
  settings, and it expires within the hour. Re-mint per run; never persist it.
- **Forks:** to submit from a fork instead of a same-repo branch, set `CONVERSION_REPO` to the
  fork and open a cross-repo PR. The `gate` workflow runs on fork PRs safely (no secrets, no
  `pull_request_target`).
- **Never** add this App's key to the `gate` workflow or share a job with the (future,
  environment-gated) publish pipeline.
