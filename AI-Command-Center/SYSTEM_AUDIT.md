# SYSTEM AUDIT & WORKSTATION CAPABILITY REPORT

**Document ID:** `AUDIT-OMNI-2026-10-16`  
**System:** Google Antigravity Workstation Command Center  
**Audit Target:** Host Laptop Environment & Workstation Resources  
**Status:** Verified Facts Grounded (Zero Speculation)  

---

## 1. Executive Summary

A comprehensive, non-destructive audit of the host environment was performed on **October 16, 2026**. The environment is a Windows 10 x64 workstation equipped with a quad-core Intel Core i7-6700HQ CPU, 16 GB of DDR4 RAM, a dual-GPU subsystem (Intel HD 530 + NVIDIA GeForce GTX 960M 4GB VRAM), and three physical/logical partitions totaling ~1.03 TB. 

The machine is well-suited for high-throughput orchestration, Python/Node.js application development, data engineering, and cloud-assisted AI workflows. However, local LLM execution is bounded by GPU architecture (NVIDIA Maxwell 5.0, 4 GB VRAM) and free system RAM (~3.67 GB available under active load). The primary execution drive `E:\` provides abundant headroom (314.63 GB free), whereas system drive `C:\` has 26.13 GB free and must be preserved against large model weight downloads and virtual environment bloat.

---

## 2. Verified Hardware & Operating System Specifications

| Subsystem | Metric | Verified Value | Ground-Truth Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | OS Name & Build | Windows 10 (Build 10.0.19045, AMD64) | Fully patched x64 architecture |
| **CPU** | Processor Model | Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz | Skylake architecture, 4 physical cores, 8 logical threads, 2.60 GHz base (up to 3.50 GHz turbo) |
| **System Memory** | Total RAM | 15.83 GB (~16 GB DDR4) | Hardware capacity |
| **System Memory** | Memory Utilization | 12.16 GB Used / 3.67 GB Available (76% load) | **Constraint:** Heavy concurrent processes or 7B+ local models will trigger paging/OOM |
| **Primary GPU** | Dedicated GPU | NVIDIA GeForce GTX 960M (4.0 GB VRAM) | Maxwell architecture (Compute 5.0). Driver: `32.0.15.8180` |
| **Secondary GPU** | Integrated GPU | Intel(R) HD Graphics 530 (1.0 GB Shared) | Driver: `23.20.16.4973`, display routing |
| **Storage: C:\** | System Drive (SSD) | Total: 97.73 GB \| Free: **26.13 GB** (73.3% used) | **Critical:** Must NOT store model weights or large datasets here |
| **Storage: D:\** | Secondary Partition | Total: 344.84 GB \| Free: **69.04 GB** (80.0% used) | Medium headroom |
| **Storage: E:\** | Development Workspace | Total: 586.54 GB \| Free: **314.63 GB** (46.4% used) | **Optimal:** Primary location for repositories, datasets, and virtual environments |
| **Power & Battery**| Battery Status | 29% charge, AC adapter connected (charging) | Wall power available; thermal dissipation should be monitored under sustained compute |

---

## 3. Development Runtimes & Tooling Inventory

| Tool / Runtime | Verified Version | Executable Path | Operational Status |
| :--- | :--- | :--- | :--- |
| **Python** | `Python 3.13.15` | `C:\Users\amehr\AppData\Local\Programs\Python\Python313\python.EXE` | Verified active, pip available |
| **Node.js** | `v26.4.0` | `C:\Program Files\nodejs\node.EXE` | Verified modern LTS runtime |
| **npm** | `11.17.0` | System PATH | Ready for frontend / SSR builds |
| **Git** | `git 2.54.0.windows.1` | `C:\Program Files\Git\cmd\git.EXE` | Configured with branch `master` |
| **GitHub CLI** | `gh 2.95.0` | System PATH | Fully authenticated, direct GitHub API access |
| **Docker** | `Docker 29.6.1 (build 8900f1d)` | System PATH | Docker daemon available for isolated microservices |
| **VS Code** | `1.136.1` | System PATH | Active primary IDE |
| **Ollama** | Installed | `E:\anti gravity\Tools\Ollama\ollama.EXE` | Installed on `E:\`, but daemon currently offline (port 11434 unreachable) |

---

## 4. Existing Workspace Inventory (`e:\anti`)

A scan of the working root `e:\anti` identified:
- **Total Root Files:** 614 files
- **Directories:** 138 top-level folders
- **Key Asset Categories:**
  - **Python Scripts (178 files):** Scraping, data synthesis, career processing, testing, and automation engines.
  - **Interactive Dashboards (60 HTML files):** Portfolio showcases, career cockpits, recruitment trackers, and API explorers.
  - **Data Registries (62 CSV files):** Bangalore job listings, MNC strike targets, HR connection databases, and company directories.
  - **Specifications & Documentation (139 Markdown files):** Constitutional directives, ubiquitous language (`CONTEXT.md`), and candidate credentials.
  - **Batch Scripts (63 files):** Launcher scripts for local web services, CLI tools, and automation workers.
- **Git Status:** Repository initialized on branch `master`. Active development state with untracked/modified artifacts.

---

## 5. Architectural Bottlenecks & Critical Constraints

1. **Local VRAM & Memory Limits:**
   - The NVIDIA GTX 960M has 4 GB VRAM with compute capability 5.0 (Maxwell). Modern 7B or 8B parameter models (e.g., Llama 3 8B, Mistral 7B) require 4.5–6 GB VRAM even at Q4 quantization, which would cause layer offloading to system RAM.
   - With only 3.67 GB of available system RAM, loading a 7B model locally will exhaust memory and cause disk swapping or system freezing.
   - **Resolution:** Restrict local Ollama models to compact, highly quantized architectures ($\le 3$B parameters, e.g., Llama 3.2 1B/3B, Qwen 2.5 1.5B/3B, or Phi-3 Mini 3.8B Q4). Delegate heavy analytical reasoning to cloud frontier models (Google Gemini / Antigravity).

2. **C:\ Drive Preservation:**
   - `C:\` has only 26.13 GB free.
   - Default directories for Hugging Face cache (`~/.cache/huggingface`) and Ollama models (`~/.ollama/models`) reside on `C:\`.
   - **Resolution:** Set `OLLAMA_MODELS=E:\anti gravity\Tools\Ollama\models` and `HF_HOME=E:\anti\.cache` to keep all model weights on `E:\` (which has 314 GB free).

3. **Ollama Service Offline:**
   - Ollama is installed on `E:\`, but the background service was not running during the audit.
   - **Resolution:** Provide an on-demand launcher batch script (`START_OLLAMA_LEAN.bat`) that starts Ollama pointing to the `E:\` storage directory only when local inference is specifically needed.

---

## 6. Prioritized Action Plan

| Priority | Stage | Action Item | Expected Outcome |
| :---: | :--- | :--- | :--- |
| **P0** | Foundation | Establish dedicated `AI-Command-Center/` structure | Clean, modular workspace without touching existing root scripts |
| **P0** | Architecture | Formulate `AI_STACK.md` & `DECISIONS.md` | Clear role definitions and zero-cost resource boundaries |
| **P1** | Career OS | Synthesize `CAREER_PROFILE_MASTER.md` & ATS Resume | 100% verified ground-truth candidate assets for Bangalore roles |
| **P1** | Product | Build & Test Flagship Career Operations Engine | Functional SQLite deduplication, 0-100 scoring, and outreach generator |
| **P2** | Portfolio | Author `PORTFOLIO_AUDIT.md` (GitHub & Web Portfolio) | Concrete, actionable enhancements for recruiter conversion |
| **P2** | Security | Author `SECURITY_AND_RECOVERY.md` & Test Suite | Disaster recovery, secret hygiene, and automated verification proof |
