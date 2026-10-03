# ⚖️ STACK EVALUATION & TECHNOLOGY SELECTION: ANTIGRAVITY OMEGA

**Evaluation Criteria**: Architectural depth, hardware footprint (16GB RAM / 4GB VRAM constraint), replaceability, local-first viability, and maintenance overhead.  
**Guiding Law**: *Ponytail Minimalism — "The best code is the code you never wrote. Stop at the first rung of The Ladder."*

---

## 1. Local AI & Inference Engines

| Candidate | Architecture | RAM/VRAM Requirement | Suitability for GTX 960M / 16GB RAM | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ollama** | Native Go + C++ (llama.cpp) | **~1.5 - 2.5 GB VRAM** (for 3B models) | **EXCELLENT** | **SELECTED (CORE)** | Already installed on `E:`. OpenAI API compatible. Supports cuBLAS & Vulkan for Maxwell GPUs. Minimal idle RAM (<60MB). |
| **Open WebUI** | Python + Svelte (Docker) | ~800MB RAM | GOOD | **OPTIONAL (WAVE 2)** | Excellent UI for Ollama, but adds container overhead. Can run on-demand or use lightweight React/Next.js dashboard. |
| **LM Studio** | Electron + llama.cpp | ~1.2 GB RAM (Electron overhead) | MODERATE | **REJECTED** | Redundant with Ollama. High Electron RAM footprint. GUI-only workflow. |
| **LocalAI** | Go + multi-backend | ~1.5 GB RAM | MODERATE | **REJECTED** | Heavier configuration than Ollama without additional benefit for GGUF. |
| **Dify / Flowise** | Multi-container microservices | 3.5 - 5.0 GB RAM | POOR (High RAM pressure) | **ON-DEMAND (WAVE 2)** | Powerful visual workflow builder, but running 5+ containers constantly would starve the 2.5GB free host RAM. |
| **Aider / OpenHands** | Python / Node CLI & Canvas | ~400MB - 1GB RAM | GOOD | **SELECTED (AGENTIC)** | Aider runs natively in terminal. OpenHands canvas already partially active on port 3001/8000. |

---

## 2. Automation & Workflow Orchestration

| Candidate | Architecture | Idle Footprint | Integration Capabilities | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **n8n** | Node.js (SQLite / Postgres) | **~250 - 400 MB RAM** | 400+ nodes, webhooks, custom Python/JS | **SELECTED (CORE)** | Industry standard. Can run natively via Node/npx on Windows without Docker, or inside a lean container. Already has starter scripts in `e:\anti\n8n`. |
| **Activepieces** | TypeScript / Node | ~350 MB RAM | Good visual nodes | **RESERVE** | Good alternative, but smaller ecosystem than n8n. |
| **Windmill** | Rust + Python + Go | ~300 MB RAM | High-code developer scripts | **WAVE 2 CANDIDATE** | Outstanding for intensive script automation, but requires Postgres & multiple workers. |
| **Temporal / Airflow** | Heavy Java / Python distributed | 2.5 - 6.0 GB RAM | Enterprise distributed DAGs | **REJECTED** | Massive overkill for personal workstation; would exhaust host memory immediately. |

---

## 3. Database Architecture & Vector Engines

| Subsystem | Candidate | Footprint | Evaluation | Selection Decision |
| :--- | :--- | :--- | :--- | :--- |
| **Relational Primary** | **SQLite (WAL Mode)** | **< 15 MB RAM** | Zero-daemon, instant query, ACID, single file on `E:`, zero memory leak risk. | **SELECTED (RING 0 CORE)** |
| **Relational Enterprise**| **PostgreSQL** | ~80 - 150 MB RAM | Standard relational engine for multi-user services & n8n. | **SELECTED (ON-DEMAND / DOCKER)** |
| **Vector Engine** | **Qdrant** | **~80 - 150 MB RAM** | Written in Rust. Fast HNSW index. Single binary or lightweight container. Memory-mapped files. | **SELECTED (PRIMARY VECTOR)** |
| **Vector Alternative** | Chroma | ~200 MB RAM | Python-based. Easy to embed, but higher memory footprint than Qdrant. | **FALLBACK** |
| **Key-Value Cache** | **Valkey / Redis** | **~30 MB RAM** | In-memory pub/sub and state caching. | **SELECTED (ON-DEMAND)** |

---

## 4. Knowledge Management & Document Systems

