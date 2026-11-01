#!/usr/bin/env python3
"""
scripts/generate_hww_cockpit.py
Generates the self-contained HTML5 Mission Control Cockpit
for Hiring Without Whiteboards (761 companies).
"""

import sys
import json
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_DATA_PATH = BASE_DIR / "data" / "hiring_without_whiteboards.json"
OUTPUT_HTML_PATH = BASE_DIR / "hiring_without_whiteboards_cockpit.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HIRING WITHOUT WHITEBOARDS — Mission Control Cockpit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #07090e;
      --surface: #0e131f;
      --surface-card: rgba(17, 24, 39, 0.7);
      --surface-card-hover: rgba(26, 36, 56, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(99, 102, 241, 0.5);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #6366f1;
      --primary-glow: rgba(99, 102, 241, 0.2);
      --cyan: #06b6d4;
      --emerald: #10b981;
      --amber: #f59e0b;
      --purple: #a855f7;
      --rose: #f43f5e;
      --radius: 12px;
      --font-sans: 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      min-height: 100vh;
      line-height: 1.5;
      overflow-x: hidden;
    }

    /* Ambient glows */
    .ambient-glow-1 {
      position: fixed;
      top: -150px;
      left: 10%;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }
    .ambient-glow-2 {
      position: fixed;
      bottom: -150px;
      right: 10%;
      width: 600px;
      height: 600px;
      background: radial-gradient(circle, rgba(6, 182, 212, 0.08) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }

    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 32px 24px;
      position: relative;
      z-index: 1;
    }

    /* Header */
    header {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 32px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 24px;
    }
    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .brand-row {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .logo-badge {
      background: linear-gradient(135deg, #4f46e5, #06b6d4);
      color: #fff;
      padding: 8px 12px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 14px;
      letter-spacing: 0.05em;
      box-shadow: 0 4px 14px var(--primary-glow);
    }
    h1 {
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(180deg, #ffffff 30%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .header-tagline {
      color: var(--text-muted);
      font-size: 14px;
    }
    .meta-badges {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .meta-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.03);
    }
    .meta-pill.live {
      color: var(--emerald);
      border-color: rgba(16, 185, 129, 0.3);
      background: rgba(16, 185, 129, 0.06);
    }
    .meta-pill.live::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 8px var(--emerald);
    }

    /* Metrics Ribbon */
    .metrics-ribbon {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }
    .metric-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      backdrop-filter: blur(16px);
      transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.15);
    }
    .metric-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-dim);
      margin-bottom: 6px;
      font-weight: 600;
    }
    .metric-val-row {
      display: flex;
      align-items: baseline;
      gap: 8px;
    }
    .metric-val {
      font-size: 26px;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
    }
    .metric-sub {
      font-size: 12px;
      color: var(--text-muted);
    }

    /* Control Panel: Search & Filters */
    .control-panel {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      backdrop-filter: blur(16px);
    }
    .search-row {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    .search-input-wrap {
      position: relative;
      flex: 1;
      min-width: 280px;
    }
    .search-input {
      width: 100%;
      padding: 12px 16px 12px 42px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: #fff;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 12px var(--primary-glow);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 16px;
    }

    .sort-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .select-dropdown {
      padding: 11px 14px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }
    .btn-export {
      padding: 11px 16px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.2s, border-color 0.2s;
    }
    .btn-export:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Filter rows */
    .filter-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .filter-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      min-width: 70px;
    }
    .chip-group {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .filter-chip {
      padding: 6px 13px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s;
    }
    .filter-chip:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.07);
    }
    .filter-chip.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #fff;
      box-shadow: 0 2px 10px var(--primary-glow);
    }

    /* Results Header */
    .results-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      font-size: 13px;
      color: var(--text-muted);
    }
    .results-count {
      font-weight: 600;
      color: #fff;
    }

    /* Company Cards Grid */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 20px;
    }
    .company-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px;
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
      position: relative;
    }
    .company-card:hover {
      transform: translateY(-3px);
      border-color: rgba(99, 102, 241, 0.4);
      background: var(--surface-card-hover);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }
    .company-name {
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .company-link {
      color: var(--cyan);
      text-decoration: none;
      transition: color 0.15s;
    }
    .company-link:hover {
      color: #38bdf8;
      text-decoration: underline;
    }
    .ext-icon {
      font-size: 13px;
      opacity: 0.6;
    }

    .score-badge {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      background: rgba(16, 185, 129, 0.12);
      color: var(--emerald);
      border: 1px solid rgba(16, 185, 129, 0.25);
      flex-shrink: 0;
    }
    .score-badge.amber {
      background: rgba(245, 158, 11, 0.12);
      color: var(--amber);
      border-color: rgba(245, 158, 11, 0.25);
    }

    .tag-row {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .badge {
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .badge-remote {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-trial {
      background: rgba(244, 63, 94, 0.15);
      color: #fb7185;
      border: 1px solid rgba(244, 63, 94, 0.3);
    }
    .badge-takehome {
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .badge-pairing {
      background: rgba(6, 182, 212, 0.15);
      color: #67e8f9;
      border: 1px solid rgba(6, 182, 212, 0.3);
    }
    .badge-arch {
      background: rgba(168, 85, 247, 0.15);
      color: #d8b4fe;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }

    .card-location {
      font-size: 12.5px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .card-process {
      font-size: 13.5px;
      color: #cbd5e1;
      line-height: 1.55;
      background: rgba(0, 0, 0, 0.25);
      padding: 12px;
      border-radius: 8px;
      border-left: 3px solid var(--primary);
    }

    .card-cheat {
      font-size: 12px;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.02);
      padding: 10px 12px;
      border-radius: 6px;
      border: 1px dashed var(--border);
      line-height: 1.45;
    }

    .card-actions {
      display: flex;
      gap: 8px;
      margin-top: auto;
      padding-top: 8px;
    }
    .btn-card {
      flex: 1;
      padding: 8px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }
    .btn-card:hover {
      background: rgba(255, 255, 255, 0.09);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.18);
    }
    .btn-card.primary {
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border-color: rgba(99, 102, 241, 0.35);
    }
    .btn-card.primary:hover {
      background: var(--primary);
      color: #fff;
    }

    /* Deep Dive Modal */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-overlay.active {
      display: flex;
    }
    .modal-content {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      max-width: 720px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 30px;
      position: relative;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }
    .modal-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: none;
      border: none;
      color: var(--text-dim);
      font-size: 24px;
      cursor: pointer;
    }
    .modal-close:hover { color: #fff; }
    .modal-title {
      font-size: 24px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }
    .modal-sec-title {
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-dim);
      font-weight: 700;
      margin-top: 20px;
      margin-bottom: 8px;
    }
    .modal-box {
      background: rgba(0, 0, 0, 0.3);
      padding: 14px 16px;
      border-radius: 8px;
      border: 1px solid var(--border);
      font-size: 13.5px;
      line-height: 1.6;
    }
    .outreach-box {
      font-family: var(--font-mono);
      font-size: 12px;
      background: #060911;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      white-space: pre-wrap;
      word-break: break-word;
      color: #93c5fd;
    }
    .copy-btn {
      margin-top: 10px;
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--primary);
      background: var(--primary);
      color: #fff;
      cursor: pointer;
    }

    /* Empty state */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--text-dim);
      grid-column: 1 / -1;
    }
  </style>
</head>
<body>
  <div class="ambient-glow-1"></div>
  <div class="ambient-glow-2"></div>

  <div class="container">
    <header>
      <div class="header-top">
        <div class="brand-row">
          <div class="logo-badge">OMEGA ∞</div>
          <div>
            <h1>HIRING WITHOUT WHITEBOARDS</h1>
            <div class="header-tagline">Canonical 761-Employer Intelligence & Practical Engineering Assessment Suite</div>
          </div>
        </div>
        <div class="meta-badges">
          <div class="meta-pill live">761 VERIFIED EMPLOYERS</div>
          <div class="meta-pill">ZERO LEETCODE / WHITEBOARDS</div>
        </div>
      </div>
    </header>

    <!-- Metrics Ribbon -->
    <div class="metrics-ribbon">
      <div class="metric-card">
        <div class="metric-label">Total Cataloged</div>
        <div class="metric-val-row">
          <span class="metric-val">761</span>
          <span class="metric-sub">companies</span>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Remote-Friendly</div>
        <div class="metric-val-row">
          <span class="metric-val" id="kpi-remote">290</span>
          <span class="metric-sub">38.1%</span>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Take-Home Projects</div>
        <div class="metric-val-row">
          <span class="metric-val" id="kpi-takehome">522</span>
          <span class="metric-sub">68.6%</span>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Live Pairing Loops</div>
        <div class="metric-val-row">
          <span class="metric-val" id="kpi-pairing">193</span>
          <span class="metric-sub">25.4%</span>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Paid Trials / Sprints</div>
        <div class="metric-val-row">
          <span class="metric-val" id="kpi-trial" style="color: #fb7185;">32</span>
          <span class="metric-sub">4.2%</span>
        </div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Architecture Reviews</div>
        <div class="metric-val-row">
          <span class="metric-val" id="kpi-arch">89</span>
          <span class="metric-sub">11.7%</span>
        </div>
      </div>
    </div>

    <!-- Search & Filters Control Panel -->
    <div class="control-panel">
      <div class="search-row">
        <div class="search-input-wrap">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Search by company, tech stack, location, or process..." autocomplete="off">
        </div>
        <div class="sort-wrap">
          <select id="sortSelect" class="select-dropdown">
            <option value="score">Sort: Friendliness Score</option>
            <option value="alpha">Sort: Company Name (A-Z)</option>
            <option value="region">Sort: Region</option>
          </select>
          <button class="btn-export" id="exportCsvBtn">📥 Export CSV</button>
          <button class="btn-export" id="exportJsonBtn">📥 Export JSON</button>
        </div>
      </div>

      <!-- Region Filter Chips -->
      <div class="filter-row">
        <span class="filter-label">Region:</span>
        <div class="chip-group" id="regionChips">
          <div class="filter-chip active" data-region="all">All Regions</div>
          <div class="filter-chip" data-region="remote">Remote Only</div>
          <div class="filter-chip" data-region="North America">North America</div>
          <div class="filter-chip" data-region="Europe & UK">Europe & UK</div>
          <div class="filter-chip" data-region="India & APAC">India & APAC</div>
          <div class="filter-chip" data-region="Latin America">Latin America</div>
        </div>
      </div>

      <!-- Assessment Type Chips -->
      <div class="filter-row">
        <span class="filter-label">Method:</span>
        <div class="chip-group" id="methodChips">
          <div class="filter-chip" data-method="take_home">📦 Take-Home Project</div>
          <div class="filter-chip" data-method="pairing">👥 Live Pairing</div>
          <div class="filter-chip" data-method="paid_trial">💰 Paid Trial / Sprint</div>
          <div class="filter-chip" data-method="architecture">🏛️ Architecture & Systems</div>
          <div class="filter-chip" data-method="code_review">🔍 Past Work Review</div>
        </div>
      </div>
    </div>

    <!-- Results Status -->
    <div class="results-info">
      <div>Showing <span class="results-count" id="visibleCount">0</span> of 761 employers</div>
      <div id="activeFilterDesc">Showing all companies</div>
    </div>

    <!-- Cards Grid -->
    <div class="cards-grid" id="cardsGrid"></div>
  </div>

  <!-- Modal Deep Dive -->
  <div class="modal-overlay" id="detailModal">
    <div class="modal-content">
      <button class="modal-close" id="modalCloseBtn">&times;</button>
      <div class="modal-title" id="mName">Company Name</div>
      <div id="mLinkRow" style="margin-bottom: 16px;"></div>

      <div class="modal-sec-title">Location & Regions</div>
      <div class="modal-box" id="mLocation"></div>

      <div class="modal-sec-title">Interview Loop Deconstruction</div>
      <div class="modal-box" id="mProcess"></div>

      <div class="modal-sec-title">Tactical Playbook & Cheat Code</div>
      <div class="modal-box" id="mCheat" style="color: #a5b4fc;"></div>

      <div class="modal-sec-title">Tailored Hiring Manager InMail / Pitch</div>
      <div class="outreach-box" id="mOutreach"></div>
      <button class="copy-btn" id="copyOutreachBtn">📋 Copy Outreach Pitch</button>
    </div>
  </div>

  <!-- Raw Embedded JSON for 100% Offline/Self-Contained Execution -->
  <script id="raw-companies-data" type="application/json">
__JSON_DATA_PLACEHOLDER__
  </script>

  <script>
    // State
    let allCompanies = [];
    let currentRegion = 'all';
    let activeMethods = new Set();
    let currentSort = 'score';
    let currentQuery = '';

    // Initialize data
    function initData() {
      const rawEl = document.getElementById('raw-companies-data');
      if (rawEl) {
        try {
          allCompanies = JSON.parse(rawEl.textContent);
        } catch(e) {
          console.error("Failed to parse embedded JSON", e);
        }
      }
      applyFilters();
    }

    // Filter and Sort Engine
    function applyFilters() {
      let filtered = allCompanies.filter(c => {
        // Search query
        if (currentQuery) {
          const q = currentQuery.toLowerCase();
          const matchName = c.name.toLowerCase().includes(q);
          const matchLoc = (c.raw_location || '').toLowerCase().includes(q);
          const matchProc = (c.raw_process || '').toLowerCase().includes(q);
          const matchTech = (c.tech_keywords || []).some(t => t.toLowerCase().includes(q));
          if (!matchName && !matchLoc && !matchProc && !matchTech) return false;
        }

        // Region
        if (currentRegion === 'remote') {
          if (!c.is_remote) return false;
        } else if (currentRegion !== 'all') {
          const hasReg = (c.regions || []).includes(currentRegion) || (c.primary_region || '').includes(currentRegion);
          if (!hasReg) return false;
        }

        // Assessment methods
        if (activeMethods.has('take_home') && !c.has_take_home) return false;
        if (activeMethods.has('pairing') && !c.has_pairing) return false;
        if (activeMethods.has('paid_trial') && !c.has_paid_trial) return false;
        if (activeMethods.has('architecture') && !c.has_architecture) return false;
        if (activeMethods.has('code_review') && !c.has_code_review) return false;

        return true;
      });

      // Sort
      if (currentSort === 'score') {
        filtered.sort((a, b) => b.friendliness_score - a.friendliness_score || a.name.localeCompare(b.name));
      } else if (currentSort === 'alpha') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
      } else if (currentSort === 'region') {
        filtered.sort((a, b) => (a.primary_region || '').localeCompare(b.primary_region || '') || a.name.localeCompare(b.name));
      }

      renderCards(filtered);
      document.getElementById('visibleCount').textContent = filtered.length;
    }

    // Render Cards
    function renderCards(companies) {
      const grid = document.getElementById('cardsGrid');
      if (companies.length === 0) {
        grid.innerHTML = '<div class="empty-state"><h3>No companies match the selected criteria</h3><p>Try clearing some filters or searching with another term.</p></div>';
        return;
      }

      grid.innerHTML = companies.map(c => {
        const badges = [];
        if (c.is_remote) badges.push('<span class="badge badge-remote">REMOTE</span>');
        if (c.has_paid_trial) badges.push('<span class="badge badge-trial">PAID TRIAL</span>');
        if (c.has_take_home) badges.push('<span class="badge badge-takehome">TAKE-HOME</span>');
        if (c.has_pairing) badges.push('<span class="badge badge-pairing">PAIRING</span>');
        if (c.has_architecture) badges.push('<span class="badge badge-arch">SYSTEM DESIGN</span>');

        const scoreClass = c.friendliness_score >= 85 ? '' : 'amber';
        const urlLink = c.careers_url ? `<a href="${c.careers_url}" target="_blank" rel="noopener" class="company-link ext-icon" title="Open Career Page">🔗</a>` : '';

        return `
          <div class="company-card" data-id="${c.id}">
            <div class="card-top">
              <div class="company-name">
                <span>${escapeHtml(c.name)}</span>
                ${urlLink}
              </div>
              <div class="score-badge ${scoreClass}">${c.friendliness_score}/100</div>
            </div>

            <div class="tag-row">
              ${badges.join('')}
            </div>

            <div class="card-location">
              <span>📍</span>
              <span>${escapeHtml(c.raw_location || 'Location Unspecified')}</span>
            </div>

            <div class="card-process">
              ${escapeHtml(c.raw_process || 'Practical evaluation focused on day-to-day engineering.')}
            </div>

            <div class="card-cheat">
              ${escapeHtml(c.cheat_sheet)}
            </div>

            <div class="card-actions">
              <button class="btn-card primary" onclick="openDeepDive(${c.id})">Deep Dive & Pitch</button>
              ${c.careers_url ? `<button class="btn-card" onclick="copyText('${c.careers_url}', this)">Copy URL</button>` : ''}
            </div>
          </div>
        `;
      }).join('');
    }

    // Deep Dive Modal
    function openDeepDive(id) {
      const c = allCompanies.find(item => item.id === id);
      if (!c) return;

      document.getElementById('mName').textContent = c.name;
      document.getElementById('mLocation').textContent = c.raw_location || 'Not specified';
      document.getElementById('mProcess').textContent = c.raw_process || 'Practical real-world engineering assessment.';
      document.getElementById('mCheat').textContent = c.cheat_sheet;

      const linkEl = document.getElementById('mLinkRow');
      if (c.careers_url) {
        linkEl.innerHTML = `<a href="${c.careers_url}" target="_blank" rel="noopener" style="color: var(--cyan); font-size: 14px;">Visit Official Careers Portal (${c.careers_url}) ↗</a>`;
      } else {
        linkEl.innerHTML = '<span style="color: var(--text-dim); font-size: 14px;">Direct careers link not listed in registry</span>';
      }

      // Tailored outreach pitch
      const pitch = `Hi [Hiring Manager / Recruiter],\n\nI noticed ${c.name}'s engineering team values practical, real-world assessment over artificial whiteboard hazing. That respect for engineering craftsmanship strongly resonates with my background.\n\nI build resilient, production-grade systems with clean architecture, comprehensive test suites, and strict CI/CD hygiene. Rather than memorizing LeetCode trivia, I focus on what actually moves systems forward: pragmatic trade-offs, maintainable code, and high team velocity.\n\nWould love to discuss how I can contribute to your upcoming engineering roadmaps at ${c.name}.\n\nBest regards,\n[Your Name] | [GitHub / Portfolio Link]`;
      
      document.getElementById('mOutreach').textContent = pitch;

      document.getElementById('detailModal').classList.add('active');
    }

    function closeModal() {
      document.getElementById('detailModal').classList.remove('active');
    }

    // Export Helpers
    function exportFiltered(format) {
      let visible = allCompanies.filter(c => {
        if (currentQuery) {
          const q = currentQuery.toLowerCase();
          const matchName = c.name.toLowerCase().includes(q);
          const matchLoc = (c.raw_location || '').toLowerCase().includes(q);
          const matchProc = (c.raw_process || '').toLowerCase().includes(q);
          if (!matchName && !matchLoc && !matchProc) return false;
        }
        if (currentRegion === 'remote' && !c.is_remote) return false;
        if (currentRegion !== 'all' && currentRegion !== 'remote') {
          const hasReg = (c.regions || []).includes(currentRegion) || (c.primary_region || '').includes(currentRegion);
          if (!hasReg) return false;
        }
        if (activeMethods.has('take_home') && !c.has_take_home) return false;
        if (activeMethods.has('pairing') && !c.has_pairing) return false;
        if (activeMethods.has('paid_trial') && !c.has_paid_trial) return false;
        if (activeMethods.has('architecture') && !c.has_architecture) return false;
        if (activeMethods.has('code_review') && !c.has_code_review) return false;
        return true;
      });

      if (format === 'json') {
        const blob = new Blob([JSON.stringify(visible, null, 2)], { type: 'application/json' });
        downloadBlob(blob, 'hiring_without_whiteboards_filtered.json');
      } else {
        const headers = ['id', 'name', 'careers_url', 'is_remote', 'primary_region', 'raw_location', 'friendliness_score', 'raw_process'];
        let csvContent = headers.join(',') + '\\n';
        visible.forEach(c => {
          const row = [
            c.id,
            escapeCsv(c.name),
            escapeCsv(c.careers_url),
            c.is_remote ? '1' : '0',
            escapeCsv(c.primary_region),
            escapeCsv(c.raw_location),
            c.friendliness_score,
            escapeCsv(c.raw_process)
          ];
          csvContent += row.join(',') + '\\n';
        });
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        downloadBlob(blob, 'hiring_without_whiteboards_filtered.csv');
      }
    }

    function downloadBlob(blob, filename) {
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    function copyText(str, btn) {
      navigator.clipboard.writeText(str).then(() => {
        const orig = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => { btn.textContent = orig; }, 1800);
      });
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text || '';
      return div.innerHTML;
    }

    function escapeCsv(str) {
      const s = String(str || '').replace(/"/g, '""');
      return `"${s}"`;
    }

    // Event Listeners
    document.addEventListener('DOMContentLoaded', () => {
      initData();

      // Search input with debounce
      let searchTimeout;
      document.getElementById('searchInput').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          currentQuery = e.target.value.trim();
          applyFilters();
        }, 120);
      });

      // Sort
      document.getElementById('sortSelect').addEventListener('change', (e) => {
        currentSort = e.target.value;
        applyFilters();
      });

      // Region chips
      document.querySelectorAll('#regionChips .filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          document.querySelectorAll('#regionChips .filter-chip').forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          currentRegion = chip.getAttribute('data-region');
          applyFilters();
        });
      });

      // Method chips
      document.querySelectorAll('#methodChips .filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const method = chip.getAttribute('data-method');
          if (activeMethods.has(method)) {
            activeMethods.delete(method);
            chip.classList.remove('active');
          }} else {
            activeMethods.add(method);
            chip.classList.add('active');
          }
          applyFilters();
        });
      });

      // Modal close
      document.getElementById('modalCloseBtn').addEventListener('click', closeModal);
      document.getElementById('detailModal').addEventListener('click', (e) => {
        if (e.target.id === 'detailModal') closeModal();
      });

      // Copy outreach
      document.getElementById('copyOutreachBtn').addEventListener('click', function() {
        const text = document.getElementById('mOutreach').textContent;
        copyText(text, this);
      });

      // Export buttons
      document.getElementById('exportCsvBtn').addEventListener('click', () => exportFiltered('csv'));
      document.getElementById('exportJsonBtn').addEventListener('click', () => exportFiltered('json'));
    });
  </script>
</body>
</html>
"""

def generate():
    with open(JSON_DATA_PATH, "r", encoding="utf-8") as f:
        companies = json.load(f)

    json_str = json.dumps(companies, ensure_ascii=False)
    rendered = HTML_TEMPLATE.replace("__JSON_DATA_PLACEHOLDER__", json_str)

    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[✓] Cockpit successfully generated at: {OUTPUT_HTML_PATH} ({len(companies)} companies embedded)")

if __name__ == "__main__":
    generate()
