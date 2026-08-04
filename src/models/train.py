import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.features.build_features import get_feature_column_names
from src.utils.hopsworks_utils import load_features_from_store, get_hopsworks_project
from src.config import MODEL_NAME, MODEL_VERSION

_MODEL_ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "model_artifacts")


class PyTorchAQIRegressor:
    """PyTorch Deep Neural Network Wrapper for AQI Regression."""

    def __init__(self, input_dim: int = 25, hidden_dim: int = 64, lr: float = 0.01, epochs: int = 150):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.lr = lr
        self.epochs = epochs
        self.model = None

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        try:
            import torch
            import torch.nn as nn
            import torch.optim as optim

            class AQINet(nn.Module):
                def __init__(self, in_features):
                    super().__init__()
                    self.net = nn.Sequential(
                        nn.Linear(in_features, 64),
                        nn.ReLU(),
                        nn.Linear(64, 32),
                        nn.ReLU(),
                        nn.Linear(32, 1)
                    )

                def forward(self, x):
                    return self.net(x)

            in_features = X_train.shape[1]
            self.model = AQINet(in_features)
            optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
            criterion = nn.MSELoss()

            X_t = torch.tensor(X_train.values, dtype=torch.float32)
            y_t = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)

            self.model.train()
            for _ in range(self.epochs):
                optimizer.zero_grad()
                outputs = self.model(X_t)
                loss = criterion(outputs, y_t)
                loss.backward()
                optimizer.step()
        except ImportError:
            print("[PyTorch] torch not installed. PyTorchAQIRegressor skipped.")

    def predict(self, X_test: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            return np.zeros(len(X_test))
        import torch
        self.model.eval()
        with torch.no_grad():
            X_t = torch.tensor(X_test.values, dtype=torch.float32)
            preds = self.model(X_t).squeeze(1).numpy()
        return preds


def train_and_evaluate_models(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Trains multiple ML models (Random Forest, Ridge, Gradient Boosting, PyTorch Neural Net),
    evaluates using RMSE, MAE, R2, and selects the optimal models for 1-day, 2-day, and 3-day AQI forecasting.
    """
    feature_cols = get_feature_column_names()
    targets = ["target_aqi_day1", "target_aqi_day2", "target_aqi_day3"]
    
    # Filter rows with valid targets
    clean_df = df.dropna(subset=targets + feature_cols).copy()
    if len(clean_df) < 50:
        raise ValueError(f"Insufficient training samples ({len(clean_df)}). Please run backfill script first.")

    X = clean_df[feature_cols]
    results = {}
    best_models = {}
    
    os.makedirs(_MODEL_ARTIFACT_DIR, exist_ok=True)
    
    for target in targets:
        y = clean_df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        candidates = {
            "RandomForest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
            "Ridge": Ridge(alpha=1.0),
            "GradientBoosting": HistGradientBoostingRegressor(max_iter=100, random_state=42),
            "PyTorch_NeuralNet": PyTorchAQIRegressor(input_dim=len(feature_cols)),
            "NeuralNetwork_MLP": MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42)
        }
        
        target_metrics = {}
        best_model_name = None
        best_rmse = float("inf")
        best_model_obj = None
        
        for name, model in candidates.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
            mae = float(mean_absolute_error(y_test, preds))
            r2 = float(r2_score(y_test, preds))
            
            target_metrics[name] = {
                "rmse": round(rmse, 2),
                "mae": round(mae, 2),
                "r2": round(r2, 4)
            }
            
            if rmse < best_rmse:
                best_rmse = rmse
                best_model_name = name
                best_model_obj = model

        best_models[target] = {
            "name": best_model_name,
            "model": best_model_obj,
            "metrics": target_metrics[best_model_name]
        }
        results[target] = target_metrics
        
        # Save best model locally
        model_path = os.path.join(_MODEL_ARTIFACT_DIR, f"{target}_model.pkl")
        joblib.dump(best_model_obj, model_path)

    # Save metadata summary
    metadata = {
        "best_models": {t: best_models[t]["name"] for t in targets},
        "metrics": {t: best_models[t]["metrics"] for t in targets},
        "all_candidate_metrics": results,
        "feature_cols": feature_cols
    }
    joblib.dump(metadata, os.path.join(_MODEL_ARTIFACT_DIR, "model_metadata.pkl"))
    
    # Save to Hopsworks Model Registry if available
    project = get_hopsworks_project()
    if project:
        try:
            mr = project.get_model_registry()
            model_dir = _MODEL_ARTIFACT_DIR
            hopsworks_model = mr.python.create_model(
                name=MODEL_NAME,
                version=MODEL_VERSION,
                metrics=metadata["metrics"],
                description="3-Day AQI Forecast Multi-Model Ensemble"
            )
            hopsworks_model.save(model_dir)
            print("[Hopsworks Model Registry] Saved trained model to registry successfully!")
        except Exception as e:
            print(f"[Hopsworks Model Registry] Model registry upload error: {e}")

    return metadata


def load_trained_models() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Loads trained models and metadata from local artifacts or returns fallback models."""
    models = {}
    metadata = {}
    targets = ["target_aqi_day1", "target_aqi_day2", "target_aqi_day3"]
    
    meta_path = os.path.join(_MODEL_ARTIFACT_DIR, "model_metadata.pkl")
    if os.path.exists(meta_path):
        metadata = joblib.load(meta_path)

    for target in targets:
        m_path = os.path.join(_MODEL_ARTIFACT_DIR, f"{target}_model.pkl")
        if os.path.exists(m_path):
            models[target] = joblib.load(m_path)

    return models, metadata
