from typing import Any
from ml.model_registry import get_anomaly_model

class AnomalyService:
    @staticmethod
    def analyze_telemetry(telemetry_data: dict[str, Any]) -> dict[str, Any]:
        """
        Runs ML anomaly inference on telemetry record and produces explainable insights.
        """
        model = get_anomaly_model()
        if model is None:
            # Fallback heuristic if ML model not trained yet
            vib = float(telemetry_data.get("vibration", 1.8))
            idle = float(telemetry_data.get("idling_time_min", 5.0))
            temp = float(telemetry_data.get("engine_temperature", 88.0))
            is_anom = (vib >= 3.0 or idle >= 40.0 or temp >= 102.0)
            reasons = []
            if vib >= 3.0:
                reasons.append(f"Vibration ({vib:.2f} mm/s) exceeds normal baseline")
            if idle >= 40.0:
                reasons.append(f"Idling time ({idle:.0f} min) exceeds 40-minute limit")
            if temp >= 102.0:
                reasons.append(f"Engine temperature ({temp:.1f}°C) is elevated")
            return {
                "is_anomaly": is_anom,
                "anomaly_score": 65.0 if is_anom else 15.0,
                "risk_level": "HIGH" if is_anom else "LOW",
                "reason": "; ".join(reasons) if reasons else "Telemetry within normal bounds",
                "factors": reasons,
                "raw_decision_score": -0.1 if is_anom else 0.1
            }

        return model.predict_telemetry(telemetry_data)
