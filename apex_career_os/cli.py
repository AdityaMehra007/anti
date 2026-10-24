"""
cli.py - OMEGA Master Career Supremacy Command Line Interface
============================================================
Autonomous execution interface for:
  --auto-pilot : Full autonomous end-to-end cycle (Scrape -> Learn -> Tailor -> Dispatch -> Cockpit)
  --scan       : Harvest active jobs across 16,500+ listings and live portals
  --learn      : Continuous online learning from company postings and tech blogs
  --tailor     : Generate 100% truth-grounded ATS resume & cover letter
  --network    : Pull recruiters from 9,223 LinkedIn network for target company
  --interview  : Real-world STAR interview prep and curveball defenses
  --comp       : Benchmark Bangalore market compensation & negotiation scripts
  --cockpit    : Generate and launch the interactive Mission Control HTML Cockpit
"""

import sys
import argparse
import json
import webbrowser
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from apex_career_os.orchestrator import ApexCareerOrchestrator
from apex_career_os.ui.cockpit_generator import generate_cockpit_html

def main():
    parser = argparse.ArgumentParser(
        description="APEX CAREER SUPREMACY OS — Autonomous Job Conquest Engine"
    )
    parser.add_argument("--auto-pilot", action="store_true", help="Run full autonomous cycle across all 7 agents")
    parser.add_argument("--scan", action="store_true", help="Harvest and mine active jobs")
    parser.add_argument("--learn", action="store_true", help="Execute continuous online learning and ATS taxonomy updates")
    parser.add_argument("--tailor", action="store_true", help="Generate tailored ATS resume & cover letter")
    parser.add_argument("--company", type=str, default="Accenture", help="Target company name")
    parser.add_argument("--role", type=str, default="Operations & Growth Associate", help="Target role title")
    parser.add_argument("--track", type=str, default="Operations & Vendor Governance", help="Career track")
    parser.add_argument("--network", action="store_true", help="Find recruiters for target company")
    parser.add_argument("--interview", action="store_true", help="Generate STAR interview prep pack")
    parser.add_argument("--comp", action="store_true", help="Benchmark compensation percentiles")
    parser.add_argument("--cockpit", action="store_true", help="Generate interactive HTML Cockpit")
    parser.add_argument("--dissect-jd", type=str, default="", help="Dissect raw Job Description text or file")
    parser.add_argument("--universal-cockpit", action="store_true", help="Launch Universal Master Job & Skill Intelligence Cockpit")
    parser.add_argument("--limit", type=int, default=50, help="Job evaluation limit")

    args = parser.parse_args()
    orchestrator = ApexCareerOrchestrator()

    print("=" * 80)
    print("  APEX CAREER SUPREMACY OS (OMEGA CAREER UNIVERSE) v10.0.0-APEX-SUPREME")
    print("  Candidate: Aditya Mehra | Truth Layer: EXP-001 to EXP-009 (100% Verified)")
    print("=" * 80)

    if args.auto_pilot or (not any([args.scan, args.learn, args.tailor, args.network, args.interview, args.comp, args.cockpit, args.dissect_jd, args.universal_cockpit])):
        print("[APEX] Initiating full autonomous conquest cycle...")
        telemetry = orchestrator.run_full_autonomous_cycle(limit_jobs=args.limit)
        cockpit_file = generate_cockpit_html(telemetry)
        print(f"\n[APEX] SUCCESS! Cockpit generated at: {cockpit_file}")
        print(f"[APEX] Total Jobs Evaluated: {telemetry['total_jobs_evaluated']}")
        print(f"[APEX] Top-Tier Strong Matches (>=85%): {telemetry['top_tier_matches']}")
        print(f"[APEX] Active Kanban Applications: {telemetry['kanban_pipeline']['total_applications']}")
        print("\nOpening Mission Control Cockpit in your default browser...")
        try:
            webbrowser.open(f"file:///{cockpit_file}")
        except Exception:
            pass
        return

    if args.learn:
        print(f"[APEX] Running continuous online learning cycle...")
        res = orchestrator.sentinel.run_harvest_and_learn_cycle(limit=args.limit)
        print(f"Learnings Ingested: {res['new_learnings_ingested']} jobs from {res['unique_companies_profiled']} companies")
        print("\nTop Trending ATS Keywords in 2026/2027:")
        for kw in res["top_trending_ats_skills"][:10]:
            print(f"  • {kw['keyword']} ({kw['category']}) - Count: {kw['occurrence_count']}")

    if args.scan:
        print(f"[APEX] Harvesting jobs across 16,500+ database and live feeds...")
        jobs = orchestrator.sentinel.harvester.harvest_all(limit_per_source=args.limit)
        print(f"Discovered {len(jobs)} active deduplicated jobs.")
        print("\nSample Active Openings:")
        for j in jobs[:5]:
            print(f"  • {j['title']} @ {j['company']} ({j['location']}) [{j['track']}]")

    if args.network:
        print(f"[APEX] Querying 9,223 LinkedIn network for {args.company}...")
        recruiters = orchestrator.network.find_recruiters_for_company(args.company, limit=5)
        for r in recruiters:
            print(f"  • {r['name']} — {r['title']} ({r['company']})")
            print(f"    Email: {r['email']} | Corridor: {r['corridor']}")
            print(f"    LinkedIn: {r['linkedin_url']}")

    if args.interview:
        print(f"[APEX] Generating STAR Interview Prep for {args.company} — {args.role}...")
        prep = orchestrator.interview.generate_interview_prep_pack(args.company, args.role)
        print(f"Company Culture: {prep['company_culture_dna']}")
        print("\nTailored STAR Responses:")
        for qa in prep["tailored_qa_bank"]:
            print(f"\n[Q]: {qa['question']}")
            print(f"  • S: {qa['recommended_star_framework']['situation']}")
            print(f"  • T: {qa['recommended_star_framework']['task']}")
            print(f"  • A: {qa['recommended_star_framework']['action']}")
            print(f"  • R: {qa['recommended_star_framework']['result']}")

    if args.comp:
        print(f"[APEX] Benchmarking Compensation for {args.track}...")
        b = orchestrator.compensation.benchmark_role_compensation(args.track)
        print(f"  25th Percentile: ₹{b['p25_lpa']} LPA")
        print(f"  Median (P50)   : ₹{b['median_p50_lpa']} LPA")
        print(f"  75th Percentile: ₹{b['p75_lpa']} LPA")
        print(f"  Aspirational   : ₹{b['p90_aspirational_lpa']} LPA")
        print(f"  Anchor Target  : ₹{b['recommended_opening_anchor_lpa']} LPA")

    if args.tailor:
        print(f"[APEX] Synthesizing ATS Resume & Cover Letter for {args.company} — {args.role}...")
        strike = orchestrator.execute_instant_strike_for_custom_role(
            company=args.company,
            title=args.role,
            description="High-velocity operations, vendor governance, and commercial execution.",
            track=args.track
        )
        print(f"ATS Match Score: {strike['ats_evaluation']['match_score_percent']}%")
        print("\n--- RESUME PREVIEW ---")
        print(strike["resume_markdown"][:600] + "\n...")

    if args.cockpit:
        telemetry = orchestrator.run_full_autonomous_cycle(limit_jobs=30)
        cockpit_file = generate_cockpit_html(telemetry)
        print(f"[APEX] Interactive Cockpit rendered to: {cockpit_file}")
        try:
            webbrowser.open(f"file:///{cockpit_file}")
        except Exception:
            pass

    if args.universal_cockpit:
        cockpit_path = Path(r"e:\anti\universal_job_cockpit.html")
        print(f"[APEX] Opening Universal Job & Skill Cockpit at: {cockpit_path}")
        try:
            webbrowser.open(f"file:///{cockpit_path}")
        except Exception:
            pass

    if args.dissect_jd:
        from universal_jd_intelligence_engine import UniversalJDIntelligenceEngine
        engine = UniversalJDIntelligenceEngine()
        jd_input = args.dissect_jd
        if Path(jd_input).exists():
            with open(jd_input, "r", encoding="utf-8") as fp:
                jd_text = fp.read()
        else:
            jd_text = jd_input

        res = engine.dissect_jd(jd_text, role_title=args.role, company=args.company)
        print("\n" + "=" * 80)
        print("  OMEGA UNIVERSAL JOB DESCRIPTION DISSECTION")
        print("=" * 80)
        print(f"Matched Role Archetype: {res['classification']['matched_archetype_title']} ({res['classification']['match_confidence_pct']}%)")
        print(f"Job Family            : {res['classification']['family_name']}")
        print(f"Seniority Level       : {res['classification']['seniority_tier']['name']} ({res['classification']['seniority_tier']['code']})")
        print(f"Work Modality         : {res['classification']['work_modality']}")
        print(f"ATS Match Score       : {res['ats_compatibility']['ats_score_pct']}% — {res['ats_compatibility']['fit_status']}")
        print(f"Extracted Hard Skills : {', '.join(res['skills_extracted']['hard_skills'])}")
        print(f"Extracted Soft Skills : {', '.join(res['skills_extracted']['soft_skills'])}")
        print(f"Missing Skill Gaps    : {', '.join(res['ats_compatibility']['missing_skills_gaps'])}")
        print("\n--- GOOGLE X-Y-Z TAILORED RESUME BULLETS ---")
        for b in res["tailored_resume_bullets_xyz"]:
            print(f"  • {b}")
        print("\n--- HIGH-YIELD STAR INTERVIEW QUESTION ---")
        if res["star_interview_defense"]:
            star = res["star_interview_defense"][0]
            print(f"  Q: {star['question']}")
            print(f"  Trap to avoid: {star.get('trap', 'N/A')}")
            print(f"  Model Defense:\n    {star.get('model_defense', 'N/A')}")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
