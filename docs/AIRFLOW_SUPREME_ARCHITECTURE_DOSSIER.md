# APACHE AIRFLOW SUPREME ARCHITECTURE & AUTONOMOUS ORCHESTRATION DOSSIER

**System Classification**: Sovereign Data Workflow Orchestration Platform  
**Target Upstream Repository**: [`https://github.com/apache/airflow`](https://github.com/apache/airflow)  
**Version Alignment**: Apache Airflow v2.10.x / Airflow 3.0 Task SDK & Modern React Core  
**Integration Tier**: OMEGA Autonomous Operating System & Enterprise Factory Mode  

---

## 1. Executive Summary & The Orchestration Paradigm

Apache Airflow is the foundational global standard for programmatic workflow orchestration, scheduling, and data pipeline governance. Conceived at Airbnb and incubated under the Apache Software Foundation, Airflow introduced the **Configuration-as-Code** revolution: expressing Directed Acyclic Graphs (DAGs) as standard Python scripts rather than rigid XML, JSON, or drag-and-drop configurations.

In the OMEGA sovereign enterprise architecture, Apache Airflow serves as the primary distributed batch engine, handling high-throughput ETL/ELT pipelines, machine learning training cycles, regulatory financial reconciliations, and scheduled security threat hunting.

### Comparison: Airflow vs Modern Workflow Engines

| Dimension | **Apache Airflow (2.10 / 3.0)** | **Windmill Engine** | **Dagster** | **Temporal** |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Philosophy** | Directed Acyclic Graphs (DAGs) as Python code | Fast polyglot scripts & DAGs in Rust core | Software-defined Assets & data lineage | Code-as-a-State-Machine (Durable execution) |
| **Backend Core** | Python (Celery/K8s/Local) & Asyncio Triggerer | Rust (Microsecond dispatch, <40MB RAM) | Python (Asset DAG catalog) | Go / Java / TypeScript workers |
| **Scheduling Model** | Timetables, Cron, & Data-Driven Assets | Crons, Webhooks & Event Streams | Asset-based partitioning & schedules | Event-driven workflow signals & timers |
| **Execution Speed** | 20ms – 100ms dispatch | < 1.5ms native dispatch | 30ms – 150ms dispatch | Sub-millisecond event loop |
| **Worker Isolation** | Celery Workers, K8s Pods, Edge Workers | Rust native threads + nsjail sandboxes | Process / Subprocess / K8s | Native lightweight workflow threads |
| **Dynamic Workflows** | Dynamic Task Mapping (`.expand()`) | Dynamic Flow loops & sub-flows | Dynamic output mapping | Native loops in programming language |
| **Ecosystem Size** | 100+ Official Providers (AWS, GCP, Snowflake) | Rapidly growing Hub catalog | Python data tooling ecosystem | General microservices orchestration |

---

## 2. Core Airflow Architecture & Component Topology

Apache Airflow is engineered as a decoupled, multi-tier distributed architecture centered around an ACID metadata database:

```
+---------------------------------------------------------------------------------------------------+
|                                 USER & EXTERNAL INGRESS                                           |
|  - Modern Web UI (Vite / React)  ·  REST API (/api/v1/...)  ·  Airflow CLI  ·  MCP Server         |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                      AIRFLOW SCHEDULER                                            |
|  - Multi-threaded DAG Processor (Parses DAG files -> Serialized DAG JSON in DB)                   |
|  - Scheduling Loop (Evaluates Timetables, Asset triggers, SLA misses)                            |
|  - TaskInstance State Machine (Sets state = QUEUED, evaluates pools & priorities)                 |
+---------------------------------------------------------------------------------------------------+
                         │                                                  │
                         ▼                                                  ▼
+---------------------------------------------------+   +-------------------------------------------+
|               AIRFLOW TRIGGERER                   |   |            METADATA DATABASE              |
|  - Single-process Asyncio Event Loop              |   |  - PostgreSQL 16 / MySQL / SQLite         |
|  - Manages Deferred Tasks (frees worker slots)    |   |  - Serialized DAGs, DAG Runs, TaskInstances|
|  - Yields TriggerEvents -> Resumes task execution |   |  - XCom Table, Variables, Connections     |
+---------------------------------------------------+   +-------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                      AIRFLOW EXECUTORS                                            |
|   [LocalExecutor]         [CeleryExecutor]        [KubernetesExecutor]       [EdgeExecutor]       |
|    Subprocess queue       Redis/RabbitMQ broker    Dynamic K8s Pod per task   Remote On-Prem Nodes|
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                      EXECUTION WORKERS                                            |
|  - Airflow 3 Task SDK: Fast execution agent communicating over lightweight Execution API          |
|  - Executes Operators (PythonOperator, BashOperator, SQL, Docker, S3, Snowflake)                  |
|  - Emits Heartbeats, XCom updates, State changes (SUCCESS, FAILED, UP_FOR_RETRY)                  |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Deep Dive: Airflow 3.0 Architectural Evolution

The modern Apache Airflow 3.0 overhaul addresses historic architectural bottlenecks:

### A. The Execution API & Task SDK
In legacy Airflow (2.x), worker tasks connected directly to the central PostgreSQL database. Under high concurrency (thousands of tasks), database connection exhaustion occurred.
Airflow 3 introduces the **Fast Execution API**:
- Workers no longer touch the database directly.
- A dedicated HTTP Fast Execution API sits between workers and the database.
- The **Task SDK** runs inside the worker process, handling task lifecycle, XCom serialization, and logging over gRPC/HTTP.

### B. Multi-Language Task SDKs
Airflow 3 expands beyond Python workers by providing native SDKs:
- **Go SDK**: Compile native Go binaries into Airflow tasks.
- **TypeScript / Node SDK**: Run TypeScript workflows natively without Python runtime overhead.
- **Java SDK**: Enterprise JVM integration for Spark and big-data processing.

### C. Modern React UI
Legacy Flask AppBuilder is superseded by a modern, high-speed single-page application built on React, Vite, and TanStack Query, delivering instantaneous DAG graph exploration, sub-second grid navigation, and real-time log streaming.

---

## 4. Fundamental Airflow Primitives & Execution Semantics

### 1. Directed Acyclic Graph (DAG)
A collection of all tasks you want to run, organized in a way that reflects their relationships and dependencies.
- **Topological Sorting**: Airflow guarantees acyclicity using Kahn's algorithm or depth-first search. Any cycle raises `AirflowDagCycleException`.
- **Catchup & Backfill**: Airflow can backfill all historical schedule intervals between `start_date` and today.

### 2. TaskFlow API (`@dag` & `@task`)
Introduced in Airflow 2.0, the TaskFlow API allows writing idiomatic Python functions with decorator syntax:
```python
@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False)
def etl_pipeline():
    @task
    def extract() -> dict:
        return {"records": [1, 2, 3]}

    @task
    def transform(data: dict) -> list:
        return [x * 2 for x in data["records"]]

    @task
    def load(result: list):
        print(f"Loaded: {result}")

    load(transform(extract()))
