from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.database import get_db
from backend.app.db.models import Operator, Task, SafetyEvent
from backend.app.schemas.schemas import OperatorResponse

router = APIRouter(prefix="/api/operators", tags=["Operators"])

@router.get("", response_model=list[OperatorResponse])
def get_operators(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Operator).limit(limit).all()

@router.get("/{operator_id}")
def get_operator_detail(operator_id: str, db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail=f"Operator {operator_id} not found")

    # Fleet averages for contextual comparison
    fleet_avg_safety = db.query(func.avg(Operator.safety_score)).scalar() or 88.0
    fleet_avg_time = db.query(func.avg(Operator.average_task_time)).scalar() or 54.0
    fleet_avg_training = db.query(func.avg(Operator.training_score)).scalar() or 89.0

    # Recent safety events
    events = (
        db.query(SafetyEvent)
        .filter(SafetyEvent.operator_id == operator_id)
        .order_by(SafetyEvent.timestamp.desc())
        .limit(5)
        .all()
    )

    return {
        "operator": OperatorResponse.from_orm(operator),
        "fleet_baselines": {
            "fleet_avg_safety": round(float(fleet_avg_safety), 1),
            "fleet_avg_task_time": round(float(fleet_avg_time), 1),
            "fleet_avg_training": round(float(fleet_avg_training), 1)
        },
        "recent_safety_events": events
    }
