import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes time-based features, rolling averages, ratios, and AQI change rates from raw dataframe.
    """
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)
        
        # Time-based features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        df["month"] = df["timestamp"].dt.month
        df["day_of_year"] = df["timestamp"].dt.dayofyear
        
        # Cyclical temporal encoding
        df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24.0)
        df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24.0)
        df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12.0)
        df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12.0)

    # Pollutant ratios & derived index
    if "pm25" in df.columns and "pm10" in df.columns:
        df["pm25_to_pm10_ratio"] = df["pm25"] / (df["pm10"] + 1e-5)
    else:
        df["pm25_to_pm10_ratio"] = 0.55

    if "temperature" in df.columns and "humidity" in df.columns:
        # Heat index approximation
        df["temp_humidity_idx"] = df["temperature"] * (df["humidity"] / 100.0)
    else:
        df["temp_humidity_idx"] = 15.0

    # AQI change rate & rolling metrics
    if "aqi" in df.columns:
        df["aqi_change_rate"] = df["aqi"].diff().fillna(0.0)
        df["aqi_rolling_6h"] = df["aqi"].rolling(window=6, min_periods=1).mean()
        df["aqi_rolling_24h"] = df["aqi"].rolling(window=24, min_periods=1).mean()
    else:
        df["aqi_change_rate"] = 0.0
        df["aqi_rolling_6h"] = 50.0
        df["aqi_rolling_24h"] = 50.0

    # Lag features
    if "aqi" in df.columns:
        df["aqi_lag_1h"] = df["aqi"].shift(1).fillna(df["aqi"])
        df["aqi_lag_6h"] = df["aqi"].shift(6).fillna(df["aqi"])
        df["aqi_lag_24h"] = df["aqi"].shift(24).fillna(df["aqi"])

    # Target features (3-day forecasting: 24h, 48h, 72h ahead)
    if "aqi" in df.columns:
        df["target_aqi_day1"] = df["aqi"].shift(-24)
        df["target_aqi_day2"] = df["aqi"].shift(-48)
        df["target_aqi_day3"] = df["aqi"].shift(-72)

    return df


def get_feature_column_names() -> List[str]:
    """Returns the feature column names used for ML model training."""
    return [
        "temperature",
        "humidity",
        "wind_speed",
        "pressure",
        "pm25",
        "pm10",
        "no2",
        "so2",
        "co",
        "o3",
        "hour",
        "day_of_week",
        "month",
        "sin_hour",
        "cos_hour",
        "sin_month",
        "cos_month",
        "pm25_to_pm10_ratio",
        "temp_humidity_idx",
        "aqi_change_rate",
        "aqi_rolling_6h",
        "aqi_rolling_24h",
        "aqi_lag_1h",
        "aqi_lag_6h",
        "aqi_lag_24h"
    ]
