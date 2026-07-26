#!/usr/bin/env python3
"""Extract evaluator-visible per-function rows from an immutable orx run log."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


BLOCK = re.compile(
    r"^Starting (?P<id>\d\d_[A-Za-z0-9_]+)\n(?P<body>.*?)^Ending (?P=id)$",
    re.MULTILINE | re.DOTALL,
)
RE_VERIFIED = re.compile(r"^Verified \((\d+)\):", re.MULTILINE)
RE_FAULTY = re.compile(r"^Faulty \((\d+)\):", re.MULTILINE)
RE_TIME = re.compile(r"Took time:\s*([\d.]+)s")
RE_SAMPLE = re.compile(r"Sample Complexity:\s*([\d.]+)")


def stage(text: str, label: str) -> str:
    marker = f"### STAGE {label}"
    start = text.index(marker)
    next_stage = text.find("\n### STAGE ", start + len(marker))
    return text[start:] if next_stage < 0 else text[start:next_stage]


def last(pattern: re.Pattern, text: str, cast, default):
    values = pattern.findall(text)
    return cast(values[-1]) if values else default


def parse_stage(text: str, label: str) -> list[dict]:
    rows = []
    for match in BLOCK.finditer(stage(text, label)):
        body = match.group("body")
        rows.append(
            {
                "id": match.group("id"),
                "number": int(match.group("id").split("_", 1)[0]),
                "verified": last(RE_VERIFIED, body, int, 0),
                "faulty": last(RE_FAULTY, body, int, 0),
                "time_s": last(RE_TIME, body, float, 0.0),
                "sample_complexity": last(RE_SAMPLE, body, float, None),
            }
        )
    assert len(rows) == 80, f"{label}: expected 80 rows, observed {len(rows)}"
    assert [row["number"] for row in rows] == list(range(1, 81))
    return rows


def summary(rows: list[dict]) -> dict:
    samples = [row["sample_complexity"] for row in rows if row["sample_complexity"] is not None]
    return {
        "functions": len(rows),
        "coverage": sum(row["verified"] > 0 for row in rows),
        "verified_identities": sum(row["verified"] for row in rows),
        "faulty": sum(row["faulty"] for row in rows),
        "mean_time_s": sum(row["time_s"] for row in rows) / len(rows),
        "total_time_s": sum(row["time_s"] for row in rows),
        "sample_complexity_observed_functions": len(samples),
        "mean_reported_sample_complexity": sum(samples) / len(samples),
        "total_reported_sample_complexity": sum(samples),
    }


def close(left: float, right: float) -> bool:
    return abs(left - right) <= 1e-9 * max(1.0, abs(left), abs(right))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--solver", required=True)
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    text = args.log.read_text(encoding="utf-8", errors="replace")
    lr_rows = parse_stage(text, "claim-3-vanilla-full-80")
    milp_rows = parse_stage(text, f"claim-5-fresh-full-80-milp-{args.solver}")
    expected = json.loads(args.aggregate.read_text())
    reconstructed = {"lr": summary(lr_rows), "milp": summary(milp_rows)}
    for backend in ("lr", "milp"):
        for key, value in expected[backend].items():
            observed = reconstructed[backend][key]
            if isinstance(value, float):
                assert close(observed, value), (backend, key, observed, value)
            else:
                assert observed == value, (backend, key, observed, value)

    paired_rows = [
        {"id": lr["id"], "lr": lr, "milp": milp}
        for lr, milp in zip(lr_rows, milp_rows)
    ]
    result = {
        "schema_version": 1,
        "source": "immutable orx run log",
        "source_log_sha256": hashlib.sha256(args.log.read_bytes()).hexdigest(),
        "solver": args.solver,
        "row_count": len(paired_rows),
        "rows": paired_rows,
        "reconstructed_aggregate": reconstructed,
        "aggregate_cross_check": "PASS",
        "verdict": "PASS",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "rows"}, indent=2))


if __name__ == "__main__":
    main()
