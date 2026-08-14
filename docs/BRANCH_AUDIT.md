# Branch audit

The old branches were experiment lineage, not clean user-facing names. Each
was preserved under a descriptive name before the old remote ref was removed.
The old tip SHA is included as provenance; GitHub readback of the final tip is
the authority after publication.

| Old branch | Final branch | Role | Historical tip |
|---|---|---|---|
| `orx/frozen-6-of-10-baseline` | `baseline/frozen-6-of-10` | Frozen 80-function baseline; 43/80, 91 identities, sigmoid and controls | `e6454d25645fa64af3080f7a61f270b431b2ee3c` |
| `orx/exact-section-4-contract-and-boundary-audit` | `audit/section-4-theory` | Exact Section 4 proof reconstruction and boundary audit | `c7fd7c901d0d362ffe48876f380fd9567d00dcbc` |
| `orx/backend-claim-source-contract-and-harness` | `audit/versioned-backend-source` | v1/v5 source, table, and contract audit | `1f9f8abb6426eaf6763acdfdd0c072905cdddc5c` |
| `orx/fresh-full-80-gurobi-milp-comparison` | `experiment/full-80-gurobi` | Paper-relevant paired Gurobi run | `39b5adf982972492fd195f85dfc1cc426a35504d` |
| `orx/fresh-full-80-pulp-milp-robustness` | `experiment/full-80-pulp` | Open-source solver substitution and robustness check | `ffa7b986f054c5f04cb8d9b894dd5f8e0dfe3849` |
| `orx/integrated-five-claim-release-candidate` | `release/integrated-five-claim` | Final cumulative integration and evidence release candidate | `519ae8d1bc86054e48797dc2f02076844a4cea7f` |

`main` is the publication surface. It contains the authoritative README,
status, source/claim/branch audit, deterministic publication gate, and
hash-bound artifacts. Historical experiment branches retain their original
scientific snapshots; they are not merged into `main` merely to make the
history look linear.
