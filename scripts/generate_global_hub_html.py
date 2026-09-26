import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
from pathlib import Path

ROOT_DIR = Path("e:/anti")
DATA_FILE = ROOT_DIR / "data" / "bangalore_funded_startups_and_global_mncs.json"
HTML_OUT = ROOT_DIR / "apps" / "job_application_studio" / "global_mnc_and_startup_hub.html"

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
data_json_str = json.dumps(data, indent=2)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore Global MNCs, Funded Startups & Mass Hiring Hub | Aditya Mehra</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #07090e;
      --card-bg: #0d121d;
      --card-border: #1e293b;
      --card-hover: #273549;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.15);
      --green: #10b981;
      --green-glow: rgba(16, 185, 129, 0.15);
      --gold: #f59e0b;
      --purple: #a855f7;
      --rose: #f43f5e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding-bottom: 60px;
    }}
    .top-nav {{
      background: #0b0f19;
      border-bottom: 1px solid var(--card-border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand h1 {{
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.3px;
      color: #fff;
    }}
    .brand span {{
      background: #1e293b;
      color: var(--accent);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .nav-actions {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 6px;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .btn-primary {{
      background: #0284c7;
      color: #fff;
    }}
    .btn-primary:hover {{ background: #0369a1; }}
    .btn-secondary {{
      background: #1e293b;
      color: #cbd5e1;
      border-color: #334155;
    }}
    .btn-secondary:hover {{ background: #334155; color: #fff; }}
    .btn-green {{
      background: #065f46;
      color: #a7f3d0;
      border-color: #047857;
    }}
    .btn-green:hover {{ background: #047857; color: #fff; }}
    .btn-purple {{
      background: #4c1d95;
      color: #e9d5ff;
      border-color: #6d28d9;
    }}
    .btn-purple:hover {{ background: #6d28d9; color: #fff; }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
    }}

    .hero-strip {{
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .hero-strip h2 {{
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }}
    .hero-strip p {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 16px;
    }}
    .stat-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .stat-val {{
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }}
    .stat-val.blue {{ color: var(--accent); }}
    .stat-val.green {{ color: var(--green); }}
    .stat-val.gold {{ color: var(--gold); }}
    .stat-val.purple {{ color: var(--purple); }}

    .controls-bar {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .search-row {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .search-input {{
      flex: 1;
      background: #07090e;
      border: 1px solid #334155;
      color: #fff;
      font-size: 14px;
      padding: 10px 16px;
      border-radius: 8px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .pill {{
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }}
    .pill:hover {{
      background: #334155;
      color: #fff;
    }}
    .pill.active {{
      background: #0284c7;
      color: #fff;
      border-color: var(--accent);
    }}

    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(440px, 1fr));
      gap: 20px;
    }}
    .company-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .company-card:hover {{
      border-color: #38bdf8;
      transform: translateY(-2px);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 8px;
    }}
    .company-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
    }}
    .origin-badge {{
      font-size: 10px;
      font-weight: 600;
      background: #1e293b;
      color: #93c5fd;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
    }}
    .sector-tag {{
      font-size: 11px;
      color: var(--accent);
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .funding-badge {{
      display: inline-block;
      font-size: 11px;
      background: rgba(16, 185, 129, 0.1);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 3px 8px;
      border-radius: 4px;
      margin-bottom: 12px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .funding-badge.mass {{
      background: rgba(168, 85, 247, 0.1);
      color: #c084fc;
      border-color: rgba(168, 85, 247, 0.3);
    }}
    .corridor-info {{
      font-size: 12px;
      color: #cbd5e1;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .role-box {{
      background: #07090e;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 14px;
    }}
    .role-title {{
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
      margin-bottom: 4px;
    }}
    .salary-row {{
      display: flex;
      gap: 12px;
      font-size: 11px;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
      flex-wrap: wrap;
    }}
    .salary-badge {{
      color: #38bdf8;
      font-weight: 700;
    }}
    .in-hand-badge {{
      color: #10b981;
      font-weight: 700;
    }}

    /* Benefits Matrix Box */
    .benefits-matrix {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 10px 12px;
      margin-bottom: 14px;
    }}
    .benefits-heading {{
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #a7f3d0;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .benefits-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      font-size: 11px;
      color: #cbd5e1;
    }}
    .benefit-item {{
      display: flex;
      align-items: flex-start;
      gap: 5px;
      line-height: 1.3;
    }}
    .benefit-icon {{
      font-size: 12px;
      flex-shrink: 0;
    }}

    .rationale-text {{
      font-size: 11px;
      color: #94a3b8;
      font-style: italic;
      line-height: 1.4;
      margin-bottom: 14px;
      padding-left: 8px;
      border-left: 2px solid #334155;
    }}
    .contact-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: #cbd5e1;
      padding: 8px 0;
      border-top: 1px solid #1e293b;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .card-actions {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .btn-card-apply {{
      flex: 1;
      min-width: 100px;
      background: #0284c7;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 6px;
      text-align: center;
      text-decoration: none;
      transition: background 0.15s;
    }}
    .btn-card-apply:hover {{ background: #0369a1; }}
    .btn-card-walkin {{
      background: #4c1d95;
      color: #e9d5ff;
      border: 1px solid #6d28d9;
      font-size: 11px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .btn-card-walkin:hover {{ background: #6d28d9; color: #fff; }}
    .btn-card-copy {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      font-size: 11px;
      padding: 8px 10px;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .btn-card-copy:hover {{ background: #334155; color: #fff; }}
    .btn-card-call {{
      background: #1e293b;
      color: #6ee7b7;
      border: 1px solid #065f46;
      font-size: 11px;
      padding: 8px 10px;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
    }}
    .btn-card-call:hover {{ background: #065f46; color: #fff; }}

    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #10b981;
      color: #064e3b;
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      display: none;
      z-index: 100;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="brand">
      <h1>Bangalore Global MNCs, Funded Startups & Mass Hiring Hub</h1>
      <span>60 TIER-1 ENTERPRISES</span>
    </div>
    <div class="nav-actions">
      <a href="../../BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv" download class="btn btn-green">📥 Master CSV (60)</a>
      <a href="../../BANGALORE_MASS_AND_BULK_HIRING_MASTER.csv" download class="btn btn-purple">🏭 Mass Hiring CSV (15)</a>
      <a href="../candidate_clipboard_assistant.html" target="_blank" class="btn btn-secondary">📋 Clipboard Assistant</a>
      <a href="../get_me_hired_dashboard/index.html" class="btn btn-primary">← Back to Dashboard</a>
    </div>
  </nav>

  <div class="container">

    <!-- Hero Strip -->
    <div class="hero-strip">
      <h2>Curated Non-Sales Employment Matrix (Bangalore Tech Ecosystem)</h2>
      <p>Targeted exclusively for <strong>Aditya Mehra | BBA in International Business (Dayananda Sagar University '26)</strong>. Every company in this directory features verified Bangalore operations, direct HR desk lines, guaranteed <strong>0% Sales Risk (strictly non-sales / operations)</strong>, and complete employee benefit breakdowns (24/7 doorstep cabs, health insurance ₹3L–₹5L, shift allowances, meal passes, higher education sponsorship, and statutory PF/gratuity).</p>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Verified Enterprises</div>
        <div class="stat-val blue" id="stat-total">60</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Mass Hiring Giants</div>
        <div class="stat-val purple">10 IT/BPS</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Placement Agencies</div>
        <div class="stat-val gold">5 MASTERS</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Funded Unicorns</div>
        <div class="stat-val green">15 FIRMS</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">USA MNC GCCs</div>
        <div class="stat-val blue">13 GCCs</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">UK & European Giants</div>
        <div class="stat-val gold">13 FIRMS</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Big 4 Delivery Hubs</div>
        <div class="stat-val blue">4 FIRMS</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Sales Exposure Risk</div>
        <div class="stat-val green">0% (EXCLUDED)</div>
      </div>
    </div>

    <!-- Controls Bar -->
    <div class="controls-bar">
      <div class="search-row">
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Instant search by company, role (e.g. SCM, Operations, Logistics, Procurement), benefit (cabs, insurance), or corridor..." oninput="filterCompanies()">
      </div>
      <div class="filter-pills" id="sector-pills">
        <span class="pill active" onclick="setSectorFilter('all')">All Enterprises (60)</span>
        <span class="pill" onclick="setSectorFilter('mass')">🏭 Mass & Bulk Hiring Giants (10)</span>
        <span class="pill" onclick="setSectorFilter('agency')">🤝 Top Staffing & Placement Masters (5)</span>
        <span class="pill" onclick="setSectorFilter('startup')">🦄 Funded Startups & Unicorns (15)</span>
        <span class="pill" onclick="setSectorFilter('usa')">🇺🇸 USA MNC GCCs (13)</span>
        <span class="pill" onclick="setSectorFilter('uk')">🇬🇧 UK Enterprises (6)</span>
        <span class="pill" onclick="setSectorFilter('europe')">🇪🇺 Europe & Global SCM (7)</span>
        <span class="pill" onclick="setSectorFilter('big4')">🏛️ Big 4 Delivery Centers (4)</span>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="cards-grid" id="cards-container"></div>

  </div>

  <div class="toast" id="toast">Copied to clipboard!</div>

  <script>
    const allCompanies = {data_json_str};
    let currentSector = 'all';

    function setSectorFilter(sector) {{
      currentSector = sector;
      document.querySelectorAll('#sector-pills .pill').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      filterCompanies();
    }}

    function filterCompanies() {{
      const query = document.getElementById('search-box').value.toLowerCase().trim();
      const filtered = allCompanies.filter(c => {{
        let matchesSector = true;
        const cid = c.id || '';
        const cat = (c.category || '').toLowerCase();

        if (currentSector === 'mass') {{
          matchesSector = (cid.startsWith('MASS-BLR-00') || cid === 'MASS-BLR-010');
        }} else if (currentSector === 'agency') {{
          matchesSector = cid.startsWith('MASS-BLR-01') && cid !== 'MASS-BLR-010';
        }} else if (currentSector === 'startup') {{
          matchesSector = cid.startsWith('FS-');
        }} else if (currentSector === 'usa') {{
          matchesSector = cid.startsWith('US-');
        }} else if (currentSector === 'uk') {{
          matchesSector = cid.startsWith('UK-');
        }} else if (currentSector === 'europe') {{
          matchesSector = cid.startsWith('EU-');
        }} else if (currentSector === 'big4') {{
          matchesSector = cid.startsWith('B4-');
        }}

        const b = c.benefits_package || {{}};
        const benefitsStr = [b.transport, b.medical_insurance, b.shift_allowance, b.food_perks, b.higher_education, b.statutory].filter(Boolean).join(' ');
        const text = (c.company_name + ' ' + c.category + ' ' + c.bangalore_corridor + ' ' + c.target_role + ' ' + c.funding_status + ' ' + benefitsStr).toLowerCase();
        const matchesQuery = !query || text.includes(query);

        return matchesSector && matchesQuery;
      }});

      renderCards(filtered);
      document.getElementById('stat-total').innerText = filtered.length;
    }}

    function renderCards(list) {{
      const container = document.getElementById('cards-container');
      if (!list.length) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #94a3b8; font-size: 15px;">No companies matched your search filter. Try another keyword or sector pill.</div>`;
        return;
      }}

      container.innerHTML = list.map(c => {{
        const b = c.benefits_package;
        const hasBenefits = b && (b.transport || b.medical_insurance || b.shift_allowance);
        const isMass = (c.id || '').startsWith('MASS-');
        const walkinUrl = c.workday_lever_greenhouse || '';

        return `
        <div class="company-card">
          <div>
            <div class="card-header">
              <div>
                <div class="company-title">${{c.company_name}}</div>
                <div class="sector-tag">${{c.category}}</div>
              </div>
              <span class="origin-badge">${{c.origin_country}}</span>
            </div>

            <div class="funding-badge ${{isMass ? 'mass' : ''}}">⚡ ${{c.funding_status}}</div>

            <div class="corridor-info">
              <span>📍 ${{c.bangalore_corridor}}</span>
            </div>

            <div class="role-box">
              <div class="role-title">🎯 ${{c.target_role}}</div>
              <div class="salary-row">
                <span>Base: <strong class="salary-badge">₹${{c.fixed_base_lpa}}L</strong></span>
                <span>CTC: <strong class="salary-badge">₹${{c.total_ctc_min}}L - ₹${{c.total_ctc_max}}L</strong></span>
                <span>In-Hand: <strong class="in-hand-badge">~₹${{c.monthly_in_hand_est ? c.monthly_in_hand_est.toLocaleString() : 'N/A'}}/mo</strong></span>
              </div>
            </div>

            ${{hasBenefits ? `
            <div class="benefits-matrix">
              <div class="benefits-heading">🎁 Complete Employee Benefits Package</div>
              <div class="benefits-grid">
                ${{b.transport ? `<div class="benefit-item"><span class="benefit-icon">🚕</span><span>${{b.transport}}</span></div>` : ''}}
                ${{b.medical_insurance ? `<div class="benefit-item"><span class="benefit-icon">🏥</span><span>${{b.medical_insurance}}</span></div>` : ''}}
                ${{b.shift_allowance ? `<div class="benefit-item"><span class="benefit-icon">🌙</span><span>${{b.shift_allowance}}</span></div>` : ''}}
                ${{b.food_perks ? `<div class="benefit-item"><span class="benefit-icon">🍱</span><span>${{b.food_perks}}</span></div>` : ''}}
                ${{b.higher_education ? `<div class="benefit-item"><span class="benefit-icon">🎓</span><span>${{b.higher_education}}</span></div>` : ''}}
                ${{b.statutory ? `<div class="benefit-item"><span class="benefit-icon">💰</span><span>${{b.statutory}}</span></div>` : ''}}
              </div>
            </div>
            ` : ''}}

            <div class="rationale-text">"${{c.strategic_fit_rationale}}"</div>

            <div class="contact-row">
              <div>
                <div style="font-weight: 600; color: #fff;">${{c.hr_lead}}</div>
                <div style="color: #64748b; font-size: 10px;">${{c.hr_email}}</div>
              </div>
              <div>
                <span style="font-family: 'JetBrains Mono', monospace; color: #93c5fd;">${{c.desk_phone}}</span>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <a href="${{c.direct_apply_url}}" target="_blank" class="btn-card-apply">Apply Portal ↗</a>
            ${{walkinUrl ? `<a href="${{walkinUrl}}" target="_blank" class="btn-card-walkin">Walk-In / Portal ↗</a>` : ''}}
            <button class="btn-card-copy" onclick="copyText('${{c.hr_email}}', 'HR Email copied!')">📋 Email</button>
            <a href="tel:${{c.desk_phone}}" class="btn-card-call">📞 Call</a>
          </div>
        </div>
        `;
      }}).join('');
    }}

    function copyText(text, msg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(msg);
      }});
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 2000);
    }}

    window.onload = () => {{
      renderCards(allCompanies);
    }};
  </script>
</body>
</html>
"""

HTML_OUT.write_text(html_content, encoding="utf-8")
print(f"[OK] Generated interactive hub HTML at {HTML_OUT}")
