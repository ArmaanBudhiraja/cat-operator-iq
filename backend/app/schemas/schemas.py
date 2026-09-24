from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Any

# Telemetry Schemas
class TelemetryItem(BaseModel):
    timestamp: datetime | str
    machine_id: str
    operator_id: str
    task_id: str | None = None
    engine_hours: float
    fuel_used_l: float
    load_cycles: int
    idling_time_min: float
    engine_temperature: float
    oil_pressure: float
    hydraulic_pressure: float
    engine_rpm: float
    vibration: float
    coolant_temperature: float
    battery_voltage: float
    load_weight: float
    seatbelt_status: str
    proximity_distance_m: float
    worker_detected: bool
    safety_alert_triggered: bool
    fatigue_indicator: float
    weather: str

class LiveTelemetryState(BaseModel):
    telemetry: TelemetryItem
    safety_score: float
    risk_level: str # LOW, MEDIUM, HIGH, CRITICAL
    active_alerts: list[dict[str, Any]]
    radar_objects: list[dict[str, Any]]
    anomaly_detected: bool
    anomaly_details: dict[str, Any] | None = None

# Machine Schemas
class MachineResponse(BaseModel):
    machine_id: str
    machine_type: str
    machine_model: str
    machine_age_years: float
    engine_hours: float
    maintenance_age_days: int
    fuel_capacity: float
    current_fuel_level: float
    hydraulic_pressure: float
    engine_temperature: float
    engine_rpm: float
    vibration_level: float
    coolant_temperature: float
    oil_pressure: float
    battery_voltage: float
    load_weight: float
    operating_hours: float
    location: str
    status: str
    health_score: float | None = None
    health_factors: dict[str, float] | None = None

    model_config = ConfigDict(from_attributes=True)

# Operator Schemas
class OperatorResponse(BaseModel):
    operator_id: str
    name: str
    experience_years: float
    skill_level: str
    training_score: float
    safety_score: float
    average_task_accuracy: float
    average_task_time: float
    incident_count: int
    fatigue_score: float
    certification_status: str

    model_config = ConfigDict(from_attributes=True)

# Task Schemas
class TaskPredictionFactor(BaseModel):
    name: str
    delta_min: float
    reason: str

class TaskPredictionResponse(BaseModel):
    task_id: str
    predicted_time_min: float
    confidence_lower_min: float
    confidence_upper_min: float
    factors: list[TaskPredictionFactor]
    model_name: str

class TaskResponse(BaseModel):
    task_id: str
    task_type: str
    machine_id: str
    operator_id: str
    location: str
    priority: str
    scheduled_start: datetime | str
    estimated_time_min: float
    predicted_time_min: float | None = None
    actual_time_min: float | None = None
    load_cycles: int
    distance: float
    weather: str
    operator_skill: str
    machine_age: float
    status: str
    prediction_details: TaskPredictionResponse | None = None

    model_config = ConfigDict(from_attributes=True)

class TaskStatusUpdate(BaseModel):
    status: str # In Progress, Completed, Delayed, Flagged
    actual_time_min: float | None = None

# Safety Schemas
class SafetyEventResponse(BaseModel):
    event_id: str
    timestamp: datetime | str
    machine_id: str
    operator_id: str
    event_type: str
    severity: str
    risk_score: float
    details: str | None = None
    acknowledged: bool = False

    model_config = ConfigDict(from_attributes=True)

# Incident Schemas
class IncidentCreate(BaseModel):
    machine_id: str
    operator_id: str
    incident_type: str
    severity: str
    description: str
    location: str

class IncidentUpdate(BaseModel):
    resolved: bool
    resolution: str | None = None

class IncidentResponse(BaseModel):
    incident_id: str
    timestamp: datetime | str
    machine_id: str
    operator_id: str
    incident_type: str
    severity: str
    description: str
    location: str
    resolved: bool
    resolution: str | None = None
    created_at: datetime | str

    model_config = ConfigDict(from_attributes=True)

# Anomaly Schemas
class AnomalyResponse(BaseModel):
    anomaly_id: str
    timestamp: datetime | str
    machine_id: str
    operator_id: str | None = None
    anomaly_score: float
    risk_level: str
    reason: str
    factors: list[str] | dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)

# Training Schemas
class QuizQuestion(BaseModel):
    id: int
    question: str
    options: list[str]
    answer_idx: int

class TrainingCourseResponse(BaseModel):
    course_id: str
    category: str
    title: str
    description: str
    difficulty: str
    duration_min: int
    video_url: str | None = None
    quiz_questions: list[QuizQuestion] | None = None
    completion_status: str = "Not Started"
    score: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class QuizSubmission(BaseModel):
    operator_id: str
    answers: dict[int, int] # question_id -> selected_option_index

# AI Assistant Schemas
class AssistantQueryRequest(BaseModel):
    query: str
    operator_id: str = "OP001"
    machine_id: str = "EXC001"

class AssistantQueryResponse(BaseModel):
    question: str
    answer: str
    evidence: list[str]
    recommended_next_step: str
    safety_disclaimer: str
    citations: list[str] = []
    is_fallback: bool = False
    ai_provider: str = "Live AI"
    fallback_reason: str | None = None

# Simulation Trigger
class SimulationHazardRequest(BaseModel):
    hazard_type: str # worker_proximity, seatbelt_unfastened, vibration_spike, overheating, idle_excess
    machine_id: str = "EXC001"
    operator_id: str = "OP001"

# Dashboard Response
class DashboardKpis(BaseModel):
    today_tasks: int
    completed_tasks: int
    average_task_time: float
    safety_alerts: int
    idle_time_min: float
    machine_utilization: float
    fuel_efficiency_lh: float
    training_progress_pct: float

class DashboardResponse(BaseModel):
    greeting: str
    operator_name: str
    current_machine_id: str
    current_task: TaskResponse | None = None
    task_progress_pct: float
    estimated_remaining_time_min: float
    machine_health_pct: float
    safety_status: str # SAFE, WARNING, HIGH RISK, CRITICAL
    safety_score: float
    operator_status: str # NORMAL, FATIGUE WARNING
    weather: dict[str, Any]
    kpis: DashboardKpis
    active_alerts: list[dict[str, Any]]
    safety_disclaimer: str
