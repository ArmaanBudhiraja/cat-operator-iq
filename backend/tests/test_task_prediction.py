import pytest
from backend.app.services.prediction_service import PredictionService

def test_task_prediction_structure():
    sample_task = {
        "task_id": "T001",
        "task_type": "Earth Excavation",
        "weather": "Rainy",
        "operator_skill": "Expert",
        "machine_age": 3.0,
        "load_cycles": 18,
        "distance": 1.5,
        "estimated_time_min": 60.0,
        "historical_operator_avg_time": 52.0,
        "machine_utilization": 0.85
    }
    result = PredictionService.predict_task_time(sample_task)

    assert "predicted_time_min" in result
    assert result["predicted_time_min"] > 0
    assert "confidence_lower_min" in result
    assert "confidence_upper_min" in result
    assert result["confidence_lower_min"] <= result["predicted_time_min"] <= result["confidence_upper_min"]
    assert "factors" in result
    assert len(result["factors"]) >= 2
    # Verify weather and skill factors exist
    factor_names = [f["name"] for f in result["factors"]]
    assert any("Weather" in name for name in factor_names)
    assert any("Operator Skill" in name for name in factor_names)
