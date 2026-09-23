from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Task
from backend.app.services.prediction_service import PredictionService
from ml.model_registry import get_evaluation_metrics

router = APIRouter(prefix="/api/predictions", tags=["ML Predictions & Analytics"])

@router.get("/task/{task_id}")
def get_task_prediction(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_dict = {
        "task_id": task.task_id,
        "task_type": task.task_type,
        "weather": task.weather,
        "operator_skill": task.operator_skill,
        "machine_age": task.machine_age,
        "load_cycles": task.load_cycles,
        "distance": task.distance,
        "estimated_time_min": task.estimated_time_min
    }
    return PredictionService.predict_task_time(task_dict)

@router.get("/metrics")
def get_model_performance_metrics():
    """
    Returns authentic training evaluation metrics calculated from validation splits.
    Clearly specifies synthetic demonstration telemetry data source.
    """
    return get_evaluation_metrics()
