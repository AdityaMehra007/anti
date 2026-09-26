# Project NOMAD - Autonomous Offline Knowledge & AI Server

**Project NOMAD** (developed by **Crosstalk Solutions**) is an offline-first knowledge, education, and autonomous survival computing platform designed to operate completely independently of an internet connection on hardware you own.

---

## 1. System Architecture

Project NOMAD consists of a central **Command Center** orchestrating containerized offline services:

```
                          ┌────────────────────────┐
                          │   Host Web Browser     │
                          │ http://localhost:8080  │
                          └───────────┬────────────┘
                                      │
                                      ▼
                      ┌─────────────────────────────────┐
                      │    NOMAD Command Center Admin   │
                      │   (AdonisJS 6 + Inertia/React)  │
                      └────┬──────────┬───────────┬─────┘
                           │          │           │
             ┌─────────────┘          │           └─────────────┐
             ▼                        ▼                         ▼
   ┌─────────────────┐      ┌─────────────────┐       ┌─────────────────┐
   │    MySQL 8.0    │      │     Redis 7     │       │     Dozzle      │
   │ Metadata & Config│     │ Queues & Tasks  │       │ Logs (:9999)    │
   └─────────────────┘      └─────────────────┘       └─────────────────┘
                                      │
                   Communicates via Docker Engine API
                                      │
         ┌──────────────────┬─────────┴─────────┬──────────────────┐
         ▼                  ▼                   ▼                  ▼
  ┌──────────────┐   ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
  │ Kiwix Server │   │ Ollama (AI)  │    │ Kolibri      │   │ ProtoMaps    │
  │ Offline Wiki │   │ + Qdrant RAG │    │ Khan Academy │   │ Offline Maps │
  └──────────────┘   └──────────────┘    └──────────────┘   └──────────────┘
         ▼                  ▼                   ▼                  ▼
  ┌──────────────┐   ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
  │ FlatNotes    │   │ CyberChef    │    │ Stirling-PDF │   │ Supply Depot │
  │ Local Wiki   │   │ Cryptography │    │ PDF Tools    │   │ App Catalog  │
  └──────────────┘   └──────────────┘    └──────────────┘   └──────────────┘
```

---

## 2. Directory & Storage Layout

All content and databases are persistent in `e:\anti\project-nomad`:

| Path | Purpose | Content Type |
| :--- | :--- | :--- |
| `storage/zim/` | **Kiwix Information Library** | `.zim` archives (Wikipedia, Stack Exchange, PubMed, Wiktionary, Gutenberg). |
| `storage/models/` | **Ollama AI Models** | Quantized GGUF LLMs (e.g. `llama3.2`, `mistral`, `phi3`) & embedding models (`nomic-embed-text`). |
| `storage/maps/` | **ProtoMaps** | Offline `.pmtiles` vector map datasets. |
| `storage/books/` | **E-Book Library** | EPUBs, PDFs, and Calibre library data. |
| `storage/notes/` | **FlatNotes** | Markdown notes, guides, and documentation. |
| `data/mysql/` | **Relational Database** | User accounts, configuration, installed app states. |
| `data/redis/` | **In-Memory Cache** | Background jobs, content indexing queues. |

---

## 3. Quickstart & Launch Options

### Option A: Windows Launcher (Recommended for quick local access)
1. Ensure **Docker Desktop** is running.
   - *(Note: If Docker Desktop is stopped, right-click Docker Desktop in your Start Menu and choose **Run as administrator**).*
2. Double-click:
   ```cmd
   e:\anti\START_PROJECT_NOMAD.bat
   ```
   Or run in PowerShell:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File "e:\anti\project-nomad\launch_nomad.ps1"
   ```
3. The script verifies all directories, validates compose configuration, starts the stack, and opens:
   - **Command Center UI**: `http://localhost:8080`
   - **Container Logs (Dozzle)**: `http://localhost:9999`

### Option B: Native Linux WSL2 (For full upstream Linux kernel fidelity)
If you prefer running under native Ubuntu on Windows:
1. Double-click `e:\anti\SETUP_NOMAD_WSL2.bat` to provision Ubuntu via WSL2.
2. Inside your Ubuntu terminal, run the upstream installer:
   ```bash
   sudo apt-get update && sudo apt-get install -y curl
   curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh -o install_nomad.sh
   sudo bash install_nomad.sh
   ```

---

## 4. Stopping & Managing the Server

To stop the server cleanly at any time:
```cmd
e:\anti\STOP_PROJECT_NOMAD.bat
```
Or via Docker CLI:
```cmd
cd /d "e:\anti\project-nomad"
docker compose -f docker-compose.windows.yml down
```

---

## 5. Adding Offline Content

### 1. Offline Wikipedia & References (Kiwix)
- Two starter Wikipedia mini packages are already pre-loaded into `storage/zim/`:
  - `wikipedia_en_100_mini_2025-06.zim`
  - `wikipedia_en_100_mini_2026-01.zim`
- To download larger collections (e.g., Full English Wikipedia with images, medical encyclopedias, or Stack Overflow), visit:
  [https://download.kiwix.org/zim/](https://download.kiwix.org/zim/)
  and drop any `.zim` file directly into `e:\anti\project-nomad\storage\zim\`.

### 2. Local AI Models (Ollama + Qdrant RAG)
- In the NOMAD Command Center (`http://localhost:8080`), navigate to the **AI Assistant** tab.
- Select your preferred model (e.g., `llama3.2:3b` or `mistral:7b`) to download for completely offline inference.
- Document uploads will automatically be vectorized into **Qdrant** for offline semantic search and retrieval-augmented generation.

### 3. Offline Maps (ProtoMaps)
- Download regional map `.pmtiles` packages directly through the NOMAD UI or manually place them in `e:\anti\project-nomad\storage\maps\`.

---

## 6. Generated Credentials & Security
- **APP_KEY**: `s1Ba2oSN53Sd6I2I1aKQnwJ2hBv3Hojc`
- **DB_USER**: `nomad_user`
- **DB_PASSWORD**: `ZJLC8jzwWBuvnyqCQF2KAMKA`
- **DB_NAME**: `nomad`
- **MYSQL_ROOT_PASSWORD**: `ZJLC8jzwWBuvnyqCQF2KAMKA_root`
