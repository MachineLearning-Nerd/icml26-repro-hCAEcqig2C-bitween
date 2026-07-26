# Evaluator entry for Claim 5

Current status: **BLOCKED** until a fresh full-80 MILP run and independent
paired comparison finish.

Fixed campaign command:

```text
uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py
```

Source/table verifier:

```text
.venv/bin/python repro/src/verify_backend_source.py --out .openresearch/artifacts/claim5_backend/source_audit_output.json
```

Fresh paired verifier after the configured MILP run:

```text
.venv/bin/python repro/src/compare_backends.py --lr-dir .openresearch/artifacts/baseline/vanilla_seed42 --milp-dir .openresearch/artifacts/claim5_backend/milp_<solver>_seed42 --solver <solver> --out .openresearch/artifacts/claim5_backend/comparison_<solver>.json
```

The evaluator-visible Space page must put the source-version mismatch first,
then expose all 40 legacy rows, all fresh aggregate and paired results, raw
JSON and per-function data, controls, exact command, Git SHA, seed, CPU
allocation, runtime, cost, and limitations inline.
