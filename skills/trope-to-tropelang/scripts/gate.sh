#!/usr/bin/env bash
# Acceptance gate for a converted trope. An agent must see ALL PASS before returning its file.
#   usage: bash skills/trope-to-tropelang/scripts/gate.sh <file.trl>
# Gates: preamble complete · validates · round-trips (log-register) · DRY report · drams (informational).
set -uo pipefail
f="${1:?usage: gate.sh <file.trl>}"
root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"
fail=0
echo "── gate: $f ──"

# 1 · preamble completeness
for k in trope category source domain; do
  grep -qE "^//\s*@$k\b" "$f" || { echo "✗ preamble missing @$k"; fail=1; }
done
[ $fail -eq 0 ] && echo "✓ preamble (@trope/@category/@source/@domain)"

# 2 · structural validator (errors fail; warnings ok)
if python3 skills/trope-to-tropelang/scripts/validate_tropelang.py "$f" 2>&1 | grep -qE "✗|ERROR|error:"; then
  echo "✗ validator errors"; python3 skills/trope-to-tropelang/scripts/validate_tropelang.py "$f" 2>&1 | grep -E "✗|error" | head; fail=1
else echo "✓ validates"; fi

# 3 · round-trip (a self-contained trope is log-register and MUST round-trip; if it declares
#     concept/verb/state it's library-register — that's a smell: move vocabulary to a module)
# fidelity.rs prints ok|library-register to STDOUT; cargo build noise + parse-error detail go
# to STDERR and must not be read as the result (a cold-build warning was tripping this).
rt="$(cargo run --quiet --example fidelity -- "$f" 2>/dev/null)"
case "$rt" in
  ok) echo "✓ round-trips" ;;
  library-register*) echo "⚠ library-register: a TROPE should import vocabulary, not declare concept/verb/state — move it to a module" ;;
  *) echo "✗ round-trip: $rt"; fail=1 ;;
esac

# 4 · DRY — inline-invented tags to consider consolidating (informational)
echo "· DRY (consolidate inline-invented tags if they duplicate corpus vocab):"
python3 skills/trope-to-tropelang/scripts/corpus_reuse.py "$f" 2>&1 | grep -iE "inline|reuse|consolidat" | head -4 || echo "  (none flagged)"

# 5 · drams (informational; for a NEW MODULE confirm an unrelated eval did not move — scaffold rule)
echo "· drams: $(python3 skills/trope-to-tropelang/scripts/drams.py "$f" 2>&1 | sed -n '2p' | sed 's/^  //')"

[ $fail -eq 0 ] && echo "── GATE PASS ──" || { echo "── GATE FAIL ──"; exit 1; }
