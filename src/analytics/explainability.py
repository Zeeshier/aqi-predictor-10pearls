import numpy as np
import pandas as pd
from typing import Dict, Any, List

from src.features.build_features import get_feature_column_names
from src.config import AQI_THRESHOLDS


def compute_shap_feature_importance(model: Any, X_sample: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Computes SHAP feature importance values for model explainability.
    Returns sorted list of features with mean absolute SHAP values and relative impact.
    """
    feature_cols = get_feature_column_names()
    X = X_sample[feature_cols].copy()
    
    try:
        import shap
        if hasattr(model, "predict"):
            explainer = shap.Explainer(model.predict, X)
            shap_values = explainer(X)
            vals = np.abs(shap_values.values).mean(axis=0)
        else:
            vals = np.zeros(len(feature_cols))
    except Exception as e:
        print(f"[SHAP] Error computing SHAP values: {e}. Fallback to feature importances or variance.")
        if hasattr(model, "feature_importances_"):
            vals = model.feature_importances_
        else:
            vals = X.std().values

    total_importance = float(np.sum(vals)) + 1e-6
    importance_list = []
    for col, score in zip(feature_cols, vals):
        importance_list.append({
            "feature": col,
            "shap_value": round(float(score), 4),
            "percentage": round(float(score / total_importance * 100.0), 2)
        })
        
    importance_list.sort(key=lambda x: x["shap_value"], reverse=True)
    return importance_list


def evaluate_aqi_hazardous_alerts(predicted_aqi: float) -> Dict[str, Any]:
    """
    Evaluates AQI value against US AQI standard thresholds to generate warning alerts.
    """
    aqi_int = round(predicted_aqi)
    category = "GOOD"
    color = "#10B981" # Green
    level = "Low Risk"
    advice = "Air quality is satisfactory, and air pollution poses little or no risk."
    alert_triggered = False

    if aqi_int <= 50:
        category = "Good"
        color = "#10B981"
    elif aqi_int <= 100:
        category = "Moderate"
        color = "#FBBF24"
        advice = "Air quality is acceptable; however, sensitive individuals may experience minor symptoms."
    elif aqi_int <= 150:
        category = "Unhealthy for Sensitive Groups"
        color = "#F97316"
        advice = "Members of sensitive groups (children, elderly, asthmatics) should limit outdoor exposure."
        alert_triggered = True
    elif aqi_int <= 200:
        category = "Unhealthy"
        color = "#EF4444"
        level = "High Risk"
        advice = "Everyone may begin to experience health effects. Wear protective masks (N95) outdoors."
        alert_triggered = True
    elif aqi_int <= 300:
        category = "Very Unhealthy"
        color = "#8B5CF6"
        level = "Severe Warning"
        advice = "Health alert: everyone may experience more serious health effects. Avoid all outdoor physical activity."
        alert_triggered = True
    else:
        category = "Hazardous"
        color = "#991B1B"
        level = "Emergency Alert"
        advice = "Health warnings of emergency conditions. Entire population is more likely to be affected."
        alert_triggered = True

    return {
        "aqi": aqi_int,
        "category": category,
        "color": color,
        "risk_level": level,
        "health_advice": advice,
        "alert_triggered": alert_triggered
    }
