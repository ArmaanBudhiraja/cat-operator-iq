# CAT OperatorIQ — Complete Beginner Guide

Welcome to the definitive beginner-friendly technical guide for **CAT OperatorIQ**.

This guide is designed for developers, engineering students, data scientists, and interview candidates who know basic programming (Python, JavaScript, basic SQL) but want to understand **every single moving part** of this heavy equipment IoT and AI assistance platform.

---

## 1. Project in One Minute

### What is CAT OperatorIQ?
**CAT OperatorIQ** is an industrial operator assistance and fleet telemetry monitoring system built for Caterpillar heavy machinery (such as 36-ton excavators, wheel loaders, dozers, and haul trucks). It functions like a digital co-pilot inside the machine cab and a live operational command center for site supervisors.

### What Problem Does It Solve?
Operating 40-ton construction machinery in high-risk environments (quarries, deep trenches, highway construction) is difficult and dangerous:
1. **Blind spots cause accidents:** Ground workers can walk into exclusion zones unnoticed.
2. **Operators miss early machine failures:** High vibration, low oil pressure, or thermal spikes can lead to catastrophic breakdowns.
3. **Unscheduled delays ruin project budgets:** Tasks take longer than expected due to weather, ground conditions, or operator fatigue.
4. **Safety compliance is hard to audit:** Site managers need auditable records of safety events, seatbelt compliance, and operator training certifications.

CAT OperatorIQ solves these problems by combining **real-time IoT telemetry streaming**, **an auditable 8-rule safety scoring engine**, **machine learning for task duration prediction and anomaly detection**, **an offline-capable domain AI assistant**, and **interactive operator training**.

### Who Uses It?
1. **Machine Operators (e.g., Marcus Vance in Cab Mode):** Sits in the cab of an excavator (like `EXC001`), sees a live 2D proximity radar showing nearby ground workers, monitors machine health, receives predictive task ETAs, and asks the AI assistant questions about warnings.
2. **Fleet Supervisors (e.g., Sarah Jenkins in Fleet Mode):** Manages multiple machines and operators across job sites, dispatches tasks, reviews safety compliance audits, monitors fleet health, and tracks open incidents.

### What Happens When Someone Opens the Application?
```
User Opens Browser (http://localhost:5173)
       │
       ▼
React App Mounts (Vite + React 18)
       │
       ├──► Connects to WebSocket: ws://localhost:8000/ws/telemetry
       │    (Streams live machine telemetry and 2D worker radar positions every 2 seconds)
       │
       └──► Sends HTTP GET /api/dashboard?operator_id=OP001&machine_id=EXC001
            │
            ▼
      FastAPI Backend (Python 3.12)
            │
            ├──► Queries Database (SQLite / PostgreSQL) for Tasks, Operator Scores, KPIs
            │
            ├──► Calls SafetyEngine (Evaluates 8 safety rules on current telemetry)
            │
            ├──► Calculates Composite Machine Health Score (Thermal, Vibration, Oil, Maintenance)
            │
            └──► Returns JSON to Frontend
                     │
                     ▼
      Dashboard Renders UI (Cards, Radar Canvas, Charts, Active Alerts)
```

### Simple Diagram Explanation:
- **User:** The machine operator or site supervisor interacting with the screen.
- **Frontend:** The React application rendering widgets, SVG gauges, and HTML5 canvas radar.
- **Backend:** The FastAPI server handling business logic, calculations, and WebSocket streaming.
- **Services:** Dedicated Python modules (`SafetyEngine`, `AnomalyService`, `PredictionService`, `AssistantService`, `SimulationService`).
- **Database / ML:** The SQLite/PostgreSQL relational storage and Scikit-learn `.joblib` model binaries.
- **Response:** JSON payloads containing sanitized, validated data.
- **Frontend:** State updates trigger smooth React re-renders without full-page reloads.

---

## 2. The Problem

### Imagine a Day on a Construction Site
Imagine an operator named **Marcus Vance** climbing into the cab of a 36-ton **CAT 336 Heavy Duty Hydraulic Excavator** at 7:00 AM on **Site Alpha - Sector 4 Foundation**.

```
                           ┌───────────────────────────┐
                           │      CAT 336 EXCAVATOR    │
                           │   Weight: 36 Tonnes       │
                           │   Engine: 311 HP (232 kW) │
                           │   Bucket Capacity: 2.2 m³ │
                           └─────────────┬─────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
             [Operator Cab]       [Hydraulic Arm]       [Undercarriage]
             Marcus Vance         Swing Radius: 10m     Steel Tracks
```

During a typical shift, several critical challenges arise:

1. **The Ground Worker Hazard (Proximity):**
   - A surveyor carrying a GPS grade rod walks behind the excavator to verify trench depth.
   - The excavator's rear counterweight creates a massive blind spot.
   - If the operator swings the bucket without knowing someone is within 3 meters, it could be fatal.
   - **How OperatorIQ helps:** The machine sensors detect ground personnel proximity (`proximity_distance_m: 2.1`) and trigger **RULE_2_PROXIMITY_CRITICAL**. The system immediately renders the worker on the cab's 2D radar, turns the dashboard banner bright red, and alerts the operator to pause movement.

2. **The Mechanical Fatigue Hazard (Anomalies):**
   - While digging through dense rocky stratum, a hydraulic hose starts pulsing irregularly and the track tension slackens.
   - The vibration sensor spikes from normal ($1.75\text{ mm/s}$) to $4.2\text{ mm/s}$, and oil pressure drops from $43\text{ psi}$ to $28\text{ psi}$.
   - Without early detection, the hydraulic pump could seize, causing a $\$45,000$ repair and 3 days of project downtime.
   - **How OperatorIQ helps:** The **Isolation Forest Anomaly Detection Model** detects that this combination of vibration and pressure is an outlier ($p < 0.05$). An alert is flagged with explainable factors: `"Vibration is 32% above machine baseline; Oil pressure is 35% below baseline"`.

3. **The Task Estimation Dilemma (Duration & Delays):**
   - The project manager assigns Marcus a task: *"Excavate 400 cubic meters of earth for foundation footing"*. Standard manual charts say this takes 60 minutes.
   - But it rained heavily last night (muddy soil), Marcus is an expert operator, the machine is 2.4 years old, and the task requires 18 high-capacity truck load cycles.
   - **How OperatorIQ helps:** The **Gradient Boosting Task Duration Model** ingests these exact variables and predicts an actual completion time of **54.0 minutes** (confidence interval: 48.0 to 60.0 minutes), explaining the $+7.5\text{ min}$ weather penalty and $-6.5\text{ min}$ expert skill credit.

4. **Operator Fatigue & Seatbelts:**
   - In heavy equipment, rollover protective structures (ROPS) only protect the operator if the seatbelt is fastened. Operators occasionally unfasten the belt to lean out or get complacent during long shifts.
   - **How OperatorIQ helps:** Telemetry checks `seatbelt_status`. If unfastened during machine operation, **RULE_1** fires, adding $+35.0$ risk points and logging an advisory event.

---

## 3. What the System Does

CAT OperatorIQ delivers nine core capabilities:

| Capability | What It Does | Who Benefits |
| :--- | :--- | :--- |
| **Live Telemetry Streaming** | Streams sensor feeds (RPM, temperatures, pressures, vibration, fuel, hours) over WebSockets every 2 seconds. | Operator & Fleet Manager |
| **2D Proximity Radar** | Visualizes machine center $(0,0)$ and surrounding ground personnel on a dynamic polar/Cartesian radar canvas with colored exclusion zones. | Cab Operator |
| **Transparent Safety Engine** | Evaluates 8 deterministic safety rules to compute a 0–100 risk score and categorize operations into `SAFE`, `WARNING`, `HIGH RISK`, or `CRITICAL`. | Operator & Safety Officer |
| **Machine Health Diagnostics** | Aggregates thermal, vibration, oil pressure, and maintenance age into a transparent composite percentage score ($0-100\%$). | Maintenance Technicians |
| **Predictive Task Scheduling** | Predicts task completion time with 90% confidence intervals and feature-by-feature explanation. | Site Dispatchers |
| **ML Anomaly Detection** | Identifies multidimensional telemetry deviations using an Isolation Forest model with human-readable diagnostic explanations. | Fleet Reliability Engineers |
| **Domain AI Assistant** | Answers natural language questions about machines, safety alerts, tasks, and maintenance backed by a local knowledge base. | In-Cab Operators |
| **Incident Logging & Resolution** | Automatically logs critical safety events and supports manual incident reporting with supervisor resolution tracking. | Safety Supervisors |
| **Interactive Training Hub** | Delivers equipment safety courses with video links and automated 3-question practical quizzes that update operator competency records. | Operators & HR |

---

## 4. Complete Architecture

```mermaid
flowchart TD
    subgraph ClientLayer["Frontend Client (React 18 + Vite + Tailwind)"]
        UI["In-Cab & Supervisor UI"]
        RadarCanvas["2D Proximity Radar Canvas"]
        SimControls["Simulation Hazard Injector"]
        SimContext["SimulationContext (State & Polling Fallback)"]
        APIClient["API Service (fetch client in api.ts)"]
    end

    subgraph TransportLayer["Communication & Network Layer"]
        WSConn["WebSocket Connection (/ws/telemetry)"]
        HTTPConn["REST HTTP Requests (/api/*)"]
        ViteProxy["Vite Dev Server Reverse Proxy (port 5173 -> 8000)"]
    end

    subgraph BackendLayer["Backend Server (FastAPI + Python 3.12)"]
        FastAPIApp["FastAPI Main Application (main.py)"]
        SimService["SimulationService (simulation_manager singleton)"]
        SafetyEngine["SafetyEngine (8-Rule Additive Evaluator)"]
        AnomalyService["AnomalyService (ML & Heuristic Detector)"]
        PredictionService["PredictionService (Task Duration Regressor)"]
        AssistantService["AssistantService (Intent Engine & Local RAG)"]
        RecService["RecommendationService (Multi-Domain Advisory)"]
    end

    subgraph MLLayer["Machine Learning & Analytics (Scikit-Learn)"]
        TaskModel["task_time_model.joblib (GradientBoosting)"]
        AnomModel["anomaly_model.joblib (IsolationForest)"]
        Preproc["TaskDataPreprocessor (OneHotEncoder + Scaler)"]
        Metrics["metrics.json (MAE: 4.13m, R²: 0.9642)"]
    end

    subgraph StorageLayer["Data & Persistence Layer"]
        SQLAlchemy["SQLAlchemy 2.0 ORM Engine"]
        SQLiteDB[("SQLite Database: cat_operator_iq.db")]
        PostgresDB[("PostgreSQL 16: cat_operator_iq (Docker)")]
        KnowledgeBase["Knowledge Base Markdown Files (/knowledge_base)"]
        CSVFiles["Synthetic Dataset CSVs (/data/*.csv)"]
    end

    %% Wiring
    UI --> SimContext
    UI --> APIClient
    SimControls --> SimContext
    SimContext --> WSConn
    APIClient --> HTTPConn

    WSConn --> ViteProxy
    HTTPConn --> ViteProxy
    ViteProxy --> FastAPIApp

    FastAPIApp --> SimService
    FastAPIApp --> SafetyEngine
    FastAPIApp --> AnomalyService
    FastAPIApp --> PredictionService
    FastAPIApp --> AssistantService
    FastAPIApp --> RecService

    PredictionService --> TaskModel
    AnomalyService --> AnomModel
    AssistantService --> KnowledgeBase

    FastAPIApp --> SQLAlchemy
    SQLAlchemy --> SQLiteDB
    SQLAlchemy -.-> PostgresDB
```

