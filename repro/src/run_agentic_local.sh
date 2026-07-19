#!/usr/bin/env bash
# Run A-Bitwen (Claim 2) or the neural baseline (Claim 3) LOCALLY via HF Inference
# Providers — no GPU, no Colab. Uses the paper's exact agentic model (gpt-oss-120b),
# which the HF router serves and which follows Bitwen's <answer>Eq(...)</answer> format.
#
#   Usage:  HF_TOKEN=$(hf auth token) bash run_agentic_local.sh abitween   # Claim 2
#           HF_TOKEN=$(hf auth token) bash run_agentic_local.sh neural     # Claim 3
set -uo pipefail

PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$PAPER/.venv/bin/python"

MODEL="openai/gpt-oss-120b"                       # paper's exact model (faithful)
BASE_URL="https://router.huggingface.co/v1"
API_KEY="${HF_TOKEN:?set HF_TOKEN (e.g. HF_TOKEN=$(hf auth token))}"
COND="${1:?usage: $0 abitween|neural}"
RES="$PAPER/outputs/${COND}-gptoss"
MAX_TOKENS="${MAX_TOKENS:-32000}"
TIMEOUT="${TIMEOUT:-1800}"

mkdir -p "$RES"
if [ "$COND" = "abitween" ]; then
  TOOLS=(--custom_tools infer_property_tool symbolic_verify_tool)      # Claim 2: full A-Bitwen
elif [ "$COND" = "neural" ]; then
  TOOLS=(--custom_tools)                                               # Claim 3: tools OFF
else
  echo "condition must be abitween|neural"; exit 2
fi

cd "$PAPER/upstream"   # bitween.ini is package-relative; cwd here for cleanliness
for MOD in bitween.evaluation.evaluation_rsr_bench_agentic_paper \
           bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended; do
  echo ">>> [$COND] $MOD  $(date -u +%FT%TZ)"
  "$PY" -m "$MOD" --agent_type openai --model_id "$MODEL" \
        --base_url "$BASE_URL" --api_key "$API_KEY" \
        --max_tokens "$MAX_TOKENS" --timeout_sec "$TIMEOUT" \
        --res_dir "$RES" "${TOOLS[@]}"
  echo "<<< [$COND] $MOD exit=$?  $(date -u +%FT%TZ)"
done
echo "DONE [$COND] -> $RES"
