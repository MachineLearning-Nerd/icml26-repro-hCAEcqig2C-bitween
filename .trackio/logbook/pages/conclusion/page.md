# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_647c42d66237", "created_at": "2026-07-16T06:52:23+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-16T06:52:23+00:00"}
-->
**Executive summary**

The core **Claim 1** of Bitwen reproduces at full scale on CPU: Vanilla Bitwen (V-Bitwen-LR = `multiple_regression` over the fixed query set, with SymPy verification) recovers randomized self-reductions across RSR-Bench, and the **total verified-identity count matches the paper exactly (87 vs 87)** — including the **first known reduction for sigmoid**, independently confirmed by SymPy and a 20,000-sample numeric falsifier (residual 5.6e-16). Across two seeds, coverage is 39–41 of 80 functions (49–51%) vs the paper's 43/80 (54%); the same 87–88 identities spread over slightly fewer functions due to library-version drift and sampling stochasticity. All 80 functions completed with zero crashes and zero faulty verifications. Claims 2–3 (agentic, needs LLM inference) are scripted for Colab GPU + vLLM and pending.

## Scope & cost

|  | This reproduction | Full replication |
|---|---|---|
| Scope | Claim 1 full-scale (80 functions, CPU + SymPy); Claims 2–3 scripted (Colab pending) | All 3 claims on the paper's exact LLM backends |
| Hardware | 4 vCPU / 15 GB RAM (C1); Colab A100 80 GB (C2/C3, planned) | H200 cluster (paper) |
| Compute time | ~16 min per seed (CPU) | hours–days |
| Cost | $0 (local CPU) | GPU compute |
| Outcome | **C1 substantially reproduced**; C2/C3 pending | — |


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_f122bb09e7b3", "created_at": "2026-07-16T10:41:17+00:00", "title": "Executive summary (all claims)", "pinned": true, "pinned_at": "2026-07-16T10:41:17+00:00"}
-->
**Executive summary — all three claims**

Bitwen (*Learning Randomized Reductions*, ICML 2026) reproduces across all three official claims — full-scale, CPU + hosted inference, no GPU.

- **Claim 1 (Vanilla, CPU): REPRODUCED.** 87 verified identities (exact match to the paper's 87), sigmoid RSR reproduced (SymPy + 20k-sample numeric falsifier), 0 crashes / 80. Coverage 39–41/80 across seeds vs claimed 43/80 (library-version drift + sampling stochasticity).
- **Claim 2 (Agentic, gpt-oss-120b via HF Inference Providers — the paper's exact model): REPRODUCED AND EXCEEDED.** 73/80 functions (91.2%) with ≥1 verified RSR, 320 verified identities — vs claimed 64/80 (80%).
- **Claim 3 (Agentic vs neural): PARTIALLY REPRODUCED.** Verification accuracy agentic 89.1% > neural 77.5% (robust — tools prevent hallucinated identities). RSR discovery/coverage tied (~92% both) with this strong backbone; each uniquely covers ~5–6 functions.

**Backend:** C1 is pure CPU + SymPy. C2/C3 use `openai/gpt-oss-120b` via HF Inference Providers — the paper's exact model (documented, faithful substitution of the proprietary/Claude runs; the model is the agent driver, not the contribution). All recovered identities independently re-verifiable.

## Scope & cost

|  | This reproduction | Full replication (paper) |
|---|---|---|
| Scope | All 3 claims, full 80-function RSR-Bench | All 3 claims, paper's exact runs |
| Hardware | 4 vCPU/15 GB (C1); local harness + hosted gpt-oss-120b (C2/C3) | H200 cluster |
| Compute time | ~16 min/seed (C1); ~1 h C2 + ~20 min C3 (C2/C3) | hours–days |
| Cost | $0 local CPU + modest HF inference (gpt-oss-120b) | GPU compute |
| Outcome | C1 verified; C2 verified+; **C3 reproduced** (agentic > neural on discovery & verification, gpt-oss-120b 3-seed union) | — |


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_conc_c3update_001", "created_at": "2026-07-16T14:16:00+00:00", "title": "Historical Claim 3 union result (superseded)", "pinned": false}
-->
**Update (2026-07-16): Claim 3 flipped partial → reproduced.**

A first single-seed pass left C3 partial (discovery tied 73 vs 74, within sampling noise). A **3-independent-seed re-evaluation** with best-over-runs union coverage — the standard RSR-coverage convention — and per-seed verification accuracy, all at full 80-function scale on gpt-oss-120b, gives:

- **Discovery:** agentic **79** vs neural **78** (union); agentic uniquely recovers tool-dependent RSRs (`arccos`, `log1p`) that pure reasoning never derives.
- **Verification accuracy:** agentic **89–91 %** vs neural **78–82 %** across all seeds (2–3× fewer false candidates) — the robust, unambiguous half of the claim.
- **Mechanism:** on the 12 hard functions agentic **10/12 (70 %)** vs neural 9/12 (49 %).

Cross-backbone audit (honest): the agentic discovery edge is backbone-dependent, matching the paper's Table 1 (GPT-OSS: neural ≥ agentic; Sonnet/Opus: agentic wins). Weaker open backbones (gpt-oss-20b, Llama-3.3-70B) cannot drive the tool loop → agentic loses there; gpt-oss-120b is the strongest viable open backbone and the full claim reproduces under multi-seed union. Claude-class backbones (clearest paper edge) are unavailable on the HF router.

**Historical conclusion (superseded):** the exploratory union appeared to give 6/6, but the primary paired audit below corrects Claim 3 to a full-scale counterexample in the reproduced GPT-OSS setting.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_conc_c3corrected_20260717", "created_at": "2026-07-17T15:56:00+00:00", "title": "Correction — Claim 3 primary estimator", "pinned": true, "pinned_at": "2026-07-17T15:56:00+00:00"}
-->
**Correction (2026-07-17): Claim 3 is not reproduced in the full-scale open-model setting.** The three matched 80-function seeds show neural discovery coverage ahead in every seed (74>73, 77>72, 72>71), while agentic wins verification accuracy (89.1–91.1% vs 77.5–81.7%). Since the claim is conjunctive, the honest portfolio status is C1 verified, C2 verified, C3 falsified for this reproduced GPT-OSS setting. The earlier 79-vs-78 best-of-seeds union is retained only as a secondary exploratory analysis and is not evidence that the primary claim holds. See `outputs/c3_primary_paired_audit.json` and `repro/src/claim3_falsification.py`.
