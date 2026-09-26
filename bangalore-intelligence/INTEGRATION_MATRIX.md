# INTEGRATION MATRIX & TOOL ORCHESTRATION ARCHITECTURE
**System:** Bangalore Market Intelligence & Career Ops Engine  
**Workstation:** `e:\anti` | Windows 11 Enterprise  
**Status:** Certified 100% Operational  

---

## 1. Complete Integration Architecture

```
                                  ┌───────────────────────────────┐
                                  │   ANTIGRAVITY AGENT ENGINE    │
                                  │  (Python 3.13 / Node v26.4)   │
                                  └──────────────┬────────────────┘
                                                 │
         ┌───────────────────────────────────────┼───────────────────────────────────────┐
         ▼                                       ▼                                       ▼
┌───────────────────┐                 ┌───────────────────────┐               ┌─────────────────────┐
│  MCP SERVER LAYER │                 │ BROWSER & SCRAPE CORE │               │ STORAGE & FTS5 CORE │
├───────────────────┤                 ├───────────────────────┤               ├─────────────────────┤
│ • filesystem      │                 │ • agent-browser (CDP) │               │ • SQLite3 Relational│
│ • firecrawl       │                 │ • Playwright Engine   │               │ • FTS5 Full-Text    │
│ • memory          │                 │ • Instant Data Scraper│               │ • CSV Master Ledgers│
│ • github          │                 │ • JobSpy Live Minework│               │ • OpenPyXL Spreadsh.│
│ • chrome-devtools │                 │ • Free HTTP Extractors│               │ • HTML Interactive │
└───────────────────┘                 └───────────────────────┘               └─────────────────────┘
```

---

## 2. Capability Dimension Matrix & Protocol Mapping

| Integration Layer | Current Tool / Engine | Protocol / Transport | Authentication Mode | Cost | Fallback Provider |
|:---|:---|:---|:---|:---:|:---|
| **Filesystem Operations** | Antigravity `filesystem` | Native OS File I/O | Local OS Process Rights | \$0.00 | Python `pathlib` / `os` |
| **Relational Database** | SQLite3 (`BANGALORE_APEX...`) | Embedded C Engine | File-level ACID Lock | \$0.00 | PostgreSQL / Neon MCP |
| **Search Engine** | SQLite FTS5 Virtual Index | Tokenized inverted index| In-Memory / Disk FTS5 | \$0.00 | Ripgrep `grep_search` |
| **Web Scraping (Fast)** | Firecrawl MCP & JobSpy | HTTP / Headless JSON | Free local library | \$0.00 | Python `requests` + `BeautifulSoup` |
| **Web Automation (Deep)**| `agent-browser` 0.38.1 | Chrome DevTools Protocol| Local Chromium instance| \$0.00 | Playwright CLI |
| **Job Market Sourcing** | `jobspy_market_scraper.py` | Multi-board scraper | Heuristic parsing | \$0.00 | Direct Careers Portal parsers |
| **Candidate Identity** | DSU BBA IB 2026 Grounding | Cryptographic Merkle hash| SHA-256 Block validation | \$0.00 | Immutable Markdown Ledgers |
| **Task Scheduling** | Antigravity Scheduler | Cron Daemon (`0 * * * *`)| Event-driven async loop | \$0.00 | Windows Task Scheduler |
| **Subagent Swarm** | `invoke_subagent` IPC | JSON-RPC Agent Pipeline | Memory-mapped messages | \$0.00 | Python multiprocessing |

---

## 3. Data Flow & Security Boundary

- **Inbound Data**: Public corporate directories, company career boards, BSE/NSE company filings, LinkedIn public directory queries, MCA company registry.
- **Data Hygiene Filter**: Strip personal mobile numbers, home addresses, and private personal communications. Only retain official corporate domain emails (`@company.com`) and office desk lines (`+91-80-XXXX-XXXX`).
- **Outbound Boundary**: Strictly blocked from sending emails, SMS, or LinkedIn automated connection requests without explicit human sign-off.
