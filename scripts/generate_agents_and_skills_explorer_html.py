#!/usr/bin/env python3
"""
generate_agents_and_skills_explorer_html.py

Generates the interactive, ultra-fast Master AI Workforce Command Center.
Indexes all 3,368 Agents, 3,670 Skills, 94 Workflows, and 10 Career OS Engines (7,142 Total Assets).
Features instant search (<10ms), category pills, domain filtering, and pagination.
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
INVENTORY_JSON = DATA_DIR / "all_agents_and_skills_inventory.json"
HTML_OUT = ROOT_DIR / "apps" / "job_application_studio" / "agents_and_skills_explorer.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master AI Workforce Explorer | 7,142 Agents & Skills</title>
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
      --font-main: 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-family: var(--font-main);
      padding-bottom: 80px;
    }

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
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-icon {
      background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
      color: #fff;
      font-weight: 900;
      font-size: 16px;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-title { font-size: 16px; font-weight: 700; }
    .brand-sub { font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); }
    .nav-links { display: flex; gap: 10px; }
    .nav-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }
    .nav-btn:hover { background: var(--bg-card-hover); color: #fff; border-color: var(--accent-cyan); }
    .nav-btn.primary { background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue)); color: #000; font-weight: 700; border: none; }

    .hero { max-width: 1400px; margin: 0 auto; padding: 32px 24px 16px; }
    .hero-tag {
      display: inline-block;
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid rgba(139, 92, 246, 0.3);
      color: var(--accent-purple);
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 20px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }
    .hero-title {
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 8px;
      background: linear-gradient(135deg, #ffffff 40%, var(--accent-purple));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc { color: var(--text-secondary); font-size: 14px; max-width: 900px; margin-bottom: 20px; }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }
    .metric-box {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px 18px;
    }
    .metric-val { font-size: 22px; font-weight: 800; color: #fff; font-family: var(--font-mono); }
    .metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }

    .controls-panel {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .search-row { display: flex; gap: 12px; }
    .search-input {
      flex: 1;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px 18px;
      color: #fff;
      font-size: 14px;
      outline: none;
    }
    .search-input:focus { border-color: var(--accent-purple); }

    .pill-group { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .pill-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-right: 4px; }
    .filter-pill {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .filter-pill:hover { background: var(--bg-card-hover); color: #fff; }
    .filter-pill.active { background: var(--accent-purple); color: #fff; border-color: var(--accent-purple); font-weight: 700; }

    .results-info {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 24px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: var(--text-secondary);
    }

    .assets-grid {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 24px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }
    .asset-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 18px;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .asset-card:hover {
      border-color: rgba(139, 92, 246, 0.5);
      background: var(--bg-card-hover);
      transform: translateY(-2px);
    }
    .card-badge-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .category-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .cat-agent { background: rgba(0, 242, 254, 0.15); color: var(--accent-cyan); }
    .cat-skill { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }
    .cat-workflow { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
    .cat-engine { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }

    .asset-name { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 6px; word-break: break-all; }
    .asset-domain { font-size: 12px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.4; }
    .asset-path {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      background: var(--bg-secondary);
      padding: 6px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
      word-break: break-all;
    }

    .card-actions { display: flex; gap: 8px; }
    .card-btn {
      flex: 1;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-secondary);
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }
    .card-btn:hover { background: var(--bg-card); color: #fff; border-color: var(--accent-cyan); }

    .pagination {
      max-width: 1400px;
      margin: 28px auto 0;
      padding: 0 24px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
    }
    .page-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }
    .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .page-btn:hover:not(:disabled) { border-color: var(--accent-purple); }

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
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s;
      z-index: 1000;
    }
    .toast.show { opacity: 1; transform: translateY(0); }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <header class="top-nav">
    <div class="brand">
      <div class="brand-icon">AI</div>
      <div>
        <div class="brand-title">Master AI Workforce Explorer</div>
        <div class="brand-sub">ADI CAREER OS • 7,142 AGENTS, SKILLS & ENGINES</div>
      </div>
    </div>
    <div class="nav-links">
      <a href="http://localhost:9119/apps/job_application_studio/bangalore_tech_parks_studio.html" class="nav-btn">🏢 Tech Parks Directory</a>
      <a href="http://localhost:9119/apps/job_application_studio/bangalore_non_stop_outreach_studio.html" class="nav-btn">⚡ 4,500 Blitz Studio</a>
      <a href="http://localhost:9119/apps/get_me_hired_dashboard/index.html" class="nav-btn">📊 Master Dashboard</a>
      <a href="http://localhost:9119/apps/index.html" class="nav-btn">🌐 Master Hub</a>
      <a href="#" class="nav-btn primary" onclick="exportCatalogCSV()">📥 Download Full Catalog CSV</a>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-tag">Exhaustive Autonomous Capability Inventory</div>
    <h1 class="hero-title">Master AI Workforce & Capabilities Command Center</h1>
    <p class="hero-desc">
      Inspect and search across the entire operational workforce: 3,368 Autonomous Agents, 3,670 Specialized Skills,
      94 Automation Workflows, and 10 Core Career OS Engines. Filter by functional domain from International Trade / EXIM
      to B2B Operations, Cloud Infrastructure, and Executive Strategy.
    </p>

    <!-- Metrics -->
    <div class="metric-grid">
      <div class="metric-box">
        <div class="metric-val" id="metricGrandTotal">7,142</div>
        <div class="metric-label">Total Cataloged Assets</div>
      </div>
      <div class="metric-box">
        <div class="metric-val" id="metricAgents">3,368</div>
        <div class="metric-label">Autonomous Agents</div>
      </div>
      <div class="metric-box">
        <div class="metric-val" id="metricSkills">3,670</div>
        <div class="metric-label">Specialized Skills</div>
      </div>
      <div class="metric-box">
        <div class="metric-val" id="metricWorkflows">94</div>
        <div class="metric-label">Automation Workflows</div>
      </div>
      <div class="metric-box">
        <div class="metric-val" id="metricEngines">10</div>
        <div class="metric-label">Career OS Core Engines</div>
      </div>
    </div>

    <!-- Controls -->
    <div class="controls-panel">
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Instant search by keyword, agent name, domain, or path (e.g. exim, b2b, finance, resume, cloud, docker)..." oninput="handleSearch()">
      </div>

      <!-- Category Filter Pills -->
      <div class="pill-group">
        <span class="pill-label">Category:</span>
        <button class="filter-pill active" onclick="setCategoryFilter('all', this)">All (7,142)</button>
        <button class="filter-pill" onclick="setCategoryFilter('Career OS Execution Engine', this)">Career Engines (10)</button>
        <button class="filter-pill" onclick="setCategoryFilter('Autonomous Agent', this)">Agents (3,368)</button>
        <button class="filter-pill" onclick="setCategoryFilter('Autonomous Skill', this)">Skills (3,670)</button>
        <button class="filter-pill" onclick="setCategoryFilter('Automation Workflow', this)">Workflows (94)</button>
      </div>

      <!-- Domain Filter Pills -->
      <div class="pill-group">
        <span class="pill-label">Domain:</span>
        <button class="filter-pill active" onclick="setDomainFilter('all', this)">All Domains</button>
        <button class="filter-pill" onclick="setDomainFilter('EXIM', this)">🚢 EXIM & Logistics (460)</button>
        <button class="filter-pill" onclick="setDomainFilter('B2B', this)">💼 B2B & Operations (460)</button>
        <button class="filter-pill" onclick="setDomainFilter('Finance', this)">💰 Finance & Treasury (461)</button>
        <button class="filter-pill" onclick="setDomainFilter('Growth', this)">📈 Growth & SEO (461)</button>
        <button class="filter-pill" onclick="setDomainFilter('Market', this)">🎯 Market Intel (461)</button>
        <button class="filter-pill" onclick="setDomainFilter('Talent', this)">👥 Talent & HR (460)</button>
        <button class="filter-pill" onclick="setDomainFilter('Security', this)">🛡️ Security (404)</button>
        <button class="filter-pill" onclick="setDomainFilter('Cloud', this)">☁️ Cloud & DevOps (430)</button>
        <button class="filter-pill" onclick="setDomainFilter('Intelligence', this)">🤖 AI & Data (836)</button>
      </div>
    </div>
  </section>

  <!-- Results Count -->
  <div class="results-info">
    <span id="resultsCount">Showing 1-50 of 7,142 assets</span>
    <span id="searchSpeed">Search Latency: &lt;5ms</span>
  </div>

  <!-- Assets Grid -->
  <main class="assets-grid" id="assetsGrid">
    <!-- Injected via JS -->
  </main>

  <!-- Pagination -->
  <div class="pagination">
    <button class="page-btn" id="prevBtn" onclick="prevPage()">← Previous</button>
    <span id="pageIndicator" style="font-family: var(--font-mono); font-size: 13px;">Page 1 of 143</span>
    <button class="page-btn" id="nextBtn" onclick="nextPage()">Next →</button>
  </div>

  <div id="toast" class="toast">Copied to clipboard!</div>

  <script>
    const RAW_DATA = __RAW_INVENTORY_JSON__;
    const ALL_ITEMS = [
      ...RAW_DATA.career_engines,
      ...RAW_DATA.workflows,
      ...RAW_DATA.agents,
      ...RAW_DATA.skills
    ];

    let currentCategory = 'all';
    let currentDomain = 'all';
    let searchQuery = '';
    let currentPage = 1;
    const PAGE_SIZE = 48;
    let filteredItems = ALL_ITEMS;

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    function copyText(text, label) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied ${label}!`);
      });
    }

    function setCategoryFilter(cat, btn) {
      currentCategory = cat;
      document.querySelectorAll('.pill-group:nth-of-type(1) .filter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      currentPage = 1;
      applyFilters();
    }

    function setDomainFilter(dom, btn) {
      currentDomain = dom;
      document.querySelectorAll('.pill-group:nth-of-type(2) .filter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      currentPage = 1;
      applyFilters();
    }

    function handleSearch() {
      searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
      currentPage = 1;
      applyFilters();
    }

    function applyFilters() {
      const t0 = performance.now();
      filteredItems = ALL_ITEMS.filter(item => {
        let matchCat = true;
        if (currentCategory !== 'all') {
          matchCat = item.category === currentCategory;
        }

        let matchDom = true;
        if (currentDomain !== 'all') {
          matchDom = item.domain.toLowerCase().includes(currentDomain.toLowerCase()) || 
                     item.name.toLowerCase().includes(currentDomain.toLowerCase());
        }

        let matchQuery = true;
        if (searchQuery) {
          matchQuery = item.name.toLowerCase().includes(searchQuery) ||
                       item.domain.toLowerCase().includes(searchQuery) ||
                       item.relative_path.toLowerCase().includes(searchQuery);
        }

        return matchCat && matchDom && matchQuery;
      });

      const t1 = performance.now();
      document.getElementById('searchSpeed').innerText = `Search Latency: ${(t1 - t0).toFixed(1)}ms`;

      renderGrid();
    }

    function renderGrid() {
      const container = document.getElementById('assetsGrid');
      const total = filteredItems.length;
      const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
      if (currentPage > totalPages) currentPage = totalPages;

      const startIdx = (currentPage - 1) * PAGE_SIZE;
      const endIdx = Math.min(startIdx + PAGE_SIZE, total);
      const pageItems = filteredItems.slice(startIdx, endIdx);

      document.getElementById('resultsCount').innerText = total === 0 ? 'No matching assets found' : `Showing ${startIdx + 1}-${endIdx} of ${total.toLocaleString()} assets`;
      document.getElementById('pageIndicator').innerText = `Page ${currentPage} of ${totalPages}`;
      document.getElementById('prevBtn').disabled = currentPage <= 1;
      document.getElementById('nextBtn').disabled = currentPage >= totalPages;

      if (total === 0) {
        container.innerHTML = `<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);">No agents or skills match your search filters.</div>`;
        return;
      }

      container.innerHTML = pageItems.map(item => {
        let catClass = 'cat-skill';
        if (item.category.includes('Agent')) catClass = 'cat-agent';
        else if (item.category.includes('Workflow')) catClass = 'cat-workflow';
        else if (item.category.includes('Engine')) catClass = 'cat-engine';

        return `
          <div class="asset-card">
            <div>
              <div class="card-badge-row">
                <span class="category-badge ${catClass}">${item.category}</span>
              </div>
              <div class="asset-name">${item.name}</div>
              <div class="asset-domain">${item.domain}</div>
            </div>
            <div>
              <div class="asset-path">${item.relative_path}</div>
              <div class="card-actions">
                <button class="card-btn" onclick="copyText('${item.relative_path}', 'Path')">📋 Copy Path</button>
                <button class="card-btn" onclick="copyText('${item.name}', 'Name')">🏷️ Copy Name</button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        renderGrid();
        window.scrollTo({ top: 380, behavior: 'smooth' });
      }
    }

    function nextPage() {
      const totalPages = Math.ceil(filteredItems.length / PAGE_SIZE);
      if (currentPage < totalPages) {
        currentPage++;
        renderGrid();
        window.scrollTo({ top: 380, behavior: 'smooth' });
      }
    }

    function exportCatalogCSV() {
      let rows = [["Category", "Name", "Domain", "Relative Path", "File Name"]];
      filteredItems.forEach(i => {
        rows.push([`"${i.category}"`, `"${i.name}"`, `"${i.domain}"`, `"${i.relative_path}"`, `"${i.file_name}"`]);
      });
      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "AGENTS_AND_SKILLS_FILTERED_CATALOG.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast("Downloaded catalog CSV!");
    }

    // Initialize
    applyFilters();
  </script>
</body>
</html>
"""

def main():
    print("[*] Reading all agents and skills inventory...")
    with open(INVENTORY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    html_content = HTML_TEMPLATE.replace("__RAW_INVENTORY_JSON__", json_str)

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Successfully generated Agents & Skills Explorer HTML -> {HTML_OUT} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
