# 📊 RESOURCE PLAN & GOVERNOR BUDGET: ANTIGRAVITY OMEGA

**Baseline Measurements**: Intel Core i7-6700HQ (4C/8T) | 16 GB Physical RAM (DDR4-2133) | GTX 960M (4 GB VRAM)  
**Host Budget Baseline**: ~13.4 GB actively committed by OS & Dev tools -> **~2.6 GB Dynamic RAM Headroom**.

---

## 1. Measured Resource Catalog

| Component | CPU Allocation | Host RAM Target | Dedicated GPU VRAM | Storage Footprint | Network Bandwidth | Priority Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Windows OS & Drivers** | 1 - 2% idle | ~3.8 GB baseline | ~340 MB (DWM/display) | Drive C: (80 GB) | < 50 Kbps | **SYSTEM** |
| **Antigravity IDE & Language Svr**| 2 - 8% dynamic | ~4.2 GB active | ~150 MB (GPU UI accel) | Drive C: (4 GB) | < 1 Mbps | **DEVELOPMENT** |
| **AIOS Gateway Router (:8090)** | < 0.5% idle | **~45 MB** | 0 MB | Drive E: (< 50 MB) | Local loopback | **CORE (Ring 0)** |
| **Ollama Inference Engine** | 0% idle / 100% on run| **~60 MB idle** | **~2.1 GB VRAM** (Qwen 3B) | Drive E: (OllamaData) | Local loopback | **CORE (Ring 0)** |
| **SQLite Master DB (WAL)** | < 0.1% | **~15 MB** | 0 MB | Drive E: (< 100 MB) | In-process | **CORE (Ring 0)** |
| **OMEGA Health Daemon** | < 0.2% | **~35 MB** | 0 MB | Drive E: (< 20 MB) | Local loopback | **CORE (Ring 0)** |
| **Master Command UI (:3000)** | < 0.2% | **~30 MB** | 0 MB | Drive E: (< 50 MB) | Local loopback | **CORE (Ring 0)** |
| **n8n Automation Engine (:5678)**| 0.5 - 2% | **~250 MB** | 0 MB | Drive E: (< 500 MB) | Local / Webhook | **ON-DEMAND (Ring 1)** |
| **Qdrant Vector DB (:6333)** | 0.2% idle | **~90 MB** | 0 MB (CPU memory map)| Drive E: (< 1 GB) | Local loopback | **ON-DEMAND (Ring 1)** |
| **Meilisearch (:7700)** | 0.1% idle | **~75 MB** | 0 MB | Drive E: (< 200 MB) | Local loopback | **ON-DEMAND (Ring 1)** |
| **Docker Desktop Daemon** | 1 - 3% | **~800 MB** (capped) | 0 MB | Drive E: (Docker root)| Internal VMSwitch | **ON-DEMAND (Ring 2)** |
| **Supabase Local Stack** | 2 - 5% | **~900 MB** (multi-cntr)| 0 MB | Drive E: (Docker vol) | Local loopback | **ON-DEMAND (Ring 2)** |
| **Playwright Browser Runner** | 5 - 20% on test| **~600 MB** (temp) | ~200 MB | Temp directory | Outbound HTTP | **LAB / EPHEMERAL** |

---

## 2. Resource Governor Operational Modes

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        RESOURCE GOVERNOR MODES                         │
├─────────────────┬──────────────────────────────────┬───────────────────┤
│ Mode            │ Active Services                  │ Host RAM Consumed │
├─────────────────┼──────────────────────────────────┼───────────────────┤
│ 1. LEAN CORE    │ Gateway + Ollama + SQLite + UI   │ ~185 MB           │
│ 2. AI ASSIST    │ Lean Core + Qwen 3B + Qdrant     │ ~275 MB + 2.1G GPU│
│ 3. AUTOMATION   │ Lean Core + n8n + Webhooks       │ ~435 MB           │
│ 4. FULL SPRINT  │ Lean Core + n8n + Docker / Supa  │ ~1.95 GB          │
│ 5. STANDBY      │ All user services stopped        │ 0 MB (Zero drain) │
└─────────────────┴──────────────────────────────────┴───────────────────┘
```

---

## 3. Storage Watermark Safeguards

1. **Drive C: Safeguard (< 15 GB Free Trigger)**:
   - When Drive C: free space drops below 15 GB, trigger automatic alert and refuse npm/pip global caching on C:.
   - Enforce environment redirection:
     - `UV_CACHE_DIR=E:\anti\aios\data\cache\uv`
     - `OLLAMA_MODELS=E:\anti gravity\OllamaData\models`
2. **Drive E: Watermark (< 50 GB Free Trigger)**:
   - Normal operating threshold. Currently 335.76 GB Free. Safe for extensive model caches, logs, databases, and Docker images.

---

## 4. CPU & GPU Thermal Throttling Mitigation

- Mobile CPU (`i7-6700HQ`) thermal dissipation is limited to laptop chassis cooling.
- Background worker threads (builds, tests, embeddings) are pinned to a maximum concurrency of **4 worker threads** using Python `ThreadPoolExecutor(max_workers=4)` or uv/pytest `-n 4`.
- GPU batch size during Ollama model loading is locked to `-ngl 99` (offloading all layers for 3B models into Maxwell VRAM), ensuring the GPU handles 100% of tensor operations without CPU bus roundtrip bottlenecks.
