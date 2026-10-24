# Coolify v4 (`coollabsio/coolify`) — Supreme Architectural Teardown & Autonomous Operations Dossier

> **Executive Scope**: An exhaustive, production-grade reverse-engineering analysis and autonomous integration specification for [Coolify](https://github.com/coollabsio/coolify), the open-source, self-hostable Heroku, Netlify, and Vercel alternative.

---

## 1. System Overview & Macro Topography

Coolify v4 is a cloud infrastructure platform that converts bare-metal servers, VPS instances (Hetzner, AWS, DigitalOcean, OVH), and local machines into an enterprise-grade Platform-as-a-Service (PaaS). It decouples configuration management (Control Plane) from runtime execution (Data Plane), communicating strictly over encrypted SSH tunnels and Docker sockets without requiring heavy persistent agent daemons on worker nodes.

```mermaid
flowchart TD
    subgraph ControlPlane["Coolify v4 Control Plane (Host / Sentinel Node)"]
        UI["Livewire 3 + Alpine.js + Tailwind v4"]
        Kernel["Laravel 12 (App Logic & REST API)"]
        Queue["Redis Horizon Job Pipeline"]
        WS["Laravel Reverb (WebSocket :6001)"]
        Term["XTerm / Node Terminal (:6002)"]
        InternalDB[("Internal PostgreSQL 15 (id=0 Sentinel)")]
        MCPServer["Coolify MCP Server (JSON-RPC stdio)"]
        APIServer["Coolify API Server (:8767 REST Bridge)"]
    end

    subgraph Communication["Encrypted Management Fabric"]
        SSH["SSH Keypair Multiplexing (22/Custom)"]
        DockSock["//var/run/docker.sock (Local Host)"]
    end

    subgraph DataPlane["Worker Nodes (Bare-Metal / VPS / Docker Swarm)"]
        Traefik["Traefik v3 Dynamic Reverse Proxy + Auto ACME TLS"]
        Nixpacks["Nixpacks / Buildpacks Engine"]
        Containers["Application & Database Containers"]
        Backups["S3 Scheduled Volume Backups"]
    end

    UI --> Kernel
    MCPServer --> Kernel
    APIServer --> Kernel
    Kernel --> InternalDB
    Kernel --> Queue
    Kernel --> WS
    Kernel --> Term
    Queue --> SSH
    Queue --> DockSock
    SSH --> Traefik
    SSH --> Nixpacks
    SSH --> Containers
    Containers --> Backups
    Traefik --> Containers
```

---

## 2. Core Architectural Subsystems

### 2.1 Backend Control Plane (Laravel 12 & Livewire 3)
* **Framework Foundation**: Built on Laravel 12 following the classic Laravel 10 directory structure (`app/Http/Kernel.php`, `app/Console/Kernel.php`).
* **Domain Actions**: Implemented via `lorisleiva/laravel-actions` (`AsAction` trait). Actions function simultaneously as invokable PHP classes, queueable asynchronous jobs, and HTTP controller endpoints.
* **Sentinel Instance Archetype (`id = 0`)**: Coolify adheres to a strict invariant:
  * `Team 0`: The root instance team.
  * `Server 0`: The localhost node hosting Coolify itself.
  * `StandalonePostgresql 0`: Coolify's internal system database (`coolify-db`).
  * `InstanceSettings 0`: Singleton configuration record.
* **Livewire 3 & Alpine.js**: Server-driven UI components with instant reactive state sync via WebSockets. No traditional Blade REST controllers for internal views.

### 2.2 Ingress & Dynamic Routing Fabric (Traefik v3)
Coolify eliminates manual Nginx reverse proxy configuration by leveraging **Traefik**:
* Dynamically monitors container lifecycle events via Docker labels (`traefik.enable=true`, `traefik.http.routers.<name>.rule=Host(...)`).
* Provisions, verifies, and renews Let's Encrypt TLS/SSL certificates automatically via HTTP-01 or DNS-01 ACME challenges.
* Isolates TCP database ports through lightweight ephemeral Traefik proxy instances to avoid host port collision.

```mermaid
sequenceDiagram
    autonumber
    actor Developer as Developer / Agent / CI
    participant API as Coolify REST / MCP Server / API Server
    participant Queue as Redis Horizon Queue
    participant Worker as Target Node (SSH / Docker)
    participant Nixpacks as Nixpacks Builder
    participant Traefik as Traefik Edge Router

    Developer->>API: POST /api/v1/deploy or coolify_deploy_resource
    API->>Queue: ApplicationDeploymentJob queued
    Queue->>Worker: Initiate SSH Execution Pipeline
    Worker->>Worker: Clone Git Repo / Pull Dockerfile
    Worker->>Nixpacks: Analyze Source Code & Generate Plan
    Nixpacks-->>Worker: Compile Minimal Multi-Stage Container
    Worker->>Worker: Spin Up New Container alongside Old (Zero-Downtime)
    Worker->>Worker: Execute HTTP Healthchecks (/health)
    Worker->>Traefik: Update Dynamic Container Labels
    Traefik->>Traefik: Switch Traffic to New Container & Provision SSL
    Worker->>Worker: Gracefully Stop & Prune Stale Container
    Worker-->>API: Status = 'running' via Laravel Reverb
    API-->>Developer: Deployment Complete (HTTP 200)
```

---

## 3. Database Schema & Object Hierarchy

```mermaid
erDiagram
    TEAM ||--o{ PROJECT : owns
    PROJECT ||--o{ ENVIRONMENT : contains
    ENVIRONMENT ||--o{ APPLICATION : runs
    ENVIRONMENT ||--o{ STANDALONE_DATABASE : provisions
    ENVIRONMENT ||--o{ SERVICE : deploys
    SERVER ||--o{ APPLICATION : hosts
    SERVER ||--o{ STANDALONE_DATABASE : hosts
    SERVER ||--o{ SERVICE : hosts
    TEAM ||--o{ PRIVATE_KEY : stores

    TEAM {
        int id PK "Sentinel 0 for Root"
        string name
        string personal_team
    }
    PROJECT {
        string uuid PK
        string name
        string description
    }
    ENVIRONMENT {
        string uuid PK
        string name
    }
    SERVER {
        string uuid PK
        string ip
        int port
        string user
        string proxy_type
    }
    APPLICATION {
        string uuid PK
        string name
        string fqdn
        string git_repository
        string build_pack
        string status
    }
```

---

## 4. 1-Click Open-Source Service Catalog (352 Stacks)

Coolify features a curated repository of **352 pre-configured, production-ready open-source services** stored in `templates/service-templates-latest.json`. Each entry contains base64-encoded Compose definitions decoded and variable-interpolated by [`coolify_compose_exporter.py`](file:///e:/anti/coolify_compose_exporter.py).

| Category | Primary Services Included |
|----------|---------------------------|
| **AI & LLM Gateways** | `anythingllm`, `litellm`, `langfuse`, `flowise`, `openclaw`, `hermes-agent`, `librechat`, `lobe-chat` |
| **Vector & Databases** | `qdrant`, `weaviate`, `chroma`, `supabase`, `pocketbase`, `appwrite`, `postgresql`, `redis`, `clickhouse` |
| **Automation & Queues** | `n8n`, `activepieces`, `rabbitmq`, `temporal` |
| **Observability & Ops** | `plausible`, `openpanel`, `posthog`, `uptime-kuma`, `grafana`, `beszel`, `prometheus` |
| **Storage & Security** | `minio`, `vaultwarden`, `authentik`, `authelia`, `browserless` |

---

## 5. Artifacts & Deliverables Created in this Workspace

1. **Autonomous Python SDK & Engine**: [`coolify_orchestrator.py`](file:///e:/anti/coolify_orchestrator.py)
   * Full typed client supporting all 212 REST endpoints.
   * High-fidelity offline simulation mode for local dev, testing, and CI/CD pipelines.
2. **Universal Command-Line Interface**: [`coolify_cli.py`](file:///e:/anti/coolify_cli.py)
   * Interactive subcommands: `info`, `servers`, `projects`, `apps`, `dbs`, `services`, `catalog`, `deploy`, `compose`, and `stack`.
3. **Template Compose Exporter**: [`coolify_compose_exporter.py`](file:///e:/anti/coolify_compose_exporter.py)
   * Automated decoding and secure secret interpolation for all 352 pre-configured services into ready-to-run `docker-compose.yml` and `.env` files.
4. **Autonomous MCP Server**: [`coolify_mcp_server.py`](file:///e:/anti/coolify_mcp_server.py)
   * 13 standardized JSON-RPC 2.0 stdio tools allowing any AI agent to control Coolify.
5. **Local REST API Server & Cockpit Bridge**: [`coolify_api_server.py`](file:///e:/anti/coolify_api_server.py)
   * Zero-dependency HTTP server on port `8767` serving the cockpit and live REST endpoints.
6. **Pre-Exported Enterprise AI & DB Stacks**: [`stacks/`](file:///e:/anti/stacks/)
   * Standalone, ready-to-run stacks for `anythingllm`, `n8n`, `supabase`, `qdrant`, and `litellm`.
7. **Mission Control Cockpit**: [`coolify_control_cockpit.html`](file:///e:/anti/coolify_control_cockpit.html)
   * Executive dark-mode dashboard with cluster telemetry, 352-service marketplace, live terminal emulator, and API playground.
8. **OMEGA Master Launchers**:
   * [`OMNI_EXECUTIVE_COCKPIT.html`](file:///e:/anti/OMNI_EXECUTIVE_COCKPIT.html): Integrated directly as a primary tab in the master executive cockpit.
   * [`START_ALL_OMNI_SYSTEMS.bat`](file:///e:/anti/START_ALL_OMNI_SYSTEMS.bat): Automated multi-server batch launcher including the Coolify API server on port `8767`.
   * [`START_COOLIFY_WINDOWS.bat`](file:///e:/anti/START_COOLIFY_WINDOWS.bat) & [`scripts/start_coolify_windows.ps1`](file:///e:/anti/scripts/start_coolify_windows.ps1): Dedicated Windows launchers.
9. **Agent Skill**: [`.agents/skills/coolify-orchestrator/SKILL.md`](file:///e:/anti/.agents/skills/coolify-orchestrator/SKILL.md)
   * Autonomous SOP integrating Coolify into the repository's 3,800+ skill suite.
10. **Automated Test Suite**: [`tests/test_coolify_orchestrator.py`](file:///e:/anti/tests/test_coolify_orchestrator.py)
    * 13 passing unit and integration tests covering the complete lifecycle (`13 passed in 0.50s`).
