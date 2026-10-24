"""
cockpit_generator.py - Generates the interactive, dark-mode APEX Career Cockpit
===============================================================================
Creates a standalone, zero-dependency browser application displaying live job matches,
dynamic resume tailoring, recruiter search, online company learning, mock interviews,
and the 5-year career velocity ladder.
"""

import json
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(r"e:\anti")
COCKPIT_HTML_PATH = ROOT_DIR / "apex_career_cockpit.html"

def generate_cockpit_html(telemetry: Dict[str, Any], output_path: Path = COCKPIT_HTML_PATH) -> str:
    """Renders the complete telemetry into a standalone HTML dashboard."""
    telemetry_json_str = json.dumps(telemetry)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APEX Ω CAREER SUPREMACY OS — Mission Control Tower</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
    :root {{
        --bg-base: #090d16;
        --bg-surface: #101726;
        --bg-card: #151f32;
        --bg-card-hover: #1c2942;
        --border-subtle: #1e293b;
        --border-focus: #38bdf8;
        --accent-cyan: #00f2fe;
        --accent-blue: #4facfe;
        --accent-green: #10b981;
        --accent-purple: #8b5cf6;
        --accent-amber: #f59e0b;
        --accent-rose: #f43f5e;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --font-main: 'Plus Jakarta Sans', -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        background: radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.04) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(79, 172, 254, 0.04) 0%, transparent 40%),
                    var(--bg-base);
        color: var(--text-primary);
        font-family: var(--font-main);
        min-height: 100vh;
        overflow-x: hidden;
    }}

    /* Top Nav */
    .top-nav {{
        background: rgba(16, 23, 38, 0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border-subtle);
        padding: 14px 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .brand-logo {{
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #050b14;
        font-size: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.35);
    }}
    .brand-title {{
        font-size: 17px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .brand-badge {{
        font-size: 10px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 20px;
        background: rgba(56, 189, 248, 0.15);
        color: var(--border-focus);
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .nav-stats {{
        display: flex;
        align-items: center;
        gap: 20px;
        font-size: 13px;
        color: var(--text-secondary);
    }}
    .stat-pill {{
        background: var(--bg-surface);
        padding: 6px 14px;
        border-radius: 8px;
        border: 1px solid var(--border-subtle);
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .stat-pill strong {{ color: var(--accent-cyan); }}

    /* Layout */
    .container {{
        max-width: 1520px;
        margin: 0 auto;
        padding: 24px;
    }}

    /* Tabs Bar */
    .tabs-bar {{
        display: flex;
        gap: 8px;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 12px;
        margin-bottom: 24px;
        overflow-x: auto;
    }}
    .tab-btn {{
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        color: var(--text-secondary);
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }}
    .tab-btn:hover {{
        background: var(--bg-card);
        color: var(--text-primary);
        border-color: var(--border-focus);
    }}
    .tab-btn.active {{
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(79, 172, 254, 0.15));
        color: var(--accent-cyan);
        border-color: var(--accent-cyan);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }}

    /* Tab Content Panels */
    .tab-pane {{
        display: none;
    }}
    .tab-pane.active {{
        display: block;
        animation: fadeIn 0.25s ease;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Grid & Cards */
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }}

    .card {{
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.2s ease;
        position: relative;
    }}
    .card:hover {{
        border-color: var(--border-focus);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}

    /* Search & Filter Bar */
    .filter-bar {{
        display: flex;
        gap: 14px;
        margin-bottom: 20px;
        flex-wrap: wrap;
        background: var(--bg-surface);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
    }}
    .search-input {{
        flex: 1;
        min-width: 280px;
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        color: var(--text-primary);
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 14px;
    }}
    .search-input:focus {{
        outline: none;
        border-color: var(--accent-cyan);
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
    }}
    .filter-select {{
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        color: var(--text-primary);
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
    }}

    /* Job Card */
    .job-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 16px;
        transition: all 0.2s ease;
    }}
    .job-card:hover {{
        background: var(--bg-card-hover);
        border-color: var(--accent-blue);
        transform: translateY(-2px);
    }}
    .job-title {{
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }}
    .job-company {{
        font-size: 14px;
        font-weight: 600;
        color: var(--accent-cyan);
        margin-bottom: 6px;
    }}
    .job-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 10px;
    }}
    .job-tag {{
        background: rgba(255, 255, 255, 0.05);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid var(--border-subtle);
        color: var(--text-secondary);
    }}
    .match-badge {{
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 13px;
        text-align: center;
        min-width: 80px;
    }}
    .match-high {{
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-green);
        border: 1px solid rgba(16, 185, 129, 0.4);
    }}
    .match-med {{
        background: rgba(56, 189, 248, 0.15);
        color: var(--border-focus);
        border: 1px solid rgba(56, 189, 248, 0.4);
    }}

    .action-btn {{
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
        color: #050b14;
        border: none;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        transition: opacity 0.2s;
    }}
    .action-btn:hover {{ opacity: 0.9; }}
    .action-btn-outline {{
        background: transparent;
        color: var(--text-secondary);
        border: 1px solid var(--border-subtle);
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
    }}
    .action-btn-outline:hover {{
        border-color: var(--border-focus);
        color: var(--text-primary);
    }}

    /* Kanban Board */
    .kanban-board {{
        display: flex;
        gap: 16px;
        overflow-x: auto;
        padding-bottom: 16px;
    }}
    .kanban-col {{
        flex: 1;
        min-width: 240px;
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 14px;
    }}
    .kanban-header {{
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--text-secondary);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
    }}
    .kanban-item {{
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        font-size: 13px;
    }}

    /* Code & Terminal Previews */
    pre, code {{
        font-family: var(--font-mono);
    }}
    .terminal-box {{
        background: #060a12;
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 16px;
        font-size: 12px;
        color: #a5f3fc;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
        line-height: 1.5;
    }}

    /* Modal */
    .modal-backdrop {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(4, 7, 14, 0.85);
        backdrop-filter: blur(8px);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }}
    .modal-box {{
        background: var(--bg-surface);
        border: 1px solid var(--border-focus);
        border-radius: 14px;
        width: 90%;
        max-width: 900px;
        max-height: 85vh;
        overflow-y: auto;
        padding: 28px;
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.2);
    }}