### Architecture Walkthrough:
1. **Frontend:** React application rendered in the browser. It communicates over two channels:
   - **Persistent WebSocket (`/ws/telemetry`):** Receives state updates every 2 seconds.
   - **REST HTTP API (`/api/*`):** Used for explicit queries (loading dashboard, changing task status, submitting quizzes, creating incidents).
2. **Backend:** FastAPI application running on Uvicorn. Routes are organized into 12 domain routers.
3. **Simulation Engine:** `simulation_manager` runs an active virtual telemetry loop for demo machine `EXC001`, updating engine hours, fluctuating sensors with Gaussian jitter, and updating worker positions in polar coordinates.
4. **Safety & Anomaly Engines:** Evaluate every telemetry tick against safety rules and Isolation Forest decision boundaries.
5. **Persistence:** SQLAlchemy connects to SQLite (`cat_operator_iq.db`) for lightweight single-command execution or PostgreSQL when deployed with Docker Compose.

---

## 5. Project Folder Structure

Below is the verified directory structure of the repository:

```
cat-operator-iq/
├── .env.example                  # Environment configuration template
├── Dockerfile.backend            # Multi-stage Docker build for FastAPI backend
├── docker-compose.yml            # Multi-container orchestration (PostgreSQL + Backend + Frontend)
├── README.md                     # Project overview and hackathon demo documentation
│
├── backend/                      # Python FastAPI Backend
│   ├── requirements.txt          # Python package dependencies
│   ├── app/
│   │   ├── config.py             # Settings, directories, database URL configuration
│   │   ├── main.py               # FastAPI initialization, middleware, routes, WebSocket loop
│   │   ├── api/                  # 12 REST API Router modules
│   │   │   ├── anomalies.py      # /api/anomalies endpoint
│   │   │   ├── assistant.py      # /api/assistant/query endpoint
│   │   │   ├── dashboard.py      # /api/dashboard endpoint
│   │   │   ├── incidents.py      # /api/incidents endpoints (CRUD & analytics)
│   │   │   ├── machines.py       # /api/machines endpoints & telemetry history
│   │   │   ├── operators.py      # /api/operators endpoints & fleet baselines
│   │   │   ├── predictions.py    # /api/predictions endpoints & ML metrics
│   │   │   ├── reports.py        # /api/reports/generate audit reports
│   │   │   ├── safety.py         # /api/safety/live & /events endpoints
│   │   │   ├── simulation.py     # /api/simulation/inject & /reset endpoints
│   │   │   ├── tasks.py          # /api/tasks endpoints (listing, detail, status update)
│   │   │   └── training.py       # /api/training courses & quiz submission
│   │   ├── db/
│   │   │   ├── database.py       # SQLAlchemy engine, session maker, get_db dependency
│   │   │   └── models.py         # 12 SQLAlchemy ORM table models
│   │   ├── schemas/
│   │   │   └── schemas.py        # Pydantic v2 validation schemas
│   │   └── services/
│   │       ├── anomaly_service.py       # Anomaly inference wrapper
│   │       ├── assistant_service.py     # Deterministic intent engine + local RAG
│   │       ├── prediction_service.py    # Task duration prediction wrapper
│   │       ├── recommendation_service.py# Multi-domain explainable recommendations
│   │       ├── safety_engine.py         # 8-rule additive safety scoring engine
│   │       └── simulation_service.py    # Singleton simulation state, radar, hazard injection
│   └── tests/
│       ├── test_anomaly_detection.py    # Tests for Isolation Forest anomaly pipeline
│       ├── test_api_endpoints.py        # TestClient tests for FastAPI HTTP routes
│       ├── test_assistant_service.py    # Tests for intent routing and disclaimers
│       ├── test_safety_engine.py        # Tests for all 8 safety rules and score thresholds
│       └── test_task_prediction.py      # Tests for regression inference and confidence bounds
│
├── data/                         # SQLite DB and synthetic CSV datasets
│   ├── cat_operator_iq.db        # SQLite database file containing seeded relational data
│   ├── courses.csv               # 6 training courses
│   ├── incidents.csv             # 300 synthetic safety incidents
│   ├── machine.csv               # 50 machines (Excavators, Loaders, Dozers, Graders, etc.)
│   ├── operators.csv             # 100 operators with varying experience and scores
│   ├── safety_events.csv         # 500 historical safety events
│   ├── tasks.csv                 # 2,000 tasks with real and estimated completion times
│   ├── telemetry.csv             # 10,000 telemetry records
│   └── training_progress.csv     # 500 course progress records
│
├── database/                     # SQL DDL schemas
│   └── schema.sql                # Complete relational schema (PostgreSQL & SQLite compatible)
│
├── frontend/                     # React + TypeScript + Vite SPA
│   ├── package.json              # Frontend npm dependencies and scripts
│   ├── vite.config.ts            # Vite dev configuration with proxy to port 8000
│   ├── Dockerfile.frontend       # Production Nginx container build
│   ├── src/
│   │   ├── main.tsx              # React DOM entrypoint
│   │   ├── App.tsx               # Root component, router setup, providers
│   │   ├── index.css             # Tailwind base styles, typography, scrollbars
│   │   ├── context/
│   │   │   ├── RoleContext.tsx        # Role switcher (Operator vs Supervisor), active machine/operator
│   │   │   └── SimulationContext.tsx  # WebSocket telemetry consumer, fallback polling, hazard injector
│   │   ├── services/
│   │   │   └── api.ts                 # Type-safe fetch API client
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript interfaces matching backend schemas
│   │   ├── components/
│   │   │   ├── Navbar.tsx             # Top navigation bar with role toggle and status
│   │   │   ├── Sidebar.tsx            # Left navigation bar with 9 category items
│   │   │   ├── ProximityRadar.tsx     # 2D Canvas radar component showing machine & ground workers
│   │   │   ├── SafetyAlertBanner.tsx  # Exception-first alert banner with advisory disclaimer
│   │   │   ├── SimulationControls.tsx # Interactive button bar to inject live hazards
│   │   │   ├── TelemetryLiveFeed.tsx  # Gauge cards displaying real-time sensor metrics
│   │   │   ├── IncidentModal.tsx      # Modal form to log a new safety incident
│   │   │   ├── QuizModal.tsx          # Interactive practical quiz modal
│   │   │   ├── StateViews.tsx         # Loading skeletons and error boundary displays
│   │   │   └── ui/                    # Reusable UI component library (Button, Card, Badge, Drawer, etc.)
│   │   └── pages/
│   │       ├── DashboardPage.tsx      # Main in-cab operator dashboard
│   │       ├── TasksPage.tsx          # Task list, ML prediction breakdown, status toggles
│   │       ├── MachineHealthPage.tsx  # Fleet health overview, Recharts telemetry history
│   │       ├── SafetyPage.tsx         # Live radar, 8-rule breakdown, safety events log
│   │       ├── BehaviorPage.tsx       # Operator fatigue, idling, and safety score analytics
│   │       ├── TrainingPage.tsx       # Training modules, progress tracking, quiz launcher
│   │       ├── IncidentsPage.tsx      # Incident tracking, filtering, resolution actions
│   │       ├── AssistantPage.tsx      # AI Assistant chat interface with suggestions & evidence
│   │       └── ReportsPage.tsx        # Shift audit report generator with print view
│
├── knowledge_base/               # Markdown domain guides for Assistant RAG
│   ├── machine_guides/
│   │   └── cat_336_excavator.md           # Specifications, capacities, operating ranges
│   ├── maintenance/
│   │   └── vibration_diagnostics.md       # Vibration troubleshooting thresholds
│   ├── safety_guides/
│   │   ├── proximity_exclusion_zones.md   # 3m critical zone protocols
│   │   └── seatbelt_and_rops.md           # ROPS survival guidelines
│   └── training/
│       └── anti_idling_techniques.md      # Auto-idle techniques and fuel efficiency
│
├── ml/                           # Machine Learning training & evaluation scripts
│   ├── data_preprocessing.py     # OneHotEncoder for task/weather + StandardScaler for numeric metrics
│   ├── feature_engineering.py    # Weather severity index, machine wear index, thermal ratio
│   ├── task_time_model.py        # TaskTimePredictor class (RandomForest & GradientBoosting)
│   ├── anomaly_detection.py      # TelemetryAnomalyDetector class (IsolationForest)
│   ├── model_registry.py         # Singleton model loaders for trained joblib files
│   ├── train_models.py           # Training pipeline: trains models and saves metrics.json
│   └── evaluate_models.py        # Model evaluation utility
│
├── models/                       # Serialized trained model binaries
│   ├── anomaly_model.joblib      # Fitted Isolation Forest model
│   ├── task_time_model.joblib    # Fitted Gradient Boosting regressor
│   └── metrics.json              # Model evaluation metrics (MAE: 4.13m, R²: 0.9642)
│
└── scripts/                      # Setup and verification scripts
    ├── generate_data.py          # Generates synthetic datasets with correlated distributions
    ├── seed_database.py          # Seeds database from generated CSV files
    └── verify_demo.py            # End-to-end 9-scene live verification test script
```

---

## 6. Technology Stack

Every technology in this project was chosen for a specific industrial software requirement:

| Technology | Role in Project | Location | Why Used | What Happens If Removed |
| :--- | :--- | :--- | :--- | :--- |
| **React 18** | Frontend UI Framework | `frontend/src/` | Declarative component model and reactive state updates when receiving high-frequency telemetry. | No interactive UI; would need plain HTML or server-rendered templates. |
| **TypeScript** | Static Typing | `frontend/src/**/*.tsx`, `types/index.ts` | Eliminates runtime typos and guarantees frontend data shapes match backend Pydantic schemas. | Bugs would slip into production during telemetry parsing or API responses. |
| **Vite 5** | Frontend Build Tool & Dev Server | `frontend/vite.config.ts` | Sub-second hot-module reloading and native proxying of API/WebSocket traffic. | Slower builds and complex Webpack configuration required. |
| **Tailwind CSS 3** | UI Styling | `frontend/tailwind.config.js`, `index.css` | High-performance atomic styling without bloated external UI frameworks. | UI styles would break; manual CSS stylesheets would be needed. |
| **Recharts 2** | Metric Visualization | `frontend/src/pages/MachineHealthPage.tsx` | Declarative SVG charting for multi-sensor time-series telemetry trends. | Telemetry trend graphs would disappear. |
| **Lucide React** | Industrial Icons | `frontend/src/components/**/*.tsx` | Clean, crisp, lightweight icons for machinery, safety, alerts, and navigation. | Visual cues on buttons and navigation would be missing. |
| **FastAPI** | Backend Web Framework | `backend/app/main.py`, `backend/app/api/` | High performance (asyncio), automatic OpenAPI docs (`/docs`), and native WebSocket support. | Backend would require Flask or Django with significantly more boilerplate. |
| **Pydantic v2** | Data Validation & Schemas | `backend/app/schemas/schemas.py` | Strict validation of incoming payloads and automatic serialization of models to JSON. | Unvalidated user inputs could crash backend services. |
| **SQLAlchemy 2.0** | Relational ORM | `backend/app/db/` | Database abstraction supporting both local SQLite and production PostgreSQL with identical code. | Raw SQL strings would be needed everywhere, increasing SQL injection risk. |
| **SQLite** | Local Relational Database | `data/cat_operator_iq.db` | Zero-configuration single-file database that runs out of the box on any developer machine. | Developer would be forced to install and configure PostgreSQL before running the app. |
| **PostgreSQL 16** | Production Database | `docker-compose.yml` | Industrial-grade relational database for multi-user concurrent deployment in Docker. | System would remain single-node SQLite without enterprise concurrency. |
| **Scikit-Learn** | Machine Learning | `ml/` | Industry standard library for `IsolationForest` (anomalies) and `GradientBoostingRegressor` (durations). | Custom ML algorithms would need to be written from scratch. |
| **Pandas & NumPy** | Data Processing | `ml/`, `scripts/generate_data.py` | High-speed tabular manipulation and vectorized matrix calculations for telemetry. | Data preparation scripts would be dramatically slower and more complex. |
| **Joblib** | Model Serialization | `models/*.joblib`, `ml/model_registry.py` | Efficient disk persistence and fast loading of trained Scikit-learn pipelines. | Models would have to be retrained on every backend server startup. |
| **WebSockets** | Real-Time Telemetry Push | `backend/app/main.py`, `SimulationContext.tsx` | Pushes live machine state and radar coordinates to clients every 2 seconds without HTTP polling overhead. | High server load from rapid HTTP polling; laggy radar updates. |
| **Docker & Compose** | Containerization | `Dockerfile.*`, `docker-compose.yml` | Packages backend, frontend, and PostgreSQL into deterministic containers runnable on any OS. | "Works on my machine" setup headaches across different operating systems. |

