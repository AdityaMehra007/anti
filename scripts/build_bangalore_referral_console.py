"""
Builder script to generate standalone BANGALORE_LIVE_REFERRAL_CONSOLE.html
"""

import os
import json

def build_console():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(root_dir, 'data', 'bangalore_live_referral_dockets.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        dockets_data = json.load(f)
        
    json_payload = json.dumps(dockets_data, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bengaluru Live Referral Strike Console - Aditya Mehra</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-tertiary: #1f2937;
            --border-color: #374151;
            --accent-blue: #3b82f6;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --card-hover: rgba(59, 130, 246, 0.08);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        /* Header */
        header {{
            background: linear-gradient(180deg, rgba(31, 41, 55, 0.8) 0%, rgba(17, 24, 39, 0.95) 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 2rem;
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(12px);
        }}

        .header-content {{
            max-width: 1440px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .logo-area {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .badge-live {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        h1 {{
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        .subtitle {{
            font-size: 0.825rem;
            color: var(--text-muted);
        }}

        /* Metrics Bar */
        .metrics-grid {{
            display: flex;
            gap: 1.25rem;
            align-items: center;
        }}

        .metric-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-align: right;
        }}

        .metric-val {{
            font-size: 1.15rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-blue);
        }}

        .metric-lbl {{
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Main Container */
        main {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
            width: 100%;
            flex: 1;
        }}

        /* Control Panel */
        .controls {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }}

        .search-row {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-box input:focus {{
            border-color: var(--accent-blue);
        }}

        .search-icon {{
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .filter-group {{
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-right: 0.25rem;
            font-weight: 600;
            min-width: 75px;
        }}

        .pill-btn {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            font-size: 0.785rem;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .pill-btn:hover {{
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
            border-color: var(--accent-blue);
        }}

        .pill-btn.active {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
            font-weight: 600;
        }}

        /* Target Companies & Contacts Grid */
        .targets-container {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .company-block {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .company-block:hover {{
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
        }}

        .company-header {{
            background: var(--bg-tertiary);
            padding: 1rem 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 0.75rem;
        }}

        .company-title-area {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .company-name {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
        }}

        .hub-tag {{
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
        }}

        .role-tag {{
            background: rgba(16, 185, 129, 0.15);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .job-link-btn {{
            color: var(--accent-blue);
            text-decoration: none;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .job-link-btn:hover {{
            text-decoration: underline;
        }}

        /* Contacts Grid */
        .contacts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 1rem;
            padding: 1.25rem;
        }}

        @media (max-width: 640px) {{
            .contacts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .contact-card {{
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
            position: relative;
            transition: transform 0.15s, border-color 0.15s;
        }}

        .contact-card:hover {{
            border-color: rgba(59, 130, 246, 0.5);
            transform: translateY(-2px);
        }}

        .contact-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.5rem;
        }}

        .contact-name {{
            font-size: 1rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .contact-role {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.15rem;
        }}

        .tag-recruiter {{
            background: rgba(245, 158, 11, 0.15);
            color: #fcd34d;
            border: 1px solid rgba(245, 158, 11, 0.3);
            font-size: 0.65rem;
            font-weight: 600;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            text-transform: uppercase;
        }}

        /* Action Buttons */
        .actions-row {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .btn-action {{
            flex: 1;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.775rem;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            transition: all 0.15s;
            text-decoration: none;
            border: none;
        }}

        .btn-primary {{
            background: var(--accent-blue);
            color: #ffffff;
        }}

        .btn-primary:hover {{
            background: #2563eb;
        }}

        .btn-secondary {{
            background: var(--bg-tertiary);
            color: var(--text-main);
            border: 1px solid var(--border-color);
        }}

        .btn-secondary:hover {{
            background: #374151;
            border-color: #4b5563;
        }}

        .btn-emerald {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .btn-emerald:hover {{
            background: rgba(16, 185, 129, 0.25);
        }}

        /* Status Dropdown */
        .status-select {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            font-size: 0.75rem;
            padding: 0.35rem 0.6rem;
            border-radius: 6px;
            cursor: pointer;
            outline: none;
        }}

        .status-select.contacted {{
            border-color: var(--accent-amber);
            color: var(--accent-amber);
        }}

        .status-select.referred {{
            border-color: var(--accent-emerald);
            color: var(--accent-emerald);
        }}

        /* Toast Alert */
        #toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--accent-emerald);
            color: #ffffff;
            padding: 0.85rem 1.5rem;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            display: none;
            z-index: 1000;
            animation: slideUp 0.2s ease-out;
        }}

        @keyframes slideUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo-area">
                <span class="badge-live">LIVE</span>
                <div>
                    <h1>Bengaluru Referral Strike Console</h1>
                    <div class="subtitle">Aditya Mehra | Verified 1-Click LinkedIn Outreach Dispatcher</div>
                </div>
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-val" id="totalCompanies">45</div>
                    <div class="metric-lbl">Target Companies</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" id="totalContacts">189</div>
                    <div class="metric-lbl">Curated Contacts</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" id="contactedCount">0</div>
                    <div class="metric-lbl">Contacted Today</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" id="referredCount">0</div>
                    <div class="metric-lbl">Referrals Logged</div>
                </div>
            </div>
        </div>
    </header>

    <main>
        <section class="controls">
            <div class="search-row">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchInput" placeholder="Search by name, role, company, or corridor...">
                </div>
                <div class="filter-group">
                    <span class="filter-label">Corridor:</span>
                    <button class="pill-btn active" onclick="filterCorridor('ALL', this)">All Corridors</button>
                    <button class="pill-btn" onclick="filterCorridor('Outer Ring Road', this)">Outer Ring Road</button>
                    <button class="pill-btn" onclick="filterCorridor('Bellandur', this)">Bellandur</button>
                    <button class="pill-btn" onclick="filterCorridor('Manyata', this)">Manyata</button>
                    <button class="pill-btn" onclick="filterCorridor('Whitefield', this)">Whitefield</button>
                    <button class="pill-btn" onclick="filterCorridor('Domlur', this)">Domlur</button>
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Company:</span>
                <button class="pill-btn company-pill active" onclick="filterCompany('ALL', this)">All Companies</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Accenture', this)">Accenture</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Deloitte', this)">Deloitte</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Goldman Sachs', this)">Goldman Sachs</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Amazon', this)">Amazon</button>
                <button class="pill-btn company-pill" onclick="filterCompany('IBM', this)">IBM</button>
                <button class="pill-btn company-pill" onclick="filterCompany('JPMorgan', this)">JPMorganChase</button>
                <button class="pill-btn company-pill" onclick="filterCompany('KPMG', this)">KPMG</button>
                <button class="pill-btn company-pill" onclick="filterCompany('PhonePe', this)">PhonePe</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Delhivery', this)">Delhivery</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Domain:</span>
                <button class="pill-btn domain-pill active" onclick="filterDomain('ALL', this)">All Domains</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Operations', this)">Business Operations</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Supply Chain', this)">Supply Chain & Logistics</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Advisory', this)">Advisory & Risk</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Trade', this)">Trade Finance & Markets</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Business Development', this)">Merchant BD & Commercial</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Status:</span>
                <button class="pill-btn active" onclick="filterStatus('ALL', this)">All</button>
                <button class="pill-btn" onclick="filterStatus('Pending', this)">Pending</button>
                <button class="pill-btn" onclick="filterStatus('Contacted', this)">Contacted</button>
                <button class="pill-btn" onclick="filterStatus('Referral Submitted', this)">Referral Submitted</button>
            </div>
        </section>

        <section class="targets-container" id="targetsContainer">
            <!-- Dynamic Render -->
        </section>
    </main>

    <div id="toast">Copied to clipboard!</div>

    <script>
        const dockets = {json_payload};

        let activeCorridor = 'ALL';
        let activeCompany = 'ALL';
        let activeDomain = 'ALL';
        let activeStatus = 'ALL';
        let searchTerm = '';

        function getStatus(contactName) {{
            return localStorage.getItem('status_' + contactName) || 'Pending';
        }}

        function setStatus(contactName, status) {{
            localStorage.setItem('status_' + contactName, status);
            updateMetrics();
            render();
        }}

        function copyText(text, label) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast(`✓ Copied ${{label}} to clipboard!`);
            }});
        }}

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => {{
                t.style.display = 'none';
            }}, 2400);
        }}

        function filterCorridor(corridor, btn) {{
            activeCorridor = corridor;
            btn.parentNode.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            render();
        }}

        function filterCompany(company, btn) {{
            activeCompany = company;
            btn.parentNode.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            render();
        }}

        function filterDomain(domain, btn) {{
            activeDomain = domain;
            btn.parentNode.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            render();
        }}

        function filterStatus(status, btn) {{
            activeStatus = status;
            btn.parentNode.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            render();
        }}

        document.getElementById('searchInput').addEventListener('input', (e) => {{
            searchTerm = e.target.value.toLowerCase();
            render();
        }});

        function updateMetrics() {{
            let contacted = 0;
            let referred = 0;
            let total = 0;

            dockets.forEach(t => {{
                t.contacts.forEach(c => {{
                    total++;
                    const s = getStatus(c.full_name);
                    if (s === 'Contacted') contacted++;
                    if (s === 'Referral Submitted') referred++;
                }});
            }});

            document.getElementById('totalContacts').innerText = total;
            document.getElementById('contactedCount').innerText = contacted;
            document.getElementById('referredCount').innerText = referred;
        }}

        function render() {{
            const container = document.getElementById('targetsContainer');
            container.innerHTML = '';

            let matchedCompanyCount = 0;

            dockets.forEach((target, tIdx) => {{
                // Corridor filter
                if (activeCorridor !== 'ALL') {{
                    const hay = (target.corridor + ' ' + target.hub).toLowerCase();
                    if (!hay.includes(activeCorridor.toLowerCase())) return;
                }}

                // Company filter
                if (activeCompany !== 'ALL') {{
                    const hay = (target.canonical_company + ' ' + target.company).toLowerCase();
                    if (!hay.includes(activeCompany.toLowerCase())) return;
                }}

                // Domain filter
                if (activeDomain !== 'ALL') {{
                    const hay = target.job_title.toLowerCase();
                    if (!hay.includes(activeDomain.toLowerCase())) return;
                }}

                // Filter contacts
                const filteredContacts = target.contacts.filter(c => {{
                    const s = getStatus(c.full_name);
                    if (activeStatus !== 'ALL' && s !== activeStatus) return false;

                    if (searchTerm) {{
                        const haystack = (c.full_name + ' ' + c.position + ' ' + target.company + ' ' + target.corridor + ' ' + target.job_title).toLowerCase();
                        if (!haystack.includes(searchTerm)) return false;
                    }}
                    return true;
                }});

                if (filteredContacts.length === 0) return;
                matchedCompanyCount++;

                const compEl = document.createElement('div');
                compEl.className = 'company-block';
                compEl.innerHTML = `
                    <div class="company-header">
                        <div class="company-title-area">
                            <span class="company-name">${{target.canonical_company}}</span>
                            <span class="hub-tag">${{target.hub}} (${{target.corridor}})</span>
                            <span class="role-tag">${{target.job_title}}</span>
                        </div>
                        <a href="${{target.job_url}}" target="_blank" class="job-link-btn">
                            Official Careers / Req Link ↗
                        </a>
                    </div>
                    <div class="contacts-grid" id="grid_${{tIdx}}"></div>
                `;

                const grid = compEl.querySelector(`#grid_${{tIdx}}`);

                filteredContacts.forEach(contact => {{
                    const curStatus = getStatus(contact.full_name);
                    const card = document.createElement('div');
                    card.className = 'contact-card';
                    card.innerHTML = `
                        <div class="contact-top">
                            <div>
                                <div class="contact-name">${{contact.full_name}}</div>
                                <div class="contact-role">${{contact.position}}</div>
                            </div>
                            <div style="display: flex; gap: 0.35rem; align-items: center;">
                                ${{contact.is_recruiter ? '<span class="tag-recruiter">Recruiter</span>' : ''}}
                                <select class="status-select ${{curStatus.toLowerCase().replace(' ', '-')}}" onchange="setStatus('${{contact.full_name}}', this.value)">
                                    <option value="Pending" ${{curStatus === 'Pending' ? 'selected' : ''}}>Pending</option>
                                    <option value="Contacted" ${{curStatus === 'Contacted' ? 'selected' : ''}}>Contacted</option>
                                    <option value="Referral Submitted" ${{curStatus === 'Referral Submitted' ? 'selected' : ''}}>Referral Submitted</option>
                                </select>
                            </div>
                        </div>

                        <div class="actions-row">
                            <a href="${{contact.linkedin_url}}" target="_blank" class="btn-action btn-primary">
                                Open LinkedIn ↗
                            </a>
                            <button class="btn-action btn-secondary" onclick="copyText(\\x60${{contact.connection_note.replace(/`/g, '\\\\`').replace(/\\$/g, '\\\\$')}}\\x60, 'Connection Note')">
                                Copy 300c Note
                            </button>
                        </div>
                        <div class="actions-row">
                            <button class="btn-action btn-emerald" onclick="copyText(\\x60${{contact.referral_ask.replace(/`/g, '\\\\`').replace(/\\$/g, '\\\\$')}}\\x60, 'Referral Ask')">
                                Copy Referral Ask
                            </button>
                            <button class="btn-action btn-secondary" onclick="copyText(\\x60${{contact.referral_docket.replace(/`/g, '\\\\`').replace(/\\$/g, '\\\\$')}}\\x60, 'Referral Docket')">
                                Copy Docket
                            </button>
                        </div>
                    `;
                    grid.appendChild(card);
                }});

                container.appendChild(compEl);
            }});

            document.getElementById('totalCompanies').innerText = matchedCompanyCount;
        }}

        // Initial render
        updateMetrics();
        render();
    </script>
</body>
</html>
"""

    console_root = os.path.join(root_dir, 'BANGALORE_LIVE_REFERRAL_CONSOLE.html')
    with open(console_root, 'w', encoding='utf-8') as f:
        f.write(html_content)

    console_project = os.path.join(root_dir, 'teamwork_projects', 'bangalore_referral_strike', 'index.html')
    with open(console_project, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Generated {console_root} and {console_project} successfully.")

if __name__ == '__main__':
    build_console()
