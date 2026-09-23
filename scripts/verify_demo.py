import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def put(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers={"Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_verification():
    print("============================================================")
    print("CAT OperatorIQ - End-to-End Live Hackathon Demo Verification")
    print("============================================================")

    # 1. Health Check
    health = get("/api/health")
    assert health["status"] == "healthy", "Health check failed"
    print("✓ SCENE 1: Health check passed - Backend online and streaming.")

    # 2. Operator Dashboard
    dash = get("/api/dashboard?operator_id=OP001&machine_id=EXC001")
    assert "MARCUS VANCE" in dash["greeting"]
    assert dash["current_machine_id"] == "EXC001"
    print(f"✓ SCENE 1: Dashboard loaded. Greeting: '{dash['greeting']}', Tasks Today: {dash['kpis']['today_tasks']}")

    # 3. Task Prediction Check
    task = get("/api/tasks/T001")
    assert task["task_id"] == "T001"
    pred = task["prediction_details"]
    assert pred["predicted_time_min"] > 0
    print(f"✓ SCENE 2: Task T001 ML Duration: {pred['predicted_time_min']} min (Range: {pred['confidence_lower_min']}-{pred['confidence_upper_min']} min). Factors: {len(pred['factors'])} factors.")

    # 4. Inject Hazard: Worker Proximity (2.1m)
    inj = post("/api/simulation/inject", {"hazard_type": "worker_proximity", "machine_id": "EXC001", "operator_id": "OP001"})
    assert inj["result"]["status"] == "Injected"
    print("✓ SCENE 3: Injected 'worker_proximity' hazard.")

    # 5. Verify Safety Engine reacts with CRITICAL score
    safety = get("/api/safety/live")
    assert safety["risk_level"] == "CRITICAL" or safety["safety_score"] >= 45.0
    critical_worker = [w for w in safety["radar_objects"] if w["status"] == "CRITICAL"]
    assert len(critical_worker) > 0
    print(f"✓ SCENE 4: Safety Center reacted: Risk = {safety['risk_level']} (Score: {safety['safety_score']}). Radar detected worker at {critical_worker[0]['distance']}m.")

    # 6. Verify Incident was automatically logged
    incidents = get("/api/incidents?machine_id=EXC001")
    assert len(incidents) > 0
    latest_inc = incidents[0]
    print(f"✓ SCENE 5: Incident automatically logged: ID={latest_inc['incident_id']} ({latest_inc['incident_type']} - {latest_inc['severity']})")

    # 7. AI Assistant Query
    ai_resp = post("/api/assistant/query", {"query": "Why is EXC001 showing a warning?", "operator_id": "OP001", "machine_id": "EXC001"})
    assert "answer" in ai_resp
    assert len(ai_resp["evidence"]) > 0
    assert "AI-generated recommendations are advisory" in ai_resp["safety_disclaimer"]
    print(f"✓ SCENE 6: AI Assistant Answer: '{ai_resp['answer'][:80]}...' [Evidence: {len(ai_resp['evidence'])}, Disclaimer: Present]")

    # 8. Complete Training Quiz
    quiz_res = post("/api/training/TRN001/quiz", {"operator_id": "OP001", "answers": {"1": 1, "2": 2, "3": 0}})
    assert quiz_res["passed"] is True
    print(f"✓ SCENE 7: Training Quiz completed on TRN001: Score = {quiz_res['score_pct']}% (Passed).")

    # 9. Mark Incident Resolved
    resolve_res = put(f"/api/incidents/{latest_inc['incident_id']}", {"resolved": True, "resolution": "Remediation verified by shift supervisor."})
    assert resolve_res["resolved"] is True
    print(f"✓ SCENE 8: Incident {latest_inc['incident_id']} marked RESOLVED.")

    # 10. Generate Audit Report
    report = get("/api/reports/generate?report_type=daily_operator&operator_id=OP001&machine_id=EXC001")
    assert "REP-OP" in report["report_id"]
    print(f"✓ SCENE 9: Generated Official Shift Audit Report: {report['report_id']} ({report['report_title']})")

    # 11. Reset Simulation
    reset = post("/api/simulation/reset", {})
    assert reset["status"] == "Reset"
    print("✓ Cleanup: Reset simulation back to nominal baseline.")

    print("\n============================================================")
    print("ALL 9 HACKATHON DEMO SCENES VERIFIED WITH 100% SUCCESS!")
    print("============================================================")

if __name__ == "__main__":
    run_verification()
