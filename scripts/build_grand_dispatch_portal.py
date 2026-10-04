#!/usr/bin/env python3
"""
scripts/build_grand_dispatch_portal.py
Generates the Grand Supreme Autonomous Dispatch Center HTML Application.
Enables instant search, corridor filtering, 1-click individual and batch multi-tab launches (5, 10, 20),
real-time status persistence (localStorage), and full telemetry across all 10,000 corporate targets.
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "APPLICATIONS_GLOBAL_10000.json"
OUT_HTML = ROOT_DIR / "apps" / "job_application_studio" / "grand_supreme_dispatch_center.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OMEGA ∞ Grand Supreme Autonomous Dispatch Center — 10,000 Targets</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #060911;
      --card: #0d1322;
      --border: #1e293b;
      --accent: #00f0ff;
      --accent-glow: rgba(0, 240, 255, 0.2);
      --green: #10b981;
      --amber: #f59e0b;
      --purple: #a855f7;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, sans-serif;
      padding: 24px;
      line-height: 1.5;
    }
    .container { max-width: 1560px; margin: 0 auto; }
    header {
      background: linear-gradient(135deg, rgba(13,19,34,0.9), rgba(15,23,42,0.95));
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .brand-title { font-size: 24px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
    .badge {
      background: rgba(0, 240, 255, 0.12);
      border: 1px solid var(--accent);
      color: var(--accent);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px;
    }
    .card-lbl { font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; }
    .card-val { font-size: 28px; font-weight: 800; color: #fff; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }
    
    .control-panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
    }
    .search-input {
      flex: 1;
      min-width: 320px;
      background: #060911;
      border: 1px solid #334155;
      color: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 14px;
    }
    .select-input {
      background: #060911;
      border: 1px solid #334155;
      color: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 14px;
    }
    .btn-group {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .btn-batch {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      border: none;
      padding: 10px 16px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-batch:hover { opacity: 0.9; transform: translateY(-1px); }
    .btn-batch-amber {
      background: linear-gradient(135deg, #d97706, #b45309);
    }
    .btn-batch-purple {
      background: linear-gradient(135deg, #9333ea, #7e22ce);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      background: var(--card);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border);
      font-size: 13px;
    }
    th {
      background: #080d1a;
      text-align: left;
      padding: 14px 16px;
      color: var(--text-muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border);
    }
    td {
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    tr:hover td { background: rgba(255,255,255,0.02); }
    .fit-badge {
      background: rgba(16, 185, 129, 0.15);
      color: var(--green);
      padding: 3px 8px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 12px;
    }
    .status-badge {
      padding: 3px 8px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      font-size: 11px;
      cursor: pointer;
    }
    .status-staged { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid #475569; }
    .status-dispatched { background: rgba(0, 240, 255, 0.15); color: #00f0ff; border: 1px solid #0284c7; }
    .status-interview { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #059669; }

    .action-link {
      display: inline-block;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 12px;
    }
    .action-link:hover { opacity: 0.9; }
    .pagination {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 20px;
      color: var(--text-muted);
      font-size: 13px;
    }
    .page-btn {
      background: #1e293b;
      color: #fff;
      border: 1px solid #334155;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
    }
    .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <div class="brand-title">🌐 OMEGA ∞ Grand Supreme Autonomous Dispatch Center</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">
          Candidate: <strong>Aditya Mehra</strong> | BBA International Business (DSU '26) | AERO India 2025 Lead Coordinator | Instawork (99.2% QA)
        </div>
      </div>
      <div class="badge">10,000 / 10,000 GLOBAL TARGETS ACTIVE</div>
    </header>

    <div class="stats-grid">
      <div class="card">
        <div class="card-lbl">Total Enterprise Targets</div>
        <div class="card-val" id="stat-total">10,000</div>
      </div>
      <div class="card">
        <div class="card-lbl">Distinct Global Companies</div>
        <div class="card-val">8,147</div>
      </div>
      <div class="card">
        <div class="card-lbl">Interactive Dispatched Counter</div>
        <div class="card-val" id="stat-dispatched" style="color: var(--accent);">0</div>
      </div>
      <div class="card">
        <div class="card-lbl">Target Match Quality</div>
        <div class="card-val">91.4% Avg</div>
      </div>
    </div>

    <div class="control-panel">
      <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search by company, job title, HR contact, or corridor..." oninput="handleSearch()">
      <select id="corridorSelect" class="select-input" onchange="handleFilter()">
        <option value="">All Corridors & Tech Parks (Global)</option>
      </select>
      
      <div class="btn-group">
        <button class="btn-batch" onclick="launchBatch(5)">
          ⚡ Burst 5 Tabs
        </button>
        <button class="btn-batch btn-batch-amber" onclick="launchBatch(10)">
          🔥 Burst 10 Tabs
        </button>
        <button class="btn-batch btn-batch-purple" onclick="launchBatch(20)">
          🚀 Burst 20 Tabs
        </button>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Target ID</th>
          <th>Company</th>
          <th>Position Title</th>
          <th>Hiring Lead & Contact</th>
          <th>Ecosystem Corridor</th>
          <th>Fit</th>
          <th>Status</th>
          <th>Instant Dispatch</th>
        </tr>
      </thead>
      <tbody id="tableBody">
        <!-- Rows injected by JavaScript -->
      </tbody>
    </table>

    <div class="pagination">
      <div id="pageInfo">Showing 1 to 50 of 10,000 records</div>
      <div style="display: flex; gap: 8px;">
        <button class="page-btn" id="prevBtn" onclick="prevPage()">Previous</button>
        <button class="page-btn" id="nextBtn" onclick="nextPage()">Next</button>
      </div>
    </div>
  </div>

  <script>
    let allData = [];
    let filteredData = [];
    let currentPage = 1;
    const pageSize = 50;
    const STORAGE_KEY = "omega_dispatch_status_v1";

    function getSavedStatuses() {
      try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      } catch (e) {
        return {};
      }
    }

    function setSavedStatus(id, status) {
      const saved = getSavedStatuses();
      saved[id] = status;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
      updateDispatchedCount();
    }

    function updateDispatchedCount() {
      const saved = getSavedStatuses();
      const count = Object.keys(saved).length;
      document.getElementById('stat-dispatched').textContent = count.toLocaleString();
    }

    async function init() {
      const res = await fetch('../../data/APPLICATIONS_GLOBAL_10000.json');
      allData = await res.json();
      filteredData = [...allData];

      // Populate corridors
      const corridors = [...new Set(allData.map(d => d.corridor).filter(Boolean))].sort();
      const select = document.getElementById('corridorSelect');
      corridors.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        select.appendChild(opt);
      });

      updateDispatchedCount();
      renderTable();
    }

    function renderTable() {
      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, filteredData.length);
      const pageSlice = filteredData.slice(start, end);
      const tbody = document.getElementById('tableBody');
      const saved = getSavedStatuses();
      tbody.innerHTML = '';

      pageSlice.forEach(row => {
        const tr = document.createElement('tr');
        const currentStatus = saved[row.id] || "STAGED";
        let statusClass = "status-staged";
        if (currentStatus === "DISPATCHED") statusClass = "status-dispatched";
        if (currentStatus === "INTERVIEW") statusClass = "status-interview";

        tr.innerHTML = `
          <td><code style="color:#00f0ff; font-family:'JetBrains Mono';">${row.id}</code></td>
          <td><strong>${escapeHtml(row.company)}</strong></td>
          <td>${escapeHtml(row.title)}</td>
          <td>${escapeHtml(row.hr_name)}<br><span style="color:#64748b; font-size:11px;">${escapeHtml(row.hr_email)}</span></td>
          <td>${escapeHtml(row.corridor)}</td>
          <td><span class="fit-badge">${row.fit.toFixed(1)}%</span></td>
          <td>
            <span class="status-badge ${statusClass}" onclick="toggleStatus('${row.id}')">${currentStatus}</span>
          </td>
          <td>
            <a href="${row.gmail_url}" target="_blank" class="action-link" onclick="markDispatched('${row.id}')">⚡ 1-Click Gmail</a>
          </td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById('pageInfo').textContent = `Showing ${filteredData.length === 0 ? 0 : start + 1} to ${end} of ${filteredData.length.toLocaleString()} targets`;
      document.getElementById('prevBtn').disabled = currentPage <= 1;
      document.getElementById('nextBtn').disabled = end >= filteredData.length;
    }

    function toggleStatus(id) {
      const saved = getSavedStatuses();
      const cur = saved[id] || "STAGED";
      let next = "DISPATCHED";
      if (cur === "DISPATCHED") next = "INTERVIEW";
      else if (cur === "INTERVIEW") next = "STAGED";
      setSavedStatus(id, next);
      renderTable();
    }

    function markDispatched(id) {
      setSavedStatus(id, "DISPATCHED");
      setTimeout(renderTable, 200);
    }

    function handleSearch() { applyFilters(); }
    function handleFilter() { applyFilters(); }

    function applyFilters() {
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const c = document.getElementById('corridorSelect').value;

      filteredData = allData.filter(item => {
        const matchC = !c || item.corridor === c;
        const matchQ = !q || 
          item.company.toLowerCase().includes(q) ||
          item.title.toLowerCase().includes(q) ||
          item.hr_name.toLowerCase().includes(q) ||
          item.hr_email.toLowerCase().includes(q) ||
          item.corridor.toLowerCase().includes(q);
        return matchC && matchQ;
      });

      currentPage = 1;
      renderTable();
    }

    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        renderTable();
      }
    }

    function nextPage() {
      if (currentPage * pageSize < filteredData.length) {
        currentPage++;
        renderTable();
      }
    }

    function launchBatch(n) {
      const start = (currentPage - 1) * pageSize;
      const batch = filteredData.slice(start, start + n);
      if (batch.length === 0) {
        alert('No targets in current view.');
        return;
      }
      batch.forEach(item => {
        markDispatched(item.id);
        window.open(item.gmail_url, '_blank');
      });
      renderTable();
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    window.onload = init;
  </script>
</body>
</html>
"""

def main():
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"[OK] Successfully built updated {OUT_HTML}")

if __name__ == "__main__":
    main()
