import os
import sys
from datetime import datetime, timedelta, timezone
import pandas as pd

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.fetch_data import generate_synthetic_observation
from src.features.build_features import compute_features
from src.utils.hopsworks_utils import save_features_to_store
from src.config import DEFAULT_CITY


def run_backfill(days: int = 180):
    """
    Backfill historical feature dataset for model training.
    Default: 180 days of hourly observations (4,320 rows).
    """
    print(f"Starting historical backfill for past {days} days ({days * 24} hours)...")
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)
    
    records = []
    current_time = start_time
    while current_time <= end_time:
        obs = generate_synthetic_observation(current_time, DEFAULT_CITY)
        records.append(obs)
        current_time += timedelta(hours=1)
        
    df_raw = pd.DataFrame(records)
    print(f"Generated {len(df_raw)} raw historical records.")
    
    df_features = compute_features(df_raw)
    print(f"Computed features: {df_features.shape[1]} columns.")
    
    saved = save_features_to_store(df_features)
    if saved:
        print("Backfill completed successfully and saved to feature store!")
    else:
        print("Backfill encountered an error during saving.")


if __name__ == "__main__":
    run_backfill(days=90)
