#!/usr/bin/env bash
# Discriminative C3 screen: run a HARD extended-module subset (inverse-trig,
# discontinuous, transcendental, special — where agentic's regression-on-novel-
# queries should beat pure reasoning) for the given models in BOTH conditions.
# This subset DOES separate discovery (unlike the easy base subset).
# Usage: bash repro/src/screen_discriminative.sh "model1" "model2" ...
set -uo pipefail
PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PAPER"; source .venv/bin/activate
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"; export OPENAI_API_KEY="$HF_TOKEN"
LOG="$PAPER/outputs/screen/_disc_log.txt"; mkdir -p "$PAPER/outputs/screen"; : > "$LOG"

# Hard functions: agentic-favored (arcsin,arccos,log1p,floor,ceil) + genuinely hard
# (erf, gudermannian, continued_fraction_tan, pade_2_2, mobius_cayley, gamma, x_to_x, frac)
SUBSET="test_arcsin,test_arccos,test_log1p,test_floor,test_ceil,test_erf,test_gudermannian,test_continued_fraction_tan,test_pade_2_2,test_mobius_cayley,test_gamma,test_x_to_x"

for M in "$@"; do
  TAG="${M//\//__}"
  for COND in neural abitween; do
    RES="outputs/screen/disc_${TAG}__${COND}"; rm -rf "$RES"; mkdir -p "$RES"
    echo "=== $(date -u +%FT%TZ) DISC MODEL=$M COND=$COND ===" | tee -a "$LOG"
    MTOK=12000; TMO=300; case "$M" in *R1*|*V4-Pro*) MTOK=16000; TMO=420;; esac
    timeout $((TMO*12+120)) .venv/bin/python repro/src/screen_c3.py \
      --model_id "$M" --condition "$COND" --res_dir "$RES" --module extended \
      --functions "$SUBSET" --max_tokens "$MTOK" --timeout_sec "$TMO" \
      2>&1 | grep -E "^\[screen\]|^SUMMARY|^=== |not found|raised|Error|Traceback|RateLimit|Status 4|Status 5" | tee -a "$LOG"
    echo "--- exit=$? done $M $COND ---" | tee -a "$LOG"
  done
done
echo "ALL_DISC_DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
