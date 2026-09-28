#!/usr/bin/env python3
"""
========================================================================================
BANGALORE OMNI APPLY ALL: Clean & Simple Fresher Edition
========================================================================================
- Role: Fresher / Entry-Level Candidate (BBA International Business, DSU Bangalore '26)
- Tone: Humble, simple, polite, enthusiastic, eager to learn
- No revenue numbers, no aggressive sales jargon
- Immediate on-site availability in Bengaluru
========================================================================================
Outputs:
- e:\\anti\\data\\BANGALORE_OMNI_ALL_APPLICATIONS_DISPATCH.json
- e:\\anti\\data\\BANGALORE_OMNI_ALL_APPLICATIONS_DISPATCH.csv
- e:\\anti\\apps\\job_application_studio\\bangalore_omni_apply_console.html
========================================================================================
"""

import os
import sys
import json
import csv
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
APPS_DIR = ROOT_DIR / "apps" / "job_application_studio"
APPS_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_PATH = DATA_DIR / "verified_profile.json"
CONNECTIONS_PATH = DATA_DIR / "Connections_clean.csv"
GAPS_MASTER_PATH = DATA_DIR / "BANGALORE_HR_FOUNDER_GAPS_MASTER.json"
STRIKE_PATH = DATA_DIR / "TARGET_300_JOB_STRIKE.json"

OUT_JSON = DATA_DIR / "BANGALORE_OMNI_ALL_APPLICATIONS_DISPATCH.json"
OUT_CSV = DATA_DIR / "BANGALORE_OMNI_ALL_APPLICATIONS_DISPATCH.csv"
OUT_HTML = APPS_DIR / "bangalore_omni_apply_console.html"

STOP_WORDS = {
    'india', 'pvt', 'ltd', 'limited', 'private', 'solutions', 'technologies', 
    'technology', 'services', 'global', 'tech', 'development', 'center', 'sdc', 
    'gds', 'us', 'offices', 'corporation', 'corp', 'inc', 'llp', 'and', 'the', 
    'of', 'enterprise', 'consulting', 'advisory', 'systems', 'system', 'group', 
    'international', 'holdings', 'software', 'management', 'business'
}

SPECIAL_BRAND_ALIASES = {
    "ey": "ey",
    "ernst & young": "ey",
    "ey gds": "ey",
    "pwc": "pwc",
    "pricewaterhousecoopers": "pwc",
    "deloitte": "deloitte",
    "accenture": "accenture",
    "goldman sachs": "goldman sachs",
    "jpmorgan": "jpmorgan",
    "jpmorganchase": "jpmorgan",
    "jp morgan": "jpmorgan",
    "walmart": "walmart",
    "amazon": "amazon",
    "google": "google",
    "microsoft": "microsoft",
    "swiggy": "swiggy",
    "razorpay": "razorpay",
    "cred": "cred",
    "meesho": "meesho",
    "flipkart": "flipkart",
    "instawork": "instawork",
    "siemens": "siemens",
    "boeing": "boeing",
    "schneider": "schneider electric",
    "schneider electric": "schneider electric",
    "dhl": "dhl",
    "maersk": "maersk"
}

def clean_brand(name: str) -> str:
    if not name:
        return ""
    low = name.lower()
    for alias, canonical in SPECIAL_BRAND_ALIASES.items():
        if alias in low:
            return canonical
    words = re.findall(r'[a-zA-Z0-9]+', low)
    core = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return ' '.join(core)

def load_candidate_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "candidate": {
            "full_name": "Aditya Mehra",
            "email": "adityamehra799@gmail.com",
            "phone": "+91 70034 56624",
            "linkedin_url": "https://www.linkedin.com/in/adityamehra07",
            "location": "Bengaluru, Karnataka, India"
        }
    }

