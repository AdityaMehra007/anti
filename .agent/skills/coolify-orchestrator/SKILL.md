---
name: coolify-orchestrator
description: "Use when orchestrating, deploying, or managing infrastructure via Coolify (PaaS). Triggers: self-hosted app deployments, Docker Compose stacks, Traefik edge routing, database provisioning (PostgreSQL, Redis, MySQL, MongoDB, ClickHouse), Nixpacks builds, multi-server SSH orchestration, 1-click open-source service templates (n8n, Plausible, Supabase, AnythingLLM, MinIO), and automated rolling deployments."
metadata:
  author: OMEGA Autonomous Core
  version: "1.0.0"
---

# Coolify Autonomous Orchestrator

Autonomous standard operating procedure and programmatic interface for managing, deploying, and maintaining cloud infrastructure, containers, and databases using Coolify v4.

## 1. Architectural Foundation

Coolify is an open-source, self-hostable PaaS alternative to Heroku, Vercel, and Netlify. It decouples the **Control Plane** from the **Data Plane**:

```
+-------------------------------------------------------------+
|                 Coolify Control Plane                       |
|   (Laravel 12 + Livewire 3 + Redis Horizon + Laravel Reverb)|
+-------------------------------------------------------------+
                               |
                   Secure SSH / Docker Socket
                               v
+-------------------------------------------------------------+
|              Data Plane (Local or Remote Server)            |
|   - Docker Engine / Swarm Daemon                            |
|   - Traefik v3 Dynamic Reverse Proxy (Auto Let's Encrypt)   |
|   - Nixpacks / Dockerfile Build Engines                     |
|   - Managed Application & Database Containers               |
+-------------------------------------------------------------+
```

### Core Invariants
1. **Sentinel ID `0`:** Coolify seeds instance-owned resources at ID `0` (`Team 0` = root team, `Server 0` = localhost host machine, `StandalonePostgresql 0` = Coolify internal DB, `InstanceSettings 0` = singleton settings). **Never alter or delete ID `0` records.**
2. **Dynamic Ingress:** Reverse proxying is automated via Traefik labels dynamically attached to containers.
3. **Multi-Server Management:** The control plane can orchestrate any remote Linux host over standard SSH keypairs without installing proprietary host agents.

---

## 2. Programmatic Python SDK & CLI Usage

The repository provides a deep-module SDK and CLI at `coolify_orchestrator.py` and `coolify_cli.py`.

### Quick CLI Commands

```bash
# Cluster summary and node telemetry
python coolify_cli.py info

# List all managed server nodes
python coolify_cli.py servers

# Search 350+ one-click pre-configured services
python coolify_cli.py catalog --search llm
python coolify_cli.py catalog --category database

# List registered applications and databases
python coolify_cli.py apps
python coolify_cli.py dbs

# Trigger automated zero-downtime deployment
python coolify_cli.py deploy <RESOURCE_UUID>

# Provision standard OMEGA autonomous cloud stack
python coolify_cli.py stack
```

### Python SDK Integration

```python
from coolify_orchestrator import CoolifyClient, CoolifyOrchestrator

# Initialize client (auto-detects LIVE or MOCK mode based on env vars)
client = CoolifyClient()
orchestrator = CoolifyOrchestrator(client)

# List servers and validate health
servers = client.list_servers()
validation = client.validate_server(servers[0]["uuid"])

# Deploy a Git repository application
app = client.create_application(
    name="my-web-app",
    git_repository="https://github.com/my-org/my-app",
    git_branch="main",
    build_pack="nixpacks",
    fqdn="https://app.mydomain.com",
    ports_exposes="3000"
)

# Trigger deployment and monitor
deployment = client.deploy(app["uuid"])
print(f"Deployment Queued: {deployment['deployment_uuid']}")

# Provision PostgreSQL or Redis
pg_db = client.create_database("postgresql", "app-primary-db")
redis_db = client.create_database("redis", "app-cache-redis")
```

---

## 3. Environment & Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `COOLIFY_BASE_URL` | Base HTTP endpoint of the Coolify instance | `http://localhost:8000` |
| `COOLIFY_API_TOKEN` | Sanctum Bearer token generated in Coolify Security UI | Empty (triggers Mock Mode) |
| `COOLIFY_MOCK` | Force offline high-fidelity simulation engine | `false` |
| `COOLIFY_TIMEOUT` | HTTP request timeout in seconds | `30` |

---

## 4. Local Deployment (Windows Docker Desktop)

To run Coolify locally on Windows:
1. Ensure Docker Desktop is running with WSL 2 backend.
2. Execute `START_COOLIFY_WINDOWS.bat` or `./scripts/start_coolify_windows.ps1`.
3. Open Mission Control at `http://localhost:8000`.
4. Open the interactive cockpit at `coolify_control_cockpit.html`.
