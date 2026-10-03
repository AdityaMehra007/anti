# Apache Airflow Production Platform & Orchestration Hub

Production deployment stack, custom operator plugin framework, and reference DAG suite for Apache Airflow.

---

## 📁 Repository Structure

```
airflow_platform/
├── dags/                               # Production DAG definitions
│   ├── enterprise_etl_pipeline.py      # TaskFlow API + Dynamic Task Mapping (AIP-42)
│   ├── asset_aware_pipeline.py         # Data-driven Asset scheduling (AIP-44 / AIP-60)
│   ├── deferrable_async_pipeline.py    # Async Deferrable Operator & Triggerer loop
│   └── maintenance_cleanup_pipeline.py # DB hygiene and log maintenance
├── plugins/                            # Extensibility layer
│   └── custom_orchestration_plugin.py  # Custom Hook & Operator pattern with telemetry
├── config/                             # Airflow configuration overrides
├── scripts/                            # Operational & CI/CD tools
│   ├── init_env.py                     # Fernet key generator and environment initializer
│   └── test_dags.py                    # Automated pytest suite for DAG syntax & integrity
├── .env.example                        # Template environment configuration
├── .env                                # Generated active environment config
├── docker-compose.yaml                 # Multi-service CeleryExecutor Docker stack
├── Dockerfile                          # Production container image definition
├── requirements.txt                    # Provider & library dependencies
└── README.md                           # Documentation and runbook
```

---

## 🚀 Quickstart

### 1. Initialize Environment
Run the bootstrap utility to generate a cryptographic Fernet key and verify required paths:
```powershell
python scripts/init_env.py
```

### 2. Run CI/CD DAG Validation Tests
Verify that all DAGs are syntactically sound, pass AST checks, adhere to mandatory tagging standards, and have no cycle errors:
```powershell
python -m pytest scripts/test_dags.py -v
```

### 3. Launch Services via Docker Compose
When Docker is running, launch the entire multi-service stack (PostgreSQL, Redis, Webserver, Scheduler, Celery Worker, Triggerer):
```bash
docker compose up -d --build
```

### 4. Access Control Plane
- **Web UI URL**: [http://localhost:8080](http://localhost:8080)
- **Default Username**: `admin`
- **Default Password**: `admin_password`

---

## ⚡ Included DAG Topologies

| DAG ID | Pattern & AIP | Description |
| :--- | :--- | :--- |
| `enterprise_etl_pipeline` | TaskFlow + AIP-42 Dynamic Mapping | Dynamic partition discovery spawning isolated mapped tasks (`.expand()`), data quality gate, typed XCom aggregation. |
| `asset_producer_telemetry_ingest` | AIP-60 Asset Producer | Emits standardized URI asset updates (`s3://data-lake-lakehouse/bronze/telemetry.parquet`). |
| `asset_consumer_metrics_aggregator` | AIP-60 Asset Consumer | Triggered dynamically on asset generation without rigid cron clocks. |
| `deferrable_async_pipeline` | Deferrable Async / Triggerer | Suspends worker thread upon submission, delegating polling to the `asyncio` Triggerer daemon to eliminate idle worker compute. |
| `airflow_maintenance_hygiene` | Operational Housekeeping | Runs weekly database pool audit and log retention cleanup. |

---

## 🛡️ Production Best Practices Implemented
1. **Zero-Lock Database Architecture**: CeleryExecutor with Redis ensures schedulers do not fight workers for row-level locks.
2. **Deterministic Fernet Encryption**: Variables and connection secrets are encrypted using AES-128-CBC Fernet keys.
3. **Automated CI/CD Validation**: Tests run pre-deployment via `scripts/test_dags.py` without requiring database connectivity.
