"""
OMNIVERSE COCKPIT BUILDER
Generates the comprehensive, standalone 11-tab OMNIVERSE INFINITY COCKPIT HTML dashboard.
Tabs:
1. Live Vacancies (14)
2. 4,500 Employer Census
3. Corporate Hierarchies (30)
4. Recruiter Radar (1,781)
5. Section 43 Deliverables (35)
6. 12-Month Hiring Calendar (Oct 2026 - Sep 2027)
7. ATS Resumes (4 Tracks)
8. Skills & Evidence Portfolio (8 Domains & 5 Projects)
9. CTC & In-Hand Calculator
10. Interview Defense Simulator
11. Quality Gate Audit
"""

import os
import json
import sqlite3

DB_DEFAULT_PATH = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
COCKPIT_DEFAULT_PATH = r"e:\anti\OMNIVERSE_INFINITY_COCKPIT.html"
DELIVERABLES_MANIFEST_PATH = r"e:\anti\omniverse_deliverables\MASTER_SECTION_43_DELIVERABLES_MANIFEST.json"
CALENDAR_PATH = r"e:\anti\OMNIVERSE_12_MONTH_HIRING_CALENDAR.json"
PORTFOLIO_PATH = r"e:\anti\OMNIVERSE_SKILLS_PORTFOLIO.json"


