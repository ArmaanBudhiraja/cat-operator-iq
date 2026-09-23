import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from ml.task_time_model import TaskTimePredictor
from ml.anomaly_detection import TelemetryAnomalyDetector
from ml.evaluate_models import evaluate_task_models, summarize_anomaly_distribution

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_and_evaluate():
    print("=" * 60)
    print("CAT OperatorIQ - ML Model Training Pipeline")
    print("=" * 60)

    # Check if data exists; if not, trigger generation
    tasks_file = DATA_DIR / "tasks.csv"
    telemetry_file = DATA_DIR / "telemetry.csv"
    operators_file = DATA_DIR / "operators.csv"

    if not tasks_file.exists() or not telemetry_file.exists():
        print("Data files not found. Triggering synthetic generator...")
        from scripts.generate_data import generate_synthetic_dataset
        generate_synthetic_dataset()

    # 1. LOAD & PREPARE TASK DATA
    print("\n[1/3] Loading task records for duration regression...")
    df_tasks = pd.read_csv(tasks_file)
    df_ops = pd.read_csv(operators_file).set_index("operator_id")

    # Filter completed tasks with actual_time_min
    train_tasks = df_tasks[df_tasks["actual_time_min"].notna()].copy()
    print(f"Loaded {len(train_tasks)} completed task records for training.")

    # Join operator historical baseline
    train_tasks["historical_operator_avg_time"] = train_tasks["operator_id"].map(
        lambda op_id: df_ops.loc[op_id, "average_task_time"] if op_id in df_ops.index else 55.0
    )
    # Synthetic machine utilization (0.5 - 0.95)
    np.random.seed(42)
    train_tasks["machine_utilization"] = np.random.uniform(0.65, 0.92, size=len(train_tasks))

    feature_cols = [
        "task_type", "weather", "operator_skill", "machine_age",
        "load_cycles", "distance", "historical_operator_avg_time", "machine_utilization"
    ]
    X = train_tasks[feature_cols]
    y = train_tasks["actual_time_min"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. TRAIN & COMPARE MODELS
    print("\n[2/3] Training and comparing regression candidates...")

    # Candidate A: Random Forest
    rf_model = TaskTimePredictor(model_type="RandomForest")
    rf_model.fit(X_train, y_train)
    rf_eval = rf_model.evaluate(X_test, y_test)
    print(f"-> RandomForestRegressor: MAE = {rf_eval['MAE']} min, RMSE = {rf_eval['RMSE']} min, R² = {rf_eval['R2']}")

    # Candidate B: Gradient Boosting
    gb_model = TaskTimePredictor(model_type="GradientBoosting")
    gb_model.fit(X_train, y_train)
    gb_eval = gb_model.evaluate(X_test, y_test)
    print(f"-> GradientBoostingRegressor: MAE = {gb_eval['MAE']} min, RMSE = {gb_eval['RMSE']} min, R² = {gb_eval['R2']}")

    # Select best model based on validation MAE
    comparison = evaluate_task_models(rf_eval, gb_eval)
    selected_name = comparison["selected_model"]
    selected_model = rf_model if selected_name == "RandomForest" else gb_model
    selected_metrics = rf_eval if selected_name == "RandomForest" else gb_eval
    print(f"\n[WINNER] Selected: {selected_name}Regressor based on {comparison['selection_metric']}.")

    # Save best regression model
    reg_save_path = MODELS_DIR / "task_time_model.joblib"
    selected_model.save(str(reg_save_path))
    print(f"Saved task prediction model to {reg_save_path}")

    # 3. TRAIN ANOMALY DETECTION MODEL (Isolation Forest)
    print("\n[3/3] Training Unsupervised Telemetry Anomaly Detector (Isolation Forest)...")
    df_telem = pd.read_csv(telemetry_file)
    print(f"Loaded {len(df_telem)} telemetry records.")

    anomaly_detector = TelemetryAnomalyDetector(contamination=0.05)
    anomaly_detector.fit(df_telem)

    # Test sample inference on telemetry
    sample_scores = []
    for idx, row in df_telem.head(1000).iterrows():
        res = anomaly_detector.predict_telemetry(row.to_dict())
        sample_scores.append(res["anomaly_score"])

    anomaly_summary = summarize_anomaly_distribution(np.array(sample_scores))
    print(f"Anomaly evaluation on 1,000 records: {anomaly_summary['anomalies_detected']} anomalies flagged ({anomaly_summary['empirical_contamination_rate'] * 100:.1f}%)")

    # Save anomaly detector
    anom_save_path = MODELS_DIR / "anomaly_model.joblib"
    anomaly_detector.save(str(anom_save_path))
    print(f"Saved anomaly detector model to {anom_save_path}")

    # 4. SAVE EVALUATION METRICS REPORT
    final_metrics = {
        "task_completion_model": {
            "selected_model": f"{selected_name}Regressor",
            "MAE_minutes": selected_metrics["MAE"],
            "RMSE_minutes": selected_metrics["RMSE"],
            "R2_score": selected_metrics["R2"],
            "comparison": comparison,
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        },
        "anomaly_detection_model": {
            "algorithm": "IsolationForest",
            "contamination_parameter": 0.05,
            "features": [
                "engine_temperature", "oil_pressure", "hydraulic_pressure",
                "engine_rpm", "vibration", "idling_time_min"
            ],
            "evaluation_sample_summary": anomaly_summary
        }
    }

    metrics_path = MODELS_DIR / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(final_metrics, f, indent=2)
    print(f"Saved full ML evaluation metrics to {metrics_path}")
    print("\nML Training Pipeline executed successfully!")

if __name__ == "__main__":
    train_and_evaluate()
