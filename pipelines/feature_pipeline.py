import os
import sys
import pandas as pd
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.fetch_data import get_current_raw_data
from src.features.build_features import compute_features
from src.utils.hopsworks_utils import load_features_from_store, save_features_to_store


def run_feature_pipeline():
    """
    Automated hourly feature pipeline:
    1. Fetch current raw weather & pollutant observation.
    2. Load recent history to calculate rolling & lag features.
    3. Compute engineered features.
    4. Upload to Hopsworks Feature Store.
    """
    print(f"[{datetime.now(timezone.utc).isoformat()}] Running hourly feature pipeline...")
    current_obs = get_current_raw_data()
    df_current = pd.DataFrame([current_obs])
    
    # Load recent history to ensure rolling/lag computations are accurate
    df_history = load_features_from_store()
    if not df_history.empty:
        # Keep last 7 days of history + new observation
        df_combined = pd.concat([df_history, df_current]).drop_duplicates(subset=["timestamp"], keep="last")
    else:
        df_combined = df_current

    df_featured = compute_features(df_combined)
    
    # Save the latest featured dataframe
    save_features_to_store(df_featured)
    print("Hourly feature pipeline executed successfully.")


if __name__ == "__main__":
    run_feature_pipeline()
