# Claim 5 versioned source audit

The exact source statement depends on the paper version. Both source archives
were retrieved with an explicit `OpenResearch-Reproduction/1.0` User-Agent on
2026-07-26.

- v1 source: `https://arxiv.org/e-print/2412.18134v1`, SHA-256
  `c9483e7747bead779af4d5691438feac34e9c38af77cb4fbe4928c90f2f5890c`.
- v5 source: `https://arxiv.org/e-print/2412.18134`, SHA-256
  `556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f`.
  The v5 PDF SHA-256 is
  `93cab4aa8cec06434b704e639bab87dd15ea95ac46a335961138a94fc1bae2b8`.

## The judge paraphrase is not one paper statement

The judge paraphrase says that regression beats MILP on nonlinear-invariant
benchmarks in sample count and runtime, citing Table 2. In v1:

- LR versus MILP is evaluated on the 40-function RSR-Bench in Table 1 and
  Figure 3.
- Table 2 is the nonlinear-invariant experiment, but its systems are Bitween,
  DIG, and SymInfer. It has no MILP column.

In v5, the nonlinear-invariant table is absent. LR versus MILP is instead
reported on the expanded 80-function RSR-Bench in the abstract, evaluation
section, and aggregate-results table.

The reproduction therefore does not silently replace the source. It audits
the complete legacy table and performs a fresh full-domain test of the current
v5 LR/MILP claim.

## Exact legacy quantifiers and a source discrepancy

The v1 prose reports aggregate sample use `1095` (MILP) versus `594` (LR) and
runtime `187.47 s` versus `130.53 s`. Exhaustively summing all rows transcribed
from v1 Table 1 gives `1180` versus `607` samples and `308.64 s` versus
`227.10 s`.

Among the 39 rows with comparable sample counts, LR uses fewer samples on 29,
the same number on 10, and more on zero. One row has no successful sample
count for either backend. LR is faster on 11 of 40 rows and slower on 29, even
though its aggregate runtime is lower because the MILP tail is much heavier.
Thus the paper's Figure 3 prose that all points are strictly below `y=x` is
not literally true for samples or per-function runtime.

## Current contract

For v5, the canonical committed table reports MILP 74 identities and 51%
function coverage at 11 seconds average, versus LR 87 identities and 54%
coverage at 5 seconds average. A fresh paired run must reproduce these
directions on all 80 functions; the committed table is context, not the fresh
verification.
