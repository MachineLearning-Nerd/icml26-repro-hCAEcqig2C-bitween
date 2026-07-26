#!/usr/bin/env python3
"""Audit an evaluator-visible Hugging Face Space candidate.

The audit starts at the root page declared by logbook.json, follows only local
Markdown links, verifies the immutable historical page set, and emits the
exact text upload allowlist with SHA-256 hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import deque
from pathlib import Path


MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "hugging_face_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
REQUIRED_CURRENT_PAGES = {
    "pages/current-scorecard/page.md",
    "pages/current-claim-1-section-4/page.md",
    "pages/current-claims-2-4-cumulative/page.md",
    "pages/current-claim-5-backends/page.md",
    "pages/current-methods/page.md",
    "pages/visibility-matrix/page.md",
    "pages/failure-boundaries/page.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def navigation_files(node: dict) -> set[str]:
    paths = {node["file"]}
    for child in node.get("children", []):
        paths.update(navigation_files(child))
    return paths


def resolve_local_link(candidate: Path, source: Path, target: str) -> Path | None:
    clean_target = target.split("#", 1)[0].split("?", 1)[0]
    if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
        return None
    resolved = (source.parent / clean_target).resolve()
    resolved.relative_to(candidate.resolve())
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--protected", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate = args.candidate.resolve()
    protected = args.protected.resolve()
    overlay = args.overlay.resolve()
    assert candidate.is_dir() and protected.is_dir() and overlay.is_dir()

    logbook = json.loads((candidate / "logbook.json").read_text())
    assert logbook["space_id"] == "DineshAI/hCAEcqig2C"
    root_relative = logbook["root"]["file"]
    assert root_relative == "pages/current-scorecard/page.md"

    candidate_files = relative_files(candidate)
    protected_files = relative_files(protected)
    overlay_files = relative_files(overlay)
    assert protected_files <= candidate_files

    historical_pages = {path for path in protected_files if path.startswith("pages/")}
    for relative in historical_pages:
        assert sha256(candidate / relative) == sha256(protected / relative), relative

    declared_navigation = navigation_files(logbook["root"])
    assert declared_navigation <= candidate_files
    assert REQUIRED_CURRENT_PAGES <= declared_navigation

    queue = deque([root_relative])
    visited_pages: list[str] = []
    opened_files: set[str] = set()
    missing_links: list[str] = []
    while queue:
        relative = queue.popleft()
        if relative in visited_pages:
            continue
        page = candidate / relative
        assert page.is_file(), relative
        visited_pages.append(relative)
        opened_files.add(relative)
        for raw_target in MARKDOWN_LINK.findall(page.read_text()):
            target = resolve_local_link(candidate, page, raw_target)
            if target is None:
                continue
            target_relative = target.relative_to(candidate).as_posix()
            if not target.is_file():
                missing_links.append(f"{relative} -> {target_relative}")
                continue
            opened_files.add(target_relative)
            if target_relative.endswith(".md") and target_relative.startswith("pages/"):
                queue.append(target_relative)

    assert not missing_links, missing_links
    assert REQUIRED_CURRENT_PAGES <= set(visited_pages)

    scorecard = (candidate / root_relative).read_text()
    required_scorecard_phrases = [
        "Previous live judged score: `6/10`",
        "Conservative projected score range",
        "Best-supported possible new score",
        "| Claim | Current points | Possible points | Confidence | Evidence status |",
    ]
    for phrase in required_scorecard_phrases:
        assert phrase in scorecard, phrase

    secret_hits: list[dict[str, str]] = []
    upload_allowlist: list[dict[str, str | int]] = []
    for relative in sorted(overlay_files):
        path = overlay / relative
        text = path.read_text(encoding="utf-8")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                secret_hits.append({"file": relative, "pattern": name})
        upload_allowlist.append(
            {
                "path": relative,
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    assert not secret_hits, secret_hits

    result = {
        "schema_version": 1,
        "verdict": "PASS",
        "canonical_entrypoint": root_relative,
        "files_opened_from_canonical_traversal": sorted(opened_files),
        "pages_visited_from_canonical_traversal": visited_pages,
        "navigation_file_count": len(declared_navigation),
        "protected_file_count": len(protected_files),
        "candidate_file_count": len(candidate_files),
        "protected_file_set_is_subset": True,
        "historical_pages_byte_identical": True,
        "missing_links": missing_links,
        "secret_hits": secret_hits,
        "text_upload_allowlist": upload_allowlist,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