---

## 7. How to Run the Project

### 1. Zero-Dependency Local Setup (Default Mode)

The project is pre-configured to run 100% locally with zero external cloud dependencies.

#### Step 1: Backend Setup
Open a terminal in the project root:

```bash
# 1. Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Generate synthetic data (creates CSV files in ./data)
PYTHONPATH=. python scripts/generate_data.py

# 4. Train the ML models (creates models/*.joblib and models/metrics.json)
PYTHONPATH=. python -m ml.train_models

# 5. Seed the SQLite database (populates ./data/cat_operator_iq.db)
PYTHONPATH=. python scripts/seed_database.py

# 6. Start the FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```

When started, FastAPI logs:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

#### Step 2: Frontend Setup
Open a second terminal window:

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Start Vite development server
npm run dev
```

Vite prints:
```
  VITE v5.2.11  ready in 240 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Open `http://localhost:5173` in your browser.

---

### 2. Docker Compose Setup (PostgreSQL + Containers)

To run the complete containerized stack:

```bash
# Build and launch PostgreSQL, Backend, and Frontend containers
docker-compose up --build
```

Docker Compose spins up:
1. `cat_postgres`: PostgreSQL 16 on port `5432` with automatic health checks (`pg_isready`).
2. `cat_backend`: Python 3.12 container that generates data, trains models, seeds PostgreSQL, and launches Uvicorn on port `8000`.
3. `cat_frontend`: Node build output served by Nginx on port `5173` (mapped from container port 80).

---

## 8. How the Frontend Works

### React for Beginners
If you are new to React, here is what is happening conceptually:
- **Components:** JavaScript functions that return HTML-like code called JSX (e.g., `<Sidebar />`, `<Navbar />`).
- **Props:** Input arguments passed to a component from its parent (e.g., `<KpiCard title="Idle Time" value="8 min" />`).
- **State (`useState`):** Variables that hold dynamic data. When state changes, React automatically re-renders that component.
- **Effects (`useEffect`):** Functions that run when a component first appears on screen (e.g., fetching initial dashboard data).
- **Context (`useContext`):** A global data store accessible by any component without passing props down through every level.

### Frontend Architecture
```
                                 [main.tsx]
                                     │
                                     ▼
                                 [App.tsx]
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
    [RoleProvider]                                   [SimulationProvider]
   (Operator/Supervisor)                           (WebSocket / Live State)
            │                                                 │
            └────────────────────────┬────────────────────────┘
                                     │
                      ┌──────────────┴──────────────┐
                      ▼                             ▼
                 [Navbar.tsx]                  [Sidebar.tsx]
                      │
                      ▼
               [React Router] ──► 9 Page Routes
```

### Deep Dive: Major Frontend Pages

#### 1. Dashboard (`frontend/src/pages/DashboardPage.tsx`)
- **Purpose:** Primary in-cab monitoring console for machine operator Marcus Vance.
- **APIs Called:** `api.getDashboard(activeOperatorId, activeMachineId)`.
- **Live Stream:** Connects to `useSimulation()` to receive live safety scores, radar coordinates, and alerts.
- **Visuals:**
  - `SimulationControls`: Interactive buttons to inject hazards (e.g., worker proximity, vibration spike).
  - `SafetyAlertBanner`: Top alert banner that dynamically changes color (Green $\to$ Yellow $\to$ Orange $\to$ Red) and displays active safety rules.
  - `ProximityRadar`: Live 2D radar screen showing worker distances.
  - `TelemetryLiveFeed`: Real-time gauges for engine temp, vibration, oil pressure, and RPM.
  - Current task progress bar and remaining time indicator.

#### 2. Tasks (`frontend/src/pages/TasksPage.tsx`)
- **Purpose:** Operator shift assignments and AI-predicted completion times.
- **APIs Called:** `api.getTasks()`, `api.getTaskDetail(id)`, `api.updateTaskStatus(id, status)`.
- **Key Feature:** Clicking a task opens a slide-out drawer (`Drawer.tsx`) showing the ML prediction breakdown:
  - Base estimated duration: $60.0\text{ min}$
  - Weather factor: $+7.5\text{ min}$ (Rainy soil conditions)
  - Operator skill factor: $-6.5\text{ min}$ (Expert efficiency bonus)
  - 90% Confidence Interval: $48.0\text{ min} - 61.0\text{ min}$

#### 3. Machines (`frontend/src/pages/MachineHealthPage.tsx`)
- **Purpose:** Fleet equipment status and diagnostic telemetry history.
- **APIs Called:** `api.getMachines()`, `api.getMachineTelemetryHistory(machineId)`.
- **Key Feature:** Calculates a **composite health score** out of 100% using four factors:
  $$\text{Health} = 0.25 \times \text{Temp} + 0.25 \times \text{Vibration} + 0.25 \times \text{Oil} + 0.25 \times \text{Maintenance}$$
  Renders Recharts time-series graphs of historical engine temperature, vibration, and hydraulic pressure.

#### 4. Safety Center (`frontend/src/pages/SafetyPage.tsx`)
- **Purpose:** Detailed site perimeter monitoring and historical safety event audits.
- **APIs Called:** `api.getLiveSafety()`, `api.getSafetyEvents(machineId)`, `api.acknowledgeSafetyEvent(id)`.
- **Key Feature:** Displays the full 8-rule breakdown showing exactly which rules are triggered and how many risk points each contributes. Includes an "Acknowledge" button for logged events.

#### 5. Operator Behavior (`frontend/src/pages/BehaviorPage.tsx`)
- **Purpose:** Tracks operator performance, fatigue accumulation, and idle fuel waste.
- **APIs Called:** `api.getOperators()`, `api.getOperatorDetail(operatorId)`.
- **Visuals:** Compares operator metrics against fleet averages (Safety Score, Task Accuracy, Idle Time, Fatigue Index).

#### 6. Training Hub (`frontend/src/pages/TrainingPage.tsx`)
- **Purpose:** Digital safety learning center with interactive quizzes.
- **APIs Called:** `api.getTraining(operatorId)`, `api.submitQuiz(courseId, answers)`.
- **Key Feature:** Operators can open a course, view video training, and take a 3-question quiz (`QuizModal.tsx`). Submitting a score of $\ge 70\%$ automatically marks the course `Completed` and awards $+1.5\%$ to the operator's training score.

#### 7. Incidents (`frontend/src/pages/IncidentsPage.tsx`)
- **Purpose:** Formal logging and resolution of safety violations.
- **APIs Called:** `api.getIncidents()`, `api.createIncident()`, `api.updateIncident()`, `api.getIncidentAnalytics()`.
- **Key Feature:** Filter incidents by severity (`Low`, `Medium`, `High`, `Critical`) or resolution status. Supervisors can click "Resolve" to enter formal resolution notes.

#### 8. OperatorIQ Assistant (`frontend/src/pages/AssistantPage.tsx`)
- **Purpose:** Conversational domain assistant.
- **APIs Called:** `api.queryAssistant(query, operatorId, machineId)`.
- **Key Feature:** Displays suggested quick-prompt buttons. Returns responses with:
  1. The direct answer.
  2. Concrete telemetry evidence.
  3. Recommended next step.
  4. Mandatory safety advisory disclaimer.
  5. Knowledge base citations.

#### 9. Reports (`frontend/src/pages/ReportsPage.tsx`)
- **Purpose:** One-click generation of printable shift audit documents.
- **APIs Called:** `api.getReport(reportType, operatorId, machineId)`.
- **Supported Reports:** `daily_operator`, `machine_health`, `safety`, `task_efficiency`. Includes a "Print / Save PDF" view styled for shift handovers.

---

## 9. How the Backend Works

FastAPI powers the entire backend of CAT OperatorIQ. It is asynchronous, validates all data through Pydantic v2 schemas, and automatically generates interactive Swagger documentation at `http://localhost:8000/docs`.

### Router Overview

The application registers 12 routers in `backend/app/main.py`:

```python
# backend/app/main.py (lines 43-54)
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
```

### Complete API Endpoint Reference

