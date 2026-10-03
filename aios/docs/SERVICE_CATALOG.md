# 📋 SERVICE CATALOG: ANTIGRAVITY OMEGA

**Registry Scope**: All system services, daemons, background engines, and on-demand stacks.  
**System Host**: Windows 10 Workstation | `AIOS_ROOT: E:\anti\aios`

---

## 1. Master Service Registry

| Service | Purpose | Version | Status | Port | Storage Location | RAM (Idle / Peak) | Dependencies | Startup Policy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AIOS Gateway Router** | Central API gateway, model routing, security proxy | `1.0.0` | **Configured** | `8090` | `E:\anti\aios\ai\` | ~45 MB / ~90 MB | Python 3.13, FastAPI | **Ring 0 (start-core)** |
| **Ollama Runner** | Local GGUF LLM execution (cuBLAS / Vulkan on GTX 960M) | `0.31.1` | **Online** | `11434`| `E:\anti gravity\Tools\Ollama\` | ~60 MB / ~2.2 GB VRAM | NVIDIA Driver 581.80 | **Ring 0 (start-core)** |
| **Qwen 2.5 Coder 3B** | Primary local code synthesis & refactoring | `3B Q4_K_M` | **Cached** | Internal | `E:\anti gravity\OllamaData\models` | ~2.1 GB VRAM (GPU) | Ollama Engine | **On-Demand (via Ollama)** |
| **Llama 3.2 1B** | Fast local classification, triage, & summarization | `1B Q4_K_M` | **Cached** | Internal | `E:\anti gravity\OllamaData\models` | ~1.1 GB VRAM (GPU) | Ollama Engine | **On-Demand (via Ollama)** |
| **Nomic Embed Text** | High-speed local vector embeddings for RAG | `v1.5 F16` | **Targeted**| Internal | `E:\anti gravity\OllamaData\models` | ~300 MB VRAM (GPU) | Ollama Engine | **On-Demand (via Ollama)** |
| **Master SQLite DB** | High-concurrency relational data store (WAL mode) | `3.45+` | **Online** | In-Proc | `E:\anti\aios\data\master.db` | ~15 MB / ~35 MB | SQLite3 runtime | **Ring 0 (Automatic)** |
| **Qdrant Vector DB** | Fast semantic similarity search & document index | `1.12+` | **Targeted**| `6333` | `E:\anti\aios\databases\qdrant\` | ~90 MB / ~180 MB | Rust / Docker | **Ring 1 (start-ai)** |
| **Meilisearch** | Fast typo-tolerant full-text search across files & notes | `1.11+` | **Targeted**| `7700` | `E:\anti\aios\databases\meili\` | ~75 MB / ~150 MB | Rust native binary | **Ring 1 (start-search)** |
| **n8n Automation** | Visual workflow orchestration & webhook triggers | `Latest` | **Installed**| `5678` | `E:\anti\n8n\` | ~250 MB / ~450 MB | Node.js 26.4 / Docker | **Ring 1 (start-automation)** |
| **OMEGA Health Daemon**| Continuous CPU, RAM, GPU, Disk, & port telemetry | `1.0.0` | **Configured** | Internal | `E:\anti\aios\scripts\` | ~35 MB / ~50 MB | Python `psutil` | **Ring 0 (start-core)** |
| **Master Command UI** | Unified executive dashboard for system control | `1.0.0` | **Configured** | `3000` | `E:\anti\aios\dashboards\` | ~30 MB / ~60 MB | Bun / Node static serv | **Ring 0 (start-core)** |
| **Omniroute Gateway** | Distributed agent communication bus | `Custom` | **Active** | `20128`| `E:\anti gravity\npm-global\` | ~120 MB / ~250 MB | Node.js | **Active (PID 33524)** |
| **OpenHands Canvas** | Agent interactive workspace & tool execution canvas | `Latest` | **Active** | `3001` / `8000` | `E:\anti gravity\npm-global\` | ~150 MB / ~350 MB | Node.js / static-serv | **Active (PIDs 33936/34224)** |
| **Supabase Local Stack**| Local Auth, Storage, Postgres, & Studio UI | `v1.200+` | **Configured** | `8000` / `5432` / `3000` | `E:\anti\supabase\` | ~800 MB / ~1.5 GB | Docker Desktop daemon | **Ring 2 (start-dev)** |
| **SearXNG Metasearch**| Private multi-engine research aggregator | `Latest` | **Candidate**| `8888` | `E:\anti\aios\infrastructure\` | ~180 MB / ~300 MB | Docker Compose | **Ring 2 (start-research)** |
| **Paperless-ngx** | Document OCR, metadata classification & archiving | `Latest` | **Candidate**| `8001` | `E:\anti\aios\documents\` | ~600 MB / ~1.2 GB | Docker / Redis / Postgres | **Ring 2 (start-docs)** |

---

## 2. Startup Group Definitions (`omega_ctl`)

- **`start-core`**: Launches Ring 0 essentials (`AIOS Gateway :8090`, `Ollama :11434`, `Health Daemon`, `Master Command UI :3000`). Total footprint: **~170 MB RAM host**.
- **`start-ai`**: Launches local inference and vector stores (`Qdrant :6333`, preloads `qwen2.5-coder:3b`).
- **`start-automation`**: Launches `n8n` workflow platform (`:5678`).
- **`start-dev`**: Initiates Docker daemon and launches on-demand local Postgres/Supabase microservices.
- **`stop-all`**: Gracefully signals and shuts down all active background daemons to reclaim 100% host RAM.
