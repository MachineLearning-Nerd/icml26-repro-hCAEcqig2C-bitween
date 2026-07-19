#!/usr/bin/env bash
# Claim 2 — Agentic Bitween (A-Bitwen) over all 80 RSR-Bench functions.
# Runs on Google Colab GPU (A100 80GB recommended) serving an open model via vLLM,
# pointed at by the upstream OpenAI-compatible agent path (no code changes).
# See docs/backend-substitution.md for the model-swap rationale.
set -euo pipefail

MODEL=${MODEL:-Qwen/Qwen2.5-72B-Instruct-AWQ}   # ~40GB, fits A100 80GB; Hermes tool-calling
PORT=${PORT:-8000}
RES=${RES:-outputs/abitween-qwen72b-awq}
MAX_TOKENS=${MAX_TOKENS:-32000}
TIMEOUT=${TIMEOUT:-1800}

# --- 0. one-time Colab setup (uncomment on first run) -----------------------
# apt-get update && apt-get install -y nodejs npm && npm i -g npx   # MCP sequential-thinking
# pip install vllm
# uv pip install -e ./upstream --no-deps && uv pip install <LR+agentic deps> strands-agents mcp

# --- 1. serve the open model (flags mirror upstream evaluation.slurm) --------
vllm serve "$MODEL" --host 127.0.0.1 --port "$PORT" \
  --gpu-memory-utilization 0.9 --max-model-len 32000 \
  --enable-auto-tool-choice --tool-call-parser hermes &
VLLM_PID=$!
trap 'kill $VLLM_PID 2>/dev/null || true' EXIT
until python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:$PORT/health')" 2>/dev/null; do
  echo "waiting for vLLM..."; sleep 5
done
echo "vLLM ready: $MODEL @ http://127.0.0.1:$PORT/v1"

# --- 2. A-Bitwen over all 80 (run base + extended into the same res_dir) -----
mkdir -p "$RES"
for MOD in bitween.evaluation.evaluation_rsr_bench_agentic_paper \
           bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended; do
  echo ">>> A-Bitwen: $MOD"
  python -m "$MOD" \
    --agent_type openai --model_id "$MODEL" \
    --base_url "http://127.0.0.1:$PORT/v1" --api_key dummy \
    --max_tokens "$MAX_TOKENS" --timeout_sec "$TIMEOUT" --res_dir "$RES" \
    --custom_tools infer_property_tool symbolic_verify_tool
done
echo "A-Bitwen done -> $RES"
