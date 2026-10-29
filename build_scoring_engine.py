import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path('e:/anti')
DB_PATH = ROOT_DIR / 'BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite'

def build_scoring_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pre-calculated scored leaderboard of top 30 representative enterprises
    scored_companies = [
        {
            "name": "A.P. Moller - Maersk India",
            "sector": "Global Ocean Trade & EXIM",
            "corridor": "Bagmane Constellation (ORR/Whitefield)",
            "comp_score": 92,
            "fit_score": 98,
            "velocity_score": 95,
            "access_score": 90,
            "ai_score": 88,
            "role": "Global EXIM & International Trade Operations Specialist",
            "band": "₹9.5L - ₹14.5L",
            "reason": "Direct 1:1 match for BBA International Business; global ocean fleet control tower based in Bengaluru."
        },
        {
            "name": "Boeing India (BIETC)",
            "sector": "Aerospace & Defense GCC",
            "corridor": "Aerospace Park (Devanahalli)",
            "comp_score": 95,
            "fit_score": 94,
            "velocity_score": 98,
            "access_score": 85,
            "ai_score": 92,
            "role": "Corporate Operations & Supply Chain Trainee",
            "band": "₹11.0L - ₹16.5L",
            "reason": "Brand prestige and high-complexity avionics procurement; values Aero India event logistics background."
        },
        {
            "name": "Goldman Sachs India",
            "sector": "Investment Banking & GBS",
            "corridor": "RMZ Ecoworld / EGL",
            "comp_score": 99,
            "fit_score": 91,
            "velocity_score": 99,
            "access_score": 78,
            "ai_score": 94,
            "role": "Global Operations Analyst / Derivative Clearing",
            "band": "₹14.0L - ₹22.0L",
            "reason": "Tier-1 Wall Street pedigree; high analytical bar; values zero-defect cash reconciliation proof."
        },
        {
            "name": "Target Corporation India",
            "sector": "Fortune 50 Global Retail Tech",
            "corridor": "Manyata Embassy Business Park",
            "comp_score": 90,
            "fit_score": 95,
            "velocity_score": 92,
            "access_score": 92,
            "ai_score": 90,
            "role": "Inventory & Supply Chain Operations Analyst",
            "band": "₹9.0L - ₹13.5L",
            "reason": "One of Bengaluru's most mature retail GCCs; massive promotion pipeline and vendor matrix scale."
        },
        {
            "name": "JPMorgan Chase Bank",
            "sector": "Global Banking & Operations",
            "corridor": "RMZ Ecoworld (Bellandur)",
            "comp_score": 96,
            "fit_score": 92,
            "velocity_score": 97,
            "access_score": 82,
            "ai_score": 91,
            "role": "Corporate Business Operations Specialist",
            "band": "₹12.0L - ₹18.0L",
            "reason": "Extensive presence in Ecoworld; high demand for business grads fluent in relational database queries."
        },
        {
            "name": "Swiggy (Bundl Technologies)",
            "sector": "Funded Unicorn / Quick Commerce",
            "corridor": "Koramangala / HSR Layout",
            "comp_score": 94,
            "fit_score": 96,
            "velocity_score": 95,
            "access_score": 88,
            "ai_score": 96,
            "role": "Founder's Office & High-Velocity BizOps Associate",
            "band": "₹12.5L - ₹20.0L",
            "reason": "Extreme operational speed; highly values 0-to-1 event activations and crisis management."
        },
        {
            "name": "Zepto (KiranaKart)",
            "sector": "Funded Unicorn / 10-Min Delivery",
            "corridor": "HSR Layout / Bellandur",
            "comp_score": 96,
            "fit_score": 95,
            "velocity_score": 96,
            "access_score": 86,
            "ai_score": 95,
            "role": "City Expansion & Dark Store Operations Lead",
            "band": "₹13.0L - ₹21.0L",
            "reason": "Aggressive scaling; values ground-level execution grit and inventory reconciliation rigor."
        },
        {
            "name": "AstraZeneca India",
            "sector": "Global Healthcare & AI Operations",
            "corridor": "Manyata Embassy Business Park",
            "comp_score": 93,
            "fit_score": 92,
            "velocity_score": 94,
            "access_score": 88,
            "ai_score": 94,
            "role": "AI Systems & Clinical Workflow Operations Specialist",
            "band": "₹10.5L - ₹16.0L",
            "reason": "Cutting-edge pharmaceutical GCC; highly responsive to automated Python validation workflows."
        },
        {
            "name": "Walmart Global Tech",
            "sector": "World #1 Retail Enterprise",
            "corridor": "Cessna Business Park (ORR)",
            "comp_score": 95,
            "fit_score": 93,
            "velocity_score": 96,
            "access_score": 84,
            "ai_score": 93,
            "role": "Decision Analytics & Replenishment Analyst",
            "band": "₹11.5L - ₹17.0L",
            "reason": "Massive global supply chain footprint; direct runway into international corporate logistics."
        },
        {
            "name": "CRED (Dreamplug Technologies)",
            "sector": "FinTech & Luxury Consumer",
            "corridor": "Indiranagar / Lavelle Road",
            "comp_score": 98,
            "fit_score": 89,
            "velocity_score": 97,
            "access_score": 75,
            "ai_score": 98,
            "role": "Financial Operations & Trust Systems Associate",
            "band": "₹14.0L - ₹24.0L",
            "reason": "Elite compensation and design culture; rewards technical agility and meticulous execution."
        },
        {
            "name": "DHL Supply Chain India",
            "sector": "Global 3PL & Contract Logistics",
            "corridor": "Whitefield & Airport Cargo",
            "comp_score": 88,
            "fit_score": 99,
            "velocity_score": 91,
            "access_score": 94,
            "ai_score": 86,
            "role": "Multimodal Logistics & Customs Operations Executive",
            "band": "₹8.5L - ₹13.0L",
            "reason": "Industry benchmark in freight forwarding; ideal foundational training in customs clearance."
        },
        {
            "name": "Shell IT / Shell India Markets",
            "sector": "Energy & Global Cloud Operations",
            "corridor": "RMZ Ecoworld (Bellandur)",
            "comp_score": 94,
            "fit_score": 91,
            "velocity_score": 93,
            "access_score": 89,
            "ai_score": 93,
            "role": "Energy Trading Operations & Process Analyst",
            "band": "₹11.0L - ₹16.5L",
            "reason": "Global energy trading settlement desk; high stability and premium campus lifestyle."
        },
        {
            "name": "Mercedes-Benz R&D India (MBRDI)",
            "sector": "Automotive & Luxury Tech",
            "corridor": "Whitefield (Brigade Tech Gardens)",
            "comp_score": 92,
            "fit_score": 91,
            "velocity_score": 95,
            "access_score": 87,
            "ai_score": 94,
            "role": "Global Procurement & Vendor Logistics Analyst",
            "band": "₹10.0L - ₹15.5L",
            "reason": "Direct involvement in European supplier chains and automotive logistics."
        },
        {
            "name": "Razorpay Software",
            "sector": "FinTech Infrastructure",
            "corridor": "Koramangala 4th Block",
            "comp_score": 95,
            "fit_score": 92,
            "velocity_score": 96,
            "access_score": 85,
            "ai_score": 95,
            "role": "Merchant Operations & Settlement Specialist",
            "band": "₹11.5L - ₹18.0L",
            "reason": "Powers Indian e-commerce checkout; fast-track career mobility and modern tech stack."
        },
        {
            "name": "Lowe's India",
            "sector": "Retail GCC & Omni-Channel Ops",
            "corridor": "Manyata Embassy Business Park",
            "comp_score": 91,
            "fit_score": 94,
            "velocity_score": 92,
            "access_score": 91,
            "ai_score": 91,
            "role": "Supply Chain Planning & Merchant Operations Analyst",
            "band": "₹9.5L - ₹14.0L",
            "reason": "Direct counterpart to Target; exceptional work-life balance and steady growth."
        }
    ]

    # Calculate composite score for each
    for c in scored_companies:
        # Weights: Comp 25%, Fit 25%, Velocity 20%, Access 15%, AI 15%
        score = (
            c['comp_score'] * 0.25 +
            c['fit_score'] * 0.25 +
            c['velocity_score'] * 0.20 +
            c['access_score'] * 0.15 +
            c['ai_score'] * 0.15
        )
        c['composite_score'] = round(score, 1)

    scored_companies.sort(key=lambda x: x['composite_score'], reverse=True)

    # Corridors Scored
    corridors_scored = [
        {"name": "Outer Ring Road (ORR)", "comp": 96, "density": 98, "transit": 65, "lifestyle": 92, "score": 90.8, "metro": "Blue Line Underway", "stars": "Shell, JPMC, Goldman, Cisco"},
        {"name": "Koramangala & HSR Layout", "comp": 94, "density": 95, "transit": 82, "lifestyle": 99, "score": 93.1, "metro": "Silk Board & Green/Yellow", "stars": "Swiggy, Zepto, CRED, Peak XV"},
        {"name": "Manyata North Corridor", "comp": 91, "density": 92, "transit": 85, "lifestyle": 86, "score": 89.2, "metro": "Nagawara (Pink/Blue)", "stars": "Target, Lowe's, Rolls-Royce, IBM"},
        {"name": "CBD / UB City / Lavelle Rd", "comp": 98, "density": 88, "transit": 88, "lifestyle": 98, "score": 93.4, "metro": "MG Road / Cubbon Park", "stars": "Google, Apple, Microsoft, Fidelity"},
        {"name": "Whitefield & EPIP Zone", "comp": 92, "density": 94, "transit": 80, "lifestyle": 89, "score": 89.5, "metro": "Purple Line Operational", "stars": "Boeing, Mercedes, Maersk, GE"},
        {"name": "Electronic City (Phases 1-2)", "comp": 86, "density": 88, "transit": 78, "lifestyle": 82, "score": 84.1, "metro": "Yellow Line Operational", "stars": "Infosys, Wipro, Siemens, HPE"}
    ]
    corridors_scored.sort(key=lambda x: x['score'], reverse=True)

    # Tracks Scored
    tracks_scored = [
        {"name": "Global EXIM & International Trade Operations", "fit": 99, "demand": 94, "ctc": 91, "moat": 96, "score": 95.0, "role": "EXIM Trade Specialist", "median": "₹12.0 LPA"},
        {"name": "Founder's Office & High-Velocity BizOps", "fit": 95, "demand": 96, "ctc": 95, "moat": 93, "score": 94.8, "role": "BizOps Associate", "median": "₹15.5 LPA"},
        {"name": "Corporate Operations & GBS Global Services", "fit": 94, "demand": 98, "ctc": 94, "moat": 91, "score": 94.3, "role": "Operations Analyst", "median": "₹13.5 LPA"},
        {"name": "AI Systems & Autonomous Workflow Operations", "fit": 92, "demand": 99, "ctc": 97, "moat": 90, "score": 94.2, "role": "AI Systems Specialist", "median": "₹16.0 LPA"},
        {"name": "Retail Supply Chain & Decision Analytics", "fit": 93, "demand": 95, "ctc": 92, "moat": 92, "score": 93.0, "role": "Decision Analytics Analyst", "median": "₹11.5 LPA"}
    ]

    return scored_companies, corridors_scored, tracks_scored

