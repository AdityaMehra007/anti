---
name: airflow-orchestrator
description: Autonomous standard operating procedure and execution capability for Apache Airflow workflow orchestration, DAG authoring, task instance execution, dynamic task mapping, datasets, and infrastructure governance.
---

# Apache Airflow Autonomous Orchestrator

## Overview
Autonomous engineering capability for Apache Airflow (https://github.com/apache/airflow) across versions 2.10.x and modern Airflow 3.0 Task SDK architectures.

This skill equips agents with:
1. Programmatic DAG authoring using the modern TaskFlow API (`@dag`, `@task`, `@task.branch`).
2. Dynamic Task Mapping (`.expand()`) for horizontal scale over runtime-evaluated partitions.
3. Data-driven scheduling via Airflow Datasets / Assets (`Dataset("uri")`).
4. Asynchronous deferrable execution via the Triggerer daemon to release worker slots on long-running I/O.
5. Pool concurrency throttling, priority weighting, and Fernet-encrypted secret vaults.
6. Multi-environment orchestration via the local REST API server, universal CLI, and MCP tools.

---

## 1. Quick Start & Execution

### Launching the Autonomous Cockpit & API Server
```powershell
# One-click Windows launch
.\START_AIRFLOW_WINDOWS.bat

# Or run API server directly (Port 8775)
python airflow_api_server.py --port 8775
```
Access the interactive Mission Control Cockpit at: `http://localhost:8775/cockpit`

### Universal CLI Operations
```bash
# System telemetry and scheduler health
python airflow_cli.py info

# List all registered DAGs
python airflow_cli.py dags

# Inspect specific DAG and its topological execution sequence
python airflow_cli.py dag financial_ledger_reconciliation

# Trigger a DAG Run with execution configuration
python airflow_cli.py trigger financial_ledger_reconciliation --conf '{"mode": "audit_strict"}'

# Pause or unpause a DAG
python airflow_cli.py pause customer_churn_prediction_ml
python airflow_cli.py unpause customer_churn_prediction_ml

# List historical DAG Runs
python airflow_cli.py dag-runs financial_ledger_reconciliation

# Inspect Task Instances for a run
python airflow_cli.py task-instances cbam_carbon_border_etl

# Inspect XCom metadata
python airflow_cli.py xcom cbam_carbon_border_etl process_docket_tariff

# Manage Airflow Variables
python airflow_cli.py variables
python airflow_cli.py variables --set cbam_tariff_multiplier 1.385 --desc "EU CBAM factor"

# Inspect Concurrency Pools
python airflow_cli.py pools

# Emit Dataset update event
python airflow_cli.py datasets --emit "s3://omega-warehouse/raw_sales/v1"

# Run security & architecture audit
python airflow_cli.py audit

# Execute 12-phase sovereign lifecycle validation
python airflow_cli.py do-everything
```

---

## 2. Python SDK Deep Module Integration

```python
from airflow_orchestrator import AirflowClient, AirflowConfig, AirflowOrchestrator

# Initialize client (auto-detects live Airflow instance or high-fidelity simulation)
client = AirflowClient(AirflowConfig(base_url="http://localhost:8080", mock_mode=False))

# Trigger DAG Run
run = client.trigger_dag("financial_ledger_reconciliation", conf={"batch_id": "BATCH-001"})
print(f"Run ID: {run['run_id']} - Status: {run['state']}")

# Emit Dataset Event to trigger downstream DAGs
client.emit_dataset_event("s3://omega-warehouse/raw_sales/v1", source="agent_etl")

# Inspect Pools
pools = client.list_pools()
for p in pools:
    print(f"Pool {p['name']}: {p['occupied_slots']}/{p['slots']} slots occupied")
```

---

## 3. Model Context Protocol (MCP) Tools

When acting as an autonomous agent in Antigravity or multi-agent swarms, use the `airflow-mcp-server`:
- `airflow_get_health`: Query scheduler, webserver, triggerer, and metadb health.
- `airflow_list_dags`: List all DAGs with schedule, tags, and pause state.
- `airflow_get_dag_details`: Get DAG structure, task graph, and topological order.
- `airflow_trigger_dag`: Dispatch execution with custom JSON conf.
- `airflow_toggle_dag_pause`: Pause or activate DAG schedules.
- `airflow_list_dag_runs`: Retrieve historical run states and execution timestamps.
- `airflow_list_task_instances`: Inspect task execution status for a run.
- `airflow_get_task_log`: Stream execution logs for an attempt.
- `airflow_get_xcom`: Pull inter-task XCom values.
- `airflow_list_variables` & `airflow_set_variable`: Manage configuration store.
- `airflow_list_connections`: Inspect configured data warehouse & cloud connections.
- `airflow_list_pools`: Monitor pool saturation and queue pressure.
- `airflow_emit_dataset_event`: Fire asset updates to trigger consumer pipelines.
- `airflow_audit_dags`: Audit DAGs for cycles, missing retries, and unthrottled heavy operators.

---

## 4. Production Stack & Docker Deployment

To launch the full distributed Airflow 2.10+ / 3.0 Celery stack with PostgreSQL 16 and Redis:
```powershell
.\scripts\start_airflow_windows.ps1 -Docker
```
Or navigate to `stacks/airflow` and execute:
```bash
docker compose up -d
```
The Airflow Webserver is available at `http://localhost:8080` (admin/admin).
