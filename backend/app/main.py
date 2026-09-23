import asyncio
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.db.database import init_db
from backend.app.services.simulation_service import simulation_manager

# Import API Routers
from backend.app.api import (
    dashboard, tasks, machines, operators,
    safety, incidents, training, predictions,
    assistant, simulation, reports, anomalies
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup if not already created
    try:
        init_db()
    except Exception as e:
        print(f"DB Init note: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Your intelligent companion for safer and smarter machine operations. An industrial-grade operator assistance system for Caterpillar machinery.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(dashboard.router)
app.include_router(tasks.router)
app.include_router(machines.router)
app.include_router(operators.router)
app.include_router(safety.router)
app.include_router(incidents.router)
app.include_router(training.router)
app.include_router(predictions.router)
app.include_router(assistant.router)
app.include_router(simulation.router)
app.include_router(reports.router)
app.include_router(anomalies.router)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "status": "ONLINE",
        "advisory_disclaimer": settings.SAFETY_DISCLAIMER,
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "simulation_active": simulation_manager.is_active,
        "machine_id": simulation_manager.current_state["machine_id"]
    }

# Real-time WebSocket Telemetry Feed
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Emit simulation state every 2 seconds
            state = simulation_manager.step()
            await websocket.send_text(json.dumps(state, default=str))
            await asyncio.sleep(2.0)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket client disconnected or encountered error: {e}")
