---
name: windmill-orchestrator
description: "Use when orchestrating, executing, or managing distributed workflows, scripts, and internal tools via Windmill. Triggers: multi-step DAG workflows, Python/TypeScript/SQL/Bash script execution, human-in-the-loop approvals, PostgreSQL SKIP LOCKED job queues, Rust native worker pools, low-code app building, typed resource credentials, cron schedules, and Windmill Hub community integrations."
metadata:
  author: OMEGA Autonomous Core
  version: "2.0.0"
---

# Windmill Autonomous Orchestrator

Autonomous standard operating procedure and programmatic interface for managing, executing, and monitoring distributed workflows, sandboxed scripts, and internal applications using Windmill (https://github.com/windmill-labs/windmill).

## 1. Architectural Foundation

Windmill is an ultra-fast, developer-first alternative to Temporal, Retool, Airplane, and Airflow. It is powered by a high-performance **Rust Core Backend**, PostgreSQL queuing, and sandboxed polyglot worker processes:

```
+--------------------------------------------------------------------------+
|                     Windmill Control Plane & UI                          |
|         (SvelteKit Frontend + Rust Warp/Axum Server Engine)              |
+--------------------------------------------------------------------------+
                                    |
                    pg_notify / FOR UPDATE SKIP LOCKED
                                    v
+--------------------------------------------------------------------------+
|                        PostgreSQL 16 Engine                              |
|   - Workspaces, Scripts, Flow DAG Topologies, Encrypted Variables/Secrets|
|   - High-Throughput Job Queue (10,000+ jobs/sec capability)              |
+--------------------------------------------------------------------------+
                                    |
                    Distributed Worker Pool Dispatch
                                    v
+--------------------------------------------------------------------------+
|                       Polyglot Execution Workers                         |
|   - Rust Native Worker: Sub-millisecond execution overhead               |
|   - Python Worker: Isolated venvs, automatic dependency resolution       |
|   - TypeScript / JavaScript: Deno / Bun v8 runtime                       |
|   - SQL / Bash / Go / PHP: Sandboxed nsjail / Docker processes           |
+--------------------------------------------------------------------------+
```

### Core Invariants
1. **Zero Cold-Start Rust Core:** Native Rust worker threads dispatch and execute non-isolated tasks in microseconds.
2. **Topological DAG Flow Resolution:** Workflows are Directed Acyclic Graphs composed of scripts with explicit inputs, transforms, conditional branching, and error handlers.
3. **Suspension & Human-in-the-Loop:** Flows can pause execution (`status: SUSPENDED`), trigger Slack Block Kit or Email alerts, and wait days for executive sign-off without consuming compute threads.
4. **Typed Resources & Secret Vault:** All credentials (PostgreSQL, Slack, AWS, OpenAI) are strongly typed and encrypted at rest using AES-256-GCM.

---

## 2. Programmatic Python SDK & CLI Usage

The repository provides a deep-module SDK and CLI at `windmill_orchestrator.py` and `windmill_cli.py`.

### Quick CLI Commands

```bash
# Platform summary, active workers, and queue telemetry
python windmill_cli.py info

# List multi-tenant workspaces
python windmill_cli.py workspaces

# List registered scripts, flow DAGs, schedules, and variables
python windmill_cli.py scripts
python windmill_cli.py flows
python windmill_cli.py schedules
python windmill_cli.py variables

# Execute a workspace script with JSON arguments
python windmill_cli.py run-script u/admin/cbam_carbon_audit --args '{"net_mass_kg": 24500}'

# Execute a multi-step DAG flow
python windmill_cli.py run-flow u/admin/enterprise_client_onboarding_dag

# Trigger an automated cron schedule immediately
python windmill_cli.py trigger-schedule nightly_reconciliation

# Set or update an encrypted workspace variable / secret
python windmill_cli.py set-variable api_key "sk_live_998124" --secret --description "Production API Key"

# Trigger a webhook route
python windmill_cli.py webhook stripe-payment-failed --payload '{"amount": 12500}'

# Approve or reject a suspended human-in-the-loop workflow job
python windmill_cli.py approve-job job-wmill-1003 --notes "Authorized by Sovereign Executive"

# Run complete 12-Phase Sovereign Full Platform Validation
python windmill_cli.py do-everything
```

### Python SDK Integration

```python
from windmill_orchestrator import WindmillClient, WindmillOrchestrator

client = WindmillClient()
orchestrator = WindmillOrchestrator(client)

# Inspect cluster health
telemetry = client.get_telemetry()
print(f"Workers: {telemetry['active_workers']}, Mode: {telemetry['mode']}")

# Run script
job = client.run_script("u/admin/cbam_carbon_audit", {"net_mass_kg": 32000.0})
print(f"Job {job['id']} completed in {job['duration_ms']}ms: {job['result']}")

# Execute flow DAG
flow_job = client.execute_flow("u/admin/enterprise_client_onboarding_dag", {"requested_credit_inr": 750000.0})
if flow_job["status"] == "SUSPENDED":
    print(f"Flow suspended at: {flow_job['result']['suspended_step']}")
    # Approve job
    client.approve_job(flow_job["id"], approved=True, notes="Executive approval confirmed.")
```

---

## 3. Mission Control Cockpit & API Server

- **Mission Control Cockpit:** `windmill_control_cockpit.html` (10 operational tabs: Script Studio, Flow DAG Visualizer, Automated Schedules & Crons, Variables & Secrets Vault, Webhook Ingress, Worker Telemetry, Low-Code Apps, Hub Marketplace, Job History, and MCP Playground).
- **Local API Server:** `windmill_api_server.py` running on `http://localhost:8768/`.
- **One-Click Windows Launcher:** `START_WINDMILL_WINDOWS.bat` and `scripts/start_windmill_windows.ps1`.

---

## 4. MCP Agent Tools

The Windmill suite exposes 21 enterprise tools via `windmill_mcp_server.py`:
- `windmill_get_system_info`: Real-time cluster health and worker telemetry.
- `windmill_list_workspaces`: Query registered multi-tenant workspaces.
- `windmill_list_scripts`, `windmill_get_script`, `windmill_run_script`: Script exploration, schema inspection, and execution.
- `windmill_list_flows`, `windmill_get_flow`, `windmill_run_flow`: Multi-step DAG orchestration and topological execution.
- `windmill_list_schedules`, `windmill_get_schedule`, `windmill_create_schedule`, `windmill_trigger_schedule`: Cron management.
- `windmill_list_variables`, `windmill_get_variable`, `windmill_set_variable`, `windmill_delete_variable`: Config & encrypted secret vault.
- `windmill_list_resources`, `windmill_get_resource`, `windmill_create_resource`: Strongly typed credentials (Postgres, S3, Slack).
- `windmill_list_jobs`, `windmill_get_job`, `windmill_approve_job`: Execution ledger & human-in-the-loop approvals.
- `windmill_list_apps`: Low-code internal application definitions.
- `windmill_search_hub`, `windmill_import_hub_item`: Windmill Hub template marketplace.
- `windmill_do_everything`: End-to-end 12-phase sovereign platform execution and manifest generation.
