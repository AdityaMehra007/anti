"""
OMEGA LIVE CAREER COMMAND CLI
Handles live interactive queries: "Find me the best jobs today", etc.
"""
import sys
import os
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
import json
from ..mcp.client import FirecrawlClient
from ..engines.job_discovery import JobDiscoveryEngine
from ..brain.career_brain import CareerBrain
from .dashboard_service import ControlTowerDashboardService

def live_career_command(query: str = "Find me the best jobs today in Bengaluru") -> str:
    discovery = JobDiscoveryEngine()
    brain = CareerBrain()
    jobs = discovery.discover_bengaluru_opportunities(limit=20)

    scored = []
    for job in jobs:
        score = brain.score_job(job)
        scored.append((job, score))

    # Rank by overall score
    scored.sort(key=lambda x: x[1].overall_score, reverse=True)

    output = []
    output.append(f"\n=======================================================")
    output.append(f"   OMEGA FIRECRAWL LIVE CAREER COMMAND: TOP {len(scored)} JOBS")
    output.append(f"   Query: {query}")
    output.append(f"=======================================================\n")

    for idx, (job, match) in enumerate(scored, 1):
        output.append(f"[{idx:02d}] {job.role.upper()} @ {job.company}")
        output.append(f"     Match Score : {match.overall_score}/100 | Fit: {match.fit_rationale}")
        output.append(f"     Location    : {job.location} ({job.work_mode}) | Requisition ID: {job.requisition_id}")
        output.append(f"     Salary Band : {job.salary or 'Competitive MNC Top Tier'}")
        output.append(f"     Verification: {job.verification_state} (Confidence: {job.confidence*100:.0f}%)")
        output.append(f"     Recruiter   : {job.public_recruiter or 'Public Talent Team'}")
        output.append(f"     Source URL  : {job.source_url}")
        output.append(f"     Next Action : {match.next_recommended_action}\n")

    return "\n".join(output)

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Find me the best jobs today in Bengaluru"
    print(live_career_command(q))
