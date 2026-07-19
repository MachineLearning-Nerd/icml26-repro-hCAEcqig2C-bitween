#!/usr/bin/env python3
"""Aggregate V-Bitwen-LR per-function logs into a summary table and cross-check
against the authors' canonical results CSV.

Reads every ``<test_id>.txt`` written by the upstream harness in ``--res_dir``,
parses the ``Equations found``, ``Verified (n)``, ``Unverified (n)``,
``Faulty (n)``, ``Unknown (n)`` and ``Took time`` lines, and writes
``summary.csv``. It then prints coverage (functions with >=1 verified identity)
and compares totals to the ``mreg (vanilla Bitween)`` columns of the canonical
``Bitween-Results(Sheet1-ICML).csv``.

For V-Bitwen-LR the paper reports RSR count == verified count (87 == 87), so
"functions with >=1 verified identity" is a faithful automatable proxy for the
paper's RSR coverage.
"""
import argparse
import csv
import os
import re
import sys

# Canonical CSV column indices for the "mreg (vanilla Bitween)" block.
MREG_NUM, MREG_RSR, MREG_VERIFIED, MREG_UNVERIFIED, MREG_TIME = 0, 18, 19, 20, 21

_RE_EQS = re.compile(r"Equations found:\s*(\d+)")
_RE_VERIFIED = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
_RE_UNVERIFIED = re.compile(r"^Unverified \((\d+)\):", re.MULTILINE)
_RE_FAULTY = re.compile(r"^Faulty \((\d+)\):", re.MULTILINE)
_RE_UNKNOWN = re.compile(r"^Unknown \((\d+)\):", re.MULTILINE)
_RE_TIME = re.compile(r"Took time:\s*([\d.]+)s")
_RE_START = re.compile(r"Starting ([\w-]+)")


def _gr(regex, text, cast=int):
    m = regex.search(text)
    return cast(m.group(1)) if m else 0


def parse_log(path: str) -> dict:
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    test_id = os.path.splitext(os.path.basename(path))[0]
    started = bool(_RE_START.search(text))
    return {
        "test_id": test_id,
        "number": int(re.split(r"_", test_id, 1)[0]) if re.match(r"\d+", test_id) else "",
        "started": started,
        "eqs_found": _gr(_RE_EQS, text),
        "verified": _gr(_RE_VERIFIED, text),
        "unverified": _gr(_RE_UNVERIFIED, text),
        "faulty": _gr(_RE_FAULTY, text),
        "unknown": _gr(_RE_UNKNOWN, text),
        "took_time_s": _gr(_RE_TIME, text, float),
        "has_rsr": 1 if _gr(_RE_VERIFIED, text) > 0 else 0,
    }


def parse_canonical_mreg(csv_path: str) -> dict:
    """Return {number: (rsr, verified, unverified, time)} for mreg, plus 'agg' totals."""
    out: dict = {}
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.reader(fh))
    for row in rows:
        cells = row + [""] * 64
        first = (cells[0] or "").strip()
        # aggregate row begins with "*"
        if first.startswith("*"):
            try:
                out["agg"] = (
                    int(float(cells[MREG_RSR])),
                    int(float(cells[MREG_VERIFIED])),
                    int(float(cells[MREG_UNVERIFIED])),
                    float(cells[MREG_TIME]),
                )
            except ValueError:
                pass
            continue
        if first.isdigit():
            num = int(first)
            try:
                out[num] = (
                    int(float(cells[MREG_RSR])),
                    int(float(cells[MREG_VERIFIED])),
                    int(float(cells[MREG_UNVERIFIED])),
                    float(cells[MREG_TIME]),
                )
            except ValueError:
                pass
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--res_dir", required=True)
    ap.add_argument("--canonical", default=None, help="canonical CSV for cross-check")
    ap.add_argument("--out", default=None, help="summary csv path (default <res_dir>/summary.csv)")
    args = ap.parse_args()

    logs = sorted(
        os.path.join(args.res_dir, f)
        for f in os.listdir(args.res_dir)
        if f.endswith(".txt") and not f.endswith("_trace.txt")
    )
    if not logs:
        print(f"No .txt logs found in {args.res_dir}", file=sys.stderr)
        sys.exit(1)

    rows = [parse_log(p) for p in logs]
    out_csv = args.out or os.path.join(args.res_dir, "summary.csv")
    fields = ["test_id", "number", "started", "eqs_found", "verified",
              "unverified", "faulty", "unknown", "took_time_s", "has_rsr"]
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    n_started = sum(r["started"] for r in rows)
    tot_verified = sum(r["verified"] for r in rows)
    tot_unverified = sum(r["unverified"] for r in rows)
    tot_faulty = sum(r["faulty"] for r in rows)
    covered = sum(r["has_rsr"] for r in rows)
    times = [r["took_time_s"] for r in rows if r["took_time_s"] > 0]
    avg_time = sum(times) / len(times) if times else 0.0

    print("=" * 64)
    print(f"V-Bitwen-LR summary  ({n} logs in {args.res_dir})")
    print("=" * 64)
    print(f"  functions started (no crash) : {n_started}/{n}")
    print(f"  functions with >=1 verified   : {covered}/{n}  ({100*covered/n:.1f}% coverage)")
    print(f"  total verified identities     : {tot_verified}")
    print(f"  total unverified candidates   : {tot_unverified}")
    print(f"  total faulty (verify errors)  : {tot_faulty}")
    print(f"  avg took_time                 : {avg_time:.2f}s")
    print(f"  wrote {out_csv}")
    print()

    if args.canonical and os.path.exists(args.canonical):
        can = parse_canonical_mreg(args.canonical)
        agg = can.get("agg")
        can_funcs = {k: v for k, v in can.items() if isinstance(k, int)}
        can_covered = sum(1 for v in can_funcs.values() if v[1] > 0)
        print("-" * 64)
        print("Cross-check vs canonical mreg (vanilla Bitween)")
        print("-" * 64)
        if agg:
            print(f"  {'metric':32s} {'ours':>10s} {'canonical':>10s}")
            print(f"  {'verified identities':32s} {tot_verified:>10d} {agg[1]:>10d}")
            print(f"  {'unverified candidates':32s} {tot_unverified:>10d} {agg[2]:>10d}")
            print(f"  {'functions covered (verified>0)':32s} {covered:>10d} {can_covered:>10d}")
            print(f"  {'coverage %':32s} {100*covered/n:>9.1f}% {100*can_covered/len(can_funcs):>9.1f}%")
            print(f"  {'avg time (s)':32s} {avg_time:>10.2f} {agg[3]:>10.2f}")
        # sigmoid specifically
        for num, (rsr, ver, unver, t) in can_funcs.items():
            if num == 33:
                print(f"  canonical #33 (sigmoid): rsr={rsr}, verified={ver}")


if __name__ == "__main__":
    main()
