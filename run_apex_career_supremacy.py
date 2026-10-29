import os
import json
from pathlib import Path

ROOT_DIR = Path('e:/anti')
APPS_DIR = ROOT_DIR / 'applications_generated'

def load_all_applications():
    apps = []
    for folder in APPS_DIR.iterdir():
        if folder.is_dir():
            mf = folder / 'APPLICATION_MANIFEST.json'
            if mf.exists():
                try:
                    with open(mf, encoding='utf-8') as f:
                        d = json.load(f)
                    
                    company = d.get('company_name') or d.get('company') or folder.name.replace('_', ' ').title()
                    role = d.get('target_role') or d.get('role') or 'Operations & Technology Associate'
                    corridor = d.get('corridor_location') or d.get('corridor') or 'Bengaluru'
                    ctc = d.get('compensation_bracket') or d.get('median_ctc') or '₹12.0L - ₹18.0L'
                    email = d.get('direct_email') or d.get('contact_email') or f"careers@{company.lower().replace(' ', '')}.com"
                    recruiter = d.get('primary_recruiter_gatekeeper') or d.get('recruiter') or 'Talent Acquisition Team'
                    careers = d.get('careers_portal_url') or d.get('careers_url') or 'https://www.linkedin.com/jobs'
                    
                    # Check for documents in folder
                    has_cover = (folder / 'COVER_LETTER.md').exists()
                    has_resume = (folder / 'ATS_RESUME.md').exists()
                    has_inmail = (folder / 'DIRECT_OUTREACH_INMAIL.md').exists()
                    has_306090 = (folder / 'DAY_30_60_90_PLAN.md').exists()
                    has_star = (folder / 'STAR_INTERVIEW_DEFENSE.md').exists()

                    apps.append({
                        'id': d.get('application_id', folder.name[:8].upper()),
                        'company': company,
                        'role': role,
                        'corridor': corridor,
                        'ctc': ctc,
                        'email': email,
                        'recruiter': recruiter,
                        'careers': careers,
                        'folder': folder.name,
                        'has_cover': has_cover,
                        'has_resume': has_resume,
                        'has_inmail': has_inmail,
                        'has_306090': has_306090,
                        'has_star': has_star
                    })
                except Exception as e:
                    pass
    return apps