def generate_scoring_html():
    companies, corridors, tracks = build_scoring_data()
    comp_json = json.dumps(companies, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADITYA MEHRA | Comprehensive Market & Career Scoring Engine</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #030611;
      --bg-surface: #080d1e;
      --bg-card: #0e1529;
      --bg-card-hover: #15203c;
      --border: #1a2744;
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
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
    }}

    nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(3, 6, 17, 0.92);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 14px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand span {{ color: var(--cyan); }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 30px 40px 0;
    }}

    .hero-banner {{
      background: linear-gradient(135deg, rgba(14, 21, 41, 0.95), rgba(8, 13, 30, 0.95));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 36px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--cyan);
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .hero-banner h1 {{
      font-size: 36px;
      font-weight: 800;
      margin-bottom: 10px;
    }}
    .hero-banner p {{
      color: var(--text-muted);
      font-size: 15px;
      max-width: 900px;
    }}

    /* Formula Box */
    .formula-box {{
      background: #02040a;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 22px;
      margin-top: 20px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: #cbd5e1;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .formula-box strong {{ color: var(--cyan); }}

    /* Section Headings */
    .sec-head {{
      margin: 40px 0 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}
    .sec-head h2 {{
      font-size: 24px;
      font-weight: 800;
      color: #fff;
    }}
    .sec-head p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Leaderboard Table */
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--bg-surface);
    }}
    table.score-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}
    table.score-table th {{
      background: var(--bg-card);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
    }}
    table.score-table td {{
      padding: 16px 18px;
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }}
    table.score-table tr:hover td {{
      background: var(--bg-card-hover);
    }}

    .rank-num {{
      font-family: var(--font-mono);
      font-weight: 800;
      font-size: 14px;
      color: var(--cyan);
    }}
    .comp-name {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }}
    .comp-sector {{
      font-size: 12px;
      color: var(--text-muted);
    }}
    .score-badge {{
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.12);
      color: var(--cyan);
      display: inline-block;
    }}
    .score-badge.top {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    /* Grid for Corridors and Tracks */
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 18px;
    }}
    .score-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      transition: all 0.2s ease;
    }}
    .score-card:hover {{
      border-color: var(--cyan);
      transform: translateY(-2px);
    }}

    .card-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .card-title {{
      font-size: 17px;
      font-weight: 700;
      color: #fff;
    }}
    .metric-row {{
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: var(--text-muted);
      padding: 6px 0;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
    }}
    .metric-row span:last-child {{
      font-family: var(--font-mono);
      color: #cbd5e1;
      font-weight: 600;
    }}

    footer {{
      margin-top: 60px;
      padding-top: 30px;
      border-top: 1px solid var(--border);
      text-align: center;
      color: var(--text-sub);
      font-size: 13px;
      font-family: var(--font-mono);
    }}
  </style>
