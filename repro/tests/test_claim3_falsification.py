from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from claim3_falsification import audit  # noqa: E402


ROOT = Path(__file__).parents[2]


def test_three_seed_primary_audit_is_complete_and_directional():
    result = audit(
        [
            str(ROOT / "outputs/abitween-gptoss"),
            str(ROOT / "outputs/abitween-gptoss-s2"),
            str(ROOT / "outputs/abitween-gptoss-s3"),
        ],
        [
            str(ROOT / "outputs/neural-gptoss"),
            str(ROOT / "outputs/neural-gptoss-s2"),
            str(ROOT / "outputs/neural-gptoss-s3"),
        ],
    )
    assert result["claim3_result"] == "not_reproduced_in_this_full_scale_open_model_reproduction"
    assert [p["discovery_direction"] for p in result["pairs"]] == [
        "neural_ahead",
        "neural_ahead",
        "neural_ahead",
    ]
    assert result["mean_covered"] == {"agentic": 72.0, "neural": 74.33333333333333}
    assert result["pooled"]["agentic"]["verification_accuracy"] > result["pooled"]["neural"]["verification_accuracy"]


def test_paired_audit_does_not_use_union_accuracy():
    result = audit(
        [str(ROOT / "outputs/abitween-gptoss")],
        [str(ROOT / "outputs/neural-gptoss")],
    )
    assert result["pairs"][0]["agentic"]["covered"] == 73
    assert result["pairs"][0]["neural"]["covered"] == 74
    assert result["pairs"][0]["agentic"]["verification_accuracy"] > result["pairs"][0]["neural"]["verification_accuracy"]
