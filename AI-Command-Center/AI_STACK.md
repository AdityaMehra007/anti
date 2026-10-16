# AI STACK ARCHITECTURE & TOOL ROLES

**Document ID:** `STACK-OMNI-2026-10-16`  
**System:** Google Antigravity Workstation Command Center  
**Design Principle:** High Leverage, Zero-Waste, Resource-Aware, Evidence-Driven  

---

## 1. Architectural Philosophy: The Lean Tiered Stack

An AI workstation must maximize productivity while respecting hardware realities. Rather than accumulating redundant tools and memory-hogging daemons, this architecture establishes clear separation of concerns across 5 distinct layers:

```
[Layer 1: Orchestration & Deep Reasoning] (Cloud: Google Antigravity + Gemini 2.5/Flash/Pro)
                          │
[Layer 2: Local Processing & Privacy]   (Local: Ollama on GTX 960M, models <= 3B params)
                          │
[Layer 3: Execution & Tooling]           (Local CLI, Python 3.13, Node 26, Git, gh CLI)
                          │
[Layer 4: Data & State Persistence]      (Local: SQLite ACID DB, JSONL Event Logs)
                          │
[Layer 5: Presentation & Public Proof]   (Angular 21 Portfolio, GitHub Repositories)
```

---

## 2. Layer-by-Layer Taxonomy & Tool Roles

### Layer 1: Primary Orchestration & Analytical Reasoning
- **Primary Tool:** Google Antigravity (Powered by Gemini models: Flash for velocity, Pro for complex architectural planning).
- **Core Responsibilities:**
  - Codebase analysis, refactoring, and multi-file code editing.
  - Autonomous multi-agent coordination with isolated context windows.
  - Web research, job requirement parsing, and strategic document synthesis.
  - Automated test execution and defect remediation.
- **Resource Footprint on Laptop:** Near-zero CPU/RAM/VRAM consumption. Operations occur through cloud API endpoints.

### Layer 2: Local AI & Offline Privacy Layer
- **Primary Tool:** Ollama (`E:\anti gravity\Tools\Ollama\ollama.EXE`).
- **Hardware Boundary:**
  - Dedicated VRAM: 4.0 GB (GTX 960M, Maxwell Compute 5.0).
  - Available System RAM: ~3.67 GB.
  - **Selected Model Parameter Class:** Strictly $\le 3$B parameters with Q4_K_M quantization (e.g. `llama3.2:1b`, `llama3.2:3b`, `qwen2.5:1.5b`).
- **Storage Rule:** All model weights must be stored on `E:\anti gravity\Tools\Ollama\models` via environment variable `OLLAMA_MODELS`, safeguarding the 26 GB `C:\` SSD partition.
- **Primary Use Cases:**
  - Private PII scrubbing (anonymizing resumes and contacts before external transmission).
  - Offline text normalization, JSON formatting, and keyword extraction.
  - Low-latency local autocomplete or terminal command generation.

### Layer 3: Execution, Automation & Development Tooling
- **Runtimes:**
  - **Python 3.13.15:** Core language for automation scripts, scrapers, scoring algorithms, and database interfaces.
  - **Node.js v26.4.0 & npm 11.17.0:** Frontend builds, Angular SSR serving, and web applications.
  - **Git 2.54.0 & GitHub CLI 2.95.0:** Deterministic version control, issue tracking, and repository synchronization.
  - **Docker 29.6.1:** Available on-demand for containerized microservices (used sparingly to preserve RAM).

### Layer 4: Data & State Persistence
- **Primary Storage:** SQLite 3 (`career_vault.db`).
  - **Why SQLite:** Zero memory overhead, zero daemon process, single-file portability, ACID compliance, and sub-millisecond query performance.
  - **Schema:** Relational tables for Job Postings, Companies, Applications, Interactions, and Evidence Records.
  - **Deduplication:** Unique constraints on `job_id` and normalized `url` strings prevent redundant entries.
- **Secondary State:** JSON / Markdown records for human-readable audit trails and Git diff transparency.

### Layer 5: Public Proof & Portfolio Distribution
- **Personal Portfolio:** `https://adi-digital-universe.ai.studio/` (Live Angular 21 + SSR showcase).
- **Code Repositories:** `https://github.com/AdityaMehra007` (Public proof of engineering capability and enterprise projects).

---

## 3. Tool Evaluation & Selection Matrix

| Candidate Tool | Evaluation | Decision | Rationale |
| :--- | :--- | :---: | :--- |
| **Google Antigravity** | Native agentic paired-programming with terminal & file execution | **ADOPT (Primary)** | Highest leverage; native tool execution; zero RAM load. |
| **Google Gemini (API / Studio)** | Long-context multimodal reasoning (up to 1M–2M tokens) | **ADOPT (Primary)** | Essential for analyzing entire company portfolios and job boards. |
| **Ollama (Local)** | Self-hosted local inference | **ADOPT (Constrained)** | Use for $\le 3$B models only. Launch on-demand. Store models on `E:\`. |
| **Heavy 7B/14B Local Models** | Requires 6GB–10GB VRAM or 12GB+ system RAM | **REJECT** | GTX 960M has 4GB VRAM; system RAM has 3.67GB free. High risk of OOM. |
| **n8n / Make / Zapier** | Workflow automation platforms | **EVALUATE / SELECTIVE** | Use Python scripts for core jobs; keep n8n as optional UI for complex multi-app webhooks. |
| **Supabase** | Managed PostgreSQL + Auth + Storage | **ADOPT (Cloud Sync)** | Ideal for syncing mobile/web client data without local DB overhead. |
| **Docker** | Container virtualization | **ON-DEMAND ONLY** | Running multiple containers consumes 2GB–4GB RAM; run only when testing production builds. |

---

## 4. Cost Governance & Resource Safeguards

1. **Financial Budget:** ₹0 initial outlay. Leverage free tiers of Google AI Studio, GitHub, Vercel, and local open-source software.
2. **Disk Budget:** 0 MB writes to `C:\` for data or models; 100% allocation on `E:\`.
3. **RAM Threshold:** Maintain at least 2.5 GB of free system memory at all times. Terminate idle background processes before starting memory-intensive builds.
