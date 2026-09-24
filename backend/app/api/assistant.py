from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Operator, Machine, Task, Incident
from backend.app.schemas.schemas import AssistantQueryRequest, AssistantQueryResponse
from backend.app.services.assistant_service import AssistantService
from backend.app.services.simulation_service import simulation_manager

router = APIRouter(prefix="/api/assistant", tags=["AI Assistant"])

@router.get("/status")
def get_assistant_status():
    return AssistantService.get_status()

@router.post("/query", response_model=AssistantQueryResponse)
def query_assistant(req: AssistantQueryRequest, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.operator_id == req.operator_id).first()
    machine = db.query(Machine).filter(Machine.machine_id == req.machine_id).first()
    active_task = (
        db.query(Task)
        .filter(Task.operator_id == req.operator_id, Task.machine_id == req.machine_id, Task.status == "In Progress")
        .first()
    )
    incidents = (
        db.query(Incident)
        .filter(Incident.machine_id == req.machine_id)
        .order_by(Incident.timestamp.desc())
        .limit(3)
        .all()
    )

    op_dict = {"name": operator.name, "training_score": operator.training_score} if operator else None
    mach_dict = {"machine_id": machine.machine_id, "type": machine.machine_type} if machine else None
    task_dict = {
        "task_id": active_task.task_id,
        "task_type": active_task.task_type,
        "status": active_task.status,
        "location": active_task.location,
        "predicted_time_min": active_task.predicted_time_min or 54.0,
        "estimated_time_min": active_task.estimated_time_min
    } if active_task else None

    # Get live telemetry & active alerts
    live_sim = simulation_manager.current_state
    active_alerts = simulation_manager.step()["active_alerts"]
    inc_list = [{"id": inc.incident_id, "type": inc.incident_type} for inc in incidents]

    result = AssistantService.query(
        user_query=req.query,
        operator_data=op_dict,
        machine_data=mach_dict,
        active_task=task_dict,
        telemetry=live_sim,
        safety_alerts=active_alerts,
        incidents=inc_list
    )

    return AssistantQueryResponse(
        question=result["question"],
        answer=result["answer"],
        evidence=result["evidence"],
        recommended_next_step=result["recommended_next_step"],
        safety_disclaimer=result["safety_disclaimer"],
        citations=result["citations"],
        is_fallback=result.get("is_fallback", False),
        ai_provider=result.get("ai_provider", "Live AI"),
        fallback_reason=result.get("fallback_reason")
    )
