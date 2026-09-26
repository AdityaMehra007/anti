# OmniRoute AI Gateway: Sovereign Agent Integration Guide

OmniRoute acts as a high-performance local AI gateway and unified reverse-proxy for all autonomous agents, developer tools, and IDEs running in this workspace.

- **Gateway URL**: `http://localhost:20128/v1`
- **Default Local Key**: `sk-omniroute-local` (or none when `REQUIRE_API_KEY=false`)
- **Dashboard**: `http://localhost:20128/dashboard/free-tiers`
- **Catalog**: 352+ providers, 150+ free tiers, 1200+ models

---

## 1. Quick Launch Commands

| Tool | Action | Command |
|---|---|---|
| **Dedicated Launcher** | Interactive menu | Double-click [`START_OMNIROUTE.bat`](../../START_OMNIROUTE.bat) |
| **Automation Suite** | Main Mission Control | Option `[10]` in [`AUTOMATION_SUITE.bat`](../../AUTOMATION_SUITE.bat) |
| **PowerShell CLI** | Check status | `powershell scripts/run_omniroute.ps1 status` |
| **PowerShell CLI** | Test prompt | `powershell scripts/run_omniroute.ps1 test "Prompt"` |
| **PowerShell CLI** | Open dashboard | `powershell scripts/run_omniroute.ps1 dashboard` |

---

## 2. Virtual Combos & Recommended Models

OmniRoute constructs dynamic, scored virtual combos automatically:

- `auto` - Best available model across all healthy free & configured providers
- `auto/coding` - Optimized for programming, refactoring, and code analysis
- `auto/fast` - Low-latency completions for rapid edits and autocomplete
- `auto/smart` - High-intelligence reasoning (e.g. Claude Sonnet / GPT-4o / DeepSeek R1)
- `auto/cheap` - Lowest cost per token routing
- `auto/offline` - Local-only models via Ollama / LM Studio

---

## 3. Agent & IDE Configurations

### A. OpenCode CLI (`opencode`)
Configured in [`opencode.config.json`](../../opencode.config.json):
```json
{
  "providers": {
    "preferred": "omniroute",
    "omniroute": {
      "base_url": "http://localhost:20128/v1",
      "api_key": "sk-omniroute-local",
      "models": {
        "fast": "auto/fast",
        "smart": "auto/smart",
        "coding": "auto/coding",
        "default": "auto"
      }
    }
  }
}
```

### B. Claude Code CLI
Export environment variables before launching Claude Code:
```bash
# Windows PowerShell
$env:ANTHROPIC_BASE_URL="http://localhost:20128/v1"
$env:ANTHROPIC_API_KEY="sk-omniroute-local"
claude
```

### C. Cursor IDE
1. Open Cursor Settings -> **Models**.
2. Enable **OpenAI API Key Override**:
   - **Base URL**: `http://localhost:20128/v1`
   - **API Key**: `sk-omniroute-local`
3. Add custom model names:
   - `auto`
   - `auto/coding`
   - `auto/fast`

### D. Cline / Roo Code (VS Code Extension)
1. Open Cline Settings -> **API Provider** -> select **OpenAI Compatible**.
2. **Base URL**: `http://localhost:20128/v1`
3. **API Key**: `sk-omniroute-local`
4. **Model ID**: `auto/coding`

### E. Python / Omega Architecture (`omega/model_router`)
OmniRoute is natively integrated via [`OmniRouteClient`](../../omega/model_router/client.py):
```python
from omega.model_router.client import OmniRouteClient, ExecutionMode

client = OmniRouteClient(base_url="http://localhost:20128/v1")
response = client.generate("auto/coding", [{"role": "user", "content": "Analyze system state"}])
print(response.content)
```

---

## 4. Verification & Testing

Run the automated test suite to ensure compliance with the ADI Constitution:
```powershell
python tests/test_omniroute_live.py
```
All 18 security, fallback, discovery, and telemetry tests must pass before production deployment.
