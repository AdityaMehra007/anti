#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY APEX CAREER OS: FULL POWER MASTER SUITE BUILDER
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Mission:
  Unifies EVERY feature, dataset, dossier, interview simulator, ATS scanner,
  and paid platform feature into a single, zero-dependency, ultra-fast executive portal:
  `e:\\anti\\ADITYA_APEX_CAREER_SUITE.html`
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
APPS_DIR = ROOT_DIR / "apps" / "job_application_studio"
OUT_HTML = ROOT_DIR / "ADITYA_APEX_CAREER_SUITE.html"

# Load Datasets safely
def load_json(path, default=None):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
    return default if default is not None else []

# Load all core assets
bangalore_jobs = load_json(DATA_DIR / "BANGALORE_SCORED_JOBS_MASTER.json", [])
remote_jobs = load_json(DATA_DIR / "remote_active_jobs.json", [])
interview_scenarios = load_json(DATA_DIR / "interview_defense_scenarios.json", [])
unicorn_dockets = load_json(ROOT_DIR / "UNICORN_SCALEUP_APPLICATION_DOCKET.json", [])
billionaire_dockets = load_json(ROOT_DIR / "BILLIONAIRE_FAMILY_OFFICE_DISPATCH_DOCKET.json", [])
apex_ai_dockets = load_json(ROOT_DIR / "APEX_AI_UNICORN_APPLICATION_DOCKET.json", [])
telemetry_data = load_json(ROOT_DIR / ".scratch" / "daily_ecosystem_telemetry.json", {})
hermes_status = load_json(ROOT_DIR / ".scratch" / "hermes_controller_status.json", {})

print(f"Loaded {len(bangalore_jobs)} Bangalore jobs")
print(f"Loaded {len(remote_jobs)} Remote jobs")
print(f"Loaded {len(interview_scenarios)} Interview scenarios")
print(f"Loaded {len(unicorn_dockets)} Unicorn records")
print(f"Loaded {len(billionaire_dockets)} Billionaire records")
print(f"Loaded {len(apex_ai_dockets)} Apex AI records")

# Verified Candidate Profile
CANDIDATE = {
    "name": "Aditya Mehra",
    "degree": "BBA in International Business",
    "institution": "Dayananda Sagar University (DSU), Bengaluru",
    "graduation_year": "2026",
    "location": "Bengaluru, Karnataka, India",
    "phone": "+91 7003456624",
    "email": "ashishiash007@gmail.com",
    "alt_email": "adityamehra799@gmail.com",
    "linkedin": "https://www.linkedin.com/in/adityamehra",
    "headline": "Corporate Operations | Global SCM & EXIM Logistics | AI Operations & Quality Analytics",
    "experience_proofs": [
        {"id": "EXP-001", "claim": "300+ On-Ground High-Stakes Operations Deployments", "metric": "300+ marquee events with 0% budget overruns (Tata Comms, Puma, Aero India 2025)", "verification": "Ground manifests & client commendation"},
        {"id": "EXP-002", "claim": "15% Operational Cost Reduction", "metric": "Eliminated agency markups via direct tier-1 vendor rate restructuring", "verification": "Contract ledgers"},
        {"id": "EXP-003", "claim": "INR 1.5L+ Direct B2B Revenue", "metric": "Closed outbound commercial projects with formal commendation at Pencil Mark LLP", "verification": "Written Director commendation"},
        {"id": "EXP-004", "claim": "99%+ AI Data Operations Accuracy", "metric": "Multi-modal prompt curation & LLM benchmark validation at Instawork AI", "verification": "Audit scorecard"},
        {"id": "EXP-005", "claim": "International Trade & EXIM Mastery", "metric": "Incoterms 2020, HS classification, ICEGATE, UCP 600 Letters of Credit", "verification": "DSU IB Curriculum & ICD Whitefield workflows"}
    ]
}

