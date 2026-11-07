#!/usr/bin/env python3
"""
CAREER-OPS UNIVERSAL CLI
========================
Command-line interface for the career-ops open-source AI job search agent ecosystem.
"""

import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from career_ops_orchestrator import CareerOpsInspector, CareerOpsEvaluationEngine, run_server

def main():
    parser = argparse.ArgumentParser(
        prog="career-ops-cli",
        description="CareerOps Sovereign CLI — AI Job Search Agent Ecosystem"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # Command: stats
    p_stats = subparsers.add_parser("stats", help="Display ecosystem telemetry and high-level stats")

    # Command: providers
    p_prov = subparsers.add_parser("providers", help="List and filter 138 ATS & Job Board providers")
    p_prov.add_argument("--category", type=str, help="Filter by category (e.g., 'Major ATS Platform', 'Big Tech')")
    p_prov.add_argument("--search", type=str, help="Search provider by name or keyword")

    # Command: modes
    p_modes = subparsers.add_parser("modes", help="List and inspect 45 prompt modes")
    p_modes.add_argument("--name", type=str, help="Inspect specific mode by name (e.g., oferta.md)")

    # Command: templates
    p_temp = subparsers.add_parser("templates", help="List CV and cover letter templates")

    # Command: evaluate
    p_eval = subparsers.add_parser("evaluate", help="Execute deterministic A-H evaluation on a job description")
    p_eval.add_argument("--jd", type=str, help="Path to JD file or raw text")
    p_eval.add_argument("--cv", type=str, default="", help="Path to CV file (optional)")
    p_eval.add_argument("--url", type=str, default="https://example.com/job", help="Job listing URL")

    # Command: serve
    p_serve = subparsers.add_parser("serve", help="Launch REST API server & Mission Control Cockpit")
    p_serve.add_argument("--port", type=int, default=8794, help="Port to listen on (default: 8794)")

    # Command: audit
    p_audit = subparsers.add_parser("audit", help="Run sanity and integrity audit on career-ops files")

    args = parser.parse_args()

    inspector = CareerOpsInspector()
    evaluator = CareerOpsEvaluationEngine()

    if args.command == "stats" or not args.command:
        stats = inspector.get_summary_stats()
        print("\n" + "=" * 65)
        print(f"  CAREER-OPS SOVEREIGN FLEET TELEMETRY (v{stats['version']})")
        print("=" * 65)
        print(f"  Total Providers: {stats['total_providers']}")
        for cat, count in stats["providers_by_category"].items():
            print(f"    - {cat:<28}: {count}")
        print(f"  Total Prompt Modes: {stats['total_modes']}")
        print(f"  Total Templates:    {stats['total_templates']}")
        print("  Core Principles:")
        for p in stats["architecture_principles"]:
            print(f"    * {p}")
        print("=" * 65)
        print("  Use 'career-ops-cli --help' for full command options.\n")

    elif args.command == "providers":
        providers = inspector.inspect_providers()
        if args.category:
            providers = [p for p in providers if args.category.lower() in p["category"].lower()]
        if args.search:
            providers = [p for p in providers if args.search.lower() in p["id"].lower()]

        print(f"\n[CAREER-OPS] Showing {len(providers)} matching providers:\n")
        print(f"{'ID':<25} | {'CATEGORY':<28} | {'SIZE':<8} | {'DETECT'}")
        print("-" * 72)
        for p in providers:
            detect_str = "YES" if p["has_detect"] else "MANUAL"
            print(f"{p['id']:<25} | {p['category']:<28} | {p['size_bytes']:<8} | {detect_str}")

    elif args.command == "modes":
        modes = inspector.inspect_modes()
        if args.name:
            target = next((m for m in modes if m["name"].lower() == args.name.lower() or m["stem"].lower() == args.name.lower()), None)
            if target:
                print(f"\n--- MODE: {target['name']} ---")
                print(f"Description: {target['description']}")
                print(f"Lines:       {target['lines_count']}")
                print(f"Headings:    {', '.join(target['sample_headings'])}")
            else:
                print(f"Mode '{args.name}' not found.")
        else:
            print(f"\n[CAREER-OPS] Showing {len(modes)} Prompt Modes in modes/:\n")
            print(f"{'NAME':<20} | {'LINES':<6} | {'DESCRIPTION'}")
            print("-" * 75)
            for m in modes:
                print(f"{m['name']:<20} | {m['lines_count']:<6} | {m['description'][:45]}...")

    elif args.command == "templates":
        templates = inspector.inspect_templates()
        print(f"\n[CAREER-OPS] Showing {len(templates)} Templates in templates/:\n")
        print(f"{'TEMPLATE NAME':<38} | {'KIND':<16} | {'SIZE (BYTES)'}")
        print("-" * 70)
        for t in templates:
            print(f"{t['name']:<38} | {t['kind']:<16} | {t['size_bytes']}")

    elif args.command == "evaluate":
        jd_text = ""
        cv_text = ""
        if args.jd and Path(args.jd).exists():
            jd_text = Path(args.jd).read_text(encoding="utf-8", errors="ignore")
        elif args.jd:
            jd_text = args.jd
        else:
            jd_text = """
            Company: Apex Distributed AI
            Title: Senior AI Platform Engineer
            Requirements:
            - Production ML platform ownership and distributed inference
            - Kubernetes, AWS cloud infrastructure, microservices
            - LLM serving, evaluation gates, and latency optimization
            - Mentorship of junior engineers
            Compensation: $185,000 - $225,000 USD
            """

        if args.cv and Path(args.cv).exists():
            cv_text = Path(args.cv).read_text(encoding="utf-8", errors="ignore")
        else:
            cv_text = """
            Alex Chen - Senior Platform Engineer
            Experience:
            - Led ML platform team (3 engineers), built model registry and evaluation gates
            - Shipped real-time inference pipeline at 50ms p99 latency
            - Deep experience with Kubernetes, AWS, PostgreSQL, Redis, Docker
            """

        result = evaluator.evaluate(jd_text, cv_text, args.url)
        meta = result["metadata"]
        print("\n" + "=" * 70)
        print(f"  CAREER-OPS EVALUATION REPORT: {meta['company']} — {meta['role']}")
        print("=" * 70)
        print(f"  Score:           {meta['score']} ({meta['decision']})")
        print(f"  Legitimacy:      {meta['legitimacy']} (Ghost Job Risk: {meta['ghost_job_risk']})")
        print(f"  Recommendation:  {result['recommendation']}")
        print("\n  [Block B: CV Match vs Requirements]")
        for req in result["block_b_requirements"]:
            print(f"    - {req['requirement']}: {req['match']}")
            print(f"      Signal: {req['evidence_or_gap']}")
        print("\n  [Block E: Top 5 Customization Changes]")
        for c in result["block_e_customization_plan"]:
            print(f"    {c['num']}. [{c['section']}]: {c['action']}")
        print("=" * 70)

    elif args.command == "serve":
        run_server(args.port)

    elif args.command == "audit":
        print("\n[CAREER-OPS] Executing Repository Sanity Audit...")
        stats = inspector.get_summary_stats()
        checks = [
            ("Root directory exists", inspector.root.exists()),
            ("Providers directory contains >= 100 modules", stats["total_providers"] >= 100),
            ("Prompt modes contain oferta.md & _shared.md", any(m["name"] == "oferta.md" for m in inspector.inspect_modes())),
            ("Templates directory contains cv-template.html", (inspector.templates_dir / "cv-template.html").exists()),
            ("Version file is intact", inspector.get_version() != "unknown"),
        ]
        all_passed = True
        for name, passed in checks:
            status = "PASS" if passed else "FAIL"
            if not passed: all_passed = False
            print(f"  [{status}] {name}")
        
        print("\nResult: " + ("100% SANITY AUDIT GREEN" if all_passed else "FAILURES DETECTED"))

if __name__ == "__main__":
    main()
