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
| **Webhook Reactor** | Python Daemon | — | **8096** | `http://localhost:8096/webhook` |
| **Frontend UI** | `plane-web` | 3000 | Cluster internal | Next.js Web App |
| **Backend REST** | `plane-api` | 8000 | Cluster internal | Django Core API |
| **Live Sync** | `plane-live` | 3000 | Cluster internal | WebSocket Collaboration |
| **PostgreSQL** | `plane-db` | 5432 | Cluster internal | Relational Models |
| **Cache & PubSub**| `plane-redis`| 6379 | Cluster internal | Valkey / Redis 7 |
| **Job Queue** | `plane-mq` | 5672 | Cluster internal | RabbitMQ AMQP |
| **Object Store** | `plane-minio` | 9000 / 9090 | Cluster internal | MinIO S3 Attachments |

---

## 7. Departmental Project & Sprint Engine (`plane_boards.py`)

Provisions standard organizational departments and automated 14-day Sprint Cycles:

```bash
# Provision all departments and 14-day sprint cycles (dry-run simulation)
python omega/orchestration/plane_boards.py --dry-run --provision-all

# Execute live provisioning to running Plane workspace
python omega/orchestration/plane_boards.py --provision-all --workspace omega
```

### Standard Departmental Topologies:
- **`CORE`**: OMEGA Core Infrastructure (Master codex, runtimes, CI/CD).
- **`CAP`**: Capital Allocator & Sovereign Treasury (DCM, liquidity corridors, cash pooling).
- **`FLEET`**: Autonomous Agent Fleet Operations (Swarm orchestration, verification ledgers).
- **`INTEL`**: Market Intelligence & Global Radar (Opportunity radars, outreach databases).

---

## 8. Bidirectional Webhook Event Reactor (`plane_webhook_server.py`)

Listens on port `8096` for real-time Plane events and triggers automated agent actions:

```bash
# Start webhook listener
python omega/orchestration/plane_webhook_server.py --port 8096

# Dispatch test event to verify round-trip processing
python omega/orchestration/plane_webhook_server.py --test-event --port 8096
```

Events are persisted to `omega/data/plane_webhook_events.jsonl` and can be inspected in real time.

---

## 9. Verification & Regression Testing

Run the complete test suite (base integration, advanced modules, and extension suite):
```bash
pytest tests/test_plane_integration.py tests/test_plane_advanced.py tests/test_plane_extensions.py -v
```
Expected output:
```text
============================= 18 passed in 1.70s ==============================
```

---

## 10. Git-to-Plane Synchronizer & Release Notes (`plane_git_bridge.py`)

Correlates repository git commits with Plane CE projects, attaches audit trail comments to issues, and compiles structured release changelogs:

```bash
# Print structured release changelog grouped by department (CORE, CAP, FLEET, INTEL)
python omega/orchestration/plane_git_bridge.py --count 10 --changelog

# Stage or sync commit audit comments into Plane issues
python omega/orchestration/plane_git_bridge.py --count 10 --dry-run
```

---

## 11. Workspace Backup, Export & Restoration Engine (`plane_backup.py`)

Exports complete workspace architectures (projects, cycles, states, issues) to JSON archives and enables instantaneous disaster recovery:

```bash
# Export full workspace backup & generate markdown dossier
python omega/orchestration/plane_backup.py --dry-run --workspace omega

# Restore workspace from an existing backup archive
python omega/orchestration/plane_backup.py --restore omega/data/backups/plane_backup_omega_<timestamp>.json --dry-run
```

---

## 12. Autonomous Agent Reactor & Verification Logger (`plane_agent_reactor.py`)

Event-driven task loop that listens to incoming webhooks and triggers autonomous execution:
- **`issue.created`**: Analyzes task scope, tags priority (`urgent`, `high`, `medium`), and attaches the OMEGA verification rubric.
- **`issue.updated`**: Detects completion transitions (`done`, `completed`), runs automated verification suites, and seals the pass/fail cryptographic evidence onto the ticket.

```bash
# Simulate issue creation event reaction
python omega/orchestration/plane_agent_reactor.py --test-event created --dry-run

# Simulate issue completion verification reaction
python omega/orchestration/plane_agent_reactor.py --test-event completed --dry-run
```

---

## 13. Interactive Browser Cockpit (`PLANE_CONTROL_CENTER.html`)

Access `PLANE_CONTROL_CENTER.html` in any browser or launch directly from `START_PLANE.bat` (`[D]`):
- Real-time HTTP health probes on ports 8095 (Ingress) and 8096 (Webhook Reactor).
- 1-click test webhook dispatches and event simulation buttons.
- Live streaming log terminal monitoring stack status and incoming payloads.
