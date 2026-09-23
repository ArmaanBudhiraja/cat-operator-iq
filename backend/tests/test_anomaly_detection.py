import pytest
from backend.app.services.anomaly_service import AnomalyService

def test_nominal_telemetry_anomaly():
    nominal_telem = {
        "engine_temperature": 88.0,
        "oil_pressure": 43.0,
        "hydraulic_pressure": 280.0,
        "engine_rpm": 1850.0,
        "vibration": 1.75,
        "idling_time_min": 6.0
    }
    result = AnomalyService.analyze_telemetry(nominal_telem)
    assert "anomaly_score" in result
    assert "risk_level" in result
    assert "reason" in result
    assert result["risk_level"] in ["LOW", "MEDIUM"]

def test_vibration_spike_anomaly_explanation():
    spiked_telem = {
        "engine_temperature": 88.0,
        "oil_pressure": 26.0,
        "hydraulic_pressure": 280.0,
        "engine_rpm": 1850.0,
        "vibration": 4.5,
        "idling_time_min": 55.0
    }
    result = AnomalyService.analyze_telemetry(spiked_telem)
    assert result["anomaly_score"] >= 40.0
    assert result["risk_level"] in ["HIGH", "CRITICAL"]
    assert len(result["factors"]) > 0
    # Must explain vibration or idle time
    factors_str = " ".join(result["factors"]).lower()
    assert "vibration" in factors_str or "idle" in factors_str
