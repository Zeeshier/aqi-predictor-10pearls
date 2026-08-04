import pytest
import pandas as pd
from datetime import datetime, timezone
from src.data.fetch_data import generate_synthetic_observation, calculate_us_aqi_pm25
from src.features.build_features import compute_features, get_feature_column_names
from src.analytics.explainability import evaluate_aqi_hazardous_alerts


def test_aqi_calculation():
    assert calculate_us_aqi_pm25(10.0) <= 50
    assert calculate_us_aqi_pm25(40.0) > 100
    assert calculate_us_aqi_pm25(200.0) > 200


def test_synthetic_observation():
    now = datetime.now(timezone.utc)
    obs = generate_synthetic_observation(now, "Lahore")
    assert "temperature" in obs
    assert "pm25" in obs
    assert "aqi" in obs
    assert obs["aqi"] >= 0


def test_compute_features():
    records = [generate_synthetic_observation(datetime.now(timezone.utc), "Lahore") for _ in range(5)]
    df = pd.DataFrame(records)
    df_feat = compute_features(df)
    
    assert "sin_hour" in df_feat.columns
    assert "cos_hour" in df_feat.columns
    assert "pm25_to_pm10_ratio" in df_feat.columns
    assert len(get_feature_column_names()) > 0


def test_alert_evaluation():
    alert_good = evaluate_aqi_hazardous_alerts(35)
    assert alert_good["category"] == "Good"
    assert not alert_good["alert_triggered"]
    
    alert_haz = evaluate_aqi_hazardous_alerts(350)
    assert alert_haz["category"] == "Hazardous"
    assert alert_haz["alert_triggered"]
