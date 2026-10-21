import csv
import json
import os

csv_path = r'e:\anti\linkedin_export\Connections.csv'
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

header_idx = -1
for i, line in enumerate(lines[:10]):
    if 'First Name' in line:
        header_idx = i
        break

reader = csv.DictReader(lines[header_idx:])
records = []
for r in reader:
    fn = r.get('First Name', '').strip()
    ln = r.get('Last Name', '').strip()
    name = f'{fn} {ln}'.strip()
    url = r.get('URL', '').strip()
    email = r.get('Email Address', '').strip()
    comp = r.get('Company', '').strip() or 'Independent / Not Disclosed'
    pos = r.get('Position', '').strip() or 'Not Specified'
    dt = r.get('Connected On', '').strip()
    records.append([name, comp, pos, email, url, dt])

data_json = json.dumps(records, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LinkedIn Network Directory — 9,223 Connections</title>
<style>
  :root {
    --bg: #0b0f19;
    --card: #151e32;
    --border: #23324d;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.25);
    --badge-bg: rgba(56, 189, 248, 0.12);
    --table-hover: #1c2944;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
  body { background: var(--bg); color: var(--text); padding: 24px; min-height: 100vh; }
  .container { max-width: 1400px; margin: 0 auto; }
  header { margin-bottom: 24px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }
  h1 { font-size: 24px; font-weight: 700; color: #fff; }
  .subtitle { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
  .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .metric-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }
  .metric-value { font-size: 28px; font-weight: 700; color: var(--accent); }
  .metric-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .toolbar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
  .search-box { flex: 1; min-width: 280px; }
  input[type="text"], select { width: 100%; padding: 10px 14px; background: var(--card); border: 1px solid var(--border); border-radius: 6px; color: #fff; font-size: 14px; outline: none; }
  input[type="text"]:focus, select:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
  .filter-select { width: 220px; }
  .btn { padding: 10px 16px; border-radius: 6px; border: 1px solid var(--border); background: var(--card); color: #fff; font-size: 14px; cursor: pointer; transition: all 0.2s; }
  .btn:hover { background: #1c2944; border-color: var(--accent); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .table-container { background: var(--card); border: 1px solid var(--border); border-radius: 8px; overflow-x: auto; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2); }
  table { width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }
  th { background: #111827; padding: 12px 16px; font-weight: 600; color: var(--text-muted); border-bottom: 1px solid var(--border); }
  td { padding: 12px 16px; border-bottom: 1px solid var(--border); vertical-align: middle; }
  tr:hover td { background: var(--table-hover); }
  .company-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; background: var(--badge-bg); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.25); max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .email-tag { display: inline-block; font-family: monospace; font-size: 12px; background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); padding: 2px 6px; border-radius: 4px; }
  a.linkedin-btn { color: #38bdf8; text-decoration: none; font-weight: 500; }
  a.linkedin-btn:hover { text-decoration: underline; }
  .pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding: 8px 0; color: var(--text-muted); font-size: 14px; }
  .page-nav { display: flex; gap: 8px; align-items: center; }
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>LinkedIn Connections Master Directory</h1>
      <div class="subtitle">Complete interactive directory of all 9,223 professional connections</div>
    </div>
    <button class="btn" onclick="exportFilteredCSV()">Export Filtered CSV</button>
  </header>

  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-value">9,223</div>
      <div class="metric-label">Total Connections</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">5,227</div>
      <div class="metric-label">Unique Organizations</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">330+</div>
      <div class="metric-label">Big 4 & MBB Consulting</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">220+</div>
      <div class="metric-label">Investment Banks & Finance</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">90</div>
      <div class="metric-label">Verified Direct Emails</div>
    </div>
  </div>

  <div class="toolbar">
    <div class="search-box">
      <input type="text" id="searchQuery" placeholder="Search by name, company, position, email..." oninput="onSearch()">
    </div>
    <select id="companyFilter" class="filter-select" onchange="onFilter()">
      <option value="">All Companies</option>
      <option value="EY">EY</option>
      <option value="Deloitte">Deloitte</option>
      <option value="Accenture">Accenture</option>
      <option value="IBM">IBM</option>
      <option value="Goldman Sachs">Goldman Sachs</option>
      <option value="Tata Consultancy Services">TCS</option>
      <option value="JPMorganChase">JPMorgan Chase</option>
      <option value="Amazon">Amazon</option>
      <option value="Capgemini">Capgemini</option>
      <option value="Christ University">Christ University</option>
      <option value="KPMG">KPMG</option>
      <option value="PwC">PwC</option>
      <option value="Google">Google</option>
      <option value="Microsoft">Microsoft</option>
      <option value="Rippling">Rippling</option>
      <option value="Stripe">Stripe</option>
      <option value="Flipkart">Flipkart</option>
      <option value="HAS_EMAIL">Only With Email</option>
    </select>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Company</th>
          <th>Position / Role</th>
          <th>Email Address</th>
          <th>Connected Date</th>
          <th>LinkedIn Profile</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  </div>

  <div class="pagination">
    <span id="resultsCount">Showing 0 of 0</span>
    <div class="page-nav">
      <button class="btn" id="prevBtn" onclick="changePage(-1)">&larr; Previous</button>
      <span id="pageDisplay">Page 1</span>
      <button class="btn" id="nextBtn" onclick="changePage(1)">Next &rarr;</button>
    </div>
  </div>
</div>

<script>
const RAW_DATA = """ + data_json + """;
let filteredData = RAW_DATA;
let currentPage = 1;
const pageSize = 50;

function renderTable() {
  const tbody = document.getElementById('tableBody');
  const start = (currentPage - 1) * pageSize;
  const pageRows = filteredData.slice(start, start + pageSize);

  tbody.innerHTML = pageRows.map(r => `
    <tr>
      <td style="font-weight:600">${escapeHtml(r[0])}</td>
      <td><span class="company-badge" title="${escapeHtml(r[1])}">${escapeHtml(r[1])}</span></td>
      <td>${escapeHtml(r[2])}</td>
      <td>${r[3] ? `<span class="email-tag">${escapeHtml(r[3])}</span>` : '<span style="color:#475569">—</span>'}</td>
      <td style="color:#94a3b8; font-size:13px;">${escapeHtml(r[5])}</td>
      <td>${r[4] ? `<a href="${escapeHtml(r[4])}" target="_blank" class="linkedin-btn">Profile &nearr;</a>` : '—'}</td>
    </tr>
  `).join('');

  const total = filteredData.length;
  const end = Math.min(start + pageSize, total);
  document.getElementById('resultsCount').innerText = `Showing ${total === 0 ? 0 : (start + 1).toLocaleString()}–${end.toLocaleString()} of ${total.toLocaleString()} connections`;
  const maxPage = Math.max(1, Math.ceil(total / pageSize));
  document.getElementById('pageDisplay').innerText = `Page ${currentPage} of ${maxPage}`;
  document.getElementById('prevBtn').disabled = (currentPage <= 1);
  document.getElementById('nextBtn').disabled = (currentPage >= maxPage);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}

function applyFilters() {
  const q = document.getElementById('searchQuery').value.toLowerCase().trim();
  const c = document.getElementById('companyFilter').value;

  filteredData = RAW_DATA.filter(r => {
    if (c === 'HAS_EMAIL') {
      if (!r[3]) return false;
    } else if (c && !r[1].toLowerCase().includes(c.toLowerCase())) {
      return false;
    }

    if (q) {
      const match = r[0].toLowerCase().includes(q) ||
                    r[1].toLowerCase().includes(q) ||
                    r[2].toLowerCase().includes(q) ||
                    r[3].toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  currentPage = 1;
  renderTable();
}

function onSearch() { applyFilters(); }
function onFilter() { applyFilters(); }

function changePage(delta) {
  const maxPage = Math.max(1, Math.ceil(filteredData.length / pageSize));
  currentPage = Math.max(1, Math.min(maxPage, currentPage + delta));
  renderTable();
  window.scrollTo({ top: 300, behavior: 'smooth' });
}

function exportFilteredCSV() {
  let csv = 'First & Last Name,Company,Position,Email Address,LinkedIn URL,Connected On\\n';
  filteredData.forEach(r => {
    csv += r.map(f => '"' + (f || '').replace(/"/g, '""') + '"').join(',') + '\\n';
  });
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'filtered_connections.csv';
  a.click();
}

renderTable();
</script>
</body>
</html>
"""

output_path = r'e:\anti\linkedin_export\connections_directory.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully created {output_path}')