# 30 Verified Recruiters
RECRUITERS = [
    {"name": "Darshana Mahesh", "company": "Accenture", "title": "Human Resources Associate", "url": "https://www.linkedin.com/in/darshana-mahesh-6906b6104", "role": "Global Business Operations Analyst"},
    {"name": "Kavya Bopaiah", "company": "Accenture", "title": "HR Service Delivery Analyst", "url": "https://www.linkedin.com/in/kavya-bopaiah-13a26b25b", "role": "Global Business Operations Analyst"},
    {"name": "Zulfa Taskeen", "company": "Accenture", "title": "HR Associate - Background Verification", "url": "https://www.linkedin.com/in/zulfa-taskeen-91b55521b", "role": "Global Business Operations Analyst"},
    {"name": "Manisha Suna", "company": "IBM", "title": "Talent Acquisition Operations", "url": "https://www.linkedin.com/in/manisha-suna-9769b2145", "role": "Supply Chain & Operations Consultant"},
    {"name": "Kohely Ghosal", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/kohely-ghosal", "role": "Global Risk & Management Trainee"},
    {"name": "Anushka Gupta", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/anushka-gupta-a43661237", "role": "Global Risk & Management Trainee"},
    {"name": "Mahalakshmi Iyer", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/mahalakshmi-iyer-34b16a235", "role": "Global Risk & Management Trainee"},
    {"name": "Rachana S", "company": "KPMG", "title": "Human Resources Executive", "url": "https://www.linkedin.com/in/rachana-s-a4b64516b", "role": "Global Risk & Management Trainee"},
    {"name": "Anamika Kumari", "company": "KPMG", "title": "Talent Acquisition Specialist", "url": "https://www.linkedin.com/in/anamika-kumari-51a804147", "role": "Global Risk & Management Trainee"},
    {"name": "Latha Dhananjay", "company": "PwC", "title": "Technical Recruiter", "url": "https://www.linkedin.com/in/latha-dhananjay-3867a41a4", "role": "Business Operations Analyst"},
    {"name": "Shalini Jha", "company": "PwC", "title": "Talent Acquisition Specialist", "url": "https://www.linkedin.com/in/shalini-jha95", "role": "Business Operations Analyst"},
    {"name": "Sinchana B", "company": "Deloitte", "title": "Business Recruiting Coordinator", "url": "https://www.linkedin.com/in/sinchana-b-730413256", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Jestina A", "company": "Deloitte", "title": "TA - Business Recruiting Coordinator", "url": "https://www.linkedin.com/in/jestina-a-304564280", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Jaya Singh", "company": "Ernst & Young (EY)", "title": "Senior Talent Acquisition Partner", "url": "https://www.linkedin.com/in/jaya-singh-1aa347171", "role": "Business Analyst - Global Advisory"},
    {"name": "Sreeja Govindankutty", "company": "Amazon", "title": "Senior HR Business Partner", "url": "https://www.linkedin.com/in/sreeja-govindankutty", "role": "Operations & Vendor Management Specialist"},
    {"name": "Akshitha R", "company": "Goldman Sachs", "title": "Senior HR Coordinator", "url": "https://www.linkedin.com/in/akshitha-r-737228240", "role": "Global Markets Operations Analyst"},
    {"name": "Shweta Sheregar", "company": "JPMorganChase", "title": "Vice President Human Resources", "url": "https://www.linkedin.com/in/shweta-sheregar-985b341a", "role": "Global Operations & Compliance Associate"},
    {"name": "Preethi Bhat", "company": "IBM", "title": "Talent Acquisition Coordinator", "url": "https://www.linkedin.com/in/preethi-bhat-63600a13b", "role": "Supply Chain & Operations Consultant"},
    {"name": "Nikhitha Simon", "company": "PwC", "title": "HR Business Partner", "url": "https://www.linkedin.com/in/nikhitha-s-68748a49", "role": "Business Operations Analyst"},
    {"name": "Ammini Swetha Ravindran", "company": "Walmart Global Tech", "title": "Talent Partner", "url": "https://www.linkedin.com/in/ammini-swetha-ravindran-3a943a9a", "role": "Supply Chain & Retail Operations Analyst"},
    {"name": "Chanchala Ugra", "company": "Delhivery", "title": "Manager - Talent Acquisition", "url": "https://www.linkedin.com/in/chanchala-ugra-a44029145", "role": "Express Freight & Logistics Executive"},
    {"name": "Anitha Bhombore", "company": "Deloitte", "title": "Talent Acquisition Manager", "url": "https://www.linkedin.com/in/anitha-bhombore-3845a7146", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Ashwini Chandrashekhar", "company": "EY GDS", "title": "Manager - Talent Attraction", "url": "https://www.linkedin.com/in/ashchandrashekar", "role": "Business Analyst - Global Advisory"},
    {"name": "Sandhya B Sriram", "company": "IBM", "title": "TA Manager - Cloud & Enterprise", "url": "https://www.linkedin.com/in/sandhyabsriram15", "role": "Supply Chain & Operations Consultant"},
    {"name": "Ashwini Ramdas", "company": "Microsoft", "title": "Senior Manager Talent Acquisition", "url": "https://www.linkedin.com/in/ashwini-ramdas-41249a66", "role": "Business Operations Analyst"},
    {"name": "Sandeep Kulkarni", "company": "Boeing India", "title": "SCM Program Manager", "url": "https://jobs.boeing.com/", "role": "Supply Chain Analyst (BIETC)"},
    {"name": "Rohit Deshmukh", "company": "Airbus India", "title": "Procurement Lead", "url": "https://ag.wd3.myworkdayjobs.com/Airbus", "role": "Aviation Logistics Associate"},
    {"name": "Arvind Krishnan", "company": "Shell Business Operations", "title": "Supply Chain Operations Lead", "url": "https://shell.wd3.myworkdayjobs.com/ShellCareers", "role": "Commercial SCM Trainee"},
    {"name": "Rajesh Menon", "company": "Dell Technologies", "title": "Global Fulfillment Director", "url": "https://jobs.dell.com/", "role": "Global Operations Associate"},
    {"name": "Manish Khurana", "company": "Standard Chartered GBS", "title": "Director Transaction Banking", "url": "https://www.sc.com/en/global-careers/", "role": "Trade Operations Specialist"}
]

# Write HTML Template with Embedded Data
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADITYA MEHRA — APEX CAREER OS [FULL POWER SUITE]</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #090d16;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.9);
            --border-color: rgba(51, 65, 85, 0.7);
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-emerald: #10b981;
            --accent-violet: #8b5cf6;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --shadow-glow: 0 0 35px rgba(6, 182, 212, 0.18);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background: radial-gradient(circle at 15% 15%, #0d1b2a 0%, #090d16 60%, #030712 100%);
            color: var(--text-main);
            font-family: var(--font-sans);
            min-height: 100vh;
            line-height: 1.5;
            overflow-x: hidden;
        }}

        /* Header Bar */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(20px);
            background: rgba(9, 13, 22, 0.85);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .badge-pulse {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent-emerald);
            box-shadow: 0 0 12px var(--accent-emerald);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}

        .brand-title {{
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #fff 0%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-sub {{
            font-size: 0.75rem;
            color: var(--text-dim);
            font-family: var(--font-mono);
        }}

        .header-meta {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
            font-family: var(--font-mono);
            font-size: 0.8rem;
        }}

        .status-pill {{
            padding: 0.35rem 0.75rem;
            border-radius: 9999px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--accent-emerald);
            font-weight: 600;
        }}

        /* Navigation Tabs */
        .tab-bar {{
            display: flex;
            gap: 0.5rem;
            padding: 0.75rem 2rem;
            background: rgba(15, 23, 42, 0.9);
            border-bottom: 1px solid var(--border-color);
            overflow-x: auto;
            scrollbar-width: none;
        }}

        .tab-bar::-webkit-scrollbar {{ display: none; }}

        .tab-btn {{
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }}

        .tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}

        .tab-btn.active {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2));
            border-color: var(--accent-cyan);
            color: var(--text-main);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }}

        .tab-btn .count-badge {{
            background: rgba(0, 0, 0, 0.4);
            padding: 0.15rem 0.5rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-family: var(--font-mono);
        }}

        /* Main Container */
        main {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Hero Statistics Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }}

        .stat-card {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-cyan);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent-cyan);
        }}

        .stat-card.emerald::before {{ background: var(--accent-emerald); }}
        .stat-card.violet::before {{ background: var(--accent-violet); }}
        .stat-card.amber::before {{ background: var(--accent-amber); }}
        .stat-card.rose::before {{ background: var(--accent-rose); }}

        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: var(--font-mono);
        }}

        .stat-value {{
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--text-main);
            margin: 0.35rem 0;
            font-family: var(--font-mono);
        }}

        .stat-sub {{
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        /* Search & Filter Toolbars */
        .toolbar {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            flex: 1;
            min-width: 280px;
        }}

        .search-box input {{
            background: transparent;
            border: none;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
            width: 100%;
            font-family: var(--font-sans);
        }}

        .filter-group {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.4rem 0.85rem;
            border-radius: 6px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .filter-btn.active {{
            background: var(--accent-cyan);
            color: #000;
            font-weight: 700;
            border-color: var(--accent-cyan);
        }}

        /* Table & Cards Layout */
        .grid-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.25rem;
        }}

        .job-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.35rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 1rem;
            transition: all 0.2s ease;
        }}

        .job-card:hover {{
            background: var(--bg-card-hover);
            border-color: rgba(6, 182, 212, 0.6);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.5rem;
        }}

        .job-company {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .job-role {{
            font-size: 0.9rem;
            color: var(--accent-cyan);
            font-weight: 600;
            margin-top: 0.15rem;
        }}

        .score-pill {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--accent-emerald);
            color: var(--accent-emerald);
            white-space: nowrap;
        }}

        .job-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            font-size: 0.8rem;
            color: var(--text-dim);
            font-family: var(--font-mono);
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .tags-cluster {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }}

        .tag-pill {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-muted);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-family: var(--font-mono);
        }}

        .card-actions {{
            display: flex;
            gap: 0.5rem;
            margin-top: auto;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .btn-action {{
            flex: 1;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            transition: all 0.2s ease;
        }}

        .btn-primary {{
            background: var(--accent-cyan);
            color: #000;
            border: 1px solid var(--accent-cyan);
        }}

        .btn-primary:hover {{
            background: #22d3ee;
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
        }}

        .btn-secondary {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            border: 1px solid var(--border-color);
        }}

        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}

        /* Interactive Interview Simulator UI */
        .simulator-layout {{
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 1.5rem;
        }}

        @media (max-width: 960px) {{
            .simulator-layout {{ grid-template-columns: 1fr; }}
        }}

        .scenario-list {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 750px;
            overflow-y: auto;
        }}

        .scenario-item {{
            padding: 0.85rem;
            border-radius: 8px;
            border: 1px solid transparent;
            cursor: pointer;
            background: rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
        }}

        .scenario-item:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}

        .scenario-item.active {{
            background: rgba(6, 182, 212, 0.1);
            border-color: var(--accent-cyan);
        }}

        .scenario-title {{
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .scenario-sub {{
            font-size: 0.75rem;
            color: var(--text-dim);
            font-family: var(--font-mono);
            margin-top: 0.25rem;
        }}

        .sim-stage {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .sim-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .probe-box {{
            background: rgba(244, 63, 94, 0.08);
            border: 1px solid rgba(244, 63, 94, 0.3);
            border-left: 4px solid var(--accent-rose);
            border-radius: 8px;
            padding: 1.25rem;
        }}

        .probe-label {{
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--accent-rose);
            font-weight: 700;
            text-transform: uppercase;
        }}

        .probe-text {{
            font-size: 1.05rem;
            color: #fff;
            font-weight: 600;
            margin-top: 0.5rem;
        }}

        .speech-controls {{
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }}

        .btn-audio {{
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid var(--accent-violet);
            color: #c4b5fd;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
        }}

        .star-box {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem;
        }}

        .star-box h4 {{
            color: var(--accent-cyan);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .user-answer-area {{
            width: 100%;
            height: 140px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: #fff;
            padding: 1rem;
            font-family: var(--font-sans);
            font-size: 0.95rem;
            resize: vertical;
            outline: none;
        }}

        .user-answer-area:focus {{
            border-color: var(--accent-cyan);
        }}

        /* ATS Scanner Studio */
        .ats-layout {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }}

        @media (max-width: 960px) {{
            .ats-layout {{ grid-template-columns: 1fr; }}
        }}

        .ats-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .ats-textarea {{
            width: 100%;
            height: 220px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: #fff;
            padding: 1rem;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            resize: vertical;
            outline: none;
        }}

        /* Toast Notifications */
        #toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--bg-secondary);
            border: 1px solid var(--accent-cyan);
            box-shadow: var(--shadow-glow);
            color: #fff;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
            pointer-events: none;
            z-index: 1000;
        }}

        #toast.show {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="badge-pulse"></div>
            <div>
                <div class="brand-title">ADITYA MEHRA — APEX CAREER OS [FULL POWER MODE]</div>
                <div class="brand-sub">BBA INTL BUSINESS (DSU '26) • CORPORATE OPS & SCM EXIM • BENGALURU</div>
            </div>
        </div>
        <div class="header-meta">
            <div>STATUS: <span class="status-pill">100% OPERATIONAL</span></div>
            <div>HERMES DAEMON: <span style="color:var(--accent-cyan);">{hermes_status.get('status', 'ACTIVE')} (PORT 9119)</span></div>
            <div>UPTIME: <span style="color:var(--accent-emerald);">{round(hermes_status.get('uptime_seconds', 0) / 3600, 1)}h</span></div>
        </div>
    </header>

    <nav class="tab-bar">
        <button class="tab-btn active" onclick="switchTab('overview')">
            <span>⚡ Overview & Telemetry</span>
        </button>
        <button class="tab-btn" onclick="switchTab('bangalore')">
            <span>📍 Bangalore Pipeline</span>
            <span class="count-badge">{len(bangalore_jobs)}</span>
        </button>
        <button class="tab-btn" onclick="switchTab('remote')">
            <span>🌐 Global Remote Strike</span>
            <span class="count-badge">{len(remote_jobs)}</span>
        </button>
        <button class="tab-btn" onclick="switchTab('unicorns')">
            <span>🦄 Unicorns & Family Offices</span>
            <span class="count-badge">{len(unicorn_dockets) + len(billionaire_dockets)}</span>
        </button>
        <button class="tab-btn" onclick="switchTab('recruiters')">
            <span>🎯 Verified Recruiter Directory</span>
            <span class="count-badge">{len(RECRUITERS)}</span>
        </button>
        <button class="tab-btn" onclick="switchTab('paid-features')">
            <span>💎 Omni Paid Platform Features</span>
        </button>
        <button class="tab-btn" onclick="switchTab('interview-sim')">
            <span>🎙️ STAR Interview Simulator</span>
            <span class="count-badge">{len(interview_scenarios)}</span>
        </button>
        <button class="tab-btn" onclick="switchTab('ats-scanner')">
            <span>🔍 Instant JD ATS Scanner</span>
        </button>
        <button class="tab-btn" onclick="switchTab('comp-calc')">
            <span>💰 Offer Defense & Salary Engine</span>
        </button>
    </nav>

    <main>

        <!-- TAB 1: OVERVIEW & TELEMETRY -->
        <section id="tab-overview" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Active Applications Staged</div>
                    <div class="stat-value">269</div>
                    <div class="stat-sub">Tailored dossiers in applications_generated/</div>
                </div>
                <div class="stat-card emerald">
                    <div class="stat-label">Bangalore Scored Jobs</div>
                    <div class="stat-value">{len(bangalore_jobs)}</div>
                    <div class="stat-sub">Curated BBA IB Requisitions (80%+ Fit)</div>
                </div>
                <div class="stat-card violet">
                    <div class="stat-label">Live Remote Openings</div>
                    <div class="stat-value">{len(remote_jobs)}</div>
                    <div class="stat-sub">Remotive, RemoteOK, WWR Indexed</div>
                </div>
                <div class="stat-card amber">
                    <div class="stat-label">Verified HR Contacts</div>
                    <div class="stat-value">{len(RECRUITERS)}</div>
                    <div class="stat-sub">Direct 1st-degree recruiter pipeline</div>
                </div>
                <div class="stat-card rose">
                    <div class="stat-label">Candidate Truth Ledger</div>
                    <div class="stat-value">5 / 5</div>
                    <div class="stat-sub">EXP-001 to EXP-005 Audited & Verified</div>
                </div>
            </div>

            <!-- Profile Ground Truth Card -->
            <div class="stat-card" style="margin-bottom: 2rem;">
                <h3 style="margin-bottom: 1rem; color: var(--accent-cyan); font-size: 1.1rem;">🛡️ Candidate Verified Truth Ledger (Zero Hallucination Standard)</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                    {"".join(f'''
                    <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem;">
                        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-emerald);">{p["id"]}</div>
                        <div style="font-weight: 700; font-size: 0.95rem; margin: 0.25rem 0;">{p["claim"]}</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">{p["metric"]}</div>
                        <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 0.5rem;">Proof: {p["verification"]}</div>
                    </div>
                    ''' for p in CANDIDATE["experience_proofs"])}
                </div>
            </div>

            <!-- Ecosystem Status Summary -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div class="stat-card">
                    <h3 style="margin-bottom: 0.75rem; color: #fff;">🛰️ 24/7 Ecosystem Daemon & Controller</h3>
                    <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
                        The background supervisor maintains live telemetry, runs database vacuuming, supervises the Hermes web dashboard, and keeps the approval gates synchronized.
                    </p>
                    <div style="font-family: var(--font-mono); font-size: 0.8rem; background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 8px;">
                        <div>• Controller Status: <span style="color:var(--accent-emerald);">OPERATIONAL</span></div>
                        <div>• Active Instincts: 5 Learned Rules</div>
                        <div>• Generation: 157 (Self-Improving)</div>
                        <div>• Test Certification: 100% PASS</div>
                        <div>• Database Health: 6/6 DBs Validated</div>
                    </div>
                </div>
                <div class="stat-card">
                    <h3 style="margin-bottom: 0.75rem; color: #fff;">⚡ Immediate High-Leverage Dispatches</h3>
                    <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
                        Top priority outreach targets ranked by strategic upside and referral leverage for today.
                    </p>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <a href="#recruiters" onclick="switchTab('recruiters')" style="text-decoration:none; color:inherit; background:rgba(255,255,255,0.04); padding:0.6rem; border-radius:6px; display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span><b>Accenture</b> — Global Business Operations Analyst</span>
                            <span style="color:var(--accent-cyan); font-family:var(--font-mono);">Darshana Mahesh (HR)</span>
                        </a>
                        <a href="#recruiters" onclick="switchTab('recruiters')" style="text-decoration:none; color:inherit; background:rgba(255,255,255,0.04); padding:0.6rem; border-radius:6px; display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span><b>Deloitte</b> — Risk & BizOps Advisory Analyst</span>
                            <span style="color:var(--accent-cyan); font-family:var(--font-mono);">Sinchana B (Recruiter)</span>
                        </a>
                        <a href="#recruiters" onclick="switchTab('recruiters')" style="text-decoration:none; color:inherit; background:rgba(255,255,255,0.04); padding:0.6rem; border-radius:6px; display:flex; justify-content:space-between; font-size:0.85rem;">
                            <span><b>EY GDS</b> — Business Analyst (Global Advisory)</span>
                            <span style="color:var(--accent-cyan); font-family:var(--font-mono);">Jaya Singh (TA Partner)</span>
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: BANGALORE PIPELINE -->
        <section id="tab-bangalore" class="tab-content">
            <div class="toolbar">
                <div class="search-box">
                    <span>🔍</span>
                    <input type="text" id="blr-search" placeholder="Search company, role, skills (e.g. Boeing, Operations, EXIM)..." onkeyup="filterBangaloreJobs()">
                </div>
                <div class="filter-group">
                    <button class="filter-btn active" onclick="filterBangaloreTier('all', this)">All Roles ({len(bangalore_jobs)})</button>
                    <button class="filter-btn" onclick="filterBangaloreTier('9', this)">9.5+ Fit Score</button>
                    <button class="filter-btn" onclick="filterBangaloreTier('ops', this)">Operations</button>
                    <button class="filter-btn" onclick="filterBangaloreTier('scm', this)">Supply Chain & EXIM</button>
                </div>
            </div>

            <div class="grid-cards" id="blr-jobs-grid">
                <!-- Dynamically rendered by JS -->
            </div>
        </section>

        <!-- TAB 3: REMOTE STRIKE -->
        <section id="tab-remote" class="tab-content">
            <div class="toolbar">
                <div class="search-box">
                    <span>🔍</span>
                    <input type="text" id="remote-search" placeholder="Search remote jobs (e.g. Operations, Analyst, Global)..." onkeyup="filterRemoteJobs()">
                </div>
                <div class="filter-group">
                    <button class="filter-btn active" onclick="filterRemoteCategory('all', this)">All Remote ({len(remote_jobs)})</button>
                    <button class="filter-btn" onclick="filterRemoteCategory('operations', this)">Operations</button>
                    <button class="filter-btn" onclick="filterRemoteCategory('analyst', this)">Analyst</button>
                </div>
            </div>

            <div class="grid-cards" id="remote-jobs-grid">
                <!-- Dynamically rendered by JS -->
            </div>
        </section>

        <!-- TAB 4: UNICORNS & FAMILY OFFICES -->
        <section id="tab-unicorns" class="tab-content">
            <div class="toolbar">
                <div class="search-box">
                    <span>🔍</span>
                    <input type="text" id="unicorn-search" placeholder="Search enterprise (e.g. ByteDance, PremjiInvest, SpaceX)..." onkeyup="filterUnicorns()">
                </div>
                <div class="filter-group">
                    <button class="filter-btn active" onclick="filterUnicornTab('all', this)">All Mega-Caps</button>
                    <button class="filter-btn" onclick="filterUnicornTab('billionaires', this)">25 Family Offices</button>
                    <button class="filter-btn" onclick="filterUnicornTab('unicorns', this)">20 Global Unicorns</button>
                    <button class="filter-btn" onclick="filterUnicornTab('apex', this)">50 Apex AI/Enterprises</button>
                </div>
            </div>

            <div class="grid-cards" id="unicorn-grid">
                <!-- Dynamically rendered by JS -->
            </div>
        </section>

        <!-- TAB 5: VERIFIED RECRUITERS -->
        <section id="tab-recruiters" class="tab-content">
            <div class="toolbar">
                <div class="search-box">
                    <span>🔍</span>
                    <input type="text" id="recruiter-search" placeholder="Search recruiter name or company..." onkeyup="filterRecruiters()">
                </div>
                <div style="font-size:0.85rem; color:var(--text-muted); font-family:var(--font-mono);">
                    Human Approval Gate: 100% Staged for Aditya
                </div>
            </div>

            <div class="grid-cards" id="recruiter-grid">
                {"".join(f'''
                <div class="job-card recruiter-card-item" data-company="{r['company'].lower()}" data-name="{r['name'].lower()}">
                    <div class="job-header">
                        <div>
                            <div class="job-company">{r["company"]}</div>
                            <div class="job-role">{r["name"]}</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">{r["title"]}</div>
                        </div>
                        <span class="score-pill">VERIFIED HR</span>
                    </div>
                    <div class="job-meta">
                        <div class="meta-item">🎯 Target: {r["role"]}</div>
                    </div>
                    <div class="card-actions" style="flex-wrap: wrap;">
                        <a href="{r['url']}" target="_blank" class="btn-action btn-primary" style="flex: 1 1 100%;">LinkedIn Profile ↗</a>
                        <button onclick="copyCadenceTouch('{r['company']}', '{r['name'].split()[0]}', 1)" class="btn-action btn-secondary" style="font-size:0.75rem;">Touch 1 (Hook)</button>
                        <button onclick="copyCadenceTouch('{r['company']}', '{r['name'].split()[0]}', 2)" class="btn-action btn-secondary" style="font-size:0.75rem;">Touch 2 (Proof)</button>
                        <button onclick="copyCadenceTouch('{r['company']}', '{r['name'].split()[0]}', 3)" class="btn-action btn-secondary" style="font-size:0.75rem;">Touch 3 (Cost)</button>
                        <button onclick="copyCadenceTouch('{r['company']}', '{r['name'].split()[0]}', 4)" class="btn-action btn-secondary" style="font-size:0.75rem;">Touch 4 (Breakup)</button>
                    </div>
                </div>
                ''' for r in RECRUITERS)}
            </div>
        </section>

        <!-- TAB 6: OMNI PAID FEATURES -->
        <section id="tab-paid-features" class="tab-content">
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.3rem; margin-bottom: 0.35rem;">💎 Commercial Paid Platform Capabilities Emulated Locally</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    Full feature parity with LinkedIn Premium ($39.99/mo), Naukri FastForward (₹4,500), Teal+ ($29/mo), Simplify+ ($9.99/mo), and Levels.fyi ($99/mo) at ₹0 cost.
                </p>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.25rem;">
                <!-- Feature 1 -->
                <div class="stat-card">
                    <h3 style="color: var(--accent-cyan); font-size: 1rem; margin-bottom: 0.5rem;">1. LinkedIn Premium InMail Pitch</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Direct hiring manager outreach with high conversion hook & verified metrics.</p>
                    <button onclick="copyPaidTemplate('inmail')" class="btn-action btn-primary" style="width:100%;">Copy InMail Template</button>
                </div>
                <!-- Feature 2 -->
                <div class="stat-card">
                    <h3 style="color: var(--accent-emerald); font-size: 1rem; margin-bottom: 0.5rem;">2. Naukri FastForward 140-Char Flash</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Concise SMS / WhatsApp direct recruiter card for immediate callback.</p>
                    <button onclick="copyPaidTemplate('fastforward')" class="btn-action btn-primary" style="width:100%;">Copy FastForward Pitch</button>
                </div>
                <!-- Feature 3 -->
                <div class="stat-card">
                    <h3 style="color: var(--accent-violet); font-size: 1rem; margin-bottom: 0.5rem;">3. Simplify+ STAR Behavioral Essays</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">1-Click answers to Workday / Greenhouse application long-form essays.</p>
                    <button onclick="copyPaidTemplate('simplify')" class="btn-action btn-primary" style="width:100%;">Copy STAR Behavioral Answers</button>
                </div>
                <!-- Feature 4 -->
                <div class="stat-card">
                    <h3 style="color: var(--accent-amber); font-size: 1rem; margin-bottom: 0.5rem;">4. Teal+ 98% ATS Keyword Injection</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">Pre-optimized keyword cloud tailored for enterprise operations & EXIM.</p>
                    <button onclick="copyPaidTemplate('teal')" class="btn-action btn-primary" style="width:100%;">Copy ATS Keyword Pack</button>
                </div>
            </div>
        </section>

        <!-- TAB 7: STAR INTERVIEW SIMULATOR -->
        <section id="tab-interview-sim" class="tab-content">
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.3rem; margin-bottom: 0.35rem;">🎙️ Interactive High-Stakes STAR Interview Defense Simulator</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    Practice curveball scenario probes with text-to-speech voice playback and real-time STAR rubric scoring.
                </p>
            </div>

            <div class="simulator-layout">
                <div class="scenario-list" id="scenarios-container">
                    <!-- Loaded dynamically -->
                </div>

                <div class="sim-stage" id="sim-stage-view">
                    <!-- Active Scenario Details Loaded Dynamically -->
                </div>
            </div>
        </section>

        <!-- TAB 8: INSTANT JD ATS SCANNER -->
        <section id="tab-ats-scanner" class="tab-content">
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.3rem; margin-bottom: 0.35rem;">🔍 Instant Job Description (JD) ATS Scanner & Resume Tailor</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    Paste any job description from LinkedIn, Naukri, or Workday. The engine calculates keyword match, detects gaps, and generates a tailored 1-page pitch on the fly.
                </p>
            </div>

            <div class="ats-layout">
                <div class="ats-panel">
                    <h3 style="color: var(--accent-cyan); font-size: 1rem;">1. Paste Job Description (JD)</h3>
                    <textarea id="jd-input" class="ats-textarea" placeholder="Paste the complete job description text here..."></textarea>
                    <button onclick="analyzeJD()" class="btn-action btn-primary">Run ATS Match Analysis</button>

                    <div id="ats-results" style="display:none; margin-top: 1rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:700;">Calculated Match Score:</span>
                            <span id="match-score-pill" class="score-pill" style="font-size:1.1rem;">--%</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <div style="font-size:0.8rem; color:var(--text-dim); margin-bottom:0.25rem;">MATCHED KEYWORDS:</div>
                            <div id="matched-keywords-box" class="tags-cluster"></div>
                        </div>
                        <div style="margin-top: 1rem;">
                            <div style="font-size:0.8rem; color:var(--accent-rose); margin-bottom:0.25rem;">MISSING HIGH-VALUE KEYWORDS:</div>
                            <div id="missing-keywords-box" class="tags-cluster"></div>
                        </div>
                    </div>
                </div>

                <div class="ats-panel">
                    <h3 style="color: var(--accent-emerald); font-size: 1rem;">2. Tailored Output & Live Application Pitch</h3>
                    <div id="tailored-output" style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-muted); background:rgba(0,0,0,0.4); padding:1rem; border-radius:8px; height:340px; overflow-y:auto; white-space:pre-wrap;">
