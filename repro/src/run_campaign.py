#!/usr/bin/env python3
"""Fixed OpenResearch entrypoint for the cumulative reproduction campaign.

The command invoking this file is inherited unchanged by every experiment node.
Variants live in committed code and ``repro/configs/campaign.json``.  The
baseline regenerates the full Vanilla Bitween result and rechecks the committed
full-scale agentic evidence and all negative controls.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "repro" / "configs" / "campaign.json"
ARTIFACT_ROOT = ROOT / ".openresearch" / "artifacts"


def run(command: list[str], *, label: str) -> float:
    """Run one strict stage, printing its exact argv and elapsed time."""
    started = time.perf_counter()
    print(f"\n### STAGE {label}", flush=True)
    print("COMMAND_JSON=" + json.dumps(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)
    elapsed = time.perf_counter() - started
    print(f"STAGE_RUNTIME_SECONDS={elapsed:.6f}", flush=True)
    return elapsed


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def print_environment(config: dict) -> None:
    print("=== REPRODUCTION CONTRACT ===", flush=True)
    print(f"GIT_SHA={git_sha()}", flush=True)
    print(f"CAMPAIGN_STAGE={config['campaign_stage']}", flush=True)
    print(f"PYTHON={sys.version.split()[0]}", flush=True)
    print(f"PLATFORM={platform.platform()}", flush=True)
    print(f"ACTUAL_LOGICAL_CPU_ALLOCATION={os.cpu_count()}", flush=True)
    print(f"ALLOCATED_VCPU_FROM_FLAVOR={config['selected_vcpus']}", flush=True)
    print(f"ALLOCATED_MEMORY_GB_FROM_FLAVOR={config['selected_memory_gb']}", flush=True)
    print(f"ESTIMATED_CPU_CORES={config['estimated_cpu_cores']}", flush=True)
    print(
        f"ESTIMATED_RUNTIME_MINUTES={config['estimated_runtime_minutes']}",
        flush=True,
    )
    print(f"SELECTED_BACKEND={config['required_backend']}", flush=True)
    print(f"SELECTED_FLAVOR={config['required_flavor']}", flush=True)
    print(f"CONFIG_JSON={json.dumps(config, sort_keys=True)}", flush=True)


def baseline(config: dict) -> None:
    python = str(ROOT / ".venv" / "bin" / "python")
    vanilla_dir = ARTIFACT_ROOT / "baseline" / "vanilla_seed42"
    vanilla_dir.mkdir(parents=True, exist_ok=True)

    runtimes: dict[str, float] = {}
    runtimes["tests"] = run(
        [python, "-m", "pytest", "-q", "repro/tests"],
        label="unit-and-negative-control-tests",
    )
    runtimes["vanilla_full80"] = run(
        [
            python,
            "repro/src/run_vanilla.py",
            "--seed",
            str(config["vanilla_seed"]),
            "--res_dir",
            str(vanilla_dir),
            "--timeout_sec",
            str(config["vanilla_timeout_seconds_per_function"]),
        ],
        label="claim-3-vanilla-full-80",
    )
    runtimes["vanilla_aggregate"] = run(
        [
            python,
            "repro/src/aggregate.py",
            "--res_dir",
            str(vanilla_dir),
            "--canonical",
            "upstream/results/Bitween-Results(Sheet1-ICML).csv",
        ],
        label="claims-2-and-3-benchmark-and-vanilla-aggregate",
    )
    runtimes["vanilla_independent"] = run(
        [
            python,
            "repro/src/verify_independent.py",
            "--res_dir",
            str(vanilla_dir),
            "--n",
            str(config["numeric_falsifier_samples"]),
        ],
        label="claim-3-independent-checker-and-controls",
    )
    runtimes["agentic_seed1"] = run(
        [
            python,
            "repro/src/aggregate.py",
            "--res_dir",
            "outputs/abitween-gptoss",
        ],
        label="claim-4-agentic-full-80-raw-evidence-regression",
    )
    runtimes["claim3_paired_audit"] = run(
        [
            python,
            "repro/src/claim3_falsification.py",
            "--agentic",
            "outputs/abitween-gptoss,outputs/abitween-gptoss-s2,outputs/abitween-gptoss-s3",
            "--neural",
            "outputs/neural-gptoss,outputs/neural-gptoss-s2,outputs/neural-gptoss-s3",
        ],
        label="historical-agentic-vs-neural-control-audit",
    )

    summary = {
        "schema_version": 1,
        "git_sha": git_sha(),
        "config": config,
        "actual_logical_cpu_allocation": os.cpu_count(),
        "runtime_seconds_by_stage": runtimes,
        "total_runtime_seconds": sum(runtimes.values()),
    }
    summary_path = ARTIFACT_ROOT / "baseline" / "runtime_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("\n=== BASELINE_RUNTIME_SUMMARY ===", flush=True)
    print(json.dumps(summary, indent=2), flush=True)
    print("BASELINE_VERDICT=PASS", flush=True)


def theory(config: dict) -> None:
    baseline(config)
    python = str(ROOT / ".venv" / "bin" / "python")
    theory_dir = ARTIFACT_ROOT / "claim1_theory"
    theory_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            python,
            "repro/src/verify_cumulative.py",
            "--vanilla-dir",
            str(ARTIFACT_ROOT / "baseline" / "vanilla_seed42"),
            "--out",
            str(ARTIFACT_ROOT / "cumulative_verdict.json"),
        ],
        label="strict-cumulative-claims-2-through-4-verifier",
    )
    run(
        [
            python,
            "repro/src/verify_theory.py",
            "--out",
            str(theory_dir / "theory_verifier_output.json"),
        ],
        label="claim-1-exhaustive-theory-verifier",
    )
    run(
        [
            python,
            "repro/src/verify_theory_independent.py",
            "--out",
            str(theory_dir / "independent_checker_output.json"),
        ],
        label="claim-1-independent-linear-algebra-checker",
    )
    print("THEORY_CLAIM_VERDICT=VERIFIED", flush=True)


def main() -> None:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    print_environment(config)
    if config["campaign_stage"] == "baseline":
        baseline(config)
        return
    if config["campaign_stage"] == "theory":
        theory(config)
        return
    raise SystemExit(f"Unsupported campaign stage: {config['campaign_stage']}")


if __name__ == "__main__":
    started = time.perf_counter()
    try:
        main()
    finally:
        print(f"TOTAL_ENTRYPOINT_RUNTIME_SECONDS={time.perf_counter() - started:.6f}")
