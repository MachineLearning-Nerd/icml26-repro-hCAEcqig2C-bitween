# Local publication gate

Run the gate from a clean checkout:

```bash
python3 repro/src/publication_gate.py --skip-producers
```

The gate is repository-native, standard-library-only, and performs no external
write. It validates:

- paper/source IDs and the three downloaded artifact hashes;
- Claim 1 primary and independent theory verifiers, including the rejected
  binary boundary witness and verified ternary witness;
- the exact 80-function domain, frozen vanilla result, sigmoid checks, agentic
  evidence, and false-identity/domain controls;
- the v1/v5 backend source audit, 80 paired Gurobi rows, aggregate values,
  zero faulty identities, label-swap control, and the labeled PuLP deviation;
- the separate three-seed neural comparison counterexample;
- absence of tracked `.trackio` publisher state, environment files, token-like
  values, and absolute local user paths.

The command writes three deterministic readback artifacts:

- `outputs/evidence_bundle.jsonl`
- `outputs/artifact_manifest.json`
- `outputs/publication_gate.json`

The gate intentionally does not rerun the expensive CPU/Gurobi/LLM producers
when `--skip-producers` is supplied. The checked-in evidence is the object of
the publication check; full producers remain available through the fixed
campaign command documented in the README.
