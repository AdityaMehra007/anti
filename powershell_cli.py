#!/usr/bin/env python3
"""
PowerShell Universal CLI
========================
Command-Line Interface for PowerShell 7+ / Core & Windows PowerShell Autonomous Ecosystem.

Usage:
    python powershell_cli.py info
    python powershell_cli.py exec "<command>" [--raw]
    python powershell_cli.py ast "<code_or_path>"
    python powershell_cli.py analyze "<code_or_path>"
    python powershell_cli.py modules
    python powershell_cli.py gallery [--search KEYWORD] [--category CAT]
    python powershell_cli.py runbooks
    python powershell_cli.py run-runbook <id> [--params JSON]
    python powershell_cli.py runspaces
    python powershell_cli.py cis-audit
    python powershell_cli.py benchmark [--iterations N]
    python powershell_cli.py do-everything
"""

import sys
import json
import argparse
import os
from powershell_orchestrator import (
    PowerShellConfig,
    PowerShellClient,
    PowerShellOrchestrator
)


def print_banner():
    banner = r"""
  _____                          _____ _          _ _ 
 |  __ \                        / ____| |        | | |
 | |__) |____      _____ _ __  | (___ | |__   ___| | |
 |  ___/ _ \ \ /\ / / _ \ '__|  \___ \| '_ \ / _ \ | |
 | |  | (_) \ V  V /  __/ |     ____) | | | |  __/ | |
 |_|   \___/ \_/\_/ \___|_|    |_____/|_| |_|\___|_|_|
   PowerShell Autonomous Ecosystem (github.com/PowerShell/PowerShell)
"""
    print(banner)


def cmd_info(client: PowerShellClient, args):
    t = client.get_telemetry()
    print("=" * 65)
    print(" POWERSHELL RUNTIME & RUNSPACE TELEMETRY")
    print("=" * 65)
    print(f" Engine Version:      {t.get('version')} ({t.get('edition')})")
    print(f" CLR Core Version:    {t.get('clr_version')}")
    print(f" Operating Mode:      {t.get('operating_mode', 'SIMULATION')}")
    print(f" Executable:          {t.get('executable_path', 'Simulated pwsh')}")
    print(f" Platform OS:         {t.get('os_platform')}")
    print(f" Active Runspaces:    {t.get('active_runspaces')} threads")
    print(f" Cmdlets Cataloged:   {t.get('total_cmdlets')} cmdlets")
    print(f" Installed Modules:   {t.get('installed_modules_count')} modules")
    print(f" PSGallery Index:     {t.get('gallery_packages_indexed')} indexed packages")
    print(f" Execution Policy:    {t.get('execution_policy')}")
    print(f" Language Mode:       {t.get('language_mode')}")
    print(f" AST Parser:          {'ONLINE' if t.get('ast_parser_available') else 'OFFLINE'}")
    print(f" PSScriptAnalyzer:    {'ONLINE' if t.get('script_analyzer_available') else 'OFFLINE'}")
    print("=" * 65)


def cmd_exec(client: PowerShellClient, args):
    cmd_text = args.command
    as_json = not args.raw
    res = client.execute(cmd_text, as_json=as_json)
    if not res.success:
        print(f"[ERROR] (Exit Code {res.exit_code}): {res.stderr}")
        sys.exit(1)

    print(f"[OK] Executed in {res.execution_time_ms} ms (Exit Code {res.exit_code}):")
    if as_json and res.objects:
        print(json.dumps(res.objects, indent=2))
    else:
        print(res.stdout)


def cmd_ast(client: PowerShellClient, args):
    target = args.target
    code = target
    if os.path.exists(target):
        with open(target, "r", encoding="utf-8") as f:
            code = f.read()

    ast_res = client.parse_ast(code)
    print("=" * 65)
    print(" SYSTEM.MANAGEMENT.AUTOMATION AST ANALYSIS")
    print("=" * 65)
    print(f" Tokens Parsed:       {ast_res.tokens_count}")
    print(f" Syntax Errors:       {'NONE (PASS)' if not ast_res.has_errors else len(ast_res.syntax_errors)}")
    if ast_res.syntax_errors:
        for err in ast_res.syntax_errors:
            print(f"   - [SYNTAX_ERROR] {err}")
    print(f" Functions Declared:  {len(ast_res.functions)}")
    for fn in ast_res.functions:
        cb = " [CmdletBinding]" if fn.get("has_cmdlet_binding") else ""
        print(f"   - {fn.get('name')} (Line {fn.get('line')}){cb}")
    print(f" Cmdlet Invocations:  {', '.join(ast_res.pipeline_calls[:15])}")
    print(f" Variables Scoped:    {', '.join(ast_res.variables_referenced[:15])}")
    print("=" * 65)


