# CAT OperatorIQ 
> **"Your intelligent companion for safer and smarter machine operations."**

An industrial-grade operator assistance command center and fleet intelligence system engineered for Caterpillar heavy construction machinery. Built for the Caterpillar Software Engineer Hackathon.

---

> [!IMPORTANT]
> ### Safety Advisory Principle
> **CAT OperatorIQ is an operator ASSISTANCE system.**  
> AI and software predictions strictly **DO NOT** control machine movement, braking, steering, hydraulic functions, emergency systems, or safety-critical machine controls.  
> Safety alerts and predictions are purely advisory.
> 
> *"AI-generated recommendations are advisory and must not replace official operating procedures, safety procedures, operator training, or professional judgment."*

---

## Key Capabilities

1. **Real-Time 360° Proximity Hazard Radar**: Interactive polar-to-Cartesian sensor radar tracking surrounding personnel across Critical (<3.0m), Warning (3–6m), and Safe (>6m) perimeter zones.
2. **Transparent 8-Rule Safety Scoring Engine**: Deterministic multi-condition evaluation calculating an explainable 0–100 risk score across seatbelt, proximity, fatigue, idling, engine temperature, vibration, repeat events, and adverse weather conditions.
3. **Machine Learning Task Duration Prediction**: Regression model (`GradientBoostingRegressor`, $R^2 = 0.964$) delivering accurate completion ETAs, 90% confidence bands, and transparent factor attribution (weather penalties, skill bonuses, machine age wear).
4. **Unsupervised Telemetry Anomaly Detection**: `IsolationForest` pipeline that analyzes 6 mechanical features and generates human-readable explanations of deviations from baseline (e.g. *"Vibration is 32% above machine baseline"*).
5. **Interactive Operator Training Hub**: Personalized safety course recommendations, competency tracking, and interactive practical quizzes with automated grading.
6. **Live Telemetry Stream & Judge Simulation Panel**: Interactive controller for hackathon judges to inject live hazards (Worker in Proximity, Seatbelt Release, Vibration Spike, Overheat) and watch the safety engine and UI react immediately.
7. **Offline-Ready AI OperatorIQ Assistant**: Natural language query engine with deterministic intent classification and RAG retrieval over synthetic Caterpillar operating manuals—operating 100% offline without requiring paid API keys.
8. **Dual-Role Navigation**: Seamless switching between in-cab **Operator** views and fleet-wide **Supervisor / Fleet Manager** analytics and audit reporting.

---

## Architecture & Tech Stack

```
Frontend (React 18 + TypeScript + Vite + Tailwind CSS + Recharts)
   │
   ├─► WebSocket (/ws/telemetry) ──────► Live 2-second telemetry stream & radar blips
   │
   └─► REST API (FastAPI)
         ├─► Rule-Based Safety Engine (8 transparent rules, 0-100 score)
         ├─► ML Anomaly Detection (Isolation Forest + Baseline Explainability)
         ├─► ML Task Predictor (Gradient Boosting Regressor, MAE=4.13m, R²=0.964)
         ├─► Recommendation Engine (Safety, Maintenance, Training, Efficiency)
         ├─► AI Assistant (Offline RAG over Markdown Operating Guides)
         └─► Database Layer (SQLAlchemy ORM: SQLite default / PostgreSQL 16)
```

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS (Caterpillar dark charcoal & industrial yellow palette), Recharts, Lucide Icons, React Router 6.
- **Backend**: Python 3.12, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic v2, WebSockets.
- **Machine Learning**: Scikit-Learn (`IsolationForest`, `GradientBoostingRegressor`, `RandomForestRegressor`), Pandas, NumPy, Joblib.
- **Database**: Dual compatibility—zero-setup SQLite for instant local Mac demonstration; PostgreSQL 16 for containerized Docker deployment.

---

## Project Repository Tree

