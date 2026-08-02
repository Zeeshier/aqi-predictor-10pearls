import os
import pandas as pd
from typing import Optional, Tuple, Dict, Any
from src.config import (
    HOPSWORKS_API_KEY,
    HOPSWORKS_PROJECT_NAME,
    FEATURE_GROUP_NAME,
    FEATURE_GROUP_VERSION,
    MODEL_NAME,
    MODEL_VERSION
)

_LOCAL_FEATURE_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data_cache.csv")


def get_hopsworks_project():
    """Connect to Hopsworks project if API key is configured."""
    if not HOPSWORKS_API_KEY:
        print("[Hopsworks] HOPSWORKS_API_KEY not found. Operating in local mode.")
        return None
    try:
        import hopsworks
        project = hopsworks.login(
            api_key_value=HOPSWORKS_API_KEY,
            project=HOPSWORKS_PROJECT_NAME,
            host="eu-west.cloud.hopsworks.ai"
        )
        return project
    except Exception as e:
        print(f"[Hopsworks] Error connecting to Hopsworks: {e}. Falling back to local mode.")
        return None


def save_features_to_store(df: pd.DataFrame) -> bool:
    """Save processed feature DataFrame to Hopsworks Feature Store or local cache."""
    # Always update local cache
    try:
        os.makedirs(os.path.dirname(_LOCAL_FEATURE_CACHE_PATH), exist_ok=True)
        if os.path.exists(_LOCAL_FEATURE_CACHE_PATH):
            existing_df = pd.read_csv(_LOCAL_FEATURE_CACHE_PATH)
            combined_df = pd.concat([existing_df, df]).drop_duplicates(subset=["timestamp"], keep="last")
            combined_df.to_csv(_LOCAL_FEATURE_CACHE_PATH, index=False)
        else:
            df.to_csv(_LOCAL_FEATURE_CACHE_PATH, index=False)
        print(f"[Feature Store] Local cache updated with {len(df)} rows.")
    except Exception as e:
        print(f"[Feature Store] Local cache save failed: {e}")

    project = get_hopsworks_project()
    if not project:
        return True

    try:
        fs = project.get_feature_store()
        aqi_fg = fs.get_or_create_feature_group(
            name=FEATURE_GROUP_NAME,
            version=FEATURE_GROUP_VERSION,
            primary_key=["timestamp"],
            event_time="timestamp",
            description="Hourly weather and pollutant features for 3-day AQI prediction",
            online_enabled=True
        )
        aqi_fg.insert(df, write_options={"wait_for_job": False})
        print(f"[Hopsworks Feature Store] Inserted {len(df)} rows into feature group '{FEATURE_GROUP_NAME}'.")
        return True
    except Exception as e:
        print(f"[Hopsworks Feature Store] Save error: {e}")
        return False


def load_features_from_store() -> pd.DataFrame:
    """Load features from Hopsworks Feature Store or local cache."""
    project = get_hopsworks_project()
    if project:
        try:
            fs = project.get_feature_store()
            aqi_fg = fs.get_feature_group(name=FEATURE_GROUP_NAME, version=FEATURE_GROUP_VERSION)
            df = aqi_fg.read()
            if df is not None and not df.empty:
                print(f"[Hopsworks Feature Store] Successfully loaded {len(df)} rows.")
                return df
        except Exception as e:
            print(f"[Hopsworks Feature Store] Load error: {e}. Reading local cache.")

    if os.path.exists(_LOCAL_FEATURE_CACHE_PATH):
        df = pd.read_csv(_LOCAL_FEATURE_CACHE_PATH)
        print(f"[Local Store] Loaded {len(df)} rows from local cache.")
        return df

    return pd.DataFrame()
