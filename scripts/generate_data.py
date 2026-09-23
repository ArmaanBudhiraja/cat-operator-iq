import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Configurable counts via environment variables
NUM_TELEMETRY = int(os.getenv("NUM_TELEMETRY", 10000))
NUM_TASKS = int(os.getenv("NUM_TASKS", 2000))
NUM_SAFETY_EVENTS = int(os.getenv("NUM_SAFETY_EVENTS", 500))
NUM_INCIDENTS = int(os.getenv("NUM_INCIDENTS", 300))
NUM_OPERATORS = int(os.getenv("NUM_OPERATORS", 100))
NUM_MACHINES = int(os.getenv("NUM_MACHINES", 50))
NUM_TRAINING_RECORDS = int(os.getenv("NUM_TRAINING_RECORDS", 500))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

MACHINE_TYPES_MODELS = {
    "Excavator": ["CAT 320 Next Gen", "CAT 336 Heavy Duty", "CAT 349 Extreme"],
    "Wheel Loader": ["CAT 950M High Lift", "CAT 966M", "CAT 980M Quarry"],
    "Dozer": ["CAT D6 XE Electric", "CAT D8T Heavy", "CAT D10 Dozer"],
    "Grader": ["CAT 140 Motor Grader", "CAT 160M AWD"],
    "Dump Truck": ["CAT 730 Articulated", "CAT 745 Extreme Haul"],
    "Compactor": ["CAT CS56B Soil", "CAT CB68B Asphalt"]
}

TASK_TYPES = [
    "Earth Excavation", "Trenching", "Material Loading",
    "Grading", "Demolition", "Compaction", "Hauling"
]

BASE_TASK_TIMES = {
    "Earth Excavation": 60.0,
    "Trenching": 75.0,
    "Material Loading": 45.0,
    "Grading": 90.0,
    "Demolition": 110.0,
    "Compaction": 50.0,
    "Hauling": 40.0
}

WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Windy", "Rainy", "Storm"]
WEATHER_WEIGHTS = [0.45, 0.25, 0.12, 0.13, 0.05]

FIRST_NAMES = [
    "Marcus", "Elena", "Carlos", "Aisha", "Jake", "Sarah", "David", "Li",
    "Vikram", "Hannah", "James", "Maria", "Kenji", "Fatima", "Chloe", "Mateo"
]
LAST_NAMES = [
    "Miller", "Vance", "Torres", "Khan", "O'Connor", "Chen", "Kowalski", "Patel",
    "Gomez", "Dubois", "Sato", "Al-Mansoor", "Novak", "Schmidt", "Silva", "Johnson"
]

LOCATIONS = [
    "Site Alpha - Sector 1 Quarry",
    "Site Alpha - Sector 4 Foundation",
    "Site Beta - East Trenching Zone",
    "Site Beta - North Overpass",
    "Site Gamma - River Basin Basin Prep",
    "Site Delta - Highway Interchange"
]

