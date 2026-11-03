"""
OMEGA GitHub Marketplace Universal CLI
======================================
Command-line interface for exploring, searching, synthesizing workflows,
auditing security, and orchestrating GitHub Actions and Apps from github.com/marketplace.

Supreme Constitution: OMEGA_CONSTITUTION.md
Operational Mode: Version OMNI-X / Production Engineering Mode
"""

import sys
import os

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import argparse
import json
from pathlib import Path
from github_marketplace_orchestrator import (
    engine,
    WorkflowSynthesizer,
    WorkflowSecurityAuditor,
    SQLITE_DB_PATH,
    MANIFEST_JSON_PATH,
    MARKETPLACE_JSON_PATH
)


def cmd_info(args):
    print("=" * 76)
    print("  OMEGA GITHUB MARKETPLACE :: SOVEREIGN ORCHESTRATION TELEMETRY")
    print("=" * 76)
    total_items = len(engine.items)
    actions_count = sum(1 for it in engine.items.values() if it.type == "action")
    apps_count = sum(1 for it in engine.items.values() if it.type == "app")
    verified_count = sum(1 for it in engine.items.values() if it.verified_creator)
    s_tier = sum(1 for it in engine.items.values() if it.tier == "S")
    avg_score = round(sum(it.security_score for it in engine.items.values()) / max(1, total_items), 1)

    print(f"  Total Catalog Items:      {total_items}")
    print(f"  GitHub Actions:           {actions_count}")
    print(f"  GitHub Apps:              {apps_count}")
    print(f"  Verified Creators:        {verified_count}")
    print(f"  S-Tier Flagships:         {s_tier}")
    print(f"  Average Security Score:   {avg_score}/100")
    print(f"  Official Categories:      {len(engine.categories)}")
    print(f"  SQLite FTS5 DB:           {SQLITE_DB_PATH}")
    print(f"  Sovereign Manifest:       {MANIFEST_JSON_PATH}")
    print("-" * 76)
    print("  Top 5 Categories by Density:")
    top_cats = sorted(engine.categories.values(), key=lambda x: x.get("item_count", 0), reverse=True)[:5]
    for c in top_cats:
        print(f"   * {c['name']:<30} [{c.get('item_count', 0):>2} items | {c.get('action_count', 0)} actions, {c.get('app_count', 0)} apps]")
    print("=" * 76)


def cmd_categories(args):
    print("=" * 76)
    print(f"  GITHUB MARKETPLACE OFFICIAL CATEGORIES ({len(engine.categories)})")
    print("=" * 76)
    print(f"  {'Category Name':<28} {'Slug':<24} {'Actions':<8} {'Apps':<8} {'Total':<6}")
    print("-" * 76)
    for c in sorted(engine.categories.values(), key=lambda x: x["name"]):
        print(f"  {c['name']:<28} {c['slug']:<24} {c.get('action_count', 0):<8} {c.get('app_count', 0):<8} {c.get('item_count', 0):<6}")
    print("=" * 76)


def cmd_search(args):
    query = " ".join(args.query) if isinstance(args.query, list) else args.query
    results = engine.search(
        query=query,
        category=args.category,
        item_type=args.type,
        verified_only=args.verified,
        limit=args.limit
    )
    print("=" * 76)
    print(f"  SEARCH RESULTS: '{query}' (Found {len(results)} items)")
    print("=" * 76)
    if not results:
        print("  No items matched your query criteria.")
        print("=" * 76)
        return

    print(f"  {'Type':<8} {'Name':<32} {'Category':<22} {'Stars':<8} {'Rating'}")
    print("-" * 76)
    for r in results:
        v_mark = "✓ " if r["verified_creator"] else "  "
        print(f"  [{r['type'].upper():<6}] {v_mark}{r['name'][:30]:<30} {r['category'][:20]:<22} {r['stars']:<8} {r['rating']}★")
    print("=" * 76)