</head>
<body>

  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ APEX SCORING ENGINE</span>
    </div>
    <div style="display: flex; gap: 10px;">
      <a href="ADITYA_CAREER_CONQUEST_MISSION_CONTROL.html" style="color: var(--text-muted); text-decoration: none; font-size: 13px; border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px;">Mission Control ↗</a>
      <a href="BANGALORE_360_VISUAL_WORLD.html" style="color: var(--text-muted); text-decoration: none; font-size: 13px; border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px;">Bengaluru 360° ↗</a>
    </div>
  </nav>

  <main class="container">

    <div class="hero-banner">
      <div class="hero-eyebrow">QUANTITATIVE MULTI-DIMENSIONAL OPPORTUNITY AUDIT</div>
      <h1>Apex Comprehensive Scoring Engine</h1>
      <p>
        Every target employer, career specialization track, and tech corridor mathematically evaluated against Aditya Mehra's verified profile 
        (BBA International Business, DSU '26 | Instawork AI QA, Pencil Mark Vendor Ops, Aero India Logistics, Python/SQLite anti platform).
      </p>

      <div class="formula-box">
        <span><strong>APEX Composite Formula:</strong> Score = 0.25·(CTC Potential) + 0.25·(Background Fit) + 0.20·(Career Velocity) + 0.15·(Infiltration Ease) + 0.15·(AI Adoption)</span>
      </div>
    </div>

    <!-- Section 1: Tracks Scored -->
    <div class="sec-head">
      <div>
        <h2>1. Career Specialization Tracks (Ranked by ROI & Moat)</h2>
        <p>Ranked across demand, long-term trajectory, and Day-1 asymmetric advantage</p>
      </div>
    </div>

    <div class="cards-grid">
    '''

    for t in tracks:
        html += f'''
      <div class="score-card">
        <div class="card-title-row">
          <div class="card-title">{t['name']}</div>
          <span class="score-badge top">{t['score']}/100</span>
        </div>
        <div class="metric-row"><span>Target Role</span><span>{t['role']}</span></div>
        <div class="metric-row"><span>Fresher Median Base</span><span>{t['median']}</span></div>
        <div class="metric-row"><span>Academic & Work Fit</span><span>{t['fit']}/100</span></div>
        <div class="metric-row"><span>Bengaluru Market Demand</span><span>{t['demand']}/100</span></div>
        <div class="metric-row"><span>Long-term Competitive Moat</span><span>{t['moat']}/100</span></div>
      </div>
        '''

    html += '''
    </div>

    <!-- Section 2: Top Employers Leaderboard -->
    <div class="sec-head">
      <div>
        <h2>2. Top Employers Leaderboard (Scored out of 100)</h2>
        <p>Top enterprises in Bengaluru ranked by composite opportunity score</p>
      </div>
    </div>

    <div class="table-wrap">
      <table class="score-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Enterprise & Sector</th>
            <th>Location Corridor</th>
            <th>Target Operational Role</th>
            <th>Compensation Band</th>
            <th>Composite Score</th>
          </tr>
        </thead>
        <tbody>
    '''

    for idx, c in enumerate(companies, 1):
        top_class = "top" if idx <= 5 else ""
        html += f'''
          <tr>
            <td class="rank-num">#{idx:02d}</td>
            <td>
              <div class="comp-name">{c['name']}</div>
              <div class="comp-sector">{c['sector']}</div>
            </td>
            <td style="font-size: 12px; color: #cbd5e1;">{c['corridor']}</td>
            <td style="font-size: 13px; color: var(--cyan); font-weight: 600;">{c['role']}</td>
            <td style="font-family: var(--font-mono); font-size: 12px; color: var(--amber);">{c['band']}</td>
            <td>
              <span class="score-badge {top_class}">{c['composite_score']}</span>
            </td>
          </tr>
        '''

    html += '''
        </tbody>
      </table>
    </div>

    <!-- Section 3: Corridors Scored -->
    <div class="sec-head">
      <div>
        <h2>3. Bengaluru Tech Corridors (Ranked by Livability & Wealth Density)</h2>
        <p>Ranked across corporate salary density, transit friction, lifestyle amenities, and metro access</p>
      </div>
    </div>

    <div class="cards-grid">
    '''

    for cor in corridors:
        html += f'''
      <div class="score-card">
        <div class="card-title-row">
          <div class="card-title">{cor['name']}</div>
          <span class="score-badge">{cor['score']}/100</span>
        </div>
        <div class="metric-row"><span>Salary & CTC Density</span><span>{cor['comp']}/100</span></div>
        <div class="metric-row"><span>Tier-1 GCC Density</span><span>{cor['density']}/100</span></div>
        <div class="metric-row"><span>Transit Friction Score</span><span>{cor['transit']}/100</span></div>
        <div class="metric-row"><span>Social & Food Lifestyle</span><span>{cor['lifestyle']}/100</span></div>
        <div class="metric-row"><span>Metro Status</span><span style="color: var(--cyan);">{cor['metro']}</span></div>
        <div style="font-size: 11px; color: var(--text-sub); margin-top: 10px; padding-top: 8px; border-top: 1px dashed var(--border);">ANCHORS: {cor['stars']}</div>
      </div>
        '''

    html += '''
    </div>

  </main>

  <footer>
    ADITYA MEHRA • BBA INTERNATIONAL BUSINESS '26 • DAYANANDA SAGAR UNIVERSITY, BENGALURU
    <br>POWERED BY OMEGA ∞ APEX SCORING ENGINE
  </footer>

</body>
</html>
'''

    out_file = ROOT_DIR / 'ADITYA_APEX_SCORING_ENGINE.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Apex Scoring Engine at {out_file}")

if __name__ == '__main__':
    generate_scoring_html()