def cmd_analyze(client: PowerShellClient, args):
    target = args.target
    code = target
    if os.path.exists(target):
        with open(target, "r", encoding="utf-8") as f:
            code = f.read()

    diags = client.analyze_script(code)
    print("=" * 65)
    print(" PSSCRIPTANALYZER SECURITY & ARCHITECTURE LINTING")
    print("=" * 65)
    if not diags:
        print(" [CLEAN] Zero rule violations detected! Code adheres to best practices.")
    else:
        print(f" Detected {len(diags)} diagnostic issue(s):")
        for d in diags:
            print(f" [{d.severity.upper()}] Line {d.line_number}: {d.rule_name}")
            print(f"   Message: {d.message}")
            if d.suggested_fix:
                print(f"   Remediation: {d.suggested_fix}")
    print("=" * 65)


def cmd_modules(client: PowerShellClient, args):
    mods = client.list_modules()
    print("=" * 65)
    print(f" INSTALLED POWERSHELL ENTERPRISE MODULES ({len(mods)})")
    print("=" * 65)
    for m in mods:
        name = m.get("Name") or m.get("name")
        version = m.get("Version") or m.get("version")
        desc = m.get("Description") or m.get("description", "")
        author = m.get("Author") or m.get("author", "")
        print(f" - {name:<32} v{str(version):<10} ({author})")
        if desc:
            print(f"     {desc[:75]}")
    print("=" * 65)


def cmd_gallery(client: PowerShellClient, args):
    pkgs = client.find_gallery_module(keyword=args.search or "", category=args.category or "")
    print("=" * 65)
    print(f" PSGALLERY PACKAGES & EXTENSIONS ({len(pkgs)})")
    print("=" * 65)
    for p in pkgs:
        print(f" - {p['name']:<22} v{p['version']:<8} [{p.get('category','Module'):<10}] DLs: {p.get('downloads',0):,}")
        print(f"     {p.get('description', '')}")
    print("=" * 65)


def cmd_runbooks(client: PowerShellClient, args):
    books = client.list_runbooks()
    print("=" * 65)
    print(f" REGISTERED ENTERPRISE RUNBOOKS ({len(books)})")
    print("=" * 65)
    for b in books:
        print(f" [{b['id']}] {b['title']} ({b['category']}) - Risk: {b.get('risk_level','LOW')}")
        print(f"     Script: {b['script_path']}")
        print(f"     {b['description']}")
    print("=" * 65)


def cmd_run_runbook(client: PowerShellClient, args):
    params = json.loads(args.params) if args.params else None
    res = client.execute_runbook(args.id, params=params)
    print("=" * 65)
    print(f" RUNBOOK EXECUTION: {res['title']} (Status: {'SUCCESS' if res['success'] else 'FAILED'})")
    print(f" Time Elapsed: {res['execution_time_ms']} ms | Exit Code: {res['exit_code']}")
    print("=" * 65)
    print(json.dumps(res["result_data"], indent=2))


def cmd_runspaces(client: PowerShellClient, args):
    spaces = client.list_runspaces()
    print("=" * 65)
    print(f" ACTIVE RUNSPACE POOL CONCURRENCY ({len(spaces)} RUNSPACES)")
    print("=" * 65)
    for s in spaces:
        print(f" - [{s['id']:02d}] {s['name']:<25} State: {s['state']:<10} Availability: {s['availability']} (Thread: {s.get('thread_id')})")
    print("=" * 65)


def cmd_cis_audit(client: PowerShellClient, args):
    orchestrator = PowerShellOrchestrator(client)
    res = orchestrator.audit_cis_hardening()
    data = res["result_data"]
    print("=" * 65)
    print(f" CIS OS HARDENING AUDIT: {data.get('Status')} ({data.get('ComplianceScore')}%)")
    print(f" Passed Checks: {data.get('PassedChecks')}/{data.get('TotalChecks')}")
    print("=" * 65)
    for f in data.get("Findings", []):
        print(f" [{f.get('Status')}] {f.get('CheckId')}: {f.get('Title')} ({f.get('Severity')})")
        print(f"     {f.get('Details')}")
    print("=" * 65)


