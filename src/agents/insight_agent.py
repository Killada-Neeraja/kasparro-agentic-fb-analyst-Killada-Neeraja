from typing import Dict, Any
import pandas as pd
import numpy as np


class InsightAgent:
    """
    Takes a cleaned dataframe and generates:
    - metrics (CPC, CPM, CVR)
    - aggregated insights
    - hypotheses about performance (e.g., ROAS drop causes)
    """

    def __init__(self):
        pass

    def _add_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["cpc"] = df["spend"] / df["clicks"].replace(0, np.nan)
        df["cpm"] = df["spend"] / df["impressions"].replace(0, np.nan) * 1000
        df["cvr"] = df["purchases"] / df["clicks"].replace(0, np.nan)
        df["roas"] = df["revenue"] / df["spend"].replace(0, np.nan)

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def _aggregate_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        insights: Dict[str, Any] = {}

        # Basic top performers
        if "campaign_name" in df.columns:
            insights["best_campaign_by_roas"] = (
                df.groupby("campaign_name")["roas"].mean().idxmax()
            )

        if "platform" in df.columns and "revenue" in df.columns:
            insights["best_platform_by_revenue"] = (
                df.groupby("platform")["revenue"].sum().idxmax()
            )

        if "country" in df.columns and "cvr" in df.columns:
            insights["best_country_by_cvr"] = (
                df.groupby("country")["cvr"].mean().idxmax()
            )

        if "creative_type" in df.columns:
            insights["best_creative_type"] = (
                df.groupby("creative_type")["roas"].mean().idxmax()
            )

        if "audience_type" in df.columns and "cpc" in df.columns:
            insights["best_audience_type"] = (
                df.groupby("audience_type")["cpc"].mean().idxmin()
            )

        return insights

    def _hypothesize_roas_change(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Very simple "top-candidate" style heuristic:
        - Check if ROAS decreased over time
        - Attribute to changes in CPC, CTR, or country mix
        """
        result: Dict[str, Any] = {"hypothesis": "", "confidence": 0.0}

        if "ad_date" not in df.columns:
            return result

        tmp = df.copy()
        tmp["ad_date"] = pd.to_datetime(tmp["ad_date"])

        by_date = (
            tmp.sort_values("ad_date")
            .groupby("ad_date")
            .agg({"roas": "mean", "cpc": "mean", "ctr": "mean"})
        )

        if len(by_date) < 2:
            return result

        first_roas = by_date["roas"].iloc[0]
        last_roas = by_date["roas"].iloc[-1]

        if last_roas >= first_roas:
            result["hypothesis"] = "ROAS has not significantly declined over time."
            result["confidence"] = 0.5
            return result

        # ROAS dropped
        roas_drop_pct = (first_roas - last_roas) / (first_roas + 1e-9)
        cpc_change = by_date["cpc"].iloc[-1] - by_date["cpc"].iloc[0]
        ctr_change = by_date["ctr"].iloc[-1] - by_date["ctr"].iloc[0]

        drivers = []
        if cpc_change > 0:
            drivers.append("increasing CPC (more expensive clicks)")
        if ctr_change < 0:
            drivers.append("declining CTR (lower engagement)")

        if not drivers:
            drivers.append("shifts in audience or country mix")

        result["hypothesis"] = (
            f"ROAS has declined by ~{roas_drop_pct * 100:.1f}% over time, "
            f"likely driven by " + " and ".join(drivers) + "."
        )
        # Confidence: crude heuristic
        result["confidence"] = min(0.9, max(0.5, float(roas_drop_pct)))
        return result

    def generate(self, df: pd.DataFrame) -> Dict[str, Any]:
        df = self._add_metrics(df)
        agg_insights = self._aggregate_insights(df)
        roas_hypothesis = self._hypothesize_roas_change(df)

        return {
            "metrics_added": True,
            "insights": agg_insights,
            "roas_hypothesis": roas_hypothesis,
            "data": df,
        }
