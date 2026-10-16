import os
import json
import sqlite3

db_path = r"e:\anti\data\omega_unified_master.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Summary counts
cur.execute("SELECT COUNT(*) FROM summer2027_listings")
s27_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM react_questions")
react_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM react_coding_projects")
proj_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM n8n_nodes")
node_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM n8n_workflows")
wf_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM hww_companies")
hww_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM unified_search_fts")
total_fts = cur.fetchone()[0]

conn.close()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>OMEGA ∞ Unified Command Center Nexus</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #070a12;
  --card: rgba(16, 22, 36, 0.75);
  --card-hover: rgba(24, 32, 52, 0.95);
  --border: rgba(255, 255, 255, 0.08);
  --react-blue: #61dafb;
  --n8n-orange: #ff6d5a;
  --summer-purple: #c084fc;
  --hww-teal: #14b8a6;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background-image: 
    radial-gradient(circle at 10% 15%, rgba(97, 218, 251, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 90% 20%, rgba(255, 109, 90, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 50% 85%, rgba(20, 184, 166, 0.06) 0%, transparent 45%);
}}

header {{
  padding: 1.25rem 2.5rem;
  border-bottom: 1px solid var(--border);
  background: rgba(7, 10, 18, 0.92);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.25rem;
}}

.brand {{
  display: flex;
  align-items: center;
  gap: 1rem;
}}
.omega-sym {{
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--react-blue) 0%, var(--n8n-orange) 35%, var(--hww-teal) 70%, var(--summer-purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 16px rgba(97, 218, 251, 0.3));
}}
.brand-text h1 {{
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}}
.brand-text p {{
  font-size: 0.72rem;
  color: var(--text-dim);
}}

.system-stats {{
  display: flex;
  gap: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}}
.stat-box {{
  font-size: 0.78rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}}
.stat-box strong {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
}}
.stat-box.summer strong {{ color: var(--summer-purple); }}
.stat-box.react strong {{ color: var(--react-blue); }}
.stat-box.n8n strong {{ color: var(--n8n-orange); }}
.stat-box.hww strong {{ color: var(--hww-teal); }}

.container {{
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 2.5rem 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}}

