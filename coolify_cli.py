#!/usr/bin/env python3
"""
Coolify Universal CLI
=====================
Command-Line Interface for Coolify v4 PaaS and Autonomous Multi-Server Orchestration.
Usage:
    python coolify_cli.py info
    python coolify_cli.py servers
    python coolify_cli.py projects
    python coolify_cli.py apps
    python coolify_cli.py dbs
    python coolify_cli.py services
    python coolify_cli.py catalog [--search KEYWORD] [--category CAT]
    python coolify_cli.py deploy <UUID>
    python coolify_cli.py stack
"""

import sys
import json
import argparse
from coolify_orchestrator import CoolifyClient, CoolifyOrchestrator, CoolifyTemplateCatalog
from coolify_compose_exporter import CoolifyComposeExporter


def print_banner():
    banner = r"""
   _____ ____  ____  __    _____________  __
  / ____/ __ \/ __ \/ /   /  _/ ____/\ \/ /
 / /   / / / / / / / /    / // /_     \  / 
/ /___/ /_/ / /_/ / /____/ // __/     / /  
\____/\____/\____/_____/___/_/       /_/   
  Coolify v4 Autonomous Enterprise Orchestrator
"""
    print(banner)


def cmd_info(orchestrator: CoolifyOrchestrator, args):
    status = orchestrator.get_cluster_status()
    print("=" * 60)
    print(" COOLIFY CLUSTER SUMMARY & TELEMETRY")
    print("=" * 60)
    print(f" Version:              {status['version']}")
    print(f" Cluster Status:       {status['status'].upper()}")
    print(f" Total Managed Nodes:  {status['total_servers']} ({status['healthy_servers']} healthy)")
    print(f" Applications:         {status['total_applications']} ({status['running_applications']} running)")
    print(f" Standalone Databases: {status['total_databases']} ({status['running_databases']} running)")
    print(f" 1-Click Services:     {status['total_services']} active")
    print(f" Catalog Templates:    {status['catalog_template_count']} templates available")
    print("=" * 60)


def cmd_servers(client: CoolifyClient, args):
    servers = client.list_servers()
    print("\n" + "=" * 75)
    print(f"{'UUID':<22} | {'NAME':<20} | {'IP ADDRESS':<15} | {'STATUS':<8} | {'PROXY'}")
    print("-" * 75)
    for s in servers:
        status = "ONLINE" if s.get("is_reachable", True) else "OFFLINE"
        print(f"{s.get('uuid'):<22} | {s.get('name', 'N/A')[:20]:<20} | {s.get('ip', 'N/A'):<15} | {status:<8} | {s.get('proxy_type', 'traefik')}")
    print("=" * 75 + "\n")


def cmd_validate_server(client: CoolifyClient, args):
    print(f"\n[*] Validating SSH connectivity and Docker daemon on {args.uuid}...")
    res = client.validate_server(args.uuid)
    print(json.dumps(res, indent=2))


def cmd_projects(client: CoolifyClient, args):
    projects = client.list_projects()
    print("\n" + "=" * 70)
    print(f"{'PROJECT UUID':<24} | {'NAME':<24} | {'ENVIRONMENTS'}")
    print("-" * 70)
    for p in projects:
        envs = ", ".join([e.get("name", "env") for e in p.get("environments", [])])
        print(f"{p.get('uuid'):<24} | {p.get('name')[:24]:<24} | {envs}")
    print("=" * 70 + "\n")


def cmd_apps(client: CoolifyClient, args):
    apps = client.list_applications()
    print("\n" + "=" * 80)
    print(f"{'APP UUID':<22} | {'NAME':<20} | {'STATUS':<9} | {'BUILD':<10} | {'FQDN'}")
    print("-" * 80)
    for a in apps:
        print(f"{a.get('uuid'):<22} | {a.get('name')[:20]:<20} | {a.get('status', 'stopped').upper():<9} | {a.get('build_pack', 'nixpacks'):<10} | {a.get('fqdn', 'N/A')}")
    print("=" * 80 + "\n")


def cmd_dbs(client: CoolifyClient, args):
    dbs = client.list_databases()
    print("\n" + "=" * 75)
    print(f"{'DB UUID':<24} | {'NAME':<22} | {'TYPE':<20} | {'STATUS'}")
    print("-" * 75)
    for d in dbs:
        print(f"{d.get('uuid'):<24} | {d.get('name')[:22]:<22} | {d.get('type'):<20} | {d.get('status', 'running').upper()}")
    print("=" * 75 + "\n")


def cmd_services(client: CoolifyClient, args):
    services = client.list_services()
    print("\n" + "=" * 70)
    print(f"{'SERVICE UUID':<24} | {'NAME':<22} | {'TEMPLATE':<15} | {'STATUS'}")
    print("-" * 70)
    for s in services:
        print(f"{s.get('uuid'):<24} | {s.get('name')[:22]:<22} | {s.get('template'):<15} | {s.get('status', 'running').upper()}")
    print("=" * 70 + "\n")