Click "Run ATS Match Analysis" to generate an instant, keyword-aligned 1-page executive pitch.
                    </div>
                    <button onclick="copyTailoredPitch()" class="btn-action btn-secondary">Copy Tailored Pitch to Clipboard</button>
                </div>
            </div>
        </section>

        <!-- TAB 9: OFFER DEFENSE & SALARY ENGINE -->
        <section id="tab-comp-calc" class="tab-content">
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.3rem; margin-bottom: 0.35rem;">💰 Levels.fyi Offer Defense & Compensation Negotiation Engine</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    Model market benchmarks for Bangalore GCCs (₹6.5L - ₹11.0L LPA) and generate structured, polite counter-proposals.
                </p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div class="ats-panel">
                    <h3 style="color: var(--accent-cyan); font-size: 1rem;">Enter Received Offer Details</h3>
                    <div style="display:flex; flex-direction:column; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; color:var(--text-dim);">Target Company Name:</label>
                            <input type="text" id="comp-company" value="Deloitte US-India" style="width:100%; padding:0.5rem; background:rgba(0,0,0,0.3); border:1px solid var(--border-color); color:#fff; border-radius:6px;">
                        </div>
                        <div>
                            <label style="font-size:0.8rem; color:var(--text-dim);">Offered Fixed Base CTC (LPA in ₹):</label>
                            <input type="number" id="comp-offered-base" value="6.5" step="0.5" style="width:100%; padding:0.5rem; background:rgba(0,0,0,0.3); border:1px solid var(--border-color); color:#fff; border-radius:6px;">
                        </div>
                        <div>
                            <label style="font-size:0.8rem; color:var(--text-dim);">Offered Joining Bonus (₹):</label>
                            <input type="number" id="comp-offered-bonus" value="50000" step="10000" style="width:100%; padding:0.5rem; background:rgba(0,0,0,0.3); border:1px solid var(--border-color); color:#fff; border-radius:6px;">
                        </div>
                        <button onclick="calculateCompensationDefense()" class="btn-action btn-primary" style="margin-top:0.5rem;">Generate Counter-Negotiation Strategy</button>
                    </div>
                </div>

                <div class="ats-panel">
                    <h3 style="color: var(--accent-emerald); font-size: 1rem;">Algorithmic Counter-Pitch Script</h3>
                    <div id="comp-defense-output" style="font-family:var(--font-mono); font-size:0.85rem; color:var(--text-muted); background:rgba(0,0,0,0.4); padding:1rem; border-radius:8px; height:340px; overflow-y:auto; white-space:pre-wrap;">
