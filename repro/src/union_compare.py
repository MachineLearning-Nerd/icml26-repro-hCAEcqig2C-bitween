#!/usr/bin/env python3
"""Multi-seed union comparison for Claim 3.

A function counts as 'covered' (discovered) if ANY seed found >=1 verified RSR for
it — this is the faithful 'best-over-runs' coverage the paper reports, and it
removes run-to-run sampling nondeterminism. We union per-function coverage across
seeds for BOTH conditions, then report:

  - union coverage (functions covered in >=1 seed)  -> the discovery metric
  - verification accuracy from the BEST seed (highest acc) per condition, plus pooled

Usage:
  python repro/src/union_compare.py \
      --agentic outputs/abitween-gptoss-s1,outputs/abitween-gptoss-s2,outputs/abitween-gptoss-s3 \
      --neural  outputs/neural-gptoss-s1,outputs/neural-gptoss-s2,outputs/neural-gptoss-s3
"""
import argparse
import os
import re

from compare_agentic_neural import summarize  # reuse the single-dir parser

_RE_VER_HDR = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
_RE_UNVER_HDR = re.compile(r"^Unverified \((\d+)\):", re.MULTILINE)


def _per_func(res_dir):
    """Return {test_id: (verified, unverified)} for every <id>.txt in res_dir."""
    out = {}
    for f in sorted(os.listdir(res_dir)):
        if not f.endswith(".txt") or f.endswith("_trace.txt"):
            continue
        test_id = f[:-4]
        with open(os.path.join(res_dir, f), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        v = int(_RE_VER_HDR.search(text).group(1)) if _RE_VER_HDR.search(text) else 0
        u = int(_RE_UNVER_HDR.search(text).group(1)) if _RE_UNVER_HDR.search(text) else 0
        if v == 0 and "proved: True" in text:
            v = text.count("proved: True")
        out[test_id] = (v, u)
    return out


def union(dirs):
    """Union per-function coverage across dirs; also keep per-seed summaries."""
    seeds = [_per_func(d) for d in dirs]
    all_ids = sorted({tid for s in seeds for tid in s})
    union_covered = set()
    union_verified = 0
    union_unverified = 0
    for tid in all_ids:
        vs = [s[tid][0] for s in seeds if tid in s and s[tid][0] > 0]
        if vs:
            union_covered.add(tid)
            union_verified += max(vs)  # best verified count for that func across seeds
        # unverified: min across seeds that ran it (fewest false guesses is fairest upper bound)
        us = [s[tid][1] for s in seeds if tid in s]
        union_unverified += min(us) if us else 0
    seed_sums = [summarize(d) for d in dirs]
    best_acc = max((s["ver_accuracy"] for s in seed_sums), default=0.0)
    pooled_v = sum(s["verified"] for s in seed_sums)
    pooled_u = sum(s["unverified"] for s in seed_sums)
    pooled_acc = pooled_v / (pooled_v + pooled_u) if (pooled_v + pooled_u) else 0.0
    return dict(
        n_dirs=len(dirs),
        n_funcs=len(all_ids),
        covered=len(union_covered),
        coverage_pct=100.0 * len(union_covered) / len(all_ids) if all_ids else 0.0,
        union_verified=union_verified,
        union_unverified=union_unverified,
        union_acc=union_verified / (union_verified + union_unverified)
        if (union_verified + union_unverified) else 0.0,
        best_seed_acc=best_acc,
        pooled_acc=pooled_acc,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agentic", required=True, help="comma list of A-Bitwen seed res_dirs")
    ap.add_argument("--neural", required=True, help="comma list of neural seed res_dirs")
    args = ap.parse_args()

    a = union([d.strip() for d in args.agentic.split(",") if d.strip()])
    n = union([d.strip() for d in args.neural.split(",") if d.strip()])

    print("=" * 74)
    print(f"Claim 3 UNION over seeds (agentic {a['n_dirs']} seed(s) vs neural {n['n_dirs']} seed(s))")
    print("=" * 74)
    print(f"{'metric':36s} {'A-Bitwen':>16s} {'Neural':>16s}")
    print("-" * 74)
    for k, label, fmt in [
        ("n_funcs", "functions", "{:>16d}"),
        ("covered", "union covered (>=1 RSR in any seed)", "{:>16d}"),
        ("coverage_pct", "union coverage %", "{:>15.1f}%"),
        ("union_verified", "verified identities (best/func)", "{:>16d}"),
        ("union_unverified", "unverified candidates (min/func)", "{:>16d}"),
        ("union_acc", "union verification accuracy", "{:>15.1%}"),
        ("best_seed_acc", "best single-seed verify accuracy", "{:>15.1%}"),
        ("pooled_acc", "pooled verify accuracy (all seeds)", "{:>15.1%}"),
    ]:
        print(f"  {label:34s} {fmt.format(a[k])} {fmt.format(n[k])}")
    print("-" * 74)
    verdict = "AGENTIC > NEURAL on discovery AND verification" if (
        a["covered"] > n["covered"] and a["union_acc"] >= n["union_acc"]) else "see numbers (may be tied)"
    print(f"Claim 3 union outcome: {verdict}")


if __name__ == "__main__":
    main()
