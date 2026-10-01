# Specification: Plane CE Subsystem & Autonomous Agent Dispatch Hub

**Date**: 2026-10-01  
**Status**: Approved (Architectural Design)  
**Author**: Antigravity  
**Target Locations**:  
- Subsystem & Containers: `external/plane/`  
- Host Launchers: `START_PLANE.bat`, `START_PLANE.ps1`  
- SDK & Connector: `omega/integrations/plane_connector.py`  
- Agent Dispatch Hub: `omega/orchestration/plane_dispatcher.py`  
- Operational Codex: `PLANE_MASTER_MANUAL.md`  
- Test Suite: `tests/test_plane_integration.py`  

---

## 1. Executive Summary & Vision

The objective is to integrate **Plane Community Edition (CE)**—the open-source, modern project management and sprint tracking system—into the OMEGA OS environment (`e:\anti`), establishing:
1. A sovereign, local containerized instance of Plane CE v1.4.2 running with Docker Compose.
2. Robust, automated Windows lifecycle scripts (`START_PLANE.bat`, `START_PLANE.ps1`) featuring automated Docker daemon discovery, health probe polling, and port management.
3. A zero-external-dependency Python SDK and integration connector (`omega/integrations/plane_connector.py`) supporting Workspaces, Projects, Issues, Cycles, Modules, and States with both dry-run simulation and live REST operations.
4. An autonomous agent dispatch hub (`omega/orchestration/plane_dispatcher.py`) bridging OMEGA agent tasks (from `TASK_REGISTRY.md` and executive operational directives) directly into Plane Kanban boards and Cycles.
5. Comprehensive operational documentation (`PLANE_MASTER_MANUAL.md`) detailing setup, API references, backup/restore routines, and agent workflows.

---

## 2. Global Constraints & Principles

1. **Zero External Dependencies for SDK**: All Python connectors and dispatch tools must use standard library primitives (`urllib.request`, `json`, `os`, `sys`, `time`, `pathlib`, `typing`, `argparse`, `unittest`).
2. **Port Conflict Elimination**: Default Plane installations bind to ports 80/443. The OMEGA integration will configure default HTTP ingress to `8090` (and configurable in `plane.env`) to prevent collision with local Windows services or development servers.
3. **Resilient Volume Persistence**: All data (PostgreSQL database, MinIO S3 assets, Redis state) resides under `external/plane/data/` to ensure zero state loss across restarts.
4. **Idempotence & Safety**: The connector and dispatcher must support `--dry-run` and handle offline or uninitialized instances gracefully with actionable error reporting.

---

## 3. Architecture & Directory Layout

```
e:\anti\
├── external/
│   └── plane/
│       ├── docker-compose.yaml       # Official Plane CE microservices stack
│       ├── plane.env                 # Configured environment variables (ports, secrets, DB)
│       └── data/                     # Persistent volumes
│           ├── pgdata/
│           ├── redis/
│           └── uploads/
├── omega/
│   ├── integrations/
│   │   ├── __init__.py
│   │   └── plane_connector.py        # Plane REST API client & sync tool
│   └── orchestration/
│       ├── __init__.py
│       └── plane_dispatcher.py       # Autonomous agent <-> Plane task & sprint bridge
├── tests/
│   └── test_plane_integration.py     # Unit and integration test suite
├── START_PLANE.bat                   # Interactive Windows CLI launcher
├── START_PLANE.ps1                   # Core PowerShell management script
└── PLANE_MASTER_MANUAL.md            # Comprehensive operational & API codex
```

---

## 4. Subsystem Components & Responsibilities

