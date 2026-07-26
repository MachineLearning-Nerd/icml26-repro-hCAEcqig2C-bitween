#!/usr/bin/env python3
"""Generate the four evidence figures used by the final reproduction report."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "five-claim-reproduction" / "images"
GREEN = "#157f5b"
BLUE = "#235789"
ORANGE = "#d97904"
RED = "#b23a48"
GRAY = "#6b7280"


def finish(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def status_figure() -> None:
    claims = [
        "C1  Section 4 theory",
        "C2  80-function benchmark",
        "C3  Vanilla + sigmoid",
        "C4  Agentic coverage",
        "C5  LR vs MILP*",
    ]
    evidence = [3, 3, 3, 3, 2]
    notes = [
        "proof reconstruction + exhaustive checks",
        "exact 80-ID cumulative regression",
        "fresh full-80 + independent falsifier",
        "80 logs, 320 verified, 0 faulty",
        "version-resolved; judge wording conflates tables",
    ]
    fig, ax = plt.subplots(figsize=(10.5, 4.3))
    y = np.arange(len(claims))
    colors = [GREEN, GREEN, GREEN, GREEN, ORANGE]
    ax.barh(y, evidence, color=colors, height=0.58)
    ax.set_yticks(y, claims)
    ax.set_xlim(0, 3.1)
    ax.set_xticks([1, 2, 3], ["partial", "substantial", "direct"])
    ax.invert_yaxis()
    for i, note in enumerate(notes):
        ax.text(0.06, i, note, va="center", ha="left", color="white", fontsize=9, weight="bold")
    ax.set_title("All five claims now have executable evidence; Claim 5 retains source-attribution risk", loc="left", weight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.15)
    fig.text(
        0.02,
        0.015,
        "Status is scientific evidence, not a live judge score. *Version-resolved LR/MILP claim.",
        color=GRAY,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    finish(fig, "01_claim_status.png")


def theory_figure() -> None:
    theory = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "claim1_theory" / "theory_verifier_output.json").read_text()
    )
    f2 = theory["binary_paper_witness"]
    f3 = theory["ternary_independent_witness"]
    f2_error = f2["distinct_function_error"]
    f3_error = f3["distinct_function_error"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw={"width_ratios": [1, 1.45]})
    ax = axes[0]
    ax.bar(["paper witness\n$\\mathbb{F}_2$", "repaired witness\n$\\mathbb{F}_3$"], [f2_error, f3_error], color=[RED, GREEN])
    ax.axhline(0.5, color=GRAY, linestyle="--", label=r"$\epsilon=1/2$")
    ax.set_ylim(0, 0.76)
    ax.set_ylabel("error between distinct linear targets")
    ax.set_title("Boundary check", weight="bold")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    ns = [int(n) for n in f3["recovery_checks_by_n"]]
    recovery = [f3["recovery_checks_by_n"][str(n)] for n in ns]
    ax.bar([str(n) for n in ns], recovery, color=BLUE)
    ax.set_yscale("log")
    ax.set_xlabel("dimension n over $\\mathbb{F}_3$")
    ax.set_ylabel("exhaustive recovery checks (log scale)")
    ax.set_title("Complete finite-domain calibration", weight="bold")
    for i, value in enumerate(recovery):
        ax.text(i, value * 1.15, f"{value:,}", ha="center", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(
        "Claim 1: the paper's binary proof misses ε=1/2; a ternary witness verifies the existential theorem",
        x=0.02,
        ha="left",
        weight="bold",
    )
    fig.tight_layout()
    finish(fig, "02_theory_boundary.png")


def backend_figure() -> None:
    gurobi = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "claim5_backend" / "comparison_gurobi.json").read_text()
    )
    pulp = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "claim5_backend" / "comparison_pulp.json").read_text()
    )
    labels = ["LR\n(Gurobi run)", "Gurobi\nMILP", "LR\n(PuLP run)", "PuLP\nMILP"]
    colors = [BLUE, ORANGE, BLUE, "#9a6700"]
    coverage = [gurobi["lr"]["coverage"], gurobi["milp"]["coverage"], pulp["lr"]["coverage"], pulp["milp"]["coverage"]]
    identities = [
        gurobi["lr"]["verified_identities"],
        gurobi["milp"]["verified_identities"],
        pulp["lr"]["verified_identities"],
        pulp["milp"]["verified_identities"],
    ]
    runtimes = [
        gurobi["lr"]["mean_time_s"],
        gurobi["milp"]["mean_time_s"],
        pulp["lr"]["mean_time_s"],
        pulp["milp"]["mean_time_s"],
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, values, title, ylim in [
        (axes[0], coverage, "Functions covered / 80", 48),
        (axes[1], identities, "Verified identities", 100),
        (axes[2], runtimes, "Mean runtime / function (s)", 20),
    ]:
        bars = ax.bar(labels, values, color=colors)
        ax.set_title(title, weight="bold")
        ax.set_ylim(0, ylim)
        ax.spines[["top", "right"]].set_visible(False)
        ax.bar_label(bars, fmt="%.2f" if title.startswith("Mean") else "%d", padding=2, fontsize=8)
        ax.tick_params(axis="x", labelsize=8)
    fig.suptitle("Claim 5: LR wins the current full-80 identity, coverage, and runtime directions", x=0.02, ha="left", weight="bold")
    fig.tight_layout()
    finish(fig, "03_backend_comparison.png")


def legacy_table_figure() -> None:
    path = ROOT / "repro" / "data" / "claim5_v1_table40.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    sample_rows = [row for row in rows if row["milp_used"]]
    milp_samples = [float(row["milp_used"]) for row in sample_rows]
    lr_samples = [float(row["lr_used"]) for row in sample_rows]
    milp_time = [float(row["milp_time_s"]) for row in rows]
    lr_time = [float(row["lr_time_s"]) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    for ax, x, y, title in [
        (axes[0], milp_samples, lr_samples, "Sample use: 29 lower, 10 equal"),
        (axes[1], milp_time, lr_time, "Runtime: 11 faster, 29 slower"),
    ]:
        ax.scatter(x, y, color=BLUE, alpha=0.78, edgecolor="white", linewidth=0.4)
        bound = max(max(x), max(y)) * 1.04
        ax.plot([0, bound], [0, bound], color=GRAY, linestyle="--", linewidth=1)
        ax.set_xlim(0, bound)
        ax.set_ylim(0, bound)
        ax.set_xlabel("MILP")
        ax.set_ylabel("LR")
        ax.set_title(title, weight="bold")
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(
        "Legacy v1 complete table: aggregate LR sample use and runtime are lower, but row-wise runtime is mixed",
        x=0.02,
        ha="left",
        weight="bold",
    )
    fig.text(
        0.02,
        0.01,
        "Complete-table sums — samples: MILP 1,180 vs LR 607; runtime: MILP 308.64 s vs LR 227.10 s. Published prose totals differ.",
        color=GRAY,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    finish(fig, "04_legacy_table_audit.png")


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titlelocation": "left"})
    status_figure()
    theory_figure()
    backend_figure()
    legacy_table_figure()
    print(f"wrote 4 figures to {OUT}")


if __name__ == "__main__":
    main()
