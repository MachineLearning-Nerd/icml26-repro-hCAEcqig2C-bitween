# Claim 5 failure boundary

Two first attempts stopped before either MILP solver ran. They are
**Historical rejected baseline** runs, not negative backend results:

- Gurobi-target run `c79c0917-4054-435e-9c68-ccd78c53a392` stopped when the
  fresh LR prefix produced 86 identities, below the precommitted cumulative
  threshold of 87.
- PuLP-target run `790d2645-2542-49b2-aa8e-b95f26b0057d` stopped at the same
  gate with 83 identities.

The wrapper had seeded NumPy, but the upstream sampler also uses Python
`random`. Commit `39b5adf`/`ffa7b98` seeded both and retained the original
threshold. The successful reruns each produced 88 LR identities and reached
the solvers.

The two seeded LR prefixes nevertheless covered 40 and 41 functions. The
remaining variation is attributed to numerical or scheduling behavior in the
scientific stack and is disclosed; the verified-identity count and all
directional backend conclusions agree.
