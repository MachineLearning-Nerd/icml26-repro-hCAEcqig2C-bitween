# Paper and source audit

## Paper

*Learning Randomized Reductions* is by Ferhat Erata, Orr Paradise, Thanos
Typaldos, Timos Antonopoulos, ThanhVu Nguyen, Shafi Goldwasser, and Ruzica
Piskac. The current arXiv record is `2412.18134v5`; it identifies the work as
accepted to ICML 2026 as a Spotlight. The OpenReview identifier is
`hCAEcqig2C`.

Primary links:

- [arXiv record](https://arxiv.org/abs/2412.18134)
- [OpenReview record](https://openreview.net/forum?id=hCAEcqig2C)
- [authors' official code](https://github.com/ferhaterata/learning-randomized-reductions)

## Hash-bound artifacts

The exact downloaded artifacts and URLs are listed in [`sources.json`](../sources.json):

| Artifact | SHA-256 |
|---|---|
| arXiv v1 source archive | `c9483e7747bead779af4d5691438feac34e9c38af77cb4fbe4928c90f2f5890c` |
| arXiv v5 source archive | `556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f` |
| arXiv v5 PDF | `93cab4aa8cec06434b704e639bab87dd15ea95ac46a335961138a94fc1bae2b8` |

The official code snapshot in `upstream/` is pinned to
`e13d4b59f6d23051c73e07cfc447336da84e7bd2` and is kept unmodified. The
reproduction code is under `repro/`.

## Version discrepancy behind the backend claim

The evaluator wording says that regression beats MILP on nonlinear-invariant
benchmarks in Table 2. That is not a literal single-table statement in the
paper:

- v1 Table 1/Figure 3 compares LR and MILP on the 40-function RSR-Bench.
- v1 Table 2 compares Bitween, DIG, and SymInfer on nonlinear invariants; it
  has no MILP column.
- v5 removes that nonlinear-invariant table and reports LR/MILP on the expanded
  80-function RSR-Bench.

The audit therefore has three explicit routes: complete v1 row reconstruction,
current v5 source anchoring, and a fresh paired full-80 Gurobi comparison. It
does not manufacture a missing LR/MILP nonlinear-invariant result.

The full v1 table sums to LR/MILP sample use `607/1180` and runtime
`227.10/308.64 s`, while the v1 prose gives `594/1095` and `130.53/187.47 s`.
Both are preserved in the evidence and the disagreement is part of the
published qualification.
