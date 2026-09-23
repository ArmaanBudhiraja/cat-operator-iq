import pandas as pd
import numpy as np

def evaluate_task_models(rf_metrics: dict, gb_metrics: dict) -> dict:
    best_model = "RandomForest" if rf_metrics["MAE"] <= gb_metrics["MAE"] else "GradientBoosting"
    return {
        "RandomForestRegressor": rf_metrics,
        "GradientBoostingRegressor": gb_metrics,
        "selected_model": best_model,
        "selection_metric": "Validation MAE"
    }

def summarize_anomaly_distribution(anomaly_scores: np.ndarray, threshold: float = 50.0) -> dict:
    anomalies_count = int(np.sum(anomaly_scores >= threshold))
    total = len(anomaly_scores)
    return {
        "total_records_evaluated": total,
        "anomalies_detected": anomalies_count,
        "empirical_contamination_rate": round(anomalies_count / max(1, total), 4),
        "mean_anomaly_score": round(float(np.mean(anomaly_scores)), 2),
        "std_anomaly_score": round(float(np.std(anomaly_scores)), 2),
        "dataset_type": "Synthetic demonstration telemetry"
    }
