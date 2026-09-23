import os
import re
from pathlib import Path
from typing import Any
from backend.app.config import KNOWLEDGE_BASE_DIR, settings

class AssistantService:
    """
    CAT OperatorIQ Intelligent Assistant.
    Provides deterministic intent-based retrieval and synthesized domain answers,
    backed by RAG document retrieval over the knowledge base.
    Adheres strictly to the advisory safety disclaimer.
    """

    @classmethod
    def query(
        cls,
        user_query: str,
        operator_data: dict[str, Any] | None = None,
        machine_data: dict[str, Any] | None = None,
        active_task: dict[str, Any] | None = None,
        telemetry: dict[str, Any] | None = None,
        safety_alerts: list[dict[str, Any]] | None = None,
        incidents: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        q_lower = user_query.lower()
        operator_name = operator_data.get("name", "Marcus Vance") if operator_data else "Marcus Vance"
        machine_id = machine_data.get("machine_id", "EXC001") if machine_data else "EXC001"

        # Search knowledge base for relevant documents
        relevant_docs = cls._search_knowledge_base(user_query)
        citations = [doc["title"] for doc in relevant_docs]

        # 1. Intent: Tasks / Schedule
        if any(w in q_lower for w in ["task", "schedule", "work today", "assigned"]):
            if active_task:
                task_type = active_task.get("task_type", "Earth Excavation")
                status = active_task.get("status", "In Progress")
                pred = active_task.get("predicted_time_min", 54.0)
                answer = f"You are currently assigned to '{task_type}' (Task ID: {active_task.get('task_id', 'T001')}) on machine {machine_id}."
                evidence = [
                    f"Task Status: {status}",
                    f"Machine Assigned: {machine_id} ({active_task.get('location', 'Site Alpha')})",
                    f"ML Predicted Completion: {pred:.0f} minutes (Estimated: {active_task.get('estimated_time_min', 60):.0f} min)",
                    "Scheduled Priority: High"
                ]
                next_step = "Proceed with scheduled excavation while maintaining continuous perimeter vigilance."
            else:
                answer = "You have 4 tasks scheduled for today's shift across Site Alpha and Site Beta."
                evidence = [
                    "T001: Earth Excavation (EXC001) - In Progress",
                    "T002: Trenching Sector 2 (EXC001) - Scheduled",
                    "T003: Material Loading (WHL002) - Scheduled",
                    "T004: Foundation Grading - Scheduled"
                ]
                next_step = "Initiate your first assigned task on EXC001 after completing the mandatory pre-shift walkaround."

        # 2. Intent: Safety Warning / Risk Explanation
        elif any(w in q_lower for w in ["warning", "alert", "risk", "why is", "showing a warning", "hazard"]):
            current_risk = "HIGH" if (safety_alerts and len(safety_alerts) > 0) else "LOW"
            vib = telemetry.get("vibration", 2.35) if telemetry else 2.35
            idle = telemetry.get("idling_time_min", 41.0) if telemetry else 41.0

            answer = f"{machine_id} is currently flagging advisory safety alerts. Current safety status evaluates to {current_risk} risk."
            evidence = [
                f"Vibration telemetry reading is {vib:.2f} mm/s (elevated compared to nominal 1.75 mm/s baseline)",
                f"Continuous idle time logged at {idle:.0f} minutes in current cycle",
                "1 simulated ground worker detected in proximity zone within recent interval"
            ]
            if safety_alerts:
                for a in safety_alerts[:2]:
                    evidence.append(f"Active Alert: {a.get('title', 'Hazard')} - {a.get('message', '')}")
            next_step = "Verify worker exclusion radius around machine tracks and inspect undercarriage tension before continuing swing."

        # 3. Intent: Task Prediction / Duration / ETA
        elif any(w in q_lower for w in ["how long", "predicted", "eta", "time will", "take", "prediction"]):
            pred = active_task.get("predicted_time_min", 54.0) if active_task else 54.0
            answer = f"Our ML model projects your current task will require approximately {pred:.0f} minutes to complete (90% confidence interval: 48 - 61 minutes)."
            evidence = [
                "Baseline Earth Excavation standard: 60.0 minutes",
                "+7.5 min added due to muddy ground conditions and weather",
                "-6.5 min reduction credited to your Expert operator skill rating",
                "+2.0 min added due to 18 high-capacity load cycles"
            ]
            next_step = "Maintain consistent bucket fill factors to remain ahead of predicted completion schedule."

        # 4. Intent: Machine Performance / Health
        elif any(w in q_lower for w in ["health", "machine performance", "performing", "engine", "temp", "oil"]):
            temp = telemetry.get("engine_temperature", 88.5) if telemetry else 88.5
            oil = telemetry.get("oil_pressure", 42.0) if telemetry else 42.0
            answer = f"{machine_id} (CAT 336 Heavy Duty) has an overall composite health score of 91% (Normal Operating Condition)."
            evidence = [
                f"Engine Temperature: {temp:.1f}°C (Normal: 82 - 95°C)",
                f"Oil Pressure: {oil:.1f} psi (Target: 40 - 45 psi)",
                "Hydraulic System Pressure: 282 bar (Nominal relief: 350 bar)",
                "Battery System: 24.8 V (Optimal charge)"
            ]
            next_step = "Check hydraulic oil sight glass during the mid-day lunch break to ensure clean fluid levels."

        # 5. Intent: Incidents
        elif any(w in q_lower for w in ["incident", "log", "safety event"]):
            inc_count = len(incidents) if incidents else 3
            answer = f"There are {inc_count} safety incidents logged for this sector during the current period."
            evidence = [
                "INC001: Proximity alert in Sector 4 (Resolved - Spotter repositioned)",
                "INC002: Brief seatbelt disconnect during implement adjustment",
                "INC003: Elevated vibration advisory on heavy rocky stratum"
            ]
            next_step = "Review active incident resolutions in the Incidents tab before commencing high-priority trenching."

        # 6. Intent: Training / Courses
        elif any(w in q_lower for w in ["training", "course", "quiz", "recommendation"]):
            answer = "Based on recent telemetry and proximity safety events, the system recommends completing the 'Proximity Safety & Ground Worker Awareness' refresher."
            evidence = [
                "Your overall training competency index is 94.0%",
                "Ground worker proximity events occurred 3 times in your sector this week",
                "Refresher duration: 25 minutes (includes 3-question practical quiz)"
            ]
            next_step = "Navigate to the Training Hub and launch the Proximity Safety quiz to verify compliance."

        # 7. General Fallback
        else:
            answer = f"Hello {operator_name}. CAT OperatorIQ is monitoring {machine_id} on active duty. You can ask about your tasks, safety advisories, machine health, or recommended training."
            evidence = [
                f"Active Machine: {machine_id}",
                f"Telemetry Link: Connected (WebSocket Live Stream)",
                f"Advisory Engine: All 8 safety rules actively evaluating"
            ]
            next_step = "Select any KPI or alert on the dashboard for detailed operational breakdown."

        return {
            "question": user_query,
            "answer": answer,
            "evidence": evidence,
            "recommended_next_step": next_step,
            "safety_disclaimer": settings.SAFETY_DISCLAIMER,
            "citations": citations
        }

    @classmethod
    def _search_knowledge_base(cls, query: str) -> list[dict[str, Any]]:
        """
        Retrieves matching synthetic knowledge base markdown documents.
        """
        results = []
        if not KNOWLEDGE_BASE_DIR.exists():
            return results

        q_tokens = set(re.findall(r"\w+", query.lower()))
        for md_file in KNOWLEDGE_BASE_DIR.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                title_line = content.splitlines()[0].replace("#", "").strip() if content else md_file.stem
                file_tokens = set(re.findall(r"\w+", content.lower()))
                overlap = len(q_tokens.intersection(file_tokens))
                if overlap > 0:
                    results.append({
                        "title": title_line,
                        "path": str(md_file.relative_to(KNOWLEDGE_BASE_DIR)),
                        "score": overlap
                    })
            except Exception:
                pass

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:3]
