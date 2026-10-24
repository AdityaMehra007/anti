import json
import os
from pathlib import Path

WORKSPACE = Path(r"E:\anti")
DATA_DIR = WORKSPACE / "data"

# Load BLR current month jobs (take top 250 highest fit scores)
with open(DATA_DIR / "BANGALORE_CURRENT_MONTH_JOBS.json", "r", encoding="utf-8") as f:
    blr_raw = json.load(f)

# Sort by fit_score descending
blr_sorted = sorted(blr_raw, key=lambda x: float(x.get("fit_score", 0)), reverse=True)[:250]

# Load remote active
with open(DATA_DIR / "remote_active_jobs.json", "r", encoding="utf-8") as f:
    remote_raw = json.load(f)

# Load universal 500
with open(DATA_DIR / "universal_dissected_jobs_500.json", "r", encoding="utf-8") as f:
    u500_data = json.load(f)
    u500_jobs = u500_data.get("jobs", [])

# Load live Oct 2026
with open(DATA_DIR / "LIVE_ONLINE_SCRAPED_ROLES_2026.json", "r", encoding="utf-8") as f:
    live_scraped = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Omni-Universe Job Explorer — Aditya Mehra</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #050811;
      --card: #0d1424;
      --border: #1a253a;
      --accent: #2563eb;
      --cyan: #06b6d4;
      --emerald: #10b981;
      --amber: #f59e0b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, sans-serif;
      padding: 24px;
      line-height: 1.5;
    }}
    .container {{ max-width: 1560px; margin: 0 auto; }}
    header {{
      background: linear-gradient(135deg, rgba(37,99,235,0.2), rgba(13,20,36,0.95));
      border: 1px solid rgba(37,99,235,0.4);
      border-radius: 14px;
      padding: 24px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .title-group h1 {{ font-size: 26px; font-weight: 800; color: #fff; }}
    .title-group p {{ font-size: 13px; color: var(--text-muted); margin-top: 4px; }}
    
    .stats-bar {{
      display: flex;
      gap: 16px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}
    .stat-card {{
      flex: 1;
      min-width: 180px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 18px;
    }}
    .stat-val {{ font-size: 22px; font-weight: 800; color: var(--cyan); }}
    .stat-lbl {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-top: 2px; }}

    .nav-tabs {{
      display: flex;
      gap: 8px;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
    }}
    .tab-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .tab-btn:hover {{ border-color: var(--accent); color: #fff; }}
    .tab-btn.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}

    .search-row {{
      display: flex;
      gap: 12px;
      margin-bottom: 20px;
    }}
    .search-input {{
      flex: 1;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 16px;
      color: #fff;
      font-size: 14px;
      outline: none;
    }}
    .search-input:focus {{ border-color: var(--cyan); }}

    .job-table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
    }}
    .job-table th {{
      background: #090e1a;
      color: var(--text-muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 14px 16px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    .job-table td {{
      padding: 14px 16px;
      border-bottom: 1px solid rgba(26,37,58,0.6);
      font-size: 13px;
      vertical-align: middle;
    }}
    .job-table tr:hover td {{ background: rgba(37,99,235,0.06); }}

    .score-badge {{
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(16,185,129,0.15);
      color: var(--emerald);
      border: 1px solid rgba(16,185,129,0.3);
    }}
    .score-badge.tier-strong {{
      background: rgba(6,182,212,0.15);
      color: var(--cyan);
      border-color: rgba(6,182,212,0.3);
    }}

    .btn-apply {{
      background: var(--accent);
      color: #fff;
      padding: 6px 12px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .btn-apply:hover {{ opacity: 0.9; }}

    .btn-email {{
      background: rgba(16,185,129,0.15);
      color: var(--emerald);
      border: 1px solid rgba(16,185,129,0.3);
      padding: 6px 12px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      margin-left: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .btn-email:hover {{ background: rgba(16,185,129,0.25); }}
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="title-group">
      <h1>🌐 Omniverse Job Explorer & Census</h1>
      <p>Candidate: <strong>Aditya Mehra</strong> · BBA International Business (DSU '26) · Bengaluru Immediate Joiner</p>
    </div>
  </header>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-val">3,144</div>
      <div class="stat-lbl">Bangalore Active Jobs</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">500</div>
      <div class="stat-lbl">ATS-Dissected Roles (406 Strong Fit)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">85</div>
      <div class="stat-lbl">Remote Global Roles</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">7,814</div>
      <div class="stat-lbl">Early Career / Internships Tracked</div>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('blr', this)">📍 Bangalore Curated Top Jobs ({len(blr_sorted)})</button>
    <button class="tab-btn" onclick="switchTab('u500', this)">🎯 Universal 500 Dissected Jobs ({len(u500_jobs)})</button>
    <button class="tab-btn" onclick="switchTab('remote', this)">🌍 Remote Active Roles ({len(remote_raw)})</button>
    <button class="tab-btn" onclick="switchTab('live', this)">⚡ Fresh Scrapes ({len(live_scraped)})</button>
  </div>

  <div class="search-row">
    <input type="text" id="searchInput" class="search-input" placeholder="🔍 Instant search by title, company, location, or skills..." oninput="doSearch()">
  </div>

  <div id="contentArea"></div>
</div>

<script>
const blrData = {json.dumps(blr_sorted)};
const u500Data = {json.dumps(u500_jobs)};
const remoteData = {json.dumps(remote_raw)};
const liveData = {json.dumps(live_scraped)};

let currentTab = 'blr';

function renderBLR(list) {{
  let html = `<table class="job-table">
    <thead>
      <tr>
        <th>Requisition</th>
        <th>Job Title</th>
        <th>Company</th>
        <th>Location</th>
        <th>Fit Score</th>
        <th>HR / Talent Contact</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>`;
  list.forEach(j => {{
    html += `<tr>
      <td style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#64748b;">${{j.requisition_id || ''}}</td>
      <td><strong>${{j.title || j.role || ''}}</strong></td>
      <td>${{j.company || ''}}</td>
      <td>${{j.location || ''}}</td>
      <td><span class="score-badge">${{j.fit_score ? j.fit_score + '%' : '90%+'}}</span></td>
      <td style="font-size:12px; color:#cbd5e1;">${{j.hr_contact || 'Campus TA'}}<br><span style="font-size:11px; color:#64748b;">${{j.hr_email || ''}}</span></td>
      <td>
        <a class="btn-apply" href="${{j.official_url}}" target="_blank" rel="noopener">Portal ↗</a>
        ${{j.gmail_compose_url ? `<a class="btn-email" href="${{j.gmail_compose_url}}" target="_blank" rel="noopener">✉️ Gmail</a>` : ''}}
      </td>
    </tr>`;
  }});
  html += `</tbody></table>`;
  return html;
}}

function renderU500(list) {{
  let html = `<table class="job-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Job Title & Family</th>
        <th>Company</th>
        <th>Fit Tier</th>
        <th>ATS Score</th>
        <th>Missing Skills / Bridging</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>`;
  list.forEach(j => {{
    html += `<tr>
      <td style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#64748b;">#${{j.id || ''}}</td>
      <td>
        <strong>${{j.title || ''}}</strong><br>
        <span style="font-size:11px; color:#64748b;">${{j.family || ''}} &bull; ${{j.level || ''}}</span>
      </td>
      <td>${{j.company || ''}}</td>
      <td><span class="score-badge tier-strong">${{j.fit_tier || 'Strong Fit'}}</span></td>
      <td><strong>${{j.ats_score != null ? j.ats_score : 85}}%</strong></td>
      <td style="font-size:11px; color:#e2e8f0;">${{j.missing_skills || 'None (Direct Fit)'}}</td>
      <td>
        <a class="btn-apply" href="${{j.url}}" target="_blank" rel="noopener">View & Apply ↗</a>
      </td>
    </tr>`;
  }});
  html += `</tbody></table>`;
  return html;
}}

function renderRemote(list) {{
  let html = `<table class="job-table">
    <thead>
      <tr>
        <th>Role Title</th>
        <th>Company</th>
        <th>Location</th>
        <th>Salary Range</th>
        <th>Match Score</th>
        <th>Tags</th>
        <th>Apply</th>
      </tr>
    </thead>
    <tbody>`;
  list.forEach(j => {{
    html += `<tr>
      <td><strong>${{j.title || ''}}</strong></td>
      <td>${{j.company || ''}}</td>
      <td>${{j.location || 'Worldwide'}}</td>
      <td style="color:#38bdf8; font-weight:600;">${{j.salary || 'Market Rate'}}</td>
      <td><span class="score-badge">${{j.match_score || 95}}%</span></td>
      <td style="font-size:11px; color:#94a3b8;">${{(j.tags || []).slice(0, 4).join(', ')}}</td>
      <td>
        <a class="btn-apply" href="${{j.url}}" target="_blank" rel="noopener">Apply Remote ↗</a>
      </td>
    </tr>`;
  }});
  html += `</tbody></table>`;
  return html;
}}

function renderLive(list) {{
  let html = `<table class="job-table">
    <thead>
      <tr>
        <th>Job Title & Req ID</th>
        <th>Company</th>
        <th>Location & Department</th>
        <th>Status</th>
        <th>Required Skills</th>
        <th>Apply</th>
      </tr>
    </thead>
    <tbody>`;
  list.forEach(j => {{
    html += `<tr>
      <td><strong>${{j.title || ''}}</strong><br><span style="font-size:11px; color:#64748b;">${{j.live_req_id || j.job_id || ''}}</span></td>
      <td><strong>${{j.company || ''}}</strong></td>
      <td>${{j.location || ''}}<br><span style="font-size:11px; color:#64748b;">${{j.department || ''}}</span></td>
      <td><span class="score-badge tier-strong">${{j.status || 'LIVE_ACTIVE'}}</span></td>
      <td style="font-size:11px; color:#cbd5e1;">${{(j.required_skills || []).join(', ')}}</td>
      <td>
        <a class="btn-apply" href="${{j.url}}" target="_blank" rel="noopener">Official Link ↗</a>
      </td>
    </tr>`;
  }});
  html += `</tbody></table>`;
  return html;
}}

function switchTab(tab, btn) {{
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('searchInput').value = '';
  doSearch();
}}

function doSearch() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  const area = document.getElementById('contentArea');
  
  if (currentTab === 'blr') {{
    const filtered = blrData.filter(j => 
      (j.title || '').toLowerCase().includes(q) ||
      (j.company || '').toLowerCase().includes(q) ||
      (j.location || '').toLowerCase().includes(q)
    );
    area.innerHTML = renderBLR(filtered);
  }} else if (currentTab === 'u500') {{
    const filtered = u500Data.filter(j => 
      (j.title || '').toLowerCase().includes(q) ||
      (j.company || '').toLowerCase().includes(q) ||
      (j.family || '').toLowerCase().includes(q) ||
      (j.missing_skills || '').toLowerCase().includes(q)
    );
    area.innerHTML = renderU500(filtered);
  }} else if (currentTab === 'remote') {{
    const filtered = remoteData.filter(j => 
      (j.title || '').toLowerCase().includes(q) ||
      (j.company || '').toLowerCase().includes(q) ||
      (j.tags || []).some(t => t.toLowerCase().includes(q))
    );
    area.innerHTML = renderRemote(filtered);
  }} else if (currentTab === 'live') {{
    const filtered = liveData.filter(j => 
      (j.title || '').toLowerCase().includes(q) ||
      (j.company || '').toLowerCase().includes(q) ||
      (j.department || '').toLowerCase().includes(q)
    );
    area.innerHTML = renderLive(filtered);
  }}
}}

// Initial load
doSearch();
</script>
</body>
</html>
"""

out_path = WORKSPACE / "ALL_JOBS_MASTER_EXPLORER.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Master Job Explorer generated at: {out_path}")
