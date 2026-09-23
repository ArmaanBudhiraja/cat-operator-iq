from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import SafetyEvent
from backend.app.services.simulation_service import simulation_manager
from backend.app.services.safety_engine import SafetyEngine

router = APIRouter(prefix="/api/safety", tags=["Safety Center"])

@router.get("/live")
def get_live_safety_state():
    """
    Returns real-time safety evaluation, 2D radar coordinates, and 8-rule point breakdown.
    """
    state = simulation_manager.step()
    detailed_eval = SafetyEngine.evaluate(state["telemetry"], recent_events_count=1)
    state["factor_breakdown"] = detailed_eval["factor_breakdown"]
    state["triggered_rules"] = detailed_eval["triggered_rules"]
    return state

@router.get("/events")
def get_safety_events(
    machine_id: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(SafetyEvent)
    if machine_id:
        query = query.filter(SafetyEvent.machine_id == machine_id)
    return query.order_by(SafetyEvent.timestamp.desc()).limit(limit).all()

@router.post("/events/{event_id}/acknowledge")
def acknowledge_safety_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(SafetyEvent).filter(SafetyEvent.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.acknowledged = True
    db.commit()
    return {"message": f"Safety event {event_id} acknowledged"}
