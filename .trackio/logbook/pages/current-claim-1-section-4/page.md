# Claim 1 — Section 4 formalization and sample complexity

## Verdict

**VERIFIED** · confidence **HIGH**

## Exact claim contract

Source: arXiv `2412.18134v5`, retrieved 2026-07-26 from
`https://arxiv.org/e-print/2412.18134`, source SHA-256
`556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f`.
The rendered PDF SHA-256 is
`93cab4aa8cec06434b704e639bab87dd15ea95ac46a335961138a94fc1bae2b8`.

Anchors: Definition 4.1 (RSR and uniform query marginals), Definition 4.3
(sample access), Definition 4.5 (learning an RSR), Claim A.1 (PAC implies RSR),
and Claim A.2 (zero-sample RSR versus proper-PAC query separation).

The contract has two quantified clauses:

1. If `F ⊆ RSR_k(Q,P)`, then
   `m_RSR(rho,xi,delta) <= m_PAC(min(rho/k,xi),delta)`, with no computational
   efficiency guarantee. Query tuples may be correlated; each query marginal
   must be uniform.
2. There exist `Q,P,F` that are efficiently RSR-learnable with zero samples,
   while every proper uniform-PAC learner for `F_n` needs at least `n` oracle
   queries for every `epsilon <= 1/2` and `delta < 1/2`.

Download the [machine-readable contract](../../evidence/claim1/claim_contract.json)
and [source audit](../../evidence/claim1/source_audit.md).

## Proof certificate and observed checks

Claim A.1 follows by a complete case split. A PAC hypothesis with error at
most `min(rho/k,xi)` is an admissible learned function. For a fresh RSR query
tuple, every marginal is uniform, so each query has error probability at most
`rho/k`. A union bound—not independence—makes the probability of any bad query
at most `rho`; when none is bad, exact recovery transfers through `p`.

The paper's A.2 witness over `F_2^n` is invalid at the written boundary:
distinct linear functions disagree on exactly `1/2` of the domain. At
`epsilon=1/2`, the zero hypothesis is already admissible. The current verifier
must reject that witness.

The exact existential claim is repaired without weakening it by using linear
functionals over `F_3^n`. Distinct functions disagree on `2/3` of the domain,
so half-error proper PAC learning requires exact identification. Fewer than
`n` query vectors have a nonzero nullspace, leaving at least three consistent
targets and best worst-case identification probability at most `1/3`, below
the required success `>1/2`. The two-query BLR identity still gives exact
zero-sample RSR recovery.

Raw verifier output:

- binary recovery assignments through `n=7`: `2,097,152` at the largest domain;
- ternary recovery assignments through `n=4`: `531,441` at the largest domain;
- independent exact-rational A.1 case checks: `2,888`;
- every enumerated `F_3` transcript with `m<n` has nullity at least one;
- broken recovery `f(x+r)` with `f(r)` omitted is rejected on `432`
  assignments;
- verdict: `VERIFIED`.

Download [primary output](../../evidence/claim1/theory_verifier_output.json),
[independent checker output](../../evidence/claim1/independent_checker_output.json),
[primary verifier source](../../evidence/claim1/verify_theory.py), and
[independent checker source](../../evidence/claim1/verify_theory_independent.py).
Both programs exit nonzero on a failed assertion.

## Non-circularity, assumptions, and limitations

No sample count or horizon was selected from the theorem formula as empirical
evidence. Finite enumerations calibrate the implementation only; the universal
certificate is the symbolic marginal-only union bound and the general
rank-nullity argument. The ternary construction is an independent witness for
the paper's existential quantifier, not a claim that the paper printed that
witness.

See the [method](../../evidence/claim1/method.md) and
[limitations](../../evidence/claim1/limitations.md).
