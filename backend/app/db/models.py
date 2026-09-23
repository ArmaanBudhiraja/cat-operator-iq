from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Index
)
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    role = Column(String(50), default="Operator") # Operator, Supervisor
    created_at = Column(DateTime, default=datetime.utcnow)

    operators = relationship("Operator", back_populates="user")

class Operator(Base):
    __tablename__ = "operators"

    operator_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=True)
    name = Column(String(150), nullable=False)
    experience_years = Column(Float, default=1.0)
    skill_level = Column(String(50), default="Intermediate") # Beginner, Intermediate, Expert
    training_score = Column(Float, default=85.0)
    safety_score = Column(Float, default=90.0)
    average_task_accuracy = Column(Float, default=92.0)
    average_task_time = Column(Float, default=55.0)
    incident_count = Column(Integer, default=0)
    fatigue_score = Column(Float, default=15.0)
    certification_status = Column(String(50), default="Certified")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="operators")
    tasks = relationship("Task", back_populates="operator")
    telemetries = relationship("Telemetry", back_populates="operator")
    safety_events = relationship("SafetyEvent", back_populates="operator")
    incidents = relationship("Incident", back_populates="operator")
    training_progresses = relationship("TrainingProgress", back_populates="operator")

class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(String(50), primary_key=True)
    machine_type = Column(String(100), nullable=False) # Excavator, Wheel Loader, Dozer, Grader, Dump Truck, Compactor
    machine_model = Column(String(100), nullable=False)
    machine_age_years = Column(Float, default=2.0)
    engine_hours = Column(Float, default=1200.0)
    maintenance_age_days = Column(Integer, default=45)
    fuel_capacity = Column(Float, default=400.0)
    current_fuel_level = Column(Float, default=75.0) # %
    hydraulic_pressure = Column(Float, default=280.0) # bar
    engine_temperature = Column(Float, default=88.0) # °C
    engine_rpm = Column(Float, default=1800.0)
    vibration_level = Column(Float, default=1.8) # mm/s
    coolant_temperature = Column(Float, default=85.0) # °C
    oil_pressure = Column(Float, default=42.0) # psi
    battery_voltage = Column(Float, default=24.5) # V
    load_weight = Column(Float, default=12.0) # tonnes
    operating_hours = Column(Float, default=8.0)
    location = Column(String(150), default="Site Alpha - Sector 4")
    status = Column(String(50), default="Operating") # Operating, Idle, Maintenance, Warning

    tasks = relationship("Task", back_populates="machine")
    telemetries = relationship("Telemetry", back_populates="machine")
    safety_events = relationship("SafetyEvent", back_populates="machine")
    incidents = relationship("Incident", back_populates="machine")
    anomalies = relationship("Anomaly", back_populates="machine")

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String(50), primary_key=True)
    task_type = Column(String(100), nullable=False) # Earth Excavation, Trenching, Material Loading, Grading, Demolition, Compaction, Hauling
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=False)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=False)
    location = Column(String(150), default="Site Alpha - Sector 4")
    priority = Column(String(50), default="Medium") # Low, Medium, High, Critical
    scheduled_start = Column(DateTime, default=datetime.utcnow)
    estimated_time_min = Column(Float, default=60.0)
    predicted_time_min = Column(Float, nullable=True)
    actual_time_min = Column(Float, nullable=True)
    load_cycles = Column(Integer, default=15)
    distance = Column(Float, default=1.2) # km
    weather = Column(String(50), default="Sunny")
    operator_skill = Column(String(50), default="Intermediate")
    machine_age = Column(Float, default=2.0)
    status = Column(String(50), default="Scheduled") # Scheduled, In Progress, Completed, Delayed, Flagged
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="tasks")
    operator = relationship("Operator", back_populates="tasks")
    telemetries = relationship("Telemetry", back_populates="task")
    prediction = relationship("Prediction", back_populates="task", uselist=False)

