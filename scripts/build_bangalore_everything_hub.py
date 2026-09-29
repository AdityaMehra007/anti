#!/usr/bin/env python3
"""
Builds the OMEGA Bangalore Everything Master Hub HTML application:
E:\anti\apps\job_application_studio\bangalore_everything_master_hub.html
"""

import json
import sqlite3
import os
import re

DB_PATH = r"E:\anti\data\aditya_global_career_intelligence.db"
TARGETS_PATH = r"E:\anti\data\BANGALORE_MEGA_4500_TARGETS.json"
SCORED_JOBS_PATH = r"E:\anti\data\BANGALORE_SCORED_JOBS_MASTER.json"
TECH_PARKS_PATH = r"E:\anti\data\bangalore_tech_parks_master.json"
OUTPUT_HTML = r"E:\anti\apps\job_application_studio\bangalore_everything_master_hub.html"

def load_data():
    print("Loading SQLite data...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Summary stats
    total_companies = c.execute("SELECT count(*) FROM companies").fetchone()[0]
    total_people = c.execute("SELECT count(*) FROM people").fetchone()[0]
    total_jobs = c.execute("SELECT count(*) FROM jobs").fetchone()[0]
    total_recruiters = c.execute("SELECT count(*) FROM people WHERE classification='RECRUITER'").fetchone()[0]
    total_hiring_managers = c.execute("SELECT count(*) FROM people WHERE classification='HIRING_MANAGER'").fetchone()[0]
    
    # Load targets (top 1500 for snappy performance in single-file HTML)
    print("Loading Mega targets...")
    with open(TARGETS_PATH, "r", encoding="utf-8") as f:
        all_targets = json.load(f)
    curated_targets = all_targets[:1200]  # rich, snappy
    
    # Load scored jobs
    print("Loading scored jobs...")
    with open(SCORED_JOBS_PATH, "r", encoding="utf-8") as f:
        scored_jobs = json.load(f)
        
    # Load tech parks
    print("Loading tech parks...")
    with open(TECH_PARKS_PATH, "r", encoding="utf-8") as f:
        tech_parks = json.load(f)

    # Load top jobs from DB
    print("Loading database jobs...")
    db_jobs = []
    for r in c.execute("SELECT job_id, company_name, job_title, normalized_title, experience_min, experience_max, skills, application_url, ats FROM jobs LIMIT 300").fetchall():
        db_jobs.append({
            "id": r[0],
            "company": r[1],
            "title": r[2],
            "normalized_title": r[3],
            "exp_min": r[4],
            "exp_max": r[5],
            "skills": r[6] or "Enterprise Execution, Operations, Tech",
            "url": r[7] or "#",
            "ats": r[8] or "Enterprise Portal"
        })
        
    conn.close()
    
    return {
        "stats": {
            "total_companies": total_companies,
            "total_people": total_people,
            "total_jobs": total_jobs,
            "total_recruiters": total_recruiters,
            "total_hiring_managers": total_hiring_managers,
            "curated_count": len(curated_targets)
        },
        "targets": curated_targets,
        "scored_jobs": scored_jobs,
        "db_jobs": db_jobs,
        "tech_parks": tech_parks
    }

def generate_html(data):
    stats = data["stats"]
    targets_json = json.dumps(data["targets"])
    scored_jobs_json = json.dumps(data["scored_jobs"])
    db_jobs_json = json.dumps(data["db_jobs"])
    tech_parks_json = json.dumps(data["tech_parks"])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bangalore Everything Master Hub — 7,618+ Companies & Hiring Radar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-dark: #07090e;
  --bg-card: #0d121c;
  --bg-card-hover: #131b2a;
  --border: #1e293b;
  --border-focus: #3b82f6;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --accent-cyan: #06b6d4;
  --accent-blue: #3b82f6;
  --accent-indigo: #6366f1;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  background-color: var(--bg-dark);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}

/* Header Banner */
.top-header {{
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(7, 9, 14, 0.95) 100%);
  border-bottom: 1px solid var(--border);
  padding: 20px 32px;
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
}}

.header-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
  gap: 20px;
}}

