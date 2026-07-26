# Claim 1 method

`repro/src/verify_theory.py` exhaustively enumerates all inputs, randomness,
and linear targets over `F_2^n` for `n=1..7` and `F_3^n` for `n=1..4`. It
checks both uniform query marginals and every BLR recovery equation. It also
checks the complete target class's distance from the zero hypothesis at the
`epsilon=1/2` boundary.

`repro/src/verify_theory_independent.py` follows a different route. It
exhaustively enumerates every ordered oracle-query transcript for `F_3^n`,
`n<=3`, `m<n`, row-reduces the transcript matrix modulo three, and checks that
the nullity is positive. It separately checks the two exact algebraic cases
for `epsilon=min(rho/k,xi)` on 2,888 rational parameter triples.

The negative control removes the second BLR oracle answer from recovery. The
verifier must find failing assignments and exits nonzero otherwise. Both
verifiers use assertions and exit nonzero on any failed contract.
