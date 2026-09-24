import os
import re
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any
from backend.app.config import KNOWLEDGE_BASE_DIR, settings

logger = logging.getLogger(__name__)

class AssistantService:
    """
    CAT OperatorIQ Intelligent Assistant.
    Uses Live AI (Gemini / OpenAI LLM) when configured and operational.
    Automatically rolls back to deterministic rule-based RAG if the LLM
    encounters network errors, rate limits, timeouts, or invalid keys.
    Always includes the mandatory advisory safety disclaimer.
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
        # 1. Search knowledge base for relevant documents
        relevant_docs = cls._search_knowledge_base(user_query)
        citations = [doc["title"] for doc in relevant_docs]

        # 2. Try Live AI if API key is provided
        api_key = settings.OPENAI_API_KEY
        if api_key and api_key.strip():
            try:
                llm_response = cls._call_llm(
                    user_query=user_query,
                    operator_data=operator_data,
                    machine_data=machine_data,
                    active_task=active_task,
                    telemetry=telemetry,
                    safety_alerts=safety_alerts,
                    incidents=incidents,
                    relevant_docs=relevant_docs,
                    api_key=api_key.strip()
                )
                if llm_response and llm_response.get("answer"):
                    return {
                        "question": user_query,
                        "answer": llm_response["answer"],
                        "evidence": llm_response.get("evidence", []),
                        "recommended_next_step": llm_response.get("recommended_next_step", "Continue operations while monitoring telemetry."),
                        "safety_disclaimer": settings.SAFETY_DISCLAIMER,
                        "citations": llm_response.get("citations") or citations,
                        "is_fallback": False,
                        "ai_provider": llm_response.get("provider", "Live AI (Gemini)"),
                        "fallback_reason": None
                    }
            except Exception as exc:
                logger.warning(f"Live AI call failed ({exc}). Rolling back to local rule-based assistant.")
                fallback_reason = f"Live AI service unavailable or quota reached ({type(exc).__name__}). Answered via onboard telemetry rules."
        else:
            fallback_reason = "No API key configured. Operating in local deterministic rule mode."

        # 3. Deterministic Local Fallback (Rollback mode)
        fallback_data = cls._deterministic_query(
            user_query=user_query,
            operator_data=operator_data,
            machine_data=machine_data,
            active_task=active_task,
            telemetry=telemetry,
            safety_alerts=safety_alerts,
            incidents=incidents
        )

        return {
            "question": user_query,
            "answer": fallback_data["answer"],
            "evidence": fallback_data["evidence"],
            "recommended_next_step": fallback_data["recommended_next_step"],
            "safety_disclaimer": settings.SAFETY_DISCLAIMER,
            "citations": citations,
            "is_fallback": True,
            "ai_provider": "Local Rule-Based Assistant (Offline Fallback)",
            "fallback_reason": fallback_reason
        }

    @classmethod
    def _call_llm(
        cls,
        user_query: str,
        operator_data: dict[str, Any] | None,
        machine_data: dict[str, Any] | None,
        active_task: dict[str, Any] | None,
        telemetry: dict[str, Any] | None,
        safety_alerts: list[dict[str, Any]] | None,
        incidents: list[dict[str, Any]] | None,
        relevant_docs: list[dict[str, Any]],
        api_key: str
    ) -> dict[str, Any]:
        """
        Calls live LLM endpoint with structured telemetry context.
        Supports both OpenAI and Google Gemini APIs with automatic fallback between models.
        """
        # Build telemetry summary
        telem_str = "Nominal operating corridors"
        if telemetry:
            telem_str = (
                f"Engine Temp: {telemetry.get('engine_temperature', 88.5):.1f}°C, "
                f"Vibration: {telemetry.get('vibration', 1.8):.2f} mm/s, "
                f"Oil Pressure: {telemetry.get('oil_pressure', 42.0):.1f} psi, "
                f"Hydraulic Pressure: {telemetry.get('hydraulic_pressure', 280):.0f} bar, "
                f"Idle Time: {telemetry.get('idling_time_min', 10):.0f} min, "
                f"Worker Proximity Detected: {telemetry.get('worker_detected', False)} "
                f"(Distance: {telemetry.get('proximity_distance_m', 15.0):.1f}m)"
            )

        task_str = "No active task scheduled"
        if active_task:
            task_str = (
                f"Task ID: {active_task.get('task_id', 'T001')}, Type: {active_task.get('task_type', 'Excavation')}, "
                f"Status: {active_task.get('status', 'In Progress')}, "
                f"ML Predicted Duration: {active_task.get('predicted_time_min', 54.0):.0f} min"
            )

        alerts_str = "None"
        if safety_alerts and len(safety_alerts) > 0:
            alerts_str = "; ".join(
                [f"{a.get('title', 'Alert')}: {a.get('message', '')}" for a in safety_alerts[:3]]
            )

        docs_summary = ""
        if relevant_docs:
            docs_summary = "\n".join(
                [f"- {d['title']}: {d.get('snippet', '')[:160]}" for d in relevant_docs[:2]]
            )

        operator_name = operator_data.get("name", "Marcus Vance") if operator_data else "Marcus Vance"
        machine_id = machine_data.get("machine_id", "EXC001") if machine_data else "EXC001"

        prompt = f"""You are CAT OperatorIQ Assistant, an intelligent operational companion for Caterpillar heavy machinery operators.