| Candidate | Architecture | Footprint | Capabilities | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Paperless-ngx** | Python / Django + Celery + OCR | ~600MB - 1.2GB RAM | Automated OCR, document tagging, PDF search | **SELECTED (WAVE 2 ON-DEMAND)** | The premier open-source document vault. Run on-demand when batch processing receipts/documents. |
| **BookStack** | PHP + MySQL | ~200 MB RAM | Hierarchical book/chapter/page wiki | **WAVE 2 CANDIDATE** | Clean, fast, lightweight documentation system. |
| **Markdown Knowledge Vault** | Native Git + SQLite | **< 20 MB RAM** | Standard markdown in `documents/` and `research/` indexed by vector engine | **SELECTED (RING 0 CORE)** | Zero lock-in, version-controlled, instant search, zero background RAM consumption. |

---

## 5. Search Engine & Retrieval

| Candidate | Architecture | Footprint | Index Capabilities | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Meilisearch** | Rust | **~60 - 120 MB RAM** | Ultra-fast typo-tolerant full-text search | **SELECTED (PRIMARY SEARCH)** | Rust binary with near-zero idle RAM. Indexes notes, CRM contacts, and local files instantaneously. |
| **SearXNG** | Python (Docker) | ~180 MB RAM | Privacy metasearch engine (Google, Bing, ArXiv) | **SELECTED (ON-DEMAND RESEARCH)** | Superb for private, rate-limit-free web research. Launch on-demand during research sprints. |
| **Elasticsearch** | Java JVM | 2.0 - 4.0 GB RAM | Heavy distributed search | **REJECTED** | Far too heavy for 16GB host RAM. |

---

## 6. Business Systems, CRM & ERP

| Candidate | Architecture | Footprint | Scope | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Twenty CRM** | NestJS + React + Postgres | ~700MB - 1GB RAM | Modern open-source CRM with GraphQL API | **SELECTED (CANDIDATE CRM)** | Sleek, modern, highly automatable. Run in container when needed. |
| **EspoCRM** | PHP + MySQL | ~150 MB RAM | Lean, fast, customizable CRM | **LIGHTWEIGHT ALTERNATIVE** | Extremely light on RAM if Twenty proves too heavy. |
| **ERPNext** | Python / Frappe + MariaDB + Redis | ~1.5 - 2.5 GB RAM | Comprehensive ERP (accounting, HR, inventory) | **WAVE 2 (EVALUATE)** | Powerful but heavy. Recommended for deployment once revenue-generating operations scale. |
| **Local SQLite CRM Engine**| Python / FastAPI | **< 40 MB RAM** | Built-in contact, pipeline, and outreach tracker | **SELECTED (RING 0 MVP)** | Immediate zero-RAM tracking in `data/crm.db`. Synchronizable with Twenty later. |

---

## 7. Observability & System Health

| Candidate | Architecture | Footprint | Telemetry Scope | Verdict | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Custom Python Health Daemon**| Python / Psutil | **< 35 MB RAM** | Host CPU, RAM, GPU, Disk E:, listening ports, service pings | **SELECTED (RING 0 CORE)** | Real-time ground truth. Zero complex daemon dependencies. Direct JSON feed to dashboard. |
| **Uptime Kuma** | Node.js + SQLite | ~90 MB RAM | HTTP/TCP ping monitoring & status pages | **SELECTED (ON-DEMAND / WAVE 2)** | Lightweight status page and notification dispatcher. |
| **Prometheus + Grafana** | Go + Node | ~450 MB RAM | Heavy time-series metrics | **WAVE 2 OPTIONAL** | Defer until multi-node infrastructure is operational. |

---

## 8. Summary of the Chosen Compact Core Stack

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        OMEGA COMPACT CORE STACK                        │
├───────────────────┬───────────────────────────────┬────────────────────┤
│ Subsystem         │ Selected Solution             │ Idle RAM Footprint │
├───────────────────┼───────────────────────────────┼────────────────────┤
│ AI Inference      │ Ollama (qwen2.5-coder:3b)     │ ~60 MB (VRAM on dem│
│ AI Gateway        │ FastAPI Router (Port 8090)    │ ~45 MB             │
│ Automation        │ n8n (Node/SQLite or Docker)   │ ~250 MB            │
│ Primary Storage   │ SQLite WAL + Drive E: Vault   │ ~15 MB             │
│ Vector Search     │ Qdrant (Rust binary / Docker) │ ~90 MB             │
│ Fast Text Search  │ Meilisearch                   │ ~75 MB             │
│ Command UI        │ Static SPA / Bun server (:3000│ ~30 MB             │
│ Observability     │ OMEGA Health Monitor Daemon   │ ~35 MB             │
├───────────────────┴───────────────────────────────┼────────────────────┤
│ TOTAL COMBINED CORE FOOTPRINT                     │ ~600 MB RAM        │
└───────────────────────────────────────────────────┴────────────────────┘
```
*Result: Massive capability running comfortably inside the available 2.5 GB RAM headroom!*