| Method | Endpoint | Purpose | Input / Query Params | Output | Files Involved |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Root status & safety disclaimer | None | JSON object with project name, tagline, status, and disclaimer | `main.py` |
| `GET` | `/api/health` | Health check & simulation status | None | `{"status": "healthy", "simulation_active": true, ...}` | `main.py` |
| `WS` | `/ws/telemetry` | Real-time WebSocket telemetry stream | WebSocket upgrade | Pushes `LiveTelemetryState` JSON every 2.0 seconds | `main.py`, `simulation_service.py` |
| `GET` | `/api/dashboard` | Aggregated operator dashboard data | `operator_id`, `machine_id` | `DashboardResponse` (KPIs, tasks, health, alerts) | `api/dashboard.py`, `models.py` |
| `GET` | `/api/tasks` | List scheduled or active tasks | `status`, `operator_id`, `limit` | Array of `TaskResponse` objects | `api/tasks.py` |
| `GET` | `/api/tasks/{task_id}` | Detailed task with ML prediction | `task_id` path param | `TaskResponse` with `prediction_details` | `api/tasks.py`, `prediction_service.py` |
| `PUT` | `/api/tasks/{task_id}/status` | Update task status & actual time | `TaskStatusUpdate` body (`status`, `actual_time_min`) | Updated `TaskResponse` | `api/tasks.py` |
| `GET` | `/api/machines` | Fleet machines list with health scores | None | Array of `MachineResponse` with health breakdown | `api/machines.py` |
| `GET` | `/api/machines/{id}` | Machine diagnostic detail | `machine_id` path param | `MachineResponse` with 4 health factors | `api/machines.py` |
| `GET` | `/api/machines/{id}/telemetry` | Historical telemetry time-series | `limit` (default 30) | Array of chronological `Telemetry` records | `api/machines.py` |
| `GET` | `/api/operators` | List fleet operators | `limit` (default 50) | Array of `OperatorResponse` | `api/operators.py` |
| `GET` | `/api/operators/{id}` | Operator detail & fleet baselines | `operator_id` path param | Operator object, fleet baselines, recent safety events | `api/operators.py` |
| `GET` | `/api/safety/live` | Real-time safety state & radar | None | Telemetry, radar coordinates, 8-rule breakdown | `api/safety.py`, `safety_engine.py` |
| `GET` | `/api/safety/events` | Historical safety events log | `machine_id`, `limit` | Array of `SafetyEvent` records | `api/safety.py` |
| `POST`| `/api/safety/events/{id}/acknowledge` | Mark safety event as acknowledged | `event_id` path param | `{"message": "Safety event SE... acknowledged"}` | `api/safety.py` |
| `GET` | `/api/incidents` | Filterable incident records | `severity`, `machine_id`, `resolved` | Array of `IncidentResponse` | `api/incidents.py` |
| `POST`| `/api/incidents` | Manually log a new incident | `IncidentCreate` JSON payload | Newly created `IncidentResponse` | `api/incidents.py` |
| `PUT` | `/api/incidents/{id}` | Resolve safety incident | `IncidentUpdate` (`resolved`, `resolution`) | Updated `IncidentResponse` | `api/incidents.py` |
| `GET` | `/api/incidents/analytics/summary` | Fleet incident frequency analytics | None | Incidents by severity, by type, top machines | `api/incidents.py` |
| `GET` | `/api/anomalies` | Detected telemetry anomalies | `machine_id`, `limit` | Array of `AnomalyResponse` with factors | `api/anomalies.py` |
| `GET` | `/api/training` | Courses list & recommendations | `operator_id` | Courses with quiz questions and recommendations | `api/training.py` |
| `POST`| `/api/training/{id}/quiz` | Evaluate & record quiz submission | `QuizSubmission` (`operator_id`, `answers`) | `{"passed": true, "score_pct": 100.0, ...}` | `api/training.py` |
| `GET` | `/api/predictions/task/{id}` | Direct task ML inference | `task_id` path param | Predicted minutes, confidence bounds, factors | `api/predictions.py` |
| `GET` | `/api/predictions/metrics` | Authentic ML validation metrics | None | Training/test sample counts, MAE, RMSE, R² | `api/predictions.py`, `metrics.json` |
| `POST`| `/api/assistant/query` | Ask the AI Assistant | `AssistantQueryRequest` (`query`, `machine_id`) | `AssistantQueryResponse` (answer, evidence, next step) | `api/assistant.py`, `assistant_service.py` |
| `POST`| `/api/simulation/inject` | Inject hazard for demonstration | `SimulationHazardRequest` (`hazard_type`) | Injection confirmation and auto-logged incident status | `api/simulation.py`, `simulation_service.py` |
| `POST`| `/api/simulation/reset` | Reset simulation to baseline | None | `{"status": "Reset", "hazard": "Nominal baseline"}` | `api/simulation.py` |
| `GET` | `/api/simulation/state` | Current raw simulation snapshot | None | Current tick state dictionary | `api/simulation.py` |
| `GET` | `/api/reports/generate` | Generate formal shift audit report | `report_type`, `operator_id`, `machine_id` | Structured report JSON for on-screen/print rendering | `api/reports.py` |

---

## 10. Database

### Database Strategy
CAT OperatorIQ uses **SQLAlchemy 2.0** with dual compatibility:
1. **Local Mode (Default):** SQLite (`data/cat_operator_iq.db`) configured with `check_same_thread: False`.
2. **Container Mode:** PostgreSQL 16 via Docker (`postgresql://cat_user:cat_password@postgres:5432/cat_operator_iq`).

The database schema is defined in DDL (`database/schema.sql`) and modeled in Python (`backend/app/db/models.py`).

### Relational Schema Reference

| Table Name | Primary Purpose | Key Columns | Relationships |
| :--- | :--- | :--- | :--- |
| `users` | User accounts and authentication roles | `user_id`, `username`, `role` (`Operator`, `Supervisor`) | Has many `operators` |
| `operators` | Machine operator profiles, skills, and cumulative metrics | `operator_id`, `name`, `skill_level`, `safety_score`, `fatigue_score` | Foreign key to `users`; Has many `tasks`, `telemetry`, `incidents` |
| `machines` | Heavy equipment specifications and operational baselines | `machine_id`, `machine_type`, `machine_model`, `engine_hours`, `location` | Has many `tasks`, `telemetry`, `safety_events`, `anomalies` |
| `tasks` | Daily work orders (excavation, grading, trenching) | `task_id`, `task_type`, `estimated_time_min`, `actual_time_min`, `status` | Belongs to `machines` & `operators`; Has one `predictions` |
| `telemetry` | High-frequency IoT machine time-series records | `telemetry_id`, `timestamp`, `engine_temperature`, `vibration`, `seatbelt_status` | Belongs to `machines`, `operators`, `tasks` |
| `safety_events` | Granular safety violation occurrences | `event_id`, `timestamp`, `event_type`, `severity`, `risk_score`, `acknowledged` | Belongs to `machines` & `operators` |
| `incidents` | Formal workplace safety incidents and resolution logs | `incident_id`, `incident_type`, `severity`, `description`, `resolved`, `resolution` | Belongs to `machines` & `operators` |
| `anomalies` | Mechanical & operational outliers detected by ML | `anomaly_id`, `anomaly_score`, `risk_level`, `reason`, `factors` (JSON) | Belongs to `machines` |
| `training_courses`| Equipment operation and safety courses | `course_id`, `category`, `title`, `duration_min`, `video_url`, `quiz_data` (JSON) | Has many `training_progress` |
| `training_progress`| Operator progress and scores on training modules | `progress_id`, `completion_status`, `score`, `attempts`, `completed_at` | Belongs to `operators` & `training_courses` |
| `predictions` | Serialized ML task duration predictions and factors | `prediction_id`, `predicted_time_min`, `confidence_lower_min`, `factors_json` | One-to-one foreign key to `tasks` |
| `recommendations`| AI/rule-generated operational advisory recommendations | `recommendation_id`, `category`, `priority`, `title`, `recommendation`, `reason`| Optional foreign keys to `machines` & `operators` |

### Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    users ||--o{ operators : "user_id"
    operators ||--o{ tasks : "operator_id"
    operators ||--o{ telemetry : "operator_id"
    operators ||--o{ safety_events : "operator_id"
    operators ||--o{ incidents : "operator_id"
    operators ||--o{ training_progress : "operator_id"

    machines ||--o{ tasks : "machine_id"
    machines ||--o{ telemetry : "machine_id"
    machines ||--o{ safety_events : "machine_id"
    machines ||--o{ incidents : "machine_id"
    machines ||--o{ anomalies : "machine_id"

    tasks ||--o{ telemetry : "task_id"
    tasks ||--|| predictions : "task_id"

    training_courses ||--o{ training_progress : "course_id"
```

### Performance Indexes
To ensure fast queries over millions of telemetry rows, `database/schema.sql` defines multi-column composite indexes:
- `idx_telemetry_machine_time` on `telemetry(machine_id, timestamp)`
- `idx_telemetry_operator_time` on `telemetry(operator_id, timestamp)`
- `idx_safety_events_machine` on `safety_events(machine_id, timestamp)`
- `idx_tasks_machine` on `tasks(machine_id)`
- `idx_anomalies_machine` on `anomalies(machine_id)`

---

## 11. Data Flow

### How Data Moves from Zero to Screen

```
   [Synthetic Generator: generate_data.py]
                     │
                     ▼
          [CSV Files in ./data/*.csv]
                     │
                     ▼
     [Database Seeder: seed_database.py]
                     │
                     ▼
   [Relational Storage: SQLite / PostgreSQL]
                     │
                     ├──► [Loaded into Memory by FastAPI on Startup]
                     │
                     ▼
 [Live Telemetry Stream: SimulationService] ──► [SafetyEngine (8 Rules)]
                     │                      ──► [AnomalyService (ML)]
                     │
                     ▼
             [FastAPI Backend]
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 [WebSocket Push]        [HTTP REST JSON]
  (/ws/telemetry)          (/api/dashboard)
         │                       │
         └───────────┬───────────┘
                     ▼
         [React Client: api.ts & SimulationContext]
                     │
                     ▼
  [Rendered UI: Dashboard, Proximity Radar, Alerts]
```

### Trace of 4 Real User Actions

#### Action 1: Viewing a Machine Detail
1. User clicks machine `EXC001` on `MachineHealthPage.tsx`.
2. Component calls `api.getMachineDetail("EXC001")` and `api.getMachineTelemetryHistory("EXC001")`.
3. FastAPI executes `get_machine_detail()` in `backend/app/api/machines.py`.
4. Backend computes composite health percentage using 4 weighted components:
   $$\text{Health} = 0.25 \times \text{Temp} + 0.25 \times \text{Vib} + 0.25 \times \text{Oil} + 0.25 \times \text{Maint}$$
5. Telemetry history is fetched, reversed into chronological order, and returned as JSON.
6. Recharts renders the time-series area charts for engine temperature and vibration.

#### Action 2: Creating a New Safety Incident
1. User clicks "+ Log Incident" on `IncidentsPage.tsx`, opening `IncidentModal.tsx`.
2. User submits form: Machine `EXC001`, Operator `OP001`, Type `Proximity Hazard`, Severity `Critical`.
3. Frontend sends `POST /api/incidents`.
4. Endpoint creates a new `Incident` record with a generated UUID (`INC04A1B2`) and persists it via `db.commit()`.
5. Frontend receives new incident and prepends it to the table list.

#### Action 3: Injecting a Hazard (Worker Proximity)
1. User clicks "Worker Proximity" on `SimulationControls.tsx`.
2. Frontend sends `POST /api/simulation/inject` with `{"hazard_type": "worker_proximity"}`.
3. `SimulationService` moves Worker W03 to distance $2.1\text{m}$ inside the machine's critical radius.
4. Auto-incident and safety event records are inserted into the database.
5. On the next 2-second WebSocket tick, `SafetyEngine` calculates score $45.0$ (`CRITICAL`).
6. `ProximityRadar.tsx` draws the worker dot red, and `SafetyAlertBanner.tsx` turns red.

#### Action 4: Submitting a Training Quiz
1. User takes quiz for course `TRN001` in `QuizModal.tsx`.
2. Frontend sends `POST /api/training/TRN001/quiz` with selected answers.
3. Backend checks answers against `training_courses.quiz_data`. Score $\ge 70\%$ marks course completed.
4. Database updates operator training competency score by $+1.5\%$.

---

## 12. Synthetic Data

Because production Caterpillar heavy machinery telemetry is proprietary, this project features a realistic synthetic data generator in `scripts/generate_data.py`.

### Why Synthetic Data?
1. **Public Availability:** Real heavy equipment CAN bus and IoT telemetry contains sensitive client and site information.
2. **Deterministic Reproducibility:** Uses `RANDOM_SEED=42` so that anyone running the script gets the exact same dataset.
3. **Statistical Realism:** Does not generate purely random numbers. Uses mathematical distributions reflecting real machine physics.

### How Values Are Generated

```
                   ┌────────────────────────────────────────┐
                   │    scripts/generate_data.py (Seed 42)  │
                   └───────────────────┬────────────────────┘
                                       │
         ┌──────────────┬──────────────┼──────────────┬──────────────┐
         ▼              ▼              ▼              ▼              ▼
     Operators       Machines        Tasks        Telemetry     Safety/Incidents
     (100 rows)      (50 rows)    (2,000 rows)  (10,000 rows)     (800 rows)
```

1. **Operators (`operators.csv`):**
   - Experience follows an **exponential distribution** ($\mu = 5.0\text{ years}$).
   - Operators with $< 2.5$ years experience are tagged `Beginner`, with lower safety scores ($\mu = 78\%$) and higher incident probabilities (Poisson $\lambda = 1.8$).
   - Operators with $> 7.0$ years experience are tagged `Expert`, with higher safety scores ($\mu = 95\%$).
   - Demo operator `OP001` is hardcoded as **Marcus Vance** (8.5 years experience, Expert, 94% training, 92.5% safety score).

2. **Machines (`machine.csv`):**
   - Real Caterpillar models: `CAT 336 Heavy Duty` (Excavator), `CAT 966M` (Wheel Loader), `CAT D8T` (Dozer), `CAT 140` (Grader), `CAT 745` (Dump Truck).
   - Machine age correlates with baseline wear: older machines have slightly higher baseline vibration ($+0.12\text{ mm/s per year}$) and higher baseline temperature ($+0.7^\circ\text{C per year}$).

3. **Tasks (`tasks.csv`):**
   - Base duration is dictated by task type: Earth Excavation ($60\text{ min}$), Trenching ($75\text{ min}$), Material Loading ($45\text{ min}$), Demolition ($110\text{ min}$).
   - Multipliers modify actual time:
     $$\text{Actual Time} = \text{Base} \times \text{WeatherMult} \times \text{SkillMult} \times \text{AgeMult} \times \mathcal{N}(1.0, 0.06)$$
     - Weather multipliers: `Sunny` ($0.96$), `Rainy` ($1.22$), `Storm` ($1.45$).
     - Operator skill multipliers: `Beginner` ($1.18$), `Intermediate` ($1.00$), `Expert` ($0.88$).

4. **Telemetry (`telemetry.csv`):**
   - 10,000 records simulating 20 days of sensor polling.
   - Normal operating conditions: Engine temp $\sim 88^\circ\text{C}$, oil pressure $\sim 42\text{ psi}$, vibration $\sim 1.8\text{ mm/s}$, hydraulic pressure $\sim 280\text{ bar}$, RPM $\sim 1850$.
   - Realistic anomalies injected probabilistically: $3.5\%$ seatbelt unfastened, $4.5\%$ ground worker detected within caution radius, $3.0\%$ engine overheating ($106-118^\circ\text{C}$), $3.5\%$ abnormal vibration ($3.9-6.5\text{ mm/s}$).

---

## 13. Machine Learning

### What is Machine Learning?
Machine learning is programming computers to learn patterns from historical data instead of writing manual rules for every single situation.
- **Supervised Learning (Regression):** The model learns from past examples with known outcomes (e.g., past tasks with actual completion times) to predict future numbers.
- **Unsupervised Learning (Anomaly Detection):** The model studies normal operating data and flags any new data point that looks geometrically unusual without needing pre-labeled tags.

### ML Models Used in CAT OperatorIQ

| Model | Type | Algorithm | Purpose | Location |
| :--- | :--- | :--- | :--- | :--- |
| **Task Time Predictor** | Supervised Regression | `GradientBoostingRegressor` | Predicts task completion duration with 90% confidence intervals and factor explanations. | `ml/task_time_model.py` |
| **Telemetry Anomaly Detector** | Unsupervised Outlier | `IsolationForest` | Identifies unusual multi-sensor combinations and generates diagnostic explanations. | `ml/anomaly_detection.py` |

---

## 14. Task Prediction

### The Problem
Standard project schedules rely on static manual estimates (e.g., "excavating always takes 60 minutes"). But on a real construction site, rain, operator inexperience, machine wear, and material cycle counts significantly change the time required.

### The ML Solution: Gradient Boosting Regression
Implemented in `ml/task_time_model.py` and trained in `ml/train_models.py`.

```
Task Features (Task Type, Weather, Skill, Machine Age, Cycles, Distance)
       │
       ▼
TaskDataPreprocessor (OneHotEncoder + StandardScaler)
       │
       ▼
GradientBoostingRegressor (100 estimators, max_depth=5, lr=0.08)
       │
       ▼
Predicted Duration (minutes) ± 90% Confidence Interval (± 1.645 * residual_std)
       │
       ▼
Factor Attribution Engine (Weather Δ, Skill Δ, Machine Age Δ, Cycle Count Δ)
```

### Verified Model Performance Metrics (`models/metrics.json`)

The pipeline trains both `RandomForestRegressor` and `GradientBoostingRegressor`, evaluates both on a 20% validation split, and selects the winner:

| Metric | Random Forest | Gradient Boosting (Selected) | Beginner Explanation |
| :--- | :--- | :--- | :--- |
| **MAE** | 4.62 minutes | **4.13 minutes** | On average, predictions are off by only 4.1 minutes. |
| **RMSE** | 6.71 minutes | **5.91 minutes** | Penalizes rare large errors; shows consistent precision. |
| **$R^2$ Score** | 0.9539 | **0.9642** | Explains **96.4%** of the variance in actual task completion time. |
| **Training Samples**| 1,588 | 1,588 | Verified synthetic dataset training split. |
| **Test Samples** | 397 | 397 | Verified synthetic dataset test split. |

### Explainable Factor Attribution
Operators do not trust black-box numbers. The model provides an attribution breakdown:
```python
# ml/task_time_model.py (lines 56-100)
# Weather impact breakdown
weather_deltas = {"Rainy": +7.5, "Storm": +14.0, "Windy": +3.2, "Sunny": -2.0}
# Operator skill breakdown
skill_deltas = {"Expert": -6.5, "Intermediate": 0.0, "Beginner": +8.0}
# Machine wear breakdown: +1.8 min per year above baseline
# Load cycles breakdown: +1.2 min per cycle above baseline of 15
```

If a task is predicted to take **54 minutes**, the operator sees:
- Baseline: 60.0 min
- Weather (Rainy): $+7.5\text{ min}$
- Skill (Expert): $-6.5\text{ min}$
- Machine Age (2.4 yrs): $+0.7\text{ min}$
- Load Cycles (18 cycles): $+3.6\text{ min}$
- **Final Prediction: 54.0 min (Confidence Range: 48.0 – 60.0 min)**

---

## 15. Anomaly Detection

### What is an Anomaly?
In heavy machinery telemetry, an anomaly is not just a single sensor exceeding a limit. An anomaly is an **unusual combination of readings** that diverges from nominal machine baselines.

For example:
- A machine idling at 1,800 RPM with low vibration is normal.
- A machine running at 1,800 RPM with vibration of $4.2\text{ mm/s}$ and declining oil pressure is an anomaly indicating mechanical stress or bearing failure.

### Isolation Forest Explained
Implemented in `ml/anomaly_detection.py`.

```
Isolation Forest Principle:
Normal points require many random splits to isolate in feature space.
Anomalous outliers exist in sparse regions and are isolated quickly (short tree depth).

   Normal Clusters (Dense)               Anomaly (Sparse Outlier)
      ● ● ● ● ●                                    ★
     ● ● ● ● ● ●                                (Isolated in 2 splits!)
      ● ● ● ● ●
  (Requires 10+ splits)
```

### Features Monitored
1. `engine_temperature` (Nominal: $88.0^\circ\text{C}$, $\sigma = 5.0$)
2. `oil_pressure` (Nominal: $42.0\text{ psi}$, $\sigma = 4.0$)
3. `hydraulic_pressure` (Nominal: $280.0\text{ bar}$, $\sigma = 15.0$)
4. `engine_rpm` (Nominal: $1850\text{ RPM}$, $\sigma = 120.0$)
5. `vibration` (Nominal: $1.8\text{ mm/s}$, $\sigma = 0.4$)
6. `idling_time_min` (Nominal: $8.0\text{ min}$, $\sigma = 6.0$)

### Anomaly Score Mapping
`model.decision_function()` produces raw decision scores (typically $-0.30$ to $+0.15$). The service normalizes this to a human-friendly $0 - 100$ severity index:
$$\text{Severity} = \text{clip}\left(\frac{0.15 - \text{RawScore}}{0.35} \times 100,\; 0.0,\; 100.0\right)$$

- $\ge 75.0$ or $\ge 3$ factor deviations $\to$ `CRITICAL`
- $\ge 50.0$ or $\ge 2$ factor deviations $\to$ `HIGH`
- $\ge 30.0$ or $\ge 1$ factor deviation $\to$ `MEDIUM`
- $< 30.0$ $\to$ `LOW`

---

## 16. Safety Engine

### Why Rule-Based Instead of Pure AI?
In construction life safety, **nondeterministic black-box models are unacceptable**. An operator or safety inspector must know with 100% mathematical certainty why a hazard was triggered.

The **Safety Engine** (`backend/app/services/safety_engine.py`) is an auditable, rule-based scoring engine evaluating **8 explicit industrial rules**.

### The 8 Safety Rules

```mermaid
graph TD
    Telem["Telemetry Record"] --> R1["Rule 1: Seatbelt Unfastened (+35 pts)"]
    Telem --> R2["Rule 2: Worker Proximity (<3m: +45 pts, 3-6m: +25 pts)"]
    Telem --> R3["Rule 3: High Fatigue (>=0.75: +30 pts, >=0.5: +15 pts)"]
    Telem --> R4["Rule 4: Excessive Idling (>=45m: +20 pts, >=25m: +10 pts)"]
    Telem --> R5["Rule 5: Engine Overheating (>=105°C: +35 pts, >=98°C: +15 pts)"]
    Telem --> R6["Rule 6: Severe Vibration (>=3.8 mm/s: +30 pts, >=2.8: +15 pts)"]
    Telem --> R7["Rule 7: Repeated Events (>=3 events: +25 pts, >=2: +12 pts)"]
    Telem --> R8["Rule 8: Weather + Load Combo (Rain/Storm + load>=18t: +20 pts)"]

    R1 & R2 & R3 & R4 & R5 & R6 & R7 & R8 --> Sum["Sum Points & Clamp to [0, 100]"]
    Sum --> RiskBand{"Risk Band Mapping"}
    RiskBand -->|0 - 30| Safe["LOW: SAFE"]
    RiskBand -->|31 - 60| Warn["MEDIUM: WARNING"]
    RiskBand -->|61 - 80| High["HIGH: ACTION REQUIRED"]
    RiskBand -->|81 - 100| Crit["CRITICAL: IMMEDIATE HAZARD"]
```

### Exact Numerical Example
Suppose machine `EXC001` is operating and the following telemetry arrives:
- `seatbelt_status`: `"Fastened"` $\to 0.0$ pts
- `worker_detected`: `True`, `proximity_distance_m`: `2.1` $\to +45.0$ pts (**RULE_2_PROXIMITY_CRITICAL**)
- `vibration`: `4.2 mm/s` $\to +30.0$ pts (**RULE_6_ABNORMAL_VIBRATION**)
- `fatigue_indicator`: `0.15` $\to 0.0$ pts

$$\text{Raw Risk} = 45.0 + 30.0 = 75.0$$
$$\text{Normalized Risk Score} = 75.0 \implies \mathbf{HIGH\; RISK}$$

If the operator also unfastens their seatbelt:
$$\text{Raw Risk} = 75.0 + 35.0 = 110.0 \implies \text{Clamped to } \mathbf{100.0} \implies \mathbf{CRITICAL}$$

### Mandatory Safety Disclaimer
Every safety response in the system includes Caterpillar's standard industrial advisory notice:
> *"AI-generated recommendations are advisory and must not replace official operating procedures, safety procedures, operator training, or professional judgment."*

---

## 17. AI Assistant

### How It Works
The assistant is implemented in `backend/app/services/assistant_service.py` and exposed via `POST /api/assistant/query`.

```
User Query: "Why is EXC001 showing a warning?"
       │
       ▼
Token Normalization & Intent Routing
       │
       ├──► Intent 1: Tasks & Schedule ("task", "schedule", "assigned")
       ├──► Intent 2: Safety & Warning ("warning", "alert", "risk", "hazard")
       ├──► Intent 3: Task Duration & ETA ("how long", "predicted", "eta", "time")
       ├──► Intent 4: Machine Health ("health", "performance", "temp", "oil")
       ├──► Intent 5: Incidents ("incident", "log", "safety event")
       ├──► Intent 6: Training & Courses ("training", "course", "quiz")
       └──► Intent 7: General Fallback
       │
       ▼
Knowledge Base Retrieval (RAG over knowledge_base/*.md)
       │
       ▼
Contextual Synthesis (Injects active operator, machine ID, live sensors)
       │
       ▼
Structured Response (Answer, Evidence, Recommended Next Step, Citations, Disclaimer)
```

### Knowledge Base Documents
The assistant searches local markdown documents in `knowledge_base/`:
- `cat_336_excavator.md`: Engine specs ($311\text{ HP}$), hydraulic relief ($350\text{ bar}$), bucket capacities.
- `vibration_diagnostics.md`: Normal ($< 2.5\text{ mm/s}$), elevated ($2.8-3.8\text{ mm/s}$), critical ($> 3.8\text{ mm/s}$) vibration troubleshooting.
- `proximity_exclusion_zones.md`: Safe ($> 6\text{m}$), caution ($3-6\text{m}$), critical ($< 3\text{m}$) protocols.
- `seatbelt_and_rops.md`: Rollover Protective Structure requirements and injury statistics.
- `anti_idling_techniques.md`: Auto-idle settings and fuel burn savings.

### Why Deterministic Fallback Is Essential
In an open-pit mine or remote quarry, cellular and satellite connectivity can drop completely. A cloud-only LLM would leave the operator without answers. OperatorIQ's deterministic RAG runs **100% locally and offline** without requiring external API keys.

---

## 18. Real-Time System

### WebSockets for Beginners
A standard HTTP request is a single question-and-answer exchange (the client asks, the server responds, the connection closes).
A **WebSocket** is an open two-way telephone call. Once connected, the server can continuously stream data to the browser every 2 seconds without the browser having to ask.

### The Simulation Engine (`backend/app/services/simulation_service.py`)
Because we are not connected to a physical Caterpillar machine CAN bus in this sandbox, `SimulationService` simulates the physical machine:

1. **State Evolution (`step()` method):**
   - Increments engine hours by $0.001\text{ hours}$ per tick.
   - Adds realistic Gaussian noise: vibration ($\pm 0.05\text{ mm/s}$), engine temperature ($\pm 0.2^\circ\text{C}$), engine RPM ($\pm 15\text{ RPM}$).
2. **2D Radar Coordinates:**
   - Simulates 3 ground workers (`W01`, `W02`, `W03`) in polar coordinates (distance in meters, angle in degrees).
   - Converts polar coordinates to Cartesian $(x, y)$ for the HTML5 canvas:
     $$x = \text{distance} \times \cos(\text{radians}(\text{angle}))$$
     $$y = \text{distance} \times \sin(\text{radians}(\text{angle}))$$
3. **Hazard Injection:**
   The `inject_hazard(type)` method allows instant live demonstration:
   - `worker_proximity`: Moves Worker W03 into the critical 2.1m zone.
   - `seatbelt_unfastened`: Sets `seatbelt_status = "Unfastened"`.
   - `vibration_spike`: Spikes vibration to $4.2\text{ mm/s}$ and drops oil pressure to $28.0\text{ psi}$.
   - `overheating`: Raises engine temperature to $108.5^\circ\text{C}$.
   - `idle_excess`: Sets idling duration to $48\text{ minutes}$.
   - `reset`: Restores all sensors to nominal baseline.

---

## 19. Incident Management

### Incident Lifecycle
```mermaid
stateDiagram-v2
    [*] --> Ingestion : Automated Hazard Injection OR Manual Modal Form
    Ingestion --> Open : Created (resolved = false)
    Open --> UnderReview : Shift Supervisor Inspects Telemetry & Operator
    UnderReview --> Resolved : Supervisor Enters Resolution Notes (resolved = true)
    Resolved --> [*]
```

### Data Captured in Every Incident
- `incident_id`: Unique identifier (e.g., `INC04A1B2`).
- `timestamp`: UTC creation time.
- `machine_id`: The machine involved (e.g., `EXC001`).
- `operator_id`: The assigned operator (e.g., `OP001`).
- `incident_type`: Category (`Proximity Hazard`, `Seatbelt Violation`, `Overheating`, `Mechanical Anomaly`).
- `severity`: `Low`, `Medium`, `High`, `Critical`.
- `description`: Detailed description of the event.
- `location`: Exact work zone (e.g., `Site Alpha - Sector 4 Foundation`).
- `resolved`: Boolean flag (`true` / `false`).
- `resolution`: Formal explanation of corrective action taken.

---

## 20. Training System

The Training Hub ensures operator competency directly addresses real safety infractions.

### The Training Loop
```
1. Operator incurs 3 Proximity Warnings during excavation shift.
       │
       ▼
2. RecommendationService flags high-priority training recommendation:
   "Complete TRN001: Proximity Safety & Ground Worker Awareness"
       │
       ▼
3. Operator navigates to Training Hub, reviews video module.
       │
       ▼
4. Operator opens QuizModal, answers 3 domain questions:
   - What is mandatory action when worker enters <3.0m zone? (Pause movement)
   - Why is seatbelt mandatory in ROPS? (Prevents ejection in rollover)
   - What indicates hydraulic cavitation? (High screeching & erratic response)
       │
       ▼
5. Backend evaluates submission (POST /api/training/TRN001/quiz)
       │
       ▼
6. Score >= 70%:
   - Course marked COMPLETED
   - Operator cumulative training score increases by +1.5%
```

---

## 21. Frontend ↔ Backend

All communication uses standard web protocols:

```
[React Browser] ──── HTTP GET / POST / PUT ───► [Nginx / Vite Proxy] ────► [FastAPI Uvicorn]
               ◄─── JSON Payload ────────────                       ◄────
               
[React Browser] ◄─── WebSocket Messages ─────── [Nginx / Vite Proxy] ◄──── [FastAPI /ws/telemetry]
```

### JSON Format Example
When the frontend asks for live safety state (`GET /api/safety/live`), the backend responds with strict JSON:
```json
{
  "telemetry": {
    "machine_id": "EXC001",
    "engine_temperature": 88.5,
    "vibration": 1.75,
    "oil_pressure": 43.0,
    "seatbelt_status": "Fastened",
    "proximity_distance_m": 8.5,
    "worker_detected": false
  },
  "safety_score": 12.0,
  "risk_level": "LOW",
  "status_label": "SAFE",
  "active_alerts": [],
  "radar_objects": [
    {"id": "W01", "name": "Worker A", "distance": 8.4, "angle": 45.0, "x": 5.94, "y": 5.94, "status": "SAFE"}
  ],
  "advisory_disclaimer": "AI-generated recommendations are advisory and must not replace official operating procedures..."
}
```

---

## 22. Complete Request Lifecycle

Let's follow one request line-by-line across every file: **`GET /api/dashboard`**.

### 1. Frontend Trigger
In `frontend/src/pages/DashboardPage.tsx`:
```tsx
// Line 28: api call triggered inside useEffect
const res = await api.getDashboard(activeOperatorId, activeMachineId);
setData(res);
```

### 2. API Service Wrapper
In `frontend/src/services/api.ts`:
```typescript
// Line 10: Constructs query string and fetches endpoint
async getDashboard(operatorId = 'OP001', machineId = 'EXC001'): Promise<DashboardData> {
  const res = await fetch(`${API_BASE}/dashboard?operator_id=${operatorId}&machine_id=${machineId}`);
  if (!res.ok) throw new Error('Failed to load dashboard');
  return res.json();
}
```

### 3. FastAPI Route Handler
In `backend/app/api/dashboard.py`:
```python
# Line 12-16: Route decorator with dependency injection for DB session
@router.get("")
def get_dashboard_data(operator_id: str = "OP001", machine_id: str = "EXC001", db: Session = Depends(get_db)):
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()
```

### 4. Database Query & Aggregation
```python
# Lines 28-36: Real database queries calculate shift statistics
total_tasks_today = db.query(Task).filter(Task.operator_id == operator_id).count()
completed_tasks = db.query(Task).filter(Task.operator_id == operator_id, Task.status == "Completed").count()
avg_task_time_row = db.query(func.avg(Task.actual_time_min)).filter(Task.actual_time_min.isnot(None)).scalar()
```

### 5. Live Simulation Integration
```python
# Line 64: Obtains current live telemetry and safety evaluations
sim_state = simulation_manager.step()
```

### 6. Machine Health Calculation
```python
# Lines 73-77: Transparent composite health algorithm
health_temp = max(0.0, 100.0 - max(0.0, (temp - 88.0) * 3.5))
health_vib = max(0.0, 100.0 - max(0.0, (vib - 1.75) * 25.0))
health_oil = max(0.0, 100.0 - max(0.0, (43.0 - oil) * 3.0))
health_maint = max(0.0, 100.0 - (maint_days * 0.4))
machine_health = round(0.25 * health_temp + 0.25 * health_vib + 0.25 * health_oil + 0.25 * health_maint, 1)
```

### 7. Response Construction & UI Rendering
The backend returns a `DashboardResponse` dictionary. The browser receives the JSON, updates React state `data`, and paints the cards, progress bars, and alerts onto the screen.

---

## 23. Error Handling

CAT OperatorIQ is engineered to fail gracefully:

1. **Database Failure or Empty Database:**
   - If the database is missing or unseeded, backend services fallback to built-in nominal demo constants (`Marcus Vance`, `EXC001`, standard baselines).
2. **WebSocket Disconnection:**
   - In `frontend/src/context/SimulationContext.tsx`, if the WebSocket fails or disconnects (`ws.onerror` / `ws.onclose`), the frontend automatically falls back to HTTP polling every 2,000ms:
     ```typescript
     if (!pollInterval) {
       pollInterval = setInterval(fetchState, 2000);
     }
     ```
3. **ML Model Binary Missing:**
   - If `task_time_model.joblib` or `anomaly_model.joblib` are not found on disk, `PredictionService` and `AnomalyService` use hardcoded statistical heuristics so the application never crashes with a 500 error.
4. **Invalid API Inputs:**
   - FastAPI validates every request body with Pydantic. If an invalid type is sent, it returns HTTP 422 with a structured error explanation.
5. **Frontend State Boundary:**
   - If an API request throws a network error, `DashboardPage` catches it and renders `ErrorState.tsx` with a human-readable message and a "Retry Connection" button.

---

## 24. Environment Variables

All settings are managed in `backend/app/config.py` with defaults provided in `.env.example`:

| Variable | Purpose | Default / Example Value | Required? | Behavior If Missing |
| :--- | :--- | :--- | :--- | :--- |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./data/cat_operator_iq.db` | No | Defaults to local SQLite file in `./data`. |
| `OPENAI_API_KEY`| Optional external LLM key | `sk-...` | No | Assistant operates 100% offline via local deterministic RAG. |
| `WEATHER_API_KEY`| Optional external live weather key | `a8f9...` | No | Runs on realistic synthetic weather data. |
| `VITE_API_URL` | Frontend API destination URL | `http://localhost:8000` | No | Vite dev server proxies `/api` and `/ws` to `localhost:8000`. |
| `RANDOM_SEED` | Seed for synthetic data and ML | `42` | No | Defaults to `42` for guaranteed reproducibility. |
| `NUM_TELEMETRY`| Number of telemetry records to generate | `10000` | No | Defaults to 10,000 records. |
| `NUM_TASKS` | Number of tasks to generate | `2000` | No | Defaults to 2,000 records. |

---

## 25. Docker

### Architecture
`docker-compose.yml` configures three isolated container services connected by a private bridge network:

```
┌────────────────────────────────────────────────────────┐
│                   DOCKER COMPOSE NETWORK               │
│                                                        │
│  ┌────────────────┐   ┌────────────────┐   ┌─────────┐ │
│  │  cat_postgres  │◄──┤  cat_backend   │◄──┤cat_front│ │
│  │   Port 5432    │   │   Port 8000    │   │Port 5173│ │
│  └────────────────┘   └────────────────┘   └─────────┘ │
└────────────────────────────────────────────────────────┘
```

1. **`cat_postgres` (`postgres:16-alpine`):**
   - Automatically initializes the database schema on first boot using `./database/schema.sql`.
   - Healthcheck runs `pg_isready -U cat_user -d cat_operator_iq` every 5 seconds.
2. **`cat_backend` (`Dockerfile.backend`):**
   - Uses `python:3.12-slim`.
   - `depends_on: postgres` with `condition: service_healthy`.
   - During build, automatically executes data generation, model training, and database seeding.
3. **`cat_frontend` (`frontend/Dockerfile.frontend`):**
   - **Stage 1 (Build):** `node:20-alpine` runs `npm install` and `npm run build`.
   - **Stage 2 (Runtime):** Lightweight `nginx:alpine` serves compiled static HTML/JS and proxies `/api/` and `/ws/` to `http://backend:8000`.

---

## 26. Testing

The repository contains 15 automated unit and integration tests under `backend/tests/`:

### Test Suite Summary
```bash
PYTHONPATH=. pytest backend/tests
```

```
backend/tests/test_anomaly_detection.py ..                               [ 13%]
backend/tests/test_api_endpoints.py .....                                [ 46%]
backend/tests/test_assistant_service.py ...                              [ 66%]
backend/tests/test_safety_engine.py ....                                 [ 93%]
backend/tests/test_task_prediction.py .                                  [100%]

======================== 15 passed in 1.62s ========================
```

- **`test_anomaly_detection.py`:** Tests that normal telemetry is flagged as non-anomalous, while extreme vibration ($4.2\text{ mm/s}$) produces an anomaly score $\ge 50.0$.
- **`test_api_endpoints.py`:** Tests `/`, `/api/health`, `/api/safety/live`, `/api/simulation/inject`, and `/api/assistant/query` using FastAPI's `TestClient`.
- **`test_assistant_service.py`:** Verifies that intent routing responds accurately and always includes the mandatory advisory disclaimer.
- **`test_safety_engine.py`:** Tests nominal safety conditions ($0$ alerts), seatbelt violations ($+35\text{ pts}$), critical proximity ($+45\text{ pts}$), and multi-hazard compound scores.
- **`test_task_prediction.py`:** Verifies that task duration predictions return positive numbers with bounded confidence intervals.

---

## 27. Debugging

| Symptom | Probable Cause | Where to Look | How to Fix |
| :--- | :--- | :--- | :--- |
| **Frontend shows "Failed to connect to backend"** | FastAPI server is not running on port 8000. | Terminal running backend; browser network tab. | Start the backend: `uvicorn backend.app.main:app --port 8000`. Check that `http://localhost:8000/api/health` returns status healthy. |
| **Radar shows no workers or radar canvas is blank** | WebSocket connection failed and fallback poll hasn't fired yet. | Browser console (`WS connection error`); `SimulationContext.tsx`. | Verify port 8000 is open. The simulation context will automatically fall back to polling within 2 seconds. |
| **Database is empty / 0 tasks shown** | Database seeding script was not run. | `data/cat_operator_iq.db`; `scripts/seed_database.py`. | Run: `PYTHONPATH=. python scripts/seed_database.py`. |
| **ML prediction returns default 54 min without factors** | Model `.joblib` files have not been generated. | `models/task_time_model.joblib`. | Run: `PYTHONPATH=. python -m ml.train_models`. |
| **Changes to Python code do not show up** | Uvicorn was started without `--reload`. | Backend terminal. | Run Uvicorn with reload flag: `uvicorn backend.app.main:app --reload --port 8000`. |
| **Node build fails with TypeScript errors** | Types in `frontend/src/types/index.ts` out of sync with backend schemas. | Terminal running `npm run build`. | Run `npm run build` and inspect the flagged line number in `src/`. |

---

## 28. How to Modify the Project

### How to Add a New Safety Rule
1. Open `backend/app/services/safety_engine.py`.
2. Inside `SafetyEngine.evaluate()`, define your rule logic and point weight:
   ```python
   # RULE 9: Low Hydraulic Pressure under Heavy Load
   hydr = float(telemetry.get("hydraulic_pressure", 280.0))
   load = float(telemetry.get("load_weight", 0.0))
   if hydr < 220.0 and load > 15.0:
       mechanical_risk = 30.0
       triggered_rules.append("RULE_9_HYDRAULIC_PRESSURE_DROP")
       active_alerts.append({
           "rule_id": "RULE_9",
           "severity": "HIGH",
           "title": "Hydraulic Pressure Loss",
           "message": f"Hydraulic pressure dropped to {hydr:.0f} bar under {load:.1f}t load.",
           "timestamp": telemetry.get("timestamp")
       })
   ```
3. Add `mechanical_risk` to `raw_risk` calculation.
4. Add a unit test in `backend/tests/test_safety_engine.py`.

### How to Add a New API Endpoint
1. Open or create a router file in `backend/app/api/` (e.g., `backend/app/api/machines.py`).
2. Define your Pydantic schema in `backend/app/schemas/schemas.py`.
3. Add the route function:
   ```python
   @router.get("/my-endpoint")
   def get_my_data(db: Session = Depends(get_db)):
       return {"status": "ok"}
   ```
4. If creating a new router file, register it in `backend/app/main.py`:
   ```python
   app.include_router(my_router.router)
   ```

### How to Add a New Frontend Page
1. Create your page component in `frontend/src/pages/MyNewPage.tsx`.
2. Add your route to `frontend/src/App.tsx`:
   ```tsx
   <Route path="/my-page" element={<MyNewPage />} />
   ```
3. Add navigation link to `frontend/src/components/Sidebar.tsx` under the appropriate category.

---

## 29. File-by-File Map

| File Path | Primary Responsibility | Key Classes / Functions | Safe to Modify? |
| :--- | :--- | :--- | :--- |
| `backend/app/main.py` | App entrypoint, middleware, routers, WebSocket | `app`, `lifespan()`, `websocket_telemetry_endpoint()` | Moderate (routing changes) |
| `backend/app/config.py` | App configuration and paths | `Settings`, `settings` | Safe |
| `backend/app/db/database.py` | SQLAlchemy database session | `engine`, `SessionLocal`, `get_db()`, `init_db()` | Advanced |
| `backend/app/db/models.py` | Relational table definitions | `User`, `Operator`, `Machine`, `Task`, `Telemetry`, etc. | Moderate (requires re-seeding) |
| `backend/app/schemas/schemas.py`| API request/response validation | `TelemetryItem`, `TaskResponse`, `MachineResponse`, etc. | Safe |
| `backend/app/services/safety_engine.py` | 8-rule safety scoring | `SafetyEngine.evaluate()` | Safe |
| `backend/app/services/simulation_service.py`| Virtual machine & radar manager | `SimulationService`, `inject_hazard()`, `step()` | Safe |
| `backend/app/services/assistant_service.py` | RAG assistant and intents | `AssistantService.query()`, `_search_knowledge_base()`| Safe |
| `backend/app/services/prediction_service.py`| Task duration regression | `PredictionService.predict_task_time()` | Safe |
| `backend/app/services/anomaly_service.py` | Isolation Forest inference | `AnomalyService.analyze_telemetry()` | Safe |
| `ml/task_time_model.py` | ML regression pipeline | `TaskTimePredictor.fit()`, `predict_one()` | Safe |
| `ml/anomaly_detection.py`| Isolation Forest pipeline | `TelemetryAnomalyDetector.fit()`, `predict_telemetry()` | Safe |
| `frontend/src/App.tsx` | Root router & providers | `App` | Safe |
| `frontend/src/services/api.ts` | API client | `api.getDashboard()`, `api.injectHazard()`, etc. | Safe |
| `frontend/src/context/SimulationContext.tsx`| Telemetry state store | `SimulationProvider`, `useSimulation()` | Moderate |
| `frontend/src/context/RoleContext.tsx` | Role state store | `RoleProvider`, `useRole()` | Safe |
| `frontend/src/components/ProximityRadar.tsx`| 2D HTML5 canvas radar | `ProximityRadar` | Safe |
| `frontend/src/pages/DashboardPage.tsx` | Main operator screen | `DashboardPage` | Safe |

---

## 30. If You Only Remember 20 Things

1. **CAT OperatorIQ** is an operator assistance and fleet monitoring platform for heavy Caterpillar machinery.
2. It serves two personas: **In-Cab Operators** (real-time assistance) and **Fleet Supervisors** (oversight and audits).
3. The frontend is built with **React 18, TypeScript, Vite, and Tailwind CSS**.
4. The backend is built with **FastAPI and Python 3.12**.
5. Telemetry streams in real time over a **persistent WebSocket (`/ws/telemetry`)** every 2 seconds.
6. The frontend automatically falls back to **HTTP polling** if the WebSocket closes.
7. Machine center $(0,0)$ and surrounding ground personnel are drawn on a custom **2D HTML5 Proximity Radar**.
8. The **Safety Engine evaluates 8 deterministic rules** rather than a black-box AI model for safety compliance.
9. Safety scores range from $0$ to $100$ and map into four bands: `SAFE`, `WARNING`, `HIGH RISK`, and `CRITICAL`.
10. Task completion time is predicted using a **Gradient Boosting Regressor** with an **MAE of 4.13 minutes** ($R^2 = 0.9642$).
11. Every task prediction provides an **explainable factor attribution** (weather, operator skill, machine age, cycles).
12. Telemetry anomalies are detected using an **Isolation Forest** unsupervised model trained on 6 sensor dimensions.
13. Every anomaly score includes **human-readable diagnostic reasons** comparing sensors against baseline values.
14. The **AI Assistant uses deterministic intent routing and local RAG** over markdown engineering guides.
15. The AI Assistant runs **100% locally and offline** without requiring external cloud API keys.
16. Every AI recommendation includes the **official Caterpillar safety disclaimer**.
17. The database layer uses **SQLAlchemy 2.0**, supporting both zero-setup SQLite and production PostgreSQL.
18. The synthetic data generator uses **realistic mathematical distributions** (Exponential, Poisson, Gaussian).
19. Operators can take interactive 3-question quizzes in the **Training Hub** to certify on safety topics.
20. The entire system can be spun up locally in two commands or in Docker with `docker-compose up --build`.

---

## 31. Beginner Glossary

- **API (Application Programming Interface):** A defined set of HTTP URLs through which the frontend and backend talk.
- **REST (Representational State Transfer):** An architectural style using standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **HTTP GET:** Request used to fetch data without modifying the server.
- **HTTP POST:** Request used to create new data (e.g., logging an incident or submitting a quiz).
- **HTTP PUT:** Request used to update existing data (e.g., updating a task or incident status).
- **JSON (JavaScript Object Notation):** Lightweight text format for exchanging structured data between client and server.
- **WebSocket:** A persistent, two-way network connection allowing the server to push updates without the client asking.
- **React Component:** A self-contained, reusable piece of user interface code.
- **React State:** Variables maintained inside a component that cause the screen to re-render when changed.
- **React Props:** Input data passed from a parent component into a child component.
- **FastAPI:** A modern, high-speed Python web framework for building APIs.
- **SQLAlchemy:** A Python Object-Relational Mapper (ORM) that translates Python code into SQL queries.
- **SQLite:** A lightweight, serverless database stored as a single file on disk (`cat_operator_iq.db`).
- **PostgreSQL:** An enterprise-grade relational database engine used for multi-user deployments.
- **Machine Learning (ML):** Algorithms that learn patterns from historical data to make predictions.
- **Regression:** A type of ML that predicts a continuous numerical value (e.g., predicting duration in minutes).
- **Feature:** An input variable used by an ML model (e.g., `weather`, `machine_age`).
- **Target:** The variable the ML model is trying to predict (e.g., `actual_time_min`).
- **MAE (Mean Absolute Error):** The average difference between predicted values and actual values.
- **$R^2$ Score (Coefficient of Determination):** A metric from 0 to 1 indicating how much variance the model explains.
- **Anomaly:** A data point that significantly differs from normal, expected patterns.
- **Isolation Forest:** An unsupervised algorithm that isolates anomalies by randomly partitioning feature space.
- **RAG (Retrieval-Augmented Generation):** Enhancing assistant answers by retrieving relevant documents from a local knowledge base.
- **Telemetry:** Automated remote measurement and transmission of sensor data from heavy machinery.
- **ROPS (Rollover Protective Structure):** The reinforced cab frame of a machine designed to protect the operator during a rollover.
- **CORS (Cross-Origin Resource Sharing):** Security mechanism that controls which web domains are allowed to talk to an API.
- **Docker:** A platform that packages software into standardized containers containing all dependencies.

---

## 32. Interview Questions

### Architecture & System Design
**Q: Why did you choose WebSockets for telemetry instead of HTTP polling?**
- *Simple Answer:* Heavy equipment sensors change rapidly. An open WebSocket stream pushes updates every 2 seconds instantly without making thousands of separate HTTP requests.
- *Technical Answer:* HTTP polling creates connection teardown overhead, HTTP header bloat, and server strain. The persistent full-duplex WebSocket connection `/ws/telemetry` pushes JSON frames with minimal network overhead. Furthermore, we implemented an automatic polling fallback in `SimulationContext.tsx` in case the WebSocket drops.

**Q: Why is safety detection implemented with explicit rules instead of an ML classifier?**
- *Simple Answer:* In construction safety, you cannot guess. Rules are 100% predictable, explainable, and auditable.
- *Technical Answer:* Black-box deep learning models suffer from hallucinations and unpredictability at distribution boundaries. Life-critical safety standards (like ISO 13849 machinery safety) require deterministic guarantees. Our `SafetyEngine` evaluates 8 transparent rules and assigns additive risk points, ensuring every alert has a clear audit trail.

### Machine Learning
**Q: How did you evaluate the task duration prediction model?**
- *Simple Answer:* We tested both Random Forest and Gradient Boosting on a 20% holdout test set. Gradient Boosting won with an average error of only 4.13 minutes.
- *Technical Answer:* We trained on 1,588 synthetic task records and evaluated on 397 holdout records. We computed MAE ($4.13\text{ min}$), RMSE ($5.91\text{ min}$), and $R^2$ ($0.9642$). Gradient Boosting was selected because its boosting iterations modeled non-linear interactions between weather severity and operator skill more effectively than standard bagging.

**Q: How does the Isolation Forest model explain anomalies?**
- *Simple Answer:* It doesn't just say "this is an anomaly." It compares each sensor against machine baselines and lists the exact reasons.
- *Technical Answer:* After the Isolation Forest decision function flags an outlier ($p < 0.05$), `TelemetryAnomalyDetector` iterates across all 6 feature dimensions, computing the percentage deviation:
  $$\text{pct\_diff} = \frac{\text{val} - \mu}{\mu} \times 100$$
  If vibration is $\ge 1.5\sigma$ above baseline, it appends an explanation like `"Vibration is 32% above machine baseline (2.35 mm/s vs nominal 1.75 mm/s)"`.

### Database & Backend
**Q: How does your database support both local single-developer setup and production Docker?**
- *Simple Answer:* We used SQLAlchemy ORM. The exact same Python models run on SQLite locally or PostgreSQL in Docker.
- *Technical Answer:* In `backend/app/config.py`, `DATABASE_URL` defaults to `sqlite:///./data/cat_operator_iq.db`. When launched via `docker-compose.yml`, the environment variable overrides this to `postgresql://cat_user:cat_password@postgres:5432/cat_operator_iq`. Because all models use standard SQLAlchemy declarative syntax, zero code changes are required.

---

## 33. Five-Minute Explanation

> *"CAT OperatorIQ is an intelligent in-cab assistance and fleet monitoring platform built for Caterpillar heavy machinery like excavators, loaders, and dozers.*
>
> *Operating heavy construction equipment is dangerous and costly. Operators face large blind spots where ground workers can be struck, machines suffer costly mechanical breakdowns if early vibration or heat spikes go unnoticed, and site tasks regularly face unscheduled delays due to weather and soil conditions.*
>
> *To solve this, we built a modern full-stack platform. The frontend is a React and TypeScript application running in the machine cab. It features a custom 2D proximity radar that maps nearby ground workers in real time, live sensor gauges, predictive task ETAs, and an AI assistant.*
>
> *The backend is powered by FastAPI in Python 3.12. It streams telemetry every 2 seconds over WebSockets and connects to an auditable 8-rule Safety Engine. We intentionally avoided black-box AI for safety decisions—every safety alert is deterministic and explainable.*
>
> *For analytics, we built two machine learning pipelines in Scikit-Learn: a Gradient Boosting Regressor that predicts task completion time with an MAE of 4.1 minutes and 96% $R^2$ score, and an Isolation Forest model that detects multi-sensor mechanical anomalies.*
>
> *Finally, the system includes an in-cab AI assistant that works 100% locally and offline using document retrieval over engineering guides, ensuring operators get instant answers even when working in remote quarries without internet.*
>
> *The entire system runs out of the box with zero external dependencies using SQLite or can be deployed with Docker Compose on PostgreSQL."*

---

## 34. Thirty-Second Explanation

> *"CAT OperatorIQ is an intelligent digital co-pilot for Caterpillar heavy machinery. It combines real-time IoT telemetry streaming over WebSockets, a live 2D worker proximity radar, an auditable 8-rule safety scoring engine, and Scikit-Learn ML models that predict task completion times within 4 minutes. With an offline-capable AI assistant and interactive training quizzes, OperatorIQ keeps machine operators safer, reduces unscheduled machine downtime, and keeps site projects on schedule."*

---

## 35. Final Architecture

```mermaid
graph TB
    subgraph Browser["User Browser (In-Cab Display / Fleet Console)"]
        UIApp["React 18 Single Page Application"]
        UIState["SimulationContext (Live Telemetry & Radar State)"]
        Radar["2D Canvas Proximity Radar"]
        Alerts["Safety Alert Banner (Advisory Disclaimer)"]
        Chat["Assistant Chat Console"]
    end

    subgraph Server["FastAPI Application Server (Python 3.12 / Uvicorn)"]
        WSEndpoint["WebSocket Handler: /ws/telemetry"]
        RouterLayer["12 REST API Routers (/api/*)"]
        SimManager["SimulationService (State Loop & Radar Coordinates)"]
        Safety["SafetyEngine (8 Deterministic Rules)"]
        Anomaly["AnomalyService (Isolation Forest)"]
        Predictor["PredictionService (Gradient Boosting)"]
        Assistant["AssistantService (Intent Engine & Local RAG)"]
    end

    subgraph Models["ML Binaries & Preprocessors"]
        TModel["task_time_model.joblib"]
        AModel["anomaly_model.joblib"]
        PData["TaskDataPreprocessor (OneHot + Scaler)"]
    end

    subgraph Data["Persistence & Storage"]
        SQLA["SQLAlchemy 2.0 ORM"]
        DB[("SQLite: cat_operator_iq.db / PostgreSQL: 16")]
        Docs["Knowledge Base Markdown Files"]
    end

    %% Connections
    UIApp --> UIState
    UIState --> Radar
    UIState --> Alerts
    UIApp --> Chat

    UIState <== "WebSocket Stream (2s ticks)" ==> WSEndpoint
    UIApp <== "HTTP REST Calls" ==> RouterLayer

    WSEndpoint --> SimManager
    RouterLayer --> SimManager
    RouterLayer --> Safety
    RouterLayer --> Anomaly
    RouterLayer --> Predictor
    RouterLayer --> Assistant

    SimManager --> Safety
    SimManager --> Anomaly

    Predictor --> TModel
    Predictor --> PData
    Anomaly --> AModel
    Assistant --> Docs

    RouterLayer --> SQLA
    SQLA --> DB
```

### Final Architecture Line-by-Line Explanation:
1. **User Browser:** Runs the React 18 single-page application. The `SimulationContext` maintains the live telemetry state. The `2D Canvas Radar` renders workers in polar coordinates. The `SafetyAlertBanner` renders exception-first warnings. The `Assistant Chat Console` submits user queries.
2. **FastAPI Application Server:** Receives both persistent WebSocket connections and standard HTTP requests. The `SimulationService` advances virtual time, adds realistic sensor noise, and triggers automated incident logging.
3. **Safety & Machine Learning Engines:** `SafetyEngine` evaluates the 8 explicit safety rules on every tick. `PredictionService` calls the serialized `GradientBoostingRegressor` to calculate duration and factor breakdowns. `AnomalyService` calls `IsolationForest` to identify outliers. `AssistantService` scans local markdown files to answer natural language queries.
4. **Persistence Layer:** `SQLAlchemy` translates all database operations into ANSI SQL, persisting records into SQLite locally or PostgreSQL in production Docker containers.
