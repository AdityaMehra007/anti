#!/usr/bin/env python3
"""
========================================================================================
OMEGA DISPATCH CONSOLE & INTERACTIVE COMMAND CENTER
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Core Capability:
  - Unified interactive command center for all 61 Tier-1 enterprise applications.
  - Granular tier-based filtering (Tier S, Tier A, Tier B).
  - One-click application launcher (copies cover letter, opens career portal).
  - External receipt logging and zero-trust DB synchronization.
  - Instant bridge to Interview Defense Simulator and OmniVanta Audit Engine.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import re
import json
import webbrowser
from typing import Dict, List, Any, Optional
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from omega.engines.omega_job_dispatcher import OmegaJobDispatcher

class OmegaDispatchConsole:
    """Unified terminal and interactive command console for career execution."""

    def __init__(self):
        self.dispatcher = OmegaJobDispatcher()
        self.jobs = self.dispatcher.jobs

    def get_job(self, job_id_or_company: str) -> Optional[Dict[str, Any]]:
        query = job_id_or_company.strip().lower()
        for j in self.jobs:
            if j["job_id"].lower() == query or query in j["company"].lower():
                return j
        return None

    def filter_by_tier(self, tier_prefix: str) -> List[Dict[str, Any]]:
        prefix = tier_prefix.strip().lower()
        return [j for j in self.jobs if prefix in j.get("tier", "").lower()]

    def render_job_card(self, job: Dict[str, Any]) -> str:
        lines = [
            "=" * 78 + "\n",
            f"  TARGET DOSSIER: {job['company']} ({job['job_id']})\n",
            "=" * 78 + "\n",
            f"  Position Title    : {job['position']}\n",
            f"  Specialization    : {job['track']}\n",
            f"  Classification    : {job['tier']}\n",
            f"  ATS Match Score   : {job['ats_score']}%\n",
            f"  Application Status: {job['status']}\n",
            f"  Career Portal URL : {job['portal_url']}\n",
            f"  Primary Recruiter : {job['contact_name']} ({job['contact_url']})\n",
            "-" * 78 + "\n",
            "  TAILORED COVER LETTER PREVIEW:\n",
            "-" * 78 + "\n",
            job['cover_letter'][:500] + ("\n  [... truncated ...]\n" if len(job['cover_letter']) > 500 else "\n"),
            "-" * 78 + "\n",
            "  LINKEDIN RECRUITER NOTE:\n",
            "-" * 78 + "\n",
            f"  {job['linkedin_note'][:300]}\n",
            "=" * 78 + "\n"
        ]
        return "".join(lines)

    def launch_job(self, job_id: str):
        job = self.get_job(job_id)
        if not job:
            print(f"[ERROR] Job ID '{job_id}' not found.")
            return
        self.dispatcher.apply_job(job["job_id"])

    def record_receipt(self, job_id: str, receipt_id: str):
        self.dispatcher.mark_applied(job_id, receipt_id)

def main():
    console = OmegaDispatchConsole()
    args = sys.argv[1:]

    if not args or args[0] in ["list", "dashboard"]:
        print("\n" + "=" * 80)
        print(f"        OMEGA DISPATCH CONSOLE // {len(console.jobs)} TARGET REQUISITIONS")
        print("=" * 80)
        print(f"{'#':<4} {'JOB ID':<13} {'TARGET ENTERPRISE':<26} {'ATS':<5} {'TIER':<10} {'STATUS'}")
        print("-" * 80)
        for idx, j in enumerate(console.jobs, 1):
            tier_short = "Tier S" if "Tier S" in j["tier"] else ("Tier A" if "Tier A" in j["tier"] else "Tier B")
            print(f"{idx:<4} {j['job_id']:<13} {j['company'][:25]:<26} {j['ats_score']}%  {tier_short:<10} {j['status']}")
        print("=" * 80)
    elif args[0] == "view" and len(args) > 1:
        job = console.get_job(args[1])
        if job:
            print(console.render_job_card(job))
        else:
            print(f"[ERROR] Job '{args[1]}' not found.")
    elif args[0] == "launch" and len(args) > 1:
        console.launch_job(args[1])
    elif args[0] == "mark" and len(args) > 2:
        console.record_receipt(args[1], args[2])
    elif args[0] == "tier" and len(args) > 1:
        tier_jobs = console.filter_by_tier(args[1])
        print(f"\nTarget Requisitions in '{args[1]}': {len(tier_jobs)}")
        for j in tier_jobs:
            print(f"  • [{j['job_id']}] {j['company']} -- {j['position']} ({j['ats_score']}%)")
    else:
        print("Usage: python omega_dispatch_console.py [list | view <JOB_ID> | launch <JOB_ID> | mark <JOB_ID> <RECEIPT> | tier <S|A|B>]")

if __name__ == "__main__":
    main()