def cmd_get(args):
    item = engine.get_item(args.slug)
    if not item:
        print(f"[!] Item not found: {args.slug}")
        return

    print("=" * 76)
    print(f"  {item['name']} ({item['type'].upper()})")
    print("=" * 76)
    print(f"  Repository:          {item['repo']}")
    print(f"  Category:            {item['category']}")
    print(f"  Author:              {item['author']} {'(Verified Creator)' if item['verified_creator'] else ''}")
    print(f"  Stars:               {item['stars']:,} | Rating: {item['rating']}★ | Installs: {item['installs']:,}")
    print(f"  Tier:                {item['tier']} | Pricing: {item['pricing_model']}")
    print(f"  Security Score:      {item['security_score']}/100 | SLSA Level: {item['slsa_level']}")
    print(f"  Recommended Version: {item['recommended_version']}")
    if item['recommended_sha']:
        print(f"  Recommended SHA:     {item['recommended_sha']}")
    print(f"  Supported Runners:   {', '.join(item['supported_runners'])}")
    print(f"  Permissions:         {', '.join(item['permissions_required'])}")
    print("-" * 76)
    print(f"  Description:\n    {item['description']}")
    print("=" * 76)


def cmd_actions(args):
    actions = [it for it in engine.items.values() if it.type == "action"]
    actions = sorted(actions, key=lambda x: x.stars, reverse=True)[:args.limit]
    print("=" * 76)
    print(f"  TOP GITHUB ACTIONS (Sorted by Stars)")
    print("=" * 76)
    print(f"  {'Action Name':<32} {'Category':<22} {'Author':<12} {'Stars':<8}")
    print("-" * 76)
    for a in actions:
        print(f"  {a.name[:30]:<32} {a.category[:20]:<22} {a.author[:10]:<12} {a.stars:<8,}")
    print("=" * 76)


def cmd_apps(args):
    apps = [it for it in engine.items.values() if it.type == "app"]
    apps = sorted(apps, key=lambda x: x.stars, reverse=True)[:args.limit]
    print("=" * 76)
    print(f"  TOP GITHUB APPS (Sorted by Stars)")
    print("=" * 76)
    print(f"  {'App Name':<32} {'Category':<22} {'Author':<12} {'Stars':<8}")
    print("-" * 76)
    for a in apps:
        print(f"  {a.name[:30]:<32} {a.category[:20]:<22} {a.author[:10]:<12} {a.stars:<8,}")
    print("=" * 76)


def cmd_generate_workflow(args):
    workflow_yaml = WorkflowSynthesizer.synthesize(
        stack=args.stack,
        options={
            "pin_sha": not args.no_pin_sha,
            "security_scan": not args.no_security,
            "cache": not args.no_cache
        }
    )
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(workflow_yaml)
        print(f"[OK] Workflow written to: {out_path}")
    else:
        print("=" * 76)
        print(f"  SYNTHESIZED GITHUB ACTIONS WORKFLOW: {args.stack.upper()}")
        print("=" * 76)
        print(workflow_yaml)
        print("=" * 76)


def cmd_audit_workflow(args):
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[!] File not found: {file_path}")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("[!] Error: specify --file <workflow.yml> or pipe content via stdin.")
        return

    result = WorkflowSecurityAuditor.audit_yaml(content)
    print("=" * 76)
    print(f"  WORKFLOW SECURITY AUDIT RESULTS")
    print("=" * 76)
    print(f"  Overall Security Score:  {result['security_score']}/100")
    print(f"  Risk Level:              {result['risk_level']}")
    print(f"  Policy Compliant:        {'YES (PASSED)' if result['is_compliant'] else 'NO (VIOLATIONS DETECTED)'}")
    print(f"  Total Findings:          {result['findings_count']}")
    print("-" * 76)
    if not result["findings"]:
        print("  [✓] Zero security findings. Workflow conforms to least privilege and SHA pinning.")
    else:
        for idx, f in enumerate(result["findings"], 1):
            print(f"  {idx}. [{f['severity']}] {f['rule']} (-{f['penalty']} pts)")
            print(f"     {f['message']}")
    print("=" * 76)