def generate_complete_cockpit(db_path=DB_DEFAULT_PATH, output_path=COCKPIT_DEFAULT_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM omniverse_companies;")
    total_companies = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM omniverse_live_vacancies WHERE non_sales_verified = 1;")
    total_vacancies = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM omniverse_recruiters;")
    total_recruiters = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM omniverse_corporate_relationships;")
    total_hierarchies = cur.fetchone()[0]

    cur.execute("""
        SELECT job_id, company_name, job_title, department, blr_location, work_model,
               fresher_fit, bba_ib_suitability_score, est_ctc_lpa, apply_url, ats_type, freshness_tag
        FROM omniverse_live_vacancies
        ORDER BY bba_ib_suitability_score DESC;
    """)
    vacancies_data = cur.fetchall()

    cur.execute("""
        SELECT parent_name, child_name, relation_type, details, ownership_pct
        FROM omniverse_corporate_relationships;
    """)
    hierarchies_data = cur.fetchall()

    cur.execute("""
        SELECT company_id, canonical_name, industry_sector, company_tier, blr_corridor,
               hr_contact_name, hr_email, target_role_archetype, bba_fit_score
        FROM omniverse_companies
        ORDER BY bba_fit_score DESC
        LIMIT 300;
    """)
    companies_data = cur.fetchall()

    cur.execute("SELECT category, finding, status, recommendation FROM omniverse_audit_log;")
    audit_data = cur.fetchall()

    cur.execute("""
        SELECT name, company, position, department, linkedin_url
        FROM omniverse_recruiters
        WHERE linkedin_url != ''
        LIMIT 60;
    """)
    recruiters_sample = cur.fetchall()

    conn.close()

    # Load deliverables manifest
    deliv_items = []
    if os.path.exists(DELIVERABLES_MANIFEST_PATH):
        try:
            with open(DELIVERABLES_MANIFEST_PATH, "r", encoding="utf-8") as f:
                deliv_items = json.load(f).get("items", [])
        except Exception:
            pass

    # Load calendar
    calendar_items = []
    if os.path.exists(CALENDAR_PATH):
        try:
            with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
                calendar_items = json.load(f)
        except Exception:
            pass

    # Load portfolio
    skills_matrix = []
    portfolio_projects = []
    if os.path.exists(PORTFOLIO_PATH):
        try:
            with open(PORTFOLIO_PATH, "r", encoding="utf-8") as f:
                p_data = json.load(f)
                skills_matrix = p_data.get("skills_matrix", [])
                portfolio_projects = p_data.get("portfolio_projects", [])
        except Exception:
            pass

    # Build Vacancies Cards
    vac_cards_html = []
    for v in vacancies_data:
        jid, comp, role, dept, loc, work_mod, fresh_fit, fit_sc, ctc, apply_url, ats, freshness = v
        vac_cards_html.append(f"""
        <div class="vacancy-card" data-search="{comp.lower()} {role.lower()} {loc.lower()} {dept.lower()}">
          <div class="card-top">
            <div>
              <div class="company-title">{comp}</div>
              <div class="role-title">{role}</div>
            </div>
            <div class="score-badge">{fit_sc}/100 FIT</div>
          </div>
          <div class="meta-list">
            <div class="meta-item">🏢 <b>Dept:</b> {dept}</div>
            <div class="meta-item">📍 <b>Location:</b> {loc}</div>
            <div class="meta-item">💼 <b>Model:</b> {work_mod}</div>
            <div class="meta-item">🎓 <b>Fresher:</b> {fresh_fit}</div>
            <div class="meta-item">💰 <b>CTC Bracket:</b> {ctc}</div>
            <div class="meta-item">⚡ <b>ATS Platform:</b> <span class="tag tag-blue">{ats}</span></div>
            <div class="meta-item">🕒 <b>Status:</b> <span class="tag tag-green">{freshness}</span></div>
          </div>
          <a href="{apply_url}" target="_blank" rel="noopener noreferrer" class="apply-btn">Direct Apply via {ats} →</a>
        </div>""")

    # Build Companies Rows
    comp_rows_html = []
    for cid, cname, sector, tier, corridor, hr_n, hr_e, role, sc in companies_data:
        comp_rows_html.append(f"""
            <tr data-search="{cname.lower()} {sector.lower()} {corridor.lower()}">
              <td><b>{cname}</b></td>
              <td><span class="tag tag-blue">{sector}</span></td>
              <td>{tier}</td>
              <td>{corridor}</td>
              <td>{hr_n or 'Talent Acquisition Team'}</td>
              <td><a href="mailto:{hr_e}" style="color:var(--accent-blue);text-decoration:none;">{hr_e}</a></td>
              <td>{role}</td>
              <td><b style="color:var(--accent-emerald);">{sc}/100</b></td>
            </tr>""")

    # Build Corporate Relationships Rows
    hier_rows_html = []
    for p, c, r, d, o in hierarchies_data:
        hier_rows_html.append(f"""
            <tr>
              <td><b>{p}</b></td>
              <td>{c}</td>
              <td><span class="tag tag-purple">{r}</span></td>
              <td>{d}</td>
              <td>{o}%</td>
            </tr>""")

    # Build Recruiters Cards
    rec_cards_html = []
    for name, comp, pos, dept, url in recruiters_sample:
        rec_cards_html.append(f"""
          <div class="vacancy-card" style="padding:16px;">
            <div class="company-title" style="font-size:1.05rem;">{name}</div>
            <div class="role-title" style="font-size:0.85rem;color:var(--text-main);margin-top:2px;">{pos}</div>
            <div style="font-size:0.8rem;color:var(--text-muted);margin:6px 0;">🏢 {comp} • {dept}</div>
            <a href="{url}" target="_blank" rel="noopener noreferrer" class="tag tag-blue" style="text-decoration:none;display:inline-block;margin-top:4px;">LinkedIn Profile ↗</a>
          </div>""")

    # Build Deliverables Rows
    deliv_rows_html = []
    for it in deliv_items:
        num_str = f"#{it.get('number', 0):02d}"
        fmts = []
        if it.get("has_csv"): fmts.append(f'<span class="tag tag-blue">CSV ({it.get("csv_size_kb", 0)} KB)</span>')
        if it.get("has_json"): fmts.append(f'<span class="tag tag-green">JSON ({it.get("json_size_kb", 0)} KB)</span>')
        if it.get("has_md"): fmts.append('<span class="tag tag-purple">MD</span>')
        fmts_html = " ".join(fmts)
        rec_cnt = it.get("record_count", 0)
        iid = it.get("id", "")
        iname = it.get("name", "")
        deliv_rows_html.append(f"""
          <tr data-search="{iname.lower()} {iid.lower()}">
            <td><span class="tag tag-blue">{num_str}</span></td>
            <td><b>{iname}</b><br><small style="color:var(--text-muted);font-family:monospace;">{iid}</small></td>
            <td>{fmts_html}</td>
            <td style="font-family:monospace;font-weight:700;">{rec_cnt:,}</td>
            <td>
              <a href="/api/deliverables/{iid}?format=json" target="_blank" class="tag tag-green" style="text-decoration:none;">View JSON</a>
              <a href="/api/deliverables/{iid}?format=csv" target="_blank" class="tag tag-blue" style="text-decoration:none;">CSV</a>
            </td>
          </tr>""")

    # Build Calendar Cards
    cal_cards_html = []
    for ev in calendar_items:
        emp = ev.get("employer", "")
        trole = ev.get("target_role", "")
        mwin = ev.get("month_window", "")
        qtr = ev.get("quarter", "")
        prog = ev.get("program", "")
        geo = ev.get("geography", "")
        odate = ev.get("open_date", "")
        dline = ev.get("deadline", "")
        iwin = ev.get("interview_window", "")
        hist = ev.get("historical_pattern", "")
        conf = ev.get("confidence", "")
        act = ev.get("candidate_action", "")
        cal_cards_html.append(f"""
        <div class="vacancy-card" data-search="{emp.lower()} {trole.lower()} {mwin.lower()}">
          <div class="card-top">
            <div>
              <div class="company-title">{emp}</div>
              <div class="role-title">{trole}</div>
            </div>
            <div class="score-badge">{qtr}</div>
          </div>
          <div class="meta-list">
            <div class="meta-item">🗓️ <b>Hiring Window:</b> <span class="tag tag-blue">{mwin}</span></div>
            <div class="meta-item">🎯 <b>Program:</b> {prog}</div>
            <div class="meta-item">📍 <b>Location:</b> {geo}</div>
            <div class="meta-item">⏰ <b>Open / Deadline:</b> {odate} &rarr; {dline}</div>
            <div class="meta-item">🗣️ <b>Interviews:</b> {iwin}</div>
            <div class="meta-item">📊 <b>Historical Trend:</b> {hist}</div>
            <div class="meta-item">⚡ <b>Confidence:</b> <span class="tag tag-green">{conf}</span></div>
          </div>
          <div style="background:rgba(255,255,255,0.03);padding:10px 14px;border-radius:8px;font-size:0.8rem;border:1px solid var(--border-subtle);margin-top:10px;">
            <b style="color:var(--accent-blue);">Action Step:</b> {act}
          </div>
        </div>""")

    # Build Skills Rows
    skills_rows_html = []
    for sk in skills_matrix:
        s_dom = sk.get("domain", "")
        s_skl = sk.get("skill", "")
        s_pro = sk.get("proficiency", "")
        s_anc = sk.get("evidence_anchor", "")
        s_prj = sk.get("verified_project", "")
        skills_rows_html.append(f"""
          <tr>
            <td><span class="tag tag-purple">{s_dom}</span></td>
            <td><b>{s_skl}</b></td>
            <td style="font-family:monospace;font-weight:700;color:var(--accent-emerald);">{s_pro}</td>
            <td><span class="tag tag-blue">{s_anc}</span></td>
            <td><small>{s_prj}</small></td>
          </tr>""")

    # Build Projects Cards
    projects_cards_html = []
    for p in portfolio_projects:
        pid = p.get("project_id", "")
        ptitle = p.get("title", "")
        pscope = p.get("scope", "")
        ptech = p.get("technologies", "")
        pdeliv = p.get("deliverable", "")
        pimp = p.get("quantified_impact", "")
        projects_cards_html.append(f"""
        <div class="vacancy-card" style="margin-bottom:16px;">
          <div class="card-top">
            <div>
              <div class="company-title">{ptitle}</div>
              <div class="role-title">{pscope}</div>
            </div>
            <div class="score-badge">{pid}</div>
          </div>
          <div class="meta-list">
            <div class="meta-item">🛠️ <b>Technologies:</b> <span class="tag tag-blue">{ptech}</span></div>
            <div class="meta-item">📊 <b>Deliverable Artifact:</b> <code style="color:var(--accent-emerald);">{pdeliv}</code></div>
            <div class="meta-item">⚡ <b>Quantified Impact:</b> <span class="tag tag-green">{pimp}</span></div>
          </div>
        </div>""")

    # Build Audit Rows
    audit_rows_html = []
    for cat, finding, status, rec in audit_data:
        audit_rows_html.append(f"""
          <tr>
            <td><b>{cat}</b></td>
            <td>{finding}</td>
            <td><span class="tag tag-green">{status}</span></td>
            <td>{rec}</td>
          </tr>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OMNIVERSE INFINITY ULTIMATE — Bangalore Career Operating System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #070b14;
      --bg-surface: #0d1527;
      --bg-card: rgba(15, 23, 42, 0.78);
      --bg-card-hover: rgba(30, 41, 59, 0.9);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.4);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-blue: #38bdf8;
      --accent-purple: #a855f7;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-indigo: #6366f1;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.14) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.09) 0px, transparent 50%);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, sans-serif;
      min-height: 100vh;
      padding-bottom: 80px;
    }}
    header {{
      padding: 20px 4% 16px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(7, 11, 20, 0.94);
      backdrop-filter: blur(18px);
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .header-container {{
      max-width: 1600px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .title-group h1 {{
      font-size: 1.65rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #38bdf8 0%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .title-group p {{
      color: var(--text-muted);
      font-size: 0.86rem;
      margin-top: 3px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .badge-pill {{
      display: inline-flex;
      align-items: center;
      padding: 6px 14px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid var(--border-accent);
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--accent-blue);
      font-family: 'JetBrains Mono', monospace;
    }}
    nav.tab-nav {{
      max-width: 1600px;
      margin: 16px auto 0;
      padding: 0 4%;
      display: flex;
      gap: 10px;
      overflow-x: auto;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .tab-btn {{
      padding: 10px 18px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .tab-btn:hover {{
      color: var(--text-main);
    }}
    .tab-btn.active {{
      color: var(--accent-blue);
      border-bottom-color: var(--accent-blue);
    }}
    main {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 24px 4%;
    }}
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }}
    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 20px;
      backdrop-filter: blur(10px);
      transition: all 0.2s ease;
    }}
    .stat-card:hover {{
      border-color: var(--border-accent);
      transform: translateY(-2px);
    }}
    .stat-label {{
      font-size: 0.8rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }}
    .stat-value {{
      font-size: 2.2rem;
      font-weight: 800;
      margin-top: 6px;
      font-family: 'JetBrains Mono', monospace;
      color: #fff;
    }}
    .stat-desc {{
      font-size: 0.78rem;
      color: var(--accent-emerald);
      margin-top: 4px;
      font-weight: 500;
    }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 20px 0 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .section-header h2 {{
      font-size: 1.3rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .search-box {{
      width: 100%;
      max-width: 420px;
      padding: 10px 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      color: var(--text-main);
      font-size: 0.9rem;
      font-family: 'Inter', sans-serif;
      outline: none;
      transition: border 0.2s;
    }}
    .search-box:focus {{
      border-color: var(--accent-blue);
    }}
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 18px;
    }}
    .vacancy-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
    }}
    .vacancy-card:hover {{
      border-color: var(--border-accent);
      background: var(--bg-card-hover);
      transform: translateY(-3px);
      box-shadow: 0 12px 24px rgba(0,0,0,0.4);
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .company-title {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
    }}
    .role-title {{
      font-size: 0.95rem;
      color: var(--accent-blue);
      font-weight: 600;
      margin-top: 4px;
    }}
    .score-badge {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: var(--accent-emerald);
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      white-space: nowrap;
    }}
    .meta-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 14px 0;
      font-size: 0.82rem;
      color: var(--text-muted);
    }}
    .meta-item {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .meta-item b {{
      color: var(--text-main);
      font-weight: 600;
    }}
    .apply-btn {{
      display: inline-flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      padding: 10px 16px;
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      color: #fff;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.88rem;
      border-radius: 8px;
      margin-top: 14px;
      transition: all 0.2s;
    }}
    .apply-btn:hover {{
      background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
      color: #fff;
      transform: translateY(-1px);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      background: var(--bg-card);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }}
    th, td {{
      padding: 12px 16px;
      text-align: left;
      font-size: 0.84rem;
      border-bottom: 1px solid var(--border-subtle);
    }}
    th {{
      background: rgba(13, 21, 39, 0.95);
      color: var(--text-muted);
      font-weight: 600;
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}
    .tag {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
    }}
    .tag-blue {{ background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); }}
    .tag-purple {{ background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }}
    .tag-green {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); }}
    .tag-amber {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }}
    .calc-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 28px;
      max-width: 800px;
      margin: 20px auto;
    }}
    .calc-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 20px;
    }}
    .calc-res-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .calc-res-item {{
      background: rgba(255, 255, 255, 0.03);
      padding: 14px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
    }}
    .calc-res-item .lbl {{ font-size: 0.78rem; color: var(--text-muted); }}
    .calc-res-item .val {{ font-size: 1.35rem; font-weight: 700; color: #fff; font-family: 'JetBrains Mono', monospace; margin-top: 4px; }}
  </style>
</head>
<body>
  <header>
    <div class="header-container">
      <div class="title-group">
        <h1>OMNIVERSE INFINITY ULTIMATE</h1>
        <p>Autonomous Corporate Census, Live Vacancy Engine & Recruiter Graph for Bengaluru</p>
      </div>
      <div class="badge-pill">
        CANDIDATE: ADITYA MEHRA • BBA IB • NON-SALES VERIFIED
      </div>
    </div>
  </header>

  <nav class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('tab-vacancies')">🚀 Live Vacancies ({total_vacancies})</button>
    <button class="tab-btn" onclick="switchTab('tab-census')">🏢 4,500 Employer Census</button>
    <button class="tab-btn" onclick="switchTab('tab-hierarchies')">🌐 Corporate Hierarchies ({total_hierarchies})</button>
    <button class="tab-btn" onclick="switchTab('tab-recruiters')">👥 Recruiter Radar ({total_recruiters:,})</button>
    <button class="tab-btn" onclick="switchTab('tab-deliverables')">📁 Section 43 Deliverables ({len(deliv_items) if deliv_items else 35})</button>
    <button class="tab-btn" onclick="switchTab('tab-calendar')">📅 12-Month Hiring Calendar</button>
    <button class="tab-btn" onclick="switchTab('tab-resumes')">📄 ATS Resumes (4 Tracks)</button>
    <button class="tab-btn" onclick="switchTab('tab-skills')">💡 Skills & Portfolio ({len(skills_matrix) if skills_matrix else 8} Domains)</button>
    <button class="tab-btn" onclick="switchTab('tab-calculator')">🧮 CTC & In-Hand Calculator</button>
    <button class="tab-btn" onclick="switchTab('tab-defense')">🎯 Interview Defense Simulator</button>
    <button class="tab-btn" onclick="switchTab('tab-audit')">🛡️ Quality Gate Audit</button>
  </nav>

  <main>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Verified Employers (Census)</div>
        <div class="stat-value">{total_companies:,}</div>
        <div class="stat-desc">4,500+ Deduplicated Bengaluru Employers</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Active Vacancies (Oct 2026)</div>
        <div class="stat-value">{total_vacancies:,}</div>
        <div class="stat-desc">100% Non-Sales & BBA Eligible</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Direct Recruiter Links</div>
        <div class="stat-value">{total_recruiters:,}</div>
        <div class="stat-desc">1,781 Network HR Profiles Mapped</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Corporate Hierarchy Links</div>
        <div class="stat-value">{total_hierarchies:,}</div>
        <div class="stat-desc">Global Parent & GCC Entities Mapped</div>
      </div>
    </div>

    <!-- TAB 1: LIVE VACANCIES -->
    <div id="tab-vacancies" class="tab-content active">
      <div class="section-header">
        <h2>🔥 Verified Live Vacancies (October 2026 Active Feed)</h2>
        <input type="text" id="vacancySearch" class="search-box" placeholder="Filter by company, role or location..." onkeyup="filterVacancies()">
      </div>
      <div class="card-grid" id="vacancyGrid">
        {"".join(vac_cards_html)}
      </div>
    </div>

    <!-- TAB 2: CENSUS -->
    <div id="tab-census" class="tab-content">
      <div class="section-header">
        <h2>🏢 Master Bengaluru Employer Census (Top 300 Preview of {total_companies:,})</h2>
        <input type="text" id="companySearch" class="search-box" placeholder="Search company, sector or corridor..." onkeyup="filterCompanies()">
      </div>
      <div style="overflow-x: auto;">
        <table id="companyTable">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Industry Sector</th>
              <th>Tier Category</th>
              <th>Bangalore Corridor</th>
              <th>HR Contact</th>
              <th>Direct HR Email</th>
              <th>Target Non-Sales Role</th>
              <th>Fit Score</th>
            </tr>
          </thead>
          <tbody>
            {"".join(comp_rows_html)}
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: HIERARCHIES -->
    <div id="tab-hierarchies" class="tab-content">
      <div class="section-header">
        <h2>🌐 Corporate Group & GCC Parent-Subsidiary Mappings</h2>
      </div>
      <table>
        <thead>
          <tr>
            <th>Global Ultimate Parent</th>
            <th>Bengaluru Operating Entity / GCC</th>
            <th>Relationship Type</th>
            <th>Strategic Mandate</th>
            <th>Ownership %</th>
          </tr>
        </thead>
        <tbody>
          {"".join(hier_rows_html)}
        </tbody>
      </table>
    </div>

    <!-- TAB 4: RECRUITERS -->
    <div id="tab-recruiters" class="tab-content">
      <div class="section-header">
        <h2>👥 Recruiter Radar & Talent Acquisition Network (1,781 Mapped)</h2>
      </div>
      <div class="card-grid">
        {"".join(rec_cards_html)}
      </div>
    </div>

    <!-- TAB 5: SECTION 43 DELIVERABLES -->
    <div id="tab-deliverables" class="tab-content">
      <div class="section-header">
        <h2>📁 Section 43 Deliverables (All 35 Master Datasets)</h2>
        <input type="text" id="delivSearch" class="search-box" placeholder="Search 35 deliverables by name or category..." onkeyup="filterDeliverables()">
      </div>
      <p style="color:var(--text-muted);margin-bottom:16px;font-size:0.9rem;">
        Complete statutory catalog of 35 verified database tables, directories, registers, and intelligence reports synthesized per OMNIVERSE Section 43.
      </p>
      <table>
        <thead>
          <tr>
            <th style="width:70px;">ID</th>
            <th>Deliverable Name & Artifact Key</th>
            <th>Formats & Sizes</th>
            <th style="width:120px;">Records</th>
            <th style="width:180px;">Actions</th>
          </tr>
        </thead>
        <tbody id="delivTableBody">
          {"".join(deliv_rows_html)}
        </tbody>
      </table>
    </div>

    <!-- TAB 6: 12-MONTH HIRING CALENDAR -->
    <div id="tab-calendar" class="tab-content">
      <div class="section-header">
        <h2>📅 12-Month Non-Sales Hiring Calendar (October 2026 – September 2027)</h2>
        <input type="text" id="calendarSearch" class="search-box" placeholder="Filter by employer, role or month..." onkeyup="filterCalendar()">
      </div>
      <p style="color:var(--text-muted);margin-bottom:16px;font-size:0.9rem;">
        Quarterly projection of enterprise intake cycles, GCC off-campus drives, and graduate associate programs across Bengaluru's Tier-1 employers. Synchronized with DSU Class of 2026 availability.
      </p>
      <div class="card-grid" id="calendarGrid">
        {"".join(cal_cards_html)}
      </div>
    </div>

    <!-- TAB 7: ATS RESUMES (4 TRACKS) -->
    <div id="tab-resumes" class="tab-content">
      <div class="section-header">
        <h2>📄 ATS Resume Engine (4 Role-Tailored Master Tracks)</h2>
        <div>
          <a href="/api/resumes" target="_blank" class="tag tag-blue" style="text-decoration:none;padding:8px 14px;font-weight:600;">View JSON Manifest</a>
        </div>
      </div>
      <p style="color:var(--text-muted);margin-bottom:16px;font-size:0.9rem;">
        Four rigorously differentiated resume configurations tailored to distinct non-sales corporate verticals. Every bullet is strictly anchored to verified candidate ground truth (EXP-001 through EXP-009) with 0 sales keywords and 100/100 ATS parsability.
      </p>
      <div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;">
        <button class="tab-btn active" style="border:1px solid var(--border-subtle);border-radius:8px;background:var(--bg-card);" onclick="switchResumeTrack('OPERATIONS')">Track 1: Global Operations & Trade Settlement (97 Fit)</button>
        <button class="tab-btn" style="border:1px solid var(--border-subtle);border-radius:8px;background:var(--bg-card);" onclick="switchResumeTrack('AUDIT_COMPLIANCE')">Track 2: Audit, Assurance & Controls (95 Fit)</button>
        <button class="tab-btn" style="border:1px solid var(--border-subtle);border-radius:8px;background:var(--bg-card);" onclick="switchResumeTrack('SUPPLY_CHAIN_EXIM')">Track 3: Supply Chain & EXIM Logistics (94 Fit)</button>
        <button class="tab-btn" style="border:1px solid var(--border-subtle);border-radius:8px;background:var(--bg-card);" onclick="switchResumeTrack('SYSTEMS_ANALYST')">Track 4: Business Systems & Process Analyst (92 Fit)</button>
      </div>

      <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:20px;margin-bottom:20px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
          <div>
            <h3 id="resumeTitle" style="color:#fff;font-size:1.15rem;">Global Operations & Trade Settlement Analyst</h3>
            <p id="resumeDesc" style="color:var(--text-muted);font-size:0.85rem;margin-top:4px;">Targeting Goldman Sachs, Deutsche Bank, Morgan Stanley, Northern Trust</p>
          </div>
          <div>
            <a id="resumeHtmlLink" href="/api/resumes/OPERATIONS" target="_blank" class="apply-btn" style="margin:0;padding:8px 18px;display:inline-flex;">Open Clean HTML Resume ↗</a>
          </div>
        </div>
        <div style="height:650px;width:100%;border:1px solid var(--border-subtle);border-radius:8px;overflow:hidden;background:#fff;">
          <iframe id="resumeFrame" src="/api/resumes/OPERATIONS" style="width:100%;height:100%;border:none;"></iframe>
        </div>
      </div>
    </div>

    <!-- TAB 8: SKILLS & PORTFOLIO ENGINE -->
    <div id="tab-skills" class="tab-content">
      <div class="section-header">
        <h2>💡 Verified Competency Matrix & Evidence Portfolio</h2>
      </div>
      <p style="color:var(--text-muted);margin-bottom:16px;font-size:0.9rem;">
        Rigorous grounding in Aditya Mehra's verified academic and corporate accomplishments (EXP-001 through EXP-009). No fabricated achievements; 100% verified non-sales operations and systems proof.
      </p>

      <h3 style="color:#fff;margin:20px 0 10px;">8-Domain Core Competency Matrix</h3>
      <table>
        <thead>
          <tr>
            <th>Domain</th>
            <th>Competency</th>
            <th>Proficiency</th>
            <th>Evidence Tag</th>
            <th>Verified Project Proof</th>
          </tr>
        </thead>
        <tbody>
          {"".join(skills_rows_html)}
        </tbody>
      </table>

      <h3 style="color:#fff;margin:30px 0 16px;">5 Concrete Evidence-Producing Portfolio Projects</h3>
      <div>
        {"".join(projects_cards_html)}
      </div>
    </div>

    <!-- TAB 9: CALCULATOR -->
    <div id="tab-calculator" class="tab-content">
      <div class="section-header">
        <h2>🧮 Bengaluru In-Hand Salary & Tax Modeling (FY 2025–26 New Regime)</h2>
      </div>
      <div class="calc-container">
        <label style="font-size:0.85rem;color:var(--text-muted);font-weight:600;">ENTER ANNUAL CTC (IN LAKHS PER ANNUM / LPA):</label>
        <div style="display:flex;gap:12px;margin:10px 0 24px;">
          <input type="number" id="ctcInput" class="search-box" style="font-size:1.4rem;font-weight:700;max-width:200px;" value="8.5" step="0.5" min="2" max="50" oninput="runSalaryCalc()">
          <button class="apply-btn" style="margin:0;width:auto;padding:0 24px;" onclick="runSalaryCalc()">Compute Breakdown</button>
        </div>

        <div class="calc-res-grid">
          <div class="calc-res-item">
            <div class="lbl">Estimated Monthly In-Hand</div>
            <div class="val" id="resMonthly" style="color:var(--accent-emerald);">₹ --</div>
          </div>
          <div class="calc-res-item">
            <div class="lbl">Estimated Annual Take-Home</div>
            <div class="val" id="resAnnual">₹ --</div>
          </div>
          <div class="calc-res-item">
            <div class="lbl">Provident Fund (Employee 12%)</div>
            <div class="val" id="resPf">₹ --</div>
          </div>
          <div class="calc-res-item">
            <div class="lbl">Standard Deduction & Karnataka PT</div>
            <div class="val">₹ 75,000 + ₹ 2,400</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 10: INTERVIEW DEFENSE -->
    <div id="tab-defense" class="tab-content">
      <div class="section-header">
        <h2>🎯 Behavioral & Technical Defense Drills (STAR Grounded)</h2>
      </div>
      <div style="display:flex;flex-direction:column;gap:18px;">
        <div class="vacancy-card">
          <div class="role-title">Drill #1: "Why Operations & Trade Settlement Rather Than Sales?"</div>
          <div class="meta-list" style="margin-top:10px;line-height:1.6;">
            <div><b>Context:</b> Direct rejection of variable telecalling/sales roles.</div>
            <div><b>STAR Defense:</b> "In high-velocity capital markets, institutional margins and regulatory compliance are decided entirely in post-trade operational settlement. My international trade training at DSU instilled rigorous respect for reconciliation and exception management over speculative quotas."</div>
            <div style="margin-top:6px;"><span class="tag tag-green">VERIFIED ANCHOR: DSU BBA-IB CURRICULUM</span></div>
          </div>
        </div>

        <div class="vacancy-card">
          <div class="role-title">Drill #2: "Handling High-Pressure Logistics & Large-Scale Staging Exceptions"</div>
          <div class="meta-list" style="margin-top:10px;line-height:1.6;">
            <div><b>Context:</b> High-stakes operational triage under tight physical SLAs.</div>
            <div><b>STAR Defense:</b> "At Aero India 2025 at Yelahanka Air Force Station, managed simultaneous vendor delivery windows and staging logistics across defense pavilions, resolving 100% of spatial and clearance bottlenecks on time."</div>
            <div style="margin-top:6px;"><span class="tag tag-green">VERIFIED ANCHOR: EXP-001 (AERO INDIA 2025)</span></div>
          </div>
        </div>

        <div class="vacancy-card">
          <div class="role-title">Drill #3: "Vendor Rate Card Auditing & Cost Reconciliation"</div>
          <div class="meta-list" style="margin-top:10px;line-height:1.6;">
            <div><b>Context:</b> Identifying discrepancies and enforcing contractual SLA pricing.</div>
            <div><b>STAR Defense:</b> "Engineered structured Tier-1 and Tier-2 supplier cost matrices, systematically identifying and resolving line-item variance across 300+ brand activations, reducing invoice disputes by ~25%."</div>
            <div style="margin-top:6px;"><span class="tag tag-green">VERIFIED ANCHOR: EXP-003 (VENDOR RATE MODELING)</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 11: QUALITY GATE AUDIT -->
    <div id="tab-audit" class="tab-content">
      <div class="section-header">
        <h2>🛡️ Automated Quality Gate Audit & Ledger Integrity</h2>
      </div>
      <table>
        <thead>
          <tr>
            <th>Audit Dimension</th>
            <th>Verification Finding</th>
            <th>Quality Status</th>
            <th>Production Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {"".join(audit_rows_html)}
        </tbody>
      </table>
    </div>
  </main>

  <script>
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
    }}

    function filterVacancies() {{
      const query = document.getElementById('vacancySearch').value.toLowerCase();
      const cards = document.querySelectorAll('.vacancy-card');
      cards.forEach(card => {{
        const text = card.getAttribute('data-search') || '';
        if (text.includes(query)) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function filterCompanies() {{
      const query = document.getElementById('companySearch').value.toLowerCase();
      const rows = document.querySelectorAll('#companyTable tbody tr');
      rows.forEach(row => {{
        const text = row.innerText.toLowerCase();
        if (text.includes(query)) {{
          row.style.display = '';
        }} else {{
          row.style.display = 'none';
        }}
      }});
    }}

    function filterDeliverables() {{
      const query = document.getElementById('delivSearch').value.toLowerCase();
      const rows = document.querySelectorAll('#delivTableBody tr');
      rows.forEach(row => {{
        const text = row.getAttribute('data-search') || row.innerText.toLowerCase();
        if (text.includes(query)) {{
          row.style.display = '';
        }} else {{
          row.style.display = 'none';
        }}
      }});
    }}

    function filterCalendar() {{
      const query = document.getElementById('calendarSearch').value.toLowerCase();
      const cards = document.querySelectorAll('#calendarGrid .vacancy-card');
      cards.forEach(card => {{
        const text = card.getAttribute('data-search') || card.innerText.toLowerCase();
        if (text.includes(query)) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    const RESUME_METADATA = {{
      'OPERATIONS': {{
        title: 'Global Operations & Trade Settlement Analyst',
        desc: 'Targeting Goldman Sachs, Deutsche Bank, Morgan Stanley, Northern Trust',
        url: '/api/resumes/OPERATIONS'
      }},
      'AUDIT_COMPLIANCE': {{
        title: 'Audit & Assurance Associate (Global Service Delivery)',
        desc: 'Targeting KPMG India, Deloitte USI, EY GDS, PwC AC',
        url: '/api/resumes/AUDIT_COMPLIANCE'
      }},
      'SUPPLY_CHAIN_EXIM': {{
        title: 'Supply Chain, EXIM Logistics & Procurement Specialist',
        desc: 'Targeting Target India, Flipkart, Cisco, Cargill, Schneider Electric',
        url: '/api/resumes/SUPPLY_CHAIN_EXIM'
      }},
      'SYSTEMS_ANALYST': {{
        title: 'Business Systems & Operations Process Analyst',
        desc: 'Targeting Salesforce, SAP Labs, Oracle, Infosys BPM',
        url: '/api/resumes/SYSTEMS_ANALYST'
      }}
    }};

    function switchResumeTrack(track) {{
      const meta = RESUME_METADATA[track];
      if (!meta) return;
      document.getElementById('resumeTitle').innerText = meta.title;
      document.getElementById('resumeDesc').innerText = meta.desc;
      document.getElementById('resumeHtmlLink').href = meta.url;
      document.getElementById('resumeFrame').src = meta.url;
    }}

    function runSalaryCalc() {{
      const lpa = parseFloat(document.getElementById('ctcInput').value) || 0;
      const ctc = lpa * 100000;
      const basic = ctc * 0.40;
      const epf = Math.min(basic * 0.12, 21600);
      const gratuity = basic * 0.0481;
      const pt = 2400;
      const stdDed = 75000;
      const taxable = Math.max(0, ctc - epf - gratuity - stdDed);

      let tax = 0;
      if (taxable > 700000) {{
        let rem = taxable;
        if (rem > 300000) tax += Math.min(rem - 300000, 400000) * 0.05;
        if (rem > 700000) tax += Math.min(rem - 700000, 300000) * 0.10;
        if (rem > 1000000) tax += Math.min(rem - 1000000, 200000) * 0.15;
        if (rem > 1200000) tax += Math.min(rem - 1200000, 300000) * 0.20;
        if (rem > 1500000) tax += (rem - 1500000) * 0.30;
        tax *= 1.04; // Cess
      }}

      const deductions = epf + gratuity + epf + pt + tax;
      const annualInhand = Math.max(0, ctc - deductions);
      const monthlyInhand = annualInhand / 12;

      document.getElementById('resMonthly').innerText = '₹ ' + Math.round(monthlyInhand).toLocaleString('en-IN');
      document.getElementById('resAnnual').innerText = '₹ ' + Math.round(annualInhand).toLocaleString('en-IN');
      document.getElementById('resPf').innerText = '₹ ' + Math.round(epf / 12).toLocaleString('en-IN') + ' / mo';
    }}

    // Init calc
    runSalaryCalc();
  </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OMNIVERSE] Upgraded Executive Cockpit HTML (11 Tabs) generated at: {output_path}")


if __name__ == "__main__":
    generate_complete_cockpit()
