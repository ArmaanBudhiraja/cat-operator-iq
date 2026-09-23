from typing import Any
from backend.app.config import settings

class RecommendationService:
    @staticmethod
    def generate_recommendations(
        telemetry: dict[str, Any] | None = None,
        operator_data: dict[str, Any] | None = None,
        machine_data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Generates explainable, actionable recommendations across Safety,
        Maintenance, Training, and Productivity domains.
        """
        recs = []

        if telemetry:
            # Seatbelt check
            if str(telemetry.get("seatbelt_status", "")).lower() == "unfastened":
                recs.append({
                    "category": "Safety",
                    "priority": "Critical",
                    "title": "Fasten Operator Seatbelt",
                    "recommendation": "Secure 3-point seatbelt restraint before continuing machine operation.",
                    "reason": "Seatbelt is unfastened during active machine shift, violating ROPS safety policy."
                })

            # Proximity check
            worker_det = bool(telemetry.get("worker_detected", False))
            dist = float(telemetry.get("proximity_distance_m", 10.0))
            if worker_det and dist <= 3.0:
                recs.append({
                    "category": "Safety",
                    "priority": "Critical",
                    "title": "Ground Worker Clearance Protocol",
                    "recommendation": "Pause hydraulic swing and implement movement. Establish visual contact with ground worker.",
                    "reason": f"Worker detected at {dist:.1f}m inside critical 3.0m exclusion boundary."
                })

            # Vibration check
            vib = float(telemetry.get("vibration", 1.8))
            if vib >= 2.8:
                recs.append({
                    "category": "Maintenance",
                    "priority": "High" if vib >= 3.8 else "Medium",
                    "title": "Undercarriage & Structural Inspection",
                    "recommendation": "Review machine condition and follow applicable maintenance procedures for track tension and hydraulic pump mounting.",
                    "reason": f"Vibration reading ({vib:.2f} mm/s) is elevated above nominal machine baseline."
                })

            # Idle time check
            idle = float(telemetry.get("idling_time_min", 0.0))
            if idle >= 30.0:
                recs.append({
                    "category": "Efficiency",
                    "priority": "Medium",
                    "title": "Enable Auto-Idle & Reduce Fuel Burn",
                    "recommendation": "Consider reducing unnecessary idle duration. Switch engine to low idle or shut down if waiting exceeds 5 minutes.",
                    "reason": f"Continuous idle time has reached {idle:.0f} minutes without digging or hauling load."
                })

            # Overheating
            temp = float(telemetry.get("engine_temperature", 88.0))
            if temp >= 100.0:
                recs.append({
                    "category": "Maintenance",
                    "priority": "High",
                    "title": "Cooling System Thermal Relief",
                    "recommendation": "Reduce hydraulic load and inspect radiator airflow for debris obstruction.",
                    "reason": f"Engine operating temperature ({temp:.1f}°C) is approaching thermal limit."
                })

        if operator_data:
            train_score = float(operator_data.get("training_score", 90.0))
            if train_score < 80.0:
                recs.append({
                    "category": "Training",
                    "priority": "High",
                    "title": "Mandatory Safety Refresher",
                    "recommendation": "Complete TRN001 Proximity Safety & Ground Worker Awareness course.",
                    "reason": f"Current operator safety training score is {train_score:.1f}% (below 80% certification benchmark)."
                })

        # Ensure default advisory recommendations if none triggered
        if not recs:
            recs.append({
                "category": "Safety",
                "priority": "Low",
                "title": "Standard Operating Discipline",
                "recommendation": "Maintain 360-degree situational awareness and monitor daily cycle efficiency.",
                "reason": "All machine telemetry parameters and operator scores are within nominal targets."
            })

        return recs
