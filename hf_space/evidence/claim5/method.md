# Claim 5 method

The verification uses three genuinely different routes.

1. `repro/src/verify_backend_source.py` verifies the versioned source
   attribution, reads the complete 40-row v1 table transcription and the
   committed 80-row v5 table, and independently recomputes every aggregate and
   paired direction.
2. The same verifier performs a complete-table consistency test rather than
   selecting favorable functions. It must reject a 39-row truncation and an
   LR/MILP label swap.
3. `repro/src/run_vanilla.py` runs the unmodified upstream discovery harness
   on every one of the 80 current benchmark functions for the configured MILP
   solver. The cumulative campaign has already run multiple regression under
   the same seed and timeout. `repro/src/compare_backends.py` independently
   reparses all 160 per-function logs, checks exact IDs `1..80`, computes
   paired and aggregate metrics, and exits nonzero unless the current v5
   directional contract holds. A label-swap mutation must be rejected.

Every route is called by the one fixed campaign command. Solver selection is
committed in `repro/configs/campaign.json`; it is never passed by changing the
run command or an environment variable.
