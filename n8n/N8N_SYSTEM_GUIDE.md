# n8n System & Automation Guide

Comprehensive operational guide for running, integrating, and developing workflows with **[n8n](https://github.com/n8n-io/n8n)** in the OMEGA ecosystem.

---

## 1. Quickstart: Launching n8n

You can launch n8n via two modes:

### Option A: One-Click Windows Launcher (Root or n8n folder)
Double-click or run:
```cmd
START_N8N.bat
```
Or with PowerShell:
```powershell
.\n8n\START_N8N.ps1
```
The launcher automatically tests if your Docker daemon is running:
- **If Docker is active**: Runs `docker compose up -d` with persistent volume `omega_n8n_data`.
- **If Docker is inactive**: Launches standalone n8n via `npx n8n` on port `5678`.

### Option B: Docker Compose (Dedicated Container)
Once Docker Desktop is started:
```bash
cd e:\anti\n8n
docker compose up -d
```
To stop the container:
```bash
docker compose down
```

The web dashboard is served at: **`http://localhost:5678`**

---

## 2. API Key Configuration

To enable programmatic control via Python or Node.js:
1. Open `http://localhost:5678` in your browser and complete initial setup.
2. Navigate to **Settings** (gear icon) -> **n8n API**.
3. Click **Create an API key** and copy the generated key.
4. Add it to `e:\anti\n8n\.env`:
   ```env
   N8N_API_KEY=your_api_key_here
   ```

---

## 3. Python Automation SDK (`n8n_client.py`)

### CLI Commands
Check server connectivity:
```bash
python n8n/n8n_client.py status
```

List active workflows:
```bash
python n8n/n8n_client.py list --active-only
```

Import a workflow template:
```bash
python n8n/n8n_client.py import n8n/workflows/outreach_dispatcher.json --activate
```

Trigger an n8n webhook:
```bash
python n8n/n8n_client.py trigger outreach-dispatch --data "{\"recipient_email\": \"lead@example.com\", \"company\": \"TechCorp\"}"
```

### Python Programmatic Usage
```python
from n8n.n8n_client import N8nClient

client = N8nClient(base_url="http://localhost:5678", api_key="your_key")

# Health check
if client.health_check():
    print("n8n is running!")

# Trigger webhook
response = client.trigger_webhook(
    path="outreach-dispatch",
    payload={"recipient_email": "candidate@domain.com", "action": "SCHEDULE_INTERVIEW"}
)

# Export all workflows to backup directory
client.export_all_workflows("e:/anti/n8n/backups")
```

---

## 4. Node.js Automation Bridge (`n8n_bridge.js`)

In JavaScript / TypeScript services:
```javascript
const { N8nBridge } = require('./n8n/n8n_bridge');

const bridge = new N8nBridge();

async function sendEvent() {
  const result = await bridge.triggerWebhook('omega-events', {
    source: 'AUTONOMOUS_DAILY_ECOSYSTEM',
    data: { batch_size: 50, completed: true }
  });
  console.log('Dispatched event:', result);
}
```

---

## 5. Pre-Built Workflow Blueprints

The following production-ready workflow templates are located in `n8n/workflows/`:

| Blueprint | File | Purpose |
| :--- | :--- | :--- |
| **AI Agent Researcher** | `workflows/ai_agent_researcher.json` | Autonomous LangChain agent node with window buffer memory, chat model, and calculator tool. |
| **Outreach Dispatcher** | `workflows/outreach_dispatcher.json` | Webhook receiver that validates contact emails, enriches metadata, and routes verified outreach batches. |
| **System Health Monitor** | `workflows/system_health_monitor.json` | Scheduled cron trigger (every 15 min) pinging internal APIs and logging health anomalies. |
| **Webhook Ingestion Bridge** | `workflows/webhook_ingestion.json` | Generic inbound webhook listener returning structured HTTP 200 acknowledgements. |

### How to Import via UI:
1. In n8n UI, navigate to **Workflows**.
2. Click the `...` menu in the top right -> **Import from File**.
3. Select any `.json` from `e:\anti\n8n\workflows\`.

---

## 6. Developing Custom Community Nodes (`custom-nodes-starter/`)

A TypeScript starter package is prepared at `e:\anti\n8n\custom-nodes-starter/`.

To build the node package:
```bash
cd e:\anti\n8n\custom-nodes-starter
npm install
npm run build
```

To link into local n8n:
```bash
npm link
# Inside your ~/.n8n/custom directory:
npm link n8n-nodes-omega-workspace
```

---

## 7. Storage & Persistence Notes

- **Docker Mode**: All database state, credentials, and executions are stored in the named Docker volume `omega_n8n_data`. Shared files reside in `e:\anti\n8n\local_files/`.
- **Native Mode**: Default state is preserved in `~/.n8n/` on Windows (`C:\Users\<user>\.n8n\`).
- **Data Pruning**: Automatically enabled (`EXECUTIONS_DATA_PRUNE=true`) with a 168-hour (7 day) retention window to maintain fast SQLite / Postgres performance.

---

## 8. Core Source Code & Monorepo Architecture

The full official **[n8n-io/n8n](https://github.com/n8n-io/n8n)** repository is cloned locally at:
`e:\anti\external\n8n`

### Monorepo Packages (`packages/`):
- `packages/cli`: Main entrypoint, process lifecycle, and backend orchestrator.
- `packages/core`: Core execution pipeline, expression evaluations, and credential managers.
- `packages/frontend` / `editor-ui`: Vue 3 workflow canvas, node configuration modals, and execution debugger.
- `packages/nodes-base`: Complete collection of 400+ built-in node definitions (HTTP, Slack, Discord, Postgres, AI Agent, etc.).
- `packages/workflow`: Core data types, interface contracts, and execution graph engine.
- `packages/modules`: Modular extensions and enterprise licensing layers.

### Building Core from Source:
```bash
cd e:\anti\external\n8n
pnpm install
pnpm build
```

