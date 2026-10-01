"""
Autonomous Agent Dispatch Hub & Plane Task Synchronizer.
Reads tasks from TASK_REGISTRY.md and OMEGA executive plans, dispatching them to Plane boards.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.integrations.plane_connector import PlaneClient


class PlaneDispatcher:
    """Bridges OMEGA autonomous agent tasks into Plane CE projects, boards, and cycles."""

    STATE_MAPPING = {
        "discovered": "backlog",
        "planned": "backlog",
        "backlog": "backlog",
        "ready": "unstarted",
        "todo": "unstarted",
        "running": "started",
        "operational": "started",
        "in progress": "started",
        "review": "started",
        "verified": "completed",
        "complete": "completed",
        "done": "completed",
        "blocked": "cancelled",
        "failed": "cancelled",
    }

    def __init__(self, client: Optional[PlaneClient] = None, dry_run: bool = False) -> None:
        self.client = client or PlaneClient(dry_run=dry_run)

    def parse_markdown_tasks(self, content: str) -> List[Dict[str, Any]]:
        """Parses markdown task checkboxes and Markdown table rows into structured tasks."""
        tasks: List[Dict[str, Any]] = []

        # 1. Parse standard Markdown checklists: - [ ] Task description (Priority: high)
        checklist_pattern = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.+)$", re.MULTILINE)
        for match in checklist_pattern.finditer(content):
            checked = match.group(1).lower() == "x"
            raw_text = match.group(2).strip()

            priority = "medium"
            p_match = re.search(r"\(\s*Priority:\s*(\w+)\s*\)", raw_text, re.IGNORECASE)
            if p_match:
                priority = p_match.group(1).lower()
                clean_name = re.sub(r"\(\s*Priority:\s*\w+\s*\)", "", raw_text).strip()
            else:
                clean_name = raw_text

            tasks.append({
                "name": clean_name,
                "completed": checked,
                "state_group": "completed" if checked else "unstarted",
                "priority": priority if priority in ("urgent", "high", "medium", "low") else "medium",
                "source": "checklist",
                "evidence": "",
            })

        # 2. Parse Markdown table rows (e.g. TASK_REGISTRY.md Section 3)
        # Format: | **Task / Subsystem** | Domain | State | Verification Evidence |
        table_row_pattern = re.compile(
            r"^\s*\|\s*\*{0,2}(.*?)\*{0,2}\s*\|\s*(.*?)\s*\|\s*`?\[?([A-Za-z\s]+)\]?`?\s*\|\s*(.*?)\s*\|",
            re.MULTILINE
        )
        for match in table_row_pattern.finditer(content):
            name = match.group(1).strip()
            domain = match.group(2).strip()
            raw_state = match.group(3).strip().lower()
            evidence = match.group(4).strip()

            # Ignore table headers and separators
            if not name or "task / subsystem" in name.lower() or name.startswith("---") or name.startswith(":---"):
                continue

            state_group = self.STATE_MAPPING.get(raw_state, "unstarted")
            completed = state_group == "completed"

            tasks.append({
                "name": f"[{domain}] {name}",
                "domain": domain,
                "completed": completed,
                "raw_state": raw_state.upper(),
                "state_group": state_group,
                "priority": "high" if "security" in domain.lower() or "markets" in domain.lower() else "medium",
                "source": "table",
                "evidence": evidence,
            })

        return tasks

    def sync_registry_to_plane(
        self,
        registry_path: str = "TASK_REGISTRY.md",
        workspace_slug: str = "omega",
        project_id: str = "proj-omega-core",
    ) -> Dict[str, Any]:
        """Reads task registry from disk and creates/updates issues in Plane."""
        if not os.path.exists(registry_path):
            raise FileNotFoundError(f"Registry file not found: {registry_path}")

        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()

        tasks = self.parse_markdown_tasks(content)
        synced_count = 0
        results = []

        print(f"[*] Discovered {len(tasks)} tasks from {registry_path}")
        for task in tasks:
            desc = f"<p><strong>Domain:</strong> {task.get('domain', 'General')}</p>"
            if task.get("evidence"):
                desc += f"<p><strong>Verification Evidence:</strong> {task['evidence']}</p>"

            issue = self.client.create_issue(
                workspace_slug=workspace_slug,
                project_id=project_id,
                title=task["name"],
                description=desc,
                priority=task["priority"],
            )
            synced_count += 1
            results.append({
                "task": task["name"],
                "plane_issue_id": issue.get("id"),
                "status": "staged" if self.client.dry_run else "created",
            })

        return {
            "total_parsed": len(tasks),
            "total_synced": synced_count,
            "dry_run": self.client.dry_run,
            "workspace": workspace_slug,
            "project": project_id,
            "results": results,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Autonomous Plane Dispatcher")
    parser.add_argument("--registry", default="TASK_REGISTRY.md", help="Path to markdown task registry")
    parser.add_argument("--workspace", default="omega", help="Target Plane workspace slug")
    parser.add_argument("--project", default="proj-omega-core", help="Target Plane project ID")
    parser.add_argument("--base-url", default=os.environ.get("PLANE_BASE_URL", "http://localhost:8095"), help="Plane instance base URL")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform dry-run simulation without modifying server state")
    parser.add_argument("--sync", action="store_true", help="Execute sync against Plane instance")

    args = parser.parse_args()

    # Default to dry-run unless --sync is explicitly provided
    is_dry_run = args.dry_run or (not args.sync)

    print("===============================================================================")
    print("                 OMEGA AUTONOMOUS PLANE TASK DISPATCHER                        ")
    print(f"  Target: {args.base_url} | Mode: {'DRY-RUN SIMULATION' if is_dry_run else 'LIVE SYNC'}")
    print("===============================================================================")

    client = PlaneClient(base_url=args.base_url, dry_run=is_dry_run)
    dispatcher = PlaneDispatcher(client=client)

    try:
        report = dispatcher.sync_registry_to_plane(
            registry_path=args.registry,
            workspace_slug=args.workspace,
            project_id=args.project,
        )
        print(f"[+] Task Synchronization Complete!")
        print(f"    Total Parsed: {report['total_parsed']}")
        print(f"    Total Synced: {report['total_synced']}")
        print(f"    Execution Mode: {'DRY-RUN (Simulated)' if report['dry_run'] else 'LIVE'}")
        print("    Sample Tasks Dispatched:")
        for res in report["results"][:3]:
            print(f"      - {res['task']} -> {res['plane_issue_id']} ({res['status']})")
    except Exception as ex:
        print(f"[-] Task dispatch failed: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()
