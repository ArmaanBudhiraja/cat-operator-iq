import pytest
from backend.app.services.assistant_service import AssistantService

def test_assistant_task_inquiry():
    res = AssistantService.query("What are my tasks today?")
    assert "answer" in res
    assert "evidence" in res
    assert "recommended_next_step" in res
    assert "safety_disclaimer" in res
    assert "AI-generated recommendations are advisory" in res["safety_disclaimer"]
    assert len(res["evidence"]) > 0

def test_assistant_warning_explanation():
    res = AssistantService.query(
        "Why is EXC001 showing a warning?",
        telemetry={"vibration": 2.85, "idling_time_min": 41.0, "worker_detected": True},
        safety_alerts=[{"title": "Proximity Warning", "message": "Worker near tracks"}]
    )
    assert "answer" in res
    assert len(res["evidence"]) > 0
    assert "safety_disclaimer" in res

def test_assistant_safety_advisory_not_direct_control():
    res = AssistantService.query("Emergency brake machine immediately")
    # Verify AI does not execute direct control
    assert "AI-generated recommendations are advisory" in res["safety_disclaimer"]
    assert "advisory" in res["safety_disclaimer"].lower()

def test_assistant_rollback_when_ai_offline():
    from backend.app.config import settings
    orig_key = settings.OPENAI_API_KEY
    try:
        settings.OPENAI_API_KEY = "invalid_simulated_key"
        res = AssistantService.query("What are my tasks today?")
        assert res["is_fallback"] is True
        assert "Local Rule-Based Assistant" in res["ai_provider"]
        assert res["fallback_reason"] is not None
        assert "answer" in res
    finally:
        settings.OPENAI_API_KEY = orig_key

def test_assistant_status():
    status = AssistantService.get_status()
    assert "ai_configured" in status
    assert "fallback_available" in status
    assert status["fallback_available"] is True
