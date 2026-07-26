# Claim 5 limitations and deviations

- The judge sentence conflates two experiments in v1 and does not match v5.
  The reproduction preserves this source mismatch rather than manufacturing
  an LR/MILP result on the nonlinear-invariant table.
- The v1 table transcription is used only for a complete published-evidence
  recalculation. It cannot establish fresh runtime on current hardware.
- Current v5 logs expose a derived `Sample Complexity` field, not v1's
  `used/budget` columns. The fresh 80-function contract therefore tests the
  current paper's verified-identity count, function coverage, correctness, and
  runtime directions. Legacy sample-use evidence remains versioned separately.
- Gurobi is the paper-relevant MILP solver. An open-source PuLP run, if
  executed, is a solver-robustness check and must be labeled as a deviation.
- Aggregate runtime is hardware- and implementation-sensitive. The paired run
  uses one container flavor, commit, seed, timeout, and harness to minimize
  this confound; it does not claim portability to every CPU.
