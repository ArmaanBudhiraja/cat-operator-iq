import pytest
from backend.app.services.safety_engine import SafetyEngine

def test_nominal_safety_condition():
    telemetry = {
        "seatbelt_status": "Fastened",
        "worker_detected": False,
        "proximity_distance_m": 12.0,
        "fatigue_indicator": 0.1,
        "idling_time_min": 5.0,
        "engine_temperature": 88.0,
        "vibration": 1.75,
        "weather": "Sunny",
        "load_weight": 14.0
    }
    result = SafetyEngine.evaluate(telemetry, recent_events_count=0)
    assert result["risk_score"] <= 30.0
    assert result["risk_level"] == "LOW"
    assert result["status_label"] == "SAFE"
    assert len(result["active_alerts"]) == 0
    assert "AI-generated recommendations are advisory" in result["advisory_disclaimer"]

def test_seatbelt_violation_rule():
    telemetry = {
        "seatbelt_status": "Unfastened",
        "worker_detected": False,
        "proximity_distance_m": 15.0,
        "fatigue_indicator": 0.1,
        "idling_time_min": 5.0,
        "engine_temperature": 88.0,
        "vibration": 1.75,
        "weather": "Sunny",
        "load_weight": 10.0
    }
    result = SafetyEngine.evaluate(telemetry)
    assert "RULE_1_SEATBELT_UNFASTENED" in result["triggered_rules"]
    assert result["risk_score"] >= 35.0
    assert any(a["title"] == "Seatbelt Unfastened" for a in result["active_alerts"])

def test_critical_proximity_hazard():
    telemetry = {
        "seatbelt_status": "Fastened",
        "worker_detected": True,
        "proximity_distance_m": 2.1,
        "fatigue_indicator": 0.1,
        "idling_time_min": 5.0,
        "engine_temperature": 88.0,
        "vibration": 1.75,
        "weather": "Sunny",
        "load_weight": 10.0
    }
    result = SafetyEngine.evaluate(telemetry)
    assert "RULE_2_PROXIMITY_CRITICAL" in result["triggered_rules"]
    assert result["risk_score"] >= 45.0
    assert any(a["severity"] == "CRITICAL" for a in result["active_alerts"])

def test_high_vibration_and_overheat():
    telemetry = {
        "seatbelt_status": "Fastened",
        "worker_detected": False,
        "proximity_distance_m": 12.0,
        "fatigue_indicator": 0.1,
        "idling_time_min": 5.0,
        "engine_temperature": 109.0,
        "vibration": 4.1,
        "weather": "Sunny",
        "load_weight": 10.0
    }
    result = SafetyEngine.evaluate(telemetry)
    assert "RULE_5_ENGINE_OVERHEAT" in result["triggered_rules"]
    assert "RULE_6_ABNORMAL_VIBRATION" in result["triggered_rules"]
    assert result["risk_score"] >= 65.0
    assert result["risk_level"] in ["HIGH", "CRITICAL"]
