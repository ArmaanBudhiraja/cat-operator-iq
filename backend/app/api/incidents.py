import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.database import get_db
from backend.app.db.models import Incident
from backend.app.schemas.schemas import IncidentCreate, IncidentUpdate, IncidentResponse

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

@router.get("", response_model=list[IncidentResponse])
def get_incidents(
    severity: Optional[str] = None,
    machine_id: Optional[str] = None,
    operator_id: Optional[str] = None,
    resolved: Optional[bool] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    if severity:
        query = query.filter(Incident.severity == severity)
    if machine_id:
        query = query.filter(Incident.machine_id == machine_id)
    if operator_id:
        query = query.filter(Incident.operator_id == operator_id)
    if resolved is not None:
        query = query.filter(Incident.resolved == resolved)

    return query.order_by(Incident.timestamp.desc()).limit(limit).all()

@router.post("", response_model=IncidentResponse)
def create_incident(inc: IncidentCreate, db: Session = Depends(get_db)):
    new_id = f"INC{uuid.uuid4().hex[:6].upper()}"
    incident = Incident(
        incident_id=new_id,
        timestamp=datetime.utcnow(),
        machine_id=inc.machine_id,
        operator_id=inc.operator_id,
        incident_type=inc.incident_type,
        severity=inc.severity,
        description=inc.description,
        location=inc.location,
        resolved=False,
        created_at=datetime.utcnow()
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: str, update: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.resolved = update.resolved
    if update.resolution:
        incident.resolution = update.resolution
    db.commit()
    db.refresh(incident)
    return incident

@router.get("/analytics/summary")
def get_incident_analytics(db: Session = Depends(get_db)):
    # Incidents by severity
    sev_rows = db.query(Incident.severity, func.count(Incident.incident_id)).group_by(Incident.severity).all()
    by_severity = {s: cnt for s, cnt in sev_rows}

    # Incidents by type
    type_rows = db.query(Incident.incident_type, func.count(Incident.incident_id)).group_by(Incident.incident_type).all()
    by_type = {t: cnt for t, cnt in type_rows}

    # Machine incident frequency top 5
    top_mach_rows = (
        db.query(Incident.machine_id, func.count(Incident.incident_id))
        .group_by(Incident.machine_id)
        .order_by(func.count(Incident.incident_id).desc())
        .limit(5)
        .all()
    )
    top_machines = [{"machine_id": m, "count": cnt} for m, cnt in top_mach_rows]

    total_incidents = db.query(Incident).count()
    open_incidents = db.query(Incident).filter(Incident.resolved == False).count()

    return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": total_incidents - open_incidents,
        "by_severity": by_severity,
        "by_type": by_type,
        "top_machines": top_machines
    }
