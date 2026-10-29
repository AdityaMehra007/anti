#!/usr/bin/env python3
"""
Windmill Universal CLI
======================
Command-Line Interface for Windmill Developer Platform, Workflow DAGs, and Script Runners.
Usage:
    python windmill_cli.py info
    python windmill_cli.py workspaces
    python windmill_cli.py scripts
    python windmill_cli.py flows
    python windmill_cli.py apps
    python windmill_cli.py resources
    python windmill_cli.py jobs [--status STATUS] [--limit N]
    python windmill_cli.py run-script <path> [--args JSON]
    python windmill_cli.py run-flow <path> [--args JSON]
    python windmill_cli.py approve-job <job_id> [--reject] [--notes NOTES]
    python windmill_cli.py hub [--search KEYWORD] [--category CAT]
    python windmill_cli.py hub-import <hub_id>
"""

import sys
import json
import argparse
from windmill_orchestrator import WindmillClient, WindmillOrchestrator, WindmillConfig


def print_banner():
    banner = r"""
 __      ___           _           _ _ _ 
 \ \    / (_)         | |         (_) | |
  \ \  / / _ _ __   __| |_ __ ___  _| | |
   \ \/ / | | '_ \ / _` | '_ ` _ \| | | |
    \  /  | | | | | (_| | | | | | | | | |
     \/   |_|_| |_|\__,_|_| |_| |_|_|_|_|
   Windmill Autonomous Workflow Engine & Developer Platform
"""
    print(banner)


def cmd_info(client: WindmillClient, args):
    telemetry = client.get_telemetry()
    print("=" * 65)
    print(" WINDMILL PLATFORM & WORKER TELEMETRY")
    print("=" * 65)
    print(f" Platform Version:     v{telemetry.get('version')}")
    print(f" Rust Engine Core:     {telemetry.get('rust_engine_version')}")
    print(f" Operating Mode:       {telemetry.get('mode', 'SIMULATION')}")
    print(f" Active Workspace:     {telemetry.get('current_workspace')}")
    print(f" Concurrency Limit:    {telemetry.get('max_concurrency')} concurrent jobs")
    print(f" Active Worker Nodes:  {telemetry.get('active_workers')} nodes (Rust Native & Docker)")
    print(f" Registered Scripts:   {telemetry.get('scripts_count')} scripts")
    print(f" Composed Flows/DAGs:  {telemetry.get('flows_count')} flows")
    print(f" Low-Code Apps:        {telemetry.get('apps_count')} apps")
    print(f" Executed Jobs:        {telemetry.get('total_jobs_executed')} ({telemetry.get('completed_jobs')} completed)")
    print(f" Suspended Approvals:  {telemetry.get('suspended_jobs')} awaiting human sign-off")
    print(f" Avg Execution Latency:{telemetry.get('average_execution_latency_ms')} ms")
    print("=" * 65)


def cmd_workspaces(client: WindmillClient, args):
    workspaces = client.list_workspaces()
    print("\n" + "=" * 70)
    print(f"{'WORKSPACE ID':<16} | {'NAME':<32} | {'TIER':<12} | {'OWNER'}")
    print("-" * 70)
    for w in workspaces:
        print(f"{w.get('id'):<16} | {w.get('name')[:32]:<32} | {w.get('tier', 'COMMUNITY'):<12} | {w.get('owner', 'admin')}")
    print("=" * 70 + "\n")


def cmd_scripts(client: WindmillClient, args):
    scripts = client.list_scripts()
    print("\n" + "=" * 80)
    print(f"{'PATH':<36} | {'LANG':<12} | {'SUMMARY'}")
    print("-" * 80)
    for s in scripts:
        print(f"{s.get('path'):<36} | {s.get('language'):<12} | {s.get('summary', 'N/A')[:28]}")
    print("=" * 80 + "\n")


def cmd_flows(client: WindmillClient, args):
    flows = client.list_flows()
    print("\n" + "=" * 80)
    print(f"{'FLOW PATH':<44} | {'STEPS':<7} | {'SUMMARY'}")
    print("-" * 80)
    for f in flows:
        steps_len = f.get("step_count", len(f.get("steps", [])))
        print(f"{f.get('path'):<44} | {steps_len:<7} | {f.get('summary', 'N/A')[:25]}")
    print("=" * 80 + "\n")


def cmd_apps(client: WindmillClient, args):
    apps = client.list_apps()
    print("\n" + "=" * 75)
    print(f"{'APP PATH':<40} | {'VERSION':<8} | {'SUMMARY'}")
    print("-" * 75)
    for a in apps:
        print(f"{a.get('path'):<40} | v{a.get('version', 1):<7} | {a.get('summary', 'N/A')[:22]}")
    print("=" * 75 + "\n")


def cmd_resources(client: WindmillClient, args):
    res = client.list_resources()
    print("\n" + "=" * 75)
    print(f"{'RESOURCE PATH':<34} | {'TYPE':<14} | {'ENCRYPTED':<10} | {'DESCRIPTION'}")
    print("-" * 75)
    for r in res:
        enc = "YES (AES)" if r.get("is_secret") else "NO"
        print(f"{r.get('path'):<34} | {r.get('resource_type'):<14} | {enc:<10} | {r.get('description', '')[:20]}")
    print("=" * 75 + "\n")