def cmd_catalog(orchestrator: CoolifyOrchestrator, args):
    catalog = orchestrator.catalog
    results = catalog.search(query=args.search or "", category=args.category or "")
    print(f"\n[*] Service Templates Catalog (Found {len(results)} matches):")
    print("=" * 80)
    print(f"{'TEMPLATE ID':<18} | {'NAME':<28} | {'CATEGORY':<14} | {'DOCUMENTATION'}")
    print("-" * 80)
    for r in results[:40]:  # Show top 40
        print(f"{r['id']:<18} | {r['name'][:28]:<28} | {r['category'][:14]:<14} | {r['documentation']}")
    if len(results) > 40:
        print(f"... and {len(results) - 40} more services available in templates.")
    print("=" * 80 + "\n")


def cmd_deploy(client: CoolifyClient, args):
    print(f"\n[*] Triggering deployment for resource: {args.uuid}...")
    res = client.deploy(args.uuid, force_rebuild=args.force)
    dep_uuid = res.get("deployment_uuid", "dep-unknown")
    print(f"[+] Deployment Queued: {dep_uuid}")
    print("[*] Streaming execution logs:")
    dep_status = client.get_deployment_status(dep_uuid)
    for log in dep_status.get("logs", []):
        print(f"    {log}")
    print(f"[SUCCESS] Resource {args.uuid} successfully verified!\n")


def cmd_compose(exporter: CoolifyComposeExporter, args):
    template_id = args.template
    target_dir = args.dir or f"./stacks/{template_id}"
    domain = args.domain or "localhost"
    print(f"\n[*] Exporting Docker Compose stack for template '{template_id}'...")
    try:
        res = exporter.save_stack(template_id, target_dir, domain)
        print(f"[SUCCESS] Stack generated in: {target_dir}")
        print(f"    Compose File: {res['compose_path']}")
        print(f"    Env File:     {res['env_path']} ({res['total_vars']} variables generated)")
        print(f"\nTo launch locally with Docker Desktop, run:")
        print(f"    cd {target_dir} && docker compose up -d\n")
    except Exception as e:
        print(f"[ERROR] Failed to export stack: {e}\n")


def cmd_stack(orchestrator: CoolifyOrchestrator, args):
    print("\n[*] Provisioning complete OMEGA autonomous infrastructure stack on Coolify...")
    res = orchestrator.provision_full_omega_stack()
    print("[+] Stack provisioned successfully:")
    print(f"    Project:   {res['project']['name']} ({res['project']['uuid']})")
    for db in res['databases']:
        print(f"    Database:  {db['name']} [{db['type']}] ({db['uuid']})")
    for svc in res['services']:
        print(f"    Service:   {svc['name']} [{svc['template']}] ({svc['uuid']})")
    print("[+] All systems live, healthy, and routed via Traefik edge proxy.\n")


def main():
    parser = argparse.ArgumentParser(description="Coolify v4 Autonomous Orchestrator & CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("info", help="Cluster overview and telemetry")
    subparsers.add_parser("servers", help="List managed servers")
    
    val_parser = subparsers.add_parser("validate-server", help="Validate a server node")
    val_parser.add_argument("uuid", help="Server UUID to validate")

    subparsers.add_parser("projects", help="List projects and environments")
    subparsers.add_parser("apps", help="List deployed applications")
    subparsers.add_parser("dbs", help="List standalone databases")
    subparsers.add_parser("services", help="List active 1-click services")

    cat_parser = subparsers.add_parser("catalog", help="Search 350+ service templates")
    cat_parser.add_argument("--search", "-s", help="Search keyword")
    cat_parser.add_argument("--category", "-c", help="Filter by category")

    dep_parser = subparsers.add_parser("deploy", help="Deploy a resource")
    dep_parser.add_argument("uuid", help="Application or service UUID")
    dep_parser.add_argument("--force", action="store_true", help="Force rebuild container without cache")

    subparsers.add_parser("stack", help="Deploy standard OMEGA autonomous cloud stack")

    cmp_parser = subparsers.add_parser("compose", help="Export standalone docker-compose.yml and .env for any template")
    cmp_parser.add_argument("template", help="Template ID (e.g. anythingllm, n8n, supabase, qdrant)")
    cmp_parser.add_argument("--dir", "-d", help="Target directory (default: ./stacks/<template>)")
    cmp_parser.add_argument("--domain", help="Target domain (default: localhost)")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    client = CoolifyClient()
    orchestrator = CoolifyOrchestrator(client)
    exporter = CoolifyComposeExporter()

    if args.command == "info":
        cmd_info(orchestrator, args)
    elif args.command == "servers":
        cmd_servers(client, args)
    elif args.command == "validate-server":
        cmd_validate_server(client, args)
    elif args.command == "projects":
        cmd_projects(client, args)
    elif args.command == "apps":
        cmd_apps(client, args)
    elif args.command == "dbs":
        cmd_dbs(client, args)
    elif args.command == "services":
        cmd_services(client, args)
    elif args.command == "catalog":
        cmd_catalog(orchestrator, args)
    elif args.command == "deploy":
        cmd_deploy(client, args)
    elif args.command == "stack":
        cmd_stack(orchestrator, args)
    elif args.command == "compose":
        cmd_compose(exporter, args)


if __name__ == "__main__":
    main()
