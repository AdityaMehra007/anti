#!/usr/bin/env python3
"""
n8n Universal CLI
=================
Production-grade Command-Line Interface for the n8n Enterprise Workflow Automation Platform.
Usage:
    python n8n_cli.py info
    python n8n_cli.py nodes [--group GROUP] [--limit N]
    python n8n_cli.py search <query> [--limit N]
    python n8n_cli.py workflows [--active-only]
    python n8n_cli.py get-workflow <name_or_id>
    python n8n_cli.py run-workflow <name_or_id> [--data JSON]
    python n8n_cli.py trigger <webhook_path> [--data JSON] [--test]
    python n8n_cli.py ai-agent <prompt>
    python n8n_cli.py executions [--limit N] [--status STATUS]
    python n8n_cli.py get-execution <exec_id>
    python n8n_cli.py credentials
    python n8n_cli.py dropzone
    python n8n_cli.py export [--dir DIR]
    python n8n_cli.py do-everything
    python n8n_cli.py serve [--port 8771]
"""

import sys
import json
import argparse
from typing import Any
from n8n_orchestrator import N8nClient, N8nOrchestrator, N8nConfig


def print_banner():
    banner = r"""
        ___       
       / _ \      
  _ __| (_) |_ __ 
 | '_ \ > _ < '_ \
 | | | | (_) | | |
 |_| |_|\___/|_| |_|
   n8n Autonomous Enterprise Workflow Platform & Agent Engine
"""
    print(banner)


def cmd_info(client: N8nClient, args):
    telemetry = client.get_telemetry()
    print("=" * 70)
    print(" N8N ENTERPRISE AUTOMATION & WORKER TELEMETRY")
    print("=" * 70)
    print(f" Platform Version:       v{telemetry.get('version')}")
    print(f" Framework Core:         {telemetry.get('framework')}")
    print(f" Operating Mode:         {telemetry.get('mode', 'SIMULATION')}")
    print(f" Execution Mode:         {telemetry.get('execution_mode', 'regular').upper()}")
    print(f" Active Worker Nodes:    {telemetry.get('active_workers', 8)} workers")
    print(f" Max Concurrency:        {telemetry.get('max_concurrency', 32)} simultaneous jobs")
    print(f" Node Catalog Total:     {telemetry.get('nodes_catalog_count', 0)} core nodes")
    print(f" Production Workflows:   {telemetry.get('active_workflows_count', 0)} workflows")
    print(f" Inbound Webhook Routes: {telemetry.get('webhook_routes_count', 0)} routes mapped")
    print(f" Credentials In Vault:   {telemetry.get('credentials_vault_count', 0)} encrypted keys")
    print(f" Total Executions:       {telemetry.get('total_executions_recorded', 0)} recorded runs")
    print("=" * 70)


def cmd_nodes(client: N8nClient, args):
    nodes = client.list_nodes(group=args.group, limit=args.limit)
    grp_desc = f" (Group: {args.group})" if args.group else ""
    print(f"\nDiscovered {len(nodes)} n8n Nodes{grp_desc}:")
    print("=" * 75)
    for n in nodes:
        name = n.get("displayName") or n.get("name")
        tech_name = n.get("name")
        grp = n.get("group", "general")
        desc = (n.get("description") or "No description provided.")[:65]
        print(f"• {name:28s} [{tech_name}] ({grp})")
        print(f"    {desc}...")
    print("=" * 75)


def cmd_search(client: N8nClient, args):
    results = client.search_nodes(args.query, limit=args.limit)
    print(f"\nFound {len(results)} matches for query '{args.query}':")
    print("=" * 80)
    for n in results:
        name = n.get("displayName") or n.get("name")
        tech_name = n.get("name")
        grp = n.get("group", "general")
        desc = (n.get("description") or "").replace("\n", " ").strip()[:140]
        print(f"• {name} [{tech_name}] ({grp})")
        if desc:
            print(f"    {desc}...")
        print("-" * 80)


def cmd_workflows(client: N8nClient, args):
    wfs = client.list_workflows(active_only=args.active_only)
    state = "Active" if args.active_only else "Total"
    print(f"\n{state} OMEGA Production Workflows ({len(wfs)}):")
    print("=" * 80)
    print(f"{'#':<3} {'ID':<25} {'NAME':<35} {'NODES':<7} {'STATUS'}")
    print("-" * 80)
    for idx, w in enumerate(wfs, 1):
        w_id = w.get("id", "unknown")[:24]
        name = w.get("name", "Unnamed")[:34]
        n_count = len(w.get("nodes", []))
        status = "ACTIVE" if w.get("active") else "PAUSED"
        print(f"{idx:<3} {w_id:<25} {name:<35} {n_count:<7} {status}")
    print("=" * 80)