def cmd_export(args):
    engine.export_all()
    print("[OK] Exported all catalog datasets into data/ (JSON, SQLite, CSV, MD, Graph).")


def cmd_do_everything(args):
    print("Executing 12-Phase Sovereign Lifecycle for GitHub Marketplace...")
    res = engine.do_everything()
    print("=" * 76)
    print(f"  {res['overall_status']}")
    print("=" * 76)
    print(f"  Execution ID:       {res['execution_id']}")
    print(f"  Phases Passed:      {res['total_phases_executed']}/{res['total_phases']}")
    print(f"  Total Duration:     {res['total_elapsed_seconds']}s")
    print(f"  Manifest Path:      {MANIFEST_JSON_PATH}")
    print("=" * 76)


def cmd_serve(args):
    import github_marketplace_api_server
    github_marketplace_api_server.run_server(port=args.port)


def main():
    parser = argparse.ArgumentParser(
        description="OMEGA GitHub Marketplace Sovereign CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # info
    subparsers.add_parser("info", help="Display ecosystem telemetry")

    # categories
    subparsers.add_parser("categories", help="List all official categories")

    # search
    search_p = subparsers.add_parser("search", help="Search Actions and Apps")
    search_p.add_argument("query", nargs="+", help="Search terms")
    search_p.add_argument("--category", "-c", help="Filter by category slug")
    search_p.add_argument("--type", "-t", choices=["action", "app"], help="Filter by item type")
    search_p.add_argument("--verified", "-v", action="store_true", help="Only verified creators")
    search_p.add_argument("--limit", "-n", type=int, default=20, help="Max results")

    # get
    get_p = subparsers.add_parser("get", help="Inspect a specific Action or App")
    get_p.add_argument("slug", help="Item id, slug, or repo")

    # actions
    act_p = subparsers.add_parser("actions", help="List top GitHub Actions")
    act_p.add_argument("--limit", "-n", type=int, default=25, help="Number of items to show")

    # apps
    app_p = subparsers.add_parser("apps", help="List top GitHub Apps")
    app_p.add_argument("--limit", "-n", type=int, default=25, help="Number of items to show")

    # generate-workflow
    gen_p = subparsers.add_parser("generate-workflow", help="Synthesize a production GitHub Actions YAML pipeline")
    gen_p.add_argument("--stack", "-s", default="python", choices=["python", "node", "docker", "universal"], help="Target stack")
    gen_p.add_argument("--no-pin-sha", action="store_true", help="Do not pin actions to commit SHAs")
    gen_p.add_argument("--no-security", action="store_true", help="Omit security scanner jobs")
    gen_p.add_argument("--no-cache", action="store_true", help="Omit package dependency caching")
    gen_p.add_argument("--out", "-o", help="Write YAML to file")

    # audit-workflow
    audit_p = subparsers.add_parser("audit-workflow", help="Audit a GitHub Actions YAML workflow for security vulnerabilities")
    audit_p.add_argument("--file", "-f", help="Path to workflow file")

    # export
    subparsers.add_parser("export", help="Export catalog datasets")

    # do-everything
    subparsers.add_parser("do-everything", help="Execute 12-phase sovereign lifecycle")

    # serve
    serve_p = subparsers.add_parser("serve", help="Start REST API server and Cockpit")
    serve_p.add_argument("--port", "-p", type=int, default=8783, help="Port to listen on (default: 8783)")

    args = parser.parse_args()

    if not args.command:
        cmd_info(args)
        return

    commands = {
        "info": cmd_info,
        "categories": cmd_categories,
        "search": cmd_search,
        "get": cmd_get,
        "actions": cmd_actions,
        "apps": cmd_apps,
        "generate-workflow": cmd_generate_workflow,
        "audit-workflow": cmd_audit_workflow,
        "export": cmd_export,
        "do-everything": cmd_do_everything,
        "serve": cmd_serve
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