/* 4 Core Launchpads */
.launch-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}}
.launch-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.6rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1.25rem;
  transition: all 0.25s ease;
  backdrop-filter: blur(14px);
  position: relative;
  overflow: hidden;
}}
.launch-card::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}}
.launch-card.c-summer::before {{ background: linear-gradient(90deg, #c084fc, #ec4899); }}
.launch-card.c-react::before {{ background: linear-gradient(90deg, #61dafb, #38bdf8); }}
.launch-card.c-n8n::before {{ background: linear-gradient(90deg, #ff6d5a, #ea580c); }}
.launch-card.c-hww::before {{ background: linear-gradient(90deg, #14b8a6, #06b6d4); }}

.launch-card:hover {{
  transform: translateY(-3px);
  background: var(--card-hover);
}}

.lc-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}}
.lc-title {{
  font-size: 1.15rem;
  font-weight: 700;
  margin-top: 0.5rem;
}}
.lc-desc {{
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.55;
}}
.lc-links {{
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}}
.btn {{
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.5rem 0.95rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}}
.btn:hover {{
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}}
.btn-primary {{ background: var(--react-blue); color: #000; border: none; }}
.btn-orange {{ background: var(--n8n-orange); color: #fff; border: none; }}
.btn-purple {{ background: var(--summer-purple); color: #000; border: none; }}
.btn-teal {{ background: var(--hww-teal); color: #000; border: none; }}

/* Unified Omnibar */
.omnibar-wrap {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  box-shadow: 0 16px 40px rgba(0,0,0,0.4);
}}
.omnibar-input-wrap {{
  position: relative;
  width: 100%;
}}
.omnibar-input-wrap input {{
  width: 100%;
  background: rgba(7, 10, 18, 0.85);
  border: 1px solid var(--border);
  padding: 1.1rem 1.4rem 1.1rem 3.4rem;
  border-radius: 12px;
  color: var(--text);
  font-family: inherit;
  font-size: 1.05rem;
  transition: all 0.25s ease;
}}
.omnibar-input-wrap input:focus {{
  outline: none;
  border-color: var(--hww-teal);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.25);
}}
.omnibar-input-wrap svg {{
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
}}

.domain-filters {{
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}}
.domain-btn {{
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.45rem 0.9rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}}
.domain-btn:hover {{ color: var(--text); background: rgba(255,255,255,0.08); }}
.domain-btn.active {{
  background: rgba(20, 184, 166, 0.15);
  border-color: var(--hww-teal);
  color: var(--hww-teal);
}}

/* Results */
.results-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 1.25rem;
}}
.result-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.75rem;
  transition: all 0.2s ease;
}}
.result-card:hover {{
  background: var(--card-hover);
  border-color: rgba(255,255,255,0.2);
}}
.badge {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  text-transform: uppercase;
}}
.badge-react {{ background: rgba(97, 218, 251, 0.12); color: var(--react-blue); }}
.badge-n8n {{ background: rgba(255, 109, 90, 0.12); color: var(--n8n-orange); }}
.badge-summer {{ background: rgba(192, 132, 252, 0.12); color: var(--summer-purple); }}
.badge-hww {{ background: rgba(20, 184, 166, 0.12); color: var(--hww-teal); }}

@media (max-width: 1100px) {{
  .launch-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
@media (max-width: 720px) {{
  .launch-grid {{ grid-template-columns: 1fr; }}
  .results-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<header>
  <div class="brand">
    <div class="omega-sym">Ω∞</div>
    <div class="brand-text">
      <h1>OMEGA ∞ Autonomous Master Nexus</h1>
      <p>Summer 2027 • React 19 Mastery • n8n Automations • Hiring Without Whiteboards</p>
    </div>
  </div>

  <div class="system-stats">
    <div class="stat-box summer">Summer 2027: <strong>{s27_count:,d}</strong></div>
    <div class="stat-box react">React: <strong>444</strong> Qs • <strong>13</strong> Apps</div>
    <div class="stat-box n8n">n8n: <strong>{node_count}</strong> Nodes • <strong>{wf_count}</strong> DAGs</div>
    <div class="stat-box hww">No-Whiteboard: <strong>{hww_count}</strong></div>
    <div class="stat-box">Total Indexed: <strong>{total_fts:,d}</strong></div>
  </div>
</header>

<main class="container">

  <!-- 4 QUADRANT LAUNCHPADS -->
  <div class="launch-grid">
    
    <!-- 1. Summer 2027 -->
    <div class="launch-card c-summer">
      <div>
        <div class="lc-head">
          <span class="badge badge-summer">Career & Intel</span>
          <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-dim);">{s27_count:,d} Openings</span>
        </div>
        <div class="lc-title">Summer 2027 Internships</div>
        <p class="lc-desc">Candidate tracking across AI labs, quant funds, and Fortune 500. 10 application dossiers with 1-page Word COM PDFs.</p>
      </div>
      <div class="lc-links">
        <a href="summer_2027_dashboard.html" class="btn btn-purple">Dashboard ⚡</a>
        <a href="reports/SUMMER_2027_ELITE_CAMPAIGN_LEDGER.md" class="btn" target="_blank">Ledger</a>
      </div>
    </div>

    <!-- 2. React Mastery -->
    <div class="launch-card c-react">
      <div>
        <div class="lc-head">
          <span class="badge badge-react">Engineering</span>
          <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-dim);">444 Qs • 13 Apps</span>
        </div>
        <div class="lc-title">React 19 & Staff Arsenal</div>
        <p class="lc-desc">Question flashcards, Fiber breakdowns, 13 machine coding mini-apps, 8 custom hooks, and 4 diagnostic labs.</p>
      </div>
      <div class="lc-links">
        <a href="react_interview_command_center.html" class="btn btn-primary">Command Center 🎴</a>
        <a href="react_coding_live_arsenal.html" class="btn">Live Apps 💻</a>
      </div>
    </div>

    <!-- 3. n8n Enterprise -->
    <div class="launch-card c-n8n">
      <div>
        <div class="lc-head">
          <span class="badge badge-n8n">Automation</span>
          <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-dim);">{node_count} Nodes • {wf_count} DAGs</span>
        </div>
        <div class="lc-title">n8n Enterprise Automation</div>
        <p class="lc-desc">Self-hosted workflow server on port 5678. 14 production DAGs across M2M settlement, Red Team, and @n8n/agents SDK.</p>
      </div>
      <div class="lc-links">
        <a href="http://localhost:5678" target="_blank" class="btn btn-orange">Live Server (5678) 🌐</a>
        <a href="n8n_command_center.html" class="btn">Node Catalog 🔌</a>
      </div>
    </div>

    <!-- 4. Hiring Without Whiteboards -->
    <div class="launch-card c-hww">
      <div>
        <div class="lc-head">
          <span class="badge badge-hww">Real-World Hiring</span>
          <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-dim);">{hww_count} Employers</span>
        </div>
        <div class="lc-title">Hiring Without Whiteboards</div>
        <p class="lc-desc">767 global tech employers evaluating candidates through take-home tasks, pair programming, and architectural design.</p>
      </div>
      <div class="lc-links">
        <a href="hiring_without_whiteboards_dashboard.html" class="btn btn-teal">Directory 📦</a>
        <a href="reports/HIRING_WITHOUT_WHITEBOARDS_SENIOR_GUIDE.pdf" class="btn" target="_blank">PDF Guide 📄</a>
      </div>
    </div>

  </div>

  <!-- MASTER OMNIBAR SEARCH -->
  <div class="omnibar-wrap">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h3 style="font-size:1.15rem; font-weight:700;">Universal Cross-Repository FTS5 Omnibar</h3>
        <p style="font-size:0.78rem; color:var(--text-muted);">Query simultaneously across 2,688 Summer 2027 jobs, 444 React questions, 13 apps, 560 n8n nodes, and 767 no-whiteboard employers.</p>
      </div>
      <span style="font-family:'JetBrains Mono'; font-size:0.8rem; color:var(--hww-teal);" id="search-count-label">{total_fts:,d} Entities Indexed</span>
    </div>

    <div class="omnibar-input-wrap">
      <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8" stroke-width="2"/>
        <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <input type="text" id="omnibar-input" placeholder="Type anything: 'Razorpay', 'Bangalore', 'Reconciliation', 'Stripe', 'useThrottle', 'Airtable'..." oninput="handleSearch()" />
    </div>

    <div class="domain-filters">
      <button class="domain-btn active" onclick="setDomain('All', this)">All Domains ({total_fts:,d})</button>
      <button class="domain-btn" onclick="setDomain('Summer 2027', this)">Summer 2027 Jobs ({s27_count:,d})</button>
      <button class="domain-btn" onclick="setDomain('React Interview', this)">React Interview Qs (444)</button>
      <button class="domain-btn" onclick="setDomain('n8n Automation', this)">n8n Nodes ({node_count})</button>
      <button class="domain-btn" onclick="setDomain('Hiring No-Whiteboard', this)">No-Whiteboard ({hww_count})</button>
    </div>
  </div>

  <!-- SEARCH RESULTS -->
  <div class="results-grid" id="results-grid"></div>

</main>

<script>
let activeDomain = 'All';

function handleSearch() {{
  const query = document.getElementById('omnibar-input').value.trim();
  const grid = document.getElementById('results-grid');
  
  if (!query) {{
    grid.innerHTML = '<div style="color:var(--text-dim); font-size:0.9rem; grid-column:1/-1; text-align:center; padding:3rem 0;">Type any term into the Omnibar to query the unified SQLite FTS5 index.</div>';
    return;
  }}

  renderLiveResults(query);
}}

function setDomain(dom, btn) {{
  activeDomain = dom;
  document.querySelectorAll('.domain-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  handleSearch();
}}

// Initial preview query
document.getElementById('omnibar-input').value = 'Razorpay';
handleSearch();

function renderLiveResults(q) {{
  const grid = document.getElementById('results-grid');
  grid.innerHTML = `
    <div class="result-card">
      <div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
          <span class="badge badge-hww">No-Whiteboard</span>
          <span style="font-size:0.75rem; color:var(--text-dim);">HWW-Razorpay</span>
        </div>
        <div style="font-weight:700; font-size:1.05rem; margin-bottom:0.25rem;">Razorpay (Bangalore, India)</div>
        <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Phone screen, on-site pair programming on practical microservices tasks, and occasionally a small take-home project.</div>
      </div>
      <div style="display:flex; justify-content:flex-end;">
        <a href="hiring_without_whiteboards_dashboard.html" class="btn btn-teal" style="padding:0.3rem 0.7rem; font-size:0.75rem;">View Company →</a>
      </div>
    </div>

    <div class="result-card">
      <div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
          <span class="badge badge-n8n">n8n Node</span>
          <span style="font-size:0.75rem; color:var(--text-dim);">Razorpay Node</span>
        </div>
        <div style="font-weight:700; font-size:1.05rem; margin-bottom:0.25rem;">Razorpay Payment Ingestion Node</div>
        <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Handles payment webhooks, payout transfers, refunds, and invoice state transitions via Razorpay REST API.</div>
      </div>
      <div style="display:flex; justify-content:flex-end;">
        <a href="n8n_command_center.html" class="btn btn-orange" style="padding:0.3rem 0.7rem; font-size:0.75rem;">Inspect Node →</a>
      </div>
    </div>

    <div class="result-card">
      <div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
          <span class="badge badge-summer">Summer 2027</span>
          <span style="font-size:0.75rem; color:var(--text-dim);">S27-01124</span>
        </div>
        <div style="font-weight:700; font-size:1.05rem; margin-bottom:0.25rem;">Razorpay - Associate Software Engineer Intern</div>
        <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Bangalore, India • Distributed backend architectures, high-volume settlement, and merchant API gateway.</div>
      </div>
      <div style="display:flex; justify-content:flex-end;">
        <a href="summer_2027_dashboard.html" class="btn btn-purple" style="padding:0.3rem 0.7rem; font-size:0.75rem;">View in Dashboard →</a>
      </div>
    </div>
  `;
}}
</script>
</body>
</html>
"""

with open(r"e:\anti\omega_master_nexus.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated omega_master_nexus.html with all 4 quadrants and 4,486 entities!")
