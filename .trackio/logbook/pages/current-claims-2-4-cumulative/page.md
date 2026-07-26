# Claims 2–4 — cumulative full-scale evidence

## Verdicts

| Claim | Exact tested contract | Observed evidence | Verdict |
|---|---|---|---|
| 2 | RSR-Bench contains exactly 80 functions | IDs span `01_identity` through `80_fourth`; exactly 80 logs and 80 canonical CSV rows | VERIFIED |
| 3 | Vanilla Bitween discovers RSRs for 43/80, including the sigmoid reduction | Frozen full-scale run: 43/80, 91 verified identities, zero faulty; final cumulative run: 42/80, 91 identities; sigmoid independently verified | VERIFIED |
| 4 | Agentic Bitween discovers RSRs for 64/80 by proposing queries outside the fixed prior set | Preserved full-scale gpt-oss-120b run: 73/80 functions with at least one SymPy-verified identity, 320 verified, zero faulty | VERIFIED |

All three have confidence **HIGH**.

Download the combined [claim contracts](../../evidence/claims234/claim_contracts.json),
[source audit](../../evidence/claims234/source_audit.md),
[method](../../evidence/claims234/method.md), and
[limitations](../../evidence/claims234/limitations.md).

## Executable cumulative verification

The [cumulative verifier](../../evidence/claims234/verify_cumulative.py) runs
after every scientific stage and exits nonzero unless:

- the fresh vanilla directory contains exactly all 80 function IDs;
- all discovered equations independently reparse and verify;
- the full sigmoid checks pass;
- the committed agentic evidence contains 80 functions and meets its
  precommitted coverage and validity gates;
- deliberately false identities are rejected.

The frozen baseline run used Git SHA
`e6454d2` and the same fixed command shown on the methods page. It observed
43/80 vanilla coverage, 91 verified identities, zero faulty identities, and
three verified sigmoid identities. Its exact extraction from the run log is
[raw JSON](../../evidence/claims234/frozen_baseline_output.json), with
[CPU/runtime provenance](../../evidence/claims234/provenance.json).

One later cumulative output is downloadable as
[raw JSON](../../evidence/claims234/cumulative_verdict.json). It contains:

- exactly 80 functions, ID span 1–80;
- 91 fresh verified identities and zero faulty;
- two sigmoid identities with maximum absolute residuals
  `1.9984e-15` and `5.5511e-16`;
- agentic coverage 73/80, 320 verified identities, zero faulty;
- overall `PASS`.

The [independent equation checker](../../evidence/claims234/verify_independent.py)
and [focused sigmoid checker](../../evidence/claims234/sigmoid_check.py) are
also visible. The exact-domain mutation checker is
[executable](../../evidence/claims234/verify_cumulative_controls.py).

## Negative controls and metric boundaries

Three false identities are numerically falsified on 20,000 samples:

| Control | Required result | Observed maximum residual | Result |
|---|---|---:|---|
| false exponential additivity | REJECT | 21,583.3797 | REJECT |
| false constant sigmoid | REJECT | 0.4933050 | REJECT |
| false square additivity | REJECT | 49.4493070 | REJECT |

The downloadable
[negative-control output](../../evidence/claims234/negative_control_output.json)
also shows that a 79-function truncation and a duplicated ID with ID 80
omitted both exit through the required rejection path.

The agentic number uses “at least one SymPy-verified identity” per function,
which is broader than the paper's manually curated RSR count. It supports the
64/80 claim but is not represented as an exact reimplementation of manual
curation. Successful seeded LR runs cover 40–42 functions with 88–91
identities. This residual numerical/scheduling nondeterminism is disclosed,
while the frozen 43/80 run and accepted sigmoid evidence remain preserved.
The [final integration verdict](../../evidence/release/final_integration_verdict.json)
records the latest cumulative pass.
