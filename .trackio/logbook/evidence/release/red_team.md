# Evaluator-blind pre-publication red team

The review used only a fresh copy of the exact judged Space revision overlaid
with the candidate text files and the evaluator rubric. It began at
`logbook.json` and the declared canonical file
`pages/current-scorecard/page.md`; repository knowledge and OpenResearch logs
were not used to fill gaps.

## Pass 1

Files opened from the canonical traversal:

```text
pages/current-scorecard/page.md
pages/current-claim-1-section-4/page.md
pages/current-claims-2-4-cumulative/page.md
pages/current-claim-5-backends/page.md
pages/current-methods/page.md
pages/visibility-matrix/page.md
pages/failure-boundaries/page.md
evidence/claim1/claim_contract.json
evidence/claim1/source_audit.md
evidence/claim1/method.md
evidence/claim1/limitations.md
evidence/claim1/theory_verifier_output.json
evidence/claim1/independent_checker_output.json
evidence/claim1/verify_theory.py
evidence/claim1/verify_theory_independent.py
evidence/claims234/cumulative_verdict.json
evidence/claims234/verify_cumulative.py
evidence/claims234/verify_independent.py
evidence/claims234/sigmoid_check.py
evidence/claim5/claim_contract.json
evidence/claim5/source_audit.md
evidence/claim5/source_audit_output.json
evidence/claim5/method.md
evidence/claim5/limitations.md
evidence/claim5/comparison_gurobi.json
evidence/claim5/comparison_pulp.json
evidence/claim5/claim5_v1_table40.csv
evidence/claim5/verify_backend_source.py
evidence/claim5/compare_backends.py
evidence/claim5/backend_run_provenance.json
evidence/claim5/failure_boundary.md
evidence/environment/run_campaign.py
evidence/environment/campaign.json
evidence/environment/pyproject.toml
evidence/environment/uv.lock
```

The navigation and all links resolved. Claim 1 and Claim 5 were directly
reviewable. The reviewer could not directly locate three required Claims 2–4
items: a source/contract bundle, the frozen 43/80 raw result, and output from
an incomplete-domain control. The fresh Claim 5 JSON exposed aggregates but
not every paired function row.

Fixes:

- added Claims 2–4 contracts, source audit, method, limitations, frozen raw
  result, provenance, and explicit mutation-control output;
- added a mutation verifier that rejects a 79-function domain and a
  duplicate-79/omitted-80 domain;
- reconstructed and exposed all 80 paired rows for both Gurobi and PuLP from
  immutable orx logs, with a separate extractor that cross-checks the
  published aggregates.

## Pass 2

Pass 2 repeats the traversal after these fixes. Its exact file-open list,
missing-link result, protected-subset result, secret scan, and text upload
allowlist are stored in the release audit JSON alongside the repository
candidate. No missing visibility cell remains after the second pass.

## Pass 3 after the final cumulative run

The final HF `cpu-upgrade` run completed at winning scientific SHA
`519ae8d1bc86054e48797dc2f02076844a4cea7f`. The publication-only candidate
was updated to its exact Gurobi aggregates, all 80 reconstructed paired rows,
runtime, CPU/cost record, and cumulative verdict. The blind traversal was then
repeated from a newly downloaded candidate directory. Publication is allowed
only if this final audit again reports no missing link or secret, historical
pages byte-identical, the judged file set a subset, and every current page
reachable from the canonical scorecard.
