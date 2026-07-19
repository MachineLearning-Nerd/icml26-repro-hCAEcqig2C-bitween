#!/usr/bin/env python3
"""Audit Claim 3 using pre-existing, paired full-scale Bitwen runs.

The paper's Claim 3 is conjunctive: Agentic Bitwen must beat the pure-neural
baseline on both discovery and verification accuracy.  This audit deliberately
uses the primary per-seed estimator (one result per complete 80-function run),
not a best-of-seeds union.  A union is useful for exploration, but it is not an
independent paired comparison and can hide the direction of a run-level result.

The input directories are the runs already recorded in the logbook.  No model
calls are made here.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import Iterable


_VERIFIED = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
_UNVERIFIED = re.compile(r"^Unverified \((\d+)\):", re.MULTILINE)


def _identity_counts(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    verified_match = _VERIFIED.search(text)
    unverified_match = _UNVERIFIED.search(text)
    verified = int(verified_match.group(1)) if verified_match else 0
    unverified = int(unverified_match.group(1)) if unverified_match else 0
    if verified == 0:
        verified = text.count("proved: True")
    return verified, unverified


def _files(directory: str) -> dict[str, tuple[int, int]]:
    root = Path(directory)
    if not root.is_dir():
        raise FileNotFoundError(root)
    result = {}
    for path in sorted(root.glob("*.txt")):
        if path.name.endswith("_trace.txt"):
            continue
        result[path.stem] = _identity_counts(path)
    return result


def summarize(directory: str) -> dict:
    counts = _files(directory)
    verified = sum(v for v, _ in counts.values())
    unverified = sum(u for _, u in counts.values())
    candidates = verified + unverified
    return {
        "directory": directory,
        "functions": len(counts),
        "covered": sum(v > 0 for v, _ in counts.values()),
        "verified": verified,
        "unverified": unverified,
        "verification_accuracy": verified / candidates if candidates else 0.0,
        "covered_ids": sorted(k for k, (v, _) in counts.items() if v > 0),
    }


def _paired(a_dir: str, n_dir: str) -> dict:
    a = _files(a_dir)
    n = _files(n_dir)
    if set(a) != set(n):
        raise AssertionError(
            f"paired runs have different function IDs: "
            f"agentic-only={sorted(set(a)-set(n))}, "
            f"neural-only={sorted(set(n)-set(a))}"
        )
    a_covered = {k for k, (v, _) in a.items() if v > 0}
    n_covered = {k for k, (v, _) in n.items() if v > 0}
    return {
        "agentic": summarize(a_dir),
        "neural": summarize(n_dir),
        "agentic_only": sorted(a_covered - n_covered),
        "neural_only": sorted(n_covered - a_covered),
        "discovery_direction": (
            "neural_ahead" if len(a_covered) < len(n_covered)
            else "agentic_ahead" if len(a_covered) > len(n_covered)
            else "tie"
        ),
    }


def _exact_mcnemar(discordant_agentic: int, discordant_neural: int) -> float:
    """Two-sided exact sign-test p-value for paired coverage outcomes."""
    total = discordant_agentic + discordant_neural
    if total == 0:
        return 1.0
    tail = sum(math.comb(total, k) for k in range(min(discordant_agentic, discordant_neural) + 1))
    return min(1.0, 2.0 * tail / (2.0**total))


def audit(agentic_dirs: Iterable[str], neural_dirs: Iterable[str]) -> dict:
    agentic_dirs = list(agentic_dirs)
    neural_dirs = list(neural_dirs)
    if len(agentic_dirs) != len(neural_dirs) or not agentic_dirs:
        raise ValueError("provide the same positive number of agentic and neural directories")
    pairs = [_paired(a, n) for a, n in zip(agentic_dirs, neural_dirs)]
    for pair in pairs:
        if pair["agentic"]["functions"] != 80 or pair["neural"]["functions"] != 80:
            raise AssertionError("Claim 3 audit requires complete 80-function runs")

    all_a = [x for pair in pairs for x in _files(pair["agentic"]["directory"])]
    all_n = [x for pair in pairs for x in _files(pair["neural"]["directory"])]
    discordant_agentic = 0
    discordant_neural = 0
    for a_dir, n_dir in zip(agentic_dirs, neural_dirs):
        a = _files(a_dir)
        n = _files(n_dir)
        for key in a:
            av = a[key][0] > 0
            nv = n[key][0] > 0
            discordant_agentic += int(av and not nv)
            discordant_neural += int(nv and not av)

    pooled_a_verified = sum(_files(d)[k][0] for d in agentic_dirs for k in _files(d))
    pooled_a_unverified = sum(_files(d)[k][1] for d in agentic_dirs for k in _files(d))
    pooled_n_verified = sum(_files(d)[k][0] for d in neural_dirs for k in _files(d))
    pooled_n_unverified = sum(_files(d)[k][1] for d in neural_dirs for k in _files(d))
    pooled_a_candidates = pooled_a_verified + pooled_a_unverified
    pooled_n_candidates = pooled_n_verified + pooled_n_unverified

    mean_a_coverage = sum(p["agentic"]["covered"] for p in pairs) / len(pairs)
    mean_n_coverage = sum(p["neural"]["covered"] for p in pairs) / len(pairs)
    mean_a_accuracy = sum(p["agentic"]["verification_accuracy"] for p in pairs) / len(pairs)
    mean_n_accuracy = sum(p["neural"]["verification_accuracy"] for p in pairs) / len(pairs)

    # The exact model row in the paper's aggregate table is retained as a
    # corroborating source audit, not silently mixed into the local counts.
    paper_gptoss = {
        "agentic_rsr_coverage_pct": 59,
        "neural_rsr_coverage_pct": 62,
        "source": "arXiv 2412.18134v5, sections/table_aggregate_results.tex",
    }
    return {
        "scope": "three paired full-scale runs, 80 functions each",
        "pairs": pairs,
        "mean_covered": {"agentic": mean_a_coverage, "neural": mean_n_coverage},
        "mean_verification_accuracy": {"agentic": mean_a_accuracy, "neural": mean_n_accuracy},
        "pooled": {
            "agentic": {
                "verified": pooled_a_verified,
                "unverified": pooled_a_unverified,
                "verification_accuracy": pooled_a_verified / pooled_a_candidates,
            },
            "neural": {
                "verified": pooled_n_verified,
                "unverified": pooled_n_unverified,
                "verification_accuracy": pooled_n_verified / pooled_n_candidates,
            },
        },
        "paired_coverage": {
            "agentic_only": discordant_agentic,
            "neural_only": discordant_neural,
            "exact_mcnemar_p_two_sided": _exact_mcnemar(discordant_agentic, discordant_neural),
        },
        "claim3_result": (
            "not_reproduced_in_this_full_scale_open_model_reproduction"
            if all(p["discovery_direction"] == "neural_ahead" for p in pairs)
            else "mixed_or_not_falsified"
        ),
        "paper_gptoss_row": paper_gptoss,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agentic", required=True, help="comma-separated run directories")
    parser.add_argument("--neural", required=True, help="comma-separated paired run directories")
    parser.add_argument("--out", help="optional JSON output path")
    args = parser.parse_args()
    result = audit(
        [x.strip() for x in args.agentic.split(",") if x.strip()],
        [x.strip() for x in args.neural.split(",") if x.strip()],
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
