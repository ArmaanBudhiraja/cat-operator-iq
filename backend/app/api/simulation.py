import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Incident, SafetyEvent
from backend.app.services.simulation_service import simulation_manager
from backend.app.schemas.schemas import SimulationHazardRequest

router = APIRouter(prefix="/api/simulation", tags=["Simulation Controls"])

@router.post("/inject")
def inject_simulation_hazard(req: SimulationHazardRequest, db: Session = Depends(get_db)):
    result = simulation_manager.inject_hazard(req.hazard_type)

    # Automatically log incident and safety event if critical condition injected
    hazard_labels = {
        "worker_proximity": ("Proximity Hazard", "Critical", "Worker detected at 2.1m inside critical radius (<3.0m). Movement halted."),
        "seatbelt_unfastened": ("Seatbelt Violation", "High", "Operator seatbelt unfastened during machine operation."),
        "vibration_spike": ("Mechanical Anomaly", "High", "Severe structural vibration spike at 4.2 mm/s with hydraulic pressure drop."),
        "overheating": ("Overheating", "High", "Engine temperature exceeded 108°C thermal threshold."),
        "idle_excess": ("Excessive Idling", "Medium", "Continuous idle time reached 48 minutes.")
    }

    if req.hazard_type in hazard_labels:
        inc_type, sev, desc = hazard_labels[req.hazard_type]
        new_inc = Incident(
            incident_id=f"INC{uuid.uuid4().hex[:6].upper()}",
            timestamp=datetime.utcnow(),
            machine_id=req.machine_id,
            operator_id=req.operator_id,
            incident_type=inc_type,
            severity=sev,
            description=desc,
            location="Site Alpha - Sector 4 Foundation",
            resolved=False,
            created_at=datetime.utcnow()
        )
        db.add(new_inc)

        new_ev = SafetyEvent(
            event_id=f"SE{uuid.uuid4().hex[:6].upper()}",
            timestamp=datetime.utcnow(),
            machine_id=req.machine_id,
            operator_id=req.operator_id,
            event_type=inc_type,
            severity=sev.upper(),
            risk_score=88.0 if sev == "Critical" else 72.0,
            details=desc,
            acknowledged=False
        )
        db.add(new_ev)
        db.commit()

    return {
        "result": result,
        "hazard_type": req.hazard_type,
        "machine_id": req.machine_id,
        "auto_incident_logged": req.hazard_type in hazard_labels
    }

@router.post("/reset")
def reset_simulation():
    res = simulation_manager.inject_hazard("reset")
    return res

@router.get("/state")
def get_simulation_state():
    return simulation_manager.step()
