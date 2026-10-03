# 📦 SOFTWARE INVENTORY: OMEGA COMMAND CENTER

**Audit Date**: `2026-10-01`  
**Classification**: Production Engineering Registry  
**Auditor**: Antigravity OMEGA Systems Organization

---

## 1. Development Runtimes, Compilers & SDKs

| Software | Version | Install Location | Type | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Python 3.13 (64-bit)** | `3.13.15` | `C:\Users\amehr\AppData\Local\Programs\Python\Python313\` | Native System | Primary backend & automation interpreter |
| **Python 3.12 (64-bit)** | `3.12.10` | `C:\Users\amehr\AppData\Local\Programs\Python\Python312\` | Native System | Secondary compatibility interpreter |
| **uv Package Manager** | `0.11.26` | `C:\Users\amehr\.local\bin\uv.exe` | Native Rust CLI | High-speed Python dependency resolver & venv runner |
| **Node.js** | `v26.4.0` | `C:\Program Files\nodejs\node.exe` | Native System | Modern V8 JavaScript/TypeScript execution |
| **npm** | `11.x` | `C:\Program Files\nodejs\npm.ps1` | Native Script | Default Node package manager |
| **pnpm** | `11.9.0` | `E:\anti gravity\npm-global\pnpm.ps1` | Symlinked Fast CLI | Disk-efficient hard-link package manager |
| **Bun** | `1.4.0` | `E:\anti gravity\npm-global\bun.ps1` | All-in-one Native | High-speed bundler, package manager, and TS runtime |
| **Rust Toolchain** | `rustc 1.98.0` | `C:\Users\amehr\.cargo\bin\rustc.exe` | Native Compiler | Systems-level low-latency compilation |
| **Cargo** | `1.98.0` | `C:\Users\amehr\.cargo\bin\cargo.exe` | Native Package Mgr | Rust package manager & build pipeline |
| **Git for Windows** | `2.54.0` | `C:\Program Files\Git\cmd\git.exe` | Native VCS | Version control and worktree engine |
| **GitHub CLI (`gh`)** | `2.95.0` | `C:\Program Files\GitHub CLI\gh.exe` | Native CLI | GitHub pull requests, issues, repo management |
| **Microsoft .NET Host** | 8.x/9.x Host | `C:\Program Files\dotnet\dotnet.exe` | CoreCLR Host | .NET runtime host (no SDK installed) |
| **MSVC C++ Runtimes** | 2005 - 2026 | System WinSxS / System32 | Redistributable | Visual C++ CRT dependencies for native DLLs |

---

## 2. Artificial Intelligence, LLMs & Local Agents

| Software | Version | Path / Address | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Ollama Runner** | `0.31.1` | `E:\anti gravity\Tools\Ollama\ollama.exe` | Installed (Drive E:) | Local GGUF LLM inference server (OpenAI API compliant) |
| **Ollama Model Cache**| Multiple | `E:\anti gravity\OllamaData\models` | Populated | Pre-downloaded `qwen2.5-coder:3b`, `llama3:latest` |
| **Antigravity IDE** | Latest | `C:\Users\amehr\AppData\Local\Programs\antigravity\` | Running | DeepMind agentic pairing platform & language server |
| **Omniroute Server** | Custom | Port `20128` (PID 33524) | Active | Distributed WebSocket message & agent gateway |
| **OpenHands Canvas** | Latest | Port `3001` / `8000` (PIDs 33936, 34224) | Active | Agent canvas static frontend & ingress routing |
| **ChatGPT Classic Desktop**| `1.2026.190` | WindowsApp UWP Package | Active | OpenAI desktop application client |
| **ChatGPT Desktop App**| `26.928.2636`| WindowsApp UWP Package | Active | Codex/ChatGPT modern client |
| **Google AI Studio PWA** | WebApp | Chrome App Host | Installed | Web IDE for Gemini 1.5/2.0 API interaction |
| **GitHub Copilot** | `1.0.12` | Desktop Extension | Installed | Code suggestion engine |

---

## 3. Editors & IDEs

| Software | Version | Publisher | Status |
| :--- | :--- | :--- | :--- |
| **Antigravity** | Active | Google DeepMind | Primary pairing and agent development studio |
| **Visual Studio Code** | `1.136.1` | Microsoft Corporation | Full general-purpose code editor |
| **Cursor** | `3.18.25` | Anysphere | AI-integrated fork of VS Code |
| **GitHub Desktop** | `3.6.4` | GitHub, Inc. | Graphical Git GUI |

---

## 4. Virtualization, Containerization & Infrastructure

| Software | Version | Daemon Status | Notes |
| :--- | :--- | :--- | :--- |
| **Docker Desktop** | `4.80.0` | Inactive (Service stopped) | Container orchestration tool for Windows |
| **Docker CLI** | `29.6.1` | Installed | CLI tool pointing to local Docker named pipe |
| **Docker Compose** | `v5.1.4` | Installed | Multi-container composition engine |
| **WSL 2** | `2.7.14.0` | Active Kernel / 0 Distros | Linux emulation layer (no distro installed yet) |

---

## 5. Web Browsers & Rendering Engines

| Software | Version | Rendering Engine | Strategic Purpose |
| :--- | :--- | :--- | :--- |
| **Google Chrome** | `154.0.8037.92` | Chromium (Blink) | Primary web interaction & DevTools automation |
| **Brave** | `154.1.96.59` | Chromium (Shields active) | Privacy-hardened testing browser |
| **Microsoft Edge** | `154.0.4258.37` | Chromium (Edge) | Windows integrated browser |
| **Edge WebView2 Runtime**| `154.0.4258.48` | Chromium Component | Embedded UI rendering for native desktop shells |

---

## 6. Business, Communications & Utilities

| Category | Application Name | Version | Role |
| :--- | :--- | :--- | :--- |
| **Communication** | WhatsApp Desktop | `2.2637.100.0` | Direct messaging client |
| **Communication** | Zoom Desktop | `5.15.10` | Video conferencing |
| **Media Player** | VLC Media Player | `3.0.20` | Audio/video preview & inspection |
| **Hardware Management**| Logitech G HUB | `2026.1.828335` | Mouse & peripheral driver suite |
| **Hardware Management**| SteelSeries GG | `110.0.0` | Audio & peripheral controller |
| **Driver Suite** | NVIDIA App / GeForce NOW | `11.0.5.420` | Display driver & GPU tuning |
| **Gaming / Simulation**| Steam, Epic Games, Riot | Installed | Gaming platforms |
