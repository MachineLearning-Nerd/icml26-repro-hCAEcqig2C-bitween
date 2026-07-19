#!/usr/bin/env bash
# Multi-seed gpt-oss-120b full-80 campaign for C3. Runs 2 extra seeds of each
# condition (s2, s3) to union with the existing s1 (outputs/{abitween,neural}-gptoss).
# Each run is an independent np.random sample (the harness has no seed arg), so
# repeated runs ARE the independent seeds we union over.
set -uo pipefail
PAPER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PAPER"; source .venv/bin/activate
LOG="$PAPER/outputs/_multiseed_log.txt"; : > "$LOG"

run() {  # <cond> <seed>
  echo "### $(date -u +%FT%TZ) START $1-s$2 ###" | tee -a "$LOG"
  bash repro/src/run_seed.sh "$1" "$2" >> "$LOG" 2>&1
  echo "### $(date -u +%FT%TZ) END   $1-s$2 exit=$? ###" | tee -a "$LOG"
}

# seed 2 (both conditions), then seed 3 (both conditions)
run abitween 2
run neural   2
run abitween 3
run neural   3

echo "=== per-seed single-run comparison ===" | tee -a "$LOG"
for s in "" -s2 -s3; do
  A="outputs/abitween-gptoss${s}"; N="outputs/neural-gptoss${s}"
  [ -d "$A" ] && [ -d "$N" ] && .venv/bin/python repro/src/compare_agentic_neural.py --agentic "$A" --neural "$N" 2>&1 | tee -a "$LOG"
done

echo "=== 3-SEED UNION ===" | tee -a "$LOG"
.venv/bin/python repro/src/union_compare.py \
  --agentic outputs/abitween-gptoss,outputs/abitween-gptoss-s2,outputs/abitween-gptoss-s3 \
  --neural  outputs/neural-gptoss,outputs/neural-gptoss-s2,outputs/neural-gptoss-s3 2>&1 | tee -a "$LOG"

echo "MULTISEED_DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