### 4.1. Containerized Services (`external/plane/docker-compose.yaml`)
- **`plane-proxy`**: Nginx ingress gateway routing incoming HTTP traffic on port `8090` to frontend and backend services.
- **`plane-web`**: Next.js client delivering the responsive Kanban, List, Calendar, and Cycle interfaces.
- **`plane-api`**: Django REST backend handling data modeling, authentication, business logic, and API endpoints.
- **`plane-live`**: WebSocket service powering real-time multi-agent and multi-user synchronization.
- **`plane-space` & `plane-admin`**: Public project documentation spaces and instance administration portal.
- **`plane-db`**: PostgreSQL 15 database storing relational models.
- **`plane-redis`**: Redis 7 cache and pub/sub broker.
- **`plane-mq`**: RabbitMQ message broker for asynchronous Celery job queues.
- **`plane-minio`**: S3-compatible object storage for file attachments and agent run artifacts.
- **`plane-worker` & `plane-beat-worker`**: Celery asynchronous background job workers and periodic scheduler.

### 4.2. Host Launchers (`START_PLANE.bat` and `START_PLANE.ps1`)
- Checks Docker daemon connectivity via `docker ps`.
- If Docker daemon is stopped, attempts to launch `C:\Program Files\Docker\Docker\Docker Desktop.exe` and waits for readiness with a countdown spinner.
- Validates the presence of `external/plane/plane.env`; initializes from defaults if absent.
- Commands supported: `up` (start stack detached), `down` (stop stack safely), `restart`, `status` (container health), `logs`, `browser` (open web dashboard).

### 4.3. API Connector (`omega/integrations/plane_connector.py`)
- **Class `PlaneClient`**:
  - `health_check() -> Dict[str, Any]`
  - `list_workspaces() -> List[Dict[str, Any]]`
  - `create_workspace(name: str, slug: str) -> Dict[str, Any]`
  - `list_projects(workspace_slug: str) -> List[Dict[str, Any]]`
  - `create_project(workspace_slug: str, name: str, identifier: str) -> Dict[str, Any]`
  - `list_states(workspace_slug: str, project_id: str) -> List[Dict[str, Any]]`
  - `create_issue(workspace_slug: str, project_id: str, title: str, description: str, state_id: Optional[str] = None, priority: str = "medium") -> Dict[str, Any]`
  - `list_issues(workspace_slug: str, project_id: str) -> List[Dict[str, Any]]`
  - `update_issue(workspace_slug: str, project_id: str, issue_id: str, **kwargs) -> Dict[str, Any]`
  - `list_cycles(workspace_slug: str, project_id: str) -> List[Dict[str, Any]]`
  - `create_cycle(workspace_slug: str, project_id: str, name: str, start_date: str, end_date: str) -> Dict[str, Any]`
- CLI flags: `--status`, `--dry-run`, `--sync-registry`, `--workspace`, `--project`.

### 4.4. Agent Dispatch Bridge (`omega/orchestration/plane_dispatcher.py`)
- Reads tasks from `TASK_REGISTRY.md` or dynamically constructed agent payloads.
- Syncs them into Plane project boards (e.g. project slug `OMEGA`).
- Automatically transitions issue states based on agent execution lifecycle:
  - `Backlog` -> `Todo` -> `In Progress` -> `Done`.
- Comments on issues with test output, commit hashes, and verification artifacts.

---

## 5. Verification & Test Plan

1. **Offline & Unit Testing (`tests/test_plane_integration.py`)**:
   - Mock HTTP server tests for `PlaneClient` verifying headers, payload encoding, error code handling (401 Unauthorized, 404 Not Found, 500 Internal Error).
   - Validation of `plane_dispatcher.py` parsing `TASK_REGISTRY.md` and generating correctly formatted Plane API payloads.
   - Dry-run validation of `plane_connector.py` confirming zero network mutations when `--dry-run` is active.
2. **Launcher Script Syntax & Integrity**:
   - PowerShell syntax verification of `START_PLANE.ps1`.
   - Batch script syntax verification of `START_PLANE.bat`.
3. **Environment & Compose Validation**:
   - `docker-compose.yaml` and `plane.env` structure verification.