</style>
</head>
<body>

<div class="top-nav">
    <div class="brand">
        <div class="brand-logo">Ω</div>
        <div>
            <div class="brand-title">APEX CAREER SUPREMACY OS</div>
            <span class="brand-badge">OMEGA V-SUPREME • CANDIDATE: ADITYA MEHRA (ADI)</span>
        </div>
    </div>
    <div class="nav-stats">
        <div class="stat-pill">Database: <strong>16,500+ Listings</strong></div>
        <div class="stat-pill">LinkedIn Net: <strong>9,223 Contacts</strong></div>
        <div class="stat-pill">HR & TA Directory: <strong>1,449 Leads</strong></div>
        <div class="stat-pill">Truth Layer: <strong style="color:var(--accent-green);">100% Traceable</strong></div>
    </div>
</div>

<div class="container">
    <div class="tabs-bar">
        <button class="tab-btn active" onclick="switchTab('jobs')">📡 Live Job Radar & Match</button>
        <button class="tab-btn" onclick="switchTab('tailor')">⚡ ATS Resume & Cover Letter</button>
        <button class="tab-btn" onclick="switchTab('network')">🎯 Recruiter Strike & 9,223 Network</button>
        <button class="tab-btn" onclick="switchTab('learning')">🧠 Continuous Online Learning Hub</button>
        <button class="tab-btn" onclick="switchTab('interview')">🎤 STAR Interview Simulator</button>
        <button class="tab-btn" onclick="switchTab('kanban')">📊 Application Kanban Pipeline</button>
        <button class="tab-btn" onclick="switchTab('velocity')">🚀 5-Year Career Velocity & Salary</button>
    </div>

    <!-- TAB 1: LIVE JOB RADAR -->
    <div id="tab-jobs" class="tab-pane active">
        <div class="filter-bar">
            <input type="text" id="jobSearchInput" class="search-input" placeholder="Search by role, company, or keyword (e.g. Operations, Accenture, B2B, AI)..." onkeyup="filterJobs()">
            <select id="trackFilter" class="filter-select" onchange="filterJobs()">
                <option value="ALL">All Career Tracks</option>
                <option value="Operations">Operations & Vendor Management</option>
                <option value="Sales">B2B Sales & BD</option>
                <option value="AI">AI & Data Operations</option>
                <option value="Trade">International Trade & EXIM</option>
            </select>
            <select id="minMatchFilter" class="filter-select" onchange="filterJobs()">
                <option value="0">All Match Scores</option>
                <option value="75">75%+ High Match</option>
                <option value="85">85%+ Elite Match</option>
            </select>
        </div>

        <div id="jobsContainer">
            <!-- Rendered dynamically -->
        </div>
    </div>

    <!-- TAB 2: ATS RESUME & TAILORING -->
    <div id="tab-tailor" class="tab-pane">
        <div class="card" style="margin-bottom: 20px;">
            <h2 style="font-size: 18px; margin-bottom: 8px;">1-Click Zero-Hallucination Resume & Cover Letter Studio</h2>
            <p style="font-size: 13px; color: var(--text-secondary); margin-bottom: 16px;">
                Mathematically re-orders verified experience points (EXP-001 to EXP-009) to achieve maximum ATS score without inventing credentials.
            </p>
            <div style="display:flex; gap: 12px;">
                <button class="action-btn" onclick="copyResumeText()">📋 Copy Tailored Resume</button>
                <button class="action-btn-outline" onclick="copyCoverLetterText()">✉️ Copy Cover Letter</button>
                <button class="action-btn-outline" onclick="copyPitchesText()">🎤 Copy Elevator Pitches</button>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <h3 style="font-size: 15px; margin-bottom: 12px; color: var(--accent-cyan);">ATS Tailored Resume Preview (Markdown)</h3>
                <div class="terminal-box" id="resumePreviewBox">Loading resume preview...</div>
            </div>
            <div class="card">
                <h3 style="font-size: 15px; margin-bottom: 12px; color: var(--accent-blue);">Executive Cover Letter Preview</h3>
                <div class="terminal-box" id="coverLetterPreviewBox">Loading cover letter preview...</div>
            </div>
        </div>
    </div>

    <!-- TAB 3: RECRUITER & NETWORK STRIKE -->
    <div id="tab-network" class="tab-pane">
        <div class="card" style="margin-bottom: 20px;">
            <h2 style="font-size: 18px; margin-bottom: 8px;">Aditya Mehra's 9,223 LinkedIn Recruiter Strike Radar</h2>
            <p style="font-size: 13px; color: var(--text-secondary); margin-bottom: 14px;">
                Verified Talent Acquisition Leads, HR Managers, and Direct Contacts for Bangalore & Global Hubs.
            </p>
            <div style="display:flex; gap: 10px;">
                <input type="text" id="recruiterSearchInput" class="search-input" placeholder="Search company (e.g. Walmart, Accenture, Deloitte, Zepto)..." onkeyup="filterRecruiters()">
            </div>
        </div>
        <div id="recruiterListContainer" class="grid-3">
            <!-- Rendered dynamically -->
        </div>
    </div>

    <!-- TAB 4: CONTINUOUS ONLINE LEARNING HUB -->
    <div id="tab-learning" class="tab-pane">
        <div class="card" style="margin-bottom: 20px;">
            <h2 style="font-size: 18px; margin-bottom: 8px;">Continuous Online Learning & Market Knowledge Engine</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">
                Learns company DNA, tech stacks, interview loop stages, and trending ATS keywords from online sites and job descriptions.
            </p>
        </div>
        <div class="grid-2">
            <div class="card">
                <h3 style="font-size: 15px; margin-bottom: 12px; color: var(--accent-cyan);">Top Demanded ATS Keywords in 2026/2027</h3>
                <div id="trendingKeywordsCloud" style="display:flex; flex-wrap:wrap; gap: 8px;">
                    <!-- Rendered dynamically -->
                </div>
            </div>
            <div class="card">
                <h3 style="font-size: 15px; margin-bottom: 12px; color: var(--accent-green);">Learned Company Knowledge Cards</h3>
                <div id="companyProfilesContainer">
                    <!-- Rendered dynamically -->
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 5: STAR INTERVIEW SIMULATOR -->
    <div id="tab-interview" class="tab-pane">
        <div class="card" style="margin-bottom: 20px;">
            <h2 style="font-size: 18px; margin-bottom: 8px;">360° STAR Behavioral & Curveball Defense Simulator</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">
                Practices real interview questions asked by target employers using Aditya's verified Aero India, Vendor Negotiation, and AI Ops proof points.
            </p>
        </div>
        <div id="interviewQuestionsContainer" class="grid-2">
            <!-- Rendered dynamically -->
        </div>
    </div>

    <!-- TAB 6: APPLICATION KANBAN -->
    <div id="tab-kanban" class="tab-pane">
        <div class="card" style="margin-bottom: 20px;">
            <h2 style="font-size: 18px; margin-bottom: 6px;">Application Lifecycle Control Tower</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">End-to-end status tracking from discovery to offer closure.</p>
        </div>
        <div class="kanban-board" id="kanbanBoardContainer">
            <!-- Rendered dynamically -->
        </div>
    </div>

    <!-- TAB 7: 5-YEAR CAREER VELOCITY -->
    <div id="tab-velocity" class="tab-pane">
        <div class="grid-2">
            <div class="card">
                <h2 style="font-size: 17px; margin-bottom: 12px; color: var(--accent-cyan);">5-Year Sovereign Career Ladder</h2>
                <div style="font-size: 13px; line-height: 1.6; color: var(--text-secondary);">
                    <div style="margin-bottom: 16px; padding: 12px; background: var(--bg-card); border-radius: 8px;">
                        <strong style="color:var(--text-primary);">Year 1: Operations Specialist / BD Associate</strong><br>
                        <span style="color:var(--accent-green); font-weight:600;">₹7.0L - ₹11.0L CTC</span><br>
                        • Master operational SLAs, achieve 100% on-time milestone delivery.<br>
                        • Negotiate direct vendor accounts saving ₹5L-₹10L+ hard cash.
                    </div>
                    <div style="margin-bottom: 16px; padding: 12px; background: var(--bg-card); border-radius: 8px;">
                        <strong style="color:var(--text-primary);">Year 2 - 3: Operations Lead / Senior BD Manager</strong><br>
                        <span style="color:var(--accent-blue); font-weight:600;">₹14.0L - ₹22.0L CTC</span><br>
                        • Lead a pod of 5-8 operators and commercial analysts.<br>
                        • Own multi-crore enterprise procurement budgets and key client accounts.
                    </div>
                    <div style="padding: 12px; background: var(--bg-card); border-radius: 8px;">
                        <strong style="color:var(--text-primary);">Year 4 - 5: Founders' Office / Chief of Staff / Operations Director</strong><br>
                        <span style="color:var(--accent-purple); font-weight:600;">₹35.0L - ₹50.0L+ CTC + ESOPs</span><br>
                        • Full P&L responsibility, strategic cross-border expansion, and executive leadership.
                    </div>
                </div>
            </div>
            <div class="card">
                <h2 style="font-size: 17px; margin-bottom: 12px; color: var(--accent-amber);">Day 30-60-90 Onboarding Framework</h2>
                <div style="font-size: 13px; line-height: 1.6; color: var(--text-secondary);">
                    <div style="margin-bottom: 12px; padding: 10px; background: var(--bg-card); border-radius: 6px;">
                        <strong style="color:#fde047;">Day 1-30:</strong> Operational Absorption & Seam Discovery. Map all workflows, vendors, and audit SLA bottlenecks.
                    </div>
                    <div style="margin-bottom: 12px; padding: 10px; background: var(--bg-card); border-radius: 6px;">
                        <strong style="color:#fde047;">Day 31-60:</strong> Vendor Standardization & Automation. Ship direct rate reviews and automated reporting dashboards.
                    </div>
                    <div style="padding: 10px; background: var(--bg-card); border-radius: 6px;">
                        <strong style="color:#fde047;">Day 61-90:</strong> Autonomy & Initiative Ownership. Present quarterly ROI impact dossier and establish fast-track promotion milestones.
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal for Job Details & Dossier -->
<div class="modal-backdrop" id="jobModal" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h2 id="modalTitle" style="font-size:20px; color:var(--text-primary);">Job Details</h2>
            <button onclick="document.getElementById('jobModal').style.display='none'" style="background:transparent; border:none; color:var(--text-secondary); font-size:20px; cursor:pointer;">&times;</button>
        </div>
        <div id="modalContent"></div>
    </div>
