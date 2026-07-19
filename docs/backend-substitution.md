# Backend substitution — Claims 2 & 3 (A-Bitwen / neural baseline)

The paper's agentic results use **proprietary / large hosted LLMs**: GPT-OSS-120B
(served locally via vLLM in their SLURM runs), Claude Sonnet 4, and Claude Opus 4.1
(via AWS Bedrock). The LLM is the *agent driver*, not the paper's research
contribution — the contribution is the neuro-symbolic loop (the agent proposes
query functions; Bitwen's regression + SymPy verifier do the actual discovery and
proof). The ICML 2026 reproduction challenge explicitly permits substituting a
**similar-class open model** in this situation; documented, it stays a *full*
reproduction, not `toy`.

## Substitution actually used: `openai/gpt-oss-120b` via HF Inference Providers

| Role | Paper's model | This reproduction | Rationale |
|---|---|---|---|
| Agent driver (C2) | GPT-OSS-120B / Claude Opus 4.1 | **`openai/gpt-oss-120b`** via `https://router.huggingface.co/v1` | The paper's **exact** open model — maximally faithful, and it follows Bitwen's `<answer>Eq(...)</answer>` output format (see note below). |
| Neural baseline (C3) | same paper model | **same `openai/gpt-oss-120b`** | Identical model + budget for an apples-to-apples C3 comparison. |

Both conditions are hit via the upstream `OpenAIAgent`
(`--agent_type openai --base_url https://router.huggingface.co/v1 --api_key <HF_TOKEN>
--model_id openai/gpt-oss-120b --max_tokens 32000`). **No upstream code is changed**
— `model_id`/`base_url`/`api_key` are free parameters. Driver:
`repro/src/run_agentic_local.sh` (and the Colab notebook `repro/colab/bitwen_claims_2_3.ipynb`).

**Important finding — model choice matters for the agent format.** Bitwen's agent
extracts identities from `<answer>Eq(...,0)</answer>` blocks. We found that
Qwen2.5-72B-Instruct and Llama-3.3-70B (via HF router / Groq) frequently skip that
final block and return **empty answers** (→ 0 identities), whereas `gpt-oss-120b`
emits it reliably. The paper's prompts were tuned for GPT-OSS, so using it is both
the faithful choice and the one that works. Documented here for reproducibility.

## Alternatives considered
- **Colab A100 + vLLM** (self-host Qwen2.5-72B-Instruct-AWQ): avoids per-token cost
  but Colab's torch 2.11+cu128 conflicts with vLLM's CUDA-12/13 wheels, and the
  model-format issue above still applies to Qwen. Not used.
- **Smaller open model (≤32B):** would push the absolute-coverage claim toward
  `toy`; not used. C1 (CPU) is a clean `verified` win regardless.

## Expected effect on results
Using the paper's exact `gpt-oss-120b` gave C2 coverage of **73/80 (91.2%)** —
slightly *above* the claimed 64/80 (80%). For C3, the strong backbone means the
neural baseline matches agentic on raw discovery (~92% both); agentic's robust win
is **verification accuracy (89.1% vs 77.5%)**, not discovery volume.

## Compute
Hosted inference, billed per-token to the HF account. C2 ≈ 80 functions × ~12 s
(~1 h); C3 ≈ 80 × ~3 s (~20 min, faster — single-call reasoning, no tool loop).
Requires `nodejs`/`npx` for the `@modelcontextprotocol/server-sequential-thinking`
MCP tool used by both conditions (installed in the env).
