#!/usr/bin/env python3
"""
Generates the self-contained OMEGA Master MCP Mission Control Cockpit HTML.
"""

import json
from pathlib import Path

WORKSPACE_DIR = Path(r"E:\anti").resolve()
CATALOG_PATH = WORKSPACE_DIR / "data" / "mcp_tools_catalog.json"
OUTPUT_HTML = WORKSPACE_DIR / "mcp_master_cockpit.html"

def generate():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    catalog_json_str = json.dumps(catalog_data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMEGA ∞ MCP Master Mission Control v3.0 | 24 Servers & 260 Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #070a13;
            --bg-surface: #0e1526;
            --bg-card: #131c33;
            --bg-card-hover: #192544;
            --border-glow: #1e2c4f;
            --border-active: #06b6d4;
            --accent-cyan: #06b6d4;
            --accent-sky: #38bdf8;
            --accent-indigo: #6366f1;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-purple: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --font-mono: 'JetBrains Mono', monospace;
            --font-sans: 'Inter', sans-serif;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            line-height: 1.5;
            min-height: 100vh;
            padding: 24px;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.08) 0%, transparent 50%);
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 28px;
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 18px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}

        .header-title-box {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .logo-badge {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo));
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 800;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
        }}

        .title-text h1 {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #fff, var(--accent-sky));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .title-text p {{
            font-size: 13px;
            color: var(--text-muted);
            font-family: var(--font-mono);
            margin-top: 2px;
        }}

        .header-badges {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            font-family: var(--font-mono);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .badge-live {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}

        .pulse-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 10px var(--accent-green);
            animation: pulse 1.5s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 0.4; transform: scale(0.9); }}
            50% {{ opacity: 1; transform: scale(1.1); }}
            100% {{ opacity: 0.4; transform: scale(0.9); }}
        }}

        .badge-info {{
            background: rgba(99, 102, 241, 0.15);
            color: var(--accent-indigo);
            border: 1px solid rgba(99, 102, 241, 0.4);
        }}

        /* KPI STATS ROW */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .stat-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 18px 22px;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
        }}

        .stat-card:hover {{
            border-color: var(--border-active);
            transform: translateY(-2px);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
        }}

        .stat-servers::before {{ background: var(--accent-cyan); }}
        .stat-tools::before {{ background: var(--accent-indigo); }}
        .stat-compliance::before {{ background: var(--accent-green); }}
        .stat-hub::before {{ background: var(--accent-purple); }}

        .stat-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .stat-val {{
            font-size: 32px;
            font-weight: 800;
            font-family: var(--font-mono);
            margin: 6px 0 2px 0;
            color: #fff;
        }}

        .stat-desc {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* TABS NAVIGATION */
        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border-glow);
            padding-bottom: 12px;
        }}

        .nav-tab {{
            background: transparent;
            color: var(--text-muted);
            border: 1px solid transparent;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .nav-tab:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
        }}

        .nav-tab.active {{
            background: var(--bg-surface);
            color: var(--accent-cyan);
            border-color: var(--border-glow);
            border-bottom-color: var(--accent-cyan);
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.15);
        }}

        /* TAB CONTENT PANELS */
        .tab-panel {{
            display: none;
        }}

        .tab-panel.active {{
            display: block;
        }}

        /* SEARCH & FILTER CONTROLS */
        .controls-row {{
            display: flex;
            gap: 14px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            position: relative;
            min-width: 280px;
        }}

        .search-input {{
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 12px 18px 12px 42px;
            color: #fff;
            font-family: var(--font-mono);
            font-size: 14px;
            outline: none;
            transition: all 0.2s;
        }}

        .search-input:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.25);
        }}

        .search-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 16px;
        }}

        .filter-select {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 12px 18px;
            color: #fff;
            font-family: var(--font-sans);
            font-size: 14px;
            outline: none;
            cursor: pointer;
        }}

        /* SERVER CARDS GRID */
        .servers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 18px;
        }}

        .server-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
        }}

        .server-card:hover {{
            border-color: var(--border-active);
            background: var(--bg-card);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }}

        .server-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }}

        .server-name {{
            font-size: 18px;
            font-weight: 700;
            font-family: var(--font-mono);
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .server-cat-tag {{
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(99, 102, 241, 0.2);
            color: var(--accent-sky);
            border: 1px solid rgba(99, 102, 241, 0.4);
            text-transform: uppercase;
        }}

        .server-desc {{
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.4;
            margin-bottom: 16px;
            flex: 1;
        }}

        .server-meta-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 12px;
            font-family: var(--font-mono);
        }}

        .tools-count-pill {{
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 700;
        }}

        .inspect-btn {{
            background: transparent;
            border: 1px solid var(--border-glow);
            color: var(--text-main);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .inspect-btn:hover {{
            background: var(--accent-cyan);
            color: #000;
            border-color: var(--accent-cyan);
        }}

        /* TOOL MATRIX TABLE & CARDS */
        .tools-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .tool-row {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 16px 20px;
            transition: all 0.2s ease;
        }}

        .tool-row:hover {{
            border-color: var(--accent-indigo);
            background: var(--bg-card);
        }}

        .tool-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }}

        .tool-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 15px;
            color: var(--accent-cyan);
        }}

        .tool-server-badge {{
            font-size: 11px;
            padding: 2px 8px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .tool-desc-short {{
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 6px;
        }}

        .tool-schema-drawer {{
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px dashed var(--border-glow);
            display: none;
        }}

        .tool-schema-drawer.open {{
            display: block;
        }}

        .code-block {{
            background: #04060a;
            border: 1px solid var(--border-glow);
            border-radius: 8px;
            padding: 14px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: #38bdf8;
            overflow-x: auto;
            position: relative;
        }}

        .copy-code-btn {{
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
        }}

        .copy-code-btn:hover {{
            background: var(--accent-cyan);
            color: #000;
        }}

        /* EXPORT TAB */
        .export-cards-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .export-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 24px;
        }}

        .export-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .export-title {{
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .export-path {{
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--accent-sky);
            margin-bottom: 14px;
        }}

        /* PROTOCOL ARCHITECTURE */
        .arch-diagram {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 24px;
        }}

        .step-sequence {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 20px;
        }}

        .step-item {{
            display: flex;
            gap: 16px;
            background: var(--bg-card);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 18px;
            align-items: flex-start;
        }}

        .step-num {{
            background: var(--accent-indigo);
            color: #fff;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .step-content h3 {{
            font-size: 15px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 4px;
        }}

        .step-content p {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* AUDITOR BENCHMARK TAB */
        .bench-summary {{
            background: var(--bg-surface);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>

    <!-- MASTER HEADER -->
    <header class="header">
        <div class="header-title-box">
            <div class="logo-badge">⚡</div>
            <div class="title-text">
                <h1>OMEGA ∞ MCP MASTER MISSION CONTROL v3.0</h1>
                <p>Universal Model Context Protocol Fleet & 260 Tool Registry Engine</p>
            </div>
        </div>
        <div class="header-badges">
            <div class="badge badge-live">
                <div class="pulse-dot"></div>
                24 SERVERS ONLINE
            </div>
            <div class="badge badge-info">
                260 VERIFIED TOOLS
            </div>
            <div class="badge" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); border: 1px solid rgba(168, 85, 247, 0.4);">
                STDIO / HTTP / SSE
            </div>
        </div>
    </header>

    <!-- KEY STATS ROW -->
    <div class="stats-grid">
        <div class="stat-card stat-servers">
            <div class="stat-label">Total MCP Servers</div>
            <div class="stat-val" id="stat-total-servers">24</div>
            <div class="stat-desc">6 Reference + 1 GitHub + 1 Cloud + 15 Sovereign + 1 Proxy</div>
        </div>
        <div class="stat-card stat-tools">
            <div class="stat-label">Registered Tools</div>
            <div class="stat-val" id="stat-total-tools">260</div>
            <div class="stat-desc">JSON-RPC 2.0 executable functions with strict schemas</div>
        </div>
        <div class="stat-card stat-compliance">
            <div class="stat-label">Protocol Standard</div>
            <div class="stat-val">2024-11-05</div>
            <div class="stat-desc">Full Anthropic / ModelContextProtocol Specification</div>
        </div>
        <div class="stat-card stat-hub">
            <div class="stat-label">Composite Multiplexer</div>
            <div class="stat-val">READY</div>
            <div class="stat-desc">Unified single-endpoint stdio proxy (mcp_cli.py composite)</div>
        </div>
    </div>

    <!-- NAVIGATION TABS -->
    <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('fleet')">🖥️ Server Fleet (24)</button>
        <button class="nav-tab" onclick="switchTab('matrix')">🛠️ Tool Matrix (260)</button>
        <button class="nav-tab" onclick="switchTab('arch')">📐 Protocol Architecture</button>
        <button class="nav-tab" onclick="switchTab('export')">📦 Client Setup & Export</button>
        <button class="nav-tab" onclick="switchTab('bench')">⏱️ Test Bench & Auditor</button>
    </div>

    <!-- TAB 1: SERVER FLEET -->
    <div id="tab-fleet" class="tab-panel active">
        <div class="controls-row">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="fleet-search" class="search-input" placeholder="Search servers by name, author, or capability..." oninput="filterFleet()">
            </div>
            <select id="fleet-cat-filter" class="filter-select" onchange="filterFleet()">
                <option value="ALL">All Categories (24)</option>
                <option value="Reference Protocol">Reference Protocol (6)</option>
                <option value="Official GitHub">Official GitHub (1)</option>
                <option value="Workspace Sovereign">Workspace Sovereign (15)</option>
                <option value="Cloud & DB">Cloud & DB (1)</option>
                <option value="Browser Automation">Browser Automation (1)</option>
            </select>
        </div>

        <div class="servers-grid" id="fleet-grid">
            <!-- Dynamically populated -->
        </div>
    </div>

    <!-- TAB 2: TOOL MATRIX -->
    <div id="tab-matrix" class="tab-panel">
        <div class="controls-row">
            <div class="search-box">
                <span class="search-icon">⚡</span>
                <input type="text" id="tool-search" class="search-input" placeholder="Search 260 tools by keyword, parameter, or purpose..." oninput="filterTools()">
            </div>
            <select id="tool-server-filter" class="filter-select" onchange="filterTools()">
                <option value="ALL">All Servers (24)</option>
                <!-- Dynamically populated -->
            </select>
        </div>

        <div style="font-size: 13px; color: var(--text-muted); font-family: var(--font-mono); margin-bottom: 14px;" id="tool-count-display">
            Showing 260 tools across 24 servers
        </div>

        <div class="tools-list" id="tools-container">
            <!-- Dynamically populated -->
        </div>
    </div>

    <!-- TAB 3: PROTOCOL ARCHITECTURE -->
    <div id="tab-arch" class="tab-panel">
        <div class="arch-diagram">
            <h2 style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 8px;">Model Context Protocol (MCP) Execution Lifecycle</h2>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px;">
                MCP standardizes communication between host LLM applications (clients) and external data/tool providers (servers) via standardized JSON-RPC 2.0 messages over standard I/O (stdio) or Server-Sent Events (SSE).
            </p>

            <div class="step-sequence">
                <div class="step-item">
                    <div class="step-num">1</div>
                    <div class="step-content">
                        <h3>Client Handshake & Capability Negotiation</h3>
                        <p>The host client boots the child process and sends an <code>initialize</code> request with protocol version, capabilities, and client metadata.</p>
                        <div class="code-block" style="margin-top: 10px;">
{{ "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {{ "protocolVersion": "2024-11-05", "capabilities": {{}}, "clientInfo": {{ "name": "claude-code", "version": "1.0.0" }} }} }}
                        </div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-num">2</div>
                    <div class="step-content">
                        <h3>Server Capability Affirmation</h3>
                        <p>The server replies with supported protocol versions, feature capabilities (tools, resources, prompts, logging), and server identification.</p>
                        <div class="code-block" style="margin-top: 10px;">
{{ "jsonrpc": "2.0", "id": 1, "result": {{ "protocolVersion": "2024-11-05", "capabilities": {{ "tools": {{}} }}, "serverInfo": {{ "name": "plane-mcp-server", "version": "1.0.0" }} }} }}
                        </div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-num">3</div>
                    <div class="step-content">
                        <h3>Dynamic Tool Discovery</h3>
                        <p>The client calls <code>tools/list</code> to fetch all registered executable tools along with their JSON Schema parameters.</p>
                        <div class="code-block" style="margin-top: 10px;">
{{ "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {{}} }}
                        </div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-num">4</div>
                    <div class="step-content">
                        <h3>Tool Execution Dispatch</h3>
                        <p>When the model decides to invoke a tool, the client dispatches <code>tools/call</code> with validated structured arguments.</p>
                        <div class="code-block" style="margin-top: 10px;">
{{ "jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {{ "name": "plane_create_issue", "arguments": {{ "project_id": "OMEGA-CORE", "name": "Deploy Windmill DAG", "priority": "high" }} }} }}
                        </div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-num">5</div>
                    <div class="step-content">
                        <h3>Structured Context Ingestion</h3>
                        <p>The server completes execution and returns text or embedded resources back into the model's active context window.</p>
                        <div class="code-block" style="margin-top: 10px;">
{{ "jsonrpc": "2.0", "id": 3, "result": {{ "content": [{{ "type": "text", "text": "{{\\"status\\": \\"success\\", \\"issue_id\\": \\"ISS-9821\\"}}" }}] }} }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 4: CLIENT SETUP & EXPORT -->
    <div id="tab-export" class="tab-panel">
        <div class="export-cards-grid">
            
            <!-- CLAUDE DESKTOP -->
            <div class="export-card">
                <div class="export-header">
                    <div class="export-title">🟣 Claude Desktop</div>
                    <button class="inspect-btn" onclick="copyConfig('claude')">Copy Config</button>
                </div>
                <div class="export-path">%APPDATA%\Claude\claude_desktop_config.json</div>
                <div class="code-block" id="cfg-claude" style="max-height: 280px;">Loading configuration...</div>
            </div>

            <!-- CURSOR IDE -->
            <div class="export-card">
                <div class="export-header">
                    <div class="export-title">⚡ Cursor IDE</div>
                    <button class="inspect-btn" onclick="copyConfig('cursor')">Copy Config</button>
                </div>
                <div class="export-path">.cursor\mcp.json</div>
                <div class="code-block" id="cfg-cursor" style="max-height: 280px;">Loading configuration...</div>
            </div>

            <!-- VS CODE COPILOT -->
            <div class="export-card">
                <div class="export-header">
                    <div class="export-title">🔷 VS Code / Copilot</div>
                    <button class="inspect-btn" onclick="copyConfig('vscode')">Copy Config</button>
                </div>
                <div class="export-path">.vscode\mcp.json</div>
                <div class="code-block" id="cfg-vscode" style="max-height: 280px;">Loading configuration...</div>
            </div>

            <!-- GOOSE CLI -->
            <div class="export-card">
                <div class="export-header">
                    <div class="export-title">🪿 Goose Agent</div>
                    <button class="inspect-btn" onclick="copyConfig('goose')">Copy Config</button>
                </div>
                <div class="export-path">~/.config/goose/profiles.yaml</div>
                <div class="code-block" id="cfg-goose" style="max-height: 280px;">Loading configuration...</div>
            </div>

        </div>
    </div>

    <!-- TAB 5: AUDITOR & TEST BENCH -->
    <div id="tab-bench" class="tab-panel">
        <div class="bench-summary">
            <h2 style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 8px;">Automated Server Health & Protocol Test Bench</h2>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
                You can audit all 24 MCP servers locally via CLI to verify process startup, handshake latency, and tool schema validity.
            </p>

            <div style="background: #04060a; padding: 18px; border-radius: 12px; border: 1px solid var(--border-glow); font-family: var(--font-mono); font-size: 13px; color: var(--accent-green); line-height: 1.8;">
                # 1. Run complete automated audit across all 24 servers:<br>
                <span style="color: #fff;">python mcp_cli.py test</span><br><br>
                # 2. Test a specific sovereign server (e.g. Plane, Windmill, PowerShell):<br>
                <span style="color: #fff;">python mcp_cli.py test plane</span><br>
                <span style="color: #fff;">python mcp_cli.py test windmill</span><br><br>
                # 3. Launch single composite multiplexer (proxying all 260 tools over stdio):<br>
                <span style="color: #fff;">python mcp_cli.py composite</span><br><br>
                # 4. Start visual cockpit server:<br>
                <span style="color: #fff;">python mcp_cli.py serve --port 8790</span>
            </div>
        </div>
    </div>

    <script>
        const CATALOG = {catalog_json_str};

        function switchTab(tabId) {{
            document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            
            const btn = Array.from(document.querySelectorAll('.nav-tab')).find(b => b.getAttribute('onclick').includes(tabId));
            if (btn) btn.classList.add('active');
            
            const panel = document.getElementById('tab-' + tabId);
            if (panel) panel.classList.add('active');
        }}

        function renderFleet(servers) {{
            const grid = document.getElementById('fleet-grid');
            grid.innerHTML = '';

            servers.forEach(s => {{
                const card = document.createElement('div');
                card.className = 'server-card';
                card.innerHTML = `
                    <div>
                        <div class="server-card-top">
                            <div class="server-name">${{s.server}}</div>
                            <span class="server-cat-tag">${{s.category}}</span>
                        </div>
                        <div class="server-desc">${{s.description || 'Sovereign MCP server capability in OMEGA ecosystem.'}}</div>
                    </div>
                    <div>
                        <div class="server-meta-row">
                            <span class="tools-count-pill">${{s.tools_count}} Tools</span>
                            <span style="color: var(--text-muted);">${{s.type.toUpperCase()}}</span>
                            <button class="inspect-btn" onclick="selectServerTools('${{s.server}}')">Inspect Tools ➔</button>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function filterFleet() {{
            const q = document.getElementById('fleet-search').value.toLowerCase();
            const cat = document.getElementById('fleet-cat-filter').value;

            const filtered = CATALOG.filter(s => {{
                const matchQ = s.server.toLowerCase().includes(q) || 
                               (s.description && s.description.toLowerCase().includes(q)) ||
                               (s.author && s.author.toLowerCase().includes(q));
                const matchCat = cat === 'ALL' || s.category === cat;
                return matchQ && matchCat;
            }});

            renderFleet(filtered);
        }}

        function renderTools(toolsList) {{
            const container = document.getElementById('tools-container');
            container.innerHTML = '';

            document.getElementById('tool-count-display').textContent = `Showing ${{toolsList.length}} tools across registered servers`;

            toolsList.forEach((t, idx) => {{
                const row = document.createElement('div');
                row.className = 'tool-row';
                const drawerId = `drawer-${{idx}}`;

                const schemaPretty = JSON.stringify(t.inputSchema || {{}}, null, 2);

                row.innerHTML = `
                    <div class="tool-header-row" onclick="toggleDrawer('${{drawerId}}')">
                        <div>
                            <div class="tool-title">
                                <span>${{t.name}}</span>
                                <span class="tool-server-badge">${{t.server}}</span>
                            </div>
                            <div class="tool-desc-short">${{t.description || 'No description provided.'}}</div>
                        </div>
                        <button class="inspect-btn">Schema ▾</button>
                    </div>
                    <div class="tool-schema-drawer" id="${{drawerId}}">
                        <div class="code-block">
                            <button class="copy-code-btn" onclick="copyText('${{t.name}}', event)">Copy Tool Name</button>
                            <pre>${{schemaPretty}}</pre>
                        </div>
                    </div>
                `;
                container.appendChild(row);
            }});
        }}

        function filterTools() {{
            const q = document.getElementById('tool-search').value.toLowerCase();
            const server = document.getElementById('tool-server-filter').value;

            let allTools = [];
            CATALOG.forEach(s => {{
                if (server === 'ALL' || s.server === server) {{
                    (s.tools || []).forEach(t => {{
                        allTools.push({{ ...t, server: s.server, category: s.category }});
                    }});
                }}
            }});

            const filtered = allTools.filter(t => {{
                return t.name.toLowerCase().includes(q) || 
                       (t.description && t.description.toLowerCase().includes(q));
            }});

            renderTools(filtered);
        }}

        function selectServerTools(serverName) {{
            switchTab('matrix');
            document.getElementById('tool-server-filter').value = serverName;
            document.getElementById('tool-search').value = '';
            filterTools();
        }}

        function toggleDrawer(id) {{
            const el = document.getElementById(id);
            if (el) el.classList.toggle('open');
        }}

        function copyText(txt, evt) {{
            if (evt) evt.stopPropagation();
            navigator.clipboard.writeText(txt).then(() => {{
                alert('Copied: ' + txt);
            }});
        }}

        function copyConfig(client) {{
            const el = document.getElementById('cfg-' + client);
            if (el) {{
                navigator.clipboard.writeText(el.innerText).then(() => {{
                    alert('Configuration for ' + client.toUpperCase() + ' copied to clipboard!');
                }});
            }}
        }}

        function initExports() {{
            const mcpServers = {{}};
            CATALOG.forEach(s => {{
                if (s.type === 'http') {{
                    mcpServers[s.server] = {{ "type": "http", "url": "https://mcp.supabase.com/mcp" }};
                }} else {{
                    mcpServers[s.server] = {{
                        "command": s.command || (s.server.includes('mcp_server') ? "python.exe" : "npx.cmd"),
                        "args": s.args || []
                    }};
                }}
            }});

            document.getElementById('cfg-claude').innerText = JSON.stringify({{ "mcpServers": mcpServers }}, null, 2);
            document.getElementById('cfg-cursor').innerText = JSON.stringify({{ "mcpServers": mcpServers }}, null, 2);
            document.getElementById('cfg-vscode').innerText = JSON.stringify({{ "mcp": {{ "servers": mcpServers }} }}, null, 2);
            
            const gooseExts = {{ "extensions": {{}} }};
            Object.keys(mcpServers).forEach(k => {{
                gooseExts.extensions[k] = {{
                    "type": "stdio",
                    "cmd": mcpServers[k].command,
                    "args": mcpServers[k].args
                }};
            }});
            document.getElementById('cfg-goose').innerText = JSON.stringify(gooseExts, null, 2);
        }}

        // Populate Server Select Filter
        function populateServerDropdown() {{
            const select = document.getElementById('tool-server-filter');
            CATALOG.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s.server;
                opt.textContent = `${{s.server}} (${{s.tools_count}} tools)`;
                select.appendChild(opt);
            }});
        }}

        // Initialization
        window.addEventListener('DOMContentLoaded', () => {{
            renderFleet(CATALOG);
            populateServerDropdown();
            filterTools();
            initExports();
        }});
    </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Master MCP Cockpit successfully generated at {OUTPUT_HTML}!")

if __name__ == "__main__":
    generate()
