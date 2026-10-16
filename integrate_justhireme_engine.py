#!/usr/bin/env python3
"""
integrate_justhireme_engine.py — Integrate JustHireMe scoring & intelligence engine
Ranks and evaluates roles across the OMEGA Master database using JustHireMe's
deterministic scoring engine, quality gates, and lead intelligence.
"""

import sys
from pathlib import Path
import sqlite3
import json

# Ensure UTF-8 output
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

JHM_BACKEND = Path(r"e:\anti\JustHireMe\backend")
sys.path.insert(0, str(JHM_BACKEND))

try:
    from ranking.evaluator import score as score_fit
    from discovery.lead_intel import signal_quality, tech_stack_from_text
    from discovery.quality_gate import evaluate_lead_quality
    print("[+] Successfully loaded JustHireMe core ranking & discovery engines.")
except Exception as e:
    print(f"[-] Error loading JustHireMe modules: {e}")
    sys.exit(1)

MASTER_DB = Path(r"e:\anti\data\omega_unified_master.db")
JHM_DB = Path(r"e:\anti\data\justhireme_leads.db")
OUT_JSON = Path(r"e:\anti\data\justhireme_evaluated_roles.json")

# Aditya Mehra's verified candidate profile
CANDIDATE_PROFILE = {
    "n": "Aditya Mehra",
    "s": "Systems & Operations Analyst, Autonomous AI Agent Architect, Full-Stack Distributed Systems",
    "skills": [
        {"n": "Python"},
        {"n": "SQLite"},
        {"n": "FTS5"},
        {"n": "React"},
        {"n": "TypeScript"},
        {"n": "Automation"},
        {"n": "n8n"},
        {"n": "Distributed Systems"},
        {"n": "Data Pipelines"},
        {"n": "API Design"}
    ],
    "exp": [
        {
            "role": "Systems & Operations Analyst",
            "co": "Autonomous Systems Architecture",
            "period": "2024 to present",
            "d": "Engineered autonomous task-dispatch DAGs, deterministic evaluation loops, and sub-millisecond FTS5 search engines across 10,400+ entities.",
            "s": ["Python", "SQLite", "FTS5", "React", "n8n"]
        }
    ],
    "projects": [
        {
            "title": "OMEGA Autonomous Enterprise Nexus",
            "stack": ["Python", "SQLite", "FTS5", "FastAPI", "React"],
            "impact": "Indexed and unified 10,447 cross-repository opportunities, documentation nodes, and test suites with sub-millisecond query latency."
        },
        {
            "title": "Autonomous M2M Micropayment Settlement",
            "stack": ["Python", "n8n", "Webhooks", "FastAPI"],
            "impact": "Designed automated micro-invoicing DAGs and state channel verification engines with sub-second finality."
        }
    ],
    "education": [
        {
            "degree": "BBA International Business",
            "school": "Dayananda Sagar University (DSU), Bengaluru",
            "grad": "2026",
            "gpa": "8.78/10.0"
        }
    ]
}

