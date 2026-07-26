# Evaluator entry for Claim 5

Version-resolved verdict: **VERIFIED** with **MEDIUM confidence** because the
judge sentence conflates two source experiments. The paper-relevant Gurobi
route, the PuLP robustness route, the complete legacy table audit, and every
negative control have passed.

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

Observed paper-relevant full-80 Gurobi comparison:

- LR versus MILP coverage: `40/80` versus `37/80`;
- verified identities: `88` versus `69`;
- mean runtime: `12.008375 s` versus `17.790875 s`;
- faulty identities: `0` versus `0`;
- label-swap control: `REJECT`.

The PuLP solver-substitution route independently passes the same current
directional contract (`41/80` versus `39/80`, `88` versus `66`, `11.938875 s`
versus `17.180875 s`).

The evaluator-visible Space page must put the source-version mismatch first,
then expose all 40 legacy rows, all fresh aggregate and paired results, raw
JSON, controls, exact command, Git SHA, seed, CPU allocation, runtime, cost,
and limitations inline. It must not present the current derived `Sample
Complexity` field as v1's `used/budget` sample metric.
