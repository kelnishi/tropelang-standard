# Conversion bot — identity & runbook

How an automated [`trope-to-tropelang`](skills/trope-to-tropelang/) run submits corpus PRs to
`tropelang-standard` so a human still reviews and approves them. There are **two delivery modes** — an
interactive *Claude Code on the web* session, and a headless *CI runner* under a GitHub App identity —
and they share the same quality bar (`tropelang gate`) and the same identity rule.

## Quickstart — launching a fresh session (minimal prompt)

A new session can run the whole loop from a one-line prompt; everything it needs is **this file** plus
`skills/trope-to-tropelang/SKILL.md` (authoring) and `STYLE.md` (conventions).

**Minimal prompt to paste into a new session:**
> Convert the next batch of high-profile tropes into the TropeLang corpus. Follow `CONVERSION_BOT.md`
> and `skills/trope-to-tropelang/SKILL.md`. Install the CLI, pick targets from the coverage gaps in
> CONVERSION_BOT.md (or `trl/tropes/BACKLOG.md`), author each with a self-confirming vignette, keep
> `tropelang selfcheck` at 100%, finalize (assemble + CHANGELOG), and push a `convert/<batch>` branch
> for CI to open the PR.

**Run checklist (the order that works):**
1. **Install the CLI (REQUIRED — not pre-installed)** — the latest `cli-*` release binary (see "The `tropelang` CLI" below); confirm `tropelang version`. The container is ephemeral, so this must be done every session.
2. **Read** `skills/trope-to-tropelang/SKILL.md` (§1 acquire → §4b recognition fidelity) and `STYLE.md` §8.
3. **Pick targets** — the coverage gaps (next section) or `BACKLOG.md` (cross-check against the tree; it lags reality).
4. **Author** each trope: preamble → imports/assoc/imply → an **agent-named `[&Verb]` event rule** → a
   concrete vignette that CARRIES the discriminator (SKILL §4b). Vary story / medium / era / scale of stakes.
5. **Self-recognize** (the bar below). Per file: `tropelang gate <f>` prints `GATE PASS`, and
   `tropelang shape <f>` confirms the file's own rule at **conf 1.00**.
6. **Finalize once** — `tropelang assemble trl/tropes/corpus.toml` (regen `index.trl`) + CHANGELOG
   `### Added` lines; confirm `tropelang selfcheck trl/tropes/corpus.toml --corpus file://trl` is **N/N (100%)**.
7. **Push** a `convert/<batch>` branch (Mode A) — CI opens the bot-authored PR to `main`. **Never** open
   the PR with the MCP token (the identity rule below).

### The recognition bar (keep selfcheck at 100%)

Every trope must confirm its OWN vignette — corpus `selfcheck` self-recognition stays at **N/N**. Full
detail is in SKILL §4b / STYLE §8; the load-bearing mechanics learned the hard way:
- **Recall keys on the event's `agent`.** A rule whose `when:` is only static tags / `@rel` edges /
  `count(...)` is never recalled (conf 0.00 on its own vignette). Anchor on an `evt … [&Verb(agent=…, …)]`;
  a *patient-only* event (`[&Strikes(target=$c)]`) is **not** recalled — name an agent (add the striker).
- **Coverage re-checks tags LITERALLY, on event-bound entities only.** Assert the discriminating tags in
  the vignette where the prose already states them — don't leave them to be derived by another rule's `then:`.
- **Engine version matters.** Use the latest `cli-*` (currently ≥ 0.4.4). ≥ 0.4.2 expands coverage over the
  `imply` closure (refined relations confirm via their base class); **≥ 0.4.3 enforces binding-inequality
  (`$x != $y`) at recognition** — older builds honored it only at eval, so distinctness-based rules
  (Pincer, Love Dodecahedron) over-fired in `shape`.
- **Found genre vocabulary locally** (promotion model): a trope needing a new `prop`/`verb` (e.g. magic)
  declares it in its own file (cf. `the_wizard.trl`'s `prop Arcane`/`verb Casts`, `siege.trl`'s `verb
  Undermines`), not in the realist prelude.

### Sourcing & coverage review (archive-access environments)

This sandbox **firewalls `allthetropes.org`** (curl/WebFetch → 403; WebSearch snippets are the only
channel). **In an environment WITH archive access, fetch the wiki directly** — for each trope's
definition (record the URL in `@source`) and for the high-profile index pages. Never tvtropes.org.

To (re-)run the coverage review — corpus vs the canonical lists:
```sh
# Corpus inventory (trope titles):
for f in $(git ls-files 'trl/tropes/**/*.trl' | grep -v index.trl); do
  grep -m1 '@trope' "$f" | sed 's/.*@trope[[:space:]]*//'; done | sort -u
```
Diff that against the allthetropes high-profile indexes:
- **Category:Omnipresent Tropes** — https://allthetropes.org/wiki/Category:Omnipresent_Tropes
- **Omnipresent Tropes** (curated) — https://allthetropes.org/wiki/Omnipresent_Tropes
- **Universal Tropes** and the cast / plot-structure indexes.

**Known high-profile gaps (2026-06 review — verify against the live lists):** ~~An Aesop · Big Good ·
Villain Protagonist · Five-Man Band · Status Quo Is God · Failure Is the Only Option · Idiot Ball ·
Take a Third Option~~ (✅ done, the `convert/high-profile-gaps` branch) · Character Development (the
general trope; instances like Coming of Age / Redemption Arc exist) · Title Drop · Genre Savvy.
Suggested next batch: Character Development, Title Drop, Genre Savvy (+ re-run the coverage review
against the live lists for fresh candidates).

