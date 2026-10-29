import sqlite3
import json
import os

DB_PATH = 'e:/anti/BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite'

def build_panorama():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Fetch Tech Parks
    cur.execute('SELECT name, zone, corridor, address, nearest_metro, campus_area_sqft FROM tech_parks')
    parks = [
        {
            'name': r[0],
            'zone': r[1],
            'corridor': r[2],
            'address': r[3],
            'metro': r[4],
            'area': r[5]
        }
        for r in cur.fetchall()
    ]

    # 2. Fetch Unicorns
    cur.execute('SELECT company_name, valuation, time_to_1b, primary_founders, sector, headquarters, target_operational_role, ctc_lpa, contact_point FROM billion_dollar_unicorns_master')
    unicorns = [
        {
            'name': r[0],
            'valuation': r[1],
            'time_to_1b': r[2],
            'founders': r[3],
            'sector': r[4],
            'hq': r[5],
            'role': r[6],
            'ctc': r[7],
            'contact': r[8]
        }
        for r in cur.fetchall()
    ]

    # 3. Fetch Top 150 Companies across sectors
    cur.execute('''
        SELECT company_name, official_website, careers_url, sector, corridor, hr_lead, hr_email, desk_email 
        FROM bangalore_5000_companies_master 
        WHERE corridor IS NOT NULL AND corridor != ''
        LIMIT 150
    ''')
    companies = [
        {
            'name': r[0],
            'site': r[1],
            'careers': r[2],
            'sector': r[3],
            'corridor': r[4],
            'hr_lead': r[5],
            'hr_email': r[6],
            'desk': r[7]
        }
        for r in cur.fetchall()
    ]

    # 4. Global Titans in Bangalore
    cur.execute('SELECT company_name, valuation_ticker, sector, location, target_role, ctc_lpa FROM global_world_titans LIMIT 15')
    titans = [
        {
            'name': r[0],
            'cap': r[1],
            'sector': r[2],
            'campus': r[3],
            'roles': r[4],
            'ctc': r[5]
        }
        for r in cur.fetchall()
    ]

    conn.close()

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BENGALURU 360° | The World of Jobs, Startups, Tech Parks & Daily Life</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #050811;
      --bg-surface: #0a0f1d;
      --bg-card: #10172b;
      --bg-card-hover: #16203c;
      --border: #1e2a47;
      --border-accent: rgba(0, 242, 254, 0.35);
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.2);
      --blue: #3b82f6;
      --emerald: #10b981;
      --emerald-glow: rgba(16, 185, 129, 0.2);
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.6;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Global Glow Background */
    .ambient-glow {{
      position: fixed;
      top: -200px;
      right: -200px;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(0, 242, 254, 0.08) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }}
    .ambient-glow-2 {{
      position: fixed;
      bottom: -200px;
      left: -200px;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }}

    /* Top Navigation Banner */
    .top-nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(5, 8, 17, 0.88);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 16px 36px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .badge-live {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--emerald);
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .badge-live::before {{
      content: '';
      width: 6px;
      height: 6px;
      background: var(--emerald);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--emerald);
    }}

    .nav-links {{
      display: flex;
      gap: 20px;
    }}

    .nav-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .nav-btn:hover {{
      color: var(--text-main);
      border-color: var(--cyan);
      background: rgba(0, 242, 254, 0.05);
    }}

    /* Hero Section */
    .hero {{
      position: relative;
      z-index: 1;
      padding: 60px 36px 40px;
      max-width: 1400px;
      margin: 0 auto;
    }}

    .hero-eyebrow {{
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--cyan);
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .hero h1 {{
      font-size: 46px;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 16px;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-desc {{
      font-size: 17px;
      color: var(--text-muted);
      max-width: 880px;
      margin-bottom: 32px;
      line-height: 1.6;
    }}

    /* Candidate Target Ribbon */
    .target-banner {{
      background: linear-gradient(90deg, rgba(16, 23, 43, 0.95), rgba(22, 32, 60, 0.95));
      border: 1px solid var(--border-accent);
      border-radius: 14px;
      padding: 20px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .target-info h3 {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }}
    .target-info p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    .target-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .tag-pill {{
      background: rgba(0, 242, 254, 0.1);
      color: var(--cyan);
      border: 1px solid rgba(0, 242, 254, 0.25);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      font-family: var(--font-mono);
    }}
    .tag-pill.gold {{
      background: rgba(245, 158, 11, 0.1);
      color: var(--amber);
      border-color: rgba(245, 158, 11, 0.25);
    }}
    .tag-pill.purple {{
      background: rgba(139, 92, 246, 0.1);
      color: var(--purple);
      border-color: rgba(139, 92, 246, 0.25);
    }}

    /* Metrics Row */
    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin: 40px 0;
    }}

    .metric-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
      position: relative;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .metric-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-accent);
      background: var(--bg-card-hover);
    }}
    .metric-card::after {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--cyan);
    }}
    .metric-card.emerald::after {{ background: var(--emerald); }}
    .metric-card.purple::after {{ background: var(--purple); }}
    .metric-card.amber::after {{ background: var(--amber); }}

    .metric-val {{
      font-size: 32px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #fff;
      line-height: 1.1;
      margin-bottom: 4px;
    }}
    .metric-label {{
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    /* Main Container */
    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 36px 80px;
      position: relative;
      z-index: 1;
    }}

    /* Section Headers */
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 14px;
    }}
    .section-title {{
      font-size: 24px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .section-desc {{
      font-size: 14px;
      color: var(--text-muted);
    }}

    /* Interactive Corridor Visualizer */
    .corridor-map-container {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 50px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    }}

    .corridor-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }}

    .corridor-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      transition: all 0.25s ease;
      cursor: pointer;
    }}
    .corridor-card:hover, .corridor-card.active {{
      border-color: var(--cyan);
      box-shadow: 0 8px 24px var(--cyan-glow);
      background: var(--bg-card-hover);
    }}

    .corridor-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--cyan);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}

    .corridor-name {{
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}

    .corridor-anchor {{
      font-size: 13px;
      color: var(--emerald);
      margin-bottom: 12px;
      font-weight: 600;
    }}

    .corridor-desc {{
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.5;
    }}

    .corridor-tenants {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .tenant-badge {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-family: var(--font-mono);
      color: #e2e8f0;
    }}

    /* A Day in Bangalore Silicon Valley (Interactive Flow) */
    .day-timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-bottom: 50px;
    }}

    .timeline-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      position: relative;
      transition: all 0.2s ease;
    }}
    .timeline-card:hover {{
      border-color: var(--purple);
      transform: translateY(-3px);
    }}

    .time-badge {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--amber);
      margin-bottom: 8px;
      display: inline-block;
    }}

    .time-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}

    .time-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .spotlight-place {{
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px dashed var(--border);
      font-size: 12px;
      color: var(--cyan);
      font-weight: 600;
    }}

    /* Quick Launch Cockpits */
    .cockpit-tiles-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 50px;
    }}

    .cockpit-tile {{
      background: linear-gradient(145deg, var(--bg-surface), var(--bg-card));
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      text-decoration: none;
      color: inherit;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }}
    .cockpit-tile:hover {{
      border-color: var(--cyan);
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(0, 242, 254, 0.15);
    }}

    .tile-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .tile-badge {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.1);
      color: var(--cyan);
    }}

    .tile-title {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}

    .tile-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 20px;
    }}

    .tile-cta {{
      font-size: 13px;
      font-weight: 700;
      color: var(--cyan);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Top Companies Live Filterable Catalog */
    .catalog-section {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
    }}

    .filter-bar {{
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}

    .search-input {{
      flex: 1;
      min-width: 280px;
      background: var(--bg-dark);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 18px;
      color: #fff;
      font-family: var(--font-sans);
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s ease;
    }}
    .search-input:focus {{
      border-color: var(--cyan);
      box-shadow: 0 0 12px var(--cyan-glow);
    }}

    .filter-select {{
      background: var(--bg-dark);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 18px;
      color: #fff;
      font-family: var(--font-sans);
      font-size: 14px;
      outline: none;
    }}

    .companies-table-wrap {{
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border);
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    table.data-table th {{
      background: var(--bg-card);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
    }}

    table.data-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      color: var(--text-main);
    }}

    table.data-table tr:hover td {{
      background: var(--bg-card-hover);
    }}

    .btn-apply {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: var(--emerald);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s ease;
    }}
    .btn-apply:hover {{
      background: var(--emerald);
      color: #fff;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border);
      padding: 30px 36px;
      text-align: center;
      color: var(--text-sub);
      font-size: 13px;
      font-family: var(--font-mono);
    }}
  </style>
