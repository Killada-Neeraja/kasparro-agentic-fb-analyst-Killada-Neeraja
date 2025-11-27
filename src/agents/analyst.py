from pathlib import Path
import json

import pandas as pd


class AnalystAgent:
    """
    Loads the Facebook ads dataset, computes core metrics,
    generates insights and creative recommendations, and
    writes them to reports/ as JSON files.
    """

    def __init__(
        self,
        data_path: str = "data/synthetic_fb_ads_undergarments.csv",
        reports_dir: str = "reports",
    ):
        self.data_path = Path(data_path)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _load_data(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        df = pd.read_csv(self.data_path)

        # Basic metric engineering
        df = df.copy()
        df["cpc"] = df["spend"] / df["clicks"].replace(0, 1)
        df["cpm"] = df["spend"] / df["impressions"].replace(0, 1) * 1000
        df["cvr"] = df["purchases"] / df["clicks"].replace(0, 1)
        df["roas"] = df["revenue"] / df["spend"].replace(0, 1)
        return df

    def _build_insights(self, df: pd.DataFrame) -> dict:
        insights: dict = {}

        if "campaign_name" in df.columns:
            insights["best_campaign_by_roas"] = (
                df.groupby("campaign_name")["roas"].mean().idxmax()
            )

        if {"platform", "revenue"}.issubset(df.columns):
            insights["best_platform_by_revenue"] = (
                df.groupby("platform")["revenue"].sum().idxmax()
            )

        if {"country", "cvr"}.issubset(df.columns):
            insights["best_country_by_cvr"] = (
                df.groupby("country")["cvr"].mean().idxmax()
            )

        if {"creative_type", "roas"}.issubset(df.columns):
            insights["best_creative_type"] = (
                df.groupby("creative_type")["roas"].mean().idxmax()
            )

        if {"audience_type", "cpc"}.issubset(df.columns):
            insights["best_audience_type"] = (
                df.groupby("audience_type")["cpc"].mean().idxmin()
            )

        return insights

    def _build_creatives(self, insights: dict) -> list:
        best_creative_type = insights.get("best_creative_type", "UGC")
        best_audience = insights.get("best_audience_type", "Retargeting")
        best_country = insights.get("best_country_by_cvr", "UK")

        creatives = [
            {
                "platform": "Facebook",
                "audience_type": best_audience,
                "creative_type": best_creative_type,
                "recommendation": (
                    "Refresh top-performing creatives with new hooks and stronger CTAs "
                    "to fight ad fatigue and sustain ROAS."
                ),
                "example_copy": (
                    f"Men in {best_country} are choosing all-day comfort. "
                    "Show real customers switching to our premium collection with a clear "
                    '"Shop Now" CTA.'
                ),
            },
            {
                "platform": "Instagram",
                "audience_type": "Broad",
                "creative_type": "Video",
                "recommendation": (
                    "Use short vertical videos highlighting before / after comfort, "
                    "plus price anchoring to drive clicks."
                ),
                "example_copy": (
                    "Not just another undergarment. In 5 seconds, show the difference: "
                    "old vs new, then flash the limited-time offer."
                ),
            },
        ]
        return creatives

    def run(self) -> dict:
        df = self._load_data()
        insights = self._build_insights(df)
        creatives = self._build_creatives(insights)

        # Write to reports/
        insights_path = self.reports_dir / "insights.json"
        creatives_path = self.reports_dir / "creatives.json"

        with insights_path.open("w") as f:
            json.dump(insights, f, indent=4)

        with creatives_path.open("w") as f:
            json.dump(creatives, f, indent=4)

        return {
            "insights": insights,
            "creatives": creatives,
        }
