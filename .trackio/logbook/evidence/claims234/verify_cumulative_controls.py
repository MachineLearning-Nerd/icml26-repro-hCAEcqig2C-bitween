#!/usr/bin/env python3
"""Mutation controls for the exact-domain cumulative verifier."""

from __future__ import annotations

import json
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent))
from verify_cumulative import require_exact_domain  # noqa: E402


def must_reject(rows: list[dict], label: str) -> dict:
    try:
        require_exact_domain(rows, label)
    except AssertionError as error:
        return {
            "label": label,
            "expected": "REJECT",
            "observed": "REJECT",
            "reason": str(error),
        }
    raise AssertionError(f"{label} mutation unexpectedly passed")


def main() -> None:
    exact = [{"number": number} for number in range(1, 81)]
    require_exact_domain(exact, "complete-domain-positive-control")
    results = [
        must_reject(exact[:-1], "truncate-to-79"),
        must_reject(exact[:-1] + [{"number": 79}], "duplicate-79-omit-80"),
    ]
    output = {
        "schema_version": 1,
        "positive_control": {
            "label": "complete IDs 01..80",
            "observed": "PASS",
        },
        "negative_controls": results,
        "verdict": "PASS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
