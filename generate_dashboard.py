#!/usr/bin/env python3
"""
Dashboard Generator for Summer 2027 Internships
Builds a standalone, zero-dependency, ultra-fast interactive HTML application.
"""

import json
import os

def build_dashboard():
    json_path = r"e:\anti\data\summer2027_active.json"
    html_path = r"e:\anti\summer_2027_dashboard.html"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Minify JSON for embedding
    minified_json = json.dumps(data, separators=(',', ':'))

    total_count = len(data)
    ai_count = sum(1 for x in data if x['category'] == 'AI/ML/Data')
    swe_count = sum(1 for x in data if x['category'] == 'Software')
    quant_count = sum(1 for x in data if x['category'] == 'Quant')
    hw_count = sum(1 for x in data if x['category'] == 'Hardware')
    pm_count = sum(1 for x in data if x['category'] == 'Product')
    t1_count = sum(1 for x in data if x['tier'] in ['Tier 1 / Big Tech', 'Quant / Prop Trading'])
    remote_count = sum(1 for x in data if x['is_remote'])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Summer 2027 Internships Command Center</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: rgba(23, 31, 51, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(30, 41, 67, 0.9);
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.3);
      --accent-light: #818cf8;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --tag-ai: #10b981;
      --tag-swe: #3b82f6;
      --tag-quant: #ec4899;
      --tag-hw: #f59e0b;
      --tag-pm: #8b5cf6;
      --tag-tier1: #f43f5e;
      --applied: #22c55e;
      --starred: #fbbf24;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at 10% 20%, #171b2f 0%, #080c14 90%);
      color: var(--text);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }}

    .title-group h1 {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #fff 30%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .title-group p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-top: 4px;
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}

    .stat-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .stat-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(99, 102, 241, 0.4);
    }}

    .stat-card .label {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .stat-card .val {{
      font-size: 1.75rem;
      font-weight: 800;
      margin-top: 4px;
      color: var(--text);
    }}

    .stat-card.applied-stat .val {{
      color: var(--applied);
    }}

    .search-panel {{
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .search-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .search-input-wrap {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: rgba(11, 15, 25, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 10px;
      padding: 12px 16px 12px 42px;
      color: var(--text);
      font-size: 1rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 1.1rem;
      pointer-events: none;
    }}

    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .pill {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .pill:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
    }}

    .pill.active {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      box-shadow: 0 0 12px var(--accent-glow);
    }}

    .actions-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.9rem;
      color: var(--text-muted);
      flex-wrap: wrap;
      gap: 12px;
    }}

    .btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text);
      padding: 8px 14px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .btn-primary {{
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }}

    .btn-primary:hover {{
      background: var(--accent-light);
      box-shadow: 0 0 14px var(--accent-glow);
    }}

    .listings-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 16px;
    }}

    .job-card {{
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      position: relative;
    }}

    .job-card:hover {{
      background: var(--card-hover);
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateY(-2px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }}

    .job-card.is-applied {{
      border-color: rgba(34, 197, 94, 0.4);
      background: rgba(16, 185, 129, 0.05);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      gap: 12px;
    }}

    .company-name {{
      font-weight: 700;
      font-size: 1.15rem;
      color: #fff;
    }}

    .job-title {{
      font-size: 1rem;
      font-weight: 600;
      color: #cbd5e1;
      margin-top: 4px;
      line-height: 1.4;
    }}

    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 12px 0;
    }}

    .badge {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 3px 8px;
      border-radius: 6px;
      border: 1px solid transparent;
    }}

    .badge-ai {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3); }}
    .badge-swe {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }}
    .badge-quant {{ background: rgba(236, 72, 153, 0.15); color: #f472b6; border-color: rgba(236, 72, 153, 0.3); }}
    .badge-hw {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }}
    .badge-pm {{ background: rgba(139, 92, 246, 0.15); color: #a78bfa; border-color: rgba(139, 92, 246, 0.3); }}
    .badge-tier1 {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border-color: rgba(244, 63, 94, 0.3); }}
    .badge-remote {{ background: rgba(14, 165, 233, 0.15); color: #38bdf8; border-color: rgba(14, 165, 233, 0.3); }}

    .card-meta {{
      font-size: 0.85rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 16px;
    }}

    .meta-row {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 14px;
      gap: 8px;
    }}

    .apply-links {{
      display: flex;
      gap: 8px;
    }}

    .apply-btn {{
      padding: 6px 12px;
      font-size: 0.8rem;
      font-weight: 700;
      border-radius: 7px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }}

    .apply-btn-direct {{
      background: #4f46e5;
      color: #fff;
    }}
    .apply-btn-direct:hover {{
      background: #4338ca;
    }}

    .apply-btn-simplify {{
      background: rgba(255, 255, 255, 0.08);
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .apply-btn-simplify:hover {{
      background: rgba(255, 255, 255, 0.15);
    }}

    .status-select {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #cbd5e1;
      padding: 5px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }}

    .status-select.applied {{
      color: #22c55e;
      border-color: #22c55e;
    }}

    .pagination {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      margin: 32px 0 16px;
    }}

    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
      grid-column: 1 / -1;
    }}

    @media (max-width: 768px) {{
      .listings-grid {{ grid-template-columns: 1fr; }}
      body {{ padding: 14px; }}
    }}
  </style>
</head>
<body>

<div class="container">
  <header>
    <div class="title-group">
      <h1>Summer 2027 Internships Command Center</h1>
      <p>Synchronized from SimplifyJobs/Summer2027-Internships &bull; Live ATS & 1-Click Application Tracker</p>
    </div>
    <div style="display: flex; gap: 8px;">
      <a href="data/summer2027_active.csv" download class="btn">&#128196; Download CSV</a>
      <button class="btn btn-primary" onclick="exportTrackedData()">&#128190; Export My Tracker</button>
    </div>
  </header>

  <!-- Metrics Overview -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">Total 2027 Roles</div>
      <div class="val" id="stat-total">{total_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">AI & ML Roles</div>
      <div class="val" style="color: #34d399;">{ai_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Software Roles</div>
      <div class="val" style="color: #60a5fa;">{swe_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Quant & Trading</div>
      <div class="val" style="color: #f472b6;">{quant_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Big Tech & Tier 1</div>
      <div class="val" style="color: #fb7185;">{t1_count}</div>
    </div>
    <div class="stat-card">
      <div class="label">Remote Eligible</div>
      <div class="val" style="color: #38bdf8;">{remote_count}</div>
    </div>
    <div class="stat-card applied-stat">
      <div class="label">My Applications</div>
      <div class="val" id="stat-applied">0</div>
    </div>
  </div>

  <!-- Search & Filter Controls -->
  <div class="search-panel">
    <div class="search-row">
      <div class="search-input-wrap">
        <span class="search-icon">&#128269;</span>
        <input type="text" id="search-input" class="search-input" placeholder="Search company, job title, technology, location..." autofocus>
      </div>
      <select id="sort-select" class="btn" onchange="applyFilters()">
        <option value="default">Sort: Default Priority</option>
        <option value="newest">Sort: Newest First</option>
        <option value="company">Sort: Company A-Z</option>
        <option value="applied">Sort: Applied First</option>
      </select>
    </div>

    <div class="filter-pills">
      <div class="pill active" data-cat="all" onclick="setCategoryFilter('all', this)">All ({total_count})</div>
      <div class="pill" data-cat="AI/ML/Data" onclick="setCategoryFilter('AI/ML/Data', this)">🤖 AI/ML/Data ({ai_count})</div>
      <div class="pill" data-cat="Software" onclick="setCategoryFilter('Software', this)">💻 Software ({swe_count})</div>
      <div class="pill" data-cat="Quant" onclick="setCategoryFilter('Quant', this)">📈 Quant Finance ({quant_count})</div>
      <div class="pill" data-cat="Hardware" onclick="setCategoryFilter('Hardware', this)">🔧 Hardware ({hw_count})</div>
      <div class="pill" data-cat="Product" onclick="setCategoryFilter('Product', this)">📱 Product ({pm_count})</div>
      <div class="pill" data-tier="Tier 1 / Big Tech" onclick="toggleTierFilter(this)">⚡ Big Tech / FAANG ({t1_count})</div>
      <div class="pill" data-remote="true" onclick="toggleRemoteFilter(this)">🌐 Remote Only ({remote_count})</div>
      <div class="pill" data-status="applied" onclick="toggleAppliedOnly(this)">✅ My Applied Only</div>
    </div>

    <div class="actions-bar">
      <span id="results-count">Showing {total_count} opportunities</span>
      <span>Page <span id="current-page">1</span> of <span id="total-pages">1</span></span>
    </div>
  </div>

  <!-- Listings Cards -->
  <div class="listings-grid" id="listings-container"></div>

  <!-- Pagination -->
  <div class="pagination">
    <button class="btn" id="prev-btn" onclick="changePage(-1)">Previous</button>
    <span id="page-indicator" style="color: var(--text-muted); font-weight: 600;">1 / 1</span>
    <button class="btn" id="next-btn" onclick="changePage(1)">Next</button>
  </div>
</div>

<script id="raw-data" type="application/json">
{minified_json}
</script>

<script>
  const ALL_JOBS = JSON.parse(document.getElementById('raw-data').textContent);
  let activeCategory = 'all';
  let tierOnly = false;
  let remoteOnly = false;
  let appliedOnly = false;
  let searchQuery = '';
  let currentPage = 1;
  const PAGE_SIZE = 48;

  // Local storage application state
  function getAppStates() {{
    try {{
      return JSON.parse(localStorage.getItem('summer2027_app_states') || '{{}}');
    }} catch (e) {{
      return {{}};
    }}
  }}

  function setAppState(id, status) {{
    const states = getAppStates();
    if (status === 'none') {{
      delete states[id];
    }} else {{
      states[id] = status;
    }}
    localStorage.setItem('summer2027_app_states', JSON.stringify(states));
    updateAppliedCounter();
    applyFilters();
  }}

  function updateAppliedCounter() {{
    const states = getAppStates();
    const appliedCount = Object.values(states).filter(s => s === 'applied' || s === 'interviewing' || s === 'offer').length;
    document.getElementById('stat-applied').innerText = appliedCount;
  }}

  function setCategoryFilter(cat, elem) {{
    activeCategory = cat;
    document.querySelectorAll('.filter-pills .pill[data-cat]').forEach(p => p.classList.remove('active'));
    elem.classList.add('active');
    currentPage = 1;
    applyFilters();
  }}

  function toggleTierFilter(elem) {{
    tierOnly = !tierOnly;
    elem.classList.toggle('active', tierOnly);
    currentPage = 1;
    applyFilters();
  }}

  function toggleRemoteFilter(elem) {{
    remoteOnly = !remoteOnly;
    elem.classList.toggle('active', remoteOnly);
    currentPage = 1;
    applyFilters();
  }}

  function toggleAppliedOnly(elem) {{
    appliedOnly = !appliedOnly;
    elem.classList.toggle('active', appliedOnly);
    currentPage = 1;
    applyFilters();
  }}

  document.getElementById('search-input').addEventListener('input', (e) => {{
    searchQuery = e.target.value.toLowerCase().trim();
    currentPage = 1;
    applyFilters();
  }});

  function getFilteredJobs() {{
    const states = getAppStates();
    return ALL_JOBS.filter(job => {{
      // Category filter
      if (activeCategory !== 'all' && job.category !== activeCategory) return false;

      // Tier filter
      if (tierOnly && job.tier !== 'Tier 1 / Big Tech' && job.tier !== 'Quant / Prop Trading') return false;

      // Remote filter
      if (remoteOnly && !job.is_remote) return false;

      // Applied only filter
      if (appliedOnly && !states[job.id]) return false;

      // Search query
      if (searchQuery) {{
        const haystack = `${{job.company}} ${{job.title}} ${{job.category}} ${{job.locations}} ${{job.tier}}`.toLowerCase();
        if (!haystack.includes(searchQuery)) return false;
      }}

      return true;
    }});
  }}

  function sortJobs(jobs) {{
    const sortVal = document.getElementById('sort-select').value;
    const states = getAppStates();
    return [...jobs].sort((a, b) => {{
      if (sortVal === 'applied') {{
        const aApp = states[a.id] ? 1 : 0;
        const bApp = states[b.id] ? 1 : 0;
        return bApp - aApp;
      }}
      if (sortVal === 'company') {{
        return a.company.localeCompare(b.company);
      }}
      if (sortVal === 'newest') {{
        return (b.date_posted || '').localeCompare(a.date_posted || '');
      }}
      // default: tier priority, then newest
      const tierRank = {{ 'Quant / Prop Trading': 2, 'Tier 1 / Big Tech': 1 }};
      const rankA = tierRank[a.tier] || 0;
      const rankB = tierRank[b.tier] || 0;
      if (rankB !== rankA) return rankB - rankA;
      return (b.date_posted || '').localeCompare(a.date_posted || '');
    }});
  }}

  function renderListings(jobs) {{
    const container = document.getElementById('listings-container');
    const states = getAppStates();
    const totalJobs = jobs.length;
    const totalPages = Math.max(1, Math.ceil(totalJobs / PAGE_SIZE));

    document.getElementById('results-count').innerText = `Showing ${{totalJobs.toLocaleString()}} opportunities`;
    document.getElementById('current-page').innerText = currentPage;
    document.getElementById('total-pages').innerText = totalPages;
    document.getElementById('page-indicator').innerText = `${{currentPage}} / ${{totalPages}}`;

    document.getElementById('prev-btn').disabled = currentPage <= 1;
    document.getElementById('next-btn').disabled = currentPage >= totalPages;

    if (totalJobs === 0) {{
      container.innerHTML = `
        <div class="empty-state">
          <h3>No matching internship listings found</h3>
          <p style="margin-top: 8px;">Try clearing filters or searching for different keywords.</p>
        </div>
      `;
      return;
    }}

    const startIdx = (currentPage - 1) * PAGE_SIZE;
    const pageJobs = jobs.slice(startIdx, startIdx + PAGE_SIZE);

    container.innerHTML = pageJobs.map(job => {{
      const st = states[job.id] || 'none';
      const isApplied = st === 'applied' || st === 'interviewing' || st === 'offer';

      let catBadgeClass = 'badge-swe';
      if (job.category === 'AI/ML/Data') catBadgeClass = 'badge-ai';
      else if (job.category === 'Quant') catBadgeClass = 'badge-quant';
      else if (job.category === 'Hardware') catBadgeClass = 'badge-hw';
      else if (job.category === 'Product') catBadgeClass = 'badge-pm';

      return `
        <div class="job-card ${{isApplied ? 'is-applied' : ''}}">
          <div>
            <div class="card-header">
              <div>
                <div class="company-name">${{escapeHtml(job.company)}}</div>
                <div class="job-title">${{escapeHtml(job.title)}}</div>
              </div>
            </div>

            <div class="badges">
              <span class="badge ${{catBadgeClass}}">${{job.category}}</span>
              ${{job.tier === 'Tier 1 / Big Tech' ? '<span class="badge badge-tier1">Tier 1 Big Tech</span>' : ''}}
              ${{job.tier === 'Quant / Prop Trading' ? '<span class="badge badge-quant">Elite Quant</span>' : ''}}
              ${{job.is_remote ? '<span class="badge badge-remote">Remote</span>' : ''}}
              ${{job.sponsorship && job.sponsorship !== 'Other' ? `<span class="badge" style="background: rgba(255,255,255,0.08); color: #cbd5e1;">${{escapeHtml(job.sponsorship)}}</span>` : ''}}
            </div>

            <div class="card-meta">
              <div class="meta-row">&#128205; ${{escapeHtml(job.locations)}}</div>
              <div class="meta-row">&#128197; Terms: ${{escapeHtml(job.terms.join(', '))}} &bull; Posted: ${{job.date_posted}}</div>
              ${{job.degrees && job.degrees.length ? `<div class="meta-row">&#127891; Degree: ${{escapeHtml(job.degrees.join(', '))}}</div>` : ''}}
            </div>
          </div>

          <div class="card-footer">
            <div class="apply-links">
              <a href="${{job.apply_url}}" target="_blank" rel="noopener noreferrer" class="apply-btn apply-btn-direct">
                Apply Direct &nearr;
              </a>
              ${{job.simplify_url ? `
                <a href="${{job.simplify_url}}" target="_blank" rel="noopener noreferrer" class="apply-btn apply-btn-simplify">
                  1-Click &nearr;
                </a>
              ` : ''}}
            </div>

            <select class="status-select ${{isApplied ? 'applied' : ''}}" onchange="setAppState('${{job.id}}', this.value)">
              <option value="none" ${{st === 'none' ? 'selected' : ''}}>Not Applied</option>
              <option value="applied" ${{st === 'applied' ? 'selected' : ''}}>Applied &#10003;</option>
              <option value="interviewing" ${{st === 'interviewing' ? 'selected' : ''}}>Interviewing &#127919;</option>
              <option value="offer" ${{st === 'offer' ? 'selected' : ''}}>Offer &#127881;</option>
              <option value="rejected" ${{st === 'rejected' ? 'selected' : ''}}>Rejected</option>
            </select>
          </div>
        </div>
      `;
    }}).join('');
  }}

  function changePage(delta) {{
    currentPage += delta;
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
    applyFilters();
  }}

  function applyFilters() {{
    const filtered = getFilteredJobs();
    const sorted = sortJobs(filtered);
    renderListings(sorted);
  }}

  function escapeHtml(str) {{
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }}

  function exportTrackedData() {{
    const states = getAppStates();
    const tracked = ALL_JOBS.filter(j => states[j.id]).map(j => ({{
      ...j,
      application_status: states[j.id]
    }}));
    const blob = new Blob([JSON.stringify(tracked, null, 2)], {{ type: 'application/json' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `my_summer2027_applications_${{new Date().toISOString().split('T')[0]}}.json`;
    a.click();
  }}

  // Initialize
  updateAppliedCounter();
  applyFilters();
</script>

</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated dashboard at {html_path} ({len(html_content):,} bytes)")

if __name__ == "__main__":
    build_dashboard()
