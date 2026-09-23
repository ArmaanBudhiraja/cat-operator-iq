-- CAT OperatorIQ Relational Schema
-- Compatible with PostgreSQL and SQLite

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Operator', -- 'Operator', 'Supervisor'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS operators (
    operator_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    name VARCHAR(150) NOT NULL,
    experience_years REAL NOT NULL DEFAULT 1.0,
    skill_level VARCHAR(50) NOT NULL DEFAULT 'Intermediate', -- Beginner, Intermediate, Expert
    training_score REAL NOT NULL DEFAULT 85.0,
    safety_score REAL NOT NULL DEFAULT 90.0,
    average_task_accuracy REAL NOT NULL DEFAULT 92.0,
    average_task_time REAL NOT NULL DEFAULT 55.0,
    incident_count INTEGER NOT NULL DEFAULT 0,
    fatigue_score REAL NOT NULL DEFAULT 15.0,
    certification_status VARCHAR(50) NOT NULL DEFAULT 'Certified',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(50) PRIMARY KEY,
    machine_type VARCHAR(100) NOT NULL, -- Excavator, Wheel Loader, Dozer, Grader, Dump Truck, Compactor
    machine_model VARCHAR(100) NOT NULL,
    machine_age_years REAL NOT NULL DEFAULT 2.0,
    engine_hours REAL NOT NULL DEFAULT 1200.0,
    maintenance_age_days INTEGER NOT NULL DEFAULT 45,
    fuel_capacity REAL NOT NULL DEFAULT 400.0,
    current_fuel_level REAL NOT NULL DEFAULT 75.0,
    hydraulic_pressure REAL NOT NULL DEFAULT 280.0,
    engine_temperature REAL NOT NULL DEFAULT 88.0,
    engine_rpm REAL NOT NULL DEFAULT 1800.0,
    vibration_level REAL NOT NULL DEFAULT 1.8,
    coolant_temperature REAL NOT NULL DEFAULT 85.0,
    oil_pressure REAL NOT NULL DEFAULT 42.0,
    battery_voltage REAL NOT NULL DEFAULT 24.5,
    load_weight REAL NOT NULL DEFAULT 12.0,
    operating_hours REAL NOT NULL DEFAULT 8.0,
    location VARCHAR(150) NOT NULL DEFAULT 'Site Alpha - Sector 4',
    status VARCHAR(50) NOT NULL DEFAULT 'Operating' -- Operating, Idle, Maintenance, Warning
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    task_type VARCHAR(100) NOT NULL, -- Earth Excavation, Trenching, Material Loading, Grading, Demolition, Compaction, Hauling
    machine_id VARCHAR(50) NOT NULL REFERENCES machines(machine_id),
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    location VARCHAR(150) NOT NULL DEFAULT 'Site Alpha - Sector 4',
    priority VARCHAR(50) NOT NULL DEFAULT 'Medium', -- Low, Medium, High, Critical
    scheduled_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_time_min REAL NOT NULL DEFAULT 60.0,
    predicted_time_min REAL,
    actual_time_min REAL,
    load_cycles INTEGER NOT NULL DEFAULT 15,
    distance REAL NOT NULL DEFAULT 1.2,
    weather VARCHAR(50) NOT NULL DEFAULT 'Sunny',
    operator_skill VARCHAR(50) NOT NULL DEFAULT 'Intermediate',
    machine_age REAL NOT NULL DEFAULT 2.0,
    status VARCHAR(50) NOT NULL DEFAULT 'Scheduled', -- Scheduled, In Progress, Completed, Delayed, Flagged
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS telemetry (
    telemetry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id VARCHAR(50) NOT NULL REFERENCES machines(machine_id),
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    task_id VARCHAR(50) REFERENCES tasks(task_id),
    engine_hours REAL NOT NULL,
    fuel_used_l REAL NOT NULL DEFAULT 15.0,
    load_cycles INTEGER NOT NULL DEFAULT 10,
    idling_time_min REAL NOT NULL DEFAULT 5.0,
    engine_temperature REAL NOT NULL DEFAULT 88.0,
    oil_pressure REAL NOT NULL DEFAULT 42.0,
    hydraulic_pressure REAL NOT NULL DEFAULT 280.0,
    engine_rpm REAL NOT NULL DEFAULT 1850.0,
    vibration REAL NOT NULL DEFAULT 1.8,
    coolant_temperature REAL NOT NULL DEFAULT 85.0,
    battery_voltage REAL NOT NULL DEFAULT 24.4,
    load_weight REAL NOT NULL DEFAULT 14.5,
    seatbelt_status VARCHAR(50) NOT NULL DEFAULT 'Fastened', -- Fastened, Unfastened
    proximity_distance_m REAL NOT NULL DEFAULT 12.0,
    worker_detected BOOLEAN NOT NULL DEFAULT 0,
    safety_alert_triggered BOOLEAN NOT NULL DEFAULT 0,
    fatigue_indicator REAL NOT NULL DEFAULT 0.15,
    weather VARCHAR(50) NOT NULL DEFAULT 'Sunny'
);