```
cat-operator-iq/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app, WebSocket /ws/telemetry, CORS, lifespan
│   │   ├── config.py                # App configuration, directory paths, safety disclaimer
│   │   ├── db/
│   │   │   ├── database.py          # SQLAlchemy engine, session maker, DB init
│   │   │   └── models.py            # 12 ORM models (Machine, Operator, Task, Telemetry, etc.)
│   │   ├── schemas/
│   │   │   └── schemas.py           # Pydantic v2 request/response validation schemas
│   │   ├── services/
│   │   │   ├── safety_engine.py     # 8-rule deterministic safety scoring engine (0-100 score)
│   │   │   ├── anomaly_service.py   # Isolation Forest inference + factor deviation explanation
│   │   │   ├── prediction_service.py# Task duration ML inference + confidence intervals + factors
│   │   │   ├── recommendation_service.py # Actionable safety & maintenance recommendations
│   │   │   ├── assistant_service.py # Deterministic intent parser + RAG search over knowledge base
│   │   │   └── simulation_service.py# Live telemetry stream generator & hazard injection
│   │   └── api/
│   │       ├── dashboard.py         # Real DB KPIs, active machine/task, role metrics
│   │       ├── tasks.py             # Task queue, detail, status updates, duration prediction
│   │       ├── machines.py          # Machine fleet, health breakdown, telemetry history
│   │       ├── operators.py         # Operator analytics and historical fleet baselines
│   │       ├── safety.py            # Live safety state, active alerts, event log
│   │       ├── incidents.py         # Incident CRUD, filters, severity statistics
│   │       ├── training.py          # Courses, interactive quizzes, progress tracking
│   │       ├── predictions.py       # ML model evaluation metrics, task inference
│   │       ├── assistant.py         # Conversational assistant endpoint
│   │       ├── simulation.py        # Trigger hazard scenarios, start/stop stream
│   │       ├── reports.py           # Generation of printable/exportable operational reports
│   │       └── anomalies.py         # Isolation Forest anomaly logs & explanations
│   ├── requirements.txt
│   └── tests/
│       ├── test_safety_engine.py    # Tests for all 8 safety rules and risk boundaries
│       ├── test_task_prediction.py  # Tests for ML duration prediction and factor breakdown
│       ├── test_anomaly_detection.py# Tests for Isolation Forest anomaly explainability
│       ├── test_assistant_service.py# Tests for AI intent matching and advisory disclaimer
│       └── test_api_endpoints.py    # FastAPI endpoint integration tests via TestClient
├── ml/
│   ├── data_preprocessing.py        # Cleaning, one-hot encoding, feature scaling
│   ├── feature_engineering.py       # Domain features (temperature ratio, stress index, idle ratio)
│   ├── task_time_model.py           # RandomForest vs GradientBoosting comparison & saving
│   ├── anomaly_detection.py         # Scikit-learn IsolationForest pipeline & explainability
│   ├── train_models.py              # CLI training runner: python -m ml.train_models
│   ├── evaluate_models.py           # MAE, RMSE, R2, anomaly contamination reports
│   └── model_registry.py           # Model artifact persistence and loader
├── models/                          # Serialized joblib artifacts & metrics.json
├── scripts/
│   ├── generate_data.py             # Deterministic seed 42 synthetic generator (10k telemetry, 2k tasks)
│   └── seed_database.py             # DB populator with realistic relational integrity
├── data/                            # Generated CSVs (machine.csv, telemetry.csv, tasks.csv, etc.)
├── knowledge_base/                  # Synthetic manuals for RAG assistant
│   ├── machine_guides/              # CAT 336 Excavator guides
│   ├── safety_guides/               # Proximity safety, ROPS seatbelt protocols
│   ├── training/                    # Anti-idling and fuel conservation techniques
│   └── maintenance/                 # Structural vibration diagnostics
├── database/
│   └── schema.sql                   # Complete DDL with foreign keys, checks, and indexes
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx           # Role switcher (Operator / Supervisor), demo banner, status
│   │   │   ├── Sidebar.tsx          # Industrial sidebar with route navigation
│   │   │   ├── KpiCard.tsx          # High-contrast metric cards with delta indicators
│   │   │   ├── ProximityRadar.tsx   # 2D interactive radar visualizer (Safe/Warning/Critical zones)
│   │   │   ├── TelemetryLiveFeed.tsx# Live gauges: RPM, Temp, Vibration, Oil Pressure, Idling
│   │   │   ├── SimulationControls.tsx # Interactive hazard injection & simulation controls
│   │   │   ├── SafetyAlertBanner.tsx# Alert banners with advisory warnings
│   │   │   ├── QuizModal.tsx        # Interactive knowledge checks with instant grading
│   │   │   ├── IncidentModal.tsx    # Modal to log or resolve incidents
│   │   │   └── StateViews.tsx       # Skeleton loaders, empty states, and error handling
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx    # "Good Morning, Operator", current machine, task ETA, KPIs
│   │   │   ├── TasksPage.tsx        # Task list, ML duration prediction breakdown, status changes
│   │   │   ├── SafetyPage.tsx       # Safety center, radar, scoring breakdown, active alerts
│   │   │   ├── MachineHealthPage.tsx# Fleet health table, transparent scoring formula breakdown
│   │   │   ├── BehaviorPage.tsx     # ML Anomaly detection dashboard, Isolation Forest explainers
│   │   │   ├── TrainingPage.tsx     # Training hub, personalized safety recommendations, quizzes
│   │   │   ├── IncidentsPage.tsx    # Incident management, severity charts, filtering & resolution
│   │   │   ├── AssistantPage.tsx    # CAT OperatorIQ conversational assistant with citations
│   │   │   └── ReportsPage.tsx      # Printable operational, safety, and health reports
│   │   ├── context/
│   │   │   ├── RoleContext.tsx      # Operator vs Supervisor view toggle
│   │   │   └── SimulationContext.tsx# Live telemetry stream and alert subscription
│   │   ├── services/
│   │   │   └── api.ts               # Axios / fetch client with typed REST & WebSocket handlers
│   │   ├── types/
│   │   │   └── index.ts             # TypeScript domain definitions
│   │   ├── index.css                # Industrial styling: dark charcoal, CAT yellow (#FFCD11)
│   │   └── App.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docs/
│   ├── architecture.md              # Architecture document with Mermaid diagrams
│   ├── presentation.md              # 5-minute hackathon pitch script
│   └── judges_questions.md          # 27 comprehensive technical Q&A
├── docker-compose.yml
├── Dockerfile.backend
├── frontend/Dockerfile.frontend
├── .env.example
└── README.md
```