def build_mission_control_html(apps):
    apps_json = json.dumps(apps, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADITYA MEHRA | Apex Career Conquest Mission Control</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #040711;
      --bg-surface: #090e1c;
      --bg-card: #0f1629;
      --bg-card-hover: #162039;
      --border: #1e2a47;
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.25);
      --emerald: #10b981;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.5;
      padding-bottom: 60px;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Nav */
    nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(4, 7, 17, 0.9);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 14px 36px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand span {{ color: var(--cyan); }}

    .badge-status {{
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: var(--emerald);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .badge-status::before {{
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 8px var(--emerald);
    }}

    .nav-links {{
      display: flex;
      gap: 12px;
    }}
    .nav-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .nav-btn:hover, .nav-btn.active {{
      border-color: var(--cyan);
      color: #fff;
      background: rgba(0, 242, 254, 0.06);
    }}

    /* Main Container */
    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 30px 36px 0;
    }}

    /* Hero Metrics */
    .hero-banner {{
      background: linear-gradient(135deg, rgba(15, 22, 41, 0.95), rgba(9, 14, 28, 0.95));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px 36px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 24px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }}
    .hero-info h1 {{
      font-size: 32px;
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .hero-info p {{
      color: var(--text-muted);
      font-size: 14px;
    }}

    .metrics-row {{
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .metric-pill {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 20px;
      text-align: center;
      min-width: 130px;
    }}
    .m-num {{
      font-size: 26px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--cyan);
    }}
    .m-lbl {{
      font-size: 11px;
      color: var(--text-sub);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    /* Tabs Bar */
    .tab-bar {{
      display: flex;
      gap: 12px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
      padding-bottom: 12px;
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .tab-btn:hover {{
      color: #fff;
    }}
    .tab-btn.active {{
      color: var(--cyan);
      background: rgba(0, 242, 254, 0.1);
    }}

    /* Filter Bar */
    .filter-wrap {{
      display: flex;
      gap: 14px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}
    .search-box {{
      flex: 1;
      min-width: 280px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 16px;
      color: #fff;
      font-family: var(--font-sans);
      font-size: 14px;
      outline: none;
    }}
    .search-box:focus {{
      border-color: var(--cyan);
      box-shadow: 0 0 12px var(--cyan-glow);
    }}

    .select-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 16px;
      color: #fff;
      font-family: var(--font-sans);
      font-size: 14px;
      outline: none;
    }}

    /* Apps Grid */
    .apps-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 18px;
    }}

    .app-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
    }}
    .app-card:hover {{
      border-color: var(--cyan);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }}

    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .app-id {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--cyan);
      background: rgba(0, 242, 254, 0.1);
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .app-ctc {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--amber);
    }}

    .app-comp {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }}
    .app-role {{
      font-size: 13px;
      color: var(--cyan);
      font-weight: 600;
      margin-bottom: 10px;
    }}
    .app-corridor {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .docket-pills {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 16px;
      padding-top: 10px;
      border-top: 1px dashed var(--border);
    }}
    .doc-pill {{
      font-family: var(--font-mono);
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid var(--border);
    }}
    .doc-pill.active {{
      background: rgba(16, 185, 129, 0.1);
      color: var(--emerald);
      border-color: rgba(16, 185, 129, 0.3);
    }}

    .card-actions {{
      display: flex;
      gap: 8px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }}
    .btn-card {{
      flex: 1;
      padding: 7px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .btn-card-primary {{
      background: var(--cyan);
      color: #040711;
      font-weight: 700;
    }}
    .btn-card-primary:hover {{
      box-shadow: 0 0 12px var(--cyan-glow);
    }}
    .btn-card-outline {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
    }}
    .btn-card-outline:hover {{
      border-color: var(--cyan);
      color: #fff;
    }}

    /* Modal Styling */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      z-index: 200;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }}
    .modal-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      width: 100%;
      max-width: 800px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 30px;
      position: relative;
    }}
    .modal-close {{
      position: absolute;
      top: 16px;
      right: 18px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
    }}
    .modal-pre {{
      background: #04060d;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: #cbd5e1;
      white-space: pre-wrap;
      line-height: 1.6;
      margin-top: 14px;
    }}

    /* Plan View */
    .plan-section {{
      display: none;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 32px;
    }}
    .plan-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      margin-top: 20px;
    }}
    .plan-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
    }}
    .plan-week {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--cyan);
      margin-bottom: 8px;
    }}
    .plan-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}
    .plan-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border);
      margin-top: 60px;
      padding-top: 30px;
      text-align: center;
      color: var(--text-sub);
      font-size: 13px;
      font-family: var(--font-mono);
    }}
  </style>
