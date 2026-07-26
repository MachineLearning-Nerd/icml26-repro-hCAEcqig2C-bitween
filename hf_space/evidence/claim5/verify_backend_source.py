#!/usr/bin/env python3
"""Versioned source and complete-table verifier for the backend claim."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V1_TABLE = ROOT / "repro" / "data" / "claim5_v1_table40.csv"
V5_TABLE = ROOT / "upstream" / "results" / "Bitween-Results(Sheet1-ICML).csv"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_v1(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 40, f"v1 Table 1 must contain 40 rows, observed {len(rows)}")
    require([int(row["id"]) for row in rows] == list(range(1, 41)), "v1 IDs must be 1..40")
    return rows


def optional_number(value: str, cast):
    return cast(value) if value else None


def audit_v1(rows: list[dict]) -> dict:
    parsed = [
        {
            **row,
            "milp_used": optional_number(row["milp_used"], int),
            "lr_used": optional_number(row["lr_used"], int),
            "milp_time_s": float(row["milp_time_s"]),
            "lr_time_s": float(row["lr_time_s"]),
        }
        for row in rows
    ]
    comparable = [row for row in parsed if row["milp_used"] is not None]
    result = {
        "row_count": len(parsed),
        "table_sums": {
            "milp_samples": sum(row["milp_used"] for row in comparable),
            "lr_samples": sum(row["lr_used"] for row in comparable),
            "milp_time_s": round(sum(row["milp_time_s"] for row in parsed), 2),
            "lr_time_s": round(sum(row["lr_time_s"] for row in parsed), 2),
        },
        "prose_totals": {
            "milp_samples": 1095,
            "lr_samples": 594,
            "milp_time_s": 187.47,
            "lr_time_s": 130.53,
        },
        "paired_sample_direction": {
            "lr_strictly_fewer": sum(row["lr_used"] < row["milp_used"] for row in comparable),
            "equal": sum(row["lr_used"] == row["milp_used"] for row in comparable),
            "lr_more": sum(row["lr_used"] > row["milp_used"] for row in comparable),
            "missing": len(parsed) - len(comparable),
        },
        "paired_runtime_direction": {
            "lr_faster": sum(row["lr_time_s"] < row["milp_time_s"] for row in parsed),
            "equal": sum(row["lr_time_s"] == row["milp_time_s"] for row in parsed),
            "lr_slower": sum(row["lr_time_s"] > row["milp_time_s"] for row in parsed),
        },
    }
    require(result["table_sums"] == {
        "milp_samples": 1180,
        "lr_samples": 607,
        "milp_time_s": 308.64,
        "lr_time_s": 227.10,
    }, "transcribed complete-table sums changed")
    require(result["paired_sample_direction"] == {
        "lr_strictly_fewer": 29, "equal": 10, "lr_more": 0, "missing": 1
    }, "v1 paired sample direction changed")
    require(result["paired_runtime_direction"] == {
        "lr_faster": 11, "equal": 0, "lr_slower": 29
    }, "v1 paired runtime direction changed")
    return result


def audit_v5(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        rows = list(csv.reader(handle))
    data_rows = [
        row
        for row in rows
        if row
        and row[0].strip().isdigit()
        and 1 <= int(row[0].strip()) <= 80
        and len(row) > 1
        and not row[1].strip().isdigit()
    ]
    require(len(data_rows) == 80, f"v5 canonical table must contain 80 rows: {len(data_rows)}")
    aggregate = next(row for row in rows if row and row[0].strip().startswith("*"))
    aggregate += [""] * 32
    milp = {
        "rsr": int(float(aggregate[13])),
        "verified": int(float(aggregate[14])),
        "unverified": int(float(aggregate[15])),
        "average_time_s": float(aggregate[16]),
    }
    lr = {
        "rsr": int(float(aggregate[18])),
        "verified": int(float(aggregate[19])),
        "unverified": int(float(aggregate[20])),
        "average_time_s": float(aggregate[21]),
    }
    milp_coverage = sum(int(float((row + [""] * 32)[14] or 0)) > 0 for row in data_rows)
    lr_coverage = sum(int(float((row + [""] * 32)[19] or 0)) > 0 for row in data_rows)
    require(lr["rsr"] > milp["rsr"], "v5 canonical LR RSR total is not higher")
    require(lr_coverage > milp_coverage, "v5 canonical LR coverage is not higher")
    require(lr["average_time_s"] < milp["average_time_s"], "v5 canonical LR is not faster")
    return {
        "row_count": len(data_rows),
        "milp": {**milp, "functions_with_verified_identity": milp_coverage},
        "lr": {**lr, "functions_with_verified_identity": lr_coverage},
        "directional_contract": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = read_v1(V1_TABLE)
    v1 = audit_v1(rows)
    v5 = audit_v5(V5_TABLE)

    controls = []
    try:
        audit_v1(rows[:-1])
    except AssertionError:
        controls.append({"name": "truncate complete v1 domain to 39 rows", "observed": "REJECT"})
    swapped_passes = (
        v5["milp"]["rsr"] > v5["lr"]["rsr"]
        and v5["milp"]["average_time_s"] < v5["lr"]["average_time_s"]
    )
    require(not swapped_passes, "label-swap negative control unexpectedly passed")
    controls.append({"name": "swap LR and MILP labels in v5 directional contract", "observed": "REJECT"})
    require(len(controls) == 2, "both negative controls must reject")

    result = {
        "schema_version": 1,
        "source_versions": {
            "v1": {
                "source_sha256": "c9483e7747bead779af4d5691438feac34e9c38af77cb4fbe4928c90f2f5890c",
                "lr_vs_milp_anchor": "sections/evaluation.tex lines 24-61; Figure 3; Table 1; 40-function RSR-Bench",
                "nla_table_anchor": "sections/evaluation.tex Table 2; Bitween vs DIG vs SymInfer; no MILP column",
            },
            "v5": {
                "source_sha256": "556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f",
                "anchor": "abstract; sections/evaluation.tex and table_aggregate_results.tex; 80-function RSR-Bench",
                "nla_status": "removed from the paper",
            },
        },
        "judge_wording": {
            "text": "On nonlinear invariant benchmarks, the regression backend outperforms the MILP backend in sample count and runtime (Table 2).",
            "source_attribution": "CONFLATES v1 Table 1 LR/MILP RSR-Bench with v1 Table 2 NLA DIG/SymInfer comparison",
        },
        "v1_complete_table_audit": v1,
        "v5_canonical_audit": v5,
        "negative_controls": controls,
        "verdict": "PASS",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print("BACKEND_SOURCE_VERDICT=PASS", flush=True)


if __name__ == "__main__":
    main()