CREATE TABLE IF NOT EXISTS safety_events (
    event_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id VARCHAR(50) NOT NULL REFERENCES machines(machine_id),
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    event_type VARCHAR(100) NOT NULL, -- Seatbelt Violation, Proximity Hazard, High Fatigue, Excessive Idling, Overheating, High Vibration
    severity VARCHAR(50) NOT NULL, -- Low, Medium, High, Critical
    risk_score REAL NOT NULL,
    details TEXT,
    acknowledged BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id VARCHAR(50) NOT NULL REFERENCES machines(machine_id),
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL, -- Low, Medium, High, Critical
    description TEXT NOT NULL,
    location VARCHAR(150) NOT NULL,
    resolved BOOLEAN NOT NULL DEFAULT 0,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS anomalies (
    anomaly_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    machine_id VARCHAR(50) NOT NULL REFERENCES machines(machine_id),
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    anomaly_score REAL NOT NULL,
    risk_level VARCHAR(50) NOT NULL, -- Low, Medium, High, Critical
    reason TEXT NOT NULL,
    factors TEXT, -- JSON formatted explanation factors
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_courses (
    course_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(100) NOT NULL, -- Safety, Machine Operation, Fuel Efficiency, Maintenance Awareness, Emergency Procedures, Productivity
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(50) NOT NULL DEFAULT 'Intermediate', -- Beginner, Intermediate, Advanced
    duration_min INTEGER NOT NULL DEFAULT 30,
    video_url VARCHAR(255),
    quiz_data TEXT, -- JSON string containing quiz questions, options, correct answers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_progress (
    progress_id VARCHAR(50) PRIMARY KEY,
    operator_id VARCHAR(50) NOT NULL REFERENCES operators(operator_id),
    course_id VARCHAR(50) NOT NULL REFERENCES training_courses(course_id),
    completion_status VARCHAR(50) NOT NULL DEFAULT 'Not Started', -- Not Started, In Progress, Completed
    score REAL DEFAULT 0.0,
    attempts INTEGER DEFAULT 0,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id VARCHAR(50) PRIMARY KEY,
    task_id VARCHAR(50) NOT NULL REFERENCES tasks(task_id),
    predicted_time_min REAL NOT NULL,
    confidence_lower_min REAL NOT NULL,
    confidence_upper_min REAL NOT NULL,
    factors_json TEXT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id VARCHAR(50) PRIMARY KEY,
    machine_id VARCHAR(50) REFERENCES machines(machine_id),
    operator_id VARCHAR(50) REFERENCES operators(operator_id),
    category VARCHAR(100) NOT NULL, -- Safety, Maintenance, Efficiency, Training
    priority VARCHAR(50) NOT NULL DEFAULT 'Medium', -- Low, Medium, High, Critical
    title VARCHAR(200) NOT NULL,
    recommendation TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_telemetry_machine_time ON telemetry(machine_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_operator_time ON telemetry(operator_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_task ON telemetry(task_id);
CREATE INDEX IF NOT EXISTS idx_safety_events_machine ON safety_events(machine_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_safety_events_operator ON safety_events(operator_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_incidents_machine ON incidents(machine_id);
CREATE INDEX IF NOT EXISTS idx_incidents_operator ON incidents(operator_id);
CREATE INDEX IF NOT EXISTS idx_tasks_machine ON tasks(machine_id);
CREATE INDEX IF NOT EXISTS idx_tasks_operator ON tasks(operator_id);
CREATE INDEX IF NOT EXISTS idx_anomalies_machine ON anomalies(machine_id);
