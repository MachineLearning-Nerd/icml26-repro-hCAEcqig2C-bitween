# Current methods, environment, and provenance

## One immutable command

Every OpenResearch node inherited this command verbatim:

```text
uv sync --frozen && uv pip install --python .venv/bin/python --no-deps -e ./upstream && .venv/bin/python repro/src/run_campaign.py
```

Variants are committed in `repro/configs/campaign.json`; no environment
variable changes scientific behavior. The repository contains one `.venv`,
Python 3.12, a committed `pyproject.toml`, and an exact `uv.lock`. The upstream
package is pinned at Git SHA
`e13d4b59` and installed without modifying upstream source.

Download the [campaign entrypoint](../../evidence/environment/run_campaign.py),
[committed campaign config](../../evidence/environment/campaign.json),
[pyproject.toml](../../evidence/environment/pyproject.toml), and
[uv.lock](../../evidence/environment/uv.lock).

## Compute and seeds

All formal scientific jobs used Hugging Face `cpu-upgrade`: 8 allocated vCPUs,
32 GB RAM, no GPU, listed price `$0.03/hour`.

| Stage | Estimated cores | Estimated time | Actual duration | Approx. cost |
|---|---:|---:|---:|---:|
| Frozen cumulative baseline | 8 | 30 min | 18m27s | $0.0092 |
| Exact Section 4 theory | 8 | 30 min | 21m08s | $0.0106 |
| Versioned source audit | 8 | 23 min | 22m28s | $0.0112 |
| Gurobi full-80 comparison | 8 | 50 min | 41m34s | $0.0208 |
| PuLP full-80 comparison | 8 | 60 min | 40m30s | $0.0203 |
| Final cumulative integration | 8 | 50 min | 34m54s | $0.0175 |

Seed 42 is applied to both Python `random` and NumPy. Two pre-solver attempts
exposed the earlier missing Python seed and remain labeled Historical rejected
baseline. The initial Gurobi run is Git SHA `39b5adf`; the successful PuLP
run is Git SHA `ffa7b98`; the final cumulative winner is Git SHA
`519ae8d1bc86054e48797dc2f02076844a4cea7f`. Full provenance, including
rejected attempts, is
[downloadable JSON](../../evidence/claim5/backend_run_provenance.json).

The report does not use `os.cpu_count()` as the allocation record because the
container can expose host topology. The selected HF flavor's allocation is the
recorded 8 vCPUs.

## Independent checks and exit behavior

Primary discovery output is independently parsed. The theory route uses a
separate exact-rational/rank checker. The sigmoid route combines SymPy with
20,000-sample numerical falsification. Backend routes independently reconstruct
all 80 paired rows. Every verifier raises on an unmet contract and exits
nonzero.

Raw evidence and checker links appear on each claim page, not only here.
