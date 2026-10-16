#!/usr/bin/env python3
"""
omega_master_engine.py — Unified Autonomous CLI Nexus
Controls all 3 ecosystems:
  1. Summer 2027 Internships (2,688 active jobs, dossiers, outreach)
  2. React 19 Mastery (444 questions, 13 live apps, 8 hooks, 4 labs)
  3. n8n Enterprise Automation (560 nodes, 14 production DAGs, server port 5678)
"""

import sys
import json
import sqlite3
import webbrowser
from pathlib import Path

# Ensure UTF-8 output across Windows consoles
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DB_PATH = Path(r"e:\anti\data\omega_unified_master.db")
NEXUS_HTML = Path(r"e:\anti\omega_master_nexus.html")

def universal_search(query: str, limit: int = 10):
    if not DB_PATH.exists():
        print("[-] Master database not found.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT domain, entity_id, title, category, content_text
            FROM unified_search_fts
            WHERE unified_search_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT domain, entity_id, title, category, content_text
            FROM unified_search_fts
            WHERE title LIKE ? OR content_text LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\n[OMEGA MASTER FTS5] Found {len(results)} matches across all repositories for '{query}':")
    print("=" * 85)
    for dom, eid, title, cat, content in results:
        preview = content[:180].replace("\n", " ").strip()
        print(f"[{dom:16s}] {title} ({cat}) -> {eid}")
        print(f"   Preview: {preview}...")
        print("-" * 85)

def show_overview():
    if not DB_PATH.exists():
        print("[-] Master database not found.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    print("\n=================================================================================")
    print("                  OMEGA ∞ UNIFIED AUTONOMOUS ENTERPRISE NEXUS                    ")
    print("=================================================================================")
    
    c.execute("SELECT COUNT(*) FROM summer2027_listings")
    print(f"  [1] Summer 2027 Internships   : {c.fetchone()[0]:,d} Active Listings Indexed")

    c.execute("SELECT COUNT(*) FROM new_grad_listings")
    print(f"  [2] New Grad 2026 Positions   : {c.fetchone()[0]:,d} Active Roles Indexed")
    
    c.execute("SELECT COUNT(*) FROM react_questions")
    q_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM react_coding_projects")
    p_count = c.fetchone()[0]
    print(f"  [3] React 19 Engineering      : {q_count} Questions • {p_count} Machine Coding Apps")

    c.execute("SELECT COUNT(*) FROM n8n_nodes")
    n_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM n8n_workflows")
    w_count = c.fetchone()[0]
    print(f"  [4] n8n Enterprise Automation : {n_count} Integration Nodes • {w_count} Active DAGs")

    c.execute("SELECT COUNT(*) FROM hww_companies")
    h_count = c.fetchone()[0]
    print(f"  [5] Hiring Without Whiteboards: {h_count} Vetted Progressive Tech Companies")

    c.execute("SELECT COUNT(*) FROM frontend_challenges")
    fc_count = c.fetchone()[0]
    print(f"  [6] Frontend Code Challenges  : {fc_count} Real-World Open-Source Hiring Tests")

    c.execute("SELECT COUNT(*) FROM ai_college_jobs")
    ai_count = c.fetchone()[0]
    print(f"  [7] 2027 AI College Jobs      : {ai_count:,d} FAANG+, Quant & AI Lab Opportunities")

    c.execute("SELECT COUNT(*) FROM new_grad_2027")
    ng27_count = c.fetchone()[0]
    print(f"  [8] New Grad 2027 Positions   : {ng27_count:,d} Active Early Career Roles Indexed")

    c.execute("SELECT COUNT(*) FROM justhireme_leads")
    jhm_count = c.fetchone()[0]
    print(f"  [9] JustHireMe Job Intel      : {jhm_count:,d} Evaluated & Scored Roles")

    c.execute("SELECT COUNT(*) FROM jobfunnel_master")
    jf_count = c.fetchone()[0]
    print(f"  [10] JobFunnel Master Funnel  : {jf_count:,d} Deduplicated Clean Postings")

    c.execute("SELECT COUNT(*) FROM unified_search_fts")
    print(f"  --> Total Unified FTS5 Index  : {c.fetchone()[0]:,d} Cross-Repository Entities")
    print("=================================================================================\n")
    conn.close()

def open_nexus():
    if NEXUS_HTML.exists():
        print(f"[+] Opening {NEXUS_HTML} in browser...")
        webbrowser.open(NEXUS_HTML.as_uri())

def main():
    if len(sys.argv) < 2:
        print("""OMEGA Master Unified CLI Engine
Usage:
  python omega_master_engine.py --nexus         # Open Universal Visual Command Center
  python omega_master_engine.py --search <term> # Fast cross-repository FTS5 search
  python omega_master_engine.py --overview      # Display metrics across all 10 ecosystems
  python omega_master_engine.py --summer        # Launch Summer 2027 Dashboard
  python omega_master_engine.py --newgrad       # Launch New Grad 2026 Dashboard
  python omega_master_engine.py --newgrad27     # Launch New Grad 2027 Dashboard
  python omega_master_engine.py --justhireme    # Launch JustHireMe Intelligence Dashboard
  python omega_master_engine.py --jobfunnel     # Launch JobFunnel Master Funnel Dashboard
  python omega_master_engine.py --ai            # Launch 2027 AI College Jobs Dashboard
  python omega_master_engine.py --react         # Launch React Interview & Coding Center
  python omega_master_engine.py --n8n           # Launch n8n Workflow Server & UI
  python omega_master_engine.py --hww           # Launch Hiring Without Whiteboards Dashboard
  python omega_master_engine.py --challenges    # Launch Frontend Challenges Dashboard
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--nexus", "-n", "nexus"]:
        open_nexus()
    elif cmd in ["--search", "-s", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search query.")
            return
        universal_search(q)
    elif cmd in ["--overview", "-o", "overview"]:
        show_overview()
    elif cmd in ["--summer"]:
        webbrowser.open(Path(r"e:\anti\summer_2027_dashboard.html").as_uri())
    elif cmd in ["--newgrad", "-ng"]:
        webbrowser.open(Path(r"e:\anti\new_grad_dashboard.html").as_uri())
    elif cmd in ["--newgrad27", "-ng27"]:
        webbrowser.open(Path(r"e:\anti\new_grad_2027_dashboard.html").as_uri())
    elif cmd in ["--justhireme", "-jhm"]:
        webbrowser.open(Path(r"e:\anti\justhireme_dashboard.html").as_uri())
    elif cmd in ["--jobfunnel", "-jf", "--funnel"]:
        webbrowser.open(Path(r"e:\anti\jobfunnel_dashboard.html").as_uri())
    elif cmd in ["--ai"]:
        webbrowser.open(Path(r"e:\anti\ai_college_jobs_dashboard.html").as_uri())
    elif cmd in ["--react"]:
        webbrowser.open(Path(r"e:\anti\react_interview_command_center.html").as_uri())
    elif cmd in ["--n8n"]:
        webbrowser.open("http://localhost:5678")
    elif cmd in ["--hww"]:
        webbrowser.open(Path(r"e:\anti\hiring_without_whiteboards_dashboard.html").as_uri())
    elif cmd in ["--challenges", "-c"]:
        webbrowser.open(Path(r"e:\anti\frontend_challenges_dashboard.html").as_uri())
    elif cmd in ["--enterprise", "-e", "--company"]:
        webbrowser.open(Path(r"e:\anti\one_person_company_dashboard.html").as_uri())
    elif cmd in ["--million", "-m", "--scale"]:
        webbrowser.open(Path(r"e:\anti\million_dollar_company_dashboard.html").as_uri())
    elif cmd in ["--hyperscale", "-hsc", "--velocity"]:
        webbrowser.open(Path(r"e:\anti\hyperscale_velocity_dashboard.html").as_uri())
    elif cmd in ["--wealth", "-w", "--billionaires"]:
        webbrowser.open(Path(r"e:\anti\billionaire_wealth_dashboard.html").as_uri())
    elif cmd in ["--portal", "-p", "--client"]:
        webbrowser.open(Path(r"e:\anti\client_onboarding_portal.html").as_uri())
    elif cmd in ["--global-money", "--money", "-gm"]:
        webbrowser.open(Path(r"e:\anti\global_money_dashboard.html").as_uri())
    elif cmd in ["--trinity", "-t", "--trinity-wealth"]:
        webbrowser.open(Path(r"e:\anti\trinity_wealth_dashboard.html").as_uri())
    elif cmd in ["--run-daily", "--daily", "--cycle"]:
        import subprocess
        subprocess.run([sys.executable, "enterprise_engine.py"])
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
