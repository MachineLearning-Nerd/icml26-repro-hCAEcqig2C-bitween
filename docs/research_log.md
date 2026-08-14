# Research log

## 2026-08-14 — publication audit

- Confirmed the paper identity from arXiv `2412.18134v5`, OpenReview
  `hCAEcqig2C`, and the authors' official Bitween repository.
- Verified the saved five-contract evidence and the separate three-seed
  Agentic-versus-Neural audit before editing the publication surface.
- Downloaded and hash-checked arXiv v1/v5 source archives and the v5 PDF.
- Chose `icml26-learning-randomized-reductions` as the descriptive final repo
  name; branch roles are documented in `docs/BRANCH_AUDIT.md`.
- Removed duplicated private `.trackio` publisher state. `.openresearch/` is
  retained as canonical machine-readable evidence; `hf_space/` is retained
  only as an explicitly archival evaluator snapshot.
- Added a local publication gate so the README cannot claim a clean release
  without checking the evidence, source hashes, controls, and hygiene.
