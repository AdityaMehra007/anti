---
name: free-for-dev
description: Autonomous SDK, CLI, and operational standard for ripienaar/free-for-dev developer cloud catalog. Indexes 1,396+ free-tier developer services across 57 categories, synthesizes zero-dollar production stacks, conducts architecture feasibility audits, and calculates commercial cash savings.
---

# Free-For-Dev Autonomous Developer Cloud & Zero-Dollar Stack Skill

Autonomous standard operating procedure and deep orchestration SDK for the authoritative `ripienaar/free-for-dev` repository (https://github.com/ripienaar/free-for-dev).

## Architecture & Primitives

1. **Authoritative Knowledge Base & Multi-Engine Index**:
   - **Catalog Corpus**: Parsed from upstream markdown (`external/free-for-dev/README.md`) containing 1,396+ developer services across 57 categories.
   - **SQLite FTS5 Storage**: Pre-compiled SQLite database with full-text search (`data/free_for_dev.sqlite3`) for instant multi-term querying.
   - **Structured Catalog**: JSON store (`data/free_for_dev_catalog.json`) with enriched quota attributes, credit card flags, and inactivity sleep risk tags.

2. **Core Capabilities**:
   - **Zero-Dollar Stack Architect**: Synthesizes end-to-end production architecture stacks combining complementary developer free tiers that cost exactly **$0.00 / month** (e.g. Jamstack SaaS, AI Agent Platforms, Mobile Backends, Microservices).
   - **Commercial Value Equivalence**: Calculates the exact dollar replacement value (AWS/GCP/Azure equivalence) of free-tier quotas (typically $150–$600/month or $1,800–$7,200/year per stack).
   - **Architecture Feasibility Auditor**: Evaluates developer technical requirements (e.g., Postgres, Redis, Auth, Email, Logging) against free tiers and flags inactivity spin-down traps.
   - **Zero-Credit-Card Verification Protocol**: Filters and attests 1,384+ services offering friction-free access requiring zero financial credentials.
   - **Differential Head-to-Head Provider Comparison**: Evaluates 2 to 5 providers side-by-side across storage, bandwidth, request quotas, and sleeping policies.

3. **Model Context Protocol (MCP)**:
   - Exposes 9 autonomous tools over stdio JSON-RPC 2.0 (`free_for_dev_mcp_server.py`) for AI agents.

## Universal CLI Commands

```bash
# Display system telemetry and catalog statistics
python free_for_dev_cli.py info

# List all 57 capability categories
python free_for_dev_cli.py categories

# Search services with filters
python free_for_dev_cli.py search "postgres" --no-card
python free_for_dev_cli.py search "docker" --tier S

# Inspect a specific service dossier
python free_for_dev_cli.py service supabase
python free_for_dev_cli.py service cloudflare-workers

# Compare 2 to 5 providers head-to-head
python free_for_dev_cli.py compare supabase neon turso
python free_for_dev_cli.py compare vercel netlify cloudflare-pages

# Synthesize a zero-dollar production stack
python free_for_dev_cli.py stack --archetype jamstack_saas
python free_for_dev_cli.py stack --archetype ai_agent_platform
python free_for_dev_cli.py stack --archetype sovereign_no_card

# Audit project requirements against free tiers
python free_for_dev_cli.py audit --requirements "postgres,nextjs,auth,redis,sentry"

# Curated zero-credit-card offerings
python free_for_dev_cli.py no-card --limit 25

# Multi-format export
python free_for_dev_cli.py export --format json
python free_for_dev_cli.py export --format csv
python free_for_dev_cli.py export --format markdown

# Execute 12-phase sovereign lifecycle
python free_for_dev_cli.py do-everything
```

## REST API Endpoints (:8771)

- `GET  /api/telemetry` — Catalog metrics, quota totals, valuation
- `GET  /api/categories` — 57 capability classifications
- `GET  /api/services?search=...&no_card=true` — Multi-attribute search
- `GET  /api/services/{id}` — Deep service inspection
- `GET  /api/stacks/archetypes` — List of 7 production archetypes
- `GET  /api/stacks/{archetype}` — Synthesize zero-dollar stack
- `GET  /api/compare?ids=a,b,c` — Head-to-head provider evaluation
- `POST /api/audit` — Architecture feasibility audit
- `POST /api/do-everything` — 12-phase sovereign lifecycle
- `GET  /` or `/cockpit` — Interactive Mission Control Cockpit

## Operational Launchers

- `START_FREE_FOR_DEV_WINDOWS.bat` — Starts API server and opens Cockpit
- `START_FREE_FOR_DEV_COCKPIT.bat` — Direct browser launch of Cockpit
- `scripts/start_free_for_dev_windows.ps1` — PowerShell native launcher
