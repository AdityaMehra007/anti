#!/usr/bin/env python3
"""
OMEGA Free-For-Dev Universal CLI
================================
Autonomous Command-Line Interface for the ripienaar/free-for-dev catalog.
Supports instant search, service inspection, provider comparisons,
zero-dollar stack synthesis, architecture audits, and 12-phase sovereign lifecycle.

Usage:
  python free_for_dev_cli.py info
  python free_for_dev_cli.py categories
  python free_for_dev_cli.py search "postgres" --no-card
  python free_for_dev_cli.py service supabase
  python free_for_dev_cli.py compare supabase neon turso
  python free_for_dev_cli.py stack --archetype jamstack_saas
  python free_for_dev_cli.py audit --requirements "postgres,nextjs,auth,redis,sentry"
  python free_for_dev_cli.py no-card
  python free_for_dev_cli.py export --format json
  python free_for_dev_cli.py do-everything
"""

import sys
import argparse
import json
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from free_for_dev_orchestrator import FreeForDevOrchestrator


def print_banner():
    banner = r"""
  ___  __  __ _____ ____    _       _____ ____  _____ _____ 
 / _ \|  \/  | ____/ ___|  / \     |  ___|  _ \| ____| ____|
| | | | |\/| |  _|| |  _  / _ \    | |_  | |_) |  _| |  _|  
| |_| | |  | | |__| |_| |/ ___ \   |  _| |  _ <| |___| |___ 
 \___/|_|  |_|_____\____/_/   \_\  |_|   |_| \_\_____|_____|
   FREE-FOR-DEV AUTONOMOUS DEVELOPER CLOUD & ZERO-DOLLAR ARCHITECT
"""
    print(banner)


def cmd_info(args, orc: FreeForDevOrchestrator):
    telem = orc.get_telemetry()
    print_banner()
    print("=" * 70)
    print("  CATALOG TELEMETRY & SOVEREIGN STATUS")
    print("=" * 70)
    print(f"  Status                  : {telem['status']}")
    print(f"  Protocol                : {telem['protocol']}")
    print(f"  Upstream Source         : {telem['upstream_repository']}")
    print(f"  Total Indexed Services  : {telem['total_services']:,}")
    print(f"  Total Categories        : {telem['total_categories']}")
    print(f"  No-Credit-Card Services : {telem['no_credit_card_count']:,} ({telem['no_credit_card_percentage']}%)")
    print(f"  S-Tier Flagships        : {telem['s_tier_count']}")
    print(f"  A-Tier Generous Quotas  : {telem['a_tier_count']}")
    print(f"  Idle-Sleep Risk Count   : {telem['idle_sleep_risk_count']}")
    print(f"  Est. Monthly Value      : ${telem['total_monthly_commercial_value_usd']:,.2f}")
    print(f"  Est. Annual Value       : ${telem['total_annual_commercial_value_usd']:,.2f}")
    print(f"  SQLite Database         : {telem['indexed_database_path']}")
    print("-" * 70)
    print("  KEY ARCHITECTURAL ROLE COVERAGE:")
    for role, count in sorted(telem["role_distribution"].items(), key=lambda x: x[1], reverse=True)[:8]:
        print(f"    - {role:22}: {count:4} services")
    print("=" * 70)


def cmd_categories(args, orc: FreeForDevOrchestrator):
    cats = orc.list_categories()
    print(f"\n[*] 57 Capabilities Categories in Free-For-Dev ({len(orc.services)} Total Services):\n")
    print(f" {'ID / SLUG':<36} | {'CATEGORY NAME':<40} | {'SERVICES':>8}")
    print("-" * 90)
    for c in cats:
        print(f" {c['id']:<36} | {c['name']:<40} | {c['services_count']:>8}")
    print("-" * 90)


