import csv
import json
from pathlib import Path
from collections import defaultdict

root = Path(r"e:\anti")
matches_csv = root / "data" / "job_to_connection_matches.csv"

jobs_map = {}
recruiters_by_job = defaultdict(list)

with open(matches_csv, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        jid = row["Job ID"]
        if jid not in jobs_map:
            jobs_map[jid] = {
                "id": jid,
                "company": row["Target Company"],
                "title": row["Job Title"],
                "url": row["Job URL"],
                "relevance": row.get("Total Contact Opportunity Score (100)", "75")
            }
        
        if "Recruiter" in row["Match Type"]:
            recruiters_by_job[jid].append({
                "name": row["Contact Name"],
                "position": row["Contact Position"],
                "linkedin": row["Contact LinkedIn URL"],
                "score": row.get("Total Contact Opportunity Score (100)", "75")
            })

for jid in recruiters_by_job:
    recruiters_by_job[jid].sort(key=lambda x: float(x["score"]) if x["score"].replace(".","").isdigit() else 0, reverse=True)

board_data = []
for jid, job in sorted(jobs_map.items()):
    recs = recruiters_by_job.get(jid, [])
    top_rec = recs[0] if recs else None
    board_data.append({
        "id": jid,
        "company": job["company"],
        "title": job["title"],
        "url": job["url"],
        "recruiter_count": len(recs),
        "top_recruiter": top_rec["name"] if top_rec else "Talent Acquisition",
        "top_position": top_rec["position"] if top_rec else "Hiring Desk",
        "top_linkedin": top_rec["linkedin"] if top_rec else job["url"],
        "note": f"Hi {top_rec['name'].split()[0] if top_rec else 'there'}, noticed {job['company']} is hiring for {job['title']}. I bring 300+ event/operations deployments (AERO India), Tier-1 vendor SLA governance, and BBA International Business (DSU). Would love to connect!",
        "pitch": f"Hi {top_rec['name'].split()[0] if top_rec else 'there'},\n\nI noticed {job['company']} is expanding its {job['title']} function in Bengaluru.\n\nQuick snapshot of my verified background:\n• 300+ On-Ground Operations Deployments (Lead Coordinator at AERO India 2025, Puma India, Tata Communications)\n• Tier-1 Vendor SLA Governance via direct rate cards & milestone enforcement\n• Commercial Operations & Client Workflows (48h proposal turnaround, account handovers)\n• 99%+ AI QA Benchmark accuracy (Instawork AI production datasets)\n• BBA International Business (DSU, Class of 2026) - Incoterms 2020 & EXIM trade compliance\n\nI have submitted my application on {job['company']}'s portal and would appreciate a brief introduction with the hiring team.\n\nPortfolio: file:///e:/anti/portfolio/index.html\n\nBest regards,\nAditya Mehra\n+91-7003456624 | adityamehra799@gmail.com"
    })

board_json = json.dumps(board_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Active Hiring MNC Strike Board — Bengaluru</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #05070c;
      --card-bg: #0b0f19;
      --card-border: #162033;
      --primary: #3b82f6;
      --success: #10b981;
      --warning: #f59e0b;
      --accent: #8b5cf6;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Space Grotesk', sans-serif;
      padding: 24px;
      line-height: 1.5;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .header h1 {{ font-size: 24px; font-weight: 700; color: #fff; }}
    .header p {{ font-size: 13px; color: var(--text-muted); }}
    .nav-links {{ display: flex; gap: 10px; }}
    .nav-btn {{
      padding: 8px 16px;
      border-radius: 6px;
      background: #162033;
      color: #38bdf8;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      border: 1px solid #1f2d47;
      transition: all 0.2s;
    }}
    .nav-btn:hover {{ background: #1e293b; border-color: var(--primary); }}
    .search-bar {{
      width: 100%;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 14px 18px;
      border-radius: 8px;
      font-size: 14px;
      font-family: 'Space Grotesk', sans-serif;
      margin-bottom: 24px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: transform 0.15s, border-color 0.15s;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: var(--primary);
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .co-name {{ font-size: 17px; font-weight: 700; color: #fff; }}
    .role-name {{ font-size: 13px; color: #93c5fd; font-weight: 500; margin-top: 2px; }}
    .pill {{
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
    }}
    .rec-box {{
      background: #060911;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 12px;
    }}
    .rec-name {{ font-weight: 600; color: #f1f5f9; font-size: 13px; }}
    .rec-pos {{ font-size: 12px; color: var(--text-muted); }}
    .actions {{
      display: flex;
      gap: 8px;
      margin-top: auto;
      flex-wrap: wrap;
    }}
    .btn {{
      flex: 1;
      min-width: 100px;
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      text-align: center;
      font-family: 'Space Grotesk', sans-serif;
    }}
    .btn:hover {{ background: #2563eb; }}
    .btn-secondary {{ background: #162033; color: #cbd5e1; }}
    .btn-secondary:hover {{ background: #1f2d47; }}
    .btn-portal {{ background: #065f46; color: #6ee7b7; }}
    .btn-portal:hover {{ background: #047857; }}
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--success);
      color: #fff;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      display: none;
      z-index: 100000;
    }}
  </style>
</head>
<body>

  <header class="header">
    <div>
      <h1>ACTIVE HIRING MNC STRIKE BOARD</h1>
      <p>34 Actively Hiring Enterprises in Bengaluru | 96 Matched Recruiters | 1-Click Apply & Connect</p>
    </div>
    <div class="nav-links">
      <a href="apex_hud.html" class="nav-btn">Apex HUD & Kanban &rarr;</a>
      <a href="../../ACTIVE_HIRING_MNC_STRIKE_BOARD.md" target="_blank" class="nav-btn">Markdown View</a>
    </div>
  </header>

  <input type="text" id="searchBar" class="search-bar" placeholder="Search actively hiring companies (Accenture, Amazon, Deloitte, Google, Zepto...) or roles..." oninput="renderCards()">

  <div class="grid" id="gridContainer"></div>

  <div class="toast" id="toast">Copied to clipboard!</div>

  <script>
    const data = {board_json};

    function renderCards() {{
      const q = document.getElementById('searchBar').value.toLowerCase();
      const grid = document.getElementById('gridContainer');
      grid.innerHTML = '';

      const filtered = data.filter(d => 
        d.company.toLowerCase().includes(q) || 
        d.title.toLowerCase().includes(q) || 
        d.top_recruiter.toLowerCase().includes(q)
      );

      filtered.forEach(d => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-head">
            <div>
              <div class="co-name">${{d.company}}</div>
              <div class="role-name">${{d.title}}</div>
            </div>
            <span class="pill">${{d.recruiter_count}} Recruiters</span>
          </div>

          <div class="rec-box">
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:2px;">Primary Gatekeeper:</div>
            <div class="rec-name">${{d.top_recruiter}}</div>
            <div class="rec-pos">${{d.top_position}}</div>
          </div>

          <div class="actions">
            <a href="${{d.url}}" target="_blank" class="btn btn-portal">Apply on Portal &rarr;</a>
            <a href="${{d.top_linkedin}}" target="_blank" class="btn btn-secondary">Recruiter Profile</a>
            <button class="btn" onclick="copyPitch('${{d.id}}')">Copy Note</button>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function copyPitch(id) {{
      const item = data.find(d => d.id === id);
      if (!item) return;
      navigator.clipboard.writeText(item.note);
      showToast('Connection Note copied!');
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 2200);
    }}

    renderCards();
  </script>
</body>
</html>
"""

out_html = root / "apps" / "job_application_studio" / "active_hiring_board.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Interactive Active Hiring Board saved to: {out_html}")
