from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from backend.app.db.database import get_db
from backend.app.db.models import Task, Machine, Operator, Telemetry, SafetyEvent, TrainingProgress
from backend.app.services.simulation_service import simulation_manager
from backend.app.config import settings

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard_data(operator_id: str = "OP001", machine_id: str = "EXC001", db: Session = Depends(get_db)):
    # 1. Fetch current operator and machine
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()

    # 2. Fetch current in-progress task
    current_task = (
        db.query(Task)
        .filter(Task.operator_id == operator_id, Task.machine_id == machine_id, Task.status == "In Progress")
        .first()
    )
    if not current_task:
        current_task = db.query(Task).filter(Task.operator_id == operator_id).first()

    # 3. Calculate Real Database KPIs
    total_tasks_today = db.query(Task).filter(Task.operator_id == operator_id).count()
    completed_tasks = db.query(Task).filter(Task.operator_id == operator_id, Task.status == "Completed").count()
    
    avg_task_time_row = (
        db.query(func.avg(Task.actual_time_min))
        .filter(Task.actual_time_min.isnot(None))
        .scalar()
    )
    avg_task_time = round(float(avg_task_time_row or 54.5), 1)

    safety_alerts_count = db.query(SafetyEvent).filter(SafetyEvent.operator_id == operator_id).count()

    # Query recent telemetry aggregates for idle and fuel
    avg_idle = (
        db.query(func.avg(Telemetry.idling_time_min))
        .filter(Telemetry.machine_id == machine_id)
        .scalar()
    )
    idle_time_min = round(float(avg_idle or 12.0), 1)

    avg_fuel = (
        db.query(func.avg(Telemetry.fuel_used_l))
        .filter(Telemetry.machine_id == machine_id)
        .scalar()
    )
    fuel_efficiency_lh = round(float(avg_fuel or 18.4), 1)

    # Calculate training progress %
    completed_courses = db.query(TrainingProgress).filter(
        TrainingProgress.operator_id == operator_id,
        TrainingProgress.completion_status == "Completed"
    ).count()
    total_courses = max(1, db.query(TrainingProgress).filter(TrainingProgress.operator_id == operator_id).count())
    training_pct = round((completed_courses / total_courses) * 100.0, 1)

    # 4. Simulation live telemetry state
    sim_state = simulation_manager.step()

    # 5. Composite machine health calculation
    # Transparent formula: Temp(25%) + Vibration(25%) + Oil(25%) + Maintenance(25%)
    vib = sim_state["telemetry"]["vibration"]
    temp = sim_state["telemetry"]["engine_temperature"]
    oil = sim_state["telemetry"]["oil_pressure"]
    maint_days = machine.maintenance_age_days if machine else 30

    health_temp = max(0.0, 100.0 - max(0.0, (temp - 88.0) * 3.5))
    health_vib = max(0.0, 100.0 - max(0.0, (vib - 1.75) * 25.0))
    health_oil = max(0.0, 100.0 - max(0.0, (43.0 - oil) * 3.0))
    health_maint = max(0.0, 100.0 - (maint_days * 0.4))
    machine_health = round(0.25 * health_temp + 0.25 * health_vib + 0.25 * health_oil + 0.25 * health_maint, 1)

    task_dict = None
    if current_task:
        task_dict = {
            "task_id": current_task.task_id,
            "task_type": current_task.task_type,
            "machine_id": current_task.machine_id,
            "operator_id": current_task.operator_id,
            "location": current_task.location,
            "priority": current_task.priority,
            "scheduled_start": str(current_task.scheduled_start),
            "estimated_time_min": current_task.estimated_time_min,
            "predicted_time_min": current_task.predicted_time_min or 54.0,
            "actual_time_min": current_task.actual_time_min,
            "load_cycles": current_task.load_cycles,
            "distance": current_task.distance,
            "weather": current_task.weather,
            "operator_skill": current_task.operator_skill,
            "machine_age": current_task.machine_age,
            "status": current_task.status
        }

    return {
        "greeting": f"GOOD MORNING, {operator.name.upper() if operator else 'OPERATOR'}",
        "operator_name": operator.name if operator else "Marcus Vance",
        "current_machine_id": machine_id,
        "current_task": task_dict,
        "task_progress_pct": 67.0,
        "estimated_remaining_time_min": 42.0,
        "machine_health_pct": machine_health,
        "safety_status": sim_state["status_label"],
        "safety_score": sim_state["safety_score"],
        "risk_level": sim_state["risk_level"],
        "operator_status": "FATIGUE WARNING" if sim_state["telemetry"]["fatigue_indicator"] >= 0.7 else "NORMAL",
        "weather": {
            "condition": "Sunny",
            "temperature_c": 32,
            "wind_speed_kmh": 11,
            "humidity_pct": 42
        },
        "kpis": {
            "today_tasks": total_tasks_today,
            "completed_tasks": completed_tasks,
            "average_task_time": avg_task_time,
            "safety_alerts": safety_alerts_count,
            "idle_time_min": idle_time_min,
            "machine_utilization": 84.5,
            "fuel_efficiency_lh": fuel_efficiency_lh,
            "training_progress_pct": training_pct
        },
        "active_alerts": sim_state["active_alerts"],
        "safety_disclaimer": settings.SAFETY_DISCLAIMER
    }
