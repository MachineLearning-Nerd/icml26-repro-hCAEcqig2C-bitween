# Evaluator entry for Claim 1

Verdict target: **VERIFIED**, subject to both executable verifiers passing on
the committed revision.

Run through the fixed campaign command:

```text
uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py
```

Direct verifier commands, executed by that campaign:

```text
.venv/bin/python repro/src/verify_theory.py --out .openresearch/artifacts/claim1_theory/theory_verifier_output.json
.venv/bin/python repro/src/verify_theory_independent.py --out .openresearch/artifacts/claim1_theory/independent_checker_output.json
```

Required output markers:

- `THEORY_EXHAUSTIVE_VERDICT=VERIFIED`
- `THEORY_INDEPENDENT_VERDICT=VERIFIED`
- `THEORY_CLAIM_VERDICT=VERIFIED`

The evaluator-visible Space page must expose the source hashes, exact
quantifiers, binary boundary rejection, ternary witness, checker output,
negative control, command, Git SHA, seed policy, CPU allocation, runtime, raw
JSON links, and limitations inline.
