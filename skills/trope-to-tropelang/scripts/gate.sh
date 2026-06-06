#!/usr/bin/env bash
# Acceptance gate for a converted trope. An agent must see `── GATE PASS ──` before returning its file.
#   usage: bash scripts/gate.sh <file.trl>
# Gates (all in the engine CLI now): preamble · validates · round-trips (log-register) · DRY · drams.
#
# Requires the `tropelang` CLI on PATH. The engine source is private, so install the prebuilt binary
# from this repo's latest `cli-*` GitHub release (see CONVERSION_BOT.md, "The tropelang CLI"):
#   curl -fsSL -o /tmp/tropelang \
#     https://github.com/kelnishi/tropelang-standard/releases/download/<cli-vX.Y.Z>/tropelang-x86_64-linux
#   sha256sum /tmp/tropelang   # verify against the release asset digest, then:
#   install -m 0755 /tmp/tropelang /usr/local/bin/tropelang
# (Do NOT `cargo install tropelang-cli` — not on crates.io — nor clone the private engine repo.)
# The corpus root (with trl/) must be the working directory so `--corpus file://trl` resolves.
set -uo pipefail
exec tropelang gate "${1:?usage: gate.sh <file.trl>}"