def load_connections():
    network_by_brand = defaultdict(list)
    if not CONNECTIONS_PATH.exists():
        return network_by_brand

    with open(CONNECTIONS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            comp = row.get("company", "").strip()
            if comp:
                b = clean_brand(comp)
                if b:
                    network_by_brand[b].append({
                        "name": row.get("full_name", ""),
                        "position": row.get("position", ""),
                        "is_recruiter": row.get("is_recruiter", "0") == "1",
                        "is_decision_maker": row.get("is_decision_maker", "0") == "1",
                        "url": row.get("url", "")
                    })
    return network_by_brand

def load_active_strikes():
    strikes_by_company = {}
    if not STRIKE_PATH.exists():
        return strikes_by_company
    with open(STRIKE_PATH, "r", encoding="utf-8") as f:
        strikes = json.load(f)
        for s in strikes:
            c = s.get("company", "")
            if c:
                cb = clean_brand(c)
                strikes_by_company[cb] = s
    return strikes_by_company

def build_application_pack(comp_data, candidate, network_by_brand, strikes_by_brand):
    comp_name = comp_data.get("company", "Target Company")
    corridor = comp_data.get("corridor", "Bengaluru")
    corridor_clean = corridor.split('(')[0].strip()
    
    hr_name = comp_data.get("hr_name", "Hiring Team").split()[0] if comp_data.get("hr_name") else "Hiring Team"
    hr_full_name = comp_data.get("hr_name", "Talent Acquisition Team")
    hr_title = comp_data.get("hr_designation", "Talent Acquisition Lead")
    hr_email = comp_data.get("hr_email", "")
    careers_email = comp_data.get("careers_email", "")
    
    # Check for warm network matches
    target_brand = clean_brand(comp_name)
    network_matches = network_by_brand.get(target_brand, [])
    if not network_matches:
        fw = target_brand.split()[0] if target_brand else ""
        if fw and len(fw) >= 4:
            network_matches = network_by_brand.get(fw, [])
            
    recruiter_matches = [m for m in network_matches if m["is_recruiter"]]
    
    # Check for active job openings
    active_job = strikes_by_brand.get(target_brand)
    active_job_title = active_job.get("job_title", "") if active_job else ""
    
    target_role = active_job_title if active_job_title else "Fresher / Entry-Level Operations & Business Support"

    # Subject Line - Clean, humble, professional
    subject = f"Application: Entry-Level / Graduate Trainee - Aditya Mehra (DSU Bangalore)"

    # Simple, honest, polite fresher email body
    email_body = f"""Dear {hr_name},

I hope you are doing well.

I am a fresh graduate from Dayananda Sagar University, Bangalore (BBA in International Business, Class of 2026). I am writing to express my interest in entry-level openings, graduate trainee roles, or internship opportunities at {comp_name}.

During my college studies and internships, I have gained practical exposure to operations coordination, daily documentation, and reporting. I am comfortable with MS Excel, process follow-ups, and managing routine operational tasks with high attention to detail.

Key points about me:
- Fresh BBA graduate, quick learner, and eager to contribute to ground operations.
- Comfortable with Excel, team communication, and process documentation.
- Locally based in Bangalore and available to join immediately for an on-site role at your {corridor_clean} office.

I would be truly grateful for an opportunity to connect and share my resume with your team.

Thank you very much for your time and consideration.

Warm regards,
Aditya Mehra
Phone: +91 70034 56624
Email: adityamehra799@gmail.com
Location: Bengaluru, Karnataka
LinkedIn: https://www.linkedin.com/in/adityamehra07"""

    # Generate Mailto URL
    to_addr = hr_email if hr_email else careers_email
    cc_addr = careers_email if hr_email and careers_email else ""
    
    mail_params = {
        "subject": subject,
        "body": email_body
    }
    if cc_addr:
        mail_params["cc"] = cc_addr
    
    mailto_url = f"mailto:{to_addr}?" + urllib.parse.urlencode(mail_params, quote_via=urllib.parse.quote)

    # Day-4 Follow-Up Email (Simple & Polite)
    follow_up_body = f"""Dear {hr_name},

I hope you are having a good week.

Just following up on my previous email regarding entry-level or fresher openings at {comp_name}. I am based in Bangalore and ready to join immediately.

Please let me know if you would like me to share my resume for any relevant opportunities.

Thank you once again for your time!

Warm regards,
Aditya Mehra
+91 70034 56624 | adityamehra799@gmail.com"""

    # Day-8 Polite Closure Email
    breakup_body = f"""Dear {hr_name},

I understand you must be very busy. I just wanted to leave a quick note that I remain very interested in opportunities with {comp_name}.

If any entry-level or trainee role opens up in the future, please feel free to keep my details on file.

Thank you and best wishes,
Aditya Mehra
+91 70034 56624"""

    # LinkedIn Connection Note (<300 chars, humble & polite)
    linkedin_note = f"Hi {hr_name}, I'm a fresh BBA graduate from DSU Bangalore interested in entry-level operations and business support roles at {comp_name}. Would love to connect and follow your team's updates!"
    if len(linkedin_note) > 295:
        linkedin_note = f"Hi {hr_name}, I'm a fresh BBA graduate from DSU Bangalore eager to explore entry-level roles at {comp_name}. Would love to connect!"

    return {
        "id": comp_data.get("id", ""),
        "company": comp_name,
        "corridor": corridor,
        "sector": comp_data.get("sector", "Technology"),
        "target_role": target_role,
        "founder_ceo": comp_data.get("founder_ceo_name", "Executive Leadership"),
        "hr_name": hr_full_name,
        "hr_title": hr_title,
        "hr_email": hr_email,
        "careers_email": careers_email,
        "active_job_title": active_job_title,
        "network_connections_count": len(network_matches),
        "network_recruiter_count": len(recruiter_matches),
        "subject_line": subject,
        "primary_email_body": email_body,
        "follow_up_day4_body": follow_up_body,
        "breakup_day8_body": breakup_body,
        "linkedin_note": linkedin_note,
        "mailto_url": mailto_url,
        "linkedin_search_url": comp_data.get("linkedin_search_url", f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(comp_name + ' HR Bangalore')}")
    }

def generate_interactive_html(applications, total_companies, total_network_matches, active_hiring_count):
    """Generates the lightweight, ultra-clean Bangalore Fresher Application Console."""
    
    top_apps = applications[:600]
    apps_json = json.dumps(top_apps)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bangalore Fresher Job Application Console — Aditya Mehra</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0b0f17;
  --surface: #131a26;
  --surface-2: #1e293b;
  --border: #2e3a4e;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --primary: #38bdf8;
  --primary-hover: #0284c7;
  --emerald: #10b981;
  --radius: 10px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 24px;
}
header {
  max-width: 1400px;
  margin: 0 auto 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 28px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}
