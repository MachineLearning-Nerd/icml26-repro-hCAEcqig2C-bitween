# Claim-to-evidence map

This page is the authoritative map for the reproduction package. A `VERIFIED`
result means that the saved contract and its executable checks pass. It does
not mean that every number or wording in every paper version was reproduced
exactly.

## Five scoped reproduction contracts

| Contract | Paper anchor | How the result is produced | Evidence | Result and qualification |
|---|---|---|---|---|
| 1 — theory | Definitions 4.1–4.5 and Appendix Claims A.1–A.2 | `verify_theory.py` reconstructs the PAC-to-RSR case split, finite-field witnesses, and BLR recovery; `verify_theory_independent.py` checks rank/nullity and the rational case grid independently. | `.openresearch/artifacts/claim1_theory/` | `VERIFIED`. The supplied binary witness is rejected at `epsilon=1/2`; an independent ternary witness proves the existential statement. |
| 2 — benchmark domain | Section 5 and the complete RSR-Bench table | `run_vanilla.py`, `aggregate.py`, and cumulative domain controls require exactly IDs `01..80`; truncated and duplicate/omitted domains are rejected. | `.openresearch/artifacts/claims234/claim_contracts.json`, `frozen_baseline_output.json`, `negative_control_output.json` | `VERIFIED`: 80 functions, IDs 1–80. |
| 3 — Vanilla Bitween | Table 1 and the sigmoid discussion | The frozen baseline runs the unmodified 80-function harness; `verify_independent.py` reparses identities, checks sigmoid identities on 20,000 samples, and rejects false identities. | `.openresearch/artifacts/claims234/frozen_baseline_output.json`, `outputs/c3_primary_paired_audit.json` | `VERIFIED_SCOPED`: frozen baseline 43/80, 91 verified identities, 0 faulty, 3 sigmoid identities. Later seeded integrations cover 39–42 functions, so run variation is disclosed. |
| 4 — Agentic Bitween | Table 1 and the agentic query-generation method | `aggregate.py` and the cumulative verifier reparse the committed 80-function agentic logs and require zero faulty identities. | `.openresearch/artifacts/claims234/frozen_baseline_output.json`, `.openresearch/artifacts/claims234/` | `VERIFIED_SCOPED`: 73/80 functions with at least one SymPy-verified identity, 320 identities, 0 faulty. This is a broader metric than the paper's manually curated 64/80 RSR count. |
| 5 — LR versus MILP | v1 Table 1/Figure 3 and v5 aggregate results | `verify_backend_source.py` audits both source versions and all legacy rows; `run_vanilla.py --method eager_milp` plus `compare_backends.py` performs paired full-80 Gurobi checks. PuLP is a labeled robustness substitution. | `.openresearch/artifacts/claim5_backend/` | `VERIFIED_VERSION_RESOLVED`: final Gurobi LR/MILP coverage 42/38, identities 91/70, mean time 10.44425/14.450125 s, 0 faulty, label swap rejected. The judge wording conflates v1 tables. |

## Separate headline comparison audit

The paper also claims that Agentic Bitween outperforms pure neural baselines
in discovery and verification. This is not one of the five scoped contracts
above because the committed evidence resolves it separately and does not
support the conjunctive headline:

- `outputs/c3_primary_paired_audit.json` compares three matched, full 80-function
  GPT-OSS runs.
- Neural discovery is ahead in all three pairs: `(74,73)`, `(77,72)`, and
  `(72,71)` for neural versus agentic coverage.
- Agentic verification accuracy is higher in the pooled audit (`0.897959` vs
  `0.791852`).
- Verdict: `not_reproduced_in_this_full_scale_open_model_reproduction`.

This is a documented counterexample to the discovery portion, not a claim that
the underlying paper is invalid. The paper's v5 aggregate row itself reports
59% Agentic versus 62% Neural GPT-OSS coverage; the positive headline comes
from a different model row.

## Controls that prevent claim inflation

- The incomplete `01..79` domain and duplicate/omitted domain are rejected.
- Three deliberately false identities are rejected by 20,000-sample numerical
  falsification.
- The Claim 1 binary witness is retained as a rejected boundary control.
- The Claim 1 recovery mutation omitting `f(r)` is rejected.
- The Claim 5 LR/MILP label swap is rejected.
- The v1 40-row table is audited completely; prose totals and row sums are
  both reported rather than silently substituted.