def generate_synthetic_dataset():
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)

    print(f"Generating synthetic industrial dataset (Seed: {RANDOM_SEED})...")

    # 1. GENERATE OPERATORS
    operators_list = []
    for i in range(1, NUM_OPERATORS + 1):
        op_id = f"OP{i:03d}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        exp_years = round(float(np.random.exponential(scale=5.0) + 0.5), 1)
        exp_years = min(35.0, exp_years)

        if exp_years < 2.5:
            skill = "Beginner"
            safety_score = round(float(np.random.normal(78.0, 7.0)), 1)
            train_score = round(float(np.random.normal(80.0, 6.0)), 1)
            avg_accuracy = round(float(np.random.normal(84.0, 5.0)), 1)
            incident_cnt = int(np.random.poisson(1.8))
        elif exp_years < 7.0:
            skill = "Intermediate"
            safety_score = round(float(np.random.normal(88.0, 5.0)), 1)
            train_score = round(float(np.random.normal(89.0, 5.0)), 1)
            avg_accuracy = round(float(np.random.normal(92.0, 4.0)), 1)
            incident_cnt = int(np.random.poisson(0.8))
        else:
            skill = "Expert"
            safety_score = round(float(np.random.normal(95.0, 3.5)), 1)
            train_score = round(float(np.random.normal(96.0, 3.0)), 1)
            avg_accuracy = round(float(np.random.normal(97.0, 2.5)), 1)
            incident_cnt = int(np.random.poisson(0.3))

        safety_score = min(100.0, max(50.0, safety_score))
        train_score = min(100.0, max(50.0, train_score))
        avg_accuracy = min(100.0, max(60.0, avg_accuracy))
        avg_time = round(float(np.random.normal(55.0 - (exp_years * 0.4), 6.0)), 1)
        fatigue = round(float(np.clip(np.random.normal(18.0, 8.0), 5.0, 85.0)), 1)
        cert_status = "Certified" if train_score >= 75.0 else "Pending Recertification"

        operators_list.append({
            "operator_id": op_id,
            "name": name,
            "experience_years": exp_years,
            "skill_level": skill,
            "training_score": train_score,
            "safety_score": safety_score,
            "average_task_accuracy": avg_accuracy,
            "average_task_time": avg_time,
            "incident_count": incident_cnt,
            "fatigue_score": fatigue,
            "certification_status": cert_status
        })

    # Hardcode OP001 as Marcus Vance (our demo operator)
    operators_list[0] = {
        "operator_id": "OP001",
        "name": "Marcus Vance",
        "experience_years": 8.5,
        "skill_level": "Expert",
        "training_score": 94.0,
        "safety_score": 92.5,
        "average_task_accuracy": 96.0,
        "average_task_time": 52.0,
        "incident_count": 1,
        "fatigue_score": 15.0,
        "certification_status": "Certified"
    }
    df_operators = pd.DataFrame(operators_list)
    df_operators.to_csv(DATA_DIR / "operators.csv", index=False)
    print(f"Generated {len(df_operators)} operators -> {DATA_DIR / 'operators.csv'}")

    # 2. GENERATE MACHINES
    machines_list = []
    types_list = list(MACHINE_TYPES_MODELS.keys())
    for i in range(1, NUM_MACHINES + 1):
        m_type = types_list[(i - 1) % len(types_list)]
        prefix = m_type[:3].upper()
        m_id = f"{prefix}{i:03d}"
        m_model = random.choice(MACHINE_TYPES_MODELS[m_type])

        age_years = round(float(np.clip(np.random.exponential(3.0) + 0.5, 0.5, 12.0)), 1)
        eng_hours = round(float(age_years * np.random.uniform(700.0, 1100.0)), 1)
        maint_days = int(np.random.randint(5, 120))

        # Older machines have slightly elevated baseline vibration and temp
        vib_base = round(float(1.5 + (age_years * 0.12) + np.random.normal(0, 0.15)), 2)
        temp_base = round(float(84.0 + (age_years * 0.7) + np.random.normal(0, 1.5)), 1)
        oil_base = round(float(45.0 - (age_years * 0.6) + np.random.normal(0, 1.2)), 1)
        fuel_lvl = round(float(np.random.uniform(30.0, 98.0)), 1)
        fuel_cap = 450.0 if "Excavator" in m_type or "Dump" in m_type else 320.0
        hydr_press = round(float(np.random.normal(280.0, 8.0)), 1)
        status = "Operating" if np.random.random() > 0.12 else ("Maintenance" if np.random.random() > 0.5 else "Idle")

        machines_list.append({
            "machine_id": m_id,
            "machine_type": m_type,
            "machine_model": m_model,
            "machine_age_years": age_years,
            "engine_hours": eng_hours,
            "maintenance_age_days": maint_days,
            "fuel_capacity": fuel_cap,
            "current_fuel_level": fuel_lvl,
            "hydraulic_pressure": hydr_press,
            "engine_temperature": temp_base,
            "engine_rpm": 1820.0,
            "vibration_level": vib_base,
            "coolant_temperature": round(temp_base - 3.5, 1),
            "oil_pressure": oil_base,
            "battery_voltage": 24.6,
            "load_weight": round(float(np.random.uniform(8.0, 22.0)), 1),
            "operating_hours": 8.0,
            "location": random.choice(LOCATIONS),
            "status": status
        })

    # Hardcode EXC001 as primary demo machine
    machines_list[0] = {
        "machine_id": "EXC001",
        "machine_type": "Excavator",
        "machine_model": "CAT 336 Heavy Duty",
        "machine_age_years": 2.4,
        "engine_hours": 2150.0,
        "maintenance_age_days": 28,
        "fuel_capacity": 450.0,
        "current_fuel_level": 78.5,
        "hydraulic_pressure": 282.0,
        "engine_temperature": 88.5,
        "engine_rpm": 1850.0,
        "vibration_level": 1.75,
        "coolant_temperature": 85.0,
        "oil_pressure": 43.5,
        "battery_voltage": 24.8,
        "load_weight": 14.5,
        "operating_hours": 8.5,
        "location": "Site Alpha - Sector 4 Foundation",
        "status": "Operating"
    }
    df_machines = pd.DataFrame(machines_list)
    df_machines.to_csv(DATA_DIR / "machine.csv", index=False)
    print(f"Generated {len(df_machines)} machines -> {DATA_DIR / 'machine.csv'}")

    # 3. GENERATE TASKS
    tasks_list = []
    base_time = datetime.now() - timedelta(days=60)
    for i in range(1, NUM_TASKS + 1):
        t_id = f"T{i:04d}"
        t_type = random.choice(TASK_TYPES)
        machine = random.choice(machines_list)
        operator = random.choice(operators_list)
        weather = np.random.choice(WEATHER_CONDITIONS, p=WEATHER_WEIGHTS)

        base_duration = BASE_TASK_TIMES[t_type]
        cycles = int(np.random.randint(8, 30))
        dist_km = round(float(np.random.uniform(0.4, 4.5)), 2)

        # Weather modifier
        w_mult = {"Sunny": 0.96, "Cloudy": 1.0, "Windy": 1.06, "Rainy": 1.22, "Storm": 1.45}[weather]
        # Operator modifier
        s_mult = {"Beginner": 1.18, "Intermediate": 1.0, "Expert": 0.88}[operator["skill_level"]]
        # Age modifier
        a_mult = 1.0 + (machine["machine_age_years"] * 0.02)

        estimated_time = round(base_duration * 1.0, 1)
        actual_time = round(base_duration * w_mult * s_mult * a_mult * np.random.normal(1.0, 0.06), 1)
        actual_time = max(15.0, actual_time)

        # Predicted time is close to actual with slight ML noise
        predicted_time = round(base_duration * w_mult * s_mult * a_mult * np.random.normal(1.0, 0.03), 1)

        task_time_offset = base_time + timedelta(hours=i * 0.7)
        status = "Completed" if i <= NUM_TASKS - 15 else ("In Progress" if i == NUM_TASKS - 14 else "Scheduled")
        priority = random.choice(["Low", "Medium", "High", "Critical"])

        tasks_list.append({
            "task_id": t_id,
            "task_type": t_type,
            "machine_id": machine["machine_id"],
            "operator_id": operator["operator_id"],
            "location": machine["location"],
            "priority": priority,
            "scheduled_start": task_time_offset.strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_time_min": estimated_time,
            "predicted_time_min": predicted_time,
            "actual_time_min": actual_time if status == "Completed" else None,
            "load_cycles": cycles,
            "distance": dist_km,
            "weather": weather,
            "operator_skill": operator["skill_level"],
            "machine_age": machine["machine_age_years"],
            "status": status
        })

    # Hardcode current task for demo
    tasks_list[-15] = {
        "task_id": "T001",
        "task_type": "Earth Excavation",
        "machine_id": "EXC001",
        "operator_id": "OP001",
        "location": "Site Alpha - Sector 4 Foundation",
        "priority": "High",
        "scheduled_start": datetime.now().strftime("%Y-%m-%d 08:00:00"),
        "estimated_time_min": 60.0,
        "predicted_time_min": 54.0,
        "actual_time_min": None,
        "load_cycles": 18,
        "distance": 1.2,
        "weather": "Sunny",
        "operator_skill": "Expert",
        "machine_age": 2.4,
        "status": "In Progress"
    }

    df_tasks = pd.DataFrame(tasks_list)
    df_tasks.to_csv(DATA_DIR / "tasks.csv", index=False)
    print(f"Generated {len(df_tasks)} tasks -> {DATA_DIR / 'tasks.csv'}")

    # 4. GENERATE TELEMETRY
    telemetry_list = []
    telemetry_time = datetime.now() - timedelta(days=20)
    for i in range(1, NUM_TELEMETRY + 1):
        m = random.choice(machines_list)
        op = random.choice(operators_list)
        t = random.choice(tasks_list)

        t_time = telemetry_time + timedelta(minutes=i * 2.8)
        eng_h = m["engine_hours"] + (i * 0.05)
        fuel_used = round(float(np.random.uniform(8.0, 32.0)), 1)
        cycles = int(np.random.randint(5, 25))
        weather = np.random.choice(WEATHER_CONDITIONS, p=WEATHER_WEIGHTS)

        # Inject realistic conditional anomalies/safety situations
        is_seatbelt_unfastened = (np.random.random() < 0.035)
        worker_close = (np.random.random() < 0.045)
        distance = round(float(np.random.uniform(1.2, 5.8)), 1) if worker_close else round(float(np.random.uniform(7.0, 25.0)), 1)
        excessive_idle = (np.random.random() < 0.06)
        idle_min = round(float(np.random.uniform(35.0, 75.0)), 1) if excessive_idle else round(float(np.random.exponential(6.0)), 1)
        overheat = (np.random.random() < 0.03)
        eng_temp = round(float(np.random.uniform(106.0, 118.0)), 1) if overheat else round(float(np.random.normal(88.0, 4.0)), 1)
        abnormal_vib = (np.random.random() < 0.035)
        vib = round(float(np.random.uniform(3.9, 6.5)), 2) if abnormal_vib else round(float(np.random.normal(1.8, 0.3)), 2)
        oil_press = round(float(np.random.uniform(22.0, 30.0)), 1) if abnormal_vib else round(float(np.random.normal(42.0, 3.0)), 1)
        fatigue = round(float(np.clip(np.random.exponential(0.18), 0.05, 0.95)), 2)

        seatbelt = "Unfastened" if is_seatbelt_unfastened else "Fastened"
        worker_detected = worker_close
        safety_alert = is_seatbelt_unfastened or (worker_close and distance <= 3.0) or overheat or abnormal_vib or (fatigue >= 0.75)

        telemetry_list.append({
            "timestamp": t_time.strftime("%Y-%m-%d %H:%M:%S"),
            "machine_id": m["machine_id"],
            "operator_id": op["operator_id"],
            "task_id": t["task_id"],
            "engine_hours": round(eng_h, 1),
            "fuel_used_l": fuel_used,
            "load_cycles": cycles,
            "idling_time_min": idle_min,
            "engine_temperature": eng_temp,
            "oil_pressure": oil_press,
            "hydraulic_pressure": round(float(np.random.normal(280.0, 12.0)), 1),
            "engine_rpm": round(float(np.random.normal(1850.0, 90.0)), 1),
            "vibration": vib,
            "coolant_temperature": round(eng_temp - 3.5, 1),
            "battery_voltage": round(float(np.random.normal(24.5, 0.4)), 1),
            "load_weight": round(float(np.random.uniform(8.0, 24.0)), 1),
            "seatbelt_status": seatbelt,
            "proximity_distance_m": distance,
            "worker_detected": worker_detected,
            "safety_alert_triggered": safety_alert,
            "fatigue_indicator": fatigue,
            "weather": weather
        })

    df_telemetry = pd.DataFrame(telemetry_list)
    df_telemetry.to_csv(DATA_DIR / "telemetry.csv", index=False)
    print(f"Generated {len(df_telemetry)} telemetry records -> {DATA_DIR / 'telemetry.csv'}")

    # 5. GENERATE SAFETY EVENTS
    safety_events_list = []
    event_types = [
        ("Seatbelt Violation", "HIGH", 70.0),
        ("Proximity Hazard", "CRITICAL", 85.0),
        ("High Fatigue", "HIGH", 65.0),
        ("Excessive Idling", "MEDIUM", 45.0),
        ("Overheating", "HIGH", 75.0),
        ("High Vibration", "HIGH", 72.0)
    ]
    for i in range(1, NUM_SAFETY_EVENTS + 1):
        ev_id = f"SE{i:04d}"
        ev_type, default_sev, score_base = random.choice(event_types)
        m = random.choice(machines_list)
        op = random.choice(operators_list)
        sev = default_sev if np.random.random() > 0.2 else "MEDIUM"
        score = round(float(score_base + np.random.normal(0, 5.0)), 1)
        score = min(100.0, max(25.0, score))
        ev_time = datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(5, 1440))

        safety_events_list.append({
            "event_id": ev_id,
            "timestamp": ev_time.strftime("%Y-%m-%d %H:%M:%S"),
            "machine_id": m["machine_id"],
            "operator_id": op["operator_id"],
            "event_type": ev_type,
            "severity": sev,
            "risk_score": score,
            "details": f"Safety rule triggered: {ev_type} recorded on {m['machine_id']} during active shift.",
            "acknowledged": bool(np.random.random() > 0.3)
        })

    df_safety = pd.DataFrame(safety_events_list)
    df_safety.to_csv(DATA_DIR / "safety_events.csv", index=False)
    print(f"Generated {len(df_safety)} safety events -> {DATA_DIR / 'safety_events.csv'}")

    # 6. GENERATE INCIDENTS
    incidents_list = []
    incident_types = [
        "Seatbelt Violation", "Proximity Hazard", "Overheating",
        "Excessive Idling", "Fatigue", "Mechanical Anomaly", "Other"
    ]
    for i in range(1, NUM_INCIDENTS + 1):
        inc_id = f"INC{i:04d}"
        inc_type = random.choice(incident_types)
        m = random.choice(machines_list)
        op = random.choice(operators_list)
        sev = random.choice(["Low", "Medium", "High", "Critical"])
        resolved = bool(np.random.random() > 0.25)
        resolution = "Operator briefed and cleared for shift resumption." if resolved else None
        inc_time = datetime.now() - timedelta(days=random.randint(0, 45), hours=random.randint(1, 23))

        incidents_list.append({
            "incident_id": inc_id,
            "timestamp": inc_time.strftime("%Y-%m-%d %H:%M:%S"),
            "machine_id": m["machine_id"],
            "operator_id": op["operator_id"],
            "incident_type": inc_type,
            "severity": sev,
            "description": f"{inc_type} event logged during excavation operations at {m['location']}.",
            "location": m["location"],
            "resolved": resolved,
            "resolution": resolution,
            "created_at": inc_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    df_incidents = pd.DataFrame(incidents_list)
    df_incidents.to_csv(DATA_DIR / "incidents.csv", index=False)
    print(f"Generated {len(df_incidents)} incidents -> {DATA_DIR / 'incidents.csv'}")

    # 7. GENERATE TRAINING COURSES & PROGRESS
    courses = [
        {
            "course_id": "TRN001",
            "category": "Safety",
            "title": "Proximity Safety & Ground Worker Awareness",
            "description": "Essential perimeter safety, blind spot management, and 3-meter critical exclusion zone compliance.",
            "difficulty": "Intermediate",
            "duration_min": 25,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        },
        {
            "course_id": "TRN002",
            "category": "Safety",
            "title": "Restraint Systems & Seatbelt Compliance",
            "description": "Mandatory three-point harness procedures and rollover protective structure (ROPS) survival guidelines.",
            "difficulty": "Beginner",
            "duration_min": 15,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        },
        {
            "course_id": "TRN003",
            "category": "Machine Operation",
            "title": "Excavator Hydraulic Optimization & Cycle Efficiency",
            "description": "Maximizing bucket fill factors while lowering engine strain and cycle turnaround times.",
            "difficulty": "Advanced",
            "duration_min": 40,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
        },
        {
            "course_id": "TRN004",
            "category": "Fuel Efficiency",
            "title": "Eco-Operating Modes & Anti-Idling Best Practices",
            "description": "Techniques for lowering unnecessary idling, auto-throttle configuration, and fuel saving.",
            "difficulty": "Beginner",
            "duration_min": 20,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
        },
        {
            "course_id": "TRN005",
            "category": "Maintenance Awareness",
            "title": "Pre-Shift Walkaround & Early Vibration Diagnostics",
            "description": "Identifying hydraulic leaks, abnormal track tension, and early mechanical vibration markers.",
            "difficulty": "Intermediate",
            "duration_min": 30,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
        },
        {
            "course_id": "TRN006",
            "category": "Emergency Procedures",
            "title": "Emergency Stop & High Thermal Runaway Protocols",
            "description": "Immediate fire suppression system activation, emergency engine shutdown, and evacuation paths.",
            "difficulty": "Advanced",
            "duration_min": 35,
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyBlazes.mp4"
        }
    ]
    df_courses = pd.DataFrame(courses)
    df_courses.to_csv(DATA_DIR / "courses.csv", index=False)

    training_progress_list = []
    for i in range(1, NUM_TRAINING_RECORDS + 1):
        prg_id = f"PRG{i:04d}"
        op = random.choice(operators_list)
        c = random.choice(courses)
        status = random.choice(["Completed", "Completed", "In Progress", "Not Started"])
        score = round(float(np.random.uniform(75.0, 100.0)), 1) if status == "Completed" else 0.0
        attempts = 1 if status == "Completed" else (1 if status == "In Progress" else 0)
        c_at = datetime.now() - timedelta(days=random.randint(1, 60)) if status == "Completed" else None

        training_progress_list.append({
            "progress_id": prg_id,
            "operator_id": op["operator_id"],
            "course_id": c["course_id"],
            "completion_status": status,
            "score": score,
            "attempts": attempts,
            "completed_at": c_at.strftime("%Y-%m-%d %H:%M:%S") if c_at else None
        })

    df_progress = pd.DataFrame(training_progress_list)
    df_progress.to_csv(DATA_DIR / "training_progress.csv", index=False)
    print(f"Generated {len(df_courses)} courses and {len(df_progress)} progress records -> {DATA_DIR / 'training_progress.csv'}")

    print("Synthetic dataset generation COMPLETE!")

if __name__ == "__main__":
    generate_synthetic_dataset()
