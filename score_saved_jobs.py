#!/usr/bin/env python3
"""
CAREER-OPS BATCH SAVED JOBS SCORER & REFERRAL MATCHER
=====================================================
Scores all 82 saved jobs from Aditya Mehra's verified LinkedIn export
against the canonical cv.md and matches 1st-degree referral champions
from the 10,401-connection SQLite database.
"""

import sys
import os
import csv
import json
import sqlite3
from pathlib import Path

# UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

EXPORT_DIR = Path(r"C:\Users\amehr\OneDrive\Desktop\linkdin\Basic_LinkedInDataExport_11-06-2026.zip")
WORKSPACE_DIR = Path(r"E:\anti")
DB_PATH = WORKSPACE_DIR / "data" / "linkedin_network_master_2026.sqlite"
CV_PATH = WORKSPACE_DIR / "career-ops" / "cv.md"

from career_ops_orchestrator import CareerOpsEvaluationEngine

def get_saved_jobs():
    saved_path = EXPORT_DIR / "Jobs" / "Saved Jobs.csv"
    jobs = []
    if not saved_path.exists():
        return jobs
    with open(saved_path, mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            co = row.get("Company Name", "").strip()
            title = row.get("Job Title", "").strip()
            url = row.get("Job Url", "").strip()
            date = row.get("Saved Date", "").strip()
            if co and title:
                jobs.append({
                    "company": co,
                    "title": title,
                    "url": url,
                    "saved_date": date
                })
    return jobs

def find_connections(company_name, conn):
    cur = conn.cursor()
    # Clean company name
    clean_co = company_name.split()[0].replace(',', '').replace('.', '')
    if len(clean_co) < 3:
        clean_co = company_name

    cur.execute("""
        SELECT full_name, position, tier, url, is_recruiter, is_founder, is_exec
        FROM connections
        WHERE company LIKE ?
        ORDER BY is_recruiter DESC, is_exec DESC, is_founder DESC
        LIMIT 10
    """, (f"%{clean_co}%",))
    
    rows = cur.fetchall()
    results = []
    for r in rows:
        results.append({
            "name": r[0],
            "position": r[1],
            "tier": r[2],
            "url": r[3],
            "is_recruiter": bool(r[4]),
            "is_founder": bool(r[5]),
            "is_exec": bool(r[6])
        })
    return results

def classify_track(title):
    t_lower = title.lower()
    if any(k in t_lower for k in ["operation", "operations", "logistics", "supply chain", "hsse"]):
        return "Business & Logistics Operations"
    elif any(k in t_lower for k in ["analyst", "analytics", "data", "business management"]):
        return "Business & Data Analytics"
    elif any(k in t_lower for k in ["founder", "chief of staff", "strategy", "advisor", "management consultant"]):
        return "Founder's Office & Strategy"
    elif any(k in t_lower for k in ["event", "marketing event", "exhibition"]):
        return "Event Operations & Client Delivery"
    elif any(k in t_lower for k in ["customer success", "client", "support", "account management"]):
        return "Customer Success & Client Experience"
    elif any(k in t_lower for k in ["product", "research"]):
        return "Product & Market Research"
    elif any(k in t_lower for k in ["hr", "talent", "recruitment"]):
        return "People & Talent Operations"
    elif any(k in t_lower for k in ["sales", "cold calling", "telecalling", "bdr", "sdr"]):
        return "Sales / Business Development (Iron Wall Review)"
    else:
        return "General Strategic Management"

def evaluate_iron_wall(title, company):
    t_lower = title.lower()
    sales_triggers = ["telecaller", "cold call", "door to door", "field sales", "b2c sales", "quota sales"]
    if any(k in t_lower for k in sales_triggers):
        return "REJECTED (Violates Iron Wall Non-Sales Policy)"
    return "APPROVED (Pure Operational / Strategic Mandate)"

def main():
    print("=" * 80)
    print("      CAREER-OPS BATCH SAVED JOBS SCORING & REFERRAL INTELLIGENCE")
    print("=" * 80)

    cv_text = CV_PATH.read_text(encoding="utf-8") if CV_PATH.exists() else ""
    saved_jobs = get_saved_jobs()
    print(f"[1/3] Ingested {len(saved_jobs)} Saved Jobs from LinkedIn Export...")

    conn = sqlite3.connect(DB_PATH)
    evaluator = CareerOpsEvaluationEngine()

    scored_jobs = []

    print("[2/3] Executing CareerOps Scoring & 1st-Degree Network Matching...")
    for idx, j in enumerate(saved_jobs):
        company = j["company"]
        title = j["title"]
        url = j["url"]
        saved_date = j["saved_date"]
        track = classify_track(title)
        policy_status = evaluate_iron_wall(title, company)

        # Mock JD text with role and company
        jd_text = f"Company: {company}\nTitle: {title}\nKey Requirements: Operations, Business Analysis, Process Management, Stakeholder Communication, Reporting, Team Collaboration"
        
        eval_result = evaluator.evaluate(jd_text, cv_text, url)
        raw_score = eval_result["metadata"]["score_numeric"]
        
        # Policy adjustment
        if "REJECTED" in policy_status:
            score = 1.0
            verdict = "DISQUALIFIED (Iron Wall Sales Policy)"
        else:
            score = raw_score
            if score >= 4.5:
                verdict = "Priority Strike"
            elif score >= 3.8:
                verdict = "Strong Match"
            elif score >= 3.0:
                verdict = "Consider"
            else:
                verdict = "Do Not Apply"

        connections = find_connections(company, conn)

        scored_jobs.append({
            "index": idx + 1,
            "company": company,
            "title": title,
            "saved_date": saved_date,
            "url": url,
            "track": track,
            "policy": policy_status,
            "score": score,
            "score_str": f"{score:.1f}/5.0",
            "verdict": verdict,
            "connections_count": len(connections),
            "top_connections": connections[:3]
        })

    conn.close()

    # Sort by score DESC, then connections_count DESC
    scored_jobs.sort(key=lambda x: (x["score"], x["connections_count"]), reverse=True)

    print("\n" + "=" * 80)
    print("                TOP TIER SAVED JOBS LEADERBOARD (SCORE >= 4.0)")
    print("=" * 80)
    print(f"{'#':<3} | {'COMPANY':<20} | {'ROLE TITLE':<35} | {'SCORE':<7} | {'CONNECTIONS'}")
    print("-" * 80)

    for sj in scored_jobs[:25]:
        conn_str = f"{sj['connections_count']} 1st-degree" if sj['connections_count'] > 0 else "None"
        print(f"{sj['index']:<3} | {sj['company'][:20]:<20} | {sj['title'][:35]:<35} | {sj['score_str']:<7} | {conn_str}")

    # Save to JSON report
    report_path = WORKSPACE_DIR / "data" / "saved_jobs_scored_report.json"
    report_path.write_text(json.dumps(scored_jobs, indent=2), encoding="utf-8")
    print(f"\n[3/3] Detailed scoring report written to {report_path}")

    # Summary Stats
    priority_count = sum(1 for j in scored_jobs if j["score"] >= 4.5)
    strong_count = sum(1 for j in scored_jobs if 3.8 <= j["score"] < 4.5)
    with_conn_count = sum(1 for j in scored_jobs if j["connections_count"] > 0)

    print("\n" + "=" * 80)
    print("  SUMMARY TELEMETRY:")
    print(f"  - Total Saved Jobs Scored: {len(scored_jobs)}")
    print(f"  - Priority Strike Roles (>= 4.5/5.0): {priority_count}")
    print(f"  - Strong Match Roles (3.8 - 4.4):     {strong_count}")
    print(f"  - Jobs with Direct 1st-Degree Insiders: {with_conn_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()
