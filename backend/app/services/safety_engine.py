from typing import Any
from backend.app.config import settings

class SafetyEngine:
    """
    Transparent, rule-based safety evaluation and scoring engine.
    Calculates safety risk on a 0-100 scale:
      0-30: LOW (Safe)
      31-60: MEDIUM (Warning)
      61-80: HIGH (Action Required)
      81-100: CRITICAL (Immediate Hazard)
    
    Adheres strictly to the advisory safety principle:
    AI recommendations are advisory and do NOT replace official procedures.
    """

    @classmethod
    def evaluate(
        cls,
        telemetry: dict[str, Any],
        recent_events_count: int = 0
    ) -> dict[str, Any]:
        """
        Evaluates 8 safety rules against real-time telemetry and contextual state.
        Returns:
            - risk_score: float (0 - 100)
            - risk_level: str ("LOW", "MEDIUM", "HIGH", "CRITICAL")
            - status_label: str ("SAFE", "WARNING", "HIGH RISK", "CRITICAL")
            - active_alerts: list of dicts with severity, title, message, rule_id
            - factor_breakdown: detailed points contributed by each risk domain
            - advisory_disclaimer: standard safety advisory note
        """
        seatbelt_risk = 0.0
        proximity_risk = 0.0
        fatigue_risk = 0.0
        temperature_risk = 0.0
        vibration_risk = 0.0
        behavior_risk = 0.0
        environmental_risk = 0.0

        active_alerts: list[dict[str, Any]] = []
        triggered_rules: list[str] = []

        # RULE 1: Seatbelt unfastened
        seatbelt_status = str(telemetry.get("seatbelt_status", "Fastened")).lower()
        if seatbelt_status == "unfastened":
            seatbelt_risk = 35.0
            triggered_rules.append("RULE_1_SEATBELT_UNFASTENED")
            active_alerts.append({
                "rule_id": "RULE_1",
                "severity": "HIGH",
                "title": "Seatbelt Unfastened",
                "message": "Operator seatbelt is unfastened during machine operation. Fasten seatbelt immediately.",
                "timestamp": telemetry.get("timestamp")
            })

        # RULE 2: Worker too close to machine (Proximity Hazard)
        worker_detected = bool(telemetry.get("worker_detected", False))
        distance_m = float(telemetry.get("proximity_distance_m", 15.0))
        if worker_detected:
            if distance_m <= 3.0:
                proximity_risk = 45.0
                triggered_rules.append("RULE_2_PROXIMITY_CRITICAL")
                active_alerts.append({
                    "rule_id": "RULE_2",
                    "severity": "CRITICAL",
                    "title": "Critical Proximity Hazard",
                    "message": f"Worker detected at {distance_m:.1f}m inside critical radius (<3.0m). Pause movement.",
                    "timestamp": telemetry.get("timestamp")
                })
            elif distance_m <= 6.0:
                proximity_risk = 25.0
                triggered_rules.append("RULE_2_PROXIMITY_WARNING")
                active_alerts.append({
                    "rule_id": "RULE_2",
                    "severity": "MEDIUM",
                    "title": "Proximity Warning",
                    "message": f"Worker detected at {distance_m:.1f}m in caution boundary (3.0m - 6.0m). Maintain visual contact.",
                    "timestamp": telemetry.get("timestamp")
                })

        # RULE 3: High fatigue indicator
        fatigue_val = float(telemetry.get("fatigue_indicator", 0.0))
        if fatigue_val >= 0.75:
            fatigue_risk = 30.0
            triggered_rules.append("RULE_3_HIGH_FATIGUE")
            active_alerts.append({
                "rule_id": "RULE_3",
                "severity": "HIGH",
                "title": "High Operator Fatigue",
                "message": f"Fatigue index reached {fatigue_val:.2f}. Operator break strongly advised.",
                "timestamp": telemetry.get("timestamp")
            })
        elif fatigue_val >= 0.50:
            fatigue_risk = 15.0
            triggered_rules.append("RULE_3_MODERATE_FATIGUE")
            active_alerts.append({
                "rule_id": "RULE_3",
                "severity": "MEDIUM",
                "title": "Moderate Fatigue Detected",
                "message": f"Fatigue index is {fatigue_val:.2f}. Ensure hydration and alertness.",
                "timestamp": telemetry.get("timestamp")
            })

        # RULE 4: Excessive Idling
        idle_time_min = float(telemetry.get("idling_time_min", 0.0))
        if idle_time_min >= 45.0:
            behavior_risk += 20.0
            triggered_rules.append("RULE_4_EXCESSIVE_IDLE_CRITICAL")
            active_alerts.append({
                "rule_id": "RULE_4",
                "severity": "MEDIUM",
                "title": "Excessive Idling",
                "message": f"Continuous machine idle time at {idle_time_min:.0f} minutes. Turn off engine to conserve fuel.",
                "timestamp": telemetry.get("timestamp")
            })
        elif idle_time_min >= 25.0:
            behavior_risk += 10.0
            triggered_rules.append("RULE_4_EXCESSIVE_IDLE_WARNING")

        # RULE 5: High Engine Temperature
        engine_temp = float(telemetry.get("engine_temperature", 85.0))
        if engine_temp >= 105.0:
            temperature_risk = 35.0
            triggered_rules.append("RULE_5_ENGINE_OVERHEAT")
            active_alerts.append({
                "rule_id": "RULE_5",
                "severity": "HIGH",
                "title": "Engine Overheating",
                "message": f"Engine coolant/block temperature reached {engine_temp:.1f}°C (>105°C threshold).",
                "timestamp": telemetry.get("timestamp")
            })
        elif engine_temp >= 98.0:
            temperature_risk = 15.0
            triggered_rules.append("RULE_5_HIGH_TEMP_WARNING")
            active_alerts.append({
                "rule_id": "RULE_5",
                "severity": "MEDIUM",
                "title": "Elevated Engine Temperature",
                "message": f"Engine temperature is elevated at {engine_temp:.1f}°C. Monitor cooling system.",
                "timestamp": telemetry.get("timestamp")
            })

        # RULE 6: Abnormal Vibration
        vibration = float(telemetry.get("vibration", 1.8))
        if vibration >= 3.8:
            vibration_risk = 30.0
            triggered_rules.append("RULE_6_ABNORMAL_VIBRATION")
            active_alerts.append({
                "rule_id": "RULE_6",
                "severity": "HIGH",
                "title": "Severe Vibration Anomaly",
                "message": f"Vibration magnitude {vibration:.2f} mm/s exceeds safe structural limit (3.8 mm/s).",
                "timestamp": telemetry.get("timestamp")
            })
        elif vibration >= 2.8:
            vibration_risk = 15.0
            triggered_rules.append("RULE_6_ELEVATED_VIBRATION")
            active_alerts.append({
                "rule_id": "RULE_6",
                "severity": "MEDIUM",
                "title": "Elevated Vibration",
                "message": f"Vibration reading {vibration:.2f} mm/s is higher than baseline.",
                "timestamp": telemetry.get("timestamp")
            })

        # RULE 7: Multiple safety events in short period
        if recent_events_count >= 3:
            behavior_risk += 25.0
            triggered_rules.append("RULE_7_REPEATED_SAFETY_EVENTS")
            active_alerts.append({
                "rule_id": "RULE_7",
                "severity": "HIGH",
                "title": "Frequent Safety Events",
                "message": f"{recent_events_count} safety occurrences logged recently. Operating discipline review required.",
                "timestamp": telemetry.get("timestamp")
            })
        elif recent_events_count >= 2:
            behavior_risk += 12.0
            triggered_rules.append("RULE_7_MODERATE_SAFETY_EVENTS")

        # RULE 8: Unsafe combination of environmental conditions and operation
        weather = str(telemetry.get("weather", "Sunny")).capitalize()
        load_weight = float(telemetry.get("load_weight", 0.0))
        if weather in ["Rainy", "Storm"] and load_weight >= 18.0:
            environmental_risk = 20.0
            triggered_rules.append("RULE_8_WEATHER_LOAD_COMBO")
            active_alerts.append({
                "rule_id": "RULE_8",
                "severity": "HIGH",
                "title": "Severe Weather + High Load Warning",
                "message": f"Adverse weather ({weather}) combined with heavy load ({load_weight:.1f}t). Risk of traction loss.",
                "timestamp": telemetry.get("timestamp")
            })

        # Raw additive risk calculation
        raw_risk = (
            seatbelt_risk +
            proximity_risk +
            fatigue_risk +
            temperature_risk +
            vibration_risk +
            behavior_risk +
            environmental_risk
        )

        # Normalize to 0-100 scale
        risk_score = round(min(100.0, max(0.0, raw_risk)), 1)

        # Map to discrete risk bands
        if risk_score <= 30.0:
            risk_level = "LOW"
            status_label = "SAFE"
        elif risk_score <= 60.0:
            risk_level = "MEDIUM"
            status_label = "WARNING"
        elif risk_score <= 80.0:
            risk_level = "HIGH"
            status_label = "HIGH RISK"
        else:
            risk_level = "CRITICAL"
            status_label = "CRITICAL"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "status_label": status_label,
            "active_alerts": active_alerts,
            "triggered_rules": triggered_rules,
            "factor_breakdown": {
                "seatbelt_risk": seatbelt_risk,
                "proximity_risk": proximity_risk,
                "fatigue_risk": fatigue_risk,
                "temperature_risk": temperature_risk,
                "vibration_risk": vibration_risk,
                "behavior_risk": behavior_risk,
                "environmental_risk": environmental_risk,
            },
            "advisory_disclaimer": settings.SAFETY_DISCLAIMER
        }
