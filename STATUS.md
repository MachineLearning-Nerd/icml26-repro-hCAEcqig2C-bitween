# STATUS — Learning Randomized Reductions (Bitwen), hCAEcqig2C

**Space:** https://huggingface.co/spaces/DineshAI/hCAEcqig2C
**Score:** 4/6 currently; primary C3 counterexample audit complete, pending Space sync/re-judge (updated 2026-07-17)

## Claims
- **C1 (Vanilla): verified (2 pt).** 87 verified identities = paper exact; sigmoid RSR reproduced.
- **C2 (Agentic): verified (2 pt).** 73/80 (91.2%) vs claimed 64/80 (80%) — exceeded.
- **C3 (Agentic vs neural): not reproduced in the matched GPT-OSS setting.** Neural discovery is ahead in all three complete seeds (74>73, 77>72, 72>71), while agentic verification accuracy is higher. The conjunctive claim therefore has a full-scale counterexample.

## C3 campaign (why the primary verdict changed)
With gpt-oss-120b (the paper's open model), the agentic **discovery** edge does not
appear in any of the three matched full-scale seeds. The earlier best-of-seeds
union was exploratory, not an independent paired estimator, and does not override
the per-seed direction.

Experiments run (full audit in `C3_EXPERIMENTS.md`):
- gpt-oss-120b × 3 seeds: agentic 73/72/71 vs neural 74/77/72; verify-acc ~90% vs
  ~80% (clear, all seeds). Primary result: `outputs/c3_primary_paired_audit.json`.
- gpt-oss-20b full/hard: agentic LOSES (too weak to drive tool loop).
- Llama-3.3-70B full-80: agentic LOSES discovery (43 vs 55).
- Kimi-K2.6: format fail. Llama-4-Maverick: no function-calling. DeepSeek-R1/V4-Pro:
  too slow (~3 min/fn). Qwen3.6: too slow. → gpt-oss-120b is the only viable backbone.
- Mechanism (hard 12-fn subset): agentic 10/12 (70%) vs neural 9/12 (49%).

## Outcome / next
- Local logbook and executable primary audit are complete; publish after HF
  authentication is refreshed.
- C3 should earn full falsification credit if the judge accepts a documented
  full-scale counterexample: discovery fails even though verification improves.
- The paper's own GPT-OSS aggregate row also reports 59% Agentic RSR coverage vs
  62% Neural Research; the positive headline comes from the unavailable
  Claude-class row.
