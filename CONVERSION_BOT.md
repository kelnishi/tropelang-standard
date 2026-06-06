# Conversion bot — identity & runbook

How an automated [`trope-to-tropelang`](skills/trope-to-tropelang/) run submits corpus PRs to
`tropelang-standard` so a human still reviews and approves them. There are **two delivery modes** — an
interactive *Claude Code on the web* session, and a headless *CI runner* under a GitHub App identity —
and they share the same quality bar (`tropelang gate`) and the same identity rule.

## The identity rule (why this exists)

`main` is protected by a ruleset requiring **1 approving review** before merge. GitHub will not
let an account approve its own PR. Therefore:

> The conversion bot must **author** PRs under an identity that is **not** the human who approves them.

- ❌ Bot authenticates as a person → that person can never approve → every merge needs an admin
  *bypass*, so the review gate never actually runs.
- ✅ Bot authors PRs under a **non-approver identity** (a GitHub App `…[bot]`, or a Claude Code web
  session that isn't the maintainer) → a human maintainer approves and merges normally, gate intact.

The automated quality bar is the **`gate` workflow** (`.github/workflows/gate.yml`): it runs
`tropelang gate` on every changed `.trl` with no secrets and a read-only token. The human approval
on top is an editorial spot-check, not a line-by-line validation.

## The `tropelang` CLI (required for the gate, both modes)

The gate (`skills/trope-to-tropelang/scripts/gate.sh` → `tropelang gate`) needs the **`tropelang`
engine CLI** on `PATH`. The engine source is private, so install the **prebuilt binary attached to this
repo's own GitHub release** — do **not** use `cargo install tropelang-cli` (not published on crates.io)
or `cargo install --git …/TropeLang` (private repo; the clone prompts for credentials):

```sh
# Resolve the latest CLI release asset. The tag is cli-vX.Y.Z; the Linux asset is tropelang-x86_64-linux.
# (Via the GitHub MCP: mcp__github__get_latest_release, or the API below.)
REL="cli-v0.4.0"   # ← use the latest cli-* release tag
curl -fsSL -o /tmp/tropelang \
  "https://github.com/kelnishi/tropelang-standard/releases/download/${REL}/tropelang-x86_64-linux"

# Verify the download against the release asset's sha256 digest BEFORE trusting it.
sha256sum /tmp/tropelang

install -m 0755 /tmp/tropelang /usr/local/bin/tropelang
tropelang version    # sanity check — engine/grammar version
```

Run the gate from the corpus root (so `--corpus file://trl` resolves):
`bash skills/trope-to-tropelang/scripts/gate.sh <file.trl>` → must print `── GATE PASS ──`.

---

## Mode A — Claude Code on the web (interactive, the default today)

This is how an interactive web session actually ships work, and it needs **no App credentials**: the
session has its own git remote (a local proxy) and its own GitHub identity via the GitHub MCP. `gh` is
**not** available — use the `mcp__github__*` tools for every GitHub action.

```sh
# 1. Work on the session's development branch (do NOT commit to main).
#    ...install the CLI (above), run the trope-to-tropelang skill, add/edit trl/ tropes...
bash skills/trope-to-tropelang/scripts/gate.sh trl/tropes/<path>/<new_trope>.trl   # local pre-flight

# 2. Commit + push to the session branch over the session's remote.
git add trl/tropes/<path>/<new_trope>.trl
git commit -m "Convert <batch-name>"
git push -u origin <session-branch>
```

Then open the PR to `main` with the **GitHub MCP** (`mcp__github__create_pull_request`, base `main`,
head `<session-branch>`). The PR is authored under the session identity — which is **not** the
maintainer — so the human can approve it and the review gate holds. The `gate` workflow runs on the PR.

## Mode B — headless CI runner (GitHub App identity)

For a fully automated runner with no human in the loop, author PRs as the dedicated
**`TropeLang Conversion Bot`** GitHub App (least-privilege: Contents + Pull requests read/write only;
no Workflows / Admin / Secrets; installed on `tropelang-standard` only; kept **separate** from the
release App). The runner needs the App's credentials in its env (secret store / env — **not** in git):

```sh
export CONVERSION_APP_ID="<the App ID>"
export CONVERSION_APP_PRIVATE_KEY="$(cat /secure/path/conversion-bot.pem)"   # inline PEM, or a path
# export CONVERSION_REPO="kelnishi/tropelang-standard"   # default; override only for a fork
```
`CONVERSION_APP_PRIVATE_KEY` accepts either the inline PEM text or a path to the `.pem`. To rotate or
recreate the key: **Settings → Developer settings → GitHub Apps**.

```sh
# 0. Mint a short-lived, repo-scoped token (contents+PR write only; auto-expires within the hour).
export GH_TOKEN="$(skills/trope-to-tropelang/scripts/bot-token.sh)"

# 1. Branch off main, convert, gate locally (install the CLI as above).
git switch -c convert/<batch-name> --no-track origin/main
bash skills/trope-to-tropelang/scripts/gate.sh trl/tropes/<path>/<new_trope>.trl

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

The PR *author* follows the token that calls the create-PR API (the installation token → the bot).
Setting the commit `user.name/email` to the bot is cosmetic but keeps history attributed; find
`<bot-user-id>` once via `gh api users/tropelang-conversion-bot[bot] --jq .id` (the `[bot]` suffix is
literal).

---

## Guardrails (both modes)

- **Never touch `trl/tropes/index.trl`.** It is rebuilt deterministically by the coordinator
  (`tropelang assemble trl/tropes/corpus.toml`), which also mints the concept entry from your
  preamble metadata (carry full `@trope/@category/@source/@domain`). Parallel agents collide on it.
- **Cross-check `BACKLOG.md` against the tree before converting** — it can lag reality (done items may
  still read `[ ]`). Don't re-convert work that already exists.
- **One batch per PR.** Keep PRs reviewable; the gate runs per changed `.trl`.
- **Don't push after approval.** The ruleset has `dismiss_stale_reviews_on_push: true` — a late commit
  nukes the human's approval and re-blocks. Land fixups as a fresh PR, not a follow-up push.
- **In CI mode the token is least-privilege and short-lived** — it can't touch workflows, releases, or
  repo settings, and it expires within the hour. Re-mint per run; never persist it.
- **Forks:** to submit from a fork, set `CONVERSION_REPO` to the fork and open a cross-repo PR. The
  `gate` workflow runs on fork PRs safely (no secrets, no `pull_request_target`).
- **Never** add the conversion App's key to the `gate` workflow or share a job with the (future,
  environment-gated) publish pipeline.
