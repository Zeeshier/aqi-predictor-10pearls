import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.hopsworks_utils import load_features_from_store
from src.models.train import train_and_evaluate_models
from scripts.backfill_features import run_backfill


def run_training_pipeline():
    """
    Automated daily training pipeline:
    1. Fetch feature dataset from Hopsworks Feature Store.
    2. Auto-trigger backfill if store is empty or dataset is too small.
    3. Train and compare ML algorithms.
    4. Compute evaluation metrics (RMSE, MAE, R2).
    5. Register best model artifacts to Hopsworks Model Registry.
    """
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting ML Training Pipeline...")
    df = load_features_from_store()
    
    if df.empty or len(df) < 50:
        print("[Training Pipeline] Feature dataset empty or insufficient. Running automatic historical backfill...")
        run_backfill(days=90)
        df = load_features_from_store()
        
    print(f"Loaded training dataset with {len(df)} samples.")
    metadata = train_and_evaluate_models(df)
    
    print("\n================ ML Training Pipeline Summary ================")
    for target, best_name in metadata["best_models"].items():
        metrics = metadata["metrics"][target]
        print(f"Target [{target}]: Best Model = {best_name} | RMSE = {metrics['rmse']} | MAE = {metrics['mae']} | R2 = {metrics['r2']}")
    print("=============================================================\n")
    print("Training pipeline completed successfully.")


if __name__ == "__main__":
    run_training_pipeline()
