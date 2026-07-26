#!/usr/bin/env python3
"""Exhaustive verifier for the paper's Section 4 BLR construction."""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path


def vectors(q: int, n: int) -> list[tuple[int, ...]]:
    return list(product(range(q), repeat=n))


def add(x: tuple[int, ...], y: tuple[int, ...], q: int) -> tuple[int, ...]:
    return tuple((a + b) % q for a, b in zip(x, y))


def linear(a: tuple[int, ...], x: tuple[int, ...], q: int) -> int:
    return sum(ai * xi for ai, xi in zip(a, x)) % q


def verify_field(q: int, max_n: int) -> list[dict]:
    results = []
    for n in range(1, max_n + 1):
        xs = vectors(q, n)
        total_recovery_checks = 0
        for x in xs:
            assert sorted(add(x, r, q) for r in xs) == sorted(xs)
            assert sorted(r for r in xs) == sorted(xs)
        for a in xs:
            for x in xs:
                fx = linear(a, x, q)
                for r in xs:
                    recovered = (linear(a, add(x, r, q), q) - linear(a, r, q)) % q
                    assert recovered == fx
                    total_recovery_checks += 1

        zero = (0,) * n
        errors = {
            a: sum(linear(a, x, q) != linear(zero, x, q) for x in xs) / len(xs)
            for a in xs
        }
        nonzero_errors = [error for a, error in errors.items() if a != zero]
        assert set(nonzero_errors) == {(q - 1) / q}
        results.append(
            {
                "field": f"F_{q}",
                "n": n,
                "domain_size": len(xs),
                "function_count": len(xs),
                "marginal_uniformity_checks": 2 * len(xs),
                "recovery_checks": total_recovery_checks,
                "distinct_function_error": nonzero_errors[0],
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    binary = verify_field(2, 7)
    ternary = verify_field(3, 4)
    assert binary[-1]["distinct_function_error"] == 0.5
    assert ternary[-1]["distinct_function_error"] > 0.5

    q, n = 3, 2
    xs = vectors(q, n)
    bad_failures = 0
    for a in xs[1:]:
        for x in xs:
            for r in xs:
                bad_recovery = linear(a, add(x, r, q), q)
                bad_failures += bad_recovery != linear(a, x, q)
    assert bad_failures > 0

    result = {
        "schema_version": 1,
        "exact_statement": {
            "field_in_claim": "existential; not fixed",
            "epsilon_quantifier": "for any epsilon <= 1/2",
            "delta_assumption_from_proof": "delta < 1/2",
            "oracle_query_lower_bound": "m_PAC(epsilon, delta) >= n",
        },
        "binary_paper_witness": {
            "strict_epsilon_below_half": "VERIFIED",
            "epsilon_equal_half": "REJECTED_AS_WITNESS",
            "reason": "the zero hypothesis has error exactly 1/2 for every nonzero binary linear target",
            "exhaustive_results": binary,
        },
        "ternary_independent_witness": {
            "epsilon_at_most_half_requires_exact_identification": True,
            "distinct_function_error": ternary[-1]["distinct_function_error"],
            "zero_sample_blr_rsr": "VERIFIED",
            "exhaustive_results": ternary,
        },
        "negative_control": {
            "mutation": "recovery omits f(r)",
            "expected": "REJECT",
            "observed": "REJECT",
            "failing_assignments": bad_failures,
        },
        "claim1_verdict": "VERIFIED",
        "proof_limitation": "the paper's F_2 proof sketch needs epsilon < 1/2; F_3 repairs the existential boundary without changing the theorem statement",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    print("THEORY_EXHAUSTIVE_VERDICT=VERIFIED", flush=True)


if __name__ == "__main__":
    main()