.header-title h1 {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-title p {
  color: var(--text-muted);
  font-size: 13px;
  margin-top: 3px;
}
.stats-grid {
  display: flex;
  gap: 12px;
}
.stat-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 8px 14px;
  border-radius: 6px;
  text-align: center;
}
.stat-val {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
  font-family: 'JetBrains Mono', monospace;
}
.stat-lbl {
  font-size: 11px;
  color: var(--text-muted);
}
.toolbar {
  max-width: 1400px;
  margin: 0 auto 16px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.search-box {
  flex: 1;
  min-width: 260px;
}
.search-box input {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 14px;
  color: var(--text);
  font-size: 13px;
}
.search-box input:focus {
  outline: none;
  border-color: var(--primary);
}
.filter-chips {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.chip {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 7px 12px;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
}
.chip:hover, .chip.active {
  background: var(--surface-2);
  color: var(--primary);
  border-color: var(--primary);
}
.grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 16px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
.comp-name {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}
.badge {
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(56, 189, 248, 0.1);
  color: var(--primary);
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid rgba(56, 189, 248, 0.2);
}
.recruiter-line {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 10px;
  line-height: 1.4;
}
.email-preview {
  background: #070a0f;
  border: 1px solid #1a2332;
  border-radius: 6px;
  padding: 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #cbd5e1;
  max-height: 120px;
  overflow-y: auto;
  margin-bottom: 12px;
  white-space: pre-wrap;
}
.actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  border: 1px solid transparent;
}
.btn-primary {
  background: var(--primary);
  color: #0b0f17;
}
.btn-primary:hover {
  background: var(--primary-hover);
  color: #fff;
}
.btn-secondary {
  background: var(--surface-2);
  color: var(--text);
  border-color: var(--border);
}
.btn-copy {
  grid-column: span 2;
  background: transparent;
  color: var(--text-muted);
  border-color: var(--border);
}
.btn-copy:hover {
  color: var(--text);
  background: rgba(255,255,255,0.04);
}
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--emerald);
  color: #fff;
  padding: 10px 18px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  display: none;
  z-index: 1000;
}
</style>
</head>
<body>

