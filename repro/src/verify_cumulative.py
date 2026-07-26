#!/usr/bin/env python3
"""Strict cumulative verifier for the claims already accepted by the judge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from aggregate import parse_log  # noqa: E402
from verify_independent import (  # noqa: E402
    REGISTRY,
    false_positive_controls,
    numeric_falsify,
    parse_verified_eqs,
)


ROOT = Path(__file__).resolve().parents[2]


def rows(directory: Path) -> list[dict]:
    return [parse_log(str(path)) for path in sorted(directory.glob("[0-9][0-9]_*.txt"))]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vanilla-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    vanilla = rows(args.vanilla_dir)
    numbers = sorted(row["number"] for row in vanilla)
    require(len(vanilla) == 80, f"Claim 2 requires 80 logs, observed {len(vanilla)}")
    require(numbers == list(range(1, 81)), "Claim 2 IDs must span 01 through 80")
    require(all(row["started"] for row in vanilla), "every Vanilla function must start")
    vanilla_covered = sum(row["has_rsr"] for row in vanilla)
    vanilla_verified = sum(row["verified"] for row in vanilla)
    vanilla_faulty = sum(row["faulty"] for row in vanilla)
    require(vanilla_covered >= 39, f"Vanilla coverage below accepted range: {vanilla_covered}")
    require(vanilla_verified >= 87, f"verified identities below canonical 87: {vanilla_verified}")
    require(vanilla_faulty == 0, f"fresh Vanilla run has {vanilla_faulty} faulty identities")

    sigmoid_path = args.vanilla_dir / "33_sigmoid.txt"
    sigmoid_eqs = parse_verified_eqs(str(sigmoid_path))
    require(sigmoid_eqs, "fresh run did not verify a sigmoid identity")
    np.random.seed(0)
    sigmoid_checks = [
        numeric_falsify(
            equation,
            REGISTRY["33_sigmoid"]["nf"],
            REGISTRY["33_sigmoid"]["sampler"],
            n=20_000,
            eps=1e-3,
        )
        for equation in sigmoid_eqs
    ]
    require(all(result[0] for result in sigmoid_checks), "numeric sigmoid checker rejected an identity")

    agentic = rows(ROOT / "outputs" / "abitween-gptoss")
    require(len(agentic) == 80, f"Agentic evidence requires 80 logs, observed {len(agentic)}")
    agentic_covered = sum(row["has_rsr"] for row in agentic)
    agentic_verified = sum(row["verified"] for row in agentic)
    agentic_faulty = sum(row["faulty"] for row in agentic)
    require(agentic_covered >= 64, f"Agentic coverage below paper claim: {agentic_covered}")
    require(agentic_verified >= 320, f"Agentic verified total regressed: {agentic_verified}")
    require(agentic_faulty == 0, f"Agentic evidence has {agentic_faulty} faulty identities")

    np.random.seed(0)
    controls = []
    for label, numeric_function, sampler, lhs in false_positive_controls():
        accepted, max_residual, valid = numeric_falsify(
            lhs, numeric_function, sampler, n=20_000, eps=1e-3
        )
        controls.append(
            {
                "label": label,
                "expected": "REJECT",
                "observed": "ACCEPT" if accepted else "REJECT",
                "max_abs_residual": max_residual,
                "valid_samples": valid,
            }
        )
    require(all(item["observed"] == "REJECT" for item in controls), "a false control passed")

    result = {
        "schema_version": 1,
        "claim2": {"function_count": 80, "id_span": [1, 80], "verdict": "VERIFIED"},
        "claim3": {
            "fresh_coverage": vanilla_covered,
            "fresh_verified_identities": vanilla_verified,
            "fresh_faulty": vanilla_faulty,
            "sigmoid_verified_identities": len(sigmoid_eqs),
            "sigmoid_max_abs_residuals": [item[1] for item in sigmoid_checks],
            "verdict": "VERIFIED",
        },
        "claim4": {
            "function_count": len(agentic),
            "coverage": agentic_covered,
            "verified_identities": agentic_verified,
            "faulty": agentic_faulty,
            "verdict": "VERIFIED",
        },
        "negative_controls": controls,
        "verdict": "PASS",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print("CUMULATIVE_VERDICT=PASS", flush=True)


if __name__ == "__main__":
    main()
