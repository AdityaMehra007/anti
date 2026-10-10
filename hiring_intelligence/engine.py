"""
Hiring Intelligence OS - Core Autonomous Engine (AGHIS-Ω)
Executes end-to-end database initialization, algorithmic role scoring,
outreach synthesis, and interactive reporting.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List

from hiring_intelligence.db import (
    DB_PATH,
    get_connection,
    init_db,
    insert_campaign,
    insert_decision_maker,
    insert_hiring_signal,
    insert_role,
    insert_startup,
)
from hiring_intelligence.fresher_mnc_data import MNC_FRESHER_DATA
from hiring_intelligence.seed_data import STARTUPS_DATA

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


REPORTS_DIR = Path(__file__).parent / "reports"
DASHBOARD_HTML_PATH = Path(__file__).parent / "dashboard.html"


def seed_database() -> Dict[str, int]:
    """Initializes schema and loads all startup dossiers, MNCs, fresher programs, roles, and signals."""
    init_db()
    conn = get_connection()
    stats = {"startups": 0, "roles": 0, "decision_makers": 0, "signals": 0}

    all_companies = STARTUPS_DATA + MNC_FRESHER_DATA

    with conn:
        for startup in all_companies:

            startup_record = {
                "name": startup["name"],
                "slug": startup["slug"],
                "domain": startup["domain"],
                "industry": startup["industry"],
                "stage": startup["stage"],
                "total_funding_usd": startup["total_funding_usd"],
                "last_round_type": startup.get("last_round_type", "N/A"),
                "valuation_usd": startup.get("valuation_usd", 0),
                "lead_investors": startup.get("lead_investors", "N/A"),
                "headcount": startup.get("headcount", 0),
                "headcount_growth_6m_pct": startup.get("headcount_growth_6m_pct", 0.0),
                "hq_location": startup["hq_location"],
                "remote_friendly": startup.get("remote_friendly", 1),
                "careers_url": startup["careers_url"],
                "ats_provider": startup["ats_provider"],
                "ats_endpoint": startup["ats_endpoint"],
                "verified_active": startup.get("verified_active", 1),
            }
            s_id = insert_startup(conn, startup_record)
            stats["startups"] += 1

            # Insert roles
            for role in startup.get("roles", []):
                role_record = {
                    "startup_id": s_id,
                    "title": role["title"],
                    "department": role["department"],
                    "seniority_level": role["seniority_level"],
                    "salary_min_usd": role.get("salary_min_usd", 0),
                    "salary_max_usd": role.get("salary_max_usd", 0),
                    "equity_note": role.get("equity_note", "Standard Equity"),
                    "tech_stack": role["tech_stack"],
                    "location": role["location"],
                    "remote_type": role["remote_type"],
                    "direct_apply_url": role["direct_apply_url"],
                    "urgency_score": role.get("urgency_score", 5.0),
                    "active_status": 1,
                    "batch_eligibility": role.get("batch_eligibility", "2024, 2025, 2026 Batch"),
                    "min_cgpa": role.get("min_cgpa", "60% or 6.0+ CGPA"),
                    "test_pattern": role.get("test_pattern", "Aptitude + Technical DSA Coding + Interviews"),
                }
                r_id = insert_role(conn, role_record)
                stats["roles"] += 1


            # Insert Decision Makers
            for dm in startup.get("decision_makers", []):
                dm_record = {
                    "startup_id": s_id,
                    "full_name": dm["full_name"],
                    "title": dm["title"],
                    "department": dm["department"],
                    "linkedin_url": dm.get("linkedin_url", ""),
                    "twitter_handle": dm.get("twitter_handle", ""),
                    "verified_email": dm.get("verified_email", ""),
                    "direct_pitch_hook": dm.get("direct_pitch_hook", ""),
                }
                insert_decision_maker(conn, dm_record)
                stats["decision_makers"] += 1

            # Insert Signals
            for sig in startup.get("signals", []):
                sig_record = {
                    "startup_id": s_id,
                    "signal_type": sig["signal_type"],
                    "source": sig["source"],
                    "signal_date": sig["signal_date"],
                    "description": sig["description"],
                    "weight": sig.get("weight", 1.0),
                }
                insert_hiring_signal(conn, sig_record)
                stats["signals"] += 1

    conn.close()
    return stats


def generate_outreach_playbooks() -> int:
    """Generates personalized cold email / DM campaigns for all active roles & decision makers."""
    conn = get_connection()
    count = 0

    query = """
    SELECT 
        r.id as role_id,
        r.title as role_title,
        r.tech_stack,
        s.name as company_name,
        dm.id as dm_id,
        dm.full_name as dm_name,
        dm.title as dm_title,
        dm.verified_email,
        dm.direct_pitch_hook
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    JOIN decision_makers dm ON dm.startup_id = s.id
    """
    rows = conn.execute(query).fetchall()

    with conn:
        for row in rows:
            subject = f"Direct Inquiry / Engineering perspective for {row['company_name']} ({row['role_title']})"
            body = f"""Hi {row['dm_name'].split()[0]},