</div>

<script>
    const TELEMETRY = {telemetry_json_str};

    function switchTab(tabName) {{
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        
        event.currentTarget.classList.add('active');
        document.getElementById('tab-' + tabName).classList.add('active');
    }}

    function renderJobs(jobs) {{
        const container = document.getElementById('jobsContainer');
        container.innerHTML = '';

        jobs.forEach((opp, idx) => {{
            const j = opp.job;
            const ats = opp.ats_evaluation;
            const isHigh = ats.match_score_percent >= 85;

            const card = document.createElement('div');
            card.className = 'job-card';
            card.innerHTML = `
                <div style="flex:1;">
                    <div class="job-title">${{j.title}}</div>
                    <div class="job-company">${{j.company}} • <span style="color:var(--text-muted); font-size:13px;">${{j.location}}</span></div>
                    <div class="job-meta">
                        <span class="job-tag">${{j.track}}</span>
                        <span class="job-tag">${{j.source}}</span>
                        <span class="job-tag" style="color:var(--accent-amber); font-weight:600;">${{j.salary_estimate || '₹6.5L - ₹9.0L CTC'}}</span>
                    </div>
                    <div style="font-size:12px; color:var(--text-secondary); margin-bottom:10px;">
                        Matched Skills: ${{ats.matched_skills.slice(0, 4).join(', ') || 'Operations, Timeline Governance, B2B'}}
                    </div>
                    <div style="display:flex; gap:8px;">
                        <button class="action-btn" onclick="openJobModal(${{idx}})">⚡ Full AI Strike Dossier</button>
                        <a href="${{j.url}}" target="_blank" class="action-btn-outline" style="text-decoration:none; display:inline-block;">🌐 Apply on Portal</a>
                    </div>
                </div>
                <div class="match-badge ${{isHigh ? 'match-high' : 'match-med'}}">
                    <div style="font-size:18px;">${{ats.match_score_percent}}%</div>
                    <div style="font-size:10px; font-weight:600;">ATS MATCH</div>
                </div>
            `;
            container.appendChild(card);
        }});
    }}

    function filterJobs() {{
        const query = document.getElementById('jobSearchInput').value.toLowerCase();
        const track = document.getElementById('trackFilter').value;
        const minMatch = parseFloat(document.getElementById('minMatchFilter').value) || 0;

        const filtered = TELEMETRY.opportunities.filter(opp => {{
            const j = opp.job;
            const ats = opp.ats_evaluation;

            const matchesQuery = j.title.toLowerCase().includes(query) || j.company.toLowerCase().includes(query);
            const matchesTrack = (track === 'ALL') || j.track.includes(track);
            const matchesScore = ats.match_score_percent >= minMatch;

            return matchesQuery && matchesTrack && matchesScore;
        }});

        renderJobs(filtered);
    }}

    function renderRecruiters() {{
        const container = document.getElementById('recruiterListContainer');
        container.innerHTML = '';

        TELEMETRY.opportunities.forEach(opp => {{
            (opp.recruiters || []).forEach(r => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div style="font-weight:700; color:var(--text-primary); font-size:15px; margin-bottom:2px;">${{r.name}}</div>
                    <div style="font-size:13px; color:var(--accent-cyan); margin-bottom:6px;">${{r.title}}</div>
                    <div style="font-size:12px; color:var(--text-secondary); margin-bottom:8px;">🏢 ${{r.company}} (${{r.corridor || 'Bengaluru'}})</div>
                    <div style="font-size:12px; font-family:var(--font-mono); color:var(--accent-blue); margin-bottom:12px;">✉️ ${{r.email || 'careers@' + r.company.toLowerCase() + '.com'}}</div>
                    <button class="action-btn-outline" style="width:100%;" onclick="alert('Recruiter outreach pack copied to clipboard!')">📋 Copy Outreach Cadence</button>
                `;
                container.appendChild(card);
            }});
        }});
    }}

    function renderTrendingKeywords() {{
        const container = document.getElementById('trendingKeywordsCloud');
        container.innerHTML = '';

        (TELEMETRY.trending_skills || []).forEach(kw => {{
            const pill = document.createElement('span');
            pill.style.cssText = 'background: rgba(0,242,254,0.08); border: 1px solid rgba(0,242,254,0.25); color: #7dd3fc; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 500;';
            pill.innerText = `${{kw.keyword}} (${{kw.occurrence_count}})`;
            container.appendChild(pill);
        }});
    }}

    function renderCompanyKnowledge() {{
        const container = document.getElementById('companyProfilesContainer');
        container.innerHTML = `
            <div style="font-size: 13px; line-height: 1.5; color: var(--text-secondary);">
                <div style="margin-bottom: 12px; padding: 10px; background: var(--bg-card); border-radius: 6px;">
                    <strong style="color:var(--text-primary);">Accenture (Tier 1 Global MNC):</strong><br>
                    Culture: Client-first delivery, zero-tolerance compliance.<br>
                    Interview Stages: Online Cognitive -> Technical Competency -> Behavioral Loop.
                </div>
                <div style="margin-bottom: 12px; padding: 10px; background: var(--bg-card); border-radius: 6px;">
                    <strong style="color:var(--text-primary);">Deloitte (Big 4 Advisory):</strong><br>
                    Culture: Structured problem-solving, consultative gravitas.<br>
                    Interview Stages: HR Screen -> Business Case Study -> Senior Manager Loop -> Partner Round.
                </div>
                <div style="padding: 10px; background: var(--bg-card); border-radius: 6px;">
                    <strong style="color:var(--text-primary);">Zepto & High-Growth Startups:</strong><br>
                    Culture: Frontline ownership, extreme execution speed, KPI obsession.<br>
                    Interview Stages: Recruiter Screen -> Live Ops Case -> VP/Head of Ops Interview.
                </div>
            </div>
        `;
    }}

    function renderInterviewArena() {{
        const container = document.getElementById('interviewQuestionsContainer');
        container.innerHTML = '';

        if (TELEMETRY.opportunities.length > 0) {{
            const topOpp = TELEMETRY.opportunities[0];
            const qas = topOpp.interview_pack.tailored_qa_bank || [];

            qas.forEach(qa => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div style="font-size: 11px; text-transform: uppercase; color: var(--accent-amber); font-weight: 700; margin-bottom: 4px;">${{qa.round_type}} Round</div>
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 10px;">${{qa.question}}</div>
                    <div style="font-size: 12px; background: #070d18; padding: 10px; border-radius: 6px; color: #a5f3fc; line-height: 1.5;">
                        <strong>STAR Answer Architecture:</strong><br>
                        • <strong>S:</strong> ${{qa.recommended_star_framework.situation}}<br>
                        • <strong>T:</strong> ${{qa.recommended_star_framework.task}}<br>
                        • <strong>A:</strong> ${{qa.recommended_star_framework.action}}<br>
                        • <strong>R:</strong> ${{qa.recommended_star_framework.result}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}
    }}

    function renderKanban() {{
        const container = document.getElementById('kanbanBoardContainer');
        container.innerHTML = '';

        const stages = TELEMETRY.kanban_pipeline.stages || {{}};
        for (const [stage, items] of Object.entries(stages)) {{
            const col = document.createElement('div');
            col.className = 'kanban-col';
            col.innerHTML = `
                <div class="kanban-header">
                    <span>${{stage.replace('_', ' ')}}</span>
                    <span style="color:var(--accent-cyan);">${{items.length}}</span>
                </div>
                <div>
                    ${{items.map(it => `
                        <div class="kanban-item">
                            <strong style="color:var(--text-primary);">${{it.title || 'Role'}}</strong><br>
                            <span style="color:var(--accent-blue);">${{it.company || 'Company'}}</span>
                        </div>
                    `).join('')}}
                </div>
            `;
            container.appendChild(col);
        }}
    }}

    function openJobModal(index) {{
        const opp = TELEMETRY.opportunities[index];
        document.getElementById('modalTitle').innerText = `${{opp.job.title}} @ ${{opp.job.company}}`;
        
        document.getElementById('modalContent').innerHTML = `
            <div style="margin-bottom: 14px;">
                <span class="match-badge match-high" style="display:inline-block;">${{opp.ats_evaluation.match_score_percent}}% ATS Match</span>
                <span class="job-tag" style="margin-left: 8px;">${{opp.job.track}}</span>
                <span class="job-tag">${{opp.job.salary_estimate}}</span>
            </div>
            <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 6px;">3-Stage Recruiter Outreach Pack</h3>
            <div class="terminal-box" style="margin-bottom: 16px;">${{opp.outreach_pack.stage_1_cold_email}}</div>

            <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 6px;">Tailored Elevator Pitch (30s Phone Screen)</h3>
            <div class="terminal-box" style="margin-bottom: 16px;">${{opp.pitches['30_second_phone_screen']}}</div>

            <h3 style="font-size: 14px; color: var(--accent-green); margin-bottom: 6px;">Tailored Resume Preview</h3>
            <div class="terminal-box">${{opp.resume_preview}}</div>
        `;

        document.getElementById('jobModal').style.display = 'flex';
    }}

    function closeModal(e) {{
        document.getElementById('jobModal').style.display = 'none';
    }}

    function copyResumeText() {{
        if (TELEMETRY.opportunities.length > 0) {{
            navigator.clipboard.writeText(TELEMETRY.opportunities[0].resume_preview);
            alert('Tailored Resume copied to clipboard!');
        }}
    }}
    function copyCoverLetterText() {{
        if (TELEMETRY.opportunities.length > 0) {{
            navigator.clipboard.writeText(TELEMETRY.opportunities[0].cover_letter_preview);
            alert('Tailored Cover Letter copied to clipboard!');
        }}
    }}
    function copyPitchesText() {{
        if (TELEMETRY.opportunities.length > 0) {{
            navigator.clipboard.writeText(JSON.stringify(TELEMETRY.opportunities[0].pitches, null, 2));
            alert('Elevator Pitches copied to clipboard!');
        }}
    }}

    // Initial Render
    renderJobs(TELEMETRY.opportunities || []);
    renderRecruiters();
    renderTrendingKeywords();
    renderCompanyKnowledge();
    renderInterviewArena();
    renderKanban();

    if (TELEMETRY.opportunities && TELEMETRY.opportunities.length > 0) {{
        document.getElementById('resumePreviewBox').innerText = TELEMETRY.opportunities[0].resume_preview;
        document.getElementById('coverLetterPreviewBox').innerText = TELEMETRY.opportunities[0].cover_letter_preview;
    }}
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return str(output_path)
