# Plane Supreme Architecture Dossier & OMEGA Sovereign Teardown

**System**: Plane Community Edition (CE) & Cloud Platform  
**Repository**: [makeplane/plane](https://github.com/makeplane/plane)  
**License**: GNU Affero General Public License v3.0 (AGPL-3.0)  
**Integration Tier**: Supreme Sovereign Ecosystem (OMEGA ∞ Core Directive Compliant)  
**Ecosystem Artifacts**:
- Universal Orchestrator: [`plane_orchestrator.py`](file:///e:/anti/plane_orchestrator.py)
- Universal CLI: [`plane_cli.py`](file:///e:/anti/plane_cli.py)
- Model Context Protocol (MCP) Server: [`plane_mcp_server.py`](file:///e:/anti/plane_mcp_server.py)
- Autonomous REST API Server: [`plane_api_server.py`](file:///e:/anti/plane_api_server.py)
- Interactive Mission Control Cockpit: [`plane_control_cockpit.html`](file:///e:/anti/plane_control_cockpit.html)
- One-Click Launchers: [`START_PLANE_COCKPIT.bat`](file:///e:/anti/START_PLANE_COCKPIT.bat) & [`START_PLANE_WINDOWS.bat`](file:///e:/anti/START_PLANE_WINDOWS.bat)
- Agent Skill: [`.agents/skills/plane-orchestrator/SKILL.md`](file:///.agents/skills/plane-orchestrator/SKILL.md)
- Sovereign Execution Manifest: [`omega/data/plane_do_everything_manifest.json`](file:///e:/anti/omega/data/plane_do_everything_manifest.json)

---

## 1. Executive Summary & Value Proposition

Plane is the premier modern, open-source project management platform engineered as a modular, self-hostable alternative to Jira, Linear, Asana, and ClickUp. Designed from the ground up for developer ergonomics, product roadmapping, and agile velocity, Plane unifies issue tracking, time-boxed sprint cycles, epic milestones, collaborative rich-text documentation, and triage intake.

Within the **OMEGA Autonomous Agent Architecture**, Plane functions as the primary operational sensory canvas and task dispatch registry. Agents consume task specifications from Plane, report execution progress, upload verified test evidence to collaborative pages, and automatically update sprint burndown metrics.

```
+-----------------------------------------------------------------------------------+
|                        OMEGA AUTONOMOUS AGENT CORE                                |
|        (Antigravity Prime, Implementer, Reviewer, Security Guard)                 |
+-----------------------------------------------------------------------------------+
                                   | (JSON-RPC 2.0 stdio / REST)
                                   v
+-----------------------------------------------------------------------------------+
|               PLANE SOVEREIGN AUTONOMOUS ORCHESTRATION LAYER                      |
|                                                                                   |
|  [plane_mcp_server.py]       [plane_cli.py]         [plane_api_server.py :8774]   |
|         |                           |                            |                |
|         +---------------------------+----------------------------+                |
|                                     v                                             |
|                        [plane_orchestrator.py]                                    |
|                                     |                                             |
|        +----------------------------+-----------------------------+               |
|        | (Dual-Mode Failover)                                     |               |
|        v                                                          v               |
|  [LIVE API CLIENT]                                    [MOCK SIMULATION ENGINE]    |
|  - REST API v1                                        - Full In-Memory Relational |
|  - Bearer / X-API-Key                                 - File-Persisted State      |
|  - Port :8095 (Docker CE)                             - 12-Phase Sovereign Engine |
+-----------------------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------------------+
|                       PLANE CONTAINER TOPOLOGY                                    |
|  +------------------+  +-------------------+  +--------------------------------+  |
|  | plane-web (:3000)|  | plane-api (DRF)   |  | plane-worker (Celery)          |  |
|  +------------------+  +-------------------+  +--------------------------------+  |
|  +------------------+  +-------------------+  +--------------------------------+  |
|  | plane-db (PG 15) |  | plane-redis (v7)  |  | plane-minio (S3 Object Store)  |  |
|  +------------------+  +-------------------+  +--------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Architectural Decomposition & Technology Stack

Plane utilizes a decoupled microservices and clean domain architecture:

### 2.1 Backend Core (`plane-api`)
- **Framework**: Python 3.11+ with **Django** and **Django REST Framework (DRF)**.
- **Relational Storage**: **PostgreSQL 15+** with extensive indexing on workspace slugs, project identifiers, and issue sequence numbers.
- **ORM & Migrations**: Django ORM enforcing foreign key constraints, polymorphic issue types, and tenant isolation.
- **Authentication**: JWT tokens, Session cookies, and long-lived API tokens (`X-API-Key`).

### 2.2 Asynchronous Worker & Scheduler (`plane-worker` & `plane-beat-worker`)
- **Worker Engine**: **Celery** backed by **Redis 7+** (with optional RabbitMQ support).
- **Task Pipelines**:
  - Webhook dispatch and delivery retries with exponential backoff.
  - Email notification rendering and SMTP delivery.
  - Bulk issue imports/exports (GitHub, Jira, Linear migration pipelines).
  - Background analytics aggregation and daily sprint burndown snapshots.

### 2.3 Reactive Frontend (`plane-web`)
- **Modern Web Architecture**: Migrated to optimized React Router / Vite and Next.js for high-speed compilation, incremental static regeneration, and client-side view caching.
- **Styling & Components**: Tailwind CSS, Radix UI primitives, Lucide icons, and custom glassmorphism design tokens.
- **Editor**: Prosemirror / Tiptap rich-text engine with Markdown shortcuts, mentions, and issue embeds.

### 2.4 Edge & Ingress (`plane-proxy` & `plane-minio`)
- **Reverse Proxy**: Nginx or Caddy routing traffic between web assets (`/`), API endpoints (`/api/`), and media storage (`/uploads/`).
- **Object Storage**: MinIO S3-compatible storage for user avatars, issue file attachments, and exported data bundles.

---

## 3. Data Dictionary & Entity Hierarchy

```
  Workspace (Root Tenant)
     │
     ├── Members & Roles (Admin, Member, Viewer, Guest)
     │
     └── Projects (Identifier: CORE, FLEET, INTEL, CAP)
           │
           ├── State Machine (Backlog, Todo, In Progress, Verification, Done, Cancelled)
           │
           ├── Issues / Work Items (Sequenced, Priorities, Estimates, Assignees)
           │     ├── Sub-issues
           │     └── Issue Links (Blocking / Blocked By)
           │
           ├── Cycles (Sprints: Time-boxed, Burndown Curves, Scope-creep)
           │
           ├── Modules (Epics / Milestones: Leads, Target Dates, % Completion)
           │
           ├── Pages (Collaborative Knowledge Base, AI Summaries)
           │
           ├── Views (Kanban Boards, Lists, Calendar, Gantt)
           │
           └── Triage Inbox (Unassigned sensor & customer requests)
```

---

## 4. The 12-Phase Sovereign Lifecycle (`do_everything`)

The `plane_orchestrator.py` engine implements an automated 12-phase verification lifecycle adhering to Section 5 and Section 14 of the OMEGA Constitution:

| Phase | Subsystem | Validation Scope |
|---|---|---|
| **Phase 1** | Pre-Flight Telemetry | Stack discovery, runtime version verification, API latency probe. |
| **Phase 2** | Workspace Hierarchy | Multi-tenant tenant boundary checks and workspace configuration. |
| **Phase 3** | Project & State Workflows | Project identifier validation, state transition integrity, color schemes. |
| **Phase 4** | Work Items Matrix | Issue CRUD, Fibonacci story point estimates, priority weighting. |
| **Phase 5** | Sprint Cycles & Burndown | Start/end date enforcement, actual vs ideal story point burndown curve. |
| **Phase 6** | Modules & Milestones | Epic milestone completion tracking and cross-cycle aggregation. |
| **Phase 7** | Collaborative Pages | Knowledge base documentation rendering, AI summary generation. |
| **Phase 8** | Custom Views & Kanban | Kanban state projection, custom filter logic, sorting criteria. |
| **Phase 9** | Triage Intake Buffer | Inbound request promotion/rejection pipeline and issue elevation. |
| **Phase 10** | Velocity Analytics | Statistical calculation of lead time, cycle time, and weekly throughput. |
| **Phase 11** | Webhook & Agent Reactor | Bi-directional event dispatch and agent task reactor triggering. |
| **Phase 12** | Sovereign Attestation | Cryptographic ledger manifest export to `omega/data/plane_do_everything_manifest.json`. |

---

## 5. Model Context Protocol (MCP) Tool Reference

The stdio MCP server (`plane_mcp_server.py`) provides 16 tools for autonomous coding agents:

1. `plane_get_info`: Runtime telemetry, version, and entity census.
2. `plane_list_workspaces`: List tenant workspaces.
3. `plane_list_projects`: Enumerate workspace projects.
4. `plane_create_project`: Provision new project initiative.
5. `plane_list_issues`: Query issues with project, cycle, or state filters.
6. `plane_create_issue`: Create task with priority and story points.
7. `plane_update_issue`: Modify state, priority, or assignees.
8. `plane_list_cycles`: List sprint cycles.
9. `plane_create_cycle`: Define time-boxed sprint.
10. `plane_get_burndown`: Compute mathematical burndown velocity.
11. `plane_list_modules`: List epic milestones.
12. `plane_create_module`: Provision epic deliverable.
13. `plane_list_pages`: List collaborative documentation pages.
14. `plane_create_page`: Create knowledge base documentation.
15. `plane_list_triage`: List pending triage requests.
16. `plane_triage_action`: Promote or reject triage items.
17. `plane_get_analytics`: Project velocity and lead-time report.
18. `plane_do_everything`: Comprehensive 12-phase execution.

---

## 6. OMEGA Constitutional Alignment

- **Zero Vibe Coding (Directive 4)**: Tasks are created with explicit story point estimates, priority tiers, and test criteria before implementation starts.
- **Deep Modules (Directive 12)**: Simple, zero-dependency orchestrator exposing high-level operations while hiding complex state machine and burndown calculations.
- **Evidence Ledgers (Directive 27)**: Every 12-phase run records exact execution timestamps, phase latencies, and output payloads into persistent JSON manifests.
- **Ponytail Minimalism (Lazy Senior Dev)**: Uses standard Python library (`urllib.request`, `json`, `dataclasses`, `socket`, `http.server`) with zero external pip dependencies required for core orchestration.
