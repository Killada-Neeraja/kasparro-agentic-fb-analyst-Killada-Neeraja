from pathlib import Path
import pandas as pd


class DataAgent:
    """
    Responsible only for loading and basic preprocessing of the dataset.
    """

    def __init__(self, data_path: str = "data/synthetic_fb_ads_undergarments.csv"):
        self.data_path = Path(data_path)

    def load(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        df = pd.read_csv(self.data_path)

        # Basic cleaning
        df = df.copy()
        # Standardize column names if needed
        df.columns = [c.strip() for c in df.columns]

        # Drop obviously broken rows (zero impressions & zero spend)
        if "impressions" in df.columns and "spend" in df.columns:
            df = df[~((df["impressions"] == 0) & (df["spend"] == 0))]

        return df
