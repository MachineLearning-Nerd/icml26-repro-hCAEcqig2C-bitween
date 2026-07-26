# Claim 1 limitations and deviations

- Finite enumeration is not presented as proof of a universally quantified
  theorem. The general argument is the independently reconstructed
  rank-nullity and two-case union-bound certificate; enumeration checks its
  complete small-domain instances and implementation.
- The paper's supplied `F_2` witness does not cover its written
  `epsilon=1/2` boundary. The verifier preserves this failure as a required
  negative control and uses `F_3` only because Claim A.2 is existential over
  the classes.
- The audit verifies the Section 4 formalization and its two stated
  sample-complexity results. It does not claim a “fundamental theorem” for RSR
  learning; the paper explicitly calls that an open question.