.logo-group {{
  display: flex;
  align-items: center;
  gap: 14px;
}}

.badge-tag {{
  background: rgba(6, 182, 212, 0.15);
  color: var(--accent-cyan);
  border: 1px solid rgba(6, 182, 212, 0.3);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

.title-main {{
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, #ffffff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.subtitle-desc {{
  font-size: 12px;
  color: var(--text-muted);
}}

.stat-pills {{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}}

.stat-pill {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 6px 14px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}}

.stat-num {{
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-cyan);
}}

.stat-lbl {{
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
}}

/* Navigation Tabs */
.nav-bar {{
  background: rgba(13, 18, 28, 0.6);
  border-bottom: 1px solid var(--border);
  padding: 0 32px;
  position: sticky;
  top: 85px;
  z-index: 40;
  backdrop-filter: blur(10px);
}}

.tabs-container {{
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  gap: 4px;
  overflow-x: auto;
}}

.tab-btn {{
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 600;
  padding: 14px 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  white-space: nowrap;
}}

.tab-btn:hover {{
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.02);
}}

.tab-btn.active {{
  color: var(--accent-cyan);
  border-bottom: 2px solid var(--accent-cyan);
  background: rgba(6, 182, 212, 0.05);
}}

/* Main Body */
.main-wrapper {{
  max-width: 1600px;
  margin: 0 auto;
  padding: 24px 32px 60px 32px;
  width: 100%;
  flex: 1;
}}

/* Search & Filter Toolbar */
.toolbar {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}}

.search-row {{
  display: flex;
  gap: 12px;
  align-items: center;
}}

.search-input {{
  flex: 1;
  background: #090d15;
  border: 1px solid var(--border);
  color: var(--text-main);
  font-family: var(--font-sans);
  font-size: 14px;
  padding: 10px 16px;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s ease;
}}

.search-input:focus {{
  border-color: var(--accent-cyan);
}}

.filter-select {{
  background: #090d15;
  border: 1px solid var(--border);
  color: var(--text-main);
  font-family: var(--font-sans);
  font-size: 13px;
  padding: 10px 14px;
  border-radius: 8px;
  outline: none;
  cursor: pointer;
}}

.action-btn {{
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  color: #fff;
  border: none;
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 13px;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: opacity 0.2s;
}}

.action-btn:hover {{
  opacity: 0.9;
}}

.action-btn.secondary {{
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border);
  color: var(--text-main);
}}

.action-btn.secondary:hover {{
  background: rgba(255, 255, 255, 0.1);
}}

/* Grid & Cards */
.grid-container {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}}

.card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.15s ease, border-color 0.15s ease;
  position: relative;
}}

.card:hover {{
  transform: translateY(-2px);
  border-color: rgba(6, 182, 212, 0.4);
  background: var(--bg-card-hover);
}}

.card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}}

.company-title {{
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
}}

.sector-tag {{
  font-size: 11px;
  color: var(--accent-cyan);
  background: rgba(6, 182, 212, 0.1);
  padding: 3px 8px;
  border-radius: 4px;
  margin-top: 4px;
  display: inline-block;
}}

.fit-badge {{
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent-emerald);
  border: 1px solid rgba(16, 185, 129, 0.3);
}}

.card-body {{
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 16px;
}}

.card-row {{
  display: flex;
  align-items: center;
  gap: 6px;
}}

.card-footer {{
  display: flex;
  gap: 8px;
  border-top: 1px solid var(--border);
  padding-top: 12px;
  margin-top: auto;
}}

.card-btn {{
  flex: 1;
  text-align: center;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.15s;
}}

.card-btn.primary {{
  background: #0284c7;
  color: white;
}}

.card-btn.primary:hover {{
  background: #0369a1;
}}

.card-btn.secondary {{
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  border: 1px solid var(--border);
}}

.card-btn.secondary:hover {{
  background: rgba(255, 255, 255, 0.1);
}}

/* Prompt Studio Tab */
.prompt-panel {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
}}

.prompt-controls {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}}

.form-group {{
  display: flex;
  flex-direction: column;
  gap: 6px;
}}

.form-group label {{
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}}

