# Claim 1 source audit

Source retrieved with an explicit `OpenResearch-Reproduction/1.0` User-Agent on
2026-07-26 from `https://arxiv.org/e-print/2412.18134`. The v5 source archive
has SHA-256
`556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f`;
the corresponding PDF has SHA-256
`93cab4aa8cec06434b704e639bab87dd15ea95ac46a335961138a94fc1bae2b8`.

## Exact anchors and assumptions

- Definition 4.1 requires each query `q_i(x,r)` to be uniformly distributed
  over `X` for fixed `x`; the queries may be correlated. Perfect recovery is
  pointwise. Approximate recovery has inner error `rho` over `r` and outer
  error `xi` over `x`.
- Definition 4.3 distinguishes independent uniform samples, correlated samples
  with uniform marginals, and adaptive oracle queries.
- Definition 4.5 defines `(Q,P)`-RSR learning, realizability, confidence
  `1-delta`, and sample complexity `m(rho,xi,delta)`.
- Appendix Claim A.1 states
  `m_RSR(rho,xi,delta) <= m_PAC(min(rho/k,xi),delta)` and explicitly permits an
  inefficient exhaustive learner.
- Appendix Claim A.2 states an existential zero-sample-RSR versus Uniform-PAC
  separation for every `epsilon <= 1/2`. Its proof assumes `delta < 1/2` and
  reasons about a proper hypothesis in `F`, consistent with the paper's use of
  `hat f in F`.

## Boundary defect and faithful resolution

The A.2 proof chooses linear functions over `F_2^n` but then fixes
`epsilon < 1/2`. That strict inequality is necessary for its witness: at
`epsilon = 1/2`, the zero linear hypothesis has error exactly `1/2` against
every nonzero target, so zero samples suffice. This is a defect in the supplied
proof witness, not by itself a falsification of the existential statement.

An independent `F_3` witness verifies the exact statement. Distinct linear
functionals over `F_3^n` agree on exactly one third of inputs, so error at most
one half requires exact identification. Fewer than `n` oracle queries leave a
nonzero nullspace and at least three consistent targets; worst-case
identification success is at most one third, below the required success for
`delta < 1/2`. The same two-query BLR relation gives a perfect, zero-sample RSR.

## Paper-source limitation

Definition 4.1 contains a tuple typo `(q_1,...,q_k,r)` where the recovery member
must be `p`; subsequent equations and the approximate definition use `p`.
This audit follows the typed signatures and equations, not the typo.
