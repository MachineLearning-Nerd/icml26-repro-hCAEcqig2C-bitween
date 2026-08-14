#!/usr/bin/env python3
"""Validate the checked-in Learning Randomized Reductions publication package."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_EXPECTATIONS = {
    "sources/arxiv-v1/source.tar.gz": "c9483e7747bead779af4d5691438feac34e9c38af77cb4fbe4928c90f2f5890c",
    "sources/arxiv-v5/source.tar.gz": "556b673c447303e3d2ce1d3c4e565edb0de7dad954bd5174941841bfe9ca961f",
    "sources/arxiv-v5/paper.pdf": "93cab4aa8cec06434b704e639bab87dd15ea95ac46a335961138a94fc1bae2b8",
}
EVIDENCE_FILES = [
    "sources.json",
    "repro/configs/campaign.json",
    "repro/configs/vanilla_lr.yaml",
    ".openresearch/artifacts/claim1_theory/claim_contract.json",
    ".openresearch/artifacts/claim1_theory/theory_verifier_output.json",
    ".openresearch/artifacts/claim1_theory/independent_checker_output.json",
    ".openresearch/artifacts/claim1_theory/cumulative_verdict.json",
    ".openresearch/artifacts/claims234/claim_contracts.json",
    ".openresearch/artifacts/claims234/frozen_baseline_output.json",
    ".openresearch/artifacts/claims234/negative_control_output.json",
    ".openresearch/artifacts/claim5_backend/claim_contract.json",
    ".openresearch/artifacts/claim5_backend/comparison_gurobi.json",
    ".openresearch/artifacts/claim5_backend/comparison_pulp.json",
    ".openresearch/artifacts/claim5_backend/rows_gurobi.json",
    ".openresearch/artifacts/claim5_backend/rows_pulp.json",
    ".openresearch/artifacts/claim5_backend/source_audit_output.json",
    ".openresearch/artifacts/release/final_integration_verdict.json",
    "outputs/c3_primary_paired_audit.json",
]
SECRET_PATTERNS = (
    re.compile(r"(?:hf_|sk-|ghp_|github_pat_)[A-Za-z0-9_\-]{20,}"),
)


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_gate() -> dict:
    manifest = load("sources.json")
    require(manifest["arxiv_id"] == "2412.18134", "wrong arXiv ID")
    require(manifest["openreview_id"] == "hCAEcqig2C", "wrong OpenReview ID")
    listed = {item["path"]: item["sha256"] for item in manifest["artifacts"]}
    require(listed == SOURCE_EXPECTATIONS, "sources.json does not match gate expectations")
    for relative, expected in SOURCE_EXPECTATIONS.items():
        require((ROOT / relative).is_file(), f"missing source artifact: {relative}")
        require(digest(relative) == expected, f"source hash mismatch: {relative}")
    require(
        manifest["official_code"]["pinned_commit"]
        == "e13d4b59f6d23051c73e07cfc447336da84e7bd2",
        "wrong official code pin",
    )
    return {"artifacts": len(SOURCE_EXPECTATIONS), "sha256": SOURCE_EXPECTATIONS}


def claim_gate() -> dict:
    theory = load(".openresearch/artifacts/claim1_theory/theory_verifier_output.json")
    independent = load(
        ".openresearch/artifacts/claim1_theory/independent_checker_output.json"
    )
    theory_cumulative = load(
        ".openresearch/artifacts/claim1_theory/cumulative_verdict.json"
    )
    frozen = load(".openresearch/artifacts/claims234/frozen_baseline_output.json")
    controls = load(".openresearch/artifacts/claims234/negative_control_output.json")
    gurobi = load(".openresearch/artifacts/claim5_backend/comparison_gurobi.json")
    pulp = load(".openresearch/artifacts/claim5_backend/comparison_pulp.json")
    source_audit = load(
        ".openresearch/artifacts/claim5_backend/source_audit_output.json"
    )
    rows_gurobi = load(".openresearch/artifacts/claim5_backend/rows_gurobi.json")
    rows_pulp = load(".openresearch/artifacts/claim5_backend/rows_pulp.json")
    release = load(".openresearch/artifacts/release/final_integration_verdict.json")
    neural = load("outputs/c3_primary_paired_audit.json")

    require(theory["verdict"] == "VERIFIED", "Claim 1 primary verifier failed")
    require(independent["verdict"] == "VERIFIED", "Claim 1 independent verifier failed")
    require(theory["binary_paper_witness"]["epsilon_equal_half"] == "REJECTED_AS_WITNESS", "binary boundary control missing")
    require(theory["ternary_independent_witness"]["zero_sample_blr_rsr"] == "VERIFIED", "ternary witness missing")
    require(theory_cumulative["verdict"] == "PASS", "Claim 1 cumulative verdict failed")

    require(frozen["claim2"]["function_count"] == 80, "wrong benchmark count")
    require(frozen["claim2"]["id_span"] == [1, 80], "wrong benchmark ID span")
    require(frozen["claim3"]["coverage"] == 43, "frozen vanilla coverage changed")
    require(frozen["claim3"]["verified_identities"] == 91, "frozen vanilla identity count changed")
    require(frozen["claim3"]["faulty"] == 0, "frozen vanilla has faulty identities")
    require(frozen["claim3"]["sigmoid_verified_identities"] >= 1, "sigmoid evidence missing")
    require(frozen["claim4"]["function_count"] == 80, "agentic domain is not full-scale")
    require(frozen["claim4"]["coverage"] >= 64, "agentic coverage is below the paper contract")
    require(frozen["claim4"]["faulty"] == 0, "agentic evidence has faulty identities")
    require(controls["verdict"] == "PASS", "negative controls failed")
    require(all(item["observed"] == "REJECT" for item in controls["identity_controls"]), "false identity accepted")
    require(all(item["observed"] == "REJECT" for item in controls["domain_controls"]["negative"]), "domain mutation accepted")

    require(source_audit["verdict"] == "PASS", "versioned source audit failed")
    require(gurobi["verdict"] == "VERIFIED", "Gurobi comparison failed")
    require(pulp["verdict"] == "VERIFIED", "PuLP comparison failed")
    require(rows_gurobi["row_count"] == 80, "Gurobi rows are incomplete")
    require(rows_pulp["row_count"] == 80, "PuLP rows are incomplete")
    require(gurobi["lr"]["coverage"] == 42 and gurobi["milp"]["coverage"] == 38, "Gurobi coverage changed")
    require(gurobi["lr"]["verified_identities"] == 91 and gurobi["milp"]["verified_identities"] == 70, "Gurobi identity counts changed")
    require(gurobi["lr"]["faulty"] == 0 and gurobi["milp"]["faulty"] == 0, "Gurobi faulty count changed")
    require(gurobi["negative_control"]["observed"] == "REJECT", "Gurobi label swap accepted")

    require(release["verdict"] == "PASS" and release["cumulative_verdict"] == "PASS", "final integration failed")
    require(neural["claim3_result"] == "not_reproduced_in_this_full_scale_open_model_reproduction", "neural comparison was overstated")
    require(all(pair["discovery_direction"] == "neural_ahead" for pair in neural["pairs"]), "neural counterexample is incomplete")
    require(neural["pooled"]["agentic"]["verification_accuracy"] > neural["pooled"]["neural"]["verification_accuracy"], "verification qualification changed")
    return {
        "scoped_contracts": 5,
        "scoped_contract_verdict": "PASS",
        "neural_headline_verdict": neural["claim3_result"],
        "gurobi_rows": rows_gurobi["row_count"],
        "pulp_rows": rows_pulp["row_count"],
    }


def hygiene_gate() -> dict:
    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()
    forbidden_paths = [
        relative for relative in tracked if relative.startswith(".trackio/")
    ]
    env_files = [
        relative
        for relative in tracked
        if Path(relative).name in {".env", ".env.local", ".env.production"}
    ]
    secret_hits: list[str] = []
    absolute_path_hits: list[str] = []
    absolute_prefixes = ("/" + "Users/", "/" + "home/")
    for relative in tracked:
        file_path = ROOT / relative
        if file_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".gz"}:
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            secret_hits.append(relative)
        if any(prefix in content for prefix in absolute_prefixes):
            absolute_path_hits.append(relative)
    require(not forbidden_paths, f"private publisher paths remain: {forbidden_paths}")
    require(not env_files, f"environment files remain: {env_files}")
    require(not secret_hits, f"token-like values remain: {secret_hits}")
    require(not absolute_path_hits, f"absolute local paths remain: {absolute_path_hits}")
    return {
        "tracked_files": len(tracked),
        "forbidden_paths": forbidden_paths,
        "env_files": env_files,
        "secret_hits": secret_hits,
        "absolute_path_hits": absolute_path_hits,
    }


def write_bundle() -> tuple[str, str]:
    records = []
    for relative in EVIDENCE_FILES:
        file_path = ROOT / relative
        require(file_path.is_file(), f"missing evidence file: {relative}")
        records.append(
            {
                "path": relative,
                "bytes": file_path.stat().st_size,
                "sha256": digest(relative),
            }
        )
    bundle_text = "".join(json.dumps(record, sort_keys=True) + "\n" for record in records)
    bundle_path = ROOT / "outputs" / "evidence_bundle.jsonl"
    bundle_path.write_text(bundle_text, encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "paper": "2412.18134",
        "openreview_id": "hCAEcqig2C",
        "source_artifacts": [
            {"path": relative, "sha256": digest(relative)}
            for relative in SOURCE_EXPECTATIONS
        ],
        "evidence_records": len(records),
        "evidence_bundle": {
            "path": "outputs/evidence_bundle.jsonl",
            "sha256": hashlib.sha256(bundle_text.encode("utf-8")).hexdigest(),
        },
        "records": records,
    }
    manifest_path = ROOT / "outputs" / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(manifest_path.relative_to(ROOT)), manifest["evidence_bundle"]["sha256"]


def main() -> None:
    skip_producers = "--skip-producers" in sys.argv[1:]
    sources = source_gate()
    claims = claim_gate()
    hygiene = hygiene_gate()
    manifest_path, bundle_sha = write_bundle()
    manifest_sha = digest(manifest_path)
    result = {
        "paper": "2412.18134",
        "openreview_id": "hCAEcqig2C",
        "producers_skipped": skip_producers,
        "sources": sources,
        "claims": claims,
        "hygiene": hygiene,
        "bundle": {"path": "outputs/evidence_bundle.jsonl", "sha256": bundle_sha},
        "artifact_manifest": {"path": manifest_path, "sha256": manifest_sha},
        "publication_gate_passed": True,
    }
    (ROOT / "outputs" / "publication_gate.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
