"""
Plane CE Workspace Backup, Export, and Restoration Engine.
Dumps all workspace projects, sprint cycles, workflow states, and issues into
portable JSON archives and generates human-readable Markdown backup dossiers.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.integrations.plane_connector import PlaneClient

BACKUP_DIR = REPO_ROOT / "omega" / "data" / "backups"


class PlaneBackupEngine:
    """Manages full exports, backups, and restorations for Plane CE workspaces."""

    def __init__(self, client: Optional[PlaneClient] = None, dry_run: bool = False) -> None:
        self.client = client or PlaneClient(dry_run=dry_run)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def export_workspace(self, workspace_slug: str = "omega") -> Dict[str, Any]:
        """Queries the Plane API to extract all projects, cycles, and issues for the workspace."""
        projects = self.client.list_projects(workspace_slug)
        if not projects and self.client.dry_run:
            projects = [
                {"id": "proj-core", "identifier": "CORE", "name": "OMEGA Core Infrastructure"},
                {"id": "proj-cap", "identifier": "CAP", "name": "Capital Allocator & Sovereign Treasury"},
                {"id": "proj-fleet", "identifier": "FLEET", "name": "Autonomous Agent Fleet Operations"},
                {"id": "proj-intel", "identifier": "INTEL", "name": "Market Intelligence & Global Radar"},
            ]

        backup_payload: Dict[str, Any] = {
            "metadata": {
                "workspace": workspace_slug,
                "exported_at": datetime.now().isoformat(),
                "exporter_version": "v1.0.0",
                "is_dry_run": self.client.dry_run,
            },
            "projects": [],
        }

        for proj in projects:
            proj_id = proj.get("id") or proj.get("identifier") or "CORE"
            cycles = self.client.list_cycles(workspace_slug, proj_id)
            issues = self.client.list_issues(workspace_slug, proj_id)

            backup_payload["projects"].append({
                "project_info": proj,
                "cycles": cycles,
                "issues": issues,
            })

        return backup_payload

    def save_backup(self, backup_payload: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Saves exported backup dictionary to disk in JSON format."""
        ws = backup_payload["metadata"]["workspace"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = filename or f"plane_backup_{ws}_{ts}.json"
        target_path = BACKUP_DIR / out_name

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(backup_payload, f, indent=2)

        return str(target_path)

    def restore_backup(
        self,
        backup_file: str,
        target_workspace: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Restores projects, cycles, and issues from a saved backup file."""
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        with open(backup_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        ws = target_workspace or payload["metadata"]["workspace"]
        created_projects = 0
        created_cycles = 0
        created_issues = 0

        for p_data in payload.get("projects", []):
            p_info = p_data.get("project_info", {})
            self.client.create_project(
                workspace_slug=ws,
                name=p_info.get("name", "Restored Project"),
                identifier=p_info.get("identifier", "REST"),
                description=p_info.get("description", ""),
            )
            created_projects += 1
            proj_id = p_info.get("id") or p_info.get("identifier") or "REST"

            for c in p_data.get("cycles", []):
                self.client.create_cycle(
                    workspace_slug=ws,
                    project_id=proj_id,
                    name=c.get("name", "Restored Sprint"),
                    start_date=c.get("start_date", "2026-10-01"),
                    end_date=c.get("end_date", "2026-10-15"),
                )
                created_cycles += 1

            for iss in p_data.get("issues", []):
                self.client.create_issue(
                    workspace_slug=ws,
                    project_id=proj_id,
                    title=iss.get("name") or iss.get("title", "Restored Task"),
                    description=iss.get("description_html", ""),
                    priority=iss.get("priority", "medium"),
                )
                created_issues += 1

        return {
            "restored_workspace": ws,
            "projects_restored": created_projects,
            "cycles_restored": created_cycles,
            "issues_restored": created_issues,
            "dry_run": self.client.dry_run,
        }

    def generate_dossier_markdown(self, backup_payload: Dict[str, Any]) -> str:
        """Generates an executive summary markdown dossier of the backup."""
        meta = backup_payload["metadata"]
        lines = [
            f"# 📦 Plane CE Backup Dossier — Workspace `{meta['workspace']}`",
            f"**Exported At:** {meta['exported_at']} | **Mode:** {'DRY-RUN' if meta['is_dry_run'] else 'LIVE'}",
            "",
            "## Projects & Boards Overview",
            "| Project Identifier | Name | Cycles | Issues |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for p in backup_payload.get("projects", []):
            info = p.get("project_info", {})
            p_ident = info.get("identifier", "CORE")
            p_name = info.get("name", "Project")
            c_count = len(p.get("cycles", []))
            i_count = len(p.get("issues", []))
            lines.append(f"| **{p_ident}** | {p_name} | {c_count} | {i_count} |")

        lines.append("")
        return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plane CE Backup & Restoration Engine")
    parser.add_argument("--workspace", default="omega", help="Target workspace slug")
    parser.add_argument("--backup", action="store_true", help="Perform full workspace backup")
    parser.add_argument("--restore", type=str, help="Path to backup JSON file to restore")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Simulate backup/restore")
    parser.add_argument("--sync", action="store_true", help="Run against live server")

    args = parser.parse_args()
    is_dry_run = args.dry_run or (not args.sync)

    engine = PlaneBackupEngine(dry_run=is_dry_run)

    print("===============================================================================")
    print("                    PLANE CE BACKUP & RESTORE ENGINE                           ")
    print(f"  Mode: {'DRY-RUN SIMULATION' if is_dry_run else 'LIVE'} | Workspace: {args.workspace}")
    print("===============================================================================")

    if args.restore:
        print(f"[*] Restoring from {args.restore}...")
        report = engine.restore_backup(args.restore, target_workspace=args.workspace)
        print(f"[+] Restoration Complete!")
        print(f"    Projects: {report['projects_restored']}")
        print(f"    Cycles:   {report['cycles_restored']}")
        print(f"    Issues:   {report['issues_restored']}")
        return

    # Default action: perform backup
    print(f"[*] Exporting workspace '{args.workspace}'...")
    data = engine.export_workspace(args.workspace)
    saved_path = engine.save_backup(data)
    dossier = engine.generate_dossier_markdown(data)

    print(f"[+] Backup saved successfully: {saved_path}")
    print("\n" + dossier)


if __name__ == "__main__":
    main()
