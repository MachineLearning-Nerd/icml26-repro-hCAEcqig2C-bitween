# Claims 2–4 method

The unmodified upstream harness at Git SHA `e13d4b59` is run across the full
80-function benchmark. A separate parser requires one and only one complete
ID span 01–80, reconstructs coverage and identity counts, and rejects faulty
identities.

For Claim 3, every recovered identity supported by the independent registry is
reparsed and numerically falsified. Sigmoid identities use 20,000 fresh
samples. Three known-false exponential, sigmoid, and square identities must be
rejected.

For Claim 4, the previously accepted full-scale gpt-oss-120b log set is parsed
anew in every cumulative run. The checker requires all 80 functions, coverage
at least 64, at least 320 verified identities, and zero faulty identities.

The fixed command, uv lock, seed, and HF CPU allocation are recorded on the
candidate's current methods page.