## The identity rule (why this exists)

`main` is protected by a ruleset requiring **1 approving review** before merge. GitHub will not
let an account approve its own PR. Therefore:

> The conversion bot must **author** PRs under an identity that is **not** the human who approves them.

- ❌ Bot authenticates as a person → that person can never approve → every merge needs an admin
  *bypass*, so the review gate never actually runs.
- ✅ Bot authors PRs under the **GitHub App `…[bot]`** identity → a human maintainer approves and
  merges normally, gate intact.

> **The PR *author* is what matters — and it follows the token that calls the create-PR API, not the
> git commit author.** A Claude Code *web* session is **not** a separate identity: its GitHub token
> (the `mcp__github__*` tools) is the **maintainer's own account** — `mcp__github__get_me` returns the
> maintainer. So a PR opened with the MCP is *maintainer-authored* and hits the self-approval wall, even
> if the commits are authored by `claude`/the bot. **Never open a conversion PR with the MCP token.**
> Author it with the App instead (the CI workflow below, or a minted App token). Corollary: **don't
> push commits to a PR you intend to approve** — some rulesets also bar the last pusher from approving.

The automated quality bar is the **`gate` workflow** (`.github/workflows/gate.yml`): it runs
`tropelang gate` on every changed `.trl` with no secrets and a read-only token. The human approval
on top is an editorial spot-check, not a line-by-line validation.

## The `tropelang` CLI (required for the gate, both modes)

> **The CLI is NOT pre-installed — install it first thing, every session.** The remote execution
> environment is ephemeral (the container is reclaimed after inactivity and re-cloned fresh), so the
> `tropelang` binary never persists between sessions. `tropelang gate`, `shape`, `assemble`, and
> `selfcheck` — the whole loop — depend on it, so install it before anything else and confirm
> `tropelang version` prints the expected engine version.

The gate (`skills/trope-to-tropelang/scripts/gate.sh` → `tropelang gate`) needs the **`tropelang`
engine CLI** on `PATH`. The engine source is private, so install the **prebuilt binary attached to this
repo's own GitHub release** — do **not** use `cargo install tropelang-cli` (not published on crates.io)
or `cargo install --git …/TropeLang` (private repo; the clone prompts for credentials):

```sh
# Resolve the latest CLI release asset. The tag is cli-vX.Y.Z; the Linux asset is tropelang-x86_64-linux.
# (Via the GitHub MCP: mcp__github__get_latest_release, or the API below.)
REL="cli-v0.4.4"   # ← use the latest cli-* release tag (resolve it, don't hardcode this one)
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

## Finalize the batch (coordinator step — do this before the PR, both modes)

After all tropes for the batch are added and each passes the gate, run the coordinator finalize once,
then commit everything together. The `gate` workflow enforces both of these on the PR.

```sh
# 1. Rebuild the registry from the new tropes (the gate's "index in sync" check = assemble --check).
tropelang assemble trl/tropes/corpus.toml          # regenerates trl/tropes/index.trl

# 2. Append the changelog delta — one line per trope, from each trope's preamble, under
#    `## [Unreleased]` → `### Added` in CHANGELOG.md:  - **<TropeName>** (<category>) — <source>

# 3. Stage the tropes + the regenerated index + the changelog in ONE commit.
git add trl/tropes/<path>/*.trl trl/tropes/index.trl CHANGELOG.md
```

> Why `index.trl` is committed here and not during conversion: the "never touch `index.trl`" guardrail
> is for *parallel* conversion agents (they'd collide on it). The coordinator assembles it **once**, at
> the end — a stale index fails the gate's `assemble --check`.

## Mode A — Claude Code on the web (interactive, the default today)

An interactive web session works on its own development branch over the session's git remote (a local
proxy). It **cannot author the PR itself** — its `mcp__github__*` token is the maintainer's account
(see the identity rule above). So it pushes a **`convert/**` branch** and lets CI open the PR as the
bot. `gh` is not available in-session; use `mcp__github__*` for *reads* (CI status, comments) only.

```sh
# Finalize the batch (above), commit, and push a convert/** branch over the session remote.
git commit -m "Convert <batch-name>"
git push -u origin convert/<batch-name>
```

The push triggers **`.github/workflows/open-conversion-pr.yml`**, which mints a conversion-App token
and opens the PR to `main` authored by `tropelang-conversion-bot[bot]` — so you, the maintainer, can
approve it. Then the `gate` workflow runs on the PR. (One-time setup: add the repo secrets
`CONVERSION_APP_ID` and `CONVERSION_APP_PRIVATE_KEY`; see the workflow header.)

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

# 1. Branch off main, convert, gate locally, finalize the batch (assemble + changelog, above).
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
literal). (In Mode A the same App opens the PR, just from CI instead of from a minted token.)

---

## Guardrails (both modes)

- **Conversion agents never hand-edit `trl/tropes/index.trl`.** It's rebuilt deterministically by the
  coordinator's single `tropelang assemble trl/tropes/corpus.toml` at the **end** of the batch (the
  "Finalize" step), which also mints the concept entry from your preamble metadata (carry full
  `@trope/@category/@source/@domain`). During conversion it's hands-off (parallel agents collide on it);
  the finalized index **is** committed in the PR — a stale one fails the gate's `assemble --check`.
- **Append the changelog delta in the finalize step** — one line per trope in `CHANGELOG.md`, so each
  batch carries its own `### Added` entries.
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
