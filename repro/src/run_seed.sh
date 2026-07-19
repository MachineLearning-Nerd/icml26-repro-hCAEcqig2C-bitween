#!/usr/bin/env bash
# Full-80 RSR-Bench run for ONE seed of ONE condition (gpt-oss-120b via HF router),
# into outputs/<COND>-gptoss-s<SEED>. Mirrors run_agentic_local.sh but parameterizes
# the res_dir so we can run multiple seeds and union them.
#
#   bash repro/src/run_seed.sh <cond:abitween|neural> <seed> [model_id]
set -uo pipefail
PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PAPER"; source .venv/bin/activate
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"; export OPENAI_API_KEY="$HF_TOKEN"

COND="${1:?cond abitween|neural}"; SEED="${2:?seed int}"; MODEL="${3:-openai/gpt-oss-120b}"
BASE_URL="https://router.huggingface.co/v1"
RES="$PAPER/outputs/${COND}-gptoss-s${SEED}"
MAX_TOKENS="${MAX_TOKENS:-32000}"; TIMEOUT="${TIMEOUT:-900}"
mkdir -p "$RES"

if [ "$COND" = "abitween" ]; then TOOLS=(--custom_tools infer_property_tool symbolic_verify_tool)
else TOOLS=(--custom_tools); fi

cd "$PAPER/upstream"
PY="$PAPER/.venv/bin/python"
for MOD in bitween.evaluation.evaluation_rsr_bench_agentic_paper \
           bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended; do
  echo ">>> [s${SEED} ${COND}] $MOD $(date -u +%FT%TZ)"
  "$PY" -m "$MOD" --agent_type openai --model_id "$MODEL" \
    --base_url "$BASE_URL" --api_key "$HF_TOKEN" \
    --max_tokens "$MAX_TOKENS" --timeout_sec "$TIMEOUT" \
    --res_dir "$RES" "${TOOLS[@]}"
  echo "<<< [s${SEED} ${COND}] $MOD exit=$? $(date -u +%FT%TZ)"
done
echo "DONE s${SEED} ${COND} -> $RES"
# build summary.csv so union_compare/compare can read it immediately
cd "$PAPER"; "$PY" repro/src/aggregate.py --res_dir "$RES" >/dev/null 2>&1 || true
echo "SEED_DONE s${SEED} ${COND} $(date -u +%FT%TZ) -> $RES"