def cmd_jobs(client: WindmillClient, args):
    jobs = client.list_jobs(limit=args.limit, status=args.status)
    print("\n" + "=" * 80)
    print(f"{'JOB ID':<18} | {'TYPE':<7} | {'STATUS':<12} | {'DURATION':<10} | {'PATH'}")
    print("-" * 80)
    for j in jobs:
        dur = f"{j.get('duration_ms', 0)}ms"
        print(f"{j.get('id'):<18} | {j.get('type'):<7} | {j.get('status'):<12} | {dur:<10} | {j.get('path')}")
    print("=" * 80 + "\n")


def cmd_run_script(client: WindmillClient, args):
    payload = {}
    if args.args:
        try:
            payload = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(f"[!] Invalid JSON args: {e}")
            sys.exit(1)
    
    print(f"[*] Dispatching script: {args.path}")
    res = client.run_script(args.path, payload)
    print("\n[+] Execution Output:")
    print(json.dumps(res, indent=2))


def cmd_run_flow(client: WindmillClient, args):
    payload = {}
    if args.args:
        try:
            payload = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(f"[!] Invalid JSON args: {e}")
            sys.exit(1)
            
    print(f"[*] Executing Flow DAG: {args.path}")
    res = client.execute_flow(args.path, payload)
    print("\n[+] Flow Execution Result:")
    print(json.dumps(res, indent=2))


def cmd_approve_job(client: WindmillClient, args):
    is_approved = not args.reject
    verdict_text = "APPROVING" if is_approved else "REJECTING"
    print(f"[*] {verdict_text} suspended job {args.job_id}...")
    res = client.approve_job(args.job_id, approved=is_approved, notes=args.notes)
    print(json.dumps(res, indent=2))


def cmd_hub(client: WindmillClient, args):
    items = client.search_hub(query=args.search or "", category=args.category or "")
    print("\n" + "=" * 85)
    print(f"{'HUB ID':<34} | {'NAME':<28} | {'CATEGORY':<14} | {'STARS'}")
    print("-" * 85)
    for i in items:
        stars = f"{i.get('stars', 0)} stars"
        print(f"{i.get('id'):<34} | {i.get('name')[:28]:<28} | {i.get('category', 'General')[:14]:<14} | {stars}")
    print("=" * 85 + "\n")


def cmd_hub_import(client: WindmillClient, args):
    print(f"[*] Importing template '{args.hub_id}' into local workspace...")
    res = client.import_from_hub(args.hub_id)
    print(json.dumps(res, indent=2))


def cmd_schedules(client: WindmillClient, args):
    schedules = client.list_schedules()
    print("\n" + "=" * 95)
    print(f"{'SCHEDULE PATH':<40} | {'CRON':<12} | {'TYPE':<6} | {'TIMEZONE':<14} | {'SUMMARY'}")
    print("-" * 95)
    for s in schedules:
        stype = "Flow" if s.get("is_flow") else "Script"
        print(f"{s.get('path'):<40} | {s.get('schedule'):<12} | {stype:<6} | {s.get('timezone', 'UTC')[:14]:<14} | {s.get('summary', '')[:20]}")
    print("=" * 95 + "\n")


def cmd_trigger_schedule(client: WindmillClient, args):
    print(f"[*] Triggering schedule '{args.path}' immediately...")
    res = client.trigger_schedule(args.path)
    print(json.dumps(res, indent=2))


def cmd_variables(client: WindmillClient, args):
    vars_list = client.list_variables()
    print("\n" + "=" * 80)
    print(f"{'VARIABLE PATH':<42} | {'SECRET':<8} | {'VALUE / PREVIEW'}")
    print("-" * 80)
    for v in vars_list:
        val_str = "********" if v.get("is_secret") else str(v.get("value"))[:26]
        sec_str = "YES" if v.get("is_secret") else "NO"
        print(f"{v.get('path'):<42} | {sec_str:<8} | {val_str}")
    print("=" * 80 + "\n")


def cmd_set_variable(client: WindmillClient, args):
    print(f"[*] Setting variable '{args.path}'...")
    res = client.set_variable(args.path, args.value, is_secret=args.secret, description=args.description)
    print(json.dumps(res, indent=2))


def cmd_webhook(client: WindmillClient, args):
    payload = {}
    if args.data:
        try:
            payload = json.loads(args.data)
        except Exception as e:
            print(f"[!] Warning: Failed to parse data as JSON: {e}")
    print(f"[*] Invoking webhook '{args.name}'...")
    res = client.trigger_webhook(args.name, payload)
    print(json.dumps(res, indent=2))


