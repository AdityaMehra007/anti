#!/usr/bin/env python3
r"""
========================================================================================
ADITYA MEHRA EXECUTIVE COMMAND CENTER BUILDER
========================================================================================
Builds a standalone, offline, master executive cockpit:
`e:\anti\ADITYA_MEHRA_EXECUTIVE_COMMAND_CENTER.html`
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
OUTPUT_HTML = ROOT_DIR / "ADITYA_MEHRA_EXECUTIVE_COMMAND_CENTER.html"
BATTLECARDS_DIR = ROOT_DIR / "atlas-global" / "battlecards"
PROPOSALS_DIR = ROOT_DIR / "atlas-global" / "proposals"

def build_command_center():
    print("=" * 80)
    print("  BUILDING ADITYA MEHRA MASTER EXECUTIVE COMMAND CENTER")
    print("=" * 80)

    # Read Battlecards
    battlecards = []
    for f in sorted(BATTLECARDS_DIR.glob("BC-*.md")):
        with open(f, "r", encoding="utf-8") as fp:
            battlecards.append({"filename": f.name, "content": fp.read()})

    # Read Proposals
    proposals = []
    for f in sorted(PROPOSALS_DIR.glob("PROPOSAL_*.md")):
        with open(f, "r", encoding="utf-8") as fp:
            proposals.append({"filename": f.name, "content": fp.read()})

    bc_json = json.dumps(battlecards)
    prop_json = json.dumps(proposals)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya Mehra | Executive Career & Operational Intelligence Cockpit</title>
    <style>
        :root {{
            --bg-main: #090D16;
            --bg-card: #111827;
            --border: #1F2937;
            --text-main: #F9FAFB;
            --text-muted: #9CA3AF;
            --accent-cyan: #38BDF8;
            --accent-emerald: #10B981;
            --accent-indigo: #818CF8;
            --accent-amber: #F59E0B;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background: var(--bg-main); color: var(--text-main); line-height: 1.6; padding: 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: flex-start; padding-bottom: 24px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }}
        .title h1 {{ font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #fff; }}
        .title p {{ font-size: 14px; color: var(--text-muted); margin-top: 6px; }}
        .badge-bar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }}
        .badge {{ background: rgba(56, 189, 248, 0.12); color: var(--accent-cyan); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.3); }}
        .badge-green {{ background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3); }}
        
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }}
        .kpi-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px; }}
        .kpi-title {{ font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--text-muted); letter-spacing: 0.5px; }}
        .kpi-val {{ font-size: 26px; font-weight: 800; margin-top: 6px; color: #fff; }}
        .kpi-sub {{ font-size: 11px; color: var(--accent-emerald); margin-top: 4px; font-weight: 600; }}

        .tabs {{ display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
        .tab-btn {{ background: transparent; border: none; color: var(--text-muted); font-size: 14px; font-weight: 700; padding: 8px 16px; border-radius: 6px; cursor: pointer; }}
        .tab-btn.active {{ background: var(--border); color: var(--accent-cyan); }}

        .viewer-container {{ display: grid; grid-template-columns: 320px 1fr; gap: 20px; height: calc(100vh - 360px); min-height: 550px; }}
        .sidebar {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; overflow-y: auto; padding: 12px; }}
        .sidebar-item {{ padding: 10px 14px; border-radius: 8px; cursor: pointer; margin-bottom: 6px; font-size: 13px; font-weight: 600; color: #D1D5DB; transition: all 0.15s; }}
        .sidebar-item:hover {{ background: rgba(255, 255, 255, 0.05); color: #fff; }}
        .sidebar-item.selected {{ background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan); border-left: 3px solid var(--accent-cyan); }}
        
        .content-pane {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; overflow-y: auto; padding: 28px; font-size: 14px; }}
        .content-pane pre {{ white-space: pre-wrap; font-family: monospace; font-size: 12.5px; color: #E5E7EB; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            <h1>ADITYA MEHRA | Executive Career & Operational Cockpit</h1>
            <p>BBA International Business (Dayananda Sagar University '26, CGPA: 6.33) | Global SCM, EXIM & Operational Leadership</p>
            <div class="badge-bar">
                <span class="badge badge-green">● Operational Lead: Aero India 2025</span>
                <span class="badge">● Puma Sports India: Brand Operations</span>
                <span class="badge">● Tata Communications: Asset Reconciliation</span>
                <span class="badge badge-green">● 100% Verified Evidence</span>
            </div>
        </div>
        <div>
            <a href="atlas-global/dashboards/atlas_dashboard.html" target="_blank" style="background: #1E293B; color: var(--accent-cyan); text-decoration: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; border: 1px solid var(--border); display: inline-block;">Open Atlas Live Data Lake ↗</a>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Interview Battlecards</div>
            <div class="kpi-val">20 Enterprises</div>
            <div class="kpi-sub">Top Bengaluru GCCs & Unicorns</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">30-60-90 Day Proposals</div>
            <div class="kpi-val">5 Master Plans</div>
            <div class="kpi-sub">Target Role Execution Plans</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Target Compensation</div>
            <div class="kpi-val">₹7.5L - ₹18.0L</div>
            <div class="kpi-sub">Audited Market Benchmarks</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Mapped Data Lake</div>
            <div class="kpi-val">7,721 Companies</div>
            <div class="kpi-sub">13,300 Decision-Makers</div>
        </div>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchSection('battlecards')">🎯 Executive Interview Battlecards (20)</button>
        <button class="tab-btn" onclick="switchSection('proposals')">📄 30-60-90 Day Operational Proposals (5)</button>
    </div>

    <!-- Battlecards Section -->
    <div id="battlecardsSection" class="viewer-container">
        <div class="sidebar" id="bcSidebar"></div>
        <div class="content-pane" id="bcContent">
            <pre id="bcText">Select a battlecard on the left to inspect operational intelligence, pain points, and interview scripts.</pre>
        </div>
    </div>

    <!-- Proposals Section -->
    <div id="proposalsSection" class="viewer-container hidden">
        <div class="sidebar" id="propSidebar"></div>
        <div class="content-pane" id="propContent">
            <pre id="propText">Select a proposal on the left to view the complete 30-60-90 day value creation plan.</pre>
        </div>
    </div>

    <script>
        const battlecards = {bc_json};
        const proposals = {prop_json};

        function switchSection(sec) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            if (sec === 'battlecards') {{
                document.getElementById('battlecardsSection').classList.remove('hidden');
                document.getElementById('proposalsSection').classList.add('hidden');
            }} else {{
                document.getElementById('battlecardsSection').classList.add('hidden');
                document.getElementById('proposalsSection').classList.remove('hidden');
            }}
        }}

        // Render Battlecards Sidebar
        const bcSidebar = document.getElementById('bcSidebar');
        battlecards.forEach((bc, idx) => {{
            const div = document.createElement('div');
            div.className = 'sidebar-item' + (idx === 0 ? ' selected' : '');
            div.textContent = bc.filename.replace('BC-', '').replace('.md', '').replaceAll('_', ' ').toUpperCase();
            div.onclick = () => {{
                document.querySelectorAll('#bcSidebar .sidebar-item').forEach(el => el.classList.remove('selected'));
                div.classList.add('selected');
                document.getElementById('bcText').textContent = bc.content;
            }};
            bcSidebar.appendChild(div);
        }});
        if (battlecards.length > 0) {{
            document.getElementById('bcText').textContent = battlecards[0].content;
        }}

        // Render Proposals Sidebar
        const propSidebar = document.getElementById('propSidebar');
        proposals.forEach((p, idx) => {{
            const div = document.createElement('div');
            div.className = 'sidebar-item' + (idx === 0 ? ' selected' : '');
            div.textContent = p.filename.replace('PROPOSAL_', '').replace('.md', '').replaceAll('_', ' ');
            div.onclick = () => {{
                document.querySelectorAll('#propSidebar .sidebar-item').forEach(el => el.classList.remove('selected'));
                div.classList.add('selected');
                document.getElementById('propText').textContent = p.content;
            }};
            propSidebar.appendChild(div);
        }});
        if (proposals.length > 0) {{
            document.getElementById('propText').textContent = proposals[0].content;
        }}
    </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  [+] Master Executive Command Center built: {OUTPUT_HTML}")
    print("=" * 80)

if __name__ == "__main__":
    build_command_center()
