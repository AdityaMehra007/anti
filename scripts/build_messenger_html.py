import json
import csv

with open(r'e:\anti\linkedin_export\connection_outreach_data.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# Priority Embed: All Tier 1 (1,351), All Senior Leadership (413), Top 400 HR, Top 400 Alumni -> ~2,560 priority active connections embedded directly
embedded_tier1 = [r for r in all_data if r['category'] == 'Tier 1: Active Job ID Mapped']
embedded_lead = [r for r in all_data if r['category'] == 'Tier 2: Senior Leadership & Executives']
embedded_hr = [r for r in all_data if r['category'] == 'Tier 2: HR & Talent Acquisition'][:400]
embedded_alum = [r for r in all_data if r['category'] == 'Tier 3: University & Alumni Network'][:400]

embedded = embedded_tier1 + embedded_lead + embedded_hr + embedded_alum
embedded_json = json.dumps(embedded, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relationship-First LinkedIn Outreach Dispatcher — 9,223 Messages</title>
<style>
  :root {{
    --bg: #0b0f19;
    --card: #151e32;
    --card-hover: #1c2944;
    --border: #23324d;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.25);
    --green: #22c55e;
    --purple: #c084fc;
    --amber: #fbbf24;
    --badge-bg: rgba(56, 189, 248, 0.12);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding: 24px; min-height: 100vh; }}
  .container {{ max-width: 1440px; margin: 0 auto; }}

  /* Top Navigation Bar */
  .top-nav {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }}
  .nav-link {{ background: var(--card); border: 1px solid var(--border); color: #cbd5e1; padding: 8px 14px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; transition: all 0.2s; display: inline-flex; align-items: center; gap: 6px; }}
  .nav-link:hover, .nav-link.active {{ background: #1e293b; color: var(--accent); border-color: var(--accent); }}

  header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
  h1 {{ font-size: 24px; font-weight: 700; color: #fff; }}
  .subtitle {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
  
  .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .metric-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
  .metric-value {{ font-size: 26px; font-weight: 700; color: var(--accent); }}
  .metric-label {{ font-size: 12px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}

  .toolbar {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }}
  .search-box {{ flex: 1; min-width: 280px; }}
  input[type="text"], select {{ width: 100%; padding: 10px 14px; background: var(--card); border: 1px solid var(--border); border-radius: 6px; color: #fff; font-size: 14px; outline: none; }}
  input[type="text"]:focus, select:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }}
  .filter-select {{ width: 260px; }}
  .btn {{ padding: 10px 16px; border-radius: 6px; border: 1px solid var(--border); background: var(--card); color: #fff; font-size: 14px; cursor: pointer; transition: all 0.2s; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; }}
  .btn:hover {{ background: #1c2944; border-color: var(--accent); }}
  
  .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(430px, 1fr)); gap: 20px; }}
  .contact-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }}
  .contact-card:hover {{ border-color: #3b82f6; }}
  .card-top {{ margin-bottom: 12px; }}
  .contact-name {{ font-size: 18px; font-weight: 700; color: #fff; display: flex; justify-content: space-between; align-items: center; }}
  .contact-pos {{ color: var(--accent); font-size: 13px; font-weight: 500; margin-top: 2px; }}
  .tag-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }}
  .company-pill {{ background: rgba(56, 189, 248, 0.12); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.25); padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
  .tier-pill {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
  .job-ref {{ font-size: 12px; color: #4ade80; background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.25); padding: 4px 8px; border-radius: 4px; margin-top: 8px; font-family: monospace; }}

  .msg-container {{ background: #0c1322; border: 1px solid #1a2740; border-radius: 6px; padding: 12px; font-size: 13px; line-height: 1.55; color: #cbd5e1; white-space: pre-wrap; margin: 12px 0; max-height: 220px; overflow-y: auto; }}
  
  .card-actions {{ display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }}
  .copy-btn {{ background: #0284c7; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }}
  .copy-btn:hover {{ background: #0369a1; }}
  .copy-btn.copied {{ background: #16a34a; }}
  .profile-link {{ color: var(--accent); text-decoration: none; font-size: 13px; font-weight: 500; }}
  .profile-link:hover {{ text-decoration: underline; }}

  .pagination {{ display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding: 12px 0; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 14px; }}
  .page-nav {{ display: flex; gap: 8px; align-items: center; }}
</style>
</head>
<body>
<div class="container">
  <div class="top-nav">
    <a href="fresher_referral_companion.html" class="nav-link">🌟 Fresher Referral Companion</a>
    <a href="connection_messenger_center.html" class="nav-link active">💬 LinkedIn Messenger Center</a>
    <a href="connections_directory.html" class="nav-link">📇 All 9,223 Connections Directory</a>
    <a href="../resumes_pdf/" class="nav-link" target="_blank">📂 Tailored PDF Resumes Folder</a>
    <a href="connections_company_summary.csv" class="nav-link" download>📊 Company Network Summary</a>
  </div>

  <header>
    <div>
      <h1>Hyper-Personalized LinkedIn Outreach Command Center</h1>
      <div class="subtitle">Aditya Mehra | Dayananda Sagar University | AERO INDIA 2025 Operations Lead</div>
    </div>
    <div style="display: flex; gap: 10px;">
      <a href="connection_personalized_messages.csv" download class="btn">📥 Export All 9,223 Messages (CSV)</a>
    </div>
  </header>

  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-value">9,223</div>
      <div class="metric-label">Total Bespoke Messages</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">1,351</div>
      <div class="metric-label">Direct Job-ID Mapped Contacts</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">1,314</div>
      <div class="metric-label">Talent Acquisition & HR Leads</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">413</div>
      <div class="metric-label">Senior Executives & Directors</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">1,206</div>
      <div class="metric-label">University Alumni & Campus Leads</div>
    </div>
  </div>

  <div class="toolbar">
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Search by name, company, position, or job ID..." oninput="onFilter()">
    </div>
    <select id="tierFilter" class="filter-select" onchange="onFilter()">
      <option value="">All Embedded Categories ({len(embedded)})</option>
      <option value="Tier 1">Tier 1: Active Job ID Mapped ({len(embedded_tier1)})</option>
      <option value="Senior Leadership">Tier 2: Senior Leadership ({len(embedded_lead)})</option>
      <option value="HR & Talent">Tier 2: HR & Talent Acquisition ({len(embedded_hr)})</option>
      <option value="University & Alumni">Tier 3: University Alumni Network ({len(embedded_alum)})</option>
    </select>
    <select id="companyFilter" class="filter-select" onchange="onFilter()">
      <option value="">All Target Companies</option>
      <option value="EY">EY (195+ connections)</option>
      <option value="Deloitte">Deloitte (99 connections)</option>
      <option value="Accenture">Accenture (89 connections)</option>
      <option value="IBM">IBM (78 connections)</option>
      <option value="Goldman Sachs">Goldman Sachs (77 connections)</option>
      <option value="Tata Consultancy">TCS (72 connections)</option>
      <option value="Capgemini">Capgemini (41 connections)</option>
      <option value="Amazon">Amazon / AWS (40 connections)</option>
      <option value="JPMorganChase">JPMorganChase (40 connections)</option>
      <option value="KPMG">KPMG India (42 connections)</option>
      <option value="PwC">PwC India (39 connections)</option>
      <option value="Rippling">Rippling (24 connections)</option>
      <option value="ICICI">ICICI Bank (23 connections)</option>
      <option value="Cognizant">Cognizant (21 connections)</option>
      <option value="Infosys">Infosys (20 connections)</option>
      <option value="PhysicsWallah">PhysicsWallah (20 connections)</option>
      <option value="Target">Target in India (17 connections)</option>
      <option value="Ditto">Ditto Insurance (17 connections)</option>
      <option value="Commonwealth">Commonwealth Bank (16 connections)</option>
      <option value="Wipro">Wipro (16 connections)</option>
      <option value="ITC">ITC Limited (16 connections)</option>
      <option value="Deutsche Bank">Deutsche Bank (15 connections)</option>
      <option value="Google">Google (15 connections)</option>
      <option value="Microsoft">Microsoft (12 connections)</option>
      <option value="Razorpay">Razorpay (3 connections)</option>
      <option value="Cisco">Cisco (3 connections)</option>
      <option value="Swiggy">Swiggy (5 connections)</option>
      <option value="Zepto">Zepto (5 connections)</option>
    </select>
  </div>

  <div class="card-grid" id="cardsGrid"></div>

  <div class="pagination">
    <div id="pageInfo">Showing 0-0 of 0</div>
    <div class="page-nav">
      <button class="btn" id="prevBtn" onclick="changePage(-1)">Previous</button>
      <span id="pageNum" style="font-weight:600; color:var(--accent);">1</span>
      <button class="btn" id="nextBtn" onclick="changePage(1)">Next</button>
    </div>
  </div>
</div>

<script>
const DATA = {embedded_json};
let filteredData = [...DATA];
let currentPage = 1;
const PAGE_SIZE = 24;

function onFilter() {{
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  const tier = document.getElementById('tierFilter').value;
  const company = document.getElementById('companyFilter').value.toLowerCase();

  filteredData = DATA.filter(c => {{
    const matchesQuery = !query || 
      c.name.toLowerCase().includes(query) ||
      c.company.toLowerCase().includes(query) ||
      c.position.toLowerCase().includes(query) ||
      c.job_info.toLowerCase().includes(query);

    const matchesTier = !tier || c.category.includes(tier);
    const matchesCompany = !company || c.company.toLowerCase().includes(company);

    return matchesQuery && matchesTier && matchesCompany;
  }});

  currentPage = 1;
  renderCards();
}}

function renderCards() {{
  const grid = document.getElementById('cardsGrid');
  const start = (currentPage - 1) * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, filteredData.length);
  const pageItems = filteredData.slice(start, end);

  document.getElementById('pageInfo').innerText = `Showing ${{filteredData.length ? start + 1 : 0}}-${{end}} of ${{filteredData.length}} Priority Contacts`;
  document.getElementById('pageNum').innerText = `Page ${{currentPage}} of ${{Math.ceil(filteredData.length / PAGE_SIZE) || 1}}`;
  document.getElementById('prevBtn').disabled = currentPage <= 1;
  document.getElementById('nextBtn').disabled = end >= filteredData.length;

  grid.innerHTML = pageItems.map((c, idx) => {{
    const safeMsg = escapeHtml(c.message);
    const id = `msg-${{start + idx}}`;
    return `
      <div class="contact-card">
        <div class="card-top">
          <div class="contact-name">
            <span>${{escapeHtml(c.name)}}</span>
            ${{c.url ? `<a href="${{c.url}}" target="_blank" class="profile-link">Profile &nearr;</a>` : ''}}
          </div>
          <div class="contact-pos">${{escapeHtml(c.position)}}</div>
          <div class="tag-row">
            <span class="company-pill">${{escapeHtml(c.company)}}</span>
            <span class="tier-pill">${{escapeHtml(c.category)}}</span>
          </div>
          ${{c.job_info ? `<div class="job-ref">🎯 ${{escapeHtml(c.job_info)}}</div>` : ''}}
        </div>
        <div class="msg-container" id="${{id}}">${{safeMsg}}</div>
        <div class="card-actions">
          <span style="font-size:11px; color:var(--text-muted);">${{c.date ? 'Connected: ' + c.date : ''}}</span>
          <button class="copy-btn" onclick="copyCard('${{id}}', this)">Copy Message</button>
        </div>
      </div>
    `;
  }}).join('');
}}

function escapeHtml(str) {{
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({{
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }}[tag] || tag));
}}

function copyCard(id, btn) {{
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text).then(() => {{
    const orig = btn.innerText;
    btn.innerText = '✓ Copied!';
    btn.classList.add('copied');
    setTimeout(() => {{
      btn.innerText = orig;
      btn.classList.remove('copied');
    }}, 2000);
  }});
}}

function changePage(dir) {{
  currentPage += dir;
  renderCards();
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// Initial load
renderCards();
</script>
</body>
</html>
"""

out_html = r'e:\anti\linkedin_export\connection_messenger_center.html'
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated {out_html} successfully with {len(embedded)} priority contacts embedded.")
