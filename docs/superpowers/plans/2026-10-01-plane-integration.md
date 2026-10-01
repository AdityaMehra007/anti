# Plane CE Subsystem & Autonomous Agent Dispatch Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy Plane Community Edition (CE) v1.4.2 into OMEGA OS with local Docker compose orchestration, robust Windows host launchers, zero-dependency REST API connector, autonomous agent task dispatch bridge, and complete operational manual.

**Architecture:** Pinned Plane CE microservice stack under `external/plane/` with persistent volumes and port collision avoidance (port 8090); PowerShell/Batch host launchers with Docker daemon discovery and health monitoring; standard library Python connector and dispatcher (`omega/integrations/plane_connector.py` and `omega/orchestration/plane_dispatcher.py`) validated via unit tests.

**Tech Stack:** Docker Compose, Nginx, Python 3.10+ (`urllib`, `json`, `unittest`), PowerShell, Windows Batch, Markdown.

**Spec:** `docs/superpowers/specs/2026-10-01-plane-integration-design.md`

## Global Constraints

- **Zero External Dependencies for Python**: Standard library only (`urllib.request`, `json`, `os`, `sys`, `time`, `pathlib`, `typing`, `argparse`, `unittest`, `http.server`).
- **Default Port**: Ingress HTTP on `8090` (configured in `plane.env`) to avoid collision with IIS/system ports 80/443.
- **Volume Safety**: Database, Redis, and MinIO assets persist in `external/plane/data/`.
- **Idempotence**: Connector and Dispatcher support `--dry-run` and safe execution against live or offline targets.

---

### Task 1: Plane CE Docker Stack & Configuration Scaffolding

**Files:**
- Create: `external/plane/docker-compose.yaml`
- Create: `external/plane/plane.env.example`
- Create: `external/plane/plane.env`

**Interfaces:**
- Produces: `external/plane/` Docker stack ready to spin up with `docker compose -f docker-compose.yaml up -d`.

- [x] **Step 1: Download official Plane CE v1.4.2 compose file and environment template**

Fetch the official `docker-compose.yml` and `variables.env` from makeplane/plane release v1.4.2 into `external/plane/`.

- [x] **Step 2: Configure non-colliding ports and directories in `external/plane/plane.env`**

Set:
`LISTEN_HTTP_PORT=8090`
`WEB_URL=http://localhost:8090`
`CORS_ALLOWED_ORIGINS=http://localhost:8090`
`APP_DOMAIN=localhost:8090`
Generate secure random secret keys for `SECRET_KEY`, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `RABBITMQ_PASSWORD`, and `AWS_SECRET_ACCESS_KEY`.

- [x] **Step 3: Verify compose file syntax and volume mappings**

Run: `docker compose -f external/plane/docker-compose.yaml --env-file external/plane/plane.env config --quiet` (or validate YAML syntax if Docker daemon is stopped).

- [x] **Step 4: Commit**

```bash
git add external/plane/
git commit -m "feat(plane): scaffold Plane CE v1.4.2 Docker Compose and environment config"
```

---

### Task 2: Windows Host Launchers (`START_PLANE.bat` and `START_PLANE.ps1`)

**Files:**
- Create: `START_PLANE.bat`
- Create: `START_PLANE.ps1`

**Interfaces:**
- Produces: Interactive CLI menu and PowerShell automation script for starting, stopping, checking status, inspecting logs, and launching the Plane web interface.

- [x] **Step 1: Implement `START_PLANE.ps1` with Docker daemon detection and health probing**

Supports `-Action up|down|restart|status|logs|browser`. If Docker daemon is stopped, attempts to launch `Docker Desktop.exe` and waits up to 60 seconds with progress status. Once containers are up, polls `http://localhost:8090` until HTTP 200/302 is received, then opens browser.

- [x] **Step 2: Implement interactive Windows CLI launcher `START_PLANE.bat`**

Displays an ASCII banner, options `[1] Start Stack`, `[2] Stop Stack`, `[3] View Status & Health`, `[4] View Logs`, `[5] Open Browser`, `[6] Run Agent Sync`, `[0] Exit`.

- [x] **Step 3: Test launcher argument parsing**

Run: `powershell -NoProfile -ExecutionPolicy Bypass -File START_PLANE.ps1 -Action status`
Expected: Clear output indicating Docker state or container status without unhandled exceptions.

- [x] **Step 4: Commit**

```bash
git add START_PLANE.bat START_PLANE.ps1
git commit -m "feat(plane): add Windows host launchers with Docker daemon discovery"
```

---

### Task 3: Unit Test Suite for Plane REST API Connector

