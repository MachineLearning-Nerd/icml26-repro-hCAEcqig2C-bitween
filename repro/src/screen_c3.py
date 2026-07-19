#!/usr/bin/env python
"""Fast C3 screener: run a SUBSET of RSR-Bench functions for one model under one
condition (abitween = agentic tools ON, neural = tools OFF), then print per-function
verified/unverified so we can cheaply compare agentic vs neural discovery before
committing to a full 80-function run.

It reuses the upstream harness verbatim (no upstream changes): it imports the
`test_*` functions from bitween.evaluation.evaluation_rsr_bench_agentic_paper and
calls them with the same (agent, res_dir, custom_tools, mcp_tools, timeout) tuple
the upstream `main()` uses. Each test writes its <test_id>.txt log; we parse those
with repro/src/aggregate.py's parse_log.

Usage:
  HF_TOKEN=$(cat ~/.cache/huggingface/token) python repro/src/screen_c3.py \\
      --model_id openai/gpt-oss-120b --condition abitween \\
      --res_dir outputs/screen/gptoss-abitween \\
      --functions test_tan,test_cot,test_inverse,test_cos,test_cosh,test_sin,test_sinh,test_log,test_sinc,test_tanh,test_sigmoid,test_softmax2_1
"""
import argparse
import os
import sys
import time

# Make `repro.src.aggregate` importable when run as a script from the paper dir.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib

_aggregate = importlib.import_module("aggregate")  # type: ignore

import bitween.evaluation.evaluation_rsr_bench_agentic_paper as MOD_BASE
import bitween.evaluation.evaluation_rsr_bench_agentic_paper_extended as MOD_EXT
from bitween.openai_agent import OpenAIAgent


BASE_URL = "https://router.huggingface.co/v1"


def get_token() -> str:
    for getter in (
        lambda: os.environ.get("HF_TOKEN"),
        lambda: os.environ.get("OPENAI_API_KEY"),
        lambda: (
            open(os.path.expanduser("~/.cache/huggingface/token")).read().strip()
            if os.path.exists(os.path.expanduser("~/.cache/huggingface/token"))
            else None
        ),
    ):
        t = getter()
        if t:
            return t
    raise SystemExit("No HF token found (set HF_TOKEN or log in with `hf`).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model_id", required=True)
    ap.add_argument("--condition", required=True, choices=("abitween", "neural"))
    ap.add_argument("--res_dir", required=True)
    ap.add_argument(
        "--functions",
        default="test_tan,test_cot,test_inverse,test_cos,test_cosh,test_sin,test_sinh,test_log,test_sinc,test_tanh,test_sigmoid,test_softmax2_1",
        help="comma list of test_* function names from the base agentic module",
    )
    ap.add_argument(
        "--module",
        default="base",
        choices=("base", "extended", "both"),
        help="which upstream module to resolve --functions from (extended holds the hard transcendental/discontinuous fns)",
    )
    ap.add_argument("--base_url", default=BASE_URL)
    ap.add_argument("--api_key", default=None)
    ap.add_argument("--max_tokens", type=int, default=16_000)
    ap.add_argument("--timeout_sec", type=float, default=300.0)
    args = ap.parse_args()

    api_key = args.api_key or get_token()
    os.makedirs(args.res_dir, exist_ok=True)

    # Condition -> custom_tools, mirroring repro/src/run_agentic_local.sh exactly.
    if args.condition == "abitween":
        custom_tools = ["infer_property_tool", "symbolic_verify_tool"]  # full A-Bitwen
    else:
        custom_tools = []  # bare --custom_tools -> tools OFF (Neural-Research baseline)
    mcp_tools = ["sequential_thinking"]  # default in BaseAgent.mcp_clients; both conditions get it

    agent = OpenAIAgent(
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=api_key,
        max_tokens=args.max_tokens,
    )

    names = [n.strip() for n in args.functions.split(",") if n.strip()]
    test_args = (agent, args.res_dir, custom_tools, mcp_tools, args.timeout_sec)

    def resolve(name):
        mods = {"base": [MOD_BASE], "extended": [MOD_EXT], "both": [MOD_BASE, MOD_EXT]}[args.module]
        for m in mods:
            fn = getattr(m, name, None)
            if fn is not None:
                return fn
        return None

    print(f"[screen] model={args.model_id} cond={args.condition} module={args.module} "
          f"tools={custom_tools or 'OFF'} n_funcs={len(names)} -> {args.res_dir}", flush=True)
    t0 = time.time()
    for n in names:
        fn = resolve(n)
        if fn is None:
            print(f"  ! {n} not found in module(s), skipping", flush=True)
            continue
        ts = time.time()
        try:
            fn(*test_args)
        except Exception as e:
            print(f"  ! {n} raised: {e}", flush=True)
        print(f"  . {n} done in {time.time()-ts:.1f}s", flush=True)
    print(f"[screen] all funcs done in {time.time()-t0:.1f}s; parsing logs", flush=True)

    # Parse the .txt logs this run produced and print a compact table.
    import glob
    covered = verified_total = unverified_total = 0
    print(f"\n{'test_id':<22}{'verified':>9}{'unverified':>11}{'has_rsr':>9}")
    print("-" * 51)
    for txt in sorted(glob.glob(os.path.join(args.res_dir, "*.txt"))):
        if txt.endswith("_trace.txt"):
            continue
        try:
            rec = _aggregate.parse_log(txt)
        except Exception as e:
            print(f"  parse error {os.path.basename(txt)}: {e}")
            continue
        verified_total += rec["verified"]
        unverified_total += rec["unverified"]
        if rec["has_rsr"]:
            covered += 1
        print(f"{rec['test_id']:<22}{rec['verified']:>9}{rec['unverified']:>11}{rec['has_rsr']:>9}")
    n_logs = len([f for f in glob.glob(os.path.join(args.res_dir, "*.txt")) if not f.endswith("_trace.txt")])
    denom = verified_total + unverified_total
    acc = (verified_total / denom) if denom else 0.0
    print("-" * 51)
    print(f"SUMMARY {args.model_id} [{args.condition}]: "
          f"covered={covered}/{n_logs}  verified_ids={verified_total}  "
          f"unverified={unverified_total}  verify_acc={acc:.1%}\n")


if __name__ == "__main__":
    main()