class Telemetry(Base):
    __tablename__ = "telemetry"

    telemetry_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=False, index=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=False, index=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"), nullable=True, index=True)
    engine_hours = Column(Float, nullable=False)
    fuel_used_l = Column(Float, default=15.0)
    load_cycles = Column(Integer, default=10)
    idling_time_min = Column(Float, default=5.0)
    engine_temperature = Column(Float, default=88.0)
    oil_pressure = Column(Float, default=42.0)
    hydraulic_pressure = Column(Float, default=280.0)
    engine_rpm = Column(Float, default=1850.0)
    vibration = Column(Float, default=1.8)
    coolant_temperature = Column(Float, default=85.0)
    battery_voltage = Column(Float, default=24.4)
    load_weight = Column(Float, default=14.5)
    seatbelt_status = Column(String(50), default="Fastened") # Fastened, Unfastened
    proximity_distance_m = Column(Float, default=12.0)
    worker_detected = Column(Boolean, default=False)
    safety_alert_triggered = Column(Boolean, default=False)
    fatigue_indicator = Column(Float, default=0.15)
    weather = Column(String(50), default="Sunny")

    machine = relationship("Machine", back_populates="telemetries")
    operator = relationship("Operator", back_populates="telemetries")
    task = relationship("Task", back_populates="telemetries")

class SafetyEvent(Base):
    __tablename__ = "safety_events"

    event_id = Column(String(50), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=False, index=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False) # Seatbelt Violation, Proximity Hazard, High Fatigue, Excessive Idling, Overheating, High Vibration
    severity = Column(String(50), nullable=False) # Low, Medium, High, Critical
    risk_score = Column(Float, nullable=False)
    details = Column(Text, nullable=True)
    acknowledged = Column(Boolean, default=False)

    machine = relationship("Machine", back_populates="safety_events")
    operator = relationship("Operator", back_populates="safety_events")

class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(String(50), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=False, index=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=False, index=True)
    incident_type = Column(String(100), nullable=False) # Seatbelt Violation, Proximity Hazard, Overheating, Excessive Idling, Fatigue, Mechanical Anomaly, Other
    severity = Column(String(50), nullable=False) # Low, Medium, High, Critical
    description = Column(Text, nullable=False)
    location = Column(String(150), nullable=False)
    resolved = Column(Boolean, default=False)
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="incidents")
    operator = relationship("Operator", back_populates="incidents")

class Anomaly(Base):
    __tablename__ = "anomalies"

    anomaly_id = Column(String(50), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=False, index=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=True)
    anomaly_score = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False) # Low, Medium, High, Critical
    reason = Column(Text, nullable=False)
    factors = Column(Text, nullable=True) # JSON formatted string
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="anomalies")

class TrainingCourse(Base):
    __tablename__ = "training_courses"

    course_id = Column(String(50), primary_key=True)
    category = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    duration_min = Column(Integer, default=30)
    video_url = Column(String(255), nullable=True)
    quiz_data = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    progresses = relationship("TrainingProgress", back_populates="course")

class TrainingProgress(Base):
    __tablename__ = "training_progress"

    progress_id = Column(String(50), primary_key=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=False)
    course_id = Column(String(50), ForeignKey("training_courses.course_id"), nullable=False)
    completion_status = Column(String(50), default="Not Started") # Not Started, In Progress, Completed
    score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    operator = relationship("Operator", back_populates="training_progresses")
    course = relationship("TrainingCourse", back_populates="progresses")

class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(String(50), primary_key=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"), nullable=False, unique=True)
    predicted_time_min = Column(Float, nullable=False)
    confidence_lower_min = Column(Float, nullable=False)
    confidence_upper_min = Column(Float, nullable=False)
    factors_json = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="prediction")

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(String(50), primary_key=True)
    machine_id = Column(String(50), ForeignKey("machines.machine_id"), nullable=True)
    operator_id = Column(String(50), ForeignKey("operators.operator_id"), nullable=True)
    category = Column(String(100), nullable=False) # Safety, Maintenance, Efficiency, Training
    priority = Column(String(50), default="Medium")
    title = Column(String(200), nullable=False)
    recommendation = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
