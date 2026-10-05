# WORKFLOW SPECIFICATION: Autonomous SaaS Venture Builder & Agent Factory
**File**: `workflows/saas_venture_builder_loop.md`  
**Domain**: Software Factory & Autonomous Entrepreneurship  
**Status**: APPROVED & ACTIVE  
**Implementation Seam**: `e:/anti/aios/projects/saas_factory.py` & `e:/anti/aios/projects/agent_harness.py`

---

## 1. Loop Profile & Overview
- **Objective**: Transform a high-level product concept into a fully scaffolded, tested, and container-ready SaaS project with pluggable capabilities (Auth, DB, Stripe, Analytics), generate dedicated tool-calling autonomous agents, register the project in `master.db` -> `saas_projects`, and output ready-to-run code.
- **Cadence**: On-demand / Event-triggered via Command UI or API endpoint.

---

## 2. Trigger
- **Primary Mechanism**: Event-driven (POST `/v1/saas/scaffold` or UI form submission).
- **Payload**:
  - `name`: String (kebab-case project slug).
  - `stack`: One of `['nextjs-fastapi', 'nextjs-flask', 'static-api', 'python-cli']`.
  - `features`: Array of selected capabilities (`['auth', 'db', 'stripe', 'analytics']`).

---

## 3. Execution Pipeline
1. **Scaffold Directory Topology**:
   - Create root folder at `projects/scaffolded/{name}/`.
   - Generate standard files (`README.md`, `.gitignore`, `.env.example`, `Makefile`, `docker-compose.yml`).
2. **Stack Specialization**:
   - For `nextjs-fastapi`: Scaffold TypeScript pages router frontend, FastAPI `main.py`, requirements, and docker service definitions.
   - For `nextjs-flask`: Scaffold Flask API with development environment bindings.
   - For `static-api`: Scaffold vanilla HTML/JS frontend and Python micro-API.
   - For `python-cli`: Scaffold `setup.py`, `src/`, and unit tests.
3. **Pluggable Feature Injection**:
   - `auth`: Generate JWT authentication middleware stub.
   - `db`: Generate SQLite schema and automated migration harness.
   - `stripe`: Generate payment checkout sessions and webhook receiver stubs.
   - `analytics`: Generate structured JSON event tracking logger.
4. **Agent Harness Synthesis**:
   - Synthesize autonomous worker agent script in `projects/agents/{name}_agent.py` bounded by `MAX_ITERATIONS = 10` and `TOKEN_BUDGET = 4096`.
5. **ACID Ledger Persistence**:
   - Insert record into SQLite `saas_projects` table.
   - Commit audit entry to `audit_logs`.

---

## 4. Checkpoint (Push-Right)
- **Design Rule**: The developer/founder is presented with a complete, tested project ready for development.
- **Decision-Ready Brief**:
  - Location: Command UI & Terminal output.
  - Brief Content: Project directory link, scaffolded file list, Makefile commands (`make dev`, `make test`), and generated agent script path.

---

## 5. Verification & Acceptance Criteria
- [x] Verified via `tests/test_saas_factory.py` (5/5 tests passing).
- [x] Tested live with sample venture `venture-autopilot` registered in `master.db`.
- [x] Zero external runtime dependencies during scaffolding (pure Python stdlib).
