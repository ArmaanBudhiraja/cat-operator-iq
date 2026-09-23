import math
import random
from datetime import datetime
from typing import Any
from backend.app.services.safety_engine import SafetyEngine
from backend.app.services.anomaly_service import AnomalyService

class SimulationService:
    """
    Manages live simulated machine telemetry streaming, hazard injection,
    and 2D radar positions of surrounding ground workers.
    """

    def __init__(self):
        self.is_active = True
        self.tick_count = 0
        self.active_injections: dict[str, Any] = {}

        # Default state for primary demo machine EXC001
        self.current_state = {
            "timestamp": datetime.utcnow().isoformat(),
            "machine_id": "EXC001",
            "operator_id": "OP001",
            "task_id": "T001",
            "engine_hours": 2150.4,
            "fuel_used_l": 18.2,
            "load_cycles": 18,
            "idling_time_min": 8.0,
            "engine_temperature": 88.5,
            "oil_pressure": 43.0,
            "hydraulic_pressure": 282.0,
            "engine_rpm": 1850.0,
            "vibration": 1.75,
            "coolant_temperature": 85.0,
            "battery_voltage": 24.8,
            "load_weight": 14.5,
            "seatbelt_status": "Fastened",
            "proximity_distance_m": 8.5,
            "worker_detected": False,
            "safety_alert_triggered": False,
            "fatigue_indicator": 0.15,
            "weather": "Sunny"
        }

        # Simulated radar workers around machine (centered at 0,0)
        # Angles in degrees, distances in meters
        self.radar_workers = [
            {"id": "W01", "name": "Worker A (Surveyor)", "distance": 8.4, "angle": 45, "status": "SAFE"},
            {"id": "W02", "name": "Worker B (Spotter)", "distance": 6.8, "angle": 210, "status": "SAFE"},
            {"id": "W03", "name": "Worker C (Laborer)", "distance": 11.2, "angle": 315, "status": "SAFE"}
        ]

    def inject_hazard(self, hazard_type: str) -> dict[str, Any]:
        """
        Manually injects specific safety anomalies for live judge demonstration.
        """
        if hazard_type == "worker_proximity":
            self.active_injections["worker_proximity"] = True
            self.current_state["worker_detected"] = True
            self.current_state["proximity_distance_m"] = 2.1
            # Move Worker C right into critical proximity zone
            for w in self.radar_workers:
                if w["id"] == "W03":
                    w["distance"] = 2.1
                    w["angle"] = 120
                    w["status"] = "CRITICAL"
            return {"status": "Injected", "hazard": "Worker inside 2.1m critical zone"}

        elif hazard_type == "seatbelt_unfastened":
            self.active_injections["seatbelt_unfastened"] = True
            self.current_state["seatbelt_status"] = "Unfastened"
            return {"status": "Injected", "hazard": "Seatbelt unfastened"}

        elif hazard_type == "vibration_spike":
            self.active_injections["vibration_spike"] = True
            self.current_state["vibration"] = 4.2
            self.current_state["oil_pressure"] = 28.0
            return {"status": "Injected", "hazard": "Vibration spiked to 4.2 mm/s with low oil pressure"}

        elif hazard_type == "overheating":
            self.active_injections["overheating"] = True
            self.current_state["engine_temperature"] = 108.5
            self.current_state["coolant_temperature"] = 104.0
            return {"status": "Injected", "hazard": "Engine thermal runaway at 108.5°C"}

        elif hazard_type == "idle_excess":
            self.active_injections["idle_excess"] = True
            self.current_state["idling_time_min"] = 48.0
            return {"status": "Injected", "hazard": "Idle duration reached 48 min"}

        elif hazard_type == "reset":
            self.active_injections.clear()
            self.current_state["worker_detected"] = False
            self.current_state["proximity_distance_m"] = 8.5
            self.current_state["seatbelt_status"] = "Fastened"
            self.current_state["vibration"] = 1.75
            self.current_state["oil_pressure"] = 43.0
            self.current_state["engine_temperature"] = 88.5
            self.current_state["idling_time_min"] = 8.0
            self.radar_workers[2]["distance"] = 11.2
            self.radar_workers[2]["status"] = "SAFE"
            return {"status": "Reset", "hazard": "Nominal baseline restored"}

        return {"status": "Ignored", "message": f"Unknown hazard: {hazard_type}"}

    def step(self) -> dict[str, Any]:
        """
        Advances the simulation by 1 tick (representing ~2 seconds of real machine telemetry).
        Adds subtle realistic sensor jitter while maintaining injected conditions.
        """
        self.tick_count += 1
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.current_state["timestamp"] = now_str
        self.current_state["engine_hours"] = round(self.current_state["engine_hours"] + 0.001, 3)

        # Baseline jitter
        noise_vib = random.uniform(-0.05, 0.05)
        noise_temp = random.uniform(-0.2, 0.2)
        noise_rpm = random.uniform(-15.0, 15.0)

        if "vibration_spike" not in self.active_injections:
            self.current_state["vibration"] = round(max(1.2, 1.75 + noise_vib), 2)
            self.current_state["oil_pressure"] = round(max(35.0, 43.0 + random.uniform(-0.5, 0.5)), 1)
        else:
            self.current_state["vibration"] = round(4.2 + noise_vib, 2)

        if "overheating" not in self.active_injections:
            self.current_state["engine_temperature"] = round(max(80.0, 88.5 + noise_temp), 1)
            self.current_state["coolant_temperature"] = round(self.current_state["engine_temperature"] - 3.5, 1)
        else:
            self.current_state["engine_temperature"] = round(108.5 + noise_temp, 1)

        if "seatbelt_unfastened" not in self.active_injections:
            self.current_state["seatbelt_status"] = "Fastened"
        else:
            self.current_state["seatbelt_status"] = "Unfastened"

        if "idle_excess" not in self.active_injections:
            self.current_state["idling_time_min"] = round(max(2.0, 8.0 + random.uniform(-0.5, 0.5)), 1)
        else:
            self.current_state["idling_time_min"] = round(self.current_state["idling_time_min"] + 0.1, 1)

        if "worker_proximity" not in self.active_injections:
            # Jitter worker positions smoothly
            for w in self.radar_workers:
                w["angle"] = (w["angle"] + random.uniform(-1.0, 1.0)) % 360
                w["distance"] = round(max(6.5, w["distance"] + random.uniform(-0.2, 0.2)), 1)
                w["status"] = "SAFE"
            self.current_state["worker_detected"] = False
            self.current_state["proximity_distance_m"] = self.radar_workers[0]["distance"]
        else:
            # Worker C stays in critical proximity zone
            self.current_state["worker_detected"] = True
            self.current_state["proximity_distance_m"] = 2.1

        self.current_state["engine_rpm"] = round(1850.0 + noise_rpm, 0)

        # Calculate Cartesian coordinates (x, y) for radar canvas rendering
        radar_objects = []
        for w in self.radar_workers:
            rad = math.radians(w["angle"])
            dist = w["distance"]
            x = round(dist * math.cos(rad), 2)
            y = round(dist * math.sin(rad), 2)
            radar_objects.append({
                "id": w["id"],
                "name": w["name"],
                "distance": dist,
                "angle": round(w["angle"], 1),
                "x": x,
                "y": y,
                "status": "CRITICAL" if dist <= 3.0 else ("WARNING" if dist <= 6.0 else "SAFE")
            })

        # Run Safety Engine Evaluation
        safety_eval = SafetyEngine.evaluate(self.current_state, recent_events_count=1)

        # Run Anomaly Engine Evaluation
        anomaly_eval = AnomalyService.analyze_telemetry(self.current_state)

        return {
            "telemetry": self.current_state.copy(),
            "safety_score": safety_eval["risk_score"],
            "risk_level": safety_eval["risk_level"],
            "status_label": safety_eval["status_label"],
            "active_alerts": safety_eval["active_alerts"],
            "radar_objects": radar_objects,
            "anomaly_detected": anomaly_eval["is_anomaly"],
            "anomaly_details": anomaly_eval,
            "advisory_disclaimer": safety_eval["advisory_disclaimer"]
        }

# Global singleton simulation manager
simulation_manager = SimulationService()