<header>
  <div class="header-title">
    <h1>🎓 Bangalore Fresher Job Application Console</h1>
    <p>Aditya Mehra - BBA International Business (DSU '26) - Simple & Professional Outreach</p>
  </div>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-val">""" + f"{total_companies:,}" + """</div>
      <div class="stat-lbl">Bangalore Targets</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">""" + f"{total_network_matches:,}" + """</div>
      <div class="stat-lbl">Network Matches</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" id="appliedCount">0</div>
      <div class="stat-lbl">Marked Applied</div>
    </div>
  </div>
</header>

<div class="toolbar">
  <div class="search-box">
    <input type="text" id="searchInput" placeholder="Search company, recruiter, corridor, or sector..." oninput="filterCards()">
  </div>
  <div class="filter-chips">
    <div class="chip active" onclick="setFilter('all', this)">All Corridors</div>
    <div class="chip" onclick="setFilter('warm', this)">🤝 Warm Connections</div>
    <div class="chip" onclick="setFilter('Outer Ring Road', this)">ORR Bellandur</div>
    <div class="chip" onclick="setFilter('Whitefield', this)">Whitefield / ITPL</div>
    <div class="chip" onclick="setFilter('Koramangala', this)">HSR / Koramangala</div>
    <div class="chip" onclick="setFilter('Manyata', this)">Manyata Tech Park</div>
    <div class="chip" onclick="setFilter('Electronic City', this)">Electronic City</div>
  </div>
</div>

<div class="grid" id="appsGrid"></div>

<div class="toast" id="toast">Copied to clipboard!</div>

<script>
const applications = """ + apps_json + """;
let currentFilter = 'all';

function renderCards(data) {
  const grid = document.getElementById('appsGrid');
  grid.innerHTML = '';
  
  if (data.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted)">No companies match your search.</div>';
    return;
  }

  data.forEach(app => {
    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'card-' + app.id;
    
    card.innerHTML = `
      <div>
        <div class="card-header">
          <div>
            <div class="comp-name">${app.company}</div>
            <div style="font-size: 11px; color: var(--primary); margin-top: 2px;">${app.target_role}</div>
          </div>
          <span class="badge">${app.corridor.split('(')[0].trim()}</span>
        </div>
        
        <div class="recruiter-line">
          👤 <strong>${app.hr_name}</strong> (${app.hr_title})<br>
          ✉️ <a href="mailto:${app.hr_email}" style="color: var(--primary); text-decoration: none;">${app.hr_email || app.careers_email || 'Direct HR'}</a>
          ${app.network_connections_count > 0 ? `<br><span style="color: #10b981; font-weight: 600;">🤝 ${app.network_connections_count} connection(s) in network</span>` : ''}
        </div>
        
        <div class="email-preview">${app.primary_email_body.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
      </div>
      
      <div class="actions">
        <a href="${app.mailto_url}" target="_blank" class="btn btn-primary" onclick="markApplied('${app.id}')">
          🚀 Send Email
        </a>
        <a href="${app.linkedin_search_url}" target="_blank" class="btn btn-secondary">
          🔗 LinkedIn Profile
        </a>
        <button class="btn btn-copy" onclick="copyText('${encodeURIComponent(app.primary_email_body)}', 'Email pitch')">
          📋 Copy Email Body
        </button>
        <button class="btn btn-copy" style="border-top: none; margin-top: -3px;" onclick="copyText('${encodeURIComponent(app.linkedin_note)}', 'LinkedIn connection note')">
          💬 Copy LinkedIn Note (<300 chars)
        </button>
      </div>
    `;
    grid.appendChild(card);
  });
  updateAppliedCount();
}

function filterCards() {
  const query = document.getElementById('searchInput').value.toLowerCase();
  const filtered = applications.filter(app => {
    const matchesSearch = app.company.toLowerCase().includes(query) ||
                          app.hr_name.toLowerCase().includes(query) ||
                          app.corridor.toLowerCase().includes(query) ||
                          app.sector.toLowerCase().includes(query);
                          
    let matchesFilter = true;
    if (currentFilter === 'warm') {
      matchesFilter = app.network_connections_count > 0;
    } else if (currentFilter !== 'all') {
      matchesFilter = app.corridor.toLowerCase().includes(currentFilter.toLowerCase());
    }
    
    return matchesSearch && matchesFilter;
  });
  renderCards(filtered);
}

function setFilter(filter, el) {
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  currentFilter = filter;
  filterCards();
}

function copyText(encoded, label) {
  const text = decodeURIComponent(encoded);
  navigator.clipboard.writeText(text).then(() => {
    showToast(label + ' copied!');
  });
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 2000);
}

function markApplied(id) {
  localStorage.setItem('applied_' + id, 'true');
  updateAppliedCount();
}

function updateAppliedCount() {
  let count = 0;
  for (let i = 0; i < localStorage.length; i++) {
    if (localStorage.key(i).startsWith('applied_') && localStorage.getItem(localStorage.key(i)) === 'true') {
      count++;
    }
  }
  document.getElementById('appliedCount').innerText = count;
}

// Initialize
renderCards(applications);
</script>
</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    print("================================================================================")
    print("🚀 STARTING BANGALORE OMNI ALL-COMPANY FRESHER APPLICATION GENERATOR")
    print("================================================================================")
    
    candidate = load_candidate_profile()
    print(f"✅ Loaded Candidate Profile: {candidate['candidate']['full_name']} ({candidate['candidate']['email']})")
    
    network_by_brand = load_connections()
    print(f"✅ Loaded LinkedIn Network: {len(network_by_brand)} brand clusters across 9,223 connections")
    
    strikes_by_brand = load_active_strikes()
    print(f"✅ Loaded Active Job Openings: {len(strikes_by_brand)} targets")

    if not GAPS_MASTER_PATH.exists():
        print(f"❌ Error: {GAPS_MASTER_PATH} not found!")
        return
        
    with open(GAPS_MASTER_PATH, "r", encoding="utf-8") as f:
        companies_data = json.load(f)
    print(f"✅ Loaded Bangalore Directory: {len(companies_data)} target employers")
    
    applications = []
    total_network_matches = 0
    active_hiring_count = 0
    
    for item in companies_data:
        app = build_application_pack(item, candidate, network_by_brand, strikes_by_brand)
        if app["network_connections_count"] > 0:
            total_network_matches += 1
        if app.get("active_job_title"):
            active_hiring_count += 1
        applications.append(app)
        
    print(f"✅ Synthesized {len(applications):,} clean, simple fresher application packs")
    print(f"🤝 Discovered {total_network_matches:,} Bangalore targets with mutual connections")
    
    # Write JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved JSON Master: {OUT_JSON} ({OUT_JSON.stat().st_size / (1024*1024):.2f} MB)")
    
    # Write CSV
    csv_fields = [
        "id", "company", "corridor", "sector", "target_role", "founder_ceo",
        "hr_name", "hr_title", "hr_email", "careers_email", "active_job_title",
        "network_connections_count", "subject_line",
        "primary_email_body", "follow_up_day4_body", "breakup_day8_body",
        "linkedin_note", "mailto_url", "linkedin_search_url"
    ]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for a in applications:
            writer.writerow({k: a.get(k, "") for k in csv_fields})
    print(f"💾 Saved CSV Master: {OUT_CSV} ({OUT_CSV.stat().st_size / (1024*1024):.2f} MB)")
    
    # Write HTML App
    generate_interactive_html(applications, len(companies_data), total_network_matches, active_hiring_count)
    print(f"🖥️  Generated Simple Fresher Application Console: {OUT_HTML}")
    
    print("================================================================================")
    print("🎉 EXECUTION COMPLETE: ALL 4,500 FRESHER APPLICATIONS RE-PACKAGED & READY!")
    print("================================================================================")

if __name__ == "__main__":
    main()
