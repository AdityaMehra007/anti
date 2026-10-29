#!/usr/bin/env python3
"""
Blackbird Enterprise CLI
Autonomous Command Line Interface for Multi-Platform OSINT Reconnaissance,
Digital Footprint Intelligence, and Defensive OPSEC Threat Modeling.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from blackbird_orchestrator import BlackbirdOrchestrator, serve_cockpit

# Ensure Windows UTF-8 terminal output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console()

BANNER = """[red]
    ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀ ▄▄▄▄    ██▓ ██▀███  ▓█████▄ 
    ▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█████▄ ▓██▒▓██ ▒ ██▒▒██▀ ██▌
    ▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒██▒ ▄██▒██▒▓██ ░▄█ ▒░██   █▌
    ▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒██░█▀  ░██░▒██▀▀█▄  ░▓█▄   ▌
    ░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▓█  ▀█▓░██░░██▓ ▒██▒░▒████▓ 
    ░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░▒▓███▀▒░▓  ░ ▒▓ ░▒▓░ ▒▒▓  ▒ 
    ▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░▒░▒   ░  ▒ ░  ░▒ ░ ▒░ ░ ▒  ▒ 
    ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░  ░    ░  ▒ ░  ░░   ░  ░ ░  ░ 
    ░          ░  ░     ░  ░░ ░      ░  ░    ░       ░     ░        ░    
        ░                  ░                     ░               ░      
