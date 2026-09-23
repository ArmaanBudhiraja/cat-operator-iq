from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Machine, Telemetry
from backend.app.schemas.schemas import MachineResponse

router = APIRouter(prefix="/api/machines", tags=["Machines"])

def calculate_machine_health(machine: Machine) -> tuple[float, dict[str, float]]:
    # Formula: 25% temp + 25% vib + 25% oil + 25% maint
    temp_score = max(0.0, 100.0 - max(0.0, (machine.engine_temperature - 85.0) * 3.0))
    vib_score = max(0.0, 100.0 - max(0.0, (machine.vibration_level - 1.5) * 28.0))
    oil_score = max(0.0, 100.0 - max(0.0, (45.0 - machine.oil_pressure) * 3.5))
    maint_score = max(0.0, 100.0 - (machine.maintenance_age_days * 0.45))

    composite = round(0.25 * temp_score + 0.25 * vib_score + 0.25 * oil_score + 0.25 * maint_score, 1)
    factors = {
        "temperature_health": round(temp_score, 1),
        "vibration_health": round(vib_score, 1),
        "oil_pressure_health": round(oil_score, 1),
        "maintenance_health": round(maint_score, 1)
    }
    return composite, factors

@router.get("", response_model=list[MachineResponse])
def get_machines(db: Session = Depends(get_db)):
    machines = db.query(Machine).all()
    results = []
    for m in machines:
        h_score, h_factors = calculate_machine_health(m)
        m_dict = MachineResponse.from_orm(m)
        m_dict.health_score = h_score
        m_dict.health_factors = h_factors
        results.append(m_dict)
    return results

@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine_detail(machine_id: str, db: Session = Depends(get_db)):
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")

    h_score, h_factors = calculate_machine_health(machine)
    res = MachineResponse.from_orm(machine)
    res.health_score = h_score
    res.health_factors = h_factors
    return res

@router.get("/{machine_id}/telemetry")
def get_machine_telemetry_history(machine_id: str, limit: int = 30, db: Session = Depends(get_db)):
    records = (
        db.query(Telemetry)
        .filter(Telemetry.machine_id == machine_id)
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
        .all()
    )
    # Return reversed to show chronological progression in sparklines/charts
    return list(reversed(records))