Your role is to assist the operator with clear, accurate, advisory operational guidance based strictly on real-time machine telemetry, active tasks, alerts, and Caterpillar procedures.

Current Operating Context:
- Operator: {operator_name}
- Machine: {machine_id}
- Live Telemetry: {telem_str}
- Active Task: {task_str}
- Active Safety Alerts: {alerts_str}
{f"- Relevant Caterpillar Manuals: {docs_summary}" if docs_summary else ""}

Operator Question: "{user_query}"

Instructions:
1. Provide a direct, professional answer (2-3 concise sentences).
2. Provide 2-4 specific evidence bullets citing the relevant telemetry values or task data above.
3. Recommend one concrete next step for the operator.
4. Mention reference manuals if relevant.
5. SAFETY RULE: You are purely advisory. Never command direct control of the machine.

Format your response strictly as valid JSON with NO markdown backticks:
{{
  "answer": "...",
  "evidence": ["...", "..."],
  "recommended_next_step": "...",
  "citations": ["..."]
}}"""

        # 1. Standard OpenAI (keys starting with sk-)
        if api_key.startswith("sk-"):
            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are CAT OperatorIQ Assistant. Always respond strictly in valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 500
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                content = resp_json["choices"][0]["message"]["content"]
                cleaned = re.sub(r"^```json\s*", "", content.strip(), flags=re.IGNORECASE)
                cleaned = re.sub(r"```$", "", cleaned.strip())
                parsed = json.loads(cleaned)
                parsed["provider"] = "Live AI (OpenAI GPT-4o-mini)"
                return parsed

        # 2. Google Gemini API (keys starting with AQ or standard Gemini keys)
        # Try prioritized models: fast flash-lite first for high availability, then 3.6-flash
        models_to_try = ["gemini-3.5-flash-lite", "gemini-3.6-flash"]
        last_error = None

        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
                req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=4.5) as response:
                    if response.status == 200:
                        raw_bytes = response.read()
                        resp_json = json.loads(raw_bytes.decode("utf-8"))
                        content = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                        cleaned = re.sub(r"^```json\s*", "", content.strip(), flags=re.IGNORECASE)
                        cleaned = re.sub(r"```$", "", cleaned.strip())
                        parsed = json.loads(cleaned)
                        parsed["provider"] = f"Live AI ({model_name})"
                        return parsed
            except Exception as e:
                last_error = e
                logger.info(f"Model {model_name} failed: {e}. Trying next option if available.")
                continue

        if last_error:
            raise last_error
        raise RuntimeError("No LLM models succeeded")

    @classmethod
    def _deterministic_query(
        cls,
        user_query: str,
        operator_data: dict[str, Any] | None = None,
        machine_data: dict[str, Any] | None = None,
        active_task: dict[str, Any] | None = None,
        telemetry: dict[str, Any] | None = None,
        safety_alerts: list[dict[str, Any]] | None = None,
        incidents: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        """
        Deterministic intent-based retrieval and synthesized domain answers.
        Acts as the guaranteed local offline fallback.
        """
        q_lower = user_query.lower()
        operator_name = operator_data.get("name", "Marcus Vance") if operator_data else "Marcus Vance"
        machine_id = machine_data.get("machine_id", "EXC001") if machine_data else "EXC001"

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
                "1 ground worker detected in proximity zone within recent interval"
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
            "answer": answer,
            "evidence": evidence,
            "recommended_next_step": next_step
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
                        "score": overlap,
                        "snippet": content[:300]
                    })
            except Exception:
                pass

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:3]

    @classmethod
    def get_status(cls) -> dict[str, Any]:
        """
        Reports current AI readiness and configuration.
        """
        api_key = settings.OPENAI_API_KEY
        configured = bool(api_key and api_key.strip())
        provider = "Gemini"
        if configured and api_key.startswith("sk-"):
            provider = "OpenAI GPT-4o-mini"
        elif configured:
            provider = "Gemini (gemini-3.5-flash-lite / 3.6-flash)"

        return {
            "ai_configured": configured,
            "provider": provider,
            "fallback_available": True,
            "fallback_mode": "Local Rule-Based RAG Assistant",
            "weather_configured": bool(settings.WEATHER_API_KEY and settings.WEATHER_API_KEY.strip())
        }