def main():
    print("[+] Querying candidate roles from OMEGA Master Database...")
    conn = sqlite3.connect(str(MASTER_DB))
    c = conn.cursor()
    c.execute("""
        SELECT domain, entity_id, title, category, content_text 
        FROM unified_search_fts 
        WHERE domain IN ('AI College Jobs 2027', 'New Grad 2027', 'New Grad 2026', 'Summer 2027')
    """)
    rows = c.fetchall()
    conn.close()

    print(f"[+] Loaded {len(rows):,d} candidate job postings. Evaluating with JustHireMe engine...")

    evaluated_leads = []
    # Evaluate top 250 diverse target roles across ecosystems
    sample_rows = rows[:300]
    for dom, eid, title, cat, text in sample_rows:
        lead_dict = {
            "title": title,
            "description": text,
            "url": "",
            "source": dom
        }
        
        # 1. Quality Gate assessment
        q_gate = evaluate_lead_quality(lead_dict, min_quality=40, target_level="entry", max_age_days=30)
        
        # 2. Tech stack extraction
        stack = tech_stack_from_text(text)
        
        # 3. Deterministic candidate fit score
        fit = score_fit(text, CANDIDATE_PROFILE, use_llm=False)
        
        evaluated_leads.append({
            "job_id": eid,
            "title": title,
            "domain": dom,
            "category": cat,
            "fit_score": fit.get("score", 0),
            "quality_score": q_gate.get("quality_score", 0),
            "is_accepted": q_gate.get("accepted", True),
            "reason": fit.get("reason", ""),
            "match_points": fit.get("match_points", []),
            "gaps": fit.get("gaps", []),
            "tech_stack": list(stack),
            "content_preview": text[:200]
        })

    # Sort by fit_score descending
    evaluated_leads.sort(key=lambda x: x["fit_score"], reverse=True)

    # Save to JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(evaluated_leads, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved {len(evaluated_leads)} evaluated roles to {OUT_JSON}")

    # Build JustHireMe Standalone SQLite Database
    conn_jhm = sqlite3.connect(str(JHM_DB))
    c_jhm = conn_jhm.cursor()
    c_jhm.execute("""
        CREATE TABLE IF NOT EXISTS justhireme_leads (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            domain TEXT,
            category TEXT,
            fit_score INTEGER,
            quality_score INTEGER,
            is_accepted INTEGER,
            reason TEXT,
            match_points TEXT,
            gaps TEXT,
            tech_stack TEXT,
            content_preview TEXT
        )
    """)
    for lead in evaluated_leads:
        c_jhm.execute("""
            INSERT OR REPLACE INTO justhireme_leads 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead["job_id"],
            lead["title"],
            lead["domain"],
            lead["category"],
            lead["fit_score"],
            lead["quality_score"],
            1 if lead["is_accepted"] else 0,
            lead["reason"],
            json.dumps(lead["match_points"]),
            json.dumps(lead["gaps"]),
            ", ".join(lead["tech_stack"]),
            lead["content_preview"]
        ))
    
    c_jhm.execute("DROP TABLE IF EXISTS justhireme_leads_fts")
    c_jhm.execute("""
        CREATE VIRTUAL TABLE justhireme_leads_fts USING fts5(
            job_id, title, domain, category, reason, tech_stack
        )
    """)
    c_jhm.execute("""
        INSERT INTO justhireme_leads_fts
        SELECT job_id, title, domain, category, reason, tech_stack FROM justhireme_leads
    """)
    conn_jhm.commit()
    conn_jhm.close()
    print(f"[+] Built dedicated JustHireMe SQLite FTS5 database: {JHM_DB}")

    # Merge into Master Unified Database
    conn_m = sqlite3.connect(str(MASTER_DB))
    c_m = conn_m.cursor()
    c_m.execute("""
        CREATE TABLE IF NOT EXISTS justhireme_leads (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            domain TEXT,
            category TEXT,
            fit_score INTEGER,
            quality_score INTEGER,
            is_accepted INTEGER,
            reason TEXT,
            match_points TEXT,
            gaps TEXT,
            tech_stack TEXT,
            content_preview TEXT
        )
    """)
    for lead in evaluated_leads:
        c_m.execute("""
            INSERT OR REPLACE INTO justhireme_leads 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead["job_id"],
            lead["title"],
            lead["domain"],
            lead["category"],
            lead["fit_score"],
            lead["quality_score"],
            1 if lead["is_accepted"] else 0,
            lead["reason"],
            json.dumps(lead["match_points"]),
            json.dumps(lead["gaps"]),
            ", ".join(lead["tech_stack"]),
            lead["content_preview"]
        ))

    c_m.execute("DELETE FROM unified_search_fts WHERE domain = 'JustHireMe Intel'")
    for lead in evaluated_leads:
        content = f"{lead['title']} {lead['domain']} {lead['category']} Fit:{lead['fit_score']} {lead['reason']} {lead['tech_stack']}"
        c_m.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "JustHireMe Intel",
            lead["job_id"],
            f"{lead['title']} [Fit: {lead['fit_score']}%]",
            f"Evaluated Lead ({lead['domain']})",
            content
        ))
    conn_m.commit()
    conn_m.close()
    print("[+] Merged JustHireMe Intel into Master Unified FTS5 Database.")

if __name__ == "__main__":
    main()
