#!/usr/bin/env python3
"""Claim 3 comparison: A-Bitwen (agentic) vs Neural-Research baseline.

Parses the per-function logs each condition wrote and compares:
  - RSR coverage  (functions with >=1 verified identity)
  - total verified identities
  - verification accuracy (verified / candidate identities)
  - token cost (if the agentic harness logged it)

Both conditions must use the SAME model + budget (run_agentic.sh / run_neural.sh
against the same vLLM endpoint). NOTE: the exact agentic log/token schema is
confirmed on the first Colab run; this parser is intentionally tolerant and
counts `Verified (n)` headers, falling back to `proved: True` lines.
"""
import argparse
import os
import re

_RE_VER_HDR = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
_RE_PROVED = re.compile(r"proved: True", re.IGNORECASE)
_RE_UNVER_HDR = re.compile(r"^Unverified \((\d+)\):", re.MULTILINE)
_RE_TOKENS = re.compile(r"tokens[:=]\s*([\d.eE]+)", re.IGNORECASE)


def summarize(res_dir: str) -> dict:
    files = sorted(f for f in os.listdir(res_dir) if f.endswith(".txt") and not f.endswith("_trace.txt"))
    n_funcs = len(files)
    covered = 0
    tot_verified = 0
    tot_unverified = 0
    tot_tokens = 0
    for f in files:
        with open(os.path.join(res_dir, f), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        v = _grab(_RE_VER_HDR, text)
        u = _grab(_RE_UNVER_HDR, text)
        if v == 0 and "proved: True" in text:
            v = text.count("proved: True")
        tot_verified += v
        tot_unverified += u
        if v > 0:
            covered += 1
        m = _RE_TOKENS.search(text)
        if m:
            try:
                tot_tokens += int(float(m.group(1)))
            except ValueError:
                pass
    candidates = tot_verified + tot_unverified
    return dict(
        funcs=n_funcs,
        covered=covered,
        coverage_pct=100 * covered / n_funcs if n_funcs else 0.0,
        verified=tot_verified,
        unverified=tot_unverified,
        ver_accuracy=(tot_verified / candidates) if candidates else 0.0,
        tokens=tot_tokens,
    )


def _grab(regex, text):
    m = regex.search(text)
    return int(m.group(1)) if m else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agentic", required=True, help="A-Bitwen res_dir")
    ap.add_argument("--neural", required=True, help="neural baseline res_dir")
    args = ap.parse_args()

    a = summarize(args.agentic)
    n = summarize(args.neural)
    print("=" * 70)
    print("Claim 3: Agentic Bitwen vs Neural-Research baseline")
    print("=" * 70)
    print(f"{'metric':34s} {'A-Bitwen':>14s} {'Neural':>14s}")
    print("-" * 70)
    for key, label, fmt in [
        ("funcs", "functions attempted", "{:>14d}"),
        ("covered", "functions with >=1 RSR", "{:>14d}"),
        ("coverage_pct", "RSR coverage %", "{:>13.1f}%"),
        ("verified", "total verified identities", "{:>14d}"),
        ("unverified", "total unverified candidates", "{:>14d}"),
        ("ver_accuracy", "verification accuracy", "{:>13.1%}"),
        ("tokens", "total tokens", "{:>14d}"),
    ]:
        print(f"  {label:32s} {fmt.format(a[key])} {fmt.format(n[key])}")
    print("-" * 70)
    verdict = "AGENTIC >= NEURAL on discovery AND verification" if (
        a["covered"] >= n["covered"] and a["ver_accuracy"] >= n["ver_accuracy"]) else "MIXED/see numbers"
    print(f"Claim 3 outcome: {verdict}")


if __name__ == "__main__":
    main()
