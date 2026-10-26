---
name: powershell-orchestrator
description: Autonomous SDK, CLI, and operational standard for PowerShell 7+ Core and Windows PowerShell environments. Enables AST parsing, PSScriptAnalyzer security auditing, pipeline object transformation, runspace concurrency, and enterprise runbooks.
---

# PowerShell Autonomous Orchestrator & Execution Skill

Autonomous standard operating procedure and deep SDK for PowerShell (https://github.com/PowerShell/PowerShell).

## Architecture & Primitives

1. **Dual-Mode Execution Architecture**:
   - **Live Host Execution**: Direct execution via `pwsh.exe` (PowerShell Core 7+) or `powershell.exe` (Windows PowerShell 5.1). Commands are piped through `ConvertTo-Json -Depth 5 -Compress` for typed structured JSON deserialization in Python.
   - **High-Fidelity Simulation Engine**: Complete offline mock engine simulating PowerShell 7.5.0 LTS on .NET 9.0, 1,842 cmdlets, 8 runspaces, AST parsing, and PSScriptAnalyzer rule checking for deterministic CI/CD and air-gapped environments.

2. **Core Capabilities**:
   - **AST Abstract Syntax Tree**: Inspects function declarations, parameters, cmdlet invocations, pipeline streams, and catches syntax errors prior to execution.
   - **PSScriptAnalyzer Security Rules**: Detects plain-text hardcoded passwords (`PSAvoidUsingPlainTextForPassword`), unsafe code execution (`PSAvoidUsingInvokeExpression`), output suppression (`PSAvoidUsingWriteHost`), and scope pollutions.
   - **Enterprise Runbooks**:
     * `cis_hardening`: CIS OS Hardening Benchmark audit (ScriptBlock logging, SMBv1, Firewall, Defender, TLS 1.3).
     * `cloud_recon`: Multi-Cloud infrastructure cost leakage & orphan asset discovery.
     * `ad_audit`: Active Directory & identity hygiene threat hunting (Kerberoasting, dormant accounts).
     * `network_diag`: Synthetic latency, ICMP, DNS resolution, and TCP socket handshake benchmarks.
     * `self_healing`: Autonomous service watchdog inspecting core daemons and initiating self-healing restarts.
   - **Model Context Protocol (MCP)**: Exposes 12 tools over JSON-RPC 2.0 stdio (`powershell_mcp_server.py`).

## CLI Usage

```bash
# Query runtime telemetry
python powershell_cli.py info

# Execute pipeline script with structured JSON output
python powershell_cli.py exec "Get-Process | Select-Object -First 5"

# Parse script AST
python powershell_cli.py ast "powershell/runbooks/cis_os_hardening.ps1"

# Audit security rules
python powershell_cli.py analyze "powershell/runbooks/cis_os_hardening.ps1"

# List enterprise runbooks & execute
python powershell_cli.py runbooks
python powershell_cli.py run-runbook cis_hardening

# Search PSGallery packages
python powershell_cli.py gallery --search Az

# Benchmark pipeline throughput
python powershell_cli.py benchmark --iterations 5

# Execute Complete 12-Phase Sovereign Lifecycle
python powershell_cli.py do-everything
```

## Mission Control Cockpit

- **File**: `powershell_control_cockpit.html`
- **Server**: `python powershell_api_server.py --port 8769`
- **One-Click Launch**: `START_POWERSHELL_COCKPIT.bat`
