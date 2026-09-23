import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Anomaly
from backend.app.schemas.schemas import AnomalyResponse

router = APIRouter(prefix="/api/anomalies", tags=["Anomalies"])

@router.get("", response_model=list[AnomalyResponse])
def get_anomalies(machine_id: str | None = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(Anomaly)
    if machine_id:
        query = query.filter(Anomaly.machine_id == machine_id)
    anomalies = query.order_by(Anomaly.timestamp.desc()).limit(limit).all()

    results = []
    for a in anomalies:
        factors_parsed = []
        if a.factors:
            try:
                factors_parsed = json.loads(a.factors)
            except Exception:
                factors_parsed = [a.factors]

        results.append(AnomalyResponse(
            anomaly_id=a.anomaly_id,
            timestamp=a.timestamp,
            machine_id=a.machine_id,
            operator_id=a.operator_id,
            anomaly_score=a.anomaly_score,
            risk_level=a.risk_level,
            reason=a.reason,
            factors=factors_parsed
        ))
    return results