.form-group input, .form-group select {{
  background: #090d15;
  border: 1px solid var(--border);
  color: var(--text-main);
  padding: 8px 12px;
  border-radius: 6px;
  font-family: var(--font-sans);
  font-size: 13px;
}}

.prompt-display {{
  background: #05070a;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.6;
  color: #38bdf8;
  max-height: 520px;
  overflow-y: auto;
  white-space: pre-wrap;
  position: relative;
}}

.copy-float-btn {{
  position: absolute;
  top: 14px;
  right: 14px;
  background: var(--accent-cyan);
  color: #000;
  border: none;
  font-weight: 700;
  font-size: 12px;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
}}

/* Empty / Loading States */
.empty-msg {{
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
  font-size: 14px;
}}
</style>
</head>
<body>

<!-- Header -->
<header class="top-header">
  <div class="header-row">
    <div class="logo-group">
      <span class="badge-tag">OMEGA &infin; APEX</span>
      <div>
        <h1 class="title-main">Bangalore Everything Master Hub</h1>
        <p class="subtitle-desc">Unified Corporate & Hiring Intelligence Across 7,618 Companies, 12,800 HR Leads & 6 Tech Corridors</p>
      </div>
    </div>
    
    <div class="stat-pills">
      <div class="stat-pill">
        <span class="stat-num">{stats['total_companies']:,}</span>
        <span class="stat-lbl">BLR Companies</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">{stats['total_recruiters']:,}</span>
        <span class="stat-lbl">Recruiters</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">{stats['total_hiring_managers']:,}</span>
        <span class="stat-lbl">Decision Makers</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">{stats['total_jobs']:,}</span>
        <span class="stat-lbl">Active Jobs</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">20</span>
        <span class="stat-lbl">Tech Parks</span>
      </div>
    </div>
  </div>
</header>

<!-- Navigation Bar -->
<nav class="nav-bar">
  <div class="tabs-container">
    <button class="tab-btn active" onclick="switchTab('tab-companies')">🏢 Companies Directory ({stats['curated_count']:,})</button>
    <button class="tab-btn" onclick="switchTab('tab-jobs')">💼 Scored Hiring Radar ({len(data['scored_jobs'])})</button>
    <button class="tab-btn" onclick="switchTab('tab-db-jobs')">📋 All Requisitions ({len(data['db_jobs'])})</button>
    <button class="tab-btn" onclick="switchTab('tab-parks')">📍 20 Tech Parks & Corridors</button>
    <button class="tab-btn" onclick="switchTab('tab-prompt')">⚡ The Apex Mega-Prompt Generator</button>
  </div>
</nav>

