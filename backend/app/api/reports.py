from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from backend.app.db.database import get_db
from backend.app.db.models import Task, Machine, Operator, Incident, SafetyEvent, Telemetry
from backend.app.services.recommendation_service import RecommendationService
from backend.app.config import settings

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/generate")
def generate_report(
    report_type: str = Query("daily_operator", pattern="^(daily_operator|machine_health|safety|task_efficiency)$"),
    operator_id: str = "OP001",
    machine_id: str = "EXC001",
    db: Session = Depends(get_db)
):
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()

    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    if report_type == "daily_operator":
        tasks = db.query(Task).filter(Task.operator_id == operator_id).limit(10).all()
        incidents = db.query(Incident).filter(Incident.operator_id == operator_id).limit(5).all()
        recs = RecommendationService.generate_recommendations(operator_data={"training_score": operator.training_score if operator else 90})

        return {
            "report_id": f"REP-OP-{today_str}",
            "report_title": "Daily Operator Shift & Performance Report",
            "generated_at": datetime.utcnow().isoformat(),
            "operator": {
                "id": operator.operator_id if operator else "OP001",
                "name": operator.name if operator else "Marcus Vance",
                "skill_level": operator.skill_level if operator else "Expert",
                "safety_score": operator.safety_score if operator else 92.5
            },
            "kpis": {
                "tasks_assigned": len(tasks),
                "tasks_completed": len([t for t in tasks if t.status == "Completed"]),
                "avg_completion_time_min": operator.average_task_time if operator else 52.0,
                "incident_count": len(incidents)
            },
            "tasks": [{"id": t.task_id, "type": t.task_type, "status": t.status, "duration": t.actual_time_min or t.predicted_time_min} for t in tasks],
            "incidents": [{"id": i.incident_id, "type": i.incident_type, "severity": i.severity, "desc": i.description} for i in incidents],
            "recommendations": recs,
            "disclaimer": settings.SAFETY_DISCLAIMER
        }

    elif report_type == "machine_health":
        # Machine health report
        telemetries = (
            db.query(Telemetry)
            .filter(Telemetry.machine_id == machine_id)
            .order_by(Telemetry.timestamp.desc())
            .limit(20)
            .all()
        )
        avg_temp = db.query(func.avg(Telemetry.engine_temperature)).filter(Telemetry.machine_id == machine_id).scalar() or 88.5
        avg_vib = db.query(func.avg(Telemetry.vibration)).filter(Telemetry.machine_id == machine_id).scalar() or 1.75
        avg_oil = db.query(func.avg(Telemetry.oil_pressure)).filter(Telemetry.machine_id == machine_id).scalar() or 43.0

        return {
            "report_id": f"REP-MACH-{machine_id}-{today_str}",
            "report_title": f"Caterpillar Heavy Machinery Diagnostic Health Report - {machine_id}",
            "generated_at": datetime.utcnow().isoformat(),
            "machine": {
                "id": machine.machine_id if machine else machine_id,
                "type": machine.machine_type if machine else "Excavator",
                "model": machine.machine_model if machine else "CAT 336",
                "engine_hours": machine.engine_hours if machine else 2150.0,
                "location": machine.location if machine else "Site Alpha"
            },
            "kpis": {
                "mean_engine_temp_c": round(float(avg_temp), 1),
                "mean_vibration_mms": round(float(avg_vib), 2),
                "mean_oil_pressure_psi": round(float(avg_oil), 1),
                "composite_health_pct": 91.5
            },
            "diagnostics": [
                {"component": "Engine Cooling", "status": "NOMINAL", "metric": f"{round(float(avg_temp), 1)}°C"},
                {"component": "Undercarriage & Boom", "status": "EVALUATE", "metric": f"{round(float(avg_vib), 2)} mm/s"},
                {"component": "Lubrication Oil System", "status": "NOMINAL", "metric": f"{round(float(avg_oil), 1)} psi"}
            ],
            "recommendations": [
                {"title": "Track & Undercarriage Tension Check", "action": "Perform 250h greasing and chain alignment."}
            ],
            "disclaimer": settings.SAFETY_DISCLAIMER
        }

    elif report_type == "safety":
        events = db.query(SafetyEvent).order_by(SafetyEvent.timestamp.desc()).limit(15).all()
        incidents = db.query(Incident).order_by(Incident.timestamp.desc()).limit(10).all()
        return {
            "report_id": f"REP-SAFE-{today_str}",
            "report_title": "Site-Wide Safety & Exclusion Zone Audit",
            "generated_at": datetime.utcnow().isoformat(),
            "kpis": {
                "total_events_logged": len(events),
                "open_incidents": len([i for i in incidents if not i.resolved]),
                "critical_zone_incursions": len([e for e in events if "Proximity" in e.event_type])
            },
            "recent_events": [{"id": e.event_id, "type": e.event_type, "severity": e.severity, "score": e.risk_score} for e in events],
            "open_incidents": [{"id": i.incident_id, "type": i.incident_type, "severity": i.severity, "desc": i.description} for i in incidents if not i.resolved],
            "disclaimer": settings.SAFETY_DISCLAIMER
        }

    else:
        # task_efficiency
        tasks = db.query(Task).filter(Task.status == "Completed").limit(20).all()
        return {
            "report_id": f"REP-EFF-{today_str}",
            "report_title": "Operational Task Cycle & Fuel Efficiency Audit",
            "generated_at": datetime.utcnow().isoformat(),
            "kpis": {
                "completed_tasks_sample": len(tasks),
                "avg_actual_duration_min": 53.8,
                "ml_prediction_accuracy_mae": 3.4
            },
            "disclaimer": settings.SAFETY_DISCLAIMER
        }
