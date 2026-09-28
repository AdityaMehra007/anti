import json
import os

def generate_html():
    target_dir = os.path.join(os.path.dirname(__file__), 'remote-resources')
    json_path = os.path.join(target_dir, 'remote_ecosystem_master.json')
    out_html = os.path.join(target_dir, 'remote_jobs_explorer.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    json_str = json.dumps(master_data['ecosystem'], ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awesome Remote Job Intelligence & Scored Ecosystem Explorer</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #111827;
      --card-border: #1f2937;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --accent: #818cf8;
      --gold: #fbbf24;
      --border-color: #374151;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    body {{
      background: var(--bg);
      color: var(--text-main);
      padding: 24px;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1440px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 18px;
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    h1 {{
      font-size: 26px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    h1 span {{
      color: var(--primary);
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 4px;
    }}
    .header-stats {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .stat-pill {{
      background: #1e1b4b;
      border: 1px solid #4338ca;
      color: #a5b4fc;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
    }}
    .stat-gold {{
      background: #451a03;
      border-color: #b45309;
      color: #fde68a;
    }}
    .controls {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 24px;
      background: #0f172a;
      padding: 20px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
    }}
    .search-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .search-input {{
      flex: 1;
      min-width: 280px;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 15px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }}
    .sort-select {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      cursor: pointer;
    }}
    .filter-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .filter-label {{
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-right: 4px;
    }}
    .btn-pill {{
      background: var(--card-bg);
      color: var(--text-muted);
      border: 1px solid var(--border-color);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 12.5px;
      cursor: pointer;
      transition: all 0.15s ease-in-out;
      user-select: none;
    }}
    .btn-pill:hover {{
      color: #fff;
      border-color: var(--primary);
    }}
    .btn-pill.active {{
      background: var(--primary);
      color: #0b1120;
      border-color: var(--primary);
      font-weight: 600;
    }}
    .btn-tag.active {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      font-weight: 600;
    }}
    .meta-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      font-size: 14px;
      color: var(--text-muted);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: transform 0.15s, border-color 0.15s;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: #38bdf888;
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .score-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      background: #064e3b;
      color: #4ade80;
      border: 1px solid #059669;
    }}
    .score-badge.tier1 {{
      background: #78350f;
      color: #fde047;
      border-color: #ca8a04;
    }}
    .section-badge {{
      font-size: 11px;
      padding: 2px 8px;
      background: #1e293b;
      color: #94a3b8;
      border-radius: 6px;
      white-space: nowrap;
      border: 1px solid #334155;
    }}
    .card-title {{
      font-size: 17px;
      font-weight: 600;
      color: #fff;
      text-decoration: none;
      display: inline-block;
      margin-bottom: 6px;
    }}
    .card-title:hover {{
      color: var(--primary);
      text-decoration: underline;
    }}
    .tier-label {{
      font-size: 11.5px;
      color: #a5b4fc;
      margin-bottom: 8px;
      font-weight: 500;
    }}
    .card-desc {{
      color: #cbd5e1;
      font-size: 13.5px;
      margin-bottom: 12px;
      flex-grow: 1;
      word-break: break-word;
    }}
    .tags-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 14px;
    }}
    .tag {{
      font-size: 11px;
      background: #1e1b4b;
      color: #c7d2fe;
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid #3730a3;
    }}
    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #1e293b;
      padding-top: 12px;
      margin-top: auto;
    }}
    .links-group {{
      display: flex;
      gap: 8px;
    }}
    .btn-link {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: var(--primary);
      text-decoration: none;
      padding: 4px 8px;
      border-radius: 4px;
      background: #0f2744;
      border: 1px solid #1e3a8a;
      transition: background 0.15s;
    }}
    .btn-link:hover {{
      background: #1e3a8a;
      color: #fff;
    }}
    .btn-career {{
      color: #4ade80;
      background: #064e3b;
      border-color: #047857;
    }}
    .btn-career:hover {{
      background: #059669;
      color: #fff;
    }}
    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
      grid-column: 1 / -1;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-top">
        <div>
          <h1><span>Scored</span> Remote Ecosystem Intelligence</h1>
          <div class="subtitle">520 Curated Resources Evaluated with Antigravity Decision Matrix V22</div>
        </div>
        <div class="header-stats">
          <div class="stat-pill stat-gold">Top 100 Scored Targets</div>
          <div class="stat-pill" id="totalPill">520 Scored Entities</div>
        </div>
      </div>
    </header>

    <div class="controls">
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="Search companies, job boards, tags, skills, or keywords..." autofocus>
        <select id="sortSelect" class="sort-select">
          <option value="score_desc">Sort: Highest Score First</option>
          <option value="score_asc">Sort: Lowest Score First</option>
          <option value="alpha_asc">Sort: Name (A-Z)</option>
          <option value="category">Sort: Category</option>
        </select>
      </div>

      <div class="filter-group">
        <span class="filter-label">Category:</span>
        <button class="btn-pill active" data-category="ALL">All Categories (520)</button>
        <button class="btn-pill" data-category='Companies with "remote DNA"'>Companies (232)</button>
        <button class="btn-pill" data-category="Job boards">Job Boards (74)</button>
        <button class="btn-pill" data-category="Job boards aggregators">Aggregators (15)</button>
        <button class="btn-pill" data-category="Tools">Tools & Stack (51)</button>
        <button class="btn-pill" data-category="Interviewing">Interviewing (14)</button>
        <button class="btn-pill" data-category="Relocation Incentives">Relocation Grants (6)</button>
        <button class="btn-pill" data-category="Housing">Coliving / Housing (14)</button>
        <button class="btn-pill" data-category="Articles & Posts">Articles & Guides (65)</button>
      </div>

      <div class="filter-group">
        <span class="filter-label">Filter:</span>
        <button class="btn-pill btn-tag active" data-tag="ALL">All</button>
        <button class="btn-pill btn-tag" data-tag="TIER1">⭐ Tier 1 Elite Only</button>
        <button class="btn-pill btn-tag" data-tag="AI/ML">AI / ML</button>
        <button class="btn-pill btn-tag" data-tag="4-Day Week">4-Day Week</button>
        <button class="btn-pill btn-tag" data-tag="DevOps/Cloud">DevOps / Cloud</button>
        <button class="btn-pill btn-tag" data-tag="Web3/Crypto">Web3 / Crypto</button>
        <button class="btn-pill btn-tag" data-tag="Backend">Backend</button>
        <button class="btn-pill btn-tag" data-tag="Frontend">Frontend</button>
        <button class="btn-pill btn-tag" data-tag="LATAM">LATAM</button>
        <button class="btn-pill btn-tag" data-tag="Europe">Europe</button>
      </div>
    </div>

    <div class="meta-bar">
      <div id="resultCount">Showing 0 matching resources</div>
      <div>Multi-Metric Algorithmic Scoring V22</div>
    </div>

    <div class="grid" id="resourceGrid"></div>
  </div>

  <script>
    const RAW_DATA = {json_str};

    const ALL_ITEMS = [];
    Object.keys(RAW_DATA).forEach(section => {{
      RAW_DATA[section].forEach(item => {{
        ALL_ITEMS.push({{
          ...item,
          sectionName: section,
          compositeScore: (item.scoring && item.scoring.composite_score) ? item.scoring.composite_score : 70.0,
          strategicTier: (item.scoring && item.scoring.strategic_tier) ? item.scoring.strategic_tier : 'Standard'
        }});
      }});
    }});

    let activeCategory = 'ALL';
    let activeTag = 'ALL';
    let searchQuery = '';
    let sortMode = 'score_desc';

    const searchInput = document.getElementById('searchInput');
    const sortSelect = document.getElementById('sortSelect');
    const resourceGrid = document.getElementById('resourceGrid');
    const resultCount = document.getElementById('resultCount');
    const totalPill = document.getElementById('totalPill');

    totalPill.textContent = `${{ALL_ITEMS.length}} Scored Entities`;

    function render() {{
      const query = searchQuery.trim().toLowerCase();

      let filtered = ALL_ITEMS.filter(item => {{
        if (activeCategory !== 'ALL' && item.sectionName !== activeCategory) {{
          return false;
        }}
        if (activeTag === 'TIER1') {{
          if (!item.strategicTier.includes('Tier 1') && item.compositeScore < 90) {{
            return false;
          }}
        }} else if (activeTag !== 'ALL') {{
          const tags = (item.tags || []).map(t => t.toLowerCase());
          if (!tags.includes(activeTag.toLowerCase())) {{
            return false;
          }}
        }}
        if (query) {{
          const content = `${{item.title}} ${{item.description || ''}} ${{item.url || ''}} ${{(item.tags || []).join(' ')}} ${{item.strategicTier}}`.toLowerCase();
          if (!content.includes(query)) {{
            return false;
          }}
        }}
        return true;
      }});

      // Sort
      filtered.sort((a, b) => {{
        if (sortMode === 'score_desc') return b.compositeScore - a.compositeScore;
        if (sortMode === 'score_asc') return a.compositeScore - b.compositeScore;
        if (sortMode === 'alpha_asc') return a.title.localeCompare(b.title);
        if (sortMode === 'category') return a.sectionName.localeCompare(b.sectionName);
        return 0;
      }});

      resultCount.textContent = `Showing ${{filtered.length}} of ${{ALL_ITEMS.length}} scored resources`;

      if (filtered.length === 0) {{
        resourceGrid.innerHTML = `
          <div class="empty-state">
            <h3>No matching resources found</h3>
            <p>Try clearing search queries or switching filters.</p>
          </div>
        `;
        return;
      }}

      resourceGrid.innerHTML = filtered.map(item => {{
        const tagsHtml = (item.tags || []).map(t => `<span class="tag">${{t}}</span>`).join('');
        const careersBtn = item.careers_url 
          ? `<a href="${{item.careers_url}}" target="_blank" rel="noopener" class="btn-link btn-career">Careers &#8599;</a>` 
          : '';
        const isTier1 = item.strategicTier.includes('Tier 1') || item.compositeScore >= 92;

        return `
          <div class="card">
            <div>
              <div class="card-top">
                <span class="score-badge ${{isTier1 ? 'tier1' : ''}}">★ ${{item.compositeScore}} / 100</span>
                <span class="section-badge">${{item.sub_section || item.sectionName}}</span>
              </div>
              <a href="${{item.url}}" target="_blank" rel="noopener" class="card-title">${{item.title}}</a>
              <div class="tier-label">${{item.strategicTier}}</div>
              <div class="card-desc">${{item.description || 'Curated remote work intelligence.'}}</div>
              <div class="tags-container">${{tagsHtml}}</div>
            </div>
            <div class="card-footer">
              <div class="links-group">
                <a href="${{item.url}}" target="_blank" rel="noopener" class="btn-link">Visit Website &#8599;</a>
                ${{careersBtn}}
              </div>
            </div>
          </div>
        `;
      }}).join('');
    }}

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      render();
    }});

    sortSelect.addEventListener('change', (e) => {{
      sortMode = e.target.value;
      render();
    }});

    document.querySelectorAll('[data-category]').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('[data-category]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeCategory = btn.getAttribute('data-category');
        render();
      }});
    }});

    document.querySelectorAll('[data-tag]').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('[data-tag]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeTag = btn.getAttribute('data-tag');
        render();
      }});
    }});

    render();
  </script>
</body>
</html>
"""
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated scored HTML explorer at: {out_html}")

if __name__ == '__main__':
    generate_html()
