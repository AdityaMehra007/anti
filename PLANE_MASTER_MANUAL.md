# ✈️ PLANE COMMUNITY EDITION (CE) — MASTER OPERATIONAL MANUAL & AGENT DISPATCH CODEX

**Subsystem**: Plane Community Edition (CE) v1.4.2  
**Integration Status**: Fully Integrated & Verified  
**Port Ingress**: `http://localhost:8095`  
**Control Center**: [`START_PLANE.bat`](file:///e:/anti/START_PLANE.bat) & [`START_PLANE.ps1`](file:///e:/anti/START_PLANE.ps1)  
**API Connector**: [`omega/integrations/plane_connector.py`](file:///e:/anti/omega/integrations/plane_connector.py)  
**Agent Dispatcher**: [`omega/orchestration/plane_dispatcher.py`](file:///e:/anti/omega/orchestration/plane_dispatcher.py)  

---

## 1. Executive Overview

Plane is an extensible open-source project management platform supporting Issues, Cycles (Sprints), Modules, Views, and Pages. Within the OMEGA OS autonomous ecosystem, Plane functions as the central operational cockpit where human operators and autonomous agents collaborate, visualize project status, and track multi-agent development cycles.

```
                    ┌────────────────────────────────────────┐
                    │          OMEGA AUTONOMOUS AGENTS       │
                    │   (Self, Research, Coder, Reviewer)    │
                    └───────────────────┬────────────────────┘
                                        │
                         [TASK_REGISTRY.md / Live Sprints]
                                        │
                                        ▼
                    ┌────────────────────────────────────────┐
                    │      omega/orchestration/              │
                    │       plane_dispatcher.py              │
                    └───────────────────┬────────────────────┘
                                        │ (REST API & Token Auth)
                                        ▼
                    ┌────────────────────────────────────────┐
                    │       omega/integrations/              │
                    │       plane_connector.py               │
                    └───────────────────┬────────────────────┘
                                        │ HTTP :8095
                                        ▼
       ┌─────────────────────────────────────────────────────────────┐
       │             PLANE CE LOCAL CONTAINER STACK                  │
       │                                                             │
       │  ┌──────────────┐   ┌──────────────┐   ┌─────────────────┐  │
       │  │ plane-proxy  │──▶│  plane-web   │──▶│    plane-api    │  │
       │  │ (Nginx :8095)│   │  (Next.js)   │   │  (Django REST)  │  │
       │  └──────────────┘   └──────────────┘   └────────┬────────┘  │
       │                                                 │           │
       │         ┌───────────────┬───────────────────────┼────────┐  │
       │         ▼               ▼                       ▼        ▼  │
       │   ┌───────────┐   ┌───────────┐           ┌──────────┐ ┌───┐│
       │   │ plane-db  │   │plane-redis│           │ plane-mq │ │S3 ││
       │   │(Postgres) │   │ (Valkey)  │           │(RabbitMQ)│ │Min││
       │   └───────────┘   └───────────┘           └──────────┘ └───┘│
       └─────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Layout & Architecture

```
e:\anti\
├── external/
│   └── plane/
│       ├── docker-compose.yaml       # Official v1.4.2 microservice orchestrator
│       ├── plane.env.example         # Version-controlled configuration template
│       ├── plane.env                 # Active local secrets & port 8095 bindings
│       └── data/                     # Persistent storage (Postgres, MinIO, Redis)
├── omega/
│   ├── integrations/
│   │   ├── __init__.py
│   │   └── plane_connector.py        # Zero-dependency Python REST client
│   └── orchestration/
│       ├── __init__.py
│       └── plane_dispatcher.py       # Autonomous agent <-> Plane task sync engine
├── tests/
│   └── test_plane_integration.py     # Mock HTTP test suite (100% pass)
├── START_PLANE.bat                   # Interactive Windows CLI launcher
├── START_PLANE.ps1                   # Core PowerShell management automation
└── PLANE_MASTER_MANUAL.md            # This manual
```

---

## 3. Quick Start & Operational Control

### Interactive Terminal Menu
Double-click or run from PowerShell:
```cmd
START_PLANE.bat
```
Options available:
- `[1] START LOCAL PLANE CE STACK`: Starts all containers in detached mode and polls port 8095.
- `[2] STOP LOCAL PLANE CE STACK`: Cleanly shuts down the container stack.
- `[3] CHECK STACK & CONTAINER HEALTH`: Reports container status and sends an API probe to `/api/instances/`.
- `[4] VIEW CONTAINER LOGS`: Live tail of API, Web, and Worker container outputs.
- `[5] OPEN PLANE WEB INTERFACE`: Opens `http://localhost:8095` in default browser.
- `[6] RUN OMEGA AGENT TASK DISPATCH DRY-RUN`: Simulates syncing `TASK_REGISTRY.md` to Plane.
- `[7] EXECUTE LIVE AGENT TASK SYNCHRONIZATION`: Dispatches tasks live to the running instance.

### Headless & Scriptable PowerShell Commands
```powershell
# Start Plane containers
powershell -ExecutionPolicy Bypass -File START_PLANE.ps1 -Action up

# Check status and health probe
powershell -ExecutionPolicy Bypass -File START_PLANE.ps1 -Action status

# Stop Plane containers
powershell -ExecutionPolicy Bypass -File START_PLANE.ps1 -Action down

# Stream live container logs
powershell -ExecutionPolicy Bypass -File START_PLANE.ps1 -Action logs
```

---

## 4. API Client & Connector Usage (`plane_connector.py`)

The connector requires **zero external dependencies** and uses Python's standard library.

### Basic Python Usage
```python
from omega.integrations.plane_connector import PlaneClient

# Initialize client (uses PLANE_API_KEY environment variable if present)
client = PlaneClient(base_url="http://localhost:8095", api_key="your-api-key")

# Health probe
health = client.health_check()
print(health)

# Workspaces & Projects
workspaces = client.list_workspaces()
projects = client.list_projects("omega")

# Issue Management
issue = client.create_issue(
    workspace_slug="omega",
    project_id="omega-core",
    title="Implement Multi-Trillion Sovereign Vault",
    description="<p>Full implementation specifications</p>",
    priority="urgent"
)
```

### Command Line Interface
```bash
# Probing instance health
python omega/integrations/plane_connector.py --status

# Dry-run health simulation (safe offline)
python omega/integrations/plane_connector.py --dry-run --status

# Listing workspaces
python omega/integrations/plane_connector.py --list-workspaces

# Creating an issue via CLI
python omega/integrations/plane_connector.py --workspace omega --project omega-core --create-issue "Deploy Fleet" --priority high
```

---

## 5. Autonomous Agent Dispatch Engine (`plane_dispatcher.py`)

The dispatcher reads markdown task checklists and task tables from [`TASK_REGISTRY.md`](file:///e:/anti/TASK_REGISTRY.md) and creates or updates issues in Plane:

```bash
# Run simulation (verifies parsing and shows staged issues without modifying state)
python omega/orchestration/plane_dispatcher.py --dry-run

# Run live synchronization to Plane project
python omega/orchestration/plane_dispatcher.py --sync --workspace omega --project proj-omega-core
```

### State Mapping Table

| OMEGA Task State | Plane State Group | Description |
| :--- | :--- | :--- |
| `[DISCOVERED]`, `[PLANNED]` | `Backlog` | Identified opportunities and roadmap items |
| `[READY]`, `Todo` | `Unstarted` | Specifications approved, ready for agent execution |
| `[RUNNING]`, `[OPERATIONAL]`, `[REVIEW]` | `Started` | Agent currently implementing or reviewing |
| `[COMPLETE]`, `[VERIFIED]` | `Completed` | Code committed and all tests verified green |
| `[BLOCKED]`, `[FAILED]` | `Cancelled` | Blocked on missing dependency or escalated |

---

## 6. Service Port & Ingress Reference

| Service | Container Name | Internal Port | Host Port | Ingress URL / Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Ingress Proxy** | `plane-proxy` | 80 / 443 | **8095** / 8443 | `http://localhost:8095` |
| **Frontend UI** | `plane-web` | 3000 | Cluster internal | Next.js Web App |
| **Backend REST** | `plane-api` | 8000 | Cluster internal | Django Core API |
| **Live Sync** | `plane-live` | 3000 | Cluster internal | WebSocket Collaboration |
| **PostgreSQL** | `plane-db` | 5432 | Cluster internal | Relational Models |
| **Cache & PubSub**| `plane-redis`| 6379 | Cluster internal | Valkey / Redis 7 |
| **Job Queue** | `plane-mq` | 5672 | Cluster internal | RabbitMQ AMQP |
| **Object Store** | `plane-minio` | 9000 / 9090 | Cluster internal | MinIO S3 Attachments |

---

## 7. Verification & Regression Testing

Run the automated test suite anytime to verify connector integrity:
```bash
python -m unittest tests/test_plane_integration.py
```
Expected output:
```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.709s

OK
```