</head>
<body>

  <!-- Top Nav -->
  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ APEX MISSION CONTROL</span>
      <div class="badge-status">Conquest Engine Active</div>
    </div>
    <div class="nav-links">
      <a href="ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html" class="nav-btn" target="_blank">Portfolio Showcase ↗</a>
      <a href="BANGALORE_360_VISUAL_WORLD.html" class="nav-btn" target="_blank">Bengaluru 360° ↗</a>
      <a href="STAR_INTERVIEW_DEFENSE_MATRIX.html" class="nav-btn" target="_blank">STAR Defense ↗</a>
      <a href="BANGALORE_LIVE_REFERRAL_CONSOLE.html" class="nav-btn" target="_blank">7,500 Referrals ↗</a>
    </div>
  </nav>

  <main class="container">

    <!-- Hero Banner -->
    <div class="hero-banner">
      <div class="hero-info">
        <h1>Autonomous Career Conquest Mission Control</h1>
        <p>Complete execution cockpit managing 288+ pre-compiled enterprise application dossiers for Aditya Mehra (BBA IB, DSU '26)</p>
      </div>
      <div class="metrics-row">
        <div class="metric-pill">
          <div class="m-num" id="totalAppsCount">{len(apps)}</div>
          <div class="m-lbl">Ready Dossiers</div>
        </div>
        <div class="metric-pill">
          <div class="m-num">5</div>
          <div class="m-lbl">Target Tracks</div>
        </div>
        <div class="metric-pill">
          <div class="m-num">₹14.5L</div>
          <div class="m-lbl">Target Median CTC</div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('apps')">Application Dossiers ({len(apps)})</button>
      <button class="tab-btn" onclick="switchTab('plan')">30-Day Execution Playbook</button>
      <button class="tab-btn" onclick="switchTab('salary')">CTC & In-Hand Calculator</button>
    </div>

    <!-- Applications Tab -->
    <div id="appsTab">
      <div class="filter-wrap">
        <input type="text" id="searchInput" class="search-box" placeholder="Search by company, role, or corridor (e.g., 'Maersk', 'Operations', 'Whitefield')...">
        <select id="corridorFilter" class="select-box">
          <option value="">All Locations</option>
          <option value="Manyata">Manyata North</option>
          <option value="Bellandur">Bellandur / ORR</option>
          <option value="Whitefield">Whitefield</option>
          <option value="Koramangala">Koramangala / HSR</option>
          <option value="Electronic City">Electronic City</option>
        </select>
      </div>

      <div class="apps-grid" id="appsGrid">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- 30-Day Plan Tab -->
    <div id="planTab" class="plan-section">
      <h2 style="font-size: 22px; font-weight: 800; color: #fff; margin-bottom: 8px;">The 30-Day High-Velocity Offer Sprint</h2>
      <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 24px;">Structured week-by-week battle plan to convert applications into 3-5 concurrent offers.</p>

      <div class="plan-grid">
        <div class="plan-card">
          <div class="plan-week">WEEK 01 • DAYS 01 - 07</div>
          <div class="plan-title">The First-Wave Pipeline Saturation</div>
          <p class="plan-desc">
            Dispatch 35 precision InMails to HR gatekeepers across Tier-1 GCCs (Maersk, Boeing, Target, Goldman Sachs). Submit 15 official careers portal applications with tailored ATS resumes.
          </p>
        </div>
        <div class="plan-card">
          <div class="plan-week">WEEK 02 • DAYS 08 - 14</div>
          <div class="plan-title">Referral Multiplier & Alumni Blitz</div>
          <p class="plan-desc">
            Engage DSU alumni and 2nd-degree connections in Bengaluru. Execute warm referral requests via BANGALORE_LIVE_REFERRAL_CONSOLE. Follow up on week 1 outbox with portfolio links.
          </p>
        </div>
        <div class="plan-card">
          <div class="plan-week">WEEK 03 • DAYS 15 - 21</div>
          <div class="plan-title">Screening Calls & STAR Domination</div>
          <p class="plan-desc">
            Convert recruiter screening calls into hiring manager rounds. Deploy pre-rehearsed STAR answers from STAR_INTERVIEW_DEFENSE_MATRIX for curveballs on BBA in tech and logistics crises.
          </p>
        </div>
        <div class="plan-card">
          <div class="plan-week">WEEK 04 • DAYS 22 - 30</div>
          <div class="plan-title">Case Study Demos & Offer Bidding</div>
          <p class="plan-desc">
            Present live proof-of-work (anti repository, Instawork benchmarks). Generate competitive bid tension across multiple offers to negotiate base CTC into the ₹12.5L – ₹18.0L bracket.
          </p>
        </div>
      </div>
    </div>

    <!-- Salary Tab -->
    <div id="salaryTab" class="plan-section">
      <h2 style="font-size: 22px; font-weight: 800; color: #fff; margin-bottom: 8px;">CTC to In-Hand Net Salary Calculator (New Tax Regime FY26-27)</h2>
      <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 24px;">Instant mathematical calculation of take-home salary after Indian income tax and standard deductions.</p>

      <div style="max-width: 500px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 24px;">
        <label style="font-size: 13px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px;">Annual Gross CTC (in Lakhs INR):</label>
        <input type="number" id="ctcInput" value="14.5" step="0.5" class="search-box" style="margin-bottom: 16px;" oninput="calculateTax()">
        
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed var(--border); font-size: 13px;">
          <span style="color: var(--text-muted);">Standard Deduction:</span>
          <span style="color: #fff; font-family: var(--font-mono);">₹75,000</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed var(--border); font-size: 13px;">
          <span style="color: var(--text-muted);">Estimated Annual Income Tax:</span>
          <span style="color: var(--rose); font-family: var(--font-mono);" id="taxOutput">₹1,12,500</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 12px 0 0; font-size: 16px; font-weight: 700;">
          <span style="color: #fff;">Monthly Take-Home:</span>
          <span style="color: var(--emerald); font-family: var(--font-mono);" id="monthlyOutput">₹1,05,200</span>
        </div>
      </div>
    </div>

  </main>

  <!-- Pitch Modal -->
  <div class="modal-overlay" id="pitchModal" onclick="if(event.target === this) closeModal()">
    <div class="modal-box">
      <button class="modal-close" onclick="closeModal()">✕</button>
      <h3 style="font-size: 18px; font-weight: 700; color: #fff;" id="modalTitle">Company Outreach Dossier</h3>
      <div style="font-size: 13px; color: var(--cyan); margin-bottom: 14px;" id="modalSubtitle">Target Role</div>
      <div class="modal-pre" id="modalContent">Content...</div>
      <div style="margin-top: 16px; display: flex; justify-content: flex-end; gap: 10px;">
        <button class="nav-btn" onclick="copyModalContent()">Copy Pitch 📋</button>
      </div>
    </div>
  </div>

  <footer>
    ADITYA MEHRA • BBA INTERNATIONAL BUSINESS '26 • DAYANANDA SAGAR UNIVERSITY, BENGALURU
    <br>POWERED BY OMEGA ∞ SUPREME AUTONOMOUS CAREER SUITE
  </footer>

  <script>
    const allApps = {apps_json};
    const appsGrid = document.getElementById('appsGrid');
    const searchInput = document.getElementById('searchInput');
    const corridorFilter = document.getElementById('corridorFilter');

    function renderApps(list) {{
      appsGrid.innerHTML = '';
      if (list.length === 0) {{
        appsGrid.innerHTML = '<div style="color: var(--text-sub); grid-column: 1/-1; text-align: center; padding: 40px;">No matching application dossiers found.</div>';
        return;
      }}

      list.forEach(app => {{
        const card = document.createElement('div');
        card.className = 'app-card';
        card.innerHTML = `
          <div>
            <div class="card-head">
              <span class="app-id">${{app.id}}</span>
              <span class="app-ctc">${{app.ctc}}</span>
            </div>
            <div class="app-comp">${{app.company}}</div>
            <div class="app-role">${{app.role}}</div>
            <div class="app-corridor">📍 ${{app.corridor}}</div>
            <div class="docket-pills">
              <span class="doc-pill ${{app.has_cover ? 'active' : ''}}">Cover Letter</span>
              <span class="doc-pill ${{app.has_resume ? 'active' : ''}}">ATS Resume</span>
              <span class="doc-pill ${{app.has_inmail ? 'active' : ''}}">InMail Pitch</span>
              <span class="doc-pill ${{app.has_star ? 'active' : ''}}">STAR Defense</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="btn-card btn-card-primary" onclick="openPitch('${{app.company.replace(/'/g, "\\\\'")}}', '${{app.role.replace(/'/g, "\\\\'")}}', '${{app.email}}', '${{app.careers}}')">Pitch & Dossier ✉</button>
            <a href="${{app.careers}}" target="_blank" class="btn-card btn-card-outline">Careers Portal ↗</a>
          </div>
        `;
        appsGrid.appendChild(card);
      }});
    }}

    function filterData() {{
      const q = searchInput.value.toLowerCase();
      const c = corridorFilter.value.toLowerCase();

      const filtered = allApps.filter(a => {{
        const matchesQ = !q || a.company.toLowerCase().includes(q) || a.role.toLowerCase().includes(q) || a.corridor.toLowerCase().includes(q);
        const matchesC = !c || a.corridor.toLowerCase().includes(c);
        return matchesQ && matchesC;
      }});

      renderApps(filtered);
    }}

    searchInput.addEventListener('input', filterData);
    corridorFilter.addEventListener('change', filterData);

    function switchTab(tab) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      document.getElementById('appsTab').style.display = tab === 'apps' ? 'block' : 'none';
      document.getElementById('planTab').style.display = tab === 'plan' ? 'block' : 'none';
      document.getElementById('salaryTab').style.display = tab === 'salary' ? 'block' : 'none';
    }}

    function openPitch(company, role, email, careers) {{
      document.getElementById('modalTitle').innerText = company;
      document.getElementById('modalSubtitle').innerText = role + ' | ' + email;
      
      const pitch = `Subject: Aditya Mehra — Candidate for ${{role}} (${{company}} Bengaluru)\\n\\nDear Talent Acquisition Lead,\\n\\nI noticed ${{company}}'s active expansion for operations and technology talent in Bengaluru.\\n\\nAs a final-year BBA International Business graduate from Dayananda Sagar University (DSU, 2026), my background directly intersects with ${{company}}'s delivery benchmarks:\\n\\n1. Operational Rigor: Coordinated high-footfall field logistics during Aero India (Salt in My Cocoa) and commercial vendor matrices at Pencil Mark, executing 100% balance reconciliations with zero discrepancy.\\n2. Technical & Data Grounding: Completed AI robotics data quality audits at Instawork with 99.2% precision, and engineered autonomous operational workflow engines in Python & SQLite with 16/16 verified unit tests green.\\n3. Immediate Joining Readiness: Full-time availability in Bengaluru with zero notice period friction.\\n\\nVerified Proof-of-Work & Verification Codebase:\\n• GitHub Repository: https://github.com/AdityaMehra007/anti\\n• Official Careers Portal: ${{careers}}\\n\\nI would welcome a brief 5-minute conversation this week to share how I can immediately unblock your team's operational backlog.\\n\\nBest regards,\\nAditya Mehra\\nBengaluru, India | +91 7003456624 | adityamehra799@gmail.com\\nLinkedIn: linkedin.com/in/aditya-mehra | GitHub: github.com/AdityaMehra007`;

      document.getElementById('modalContent').innerText = pitch;
      document.getElementById('pitchModal').style.display = 'flex';
    }}

    function closeModal() {{
      document.getElementById('pitchModal').style.display = 'none';
    }}

    function copyModalContent() {{
      const text = document.getElementById('modalContent').innerText;
      navigator.clipboard.writeText(text);
      alert('Outreach pitch copied to clipboard!');
    }}

    function calculateTax() {{
      const ctcL = parseFloat(document.getElementById('ctcInput').value) || 0;
      const ctc = ctcL * 100000;
      const stdDeduction = 75000;
      const taxable = Math.max(0, ctc - stdDeduction);

      let tax = 0;
      if (taxable > 1500000) {{
        tax += (taxable - 1500000) * 0.30;
        tax += 300000 * 0.20;
        tax += 300000 * 0.15;
        tax += 300000 * 0.10;
        tax += 300000 * 0.05;
      }} else if (taxable > 1200000) {{
        tax += (taxable - 1200000) * 0.20;
        tax += 300000 * 0.15;
        tax += 300000 * 0.10;
        tax += 300000 * 0.05;
      }} else if (taxable > 900000) {{
        tax += (taxable - 900000) * 0.15;
        tax += 300000 * 0.10;
        tax += 300000 * 0.05;
      }} else if (taxable > 600000) {{
        tax += (taxable - 600000) * 0.10;
        tax += 300000 * 0.05;
      }} else if (taxable > 300000) {{
        tax += (taxable - 300000) * 0.05;
      }}

      // Section 87A rebate for taxable <= 700000
      if (taxable <= 700000) {{
        tax = 0;
      }} else {{
        tax = tax * 1.04; // Cess
      }}

      const annualInHand = ctc - tax - 2400; // Professional Tax
      const monthlyInHand = Math.round(annualInHand / 12);

      document.getElementById('taxOutput').innerText = '₹' + Math.round(tax).toLocaleString('en-IN');
      document.getElementById('monthlyOutput').innerText = '₹' + monthlyInHand.toLocaleString('en-IN');
    }}

    // Initial render
    renderApps(allApps);
    calculateTax();
  </script>