---

## Machine Health Calcumation

Individual Data Machine Health
```bash
health_temp = max(0, 100 - max(0, (temp - 88) * 3.5))
health_vib  = max(0, 100 - max(0, (vib - 1.75) * 25))
health_oil  = max(0, 100 - max(0, (43 - oil) * 3))
health_maint = max(0, 100 - (maint_days * 0.4))
```

Cummulative Machine Health
```bash
Machine Health = 
25% Temperature Health
+ 25% Vibration Health
+ 25% Oil Pressure Health
+ 25% Maintenance Health
```

## Quickstart Guide (Local Execution)

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Node.js 18+ & npm (tested on Node v24)

### Step 1: Clone and Enter Repository
```bash
cd cat-operator-iq
```

### Step 2: Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Generate Synthetic Data, Train ML Models & Seed Database
```bash
# 1. Generate 10,000 telemetry records, 2,000 tasks, 500 safety events, 300 incidents (Seed 42)
PYTHONPATH=. python scripts/generate_data.py

# 2. Train Gradient Boosting Regressor & Isolation Forest anomaly detector
PYTHONPATH=. python -m ml.train_models

# 3. Seed SQLite / PostgreSQL database
PYTHONPATH=. python scripts/seed_database.py
```

### Step 4: Run Backend Test Suite
```bash
PYTHONPATH=. pytest backend/tests -v
```
*(All 15 tests should pass with 100% success).*

### Step 5: Start Backend Server
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- WebSocket Endpoint: `ws://localhost:8000/ws/telemetry`

