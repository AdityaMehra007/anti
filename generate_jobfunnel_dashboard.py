#!/usr/bin/env python3
"""
generate_jobfunnel_dashboard.py - Generates standalone interactive jobfunnel_dashboard.html
"""

import json
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
SAMPLE_PATH = ROOT_DIR / "data" / "jobfunnel_sample_500.json"
OUT_HTML = ROOT_DIR / "jobfunnel_dashboard.html"

with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
    sample_roles = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>JobFunnel Master Funnel & Deduplication Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card: rgba(17, 24, 39, 0.7);
      --card-hover: rgba(30, 41, 59, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --text: #f3f4f6;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --amber: #f59e0b;
      --amber-dark: #d97706;
      --emerald: #10b981;
      --indigo: #6366f1;
      --cyan: #06b6d4;
      --rose: #f43f5e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-image: 
        radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.10) 0px, transparent 50%);
      background-attachment: fixed;
    }}
    header {{
      padding: 1.5rem 2.5rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(12px);
      flex-wrap: wrap;
      gap: 1.5rem;
    }}
    .brand {{ display: flex; align-items: center; gap: 1rem; }}
    .funnel-badge {{
      width: 44px; height: 44px; border-radius: 12px;
      background: linear-gradient(135deg, #f59e0b, #d97706);
      display: flex; align-items: center; justify-content: center;
      font-weight: 800; font-size: 1.3rem; color: #000;
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.4);
    }}
    .brand-text h1 {{ font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; }}
    .brand-text p {{ font-size: 0.8rem; color: var(--text-muted); }}
    .nav-links {{ display: flex; gap: 0.75rem; }}
    .btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .btn:hover {{ background: rgba(255, 255, 255, 0.12); }}
    .btn-amber {{ background: var(--amber); color: #000; border: none; font-weight: 700; }}
    .btn-amber:hover {{ background: #fbbf24; }}
    .container {{ max-width: 1540px; margin: 0 auto; padding: 2rem; width: 100%; display: flex; flex-direction: column; gap: 2rem; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .stat-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      padding: 1.25rem; display: flex; flex-direction: column; gap: 0.35rem;
      backdrop-filter: blur(8px);
    }}
    .stat-val {{ font-size: 1.85rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--amber); }}
    .stat-lbl {{ font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }}
    .controls-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 16px;
      padding: 1.25rem; display: flex; flex-direction: column; gap: 1rem;
    }}
    .search-bar {{
      width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border);
      border-radius: 10px; padding: 0.85rem 1.25rem; color: #fff; font-size: 0.95rem;
      font-family: inherit; outline: none; transition: border-color 0.2s;
    }}
    .search-bar:focus {{ border-color: var(--amber); }}
    .filter-tabs {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
    .filter-btn {{
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.45rem 0.9rem; border-radius: 8px;
      font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all 0.15s;
    }}
    .filter-btn.active {{ background: var(--amber); color: #000; border-color: var(--amber); font-weight: 700; }}
    .roles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 1.25rem; }}
    .role-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      padding: 1.25rem; display: flex; flex-direction: column; justify-content: space-between;
      gap: 1rem; transition: transform 0.2s, border-color 0.2s;
    }}
    .role-card:hover {{ transform: translateY(-2px); border-color: rgba(245, 158, 11, 0.4); background: var(--card-hover); }}
    .badge {{
      display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.72rem;
      font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
      padding: 0.25rem 0.65rem; border-radius: 20px;
    }}
    .badge-interested {{ background: rgba(245, 158, 11, 0.15); color: var(--amber); border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-new {{ background: rgba(99, 102, 241, 0.15); color: var(--indigo); border: 1px solid rgba(99, 102, 241, 0.3); }}
    .badge-remote {{ background: rgba(16, 185, 129, 0.15); color: var(--emerald); border: 1px solid rgba(16, 185, 129, 0.3); }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="funnel-badge">⏳</div>
      <div class="brand-text">
        <h1>JobFunnel Master Funnel & Deduplication Engine</h1>
        <p>Dual-Stage Exact Hash & TF-IDF Cosine Similarity Filter • 6,910 Unique Listings</p>
      </div>
    </div>
    <div class="nav-links">
      <a href="omega_master_nexus.html" class="btn">← Master Nexus</a>
      <a href="reports/JOBFUNNEL_MASTER_INTELLIGENCE_GUIDE.pdf" target="_blank" class="btn btn-amber">Executive PDF 📄</a>
    </div>
  </header>

  <main class="container">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-val">8,576</div>
        <div class="stat-lbl">Raw Listings Ingested</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color:var(--rose);">1,666</div>
        <div class="stat-lbl">Duplicates Purged (19.4%)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">6,910</div>
        <div class="stat-lbl">Net Master Funnel Roles</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color:var(--emerald);">17,657</div>
        <div class="stat-lbl">Total Master FTS5 Index</div>
      </div>
    </div>

    <div class="controls-card">
      <input type="text" id="search-input" class="search-bar" placeholder="Search by company, role title, tags or location (e.g., 'Tesla', 'OpenAI', 'Quant', 'San Francisco')..." oninput="render()" />
      <div class="filter-tabs">
        <button class="filter-btn active" onclick="setStatus('all', this)">All Status (6,910)</button>
        <button class="filter-btn" onclick="setStatus('interested', this)">Interested (542)</button>
        <button class="filter-btn" onclick="setStatus('new', this)">New (6,368)</button>
        <button class="filter-btn" onclick="setRemoteness('FULLY_REMOTE', this)">Remote Only (231)</button>
      </div>
    </div>

    <div class="roles-grid" id="roles-grid"></div>
  </main>

  <script>
    const sampleRoles = {json.dumps(sample_roles)};
    let currentStatus = 'all';
    let currentRemoteness = 'all';

    function setStatus(s, btn) {{
      currentStatus = s;
      currentRemoteness = 'all';
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    }}

    function setRemoteness(r, btn) {{
      currentRemoteness = r;
      currentStatus = 'all';
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    }}

    function render() {{
      const q = document.getElementById('search-input').value.toLowerCase().trim();
      const grid = document.getElementById('roles-grid');
      
      const filtered = sampleRoles.filter(r => {{
        if (currentStatus !== 'all' && r.status.toLowerCase() !== currentStatus) return false;
        if (currentRemoteness !== 'all' && r.remoteness !== currentRemoteness) return false;
        if (!q) return true;
        return (
          r.title.toLowerCase().includes(q) ||
          r.company.toLowerCase().includes(q) ||
          r.location.toLowerCase().includes(q) ||
          r.tags.toLowerCase().includes(q)
        );
      }});

      if (!filtered.length) {{
        grid.innerHTML = '<div style="color:var(--text-dim); text-align:center; grid-column:1/-1; padding:3rem;">No matching roles found in sample cache. Use CLI for full 6,910 FTS5 index.</div>';
        return;
      }}

      grid.innerHTML = filtered.map(r => `
        <div class="role-card">
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
              <span class="badge badge-${{r.status.toLowerCase()}}">${{r.status}}</span>
              <span style="font-size:0.75rem; color:var(--text-dim); font-family:'JetBrains Mono';">${{r.provider}}</span>
            </div>
            <div style="font-weight:700; font-size:1.05rem; margin-bottom:0.25rem;">${{r.company}}</div>
            <div style="font-size:0.9rem; color:var(--text-muted); margin-bottom:0.5rem;">${{r.title}}</div>
            <div style="font-size:0.78rem; color:var(--text-dim); line-height:1.4;">📍 ${{r.location || 'Location Unspecified'}} • ${{r.remoteness}} ${{r.wage ? '• ' + r.wage : ''}}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.75rem; color:var(--text-dim); font-family:'JetBrains Mono';">${{r.id}}</span>
            ${{r.url ? `<a href="${{r.url}}" target="_blank" class="btn btn-amber" style="padding:0.35rem 0.75rem; font-size:0.75rem;">Apply Portal ↗</a>` : ''}}
          </div>
        </div>
      `).join('');
    }}

    render();
  </script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Successfully created {OUT_HTML}")
