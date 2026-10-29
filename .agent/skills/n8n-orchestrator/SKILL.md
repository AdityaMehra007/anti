---
name: n8n-orchestrator
description: "Use when orchestrating, executing, or managing distributed workflows, node DAGs, and autonomous agents via n8n. Triggers: multi-step workflow graphs, 560+ core and community nodes, LangChain AI agent reasoning loops, inbound webhook ingress, cron schedules, dropzone file processing, AES-256 credential management, and disaster recovery exports."
metadata:
  author: OMEGA Autonomous Core
  version: "2.0.0"
---

# n8n Autonomous Orchestrator

Autonomous standard operating procedure and programmatic interface for managing, executing, and monitoring fair-code workflow automation, event-driven node DAGs, and LangChain AI agent reasoning using n8n (https://github.com/n8n-io/n8n).

## 1. Architectural Foundation

n8n is an enterprise-grade, fair-code workflow automation platform with native AI agent integration. It unifies:
1. **560+ Pre-Built Integrations**: First-party nodes for databases (Postgres, MongoDB, Redis), cloud providers (AWS, GCP, Azure), enterprise SaaS (Slack, GitHub, Jira, Stripe, HubSpot), and core utilities.
2. **LangChain AI Ecosystem**: Native multi-agent loops, conversation memory windows, vector stores, and tool connectors (@n8n/n8n-nodes-langchain).
3. **Event-Driven & Polling Ingress**: High-throughput webhooks, recurring cron schedules, error triggers, sub-workflow executions, and dropzone file ingestion.

```
+--------------------------------------------------------------------------+
|                        n8n Web UI & Control Plane                        |
|                  (Vue.js 3 Frontend + TypeScript Core)                   |
+--------------------------------------------------------------------------+
                                    |
                    REST API (/api/v1/...) / Webhooks
                                    v
+--------------------------------------------------------------------------+
|                         n8n Node Execution Engine                        |
|   - Directed Graph Traversal & Topological Branching                     |
|   - VM2 / Node.js Isolated Sandbox Execution                             |
|   - Redis & BullMQ Queue Mode (Multi-Instance Scaling)                   |
+--------------------------------------------------------------------------+
                                    |
                    Node & State Persistence Layer
                                    v
+--------------------------------------------------------------------------+
|                  PostgreSQL / SQLite Arsenal Database                    |
|   - 560+ Core Nodes Catalog (FTS5 Full-Text Search)                      |
|   - 14 OMEGA Production Workflow DAGs                                    |
|   - AES-256-GCM Encrypted Credentials Vault                              |
|   - Execution History & Per-Node Audit Trails                            |
+--------------------------------------------------------------------------+
```

### Core Invariants
1. **Topological Node Traversal:** Every node receives data as arrays of JSON objects (`[{ "json": { ... } }]`), executes transformations or API calls, and emits data to downstream branch connections.
2. **LangChain Autonomous Reasoning:** AI Agent nodes dynamically plan, select tools from connected tool nodes, consult memory buffers, and emit structured outputs.
3. **Zero-Loss Webhook Processing:** Production and test webhooks validate routing, parse payloads, and spawn tracked executions immediately.
4. **Dual Execution Runtime:** Works seamlessly against a live running n8n instance (port 5678 / 8771) or the high-fidelity offline Python simulation engine when running in air-gapped or CI/CD test environments.

---

## 2. Programmatic Python SDK & CLI Usage

The repository provides a deep-module SDK and CLI at `n8n_orchestrator.py` and `n8n_cli.py`.

### Quick CLI Commands

```bash
# Platform summary, worker nodes, and queue telemetry
python n8n_cli.py info

# Search 560+ core nodes via SQLite FTS5
python n8n_cli.py search "webhook" --limit 5
python n8n_cli.py search "langchain" --limit 5
python n8n_cli.py search "postgres" --limit 5

# List registered production workflows
python n8n_cli.py workflows

# Execute a workflow DAG with custom input payload
python n8n_cli.py run-workflow outreach_dispatcher --data '{"recipient": "lead@tier1.com", "action": "OUTREACH"}'

# Dispatch inbound webhook
python n8n_cli.py trigger outreach-dispatch --data '{"event": "lead_intake", "company": "Fortune500"}'

# Run LangChain Autonomous Agent reasoning node
python n8n_cli.py ai-agent "Assess cross-border trade compliance requirements for EU CBAM 2026."

# List execution history
python n8n_cli.py executions --limit 10

# Audit encrypted credentials in vault
python n8n_cli.py credentials

# Ingest dropzone files
python n8n_cli.py dropzone

# Export workflows to backup folder
python n8n_cli.py export --dir n8n/backups

# Execute end-to-end 12-Phase Sovereign Lifecycle
python n8n_cli.py do-everything

# Launch local REST API server and Mission Control Cockpit
python n8n_cli.py serve --port 8771
```

### Programmatic Python SDK Usage

```python
from n8n_orchestrator import N8nClient, N8nOrchestrator, N8nConfig

# Initialize client (auto-detects live n8n on port 5678 or uses mock engine)
client = N8nClient(N8nConfig(mock_mode=False))

# Health check & telemetry
telemetry = client.get_telemetry()
print(f"n8n version: {telemetry['version']} | Nodes: {telemetry['nodes_catalog_count']}")

# Search nodes via FTS5
nodes = client.search_nodes("langchain", limit=5)
for n in nodes:
    print(f"Node: {n['displayName']} [{n['name']}] ({n['group']})")

# Execute production workflow DAG
result = client.execute_workflow(
    "ai_agent_researcher",
    input_data={"chatInput": "Research top 10 GCC hubs in Bangalore"}
)
print(f"Execution ID: {result['id']} | Status: {result['status']}")

# Dispatch webhook
wh = client.trigger_webhook("outreach-dispatch", {"lead_id": "LD-9901", "channel": "email"})
print(f"Webhook result: {wh['status']}")

# Run 12-Phase Sovereign Lifecycle verification
orchestrator = N8nOrchestrator(client)
manifest = orchestrator.do_everything()
print(f"Manifest Generated: {manifest['execution_id']} | Status: {manifest['status']}")
```

---

## 3. Mission Control Cockpit & API Server

- **Web Cockpit**: `n8n_control_cockpit.html` (Interactive dark cyber-glass UI with 10 operational tabs).
- **REST API Server**: `n8n_api_server.py` on port `8771`.
- **One-Click Launchers**:
  - `START_N8N_COCKPIT.bat`: Launches API server and opens the browser cockpit.
  - `START_N8N.bat`: Launches containerized n8n engine on port `5678`.

---

## 4. MCP Tools Integration

The Model Context Protocol server at `n8n_mcp_server.py` exposes 15 tools to Antigravity and Claude agents:
- `n8n_get_system_info`
- `n8n_search_nodes`
- `n8n_list_nodes_by_group`
- `n8n_get_node_details`
- `n8n_list_workflows`
- `n8n_get_workflow`
- `n8n_execute_workflow`
- `n8n_trigger_webhook`
- `n8n_run_ai_agent`
- `n8n_list_executions`
- `n8n_get_execution`
- `n8n_list_credentials`
- `n8n_scan_dropzone`
- `n8n_export_workflows`
- `n8n_do_everything_lifecycle`
