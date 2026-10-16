import os
import json

companies_path = r"e:\anti\data\hiring_without_whiteboards.json"
companies = json.load(open(companies_path, encoding="utf-8"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Hiring Without Whiteboards — Enterprise Directory & Command Center</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #090d16;
  --card: rgba(18, 24, 38, 0.75);
  --card-hover: rgba(26, 35, 56, 0.95);
  --border: rgba(255, 255, 255, 0.08);
  --accent-teal: #14b8a6;
  --accent-blue: #38bdf8;
  --accent-purple: #c084fc;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
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
    radial-gradient(circle at 10% 12%, rgba(20, 184, 166, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 90% 88%, rgba(56, 189, 248, 0.06) 0%, transparent 40%);
}}

header {{
  padding: 1.1rem 2.2rem;
  border-bottom: 1px solid var(--border);
  background: rgba(9, 13, 22, 0.9);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}}

.brand {{
  display: flex;
  align-items: center;
  gap: 0.85rem;
}}
.brand-badge {{
  background: linear-gradient(135deg, var(--accent-teal), #06b6d4);
  color: #000;
  font-weight: 800;
  font-size: 1rem;
  padding: 0.4rem 0.75rem;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(20, 184, 166, 0.3);
}}
.brand-title h1 {{
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #14b8a6, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.brand-title p {{
  font-size: 0.75rem;
  color: var(--text-dim);
}}

.stats-bar {{
  display: flex;
  gap: 1.5rem;
  align-items: center;
}}
.stat-pill {{
  font-size: 0.8rem;
  color: var(--text-muted);
}}
.stat-pill strong {{
  color: var(--accent-teal);
  font-family: 'JetBrains Mono', monospace;
}}

.container {{
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;
}}

.controls-row {{
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}}
.search-box {{
  flex: 1;
  min-width: 300px;
  position: relative;
}}
.search-box input {{
  width: 100%;
  background: var(--card);
  border: 1px solid var(--border);
  padding: 0.8rem 1rem 0.8rem 2.8rem;
  border-radius: 12px;
  color: var(--text);
  font-family: inherit;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}}
.search-box input:focus {{
  outline: none;
  border-color: var(--accent-teal);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.25);
}}
.search-box svg {{
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
}}

.filter-pills {{
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}}
.pill {{
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  padding: 0.45rem 0.9rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}}
.pill:hover {{ border-color: rgba(255,255,255,0.2); color: var(--text); }}
.pill.active {{
  background: rgba(20, 184, 166, 0.15);
  border-color: var(--accent-teal);
  color: var(--accent-teal);
}}

/* Grid */
.grid-wrap {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}}
.comp-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  transition: all 0.25s ease;
  backdrop-filter: blur(12px);
}}
.comp-card:hover {{
  border-color: rgba(20, 184, 166, 0.4);
  transform: translateY(-2px);
  background: var(--card-hover);
}}
.comp-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
}}
.comp-name {{
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
}}
.comp-loc {{
  font-size: 0.8rem;
  color: var(--text-dim);
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}}
.comp-process {{
  font-size: 0.86rem;
  line-height: 1.6;
  color: var(--text-muted);
  max-height: 110px;
  overflow-y: auto;
  padding-right: 0.4rem;
}}
.tags-wrap {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}}
.tag {{
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.55rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-muted);
}}
.tag.teal {{ background: rgba(20, 184, 166, 0.12); color: var(--accent-teal); }}
.tag.blue {{ background: rgba(56, 189, 248, 0.12); color: var(--accent-blue); }}

.comp-foot {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}}
.btn {{
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.45rem 0.9rem;
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
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.25);
}}
.btn-teal {{
  background: var(--accent-teal);
  color: #000;
  border: none;
}}
.btn-teal:hover {{
  background: #2dd4bf;
}}
</style>
</head>
<body>

