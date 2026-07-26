# Claims 2–4 limitations and deviations

- The paper's “first known” priority wording for sigmoid is a literature claim;
  the reproduction directly verifies the identity, not historical priority.
- Full vanilla coverage varies from 39 to 43 across recorded runs. The frozen
  baseline exactly matches 43/80; later runs preserve at least 87 identities
  and the exact sigmoid reduction.
- Even after seeding both Python and NumPy, the two backend-stage LR prefixes
  produce 88 identities but cover 40 and 41 functions. Residual numerical or
  scheduling nondeterminism remains.
- Agentic coverage is measured as at least one SymPy-verified identity per
  function. It is broader than the paper's manually curated RSR label.
- The expensive LLM generation is not repeated in this CPU-only campaign; the
  existing full-scale raw log set is cumulatively reparsed and checked.
