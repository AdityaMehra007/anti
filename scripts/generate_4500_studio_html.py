#!/usr/bin/env python3
"""
========================================================================================
BANGALORE 4,500 COMPANIES NON-STOP OUTREACH STUDIO HTML GENERATOR
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Generates the ultra-high-velocity, interactive Non-Stop Outreach Studio web app
at apps/job_application_studio/bangalore_non_stop_outreach_studio.html.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MASTER_JSON = ROOT_DIR / "data" / "bangalore_4500_companies_master.json"
HTML_OUT = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_non_stop_outreach_studio.html"

def generate_studio_html():
    if not MASTER_JSON.exists():
        print(f"[!] Error: {MASTER_JSON} not found. Run compile_4500_non_stop_engine.py first.")
        return False

    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        all_companies = json.load(f)

    # First 100 preview embedded for instant zero-latency rendering
    preview_100 = all_companies[:100]
    preview_json_str = json.dumps(preview_100, separators=(',', ':'))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore 4,500 Companies Non-Stop Outreach Studio | Aditya Mehra</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #07090e;
      --card-bg: #0d121d;
      --card-border: #1e293b;
      --card-hover: #1e293f;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.15);
      --green: #10b981;
      --green-glow: rgba(16, 185, 129, 0.15);
      --gold: #f59e0b;
      --purple: #a855f7;
      --purple-glow: rgba(168, 85, 247, 0.15);
      --rose: #f43f5e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding-bottom: 60px;
    }}

    /* Top sticky navbar */
    .top-nav {{
      background: #0b0f19;
      border-bottom: 1px solid var(--card-border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand h1 {{
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: #fff;
    }}
    .brand span {{
      background: #1e293b;
      color: var(--accent);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}
    .nav-actions {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 6px;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .btn-primary {{ background: #0284c7; color: #fff; }}
    .btn-primary:hover {{ background: #0369a1; }}
    .btn-secondary {{ background: #1e293b; color: #cbd5e1; border-color: #334155; }}
    .btn-secondary:hover {{ background: #334155; color: #fff; }}
    .btn-green {{ background: #065f46; color: #a7f3d0; border-color: #047857; }}
    .btn-green:hover {{ background: #047857; color: #fff; }}
    .btn-purple {{ background: #4c1d95; color: #e9d5ff; border-color: #6d28d9; }}
    .btn-purple:hover {{ background: #6d28d9; color: #fff; }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
    }}

    /* Non-Stop Blitz Control Deck */
    .blitz-deck {{
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 2px solid #38bdf8;
      box-shadow: 0 10px 30px rgba(56, 189, 248, 0.1);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .blitz-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .blitz-title {{
      font-size: 18px;
      font-weight: 800;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .blitz-badge {{
      background: rgba(56, 189, 248, 0.15);
      color: #7dd3fc;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 99px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .progress-bar-wrap {{
      background: #07090e;
      border: 1px solid #1e293b;
      border-radius: 8px;
      height: 10px;
      overflow: hidden;
      margin-bottom: 18px;
    }}
    .progress-bar-fill {{
      background: linear-gradient(90deg, #38bdf8, #10b981);
      height: 100%;
      width: 0%;
      transition: width 0.3s ease;
    }}

    /* Active Target Showcase */
    .target-spotlight {{
      background: #07090e;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 20px;
      display: grid;
      grid-template-columns: 1.5fr 1fr 1.2fr;
      gap: 20px;
      align-items: center;
      margin-bottom: 16px;
    }}
    @media (max-width: 960px) {{
      .target-spotlight {{ grid-template-columns: 1fr; }}
    }}
    .spotlight-comp {{
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }}
    .spotlight-sub {{
      font-size: 12px;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .spotlight-hr {{
      font-size: 14px;
      font-weight: 700;
      color: #e2e8f0;
      margin-bottom: 4px;
    }}
    .spotlight-email {{
      font-size: 12px;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }}
    .spotlight-phone {{
      font-size: 12px;
      color: #34d399;
      font-family: 'JetBrains Mono', monospace;
      margin-top: 2px;
    }}
    .spotlight-actions {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .btn-blitz-fire {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #fff;
      font-size: 14px;
      font-weight: 800;
      padding: 12px 18px;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
      transition: all 0.15s ease;
    }}
    .btn-blitz-fire:hover {{
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
    }}
    .blitz-mini-actions {{
      display: flex;
      gap: 8px;
    }}
    .btn-blitz-sub {{
      flex: 1;
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      font-size: 11px;
      font-weight: 600;
      padding: 8px 10px;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      text-decoration: none;
      transition: background 0.15s;
    }}
    .btn-blitz-sub:hover {{ background: #334155; color: #fff; }}

    /* Stats Grid */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 16px;
    }}
    .stat-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .stat-val {{
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }}
    .stat-val.blue {{ color: var(--accent); }}
    .stat-val.green {{ color: var(--green); }}
    .stat-val.purple {{ color: var(--purple); }}
    .stat-val.gold {{ color: var(--gold); }}

    /* Controls Bar */
    .controls-bar {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .search-row {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .search-input {{
      flex: 1;
      min-width: 280px;
      background: #07090e;
      border: 1px solid #334155;
      color: #fff;
      font-size: 14px;
      padding: 10px 16px;
      border-radius: 8px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{ border-color: var(--accent); }}
    .filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .pill {{
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }}
    .pill:hover {{ background: #334155; color: #fff; }}
    .pill.active {{ background: #0284c7; color: #fff; border-color: var(--accent); }}

    /* Batch toolbar */
    .batch-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #090d16;
      border: 1px solid var(--card-border);
      padding: 12px 18px;
      border-radius: 8px;
      font-size: 12px;
      color: #cbd5e1;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .batch-actions {{
      display: flex;
      gap: 8px;
      align-items: center;
    }}

    /* Cards Grid */
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 18px;
      margin-bottom: 24px;
    }}
    .company-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, border-color 0.15s ease;
      position: relative;
    }}
    .company-card:hover {{
      border-color: #38bdf8;
      transform: translateY(-2px);
    }}
    .company-card.contacted {{
      border-color: rgba(16, 185, 129, 0.4);
      background: rgba(6, 95, 70, 0.08);
    }}
    .card-badge-status {{
      position: absolute;
      top: 16px;
      right: 16px;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .status-queued {{ background: #1e293b; color: #94a3b8; }}
    .status-sent {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }}

    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
      padding-right: 70px;
    }}
    .card-sector {{
      font-size: 11px;
      color: var(--accent);
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .card-corridor {{
      font-size: 12px;
      color: #cbd5e1;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .card-role-box {{
      background: #07090e;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 10px 12px;
      margin-bottom: 14px;
    }}
    .card-role-title {{
      font-size: 12px;
      font-weight: 700;
      color: #e2e8f0;
    }}
    .card-hr-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: #cbd5e1;
      padding: 8px 0;
      border-top: 1px solid #1e293b;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .card-actions {{
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .btn-card-action {{
      flex: 1;
      min-width: 90px;
      font-size: 11px;
      font-weight: 700;
      padding: 8px 10px;
      border-radius: 6px;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
    }}
    .btn-mail {{ background: #0284c7; color: #fff; }}
    .btn-mail:hover {{ background: #0369a1; }}
    .btn-copy {{ background: #1e293b; color: #cbd5e1; border-color: #334155; }}
    .btn-copy:hover {{ background: #334155; color: #fff; }}
    .btn-call {{ background: #1e293b; color: #6ee7b7; border-color: #065f46; }}
    .btn-call:hover {{ background: #065f46; color: #fff; }}
    .btn-linkedin {{ background: #1e293b; color: #93c5fd; border-color: #1e3a8a; }}
    .btn-linkedin:hover {{ background: #1e3a8a; color: #fff; }}
    .btn-toggle-sent {{
      background: #1e293b;
      color: #94a3b8;
      border-color: #334155;
      padding: 8px 10px;
      font-size: 11px;
    }}
    .btn-toggle-sent.active {{
      background: #065f46;
      color: #a7f3d0;
      border-color: #059669;
    }}

    /* Pagination controls */
    .pagination-bar {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      padding: 20px 0;
    }}
    .page-btn {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }}
    .page-btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}
    .page-info {{
      font-size: 13px;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Toast popup */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #10b981;
      color: #064e3b;
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      display: none;
      z-index: 100;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="brand">
      <h1>Bangalore 4,500 Companies Non-Stop Outreach Studio</h1>
      <span id="nav-count">4,500 TARGETS</span>
    </div>
    <div class="nav-actions">
      <a href="../../BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv" download class="btn btn-green">📥 Master CSV (4,500)</a>
      <a href="../candidate_clipboard_assistant.html" target="_blank" class="btn btn-secondary">📋 Clipboard Assistant</a>
      <a href="global_mnc_and_startup_hub.html" class="btn btn-purple">🌐 Global 60 Hub</a>
      <a href="../get_me_hired_dashboard/index.html" class="btn btn-primary">← Back to Dashboard</a>
    </div>
  </nav>

  <div class="container">

    <!-- Non-Stop Blitz Control Deck -->
    <div class="blitz-deck">
      <div class="blitz-header">
        <div class="blitz-title">
          <span>⚡ NON-STOP OUTREACH BLITZ MODE</span>
          <span class="blitz-badge" id="blitz-progress-text">Target 1 of 4,500</span>
        </div>
        <div style="font-size: 12px; color: #94a3b8;">
          <span>Keyboard Shortcut: Press <strong>[Space]</strong> or <strong>[Enter]</strong> to Send & Next</span>
        </div>
      </div>

      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" id="blitz-progress-bar"></div>
      </div>

      <!-- Active Spotlight Card -->
      <div class="target-spotlight" id="spotlight-card">
        <div>
          <div class="spotlight-comp" id="spot-comp">Loading Target...</div>
          <div class="spotlight-sub">
            <span style="color: #38bdf8;" id="spot-sector">Sector</span>
            <span>•</span>
            <span id="spot-corridor">Corridor</span>
          </div>
          <div style="margin-top: 10px; font-size: 12px; color: #e2e8f0;">
            <strong>Target Role:</strong> <span id="spot-role" style="color: #34d399;">Operations Analyst</span>
          </div>
        </div>

        <div>
          <div class="spotlight-hr" id="spot-hr">HR Lead Name</div>
          <div style="font-size: 11px; color: #94a3b8; margin-bottom: 4px;" id="spot-desig">Designation</div>
          <div class="spotlight-email" id="spot-email">email@domain.com</div>
          <div class="spotlight-phone" id="spot-phone">+91-80-00000000</div>
        </div>

        <div class="spotlight-actions">
          <button class="btn-blitz-fire" onclick="fireBlitzCurrent()">
            <span>✉️ Send Email & Next Target</span>
            <span>➔</span>
          </button>
          <div class="blitz-mini-actions">
            <button class="btn-blitz-sub" onclick="copyCurrentPitch()">📋 Copy Pitch</button>
            <a id="spot-call-btn" href="#" class="btn-blitz-sub" style="color: #6ee7b7;">📞 Call Desk</a>
            <a id="spot-linkedin-btn" href="#" target="_blank" class="btn-blitz-sub" style="color: #93c5fd;">💼 LinkedIn</a>
            <button class="btn-blitz-sub" onclick="skipBlitzTarget()">⏭️ Skip</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Verified Targets</div>
        <div class="stat-val blue" id="stat-total">4,500</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Contacted So Far</div>
        <div class="stat-val green" id="stat-contacted">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Pending Queued</div>
        <div class="stat-val gold" id="stat-pending">4,500</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Outer Ring Road (ORR)</div>
        <div class="stat-val purple">1,200+</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Whitefield Corridor</div>
        <div class="stat-val blue">950+</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Sales Exposure Risk</div>
        <div class="stat-val green">0% (EXCLUDED)</div>
      </div>
    </div>

    <!-- Controls Bar -->
    <div class="controls-bar">
      <div class="search-row">
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Instant search 4,500 companies by name, HR lead, corridor (e.g. ORR, Whitefield, E-City), sector, or role..." oninput="handleSearch()">
      </div>

      <div class="filter-pills" id="corridor-pills">
        <span class="pill active" onclick="setCorridorFilter('all')">All Corridors (4,500)</span>
        <span class="pill" onclick="setCorridorFilter('orr')">Outer Ring Road (1,200+)</span>
        <span class="pill" onclick="setCorridorFilter('whitefield')">Whitefield & ITPL (950+)</span>
        <span class="pill" onclick="setCorridorFilter('ecity')">Electronic City (850+)</span>
        <span class="pill" onclick="setCorridorFilter('manyata')">Manyata & Hebbal (600+)</span>
        <span class="pill" onclick="setCorridorFilter('koramangala')">Koramangala & HSR (500+)</span>
        <span class="pill" onclick="setCorridorFilter('cbd')">CBD & MG Road (400+)</span>
      </div>

      <div class="batch-bar">
        <div>
          <span>Showing <strong id="filter-count" style="color: #fff;">4,500</strong> matching companies</span>
          <span style="margin: 0 8px; color: #475569;">|</span>
          <span>Page <strong id="page-current" style="color: #38bdf8;">1</strong> of <strong id="page-total">90</strong></span>
        </div>
        <div class="batch-actions">
          <button class="btn btn-secondary" style="font-size: 11px;" onclick="openNextBatch(5)">⚡ Open Next 5 Emails</button>
          <button class="btn btn-secondary" style="font-size: 11px;" onclick="markPageSent()">✅ Mark Page as Sent</button>
          <button class="btn btn-secondary" style="font-size: 11px;" onclick="exportContactedList()">📥 Export Contacted List</button>
        </div>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="cards-grid" id="cards-container"></div>

    <!-- Pagination Controls -->
    <div class="pagination-bar">
      <button class="page-btn" id="btn-prev" onclick="changePage(-1)">← Previous</button>
      <span class="page-info" id="pagination-text">Page 1 of 90</span>
      <button class="page-btn" id="btn-next" onclick="changePage(1)">Next →</button>
    </div>

  </div>

  <div class="toast" id="toast">Copied to clipboard!</div>

  <script>
    // Initial preview data (first 100 loaded synchronously)
    let allCompanies = {preview_json_str};
    let filteredCompanies = allCompanies;
    let contactedIds = new Set(JSON.parse(localStorage.getItem('adi_contacted_ids') || '[]'));
    let blitzIndex = 0;
    let currentPage = 1;
    const pageSize = 50;
    let currentCorridor = 'all';

    const CANDIDATE = {{
      name: "Aditya Mehra",
      phone: "+91-7003456624",
      email: "adityamehra799@gmail.com",
      degree: "BBA in International Business",
      univ: "Dayananda Sagar University (DSU), Bengaluru",
      year: "2026"
    }};

    // Asynchronously fetch full 4,500 dataset in background
    async function loadFullDataset() {{
      try {{
        const res = await fetch('../../data/bangalore_4500_companies_master.json');
        if (res.ok) {{
          allCompanies = await res.json();
          document.getElementById('nav-count').innerText = allCompanies.length.toLocaleString() + ' TARGETS';
          document.getElementById('stat-total').innerText = allCompanies.length.toLocaleString();
          applyFilters();
        }}
      }} catch (err) {{
        console.warn('Background fetch of full 4500 JSON failed, using preview:', err);
      }}
    }}

    function generatePitch(c) {{
      const salutation = (c.hr_name && c.hr_name.toLowerCase() !== 'talent acquisition') ? `Dear ${{c.hr_name.split(' ')[0]}},` : `Dear ${{c.company}} Hiring Team,`;
      const subject = `Application: ${{c.target_role}} - ${{CANDIDATE.name}} (BBA DSU '26)`;
      const body = `${{salutation}}

I hope this email finds you well.

I am writing to express my strong interest in early-career ${{c.target_role}} openings at ${{c.company}} in Bengaluru.

I will graduate with a ${{CANDIDATE.degree}} from ${{CANDIDATE.univ}} in ${{CANDIDATE.year}}. My operational background is anchored entirely in verified on-ground execution:

1. Operations & Logistics Rigor: Lead Coordinator at AERO India 2025 (Yelahanka Air Force Base) and brand activations for Puma India and Tata Communications across 300+ field deployments.
2. Vendor Governance & SLA Enforcement: Structured Tier-1 supplier rate cards and enforced milestone delivery contracts with zero operational slippage.
3. Commercial Execution & Process Coordination: Drove enterprise client operations, compressed proposal turnaround from 7 days to 48 hours, and executed milestone handovers.
4. Technical & Trade Foundations: Managed AI data curation at Instawork AI (99%+ QA benchmark) and possess working proficiency in Incoterms 2020 rules and international documentation compliance.

Given ${{c.company}}'s footprint in Bengaluru, I am eager to contribute hands-on operational grit, vendor discipline, and analytical problem-solving to your team.

My resume is attached for your review. I would welcome an introductory 10-minute conversation at your convenience.

Thank you very much for your time and consideration.

Warm regards,

${{CANDIDATE.name}}
Bengaluru, Karnataka, India
Phone: ${{CANDIDATE.phone}}
Email: ${{CANDIDATE.email}}
LinkedIn: https://www.linkedin.com/in/aditya-mehra
`;
      return {{ subject, body }};
    }}

    function getMailtoUrl(c) {{
      const p = generatePitch(c);
      const ccPart = (c.careers_email && c.careers_email !== c.hr_email) ? `&cc=${{encodeURIComponent(c.careers_email)}}` : '';
      return `mailto:${{c.hr_email}}?subject=${{encodeURIComponent(p.subject)}}&body=${{encodeURIComponent(p.body)}}${{ccPart}}`;
    }}

    function setCorridorFilter(corr) {{
      currentCorridor = corr;
      document.querySelectorAll('#corridor-pills .pill').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      applyFilters();
    }}

    function handleSearch() {{
      applyFilters();
    }}

    function applyFilters() {{
      const q = document.getElementById('search-box').value.toLowerCase().trim();
      filteredCompanies = allCompanies.filter(c => {{
        let matchesCorr = true;
        const corrStr = (c.corridor || '').toLowerCase();
        if (currentCorridor === 'orr') matchesCorr = corrStr.includes('outer ring road') || corrStr.includes('bellandur') || corrStr.includes('sarjapur');
        else if (currentCorridor === 'whitefield') matchesCorr = corrStr.includes('whitefield') || corrStr.includes('itpl') || corrStr.includes('epip');
        else if (currentCorridor === 'ecity') matchesCorr = corrStr.includes('electronic city');
        else if (currentCorridor === 'manyata') matchesCorr = corrStr.includes('manyata') || corrStr.includes('hebbal') || corrStr.includes('nagawara');
        else if (currentCorridor === 'koramangala') matchesCorr = corrStr.includes('koramangala') || corrStr.includes('hsr');
        else if (currentCorridor === 'cbd') matchesCorr = corrStr.includes('mg road') || corrStr.includes('cbd') || corrStr.includes('indiranagar');

        const text = (c.company + ' ' + c.hr_name + ' ' + c.sector + ' ' + c.corridor + ' ' + c.target_role + ' ' + c.hr_email).toLowerCase();
        const matchesQ = !q || text.includes(q);

        return matchesCorr && matchesQ;
      }});

      currentPage = 1;
      updateStats();
      renderPage();
      updateBlitzDeck();
    }}

    function updateStats() {{
      const total = allCompanies.length;
      const contacted = contactedIds.size;
      const pending = Math.max(0, total - contacted);

      document.getElementById('stat-contacted').innerText = contacted.toLocaleString();
      document.getElementById('stat-pending').innerText = pending.toLocaleString();
      document.getElementById('filter-count').innerText = filteredCompanies.length.toLocaleString();

      const pct = total ? Math.min(100, Math.round((contacted / total) * 100)) : 0;
      document.getElementById('blitz-progress-bar').style.width = pct + '%';
      document.getElementById('blitz-progress-text').innerText = `Target ${{blitzIndex + 1}} of ${{allCompanies.length}} (${{contacted}} Contacted • ${{pct}}%)`;
    }}

    function updateBlitzDeck() {{
      if (!allCompanies.length) return;
      if (blitzIndex >= allCompanies.length) blitzIndex = 0;
      const c = allCompanies[blitzIndex];

      document.getElementById('spot-comp').innerText = c.company;
      document.getElementById('spot-sector').innerText = c.sector;
      document.getElementById('spot-corridor').innerText = '📍 ' + c.corridor;
      document.getElementById('spot-role').innerText = c.target_role;
      document.getElementById('spot-hr').innerText = c.hr_name;
      document.getElementById('spot-desig').innerText = c.designation;
      document.getElementById('spot-email').innerText = c.hr_email;
      document.getElementById('spot-phone').innerText = c.phone;
      document.getElementById('spot-call-btn').href = 'tel:' + c.phone;
      document.getElementById('spot-linkedin-btn').href = c.linkedin_url;
    }}

    function fireBlitzCurrent() {{
      if (!allCompanies.length) return;
      const c = allCompanies[blitzIndex];
      window.location.href = getMailtoUrl(c);
      toggleContacted(c.id, true);
      blitzIndex++;
      updateStats();
      updateBlitzDeck();
      renderPage();
    }}

    function skipBlitzTarget() {{
      blitzIndex++;
      updateStats();
      updateBlitzDeck();
    }}

    function copyCurrentPitch() {{
      if (!allCompanies.length) return;
      const c = allCompanies[blitzIndex];
      const p = generatePitch(c);
      copyText(`To: ${{c.hr_email}}\\nSubject: ${{p.subject}}\\n\\n${{p.body}}`, 'Full Email Pitch Copied!');
    }}

    function toggleContacted(id, forceValue) {{
      if (forceValue === true) contactedIds.add(id);
      else if (forceValue === false) contactedIds.delete(id);
      else {{
        if (contactedIds.has(id)) contactedIds.delete(id);
        else contactedIds.add(id);
      }}
      localStorage.setItem('adi_contacted_ids', JSON.stringify([...contactedIds]));
      updateStats();
      renderPage();
    }}

    function openNextBatch(count) {{
      const uncontacted = filteredCompanies.filter(c => !contactedIds.has(c.id)).slice(0, count);
      if (!uncontacted.length) {{
        showToast('All visible companies have already been contacted!');
        return;
      }}
      uncontacted.forEach((c, i) => {{
        setTimeout(() => {{
          window.open(getMailtoUrl(c), '_blank');
          toggleContacted(c.id, true);
        }}, i * 200);
      }});
      showToast(`Triggered ${{uncontacted.length}} outreach drafts!`);
    }}

    function markPageSent() {{
      const start = (currentPage - 1) * pageSize;
      const pageItems = filteredCompanies.slice(start, start + pageSize);
      pageItems.forEach(c => contactedIds.add(c.id));
      localStorage.setItem('adi_contacted_ids', JSON.stringify([...contactedIds]));
      updateStats();
      renderPage();
      showToast(`Marked ${{pageItems.length}} companies on Page ${{currentPage}} as sent!`);
    }}

    function exportContactedList() {{
      const contactedItems = allCompanies.filter(c => contactedIds.has(c.id));
      if (!contactedItems.length) {{
        showToast('No companies marked as contacted yet.');
        return;
      }}
      const csvContent = "data:text/csv;charset=utf-8," + 
        ["ID,Company,HR Lead,Email,Phone,Corridor,Sector,Target Role"].concat(
          contactedItems.map(c => `"${{c.id}}","${{c.company}}","${{c.hr_name}}","${{c.hr_email}}","${{c.phone}}","${{c.corridor}}","${{c.sector}}","${{c.target_role}}"`)
        ).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `ADI_CONTACTED_COMPANIES_${{new Date().toISOString().slice(0,10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    function renderPage() {{
      const container = document.getElementById('cards-container');
      const totalPages = Math.ceil(filteredCompanies.length / pageSize) || 1;
      if (currentPage > totalPages) currentPage = totalPages;

      document.getElementById('page-current').innerText = currentPage;
      document.getElementById('page-total').innerText = totalPages;
      document.getElementById('pagination-text').innerText = `Page ${{currentPage}} of ${{totalPages}}`;
      document.getElementById('btn-prev').disabled = (currentPage <= 1);
      document.getElementById('btn-next').disabled = (currentPage >= totalPages);

      const start = (currentPage - 1) * pageSize;
      const pageItems = filteredCompanies.slice(start, start + pageSize);

      if (!pageItems.length) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 50px; color: #94a3b8; font-size: 15px;">No companies matched your search query. Try another keyword.</div>`;
        return;
      }}

      container.innerHTML = pageItems.map(c => {{
        const isSent = contactedIds.has(c.id);
        return `
        <div class="company-card ${{isSent ? 'contacted' : ''}}">
          <span class="card-badge-status ${{isSent ? 'status-sent' : 'status-queued'}}">
            ${{isSent ? '✓ CONTACTED' : 'QUEUED'}}
          </span>

          <div>
            <div class="card-title">${{c.company}}</div>
            <div class="card-sector">${{c.sector}}</div>
            <div class="card-corridor">📍 ${{c.corridor}}</div>

            <div class="card-role-box">
              <div class="card-role-title">🎯 ${{c.target_role}}</div>
              <div style="font-size: 11px; color: #38bdf8; margin-top: 2px;">Candidate Fit Score: ${{c.fit_score}}% Match</div>
            </div>

            <div class="card-hr-row">
              <div>
                <div style="font-weight: 700; color: #fff;">${{c.hr_name}}</div>
                <div style="color: #64748b; font-size: 10px;">${{c.designation}}</div>
                <div style="color: #38bdf8; font-size: 11px; font-family: monospace;">${{c.hr_email}}</div>
              </div>
              <div style="font-family: monospace; color: #34d399;">
                ${{c.phone}}
              </div>
            </div>
          </div>

          <div class="card-actions">
            <a href="${{getMailtoUrl(c)}}" class="btn-card-action btn-mail">✉️ Email</a>
            <button class="btn-card-action btn-copy" onclick="copyCardPitch('${{c.id}}')">📋 Pitch</button>
            <a href="tel:${{c.phone}}" class="btn-card-action btn-call">📞 Call</a>
            <a href="${{c.linkedin_url}}" target="_blank" class="btn-card-action btn-linkedin">💼 LinkedIn</a>
            <button class="btn-card-action btn-toggle-sent ${{isSent ? 'active' : ''}}" onclick="toggleContacted('${{c.id}}')">
              ${{isSent ? '✓ Sent' : '+ Mark'}}
            </button>
          </div>
        </div>
        `;
      }}).join('');
    }}

    function copyCardPitch(id) {{
      const c = allCompanies.find(x => x.id === id);
      if (!c) return;
      const p = generatePitch(c);
      copyText(`To: ${{c.hr_email}}\\nSubject: ${{p.subject}}\\n\\n${{p.body}}`, 'Email Pitch Copied to Clipboard!');
    }}

    function changePage(delta) {{
      currentPage += delta;
      renderPage();
      window.scrollTo({{ top: 400, behavior: 'smooth' }});
    }}

    function copyText(text, msg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(msg);
      }});
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 2200);
    }}

    // Keyboard shortcut for Blitz mode
    document.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'INPUT') return;
      if (e.code === 'Space' || e.code === 'Enter') {{
        e.preventDefault();
        fireBlitzCurrent();
      }}
    }});

    window.onload = () => {{
      updateStats();
      renderPage();
      updateBlitzDeck();
      loadFullDataset();
    }};
  </script>
</body>
</html>
"""

    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html_content, encoding="utf-8")
    print(f"[OK] Generated Non-Stop Outreach Studio at {HTML_OUT}")
    return True

if __name__ == "__main__":
    generate_studio_html()