<!-- Main Container -->
<main class="main-wrapper">

  <!-- TAB 1: COMPANIES DIRECTORY -->
  <section id="tab-companies" class="tab-content">
    <div class="toolbar">
      <div class="search-row">
        <input type="text" id="companySearch" class="search-input" placeholder="Search by company name, HR lead, corridor, or tech stack..." oninput="filterCompanies()">
        <select id="sectorFilter" class="filter-select" onchange="filterCompanies()">
          <option value="">All Sectors (10 Industries)</option>
          <option value="Global Capability Centers">GCCs & Tech Giants</option>
          <option value="Enterprise SaaS">Enterprise SaaS & Cloud</option>
          <option value="FinTech">FinTech & Payments</option>
          <option value="EXIM">EXIM & Global Logistics</option>
          <option value="Aerospace">Aerospace & Heavy Eng</option>
          <option value="Automotive">Automotive & EV</option>
          <option value="Investment Banking">Investment Banking</option>
        </select>
        <select id="corridorFilter" class="filter-select" onchange="filterCompanies()">
          <option value="">All Corridors (6 Zones)</option>
          <option value="Outer Ring Road">Outer Ring Road (ORR)</option>
          <option value="Whitefield">Whitefield & ITPL</option>
          <option value="Manyata">Manyata & Hebbal</option>
          <option value="Koramangala">Koramangala & HSR</option>
          <option value="Electronic City">Electronic City</option>
          <option value="Central">CBD & MG Road</option>
        </select>
        <button class="action-btn secondary" onclick="exportCompaniesCSV()">📥 Export Filtered CSV</button>
      </div>
    </div>
    
    <div id="companiesGrid" class="grid-container">
      <!-- Dynamic Company Cards -->
    </div>
  </section>

  <!-- TAB 2: SCORED HIRING RADAR -->
  <section id="tab-jobs" class="tab-content" style="display:none;">
    <div class="toolbar">
      <div class="search-row">
        <input type="text" id="jobSearch" class="search-input" placeholder="Filter scored jobs by role, company, or tier..." oninput="filterScoredJobs()">
        <button class="action-btn secondary" onclick="exportJobsJSON()">📥 Export Jobs JSON</button>
      </div>
    </div>
    
    <div id="jobsGrid" class="grid-container">
      <!-- Dynamic Scored Job Cards -->
    </div>
  </section>

  <!-- TAB 3: ALL REQUISITIONS -->
  <section id="tab-db-jobs" class="tab-content" style="display:none;">
    <div class="toolbar">
      <div class="search-row">
        <input type="text" id="dbJobSearch" class="search-input" placeholder="Search database jobs by title, company, or skills..." oninput="filterDbJobs()">
      </div>
    </div>
    
    <div id="dbJobsGrid" class="grid-container">
      <!-- Dynamic DB Job Cards -->
    </div>
  </section>

  <!-- TAB 4: TECH PARKS & CORRIDORS -->
  <section id="tab-parks" class="tab-content" style="display:none;">
    <div class="grid-container" id="parksGrid">
      <!-- Dynamic Tech Park Cards -->
    </div>
  </section>

  <!-- TAB 5: APEX MEGA-PROMPT GENERATOR -->
  <section id="tab-prompt" class="tab-content" style="display:none;">
    <div class="prompt-panel">
      <div class="prompt-controls">
        <div class="form-group">
          <label>Target Company</label>
          <input type="text" id="pCompany" value="Walmart Global Tech India" oninput="updatePrompt()">
        </div>
        <div class="form-group">
          <label>Target Role / Requisition</label>
          <input type="text" id="pRole" value="Operations & Business Execution Analyst" oninput="updatePrompt()">
        </div>
        <div class="form-group">
          <label>Target Corridor</label>
          <select id="pCorridor" onchange="updatePrompt()">
            <option value="Outer Ring Road (Bellandur / Kadubeesanahalli / Sarjapur)">Outer Ring Road (ORR)</option>
            <option value="Whitefield & ITPL">Whitefield & ITPL</option>
            <option value="Manyata Tech Park & Hebbal">Manyata & Hebbal</option>
            <option value="Koramangala & HSR Layout">Koramangala & HSR</option>
            <option value="Electronic City">Electronic City</option>
            <option value="Central Business District (CBD)">CBD / MG Road</option>
          </select>
        </div>
        <div class="form-group">
          <label>Candidate Profile / Degree</label>
          <input type="text" id="pCandidate" value="Aditya Mehra (BBA International Business DSU '26)" oninput="updatePrompt()">
        </div>
      </div>

      <div style="display: flex; gap: 10px; margin-bottom: 14px;">
        <button class="action-btn" onclick="copyPrompt()">📋 Copy Mega-Prompt</button>
        <button class="action-btn secondary" onclick="openChatGPT()">Launch in ChatGPT &rarr;</button>
        <button class="action-btn secondary" onclick="openClaude()">Launch in Claude &rarr;</button>
      </div>

      <div class="prompt-display">
        <button class="copy-float-btn" onclick="copyPrompt()">Copy</button>
        <pre id="promptText"></pre>
      </div>
    </div>
  </section>

</main>

<script>
// Embedded Data
const targets = {targets_json};
const scoredJobs = {scored_jobs_json};
const dbJobs = {db_jobs_json};
const techParks = {tech_parks_json};

let currentFilteredTargets = targets;

// Tab Switching
function switchTab(tabId) {{
  document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(tabId).style.display = 'block';
  event.currentTarget.classList.add('active');
}}

