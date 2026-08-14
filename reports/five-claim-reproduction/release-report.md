# Release report: Learning Randomized Reductions

> Archival release/provenance report. The root README, STATUS, claim map, and
> local publication gate are authoritative for the current repository state.

- Previous live judged score: `6/10`
- Conservative projected score range after the proposed change: `8–10/10`
- Best-supported possible new score: `10/10` — forecast only, not a judge result

## Claim forecast

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 — Section 4 theory | 0/2 | 2/2 | HIGH | VERIFIED | Exact A.1 derivation; exact existential A.2 witness; independent rational/rank checker; broken recovery and defective binary boundary witness rejected. |
| 2 — 80-function benchmark | 2/2 | 2/2 | HIGH | VERIFIED | Exact IDs 01–80 in every cumulative run; incomplete and duplicate-ID domains rejected. |
| 3 — vanilla and sigmoid | 2/2 | 2/2 | HIGH | VERIFIED | Frozen 43/80; final 42/80 with 91 verified, zero faulty; three sigmoid identities pass 20,000-sample falsification; three false identities rejected. |
| 4 — agentic coverage | 2/2 | 2/2 | HIGH | VERIFIED | Preserved full-scale gpt-oss-120b evidence gives 73/80, 320 verified, zero faulty; broader coverage metric disclosed. |
| 5 — regression versus MILP | 0/2 | 2/2 | MEDIUM | VERIFIED | Final paired Gurobi full-80 gives LR/MILP 42/38 coverage, 91/70 identities, 10.444/14.450 s mean runtime, zero faulty; PuLP robustness and complete v1 table agree in aggregate direction. Source-version conflation remains review risk. |

Current total score: `6/10`. Conservative projected total: `8–10/10`.
Best-supported possible total: `10/10`, explicitly a forecast. Claims 1 and 5
changed from absent/inconclusive to direct evaluator-visible evidence. No claim
is `BLOCKED`.

The exact publication action is one text-only Hub API commit to the existing
Space `DineshAI/hCAEcqig2C`, followed by a fresh download, hash verification,
canonical traversal, and a fast-forward publication commit to GitHub `main`.
No second Space will be created.

## Baseline and winning state

- Previous HF Head:
  `ae46d4e51ffd7d29e2d5d71ae39df4e2e9fce037`
- Previous Judge Head:
  `ae46d4e51ffd7d29e2d5d71ae39df4e2e9fce037`
- Previous judged score: `6/10`
- Frozen baseline run: `c8d858bf-03ac-47a8-96c2-128df8251af5`
- Winning experiment:
  `release/integrated-five-claim`
- Winning scientific Git SHA:
  `519ae8d1bc86054e48797dc2f02076844a4cea7f`
- Final run: `1641598f-0324-42b5-8d1f-6c7399526fa8`
- Final status: `done`

The final run used HF `cpu-upgrade`, 8 allocated vCPUs, 32 GB RAM, no GPU.
The estimate was 8 cores and 50 minutes. Provider duration was 34m54s;
entrypoint runtime was 2066.746638 s; estimated cost was `$0.01745`.

## Experiment tree

```text
Frozen 6-of-10 baseline
└── Exact Section 4 contract and boundary audit
    └── Backend claim source contract and harness
        ├── Fresh full-80 Gurobi MILP comparison
        │   └── Integrated five-claim release candidate  ← winner
        └── Fresh full-80 PuLP MILP robustness
```

The root is frozen. Each scientific child inherited one fixed command. The
final presentation commit is not an experiment and does not alter the winning
scientific SHA.

## Final numerical result

The final cumulative run reports:

| Evidence | Result |
|---|---|
| Claim 1 primary / independent | VERIFIED / VERIFIED |
| Binary proof witness at `epsilon=1/2` | REJECTED_AS_WITNESS |
| Ternary exact existential witness | VERIFIED |
| Broken recovery mutation | REJECT |
| Claim 2 domain | exactly 80, IDs 01–80 |
| Claim 3 | 42/80, 91 verified, 0 faulty, 3 sigmoid identities |
| Claim 4 | 73/80, 320 verified, 0 faulty |
| Claim 5 LR / Gurobi coverage | 42 / 38 |
| Claim 5 LR / Gurobi identities | 91 / 70 |
| Claim 5 LR / Gurobi mean runtime | 10.44425 / 14.450125 s |
| Claim 5 faulty | 0 / 0 |
| Claim 5 label swap | REJECT |
| Overall | PASS |

## Command ledger

The immutable experiment command on every node was:

```text
uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py
```

The formal launch shape was:

```text
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 2h
```

It was used for the baseline, theory, source audit, Gurobi, PuLP, and final
integration nodes. Monitoring used:

