# Status — Learning Randomized Reductions

Publication gate: `PASS` when
`python3 repro/src/publication_gate.py --skip-producers` succeeds.

## Current evidence

| Area | Status | Evidence |
|---|---|---|
| Section 4 theory | `VERIFIED` | Primary and independent verifiers pass; binary boundary witness rejected; ternary witness verified. |
| RSR-Bench domain | `VERIFIED` | Exact IDs `01..80`; negative domain mutations rejected. |
| Vanilla Bitween | `VERIFIED_SCOPED` | Frozen baseline 43/80, 91 verified identities, 0 faulty, 3 sigmoid identities; later run variation is retained. |
| Agentic Bitween | `VERIFIED_SCOPED` | 73/80 functions, 320 verified identities, 0 faulty under the at-least-one-verified metric. |
| LR versus MILP | `VERIFIED_VERSION_RESOLVED` | Gurobi full-80 comparison passes; v1/v5 source discrepancy is documented; PuLP is labeled a substitution. |
| Agentic versus Neural headline | `NOT_REPRODUCED` | Three matched GPT-OSS pairs have neural discovery ahead; agentic verification accuracy is higher. |

## Publication state

- No live judge score or forecast is claimed.
- `.openresearch/artifacts/` is the canonical evidence store.
- `hf_space/` is retained as an archival evaluator snapshot only.
- The duplicated private `.trackio/` publisher state has been removed.
- Source artifacts and hashes are recorded in `sources.json`.
- Branch roles and old-to-new names are recorded in `docs/BRANCH_AUDIT.md`.