// Filter & Render Companies
function filterCompanies() {{
  const query = document.getElementById('companySearch').value.toLowerCase();
  const sector = document.getElementById('sectorFilter').value.toLowerCase();
  const corridor = document.getElementById('corridorFilter').value.toLowerCase();

  currentFilteredTargets = targets.filter(t => {{
    const matchesQuery = !query || 
      (t.company && t.company.toLowerCase().includes(query)) ||
      (t.hr_name && t.hr_name.toLowerCase().includes(query)) ||
      (t.corridor && t.corridor.toLowerCase().includes(query)) ||
      (t.job_title && t.job_title.toLowerCase().includes(query));

    const matchesSector = !sector || (t.sector && t.sector.toLowerCase().includes(sector));
    const matchesCorridor = !corridor || (t.corridor && t.corridor.toLowerCase().includes(corridor));

    return matchesQuery && matchesSector && matchesCorridor;
  }});

  renderCompanies();
}}

function renderCompanies() {{
  const grid = document.getElementById('companiesGrid');
  if (currentFilteredTargets.length === 0) {{
    grid.innerHTML = '<div class="empty-msg">No companies found matching your criteria.</div>';
    return;
  }}

  grid.innerHTML = currentFilteredTargets.slice(0, 100).map(t => `
    <div class="card">
      <div class="card-header">
        <div>
          <h3 class="company-title">${{t.company || 'Bangalore Tech Enterprise'}}</h3>
          <span class="sector-tag">${{t.sector ? t.sector.split('&')[0] : 'Tech Enterprise'}}</span>
        </div>
        <span class="fit-badge">Fit: ${{t.fit_score || 90}}%</span>
      </div>
      
      <div class="card-body">
        <div class="card-row">📍 <strong>Corridor:</strong> ${{t.corridor ? t.corridor.split('(')[0] : 'Bengaluru'}}</div>
        <div class="card-row">💼 <strong>Target Role:</strong> ${{t.job_title || 'Operations & Business Analyst'}}</div>
        <div class="card-row">👤 <strong>HR / TA Lead:</strong> ${{t.hr_name || 'Talent Acquisition Team'}}</div>
        <div class="card-row">📧 <strong>Direct Email:</strong> ${{t.hr_email || t.careers_email || 'careers@company.com'}}</div>
        <div class="card-row">📞 <strong>Desk Line:</strong> ${{t.phone || '+91-80-4000-XXXX'}}</div>
      </div>

      <div class="card-footer" style="display:flex; gap:6px; flex-wrap:wrap;">
        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${{encodeURIComponent(t.hr_email || t.careers_email || '')}}&su=${{encodeURIComponent(t.email_subject || '')}}&body=${{encodeURIComponent(t.email_body || '')}}" target="_blank" class="card-btn primary" style="background:#ea4335;">📮 Web Gmail (1-Click)</a>
        <a href="${{t.mailto_url || 'mailto:' + (t.hr_email || '')}}" class="card-btn secondary">✉️ Mail App</a>
        <a href="${{t.linkedin_url || '#'}}" target="_blank" class="card-btn secondary">🔗 LinkedIn</a>
      </div>
    </div>
  `).join('');
}}

// Render Scored Jobs
function filterScoredJobs() {{
  const query = document.getElementById('jobSearch').value.toLowerCase();
  const filtered = scoredJobs.filter(j => 
    !query || 
    (j.company && j.company.toLowerCase().includes(query)) ||
    (j.role && j.role.toLowerCase().includes(query)) ||
    (j.tier && j.tier.toLowerCase().includes(query))
  );

  const grid = document.getElementById('jobsGrid');
  if (filtered.length === 0) {{
    grid.innerHTML = '<div class="empty-msg">No scored jobs found.</div>';
    return;
  }}

  grid.innerHTML = filtered.map(j => `
    <div class="card">
      <div class="card-header">
        <div>
          <h3 class="company-title">${{j.company}}</h3>
          <span class="sector-tag">${{j.tier}}</span>
        </div>
        <span class="fit-badge">${{j.score}} / 10</span>
      </div>
      
      <div class="card-body">
        <div class="card-row">💼 <strong>Role:</strong> ${{j.role}}</div>
        <div class="card-row">📍 <strong>Location:</strong> ${{j.location}}</div>
        <div class="card-row">👤 <strong>Recruiter:</strong> ${{j.recruiter_name}} (${{j.recruiter_title}})</div>
      </div>

      <div class="card-footer" style="display:flex; gap:6px; flex-wrap:wrap;">
        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${{encodeURIComponent((j.mailto_url && j.mailto_url.includes('mailto:')) ? j.mailto_url.split('mailto:')[1].split('?')[0] : '')}}&su=${{encodeURIComponent(j.email_subject || '')}}&body=${{encodeURIComponent(j.email_body || '')}}" target="_blank" class="card-btn primary" style="background:#ea4335;">📮 Web Gmail (1-Click)</a>
        <a href="${{j.mailto_url}}" class="card-btn secondary">✉️ Mail App</a>
        <a href="${{j.portal_url}}" target="_blank" class="card-btn secondary">🌐 Portal</a>
      </div>
    </div>
  `).join('');
}}