```
Dependencies and XCom passing are inferred automatically from function arguments and returns.

### 3. Dynamic Task Mapping (`.expand()`)
Enables generating task instances dynamically at runtime based on upstream results:
```python
@task
def get_files() -> list[str]:
    return ["s3://bucket/part1.parquet", "s3://bucket/part2.parquet"]

@task
def process_file(file_path: str):
    # Runs in parallel as mapped task instances: process_file[0], process_file[1]
    return parse(file_path)

files = get_files()
process_file.expand(file_path=files)
```

### 4. Data-Driven Scheduling (Airflow Assets / Datasets)
DAGs can be triggered not just by time, but by data availability. When an upstream task produces an update to a dataset URI:
```python
raw_sales_dataset = Dataset("s3://warehouse/sales/raw.parquet")

@dag(schedule="@hourly")
def producer_dag():
    @task(outlets=[raw_sales_dataset])
    def extract_sales():
        write_s3_parquet()

@dag(schedule=[raw_sales_dataset])
def consumer_dag():
    @task
    def build_aggregates():
        pass
```
Airflow 2.10+ and 3.0 support boolean expression asset triggers: `schedule=(dataset_a & dataset_b) | dataset_c`.

### 5. Deferrable Operators & The Triggerer
Standard sensors block worker threads while polling external systems. **Deferrable Operators** yield execution to the asyncio-based **Triggerer** daemon:
1. Operator calls `self.defer(trigger=ExternalSensorTrigger(...), method_name='execute_complete')`.
2. Worker process releases task execution and terminates its slot.
3. Triggerer event loop monitors the external event asynchronously (1 process can monitor 10,000+ triggers).
4. When the event fires, the Triggerer notifies the Scheduler to re-queue the task on a worker at `execute_complete`.

### 6. Pools, Concurrency & Slots
Airflow controls concurrency to prevent overwhelming downstream databases:
- **Pools**: Named buckets with slot limits (e.g. `snowflake_pool` with 10 slots).
- **Task Priorities**: `priority_weight` determines which queued task claims the next available slot.
- **Concurrency Controls**:
  - `max_active_runs`: Maximum concurrent runs per DAG.
  - `max_active_tasks_per_dag`: Maximum concurrent tasks across all active runs of a DAG.

### 7. XCom (Cross-Communication)
XCom allows tasks to exchange small pieces of metadata (task outputs, row counts, partition keys).
- Stored in the metadata database or offloaded to S3/GCS via custom XCom backends for larger payloads.

---

## 5. Security & Secrets Management

1. **Fernet Encryption**: Airflow securely encrypts database connection passwords and extra fields using 128-bit AES in CBC mode with HMAC SHA256 authentication.
2. **External Secrets Backends**: Natively integrates with AWS Secrets Manager, HashiCorp Vault, Google Cloud Secret Manager, and Infisical.
3. **Role-Based Access Control (RBAC)**: Fine-grained permissions per DAG, connection, variable, and UI view.

---

## 6. OMEGA Autonomous Architecture Integration

In this repository, the Apache Airflow Autonomous Orchestration Ecosystem is integrated as follows:

1. **Autonomous Orchestration SDK** (`airflow_orchestrator.py`):
   - Dual-mode: Connects to live Airflow instances via REST API or runs high-fidelity offline simulation.
   - Comprehensive mock scheduler, worker pool, dynamic task mapper, dataset pub/sub, XCom engine, and triggerer.
2. **Universal CLI** (`airflow_cli.py`):
   - Comprehensive command-line control for agents and operators (`dags`, `dag-runs`, `trigger`, `tasks`, `xcom`, `pools`, `audit`, `do-everything`).
3. **Local REST API Server** (`airflow_api_server.py`):
   - Runs on port 8775 (with auto-fallback).
   - Bridges Airflow v1 API endpoints with the live Mission Control Cockpit.
4. **Model Context Protocol (MCP) Server** (`airflow_mcp_server.py`):
   - Exposes 15 high-leverage tools for AI agents via JSON-RPC 2.0.
5. **Mission Control Cockpit** (`airflow_control_cockpit.html`):
   - Glassmorphic operations cockpit with SVG topological DAG visualizer, Grid/Gantt execution matrix, live log stream, and secrets vault.
6. **Agent Skill** (`.agent/skills/airflow-orchestrator/SKILL.md`):
   - Protocol and standard operating procedure for autonomous Airflow engineering.
