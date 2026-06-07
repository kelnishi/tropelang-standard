# PR comment payloads (cloud-session path for `bot-comment.yml`)

A cloud Claude Code session has no `gh` and can't hold the conversion App's key — it reaches GitHub
only via `git push`. To post a PR comment **as `tropelang-conversion-bot[bot]`** from such a session,
drop a JSON payload here and push it on a `convert/**` branch. The `bot-comment.yml` workflow posts each
**newly-added** payload once (diff-filter=A), then leaves it in place as an audit log.

Local sessions don't need this — use `gh workflow run bot-comment.yml -f pr=… -f body=…` directly.

## Payload shape

One JSON file per comment. Name it whatever (e.g. `pr38-rogue-one-reply.json`); only `*.json` files are
read.

```json
{
  "pr": 38,
  "body": "Markdown comment body.\n\nMultiple paragraphs are fine.",
  "reply_to": null
}
```

- `pr` — the PR number (integer).
- `body` — the comment Markdown.
- `reply_to` — optional. A **review-comment id** to reply to in-thread (get it from
  `GET /repos/{owner}/{repo}/pulls/{pr}/comments`). Omit or `null` for a top-level PR conversation comment.

## Notes

- Each payload posts **once**, when first added in a push. Editing an existing payload later will **not**
  re-post it (the workflow only acts on added files). To post a correction, add a new payload.
- The bot can comment but **cannot approve** its own PR — approval stays with a human maintainer.