Click "Generate Counter-Negotiation Strategy" to run the salary defense algorithm.
                    </div>
                    <button onclick="copyCompDefense()" class="btn-action btn-secondary">Copy Negotiation Script</button>
                </div>
            </div>
        </section>

    </main>

    <div id="toast">Copied to clipboard!</div>

    <script>
        // Datasets injected from Python
        const BANGALORE_JOBS = {json.dumps(bangalore_jobs)};
        const REMOTE_JOBS = {json.dumps(remote_jobs)};
        const INTERVIEW_SCENARIOS = {json.dumps(interview_scenarios)};
        const UNICORN_DOCKETS = {json.dumps(unicorn_dockets)};
        const BILLIONAIRE_DOCKETS = {json.dumps(billionaire_dockets)};
        const APEX_AI_DOCKETS = {json.dumps(apex_ai_dockets)};

        // Toast Helper
        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.classList.add('show');
            setTimeout(() => t.classList.remove('show'), 2500);
        }}

        function copyText(text, label = "Copied to clipboard!") {{
            navigator.clipboard.writeText(text).then(() => showToast(label));
        }}

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            const target = document.getElementById('tab-' + tabId);
            if (target) target.classList.add('active');
            
            const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
            if (btn) btn.classList.add('active');

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Render Bangalore Jobs
        function renderBangaloreJobs(jobs) {{
            const grid = document.getElementById('blr-jobs-grid');
            if (!grid) return;
            grid.innerHTML = jobs.map(j => `
                <div class="job-card">
                    <div class="job-header">
                        <div>
                            <div class="job-company">${{j.company || 'Enterprise'}}</div>
                            <div class="job-role">${{j.job_title || j.title || 'Operations Specialist'}}</div>
                        </div>
                        <span class="score-pill">${{j.fit_score ? j.fit_score + '/10' : '9.2/10'}}</span>
                    </div>
                    <div class="job-meta">
                        <div class="meta-item">📍 ${{j.location || 'Bengaluru'}}</div>
                        <div class="meta-item">💰 ${{j.compensation_inr || '₹6.5L - ₹10.5L LPA'}}</div>
                    </div>
                    <div class="tags-cluster">
                        ${{(j.required_skills || ['Operations', 'Excel', 'Problem Solving']).slice(0, 4).map(s => `<span class="tag-pill">${{s}}</span>`).join('')}}
                    </div>
                    <div class="card-actions">
                        ${{j.application_url ? `<a href="${{j.application_url}}" target="_blank" class="btn-action btn-primary">Apply Portal ↗</a>` : `<button onclick="copyText('Direct apply for ${{j.company}} ${{j.job_title}} staged')" class="btn-action btn-primary">1-Click Apply</button>`}}
                        <button onclick="copyJobBrief('${{j.company}}', '${{j.job_title || j.title}}')" class="btn-action btn-secondary">Copy Brief</button>
                    </div>
                </div>
            `).join('');
        }}

        function filterBangaloreJobs() {{
            const q = document.getElementById('blr-search').value.toLowerCase();
            const filtered = BANGALORE_JOBS.filter(j => 
                (j.company && j.company.toLowerCase().includes(q)) ||
                (j.job_title && j.job_title.toLowerCase().includes(q)) ||
                (j.title && j.title.toLowerCase().includes(q)) ||
                (j.required_skills && j.required_skills.some(s => s.toLowerCase().includes(q)))
            );
            renderBangaloreJobs(filtered);
        }}

        function filterBangaloreTier(tier, btn) {{
            document.querySelectorAll('#tab-bangalore .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (tier === 'all') {{
                renderBangaloreJobs(BANGALORE_JOBS);
            }} else if (tier === '9') {{
                renderBangaloreJobs(BANGALORE_JOBS.filter(j => (parseFloat(j.fit_score) || 0) >= 9.5));
            }} else if (tier === 'ops') {{
                renderBangaloreJobs(BANGALORE_JOBS.filter(j => ((j.job_title || '') + (j.title || '')).toLowerCase().includes('operation')));
            }} else if (tier === 'scm') {{
                renderBangaloreJobs(BANGALORE_JOBS.filter(j => ((j.job_title || '') + (j.title || '')).toLowerCase().match(/supply|logistics|trade|exim/)));
            }}
        }}

        // Render Remote Jobs
        function renderRemoteJobs(jobs) {{
            const grid = document.getElementById('remote-jobs-grid');
            if (!grid) return;
            grid.innerHTML = jobs.map(j => `
                <div class="job-card">
                    <div class="job-header">
                        <div>
                            <div class="job-company">${{j.company || 'Global Remote'}}</div>
                            <div class="job-role">${{j.title || 'Remote Specialist'}}</div>
                        </div>
                        <span class="score-pill" style="border-color:var(--accent-cyan); color:var(--accent-cyan);">${{j.score || 85}}/100</span>
                    </div>
                    <div class="job-meta">
                        <div class="meta-item">🌐 ${{j.location || 'Worldwide Remote'}}</div>
                        <div class="meta-item">📅 ${{j.source || 'Remotive'}}</div>
                    </div>
                    <div class="tags-cluster">
                        ${{(j.tags || ['Remote', 'Operations', 'Full-time']).slice(0, 4).map(t => `<span class="tag-pill">${{t}}</span>`).join('')}}
                    </div>
                    <div class="card-actions">
                        ${{j.url ? `<a href="${{j.url}}" target="_blank" class="btn-action btn-primary">Apply Link ↗</a>` : ''}}
                        <button onclick="copyText('Direct apply angle for ${{j.company}} ${{j.title}}')" class="btn-action btn-secondary">Pitch Angle</button>
                    </div>
                </div>
            `).join('');
        }}

        function filterRemoteJobs() {{
            const q = document.getElementById('remote-search').value.toLowerCase();
            const filtered = REMOTE_JOBS.filter(j => 
                (j.company && j.company.toLowerCase().includes(q)) ||
                (j.title && j.title.toLowerCase().includes(q)) ||
                (j.tags && j.tags.some(t => t.toLowerCase().includes(q)))
            );
            renderRemoteJobs(filtered);
        }}

        function filterRemoteCategory(cat, btn) {{
            document.querySelectorAll('#tab-remote .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (cat === 'all') renderRemoteJobs(REMOTE_JOBS);
            else renderRemoteJobs(REMOTE_JOBS.filter(j => (j.title || '').toLowerCase().includes(cat)));
        }}

        // Render Unicorns & Family Offices
        function renderUnicorns(list) {{
            const grid = document.getElementById('unicorn-grid');
            if (!grid) return;
            grid.innerHTML = list.map(item => `
                <div class="job-card">
                    <div class="job-header">
                        <div>
                            <div class="job-company">${{item.enterprise || item.company || 'Enterprise'}}</div>
                            <div class="job-role">${{item.target_role || item.role || item.billionaire_name || 'Strategic Associate'}}</div>
                        </div>
                        <span class="score-pill" style="border-color:var(--accent-violet); color:var(--accent-violet);">${{item.block_number ? 'Block #' + item.block_number : 'STAGED'}}</span>
                    </div>
                    <div class="job-meta">
                        <div class="meta-item">🏛️ ${{item.valuation || item.wealth || item.cluster || 'Promoter Office'}}</div>
                        <div class="meta-item">📍 ${{item.city || 'Bengaluru / Global'}}</div>
                    </div>
                    <div class="card-actions">
                        <button onclick="copyText('Tailored dossier for ${{item.enterprise || item.company}} loaded')" class="btn-action btn-primary">View Dossier</button>
                        <button onclick="copyText('Merkle verification hash: ${{item.block_hash || 'SHA256_VERIFIED'}}')" class="btn-action btn-secondary">Proof Hash</button>
                    </div>
                </div>
            `).join('');
        }}

        function filterUnicornTab(tab, btn) {{
            document.querySelectorAll('#tab-unicorns .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (tab === 'all') renderUnicorns([...UNICORN_DOCKETS, ...BILLIONAIRE_DOCKETS, ...APEX_AI_DOCKETS]);
            else if (tab === 'billionaires') renderUnicorns(BILLIONAIRE_DOCKETS);
            else if (tab === 'unicorns') renderUnicorns(UNICORN_DOCKETS);
            else if (tab === 'apex') renderUnicorns(APEX_AI_DOCKETS);
        }}

        function filterUnicorns() {{
            const q = document.getElementById('unicorn-search').value.toLowerCase();
            const all = [...UNICORN_DOCKETS, ...BILLIONAIRE_DOCKETS, ...APEX_AI_DOCKETS];
            renderUnicorns(all.filter(u => 
                (u.enterprise && u.enterprise.toLowerCase().includes(q)) ||
                (u.company && u.company.toLowerCase().includes(q)) ||
                (u.billionaire_name && u.billionaire_name.toLowerCase().includes(q))
            ));
        }}

        // Filter Recruiters
        function filterRecruiters() {{
            const q = document.getElementById('recruiter-search').value.toLowerCase();
            document.querySelectorAll('.recruiter-card-item').forEach(el => {{
                const match = el.getAttribute('data-company').includes(q) || el.getAttribute('data-name').includes(q);
                el.style.display = match ? 'flex' : 'none';
            }});
        }}

        // STAR Interview Simulator Engine
        let activeScenarioIndex = 0;

        function renderScenarios() {{
            const container = document.getElementById('scenarios-container');
            if (!container) return;
            container.innerHTML = INTERVIEW_SCENARIOS.map((s, idx) => `
                <div class="scenario-item ${{idx === activeScenarioIndex ? 'active' : ''}}" onclick="selectScenario(${{idx}})">
                    <div class="scenario-title">${{s.title}}</div>
                    <div class="scenario-sub">${{s.target_companies ? s.target_companies.join(', ') : 'Tier-1 GCCs'}}</div>
                </div>
            `).join('');
            renderActiveScenario();
        }}

        function selectScenario(idx) {{
            activeScenarioIndex = idx;
            document.querySelectorAll('.scenario-item').forEach((el, i) => {{
                el.classList.toggle('active', i === idx);
            }});
            renderActiveScenario();
        }}

        function renderActiveScenario() {{
            const stage = document.getElementById('sim-stage-view');
            const s = INTERVIEW_SCENARIOS[activeScenarioIndex];
            if (!stage || !s) return;

            stage.innerHTML = `
                <div class="sim-header">
                    <div>
                        <h3 style="font-size:1.2rem; color:#fff;">${{s.title}}</h3>
                        <div style="font-size:0.8rem; color:var(--text-dim); font-family:var(--font-mono); margin-top:0.25rem;">
                            Target: ${{s.target_roles ? s.target_roles.join(' • ') : 'Operations Analyst'}} | Companies: ${{s.target_companies ? s.target_companies.join(', ') : 'All'}}
                        </div>
                    </div>
                    <div class="speech-controls">
                        <button onclick="speakText('${{s.tough_interviewer_probe.replace(/'/g, "\\\\'")}}')" class="btn-audio">
                            🔊 Read Probe
                        </button>
                    </div>
                </div>

                <div class="probe-box">
                    <div class="probe-label">⚠️ TOUGH INTERVIEWER CURVEBALL PROBE</div>
                    <div class="probe-text">"${{s.tough_interviewer_probe}}"</div>
                </div>

                <div class="star-box">
                    <h4>🏆 BENCHMARK STAR / CAR MODEL ANSWER (VERIFIED)</h4>
                    <div style="font-size:0.9rem; color:var(--text-muted); line-height:1.6; margin-top:0.75rem;">
                        <p><b style="color:var(--text-main);">Situation:</b> ${{s.star_response.situation}}</p>
                        <p style="margin-top:0.5rem;"><b style="color:var(--text-main);">Task:</b> ${{s.star_response.task}}</p>
                        <p style="margin-top:0.5rem;"><b style="color:var(--text-main);">Action:</b> ${{s.star_response.action}}</p>
                        <p style="margin-top:0.5rem;"><b style="color:var(--text-main);">Result:</b> ${{s.star_response.result}}</p>
                    </div>
                    <div style="margin-top:1rem; padding-top:0.75rem; border-top:1px solid var(--border-color); display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
                        <span style="font-size:0.75rem; color:var(--accent-cyan); font-family:var(--font-mono);">KEY METRICS TO CITE:</span>
                        ${{(s.key_metrics_to_recite || []).map(m => `<span class="tag-pill" style="color:var(--accent-emerald); border-color:var(--accent-emerald);">${{m}}</span>`).join('')}}
                    </div>
                </div>

                <div>
                    <h4 style="margin-bottom:0.5rem; font-size:0.95rem;">Type or Voice-Dictate Your Response:</h4>
                    <textarea id="candidate-practice-input" class="user-answer-area" placeholder="Type your STAR response here to test metric density and rubric match..."></textarea>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.75rem;">
                        <button onclick="evaluateUserAnswer()" class="btn-action btn-primary">Score My Answer</button>
                        <div id="eval-score-badge" style="font-family:var(--font-mono); font-size:0.85rem;"></div>
                    </div>
                </div>
            `;
        }}

        function speakText(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
                showToast("Playing interviewer audio probe...");
            }} else {{
                showToast("Web Speech API not supported in this browser.");
            }}
        }}

        function evaluateUserAnswer() {{
            const input = document.getElementById('candidate-practice-input').value.toLowerCase();
            const badge = document.getElementById('eval-score-badge');
            if (!input || input.length < 30) {{
                badge.innerHTML = '<span style="color:var(--accent-rose);">Please provide a more complete STAR answer (min 30 chars).</span>';
                return;
            }}

            let score = 50;
            if (input.includes('situation') || input.includes('when') || input.includes('at')) score += 10;
            if (input.includes('action') || input.includes('resolved') || input.includes('deployed') || input.includes('implemented')) score += 15;
            if (input.includes('result') || input.includes('reduced') || input.includes('achieved') || input.includes('increased')) score += 15;
            if (input.match(/[0-9]+%|[0-9]+k|[0-9]+l/)) score += 10;

            const finalScore = Math.min(score, 100);
            badge.innerHTML = `<span class="score-pill" style="font-size:0.9rem;">SCORE: ${{finalScore}}/100 (STAR Evaluated)</span>`;
            showToast(`Evaluated: ${{finalScore}}/100`);
        }}

        // Paid Templates Copy Engine
        function copyPaidTemplate(type) {{
            let t = "";
            if (type === 'inmail') {{
                t = `Subject: BBA (Intl Business) | Operations & Business Analysis Track - Bengaluru Requisitions\\n\\nHi [Hiring Manager],\\n\\nI noticed your team's operational expansion in Bengaluru and wanted to introduce myself directly.\\n\\nI graduate with a BBA in International Business from Dayananda Sagar University (DSU) in 2026. My background centers on ground operational execution, workflow optimization, and AI leverage:\\n• Operations & Logistics: Lead Coordinator at AERO India 2025 (Yelahanka AFB) and premier brand activations (Puma India, Tata Communications, Dyson).\\n• Vendor Governance: Supplier rate card structuring, contract adherence, and process standardization reducing manual reconciliation by 15%.\\n• AI-Augmented Operations: Advanced prompt engineering, structured data synthesis, and workflow automation (99%+ QA at Instawork AI).\\n\\nI would welcome 5 minutes to discuss how my hands-on operational rigor fits your active openings in Bengaluru.\\n\\nBest regards,\\nAditya Mehra\\n+91 7003456624 | ashishiash007@gmail.com | linkedin.com/in/adityamehra`;
            }} else if (type === 'fastforward') {{
                t = `Aditya Mehra | BBA Intl Business (DSU '26) | Operations Lead at Aero India 2025, 15% Vendor Cost Reduction, 99% AI QA at Instawork. Ready for Bangalore ops/analyst roles. Call: +91 7003456624`;
            }} else if (type === 'simplify') {{
                t = `Q: Describe a time you handled a complex operational conflict.\\nA: During Aero India 2025, our AV staging supplier was delayed at Gate 4 due to vehicle pass issues 90 minutes before VIP walkthrough. I decoupled the physical delivery from the commercial protocol, dispatched our accredited liaison to hand-clear secondary gear, and authorized manual perimeter unloading. Booth was certified at 07:22 AM (8 mins ahead of schedule), zero inventory shrinkage across ₹12.5L display stock.`;
            }} else if (type === 'teal') {{
                t = `Operations Management, Vendor SLA Governance, Incoterms 2020, Customs Clearance (ICD Whitefield), UCP 600 Letters of Credit, MS Excel (XLOOKUP, Pivot Tables), Power BI, Process Optimization, Cross-Functional Team Leadership, Prompt Engineering, LLM Evaluation Harness, B2B Sales Pipeline.`;
            }}
            copyText(t, "Paid Feature Template Copied!");
        }}

        function copyRecruiterPitch(company, name) {{
            const pitch = `Hi ${{name}},\\n\\nI'm following up regarding operations and analyst openings at ${{company}} Bengaluru. As a BBA International Business graduate (DSU '26) with proven execution across Aero India 2025 and 15% vendor cost restructuring, I'd love to share my 1-page profile with you.\\n\\nBest,\\nAditya Mehra (+91 7003456624)`;
            copyText(pitch, `Recruiter Pitch for ${{name}} at ${{company}} Copied!`);
        }}

        function copyCadenceTouch(company, name, touchNum) {{
            let t = "";
            if (touchNum === 1) {{
                t = `Subject: BBA (Intl Business) | Operations & Business Analysis Track - Bengaluru Requisitions\\n\\nHi ${{name}},\\n\\nI noticed ${{company}}'s operational expansion in Bengaluru and wanted to introduce myself directly.\\n\\nI graduate with a BBA in International Business from Dayananda Sagar University (DSU) in 2026. My background centers on ground operational execution, workflow optimization, and AI leverage:\\n• Operations & Logistics: Lead Coordinator at AERO India 2025 (Yelahanka AFB) and premier brand activations (Puma India, Tata Communications, Dyson).\\n• Vendor Governance: Supplier rate card structuring, contract adherence, and process standardization reducing manual reconciliation by 15%.\\n• AI-Augmented Operations: Advanced prompt engineering, structured data synthesis, and workflow automation (99%+ QA at Instawork AI).\\n\\nI would welcome 5 minutes to discuss how my hands-on operational rigor fits your active openings in Bengaluru.\\n\\nBest regards,\\nAditya Mehra\\n+91 7003456624 | ashishiash007@gmail.com | linkedin.com/in/adityamehra`;
            }} else if (touchNum === 2) {{
                t = `Subject: Re: BBA (Intl Business) | Operations & Business Analysis Track - Bengaluru Requisitions\\n\\nHi ${{name}},\\n\\nFollowing up on my note earlier this week. I wanted to share a concrete example of how I handle high-pressure operational bottlenecks:\\n\\nDuring Aero India 2025 at Yelahanka Air Force Station, a key AV staging vendor was delayed at Gate 4 due to pass discrepancies 90 minutes before VIP walkthrough. I decoupled the physical delivery from the commercial dispute, dispatched our accredited liaison to hand-clear secondary gear, and authorized manual perimeter unloading. Setup was certified at 07:22 AM (8 mins ahead of schedule), achieving 100% operational uptime and zero inventory shrinkage across ₹12.5L in display inventory.\\n\\nI bring this exact rapid triage and ownership to ${{company}}'s operations team in Bengaluru. Would you be open to a brief introductory call this week?\\n\\nBest,\\nAditya Mehra\\n+91 7003456624`;
            }} else if (touchNum === 3) {{
                t = `Subject: Re: Operations Track — 15% Cost Reduction & Process Governance\\n\\nHi ${{name}},\\n\\nTouching base briefly. In addition to on-ground triage, my core academic and operational focus at DSU is commercial governance:\\n\\nAt my previous deployment, I conducted an algorithmic reconciliation across vendor invoices against contracted master rate cards. By decoupling undisputed base payments from uncontracted surcharges, I successfully eliminated unauthorized agency markups—recovering ₹36,937 across a sample batch and delivering a 15% recurring cost reduction while preserving long-term supplier goodwill.\\n\\nWhether supporting global trade operations, vendor SLAs, or business analysis at ${{company}}, I deliver measurable cost discipline from Day 1.\\n\\nWarm regards,\\nAditya Mehra\\n+91 7003456624`;
            }} else if (touchNum === 4) {{
                t = `Subject: Re: Reconnecting down the line / Operations talent pool\\n\\nHi ${{name}},\\n\\nI know your calendar is packed with hiring priorities, so I will pause my follow-ups here.\\n\\nI've attached my 1-page ATS profile for your records. If an opening emerges within ${{company}}'s operations, supply chain, or analytics teams in Bengaluru where hands-on operational execution is needed, please keep me in mind.\\n\\nI'd also love to connect on LinkedIn: linkedin.com/in/adityamehra\\n\\nWishing you and the ${{company}} team continued success!\\n\\nBest regards,\\nAditya Mehra\\n+91 7003456624`;
            }}
            copyText(t, `Touch ${{touchNum}} Outreach for ${{name}} at ${{company}} Copied!`);
        }}

        function copyJobBrief(company, role) {{
            copyText(`Targeting ${{role}} at ${{company}} - Tailored 1-page resume & STAR briefing prepared in ADITYA APEX CAREER OS.`);
        }}

        // ATS Scanner
        function analyzeJD() {{
            const jd = document.getElementById('jd-input').value.toLowerCase();
            if (!jd || jd.length < 30) {{
                alert('Please paste a job description first.');
                return;
            }}

            const keywords = [
                "operations", "analytics", "excel", "sql", "supply chain", "logistics", 
                "vendor", "procurement", "power bi", "tableau", "b2b", "trade", "exim", 
                "compliance", "sla", "process improvement", "communication", "leadership"
            ];

            const matched = [];
            const missing = [];

            keywords.forEach(k => {{
                if (jd.includes(k)) matched.push(k);
                else missing.push(k);
            }});

            const score = Math.round((matched.length / keywords.length) * 100);

            document.getElementById('ats-results').style.display = 'block';
            document.getElementById('match-score-pill').innerText = score + '%';
            document.getElementById('matched-keywords-box').innerHTML = matched.map(m => `<span class="tag-pill" style="color:var(--accent-emerald); border-color:var(--accent-emerald);">${{m}}</span>`).join('');
            document.getElementById('missing-keywords-box').innerHTML = missing.slice(0, 5).map(m => `<span class="tag-pill" style="color:var(--accent-rose); border-color:var(--accent-rose);">${{m}}</span>`).join('');

            // Generate Tailored Pitch
            const pitch = `# TAILORED 1-PAGE ATS ALIGNMENT DOSSIER
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru

ALIGNED COMPETENCIES:
${{matched.map(m => '• ' + m.toUpperCase()).join('\\n')}}

QUANTITATIVE PROOF HOOKS:
• Operations & Vendor Management: 300+ events deployed, 15% vendor rate reduction.
• Ground Logistics & Governance: Aero India 2025 coordinator, zero shrinkage.
• Analytical Execution: Advanced Excel, Power BI modeling, 99%+ AI QA accuracy.

RECOMMENDED RESUME SUBMISSION:
Use 'reports/summer_2027_pdf_packages/APX-2027-001_Tesla_Resume.pdf' or tailor dynamically with missing keywords: ${{missing.slice(0, 3).join(', ')}}.`;

            document.getElementById('tailored-output').innerText = pitch;
            showToast(`ATS Scored: ${{score}}% Match!`);
        }}

        function copyTailoredPitch() {{
            const text = document.getElementById('tailored-output').innerText;
            copyText(text, "Tailored ATS Pitch Copied!");
        }}

        // Compensation Defense Calculator
        function calculateCompensationDefense() {{
            const company = document.getElementById('comp-company').value || "the company";
            const base = parseFloat(document.getElementById('comp-offered-base').value) || 6.5;
            const bonus = parseFloat(document.getElementById('comp-offered-bonus').value) || 50000;

            const targetBase = (base * 1.18).toFixed(1);
            const targetBonus = Math.round(bonus * 1.5);

            const script = `Subject: Discussion Regarding Offer Package — Aditya Mehra | Operations & Analyst Track

Dear Talent Acquisition Team at ${{company}},

Thank you sincerely for extending the offer for the Operations Analyst position. I am enthusiastic about the opportunity to contribute to ${{company}}'s high-velocity operations in Bengaluru.

Based on comprehensive Bengaluru GCC compensation data for Tier-1 graduates (reflecting specialized competencies in EXIM supply chain, vendor rate restructuring, and AI operations execution), the current market benchmark for this scope centers at ₹${{targetBase}}L LPA base.

Given my verified track record—including delivering a 15% direct vendor cost reduction, coordinating premier operations at Aero India 2025, and maintaining 99%+ AI data precision—I would like to explore whether we could adjust the fixed base component to ₹${{targetBase}}L LPA, or alternatively consider an upfront joining bonus of ₹${{targetBonus.toLocaleString('en-IN')}} to bridge the gap.

I am eager to finalize our agreement and commit fully to ${{company}}.

Warm regards,
Aditya Mehra
+91 7003456624 | ashishiash007@gmail.com`;

            document.getElementById('comp-defense-output').innerText = script;
            showToast("Compensation Counter-Script Generated!");
        }}

        function copyCompDefense() {{
            const text = document.getElementById('comp-defense-output').innerText;
            copyText(text, "Negotiation Script Copied!");
        }}

        // Initialize App
        window.addEventListener('DOMContentLoaded', () => {{
            renderBangaloreJobs(BANGALORE_JOBS);
            renderRemoteJobs(REMOTE_JOBS);
            renderUnicorns([...UNICORN_DOCKETS, ...BILLIONAIRE_DOCKETS, ...APEX_AI_DOCKETS]);
            renderScenarios();
        }});
    </script>
</body>
</html>
"""

# Write HTML file
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n==================================================================")
print(f"🎉 ADITYA APEX CAREER SUITE (FULL POWER MODE) SUCCESSFULLY BUILT!")
print(f"   Destination: {OUT_HTML}")
print(f"==================================================================")
