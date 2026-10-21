"""
Generate All Companies Interactive Job Search Portal & Explorer
File: e:\\anti\\linkedin_export\\job_search_portal.html
"""

import json
import os
import re

html_source = r'e:\anti\linkedin_export\all_companies_best_messages.html'
with open(html_source, 'r', encoding='utf-8') as f:
    text = f.read()

comps = json.loads(re.search(r'const COMPANIES = (\[.*?\]);', text, re.DOTALL).group(1))

jobs_list = []
for c in comps:
    for j in c.get('all_jobs', []):
        jobs_list.append({
            'company': c['company'],
            'sector': c['sector'],
            'group': c.get('group', c['sector']),
            'connections_count': c['connections_count'],
            'champion_name': c['champion_name'],
            'champion_position': c['champion_position'],
            'champion_url': c['champion_url'],
            'role': j['role'],
            'job_id': j['id'],
            'job_url': j['url'],
            'job_type': j['type'],
            'message_referral': c['message_referral'],
            'message_exec': c['message_exec'],
            'message_connect': c['message_connect']
        })

jobs_json = json.dumps(jobs_list, ensure_ascii=False)
output_html = r'e:\anti\linkedin_export\job_search_portal.html'

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra | All Companies Enterprise Job Search Portal (141 Requisitions)</title>
<style>
  :root {{
    --bg: #070b13;
    --card: #0f172a;
    --card-hover: #17243d;
    --border: #1e293b;
    --border-highlight: #38bdf8;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --green: #10b981;
    --amber: #f59e0b;
    --purple: #a855f7;
    --blue-linkedin: #0a66c2;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding: 20px; min-height: 100vh; }}

  /* Top Navigation */
  .top-nav {{
    display: flex;
    gap: 12px;
    background: #0f172a;
    padding: 12px 20px;
    border-radius: 12px;
    border: 1px solid var(--border);
    margin-bottom: 24px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .top-nav .nav-brand {{
    font-weight: 800;
    font-size: 16px;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-right: 12px;
  }}
  .top-nav a {{
    color: var(--text-muted);
    text-decoration: none;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
    transition: all 0.2s;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
  }}
  .top-nav a:hover, .top-nav a.active {{
    color: #fff;
    background: rgba(56, 189, 248, 0.15);
    border-color: var(--accent);
  }}

  /* Header */
  .header-card {{
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.7));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
  }}
  .header-card h1 {{
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .header-card p {{
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 16px;
  }}
  .metric-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-top: 16px;
  }}
  .metric-box {{
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
  }}
  .metric-box .label {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px; }}
  .metric-box .val {{ font-size: 20px; font-weight: 800; color: var(--accent); margin-top: 4px; }}

  /* Search & Filter Bar */
  .search-section {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 24px;
  }}
  .search-inputs-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }}
  .search-input {{
    flex: 2;
    min-width: 280px;
    background: #020617;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s;
  }}
  .search-input:focus {{ border-color: var(--accent); }}
  .filter-select {{
    flex: 1;
    min-width: 200px;
    background: #020617;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 14px;
    outline: none;
    cursor: pointer;
  }}

  /* Filter Pills */
  .pills-bar {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
  }}
  .pill {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-muted);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .pill:hover {{ color: #fff; background: rgba(255,255,255,0.12); }}
  .pill.active {{
    background: var(--accent);
    color: #070b13;
    border-color: var(--accent);
    font-weight: 700;
  }}

  /* Results Info */
  .results-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 600;
  }}

  /* Jobs Grid */
  .jobs-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 18px;
  }}
  .job-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease;
  }}
  .job-card:hover {{
    border-color: var(--border-highlight);
    background: var(--card-hover);
    transform: translateY(-2px);
  }}

  .job-card-top {{
    margin-bottom: 14px;
  }}
  .company-badge-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
  }}
  .company-name {{
    font-size: 18px;
    font-weight: 800;
    color: #fff;
  }}
  .badge-tag {{
    background: rgba(56, 189, 248, 0.15);
    color: var(--accent);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
  }}
  .badge-primary {{
    background: rgba(16, 185, 129, 0.15);
    color: var(--green);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
  }}
  .badge-alt {{
    background: rgba(168, 85, 247, 0.15);
    color: var(--purple);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
  }}

  .job-role {{
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.4;
    margin-bottom: 8px;
  }}
  .job-req-id {{
    font-family: monospace;
    font-size: 12px;
    color: var(--accent);
    background: rgba(56, 189, 248, 0.1);
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 12px;
  }}

  /* Champion Callout */
  .champ-callout {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 16px;
    font-size: 12px;
  }}
  .champ-callout .name {{
    color: #fff;
    font-weight: 700;
  }}
  .champ-callout .title {{
    color: var(--text-muted);
    margin-top: 2px;
  }}

  /* Card Action Buttons */
  .card-actions {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: auto;
  }}
  .btn {{
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
    text-align: center;
    cursor: pointer;
    border: none;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
  }}
  .btn-portal {{
    background: var(--accent);
    color: #070b13;
  }}
  .btn-portal:hover {{ background: #7dd3fc; }}
  .btn-champion {{
    background: var(--blue-linkedin);
    color: #fff;
  }}
  .btn-champion:hover {{ background: #004182; }}
  .btn-copy-msg {{
    grid-column: span 2;
    background: rgba(255,255,255,0.08);
    color: #e2e8f0;
    border: 1px solid var(--border);
  }}
  .btn-copy-msg:hover {{ background: rgba(255,255,255,0.15); color: #fff; }}

  /* Toast */
  #toast {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--accent);
    color: #070b13;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 14px;
    display: none;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    z-index: 9999;
  }}
  #toast.show {{ display: block; animation: fadeIn 0.3s ease; }}
  @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
</style>
</head>
<body>

  <!-- Top Navigation -->
  <div class="top-nav">
    <div class="nav-brand">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      ADITYA MEHRA • OUTREACH ENGINE
    </div>
    <a href="job_search_portal.html" class="active">🔍 Job Search Portal ({len(jobs_list)} Openings)</a>
    <a href="all_companies_best_messages.html">★ 112 Companies Best Messages</a>
    <a href="connection_messenger_center.html">🚀 Master Messenger Center (9,223 Leads)</a>
    <a href="fresher_referral_companion.html">🎯 Fresher Referral Companion</a>
    <a href="connection_personalized_messages.csv" download>📥 Download Master CSV</a>
  </div>

  <!-- Header -->
  <div class="header-card">
    <h1>All Companies Enterprise Job Search Portal & Requisition Directory</h1>
    <p>
      Search, filter, and discover all <b>{len(jobs_list)} verified fresher & entry-level openings</b> across all <b>{len(comps)} target employers</b>. Each job card is mapped with its verified Requisition ID, official application portal link, #1 internal referral champion, and 1-click tailored referral message.
    </p>
    <div class="metric-row">
      <div class="metric-box">
        <div class="label">Total Openings Cataloged</div>
        <div class="val">{len(jobs_list)}</div>
      </div>
      <div class="metric-box">
        <div class="label">Target Companies</div>
        <div class="val">{len(comps)}</div>
      </div>
      <div class="metric-box">
        <div class="label">Mutual 1st-Degree Network</div>
        <div class="val">{sum(c['connections_count'] for c in comps):,} contacts</div>
      </div>
      <div class="metric-box">
        <div class="label">Seniority Tier</div>
        <div class="val" style="font-size: 16px; color: var(--green);">100% Fresher / Campus 2026</div>
      </div>
    </div>
  </div>

  <!-- Search Section -->
  <div class="search-section">
    <div class="search-inputs-row">
      <input type="text" id="searchInput" class="search-input" placeholder="Search by Job Title, Company Name, Requisition ID, or Keywords (e.g. Operations, Supply Chain, Banking, Bangalore)...">
      <select id="sectorSelect" class="filter-select">
        <option value="all">All Sectors ({len(jobs_list)} Jobs)</option>
      </select>
    </div>
    <div class="pills-bar">
      <span style="font-size: 12px; color: var(--text-muted); font-weight: 700; margin-right: 4px;">Quick Filters:</span>
      <button class="pill active" onclick="filterByQuick('all', this)">All ({len(jobs_list)})</button>
      <button class="pill" onclick="filterByQuick('operations', this)">Operations ({sum(1 for j in jobs_list if 'operat' in j['role'].lower())})</button>
      <button class="pill" onclick="filterByQuick('supply chain', this)">Supply Chain ({sum(1 for j in jobs_list if 'supply' in j['role'].lower() or 'scm' in j['role'].lower())})</button>
      <button class="pill" onclick="filterByQuick('banking', this)">Banking & Finance ({sum(1 for j in jobs_list if any(k in (j['sector']+j['role']).lower() for k in ['bank', 'finance', 'invest']))})</button>
      <button class="pill" onclick="filterByQuick('consulting', this)">Big 4 & Consulting ({sum(1 for j in jobs_list if 'consult' in (j['sector']+j['role']).lower())})</button>
      <button class="pill" onclick="filterByQuick('tech', this)">Big Tech & Cloud ({sum(1 for j in jobs_list if any(k in (j['sector']+j['role']).lower() for k in ['tech', 'cloud', 'software']))})</button>
      <button class="pill" onclick="filterByQuick('trainee', this)">Graduate Trainee ({sum(1 for j in jobs_list if 'trainee' in j['role'].lower())})</button>
    </div>
  </div>

  <!-- Results Bar -->
  <div class="results-bar">
    <div id="resultsCount">Showing {len(jobs_list)} open requisitions</div>
    <div style="font-size: 12px; color: var(--accent);">Target Batch: Class of 2026 • Verified Requisitions</div>
  </div>

  <!-- Jobs Grid -->
  <div class="jobs-grid" id="jobsGrid"></div>

  <!-- Toast -->
  <div id="toast">Copied to clipboard!</div>

  <script>
    const JOBS = {jobs_json};

    // Populate sector select
    const sectors = Array.from(new Set(JOBS.map(j => j.group || j.sector))).sort();
    const sel = document.getElementById('sectorSelect');
    sectors.forEach(s => {{
      const opt = document.createElement('option');
      opt.value = s;
      const cnt = JOBS.filter(j => (j.group === s || j.sector === s)).length;
      opt.textContent = `${{s}} (${{cnt}} jobs)`;
      sel.appendChild(opt);
    }});

    let currentList = JOBS;
    let quickFilter = 'all';

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => {{ t.classList.remove('show'); }}, 2500);
    }}

    function copyJobReferral(idx) {{
      const j = currentList[idx];
      const msg = j.message_referral;
      navigator.clipboard.writeText(msg).then(() => {{
        showToast(`Copied referral ask for ${{j.role}} at ${{j.company}}!`);
      }}).catch(() => {{
        const ta = document.createElement("textarea");
        ta.value = msg;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        showToast(`Copied referral ask for ${{j.role}} at ${{j.company}}!`);
      }});
    }}

    function filterByQuick(type, el) {{
      quickFilter = type;
      document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      filterJobs();
    }}

    function filterJobs() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const s = document.getElementById('sectorSelect').value;

      currentList = JOBS.filter(j => {{
        if (s !== 'all' && (j.group !== s && j.sector !== s)) return false;

        if (quickFilter !== 'all') {{
          const fullText = (j.role + ' ' + j.sector + ' ' + j.company).toLowerCase();
          if (quickFilter === 'operations' && !j.role.toLowerCase().includes('operat')) return false;
          if (quickFilter === 'supply chain' && !fullText.includes('supply') && !fullText.includes('scm')) return false;
          if (quickFilter === 'banking' && !fullText.includes('bank') && !fullText.includes('finance') && !fullText.includes('invest')) return false;
          if (quickFilter === 'consulting' && !fullText.includes('consult')) return false;
          if (quickFilter === 'tech' && !fullText.includes('tech') && !fullText.includes('cloud') && !fullText.includes('software')) return false;
          if (quickFilter === 'trainee' && !j.role.toLowerCase().includes('trainee')) return false;
        }}

        if (q) {{
          return j.company.toLowerCase().includes(q) ||
                 j.role.toLowerCase().includes(q) ||
                 j.job_id.toLowerCase().includes(q) ||
                 j.sector.toLowerCase().includes(q) ||
                 j.champion_name.toLowerCase().includes(q);
        }}
        return true;
      }});

      renderGrid(currentList);
    }}

    function renderGrid(list) {{
      const grid = document.getElementById('jobsGrid');
      document.getElementById('resultsCount').textContent = `Showing ${{list.length}} open requisition${{list.length === 1 ? '' : 's'}}`;

      let html = '';
      list.forEach((j, idx) => {{
        html += `
          <div class="job-card">
            <div class="job-card-top">
              <div class="company-badge-row">
                <div class="company-name">${{escapeHtml(j.company)}}</div>
                <span class="${{j.job_type === 'Primary' ? 'badge-primary' : 'badge-alt'}}">${{j.job_type}}</span>
              </div>
              <div style="margin-bottom: 8px;">
                <span class="badge-tag">${{escapeHtml(j.sector)}}</span>
                <span style="font-size: 11px; color: var(--text-muted); margin-left: 6px;">${{j.connections_count}} mutuals</span>
              </div>
              <div class="job-role">${{escapeHtml(j.role)}}</div>
              <div class="job-req-id">Req ID: ${{escapeHtml(j.job_id)}}</div>

              <div class="champ-callout">
                <div class="name">⭐ Champion: ${{escapeHtml(j.champion_name)}}</div>
                <div class="title">${{escapeHtml(j.champion_position)}}</div>
              </div>
            </div>

            <div class="card-actions">
              <a href="${{j.job_url}}" target="_blank" class="btn btn-portal">Apply / Portal ↗</a>
              ${{j.champion_url ? `<a href="${{j.champion_url}}" target="_blank" class="btn btn-champion">Champion Profile</a>` : '<button class="btn btn-champion" disabled>No Profile Link</button>'}}
              <button class="btn btn-copy-msg" onclick="copyJobReferral(${{idx}})">Copy Tailored Referral Message</button>
            </div>
          </div>
        `;
      }});

      grid.innerHTML = html;
    }}

    function escapeHtml(text) {{
      return (text || '')
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }}

    document.getElementById('searchInput').addEventListener('input', filterJobs);
    document.getElementById('sectorSelect').addEventListener('change', filterJobs);

    renderGrid(JOBS);
  </script>
</body>
</html>
'''

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated Enterprise Job Search Portal: {output_html} ({os.path.getsize(output_html) / 1024:.1f} KB)")
