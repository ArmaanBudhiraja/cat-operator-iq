import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

ANOMALY_FEATURES = [
    "engine_temperature",
    "oil_pressure",
    "hydraulic_pressure",
    "engine_rpm",
    "vibration",
    "idling_time_min"
]

NOMINAL_BASELINES = {
    "engine_temperature": {"mean": 88.0, "std": 5.0, "unit": "°C", "label": "Engine temperature"},
    "oil_pressure": {"mean": 42.0, "std": 4.0, "unit": "psi", "label": "Oil pressure"},
    "hydraulic_pressure": {"mean": 280.0, "std": 15.0, "unit": "bar", "label": "Hydraulic pressure"},
    "engine_rpm": {"mean": 1850.0, "std": 120.0, "unit": "RPM", "label": "Engine RPM"},
    "vibration": {"mean": 1.8, "std": 0.4, "unit": "mm/s", "label": "Vibration"},
    "idling_time_min": {"mean": 8.0, "std": 6.0, "unit": "min", "label": "Idling duration"}
}

class TelemetryAnomalyDetector:
    def __init__(self, contamination: float = 0.05):
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_fitted = False
        self.baselines = NOMINAL_BASELINES

    def fit(self, df: pd.DataFrame):
        X = df[ANOMALY_FEATURES].copy().fillna(df[ANOMALY_FEATURES].median())
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.model.fit(X_scaled)

        # Update empirical baselines from training data
        for col in ANOMALY_FEATURES:
            self.baselines[col] = {
                "mean": float(df[col].mean()),
                "std": max(0.1, float(df[col].std())),
                "unit": NOMINAL_BASELINES[col]["unit"],
                "label": NOMINAL_BASELINES[col]["label"]
            }

        self.is_fitted = True
        return self

    def predict_telemetry(self, telemetry_data: dict) -> dict:
        """
        Runs Isolation Forest anomaly inference on a telemetry record and generates
        human-readable explanations of deviations from machine baseline.
        """
        row_dict = {f: float(telemetry_data.get(f, self.baselines[f]["mean"])) for f in ANOMALY_FEATURES}
        X_df = pd.DataFrame([row_dict])
        X_scaled = self.scaler.transform(X_df)

        # decision_function yields raw anomaly score (lower means more anomalous)
        raw_score = float(self.model.decision_function(X_scaled)[0])
        # Map raw score to 0 - 100 anomaly severity index
        # raw_score typically ranges from -0.3 (highly anomalous) to +0.2 (normal)
        normalized_score = round(float(np.clip((0.15 - raw_score) / 0.35 * 100.0, 0.0, 100.0)), 1)
        is_anomaly = bool(self.model.predict(X_scaled)[0] == -1 or normalized_score >= 50.0)

        # Explanation generation
        reasons = []
        for feat in ANOMALY_FEATURES:
            val = float(telemetry_data.get(feat, self.baselines[feat]["mean"]))
            base_mean = self.baselines[feat]["mean"]
            base_std = self.baselines[feat]["std"]
            unit = self.baselines[feat]["unit"]
            label = self.baselines[feat]["label"]

            pct_diff = ((val - base_mean) / base_mean) * 100.0

            if feat == "vibration" and val >= base_mean + 1.5 * base_std:
                reasons.append(f"Vibration is {abs(pct_diff):.0f}% above machine baseline ({val:.2f} {unit} vs nominal {base_mean:.1f} {unit})")
            elif feat == "idling_time_min" and val >= base_mean + 2.0 * base_std:
                diff_min = val - base_mean
                reasons.append(f"Idle time is {diff_min:.0f} minutes above normal operating threshold")
            elif feat == "oil_pressure" and val <= base_mean - 1.5 * base_std:
                reasons.append(f"Oil pressure is {abs(pct_diff):.0f}% below baseline ({val:.1f} {unit} vs nominal {base_mean:.1f} {unit})")
            elif feat == "engine_temperature" and val >= base_mean + 1.8 * base_std:
                reasons.append(f"Engine temperature is {abs(pct_diff):.0f}% above normal operating thermal range ({val:.1f} {unit})")
            elif feat == "hydraulic_pressure" and abs(pct_diff) >= 20.0:
                reasons.append(f"Hydraulic pressure deviation of {pct_diff:+.0f}% detected ({val:.0f} {unit})")

        # Determine risk level
        if normalized_score >= 75.0 or len(reasons) >= 3:
            risk_level = "CRITICAL"
        elif normalized_score >= 50.0 or len(reasons) >= 2:
            risk_level = "HIGH"
        elif normalized_score >= 30.0 or len(reasons) >= 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        primary_reason = (
            "; ".join(reasons) if reasons
            else "Telemetry metrics within nominal historical baselines"
        )

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": normalized_score,
            "risk_level": risk_level,
            "reason": primary_reason,
            "factors": reasons,
            "raw_decision_score": round(raw_score, 4)
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
