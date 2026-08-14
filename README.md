# Learning Randomized Reductions (Bitween)

ICML 2026 reproduction audit for *Learning Randomized Reductions*.

Paper: [arXiv 2412.18134](https://arxiv.org/abs/2412.18134) · OpenReview
`hCAEcqig2C` · [official authors' code](https://github.com/ferhaterata/learning-randomized-reductions)

This repository is an independent reproduction and audit. It is not the
authors' official implementation.

## Result at a glance

The checked-in package has five scoped reproduction contracts, all passing,
with important qualifications documented below. A separate matched audit of
the paper's Agentic-versus-Neural headline does **not** reproduce the claimed
discovery advantage.

| Contract | Status | What the saved evidence shows |
|---|---|---|
| Section 4 theory | `VERIFIED` | PAC-to-RSR case split, finite-field separation, and BLR recovery pass; the paper's supplied binary witness is rejected at `epsilon=1/2`, and an independent ternary witness repairs the proof route. |
| RSR-Bench domain | `VERIFIED` | Exactly 80 functions, IDs `01..80`; incomplete and duplicate/omitted domains are rejected. |
| Vanilla Bitween | `VERIFIED_SCOPED` | Frozen baseline: 43/80 functions, 91 verified identities, 0 faulty, and 3 sigmoid identities; later seeded runs cover 39–42 functions, so run variation is disclosed. |
| Agentic Bitween | `VERIFIED_SCOPED` | 73/80 functions with at least one SymPy-verified identity, 320 identities, 0 faulty; this is broader than the paper's manually curated 64/80 RSR metric. |
| LR versus MILP | `VERIFIED_VERSION_RESOLVED` | Final paired Gurobi run: LR/MILP coverage 42/38, verified identities 91/70, mean time 10.44425/14.450125 s, 0 faulty, label swap rejected. |

### Separate Agentic-versus-Neural audit

`outputs/c3_primary_paired_audit.json` contains three matched full-80 GPT-OSS
runs. Neural discovery is ahead in every pair: `(74,73)`, `(77,72)`, and
`(72,71)` for neural versus agentic coverage. Agentic verification accuracy is
higher when identities are checked (`0.897959` versus `0.791852`). The result
is `not_reproduced_in_this_full_scale_open_model_reproduction`; it is not
silently converted into a positive claim.

No live judge score, score forecast, or author endorsement is claimed here.

The complete mapping is in [`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md).

## What the paper does

Bitween learns randomized self-reductions (RSRs): identities that recover or
verify `f(x)` using evaluations of `f` at correlated random query points. The
paper formalizes RSR learning under uniform query marginals, gives PAC/sample-
complexity results, introduces Vanilla Bitween with fixed query templates,
and introduces Agentic Bitween, where an LLM proposes richer query functions.
The benchmark is RSR-Bench, an 80-function suite spanning arithmetic,
transcendentals, activations, rational functions, continued fractions, and
multivariate examples.

The current arXiv record lists Ferhat Erata, Orr Paradise, Thanos Typaldos,
Timos Antonopoulos, ThanhVu Nguyen, Shafi Goldwasser, and Ruzica Piskac as
authors, and identifies the work as an ICML 2026 Spotlight.

## How each result is produced

| Evidence path | Producer | Output |
|---|---|---|
| Theory | `repro/src/verify_theory.py` and `verify_theory_independent.py` | Primary and independent theory JSON, including binary boundary rejection, ternary witness, rank/nullity checks, and a broken-recovery control. |
| Domain and Vanilla | `repro/src/run_vanilla.py`, `aggregate.py`, `verify_independent.py`, `sigmoid_check.py` | Full 80-function logs, aggregate counts, independently reparsed identities, 20,000-sample sigmoid checks, and false-identity controls. |
| Agentic | `repro/src/aggregate.py` plus the cumulative verifier | Reparse of the committed full-scale agentic logs; expensive LLM generation is not claimed as newly rerun. |
| Agentic versus Neural | `repro/src/claim3_falsification.py` | Three paired GPT-OSS full-scale comparisons; every pair must retain the direction `neural_ahead`. |
| Backend comparison | `repro/src/verify_backend_source.py`, `run_vanilla.py --method eager_milp`, and `compare_backends.py` | Complete v1 table audit, current v5 source audit, paired Gurobi rows, aggregate metrics, and LR/MILP label-swap control. |

The canonical machine-readable evidence lives under
`.openresearch/artifacts/`. The publication gate bundles the selected evidence
without writing to any external service.

## Repository layout

```text
upstream/                    unmodified authors' code at the pinned commit
repro/configs/               fixed campaign and Vanilla-LR contracts
repro/src/                   producers, independent checkers, and controls
repro/tests/                 focused verifier tests
outputs/                     saved paired audit and publication readback JSON
.openresearch/artifacts/     canonical claim, provenance, and run evidence
sources/                     hash-bound arXiv v1/v5 source artifacts
docs/                        claim, source, branch, research, and gate guides
hf_space/                    archival evaluator snapshot; not canonical output
reports/                     detailed scientific report and historical release notes
```

The old duplicated `.trackio/` publisher state was removed. No token, private
publisher path, or external write is required to inspect or validate this
repository.

## Reproduce or validate

The fixed campaign command used by the experiment lineage is:

```bash
uv sync --frozen
uv pip install --python .venv/bin/python --no-deps -e ./upstream
.venv/bin/python repro/src/run_campaign.py
```

This command can launch expensive full-scale CPU/Gurobi stages described in
`repro/configs/campaign.json`; it is not needed for a read-only publication
check. To validate the checked-in evidence without rerunning producers:

```bash
python3 repro/src/publication_gate.py --skip-producers
python3 -m unittest discover -s repro/tests -p 'test_*.py'
```

The gate checks source hashes, all five scoped contracts, the separate neural
counterexample, controls, and repository hygiene, then writes:

- `outputs/evidence_bundle.jsonl`
- `outputs/artifact_manifest.json`
- `outputs/publication_gate.json`

## Branch lineage

`main` is the clean publication surface. Historical experiment branches are
preserved under descriptive names:

| Final branch | Role |
|---|---|
| `baseline/frozen-6-of-10` | Frozen full-domain baseline and accepted 43/80 Vanilla result. |
| `audit/section-4-theory` | Section 4 theorem and boundary audit. |
| `audit/versioned-backend-source` | v1/v5 source and complete-table audit. |
| `experiment/full-80-gurobi` | Paper-relevant Gurobi comparison. |
| `experiment/full-80-pulp` | Open-source PuLP robustness substitution. |
| `release/integrated-five-claim` | Cumulative release candidate and final run. |

The old `orx/*` to final mapping, historical tips, and branch policy are in
[`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md). Branches are evidence lineage,
not separate undocumented claims.

## Limitations and interpretation boundaries

- The supplied Appendix A.2 binary witness does not establish the boundary
  case `epsilon=1/2`; the ternary construction is the independent repair.
- Vanilla coverage varies across seeded runs because the upstream numerical
  stack has residual variation. The frozen 43/80 result and later counts are
  all retained.
- Agentic coverage counts functions with at least one verified identity; the
  paper's 64/80 value is manually curated, so 73/80 is not an exact re-count of
  that curation policy.
- The expensive LLM generation is preserved as committed raw evidence rather
  than represented as a new local rerun.
- The v1 backend table and v5 current harness expose different sample metrics;
  the source audit keeps those metrics separate. Gurobi is the primary route;
  PuLP is explicitly a solver substitution.
- Runtime is hardware- and implementation-sensitive. The paired comparison
  uses the same seed, timeout, commit, and container flavor for both backends,
  but does not claim universal portability.

## Citation

```bibtex
@inproceedings{erata2026learning,
  title     = {Learning Randomized Reductions},
  author    = {Erata, Ferhat and Paradise, Orr and Typaldos, Thanos and
               Antonopoulos, Timos and Nguyen, ThanhVu and Goldwasser, Shafi
               and Piskac, Ruzica},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year      = {2026},
  volume    = {306},
  eprint    = {2412.18134},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG}
}
```

## Thank you

Thank you to Ferhat Erata, Orr Paradise, Thanos Typaldos, Timos Antonopoulos,
ThanhVu Nguyen, Shafi Goldwasser, and Ruzica Piskac for developing Bitween,
publishing the RSR-Bench task, and making the source and claims concrete enough
to audit. This reproduction is offered as a careful companion to the paper:
qualifications and failed controls are kept visible because they make the
result more useful to future readers.
