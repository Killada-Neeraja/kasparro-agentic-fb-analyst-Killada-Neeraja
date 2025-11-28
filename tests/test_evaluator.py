import sys
from pathlib import Path

# Add src/ to sys.path so "agents" can be imported
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.evaluator import EvaluatorAgent


def make_evaluator(conf_min=0.6, min_insights=3):
    config = {
        "confidence_min": conf_min,
        "min_insights": min_insights,
    }
    return EvaluatorAgent(config=config)


def test_evaluator_passes_valid_insights():
    evaluator = make_evaluator()

    insights_payload = {
        "insights": [
            {
                "id": "I1",
                "title": "High ROAS on core campaign",
                "description": "Core campaign has strong ROAS and should be scaled.",
                "impact": "high",
                "confidence": 0.9,
                "evidence": ["Core Campaign"],
            },
            {
                "id": "I2",
                "title": "Low CTR on remarketing",
                "description": "Remarketing ads are not getting enough clicks.",
                "impact": "medium",
                "confidence": 0.8,
                "evidence": ["Remarketing Campaign"],
            },
            {
                "id": "I3",
                "title": "High spend, low ROAS",
                "description": "One campaign burns budget with poor returns.",
                "impact": "high",
                "confidence": 0.85,
                "evidence": ["Prospecting Campaign"],
            },
        ]
    }

    result = evaluator.evaluate(insights_payload)
    assert result["status"] == "pass"
    assert result["insight_count"] == 3
    assert result["issues"] == []


def test_evaluator_flags_low_confidence_and_missing_fields():
    evaluator = make_evaluator(conf_min=0.7, min_insights=2)

    insights_payload = {
        "insights": [
            {
                # missing id/title
                "description": "Badly formed insight",
                "impact": "high",
                "confidence": 0.3,
            }
        ]
    }

    result = evaluator.evaluate(insights_payload)
    assert result["status"] == "fail"
    assert result["insight_count"] == 1
    assert any("missing_id" in issue for issue in result["issues"])
    assert any("low_confidence" in issue for issue in result["issues"])


def test_evaluator_handles_empty_list():
    evaluator = make_evaluator()

    result = evaluator.evaluate({"insights": []})
    assert result["status"] == "fail"
    assert "no_insights_generated" in result["issues"]
