#!/usr/bin/env bash
# Acceptance gate for a converted trope. An agent must see `── GATE PASS ──` before returning its file.
#   usage: bash scripts/gate.sh <file.trl>
# Gates (all in the engine CLI now): preamble · validates · round-trips (log-register) · DRY · drams.
#
# Requires the `tropelang` CLI on PATH (the published engine):
#   cargo install tropelang-cli              # from crates.io (release)
#   cargo install --git https://github.com/kelnishi/TropeLang tropelang-cli   # pre-release
# The corpus root (with trl/) must be the working directory so `--corpus file://trl` resolves.
set -uo pipefail
exec tropelang gate "${1:?usage: gate.sh <file.trl>}"
