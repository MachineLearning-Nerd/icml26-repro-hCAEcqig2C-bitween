# Evaluator visibility matrix

This matrix was built by traversing only the candidate's canonical scorecard
and its links. “Yes” means the item is inline or directly downloadable from
the named page.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Section 4](../current-claim-1-section-4/page.md) | Yes: two verifier sources | Yes: hashes, counts, boundary | Two JSON outputs | Independent rational/rank checker | Broken recovery rejected on 432 assignments; F2 boundary witness rejected | A.1 bound, marginal correlation condition, exact existential A.2 quantifiers | VERIFIED |
| 2 | [Claims 2–4](../current-claims-2-4-cumulative/page.md) | Yes: cumulative and mutation verifiers | Yes: 80 and ID span | Frozen and cumulative JSON | Independent directory/ID parser | 79-function and duplicate-ID mutations rejected with raw output | Exactly 80 RSR-Bench functions | VERIFIED |
| 3 | [Claims 2–4](../current-claims-2-4-cumulative/page.md) | Yes: cumulative, equation, sigmoid checkers | Yes: paper/observed coverage, identity and residual counts | Frozen and cumulative JSON | SymPy plus 20,000-sample falsifier | Three false identities rejected with raw output | Vanilla 43/80 and valid sigmoid reduction | VERIFIED |
| 4 | [Claims 2–4](../current-claims-2-4-cumulative/page.md) | Yes: cumulative and domain verifiers | Yes: 73/80, 320, zero faulty | Frozen and cumulative JSON | Independent committed-evidence parser | Incomplete domain and threshold/validity assertions exit nonzero | Agent-proposed-query full-80 coverage versus 64/80 | VERIFIED |
| 5 | [Backend comparison](../current-claim-5-backends/page.md) | Yes: source, paired-result, and immutable-log extractors | Yes: all aggregate metrics and discrepancies | 40-row CSV, two 80-row JSON files, and aggregate JSON | Independent paired parser plus log-to-row aggregate cross-check | Truncated table and two label swaps rejected | Versioned LR/MILP RSR-Bench sample/runtime and current full-80 direction | VERIFIED |

Cross-cutting environment, exact command, Git SHAs, seed, CPU, runtime, and
cost are on [Current methods](../current-methods/page.md). Limitations and
deviations are inline on every claim page and available as raw Markdown.
The [evaluator-blind review](../../evidence/release/red_team.md) records every
file opened, the first-pass gaps, the fixes, and the repeated traversal.