def cmd_get_workflow(client: N8nClient, args):
    wf = client.get_workflow(args.name_or_id)
    if not wf:
        print(f"[-] Workflow '{args.name_or_id}' not found.")
        sys.exit(1)
    print(json.dumps(wf, indent=2))


def cmd_run_workflow(client: N8nClient, args):
    payload = {}
    if args.data:
        try:
            payload = json.loads(args.data)
        except Exception:
            payload = {"raw_input": args.data}

    print(f"\nExecuting workflow '{args.name_or_id}'...")
    res = client.execute_workflow(args.name_or_id, input_data=payload)
    print("=" * 70)
    print(" EXECUTION RESULT")
    print("=" * 70)
    print(f" Execution ID:     {res['id']}")
    print(f" Workflow Name:    {res['workflowName']}")
    print(f" Execution Status: {res['status']}")
    print(f" Nodes Executed:   {res['nodesCount']} nodes ({', '.join(res['executedNodes'])})")
    print(f" Latency:          {res['executionTimeMs']} ms")
    print("-" * 70)
    print(" Output Data:")
    print(json.dumps(res["data"]["resultData"]["runData"], indent=2))
    print("=" * 70)


def cmd_trigger(client: N8nClient, args):
    payload = {}
    if args.data:
        try:
            payload = json.loads(args.data)
        except Exception:
            payload = {"payload": args.data}

    print(f"\nDispatching Webhook to route '/{args.webhook_path.strip('/')}' (test={args.test})...")
    res = client.trigger_webhook(args.webhook_path, payload, test_mode=args.test)
    print("=" * 70)
    print(" WEBHOOK DISPATCH COMPLETED")
    print("=" * 70)
    print(f" Inbound Route:    /{res['path']}")
    print(f" Target Workflow:  {res['workflowName']} [{res['workflowId']}]")
    print(f" Execution ID:     {res['executionId']}")
    print(f" Processing Time:  {res['executionTimeMs']} ms")
    print(f" Test Mode:        {res['testMode']}")
    print("=" * 70)


def cmd_ai_agent(client: N8nClient, args):
    print(f"\nInvoking n8n LangChain AI Agent Node with prompt: '{args.prompt}'...")
    res = client.run_ai_agent(args.prompt)
    print("=" * 70)
    print(" N8N LANGCHAIN AUTONOMOUS AGENT REASONING")
    print("=" * 70)
    print(f" Model Engine:      {res['model']}")
    print(f" Temperature:       {res['temperature']}")
    print("\n Agent Intermediate Thoughts:")
    for t in res.get("thoughts", []):
        print(f"   [thought] {t}")
    print("\n Tool Calls & Observations:")
    for step in res.get("intermediateSteps", []):
        print(f"   • Action: {step['action']}({step['input']}) -> {step['observation']}")
    print("\n Final Agent Output:")
    print(f"   {res['output']}")
    print("=" * 70)


def cmd_executions(client: N8nClient, args):
    execs = client.list_executions(status=args.status, limit=args.limit)
    print(f"\nExecution History ({len(execs)} records):")
    print("=" * 80)
    print(f"{'ID':<18} {'WORKFLOW':<30} {'STATUS':<10} {'NODES':<7} {'LATENCY (ms)'}")
    print("-" * 80)
    for e in execs:
        e_id = e.get("id", "")[:17]
        w_name = e.get("workflowName", "Unknown")[:29]
        status = e.get("status", "SUCCESS")
        nodes = e.get("nodesCount", 0)
        ms = e.get("executionTimeMs", 0)
        print(f"{e_id:<18} {w_name:<30} {status:<10} {nodes:<7} {ms}")
    print("=" * 80)


def cmd_get_execution(client: N8nClient, args):
    e = client.get_execution(args.exec_id)
    if not e:
        print(f"[-] Execution '{args.exec_id}' not found.")
        sys.exit(1)
    print(json.dumps(e, indent=2))


def cmd_credentials(client: N8nClient, args):
    creds = client.list_credentials()
    print(f"\nEncrypted Enterprise Credentials ({len(creds)}):")
    print("=" * 75)
    print(f"{'ID':<18} {'NAME':<35} {'TYPE':<20}")
    print("-" * 75)
    for c in creds:
        print(f"{c['id']:<18} {c['name']:<35} {c['type']:<20}")
    print("=" * 75)


def cmd_dropzone(client: N8nClient, args):
    processed = client.scan_dropzone()
    print(f"\nScanned Dropzone. Processed {len(processed)} files:")
    for p in processed:
        print(f" • {p['original']} ({p['size_bytes']} bytes) -> {p['processed_path']}")


