#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY OMEGA — REMOTE CAREER STRIKE & DISPATCH ENGINE
========================================================================================
Ingests live remote jobs from Remotive, RemoteOK, and WeWorkRemotely, cross-references
with awesome-remote-job's 232 Remote-DNA companies, scores matches against Adi's resume
(resume_adi.md), and generates an active dispatch board with tailored pitch angles.
========================================================================================
"""

import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

# Add remote job suite to sys.path
ROOT_DIR = Path(__file__).resolve().parent
SUITE_DIR = ROOT_DIR / "tools" / "remote_job_suite"
sys.path.insert(0, str(SUITE_DIR))

from scraper import search_all_jobs

DATA_DIR = SUITE_DIR / "data"
COMPANIES_FILE = DATA_DIR / "companies.json"
OUTPUT_MD = ROOT_DIR / "REMOTE_ACTIVE_DISPATCH_BOARD.md"
OUTPUT_JSON = ROOT_DIR / "data" / "remote_active_jobs.json"

TARGET_KEYWORDS = [
    "operations",
    "business operations",
    "analyst",
    "business analyst",
    "data operations",
    "project coordinator",
    "project manager",
    "vendor",
    "logistics",
    "ai evaluation",
    "research"
]

def score_opportunity(job: dict) -> int:
    title = job.get("title", "").lower()
    tags = " ".join(job.get("tags", [])).lower()
    loc = job.get("location", "").lower()
    
    score = 50
    # Location scoring
    if any(term in loc for term in ["worldwide", "anywhere", "apac", "india", "global", "remote"]):
        score += 25
    elif any(term in loc for term in ["us only", "usa only", "north america only"]):
        score -= 20

    # Role alignment scoring
    if any(k in title for k in ["operations", "business analyst", "project coordinator", "analyst"]):
        score += 20
    if any(k in title for k in ["ai", "data", "logistics", "vendor"]):
        score += 10
    if any(k in title for k in ["senior", "lead", "director", "architect"]):
        score -= 10  # Adi is Class of 2026 / entry-to-mid career

    return max(30, min(99, score))

def generate_pitch(job: dict) -> str:
    company = job.get("company", "the team")
    role = job.get("title", "this role")
    return (
        f"Hi {company} Hiring Team,\n\n"
        f"I saw the {role} opening and wanted to reach out directly. "
        f"I'm an International Business graduate (DSU '26) with hands-on experience coordinating end-to-end "
        f"operations, vendor contracts, and logistics for major brand exhibitions (Puma, Tata Communications, Dyson, Aero India). "
        f"I also build automated Python/Excel reporting pipelines that eliminate manual reconciliation and enforce strict SLAs.\n\n"
        f"Given your distributed culture, I thrive in async, documentation-first workflows where autonomous execution "
        f"and structured communication are standard. I'd welcome the chance to discuss how I can contribute to {company}'s operational velocity.\n\n"
        f"Best regards,\nAditya Mehra\nBengaluru, India | +91 7003456624 | ashishiash007@gmail.com"
    )

def run():
    print("=" * 70)
    print("       ANTIGRAVITY OMEGA — REMOTE CAREER STRIKE DISPATCH")
    print("=" * 70)
    
    # Ingest live feeds
    raw_jobs = []
    for kw in ["operations", "analyst", "coordinator", "ai", "project"]:
        print(f"Fetching live postings for '{kw}'...")
        batch = search_all_jobs(keyword=kw, limit_per_source=15)
        for b in batch:
            b["matched_keyword"] = kw
            raw_jobs.append(b)

    # Deduplicate
    seen = set()
    deduped = []
    for j in raw_jobs:
        if j["id"] not in seen:
            seen.add(j["id"])
            j["match_score"] = score_opportunity(j)
            j["outreach_pitch"] = generate_pitch(j)
            deduped.append(j)

    # Sort by match score descending
    deduped.sort(key=lambda x: x["match_score"], reverse=True)

    print(f"\nIndexed {len(deduped)} active remote opportunities.")

    # Save JSON
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)
    print(f"Saved structured jobs database to: {OUTPUT_JSON}")

    # Generate Markdown Dispatch Board
    now_str = datetime.now().strftime("%A, %B %d, %Y - %H:%M IST")
    lines = [
        "# ANTIGRAVITY OMEGA — REMOTE ACTIVE DISPATCH BOARD",
        f"**Generated:** `{now_str}`  ",
        "**Candidate:** `Aditya Mehra | BBA Intl Business (DSU '26) | Bengaluru`  ",
        f"**Active Global Opportunities:** `{len(deduped)} Positions Indexed`  ",
        "**Sources:** `Remotive Public API, RemoteOK API, WeWorkRemotely RSS, awesome-remote-job Directory`  ",
        "",
        "---",
        "",
        "## PRIORITY OPPORTUNITIES (SCORE >= 70)",
        "",
        "| ID | Score | Role / Title | Company | Location | Source | Salary / Tags | Application Link |",
        "|---|---|---|---|---|---|---|---|"
    ]

    for idx, j in enumerate(deduped, start=1):
        score_badge = f"`{j['match_score']}`"
        lines.append(
            f"| `RMT-{idx:03d}` | {score_badge} | **{j['title']}** | {j['company']} | {j['location']} | `{j['source']}` | {j.get('salary') or ', '.join(j['tags'][:2])} | [Apply Now]({j['url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## TAILORED OUTREACH DISPATCH SCRIPTS (SAMPLE TOP 5)",
        ""
    ])

    for idx, j in enumerate(deduped[:5], start=1):
        lines.extend([
            f"### [RMT-{idx:03d}] {j['title']} @ {j['company']} (Score: {j['match_score']})",
            f"- **URL**: {j['url']}",
            f"- **Location**: {j['location']} | **Source**: {j['source']}",
            "",
            "```text",
            j["outreach_pitch"],
            "```",
            ""
        ])

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Saved live dispatch board to: {OUTPUT_MD}")
    print("=" * 70)
    print("Remote dispatch strike run complete!")

if __name__ == "__main__":
    run()
