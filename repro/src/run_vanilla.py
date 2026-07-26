#!/usr/bin/env python3
"""Drive V-Bitween-LR (multiple_regression) over all 80 RSR-Bench functions.

Sets a numpy seed for best-effort reproducibility, then executes the two
upstream harness modules' ``__main__`` blocks (functions 1-40 and 41-80) via
:mod:`runpy`, writing per-function logs to ``--res_dir``. No upstream code is
modified; this only re-uses the authors' exact active test list.

Usage:
    python run_vanilla.py --seed 42 --res_dir outputs/vbitween-lr/seed42 \
        --timeout_sec 1800 --method multiple_regression
"""
import argparse
import os
import random
import runpy
import sys
import time

import numpy as np


def run_module(modname: str, argv: list[str]) -> None:
    """Execute an upstream harness module's ``__main__`` block with given argv."""
    saved = sys.argv
    sys.argv = argv
    try:
        runpy.run_module(modname, run_name="__main__")
    finally:
        sys.argv = saved


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=42, help="numpy random seed")
    ap.add_argument("--res_dir", required=True, help="output directory for per-function .txt logs")
    ap.add_argument("--timeout_sec", type=float, default=1800.0, help="per-function wall cap (s)")
    ap.add_argument("--method", default="multiple_regression", help="fitting method")
    ap.add_argument("--milp", choices=["gurobi", "pulp", "glpk"], help="MILP solver")
    ap.add_argument("--scope", choices=["both", "base", "extended"], default="both")
    args = ap.parse_args()

    os.makedirs(args.res_dir, exist_ok=True)
    random.seed(args.seed)
    np.random.seed(args.seed)

    common_argv = [
        "harness",
        "--method", args.method,
        "--res_dir", args.res_dir,
        "--timeout_sec", str(args.timeout_sec),
    ]
    if args.milp:
        common_argv.extend(["--milp", args.milp])

    st = time.time()
    if args.scope in ("both", "base"):
        print(f"[run_vanilla] base (functions 1-40), seed={args.seed} -> {args.res_dir}", flush=True)
        run_module("bitween.evaluation.evaluation_rsr_bench_paper", common_argv)
    if args.scope in ("both", "extended"):
        print(f"[run_vanilla] extended (functions 41-80), seed={args.seed} -> {args.res_dir}", flush=True)
        run_module("bitween.evaluation.evaluation_rsr_bench_paper_extended", common_argv)

    print(f"[run_vanilla] DONE in {time.time() - st:.1f}s -> {args.res_dir}", flush=True)


if __name__ == "__main__":
    main()
