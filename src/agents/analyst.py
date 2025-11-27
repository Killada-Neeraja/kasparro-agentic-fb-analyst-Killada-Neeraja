from pathlib import Path
import json
import pandas as pd


class AnalystAgent:
     """
    Loads the Facebook ads dataset, computes metrics & generates insights.
    """
    def __init__(self,
                 data_path: str = "data/synthetic_fb_ads_undergarments.csv",
                 reports_dir: str = "reports"):
        self.data_path = Path(data_path)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _load_data(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        df = pd.read_csv(self.data_path)
        return df

    def _add_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        df["cpc"] = df["spend"] / df["clicks"]
        df["cpm"] = df["spend"] / df["impressions"] * 1000
        df["cvr"] = df["purchases"] / df["clicks"]
        df.replace([float("inf"), -float("inf")], 0, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def _generate_insights(self, df: pd.DataFrame) -> dict:
        insights = {}
        insights["best_campaign_by_roas"] = df.groupby("campaign_name")["roas"].mean().idxmax()
        insights["best_platform_by_revenue"] = df.groupby("platform")["revenue"].sum().idxmax()
        insights["best_country_by_cvr"] = df.groupby("country")["cvr"].mean().idxmax()
        insights["best_creative_type"] = df.groupby("creative_type")["roas"].mean().idxmax()
        insights["best_audience_type"] = df.groupby("audience_type")["cpc"].mean().idxmin()
        return insights

    def _generate_creatives(self) -> list:
        return [
            {
                "platform": "Facebook",
                "audience_type": "Retargeting",
                "creative_type": "UGC",
                "recommendation": "Use testimonies showing comfort and fit for men’s premium line.",
                "example_copy": "Engineered for comfort — see why men love our collection."
            }
        ]

    def run(self):
        df = self._load_data()
        df = self._add_metrics(df)

        insights = self._generate_insights(df)
        creatives = self._generate_creatives()

        with open(self.reports_dir / "insights.json", "w") as f:
            json.dump(insights, f, indent=4)

        with open(self.reports_dir / "creatives.json", "w") as f:
            json.dump(creatives, f, indent=4)

        return {"insights": insights, "creatives": creatives}