// Render DB Jobs
function filterDbJobs() {{
  const query = document.getElementById('dbJobSearch').value.toLowerCase();
  const filtered = dbJobs.filter(j => 
    !query || 
    (j.company && j.company.toLowerCase().includes(query)) ||
    (j.title && j.title.toLowerCase().includes(query)) ||
    (j.skills && j.skills.toLowerCase().includes(query))
  );

  const grid = document.getElementById('dbJobsGrid');
  grid.innerHTML = filtered.slice(0, 100).map(j => `
    <div class="card">
      <div class="card-header">
        <div>
          <h3 class="company-title">${{j.title}}</h3>
          <span class="sector-tag">${{j.company}}</span>
        </div>
        <span class="fit-badge">${{j.exp_min}}-${{j.exp_max}} Yrs</span>
      </div>
      
      <div class="card-body">
        <div class="card-row">⚙️ <strong>ATS:</strong> ${{j.ats}}</div>
        <div class="card-row">🎯 <strong>Skills:</strong> ${{j.skills.substring(0, 75)}}...</div>
      </div>

      <div class="card-footer">
        <a href="${{j.url}}" target="_blank" class="card-btn primary">🚀 Direct Apply</a>
      </div>
    </div>
  `).join('');
}}

// Render Tech Parks
function renderTechParks() {{
  const grid = document.getElementById('parksGrid');
  grid.innerHTML = techParks.map(p => `
    <div class="card">
      <div class="card-header">
        <div>
          <h3 class="company-title">${{p.name}}</h3>
          <span class="sector-tag">${{p.zone || p.corridor || 'Bengaluru'}}</span>
        </div>
      </div>
      
      <div class="card-body">
        <div class="card-row">📍 <strong>Address:</strong> ${{p.address || 'Bengaluru, Karnataka'}}</div>
        <div class="card-row">🚇 <strong>Transit:</strong> ${{p.nearest_metro || p.transit || 'Direct arterial connection'}}</div>
        <div class="card-row">🏢 <strong>Key Tenants:</strong> ${{p.major_companies ? p.major_companies.slice(0, 4).join(', ') : 'Global MNCs & Tech Centers'}}</div>
      </div>

      <div class="card-footer">
        <button class="card-btn secondary" onclick="filterByTechPark('${{p.name}}')">🔍 View Tenants</button>
      </div>
    </div>
  `).join('');
}}

function filterByTechPark(name) {{
  document.getElementById('companySearch').value = name.split(' ')[0];
  switchTab('tab-companies');
  filterCompanies();
}}

