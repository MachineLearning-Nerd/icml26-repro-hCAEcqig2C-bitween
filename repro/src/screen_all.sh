#!/usr/bin/env bash
# Screen candidate C3 backbones on the 12-function hard subset, both conditions.
# Writes one SUMMARY line per (model, condition) to outputs/screen/_screen_log.txt.
set -uo pipefail
PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PAPER"
source .venv/bin/activate
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"
export OPENAI_API_KEY="$HF_TOKEN"

LOG="$PAPER/outputs/screen/_screen_log.txt"
mkdir -p "$PAPER/outputs/screen"
: > "$LOG"

SUBSET="test_tan,test_cot,test_inverse,test_cos,test_cosh,test_sin,test_sinh,test_log,test_sinc,test_tanh,test_sigmoid,test_softmax2_1"

MODELS=(
  "openai/gpt-oss-120b"
  "deepseek-ai/DeepSeek-V4-Pro"
  "moonshotai/Kimi-K2.6"
  "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
  "Qwen/Qwen3.6-35B-A3B"
  "deepseek-ai/DeepSeek-R1"
)

for M in "${MODELS[@]}"; do
  TAG="${M//\//__}"
  for COND in neural abitween; do
    RES="outputs/screen/${TAG}__${COND}"
    rm -rf "$RES"; mkdir -p "$RES"
    echo "=== $(date -u +%FT%TZ) MODEL=$M COND=$COND ===" | tee -a "$LOG"
    MTOK=12000; TMO=300
    # reasoning models get a bit more headroom
    case "$M" in *R1*|*V4-Pro*) MTOK=16000; TMO=420;; esac
    timeout $((TMO*12+120)) .venv/bin/python repro/src/screen_c3.py \
      --model_id "$M" --condition "$COND" --res_dir "$RES" \
      --functions "$SUBSET" --max_tokens "$MTOK" --timeout_sec "$TMO" \
      2>&1 | grep -E "^\[screen\]|^SUMMARY|^=== |not found|raised|Error|error|Traceback" \
      | tee -a "$LOG"
    echo "--- exit=$? done $M $COND ---" | tee -a "$LOG"
  done
done
echo "ALL_SCREEN_DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