[/red]"""


def print_banner():
    console.print(BANNER)
    console.print("   [bold white]Blackbird OSINT & Defensive Intelligence Suite[/bold white] | [cyan]v2.4 Enterprise[/cyan]\n")


def display_results_table(result: dict):
    accounts = result.get("accounts", [])
    target = result.get("target")

    table = Table(title=f"Accounts Discovered for @{target} ({len(accounts)} verified)", border_style="cyan")
    table.add_column("Platform", style="bold white")
    table.add_column("Category", style="cyan")
    table.add_column("Verified URL", style="sky_blue2")
    table.add_column("Latency", justify="right", style="green")

    for acc in accounts:
        table.add_row(
            acc.get("name", "Unknown"),
            acc.get("category", "misc"),
            acc.get("url", ""),
            f"{acc.get('latency_ms', '-')}ms"
        )
    console.print(table)


def display_threat_audit(result: dict):
    threat = result.get("threat_audit", {})
    ai = result.get("ai_profile", {})
    target = result.get("target")

    footprint = threat.get("footprint_index", 0)
    tier = threat.get("threat_tier", "LOW")
    color = "red" if footprint >= 70 else "yellow" if footprint >= 40 else "green"

    summary_text = (
        f"[bold]Target:[/bold] [cyan]@{target}[/cyan]\n"
        f"[bold]Digital Footprint Score:[/bold] [{color}]{footprint} / 100[/{color}] ({tier})\n"
        f"[bold]Discovered Endpoints:[/bold] {result.get('found_count', 0)} / {result.get('total_sites_probed', 0)}\n"
        f"[bold]Credential Stuffing Risk:[/bold] [yellow]{threat.get('credential_stuffing_risk')}[/yellow]\n"
        f"[bold]Handle Impersonation Risk:[/bold] [sky_blue2]{threat.get('impersonation_vulnerability')}[/sky_blue2]\n\n"
        f"[bold purple]AI Behavioral Synthesis:[/bold purple]\n"
        f"{ai.get('summary')}\n\n"
        f"[bold]Tags:[/bold] {', '.join(ai.get('tags', []))}"
    )

    console.print(Panel(summary_text, title="[bold]Defensive OPSEC Threat Audit[/bold]", border_style=color))

    recs = threat.get("recommendations", [])
    if recs:
        rec_table = Table(title="Recommended Defensive Hardening Countermeasures", border_style="yellow")
        rec_table.add_column("Priority", style="bold red")
        rec_table.add_column("Action", style="bold white")
        rec_table.add_column("Rationale", style="white")

        for r in recs:
            rec_table.add_row(r.get("priority"), r.get("action"), r.get("rationale"))
        console.print(rec_table)


def main():
    parser = argparse.ArgumentParser(
        prog="blackbird_cli",
        description="Blackbird OSINT & Defensive Footprint Intelligence Suite"
    )
    parser.add_argument("-u", "--username", nargs="*", help="Target username(s) to search")
    parser.add_argument("-e", "--email", nargs="*", help="Target email(s) to search")
    parser.add_argument("--permute", action="store_true", help="Permute username combinations")
    parser.add_argument("-c", "--category", help="Filter target sites by category (e.g. tech, social, gaming)")
    parser.add_argument("--no-nsfw", action="store_true", default=True, help="Exclude adult / NSFW sites")
    parser.add_argument("--audit", action="store_true", default=True, help="Run defensive risk audit and threat model")
    parser.add_argument("--demo", action="store_true", help="Run instant high-fidelity simulation demonstration")
    parser.add_argument("--stats", action="store_true", help="Display platform census and dataset statistics")
    parser.add_argument("--export-all", action="store_true", default=True, help="Auto-export JSON, CSV, MD, and HTML reports")
    parser.add_argument("--fast", action="store_true", help="Use fast local mock probe instead of live network")
    parser.add_argument("--serve", nargs="?", const=8777, type=int, help="Launch Mission Control Cockpit server (default port 8777)")

    args = parser.parse_args()

    print_banner()
    orchestrator = BlackbirdOrchestrator()

    if args.serve:
        serve_cockpit(port=args.serve)
        return

    if args.stats:
        stats = orchestrator.get_statistics()
        console.print(Panel(
            f"[bold]Total Username Reconnaissance Platforms:[/bold] [green]{stats['total_username_platforms']}[/green]\n"
            f"[bold]Total Email Reconnaissance Platforms:[/bold] [green]{stats['total_email_platforms']}[/green]\n"
            f"[bold]Active User Agents Cached:[/bold] [cyan]{stats['datasets_loaded']['user_agents_count']}[/cyan]\n\n"
            f"[bold]Top Platform Categories:[/bold]\n" +
            "\n".join([f"  • [cyan]{k}[/cyan]: {v} sites" for k, v in list(stats['category_distribution'].items())[:10]]),
            title="[bold]Blackbird Intelligence Platform Census[/bold]",
            border_style="cyan"
        ))
        return

    if args.demo:
        demo_target = (args.username[0] if args.username else "octocat")
        console.print(f"[bold yellow]Running Instant High-Fidelity Simulation for @{demo_target}...[/bold yellow]\n")
        res = orchestrator.run_mock_scan(target=demo_target)
        display_results_table(res)
        display_threat_audit(res)

        p_json = orchestrator.export_json(res)
        p_csv = orchestrator.export_csv(res)
        p_md = orchestrator.export_markdown_dossier(res)
        p_html = orchestrator.export_html_report(res)

        console.print(f"\n[bold green]✔ Scan complete! Generated 4 reports in {orchestrator.reports_dir}:[/bold green]")
        console.print(f"  • JSON: {p_json.name}")
        console.print(f"  • CSV:  {p_csv.name}")
        console.print(f"  • Markdown Dossier: {p_md.name}")
        console.print(f"  • Interactive HTML: {p_html.name}")
        return

    targets = []
    if args.username:
        if args.permute and len(args.username) > 1:
            targets = orchestrator.generate_permutations(args.username)
            console.print(f"[cyan]Generated {len(targets)} permutations from input handles.[/cyan]")
        else:
            targets = args.username

    if not targets and not args.email:
        console.print("[yellow]No target specified. Running demo on handle '@octocat'.[/yellow]\n")
        targets = ["octocat"]
        args.fast = True

    for target in targets:
        console.print(f"[bold cyan]Initiating OSINT Reconnaissance for @{target}...[/bold cyan]")
        if args.fast:
            res = orchestrator.run_mock_scan(target=target)
        else:
            res = asyncio.run(orchestrator.run_live_username_scan(
                username=target,
                category=args.category,
                no_nsfw=args.no_nsfw,
                site_limit=100
            ))

        display_results_table(res)
        if args.audit:
            display_threat_audit(res)

        if args.export_all:
            p_json = orchestrator.export_json(res)
            p_csv = orchestrator.export_csv(res)
            p_md = orchestrator.export_markdown_dossier(res)
            p_html = orchestrator.export_html_report(res)
            console.print(f"\n[green]Dossiers exported to {orchestrator.reports_dir}[/green]")


if __name__ == "__main__":
    main()