def cmd_search(args, orc: FreeForDevOrchestrator):
    results = orc.search_services(
        query=args.query or "",
        category=args.category or "",
        no_card_only=args.no_card,
        tier=args.tier or "",
        role=args.role or "",
        limit=args.limit
    )
    print(f"\n[+] Found {len(results)} services matching criteria:\n")
    print(f" {'TIER':<4} | {'NAME':<24} | {'NO-CC':<5} | {'CATEGORY':<28} | {'QUOTA SUMMARY'}")
    print("-" * 95)
    for s in results:
        cc_str = "YES" if not s["requires_credit_card"] else "NO"
        tier_str = f"[{s['tier_rating']}]"
        print(f" {tier_str:<4} | {s['name'][:24]:<24} | {cc_str:<5} | {s['category'][:28]:<28} | {s['quota_summary'][:40]}")
    print("-" * 95)


def cmd_service(args, orc: FreeForDevOrchestrator):
    srv = orc.get_service(args.service_id)
    if not srv:
        print(f"[-] Service not found: {args.service_id}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f"  SERVICE DOSSIER: {srv['name']} [{srv['tier_rating']}-Tier]")
    print("=" * 70)
    print(f"  Identifier          : {srv['id']}")
    print(f"  Official URL        : {srv['url']}")
    print(f"  Category            : {srv['category']} ({srv['category_slug']})")
    print(f"  Requires Credit Card: {'YES (Verification Required)' if srv['requires_credit_card'] else 'NO (Zero Financial Friction)'}")
    print(f"  Pauses on Inactivity: {'YES (Sleeps after idle period)' if srv['inactivity_sleep'] else 'NO (Always Active)'}")
    print(f"  Commercial Value    : ${srv['commercial_equivalent_usd']:.2f} / month")
    print(f"  Quota Highlights    : {srv['quota_summary']}")
    print(f"  Architectural Roles : {', '.join(srv['architectural_roles'])}")
    print(f"  Tags                : {', '.join(srv['tags'])}")
    print("-" * 70)
    print(f"  Raw Entry Description:\n  {srv['description']}")
    print("=" * 70 + "\n")


def cmd_compare(args, orc: FreeForDevOrchestrator):
    if not args.providers or len(args.providers) < 2:
        print("[-] Please provide at least 2 provider names or IDs to compare.")
        sys.exit(1)

    res = orc.compare_providers(args.providers)
    if "error" in res:
        print(f"[-] Error: {res['error']}")
        sys.exit(1)

    services = res["services"]
    print("\n" + "=" * 85)
    print(f"  OMEGA HEAD-TO-HEAD PROVIDER COMPARISON ({len(services)} Providers)")
    print("=" * 85)
    headers = [s["name"] for s in services]
    print(f"  {'METRIC':<24} | " + " | ".join(f"{h[:18]:<18}" for h in headers))
    print("-" * 85)

    def row(label, fn):
        vals = [fn(s) for s in services]
        print(f"  {label:<24} | " + " | ".join(f"{str(v)[:18]:<18}" for v in vals))

    row("Tier Grade", lambda s: f"[{s['tier_rating']}-Tier]")
    row("Category", lambda s: s["category"][:18])
    row("Credit Card Free", lambda s: "YES (No CC)" if not s["requires_credit_card"] else "NO (Card Req)")
    row("Inactivity Sleep", lambda s: "YES (Sleeps)" if s["inactivity_sleep"] else "NO (Active)")
    row("Storage Quota", lambda s: f"{s['storage_mb']} MB" if s["storage_mb"] else "Unmetered/N/A")
    row("Bandwidth Quota", lambda s: f"{s['bandwidth_gb']} GB" if s["bandwidth_gb"] else "Standard Tier")
    row("Commercial Equiv", lambda s: f"${s['commercial_equivalent_usd']:.2f}/mo")

    print("-" * 85)
    print(f"  AI SYNTHESIS RECOMMENDATION:\n  >>> {res['recommendation']}")
    print("=" * 85 + "\n")


def cmd_stack(args, orc: FreeForDevOrchestrator):
    stack = orc.architect_zero_dollar_stack(args.archetype or "jamstack_saas")
    print("\n" + "=" * 75)
    print(f"  OMEGA ZERO-DOLLAR STACK ARCHITECT: {stack['name']}")
    print("=" * 75)
    print(f"  Use Case                : {stack['target_use_case']}")
    print(f"  Total Cost              : $0.00 / month (100% Free Developer Tier)")
    print(f"  Commercial Value Equiv  : ${stack['estimated_commercial_monthly_value_usd']:,.2f} / month")
    print(f"  Annual Cash Saved       : ${stack['estimated_annual_savings_usd']:,.2f} / year")
    print(f"  Credit Card Required    : {'NO (Zero Cards Required)' if stack['all_credit_card_free'] else 'Minor verification required'}")
    print(f"  Combined Quotas         : {stack['combined_quotas']['storage_readable']}, {stack['combined_quotas']['bandwidth_readable']}, {stack['combined_quotas']['requests_readable']}")
    print("-" * 75)
    print("  ARCHITECTURE TOPOLOGY:")
    print(stack["architecture_blueprint"])
    print("-" * 75)
    print("  CURATED PROVIDER LINEUP:")
    for s in stack["services"]:
        cc = "⚡ No CC" if not s["requires_credit_card"] else "💳 Card Req"
        inact = " | ⚠️ Sleep on idle" if s["inactivity_sleep"] else ""
        print(f"    - [{s['role'].upper()}]: {s['name']} ({cc}{inact})")
        print(f"      Link: {s['url']}")
        print(f"      Limit: {s['quota_summary']}")
    print("=" * 75 + "\n")


def cmd_audit(args, orc: FreeForDevOrchestrator):
    if not args.requirements:
        print("[-] Please provide requirements via --requirements (e.g., 'postgres,nextjs,auth,redis')")
        sys.exit(1)

    req_list = [r.strip() for r in args.requirements.split(",") if r.strip()]
    audit = orc.audit_architecture(req_list)
    print("\n" + "=" * 75)
    print(f"  OMEGA ARCHITECTURE ZERO-DOLLAR FEASIBILITY AUDIT")
    print("=" * 75)
    print(f"  Verdict                 : {audit['verdict']}")
    print(f"  Requirements Analyzed   : {audit['total_requirements_analyzed']}")
    print(f"  Coverage                : {audit['coverage_percentage']}% ({audit['covered_requirements_count']} covered)")
    print(f"  Commercial Equiv Value  : ${audit['estimated_commercial_monthly_value_usd']:,.2f}/mo (${audit['estimated_annual_savings_usd']:,.2f}/yr)")
    print("-" * 75)
    print("  MAPPING BREAKDOWN:")
    for m in audit["matched_providers"]:
        cc = "⚡ No CC" if not m["requires_credit_card"] else "💳 Card Req"
        print(f"    * {m['requirement']:<18} -> {m['recommended_service']:<20} ({cc}) [{m['quota']}]")
    if audit["unmatched_requirements"]:
        print("\n  UNMATCHED REQUIREMENTS:")
        for u in audit["unmatched_requirements"]:
            print(f"    ! {u} (Consider self-hosted open source alternative)")
    if audit["quota_and_operational_warnings"]:
        print("\n  OPERATIONAL NOTICES & SLEEP WARNINGS:")
        for w in audit["quota_and_operational_warnings"]:
            print(f"    ▲ {w}")
    print("=" * 75 + "\n")


def cmd_no_card(args, orc: FreeForDevOrchestrator):
    results = orc.search_services(no_card_only=True, limit=args.limit or 25)
    print(f"\n[+] Curated 100% Zero-Credit-Card Developer Offerings (Top {len(results)} of 1,384):\n")
    print(f" {'TIER':<4} | {'NAME':<24} | {'CATEGORY':<30} | {'QUOTA HIGHLIGHTS'}")
    print("-" * 90)
    for s in results:
        print(f" [{s['tier_rating']}]  | {s['name'][:24]:<24} | {s['category'][:30]:<30} | {s['quota_summary'][:35]}")
    print("-" * 90)


def cmd_export(args, orc: FreeForDevOrchestrator):
    fmt = args.format or "json"
    out = orc.export_catalog(fmt, Path(args.output) if args.output else None)
    print(f"[+] Successfully exported catalog in {fmt.upper()} format to: {out} ({out.stat().st_size:,} bytes)")


def cmd_do_everything(args, orc: FreeForDevOrchestrator):
    print("\n" + "=" * 75)
    print("  EXECUTING OMEGA 12-PHASE SOVEREIGN LIFECYCLE (FREE-FOR-DEV)")
    print("=" * 75)
    out_path = Path(args.manifest_out) if args.manifest_out else None
    res = orc.execute_sovereign_lifecycle(manifest_out=out_path)
    for p in res["phases"]:
        status_symbol = "✔" if p["status"] == "PASSED" else "✖"
        print(f"  [{status_symbol}] Phase {p['phase']:2}: {p['name']:<58} ({p['elapsed_seconds']}s)")
    print("-" * 75)
    print(f"  Total Phases   : {res['total_phases_executed']}")
    print(f"  Total Elapsed  : {res['total_elapsed_seconds']} seconds")
    print(f"  Overall Status : {res['overall_status']}")
    print(f"  Manifest Saved : {out_path or 'omega/data/free_for_dev_do_everything_manifest.json'}")
    print("=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(description="OMEGA Free-For-Dev Developer Cloud CLI")
    subparsers = parser.add_subparsers(dest="command")

    # info
    subparsers.add_parser("info", help="Display system telemetry and statistics")

    # categories
    subparsers.add_parser("categories", help="List all 57 capability categories")

    # search
    p_search = subparsers.add_parser("search", help="Search developer services")
    p_search.add_argument("query", nargs="?", default="", help="Search query")
    p_search.add_argument("--category", "-c", help="Filter by category slug or name")
    p_search.add_argument("--no-card", action="store_true", help="Only show services with NO credit card required")
    p_search.add_argument("--tier", "-t", choices=["S", "A", "B", "C"], help="Filter by tier rating")
    p_search.add_argument("--role", "-r", help="Filter by architectural role")
    p_search.add_argument("--limit", "-l", type=int, default=25, help="Max results to return")

    # service
    p_srv = subparsers.add_parser("service", help="Inspect a specific service")
    p_srv.add_argument("service_id", help="Service slug, ID, or name")

    # compare
    p_comp = subparsers.add_parser("compare", help="Compare 2 to 5 providers side-by-side")
    p_comp.add_argument("providers", nargs="+", help="Provider names or IDs to compare")

    # stack
    p_stack = subparsers.add_parser("stack", help="Synthesize a zero-dollar production architecture stack")
    p_stack.add_argument("--archetype", "-a", choices=[
        "jamstack_saas", "ai_agent_platform", "mobile_app_backend",
        "microservices_api", "ecommerce_store", "sovereign_no_card", "analytics_data_pipeline"
    ], default="jamstack_saas", help="Architecture archetype")

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit project requirements against free tiers")
    p_audit.add_argument("--requirements", "-r", required=True, help="Comma-separated requirements (e.g. 'postgres,nextjs,auth,redis')")

    # no-card
    p_nocard = subparsers.add_parser("no-card", help="List top zero-credit-card offerings")
    p_nocard.add_argument("--limit", "-l", type=int, default=25, help="Max items to list")

    # export
    p_exp = subparsers.add_parser("export", help="Export catalog in JSON, CSV, or Markdown")
    p_exp.add_argument("--format", "-f", choices=["json", "csv", "markdown"], default="json", help="Export format")
    p_exp.add_argument("--output", "-o", help="Target output file path")

    # do-everything
    p_do = subparsers.add_parser("do-everything", help="Execute 12-phase sovereign lifecycle")
    p_do.add_argument("--manifest-out", help="Custom manifest output path")

    args = parser.parse_args()

    orc = FreeForDevOrchestrator(auto_ingest=True)

    if args.command == "info" or not args.command:
        cmd_info(args, orc)
    elif args.command == "categories":
        cmd_categories(args, orc)
    elif args.command == "search":
        cmd_search(args, orc)
    elif args.command == "service":
        cmd_service(args, orc)
    elif args.command == "compare":
        cmd_compare(args, orc)
    elif args.command == "stack":
        cmd_stack(args, orc)
    elif args.command == "audit":
        cmd_audit(args, orc)
    elif args.command == "no-card":
        cmd_no_card(args, orc)
    elif args.command == "export":
        cmd_export(args, orc)
    elif args.command == "do-everything":
        cmd_do_everything(args, orc)


if __name__ == "__main__":
    main()
