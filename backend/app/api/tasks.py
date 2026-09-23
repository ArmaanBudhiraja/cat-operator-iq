from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.db.database import get_db
from backend.app.db.models import Task, Machine, Operator
from backend.app.schemas.schemas import TaskResponse, TaskStatusUpdate
from backend.app.services.prediction_service import PredictionService

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get("", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    operator_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if operator_id:
        query = query.filter(Task.operator_id == operator_id)
    tasks = query.order_by(Task.scheduled_start.desc()).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_detail(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # Generate ML prediction details
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
    prediction = PredictionService.predict_task_time(task_dict)

    res = TaskResponse.from_orm(task)
    res.prediction_details = prediction
    return res

@router.put("/{task_id}/status")
def update_task_status(task_id: str, update: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task.status = update.status
    if update.actual_time_min is not None:
        task.actual_time_min = update.actual_time_min
    elif update.status == "Completed" and not task.actual_time_min:
        task.actual_time_min = task.predicted_time_min or task.estimated_time_min

    db.commit()
    db.refresh(task)
    return {"message": f"Task {task_id} updated to {update.status}", "task": TaskResponse.from_orm(task)}