<header>
  <div class="brand">
    <div class="brand-badge">HWW</div>
    <div class="brand-title">
      <h1>Hiring Without Whiteboards Directory</h1>
      <p>Real-World Coding • Take-Home Projects • Pair Programming • Practical Evaluation</p>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-pill">Companies: <strong>{len(companies)}</strong></div>
    <div class="stat-pill">Remote-Friendly: <strong id="stat-remote">0</strong></div>
    <div class="stat-pill">India Hubs: <strong id="stat-india">0</strong></div>
  </div>
</header>

<main class="container">

  <div class="controls-row">
    <div class="search-box">
      <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8" stroke-width="2"/>
        <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <input type="text" id="comp-search" placeholder="Search 767 companies, locations (San Francisco, London, Bangalore), or interview style..." oninput="filterCompanies()" />
    </div>

    <div class="filter-pills" id="style-filters">
      <button class="pill active" onclick="setStyleFilter('All', this)">All Companies</button>
      <button class="pill" onclick="setStyleFilter('Remote', this)">🌐 Remote Friendly</button>
      <button class="pill" onclick="setStyleFilter('Take-Home', this)">📦 Take-Home Project</button>
      <button class="pill" onclick="setStyleFilter('Pairing', this)">🤝 Pair Programming</button>
      <button class="pill" onclick="setStyleFilter('Design', this)">🏛️ System Design</button>
      <button class="pill" onclick="setStyleFilter('India', this)">🇮🇳 India Hubs</button>
    </div>
  </div>

  <div class="grid-wrap" id="companies-grid"></div>

</main>

<script>
const COMPANIES = {json.dumps(companies)};

let activeFilter = 'All';

function countStats() {{
  const remCount = COMPANIES.filter(c => c.is_remote).length;
  const indCount = COMPANIES.filter(c => c.is_india).length;
  document.getElementById('stat-remote').textContent = remCount;
  document.getElementById('stat-india').textContent = indCount;
}}

function setStyleFilter(fil, btn) {{
  activeFilter = fil;
  document.querySelectorAll('#style-filters .pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  renderGrid();
}}

function renderGrid() {{
  const query = document.getElementById('comp-search').value.toLowerCase();
  const grid = document.getElementById('companies-grid');
  grid.innerHTML = '';

  const filtered = COMPANIES.filter(c => {{
    let matchF = true;
    if (activeFilter === 'Remote') matchF = c.is_remote;
    else if (activeFilter === 'Take-Home') matchF = c.styles.includes('Take-Home Project');
    else if (activeFilter === 'Pairing') matchF = c.styles.includes('Pair Programming');
    else if (activeFilter === 'Design') matchF = c.styles.includes('System Design');
    else if (activeFilter === 'India') matchF = c.is_india;

    const matchQ = c.name.toLowerCase().includes(query) || 
                   c.location.toLowerCase().includes(query) || 
                   c.process.toLowerCase().includes(query) ||
                   c.styles.some(s => s.toLowerCase().includes(query));

    return matchF && matchQ;
  }});

  filtered.slice(0, 90).forEach(c => {{
    const card = document.createElement('div');
    card.className = 'comp-card';
    card.innerHTML = `
      <div>
        <div class="comp-head">
          <div>
            <div class="comp-name">${{c.name}}</div>
            <div class="comp-loc">📍 ${{c.location}}</div>
          </div>
        </div>
        <div class="comp-process" style="margin: 0.75rem 0;">${{c.process || 'Real-world practical engineering interview.'}}</div>
        <div class="tags-wrap">
          ${{c.styles.map(s => `<span class="tag ${{s.includes('Take-Home') ? 'teal' : s.includes('Pair') ? 'blue' : ''}}">${{s}}</span>`).join('')}}
        </div>
      </div>
      <div class="comp-foot">
        <span style="font-size:0.75rem; color:var(--text-dim);">${{c.section || 'General'}}</span>
        <a href="${{c.url}}" target="_blank" class="btn btn-teal">Careers Portal ↗</a>
      </div>
    `;
    grid.appendChild(card);
  }});
}}

function filterCompanies() {{
  renderGrid();
}}

countStats();
renderGrid();
</script>
</body>
</html>
"""

out_file = r"e:\anti\hiring_without_whiteboards_dashboard.html"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated hiring_without_whiteboards_dashboard.html successfully!")