def cmd_export(client: N8nClient, args):
    exported = client.export_workflows(dest_dir=args.dir)
    print(f"\nSuccessfully exported {len(exported)} workflows:")
    for path in exported:
        print(f" • {path}")


def cmd_do_everything(client: N8nClient, args):
    orchestrator = N8nOrchestrator(client)
    res = orchestrator.do_everything()
    print("\n" + "=" * 70)
    print(f" N8N SOVEREIGN LIFECYCLE EXECUTION COMPLETED")
    print("=" * 70)
    print(f" Protocol:       {res['protocol']}")
    print(f" Execution ID:   {res['execution_id']}")
    print(f" Total Phases:   {res['total_phases_executed']} PASSED")
    print(f" Elapsed Time:   {res['total_elapsed_seconds']}s")
    print(f" Status:         {res['status']}")
    print(" Manifest File:  omega/data/n8n_do_everything_manifest.json")
    print("=" * 70)


def cmd_serve(client: N8nClient, args):
    from n8n_api_server import run_server
    run_server(port=args.port)


def main():
    parser = argparse.ArgumentParser(description="n8n Universal Enterprise CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # info
    subparsers.add_parser("info", help="View platform telemetry and status")

    # nodes
    p_nodes = subparsers.add_parser("nodes", help="List node catalog")
    p_nodes.add_argument("--group", help="Filter by node group")
    p_nodes.add_argument("--limit", type=int, default=20, help="Max nodes to display")

    # search
    p_search = subparsers.add_parser("search", help="FTS5 search across 560+ core nodes")
    p_search.add_argument("query", help="Search keyword")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")

    # workflows
    p_wf = subparsers.add_parser("workflows", help="List active production workflows")
    p_wf.add_argument("--active-only", action="store_true", help="Show active only")

    # get-workflow
    p_gwf = subparsers.add_parser("get-workflow", help="Get workflow details")
    p_gwf.add_argument("name_or_id", help="Workflow ID or Name")

    # run-workflow
    p_rwf = subparsers.add_parser("run-workflow", help="Execute workflow DAG")
    p_rwf.add_argument("name_or_id", help="Workflow ID or Name")
    p_rwf.add_argument("--data", help="Input JSON string")

    # trigger
    p_trg = subparsers.add_parser("trigger", help="Trigger inbound webhook")
    p_trg.add_argument("webhook_path", help="Webhook route path")
    p_trg.add_argument("--data", help="Payload JSON string")
    p_trg.add_argument("--test", action="store_true", help="Send to test webhook")

    # ai-agent
    p_ai = subparsers.add_parser("ai-agent", help="Run n8n LangChain AI agent node")
    p_ai.add_argument("prompt", help="User prompt or query for agent")

    # executions
    p_exec = subparsers.add_parser("executions", help="List workflow execution history")
    p_exec.add_argument("--limit", type=int, default=15, help="Max records")
    p_exec.add_argument("--status", help="Filter by status (SUCCESS, ERROR)")

    # get-execution
    p_gexec = subparsers.add_parser("get-execution", help="Get execution details")
    p_gexec.add_argument("exec_id", help="Execution ID")

    # credentials
    subparsers.add_parser("credentials", help="List enterprise credentials")

    # dropzone
    subparsers.add_parser("dropzone", help="Scan dropzone and ingest files")

    # export
    p_exp = subparsers.add_parser("export", help="Export all workflows to backups")
    p_exp.add_argument("--dir", help="Destination directory")

    # do-everything
    subparsers.add_parser("do-everything", help="Run full 12-Phase Sovereign Lifecycle")

    # serve
    p_srv = subparsers.add_parser("serve", help="Launch local API server and Mission Control")
    p_srv.add_argument("--port", type=int, default=8771, help="Port to bind (default 8771)")

    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    client = N8nClient()

    cmd_map = {
        "info": cmd_info,
        "nodes": cmd_nodes,
        "search": cmd_search,
        "workflows": cmd_workflows,
        "get-workflow": cmd_get_workflow,
        "run-workflow": cmd_run_workflow,
        "trigger": cmd_trigger,
        "ai-agent": cmd_ai_agent,
        "executions": cmd_executions,
        "get-execution": cmd_get_execution,
        "credentials": cmd_credentials,
        "dropzone": cmd_dropzone,
        "export": cmd_export,
        "do-everything": cmd_do_everything,
        "serve": cmd_serve
    }

    handler = cmd_map.get(args.command)
    if handler:
        handler(client, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