def cmd_benchmark(client: PowerShellClient, args):
    orchestrator = PowerShellOrchestrator(client)
    res = orchestrator.benchmark_pipeline(iterations=args.iterations)
    print("=" * 65)
    print(" POWERSHELL PIPELINE THROUGHPUT BENCHMARK")
    print("=" * 65)
    print(f" Iterations:          {res['iterations']}")
    print(f" Objects Per Run:     {res['objects_per_run']:,}")
    print(f" Average Latency:     {res['average_latency_ms']} ms")
    print(f" Min / Max Latency:   {res['min_latency_ms']} ms / {res['max_latency_ms']} ms")
    print(f" Pipeline Throughput: {res['throughput_objects_per_sec']:,} objects/second")
    print("=" * 65)


def cmd_do_everything(client: PowerShellClient, args):
    orchestrator = PowerShellOrchestrator(client)
    manifest = orchestrator.do_everything()
    print("=" * 65)
    print(f" SOVEREIGN MANIFEST: {manifest['execution_id']}")
    print(f" Overall Status:     {manifest['overall_status']}")
    print(f" Total Phases:       {manifest['total_phases_executed']} phases")
    print(f" Total Elapsed:      {manifest['total_elapsed_seconds']}s")
    print("=" * 65)
    for p in manifest["phases"]:
        print(f" Phase {p['phase']:02d}: {p['name']} -> [{p['status']}] ({p['elapsed_seconds']}s)")
        print(f"          {p['description']}")
    print("=" * 65)


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="PowerShell Autonomous Ecosystem CLI")
    parser.add_argument("--mock", action="store_true", help="Force mock simulation mode")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("info", help="Display PowerShell runtime telemetry")
    
    p_exec = subparsers.add_parser("exec", help="Execute command or script")
    p_exec.add_argument("command", help="PowerShell command string")
    p_exec.add_argument("--raw", action="store_true", help="Do not wrap with ConvertTo-Json")

    p_ast = subparsers.add_parser("ast", help="Parse script AST")
    p_ast.add_argument("target", help="PowerShell code or path to .ps1 file")

    p_ana = subparsers.add_parser("analyze", help="Run PSScriptAnalyzer rules")
    p_ana.add_argument("target", help="PowerShell code or path to .ps1 file")

    subparsers.add_parser("modules", help="List installed enterprise modules")

    p_gal = subparsers.add_parser("gallery", help="Search PSGallery packages")
    p_gal.add_argument("--search", default="", help="Search keyword")
    p_gal.add_argument("--category", default="", help="Filter category")

    subparsers.add_parser("runbooks", help="List registered enterprise runbooks")

    p_run = subparsers.add_parser("run-runbook", help="Execute an enterprise runbook")
    p_run.add_argument("id", help="Runbook ID (e.g. cis_hardening, cloud_recon)")
    p_run.add_argument("--params", default="", help="JSON parameter object")

    subparsers.add_parser("runspaces", help="List active runspace pool threads")
    subparsers.add_parser("cis-audit", help="Run 1-click CIS OS Hardening audit")

    p_bench = subparsers.add_parser("benchmark", help="Benchmark pipeline throughput")
    p_bench.add_argument("--iterations", type=int, default=5, help="Number of benchmark iterations")

    subparsers.add_parser("do-everything", help="Execute full 12-phase sovereign lifecycle")

    args = parser.parse_args()

    config = PowerShellConfig(mock_mode=args.mock)
    client = PowerShellClient(config)

    commands = {
        "info": cmd_info,
        "exec": cmd_exec,
        "ast": cmd_ast,
        "analyze": cmd_analyze,
        "modules": cmd_modules,
        "gallery": cmd_gallery,
        "runbooks": cmd_runbooks,
        "run-runbook": cmd_run_runbook,
        "runspaces": cmd_runspaces,
        "cis-audit": cmd_cis_audit,
        "benchmark": cmd_benchmark,
        "do-everything": cmd_do_everything,
    }

    if not args.command:
        cmd_info(client, args)
    elif args.command in commands:
        commands[args.command](client, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
