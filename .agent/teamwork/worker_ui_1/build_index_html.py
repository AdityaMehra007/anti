import json
import os

ROOT_DIR = r"e:\anti"
PROJECT_DIR = os.path.join(ROOT_DIR, "teamwork_projects", "bangalore_referral_strike")
DOCKETS_PATH = os.path.join(PROJECT_DIR, "bangalore_live_referral_dockets.json")
INDEX_PATH = os.path.join(PROJECT_DIR, "index.html")

with open(DOCKETS_PATH, "r", encoding="utf-8") as f:
    dockets = json.load(f)

dockets_json_str = json.dumps(dockets, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
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
            flex-wrap: wrap;
        }}

        .metric-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-align: right;
            min-width: 110px;
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
            min-width: 80px;
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
            flex-wrap: wrap;
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
            border: 1px solid transparent;
            min-height: 34px;
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
            border-color: var(--border-color);
        }}

        .btn-secondary:hover {{
            background: #374151;
            border-color: #4b5563;
        }}

        .btn-emerald {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.3);
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
            transition: border-color 0.2s, color 0.2s;
        }}

        .status-select.contacted {{
            border-color: var(--accent-amber);
            color: var(--accent-amber);
        }}

        .status-select.referral-submitted {{
            border-color: var(--accent-emerald);
            color: var(--accent-emerald);
        }}

        .status-select.pending {{
            border-color: var(--border-color);
            color: var(--text-muted);
        }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 3.5rem 1.5rem;
            background: var(--bg-secondary);
            border: 1px dashed var(--border-color);
            border-radius: 12px;
            color: var(--text-muted);
        }}

        .empty-state h3 {{
            color: var(--text-main);
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }}

        .empty-state p {{
            font-size: 0.875rem;
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
                    <div class="metric-val" id="totalCompanies">46</div>
                    <div class="metric-lbl">Target Companies</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val" id="totalContacts">193</div>
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
                    <input type="text" id="searchInput" placeholder="Search by name, role, company, hub, or corridor...">
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Corridor:</span>
                <button class="pill-btn corridor-pill active" onclick="filterCorridor('ALL', this)">All Corridors</button>
                <button class="pill-btn corridor-pill" onclick="filterCorridor('Outer Ring Road', this)">Outer Ring Road</button>
                <button class="pill-btn corridor-pill" onclick="filterCorridor('Bellandur', this)">Bellandur</button>
                <button class="pill-btn corridor-pill" onclick="filterCorridor('Manyata', this)">Manyata</button>
                <button class="pill-btn corridor-pill" onclick="filterCorridor('Whitefield', this)">Whitefield</button>
                <button class="pill-btn corridor-pill" onclick="filterCorridor('Domlur', this)">Domlur</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Company:</span>
                <button class="pill-btn company-pill active" onclick="filterCompany('ALL', this)">All Companies</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Accenture', this)">Accenture</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Deloitte', this)">Deloitte</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Goldman Sachs', this)">Goldman Sachs</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Amazon', this)">Amazon</button>
                <button class="pill-btn company-pill" onclick="filterCompany('IBM', this)">IBM</button>
                <button class="pill-btn company-pill" onclick="filterCompany('JPMorganChase', this)">JPMorganChase</button>
                <button class="pill-btn company-pill" onclick="filterCompany('KPMG', this)">KPMG</button>
                <button class="pill-btn company-pill" onclick="filterCompany('PwC', this)">PwC</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Walmart Global Tech', this)">Walmart Global Tech</button>
                <button class="pill-btn company-pill" onclick="filterCompany('Delhivery', this)">Delhivery</button>
                <button class="pill-btn company-pill" onclick="filterCompany('PhonePe', this)">PhonePe</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Domain:</span>
                <button class="pill-btn domain-pill active" onclick="filterDomain('ALL', this)">All Domains</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Operations', this)">Operations</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Supply Chain', this)">Supply Chain</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Advisory/Risk', this)">Advisory/Risk</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Trade Finance', this)">Trade Finance</button>
                <button class="pill-btn domain-pill" onclick="filterDomain('Merchant BD', this)">Merchant BD</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Status:</span>
                <button class="pill-btn status-pill active" onclick="filterStatus('ALL', this)">All</button>
                <button class="pill-btn status-pill" onclick="filterStatus('Pending', this)">Pending</button>
                <button class="pill-btn status-pill" onclick="filterStatus('Contacted', this)">Contacted</button>
                <button class="pill-btn status-pill" onclick="filterStatus('Referral Submitted', this)">Referral Submitted</button>
            </div>
        </section>

        <section class="targets-container" id="targetsContainer">
            <!-- Dynamic Render -->
        </section>
    </main>

    <div id="toast">Copied to clipboard!</div>

    <script>
        const dockets = {dockets_json_str};

        // Multi-dimensional active filter states
        let activeCorridor = 'ALL';
        let activeCompany = 'ALL';
        let activeDomain = 'ALL';
        let activeStatus = 'ALL';
        let searchTerm = '';

        // Safe Storage Abstraction with fallback for SecurityError in sandboxed environments
        const safeStorage = {{
            getItem: function(key) {{
                try {{
                    return window.localStorage.getItem(key);
                }} catch (e) {{
                    return (window.__fallbackStore && window.__fallbackStore[key]) || null;
                }}
            }},
            setItem: function(key, val) {{
                try {{
                    window.localStorage.setItem(key, val);
                }} catch (e) {{
                    window.__fallbackStore = window.__fallbackStore || {{}};
                    window.__fallbackStore[key] = val;
                }}
            }}
        }};

        function getStatus(contactName) {{
            const key = 'blr_referral_status_' + contactName;
            return safeStorage.getItem(key) || safeStorage.getItem('status_' + contactName) || 'Pending';
        }}

        function setStatus(contactName, status) {{
            const key = 'blr_referral_status_' + contactName;
            safeStorage.setItem(key, status);
            updateMetrics();
            render();
        }}

        // Fallback clipboard copy via textarea execCommand
        function fallbackCopy(text) {{
            return new Promise((resolve, reject) => {{
                try {{
                    const textArea = document.createElement("textarea");
                    textArea.value = text;
                    textArea.style.position = "fixed";
                    textArea.style.top = "-9999px";
                    textArea.style.left = "-9999px";
                    textArea.setAttribute("readonly", "");
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    const successful = document.execCommand('copy');
                    document.body.removeChild(textArea);
                    if (successful) resolve();
                    else reject(new Error('execCommand copy failed'));
                }} catch (err) {{
                    reject(err);
                }}
            }});
        }}

        // 1-Click Clipboard Copy Handler with dual visual feedback (toast + button tactile swap)
        function copyText(text, label, btn) {{
            const handleSuccess = () => {{
                showToast(`Copied ${{label}} to clipboard!`);
                if (btn) {{
                    const originalHTML = btn.innerHTML;
                    const originalBorder = btn.style.borderColor;
                    const originalColor = btn.style.color;
                    btn.innerHTML = 'Copied! ✓';
                    btn.style.borderColor = 'var(--accent-emerald)';
                    btn.style.color = '#34d399';
                    btn.disabled = true;
                    setTimeout(() => {{
                        btn.innerHTML = originalHTML;
                        btn.style.borderColor = originalBorder;
                        btn.style.color = originalColor;
                        btn.disabled = false;
                    }}, 1200);
                }}
            }};

            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(text).then(handleSuccess).catch(() => {{
                    fallbackCopy(text).then(handleSuccess).catch(() => {{
                        showToast(`Failed to copy to clipboard`);
                    }});
                }});
            }} else {{
                fallbackCopy(text).then(handleSuccess).catch(() => {{
                    showToast(`Failed to copy to clipboard`);
                }});
            }}
        }}

        // Helper to retrieve exact contact asset from in-memory dockets and dispatch to copyText
        function copyContactAsset(targetIdx, contactIdx, assetType, btn) {{
            const target = dockets[targetIdx];
            if (!target) return;
            const contact = target.contacts[contactIdx];
            if (!contact) return;

            let text = '';
            let label = assetType;
            if (assetType === '300c Note') {{
                text = contact.connection_note;
            }} else if (assetType === 'Referral Ask') {{
                text = contact.referral_ask;
            }} else if (assetType === 'Docket') {{
                text = contact.referral_docket;
            }}
            copyText(text, label, btn);
        }}

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            clearTimeout(window.__toastTimeout);
            window.__toastTimeout = setTimeout(() => {{
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
            searchTerm = e.target.value.toLowerCase().trim();
            render();
        }});

        // Multi-dimensional matching predicates
        function matchesCorridor(target, selected) {{
            if (selected === 'ALL') return true;
            const hay = ((target.corridor || '') + ' ' + (target.hub || '')).toLowerCase();
            if (selected === 'Outer Ring Road') {{
                return hay.includes('outer ring road') || hay.includes('orr');
            }}
            if (selected === 'Manyata') {{
                return hay.includes('manyata') || hay.includes('hebbal');
            }}
            if (selected === 'Bellandur') {{
                return hay.includes('bellandur');
            }}
            if (selected === 'Whitefield') {{
                return hay.includes('whitefield') || hay.includes('itpl');
            }}
            if (selected === 'Domlur') {{
                return hay.includes('domlur') || hay.includes('egl') || hay.includes('intermediate ring road');
            }}
            return hay.includes(selected.toLowerCase());
        }}

        function matchesCompany(target, selected) {{
            if (selected === 'ALL') return true;
            const c1 = (target.canonical_company || '').toLowerCase();
            const c2 = (target.company || '').toLowerCase();
            const hay = c1 + ' ' + c2;
            const normSel = selected.toLowerCase().replace(/[^a-z0-9]/g, '');
            const normHay = hay.replace(/[^a-z0-9]/g, '');

            if (normHay.includes(normSel) || normSel.includes(normHay)) return true;
            if (selected === 'PwC' && (hay.includes('pwc') || hay.includes('pricewaterhouse'))) return true;
            if ((selected === 'JPMorganChase' || selected === 'JPMorgan') && hay.includes('jpmorgan')) return true;
            if ((selected === 'Walmart Global Tech' || selected === 'Walmart') && hay.includes('walmart')) return true;
            if (selected === 'PhonePe' && hay.includes('phonepe')) return true;
            return hay.includes(selected.toLowerCase());
        }}

        function matchesDomain(target, selected) {{
            if (selected === 'ALL') return true;
            const dom = (target.domain || '').toLowerCase();
            const title = (target.job_title || '').toLowerCase();
            const hay = dom + ' ' + title;

            if (selected === 'Operations') {{
                return hay.includes('operation') || hay.includes('ops') || hay.includes('support') || hay.includes('community') || hay.includes('experience');
            }}
            if (selected === 'Supply Chain') {{
                return hay.includes('supply chain') || hay.includes('logistics') || hay.includes('freight') || hay.includes('procurement') || hay.includes('vendor') || hay.includes('cargo');
            }}
            if (selected === 'Advisory/Risk') {{
                return hay.includes('risk') || hay.includes('advisory') || hay.includes('audit') || hay.includes('compliance');
            }}
            if (selected === 'Trade Finance') {{
                return hay.includes('trade') || hay.includes('finance') || hay.includes('receivables') || hay.includes('exim') || hay.includes('markets');
            }}
            if (selected === 'Merchant BD') {{
                return hay.includes('merchant') || hay.includes('business development') || hay.includes('bd') || hay.includes('commercial') || hay.includes('brand activation') || hay.includes('sales');
            }}
            return hay.includes(selected.toLowerCase());
        }}

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

        function escapeJsStr(str) {{
            return (str || '').replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
        }}

        function render() {{
            const container = document.getElementById('targetsContainer');
            container.innerHTML = '';

            let matchedCompanyCount = 0;

            dockets.forEach((target, tIdx) => {{
                // 1. Corridor filter
                if (!matchesCorridor(target, activeCorridor)) return;

                // 2. Company filter
                if (!matchesCompany(target, activeCompany)) return;

                // 3. Domain filter
                if (!matchesDomain(target, activeDomain)) return;

                // 4. Filter contacts: Status ∩ SearchTerm
                const filteredContactsWithIdx = [];
                target.contacts.forEach((c, cIdx) => {{
                    const s = getStatus(c.full_name);
                    if (activeStatus !== 'ALL' && s !== activeStatus) return;

                    if (searchTerm) {{
                        const haystack = (c.full_name + ' ' + c.position + ' ' + target.company + ' ' + (target.canonical_company || '') + ' ' + (target.corridor || '') + ' ' + (target.hub || '') + ' ' + (target.job_title || '') + ' ' + (target.domain || '')).toLowerCase();
                        if (!haystack.includes(searchTerm)) return;
                    }}
                    filteredContactsWithIdx.push({{ contact: c, cIdx: cIdx }});
                }});

                if (filteredContactsWithIdx.length === 0) return;
                matchedCompanyCount++;

                const compEl = document.createElement('div');
                compEl.className = 'company-block';
                compEl.innerHTML = `
                    <div class="company-header">
                        <div class="company-title-area">
                            <span class="company-name">${{target.canonical_company || target.company}}</span>
                            <span class="hub-tag">${{target.hub}} (${{target.corridor}})</span>
                            <span class="role-tag">${{target.job_title}}</span>
                        </div>
                        <a href="${{target.job_url || target.careers_url}}" target="_blank" rel="noopener noreferrer" class="job-link-btn">
                            Official Careers / Req Link ↗
                        </a>
                    </div>
                    <div class="contacts-grid" id="grid_${{tIdx}}"></div>
                `;

                const grid = compEl.querySelector(`#grid_${{tIdx}}`);

                filteredContactsWithIdx.forEach(({{ contact, cIdx }}) => {{
                    const curStatus = getStatus(contact.full_name);
                    const statusClass = curStatus.toLowerCase().replace(/\\s+/g, '-');
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
                                <select class="status-select ${{statusClass}}" onchange="setStatus('${{escapeJsStr(contact.full_name)}}', this.value)">
                                    <option value="Pending" ${{curStatus === 'Pending' ? 'selected' : ''}}>Pending</option>
                                    <option value="Contacted" ${{curStatus === 'Contacted' ? 'selected' : ''}}>Contacted</option>
                                    <option value="Referral Submitted" ${{curStatus === 'Referral Submitted' ? 'selected' : ''}}>Referral Submitted</option>
                                </select>
                            </div>
                        </div>

                        <div class="actions-row">
                            <a href="${{contact.linkedin_url}}" target="_blank" rel="noopener noreferrer" class="btn-action btn-primary">
                                Open LinkedIn ↗
                            </a>
                            <button class="btn-action btn-secondary" onclick="copyContactAsset(${{tIdx}}, ${{cIdx}}, '300c Note', this)">
                                Copy 300c Note
                            </button>
                        </div>
                        <div class="actions-row">
                            <button class="btn-action btn-emerald" onclick="copyContactAsset(${{tIdx}}, ${{cIdx}}, 'Referral Ask', this)">
                                Copy Referral Ask
                            </button>
                            <button class="btn-action btn-secondary" onclick="copyContactAsset(${{tIdx}}, ${{cIdx}}, 'Docket', this)">
                                Copy Docket
                            </button>
                        </div>
                    `;
                    grid.appendChild(card);
                }});

                container.appendChild(compEl);
            }});

            if (matchedCompanyCount === 0) {{
                container.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                        <h3>No matching referral targets found</h3>
                        <p>Try resetting or broadening your corridor, company, domain, or status filters.</p>
                    </div>
                `;
            }}

            const isFiltered = (activeCorridor !== 'ALL' || activeCompany !== 'ALL' || activeDomain !== 'ALL' || activeStatus !== 'ALL' || !!searchTerm);
            document.getElementById('totalCompanies').innerText = isFiltered
                ? `${{matchedCompanyCount}} / ${{dockets.length}}`
                : `${{dockets.length}}`;
        }}

        // Initial setup
        updateMetrics();
        render();
    </script>
</body>
</html>
"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully generated {INDEX_PATH} with {len(dockets)} inlined dockets.")
