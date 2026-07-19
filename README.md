# Repro — Learning Randomized Reductions (Bitwen), ICML 2026

Reproduction of *Learning Randomized Reductions* (Bitwen) for the
[ICML 2026 Agent Reproduction Challenge](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge).
Paper: ICML 2026 spotlight · [arXiv 2412.18134](https://arxiv.org/abs/2412.18134) ·
OpenReview `hCAEcqig2C` · code: [ferhaterata/learning-randomized-reductions](https://github.com/ferhaterata/learning-randomized-reductions)
(pinned commit `e13d4b59`, run unmodified).

Bitwen discovers **randomized self-reductions (RSRs)** — algebraic identities that
let you verify/self-correct/private-compute a function by evaluating it at
correlated random points. It ships in two variants: **V-Bitwen** (symbolic
regression) and **A-Bitwen** (LLM agent proposing novel query functions).

## Official claims (6 pts max)
1. Vanilla Bitwen finds RSRs for 43/80 functions (54%), incl. the first sigmoid reduction.
2. Agentic Bitwen finds RSRs for 64/80 functions (80%).
3. Agentic Bitwen outperforms pure neural baselines on discovery + verification.

## Status
| Claim | Status | Evidence |
|---|---|---|
| **C1 (Vanilla)** | ✅ substantially reproduced (CPU, full scale) | 87 verified identities (exact match); sigmoid RSR reproduced; 39/80 coverage vs 44 canonical |
| C2 (Agentic) | ⏳ scripts ready, run on Colab GPU + vLLM | `repro/src/run_agentic.sh` |
| **C3 (vs neural)** | **full-scale GPT-OSS counterexample** | three matched seeds: neural discovery 74/77/72 vs agentic 73/72/71; agentic verification accuracy remains higher |

## Repo layout
```
upstream/                     pinned, unmodified Bitwen (commit e13d4b59)
repro/
  configs/vanilla_lr.yaml     C1 config
  src/run_vanilla.py          drives both harness modules (all 80), seed-controlled
  src/aggregate.py            parse logs -> summary.csv + canonical cross-check
  src/verify_independent.py   independent SymPy + numeric-falsifier negative control
  src/sigmoid_check.py        focused sigmoid-RSR demo (C1 clause)
  src/run_agentic.sh          Colab: vLLM + A-Bitwen over 80 (C2)
  src/run_neural.sh           Colab: neural baseline, same model (C3)
  src/compare_agentic_neural.py  C3 comparison table
  src/claim3_falsification.py  primary paired, no-union C3 audit
  tests/test_verify.py        unit tests for the falsifier (4/4 passing)
outputs/
  vbitween-lr/seed*/          per-function .txt logs + summary.csv
  canonical/                  authors' canonical results CSV
  c3_primary_paired_audit.json  three-seed primary C3 audit
docs/                         methodology.md, backend-substitution.md
.trackio/                     Trackio logbook (publishes to a public HF Space)
```

## Reproduce Claim 1 (CPU)
```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python numpy sympy scipy pandas scikit-learn joblib tqdm func-timeout pulp z3-solver pycparser python-dotenv gurobipy pytest
uv pip install --python .venv/bin/python --no-deps -e ./upstream
.venv/bin/python repro/src/run_vanilla.py --seed 42 --res_dir outputs/vbitween-lr/seed42
.venv/bin/python repro/src/aggregate.py --res_dir outputs/vbitween-lr/seed42 --canonical outputs/canonical/Bitween-Results(Sheet1-ICML).csv
.venv/bin/python repro/src/verify_independent.py --res_dir outputs/vbitween-lr/seed42
```

## Reproduce Claims 2–3 (Colab GPU + vLLM)
See `docs/backend-substitution.md`. Serve an open model (Qwen2.5-72B-Instruct-AWQ)
with vLLM, then `bash repro/src/run_agentic.sh` (C2) and `bash repro/src/run_neural.sh`
(C3) against the same endpoint, and compare with `compare_agentic_neural.py`.

## Logbook
`trackio logbook publish <hf-user>/hCAEcqig2C` publishes the Trackio logbook in
`.trackio/` to a public HF Space (tags `icml2026-repro`, `paper-hCAEcqig2C`).
Requires `hf auth login` (write token).
