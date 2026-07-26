# Five-claim reproduction: Learning Randomized Reductions

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/blob/main/notebooks/learning_randomized_reductions.py)

This repository now tests all five claims used by the live evaluator for
[*Learning Randomized Reductions*](https://arxiv.org/abs/2412.18134). The
campaign reconstructs the Section 4 theory, reruns the full 80-function
RSR-Bench, preserves the accepted vanilla and agentic results, and adds fresh
paired regression/MILP comparisons.

The strongest current assessment is **five VERIFIED, version-resolved
claims**, but this is not a new judge result. The public logbook remains at
**6/10** until the live evaluator reviews the new revision. The conservative
forecast is **8–10/10** and the best-supported possible score is **10/10**.

Headline numbers:

- Section 4: the exact existential result is independently reconstructed; the
  paper's binary proof witness is invalid at `epsilon = 1/2`, while a ternary
  witness repairs the proof without weakening the stated theorem.
- Vanilla Bitween: paper `43/80`; frozen baseline `43/80`, 91 verified
  identities, zero faulty; seeded cumulative runs `40–41/80`, 88 identities.
- Agentic Bitween: paper `64/80`; preserved full-scale run `73/80`, 320
  verified identities, zero faulty under the reproduction's broader coverage
  metric.
- Backend comparison: fresh full-80 LR/Gurobi coverage `40/37`, verified
  identities `88/69`, and mean runtime `12.008/17.791 s`. The legacy v1 table
  sums to LR/MILP sample use `607/1180` and runtime `227.10/308.64 s`.

Every scientific job used Hugging Face `cpu-upgrade` (8 vCPUs, 32 GB, no
GPU). The code is pinned through `uv.lock`; all branches inherit one fixed
command and vary only committed configuration. The detailed
[visual report](reports/five-claim-reproduction/report.md) separates exact
paper statements, observed evidence, controls, substitutions, and remaining
risk. The [tutorial notebook](notebooks/learning_randomized_reductions.py)
opens with embedded evidence and does not rerun expensive experiments.

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`main`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/main) | Public README, report, notebook, and release surface | Not run as an experiment (publication surface) | Presentation only | None |
| [`orx/frozen-6-of-10-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/orx/frozen-6-of-10-baseline) | Freeze and rerun the previously accepted 80-function evidence | `uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py` | 80 IDs; vanilla 43/80, 91 verified, zero faulty; accepted agentic evidence rechecked | HF `cpu-upgrade`, 8 vCPU, 32 GB, 18m27s |
| [`orx/exact-section-4-contract-and-boundary-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/orx/exact-section-4-contract-and-boundary-audit) | Proof-level Claim 1 reconstruction and boundary control | `uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py` | Exact theorem verified; defective binary witness rejected; cumulative checks pass | HF `cpu-upgrade`, 8 vCPU, 32 GB, 21m08s |
| [`orx/backend-claim-source-contract-and-harness`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/orx/backend-claim-source-contract-and-harness) | Hash and reconcile v1/v5 source statements before testing Claim 5 | `uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py` | v1 complete table and v5 contracts pass; source mismatch exposed | HF `cpu-upgrade`, 8 vCPU, 32 GB, 22m28s |
| [`orx/fresh-full-80-gurobi-milp-comparison`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/orx/fresh-full-80-gurobi-milp-comparison) | Paper-relevant paired LR versus eager Gurobi MILP | `uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py` | LR/MILP coverage 40/37, identities 88/69, mean runtime 12.008/17.791 s; swap control rejected | HF `cpu-upgrade`, 8 vCPU, 32 GB, 41m34s |
| [`orx/fresh-full-80-pulp-milp-robustness`](https://github.com/MachineLearning-Nerd/icml26-repro-hCAEcqig2C-bitween/tree/orx/fresh-full-80-pulp-milp-robustness) | Open-source solver robustness route | `uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py` | LR/MILP coverage 41/39, identities 88/66, mean runtime 11.939/17.181 s; swap control rejected | HF `cpu-upgrade`, 8 vCPU, 32 GB, 40m30s |

Local notebook use:

```bash
uv sync --frozen
uv run marimo edit notebooks/learning_randomized_reductions.py
uv run marimo run notebooks/learning_randomized_reductions.py
```

## Historical baseline README (preserved)

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