def cmd_do_everything(client: WindmillClient, args):
    orchestrator = WindmillOrchestrator(client)
    print("\n" + "=" * 70)
    print(" EXECUTING SOVEREIGN WINDMILL AUTONOMOUS WORKFLOW CYCLE (12 PHASES)")
    print("=" * 70)
    manifest = orchestrator.do_everything()
    print(f"\n[+] Sovereign Windmill Manifest Generated: {manifest['execution_id']}")
    print(f"    Protocol:       {manifest['protocol']}")
    print(f"    Status:         {manifest['status']}")
    print(f"    Phases Run:     {manifest['total_phases_executed']} / 12 PASSED")
    print(f"    Total Time:     {manifest['total_elapsed_seconds']}s")
    print("\n[-] Phase Breakdown:")
    for p in manifest["phases"]:
        print(f"    [{p['phase']:02d}] {p['name']:<50} | {p['status']} ({p['elapsed_seconds']}s)")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Windmill Autonomous Workflow CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    subparsers.add_parser("info", help="Display platform telemetry & worker pool status")
    subparsers.add_parser("workspaces", help="List multi-tenant workspaces")
    subparsers.add_parser("scripts", help="List runnable scripts")
    subparsers.add_parser("flows", help="List composed DAG flows")
    subparsers.add_parser("apps", help="List low-code applications")
    subparsers.add_parser("resources", help="List typed enterprise resources")
    subparsers.add_parser("schedules", help="List registered automated cron schedules")
    subparsers.add_parser("variables", help="List workspace variables & encrypted secrets")

    p_trig_s = subparsers.add_parser("trigger-schedule", help="Trigger an automated schedule run immediately")
    p_trig_s.add_argument("path", type=str, help="Schedule path (e.g. u/admin/hourly_carbon_audit_schedule)")

    p_set_v = subparsers.add_parser("set-variable", help="Set or update a workspace variable")
    p_set_v.add_argument("path", type=str, help="Variable path (e.g. u/admin/my_config)")
    p_set_v.add_argument("value", type=str, help="Variable value")
    p_set_v.add_argument("--secret", action="store_true", help="Encrypt as secret")
    p_set_v.add_argument("--description", type=str, default="", help="Description")

    p_wh = subparsers.add_parser("webhook", help="Trigger a webhook endpoint")
    p_wh.add_argument("name", type=str, help="Webhook name (e.g. stripe-billing, security-alert)")
    p_wh.add_argument("--data", type=str, default="", help="JSON string payload")
    
    p_jobs = subparsers.add_parser("jobs", help="List recent execution jobs")
    p_jobs.add_argument("--limit", type=int, default=20, help="Max jobs to display")
    p_jobs.add_argument("--status", type=str, default=None, help="Filter by status (COMPLETED, SUSPENDED, ERROR)")

    p_run_s = subparsers.add_parser("run-script", help="Execute a script")
    p_run_s.add_argument("path", type=str, help="Script path (e.g. u/admin/cbam_carbon_audit)")
    p_run_s.add_argument("--args", type=str, default="", help="JSON string arguments")

    p_run_f = subparsers.add_parser("run-flow", help="Execute a Flow DAG")
    p_run_f.add_argument("path", type=str, help="Flow path (e.g. u/admin/enterprise_client_onboarding_dag)")
    p_run_f.add_argument("--args", type=str, default="", help="JSON string arguments")

    p_appr = subparsers.add_parser("approve-job", help="Sign off on a suspended approval step")
    p_appr.add_argument("job_id", type=str, help="Job ID")
    p_appr.add_argument("--reject", action="store_true", help="Reject rather than approve")
    p_appr.add_argument("--notes", type=str, default="", help="Approval audit notes")

    p_hub = subparsers.add_parser("hub", help="Search Windmill Hub automations")
    p_hub.add_argument("--search", type=str, default="", help="Search query")
    p_hub.add_argument("--category", type=str, default="", help="Filter by category")

    p_import = subparsers.add_parser("hub-import", help="Import template from Hub")
    p_import.add_argument("hub_id", type=str, help="Hub Item ID")

    subparsers.add_parser("do-everything", help="Execute complete 12-phase sovereign Windmill workflow cycle")

    args = parser.parse_args()
    if not args.subcommand:
        print_banner()
        parser.print_help()
        sys.exit(0)

    client = WindmillClient()

    cmd_map = {
        "info": cmd_info,
        "workspaces": cmd_workspaces,
        "scripts": cmd_scripts,
        "flows": cmd_flows,
        "apps": cmd_apps,
        "resources": cmd_resources,
        "schedules": cmd_schedules,
        "variables": cmd_variables,
        "trigger-schedule": cmd_trigger_schedule,
        "set-variable": cmd_set_variable,
        "webhook": cmd_webhook,
        "jobs": cmd_jobs,
        "run-script": cmd_run_script,
        "run-flow": cmd_run_flow,
        "approve-job": cmd_approve_job,
        "hub": cmd_hub,
        "hub-import": cmd_hub_import,
        "do-everything": cmd_do_everything,
    }

    fn = cmd_map.get(args.subcommand)
    if fn:
        fn(client, args)


if __name__ == "__main__":
    main()
