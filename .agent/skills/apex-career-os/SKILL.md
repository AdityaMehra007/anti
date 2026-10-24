---
name: apex-career-os
description: Autonomous master career intelligence, multi-source job hunting, online learning, ATS resume tailoring, 9,223 recruiter network matching, and interview simulation engine for Aditya Mehra.
---

# APEX CAREER SUPREMACY OS (Ω-CAREER-UNIVERSE)

Master skill for autonomous career execution, job discovery, recruiter orchestration, and career velocity.

## When to Use This Skill
- Finding, scraping, and scoring job opportunities across Bangalore, Pan-India, and Global remote markets.
- Learning from online career boards, engineering blogs, and company websites to extract hiring signals, interview loops, and ATS keywords.
- Generating 100% truth-grounded, zero-hallucination ATS resumes and cover letters for Aditya Mehra (BBA International Business, DSU Bangalore).
- Matching target companies against Aditya's 9,223 LinkedIn connections to find direct Talent Acquisition leads and draft personalized outreach cadences.
- Simulating company-specific interview loops with STAR-method situational answers based on verified achievements (Aero India 2025, 15% procurement cost reduction, Pencil Mark BD revenue).
- Benchmarking compensation and planning 30-60-90 day onboarding and 5-year hyper-growth ladders.

## Quick CLI Usage
```bash
# Run full autonomous cycle (Scan -> Learn -> Match -> Tailor -> Dispatch -> Web Cockpit)
python -m apex_career_os.cli --auto-pilot

# Continuous online learning and ATS keyword taxonomy update
python -m apex_career_os.cli --learn

# Harvest active jobs from 16,500+ database and live APIs
python -m apex_career_os.cli --scan

# Instant strike for a specific company and role
python -m apex_career_os.cli --tailor --company "Google" --role "Operations Associate"

# Find verified recruiters in 9,223 network for a company
python -m apex_career_os.cli --network --company "Deloitte"

# Generate real interview prep and STAR responses
python -m apex_career_os.cli --interview --company "Accenture" --role "Operations Analyst"

# Open the Mission Control Web Cockpit in browser
python -m apex_career_os.cli --cockpit
```

## Python API Integration
```python
from apex_career_os.orchestrator import ApexCareerOrchestrator

orch = ApexCareerOrchestrator()
# Execute instant strike for any company
strike_pack = orch.execute_instant_strike_for_custom_role(
    company="Zepto",
    title="City Operations Lead",
    description="Manage dark store logistics, inventory turnaround, and ground vendor SLAs.",
    track="Operations & Vendor Governance"
)
print("ATS Match:", strike_pack["ats_evaluation"]["match_score_percent"])
print("Recruiters:", [r["name"] for r in strike_pack["recruiters"]])
```

## Architecture & Subagents
1. **SentinelLearnerAgent**: Live web scraper, multi-portal aggregator, continuous knowledge harvester.
2. **TruthTailorAgent**: Zero-hallucination resume, cover letter, and elevator pitch generator.
3. **NetworkStrikeAgent**: 9,223 LinkedIn recruiter search, warm referral, and 3-touch cadence engine.
4. **AutoApplyDispatcherAgent**: ATS autofill payload assembler & Kanban pipeline manager.
5. **InterviewMasterAgent**: STAR interview coach, question bank, and curveball defense trainer.
6. **CompensationStrategistAgent**: Market benchmark calculator, offer breakdown, and counter-offer scripts.
7. **CareerGrowthArchitectAgent**: 30-60-90 day onboarding blueprints & 5-year executive career ladder.
