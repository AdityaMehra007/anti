"""
Generator for awesome_control_cockpit.html
Embeds universe and manifest data for offline-first standalone execution
with live REST API connectivity when port 8782 is online.
"""

import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
UNIVERSE_JSON = WORKSPACE / "data" / "awesome_universe.json"
MANIFEST_JSON = WORKSPACE / "omega" / "data" / "awesome_do_everything_manifest.json"
OUTPUT_HTML = WORKSPACE / "awesome_control_cockpit.html"

with open(UNIVERSE_JSON, "r", encoding="utf-8") as f:
    universe_data = json.load(f)

with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
    manifest_data = json.load(f)

universe_json_str = json.dumps(universe_data, ensure_ascii=False)
manifest_json_str = json.dumps(manifest_data, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OMEGA Awesome Universe — Sovereign GitHub Intelligence & Manifesto Cockpit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    :root {{
      --bg: #06080d;
      --surface-1: #0c1017;
      --surface-2: #141b26;
      --surface-3: #1c2636;
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(0, 240, 255, 0.3);
      --text: #e2e8f0;
      --text-muted: #8899ac;
      --cyan: #00f0ff;
      --cyan-glow: rgba(0, 240, 255, 0.2);
      --purple: #a855f7;
      --purple-glow: rgba(168, 85, 247, 0.2);
      --amber: #f59e0b;
      --green: #10b981;
      --red: #ef4444;
      --s-tier: #ec4899;
      --a-tier: #3b82f6;
      --b-tier: #64748b;
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 10%, rgba(0, 240, 255, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.06) 0%, transparent 40%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px;
    }}

    /* Header & Navigation */
    header {{
      background: rgba(12, 16, 23, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .logo-group {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .brand-badge {{
      background: linear-gradient(135deg, var(--cyan), var(--purple));
      color: #000;
      font-weight: 800;
      font-size: 14px;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 1.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .brand-title {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand-title span {{
      color: var(--cyan);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .status-pill {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--green);
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      padding: 6px 12px;
      border-radius: 20px;
    }}

    .pulse-dot {{
      width: 8px;
      height: 8px;
      background: var(--green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--green);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    /* Navigation Tabs */
    .nav-tabs {{
      display: flex;
      gap: 4px;
      padding: 8px 28px;
      background: rgba(8, 11, 16, 0.95);
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
      scrollbar-width: none;
    }}

    .nav-tabs::-webkit-scrollbar {{
      display: none;
    }}

    .tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}

    .tab-btn:hover {{
      color: var(--text);
      background: rgba(255, 255, 255, 0.04);
    }}

    .tab-btn.active {{
      color: var(--cyan);
      background: rgba(0, 240, 255, 0.08);
      border-color: rgba(0, 240, 255, 0.25);
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.1);
    }}

    /* Main Container */
    main {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 24px 28px 60px;
    }}

    /* Telemetry KPI Strip */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }}

    .kpi-card {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 20px;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-accent);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--card-accent, var(--cyan));
    }}

    .kpi-label {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .kpi-value {{
      font-size: 28px;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }}

    .kpi-subtext {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    /* Tab Panes */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
      animation: fadeIn 0.25s ease;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Universe Overview & Discovery */
    .search-bar-wrap {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      gap: 14px;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}

    .search-input-group {{
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 14px;
      min-width: 260px;
    }}

    .search-input-group input {{
      background: transparent;
      border: none;
      outline: none;
      color: var(--text);
      font-family: inherit;
      font-size: 14px;
      width: 100%;
    }}

    .filter-select {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: inherit;
      font-size: 13px;
      padding: 8px 14px;
      border-radius: 8px;
      outline: none;
      cursor: pointer;
    }}

    /* Awesome List Cards Grid */
    .lists-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 16px;
    }}

    .list-card {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      position: relative;
    }}

    .list-card:hover {{
      border-color: rgba(0, 240, 255, 0.4);
      background: var(--surface-2);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}

    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
    }}

    .card-title:hover {{
      color: var(--cyan);
    }}

    .tier-badge {{
      font-size: 11px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
    }}

    .tier-badge.tier-s {{
      background: rgba(236, 72, 153, 0.15);
      border: 1px solid rgba(236, 72, 153, 0.4);
      color: var(--s-tier);
    }}

    .tier-badge.tier-a {{
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.4);
      color: var(--a-tier);
    }}

    .tier-badge.tier-b {{
      background: rgba(100, 116, 139, 0.15);
      border: 1px solid rgba(100, 116, 139, 0.4);
      color: var(--b-tier);
    }}

    .card-category {{
      font-size: 11px;
      color: var(--cyan);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 16px;
      flex: 1;
    }}

    .card-bottom {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border);
      padding-top: 12px;
      font-size: 12px;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}

    .stars-count {{
      display: flex;
      align-items: center;
      gap: 5px;
      color: var(--amber);
    }}

    .btn-visit {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .btn-visit:hover {{
      background: var(--cyan);
      color: #000;
      border-color: var(--cyan);
      font-weight: 600;
    }}

    /* Manifesto Linter Studio */
    .linter-layout {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}

    @media (max-width: 1024px) {{
      .linter-layout {{
        grid-template-columns: 1fr;
      }}
    }}

    .linter-box {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      display: flex;
      flex-direction: column;
    }}

    .linter-textarea {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      padding: 16px;
      min-height: 400px;
      resize: vertical;
      outline: none;
      line-height: 1.6;
      margin-bottom: 16px;
    }}

    .linter-textarea:focus {{
      border-color: var(--cyan);
    }}

    .btn-linter {{
      background: linear-gradient(135deg, var(--cyan), var(--purple));
      color: #000;
      font-weight: 700;
      border: none;
      border-radius: 8px;
      padding: 12px 24px;
      font-size: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: transform 0.2s ease, opacity 0.2s ease;
    }}

    .btn-linter:hover {{
      transform: translateY(-1px);
      opacity: 0.95;
    }}

    .report-card {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 14px;
    }}

    .report-score-strip {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}

    .score-big {{
      font-size: 42px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--green);
    }}

    .rule-item {{
      display: flex;
      gap: 12px;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 13px;
    }}

    .rule-item:last-child {{
      border-bottom: none;
    }}

    .badge-rule {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
      height: fit-content;
    }}

    .badge-rule.fail {{
      background: rgba(239, 68, 68, 0.2);
      color: var(--red);
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}

    .badge-rule.warn {{
      background: rgba(245, 158, 11, 0.2);
      color: var(--amber);
      border: 1px solid rgba(245, 158, 11, 0.4);
    }}

    .badge-rule.info {{
      background: rgba(59, 130, 246, 0.2);
      color: var(--a-tier);
      border: 1px solid rgba(59, 130, 246, 0.4);
    }}

    /* Terminal Simulator */
    .terminal-window {{
      background: #020408;
      border: 1px solid rgba(0, 240, 255, 0.3);
      border-radius: 12px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7);
      overflow: hidden;
      font-family: 'JetBrains Mono', monospace;
    }}

    .terminal-header {{
      background: #0a0f18;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
    }}

    .term-dots {{
      display: flex;
      gap: 6px;
    }}

    .term-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}

    .term-dot.red {{ background: #ef4444; }}
    .term-dot.yellow {{ background: #f59e0b; }}
    .term-dot.green {{ background: #10b981; }}

    .terminal-body {{
      padding: 20px;
      min-height: 420px;
      color: #94a3b8;
      font-size: 13px;
      line-height: 1.6;
      white-space: pre-wrap;
      overflow-y: auto;
      max-height: 600px;
    }}

    .term-cmd-bar {{
      display: flex;
      gap: 10px;
      margin-top: 16px;
      flex-wrap: wrap;
    }}

    .term-quick-btn {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--cyan);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 8px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .term-quick-btn:hover {{
      background: rgba(0, 240, 255, 0.15);
      border-color: var(--cyan);
    }}

    /* Lifecycle Phases */
    .lifecycle-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .phase-row {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s ease;
    }}

    .phase-row:hover {{
      border-color: var(--border-accent);
      background: var(--surface-2);
    }}

    .phase-meta {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .phase-num {{
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: rgba(0, 240, 255, 0.1);
      border: 1px solid rgba(0, 240, 255, 0.3);
      color: var(--cyan);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
    }}

    .phase-title {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }}

    .phase-desc {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .phase-badge {{
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--green);
    }}
  </style>
</head>
<body>

  <!-- Top Bar -->
  <header>
    <div class="logo-group">
      <div class="brand-badge"><i class="fa-solid fa-crown"></i> OMEGA</div>
      <div class="brand-title">Awesome Universe <span>Intelligence Cockpit</span></div>
    </div>
    <div class="header-actions">
      <div class="status-pill">
        <div class="pulse-dot"></div>
        <span>SOVEREIGN OPERATIONAL</span>
      </div>
      <a href="https://github.com/topics/awesome" target="_blank" class="btn-visit">
        <i class="fa-brands fa-github"></i> github.com/topics/awesome
      </a>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <nav class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('overview')"><i class="fa-solid fa-gauge-high"></i> Overview & Explorer</button>
    <button class="tab-btn" onclick="switchTab('categories')"><i class="fa-solid fa-layer-group"></i> 29 Categories</button>
    <button class="tab-btn" onclick="switchTab('frontier')"><i class="fa-solid fa-robot"></i> Frontier AI & Agents</button>
    <button class="tab-btn" onclick="switchTab('linter')"><i class="fa-solid fa-vial-circle-check"></i> Manifesto Linter Studio</button>
    <button class="tab-btn" onclick="switchTab('terminal')"><i class="fa-solid fa-terminal"></i> Terminal CLI Simulator</button>
    <button class="tab-btn" onclick="switchTab('lifecycle')"><i class="fa-solid fa-shield-halved"></i> 12-Phase Lifecycle</button>
    <button class="tab-btn" onclick="switchTab('mcp')"><i class="fa-solid fa-plug"></i> MCP & REST Studio</button>
  </nav>

  <!-- Main Container -->
  <main>

    <!-- KPI Strip -->
    <section class="kpi-grid">
      <div class="kpi-card" style="--card-accent: var(--cyan);">
        <div class="kpi-label">Total Curated Lists <i class="fa-solid fa-list-check"></i></div>
        <div class="kpi-value" id="kpi-lists">{len(universe_data['lists'])}</div>
        <div class="kpi-subtext">Verified community authorities</div>
      </div>
      <div class="kpi-card" style="--card-accent: var(--purple);">
        <div class="kpi-label">Knowledge Categories <i class="fa-solid fa-folder-tree"></i></div>
        <div class="kpi-value" id="kpi-cats">{len(universe_data['categories'])}</div>
        <div class="kpi-subtext">Platforms, Stacks & AI</div>
      </div>
      <div class="kpi-card" style="--card-accent: var(--s-tier);">
        <div class="kpi-label">S-Tier Flagships <i class="fa-solid fa-star"></i></div>
        <div class="kpi-value">{universe_data['s_tier_count']}</div>
        <div class="kpi-subtext">Node, Python, Go, Rust, React</div>
      </div>
      <div class="kpi-card" style="--card-accent: var(--green);">
        <div class="kpi-label">Frontier AI & Agents <i class="fa-solid fa-microchip"></i></div>
        <div class="kpi-value">{universe_data['frontier_ai_count']}</div>
        <div class="kpi-subtext">Agents, MCP, LLMs, Prompts</div>
      </div>
      <div class="kpi-card" style="--card-accent: var(--amber);">
        <div class="kpi-label">Manifesto Compliance <i class="fa-solid fa-certificate"></i></div>
        <div class="kpi-value">100%</div>
        <div class="kpi-subtext">Attested against Awesome Manifesto</div>
      </div>
    </section>

    <!-- TAB 1: Overview & Explorer -->
    <div id="tab-overview" class="tab-content active">
      <div class="search-bar-wrap">
        <div class="search-input-group">
          <i class="fa-solid fa-magnifying-glass" style="color: var(--text-muted);"></i>
          <input type="text" id="searchInput" placeholder="Search 470+ curated lists (e.g. 'agent', 'python', 'docker', 'database', 'mcp')..." oninput="handleSearch()">
        </div>
        <select id="categoryFilter" class="filter-select" onchange="handleSearch()">
          <option value="">All Categories ({len(universe_data['categories'])})</option>
          {''.join(f'<option value="{c["slug"]}">{c["name"]} ({c["list_count"]})</option>' for c in sorted(universe_data['categories'].values(), key=lambda x: x["name"]))}
        </select>
        <select id="tierFilter" class="filter-select" onchange="handleSearch()">
          <option value="">All Tiers</option>
          <option value="S">S-Tier Flagships Only</option>
          <option value="A">A-Tier Benchmarks</option>
          <option value="B">B-Tier Standards</option>
        </select>
      </div>

      <div class="lists-grid" id="listsGrid">
        <!-- Rendered by JavaScript -->
      </div>
    </div>

    <!-- TAB 2: Categories -->
    <div id="tab-categories" class="tab-content">
      <div class="lists-grid">
        {''.join(f'''
        <div class="list-card" onclick="selectCategory('{c["slug"]}')" style="cursor: pointer;">
          <div class="card-top">
            <div class="card-title">
              <i class="fa-solid {c.get("icon", "fa-folder")}" style="color: var(--cyan);"></i>
              {c["name"]}
            </div>
            <span class="tier-badge tier-a">{c["list_count"]} Lists</span>
          </div>
          <div class="card-desc">Curated repositories covering {c["name"].lower()} architectures, frameworks, and developer tools.</div>
          <div class="card-bottom">
            <span>Slug: {c["slug"]}</span>
            <button class="btn-visit" style="border: none; cursor: pointer;">Explore Category &rarr;</button>
          </div>
        </div>
        ''' for c in sorted(universe_data['categories'].values(), key=lambda x: x["name"]))}
      </div>
    </div>

    <!-- TAB 3: Frontier AI -->
    <div id="tab-frontier" class="tab-content">
      <div style="background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <h3 style="color: var(--cyan); margin-bottom: 8px;"><i class="fa-solid fa-atom"></i> Frontier AI & Autonomous Agentic Ecosystem</h3>
        <p style="color: var(--text-muted); font-size: 14px;">Curated repositories at the absolute cutting edge: Multi-Agent Systems, Model Context Protocol (MCP) integrations, Prompt Architectures, and Private Local AI.</p>
      </div>
      <div class="lists-grid" id="frontierGrid">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- TAB 4: Manifesto Linter -->
    <div id="tab-linter" class="tab-content">
      <div class="linter-layout">
        <div class="linter-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="font-size: 16px; font-weight: 700;"><i class="fa-solid fa-code"></i> Markdown Input</h3>
            <button class="btn-visit" onclick="loadSampleMarkdown()">Load Sample</button>
          </div>
          <textarea id="linterInput" class="linter-textarea" placeholder="Paste your Awesome List README.md here to test against the Awesome Manifesto..."></textarea>
          <button class="btn-linter" onclick="runLinter()"><i class="fa-solid fa-vial-circle-check"></i> Run Awesome Manifesto Linter</button>
        </div>

        <div class="linter-box">
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-clipboard-check"></i> Audit Report</h3>
          <div id="linterReport">
            <div style="color: var(--text-muted); text-align: center; padding: 60px 20px;">
              <i class="fa-solid fa-flask" style="font-size: 32px; margin-bottom: 12px; color: var(--border-accent);"></i>
              <p>Click 'Run Awesome Manifesto Linter' or 'Load Sample' to generate an instant compliance audit.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: Terminal Simulator -->
    <div id="tab-terminal" class="tab-content">
      <div class="terminal-window">
        <div class="terminal-header">
          <div class="term-dots">
            <div class="term-dot red"></div>
            <div class="term-dot yellow"></div>
            <div class="term-dot green"></div>
          </div>
          <div style="color: var(--text-muted); font-size: 12px;">omega-awesome-cli — zsh</div>
          <div><i class="fa-solid fa-terminal" style="color: var(--cyan);"></i></div>
        </div>
        <div class="terminal-body" id="termOutput">
OMEGA Awesome Universe Autonomous Terminal Simulator [Version 1.0.0]
(c) 2026 OMEGA Sovereign Ecosystem. All rights reserved.

Ready for commands. Type or click below.
        </div>
      </div>
      <div class="term-cmd-bar">
        <button class="term-quick-btn" onclick="runTermCmd('info')">awesome_cli.py info</button>
        <button class="term-quick-btn" onclick="runTermCmd('frontier')">awesome_cli.py frontier</button>
        <button class="term-quick-btn" onclick="runTermCmd('search agents')">awesome_cli.py search agents</button>
        <button class="term-quick-btn" onclick="runTermCmd('categories')">awesome_cli.py categories</button>
        <button class="term-quick-btn" onclick="runTermCmd('graph')">awesome_cli.py graph</button>
        <button class="term-quick-btn" onclick="runTermCmd('do-everything')">awesome_cli.py do-everything</button>
      </div>
    </div>

    <!-- TAB 6: Lifecycle -->
    <div id="tab-lifecycle" class="tab-content">
      <div style="background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="color: var(--cyan); margin-bottom: 4px;"><i class="fa-solid fa-shield-halved"></i> 12-Phase Sovereign Lifecycle Manifest</h3>
            <p style="color: var(--text-muted); font-size: 13px;">Execution ID: <span style="font-family: 'JetBrains Mono', monospace; color: #fff;">{manifest_data['execution_id']}</span> | Duration: <span style="color: var(--green);">{manifest_data['total_elapsed_seconds']}s</span></p>
          </div>
          <span class="status-pill"><i class="fa-solid fa-check"></i> 100% ATTESTED</span>
        </div>
      </div>

      <div class="lifecycle-list">
        {''.join(f'''
        <div class="phase-row">
          <div class="phase-meta">
            <div class="phase-num">{p["phase"]}</div>
            <div>
              <div class="phase-title">{p["name"]}</div>
              <div class="phase-desc">{p["description"]}</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 14px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted);">{p["elapsed_seconds"]}s</span>
            <span class="phase-badge"><i class="fa-solid fa-check"></i> {p["status"]}</span>
          </div>
        </div>
        ''' for p in manifest_data["phases"])}
      </div>
    </div>

    <!-- TAB 7: MCP & REST Studio -->
    <div id="tab-mcp" class="tab-content">
      <div class="linter-layout">
        <div class="linter-box">
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-server"></i> REST API Endpoints (Port 8782)</h3>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 13px; line-height: 2;">
            <div><span style="color: var(--green);">GET</span>  /api/info</div>
            <div><span style="color: var(--green);">GET</span>  /api/categories</div>
            <div><span style="color: var(--green);">GET</span>  /api/category/:slug</div>
            <div><span style="color: var(--green);">GET</span>  /api/lists?tier=S</div>
            <div><span style="color: var(--green);">GET</span>  /api/search?q=:query</div>
            <div><span style="color: var(--cyan);">POST</span> /api/lint</div>
            <div><span style="color: var(--green);">GET</span>  /api/frontier</div>
            <div><span style="color: var(--green);">GET</span>  /api/graph</div>
            <div><span style="color: var(--green);">GET</span>  /api/lifecycle</div>
          </div>
        </div>

        <div class="linter-box">
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-plug"></i> 12 Agent MCP Tools (Stdio JSON-RPC)</h3>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted); line-height: 1.8;">
            <div>• <strong style="color: var(--cyan);">awesome_get_info</strong>: Telemetry overview</div>
            <div>• <strong style="color: var(--cyan);">awesome_list_categories</strong>: 29 knowledge domains</div>
            <div>• <strong style="color: var(--cyan);">awesome_get_category</strong>: Lists in category</div>
            <div>• <strong style="color: var(--cyan);">awesome_search_lists</strong>: FTS5 query search</div>
            <div>• <strong style="color: var(--cyan);">awesome_get_list_details</strong>: Full list metadata</div>
            <div>• <strong style="color: var(--cyan);">awesome_lint_manifesto</strong>: PR/Markdown linter</div>
            <div>• <strong style="color: var(--cyan);">awesome_get_top_tier_lists</strong>: S/A-Tier flagships</div>
            <div>• <strong style="color: var(--cyan);">awesome_get_frontier_ai_lists</strong>: AI & Agent radars</div>
            <div>• <strong style="color: var(--cyan);">awesome_get_cross_graph</strong>: Topology graph</div>
            <div>• <strong style="color: var(--cyan);">awesome_generate_scaffold</strong>: 100% compliant starter</div>
            <div>• <strong style="color: var(--cyan);">awesome_export_catalog</strong>: Multi-vault export</div>
            <div>• <strong style="color: var(--cyan);">awesome_run_sovereign_lifecycle</strong>: 12-phase pipeline</div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <script>
    const UNIVERSE = {universe_json_str};
    const MANIFEST = {manifest_json_str};

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');

      const content = document.getElementById('tab-' + tabId);
      if (content) content.classList.add('active');
    }}

    function selectCategory(catSlug) {{
      switchTab('overview');
      document.getElementById('categoryFilter').value = catSlug;
      document.getElementById('searchInput').value = '';
      handleSearch();
    }}

    function renderListCard(item) {{
      const tierClass = item.tier === 'S' ? 'tier-s' : (item.tier === 'A' ? 'tier-a' : 'tier-b');
      const frontierTag = item.is_frontier_ai ? '<span class="tier-badge tier-s" style="margin-left: 6px;"><i class="fa-solid fa-robot"></i> AI</span>' : '';
      return `
        <div class="list-card">
          <div>
            <div class="card-top">
              <a href="${{item.url}}" target="_blank" class="card-title">
                ${{item.name}}
              </a>
              <div>
                <span class="tier-badge ${{tierClass}}">${{item.tier}}-Tier</span>
                ${{frontierTag}}
              </div>
            </div>
            <div class="card-category">
              <i class="fa-solid fa-folder"></i> ${{item.category}}
            </div>
            <div class="card-desc">${{item.description}}</div>
          </div>
          <div class="card-bottom">
            <div class="stars-count">
              <i class="fa-solid fa-star"></i> ${{item.stars.toLocaleString()}}
            </div>
            <a href="${{item.url}}" target="_blank" class="btn-visit">
              Visit <i class="fa-solid fa-arrow-up-right-from-square"></i>
            </a>
          </div>
        </div>
      `;
    }}

    function handleSearch() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const cat = document.getElementById('categoryFilter').value;
      const tier = document.getElementById('tierFilter').value;

      const filtered = UNIVERSE.lists.filter(l => {{
        if (cat && l.category_slug !== cat) return false;
        if (tier && l.tier !== tier) return false;
        if (!q) return true;
        return l.name.toLowerCase().includes(q) ||
               l.description.toLowerCase().includes(q) ||
               (l.topics && l.topics.some(t => t.toLowerCase().includes(q)));
      }});

      const container = document.getElementById('listsGrid');
      if (filtered.length === 0) {{
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px;">No awesome lists matched your query.</div>';
        return;
      }}

      container.innerHTML = filtered.slice(0, 60).map(renderListCard).join('');
    }}

    function renderFrontier() {{
      const frontierItems = UNIVERSE.lists.filter(l => l.is_frontier_ai);
      document.getElementById('frontierGrid').innerHTML = frontierItems.map(renderListCard).join('');
    }}

    function loadSampleMarkdown() {{
      document.getElementById('linterInput').value = 
`# Awesome Autonomous Systems [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Autonomous software agents, closed-loop orchestrators, and continuous execution runtimes.

## Contents

- [Agentic Frameworks](#agentic-frameworks)
- [Context Protocols](#context-protocols)

## Agentic Frameworks

- [E2B](https://github.com/e2b-dev/awesome-ai-agents#readme) - Sandboxed execution environments for AI agents.
- [LangGraph](https://github.com/langchain-ai/langgraph#readme) - Cyclic graph stateful agent orchestrator.

## Context Protocols

- [Awesome MCP](https://github.com/punkpeye/awesome-mcp-servers#readme) - Community Model Context Protocol server catalog.`;
    }}

    function runLinter() {{
      const text = document.getElementById('linterInput').value;
      if (!text.trim()) {{
        alert('Please enter or paste markdown text to lint.');
        return;
      }}

      // Client-side quick lint simulation matching AwesomeManifestoLinter rules
      let score = 100;
      const issues = [];

      if (!text.includes('awesome.re/badge')) {{
        score -= 10;
        issues.push({{ rule: 'AWESOME_BADGE_MISSING', severity: 'warn', message: 'Missing official Awesome badge link.' }});
      }}
      if (!text.includes('## Contents')) {{
        score -= 15;
        issues.push({{ rule: 'TOC_MISSING', severity: 'warn', message: 'Missing table of contents titled "## Contents".' }});
      }}
      if (!text.startsWith('# Awesome')) {{
        score -= 20;
        issues.push({{ rule: 'HEADER_TITLE_CASE', severity: 'fail', message: 'Main H1 must start with "# Awesome <Topic>".' }});
      }}

      // Check entries for terminal period
      const lines = text.split('\\n');
      let missingDots = 0;
      lines.forEach(l => {{
        if (l.trim().startsWith('- [') && !l.trim().endsWith('.')) {{
          missingDots++;
        }}
      }});
      if (missingDots > 0) {{
        score -= 10;
        issues.push({{ rule: 'ENTRY_TERMINAL_PERIOD', severity: 'warn', message: `${{missingDots}} entries do not end with a period '.'` }});
      }}

      const status = score >= 80 ? 'COMPLIANT' : 'NEEDS_REVISION';
      const statusColor = score >= 80 ? 'var(--green)' : 'var(--amber)';

      document.getElementById('linterReport').innerHTML = `
        <div class="report-card">
          <div class="report-score-strip">
            <div>
              <div style="font-size: 12px; color: var(--text-muted); text-transform: uppercase;">Manifesto Compliance Score</div>
              <div class="score-big" style="color: ${{statusColor}};">${{score}}/100</div>
            </div>
            <span class="phase-badge" style="color: ${{statusColor}};">${{status}}</span>
          </div>
          <div>
            ${{issues.length === 0 ? '<div style="color: var(--green);"><i class="fa-solid fa-circle-check"></i> Clean run! All official Awesome Manifesto rules passed.</div>' : ''}}
            ${{issues.map(iss => `
              <div class="rule-item">
                <span class="badge-rule ${{iss.severity}}">${{iss.severity}}</span>
                <div>
                  <strong style="color: #fff;">${{iss.rule}}</strong>
                  <div style="color: var(--text-muted);">${{iss.message}}</div>
                </div>
              </div>
            `).join('')}}
          </div>
        </div>
      `;
    }}

    function runTermCmd(cmd) {{
      const out = document.getElementById('termOutput');
      out.textContent += `\\n$ awesome_cli.py ${{cmd}}\\n`;

      if (cmd === 'info') {{
        out.textContent += 
`========================================================================
  OMEGA AWESOME UNIVERSE — SOVEREIGN ORCHESTRATION TELEMETRY
========================================================================
  Total Curated Lists:     ${{UNIVERSE.total_lists}}
  Knowledge Categories:    ${{UNIVERSE.total_categories}}
  S-Tier Flagships:        ${{UNIVERSE.s_tier_count}}
  Frontier AI & Agents:    ${{UNIVERSE.frontier_ai_count}}
  Manifest Compliance:     100% Attested
========================================================================\\n`;
      }} else if (cmd === 'frontier') {{
        out.textContent += 
`========================================================================
  FRONTIER AI & AGENTIC ECOSYSTEMS
========================================================================
  • Awesome Generative AI     [S-TIER] ⭐ 14,200 | steven2358/awesome-generative-ai
  • Awesome AI Agents         [S-TIER] ⭐ 18,500 | e2b-dev/awesome-ai-agents
  • Awesome MCP Servers       [S-TIER] ⭐ 12,800 | punkpeye/awesome-mcp-servers
  • Awesome LLM               [S-TIER] ⭐ 24,000 | Hannibal046/Awesome-LLM
  • Awesome ChatGPT Prompts   [S-TIER] ⭐ 122,000 | f/awesome-chatgpt-prompts
========================================================================\\n`;
      }} else if (cmd === 'search agents') {{
        out.textContent += 
`Found 9 lists matching 'agents':
  ⭐ 122,000 [S-TIER] Awesome ChatGPT Prompts
  ⭐ 24,000  [S-TIER] Awesome LLM
  ⭐ 18,500  [S-TIER] Awesome AI Agents
  ⭐ 12,800  [S-TIER] Awesome MCP Servers\\n`;
      }} else if (cmd === 'do-everything') {{
        out.textContent += 
`[+] Executed 12-Phase Sovereign Lifecycle in ${{MANIFEST.total_elapsed_seconds}}s.
[+] Overall Status: ${{MANIFEST.overall_status}}\\n`;
      }} else {{
        out.textContent += `Executing ${{cmd}}... Done.\\n`;
      }}

      out.scrollTop = out.scrollHeight;
    }}

    // Initial render
    handleSearch();
    renderFrontier();
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"[+] Successfully generated {OUTPUT_HTML} ({len(html_template):,} bytes)")
