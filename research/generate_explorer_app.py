#!/usr/bin/env python3
"""
Generate the enhanced interactive System Prompts Explorer web application
with Search, Filter, Live File Inspection, and Side-by-Side Comparator.
"""

import json
from pathlib import Path

INDEX_JSON_PATH = Path(r"e:\anti\research\SYSTEM_PROMPTS_MASTER_INDEX.json")
OUTPUT_HTML_PATH = Path(r"e:\anti\research\system_prompts_explorer.html")
OUTPUT_JS_PATH = Path(r"e:\anti\research\system_prompts_data.js")
LAUNCHER_BAT = Path(r"e:\anti\research\launch_explorer.bat")

def main():
    with open(INDEX_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    js_content = f"window.SYSTEM_PROMPTS_DATA = {json.dumps(data)};"
    with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    # Generate 1-click batch launcher
    with open(LAUNCHER_BAT, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo Starting System Prompts Intelligence Explorer on port 8080...\n")
        f.write("start \"\" \"http://localhost:8080/system_prompts_explorer.html\"\n")
        f.write("python -m http.server 8080 --directory \"%~dp0\"\n")
        
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Prompts Intelligence Explorer</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #090d16;
      --bg-card: rgba(18, 26, 43, 0.75);
      --bg-card-hover: rgba(28, 40, 65, 0.9);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.4);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --accent-blue: #38bdf8;
      --accent-purple: #a855f7;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.12) 0px, transparent 50%);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, sans-serif;
      min-height: 100vh;
      padding-bottom: 60px;
    }
    header {
      padding: 30px 5% 20px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(9, 13, 22, 0.85);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .header-content {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }
    .title-group h1 {
      font-size: 1.7rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #38bdf8 0%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .title-group p {
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 3px;
    }
    .nav-tabs {
      display: flex;
      gap: 10px;
      margin-top: 15px;
    }
    .tab-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: var(--accent-blue);
      color: #090d16;
      border-color: var(--accent-blue);
    }
    .stats-bar {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .stat-pill {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .stat-pill strong { color: var(--accent-blue); font-weight: 700; }
    
    main {
      max-width: 1400px;
      margin: 25px auto;
      padding: 0 5%;
    }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    
    .search-box {
      width: 100%;
      position: relative;
      margin-bottom: 20px;
    }
    .search-box input {
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 14px 20px 14px 46px;
      border-radius: 12px;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.2s ease;
    }
    .search-box input:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }
    .search-icon {
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }
    .filters-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      margin-bottom: 15px;
    }
    .filter-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 600;
      margin-right: 4px;
    }
    .pill-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 5px 11px;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .pill-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
    }
    .pill-btn.active {
      background: var(--accent-blue);
      color: #090d16;
      border-color: var(--accent-blue);
      font-weight: 600;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 18px;
      margin-top: 20px;
    }
    .prompt-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .prompt-card:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-accent);
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
    }
    .provider-tag {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 7px;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }
    .tag-Anthropic { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .tag-Google { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .tag-OpenAI { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .tag-xAI { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .tag-Default { background: rgba(255, 255, 255, 0.08); color: #cbd5e1; border: 1px solid var(--border-subtle); }
    
    .prompt-name {
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }
    .prompt-excerpt {
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.45;
      max-height: 60px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .card-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }
    .badge {
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: #94a3b8;
    }
    .badge.active { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border-subtle);
      padding-top: 10px;
      margin-top: auto;
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }

    /* Comparator */
    .compare-container {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 25px;
    }
    .selectors-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 25px;
    }
    .select-group label {
      display: block;
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 8px;
      font-weight: 600;
    }
    .select-group select {
      width: 100%;
      background: #090d16;
      border: 1px solid var(--border-subtle);
      color: #fff;
      padding: 12px;
      border-radius: 8px;
      outline: none;
      font-size: 0.9rem;
    }
    .compare-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    .compare-table th, .compare-table td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      text-align: left;
    }
    .compare-table th {
      background: rgba(255, 255, 255, 0.03);
      color: var(--accent-blue);
      font-weight: 600;
    }
    .diff-yes { color: var(--accent-emerald); font-weight: bold; }
    .diff-no { color: var(--text-muted); }

    /* Modal */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }
    .modal-overlay.active { display: flex; }
    .modal-content {
      background: #0f172a;
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      width: 100%;
      max-width: 950px;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }
    .modal-header {
      padding: 18px 24px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-body {
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      cursor: pointer;
    }
    .code-preview {
      background: #090d16;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      white-space: pre-wrap;
      max-height: 450px;
      overflow-y: auto;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .copy-btn {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--accent-blue);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 600;
    }
    .copy-btn:hover { background: rgba(56, 189, 248, 0.25); }
  </style>
</head>
<body>

  <header>
    <div class="header-content">
      <div class="title-group">
        <h1>System Prompts Intelligence Explorer</h1>
        <p>Forensic database of 423 production AI system prompts & agent scaffolds</p>
        <div class="nav-tabs">
          <button class="tab-btn active" onclick="switchTab('browse')">Browse & Search</button>
          <button class="tab-btn" onclick="switchTab('compare')">Side-by-Side Comparator</button>
        </div>
      </div>
      <div class="stats-bar">
        <div class="stat-pill">Total Prompts: <strong id="totalCount">423</strong></div>
        <div class="stat-pill">Tokens: <strong id="totalTokens">~3.5M</strong></div>
        <div class="stat-pill">Providers: <strong id="providerCount">18</strong></div>
      </div>
    </div>
  </header>

  <main>
    <!-- Tab 1: Browse -->
    <div class="tab-content active" id="tabBrowse">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="Search by model name, tool, keyword, or capability...">
      </div>

      <div class="filters-row" id="providerFilters">
        <span class="filter-label">Provider:</span>
        <button class="pill-btn active" data-provider="all">All</button>
      </div>

      <div class="filters-row" id="capabilityFilters">
        <span class="filter-label">Capability:</span>
        <button class="pill-btn" data-cap="tool_calling">Tool Calling</button>
        <button class="pill-btn" data-cap="shell_execution">Shell / Bash</button>
        <button class="pill-btn" data-cap="planning_mode">Planning Mode</button>
        <button class="pill-btn" data-cap="subagents">Subagents</button>
        <button class="pill-btn" data-cap="safety_guardrails">Safety Guardrails</button>
      </div>

      <div class="grid" id="promptsGrid"></div>
    </div>

    <!-- Tab 2: Compare -->
    <div class="tab-content" id="tabCompare">
      <div class="compare-container">
        <h2>Side-by-Side Architectural Comparator</h2>
        <p style="color:var(--text-muted); margin-top:4px; font-size:0.9rem;">Select two system prompts to compare metrics, capabilities, and tool coverage.</p>
        
        <div class="selectors-row" style="margin-top:20px;">
          <div class="select-group">
            <label>Prompt A (Baseline)</label>
            <select id="selectPromptA"></select>
          </div>
          <div class="select-group">
            <label>Prompt B (Target to Compare)</label>
            <select id="selectPromptB"></select>
          </div>
        </div>

        <div id="compareResult"></div>
      </div>
    </div>
  </main>

  <!-- Modal -->
  <div class="modal-overlay" id="detailModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 id="modalTitle" style="font-size:1.2rem;">Prompt Details</h2>
        <div style="display:flex; gap:10px; align-items:center;">
          <button class="copy-btn" id="copyModalBtn" onclick="copyModalContent()">Copy Content</button>
          <button class="close-btn" id="closeModal">&times;</button>
        </div>
      </div>
      <div class="modal-body">
        <div id="modalMeta" style="font-size:0.85rem; color:var(--text-muted);"></div>
        <div class="code-preview" id="modalExcerpt"></div>
      </div>
    </div>
  </div>

  <script src="system_prompts_data.js"></script>
  <script>
    const data = window.SYSTEM_PROMPTS_DATA;
    const grid = document.getElementById('promptsGrid');
    const searchInput = document.getElementById('searchInput');
    const providerFiltersContainer = document.getElementById('providerFilters');
    const capabilityFiltersContainer = document.getElementById('capabilityFilters');

    let currentProvider = 'all';
    let activeCapabilities = new Set();
    let searchTerm = '';

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      if (tabId === 'browse') {
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
        document.getElementById('tabBrowse').classList.add('active');
      } else {
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('tabCompare').classList.add('active');
        initComparator();
      }
    }

    // Populate Providers
    const providers = Object.keys(data.provider_breakdown).sort((a, b) => 
      data.provider_breakdown[b].count - data.provider_breakdown[a].count
    );

    providers.forEach(p => {
      const btn = document.createElement('button');
      btn.className = 'pill-btn';
      btn.dataset.provider = p;
      btn.textContent = `${p} (${data.provider_breakdown[p].count})`;
      providerFiltersContainer.appendChild(btn);
    });

    providerFiltersContainer.addEventListener('click', (e) => {
      if (!e.target.classList.contains('pill-btn')) return;
      providerFiltersContainer.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentProvider = e.target.dataset.provider;
      render();
    });

    capabilityFiltersContainer.addEventListener('click', (e) => {
      if (!e.target.classList.contains('pill-btn')) return;
      const cap = e.target.dataset.cap;
      if (activeCapabilities.has(cap)) {
        activeCapabilities.delete(cap);
        e.target.classList.remove('active');
      } else {
        activeCapabilities.add(cap);
        e.target.classList.add('active');
      }
      render();
    });

    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase().trim();
      render();
    });

    function getTagClass(provider) {
      if (['Anthropic', 'Google', 'OpenAI', 'xAI'].includes(provider)) {
        return `tag-${provider}`;
      }
      return 'tag-Default';
    }

    function render() {
      grid.innerHTML = '';
      const filtered = data.prompts.filter(item => {
        if (currentProvider !== 'all' && item.provider !== currentProvider) return false;
        for (const cap of activeCapabilities) {
          if (!item.capabilities[cap]) return false;
        }
        if (searchTerm) {
          const matchName = item.model_name.toLowerCase().includes(searchTerm);
          const matchExcerpt = item.excerpt.toLowerCase().includes(searchTerm);
          const matchCat = item.category.toLowerCase().includes(searchTerm);
          const matchTools = item.detected_tools.some(t => t.toLowerCase().includes(searchTerm));
          if (!matchName && !matchExcerpt && !matchCat && !matchTools) return false;
        }
        return true;
      });

      filtered.forEach(item => {
        const card = document.createElement('div');
        card.className = 'prompt-card';
        card.onclick = () => openModal(item);

        const badgesHtml = [
          item.has_tools ? '<span class="badge active">Tools</span>' : '',
          item.has_shell ? '<span class="badge active">Shell</span>' : '',
          item.has_planning ? '<span class="badge active">Plan</span>' : '',
          item.has_subagents ? '<span class="badge active">Subagents</span>' : '',
          item.has_safety ? '<span class="badge active">Safety</span>' : ''
        ].filter(Boolean).join('');

        card.innerHTML = `
          <div class="card-top">
            <span class="provider-tag ${getTagClass(item.provider)}">${item.provider}</span>
            <span style="font-size:0.75rem; color:var(--text-muted);">${item.category}</span>
          </div>
          <div class="prompt-name">${item.model_name}</div>
          <div class="prompt-excerpt">${item.excerpt || 'No excerpt available.'}</div>
          <div class="card-badges">${badgesHtml}</div>
          <div class="card-footer">
            <span>~${item.est_tokens.toLocaleString()} tokens</span>
            <span>${item.line_count} lines</span>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    // Modal
    const modal = document.getElementById('detailModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMeta = document.getElementById('modalMeta');
    const modalExcerpt = document.getElementById('modalExcerpt');
    const closeModal = document.getElementById('closeModal');

    async function openModal(item) {
      modalTitle.textContent = `${item.model_name} (${item.provider})`;
      modalMeta.innerHTML = `
        <strong>Path:</strong> <code>system_prompts_leaks/${item.rel_path}</code> | 
        <strong>Tokens:</strong> ~${item.est_tokens.toLocaleString()} | 
        <strong>Lines:</strong> ${item.line_count.toLocaleString()}
      `;
      modalExcerpt.textContent = "Loading full prompt...";
      modal.classList.add('active');

      // Attempt live fetch if served via local HTTP server
      try {
        const res = await fetch(`system_prompts_leaks/${item.rel_path}`);
        if (res.ok) {
          const fullText = await res.text();
          modalExcerpt.textContent = fullText;
          return;
        }
      } catch (err) {}
      // Fallback
      modalExcerpt.textContent = item.excerpt + "\\n\\n[Note: Launch via launch_explorer.bat to view full uncompressed 423 markdown prompts live]";
    }

    function copyModalContent() {
      navigator.clipboard.writeText(modalExcerpt.textContent);
      const btn = document.getElementById('copyModalBtn');
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy Content', 2000);
    }

    closeModal.onclick = () => modal.classList.remove('active');
    modal.onclick = (e) => { if (e.target === modal) modal.classList.remove('active'); };

    // Comparator
    let comparatorInitialized = false;
    function initComparator() {
      if (comparatorInitialized) return;
      comparatorInitialized = true;
      const selectA = document.getElementById('selectPromptA');
      const selectB = document.getElementById('selectPromptB');

      data.prompts.forEach((p, idx) => {
        const optA = document.createElement('option');
        optA.value = idx;
        optA.textContent = `[${p.provider}] ${p.model_name} (~${p.est_tokens.toLocaleString()} tok)`;
        selectA.appendChild(optA);

        const optB = document.createElement('option');
        optB.value = idx;
        optB.textContent = `[${p.provider}] ${p.model_name} (~${p.est_tokens.toLocaleString()} tok)`;
        selectB.appendChild(optB);
      });

      // Default selections: Google Antigravity and Claude Code Fable 5.1
      const defaultA = data.prompts.findIndex(p => p.rel_path.includes('antigravity-cli'));
      const defaultB = data.prompts.findIndex(p => p.rel_path.includes('claude-code-fable-5.1'));

      if (defaultA !== -1) selectA.value = defaultA;
      if (defaultB !== -1) selectB.value = defaultB;

      selectA.onchange = renderCompare;
      selectB.onchange = renderCompare;
      renderCompare();
    }

    function renderCompare() {
      const idxA = document.getElementById('selectPromptA').value;
      const idxB = document.getElementById('selectPromptB').value;
      const pA = data.prompts[idxA];
      const pB = data.prompts[idxB];
      const res = document.getElementById('compareResult');

      const boolBadge = (val) => val ? '<span class="diff-yes">YES</span>' : '<span class="diff-no">-</span>';

      res.innerHTML = `
        <table class="compare-table">
          <thead>
            <tr>
              <th style="width:30%;">Feature / Metric</th>
              <th style="width:35%;">${pA.model_name} (${pA.provider})</th>
              <th style="width:35%;">${pB.model_name} (${pB.provider})</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Category</td><td>${pA.category}</td><td>${pB.category}</td></tr>
            <tr><td>Est. Tokens</td><td><strong>~${pA.est_tokens.toLocaleString()}</strong></td><td><strong>~${pB.est_tokens.toLocaleString()}</strong></td></tr>
            <tr><td>Line Count</td><td>${pA.line_count.toLocaleString()}</td><td>${pB.line_count.toLocaleString()}</td></tr>
            <tr><td>Tool Calling</td><td>${boolBadge(pA.has_tools)}</td><td>${boolBadge(pB.has_tools)}</td></tr>
            <tr><td>Planning Mode</td><td>${boolBadge(pA.has_planning)}</td><td>${boolBadge(pB.has_planning)}</td></tr>
            <tr><td>Subagents</td><td>${boolBadge(pA.has_subagents)}</td><td>${boolBadge(pB.has_subagents)}</td></tr>
            <tr><td>Shell Execution</td><td>${boolBadge(pA.has_shell)}</td><td>${boolBadge(pB.has_shell)}</td></tr>
            <tr><td>Safety Guardrails</td><td>${boolBadge(pA.has_safety)}</td><td>${boolBadge(pB.has_safety)}</td></tr>
            <tr><td>Tools Detected</td><td>${pA.detected_tools.join(', ') || 'None'}</td><td>${pB.detected_tools.join(', ') || 'None'}</td></tr>
            <tr><td>Path</td><td><code>${pA.rel_path}</code></td><td><code>${pB.rel_path}</code></td></tr>
          </tbody>
        </table>
      `;
    }

    render();
  </script>
</body>
</html>
"""
    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Successfully generated updated {OUTPUT_HTML_PATH} and {LAUNCHER_BAT}.")

if __name__ == "__main__":
    main()
