---
name: plane-orchestrator
description: Autonomous SDK, CLI, MCP Server, and operational standard for Plane (https://github.com/makeplane/plane). Enables multi-tenant workspace management, issue tracking, Kanban projection, sprint cycles with real-time SVG burndown curves, epic milestone roadmaps, collaborative knowledge documentation, triage intake queues, velocity analytics, and 12-phase sovereign lifecycle execution.
---

# Plane Autonomous Orchestrator & Execution Skill

Autonomous standard operating procedure, deep Python SDK, CLI, and Model Context Protocol (MCP) server for Plane (https://github.com/makeplane/plane).

## Architecture & Primitives

1. **Dual-Mode Execution Architecture**:
   - **Live REST API Mode**: Connects directly to real Plane Community Edition (CE) or Plane Cloud instances (`http://localhost:8095` or `https://app.plane.so`) via Bearer or `X-API-Key` tokens.
   - **High-Fidelity Simulation Engine**: Complete offline mock engine simulating Plane v1.4+ (PostgreSQL models, state machine workflows, burndown curves, and triage queues) for deterministic testing, CI/CD, and air-gapped agent operations.

2. **Core Capabilities**:
   - **Workspaces & Projects**: Scoped initiatives with identifiers (e.g. `CORE`, `FLEET`, `CAP`), leads, icon emojis, and feature toggles.
   - **State Machine Workflows**: Dynamic state progression (`backlog` -> `unstarted` -> `started` -> `completed` -> `cancelled`) with custom color schemes and sequencing.
   - **Work Items / Issues**: Hierarchical tasks with priority tiers (`urgent`, `high`, `medium`, `low`, `none`), Fibonacci story point estimates, assignees, cycle and module bindings.
   - **Cycles (Sprints)**: Iteration planning with start/end bounds, total points, completed points, scope-creep tracking, and mathematical burndown velocity curves.
   - **Modules (Epics / Milestones)**: Strategic milestones grouping cross-cycle work items with percentage completion tracking.
   - **Collaborative Pages**: Rich documentation knowledge base with AI summaries and multi-level permissions.
   - **Triage Queue**: Inbound request intake buffer for sensors, agents, and external webhooks with automated promote/reject actions.
   - **Velocity & Analytics**: Statistical lead time, cycle time, weekly throughput, and priority distribution metrics.
   - **Docker Stack Orchestration**: Complete multi-container deployment specification (`plane-web`, `plane-api`, `plane-worker`, `plane-db`, `plane-redis`, `plane-minio`).

3. **12-Phase Sovereign Lifecycle (`do-everything`)**:
   - Phase 1: Environment & Stack Pre-Flight Telemetry
   - Phase 2: Workspace & Enterprise Hierarchy Certification
   - Phase 3: Project Configuration & State Machine Workflow Validation
   - Phase 4: Issue & Task Lifecycle Matrix (CRUD, Estimates, Sub-tasks)
   - Phase 5: Sprint Cycles & Real-Time Burndown Velocity Engine
   - Phase 6: Modules & Epics Milestone Completion Tracking
   - Phase 7: Collaborative Pages & Knowledge Base Documentation
   - Phase 8: Custom Views, Kanban Projection & Filter Engine
   - Phase 9: Triage Intake Buffer & Autonomous Promotion Pipeline
   - Phase 10: Velocity Analytics, Lead Time & Throughput Calculation
   - Phase 11: Webhook Subscription & Agent Reactor Event Dispatch
   - Phase 12: Sovereign Execution Manifest & Cryptographic Attestation

---

## Universal CLI Usage

```bash
# Query system telemetry & mode
python plane_cli.py info

# List workspaces & projects
python plane_cli.py workspaces
python plane_cli.py projects --workspace omega

# Create project
python plane_cli.py create-project "Security Ops" "SEC" --desc "SecOps & Hardening" --emoji "🛡️"

# Manage work items / issues
python plane_cli.py issues --project proj-core-01
python plane_cli.py create-issue "Implement Webhook Verification" --project proj-core-01 --priority high --estimate 5
python plane_cli.py update-issue iss-005 --state st-proj-core-01-done

# Inspect sprint cycles & calculate burndown
python plane_cli.py cycles --project proj-core-01
python plane_cli.py burndown cyc-omega-sprint-25

# Inspect milestones, pages & triage
python plane_cli.py modules --project proj-core-01
python plane_cli.py pages --project proj-core-01
python plane_cli.py triage --project proj-core-01
python plane_cli.py triage-action trg-001 --action accept

# Calculate velocity & cycle time analytics
python plane_cli.py analytics --project proj-core-01

# Inspect Docker Compose container configuration
python plane_cli.py docker-config

# Execute Complete 12-Phase Sovereign Lifecycle
python plane_cli.py do-everything
```

---

## Model Context Protocol (MCP) Integration

The Plane MCP server runs on stdio and exposes 16 tools:

```json
{
  "name": "plane_do_everything",
  "description": "Execute comprehensive 12-Phase Sovereign Plane Lifecycle",
  "inputSchema": { "type": "object", "properties": {} }
}
```

To run stdio server:
```bash
python plane_mcp_server.py
```

---

## Mission Control Cockpit & API Server

- **REST API Server**: Port `8774` (`python plane_api_server.py --port 8774`)
- **Interactive Cockpit UI**: `http://localhost:8774/cockpit` or open `plane_control_cockpit.html` directly.
- **One-Click Launchers**:
  - `START_PLANE_COCKPIT.bat`: Starts REST server on `:8774` and opens browser cockpit.
  - `START_PLANE_WINDOWS.bat`: Executes 12-Phase sovereign lifecycle and opens cockpit.
