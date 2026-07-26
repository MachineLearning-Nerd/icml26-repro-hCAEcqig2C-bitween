#!/usr/bin/env python3
"""Strict paired comparison of fresh LR and MILP full-80 runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


RE_VERIFIED = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
RE_FAULTY = re.compile(r"^Faulty \((\d+)\):", re.MULTILINE)
RE_TIME = re.compile(r"Took time:\s*([\d.]+)s")
RE_SAMPLE = re.compile(r"Sample Complexity:\s*([\d.]+)")


def last(regex: re.Pattern, text: str, cast, default=0):
    values = regex.findall(text)
    return cast(values[-1]) if values else default


def parse(directory: Path) -> list[dict]:
    result = []
    for path in sorted(directory.glob("[0-9][0-9]_*.txt")):
        text = path.read_text(encoding="utf-8", errors="replace")
        result.append(
            {
                "id": path.stem,
                "number": int(path.stem.split("_", 1)[0]),
                "verified": last(RE_VERIFIED, text, int),
                "faulty": last(RE_FAULTY, text, int),
                "time_s": last(RE_TIME, text, float),
                "sample_complexity": last(RE_SAMPLE, text, float, None),
            }
        )
    if len(result) != 80 or [row["number"] for row in result] != list(range(1, 81)):
        raise AssertionError(f"backend comparison requires exact IDs 1..80, observed {len(result)}")
    return result


def summarize(rows: list[dict]) -> dict:
    times = [row["time_s"] for row in rows]
    samples = [row["sample_complexity"] for row in rows if row["sample_complexity"] is not None]
    return {
        "functions": len(rows),
        "coverage": sum(row["verified"] > 0 for row in rows),
        "verified_identities": sum(row["verified"] for row in rows),
        "faulty": sum(row["faulty"] for row in rows),
        "mean_time_s": sum(times) / len(times),
        "total_time_s": sum(times),
        "sample_complexity_observed_functions": len(samples),
        "mean_reported_sample_complexity": sum(samples) / len(samples) if samples else None,
        "total_reported_sample_complexity": sum(samples) if samples else None,
    }


def v5_contract(lr: dict, milp: dict) -> bool:
    return (
        lr["verified_identities"] > milp["verified_identities"]
        and lr["coverage"] > milp["coverage"]
        and lr["mean_time_s"] < milp["mean_time_s"]
        and lr["faulty"] == 0
        and milp["faulty"] == 0
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lr-dir", type=Path, required=True)
    parser.add_argument("--milp-dir", type=Path, required=True)
    parser.add_argument("--solver", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    lr_rows = parse(args.lr_dir)
    milp_rows = parse(args.milp_dir)
    if [row["id"] for row in lr_rows] != [row["id"] for row in milp_rows]:
        raise AssertionError("paired function IDs differ")
    lr = summarize(lr_rows)
    milp = summarize(milp_rows)
    current_pass = v5_contract(lr, milp)
    if not current_pass:
        raise AssertionError(f"fresh v5 directional contract failed: LR={lr}, MILP={milp}")
    if v5_contract(milp, lr):
        raise AssertionError("label-swap negative control unexpectedly passed")

    paired = {
        "lr_more_verified": sum(a["verified"] > b["verified"] for a, b in zip(lr_rows, milp_rows)),
        "equal_verified": sum(a["verified"] == b["verified"] for a, b in zip(lr_rows, milp_rows)),
        "milp_more_verified": sum(a["verified"] < b["verified"] for a, b in zip(lr_rows, milp_rows)),
        "lr_faster": sum(a["time_s"] < b["time_s"] for a, b in zip(lr_rows, milp_rows)),
        "equal_time": sum(a["time_s"] == b["time_s"] for a, b in zip(lr_rows, milp_rows)),
        "milp_faster": sum(a["time_s"] > b["time_s"] for a, b in zip(lr_rows, milp_rows)),
    }
    result = {
        "schema_version": 1,
        "solver": args.solver,
        "scope": "fresh paired full 80-function RSR-Bench",
        "lr": lr,
        "milp": milp,
        "paired_direction": paired,
        "v5_exact_directional_contract": "PASS",
        "negative_control": {"mutation": "swap LR/MILP labels", "observed": "REJECT"},
        "legacy_sample_metric_limitation": "current v5 harness reports a derived average sample-complexity value, not the v1 used/budget table field",
        "verdict": "VERIFIED",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print(f"BACKEND_COMPARISON_{args.solver.upper()}_VERDICT=VERIFIED", flush=True)


if __name__ == "__main__":
    main()
