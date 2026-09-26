# ANTIGRAVITY OMNIVERSE: UNIVERSAL CONNECTOR BUS SPECIFICATION
## Document ID: `OMNIVERSE-04-CONN` | Status: APPROVED | Mode: OMNI-X PRODUCTION

---

## 1. Universal Connector Architecture

The Omniverse Connector Bus decouples agents from specific vendor SDKs, protocols, or execution surfaces. Every external system, database, protocol, or cloud service connects through an immutable standardized interface:

- **MCP Connectors**: Firecrawl, GitHub, Filesystem, Memory Graph.
- **Native Execution**: PowerShell, Bash/WSL2, Pytest/CLI, Tools 300 Library.
- **Browser Automation**: Camofox (Port 9377), Playwright, Headless DOM.
- **Data & DB Connectors**: SQLite WAL, PostgreSQL, Chroma Vector, JSONL Memory.

---

## 2. Standard Connector Registration Schema

Every connector must implement and register the contract:
- `connector_id`: Unique identifier
- `name`: Interface name
- `provider`: Underlying provider/protocol
- `capabilities`: Supported actions
- `authentication`: Secret reference without prompt exposure
- `permissions`: Read/write boundaries
- `rate_limits`: Request & concurrency limits
- `cost_profile`: Dollar cost tracking
- `security`: Input sanitization, SSRF defense
- `audit_policy`: Trace logging
- `failure_behavior`: Retry backoff and fallback connector

---

## 3. Core Connector Registry (Workspace Baseline)

- `CONN-FS-01`: `filesystem_bus` (MCP Lazy)
- `CONN-FC-01`: `firecrawl_bus` (MCP Lazy)
- `CONN-GH-01`: `github_bus` (MCP Lazy)
- `CONN-MEM-01`: `memory_graph_bus` (MCP Lazy)
- `CONN-CAM-01`: `camofox_browser` (Port 9377)
- `CONN-SQL-01`: `sqlite_wal_bus` (Platform DB, Ledger DB, Approvals DB)
- `CONN-T300-01`: `tools_300_bus` (300 Specialist Tools)

---

## 4. Secret Isolation & Prompt-Leak Defense

1. **Zero Secret Printing**: API keys, session tokens, and passwords are never returned in tool call results or stored in markdown artifacts.
2. **Environment Sanitization**: Connectors inject credentials at the transport layer directly, preventing LLM context leakage.
3. **SSRF Hardening**: Web scrape connectors validate target hosts, blocking loopback addresses, local network IPs, and cloud metadata endpoints.
