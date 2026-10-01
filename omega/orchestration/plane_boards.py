"""
Multi-Departmental Board & Sprint Cycle Provisioner for Plane CE.
Provisions core departmental projects, default Kanban states, and automated 14-day Sprint Cycles.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.integrations.plane_connector import PlaneClient

DEPARTMENT_PROJECTS = [
    {
        "name": "OMEGA Core Infrastructure",
        "identifier": "CORE",
        "description": "Core system architecture, master codex, and base runtime.",
    },
    {
        "name": "Capital Allocator & Sovereign Treasury",
        "identifier": "CAP",
        "description": "Multi-currency treasury, cash pooling, DCM, and liquidity management.",
    },
    {
        "name": "Autonomous Agent Fleet Operations",
        "identifier": "FLEET",
        "description": "Planetary multi-agent swarms, dispatchers, and verification ledgers.",
    },
    {
        "name": "Market Intelligence & Global Radar",
        "identifier": "INTEL",
        "description": "Predictive macro intelligence, career radar, and high-signal lead scrapers.",
    },
]


class PlaneBoardEngine:
    """Provisions departmental projects, Kanban views, and automated sprint cycles."""

    def __init__(self, client: Optional[PlaneClient] = None, dry_run: bool = False) -> None:
        self.client = client or PlaneClient(dry_run=dry_run)

    def calculate_sprint_cycles(
        self,
        sprint_count: int = 3,
        sprint_days: int = 14,
        start_date: Optional[datetime] = None,
    ) -> List[Dict[str, str]]:
        """Calculates sequential sprint cycles starting from a given date."""
        base_date = start_date or datetime.now()
        cycles = []

        current_start = base_date
        for i in range(1, sprint_count + 1):
            current_end = current_start + timedelta(days=sprint_days)
            cycles.append({
                "name": f"Sprint {i}",
                "start_date": current_start.strftime("%Y-%m-%d"),
                "end_date": current_end.strftime("%Y-%m-%d"),
            })
            current_start = current_end

        return cycles

    def provision_department_projects(
        self,
        workspace_slug: str = "omega",
    ) -> List[Dict[str, Any]]:
        """Provisions all standard departmental projects in the target workspace."""
        results = []
        for dept in DEPARTMENT_PROJECTS:
            res = self.client.create_project(
                workspace_slug=workspace_slug,
                name=dept["name"],
                identifier=dept["identifier"],
                description=dept["description"],
            )
            results.append(res)
        return results

    def provision_sprint_cycles(
        self,
        workspace_slug: str = "omega",
        project_id: str = "CORE",
        sprint_count: int = 3,
        sprint_days: int = 14,
    ) -> List[Dict[str, Any]]:
        """Provisions sequential sprint cycles for a target project."""
        cycles = self.calculate_sprint_cycles(sprint_count=sprint_count, sprint_days=sprint_days)
        results = []
        for cycle in cycles:
            res = self.client.create_cycle(
                workspace_slug=workspace_slug,
                project_id=project_id,
                name=cycle["name"],
                start_date=cycle["start_date"],
                end_date=cycle["end_date"],
            )
            results.append(res)
        return results

    def provision_all(
        self,
        workspace_slug: str = "omega",
        sprint_count: int = 3,
    ) -> Dict[str, Any]:
        """Orchestrates provisioning of all department projects and their initial sprint cycles."""
        print(f"[*] Provisioning {len(DEPARTMENT_PROJECTS)} departmental projects in '{workspace_slug}'...")
        projects = self.provision_department_projects(workspace_slug=workspace_slug)

        cycle_map = {}
        for proj in projects:
            proj_id = proj.get("id") or proj.get("identifier") or "CORE"
            print(f"[*] Provisioning {sprint_count} sprint cycles for project '{proj_id}'...")
            cycle_results = self.provision_sprint_cycles(
                workspace_slug=workspace_slug,
                project_id=proj_id,
                sprint_count=sprint_count,
            )
            cycle_map[proj_id] = cycle_results

        return {
            "workspace": workspace_slug,
            "dry_run": self.client.dry_run,
            "projects_provisioned": projects,
            "cycles_provisioned": cycle_map,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Plane Board & Sprint Engine")
    parser.add_argument("--workspace", default="omega", help="Target Plane workspace slug")
    parser.add_argument("--sprint-count", type=int, default=3, help="Number of 14-day sprint cycles to provision")
    parser.add_argument("--base-url", default=os.environ.get("PLANE_BASE_URL", "http://localhost:8095"), help="Plane instance base URL")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Simulate provisioning without network changes")
    parser.add_argument("--provision-all", action="store_true", help="Provision all departments and sprint cycles")

    args = parser.parse_args()

    client = PlaneClient(base_url=args.base_url, dry_run=args.dry_run)
    engine = PlaneBoardEngine(client=client)

    print("===============================================================================")
    print("             OMEGA PLANE DEPARTMENTAL BOARD & SPRINT ENGINE                    ")
    print(f"  Target: {args.base_url} | Mode: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print("===============================================================================")

    if args.provision_all or not sys.argv[1:]:
        report = engine.provision_all(workspace_slug=args.workspace, sprint_count=args.sprint_count)
        print(f"[+] Provisioning Complete!")
        print(f"    Departments: {len(report['projects_provisioned'])}")
        print(f"    Mode: {'DRY-RUN (Simulated)' if report['dry_run'] else 'LIVE'}")
        for p in report["projects_provisioned"]:
            print(f"      - {p.get('name')} [{p.get('identifier')}]")


if __name__ == "__main__":
    main()
