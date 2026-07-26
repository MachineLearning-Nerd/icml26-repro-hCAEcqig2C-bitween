# Claim 5 — regression versus MILP

## Verdict

**VERIFIED** · confidence **MEDIUM**

The verdict is version-resolved because the evaluator sentence combines two
different source experiments.

## Source contract before measurement

The evaluator wording is: “On nonlinear invariant benchmarks, the regression
backend outperforms the MILP backend in sample count and runtime (Table 2).”
No paper version contains that exact comparison:

- v1 SHA-256
  `c9483e7747bead779af4d5691438feac34e9c38af77cb4fbe4928c90f2f5890c`
  compares LR/MILP on the 40-function RSR-Bench in Table 1/Figure 3;
- v1 Table 2 compares Bitween, DIG, and SymInfer on nonlinear invariants and
  has no MILP column;
- v5 SHA-256
  `556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f`
  removes that nonlinear-invariant experiment and compares LR/MILP on the
  expanded 80-function RSR-Bench.

The machine-readable [contract](../../evidence/claim5/claim_contract.json),
[source audit](../../evidence/claim5/source_audit.md), and
[source-audit output](../../evidence/claim5/source_audit_output.json) expose
all anchors and quantifiers.

## Route 1: complete legacy table

The verifier transcribes and checks all 40 v1 Table 1 rows:

| Source | MILP samples | LR samples | MILP runtime | LR runtime |
|---|---:|---:|---:|---:|
| v1 prose | 1,095 | 594 | 187.47 s | 130.53 s |
| Sum of every Table 1 row | 1,180 | 607 | 308.64 s | 227.10 s |

LR uses strictly fewer samples on 29 comparable rows, the same on 10, more on
zero, with one missing LR value. LR is faster on 11 rows and slower on 29,
although its complete-table aggregate runtime is smaller. These qualifications
are evidence, not suppressed discrepancies.

Download the [40-row CSV](../../evidence/claim5/claim5_v1_table40.csv) and
[executable source verifier](../../evidence/claim5/verify_backend_source.py).
A 39-row truncation control is rejected.

## Route 2: fresh paper-relevant full-80 Gurobi comparison

The paired run uses the same commit, seed 42, timeout, environment, and fixed
command for LR and eager Gurobi MILP:

| Metric | LR | Gurobi MILP |
|---|---:|---:|
| Functions | 80 | 80 |
| Functions with a verified identity | 42 | 38 |
| Verified identities | 91 | 70 |
| Faulty identities | 0 | 0 |
| Mean runtime per function | 10.44425 s | 14.450125 s |
| Total runtime | 835.54 s | 1,156.01 s |

Paired directions: LR has more identities on 18 functions, MILP on 11, equal
on 51; LR is faster on 38 and MILP on 42. The exact current contract—more LR
coverage and identities, lower average time, zero faulty on both—passes.
A label-swap mutation is rejected.

Download [raw Gurobi aggregates](../../evidence/claim5/comparison_gurobi.json),
the [complete 80 paired rows](../../evidence/claim5/rows_gurobi.json), and the
[independent comparison parser](../../evidence/claim5/compare_backends.py).
The rows were reconstructed from the immutable orx log by a separate
[log extractor](../../evidence/claim5/extract_backend_log_rows.py), which
cross-checks every aggregate and exits nonzero on disagreement.

## Route 3: solver-substitution robustness

The same paired full-80 route with open-source PuLP gives:

| Metric | LR | PuLP MILP |
|---|---:|---:|
| Functions with a verified identity | 41 | 39 |
| Verified identities | 88 | 66 |
| Faulty identities | 0 | 0 |
| Mean runtime per function | 11.938875 s | 17.180875 s |

The label-swap mutation is again rejected. PuLP is robustness evidence only,
not a substitute for the paper-relevant Gurobi route. Download
[raw PuLP results](../../evidence/claim5/comparison_pulp.json).
The [complete PuLP paired rows](../../evidence/claim5/rows_pulp.json) pass the
same independent aggregate cross-check.

## Sample metric limitation

The current v5 harness prints a derived average `Sample Complexity`; it is not
the v1 `used/budget` table field and is observed on different numbers of
successful functions. Its raw final Gurobi totals are LR `3425.422` over 64
functions and MILP `1216.688` over 46. This fresh metric numerically favors
MILP and is **not** presented as a reproduction of the legacy sample-count
claim.

The Claim 5 verdict rests on the exact current coverage/identity/runtime
contract and the complete legacy sample-table audit. Confidence is MEDIUM
because an evaluator might require the impossible conflated experiment rather
than the paper's actual tables. See [method](../../evidence/claim5/method.md),
[limitations](../../evidence/claim5/limitations.md), and
[run provenance](../../evidence/claim5/backend_run_provenance.json).
