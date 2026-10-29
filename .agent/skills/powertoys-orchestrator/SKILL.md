---
name: powertoys-orchestrator
description: Autonomous SDK, CLI, and operational standard for Microsoft PowerToys (https://github.com/microsoft/PowerToys). Enables FancyZones window management, PowerToys Run modular fuzzy launcher, Awake keep-awake policies, Keyboard Manager key remapping, Hosts file editing, Advanced Paste AI transformations, Workspaces orchestration, and CIS Windows workstation hardening.
---

# Microsoft PowerToys Autonomous Orchestrator & Execution Skill

Autonomous standard operating procedure, deep Python SDK, and Model Context Protocol (MCP) server for Microsoft PowerToys (https://github.com/microsoft/PowerToys).

## Architecture & Primitives

1. **Dual-Mode Execution Architecture**:
   - **Live Windows Host**: Detects and interacts with native PowerToys (`PowerToys.exe`, settings in `%LOCALAPPDATA%\Microsoft\PowerToys`, `%SystemRoot%\System32\drivers\etc\hosts`, and Win32 process handles).
   - **High-Fidelity Simulation Engine**: Complete offline mock engine simulating PowerToys v0.88.0 on .NET 9.0 (WinUI 3 / WASDK 1.6), covering all 24 utilities, multi-monitor window coordinate math, fuzzy scoring algorithms, and power policies for deterministic CI/CD and air-gapped agent operations.

2. **Core Capabilities**:
   - **FancyZones Engine**: Computes exact pixel bounding boxes for standard (1080p, 1440p, 4K) and 32:9 Super UltraWide displays (5120x1440), accounting for zone spacing, margins, and taskbar offsets.
   - **PowerToys Run (PT Run)**: Built-in multi-plugin fuzzy search engine supporting Calculator expressions (`sqrt(144) + 12`), Unit Conversions (`100 km in miles`), Process Switching (Window Walker), Programs, System Commands (lock, sleep, restart), and Terminal execution (`> cmd`).
   - **Awake Power Sentinel**: Manages system stay-awake assertions across `PASSIVE`, `INDEFINITE`, and `TIMED` modes with display assertion flags.
   - **Keyboard Manager (KBM)**: Low-level physical key remapping and global/app-specific shortcut translation matrix with conflict detection for reserved Windows hotkeys.
   - **Hosts File Vault**: RFC-compliant parser and validator for Windows hosts DNS resolution with loopback protection and toggle capabilities.
   - **Advanced Paste AI Pipeline**: Clipboard content transformation supporting Markdown to JSON, JSON formatting, case conversions (`snake_case` <-> `camelCase`), PII and API token redaction, and executive bullet summarization.
   - **Workspaces Orchestrator**: Multi-window workstation deployment mapping applications to target FancyZones zones.
   - **CIS Workstation Hardening Audit**: Verification of diagnostic telemetry opt-out, non-elevated privilege boundaries, and host DNS integrity.

3. **12-Phase Sovereign Lifecycle (`do-everything`)**:
   - Phase 1: PowerToys Runner & Architecture Telemetry Pre-Flight
   - Phase 2: FancyZones Multi-Monitor Grid & Canvas Layout Certification
   - Phase 3: PowerToys Run Modular Plugin Fuzzy Search Benchmark
   - Phase 4: Awake Daemon Power State & Display Keep-Alive Verification
   - Phase 5: Keyboard Manager Key Remapping & Modifier Matrix Audit
   - Phase 6: Hosts File Syntax Validation & DNS Security Audit
   - Phase 7: Advanced Paste AI Transformation Pipeline Certification
   - Phase 8: Text Extractor OCR & Windows Vision Framework Probe
   - Phase 9: Workspaces Multi-Application Layout Orchestration
   - Phase 10: Windows PowerToys Security & Hardening Assessment
   - Phase 11: Real-Time Snapping & Launcher Latency Benchmarking
   - Phase 12: Sovereign Execution Manifest & Cryptographic Attestation

---

## CLI Usage

```bash
# Query runtime telemetry
python powertoys_cli.py info

# List all 24 utility modules
python powertoys_cli.py modules

# Toggle utility module state
python powertoys_cli.py toggle FancyZones --disable

# Calculate FancyZones pixel coordinates for 4K display
python powertoys_cli.py fancyzones --layout priority-grid-01 --resolution 3840x2160

# Configure Awake stay-awake policy
python powertoys_cli.py awake --mode indefinite --keep-display

# Execute PowerToys Run search query
python powertoys_cli.py run-launcher "sqrt(256) * 4"
python powertoys_cli.py run-launcher "100 km to miles"
python powertoys_cli.py run-launcher "> ipconfig /all"

# Keyboard Manager remap
python powertoys_cli.py keyboard
python powertoys_cli.py keyboard --remap-key CapsLock LeftCtrl

# Inspect and add hosts records
python powertoys_cli.py hosts
python powertoys_cli.py hosts --add 127.0.0.1 sandbox.omega.local "Cluster API"

# Transform clipboard text via Advanced Paste
python powertoys_cli.py advanced-paste --text "user_account_id" --format snake_to_camel

# Launch multi-app workspace
python powertoys_cli.py workspaces --launch "Full-Stack Dev"

# Execute CIS workstation security audit
python powertoys_cli.py security-audit

# Run performance micro-benchmarks
python powertoys_cli.py benchmark --iterations 2000

# Execute 12-phase sovereign lifecycle
python powertoys_cli.py do-everything
```

---

## REST API & Cockpit Bridge

Run the local server on port 8770:
```bash
python powertoys_api_server.py --port 8770
```
- **Mission Control Cockpit**: `http://localhost:8770/cockpit`
- **Telemetry**: `GET http://localhost:8770/api/v1/info`
- **Modules**: `GET http://localhost:8770/api/v1/modules`
- **Run Query**: `GET http://localhost:8770/api/v1/run?q=calc`
- **Do Everything**: `POST http://localhost:8770/api/v1/do-everything`

---

## Model Context Protocol (MCP) Server

Connect AI agents using stdio:
```json
{
  "mcpServers": {
    "powertoys": {
      "command": "python",
      "args": ["e:\\anti\\powertoys_mcp_server.py"]
    }
  }
}
```
Exposes 16 agent tools: `powertoys_get_status`, `powertoys_list_modules`, `powertoys_toggle_module`, `powertoys_calculate_fancyzones`, `powertoys_query_pt_run`, `powertoys_set_awake`, `powertoys_get_keyboard_remaps`, `powertoys_add_key_remap`, `powertoys_list_hosts`, `powertoys_add_hosts_entry`, `powertoys_transform_paste`, `powertoys_extract_ocr`, `powertoys_launch_workspace`, `powertoys_security_audit`, `powertoys_benchmark`, `powertoys_do_everything`.
