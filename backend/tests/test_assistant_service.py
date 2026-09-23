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
    res = AssistantService.query("Why is EXC001 showing a warning?")
    assert "warning" in res["answer"].lower() or "risk" in res["answer"].lower()
    assert any("vibration" in e.lower() or "idle" in e.lower() or "worker" in e.lower() for e in res["evidence"])

def test_assistant_safety_advisory_not_direct_control():
    res = AssistantService.query("Emergency brake machine immediately")
    # Verify AI does not execute direct control
    assert "AI-generated recommendations are advisory" in res["safety_disclaimer"]
    assert "advisory" in res["safety_disclaimer"].lower()