```text
orx exp wait <experiment-id> --interval 15 --timeout 480
orx runs 66ee179d-0f08-44ec-a39e-b46683ec8ef2
orx logs <run-id> --bytes <bounded-byte-count>
```

Release checks used:

```text
uv run marimo check notebooks/learning_randomized_reductions.py
.venv/bin/python repro/src/verify_cumulative_controls.py
.venv/bin/python repro/src/extract_backend_log_rows.py --log <immutable-orx-log> --solver <gurobi|pulp> --aggregate <aggregate-json> --out <row-json>
.venv/bin/python repro/src/audit_space_candidate.py --candidate <fresh-candidate> --protected <judged-revision> --overlay hf_space --output <audit-json>
```

Paper retrieval used an explicit browser User-Agent from
`https://arxiv.org/e-print/2412.18134`; the source and PDF hashes are on the
Claim 1 and Claim 5 source pages.

## Evidence paths

- Scientific report: `reports/five-claim-reproduction/report.md`
- Tutorial notebook: `notebooks/learning_randomized_reductions.py`
- Final verdict:
  `.openresearch/artifacts/release/final_integration_verdict.json`
- Final candidate audit:
  `.openresearch/artifacts/release/candidate_audit_release.json`
- Claim 1:
  `.openresearch/artifacts/claim1_theory/`
- Claims 2–4:
  `.openresearch/artifacts/claims234/`
- Claim 5:
  `.openresearch/artifacts/claim5_backend/`
- Evaluator-visible overlay: `hf_space/`

The visual report and its four figures are mirrored into the OpenResearch
Files directory under `integrated-five-claim-release-candidate/`.

## Runtime and cost

Formal successful HF jobs:

| Stage | Runtime | Approx. cost |
|---|---:|---:|
| Baseline | 18m27s | $0.0092 |
| Theory | 21m08s | $0.0106 |
| Source audit | 22m28s | $0.0112 |
| Initial Gurobi | 41m34s | $0.0208 |
| PuLP | 40m30s | $0.0203 |
| Final integration | 34m54s | $0.0175 |

Including the three preserved environmental/pre-solver failed attempts, the
campaign cost is approximately `$0.101`. Local work was limited to
single-core, sub-five-minute source, JSON, notebook, figure, and audit checks.

## Protection and evaluator visibility

The final blind audit starts only at
`pages/current-scorecard/page.md`, opens 48 linked files, finds zero missing
links and zero secret patterns, and validates `logbook.json`. All 19 files from
the exact judged revision remain in the candidate file set. Every historical
page is byte-identical; only `README.md` and `logbook.json` are overlaid to put
current verification first. The old file set is therefore a subset of the new
68-file candidate.

The exact SHA-256 manifest and byte count for every upload path are in
`.openresearch/artifacts/release/candidate_audit_release.json`.

## Exact Hugging Face upload allowlist

```text
README.md
evidence/claim1/claim_contract.json
evidence/claim1/independent_checker_output.json
evidence/claim1/limitations.md
evidence/claim1/method.md
evidence/claim1/source_audit.md
evidence/claim1/theory_verifier_output.json
evidence/claim1/verify_theory.py
evidence/claim1/verify_theory_independent.py
evidence/claim5/backend_run_provenance.json
evidence/claim5/claim5_v1_table40.csv
evidence/claim5/claim_contract.json
evidence/claim5/compare_backends.py
evidence/claim5/comparison_gurobi.json
evidence/claim5/comparison_pulp.json
evidence/claim5/extract_backend_log_rows.py
evidence/claim5/failure_boundary.md
evidence/claim5/limitations.md
evidence/claim5/method.md
evidence/claim5/rows_gurobi.json
evidence/claim5/rows_pulp.json
evidence/claim5/source_audit.md
evidence/claim5/source_audit_output.json
evidence/claim5/verify_backend_source.py
evidence/claims234/EVAL.md
evidence/claims234/claim_contracts.json
evidence/claims234/cumulative_verdict.json
evidence/claims234/frozen_baseline_output.json
evidence/claims234/limitations.md
evidence/claims234/method.md
evidence/claims234/negative_control_output.json
evidence/claims234/provenance.json
evidence/claims234/sigmoid_check.py
evidence/claims234/source_audit.md
evidence/claims234/verify_cumulative.py
evidence/claims234/verify_cumulative_controls.py
evidence/claims234/verify_independent.py
evidence/environment/campaign.json
evidence/environment/pyproject.toml
evidence/environment/run_campaign.py
evidence/environment/uv.lock
evidence/release/final_integration_verdict.json
evidence/release/red_team.md
logbook.json
pages/current-claim-1-section-4/page.md
pages/current-claim-5-backends/page.md
pages/current-claims-2-4-cumulative/page.md
pages/current-methods/page.md
pages/current-scorecard/page.md
pages/failure-boundaries/page.md
pages/visibility-matrix/page.md
```
