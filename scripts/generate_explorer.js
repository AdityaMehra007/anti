const fs = require('fs');
const path = require('path');

const masterDb = path.join(__dirname, 'public_apis_master.json');
const catDb = path.join(__dirname, 'public_apis_categories.json');
const htmlOutput = path.join(__dirname, 'public_apis_explorer.html');

const apis = JSON.parse(fs.readFileSync(masterDb, 'utf-8'));
const categories = JSON.parse(fs.readFileSync(catDb, 'utf-8'));

const template = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Public APIs Master Explorer (1,737 APIs)</title>
  <style>
    :root {
      --bg: #0b0f17;
      --card-bg: #121824;
      --border: #232d3f;
      --text: #c9d1d9;
      --text-muted: #8b949e;
      --accent: #38bdf8;
      --accent-hover: #7dd3fc;
      --badge-noauth: #10b981;
      --badge-key: #f59e0b;
      --badge-oauth: #8b5cf6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: var(--bg); color: var(--text); padding: 28px 20px; line-height: 1.5; }
    .container { max-width: 1440px; margin: 0 auto; }
    header { margin-bottom: 24px; padding-bottom: 18px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 16px; }
    h1 { font-size: 28px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 10px; }
    .subtitle { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
    .quick-stats { display: flex; gap: 14px; font-size: 13px; }
    .stat-pill { background: #162032; border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px; color: #e2e8f0; }
    .stat-pill b { color: var(--accent); }
    .search-panel { background: #131a29; border: 1px solid var(--border); border-radius: 10px; padding: 18px; margin-bottom: 22px; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 12px; }
    @media (max-width: 900px) { .search-panel { grid-template-columns: 1fr; } }
    input[type="text"], select { width: 100%; background: #0b0f17; border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px; color: #fff; font-size: 14px; outline: none; transition: border-color 0.2s; }
    input[type="text"]:focus, select:focus { border-color: var(--accent); }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }
    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 18px; display: flex; flex-direction: column; transition: all 0.2s ease; position: relative; }
    .card:hover { transform: translateY(-3px); border-color: var(--accent); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
    .card-title { font-size: 17px; font-weight: 600; color: #fff; text-decoration: none; transition: color 0.15s; }
    .card-title:hover { color: var(--accent); text-decoration: underline; }
    .cat-tag { font-size: 11px; font-weight: 500; padding: 2px 8px; border-radius: 12px; background: #1e293b; color: #94a3b8; border: 1px solid #334155; white-space: nowrap; }
    .card-desc { font-size: 13.5px; color: #94a3b8; flex-grow: 1; margin-bottom: 14px; }
    .badges { display: flex; flex-wrap: wrap; gap: 6px; font-size: 11px; margin-top: auto; }
    .badge { padding: 3px 8px; border-radius: 4px; font-weight: 600; }
    .badge-noauth { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-key { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-oauth { background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }
    .badge-cors { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-https { background: rgba(148, 163, 184, 0.12); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.25); }
    .count-indicator { margin-bottom: 14px; font-size: 14px; color: var(--text-muted); }
    .count-indicator b { color: #fff; }
    .empty-state { grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-muted); font-size: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>⚡ Public APIs Master Directory</h1>
        <p class="subtitle">Complete offline index of 1,737 free APIs across 52 categories from <a href="https://github.com/public-apis/public-apis" target="_blank" style="color:var(--accent); text-decoration:none;">public-apis/public-apis</a></p>
      </div>
      <div class="quick-stats">
        <div class="stat-pill">Total: <b>${apis.length}</b></div>
        <div class="stat-pill">Categories: <b>${Object.keys(categories).length}</b></div>
        <div class="stat-pill">No Auth: <b>${apis.filter(a => a.auth.toLowerCase() === 'no').length}</b></div>
      </div>
    </header>

    <div class="search-panel">
      <input type="text" id="searchInput" placeholder="Search by name, capability, or keyword (e.g., job, scraper, llm, salary, crypto)..." autofocus>
      <select id="catFilter">
        <option value="">All Categories (${apis.length})</option>
      </select>
      <select id="authFilter">
        <option value="">All Auth Requirements</option>
        <option value="no">No Auth Needed</option>
        <option value="apikey">API Key</option>
        <option value="oauth">OAuth</option>
      </select>
      <select id="corsFilter">
        <option value="">All CORS Support</option>
        <option value="yes">CORS Supported (Browser OK)</option>
        <option value="no">CORS Disabled</option>
      </select>
    </div>

    <div class="count-indicator" id="countBar">Showing <b>${apis.length}</b> APIs</div>
    <div class="grid" id="grid"></div>
  </div>

  <script>
    const DATA = ${JSON.stringify(apis)};
    const CATS = ${JSON.stringify(categories)};
    
    const searchInput = document.getElementById('searchInput');
    const catFilter = document.getElementById('catFilter');
    const authFilter = document.getElementById('authFilter');
    const corsFilter = document.getElementById('corsFilter');
    const grid = document.getElementById('grid');
    const countBar = document.getElementById('countBar');

    Object.entries(CATS).sort((a,b) => b[1] - a[1]).forEach(([cat, count]) => {
      const opt = document.createElement('option');
      opt.value = cat.toLowerCase();
      opt.textContent = \`\${cat} (\${count})\`;
      catFilter.appendChild(opt);
    });

    function getAuthClass(auth) {
      const lower = auth.toLowerCase();
      if (lower === 'no') return 'badge-noauth';
      if (lower.includes('oauth')) return 'badge-oauth';
      return 'badge-key';
    }

    function render() {
      const q = searchInput.value.trim().toLowerCase();
      const cat = catFilter.value;
      const auth = authFilter.value;
      const cors = corsFilter.value;

      const filtered = DATA.filter(item => {
        if (cat && item.category.toLowerCase() !== cat) return false;
        if (auth && !item.auth.toLowerCase().includes(auth)) return false;
        if (cors && item.cors.toLowerCase() !== cors) return false;
        if (q) {
          const hay = \`\${item.name} \${item.description} \${item.category}\`.toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });

      countBar.innerHTML = \`Showing <b>\${filtered.length.toLocaleString()}</b> of <b>\${DATA.length.toLocaleString()}</b> APIs\`;

      if (filtered.length === 0) {
        grid.innerHTML = '<div class="empty-state">No matching APIs found. Try clearing filters or searching for broader terms.</div>';
        return;
      }

      const limit = 200;
      const visible = filtered.slice(0, limit);
      
      grid.innerHTML = visible.map(item => \`
        <div class="card">
          <div class="card-top">
            <a class="card-title" href="\${item.url}" target="_blank" rel="noopener noreferrer">\${item.name}</a>
            <span class="cat-tag">\${item.category}</span>
          </div>
          <p class="card-desc">\${item.description}</p>
          <div class="badges">
            <span class="badge \${getAuthClass(item.auth)}">Auth: \${item.auth}</span>
            <span class="badge badge-cors">CORS: \${item.cors}</span>
            <span class="badge badge-https">HTTPS: \${item.https}</span>
          </div>
        </div>
      \`).join('');

      if (filtered.length > limit) {
        grid.innerHTML += \`<div class="empty-state" style="padding: 24px;">Showing top \${limit} results. Use specific keywords or category filter to see the rest.</div>\`;
      }
    }

    searchInput.addEventListener('input', render);
    catFilter.addEventListener('change', render);
    authFilter.addEventListener('change', render);
    corsFilter.addEventListener('change', render);

    render();
  </script>
</body>
</html>`;

fs.writeFileSync(htmlOutput, template, 'utf-8');
console.log('Successfully written', htmlOutput);