// Mega Prompt Generator Logic
function updatePrompt() {{
  const company = document.getElementById('pCompany').value;
  const role = document.getElementById('pRole').value;
  const corridor = document.getElementById('pCorridor').value;
  const candidate = document.getElementById('pCandidate').value;

  const promptTemplate = `# OMEGA APEX BANGALORE CORPORATE & CAREER INTELLIGENCE DIRECTIVE

TARGET ENTITY: ${{company}}
TARGET REQUISITION: ${{role}}
TARGET CORRIDOR: ${{corridor}}
CANDIDATE DOSSIER: ${{candidate}}

You are OMEGA-BENGALURU-PRIME, the world's most capable corporate intelligence engine, talent headhunter, and outbound recruiter for Bengaluru (Bangalore).

EXECUTE THE FOLLOWING 7 MODULES EXHAUSTIVELY:

1. CORPORATE & ENTITY DEEP-DIVE:
   - Identify Indian legal subsidiary entity, CIN/MCA status, founding year, and Bangalore campus block.
   - Headcount scale (Bangalore vs Global), revenue bracket, funding/market cap, core business model.
   - Core production technology stack, cloud infrastructure, and enterprise platforms.

2. LIVE HIRING & REQUISITION RADAR:
   - Open positions matching ${{role}} across Entry (0-2y), Mid (3-6y), and Senior (7y+).
   - ATS vendor detection (Workday/Greenhouse/Lever/Darwinbox/Taleo) and direct application link.
   - Mandatory keywords and competency filters.

3. RECRUITER & DECISION-MAKER HARVESTING:
   - Identify Head of Talent Acquisition, Lead Technical Recruiter, and Department VP/Director at ${{company}} in Bengaluru.
   - Provide verified email syntax (e.g. first.last@company.com), Bangalore desk line (+91-80-XXXX-XXXX), and LinkedIn search query.

4. 9-VECTOR FIT MATCHING & ATS KEYWORDS:
   - Score candidate fit (0-100) based on ${{candidate}} against ${{role}}.
   - List the top 10 mandatory ATS keyword tokens to inject into the resume.

5. 3-CHANNEL OUTBOUND OUTREACH SUITE:
   - Generate a 120-150 word high-conversion executive cold email with verified proof points.
   - Generate a LinkedIn connection note under 300 characters.
   - Generate an internal employee referral request script.

6. INTERVIEW GAUNTLET & SALARY INTELLIGENCE:
   - Exact 5-stage interview sequence and top 5 company-specific defense questions.
   - Bangalore market compensation calibration: Base INR LPA, Bonus %, ESOP/RSU, and in-hand monthly net.

7. AUTOMATION EXECUTION SCRIPT:
   - Runnable Python script to test SMTP deliverability and monitor the requisition automatically.`;

  document.getElementById('promptText').innerText = promptTemplate;
}}

function copyPrompt() {{
  const text = document.getElementById('promptText').innerText;
  navigator.clipboard.writeText(text).then(() => {{
    alert("Apex Mega-Prompt successfully copied to clipboard!");
  }});
}}

function openChatGPT() {{
  window.open('https://chatgpt.com', '_blank');
}}

function openClaude() {{
  window.open('https://claude.ai', '_blank');
}}

// CSV Export
function exportCompaniesCSV() {{
  const rows = [
    ["Company", "Sector", "Corridor", "Target Role", "HR Lead", "Email", "Phone", "LinkedIn"]
  ];
  currentFilteredTargets.forEach(t => {{
    rows.push([
      `"${{t.company || ''}}"`,
      `"${{t.sector || ''}}"`,
      `"${{t.corridor || ''}}"`,
      `"${{t.job_title || ''}}"`,
      `"${{t.hr_name || ''}}"`,
      `"${{t.hr_email || t.careers_email || ''}}"`,
      `"${{t.phone || ''}}"`,
      `"${{t.linkedin_url || ''}}"`
    ]);
  }});
  const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "bangalore_filtered_companies.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}}

function exportJobsJSON() {{
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(scoredJobs, null, 2));
  const link = document.createElement("a");
  link.setAttribute("href", dataStr);
  link.setAttribute("download", "bangalore_scored_jobs.json");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}}

// Initialization
document.addEventListener('DOMContentLoaded', () => {{
  renderCompanies();
  filterScoredJobs();
  filterDbJobs();
  renderTechParks();
  updatePrompt();
}});
</script>
</body>
</html>
"""
    print(f"Writing HTML output to {OUTPUT_HTML}...")
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Done! File size: {os.path.getsize(OUTPUT_HTML):,} bytes.")

def main():
    data = load_data()
    generate_html(data)

if __name__ == "__main__":
    main()
