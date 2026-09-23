import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from backend.app.config import DATA_DIR
from backend.app.db.database import SessionLocal, init_db
from backend.app.db.models import (
    User, Operator, Machine, Task, Telemetry,
    SafetyEvent, Incident, Anomaly, TrainingCourse,
    TrainingProgress, Prediction, Recommendation
)

def seed():
    print("=" * 60)
    print("CAT OperatorIQ - Database Seeding Pipeline")
    print("=" * 60)

    # Initialize tables
    print("Initializing database tables...")
    init_db()
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("Database already contains data. Clearing existing records for clean seed...")
            db.query(Recommendation).delete()
            db.query(Prediction).delete()
            db.query(TrainingProgress).delete()
            db.query(TrainingCourse).delete()
            db.query(Anomaly).delete()
            db.query(Incident).delete()
            db.query(SafetyEvent).delete()
            db.query(Telemetry).delete()
            db.query(Task).delete()
            db.query(Machine).delete()
            db.query(Operator).delete()
            db.query(User).delete()
            db.commit()

        # 1. SEED USERS
        print("[1/9] Seeding users...")
        users = [
            User(
                user_id="USR001",
                username="operator_marcus",
                full_name="Marcus Vance",
                email="marcus.vance@cat-fleet.demo",
                role="Operator"
            ),
            User(
                user_id="USR002",
                username="supervisor_sarah",
                full_name="Sarah Jenkins",
                email="sarah.jenkins@cat-fleet.demo",
                role="Supervisor"
            )
        ]
        db.add_all(users)
        db.commit()

        # 2. SEED OPERATORS
        print("[2/9] Seeding operators...")
        df_ops = pd.read_csv(DATA_DIR / "operators.csv")
        ops_objects = []
        for _, r in df_ops.iterrows():
            u_id = "USR001" if r["operator_id"] == "OP001" else None
            ops_objects.append(Operator(
                operator_id=r["operator_id"],
                user_id=u_id,
                name=r["name"],
                experience_years=float(r["experience_years"]),
                skill_level=r["skill_level"],
                training_score=float(r["training_score"]),
                safety_score=float(r["safety_score"]),
                average_task_accuracy=float(r["average_task_accuracy"]),
                average_task_time=float(r["average_task_time"]),
                incident_count=int(r["incident_count"]),
                fatigue_score=float(r["fatigue_score"]),
                certification_status=r["certification_status"]
            ))
        db.bulk_save_objects(ops_objects)
        db.commit()

        # 3. SEED MACHINES
        print("[3/9] Seeding machines...")
        df_machines = pd.read_csv(DATA_DIR / "machine.csv")
        machine_objects = []
        for _, r in df_machines.iterrows():
            machine_objects.append(Machine(
                machine_id=r["machine_id"],
                machine_type=r["machine_type"],
                machine_model=r["machine_model"],
                machine_age_years=float(r["machine_age_years"]),
                engine_hours=float(r["engine_hours"]),
                maintenance_age_days=int(r["maintenance_age_days"]),
                fuel_capacity=float(r["fuel_capacity"]),
                current_fuel_level=float(r["current_fuel_level"]),
                hydraulic_pressure=float(r["hydraulic_pressure"]),
                engine_temperature=float(r["engine_temperature"]),
                engine_rpm=float(r["engine_rpm"]),
                vibration_level=float(r["vibration_level"]),
                coolant_temperature=float(r["coolant_temperature"]),
                oil_pressure=float(r["oil_pressure"]),
                battery_voltage=float(r["battery_voltage"]),
                load_weight=float(r["load_weight"]),
                operating_hours=float(r["operating_hours"]),
                location=r["location"],
                status=r["status"]
            ))
        db.bulk_save_objects(machine_objects)
        db.commit()

        # 4. SEED TASKS
        print("[4/9] Seeding tasks...")
        df_tasks = pd.read_csv(DATA_DIR / "tasks.csv")
        task_objects = []
        for _, r in df_tasks.iterrows():
            task_objects.append(Task(
                task_id=r["task_id"],
                task_type=r["task_type"],
                machine_id=r["machine_id"],
                operator_id=r["operator_id"],
                location=r["location"],
                priority=r["priority"],
                scheduled_start=datetime.strptime(str(r["scheduled_start"]), "%Y-%m-%d %H:%M:%S") if pd.notna(r["scheduled_start"]) else datetime.utcnow(),
                estimated_time_min=float(r["estimated_time_min"]),
                predicted_time_min=float(r["predicted_time_min"]) if pd.notna(r["predicted_time_min"]) else None,
                actual_time_min=float(r["actual_time_min"]) if pd.notna(r["actual_time_min"]) else None,
                load_cycles=int(r["load_cycles"]),
                distance=float(r["distance"]),
                weather=r["weather"],
                operator_skill=r["operator_skill"],
                machine_age=float(r["machine_age"]),
                status=r["status"]
            ))
        db.bulk_save_objects(task_objects)
        db.commit()

        # 5. SEED TELEMETRY (chunked)
        print("[5/9] Seeding telemetry records...")
        df_telem = pd.read_csv(DATA_DIR / "telemetry.csv")
        telem_objects = []
        for _, r in df_telem.iterrows():
            telem_objects.append(Telemetry(
                timestamp=datetime.strptime(str(r["timestamp"]), "%Y-%m-%d %H:%M:%S") if pd.notna(r["timestamp"]) else datetime.utcnow(),
                machine_id=r["machine_id"],
                operator_id=r["operator_id"],
                task_id=r["task_id"] if pd.notna(r["task_id"]) else None,
                engine_hours=float(r["engine_hours"]),
                fuel_used_l=float(r["fuel_used_l"]),
                load_cycles=int(r["load_cycles"]),
                idling_time_min=float(r["idling_time_min"]),
                engine_temperature=float(r["engine_temperature"]),
                oil_pressure=float(r["oil_pressure"]),
                hydraulic_pressure=float(r["hydraulic_pressure"]),
                engine_rpm=float(r["engine_rpm"]),
                vibration=float(r["vibration"]),
                coolant_temperature=float(r["coolant_temperature"]),
                battery_voltage=float(r["battery_voltage"]),
                load_weight=float(r["load_weight"]),
                seatbelt_status=r["seatbelt_status"],
                proximity_distance_m=float(r["proximity_distance_m"]),
                worker_detected=bool(r["worker_detected"]),
                safety_alert_triggered=bool(r["safety_alert_triggered"]),
                fatigue_indicator=float(r["fatigue_indicator"]),
                weather=r["weather"]
            ))
        # Save in chunks of 2,000 for SQLite performance
        chunk_size = 2000
        for i in range(0, len(telem_objects), chunk_size):
            db.bulk_save_objects(telem_objects[i:i + chunk_size])
            db.commit()

        # 6. SEED SAFETY EVENTS
        print("[6/9] Seeding safety events...")
        df_safety = pd.read_csv(DATA_DIR / "safety_events.csv")
        safety_objs = []
        for _, r in df_safety.iterrows():
            safety_objs.append(SafetyEvent(
                event_id=r["event_id"],
                timestamp=datetime.strptime(str(r["timestamp"]), "%Y-%m-%d %H:%M:%S"),
                machine_id=r["machine_id"],
                operator_id=r["operator_id"],
                event_type=r["event_type"],
                severity=r["severity"],
                risk_score=float(r["risk_score"]),
                details=r["details"],
                acknowledged=bool(r["acknowledged"])
            ))
        db.bulk_save_objects(safety_objs)
        db.commit()

        # 7. SEED INCIDENTS
        print("[7/9] Seeding incidents...")
        df_inc = pd.read_csv(DATA_DIR / "incidents.csv")
        inc_objs = []
        for _, r in df_inc.iterrows():
            inc_objs.append(Incident(
                incident_id=r["incident_id"],
                timestamp=datetime.strptime(str(r["timestamp"]), "%Y-%m-%d %H:%M:%S"),
                machine_id=r["machine_id"],
                operator_id=r["operator_id"],
                incident_type=r["incident_type"],
                severity=r["severity"],
                description=r["description"],
                location=r["location"],
                resolved=bool(r["resolved"]),
                resolution=r["resolution"] if pd.notna(r["resolution"]) else None,
                created_at=datetime.strptime(str(r["created_at"]), "%Y-%m-%d %H:%M:%S")
            ))
        db.bulk_save_objects(inc_objs)
        db.commit()

        # 8. SEED TRAINING COURSES & PROGRESS
        print("[8/9] Seeding training modules and quizzes...")
        df_courses = pd.read_csv(DATA_DIR / "courses.csv")
        course_objs = []
        quiz_data_sample = json.dumps([
            {
                "id": 1,
                "question": "What is the mandatory action when a ground worker enters the critical proximity zone (<3.0m)?",
                "options": [
                    "Sound horn twice and accelerate cycle",
                    "Immediately pause machine movement and establish positive eye contact",
                    "Continue swinging with caution",
                    "Radio the fleet supervisor within 15 minutes"
                ],
                "answer_idx": 1
            },
            {
                "id": 2,
                "question": "Why is operating an excavator with an unfastened seatbelt hazardous in Rollover Protective Structures (ROPS)?",
                "options": [
                    "It reduces hydraulic pump pressure",
                    "It invalidates the digital clock",
                    "The operator can be thrown from the protective zone during a tip-over",
                    "Engine RPM drops automatically"
                ],
                "answer_idx": 2
            },
            {
                "id": 3,
                "question": "Which indicator suggests abnormal hydraulic pump cavitation or excessive strain?",
                "options": [
                    "High-pitched screeching and erratic joystick response",
                    "Clean hydraulic sight glass",
                    "Fuel level above 80%",
                    "Coolant temperature at 85°C"
                ],
                "answer_idx": 0
            }
        ])

        for _, r in df_courses.iterrows():
            course_objs.append(TrainingCourse(
                course_id=r["course_id"],
                category=r["category"],
                title=r["title"],
                description=r["description"],
                difficulty=r["difficulty"],
                duration_min=int(r["duration_min"]),
                video_url=r["video_url"],
                quiz_data=quiz_data_sample
            ))
        db.bulk_save_objects(course_objs)
        db.commit()

        df_prg = pd.read_csv(DATA_DIR / "training_progress.csv")
        prg_objs = []
        for _, r in df_prg.iterrows():
            prg_objs.append(TrainingProgress(
                progress_id=r["progress_id"],
                operator_id=r["operator_id"],
                course_id=r["course_id"],
                completion_status=r["completion_status"],
                score=float(r["score"]) if pd.notna(r["score"]) else 0.0,
                attempts=int(r["attempts"]),
                completed_at=datetime.strptime(str(r["completed_at"]), "%Y-%m-%d %H:%M:%S") if pd.notna(r["completed_at"]) else None
            ))
        db.bulk_save_objects(prg_objs)
        db.commit()

        # 9. SEED ANOMALIES & INITIAL RECOMMENDATIONS
        print("[9/9] Seeding initial machine anomalies & smart recommendations...")
        anomalies = [
            Anomaly(
                anomaly_id="ANOM001",
                timestamp=datetime.utcnow(),
                machine_id="EXC001",
                operator_id="OP001",
                anomaly_score=68.5,
                risk_level="HIGH",
                reason="Vibration is 32% above machine baseline; Idle time is 41 minutes above normal",
                factors=json.dumps([
                    "Vibration is 32% above machine baseline (2.35 mm/s vs nominal 1.75 mm/s)",
                    "Idle time is 41 minutes above normal operating threshold",
                    "Hydraulic pressure deviation of +12% detected"
                ])
            ),
            Anomaly(
                anomaly_id="ANOM002",
                timestamp=datetime.utcnow(),
                machine_id="WHL002",
                operator_id="OP003",
                anomaly_score=54.2,
                risk_level="MEDIUM",
                reason="Engine temperature is 18% above normal operating thermal range",
                factors=json.dumps([
                    "Engine temperature reached 104°C during high load cycle",
                    "Coolant temperature differential exceeded 8°C"
                ])
            )
        ]
        db.add_all(anomalies)

        recs = [
            Recommendation(
                recommendation_id="REC001",
                machine_id="EXC001",
                operator_id="OP001",
                category="Training",
                priority="High",
                title="Proximity Safety Refresher",
                recommendation="Enroll in and complete TRN001 Proximity Safety & Ground Worker Awareness.",
                reason="3 proximity warnings recorded in current sector during this shift."
            ),
            Recommendation(
                recommendation_id="REC002",
                machine_id="EXC001",
                operator_id="OP001",
                category="Maintenance",
                priority="Medium",
                title="Hydraulic Sump Inspection",
                recommendation="Perform 250-hour hydraulic fluid check and check track tension.",
                reason="Vibration level currently operating at 2.35 mm/s (elevated above 1.75 mm/s baseline)."
            ),
            Recommendation(
                recommendation_id="REC003",
                machine_id="EXC001",
                operator_id="OP001",
                category="Efficiency",
                priority="Low",
                title="Auto-Idle Configuration",
                recommendation="Enable Auto-Idle mode to lower idling fuel burn during haul truck waiting cycles.",
                reason="Today's idle time accounts for 38% of total engine running time."
            )
        ]
        db.add_all(recs)
        db.commit()

        print("\nDatabase seeded successfully!")
        print(f"Total Operators: {db.query(Operator).count()}")
        print(f"Total Machines: {db.query(Machine).count()}")
        print(f"Total Tasks: {db.query(Task).count()}")
        print(f"Total Telemetry: {db.query(Telemetry).count()}")
        print(f"Total Incidents: {db.query(Incident).count()}")
        print(f"Total Training Progress: {db.query(TrainingProgress).count()}")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