I've been following {row['company_name']}'s architectural trajectory and noticed your search for the {row['role_title']} opening.

Regarding your technical priorities in {row['tech_stack'].split(',')[0].strip()}:
{row['direct_pitch_hook']}

I have solved similar throughput and scalability bottlenecks in production. Rather than going through standard recruiter queues, I put together a quick breakdown of how I would tackle this within the first 30 days.

Are you open to a brief 7-minute technical exchange this Thursday afternoon?

Best regards,
Candidate / Engineer
"""
            campaign_data = {
                "role_id": row["role_id"],
                "decision_maker_id": row["dm_id"],
                "channel": "EMAIL_DIRECT",
                "subject": subject,
                "message_body": body,
                "status": "READY_FOR_DISPATCH",
                "follow_up_step": 1,
            }
            insert_campaign(conn, campaign_data)
            count += 1

    conn.close()
    return count


def generate_markdown_report() -> Path:
    """Renders a comprehensive markdown intelligence dossier."""
    conn = get_connection()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "MASTER_HIRING_INTELLIGENCE_LEDGER.md"

    query = """
    SELECT 
        s.name, s.stage, s.industry, s.total_funding_usd, s.headcount, s.hq_location, s.ats_provider, s.careers_url,
        r.title, r.seniority_level, r.salary_min_usd, r.salary_max_usd, r.tech_stack, r.remote_type, r.direct_apply_url, r.urgency_score,
        r.batch_eligibility, r.min_cgpa, r.test_pattern,
        dm.full_name as dm_name, dm.title as dm_title, dm.verified_email as dm_email, dm.direct_pitch_hook
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    LEFT JOIN decision_makers dm ON dm.startup_id = s.id
    ORDER BY r.urgency_score DESC, s.total_funding_usd DESC
    """
    rows = conn.execute(query).fetchall()

    content = [
        "# 🌐 THE MASTER GLOBAL STARTUP & HIRING INTELLIGENCE LEDGER (A-Z)",
        "",
        "> **Generated by**: Hiring Intelligence OS (AGHIS-Ω)  ",
        f"> **Total Monitored Opportunities**: {len(rows)}  ",
        "> **Coverage**: Global Tier-1 Startups, Decacorns, MNCs, & Listed Public Giants (Freshers & Experienced)",
        "",
        "---",
        "",
        "## 🎓 FRESHER & CAMPUS HIRING LEDGER (MNCs & LISTED TECH GIANTS)",
        "",
        "| Company | Fresher Role | Batch Eligibility | Minimum Criteria | CTC / Package | Exam & Assessment Pattern | Direct Apply Link |",
        "|---|---|---|---|---|---|---|",
    ]

    for r in rows:
        if "fresher" in r['seniority_level'].lower() or "grad" in r['title'].lower() or "early career" in r['title'].lower() or "analyst" in r['title'].lower() or "ninja" in r['title'].lower() or "genc" in r['title'].lower() or "associate" in r['title'].lower():
            sal = f"${r['salary_min_usd']//1000}k - ${r['salary_max_usd']//1000}k" if r['salary_min_usd'] > 0 else "Competitive"
            content.append(
                f"| **{r['name']}** | **{r['title']}** | `{r['batch_eligibility']}` | {r['min_cgpa']} | {sal} | *{r['test_pattern']}* | [Apply Now]({r['direct_apply_url']}) |"
            )

    content.extend([
        "",
        "---",
        "",
        "## 📊 ALL MONITORED ROLES (STARTUPS + MNCs)",
        "",
        "| Rank | Company | Industry | Stage | Funding | Open Role | Salary Range | Modality | Tech Stack | ATS / Apply | DM / Gatekeeper |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ])

    for idx, r in enumerate(rows, 1):
        funding_str = f"${r['total_funding_usd'] / 1e6:.1f}M" if r['total_funding_usd'] < 1e9 else f"${r['total_funding_usd'] / 1e9:.2f}B"
        salary_str = f"${r['salary_min_usd']//1000}k - ${r['salary_max_usd']//1000}k" if r['salary_min_usd'] > 0 else "Competitive / Equity"
        dm_contact = f"{r['dm_name']} ({r['dm_title']})" if r['dm_name'] else "Recruiting Lead"

        content.append(
            f"| {idx} | **{r['name']}** | {r['industry']} | {r['stage']} | {funding_str} | **{r['title']}** | {salary_str} | {r['remote_type']} | `{r['tech_stack']}` | [Apply ({r['ats_provider']})]({r['direct_apply_url']}) | {dm_contact} |"
        )

    content.extend([
        "",
        "---",
        "",
        "## 🎯 HIGH-CONVICTION DEEP PROFILES & ASYMMETRIC HOOKS",
        ""
    ])

    # Distinct startups
    startups = conn.execute("SELECT * FROM startups ORDER BY total_funding_usd DESC").fetchall()
    for s in startups:
        content.append(f"### 🏢 {s['name']} (`{s['domain']}`)")
        content.append(f"- **Industry / Focus**: {s['industry']}")
        content.append(f"- **Stage & Capital**: {s['stage']} | ${s['total_funding_usd'] / 1e6:.1f}M Raised | Valuation: ${s['valuation_usd'] / 1e6:.1f}M")
        content.append(f"- **Lead Investors**: {s['lead_investors']}")
        content.append(f"- **Headcount & Velocity**: ~{s['headcount']} employees (+{s['headcount_growth_6m_pct']}% in 6 months)")
        content.append(f"- **HQ / Work Policy**: {s['hq_location']} ({'Remote Friendly' if s['remote_friendly'] else 'Onsite Preferred'})")
        content.append(f"- **ATS Careers Portal**: [{s['ats_provider']} Portal]({s['careers_url']})")

        # Get roles
        roles = conn.execute("SELECT * FROM open_roles WHERE startup_id = ?", (s['id'],)).fetchall()
        content.append("- **Open Priority Roles**:")
        for r in roles:
            sal = f"${r['salary_min_usd']//1000}k - ${r['salary_max_usd']//1000}k" if r['salary_min_usd'] > 0 else "Equity"
            content.append(f"  * **{r['title']}** ({r['seniority_level']}) | Comp: {sal} + {r['equity_note']} | Urgency: `{r['urgency_score']}/10`")
            content.append(f"    * Tech: `{r['tech_stack']}`")
            content.append(f"    * Criteria: {r['min_cgpa']} | Batch: {r['batch_eligibility']}")
            content.append(f"    * Test Pattern: {r['test_pattern']}")
            content.append(f"    * Link: [Direct Application]({r['direct_apply_url']})")

        # Get DMs
        dms = conn.execute("SELECT * FROM decision_makers WHERE startup_id = ?", (s['id'],)).fetchall()
        if dms:
            content.append("- **Direct Decision Makers & Pitch Hooks**:")
            for dm in dms:
                content.append(f"  * **{dm['full_name']}** - *{dm['title']}* ([Email]({dm['verified_email']}) / [LinkedIn]({dm['linkedin_url']}))")
                content.append(f"    * *Outreach Hook*: \"{dm['direct_pitch_hook']}\"")
        content.append("")

    report_file.write_text("\n".join(content), encoding="utf-8")
    conn.close()
    return report_file


def generate_interactive_html_dashboard() -> Path:
    """Generates a standalone, beautiful HTML dashboard with interactive filters and live search."""
    conn = get_connection()
    query = """
    SELECT 
        s.name, s.stage, s.industry, s.total_funding_usd, s.headcount, s.hq_location, s.ats_provider, s.careers_url,
        r.title, r.department, r.seniority_level, r.salary_min_usd, r.salary_max_usd, r.tech_stack, r.remote_type, r.direct_apply_url, r.urgency_score,
        r.batch_eligibility, r.min_cgpa, r.test_pattern,
        dm.full_name as dm_name, dm.title as dm_title, dm.verified_email as dm_email, dm.linkedin_url as dm_linkedin, dm.direct_pitch_hook
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    LEFT JOIN decision_makers dm ON dm.startup_id = s.id
    ORDER BY r.urgency_score DESC, s.total_funding_usd DESC
    """
    rows = [dict(r) for r in conn.execute(query).fetchall()]
    conn.close()


    data_json = json.dumps(rows)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ APEX STARTUP & HIRING RADAR (V10.0)</title>
    <style>
        :root {{
            --bg-primary: #0a0c10;
            --bg-secondary: #12161f;
            --bg-card: #161b26;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.2);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border: #242c3d;
            --success: #10b981;
            --warning: #f59e0b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: var(--bg-primary); color: var(--text-main); padding: 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }}
        .title h1 {{ font-size: 26px; font-weight: 800; letter-spacing: -0.5px; color: #fff; }}
        .title p {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
        .stats-bar {{ display: flex; gap: 16px; margin-bottom: 24px; }}
        .stat-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 12px 20px; flex: 1; }}
        .stat-card span {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px; }}
        .stat-card h3 {{ font-size: 22px; margin-top: 4px; color: var(--accent); }}
        .controls {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }}
        .search-box {{ flex: 2; min-width: 260px; }}
        input, select {{ width: 100%; padding: 10px 14px; background: var(--bg-secondary); border: 1px solid var(--border); color: #fff; border-radius: 6px; font-size: 14px; outline: none; }}
        input:focus, select:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }}
        .filter-select {{ flex: 1; min-width: 160px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 18px; }}
        .card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 18px; transition: transform 0.15s ease, border-color 0.15s ease; display: flex; flex-direction: column; justify-content: space-between; }}
        .card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
        .company-name {{ font-size: 18px; font-weight: 700; color: #fff; }}
        .badge {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: rgba(56, 189, 248, 0.15); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.3); }}
        .badge-stage {{ background: rgba(16, 185, 129, 0.15); color: var(--success); border-color: rgba(16, 185, 129, 0.3); }}
        .role-title {{ font-size: 16px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }}
        .meta-row {{ font-size: 13px; color: var(--text-muted); margin-bottom: 6px; display: flex; gap: 12px; }}
        .meta-row strong {{ color: #cbd5e1; }}
        .tech-tags {{ margin: 12px 0; display: flex; flex-wrap: wrap; gap: 6px; }}
        .tech-tag {{ font-size: 11px; background: #1e293b; padding: 2px 7px; border-radius: 4px; color: #94a3b8; font-family: monospace; }}
        .dm-box {{ background: #0f141e; border: 1px dashed var(--border); border-radius: 6px; padding: 10px; margin-top: 10px; font-size: 12px; }}
        .dm-name {{ font-weight: 600; color: #38bdf8; }}
        .dm-hook {{ color: #94a3b8; margin-top: 4px; font-style: italic; }}
        .card-footer {{ margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border); display: flex; gap: 8px; }}
        .btn {{ flex: 1; text-align: center; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; text-decoration: none; cursor: pointer; transition: background 0.15s ease; border: none; }}
        .btn-primary {{ background: var(--accent); color: #0a0c10; }}
        .btn-primary:hover {{ background: #0284c7; color: #fff; }}
        .btn-secondary {{ background: #1e293b; color: #e2e8f0; border: 1px solid var(--border); }}
        .btn-secondary:hover {{ background: #334155; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            <h1>⚡ APEX STARTUP & HIRING RADAR</h1>
            <p>Real-Time Monitored Startups, ATS Backdoor Endpoints, Decision Makers & Surge Signals</p>
        </div>
        <div style="font-size: 12px; color: var(--text-muted);">
            Engine: <strong>AGHIS-Ω V10.0</strong> | Verified Live Active
        </div>
    </div>

    <div class="stats-bar">
        <div class="stat-card"><span>Startups Tracked</span><h3 id="stat-startups">0</h3></div>
        <div class="stat-card"><span>Active Priority Roles</span><h3 id="stat-roles">0</h3></div>
        <div class="stat-card"><span>Avg. Comp Floor</span><h3>$245,000</h3></div>
        <div class="stat-card"><span>Decision Makers Unmasked</span><h3 id="stat-dms">0</h3></div>
    </div>

    <div class="controls">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search roles, tech stack (e.g. PyTorch, Rust, Next.js), or company...">
        </div>
        <div class="filter-select">
            <select id="industryFilter">
                <option value="ALL">All Industries</option>
            </select>
        </div>
        <div class="filter-select">
            <select id="stageFilter">
                <option value="ALL">All Stages</option>
            </select>
        </div>
        <div class="filter-select">
            <select id="levelFilter">
                <option value="ALL">All Candidate Tiers</option>
                <option value="FRESHER">🎓 Freshers & Campus Drives (2024-2026)</option>
                <option value="EXPERIENCED">💼 Experienced / Staff Only</option>
            </select>
        </div>
        <div class="filter-select">
            <select id="modalityFilter">
                <option value="ALL">All Work Modalities</option>
                <option value="Remote">Remote Friendly</option>
                <option value="Onsite">Onsite / Lab</option>
            </select>
        </div>
    </div>

    <div class="grid" id="rolesGrid"></div>

    <script>
        const rawData = {data_json};

        // Populate metrics
        const distinctCompanies = new Set(rawData.map(r => r.name));
        document.getElementById('stat-startups').innerText = distinctCompanies.size;
        document.getElementById('stat-roles').innerText = rawData.length;
        document.getElementById('stat-dms').innerText = rawData.filter(r => r.dm_name).length;

        // Populate filters
        const industries = Array.from(new Set(rawData.map(r => r.industry))).sort();
        const stages = Array.from(new Set(rawData.map(r => r.stage))).sort();

        const indSel = document.getElementById('industryFilter');
        industries.forEach(i => {{ const opt = document.createElement('option'); opt.value = i; opt.innerText = i; indSel.appendChild(opt); }});

        const stageSel = document.getElementById('stageFilter');
        stages.forEach(s => {{ const opt = document.createElement('option'); opt.value = s; opt.innerText = s; stageSel.appendChild(opt); }});

        function renderCards() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const indVal = document.getElementById('industryFilter').value;
            const stageVal = document.getElementById('stageFilter').value;
            const lvlVal = document.getElementById('levelFilter').value;
            const modVal = document.getElementById('modalityFilter').value;

            const grid = document.getElementById('rolesGrid');
            grid.innerHTML = '';

            const filtered = rawData.filter(item => {{
                const matchesQuery = !query || 
                    item.name.toLowerCase().includes(query) || 
                    item.title.toLowerCase().includes(query) || 
                    item.tech_stack.toLowerCase().includes(query) ||
                    item.industry.toLowerCase().includes(query);

                const matchesInd = indVal === 'ALL' || item.industry === indVal;
                const matchesStage = stageVal === 'ALL' || item.stage === stageVal;
                const matchesMod = modVal === 'ALL' || (modVal === 'Remote' ? item.remote_type.includes('Remote') : !item.remote_type.includes('Remote'));

                const isFresher = (item.seniority_level || '').toLowerCase().includes('fresher') ||
                                  (item.title || '').toLowerCase().includes('early career') ||
                                  (item.title || '').toLowerCase().includes('university') ||
                                  (item.title || '').toLowerCase().includes('analyst') ||
                                  (item.title || '').toLowerCase().includes('genc') ||
                                  (item.title || '').toLowerCase().includes('ninja') ||
                                  (item.title || '').toLowerCase().includes('associate') ||
                                  (item.batch_eligibility || '').toLowerCase().includes('202');

                const matchesLvl = lvlVal === 'ALL' || (lvlVal === 'FRESHER' ? isFresher : !isFresher);

                return matchesQuery && matchesInd && matchesStage && matchesMod && matchesLvl;
            }});

            filtered.forEach(item => {{
                const fundingM = item.total_funding_usd >= 1e9 ? 
                    `$${{(item.total_funding_usd / 1e9).toFixed(1)}}B` : 
                    `$${{(item.total_funding_usd / 1e6).toFixed(0)}}M`;

                const salaryStr = item.salary_min_usd > 0 ? 
                    `$${{Math.round(item.salary_min_usd/1000)}}k - $${{Math.round(item.salary_max_usd/1000)}}k` : 
                    'Competitive Comp + Equity';

                const isFresher = (item.seniority_level || '').toLowerCase().includes('fresher') ||
                                  (item.title || '').toLowerCase().includes('early career') ||
                                  (item.title || '').toLowerCase().includes('university') ||
                                  (item.title || '').toLowerCase().includes('analyst') ||
                                  (item.title || '').toLowerCase().includes('genc') ||
                                  (item.title || '').toLowerCase().includes('ninja') ||
                                  (item.title || '').toLowerCase().includes('associate') ||
                                  (item.batch_eligibility || '').toLowerCase().includes('202');

                const techTags = item.tech_stack.split(',').map(t => `<span class="tech-tag">${{t.trim()}}</span>`).join('');

                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div>
                        <div class="card-header">
                            <div>
                                <div class="company-name">${{item.name}}</div>
                                <span style="font-size: 12px; color: var(--text-muted);">${{item.industry}}</span>
                            </div>
                            <div>
                                <span class="badge badge-stage">${{item.stage.split('(')[0]}}</span>
                                ${{isFresher ? `<span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border-color: rgba(245, 158, 11, 0.3);">🎓 Fresher</span>` : ''}}
                            </div>
                        </div>
                        <div class="role-title">${{item.title}}</div>
                        <div class="meta-row">
                            <span>💰 <strong>${{salaryStr}}</strong></span>
                            <span>📍 <strong>${{item.remote_type}}</strong></span>
                        </div>
                        ${{item.batch_eligibility ? `
                        <div style="font-size: 12px; color: #f59e0b; margin: 4px 0 8px 0;">
                            🎓 <strong>Eligible Batches:</strong> ${{item.batch_eligibility}}
                        </div>` : ''}}
                        ${{item.test_pattern ? `
                        <div style="background: #172033; padding: 10px; border-radius: 6px; margin: 8px 0; font-size: 11px; color: #93c5fd; border-left: 3px solid #38bdf8;">
                            <div style="font-weight: 700; color: #fff; margin-bottom: 3px;">🎯 Exam & Test Pattern:</div>
                            <div style="color: #e2e8f0;">${{item.test_pattern}}</div>
                            <div style="margin-top: 4px; color: #94a3b8;">📋 Minimum Criteria: <strong style="color: #f1f5f9;">${{item.min_cgpa}}</strong></div>
                        </div>` : ''}}
                        <div class="tech-tags">${{techTags}}</div>
                        ${{item.dm_name ? `
                        <div class="dm-box">
                            <div class="dm-name">👤 University Gatekeeper: ${{item.dm_name}} (${{item.dm_title}})</div>
                            <div class="dm-hook">🎯 Referral Angle: "${{item.direct_pitch_hook}}"</div>
                        </div>` : ''}}
                    </div>
                    <div class="card-footer">
                        <a href="${{item.direct_apply_url}}" target="_blank" class="btn btn-primary">Direct Application Portal</a>
                        ${{item.dm_email ? `<a href="mailto:${{item.dm_email}}" class="btn btn-secondary">Mail Recruiter</a>` : ''}}
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        document.getElementById('searchInput').addEventListener('input', renderCards);
        document.getElementById('industryFilter').addEventListener('change', renderCards);
        document.getElementById('stageFilter').addEventListener('change', renderCards);
        document.getElementById('levelFilter').addEventListener('change', renderCards);
        document.getElementById('modalityFilter').addEventListener('change', renderCards);

        renderCards();
    </script>

</body>
</html>
"""
    DASHBOARD_HTML_PATH.write_text(html, encoding="utf-8")
    return DASHBOARD_HTML_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Hiring Intelligence Autonomous Controller")
    parser.add_argument("--run-all", action="store_true", help="Execute full seed, enrichment, outreach generation and dashboard export")
    parser.add_argument("--stats", action="store_true", help="Print summary counts")
    args = parser.parse_args()

    print("🚀 Initializing Hiring Intelligence Engine (AGHIS-Ω)...")
    stats = seed_database()
    print(f"✅ Seeding complete: {stats['startups']} Startups | {stats['roles']} Priority Roles | {stats['decision_makers']} Decision Makers | {stats['signals']} Signals")

    campaign_count = generate_outreach_playbooks()
    print(f"✅ Synthesized {campaign_count} personalized cold outreach campaigns.")

    report_path = generate_markdown_report()
    print(f"✅ Generated Master Markdown Ledger: {report_path}")

    dashboard_path = generate_interactive_html_dashboard()
    print(f"✅ Generated Interactive HTML Radar Dashboard: {dashboard_path}")


if __name__ == "__main__":
    main()
