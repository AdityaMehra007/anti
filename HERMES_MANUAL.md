# Nous Research Hermes Agent — Complete Operations Manual

Welcome to your production-ready installation of **Nous Research Hermes Agent** (`v0.21.0`) configured inside `e:\anti`.

---

## 1. Quick Launch Matrix

You can launch and interact with Hermes Agent through any of these entrypoints:

| Interface | Launcher / Command | Description |
| :--- | :--- | :--- |
| **Desktop Shortcut** | `Hermes Control Center.lnk` | Unified menu on your Windows Desktop for all agent services. |
| **Master Control Center** | [`HERMES_CONTROL_CENTER.bat`](file:///e:/anti/HERMES_CONTROL_CENTER.bat) | Interactive menu with one-key actions for CLI, TUI, Web, ACP, Cron, and Config. |
| **Web Dashboard** | [`START_WEB_DASHBOARD.bat`](file:///e:/anti/START_WEB_DASHBOARD.bat) <br> URL: [http://127.0.0.1:9119](http://127.0.0.1:9119) | Complete browser dashboard with Chat, Sessions, Skills, Cron, MCPs, and Analytics. |
| **Interactive Terminal** | [`RUN_HERMES.bat`](file:///e:/anti/RUN_HERMES.bat) or `.\hermes.bat` | Standard interactive chat session in a dedicated terminal window. |
| **Modern Fullscreen TUI** | [`RUN_HERMES_TUI.bat`](file:///e:/anti/RUN_HERMES_TUI.bat) or `.\hermes_tui.bat` | Modern Rich/Textual terminal user interface. |
| **ACP Server (IDEs)** | [`START_ACP_SERVER.bat`](file:///e:/anti/START_ACP_SERVER.bat) | Agent Client Protocol server for VS Code, JetBrains, Zed, and Cursor. |
| **Headless One-Shot** | `.\hermes.bat -z "prompt"` | Run a single query headlessly and exit with stdout. |

---

## 2. System Architecture & Environment

- **Repository Root**: `e:\anti\external\hermes-agent`
- **Active Workspace**: `e:\anti`
- **Python Virtualenv**: `e:\anti\external\hermes-agent\.venv` (Python 3.11.15)
- **Node Environment**: Node `v26.4.0` / NPM `11.17.0`
- **Web Frontend Dist**: `e:\anti\external\hermes-agent\hermes_cli\web_dist` (Production Vite/React SPA)
- **Configuration Directory**: `%LOCALAPPDATA%\hermes` (`C:\Users\amehr\AppData\Local\hermes`)
  - `config.yaml`: Core agent configuration (model, provider, memory mode, display settings)
  - `.env`: API credentials (OpenRouter, OpenAI, Anthropic)
  - `SOUL.md`: Persona and behavioral guidance
  - `memories/USER.md`: Persistent user preferences and profile
  - `skills/`: User-level skills repository

---

## 3. Active Capabilities & Toolsets

### 3.1 3,679 Verified Skills
- **3,628 Workspace Skills**: Fully indexed and trusted from [`e:\anti\.agents\skills`](file:///e:/anti/.agents/skills) across engineering, finance, security, devops, architecture, and marketing.
- **51 Bundled Skills**: Core Nous Research tools copied to `%LOCALAPPDATA%\hermes\skills` (GitHub integration, web development, research, sysadmin).
- **Skill Management**:
  ```powershell
  hermes skills list             # View all registered skills
  hermes skills trust <path>     # Trust additional skill directories
  ```

### 3.2 Agent Client Protocol (ACP)
Hermes Agent is configured and verified with `agent-client-protocol==0.9.0`:
```powershell
hermes acp --check             # Output: Hermes ACP check OK
```
Use [`START_ACP_SERVER.bat`](file:///e:/anti/START_ACP_SERVER.bat) to connect external editors (e.g., VS Code extension or Zed ACP client).

### 3.3 Scheduled Tasks & Cron Engine
Automate tasks and agent loops on fixed schedules:
```powershell
hermes cron list               # View scheduled jobs
hermes cron create             # Interactive cron creation
hermes cron doctor             # Health check for scheduled tasks
hermes cron tick               # Manually execute due jobs
```

### 3.4 Multi-Agent Autonomous Delegation
Hermes can spin up isolated subagent child processes to divide and conquer large refactors:
- Tested and verified with subagent worker execution.
- Configurable recursion depth and toolset scoping per delegated task.

---

## 4. Configuration & Provider Settings

### Provider & Model Defaults
- **Current Provider**: `openrouter`
- **Active Model**: `nvidia/nemotron-3.5-lightning:free`
- **Switching Models**:
  ```powershell
  hermes model                 # Interactive model selector
  hermes config set model.default anthropic/claude-sonnet-4.6
  ```
- **Setting Fallback Chains**:
  ```powershell
  hermes fallback add          # Add fallback provider in case of rate limits
  ```

### Memory System
- **Profile**: Automatically learns user preferences and records them in `%LOCALAPPDATA%\hermes\memories\USER.md`.
- **Cross-Session Storage**: SQLite WAL database ensuring instant retrieval without data corruption.

---

## 5. Summary of Created Files

| File | Purpose |
| :--- | :--- |
| [`HERMES_CONTROL_CENTER.bat`](file:///e:/anti/HERMES_CONTROL_CENTER.bat) | Master interactive control panel with numbered menu options. |
| [`START_WEB_DASHBOARD.bat`](file:///e:/anti/START_WEB_DASHBOARD.bat) | One-click background launcher for Web UI on port 9119. |
| [`START_ACP_SERVER.bat`](file:///e:/anti/START_ACP_SERVER.bat) | One-click launcher for editor ACP server. |
| [`RUN_HERMES.bat`](file:///e:/anti/RUN_HERMES.bat) | Diagnostics-checked interactive CLI launcher. |
| [`RUN_HERMES_TUI.bat`](file:///e:/anti/RUN_HERMES_TUI.bat) | Modern fullscreen TUI launcher. |
| [`hermes.bat`](file:///e:/anti/hermes.bat) | Direct command-line wrapper. |
| [`hermes_tui.bat`](file:///e:/anti/hermes_tui.bat) | Direct TUI wrapper. |
| `Desktop\Hermes Control Center.lnk` | Direct Windows desktop shortcut to Control Center. |
| `Desktop\Hermes Web Dashboard.lnk` | Direct Windows desktop shortcut to Web Dashboard. |
| `Desktop\Hermes Agent Chat.lnk` | Direct Windows desktop shortcut to Interactive Chat. |
