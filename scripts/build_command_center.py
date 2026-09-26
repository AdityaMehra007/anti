import csv
import json
from pathlib import Path

jobs_path = Path("data/jobs_master.csv")
referrals_path = Path("data/referral_targets.csv")

referrals_by_job = {}
if referrals_path.exists():
    with open(referrals_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            jid = r.get("Job ID", "").strip()
            if jid not in referrals_by_job:
                referrals_by_job[jid] = []
            referrals_by_job[jid].append(r)

jobs = []
with open(jobs_path, "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        jid = row.get("Job ID", "").strip()
        matched_refs = referrals_by_job.get(jid, [])
        top_ref = matched_refs[0] if matched_refs else None

        role_lower = row.get("Role", "").lower()
        if any(k in role_lower for k in ["supply chain", "logistics", "freight", "exim", "cargo", "procurement"]):
            track = "Supply Chain & EXIM"
        elif any(k in role_lower for k in ["ai", "data", "quality", "benchmark"]):
            track = "AI & Data Operations"
        elif any(k in role_lower for k in ["event", "brand", "activation", "community", "retail"]):
            track = "Brand Ops & Activations"
        elif any(k in role_lower for k in ["advisory", "consultant", "risk", "audit"]):
            track = "Advisory & Risk"
        else:
            track = "Business Operations"

        jobs.append({
            "id": jid,
            "company": row.get("Company", "N/A"),
            "role": row.get("Role", "N/A"),
            "location": row.get("Location", "Bengaluru, India"),
            "salary": row.get("Salary", "Competitive"),
            "match_score": float(row.get("Match Score", 75.0)),
            "priority": row.get("Priority", "HIGH"),
            "portal_url": row.get("Application URL", row.get("Job URL", "#")),
            "track": track,
            "skills": row.get("Skills", ""),
            "recruiter_name": top_ref.get("Contact Name", "Talent Acquisition Team") if top_ref else "Direct Careers Portal",
            "recruiter_pos": top_ref.get("Contact Position", "Recruiter") if top_ref else "Talent Acquisition",
            "recruiter_url": top_ref.get("LinkedIn URL", "#") if top_ref else "#",
            "total_recruiters": len(matched_refs)
        })

jobs.sort(key=lambda x: x["match_score"], reverse=True)

html_parts = []
html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ADI OMEGA OS — Master Job Strike Command Center</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #07090e;
      --card: rgba(15, 23, 42, 0.75);
      --border: rgba(51, 65, 85, 0.6);
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --accent: #818cf8;
      --success: #34d399;
      --warning: #fbbf24;
      --text: #f8fafc;
      --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 24px;
      line-height: 1.5;
      min-height: 100vh;
    }
    .container { max-width: 1540px; margin: 0 auto; }
    header {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(16px);
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .brand h1 {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand p { color: var(--muted); font-size: 14px; margin-top: 4px; }
    .nav-links { display: flex; gap: 12px; }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }
    .btn-primary {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }
    .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4); }
    .btn-secondary {
      background: rgba(30, 41, 59, 0.8);
      color: var(--text);
      border-color: var(--border);
    }
    .btn-secondary:hover { background: rgba(51, 65, 85, 0.8); }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px 24px;
      backdrop-filter: blur(12px);
    }
    .stat-label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-val { font-size: 30px; font-weight: 800; color: #fff; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }
    .stat-desc { font-size: 12px; color: var(--success); margin-top: 4px; }

    .controls-bar {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      margin-bottom: 24px;
      backdrop-filter: blur(12px);
    }
    .search-input {
      flex: 1;
      min-width: 280px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border);
      color: #fff;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s;
    }
    .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 2px var(--primary-glow); }
    .filter-btn {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--border);
      color: var(--muted);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .filter-btn.active {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--primary);
      color: var(--primary);
    }

    .table-container {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      backdrop-filter: blur(16px);
      box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th {
      background: rgba(15, 23, 42, 0.95);
      padding: 16px 20px;
      font-size: 12px;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border);
    }
    td {
      padding: 18px 20px;
      font-size: 14px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.3);
      vertical-align: middle;
    }
    tr:hover td { background: rgba(30, 41, 59, 0.4); }
    .company-cell { font-weight: 700; color: #fff; font-size: 15px; }
    .role-cell { color: #e2e8f0; font-weight: 600; }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      text-transform: uppercase;
    }
    .badge-score { background: rgba(52, 211, 153, 0.15); color: var(--success); border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-track { background: rgba(129, 140, 248, 0.15); color: var(--accent); border: 1px solid rgba(129, 140, 248, 0.3); }
    .recruiter-link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .recruiter-link:hover { text-decoration: underline; }
    .action-group { display: flex; gap: 8px; flex-wrap: wrap; }
    .action-btn {
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid var(--border);
      background: rgba(30, 41, 59, 0.8);
      color: #e2e8f0;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
    }
    .action-btn:hover { background: var(--primary); color: #000; border-color: var(--primary); }

    .modal {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.85);
      backdrop-filter: blur(8px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal.active { display: flex; }
    .modal-card {
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 16px;
      max-width: 680px;
      width: 100%;
      padding: 28px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.6);
    }
    .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .modal-header h3 { font-size: 18px; font-weight: 700; color: var(--primary); }
    .close-btn { background: none; border: none; color: var(--muted); font-size: 24px; cursor: pointer; }
    .inmail-box {
      background: #07090e;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      color: #e2e8f0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      white-space: pre-wrap;
      line-height: 1.6;
      max-height: 360px;
      overflow-y: auto;
      margin-bottom: 20px;
    }
    .modal-actions { display: flex; justify-content: flex-end; gap: 12px; }

    .toast {
      position: fixed;
      bottom: 30px;
      right: 30px;
      background: var(--success);
      color: #000;
      padding: 12px 24px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14px;
      display: none;
      z-index: 2000;
      box-shadow: 0 10px 25px rgba(52, 211, 153, 0.4);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <h1>⚡ ADI OMEGA OS — MASTER JOB COMMAND CENTER</h1>
        <p>Candidate: Aditya Mehra | BBA Intl Business (DSU '26) | Ground Truth Verification: 100%</p>
      </div>
      <div class="nav-links">
        <a href="strike_300.html" class="btn btn-secondary">🎯 300 Strike Studio</a>
        <a href="mega_studio.html" class="btn btn-secondary">🏢 4,500 Mega Studio</a>
        <a href="../../interview_simulator.html" class="btn btn-secondary">🎙️ Interview Simulator</a>
        <a href="http://127.0.0.1:9119" target="_blank" class="btn btn-primary">🚀 Hermes Dashboard (Port 9119)</a>
      </div>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Active Requisitions</div>
        <div class="stat-val">61</div>
        <div class="stat-desc">Verified Bangalore Openings</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Matched HR Gatekeepers</div>
        <div class="stat-val">96</div>
        <div class="stat-desc">Direct 1st-Degree Contacts</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Tailored Dossiers</div>
        <div class="stat-val">51</div>
        <div class="stat-desc">Complete Packages Ready</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Network Leverage</div>
        <div class="stat-val">9,223</div>
        <div class="stat-desc">Indexed LinkedIn Connections</div>
      </div>
    </div>

    <div class="controls-bar">
      <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search by Company, Role, Corridor, or Recruiter..." onkeyup="filterJobs()">
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <button class="filter-btn active" onclick="setTrack('ALL', this)">All Tracks</button>
        <button class="filter-btn" onclick="setTrack('Business Operations', this)">Business Operations</button>
        <button class="filter-btn" onclick="setTrack('Supply Chain & EXIM', this)">Supply Chain & EXIM</button>
        <button class="filter-btn" onclick="setTrack('Advisory & Risk', this)">Advisory & Risk</button>
        <button class="filter-btn" onclick="setTrack('AI & Data Operations', this)">AI & Data</button>
        <button class="filter-btn" onclick="setTrack('Brand Ops & Activations', this)">Brand Activations</button>
      </div>
    </div>

    <div class="table-container">
      <table id="jobsTable">
        <thead>
          <tr>
            <th>Company</th>
            <th>Role & Requisition</th>
            <th>Track</th>
            <th>Match Score</th>
            <th>Primary Gatekeeper (LinkedIn)</th>
            <th>Action Arsenal</th>
          </tr>
        </thead>
        <tbody id="tableBody">
""")

for j in jobs:
    jid = j["id"]
    comp = j["company"]
    role = j["role"]
    track = j["track"]
    score = j["match_score"]
    rec_name = j["recruiter_name"]
    rec_pos = j["recruiter_pos"]
    rec_url = j["recruiter_url"]
    portal_url = j["portal_url"]
    first_name = rec_name.split()[0] if rec_name else "Talent Partner"

    clean_comp = comp.replace("'", "")
    clean_role = role.replace("'", "")
    clean_rec = rec_name.replace("'", "")

    inmail_msg = (
        f"Subject: BBA (Intl Business) | Operations & Analysis Track - {clean_comp} Bengaluru\\n\\n"
        f"Hi {first_name},\\n\\n"
        f"I noticed {clean_comp}'s current operational growth in Bengaluru and wanted to introduce myself directly regarding {clean_role} openings.\\n\\n"
        "I graduate with a BBA in International Business from Dayananda Sagar University (DSU) in 2026. My core operational grounding includes:\\n"
        " - Ground Operations & Logistics: Directed execution at AERO India 2025 (Yelahanka AFB) and premier brand activations (Puma India, Tata Communications, Dyson).\\n"
        " - Vendor Governance: Supplier rate card structuring, contract adherence, and process standardization reducing manual reconciliation by ~25%.\\n"
        " - AI-Augmented Operations: Advanced prompt engineering, structured data synthesis, and workflow automation in fast-paced operational setups.\\n\\n"
        f"I would welcome 5 minutes to discuss how my hands-on execution rigor fits your active requirements at {clean_comp}.\\n\\n"
        "Best regards,\\nAditya Mehra | +91-7003456624 | ashishiash007@gmail.com"
    ).replace('"', '&quot;')

    rec_display = f'<a href="{rec_url}" target="_blank" class="recruiter-link">👤 {rec_name}</a><div style="font-size:11px;color:var(--muted);margin-top:2px;">{rec_pos}</div>' if rec_url != '#' else f'<span style="color:var(--muted);">Direct Portal</span>'

    safe_comp_file = comp.replace(" ", "_").replace("&", "_").replace("(", "").replace(")", "")
    cv_link = f"../../Company_Tailored_CVs/CV_{jid}_{safe_comp_file}.md"
    cl_link = f"../../Company_Tailored_CVs/Cover_Letter_{jid}_{safe_comp_file}.md"

    html_parts.append(f"""
          <tr data-track="{track}" data-search="{comp.lower()} {role.lower()} {rec_name.lower()}">
            <td>
              <div class="company-cell">{comp}</div>
              <div style="font-size:11px;color:var(--muted);font-family:'JetBrains Mono';">{jid}</div>
            </td>
            <td>
              <div class="role-cell">{role}</div>
              <div style="font-size:12px;color:var(--muted);margin-top:2px;">{j['location']}</div>
            </td>
            <td><span class="badge badge-track">{track}</span></td>
            <td><span class="badge badge-score">{score}/100</span></td>
            <td>{rec_display}</td>
            <td>
              <div class="action-group">
                <button class="action-btn" onclick="openInMailModal('{clean_comp}', '{clean_role}', '{clean_rec}', `{inmail_msg}`)">✉️ InMail</button>
                <a href="{portal_url}" target="_blank" class="action-btn">🌐 Portal</a>
              </div>
            </td>
          </tr>
""")

html_parts.append("""
        </tbody>
      </table>
    </div>
  </div>

  <div class="modal" id="inmailModal">
    <div class="modal-card">
      <div class="modal-header">
        <h3 id="modalTitle">Pre-Composed Recruiter InMail</h3>
        <button class="close-btn" onclick="closeModal()">&times;</button>
      </div>
      <div class="inmail-box" id="modalContent"></div>
      <div class="modal-actions">
        <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        <button class="btn btn-primary" onclick="copyInMail()">📋 Copy to Clipboard</button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast">✓ InMail Copied to Clipboard!</div>

  <script>
    let currentTrack = 'ALL';
    let currentInMail = '';

    function filterJobs() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const rows = document.querySelectorAll('#tableBody tr');
      rows.forEach(r => {
        const text = r.getAttribute('data-search') || '';
        const track = r.getAttribute('data-track') || '';
        const matchesTrack = currentTrack === 'ALL' || track === currentTrack;
        const matchesQuery = !q || text.includes(q);
        r.style.display = (matchesTrack && matchesQuery) ? '' : 'none';
      });
    }

    function setTrack(track, btn) {
      currentTrack = track;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterJobs();
    }

    function openInMailModal(comp, role, recruiter, msg) {
      currentInMail = msg;
      document.getElementById('modalTitle').innerText = 'InMail: ' + comp + ' (' + recruiter + ')';
      document.getElementById('modalContent').innerText = msg;
      document.getElementById('inmailModal').classList.add('active');
    }

    function closeModal() {
      document.getElementById('inmailModal').classList.remove('active');
    }

    function copyInMail() {
      navigator.clipboard.writeText(currentInMail).then(() => {
        const toast = document.getElementById('toast');
        toast.style.display = 'block';
        setTimeout(() => { toast.style.display = 'none'; }, 2500);
      });
    }
  </script>
</body>
</html>
""")

out_path = Path("apps/job_application_studio/command_center.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(html_parts))

print(f"Successfully built {out_path} with {len(jobs)} interactive requisitions!")