### Step 6: Start Frontend Development Server (In a New Terminal)
```bash
cd frontend
npm install
npm run dev
```
- Open your browser to: **[http://localhost:5173](http://localhost:5173)**

---

## Running with Docker Compose

To launch the complete multi-container stack with PostgreSQL 16:
```bash
docker-compose up --build
```
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `localhost:5432`

---

## 9-Scene Hackathon Demonstration Script

For presentation to judges, execute this seamless 2-minute narrative:

1. **Scene 1 (Login & Cockpit)**: View the main **Dashboard**. See `"GOOD MORNING, MARCUS VANCE"`, active machine `EXC001` (CAT 336 Heavy Duty), current task Earth Excavation, and live CAN-bus telemetry gauges streaming at 1,850 RPM.
2. **Scene 2 (ML Task Prediction)**: Open **My Tasks**. Click Task `T001`. See the `GradientBoostingRegressor` model project an ETA of **54 minutes** (90% confidence range: 48–61 min) with explainable factor decomposition ($+7.5$ min due to Rain, $-6.5$ min due to Expert operator skill).
3. **Scene 3 (Live Hazard Incursion)**: On the **Judge Testing Panel**, click **"Worker in Proximity (2.1m)"**.  
   *Observation*: The 360° Proximity Radar instantly flashes red. Worker C is pinpointed at 2.1m. The Safety Engine jumps to **CRITICAL (88/100 RISK)**, and an advisory banner alerts the operator to pause hydraulic movement.
4. **Scene 4 (Automated Incident Creation)**: Switch to the **Incidents** tab.  
   *Observation*: Incident `INC001` has been automatically logged with GPS sector, severity `Critical`, and timestamp without requiring manual paperwork.
5. **Scene 5 (Explainable Anomaly Detection)**: Open **ML Behavior & Anomalies**.  
   *Observation*: The Isolation Forest card highlights specific mechanical deviations: *"Vibration is 32% above machine baseline (2.35 mm/s vs 1.75 mm/s)"* and *"Idle time is 41 minutes above normal"*.
6. **Scene 6 (Conversational AI Assistant)**: Open **AI OperatorIQ Assistant**. Click the chip query: *"Why is EXC001 showing a warning?"*  
   *Observation*: The assistant retrieves live telemetry evidence and RAG knowledge base guides, recommends next steps, and explicitly outputs the mandatory safety disclaimer.
7. **Scene 7 (Personalized Training)**: Open **Training Hub**. See the personalized safety recommendation: *"Proximity Safety Refresher"*. Click **Take Competency Quiz**, answer 3 practical questions, and receive an instant passing score and competency certification.
8. **Scene 8 (Incident Resolution)**: Return to **Incidents**, click **Mark Resolved** on the incursion, and confirm supervisor sign-off.
9. **Scene 9 (Supervisor Role Switch)**: In the top navigation bar, toggle the switch from **Operator** to **Supervisor / Fleet**.  
   *Observation*: The dashboard updates to show fleet-wide utilization across 50 machines, operator comparisons against fleet baselines, and generates an exportable, printable **Official Shift Audit Report**.

---

## Machine Learning Model Details

| Model Domain | Algorithm | Validation MAE / Metric | Features Evaluated | Artifact Saved |
| :--- | :--- | :--- | :--- | :--- |
| **Task Duration** | `GradientBoostingRegressor` | **MAE = 4.13 min**, $R^2 = 0.964$ | Weather, Skill, Machine Age, Load Cycles, Distance, Operator Baseline | `models/task_time_model.joblib` |
| **Telemetry Outliers** | `IsolationForest` | **Contamination: 5%** | Temp, Oil Pressure, Hydraulic Pressure, RPM, Vibration, Idle Time | `models/anomaly_model.joblib` |

---

## Transparent 8-Rule Safety Scoring

The Safety Risk Score evaluates between **0 and 100 points**:
- `0 - 30`: **LOW** (Safe / Normal Operation)
- `31 - 60`: **MEDIUM** (Advisory Caution)
- `61 - 80`: **HIGH** (Action Required)
- `81 - 100`: **CRITICAL** (Immediate Incursion Hazard)

$$\text{Risk Score} = \text{Seatbelt} (35) + \text{Proximity} (45) + \text{Fatigue} (30) + \text{Thermal} (35) + \text{Vibration} (30) + \text{Excess Idle} (20) + \text{Combo Hazards} (20)$$

---

## Future Scalability Roadmap

1. **Direct CAN-Bus Hardware Tap**: Integration with Caterpillar Product Link™ PLE641 telematics and J1939 CAN-bus protocols.
2. **On-Machine Edge Inference**: Exporting models to ONNX and TensorRT for deployment onto in-cab ruggedized Edge TPUs with sub-10ms latency.
3. **Computer Vision Fusion**: Replacing simulated worker distance tags with real-time stereo camera and LiDAR 3D bounding-box detection (YOLOv10 / ByteTrack).
4. **Digital Twin Integration**: Real-time 3D telemetry visualization connected with Caterpillar MineStar™ and Trimble earthmoving telematics.