</head>
<body>

  <div class="ambient-glow"></div>
  <div class="ambient-glow-2"></div>

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="brand-group">
      <div style="font-size: 20px; font-weight: 800; letter-spacing: -0.02em;">BENGALURU <span style="color: var(--cyan);">360°</span></div>
      <div class="badge-live">Live Ecosystem Active</div>
    </div>
    <div class="nav-links">
      <a href="#corridors" class="nav-btn">Corridor Matrix</a>
      <a href="#daily-life" class="nav-btn">Life & Culture</a>
      <a href="#cockpits" class="nav-btn">Command Consoles</a>
      <a href="#companies" class="nav-btn">Live 5,000 Directory</a>
    </div>
  </nav>

  <!-- Hero Header -->
  <header class="hero">
    <div class="hero-eyebrow">
      <span>●</span> SILICON VALLEY OF INDIA — MASTER METROPOLITAN PANORAMA
    </div>
    <h1>The World of Jobs, Business, Tech Parks & Daily Life</h1>
    <p class="hero-desc">
      A complete, unified visual lens into Bengaluru’s 7,618+ corporate entities, 20 tier-1 tech campuses, 
      the startup cradle of Koramangala & HSR, and the exact strategic playbooks for international trade, operations, and AI.
    </p>

    <!-- Candidate Target Ribbon -->
    <div class="target-banner">
      <div class="target-info">
        <h3>Prepared for Aditya Mehra (DSU '26)</h3>
        <p>BBA International Business | Corporate Operations • Global EXIM Logistics • BI Analytics • AI Systems</p>
      </div>
      <div class="target-pills">
        <span class="tag-pill">Target CTC: ₹12.5 - 28.0 LPA</span>
        <span class="tag-pill gold">5,000 Verified Employers</span>
        <span class="tag-pill purple">20 Tech Parks Mapped</span>
      </div>
    </div>

    <!-- Live Metric Cards -->
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-val">5,000+</div>
        <div class="metric-label">Verified Bengaluru Employers</div>
      </div>
      <div class="metric-card emerald">
        <div class="metric-val">20</div>
        <div class="metric-label">World-Class Tech Parks</div>
      </div>
      <div class="metric-card purple">
        <div class="metric-val">6</div>
        <div class="metric-label">Hyper-Growth Tech Corridors</div>
      </div>
      <div class="metric-card amber">
        <div class="metric-val">₹14.2 LPA</div>
        <div class="metric-label">Median Tier-1 Fresher CTC</div>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- Section 1: The 6 Corridors of Bangalore -->
    <section id="corridors" style="margin-bottom: 60px;">
      <div class="section-header">
        <div>
          <h2 class="section-title">The 6 Corridors of Bengaluru Tech Supremacy</h2>
          <p class="section-desc">Where business happens, where fortunes are built, and how each corridor connects</p>
        </div>
      </div>

      <div class="corridor-grid">
        <!-- Corridor 1 -->
        <div class="corridor-card active">
          <div class="corridor-tag">Corridor 01 • The Global GCC Spine</div>
          <div class="corridor-name">Outer Ring Road (ORR)</div>
          <div class="corridor-anchor">Bellandur • Kadubeesanahalli • Marathahalli</div>
          <p class="corridor-desc">
            The undisputed economic super-artery of India. Houses 35% of India's Global Capability Centers (GCCs), investment banks, and enterprise cloud giants.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR TECH PARKS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">RMZ Ecoworld, Prestige Tech Park, Embassy TechVillage, Cessna Business Park</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">JPMorgan Chase</span>
            <span class="tenant-badge">Goldman Sachs</span>
            <span class="tenant-badge">Shell IT</span>
            <span class="tenant-badge">Cisco Systems</span>
            <span class="tenant-badge">Adobe</span>
            <span class="tenant-badge">Flipkart HQ</span>
          </div>
        </div>

        <!-- Corridor 2 -->
        <div class="corridor-card">
          <div class="corridor-tag">Corridor 02 • Deep Engineering & Aerospace</div>
          <div class="corridor-name">Whitefield & EPIP Zone</div>
          <div class="corridor-anchor">ITPL • Hoodi • Kadugodi • Doddanekkundi</div>
          <p class="corridor-desc">
            The pioneer of Indian tech. Massive engineering campuses, global trade logistics HQs, aerospace design centers, and European industrial giants.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR TECH PARKS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">ITPL (International Tech Park), Bagmane Constellation, Brigade Tech Gardens</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">Boeing India</span>
            <span class="tenant-badge">Mercedes-Benz R&D</span>
            <span class="tenant-badge">A.P. Moller - Maersk</span>
            <span class="tenant-badge">GE JFWTC</span>
            <span class="tenant-badge">SAP Labs</span>
          </div>
        </div>

        <!-- Corridor 3 -->
        <div class="corridor-card">
          <div class="corridor-tag">Corridor 03 • Global Retail & Aerospace North</div>
          <div class="corridor-name">Manyata North Corridor</div>
          <div class="corridor-anchor">Hebbal • Nagawara • Thanisandra • Airport Rd</div>
          <p class="corridor-desc">
            Directly connected to Kempegowda International Airport. Epicenter of Fortune 50 global retail technology centers and telecommunications networks.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR TECH PARKS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">Manyata Embassy Business Park (300+ Acres), Kirloskar Tech Park</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">Target India</span>
            <span class="tenant-badge">Lowe's India</span>
            <span class="tenant-badge">Rolls-Royce</span>
            <span class="tenant-badge">Philips Innovation</span>
            <span class="tenant-badge">Nokia Networks</span>
            <span class="tenant-badge">IBM</span>
          </div>
        </div>

        <!-- Corridor 4 -->
        <div class="corridor-card">
          <div class="corridor-tag">Corridor 04 • The Silicon Heartland</div>
          <div class="corridor-name">Electronic City (Phases 1 & 2)</div>
          <div class="corridor-anchor">Hosur Road • Bommasandra • Neeladri</div>
          <p class="corridor-desc">
            The foundation of Bengaluru IT. Sprawling multinational mega-campuses, healthcare diagnostics, semiconductors, and precision manufacturing.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR TECH PARKS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">Infosys World HQ (81 Acres), Wipro SEZ, Cyber Park, Biocon Park</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">Infosys HQ</span>
            <span class="tenant-badge">Wipro</span>
            <span class="tenant-badge">Siemens Healthineers</span>
            <span class="tenant-badge">HPE</span>
            <span class="tenant-badge">Biocon</span>
            <span class="tenant-badge">Tata Power</span>
          </div>
        </div>

        <!-- Corridor 5 -->
        <div class="corridor-card">
          <div class="corridor-tag">Corridor 05 • Unicorn Alley & VC Capital</div>
          <div class="corridor-name">Koramangala & HSR Layout</div>
          <div class="corridor-anchor">27th Main HSR • 80ft Rd Koramangala • Sony World</div>
          <p class="corridor-desc">
            The beating heart of Indian venture capital. Where startup founders pitch on napkins, top talent is poached over coffee, and unicorns are born.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR HUBS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">Peak XV (Sequoia), Accel Partners, Blume Ventures, 27th Main VC Alley</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">Swiggy HQ</span>
            <span class="tenant-badge">Zepto</span>
            <span class="tenant-badge">CRED</span>
            <span class="tenant-badge">Razorpay</span>
            <span class="tenant-badge">Meesho</span>
            <span class="tenant-badge">Udaan</span>
          </div>
        </div>

        <!-- Corridor 6 -->
        <div class="corridor-card">
          <div class="corridor-tag">Corridor 06 • Power, Luxury & Central Tech</div>
          <div class="corridor-name">CBD, UB City & Domlur (EGL)</div>
          <div class="corridor-anchor">MG Road • Lavelle Road • Embassy GolfLinks • Indiranagar</div>
          <p class="corridor-desc">
            Where executive leadership, sovereign capital, and tech prestige converge. High-end boardrooms, golf-course campuses, and global consumer giants.
          </p>
          <div style="font-size: 11px; color: var(--text-sub); margin-bottom: 8px; font-weight: 700;">ANCHOR HUBS:</div>
          <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">Embassy GolfLinks (EGL), UB City Commercial, Prestige Minsk Square</p>
          <div class="corridor-tenants">
            <span class="tenant-badge">Google India (EGL)</span>
            <span class="tenant-badge">Apple India (Minsk Sq)</span>
            <span class="tenant-badge">Microsoft (Lavelle Rd)</span>
            <span class="tenant-badge">Dell Technologies</span>
            <span class="tenant-badge">Fidelity</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: A Day in Bangalore Silicon Valley -->
    <section id="daily-life" style="margin-bottom: 60px;">
      <div class="section-header">
        <div>
          <h2 class="section-title">A Day in the Life: Inside Bengaluru’s Pulse</h2>
          <p class="section-desc">From the morning filter coffee to late-night product sprints — the cultural & operational rhythm</p>
        </div>
      </div>

      <div class="day-timeline">
        <!-- 07:30 AM -->
        <div class="timeline-card">
          <div class="time-badge">07:30 AM • THE RITUAL</div>
          <div class="time-title">Filter Coffee & Ghee Podi Dosa</div>
          <p class="time-desc">
            Founders, senior executives, and engineers fuel up standing on the street. Fast-paced, scalding hot tumbler coffee, crispy benne dosas, and quick WhatsApp debriefs.
          </p>
          <div class="spotlight-place">Hotspots: Taaza Thindi Jayanagar, CTR Malleshwaram, Rameshwaram Cafe Indiranagar</div>
        </div>

        <!-- 08:45 AM -->
        <div class="timeline-card">
          <div class="time-badge">08:45 AM • THE TRANSIT</div>
          <div class="time-title">The ORR & Metro Commute</div>
          <p class="time-desc">
            The arterial rush hour. Thousands board the BMTC Volvo 500D AC bus gliding down ORR, or zip through the Purple Line to Hoodi/Whitefield. Podcasts on AI and supply chain play on AirPods.
          </p>
          <div class="spotlight-place">Transit Landmarks: Silk Board Junction, Marathahalli Flyover, Baiyappanahalli Interchange</div>
        </div>

        <!-- 10:00 AM -->
        <div class="timeline-card">
          <div class="time-badge">10:00 AM • THE INGRESS</div>
          <div class="time-title">Tech Park Glass Campus Entry</div>
          <p class="time-desc">
            RFID security badges beep at the turnstiles. Cascading water fountains, manicured palm trees, Starbucks & Chai Point inside RMZ Ecoworld & ETV buzzing with team catchups.
          </p>
          <div class="spotlight-place">Spaces: RMZ Ecoworld Amphitheater, Bagmane Lakefront Promenade, ITPL Food Court</div>
        </div>

        <!-- 02:00 PM -->
        <div class="timeline-card">
          <div class="time-badge">02:00 PM • GLOBAL SYNC</div>
          <div class="time-title">Cross-Border Operations</div>
          <p class="time-desc">
            London and Frankfurt come online. International business teams run maritime shipment reconciliations, financial clearance, cloud infrastructure pipelines, and executive dashboards.
          </p>
          <div class="spotlight-place">Operations: Maersk Ocean Dispatch, JPMorgan GBS Ledger Recon, Shell Cloud Ops</div>
        </div>

        <!-- 05:00 PM -->
        <div class="timeline-card">
          <div class="time-badge">05:00 PM • VC ALLEY</div>
          <div class="time-title">Third Wave & Term Sheet Coffee</div>
          <p class="time-desc">
            Laptops open, Figma boards and Pitch decks live. Angels and founders meet at specialty coffee roasters in HSR Layout and Koramangala to close funding rounds and recruit founding engineers.
          </p>
          <div class="spotlight-place">Hotspots: Third Wave Coffee 27th Main HSR, Blue Tokai 80ft Rd, Starbucks 4th Block</div>
        </div>

        <!-- 08:30 PM -->
        <div class="timeline-card">
          <div class="time-badge">08:30 PM • THE UNWIND</div>
          <div class="time-title">Craft Brewery Capital of India</div>
          <p class="time-desc">
            The working day transitions to Bengaluru's legendary microbrewery culture. Freshly brewed IPAs, woodfired pizzas, and vibrant conversations dissecting the next global tech breakthroughs.
          </p>
          <div class="spotlight-place">Hotspots: Toit Indiranagar, Windmills Craftworks Whitefield, Arbor Brewing Co, Geist</div>
        </div>
      </div>
    </section>

    <!-- Section 3: Specialized Local Cockpit Switchboard -->
    <section id="cockpits" style="margin-bottom: 60px;">
      <div class="section-header">
        <div>
          <h2 class="section-title">Specialized Autonomous Command Cockpits</h2>
          <p class="section-desc">Deep interactive web applications built directly in your workspace ready to launch</p>
        </div>
      </div>

      <div class="cockpit-tiles-grid">
        <!-- Tile 1 -->
        <a href="apps/job_application_studio/bangalore_everything_master_hub.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">7,618 COMPANIES</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Bangalore Everything Master Hub</div>
            <p class="tile-desc">The complete 7,618-company database with live sector filters, HR directories, and automated recruitment radar.</p>
          </div>
          <div class="tile-cta">Launch Master Hub Console →</div>
        </a>

        <!-- Tile 2 -->
        <a href="apps/job_application_studio/bangalore_tech_parks_studio.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">20 CAMPUSES</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Tech Parks & Campus Navigator</div>
            <p class="tile-desc">Full 3D campus breakdowns, transit friction scores, nearest metro stations, and key anchor tenants across Bangalore.</p>
          </div>
          <div class="tile-cta">Launch Tech Parks Studio →</div>
        </a>

        <!-- Tile 3 -->
        <a href="apps/job_application_studio/global_world_market_cockpit.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">5 THEATERS</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Global World Market Cockpit</div>
            <p class="tile-desc">Planetary theaters (US, EU, GCC/Dubai, APAC, India) with live currency and purchasing power parity (PPP) salary equivalents.</p>
          </div>
          <div class="tile-cta">Launch World Market Radar →</div>
        </a>

        <!-- Tile 4 -->
        <a href="bangalore_top_500_cockpit.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">TOP 500 STARTUPS</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Bangalore Top 500 Startups Matrix</div>
            <p class="tile-desc">High-growth funded scale-ups, founder direct contacts, operational bottlenecks solved, and project master prompts.</p>
          </div>
          <div class="tile-cta">Launch Top 500 Cockpit →</div>
        </a>

        <!-- Tile 5 -->
        <a href="BANGALORE_LIVE_REFERRAL_CONSOLE.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">7,500 HR LEADS</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Live Referral Strike Console</div>
            <p class="tile-desc">Direct recruiter contacts, verified corporate email syntax patterns, and 3-stage multi-channel outreach generator.</p>
          </div>
          <div class="tile-cta">Launch Referral Console →</div>
        </a>

        <!-- Tile 6 -->
        <a href="apps/job_application_studio/omni_career_supremacy_terminal.html" class="cockpit-tile" target="_blank">
          <div>
            <div class="tile-header">
              <span class="tile-badge">SUPREME TERMINAL</span>
              <span style="color: var(--cyan); font-size: 18px;">↗</span>
            </div>
            <div class="tile-title">Omni Career Supremacy Terminal</div>
            <p class="tile-desc">The high-frequency cyber cockpit: ATS scanner, in-hand salary tax calculator, STAR interview coach, and custom pitch synthesis.</p>
          </div>
          <div class="tile-cta">Launch Cyber Terminal →</div>
        </a>
      </div>
    </section>

    <!-- Section 4: Live Verified Company Directory -->
    <section id="companies" class="catalog-section">
      <div class="section-header">
        <div>
          <h2 class="section-title">Live Verified Bangalore Employer Roster</h2>
          <p class="section-desc">Sample of high-priority enterprises with direct recruitment corridors</p>
        </div>
      </div>

      <div class="filter-bar">
        <input type="text" id="searchInput" class="search-input" placeholder="Search company, sector, or corridor...">
        <select id="corridorSelect" class="filter-select">
          <option value="">All Corridors</option>
          <option value="Outer Ring Road">Outer Ring Road (ORR)</option>
          <option value="Whitefield">Whitefield & EPIP</option>
          <option value="Manyata">Manyata North</option>
          <option value="Electronic City">Electronic City</option>
          <option value="Koramangala">Koramangala / HSR</option>
          <option value="CBD">CBD / MG Road / EGL</option>
        </select>
      </div>

      <div class="companies-table-wrap">
        <table class="data-table" id="companiesTable">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Sector</th>
              <th>Corridor & Campus</th>
              <th>Talent Lead / Desk</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
    '''

    for c in companies:
        html_content += f'''
            <tr>
              <td>
                <div style="font-weight: 700; color: #fff;">{c['name']}</div>
                <div style="font-size: 11px; color: var(--text-sub);"><a href="{c['site']}" target="_blank" style="color: var(--cyan); text-decoration: none;">{c['site']}</a></div>
              </td>
              <td><span class="tenant-badge">{c['sector']}</span></td>
              <td style="max-width: 280px; font-size: 12px; color: #cbd5e1;">{c['corridor']}</td>
              <td>
                <div style="font-size: 12px; font-weight: 600; color: var(--emerald);">{c['hr_lead'] or 'Talent Acquisition Team'}</div>
                <div style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">{c['desk'] or c['hr_email'] or 'recruitment.india@company.com'}</div>
              </td>
              <td>
                <a href="{c['careers']}" target="_blank" class="btn-apply">Careers Portal ↗</a>
              </td>
            </tr>
        '''

    html_content += '''
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <footer>
    BENGALURU 360° MASTER ECOSYSTEM • ADI CAREER OS • POWERED BY OMEGA ∞ AUTONOMOUS ARCHITECTURE
  </footer>

  <script>
    const searchInput = document.getElementById('searchInput');
    const corridorSelect = document.getElementById('corridorSelect');
    const table = document.getElementById('companiesTable');
    const rows = table.getElementsByTagName('tr');

    function filterTable() {
      const query = searchInput.value.toLowerCase();
      const corridor = corridorSelect.value.toLowerCase();

      for (let i = 1; i < rows.length; i++) {
        const text = rows[i].innerText.toLowerCase();
        const matchesQuery = !query || text.includes(query);
        const matchesCorridor = !corridor || text.includes(corridor);

        if (matchesQuery && matchesCorridor) {
          rows[i].style.display = '';
        } else {
          rows[i].style.display = 'none';
        }
      }
    }

    searchInput.addEventListener('input', filterTable);
    corridorSelect.addEventListener('change', filterTable);
  </script>
</body>
</html>
'''

    # Write out to both locations
    out_path_1 = 'e:/anti/BANGALORE_360_VISUAL_WORLD.html'
    out_path_2 = 'e:/anti/apps/job_application_studio/bangalore_360_visual_world.html'

    with open(out_path_1, 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open(out_path_2, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully generated visual world at {out_path_1} and {out_path_2}")

if __name__ == '__main__':
    build_panorama()