</body>
</html>
'''

    out_file_1 = ROOT_DIR / 'ADITYA_CAREER_CONQUEST_MISSION_CONTROL.html'
    out_file_2 = ROOT_DIR / 'apps' / 'job_application_studio' / 'aditya_career_conquest_mission_control.html'

    with open(out_file_1, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(out_file_2, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated Career Conquest Mission Control at {out_file_1} and {out_file_2}")

def build_30_day_playbook():
    playbook_md = """# 🏆 ADITYA MEHRA — 30-DAY CAREER CONQUEST PLAYBOOK
**Target CTC**: ₹12.5 LPA – ₹24.0 LPA | **Target Base**: Bengaluru GCCs & High-Growth Unicorns  
**Degree**: BBA International Business (Dayananda Sagar University '26)  
**Notice Period**: 0 Days (Immediate Joining) | **Verified Experience**: 3 Internships (2 Corp + 1 NGO) + Event Ops

---

## 🎯 The Core Philosophy: Asymmetric Proof-of-Work
An average BBA fresher applies randomly on job boards with a 1-page generic resume and waits.  
You do **not** do that. You attack with:
1. **Pre-Staged Application Dossiers**: Tailored ATS resumes, customized cover letters, and 30-60-90 day blueprints.
2. **Deterministic Technical Proof-of-Work**: A live GitHub repository (`anti`) with 16/16 verified unit tests passing green.
3. **Field-Tested Operations Integrity**: Measurable results from Aero India (0.0% variance), Instawork (99.2% accuracy), and Pencil Mark vendor procurement.

---

## 📅 The 30-Day Master Schedule

### Week 1: Ground-Zero Saturation (Days 1 – 7)
* **Goal**: 35 direct HR/Recruiter touches + 20 official careers applications submitted.
* **Daily Rhythm (09:30 AM – 12:30 PM)**:
  * Open `ADITYA_CAREER_CONQUEST_MISSION_CONTROL.html`.
  * Target 5 high-priority GCCs daily (Maersk, Boeing, Target, Lowe's, Goldman Sachs, JPMorgan).
  * Copy the tailored InMail pitch and send via LinkedIn to the designated Talent Acquisition Lead.
  * Submit the official application through the pre-linked Careers Portal URL using your corresponding tailored ATS resume.
* **Evening Rhythm (05:00 PM – 06:30 PM)**:
  * Run `python sovereign_strike_cli.py --target "<Company>" --track operations` for newly identified openings.
  * Log all dispatched touches in `data/approval_queue.csv`.

### Week 2: Warm Referrals & Alumni Infiltration (Days 8 – 14)
* **Goal**: Convert 10 warm referrals from Dayananda Sagar University (DSU) alumni and 2nd-degree connections.
* **Execution**:
  * Open `BANGALORE_LIVE_REFERRAL_CONSOLE.html`.
  * Filter for DSU Alumni and Tier-1 Tech Park employees in RMZ Ecoworld, Manyata, and ITPL.
  * Send the warm referral request script:
    > *"Hi [Name], I noticed your journey at [Company] from DSU. As a final-year BBA International Business student graduating this year with operations experience across Aero India and Instawork, I am applying for the [Role] role. I've open-sourced my project portfolio at github.com/AdityaMehra007/anti. If my background looks aligned, would you be open to submitting an internal referral? Truly appreciate your time!"*

### Week 3: Screening Calls & STAR Domination (Days 15 – 21)
* **Goal**: Convert 5+ recruiter screening calls into final rounds with Hiring Managers / Operations Directors.
* **Execution**:
  * Keep `STAR_INTERVIEW_DEFENSE_MATRIX.html` open on a second monitor during all calls.
  * When the recruiter asks: *"Why hire a BBA instead of an engineer?"* -> Deliver the exact BBA Tech & AI STAR answer.
  * When asked about crisis management -> Deliver the Aero India UPI breakdown & inventory defense.
  * Always close with the Power Counter-Question:
    > *"What are the top 2 operational bottlenecks currently consuming your team's bandwidth that you would like me to eliminate within my first 30 days?"*

### Week 4: Case Study Presentation & Multi-Bid Offer Bidding (Days 22 – 30)
* **Goal**: Secure 2 to 4 concurrent offer letters and negotiate base compensation to the top of the band.
* **Execution**:
  * In the final hiring manager round, share your screen and walk through `ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html` and your 30-60-90 Day Plan.
  * When Offer #1 arrives (e.g. ₹9.5 LPA):
    * Thank them warmly, request 72 hours to review the formal offer letter.
    * Ping the recruiter of Company #2: *"I have received a formal offer for an operations analyst position, but [Company 2] remains my primary preference due to your global trade scale. What is the timeline for completing our final decision?"*
  * Drive competing bids to push total compensation to ₹12.5L – ₹18.0L.

---

## 🛠️ Your Daily Operational Checklist

- [ ] **09:00 AM**: Check LinkedIn notifications & inbound email inbox for recruiter replies.
- [ ] **10:00 AM**: Send 5 new precision InMail pitches via `ADITYA_CAREER_CONQUEST_MISSION_CONTROL.html`.
- [ ] **11:30 AM**: Submit 3 official career portal applications with tailored resumes.
- [ ] **02:00 PM**: Follow up on applications dispatched 4 business days ago.
- [ ] **04:00 PM**: 30-minute mock rehearsal using `STAR_INTERVIEW_DEFENSE_MATRIX.html`.
- [ ] **06:00 PM**: Review daily metrics and update pipeline status.
"""
    out_file = ROOT_DIR / 'ADITYA_30_DAY_CAREER_CONQUEST_PLAYBOOK.md'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(playbook_md)
    print(f"Generated 30-Day Playbook at {out_file}")

if __name__ == '__main__':
    apps = load_all_applications()
    print(f"Loaded {len(apps)} applications.")
    build_mission_control_html(apps)
    build_30_day_playbook()
