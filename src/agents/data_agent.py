import pandas as pd

class DataAgent:
    def __init__(self, config):
        self.config = config

    def load_data(self):
        if self.config.get("use_sample_data"):
            path = self.config["data_path_sample"]
        else:
            path = self.config["data_path_full"]
        return pd.read_csv(path)

    def summarize(self, df):
        summary = df.groupby("campaign_name").agg({
            "impressions": "sum",
            "clicks": "sum",
            "spend": "sum",
            "revenue": "sum"
        })
        summary["CTR"] = summary["clicks"] / summary["impressions"]
        summary["ROAS"] = summary["revenue"] / summary["spend"]

        return summary.reset_index().to_dict(orient="records")
