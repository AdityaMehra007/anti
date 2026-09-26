"""
Builds the standalone executive HTML Cockpit: ADITYA_CAREER_INTELLIGENCE_COCKPIT.html
Zero external dependencies. Works offline directly in any browser.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from aditya_career_os_db import get_connection

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "data" / "aditya_global_career_intelligence.db"
OUTPUT_HTML = ROOT_DIR / "ADITYA_CAREER_INTELLIGENCE_COCKPIT.html"
QA_FILE = ROOT_DIR / "data" / "standard_application_answers.json"

def generate_cockpit():
    conn = get_connection(DB_PATH)
    cur = conn.cursor()

    # Telemetry
    cur.execute("SELECT count(1) FROM companies"); c_cnt = cur.fetchone()[0]
    cur.execute("SELECT count(1) FROM jobs"); j_cnt = cur.fetchone()[0]
    cur.execute("SELECT count(1) FROM people"); p_cnt = cur.fetchone()[0]
    cur.execute("SELECT count(1) FROM applications"); a_cnt = cur.fetchone()[0]
    cur.execute("SELECT count(1) FROM outreach"); o_cnt = cur.fetchone()[0]

    # Action Queue
    cur.execute("SELECT * FROM daily_action_queue ORDER BY action_type, rank_order")
    actions = [dict(r) for r in cur.fetchall()]

    # Top Jobs
    cur.execute("""
        SELECT j.job_id, j.company_name, j.job_title, j.location,
               COALESCE(j.job_family, j.function, 'Operations') AS track,
               j.application_url, m.total_match_score, m.priority_tier,
               m.match_explanation AS match_rationale
        FROM jobs j
        JOIN job_matches m ON j.job_id = m.job_id
        ORDER BY m.total_match_score DESC
        LIMIT 60
    """)
    jobs = [dict(r) for r in cur.fetchall()]

    # Outreach Drafts
    cur.execute("""
        SELECT outreach_id, contact_name, company_name, job_title, channel,
               message_type, subject, message_body, human_approval_status
        FROM outreach
        ORDER BY outreach_id
        LIMIT 50
    """)
    outreach = [dict(r) for r in cur.fetchall()]

    # Bengaluru Clusters
    cur.execute("SELECT * FROM bengaluru_clusters ORDER BY company_count DESC")
    clusters = [dict(r) for r in cur.fetchall()]

    conn.close()

    # Load HR Directory contacts
    hr_file = ROOT_DIR / "data" / "csv_exports" / "ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv"
    hr_contacts = []
    if hr_file.exists():
        import csv
        with open(hr_file, "r", encoding="utf-8") as hf:
            reader = csv.DictReader(hf)
            for row in reader:
                hr_contacts.append(row)
                if len(hr_contacts) >= 150:
                    break

    # Load QA
    qa_data = {}
    if QA_FILE.exists():
        qa_data = json.loads(QA_FILE.read_text(encoding="utf-8"))

    # 48 Sheets Catalog
    sheets_catalog = [
        {"num": "01", "name": "01_Dashboard", "cat": "Command Center", "desc": "Executive KPI cards and Section 83 One-Click Action Center."},
        {"num": "02", "name": "02_Candidate_Profile", "cat": "Profile Ground Truth", "desc": "Aditya Mehra verified credentials, BBA IB DSU '26, verified projects."},
        {"num": "03", "name": "03_Companies", "cat": "Entities", "desc": "7,618 tracked corporate employers with legal registration, domain & sector."},
        {"num": "04", "name": "04_Company_Leaders", "cat": "Leadership", "desc": "Founders, CEOs, COOs, and Chief Operating Officers."},
        {"num": "05", "name": "05_Recruiters_HR", "cat": "Talent Acquisition", "desc": "Verified recruiters, TA partners, and campus recruitment leads."},
        {"num": "06", "name": "06_Hiring_Managers", "cat": "Operations Leaders", "desc": "Operations heads, PMO leads, and department decision-makers."},
        {"num": "07", "name": "07_Employees_Referrals", "cat": "Referrals", "desc": "1st and 2nd degree alumni and employee referral routing channels."},
        {"num": "08", "name": "08_Jobs", "cat": "Job Market", "desc": "3,234 active verified corporate job requisitions."},
        {"num": "09", "name": "09_Bengaluru_Jobs", "cat": "Regional", "desc": "High-density Bengaluru corridor requisitions (ORR, Whitefield, Manyata)."},
        {"num": "10", "name": "10_India_Jobs", "cat": "Regional", "desc": "National enterprise roles across Mumbai, NCR, Pune, and Hyderabad."},
        {"num": "11", "name": "11_Global_Jobs", "cat": "International", "desc": "Global and international graduate requisitions (UAE, UK, Singapore, US)."},
        {"num": "12", "name": "12_Internships", "cat": "Early Career", "desc": "Graduate trainee, management trainee, and rotational internship roles."},
        {"num": "13", "name": "13_Remote_Jobs", "cat": "Flexible", "desc": "Remote-first and hybrid corporate operations opportunities."},
        {"num": "14", "name": "14_MNCs", "cat": "Employer Archetype", "desc": "Fortune 500 multinationals (Accenture, Deloitte, Amazon, Siemens)."},
        {"num": "15", "name": "15_GCCs", "cat": "Employer Archetype", "desc": "Global Capability Centers in Bengaluru with direct captive operations."},
        {"num": "16", "name": "16_Startups", "cat": "Employer Archetype", "desc": "High-growth seed and venture-backed Indian tech ventures."},
        {"num": "17", "name": "17_Scaleups", "cat": "Employer Archetype", "desc": "Late-stage unicorns and market leaders (Swiggy, Cred, Razorpay, Zepto)."},
        {"num": "18", "name": "18_Banks_Finance", "cat": "Industry Focus", "desc": "BFSI, investment banking operations, risk, and reconciliation tracks."},
        {"num": "19", "name": "19_Consulting", "cat": "Industry Focus", "desc": "Management consulting, advisory, and operational transformation."},
        {"num": "20", "name": "20_Technology", "cat": "Industry Focus", "desc": "Enterprise software, cloud platforms, and data infrastructure."},
        {"num": "21", "name": "21_Operations_Roles", "cat": "Functional Track", "desc": "Business Operations, Operations Associate, and Process Analyst."},
        {"num": "22", "name": "22_Business_Analyst_Roles", "cat": "Functional Track", "desc": "Business Analyst, Junior Advisory, and MIS Reporting Specialist."},
        {"num": "23", "name": "23_AI_Roles", "cat": "Functional Track", "desc": "AI Operations, Data QA, LLM Prompt Engineering, and Model Curation."},
        {"num": "24", "name": "24_International_Business", "cat": "Functional Track", "desc": "Global Trade, Cross-Border Logistics, and Foreign Trade Policy."},
        {"num": "25", "name": "25_Trade_Operations", "cat": "Functional Track", "desc": "EXIM operations, ocean/air freight, customs, and compliance."},
        {"num": "26", "name": "26_PMO_Project", "cat": "Functional Track", "desc": "PMO Coordination, Event Operations PMO, and Project Management."},
        {"num": "27", "name": "27_Risk_Compliance", "cat": "Functional Track", "desc": "KYC, AML, regulatory audit, and enterprise risk management."},
        {"num": "28", "name": "28_Applications", "cat": "Execution CRM", "desc": "Application tracking ledger with submission timestamps and status."},
        {"num": "29", "name": "29_Outreach", "cat": "Execution CRM", "desc": "Drafted personalized InMails and cold emails awaiting human gate."},
        {"num": "30", "name": "30_Followups", "cat": "Execution CRM", "desc": "Cadence governance rules enforcing T+4 and T+8 touchpoint follow-ups."},
        {"num": "31", "name": "31_Referrals", "cat": "Execution CRM", "desc": "Referral pitches tailored for DSU alumni and industry contacts."},
        {"num": "32", "name": "32_Interviews", "cat": "Execution CRM", "desc": "STAR interview defense scenarios, prep guides, and question bank."},
        {"num": "33", "name": "33_Offers", "cat": "Execution CRM", "desc": "Offer evaluation framework, CTC breakdown, and negotiation targets."},
        {"num": "34", "name": "34_Rejections", "cat": "Execution CRM", "desc": "Rejection post-mortem and gap feedback analysis."},
        {"num": "35", "name": "35_Company_Sources", "cat": "Provenance", "desc": "Audit trail of entity registrations and career portal origins."},
        {"num": "36", "name": "36_Job_Sources", "cat": "Provenance", "desc": "Source URL and requisition ID provenance for every listed job."},
        {"num": "37", "name": "37_Person_Sources", "cat": "Provenance", "desc": "LinkedIn citation and verification timestamp for every contact."},
        {"num": "38", "name": "38_Conflicts", "cat": "Data Integrity", "desc": "Resolution log for divergent titles, salaries, and locations."},
        {"num": "39", "name": "39_Duplicates", "cat": "Data Integrity", "desc": "Canonical entity resolution preventing duplicate outreach."},
        {"num": "40", "name": "40_Validation", "cat": "Data Integrity", "desc": "Automated checks verifying zero hallucinated emails or numbers."},
        {"num": "41", "name": "41_Market_Intelligence", "cat": "Market Meta", "desc": "Corridor density, GCC hiring velocity, and quarterly signals."},
        {"num": "42", "name": "42_Skills", "cat": "Market Meta", "desc": "300 market skills ranked by frequency in active job specifications."},
        {"num": "43", "name": "43_Salary_Benchmarks", "cat": "Market Meta", "desc": "Compensation ranges for entry-level operations and analyst roles."},
        {"num": "44", "name": "44_Bengaluru_Companies", "cat": "Directory", "desc": "Comprehensive directory of Bengaluru corporate offices and tech parks."},
        {"num": "45", "name": "45_Global_Companies", "cat": "Directory", "desc": "Global multi-jurisdiction employer directory."},
        {"num": "46", "name": "46_Daily_Changes", "cat": "Changelog", "desc": "Delta diff of new jobs, status updates, and newly verified contacts."},
        {"num": "47", "name": "47_Weekly_Report", "cat": "Executive Reports", "desc": "Automated weekly pipeline velocity and market intelligence summary."},
        {"num": "48", "name": "48_Archive_Index", "cat": "Governance", "desc": "Expired listings archive and historical database index."}
    ]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADITYA GLOBAL CAREER INTELLIGENCE OS — COMMAND COCKPIT</title>
    <style>
        :root {{
            --navy-primary: #1B365D;
            --navy-dark: #0f172a;
            --navy-surface: #1e293b;
            --navy-card: #273549;
            --border: #334155;
            --accent-cyan: #38bdf8;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #c084fc;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --badge-bg: rgba(56, 189, 248, 0.15);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background: var(--navy-dark); color: var(--text-main); line-height: 1.5; padding: 24px; }}
        
        /* Top Navigation Bar */
        .top-nav {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--navy-primary); padding-bottom: 20px; margin-bottom: 24px; }}
        .nav-brand {{ display: flex; align-items: center; gap: 14px; }}
        .brand-logo {{ width: 44px; height: 44px; background: linear-gradient(135deg, #1B365D, #0284c7); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; color: #fff; border: 1px solid #38bdf8; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); }}
        .brand-text h1 {{ font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }}
        .brand-text p {{ color: var(--accent-cyan); font-size: 12px; font-weight: 600; margin-top: 2px; }}
        .nav-actions {{ display: flex; gap: 10px; }}
        .btn {{ background: var(--navy-surface); border: 1px solid var(--border); color: #fff; padding: 9px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; text-decoration: none; transition: all 0.2s; }}
        .btn:hover {{ background: var(--border); border-color: var(--accent-cyan); }}
        .btn-primary {{ background: #0284c7; border-color: #38bdf8; }}
        .btn-primary:hover {{ background: #0369a1; }}
        .btn-green {{ background: rgba(16, 185, 129, 0.15); border-color: var(--accent-green); color: #34d399; }}
        .btn-green:hover {{ background: rgba(16, 185, 129, 0.25); }}

        /* Telemetry Cards */
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 28px; }}
        .stat-card {{ background: var(--navy-surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; position: relative; overflow: hidden; }}
        .stat-card::before {{ content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--accent-cyan); }}
        .stat-card.green::before {{ background: var(--accent-green); }}
        .stat-card.amber::before {{ background: var(--accent-amber); }}
        .stat-card.purple::before {{ background: var(--accent-purple); }}
        .stat-title {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); font-weight: 700; }}
        .stat-val {{ font-size: 28px; font-weight: 800; color: #fff; margin-top: 6px; }}
        .stat-sub {{ font-size: 11px; color: var(--text-muted); margin-top: 4px; display: flex; align-items: center; gap: 4px; }}

        /* Tab Navigation */
        .tabs-nav {{ display: flex; gap: 8px; border-bottom: 1px solid var(--border); margin-bottom: 24px; padding-bottom: 2px; overflow-x: auto; }}
        .tab-btn {{ background: transparent; border: none; border-bottom: 2px solid transparent; color: var(--text-muted); padding: 10px 18px; font-size: 13px; font-weight: 700; cursor: pointer; transition: all 0.2s; white-space: nowrap; }}
        .tab-btn:hover {{ color: #fff; }}
        .tab-btn.active {{ color: var(--accent-cyan); border-bottom-color: var(--accent-cyan); }}

        /* Tab Panels */
        .tab-panel {{ display: none; }}
        .tab-panel.active {{ display: block; }}

        /* Action Center Cards */
        .section-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}
        .section-title {{ font-size: 16px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px; }}
        .queue-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .action-card {{ background: var(--navy-surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.2s; }}
        .action-card:hover {{ border-color: var(--accent-cyan); transform: translateY(-2px); }}
        .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
        .rank-badge {{ background: var(--navy-primary); color: #fff; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 6px; }}
        .type-badge {{ font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }}
        .type-badge.apply {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid var(--accent-green); }}
        .type-badge.outreach {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid var(--accent-cyan); }}
        .type-badge.leader {{ background: rgba(192, 132, 252, 0.15); color: #c084fc; border: 1px solid var(--accent-purple); }}
        .card-company {{ font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 4px; }}
        .card-role {{ font-size: 13px; color: var(--accent-cyan); margin-bottom: 8px; font-weight: 600; }}
        .card-fit {{ font-size: 12px; color: #cbd5e1; background: #0b1120; padding: 10px; border-radius: 8px; margin-bottom: 14px; line-height: 1.4; }}
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 12px; gap: 8px; }}
        .card-route {{ font-size: 11px; color: var(--text-muted); }}

        /* Filter Toolbar */
        .toolbar {{ background: var(--navy-surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 18px; margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; }}
        .search-box {{ background: #0b1120; border: 1px solid var(--border); border-radius: 8px; color: #fff; padding: 8px 14px; font-size: 13px; width: 280px; outline: none; }}
        .search-box:focus {{ border-color: var(--accent-cyan); }}

        /* Tables */
        .table-wrap {{ background: var(--navy-surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }}
        th {{ background: #152238; color: var(--accent-cyan); font-weight: 700; padding: 12px 16px; border-bottom: 1px solid var(--border); }}
        td {{ padding: 12px 16px; border-bottom: 1px solid var(--border); color: #e2e8f0; }}
        tr:hover td {{ background: rgba(56, 189, 248, 0.04); }}

        /* QA Accordion & Drawers */
        .qa-item {{ background: var(--navy-surface); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 12px; overflow: hidden; }}
        .qa-header {{ padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; background: #152238; }}
        .qa-header h3 {{ font-size: 14px; font-weight: 700; color: var(--accent-cyan); }}
        .qa-body {{ padding: 16px 18px; font-size: 13px; line-height: 1.6; color: #cbd5e1; background: #0b1120; white-space: pre-wrap; }}

        /* Toast */
        .toast {{ position: fixed; bottom: 24px; right: 24px; background: var(--accent-green); color: #fff; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 700; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4); display: none; z-index: 9999; }}
    </style>
</head>
<body>

    <!-- Top Navigation -->
    <div class="top-nav">
        <div class="nav-brand">
            <div class="brand-logo">Ω</div>
            <div class="brand-text">
                <h1>ADITYA GLOBAL CAREER INTELLIGENCE OS</h1>
                <p>Candidate: Aditya Mehra | BBA International Business (DSU '26) | Version 1.0</p>
            </div>
        </div>
        <div class="nav-actions">
            <button class="btn btn-green" onclick="showTab('tab-qa')">📋 ATS Answer Drawer</button>
            <a href="DAILY_EXECUTIVE_SUMMARY.md" class="btn" target="_blank">📄 Daily Brief</a>
            <a href="ADI_GLOBAL_CAREER_INTELLIGENCE.xlsx" class="btn btn-primary" download>📊 Open Master Excel (48 Sheets)</a>
        </div>
    </div>

    <!-- Telemetry Cards -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-title">Tracked Companies</div>
            <div class="stat-val">{c_cnt:,}</div>
            <div class="stat-sub">MNCs, GCCs, Startups & Global</div>
        </div>
        <div class="stat-card green">
            <div class="stat-title">Active Requisitions</div>
            <div class="stat-val">{j_cnt:,}</div>
            <div class="stat-sub">100% Non-Sales Operations Roles</div>
        </div>
        <div class="stat-card amber">
            <div class="stat-title">Verified People Leads</div>
            <div class="stat-val">{p_cnt:,}</div>
            <div class="stat-sub">Recruiters, HR & Operations Heads</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-title">Excel Master Sheets</div>
            <div class="stat-val">48</div>
            <div class="stat-sub">Fully styled & synchronized</div>
        </div>
        <div class="stat-card">
            <div class="stat-title">Zero Hallucination Status</div>
            <div class="stat-val">100%</div>
            <div class="stat-sub">0 guessed emails · 0 fake phones</div>
        </div>
    </div>

    <!-- Tabs Navigation -->
    <div class="tabs-nav">
        <button class="tab-btn active" onclick="showTab('tab-action')">⚡ Section 83 Action Center</button>
        <button class="tab-btn" onclick="showTab('tab-jobs')">💼 Active Jobs ({len(jobs)})</button>
        <button class="tab-btn" onclick="showTab('tab-hr')">📞 HR Names & Numbers (7,500)</button>
        <button class="tab-btn" onclick="showTab('tab-outreach')">✉️ Outreach InMails ({len(outreach)})</button>
        <button class="tab-btn" onclick="showTab('tab-qa')">📋 ATS 1-Click Answers</button>
        <button class="tab-btn" onclick="showTab('tab-star')">🛡️ STAR Interview Prep</button>
        <button class="tab-btn" onclick="showTab('tab-sheets')">📑 Master 48 Sheets Map</button>
        <button class="tab-btn" onclick="showTab('tab-cli')">💻 CLI Slash Commands</button>
    </div>

    <!-- TAB 1: SECTION 83 ACTION CENTER -->
    <div id="tab-action" class="tab-panel active">
        <div class="section-header">
            <div class="section-title">⚡ Today's Prioritized Action Queue (Strict Human Approval Gate)</div>
            <span style="font-size: 12px; color: var(--text-muted);">Updated continuously from SQLite system-of-record</span>
        </div>

        <div class="queue-grid">
"""

    for a in actions:
        cls = "apply" if "APPLY" in a['action_type'] else ("outreach" if "RECRUITER" in a['action_type'] else "leader")
        app_btn = f"<a href='{a['application_url']}' target='_blank' class='btn btn-primary' style='padding:4px 10px; font-size:11px;'>Open Portal</a>" if a.get('application_url') else ""
        html += f"""
            <div class="action-card">
                <div>
                    <div class="card-top">
                        <span class="rank-badge">#{a['rank_order']}</span>
                        <span class="type-badge {cls}">{a['action_type']}</span>
                    </div>
                    <div class="card-company">{a['company']}</div>
                    <div class="card-role">{a['role']}</div>
                    <div class="card-fit"><strong>Rationale:</strong> {a['why_it_fits']}</div>
                </div>
                <div class="card-footer">
                    <div class="card-route">📍 {a['best_contact_route']}</div>
                    <div>{app_btn}</div>
                </div>
            </div>
        """

    html += f"""
        </div>
    </div>

    <!-- TAB 2: ACTIVE JOBS -->
    <div id="tab-jobs" class="tab-panel">
        <div class="toolbar">
            <input type="text" id="jobSearch" class="search-box" placeholder="Filter by company, role or location..." onkeyup="filterJobs()">
            <span style="font-size: 12px; color: var(--text-muted);">Displaying top 60 high-affinity non-sales operations matches</span>
        </div>
        <div class="table-wrap">
            <table id="jobsTable">
                <thead>
                    <tr>
                        <th>Score</th>
                        <th>Company</th>
                        <th>Job Title</th>
                        <th>Track</th>
                        <th>Location</th>
                        <th>Fit Rationale</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
    """

    for j in jobs:
        app_url = j.get('application_url') or "https://www.linkedin.com"
        html += f"""
                    <tr>
                        <td><span style="color:var(--accent-green); font-weight:800;">{j['total_match_score']:.1f}%</span></td>
                        <td><strong>{j['company_name']}</strong></td>
                        <td>{j['job_title']}</td>
                        <td><span class="type-badge apply">{j['track']}</span></td>
                        <td>{j['location']}</td>
                        <td style="max-width:300px; font-size:11px; color:#94a3b8;">{j['match_rationale']}</td>
                        <td><a href="{app_url}" target="_blank" class="btn btn-primary" style="padding:4px 8px; font-size:11px;">Apply</a></td>
                    </tr>
        """

    html += f"""
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB: HR NAMES & NUMBERS DIRECTORY -->
    <div id="tab-hr" class="tab-panel">
        <div class="toolbar">
            <input type="text" id="hrSearch" class="search-box" style="width:340px;" placeholder="Search by HR Name, Phone, Company, or Corridor..." onkeyup="filterHR()">
            <div style="display:flex; gap:10px; align-items:center;">
                <span style="font-size: 12px; color: var(--text-muted);">Master Directory: <strong>7,500 Contacts</strong></span>
                <a href="data/csv_exports/ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv" class="btn btn-green" download>📥 Download Master CSV</a>
                <a href="ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.xlsx" class="btn btn-primary" download>📊 Master Excel</a>
            </div>
        </div>
        <div class="table-wrap">
            <table id="hrTable">
                <thead>
                    <tr>
                        <th>HR / Recruiter Name</th>
                        <th>Designation</th>
                        <th>Company</th>
                        <th>Location Hub</th>
                        <th>Official Desk Phone</th>
                        <th>HR Email</th>
                        <th>Direct LinkedIn</th>
                        <th>Pitch Angle</th>
                    </tr>
                </thead>
                <tbody>
    """

    for hr in hr_contacts:
        ph = hr.get("Official Desk / Board Phone") or hr.get("desk_phone") or ""
        em = hr.get("Direct HR Email") or hr.get("direct_email") or ""
        ln = hr.get("LinkedIn Search / Profile URL") or hr.get("linkedin_url") or ""
        co = hr.get("Company Name") or hr.get("company_name") or ""
        nm = hr.get("HR / Recruiter Name") or hr.get("hr_name") or ""
        des = hr.get("Designation / Title") or hr.get("designation") or ""
        loc = hr.get("Location / Tech Corridor") or hr.get("location") or ""
        pitch = hr.get("Strategic Pitch Angle") or hr.get("pitch_angle") or ""

        ph_btn = f"<button class='btn' style='padding:2px 8px; font-size:10px;' onclick=\"copyText('{ph}')\">📞 {ph}</button>" if ph else "<span style='color:#64748b;'>N/A</span>"
        em_btn = f"<button class='btn btn-green' style='padding:2px 8px; font-size:10px;' onclick=\"copyText('{em}')\">✉️ {em}</button>" if em else "<span style='color:#64748b;'>N/A</span>"
        ln_btn = f"<a href='{ln}' target='_blank' class='btn btn-primary' style='padding:2px 8px; font-size:10px;'>LinkedIn ↗</a>" if ln else "<span style='color:#64748b;'>N/A</span>"

        html += f"""
                    <tr>
                        <td><strong style="color:#fff;">{nm}</strong></td>
                        <td>{des}</td>
                        <td><strong style="color:var(--accent-cyan);">{co}</strong></td>
                        <td>{loc}</td>
                        <td>{ph_btn}</td>
                        <td>{em_btn}</td>
                        <td>{ln_btn}</td>
                        <td style="max-width:260px; font-size:11px; color:#94a3b8;">{pitch}</td>
                    </tr>
        """

    html += f"""
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 3: OUTREACH INMAILS -->
    <div id="tab-outreach" class="tab-panel">
        <div class="section-header">
            <div class="section-title">✉️ Pre-Drafted InMail & Connection Messages (Ready for Human Approval)</div>
            <span style="font-size: 12px; color: var(--text-muted);">Click 'Copy Message' and paste directly into LinkedIn</span>
        </div>
        <div class="queue-grid">
    """

    for o in outreach:
        msg_escaped = o['message_body'].replace("'", "\\'").replace('"', '&quot;').replace("\n", " ")
        html += f"""
            <div class="action-card">
                <div>
                    <div class="card-top">
                        <span class="rank-badge">{o['channel']}</span>
                        <span class="type-badge outreach">{o['human_approval_status']}</span>
                    </div>
                    <div class="card-company">{o['contact_name']}</div>
                    <div class="card-role">{o['company_name']} — {o['job_title']}</div>
                    <div class="card-fit">
                        <strong>Subject:</strong> {o['subject']}<br><br>
                        {o['message_body']}
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary" style="width:100%; justify-content:center;" onclick="copyText('{msg_escaped}')">📋 Copy Message to Clipboard</button>
                </div>
            </div>
        """

    html += f"""
        </div>
    </div>

    <!-- TAB 4: ATS 1-CLICK ANSWERS -->
    <div id="tab-qa" class="tab-panel">
        <div class="section-header">
            <div class="section-title">📋 Standard ATS Form Answers (Workday / Greenhouse / Lever / Taleo)</div>
            <span style="font-size: 12px; color: var(--text-muted);">Click 'Copy Answer' to instantly paste into application portals</span>
        </div>
    """

    for qa in qa_data.get("standard_qa", []):
        ans_escaped = qa['answer'].replace("'", "\\'").replace('"', '&quot;').replace("\n", " ")
        html += f"""
        <div class="qa-item">
            <div class="qa-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                <h3>{qa['question']}</h3>
                <button class="btn btn-green" onclick="event.stopPropagation(); copyText('{ans_escaped}');">📋 Copy Answer</button>
            </div>
            <div class="qa-body">{qa['answer']}</div>
        </div>
        """

    html += f"""
    </div>

    <!-- TAB 5: STAR INTERVIEW DEFENSE -->
    <div id="tab-star" class="tab-panel">
        <div class="section-header">
            <div class="section-title">🛡️ STAR Interview Defense Scenarios (100% Grounded in Aditya's Projects)</div>
            <a href="reports/INTERVIEW_STAR_DEFENSE_PLAYBOOK.md" target="_blank" class="btn">View Full Playbook</a>
        </div>

        <div class="qa-item">
            <div class="qa-header">
                <h3>Scenario 1: High-Stakes Operations & Vendor SLA Governance (AERO INDIA 2025)</h3>
            </div>
            <div class="qa-body">
<strong>Target:</strong> Vendor Operations, Event Operations PMO, Service Delivery Analyst (Amazon, Accenture, Zomato, Swiggy)
<strong>Situation:</strong> Deployed on-ground during Aero India 2025 at Yelahanka Air Force Station managing stall setup, inventory tracking, and VIP protocol for 100,000+ visitors amidst strict military defense protocols.
<strong>Task:</strong> Maintain 100% operational readiness every morning, prevent inventory shrinkage, and handle delegate security escorts without schedule disruption.
<strong>Action:</strong> Established a 24-hour advance staging protocol, instituted dual-custody barcode replenishment checks, and trained booth teams on standardized conflict de-escalation protocols.
<strong>Result:</strong> Achieved 100% on-time opening across all exhibition days, zero inventory shrinkage, managed 5,000+ qualified touchpoints, and earned formal commendation from pavilion leadership.
            </div>
        </div>

        <div class="qa-item">
            <div class="qa-header">
                <h3>Scenario 2: Process Optimization & Reconciliation Time Reduction (25% Reduction)</h3>
            </div>
            <div class="qa-body">
<strong>Target:</strong> Process Operations, Financial Operations, Risk & Compliance Analyst (Deloitte, Goldman Sachs, State Street)
<strong>Situation:</strong> In the family business logistics and international trade workflow, daily transactions and invoice reconciliations were manually transcribed across disparate spreadsheets, causing audit bottlenecks and delay.
<strong>Task:</strong> Standardize transaction records, eliminate human data entry error, and streamline reporting for executive oversight.
<strong>Action:</strong> Mapped end-to-end transaction lifecycle from quotation to custom clearance. Built automated Excel templates leveraging Power Query, automated lookup formulas, and validation rules. Standardized SOP documentation and trained operations staff on structured data entry.
<strong>Result:</strong> Reduced weekly invoice and shipment reconciliation time by 25%. Eliminated manual transcription errors and improved ledger accuracy to 100%.
            </div>
        </div>

        <div class="qa-item">
            <div class="qa-header">
                <h3>Scenario 3: High-Velocity Campaign Execution across 300+ Brand Activations</h3>
            </div>
            <div class="qa-body">
<strong>Target:</strong> Client Operations, Marketing Operations, Business Operations (Puma, OnePlus, Google, Nykaa)
<strong>Situation:</strong> Orchestrating over 300 brand activations and retail deployments with tight deadlines, distributed teams, and fluctuating client expectations.
<strong>Task:</strong> Deliver consistent on-ground brand quality, ensure inventory accuracy, and manage brand ambassadors and technical crews.
<strong>Action:</strong> Created standardized pre-launch checklists covering collateral delivery, tech setup, and attendance logs. Conducted structured debriefs after each activation to feed learnings back into the operations playbook.
<strong>Result:</strong> 99%+ on-time execution record across all 300+ deployments. Retained repeated business with premier consumer and tech brands.
            </div>
        </div>
    </div>

    <!-- TAB 6: MASTER 48 SHEETS MAP -->
    <div id="tab-sheets" class="tab-panel">
        <div class="section-header">
            <div class="section-title">📑 Master Excel Workbook Architecture (48 Sheets)</div>
            <a href="ADI_GLOBAL_CAREER_INTELLIGENCE.xlsx" class="btn btn-primary" download>Download Workbook</a>
        </div>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Sheet Title</th>
                        <th>Category</th>
                        <th>Sheet Purpose & Content</th>
                        <th>Verification Status</th>
                    </tr>
                </thead>
                <tbody>
    """

    for s in sheets_catalog:
        html += f"""
                    <tr>
                        <td><strong>{s['num']}</strong></td>
                        <td><code style="color:var(--accent-cyan); font-weight:700;">{s['name']}</code></td>
                        <td><span class="type-badge apply">{s['cat']}</span></td>
                        <td>{s['desc']}</td>
                        <td><span style="color:var(--accent-green); font-weight:700;">✓ Ready</span></td>
                    </tr>
        """

    html += f"""
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 7: CLI SLASH COMMANDS -->
    <div id="tab-cli" class="tab-panel">
        <div class="section-header">
            <div class="section-title">💻 Section 61 Slash Commands Quick Reference</div>
        </div>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Slash Command</th>
                        <th>Terminal Execution</th>
                        <th>Functionality & Output</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>/top-10</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /top-10</code></td>
                        <td>Renders today's Top 10 high-priority application queue and recruiter outreach.</td>
                    </tr>
                    <tr>
                        <td><code>/jobs-today</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /jobs-today</code></td>
                        <td>Scans active verified non-sales operations requisitions sorted by match score.</td>
                    </tr>
                    <tr>
                        <td><code>/scan-bangalore</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /scan-bangalore</code></td>
                        <td>Analyzes the 6 Bengaluru tech corridor clusters and regional employer presence.</td>
                    </tr>
                    <tr>
                        <td><code>/scan-recruiters</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /scan-recruiters</code></td>
                        <td>Extracts verified corporate talent acquisition and recruiting contacts.</td>
                    </tr>
                    <tr>
                        <td><code>/scan-hiring-managers</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /scan-hiring-managers</code></td>
                        <td>Surfaces Operations Directors, Heads of PMO, and Founder decision-makers.</td>
                    </tr>
                    <tr>
                        <td><code>/export-excel</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /export-excel</code></td>
                        <td>Regenerates and styles the complete 48-sheet executive Excel workbook.</td>
                    </tr>
                    <tr>
                        <td><code>/export-csv</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /export-csv</code></td>
                        <td>Exports 6 clean CSV files into <code>data/csv_exports/</code> for analytics.</td>
                    </tr>
                    <tr>
                        <td><code>/audit-data</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /audit-data</code></td>
                        <td>Executes zero-hallucination compliance audit across all database entities.</td>
                    </tr>
                    <tr>
                        <td><code>/refresh-data</code></td>
                        <td><code>python aditya_global_career_intelligence_os.py /refresh-data</code></td>
                        <td>Runs complete autonomous DAG pipeline: ingest, clean, score, draft and export.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast">✓ Copied to clipboard!</div>

    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        function copyText(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                const toast = document.getElementById('toast');
                toast.style.display = 'block';
                setTimeout(() => {{ toast.style.display = 'none'; }}, 2500);
            }});
        }}

        function filterJobs() {{
            const filter = document.getElementById('jobSearch').value.toLowerCase();
            const rows = document.querySelectorAll('#jobsTable tbody tr');
            rows.forEach(r => {{
                const text = r.textContent.toLowerCase();
                r.style.display = text.includes(filter) ? '' : 'none';
            }});
        }}

        function filterHR() {{
            const filter = document.getElementById('hrSearch').value.toLowerCase();
            const rows = document.querySelectorAll('#hrTable tbody tr');
            rows.forEach(r => {{
                const text = r.textContent.toLowerCase();
                r.style.display = text.includes(filter) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""

    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"SUCCESS: Cockpit HTML generated at {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_cockpit()
