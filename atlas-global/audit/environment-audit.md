# ATLAS-GLOBAL: ANTIGRAVITY ENVIRONMENT & CAPABILITY AUDIT
**Project Code:** ATLAS-GLOBAL  
**System Architecture:** Antigravity Global Business & Workforce Intelligence OS  
**Audit Scope:** Full Machine, Runtime, MCP, Browser, Skills, and Connectors  
**Workstation:** `e:\anti\atlas-global` | Windows 11 Enterprise (AMD64)  
**Execution Timestamp:** 2026-09-20T16:56:30+05:30  

---

## 1. Executive Summary

This environment audit establishes the foundational operational capabilities for **ATLAS-GLOBAL**, a modular, continuously improving public-data business and workforce intelligence platform. The immediate focus is **Bengaluru (Priority #1)**, followed by **India (Priority #2)** and **Global Scale (Priority #3)**.

---

## 2. Comprehensive System Capabilities Audit

### A. Compute, Shell & Core Runtimes
- **Operating System:** Windows 11 Enterprise (x86_64 / AMD64)
- **Primary Shell:** PowerShell (Windows Terminal environment)
- **Python Runtime:** Python **3.13.15** (`C:\Users\amehr\AppData\Local\Programs\Python\Python313\python.exe`)
  - Installed Core Modules: `sqlite3`, `json`, `csv`, `requests`, `pathlib`, `hashlib`, `re`, `datetime`, `openpyxl`, `pytest`
- **Node.js Runtime:** Node.js **v26.4.0** (`C:\Program Files\nodejs\node.exe`)
  - Package Managers: `npm` (v11.17.0), `npx` (v11.17.0)
- **Version Control:** Git version 2.47+ installed and active across `e:\anti`

### B. Registered MCP Servers (20 Active)
Located in `C:\Users\amehr\.gemini\antigravity\mcp\`:
1. `filesystem`: Fast local workspace read/write/edit/search
2. `firecrawl`: Headless web crawling and structured markdown extraction
3. `firecrawl-hosted`: Hosted Firecrawl scraper
4. `github`: Repository, pull request, code inspection, and release tracking
5. `memory`: Knowledge graph entity and relationship persistence
6. `chrome-devtools-mcp`: 29 native Chrome DevTools Protocol (CDP) interaction tools
7. `cloudrun`: Google Cloud Run deployment and management
8. `firebase-mcp-server`: Google Firebase database and auth backend
9. `gmp-code-assist`: Google Cloud Code Assistant
10. `mcp-server-neon`: Serverless PostgreSQL engine
11. `notion`: Notion workspace and documentation syncing
12. `ponytail`: Senior developer minimalist optimization and bloat auditing
13. `prisma-mcp-server`: Relational schema generation and ORM
14. `sequential-thinking`: Dynamic multi-step reasoning protocol
15. `slack`: Slack messaging and team notification ops
16. `brave-search`: Privacy-preserving web search
17. `camofox`: Resilient browser scraping agent
18. `career-ops`: Candidate resume, application, and tracking engine
19. `arize-tracing-assistant`: LLM observability and evaluation tracing
20. `agent-skills`: Dynamic agent skill loader and orchestrator

### C. Browser & Web Automation Stack
- **Native Chrome DevTools Protocol (`chrome-devtools-mcp`):** 29 tools (`navigate_page`, `click`, `fill`, `evaluate_script`, `take_screenshot`, `performance_start_trace`, etc.).
- **`agent-browser` 0.38.1:** High-speed native Rust CLI via `npx agent-browser` with compact accessibility-tree snapshots and `@eN` element refs.
- **Firecrawl Engine:** Markdown converter and search extractor.
- **Installed Chrome Extensions:**
  1. `Instant Data Scraper` (`ofaokhiedipichpaobibbnahnkdoiiah`, v1.2.1) — In-browser heuristic table extractor.
  2. `Google Docs Offline` (`ghbmnnjooekpmoecnnnilnnbdlolhkhi`, v1.104.1).
  3. `Touch VPN` (`bihmplhobchoageeokmgbdihknkjbknd`, v5.0.18).
  4. `Google Pay / In-App Payments` (`nmmhkkegccagdldgiimedpiccmgmieda`, v1.0.0.6).
  5. `Code Geass Theme` (`jkinegociokldddjmcpmgpmgklfkploa`, v1.3.3).

### D. Google Workspace & Cloud Connectors
- **Google Cloud Run / Firebase:** Configured via MCP.
- **Google Search:** Native Antigravity search (`search_web`), Firecrawl search (`firecrawl_search`), and Google Jobs scraping via JobSpy.
- **Google Drive & Sheets:** Direct OAuth API token not configured in `.env`.
  - *Legitimate Free Alternative:* Python `openpyxl` / `csv` workbooks + offline standalone interactive HTML dashboards (`ADITYA_CAREER_INTELLIGENCE_COCKPIT.html`).

### E. Storage & Database Engines
- **Relational Engine:** SQLite3 with **FTS5 (Full-Text Search)** virtual tables.
- **Existing Master Database:** `BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite` (12,213 indexed records).
- **Parquet / CSV / JSON:** Native filesystem support across `e:\anti\atlas-global\data\`.

### F. Scheduling & Autonomous Loops
- **Scheduler:** Antigravity reactive Cron scheduler (`schedule` tool) running background daemon `task-737` (`0 * * * *`).
- **OS Fallback:** Windows Task Scheduler (`schtasks`).

### G. Multi-Agent & Parallel Subagent Capabilities
- **Orchestration:** `invoke_subagent`, `define_subagent`, `manage_subagents` with memory-mapped inter-agent messaging (`send_message`).

---

## 3. Policy & Guardrail Enforcement

1. **Zero Cold Calling & Zero Outbound Messages:** No emails, LinkedIn messages, or job applications are ever sent automatically.
2. **Zero Private Personal Data:** Only publicly published corporate desk phones (`+91-80-XXXX-XXXX`), corporate domain emails (`@company.com`), office addresses, and official requisitions are stored.
3. **Zero Financial Cost:** 100% free, open-source, or public data sources only. No subscriptions or trials.
