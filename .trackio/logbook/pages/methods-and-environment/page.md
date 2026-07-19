# Methods and environment


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c8795f5d16be", "created_at": "2026-07-16T06:25:18+00:00", "title": "Methods & environment"}
-->
**Paper:** *Learning Randomized Reductions* (Bitwen), ICML 2026 spotlight — arXiv [2412.18134](https://arxiv.org/abs/2412.18134), OpenReview `hCAEcqig2C`.
**Code:** github.com/ferhaterata/learning-randomized-reductions, pinned commit `e13d4b59`, run **unmodified**.

**Environment:** Python 3.12.13 (upstream needs >=3.11,<3.13; host has 3.14 so pinned via uv); numpy 2.5.1, sympy 1.14.0, scikit-learn 1.9.0, scipy 1.18.0, z3-solver 4.16, pulp, gurobipy 13.0.2 (imported upstream; unused by LR path). Only LR-path deps installed — no PySR/Julia, GPLearn, Strands, or MCP needed for Claim 1.

**Hardware:** 4 vCPU, 15 GB RAM, no usable GPU (GTX 1050 4 GB). Claim 1 is pure CPU + SymPy, so this **is full scale locally.** Claims 2–3 use Google Colab GPU + vLLM (see backend-substitution doc).

**Drivers:** `repro/src/run_vanilla.py` (runs both harness modules 1–40 + 41–80 via runpy with a fixed seed), `repro/src/aggregate.py` (parses logs, cross-checks canonical CSV), `repro/src/verify_independent.py` (independent negative control).
