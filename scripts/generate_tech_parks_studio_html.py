#!/usr/bin/env python3
"""
generate_tech_parks_studio_html.py

Generates the interactive, ultra-fast Bangalore Tech Parks & Campus Navigator Web Studio.
Zero CORS issues (inlined JSON data), responsive modern UI, instant search, Metro line filters,
and 1-click email / clipboard application dispatchers.
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TECH_PARKS_JSON = DATA_DIR / "bangalore_tech_parks_master.json"
HTML_OUT = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_tech_parks_studio.html"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore Tech Parks & Campus Navigator | ADI CAREER OS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0e17;
      --bg-secondary: #111827;
      --bg-card: #162032;
      --bg-card-hover: #1c2a42;
      --accent-cyan: #00f2fe;
      --accent-blue: #4facfe;
      --accent-green: #10b981;
      --accent-purple: #8b5cf6;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --text-primary: #f3f4f6;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;
      --border-color: #1f293d;
      --border-highlight: rgba(0, 242, 254, 0.3);
      --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-family: var(--font-main);
      line-height: 1.5;
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Navigation */
    .top-nav {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #000;
      font-weight: 900;
      font-size: 16px;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-title {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .brand-sub {
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .nav-links {
      display: flex;
      gap: 10px;
    }
    .nav-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .nav-btn:hover {
      background: var(--bg-card-hover);
      color: var(--text-primary);
      border-color: var(--accent-cyan);
    }
    .nav-btn.primary {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #000;
      border: none;
    }

    /* Hero Section */
    .hero {
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 24px 20px;
    }
    .hero-tag {
      display: inline-block;
      background: rgba(0, 242, 254, 0.1);
      border: 1px solid rgba(0, 242, 254, 0.3);
      color: var(--accent-cyan);
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 20px;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .hero-title {
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 8px;
      background: linear-gradient(135deg, #ffffff 40%, var(--accent-cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      color: var(--text-secondary);
      font-size: 14px;
      max-width: 900px;
      margin-bottom: 20px;
    }

    /* Metric Bar */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 28px;
    }
    .metric-box {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .metric-val {
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
    }
    .metric-label {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }

    /* Filter Controls */
    .controls-panel {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .search-row {
      display: flex;
      gap: 12px;
    }
    .search-input {
      flex: 1;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px 18px;
      color: #fff;
      font-size: 14px;
      font-family: var(--font-main);
      outline: none;
      transition: all 0.2s ease;
    }
    .search-input:focus {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.2);
    }
    .pill-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }
    .pill-label {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-right: 4px;
    }
    .filter-pill {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }
    .filter-pill:hover {
      background: var(--bg-card-hover);
      color: var(--text-primary);
    }
    .filter-pill.active {
      background: var(--accent-cyan);
      color: #000;
      border-color: var(--accent-cyan);
      font-weight: 700;
    }

    /* Main Content Layout */
    .content-grid {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 24px;
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 24px;
    }
    @media (max-width: 1024px) {
      .content-grid { grid-template-columns: 1fr; }
    }

    /* Tech Park Sidebar List */
    .park-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: calc(100vh - 200px);
      overflow-y: auto;
      padding-right: 6px;
    }
    .park-list::-webkit-scrollbar { width: 6px; }
    .park-list::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }

    .park-card {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
    }
    .park-card:hover {
      background: var(--bg-card);
      border-color: rgba(0, 242, 254, 0.4);
      transform: translateY(-1px);
    }
    .park-card.active {
      background: var(--bg-card);
      border-color: var(--accent-cyan);
      box-shadow: 0 0 16px rgba(0, 242, 254, 0.15);
    }
    .park-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 6px;
    }
    .park-id {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-cyan);
      background: rgba(0, 242, 254, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
    }
    .park-friction {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .friction-low { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .friction-med { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
    .friction-high { background: rgba(244, 63, 94, 0.15); color: #f43f5e; }

    .park-name {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
      line-height: 1.3;
    }
    .park-corridor {
      font-size: 11px;
      color: var(--text-secondary);
      margin-bottom: 8px;
    }
    .park-stats-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      border-top: 1px solid var(--border-color);
      padding-top: 8px;
    }

    /* Companies Panel */
    .companies-view {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .active-park-banner {
      background: linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(22, 32, 50, 0.95));
      border: 1px solid var(--border-highlight);
      border-radius: 12px;
      padding: 20px 24px;
    }
    .banner-title {
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }
    .banner-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 12px;
      color: var(--text-secondary);
      margin-bottom: 12px;
    }
    .banner-meta span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .amenities-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .amenity-pill {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-secondary);
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
    }

    /* Company Cards */
    .company-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 20px;
      transition: all 0.2s ease;
      position: relative;
    }
    .company-card:hover {
      border-color: rgba(0, 242, 254, 0.4);
      background: var(--bg-card-hover);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }
    .comp-name {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
    }
    .comp-sector {
      font-size: 12px;
      color: var(--accent-cyan);
      margin-top: 2px;
      font-weight: 500;
    }
    .salary-badge {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #10b981;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      white-space: nowrap;
    }
    .role-banner {
      background: rgba(0, 0, 0, 0.3);
      border-left: 3px solid var(--accent-cyan);
      border-radius: 4px;
      padding: 10px 14px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .role-title {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
    }
    .role-exp {
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    .contact-details {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      font-size: 12px;
      margin-bottom: 16px;
      background: var(--bg-secondary);
      padding: 12px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }
    .contact-item {
      display: flex;
      flex-direction: column;
    }
    .contact-label {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 2px;
    }
    .contact-value {
      color: #fff;
      font-weight: 600;
      font-family: var(--font-mono);
      word-break: break-all;
    }

    /* Action Buttons */
    .card-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .action-btn {
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
    }
    .action-btn.send-mail {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #000;
      font-weight: 700;
      border: none;
    }
    .action-btn.send-mail:hover {
      box-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
      transform: translateY(-1px);
    }
    .action-btn.copy-pitch {
      background: var(--bg-card);
      color: var(--text-primary);
    }
    .action-btn.copy-pitch:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-cyan);
    }
    .action-btn.linkedin {
      background: #0077b5;
      color: #fff;
      border: none;
    }
    .action-btn.linkedin:hover {
      background: #006097;
    }
    .action-btn.careers {
      background: var(--bg-card);
      color: var(--text-primary);
    }
    .action-btn.careers:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-purple);
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-card);
      border: 1px solid var(--accent-cyan);
      color: #fff;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1000;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <header class="top-nav">
    <div class="brand">
      <div class="brand-icon">TP</div>
      <div>
        <div class="brand-title">Bangalore Tech Parks Navigator</div>
        <div class="brand-sub">ADI CAREER OS • 20 CAMPUSES • 72 EMPLOYERS</div>
      </div>
    </div>
    <div class="nav-links">
      <a href="http://localhost:9119/apps/job_application_studio/bangalore_non_stop_outreach_studio.html" class="nav-btn">⚡ 4,500 Blitz Studio</a>
      <a href="http://localhost:9119/apps/get_me_hired_dashboard/index.html" class="nav-btn">📊 Master Dashboard</a>
      <a href="http://localhost:9119/apps/index.html" class="nav-btn">🌐 Master Hub</a>
      <a href="#" class="nav-btn primary" onclick="exportFilteredCSV()">📥 Export Directory CSV</a>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-tag">Verified Campus & SEZ Directory • Namma Metro Aligned</div>
    <h1 class="hero-title">Bangalore Tech Parks & Campus Directory</h1>
    <p class="hero-desc">
      Explore all 20 premier Bangalore Tech Parks and SEZs housing India's top GCCs, MNCs, and Tech Unicorns.
      Target 100% verified non-sales operations roles (Operations Analyst, Supply Chain Associate, EXIM Coordinator)
      with direct HR emails, desk phone lines, and 1-click personalized application dispatches.
    </p>

    <!-- Metrics -->
    <div class="metric-grid">
      <div class="metric-box">
        <div>
          <div class="metric-val" id="metricParks">20</div>
          <div class="metric-label">Premier Tech Parks</div>
        </div>
      </div>
      <div class="metric-box">
        <div>
          <div class="metric-val" id="metricCompanies">72</div>
          <div class="metric-label">Marquee Employers</div>
        </div>
      </div>
      <div class="metric-box">
        <div>
          <div class="metric-val">100%</div>
          <div class="metric-label">Non-Sales Operations</div>
        </div>
      </div>
      <div class="metric-box">
        <div>
          <div class="metric-val">0.0</div>
          <div class="metric-label">CGPA Leakage (Omitted)</div>
        </div>
      </div>
      <div class="metric-box">
        <div>
          <div class="metric-val" id="metricContacted">0 / 72</div>
          <div class="metric-label">Contacted Progress</div>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="controls-panel">
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Instant search across tech parks, companies, roles, or HR leads... (e.g. Cisco, Manyata, Whitefield, SCM)" oninput="filterData()">
      </div>

      <!-- Zone Filter Pills -->
      <div class="pill-group">
        <span class="pill-label">Zone:</span>
        <button class="filter-pill active" onclick="setZoneFilter('all', this)">All Zones</button>
        <button class="filter-pill" onclick="setZoneFilter('Outer Ring Road', this)">Outer Ring Road (ORR)</button>
        <button class="filter-pill" onclick="setZoneFilter('Whitefield', this)">Whitefield & ITPL</button>
        <button class="filter-pill" onclick="setZoneFilter('Electronic City', this)">Electronic City (Ph 1 & 2)</button>
        <button class="filter-pill" onclick="setZoneFilter('North Bangalore', this)">North Bangalore (Manyata)</button>
        <button class="filter-pill" onclick="setZoneFilter('South Bangalore', this)">South Bangalore (Bannerghatta/JP Nagar)</button>
        <button class="filter-pill" onclick="setZoneFilter('Central', this)">Central / EGL / Indiranagar</button>
        <button class="filter-pill" onclick="setZoneFilter('West Bangalore', this)">West Bangalore (Global Village)</button>
      </div>

      <!-- Metro Line Pills -->
      <div class="pill-group">
        <span class="pill-label">Namma Metro Line:</span>
        <button class="filter-pill active" onclick="setMetroFilter('all', this)">All Metro Lines</button>
        <button class="filter-pill" onclick="setMetroFilter('Purple', this)">🟣 Purple Line (Whitefield - Kengeri)</button>
        <button class="filter-pill" onclick="setMetroFilter('Yellow', this)">🟡 Yellow Line (Electronic City / Bommasandra)</button>
        <button class="filter-pill" onclick="setMetroFilter('Blue', this)">🔵 Blue Line (ORR / Kadubeesanahalli / Nagawara)</button>
        <button class="filter-pill" onclick="setMetroFilter('Pink', this)">🌸 Pink Line (Dairy Circle / Jayadeva / Nagawara)</button>
      </div>
    </div>
  </section>

  <!-- Main Split Layout -->
  <main class="content-grid">
    <!-- Left Sidebar: Tech Parks List -->
    <aside class="park-list" id="parkListContainer">
      <!-- Injected via JS -->
    </aside>

    <!-- Right Side: Active Park Companies & Details -->
    <section class="companies-view" id="companiesViewContainer">
      <!-- Injected via JS -->
    </section>
  </main>

  <div id="toast" class="toast">Action completed!</div>

  <!-- Raw Master Data Inlined -->
  <script>
    const TECH_PARKS = __TECH_PARKS_JSON_DATA__;

    let activeParkId = TECH_PARKS[0].id;
    let currentZoneFilter = 'all';
    let currentMetroFilter = 'all';
    let searchQuery = '';

    // Contacted tracking in localStorage
    const STORAGE_KEY = 'adi_contacted_techpark_companies';
    let contactedCompanies = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');

    function updateContactedMetric() {
      const total = TECH_PARKS.reduce((acc, p) => acc + p.companies.length, 0);
      document.getElementById('metricContacted').innerText = `${contactedCompanies.length} / ${total}`;
    }

    function toggleContacted(companyName) {
      if (contactedCompanies.includes(companyName)) {
        contactedCompanies = contactedCompanies.filter(c => c !== companyName);
        showToast(`Marked ${companyName} as not contacted`);
      } else {
        contactedCompanies.push(companyName);
        showToast(`Marked ${companyName} as CONTACTED!`);
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(contactedCompanies));
      updateContactedMetric();
      renderCompaniesView();
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2400);
    }

    function copyToClipboard(text, label) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied ${label} to clipboard!`);
      });
    }

    function selectPark(id) {
      activeParkId = id;
      renderParkList();
      renderCompaniesView();
    }

    function setZoneFilter(zone, btn) {
      currentZoneFilter = zone;
      document.querySelectorAll('.pill-group:nth-of-type(1) .filter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      filterData();
    }

    function setMetroFilter(metro, btn) {
      currentMetroFilter = metro;
      document.querySelectorAll('.pill-group:nth-of-type(2) .filter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      filterData();
    }

    function filterData() {
      searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
      renderParkList();
      renderCompaniesView();
    }

    function getFilteredParks() {
      return TECH_PARKS.filter(p => {
        // Zone Match
        let matchZone = true;
        if (currentZoneFilter !== 'all') {
          matchZone = p.zone.toLowerCase().includes(currentZoneFilter.toLowerCase()) || 
                      p.corridor.toLowerCase().includes(currentZoneFilter.toLowerCase());
        }

        // Metro Match
        let matchMetro = true;
        if (currentMetroFilter !== 'all') {
          matchMetro = p.nearest_metro.toLowerCase().includes(currentMetroFilter.toLowerCase());
        }

        // Search Query
        let matchSearch = true;
        if (searchQuery) {
          const inPark = p.name.toLowerCase().includes(searchQuery) ||
                         p.address.toLowerCase().includes(searchQuery) ||
                         p.corridor.toLowerCase().includes(searchQuery);
          const inCompanies = p.companies.some(c => 
            c.company_name.toLowerCase().includes(searchQuery) ||
            c.target_role.toLowerCase().includes(searchQuery) ||
            c.sector.toLowerCase().includes(searchQuery) ||
            c.hr_name.toLowerCase().includes(searchQuery)
          );
          matchSearch = inPark || inCompanies;
        }

        return matchZone && matchMetro && matchSearch;
      });
    }

    function renderParkList() {
      const container = document.getElementById('parkListContainer');
      const filtered = getFilteredParks();

      if (filtered.length === 0) {
        container.innerHTML = `<div style="padding: 20px; color: var(--text-muted); font-size: 13px;">No tech parks match current filters.</div>`;
        return;
      }

      // If active park not in filtered, set first
      if (!filtered.some(p => p.id === activeParkId)) {
        activeParkId = filtered[0].id;
      }

      container.innerHTML = filtered.map(p => {
        const isActive = p.id === activeParkId;
        const frictionClass = p.transit_friction_index < 32 ? 'friction-low' : (p.transit_friction_index < 46 ? 'friction-med' : 'friction-high');
        const metroShort = p.nearest_metro.split('(')[0].trim();

        return `
          <div class="park-card ${isActive ? 'active' : ''}" onclick="selectPark('${p.id}')">
            <div class="park-card-header">
              <span class="park-id">${p.id}</span>
              <span class="park-friction ${frictionClass}">Transit ${p.transit_friction_index}/100</span>
            </div>
            <div class="park-name">${p.name}</div>
            <div class="park-corridor">${p.corridor}</div>
            <div class="park-stats-row">
              <span>🚇 ${metroShort}</span>
              <span>🏢 ${p.companies.length} Employers</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderCompaniesView() {
      const container = document.getElementById('companiesViewContainer');
      const filtered = getFilteredParks();
      const park = TECH_PARKS.find(p => p.id === activeParkId);

      if (!park || filtered.length === 0) {
        container.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-muted);">Select a Tech Park to view companies.</div>`;
        return;
      }

      const amenitiesHtml = park.campus_amenities.map(a => `<span class="amenity-pill">✓ ${a}</span>`).join('');

      let companiesHtml = park.companies.map(c => {
        const isContacted = contactedCompanies.includes(c.company_name);
        const encodedSubject = encodeURIComponent(`Application: ${c.target_role} – Aditya Mehra (BBA International Business '26)`);
        const encodedBody = encodeURIComponent(c.pre_drafted_pitch);
        const mailtoUrl = `mailto:${c.hr_email}?subject=${encodedSubject}&body=${encodedBody}`;

        return `
          <div class="company-card" style="${isContacted ? 'border-color: var(--accent-green); background: rgba(16, 185, 129, 0.05);' : ''}">
            <div class="card-top">
              <div>
                <div class="comp-name">${c.company_name}</div>
                <div class="comp-sector">${c.sector} • ${c.building_block}</div>
              </div>
              <div class="salary-badge">${c.salary_lpa}</div>
            </div>

            <div class="role-banner">
              <div>
                <span style="font-size: 10px; text-transform: uppercase; color: var(--accent-cyan); font-weight: 700; display: block;">TARGET NON-SALES ROLE</span>
                <span class="role-title">${c.target_role}</span>
              </div>
              <span class="role-exp">${c.experience_level}</span>
            </div>

            <div class="contact-details">
              <div class="contact-item">
                <span class="contact-label">Talent Lead</span>
                <span class="contact-value">${c.hr_name}</span>
              </div>
              <div class="contact-item">
                <span class="contact-label">Verified Work Email</span>
                <span class="contact-value">${c.hr_email}</span>
              </div>
              <div class="contact-item">
                <span class="contact-label">Campus Desk Phone</span>
                <span class="contact-value">${c.desk_phone}</span>
              </div>
              <div class="contact-item">
                <span class="contact-label">Nearest Metro</span>
                <span class="contact-value">${park.nearest_metro.split('(')[0]}</span>
              </div>
            </div>

            <div class="card-actions">
              <a href="${mailtoUrl}" class="action-btn send-mail" onclick="markAutoContact('${c.company_name}')">
                ✉️ Send Non-Sales Pitch
              </a>
              <button class="action-btn copy-pitch" onclick="copyToClipboard(\`${c.pre_drafted_pitch.replace(/`/g, "\\`")}\`, 'Application Pitch')">
                📋 Copy Pitch
              </button>
              <a href="${c.linkedin_search_url}" target="_blank" class="action-btn linkedin">
                💼 LinkedIn Search
              </a>
              <a href="${c.direct_careers_url}" target="_blank" class="action-btn careers">
                🌐 Career Portal
              </a>
              <a href="tel:${c.desk_phone}" class="action-btn careers">
                📞 Call Desk
              </a>
              <button class="action-btn careers" onclick="toggleContacted('${c.company_name}')">
                ${isContacted ? '✅ Contacted' : '⭕ Mark Contacted'}
              </button>
            </div>
          </div>
        `;
      }).join('');

      container.innerHTML = `
        <div class="active-park-banner">
          <div class="banner-title">[${park.id}] ${park.name}</div>
          <div class="banner-meta">
            <span>📍 ${park.address}</span>
            <span>🚇 ${park.nearest_metro}</span>
            <span>📐 ${park.campus_area_sqft}</span>
          </div>
          <div class="amenities-tags">
            ${amenitiesHtml}
          </div>
        </div>
        ${companiesHtml}
      `;
    }

    function markAutoContact(companyName) {
      if (!contactedCompanies.includes(companyName)) {
        contactedCompanies.push(companyName);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(contactedCompanies));
        updateContactedMetric();
        renderCompaniesView();
      }
    }

    function exportFilteredCSV() {
      const filtered = getFilteredParks();
      let rows = [
        ["Tech Park ID", "Tech Park Name", "Zone", "Address", "Nearest Metro", "Company Name", "Building", "Sector", "Target Role", "Salary LPA", "HR Name", "HR Email", "Phone", "Careers URL"]
      ];

      filtered.forEach(p => {
        p.companies.forEach(c => {
          rows.push([
            p.id,
            `"${p.name}"`,
            `"${p.zone}"`,
            `"${p.address}"`,
            `"${p.nearest_metro}"`,
            `"${c.company_name}"`,
            `"${c.building_block}"`,
            `"${c.sector}"`,
            `"${c.target_role}"`,
            `"${c.salary_lpa}"`,
            `"${c.hr_name}"`,
            c.hr_email,
            c.desk_phone,
            c.direct_careers_url
          ]);
        });
      });

      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "BANGALORE_TECH_PARKS_FILTERED_EXPORT.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast("Downloaded filtered CSV!");
    }

    // Initialize
    updateContactedMetric();
    renderParkList();
    renderCompaniesView();
  </script>
</body>
</html>
"""

def main():
    print("[*] Reading tech parks master data...")
    with open(TECH_PARKS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    html_content = HTML_TEMPLATE.replace("__TECH_PARKS_JSON_DATA__", json_str)

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Successfully generated Tech Parks Studio HTML -> {HTML_OUT} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