**Files:**
- Create: `tests/test_plane_integration.py`

**Interfaces:**
- Consumes: `omega.integrations.plane_connector.PlaneClient`
- Produces: Validated test suite covering all client methods and error handling.

- [x] **Step 1: Write the failing test with mock HTTP server**

Test `health_check`, `list_workspaces`, `create_project`, `create_issue`, `list_issues`, `update_issue`, `create_cycle`, and `--dry-run` behavior against a local mock HTTP server.

- [x] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests/test_plane_integration.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'omega.integrations.plane_connector'`

- [x] **Step 3: Commit test suite**

```bash
git add tests/test_plane_integration.py
git commit -m "test(plane): add unit tests with mock server for Plane REST connector"
```

---

### Task 4: Zero-Dependency Plane REST API Connector (`omega/integrations/plane_connector.py`)

**Files:**
- Create: `omega/integrations/plane_connector.py`
- Create: `omega/integrations/__init__.py` (if not present)

**Interfaces:**
- Consumes: Standard library `urllib.request`, `json`, `argparse`.
- Produces: `PlaneClient` class with methods for full CRUD on Plane workspaces, projects, issues, cycles, and states.

- [x] **Step 1: Implement `PlaneClient` class**

Implements standard REST client handling Bearer API token / `x-api-key` auth, CSRF headers, session cookies, json serialization, and custom exception `PlaneAPIError`. Includes `--dry-run` logging mode.

- [x] **Step 2: Implement CLI entrypoint in `plane_connector.py`**

Supports `--status`, `--dry-run`, `--list-projects`, `--create-issue`, `--sync-registry`.

- [x] **Step 3: Run unit tests to verify they pass**

Run: `python -m unittest tests/test_plane_integration.py`
Expected: PASS all tests.

- [x] **Step 4: Commit**

```bash
git add omega/integrations/plane_connector.py
git commit -m "feat(plane): implement zero-dependency Plane REST API client and CLI"
```

---

### Task 5: Autonomous Agent Dispatch Hub (`omega/orchestration/plane_dispatcher.py`)

**Files:**
- Create: `omega/orchestration/plane_dispatcher.py`
- Create: `omega/orchestration/__init__.py` (if not present)

**Interfaces:**
- Consumes: `omega.integrations.plane_connector.PlaneClient`, `TASK_REGISTRY.md`.
- Produces: Agent-to-Plane ticket sync, sprint tracking, and artifact commenting.

- [x] **Step 1: Write unit test in `tests/test_plane_integration.py` for dispatcher parsing and sync**

Verify that markdown task entries from `TASK_REGISTRY.md` are transformed into valid Plane issue payloads with correct state mappings and priority tags.

- [x] **Step 2: Implement `PlaneDispatcher` in `omega/orchestration/plane_dispatcher.py`**

Implements task registry reader, sync loop, auto-issue creation, state transitions (`Backlog` -> `In Progress` -> `Done`), and evidence attachment generation.

- [x] **Step 3: Run tests to verify all pass**

Run: `python -m unittest tests/test_plane_integration.py`
Expected: PASS.

- [x] **Step 4: Test dispatcher CLI in dry-run mode**

Run: `python omega/orchestration/plane_dispatcher.py --dry-run`
Expected: Clean output showing parsed tasks and staged Plane issue sync actions.

- [x] **Step 5: Commit**

```bash
git add omega/orchestration/plane_dispatcher.py tests/test_plane_integration.py
git commit -m "feat(plane): implement autonomous agent dispatch hub and task sync bridge"
```

---

### Task 6: Operational Codex & Final End-to-End Verification

**Files:**
- Create: `PLANE_MASTER_MANUAL.md`

**Interfaces:**
- Produces: Complete operational guide covering architectural diagrams, environment reference, Docker lifecycle commands, API schemas, agent dispatch workflows, and troubleshooting.

- [x] **Step 1: Author `PLANE_MASTER_MANUAL.md`**

Comprehensive manual covering:
1. Quick Start (`START_PLANE.bat`)
2. Port Architecture (`8090`) & Services
3. API Authentication & Token Configuration
4. Agent Dispatch Workflows
5. Backup & Database Recovery
6. Troubleshooting & Health Probes

- [x] **Step 2: Run full regression and validation test suite**

Run: `python -m unittest discover tests -p "test_*.py"`
Run: `python omega/integrations/plane_connector.py --dry-run --status`
Run: `python omega/orchestration/plane_dispatcher.py --dry-run`

- [x] **Step 3: Commit**

```bash
git add PLANE_MASTER_MANUAL.md
git commit -m "docs(plane): add comprehensive Plane CE master operational manual"
```
