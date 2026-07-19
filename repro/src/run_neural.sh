#!/usr/bin/env bash
# Claim 3 — "Neural-Research" baseline: the SAME agentic harness + SAME model as
# A-Bitwen, but with the Bitwen custom tools DISABLED (bare --custom_tools),
# leaving only the sequential-thinking MCP tool. Same endpoint/budget as
# run_agentic.sh so the comparison is apples-to-apples.
set -euo pipefail

MODEL=${MODEL:-Qwen/Qwen2.5-72B-Instruct-AWQ}
PORT=${PORT:-8000}
RES=${RES:-outputs/neural-qwen72b-awq}
MAX_TOKENS=${MAX_TOKENS:-32000}
TIMEOUT=${TIMEOUT:-1800}

# Assumes vLLM is already serving $MODEL (start it via run_agentic.sh first,
# or run the vllm serve block there). Health check:
until python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:$PORT/health')" 2>/dev/null; do
  echo "waiting for vLLM on $PORT..."; sleep 5
done

mkdir -p "$RES"
for MOD in bitween.evaluation.evaluation_rsr_bench_agentic_paper \
           bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended; do
  echo ">>> Neural baseline: $MOD"
  python -m "$MOD" \
    --agent_type openai --model_id "$MODEL" \
    --base_url "http://127.0.0.1:$PORT/v1" --api_key dummy \
    --max_tokens "$MAX_TOKENS" --timeout_sec "$TIMEOUT" --res_dir "$RES" \
    --custom_tools          # <-- BARE: disables infer_property_tool + symbolic_verify_tool
done
echo "Neural baseline done -> $RES"
