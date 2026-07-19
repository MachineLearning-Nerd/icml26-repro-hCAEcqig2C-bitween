# Methodology — Claim 1 (Vanilla Bitwen / V-Bitwen-LR)

## Claim (official, from `claims.json` for `hCAEcqig2C`)
> "Vanilla Bitween discovers RSRs for 43 of 80 functions (54%) in RSR-Bench, including first known reduction for sigmoid"

## What V-Bitwen-LR is
Vanilla Bitwen with the linear-regression backend (`method = MULTIPLE_REGRESSION`,
labeled `mreg (vanilla Bitween)` in the canonical results CSV). It samples the
target function `f` at correlated random points over the fixed query class
`{x+y, x-y, x·y, x, y}`, fits linear/polynomial regressions to discover candidate
algebraic identities (the randomized self-reductions), then **symbolically
verifies** each candidate by SymPy proof-by-simplification (`verify()` in
`upstream/src/bitween/analyzer.py`). No LLM is involved — this is the pure
neuro-symbolic-regression path.

## Reproduction procedure
1. **Unmodified upstream code**, pinned at commit `e13d4b59` (2026-05-31),
   installed editable (`uv pip install -e ./upstream --no-deps`) with only the
   LR-path dependencies (no PySR/Julia, GPLearn, Strands, MCP, or Gurobi license).
2. **All 80 functions** are run by executing both upstream harness modules'
   `__main__` blocks — `evaluation_rsr_bench_paper` (functions 1–40) and
   `evaluation_rsr_bench_paper_extended` (41–80) — via `runpy`, driven by
   `repro/src/run_vanilla.py` with a fixed numpy seed for reproducibility.
3. Each function writes `<test_id>.txt` with `Equations found: N`,
   `Verified (n):`, `Unverified (n):`, `Faulty (n):`, `Unknown (n):`, and
   `Took time:`. `repro/src/aggregate.py` parses these into `summary.csv` and
   cross-checks totals against the authors' canonical CSV's `mreg` block
   (columns 18–21).
4. **Coverage** = number of functions with ≥1 verified identity. For V-Bitwen-LR
   the paper reports RSR count == verified count (87 == 87), so verified-coverage
   is a faithful automatable proxy for the paper's (manually curated) RSR coverage.

## Independent negative control
`repro/src/verify_independent.py` re-checks every recovered verified identity on a
representative registry of functions with **two independent mechanisms**:
- the authors' SymPy verifier, re-run on the recovered equation string; and
- a **numeric falsifier** that `lambdify`s the LHS with the *numeric* `f` and
  evaluates the residual over ~20k random inputs (independent of SymPy).
It also runs **false-positive controls** (deliberately wrong identities) that must
be rejected. Unit tests in `repro/tests/test_verify.py` (4/4 passing) guard the
falsifier on known-true and known-false identities.

## Result (seed 42)
| metric | this repro | canonical |
|---|---|---|
| verified identities | **87** | **87** |
| functions covered | 39/80 (48.8%) | 44/80 (54.3%) |
| unverified | 44 | 46 |
| avg time/function | 11.9 s | 4.8 s |

Total verified identities match exactly. Coverage is ~5 functions below the claim;
the same 87 identities are spread over fewer functions due to library-version drift
(numpy 2.5 / scikit-learn 1.9 / sympy 1.14 vs the paper's pins) and sampling
stochasticity. Multiple seeds characterize the distribution (see the logbook's
Negative-controls page).

The sigmoid RSR is reproduced and independently verified — satisfying the
"including first known reduction for sigmoid" clause.
