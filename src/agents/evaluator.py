from pathlib import Path
import json


class EvaluatorAgent:
    """
    Evaluates insights and creatives.

    Uses a confidence_min threshold (from config) to decide overall status.
    """

    def __init__(self, reports_dir: str = "reports", confidence_min: float = 0.6):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.confidence_min = confidence_min

    def evaluate(self, insights: dict, creatives: list) -> dict:
        result = {}

        required_keys = [
            "best_campaign_by_roas",
            "best_platform_by_revenue",
            "best_country_by_cvr",
            "best_creative_type",
            "best_audience_type",
        ]
        missing = [k for k in required_keys if k not in insights]
        result["missing_keys"] = missing
        result["num_creatives"] = len(creatives)
        result["has_ugc"] = any(
            c.get("creative_type", "").lower() == "ugc"
            for c in creatives
        )

        # If you later add a "roas_hypothesis" with a confidence field, this will pick it up.
        roas_hypothesis = insights.get("roas_hypothesis", {})
        if isinstance(roas_hypothesis, dict):
            hypo_conf = roas_hypothesis.get("confidence", 0.0)
        else:
            hypo_conf = 0.0
        result["hypothesis_confidence"] = hypo_conf

        # Pass/Fail logic using config threshold
        if len(missing) == 0 and result["num_creatives"] > 0 and (hypo_conf == 0.0 or hypo_conf >= self.confidence_min):
            result["status"] = "pass"
        else:
            result["status"] = "needs_improvement"

        out_path = self.reports_dir / "evaluation.json"
        with out_path.open("w") as f:
            json.dump(result, f, indent=4)

        return result
