# Failure boundaries and historical rejected baseline

Current verifiers are the code linked from the Current Claim pages. Historical
pages are preserved for provenance but do not supersede current verification.

## Historical rejected baseline

Two backend-targeted attempts stopped before either MILP solver ran. Their
cumulative LR prefixes produced 86 and 83 identities, below the precommitted
87-identity gate. This was not scientific evidence about either solver.
Inspection showed NumPy was seeded while Python `random` was not. The wrapper
was fixed to seed both; the gate was not relaxed.

The successful Gurobi and PuLP runs each produced 88 LR identities. They
covered 40 and 41 functions, respectively, so a small residual numerical or
scheduling nondeterminism remains and is disclosed.

Download the [failure record](../../evidence/claim5/failure_boundary.md) and
[run provenance](../../evidence/claim5/backend_run_provenance.json).

## Controls that must fail

| Route | Mutated or incomplete input | Required and observed result |
|---|---|---|
| Claim 1 | Omit `f(r)` from BLR recovery | REJECT, 432 failing assignments |
| Claim 1 boundary | Use printed `F_2` witness at `epsilon=1/2` | REJECT as lower-bound witness |
| Claim 2 | Incomplete 80-function domain | REJECT |
| Claim 3 | False exponential, sigmoid, and square identities | REJECT 3/3 |
| Claim 5 source | Truncate v1 table to 39 rows | REJECT |
| Claim 5 Gurobi | Swap LR/MILP labels | REJECT |
| Claim 5 PuLP | Swap LR/MILP labels | REJECT |

An unavailable, skipped, toy, or pre-solver result is never converted to
`VERIFIED`.
