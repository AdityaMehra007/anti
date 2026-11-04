"""
Builds the enhanced Bengaluru Startup Intelligence Cockpit.
"""

import json

with open('data/bangalorestartupmap_startups.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

compact_map_items = []
for item in items:
    cleaned = {k: v for k, v in item.items() if v != "$undefined"}
    compact_map_items.append({
        "n": cleaned.get("name", ""),
        "k": cleaned.get("kind", "startup"),
        "sec": cleaned.get("sector") or ("VC / Investor" if cleaned.get("kind") == "vc" else "Tech"),
        "stg": cleaned.get("stage") or ("Fund" if cleaned.get("kind") == "vc" else "Early Stage"),
        "area": cleaned.get("area") or "Bengaluru",
        "addr": cleaned.get("hsr_location") or "",
        "lat": cleaned.get("lat"),
        "lng": cleaned.get("lng"),
        "web": cleaned.get("website") or "",
        "tag": cleaned.get("tagline") or "",
        "desc": cleaned.get("description") or "",
        "fnd": cleaned.get("founders") or "",
        "fl": cleaned.get("founder_links") or [],
        "t": cleaned.get("tags") or [],
        "yr": cleaned.get("founded_year")
    })

with open('bengaluru_startup_intelligence_cockpit.html', 'r', encoding='utf-8') as f:
    cockpit_html = f.read()

# Update top metrics in header and metrics grid
old_metrics = """        <!-- Top Metrics Cards -->
        <div class="metrics-grid">
            <div class="metric-card cyan">
                <div class="metric-label">Live Priority Jobs</div>
                <div class="metric-value">75</div>
                <div class="metric-desc">Audited & scored non-sales leads</div>
            </div>
            <div class="metric-card emerald">
                <div class="metric-label">Curated Startups</div>
                <div class="metric-value">500</div>
                <div class="metric-desc">Bangalore Top 500 Curated Tech Unicorns</div>
            </div>
            <div class="metric-card blue">
                <div class="metric-label">Corporate Directory</div>
                <div class="metric-value">5,000</div>
                <div class="metric-desc">Bengaluru verified employers & careers</div>
            </div>
            <div class="metric-card purple">
                <div class="metric-label">Vetted Funding Rounds</div>
                <div class="metric-value">6</div>
                <div class="metric-desc">Capital rounds (C-CAMP, Credfix, etc.)</div>
            </div>
            <div class="metric-card amber">
                <div class="metric-label">Audit Changes</div>
                <div class="metric-value">234</div>
                <div class="metric-desc">Continuous chronological delta logs</div>
            </div>
        </div>"""

new_metrics = """        <!-- Top Metrics Cards -->
        <div class="metrics-grid">
            <div class="metric-card cyan">
                <div class="metric-label">Live Priority Jobs</div>
                <div class="metric-value">75</div>
                <div class="metric-desc">Scored non-sales BBA leads</div>
            </div>
            <div class="metric-card emerald">
                <div class="metric-label">Ecosystem Entities</div>
                <div class="metric-value">1,085</div>
                <div class="metric-desc">1,011 Startups + 74 VCs indexed</div>
            </div>
            <div class="metric-card blue">
                <div class="metric-label">GPS Mapped Pins</div>
                <div class="metric-value">699</div>
                <div class="metric-desc">Geocoded latitude & longitude coords</div>
            </div>
            <div class="metric-card purple">
                <div class="metric-label">Venture Capital Funds</div>
                <div class="metric-value">74</div>
                <div class="metric-desc">Top Bengaluru investors & partners</div>
            </div>
            <div class="metric-card amber">
                <div class="metric-label">Continuous Deltas</div>
                <div class="metric-value">235</div>
                <div class="metric-desc">Ecosystem audit & ingestion deltas</div>
            </div>
        </div>"""

if '<div class="logo-subtitle">Apex Career Operating System · 500 Startups · 5,000 Employers · 75 Priority Leads</div>' in cockpit_html:
    cockpit_html = cockpit_html.replace(
        '<div class="logo-subtitle">Apex Career Operating System · 500 Startups · 5,000 Employers · 75 Priority Leads</div>',
        '<div class="logo-subtitle">Apex Career Operating System · 1,085 Startups & VCs · 75 Priority Jobs · 699 GPS Pins</div>'
    )

if old_metrics in cockpit_html:
    cockpit_html = cockpit_html.replace(old_metrics, new_metrics)

# Add new tab button in tabs-nav
old_tabs_nav = """        <!-- Navigation Tabs -->
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab('jobs')">🎯 Live Priority Jobs (75)</button>
            <button class="tab-btn" onclick="switchTab('startups500')">🚀 Bangalore Top 500 Startups</button>
            <button class="tab-btn" onclick="switchTab('packages')">📦 Staged Application Packages</button>
            <button class="tab-btn" onclick="switchTab('briefing')">📰 Daily Intelligence Briefing</button>
            <button class="tab-btn" onclick="switchTab('funding')">💰 Funding & Investors</button>
            <button class="tab-btn" onclick="switchTab('changelog')">📜 Chronological Change Log</button>
        </div>"""

new_tabs_nav = """        <!-- Navigation Tabs -->
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab('jobs')">🎯 Live Priority Jobs (75)</button>
            <button class="tab-btn" onclick="switchTab('startupmap')">🗺️ Bangalore Startup Map (1,085)</button>
            <button class="tab-btn" onclick="switchTab('startups500')">🚀 Top 500 Startups</button>
            <button class="tab-btn" onclick="switchTab('packages')">📦 Staged Application Packages</button>
            <button class="tab-btn" onclick="switchTab('briefing')">📰 Daily Intelligence Briefing</button>
            <button class="tab-btn" onclick="switchTab('funding')">💰 Funding & Investors</button>
            <button class="tab-btn" onclick="switchTab('changelog')">📜 Chronological Change Log</button>
        </div>"""

if old_tabs_nav in cockpit_html:
    cockpit_html = cockpit_html.replace(old_tabs_nav, new_tabs_nav)

# Add CSS styles for the new Startup Map tab
map_styles = """
        /* Startup Map tab custom styling */
        .cluster-radar {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.75rem;
        }
        .cluster-radar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .cluster-radar-title {
            font-size: 1rem;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .corridor-pills {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }
        .corridor-pill {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .corridor-pill:hover {
            color: #fff;
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
        }
        .corridor-pill.active {
            background: var(--accent-cyan);
            color: #000;
            font-weight: 700;
            border-color: var(--accent-cyan);
        }
        .density-bar-container {
            height: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 9999px;
            display: flex;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }
        .density-segment { height: 100%; transition: opacity 0.2s; }
        .density-segment:hover { opacity: 0.8; }
        .density-legend {
            display: flex;
            gap: 1.25rem;
            flex-wrap: wrap;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        .density-item { display: flex; align-items: center; gap: 0.4rem; }
        .density-dot { width: 8px; height: 8px; border-radius: 2px; }

        .map-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.25rem;
            margin-top: 1.5rem;
        }
        .entity-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
            position: relative;
        }
        .entity-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        .entity-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
            gap: 0.5rem;
        }
        .entity-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
            line-height: 1.3;
        }
        .entity-badges {
            display: flex;
            gap: 0.35rem;
            flex-wrap: wrap;
        }
        .entity-badge {
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.2rem 0.5rem;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .badge-startup { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
        .badge-vc { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
        .badge-stage { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-sector { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

        .entity-loc {
            font-size: 0.8rem;
            color: var(--accent-cyan);
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }
        .entity-desc {
            font-size: 0.825rem;
            color: #cbd5e1;
            line-height: 1.5;
            margin-bottom: 0.75rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .entity-founders {
            font-size: 0.775rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }
        .entity-founders strong { color: #e2e8f0; }
        .founder-links-wrap {
            display: flex;
            gap: 0.35rem;
            flex-wrap: wrap;
            margin-top: 0.25rem;
        }
        .founder-link-pill {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #38bdf8;
            font-size: 0.725rem;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            text-decoration: none;
        }
        .founder-link-pill:hover { background: rgba(56, 189, 248, 0.2); }
        .entity-tags {
            display: flex;
            gap: 0.3rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }
        .tag-chip {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            color: #94a3b8;
            font-size: 0.7rem;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
        }
        .entity-footer {
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .geo-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #94a3b8;
        }
        .load-more-btn {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #000;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 0.9rem;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            margin: 2rem auto;
            display: block;
            transition: all 0.2s;
        }
        .load-more-btn:hover { transform: scale(1.02); opacity: 0.95; }
    </style>"""

if '/* Startup Map tab custom styling */' not in cockpit_html:
    cockpit_html = cockpit_html.replace('    </style>', map_styles + '\n    </style>')

# Tab Pane HTML for tab-startupmap
tab_startupmap_html = """
        <!-- TAB: Bangalore Startup Map (1,085 Directory) -->
        <div id="tab-startupmap" class="tab-pane">
            <div class="cluster-radar">
                <div class="cluster-radar-header">
                    <div class="cluster-radar-title">
                        <span>🗺️ Bengaluru Geographic Ecosystem Radar</span>
                        <span style="font-size: 0.8rem; font-weight: 500; color: var(--text-muted);">(Derived from bangalorestartupmap.com telemetry)</span>
                    </div>
                    <div id="mapEntityCount" style="font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan); font-weight: 600;">
                        Showing 1,085 Entities
                    </div>
                </div>

                <!-- Density Distribution Bar -->
                <div class="density-bar-container">
                    <div class="density-segment" style="width: 27%; background: #06b6d4;" title="HSR Layout: 291 startups (27%)"></div>
                    <div class="density-segment" style="width: 15%; background: #3b82f6;" title="Koramangala: 161 startups (15%)"></div>
                    <div class="density-segment" style="width: 11%; background: #a855f7;" title="Indiranagar: 114 startups (11%)"></div>
                    <div class="density-segment" style="width: 7%; background: #10b981;" title="Bellandur / ORR: 76 startups (7%)"></div>
                    <div class="density-segment" style="width: 4%; background: #f59e0b;" title="Whitefield: 42 startups (4%)"></div>
                    <div class="density-segment" style="width: 3%; background: #ec4899;" title="MG Road / CBD: 28 startups (3%)"></div>
                    <div class="density-segment" style="width: 3%; background: #6366f1;" title="Electronic City: 28 startups (3%)"></div>
                    <div class="density-segment" style="width: 30%; background: #64748b;" title="Other Hubs: 345 startups (30%)"></div>
                </div>

                <div class="density-legend">
                    <div class="density-item"><div class="density-dot" style="background: #06b6d4;"></div> HSR Layout (291)</div>
                    <div class="density-item"><div class="density-dot" style="background: #3b82f6;"></div> Koramangala (161)</div>
                    <div class="density-item"><div class="density-dot" style="background: #a855f7;"></div> Indiranagar (114)</div>
                    <div class="density-item"><div class="density-dot" style="background: #10b981;"></div> Bellandur (76)</div>
                    <div class="density-item"><div class="density-dot" style="background: #f59e0b;"></div> Whitefield (42)</div>
                    <div class="density-item"><div class="density-dot" style="background: #ec4899;"></div> MG Road (28)</div>
                    <div class="density-item"><div class="density-dot" style="background: #6366f1;"></div> Electronic City (28)</div>
                </div>

                <!-- Corridor Quick Filter Pills -->
                <div style="margin-top: 1.25rem;">
                    <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 0.5rem; font-weight: 600;">
                        Filter by Neighborhood Corridor:
                    </div>
                    <div class="corridor-pills" id="corridorPills">
                        <div class="corridor-pill active" onclick="selectCorridor('ALL', this)">All Hubs (1,085)</div>
                        <div class="corridor-pill" onclick="selectCorridor('HSR Layout', this)">HSR Layout (291)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Koramangala', this)">Koramangala (161)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Indiranagar', this)">Indiranagar (114)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Bellandur', this)">Bellandur (76)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Whitefield', this)">Whitefield (42)</div>
                        <div class="corridor-pill" onclick="selectCorridor('MG Road', this)">MG Road / CBD (28)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Electronic City', this)">Electronic City (28)</div>
                        <div class="corridor-pill" onclick="selectCorridor('Bannerghatta', this)">Bannerghatta (28)</div>
                        <div class="corridor-pill" onclick="selectCorridor('JP Nagar', this)">JP Nagar (18)</div>
                    </div>
                </div>
            </div>

            <!-- Filter Controls -->
            <div class="filter-bar">
                <input type="text" id="mapSearchInput" class="search-input" placeholder="Search 1,085 startups & VCs by name, founder, keyword, or tag (e.g. PhonePe, UPI, Seed, Blume)..." oninput="filterMapEntities()">
                <select id="mapKindFilter" class="filter-select" onchange="filterMapEntities()">
                    <option value="ALL">All Entities (1,085)</option>
                    <option value="startup">Startups Only (1,011)</option>
                    <option value="vc">VC & Investor Funds (74)</option>
                </select>
                <select id="mapSectorFilter" class="filter-select" onchange="filterMapEntities()">
                    <option value="ALL">All Sectors</option>
                    <option value="SaaS">SaaS (167)</option>
                    <option value="Deeptech">Deeptech (157)</option>
                    <option value="Fintech">Fintech (135)</option>
                    <option value="AI">AI & Machine Learning (117)</option>
                    <option value="Consumer">Consumer & Apps (108)</option>
                    <option value="Healthtech">Healthtech (89)</option>
                    <option value="D2C">D2C & Brands (59)</option>
                    <option value="Edtech">Edtech (47)</option>
                    <option value="Logistics">Logistics & Supply Chain (42)</option>
                    <option value="Gaming">Gaming & Media (19)</option>
                </select>
                <select id="mapStageFilter" class="filter-select" onchange="filterMapEntities()">
                    <option value="ALL">All Stages</option>
                    <option value="Bootstrapped">Bootstrapped</option>
                    <option value="Pre-seed">Pre-seed</option>
                    <option value="Seed">Seed</option>
                    <option value="Series A">Series A</option>
                    <option value="Series B">Series B</option>
                    <option value="Series C">Series C / C+</option>
                    <option value="Public">Public / Listed</option>
                    <option value="Acquired">Acquired</option>
                </select>
            </div>

            <!-- Grid of Cards -->
            <div class="map-grid" id="mapCardsGrid">
            </div>

            <button id="loadMoreMapBtn" class="load-more-btn" onclick="loadMoreMapEntities()" style="display: none;">
                Load More Entities
            </button>
        </div>
"""

if 'id="tab-startupmap"' not in cockpit_html:
    jobs_tab_end = '        </div>\n\n        <!-- TAB 2: Top 500 Startups -->'
    cockpit_html = cockpit_html.replace(jobs_tab_end, '        </div>\n' + tab_startupmap_html + '\n        <!-- TAB 2: Top 500 Startups -->')

# Embed compact JSON in script
compact_json_str = json.dumps(compact_map_items, ensure_ascii=False)

js_code = """
        // 1,085 Bangalore Startup Map Directory
        const mapDirectoryData = """ + compact_json_str + """;

        let currentCorridorFilter = 'ALL';
        let renderedMapCount = 0;
        const MAP_PAGE_SIZE = 60;
        let currentFilteredMapEntities = [];

        function selectCorridor(corridor, el) {
            currentCorridorFilter = corridor;
            document.querySelectorAll('#corridorPills .corridor-pill').forEach(p => p.classList.remove('active'));
            if (el) el.classList.add('active');
            filterMapEntities();
        }

        function filterMapEntities() {
            const query = (document.getElementById('mapSearchInput') ? document.getElementById('mapSearchInput').value : '').toLowerCase().trim();
            const kind = document.getElementById('mapKindFilter') ? document.getElementById('mapKindFilter').value : 'ALL';
            const sector = document.getElementById('mapSectorFilter') ? document.getElementById('mapSectorFilter').value : 'ALL';
            const stage = document.getElementById('mapStageFilter') ? document.getElementById('mapStageFilter').value : 'ALL';

            currentFilteredMapEntities = mapDirectoryData.filter(e => {
                // Corridor filter
                if (currentCorridorFilter !== 'ALL') {
                    const matchesArea = (e.area + " " + e.addr).toLowerCase().includes(currentCorridorFilter.toLowerCase());
                    if (!matchesArea) return false;
                }

                // Kind filter
                if (kind !== 'ALL' && e.k !== kind) return false;

                // Sector filter
                if (sector !== 'ALL' && !e.sec.toLowerCase().includes(sector.toLowerCase())) return false;

                // Stage filter
                if (stage !== 'ALL' && !e.stg.toLowerCase().includes(stage.toLowerCase())) return false;

                // Search query
                if (query) {
                    const tagStr = Array.isArray(e.t) ? e.t.join(" ") : "";
                    const searchBlob = (e.n + " " + e.sec + " " + e.area + " " + e.addr + " " + e.tag + " " + e.desc + " " + e.fnd + " " + tagStr).toLowerCase();
                    if (!searchBlob.includes(query)) return false;
                }

                return true;
            });

            // Update counter
            const counterEl = document.getElementById('mapEntityCount');
            if (counterEl) {
                counterEl.innerText = 'Showing ' + currentFilteredMapEntities.length + ' of ' + mapDirectoryData.length + ' Entities';
            }

            renderedMapCount = 0;
            const grid = document.getElementById('mapCardsGrid');
            if (grid) grid.innerHTML = '';
            renderNextMapBatch();
        }

        function renderNextMapBatch() {
            const grid = document.getElementById('mapCardsGrid');
            if (!grid) return;

            const nextBatch = currentFilteredMapEntities.slice(renderedMapCount, renderedMapCount + MAP_PAGE_SIZE);
            renderedMapCount += nextBatch.length;

            const fragment = document.createDocumentFragment();

            nextBatch.forEach(e => {
                const card = document.createElement('div');
                card.className = 'entity-card';

                const isVc = e.k === 'vc';
                const kindBadge = isVc ? '<span class="entity-badge badge-vc">💼 VC Fund</span>' : '<span class="entity-badge badge-startup">🚀 Startup</span>';
                const secBadge = '<span class="entity-badge badge-sector">' + (e.sec || 'Tech') + '</span>';
                const stgBadge = e.stg && e.stg !== '$undefined' && e.stg !== 'Fund' ? '<span class="entity-badge badge-stage">' + e.stg + '</span>' : '';

                // Founders & Links
                let foundersHtml = '';
                if (e.fnd && e.fnd !== '$undefined') {
                    foundersHtml = '<strong>' + (isVc ? 'Partners' : 'Founders') + ':</strong> ' + e.fnd;
                }
                let linksHtml = '';
                if (Array.isArray(e.fl) && e.fl.length > 0) {
                    linksHtml = '<div class="founder-links-wrap">' + e.fl.map(l => '<a href="' + l.url + '" target="_blank" class="founder-link-pill">🔗 ' + l.name + '</a>').join('') + '</div>';
                }

                // Tags
                let tagsHtml = '';
                if (Array.isArray(e.t) && e.t.length > 0) {
                    tagsHtml = '<div class="entity-tags">' + e.t.slice(0, 5).map(t => '<span class="tag-chip">#' + t + '</span>').join('') + '</div>';
                }

                // Geo GPS
                let geoHtml = '';
                if (e.lat && e.lng) {
                    geoHtml = '<span class="geo-badge">📍 ' + Number(e.lat).toFixed(4) + ', ' + Number(e.lng).toFixed(4) + '</span>';
                }

                // Website Link
                let webBtn = '';
                if (e.web) {
                    webBtn = '<a href="' + e.web + '" target="_blank" class="action-link" style="font-size: 0.8rem;">Visit Website →</a>';
                }

                card.innerHTML = `
                    <div>
                        <div class="entity-card-header">
                            <div class="entity-name">${e.n}</div>
                            <div class="entity-badges">
                                ${kindBadge}
                                ${secBadge}
                                ${stgBadge}
                            </div>
                        </div>

                        <div class="entity-loc">
                            <span>📍 <strong>${e.area}</strong>${e.addr ? ' · ' + e.addr : ''}${e.yr ? ' · Est. ' + e.yr : ''}</span>
                        </div>

                        ${e.tag ? '<div style="font-size: 0.85rem; font-weight: 600; color: #fff; margin-bottom: 0.4rem;">' + e.tag + '</div>' : ''}
                        ${e.desc ? '<div class="entity-desc">' + e.desc + '</div>' : ''}

                        ${foundersHtml ? '<div class="entity-founders">' + foundersHtml + linksHtml + '</div>' : ''}
                        ${tagsHtml}
                    </div>

                    <div class="entity-footer">
                        ${geoHtml}
                        ${webBtn}
                    </div>
                `;

                fragment.appendChild(card);
            });

            grid.appendChild(fragment);

            const loadMoreBtn = document.getElementById('loadMoreMapBtn');
            if (loadMoreBtn) {
                if (renderedMapCount < currentFilteredMapEntities.length) {
                    loadMoreBtn.style.display = 'block';
                    loadMoreBtn.innerText = 'Load More (' + (currentFilteredMapEntities.length - renderedMapCount) + ' remaining)';
                } else {
                    loadMoreBtn.style.display = 'none';
                }
            }
        }

        function loadMoreMapEntities() {
            renderNextMapBatch();
        }
"""

if 'const mapDirectoryData =' not in cockpit_html:
    cockpit_html = cockpit_html.replace('    <script>', '    <script>\n' + js_code)

# Ensure switchTab triggers filterMapEntities if needed
if "if (tabId === 'startupmap'" not in cockpit_html:
    cockpit_html = cockpit_html.replace(
        "function switchTab(tabId) {",
        """function switchTab(tabId) {
            if (tabId === 'startupmap' && currentFilteredMapEntities.length === 0) {
                setTimeout(filterMapEntities, 50);
            }"""
    )

with open('bengaluru_startup_intelligence_cockpit.html', 'w', encoding='utf-8') as f:
    f.write(cockpit_html)

print("bengaluru_startup_intelligence_cockpit.html updated successfully with 1,085 Bangalore Startup Map Directory!")
