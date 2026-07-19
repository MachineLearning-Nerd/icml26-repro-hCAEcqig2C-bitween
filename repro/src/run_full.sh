#!/usr/bin/env bash
# Full-80 RSR-Bench run for ONE condition of an arbitrary model, into outputs/<COND>-<TAG>.
#   bash repro/src/run_full.sh <cond:abitween|neural> <tag> <model_id>
set -uo pipefail
PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PAPER"; source .venv/bin/activate
export HF_TOKEN="$(cat ~/.cache/huggingface/token)"; export OPENAI_API_KEY="$HF_TOKEN"
COND="${1:?cond}"; TAG="${2:?tag}"; MODEL="${3:?model_id}"
BASE_URL="https://router.huggingface.co/v1"
RES="$PAPER/outputs/${COND}-${TAG}"
MAX_TOKENS="${MAX_TOKENS:-32000}"; TIMEOUT="${TIMEOUT:-900}"
mkdir -p "$RES"
[ "$COND" = abitween ] && TOOLS=(--custom_tools infer_property_tool symbolic_verify_tool) || TOOLS=(--custom_tools)
cd "$PAPER/upstream"; PY="$PAPER/.venv/bin/python"
for MOD in bitween.evaluation.evaluation_rsr_bench_agentic_paper \
           bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended; do
  echo ">>> [$COND $TAG] $MOD $(date -u +%FT%TZ)"
  "$PY" -m "$MOD" --agent_type openai --model_id "$MODEL" \
    --base_url "$BASE_URL" --api_key "$HF_TOKEN" \
    --max_tokens "$MAX_TOKENS" --timeout_sec "$TIMEOUT" --res_dir "$RES" "${TOOLS[@]}"
  echo "<<< [$COND $TAG] $MOD exit=$? $(date -u +%FT%TZ)"
done
cd "$PAPER"; "$PY" repro/src/aggregate.py --res_dir "$RES" >/dev/null 2>&1 || true
echo "FULL_DONE $COND $TAG $(date -u +%FT%TZ) -> $RES"
