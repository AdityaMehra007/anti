#!/usr/bin/env python3
"""
Plane Universal Autonomous CLI
==============================
Command-line interface for managing Plane workspaces, projects, work items,
sprint cycles, epic modules, documentation pages, triage queues, analytics,
and executing the 12-Phase Sovereign Lifecycle.

Usage:
  python plane_cli.py info
  python plane_cli.py workspaces
  python plane_cli.py projects [--workspace omega]
  python plane_cli.py create-project "Security & Auth" "SEC" --desc "Authentication protocols" --emoji "🛡️"
  python plane_cli.py issues [--project proj-core-01] [--cycle cyc-omega-sprint-25]
  python plane_cli.py create-issue "Refactor Redis queue" --project proj-core-01 --priority high --estimate 5
  python plane_cli.py update-issue iss-005 --state st-proj-core-01-done
  python plane_cli.py cycles [--project proj-core-01]
  python plane_cli.py burndown cyc-omega-sprint-25
  python plane_cli.py modules [--project proj-core-01]
  python plane_cli.py pages [--project proj-core-01]
  python plane_cli.py triage [--project proj-core-01]
  python plane_cli.py triage-action trg-001 --action accept
  python plane_cli.py analytics [--project proj-core-01]
  python plane_cli.py docker-config
  python plane_cli.py do-everything
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from plane_orchestrator import PlaneOrchestrator, PlaneConfig


def format_json(data: object) -> str:
    return json.dumps(data, indent=2)


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="plane_cli",
        description="Plane Sovereign Autonomous CLI (makeplane/plane)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Subcommand: info
    subparsers.add_parser("info", help="Display Plane runtime telemetry and connection status")

    # Subcommand: workspaces
    subparsers.add_parser("workspaces", help="List all accessible workspaces")

    # Subcommand: projects
    projects_p = subparsers.add_parser("projects", help="List projects in workspace")
    projects_p.add_argument("--workspace", "-w", default="omega", help="Workspace slug")

    # Subcommand: create-project
    cp_p = subparsers.add_parser("create-project", help="Create a new project")
    cp_p.add_argument("name", help="Project name")
    cp_p.add_argument("identifier", help="Short identifier code (e.g. SEC, CORE)")
    cp_p.add_argument("--desc", default="", help="Project description")
    cp_p.add_argument("--emoji", default="⚡", help="Project emoji icon")
    cp_p.add_argument("--workspace", "-w", default="omega", help="Workspace slug")

    # Subcommand: issues
    issues_p = subparsers.add_parser("issues", help="List work items / issues")
    issues_p.add_argument("--project", "-p", help="Filter by project ID")
    issues_p.add_argument("--cycle", "-c", help="Filter by cycle ID")
    issues_p.add_argument("--state-group", "-s", help="Filter by state group (backlog, unstarted, started, completed, cancelled)")

    # Subcommand: create-issue
    ci_p = subparsers.add_parser("create-issue", help="Create a new work item / issue")
    ci_p.add_argument("name", help="Issue title / name")
    ci_p.add_argument("--project", "-p", default="proj-core-01", help="Target project ID")
    ci_p.add_argument("--desc", default="", help="HTML / text description")
    ci_p.add_argument("--priority", choices=["urgent", "high", "medium", "low", "none"], default="medium")
    ci_p.add_argument("--estimate", type=int, help="Estimate points")
    ci_p.add_argument("--cycle", help="Sprint cycle ID")
    ci_p.add_argument("--module", help="Epic module ID")

    # Subcommand: update-issue
    ui_p = subparsers.add_parser("update-issue", help="Update issue state or properties")
    ui_p.add_argument("issue_id", help="ID of issue to update")
    ui_p.add_argument("--state", help="New state ID")
    ui_p.add_argument("--priority", choices=["urgent", "high", "medium", "low", "none"])

    # Subcommand: cycles
    cycles_p = subparsers.add_parser("cycles", help="List sprint cycles")
    cycles_p.add_argument("--project", "-p", help="Filter by project ID")

    # Subcommand: create-cycle
    cc_p = subparsers.add_parser("create-cycle", help="Create a sprint cycle")
    cc_p.add_argument("name", help="Cycle name")
    cc_p.add_argument("--project", "-p", default="proj-core-01", help="Target project ID")
    cc_p.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    cc_p.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    cc_p.add_argument("--desc", default="", help="Description")

    # Subcommand: burndown
    bd_p = subparsers.add_parser("burndown", help="Calculate burndown curve for a cycle")
    bd_p.add_argument("cycle_id", help="Cycle ID")

    # Subcommand: modules
    modules_p = subparsers.add_parser("modules", help="List epic modules and roadmaps")
    modules_p.add_argument("--project", "-p", help="Filter by project ID")

    # Subcommand: pages
    pages_p = subparsers.add_parser("pages", help="List documentation pages")
    pages_p.add_argument("--project", "-p", help="Filter by project ID")

    # Subcommand: triage
    triage_p = subparsers.add_parser("triage", help="List pending triage requests")
    triage_p.add_argument("--project", "-p", help="Filter by project ID")

    # Subcommand: triage-action
    ta_p = subparsers.add_parser("triage-action", help="Accept or reject a triage request")
    ta_p.add_argument("triage_id", help="Triage item ID")
    ta_p.add_argument("--action", choices=["accept", "reject"], required=True, help="Action to execute")

    # Subcommand: analytics
    analytics_p = subparsers.add_parser("analytics", help="Generate velocity, throughput, and lead-time report")
    analytics_p.add_argument("--project", "-p", default="proj-core-01", help="Project ID")

    # Subcommand: docker-config
    subparsers.add_parser("docker-config", help="Generate verified Docker Compose stack configuration")

    # Subcommand: do-everything
    subparsers.add_parser("do-everything", help="Execute complete 12-Phase Sovereign Plane Lifecycle")

    parsed = parser.parse_args(args)
    if not parsed.command:
        parser.print_help()
        return 0

    orchestrator = PlaneOrchestrator()

    if parsed.command == "info":
        res = orchestrator.get_info()
        print(format_json(res))

    elif parsed.command == "workspaces":
        res = orchestrator.list_workspaces()
        print(format_json(res))

    elif parsed.command == "projects":
        res = orchestrator.list_projects(parsed.workspace)
        print(format_json(res))

    elif parsed.command == "create-project":
        res = orchestrator.create_project(
            name=parsed.name,
            identifier=parsed.identifier,
            description=parsed.desc,
            emoji=parsed.emoji,
            workspace_slug=parsed.workspace
        )
        print(format_json(res))

    elif parsed.command == "issues":
        res = orchestrator.list_issues(
            project_id=parsed.project,
            cycle_id=parsed.cycle,
            state_group=parsed.state_group
        )
        print(format_json(res))

    elif parsed.command == "create-issue":
        res = orchestrator.create_issue(
            name=parsed.name,
            project_id=parsed.project,
            description_html=parsed.desc,
            priority=parsed.priority,
            estimate_point=parsed.estimate,
            cycle_id=parsed.cycle,
            module_id=parsed.module
        )
        print(format_json(res))

    elif parsed.command == "update-issue":
        updates = {}
        if parsed.state:
            updates["state_id"] = parsed.state
        if parsed.priority:
            updates["priority"] = parsed.priority
        res = orchestrator.update_issue(parsed.issue_id, updates)
        print(format_json(res))

    elif parsed.command == "cycles":
        res = orchestrator.list_cycles(parsed.project)
        print(format_json(res))

    elif parsed.command == "create-cycle":
        res = orchestrator.create_cycle(
            name=parsed.name,
            project_id=parsed.project,
            start_date=parsed.start,
            end_date=parsed.end,
            description=parsed.desc
        )
        print(format_json(res))

    elif parsed.command == "burndown":
        res = orchestrator.get_burndown(parsed.cycle_id)
        print(format_json(res))

    elif parsed.command == "modules":
        res = orchestrator.list_modules(parsed.project)
        print(format_json(res))

    elif parsed.command == "pages":
        res = orchestrator.list_pages(parsed.project)
        print(format_json(res))

    elif parsed.command == "triage":
        res = orchestrator.list_triage(parsed.project)
        print(format_json(res))

    elif parsed.command == "triage-action":
        res = orchestrator.triage_action(parsed.triage_id, parsed.action)
        print(format_json(res))

    elif parsed.command == "analytics":
        res = orchestrator.get_analytics(parsed.project)
        print(format_json(res))

    elif parsed.command == "docker-config":
        res = orchestrator.generate_docker_compose_config()
        print(format_json(res))

    elif parsed.command == "do-everything":
        res = orchestrator.do_everything()
        print(format_json(res))

    return 0


if __name__ == "__main__":
    sys.exit(main())
