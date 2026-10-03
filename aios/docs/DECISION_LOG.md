# 📜 ARCHITECTURE DECISION LOG (ADR): ANTIGRAVITY OMEGA

**Governance Standard**: OMEGA Supreme Constitution & AGENTS.md Rulings Ledger  
**Format**: `ADR-XXX: Context — Options — Decision — Consequences — Cost`

---

### ADR-001: Allocation of Primary System Workspace (`AIOS_ROOT`) to Drive E:
- **Status**: **ACCEPTED**
- **Date**: 2026-10-01
- **Context**: Drive C: has only 17.59 GB of free space available, with heavy Windows OS and application dependencies. Storing models, Docker roots, or database dumps on C: risks total OS volume saturation. Drive E: possesses 335.76 GB of healthy, free NTFS storage.
- **Decision**: Establish `AIOS_ROOT` permanently at `E:\anti\aios\`. All databases, documents, models, container volume mounts, and logs must reside on Drive E:.
- **Consequences**: Drive C: is preserved from disk starvation. All paths in scripts and configs reference Drive E:.
- **Cost**: None. Improves long-term system stability.

---

### ADR-002: Bounding Local LLM Inference to 1B–3.8B Parameters on GTX 960M
- **Status**: **ACCEPTED**
- **Date**: 2026-10-01
- **Context**: The discrete GPU is an NVIDIA GeForce GTX 960M with 4,096 MiB (4 GB) of GDDR5 VRAM and Compute Capability 5.0 (Maxwell). Attempting to load 7B or 14B models requires heavy system RAM offload or pure CPU execution, resulting in severe token latency (< 3 t/s) and exhausting the host's 2.5 GB free RAM.
- **Decision**: Set the default local model tier to **`Qwen 2.5 Coder 3B`** (at `Q4_K_M`, ~2.1 GB VRAM) for code and **`Llama 3.2 1B`** (at `Q4_K_M`, ~1.1 GB VRAM) for text classification and agent triage.
- **Consequences**: 100% of the model layers load into GPU VRAM. Inference achieves high token velocity (> 25 tokens/s) with near-zero host CPU and RAM degradation.
- **Cost**: Complex multi-file architectural refactors must be routed to Cloud AI Gateways (Gemini 2.0 / Claude 3.5).

---

### ADR-003: SQLite WAL Mode as Primary Ring 0 Relational Database
- **Status**: **ACCEPTED**
- **Date**: 2026-10-01
- **Context**: Running a dedicated PostgreSQL daemon continuously consumes 80–150 MB of resident memory and background CPU cycles. For single-user, local-first personal command centers, SQLite provides full ACID compliance with zero background memory footprint.
- **Decision**: Use SQLite with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) as the primary Ring 0 relational database (`data/master.db`). PostgreSQL is retained via Docker for on-demand multi-container services (e.g., Supabase, Twenty CRM).
- **Consequences**: Zero RAM consumption when idle. Concurrent reads and writes operate with microsecond latency.
- **Cost**: Client-server multi-tenant access is deferred to the on-demand Postgres container.

---

### ADR-004: Dual-Tier AI Gateway Routing with Client-Side PII Redaction
- **Status**: **ACCEPTED**
- **Date**: 2026-10-01
- **Context**: Neither pure local execution (limited by 4GB VRAM) nor pure cloud execution (sacrificing offline capability, privacy, and incurring API costs) meets the OMEGA North Star of Maximum Capability + Maximum Control.
- **Decision**: Deploy an in-process / lightweight FastAPI Gateway (`:8090`). The gateway inspects prompt sensitivity and complexity: routine code completions and confidential documents stay local; high-cognitive architectural evaluations route to Cloud APIs with PII masking.
- **Consequences**: Optimal balance of privacy, speed, capability, and cost.
- **Cost**: Requires maintaining an abstraction adapter layer.

---

### ADR-005: Enforcing WSL2 Memory & Core Capping via `.wslconfig`
- **Status**: **ACCEPTED**
- **Date**: 2026-10-01
- **Context**: By default on Windows 10, WSL2 claims up to 50% of total host RAM (8 GB). Given the host has 16 GB RAM with ~2.5 GB free under typical working load, unconstrained WSL2/Docker launch causes immediate memory compression, swapping, and potential system lockups.
- **Decision**: Deploy a strict `$HOME\.wslconfig` setting `memory=4GB`, `swap=2GB`, and `processors=4`.
- **Consequences**: Docker and WSL2 can never exhaust host memory. Windows and IDE remain responsive during heavy container operations.
- **Cost**: Limits container memory allocation to 4 GB maximum.
