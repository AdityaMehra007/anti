"""
Git-to-Plane Synchronizer & Automated Release Notes Bridge.
Reads git commit history, correlates commits with Plane departmental projects,
attaches audit comments to Plane issues, and generates structured release changelogs.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.integrations.plane_connector import PlaneClient

# Domain keywords mapped to Plane Project Identifiers
DEPARTMENT_MAP = {
    "CORE": ["core", "plane", "kernel", "cli", "constitution", "codex", "infra", "config", "runtime"],
    "CAP": ["capital", "banking", "treasury", "macro", "money", "syndication", "cash", "fcf", "dcm", "fintech"],
    "FLEET": ["fleet", "robot", "robotics", "terra", "telemetry", "vla", "arm", "edge", "manipulator"],
    "INTEL": ["intel", "radar", "market", "jobspy", "lead", "scrape", "scraper", "talent", "hr", "research", "signal"],
}


class PlaneGitBridge:
    """Synchronizes Git repository commits into Plane CE issues, comments, and changelogs."""

    def __init__(self, client: Optional[PlaneClient] = None, dry_run: bool = False) -> None:
        self.client = client or PlaneClient(dry_run=dry_run)

    def get_git_commits(self, count: int = 15, cwd: Optional[str] = None) -> List[Dict[str, str]]:
        """Reads recent commit history using git log."""
        target_dir = cwd or str(REPO_ROOT)
        cmd = ["git", "log", f"-n{count}", "--pretty=format:%H|%an|%ad|%s", "--date=short"]
        try:
            res = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True, check=True)
            commits = []
            for line in res.stdout.strip().splitlines():
                if not line or "|" not in line:
                    continue
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0].strip(),
                        "author": parts[1].strip(),
                        "date": parts[2].strip(),
                        "message": parts[3].strip(),
                    })
            return commits
        except Exception as ex:
            print(f"[!] Warning: Failed to read git history: {ex}")
            return []

    def classify_commit(self, message: str) -> Dict[str, Any]:
        """Classifies a commit into target Plane project identifier and issue reference."""
        # Check for explicit issue ref like CORE-12, CAP-3, etc.
        issue_ref_match = re.search(r"\b([A-Z]{3,5})-(\d+)\b", message)
        issue_ref = issue_ref_match.group(0) if issue_ref_match else None

        # Check for explicit tag like [CORE], [CAP]
        tag_match = re.search(r"\[(CORE|CAP|FLEET|INTEL)\]", message, re.IGNORECASE)
        if tag_match:
            project_id = tag_match.group(1).upper()
        elif issue_ref_match:
            project_id = issue_ref_match.group(1).upper()
        else:
            # Infer from keyword in commit message
            lower_msg = message.lower()
            project_id = "CORE"  # default
            for dept, keywords in DEPARTMENT_MAP.items():
                if any(kw in lower_msg for kw in keywords):
                    project_id = dept
                    break

        # Check if commit represents a completion
        is_closing = bool(re.search(r"\b(fix|fixes|close|closes|resolve|resolves|feat)\b", message, re.IGNORECASE))

        return {
            "project_id": project_id,
            "issue_ref": issue_ref,
            "is_closing": is_closing,
        }

    def sync_commits_to_plane(
        self,
        commits: List[Dict[str, str]],
        workspace_slug: str = "omega",
    ) -> Dict[str, Any]:
        """Processes commits and correlates them with Plane issues and project boards."""
        synced = []
        for c in commits:
            classification = self.classify_commit(c["message"])
            proj_id = classification["project_id"]
            issue_id = classification["issue_ref"] or f"auto-{c['hash'][:8]}"

            comment_body = (
                f"Autonomous Git Bridge Sync:\n"
                f"Commit: {c['hash'][:10]} by {c['author']} on {c['date']}\n"
                f"Message: {c['message']}"
            )

            # Record comment on issue
            comment_res = self.client.create_issue_comment(
                workspace_slug=workspace_slug,
                project_id=proj_id,
                issue_id=issue_id,
                comment=comment_body,
            )

            synced.append({
                "commit_hash": c["hash"][:10],
                "project_id": proj_id,
                "issue_ref": issue_id,
                "author": c["author"],
                "message": c["message"],
                "status": "staged" if self.client.dry_run else "commented",
            })

        return {
            "workspace": workspace_slug,
            "total_processed": len(commits),
            "synced_entries": synced,
            "dry_run": self.client.dry_run,
        }

    def generate_release_changelog(self, commits: List[Dict[str, str]]) -> str:
        """Generates a structured markdown release changelog grouped by Plane department."""
        grouped: Dict[str, List[Dict[str, str]]] = {"CORE": [], "CAP": [], "FLEET": [], "INTEL": []}
        for c in commits:
            cls_info = self.classify_commit(c["message"])
            target_dept = cls_info["project_id"] if cls_info["project_id"] in grouped else "CORE"
            grouped[target_dept].append(c)

        lines = [
            "# 🚀 OMEGA Autonomous Release Changelog",
            f"**Total Commits Synced:** {len(commits)}",
            "",
        ]

        dept_titles = {
            "CORE": "OMEGA Core Infrastructure",
            "CAP": "Capital Allocator & Sovereign Treasury",
            "FLEET": "Autonomous Agent Fleet Operations",
            "INTEL": "Market Intelligence & Global Radar",
        }

        for dept, dept_commits in grouped.items():
            lines.append(f"## [{dept}] {dept_titles.get(dept, dept)}")
            if not dept_commits:
                lines.append("_No commits in this cycle._")
            else:
                for c in dept_commits:
                    lines.append(f"- `{c['hash'][:7]}` **{c['author']}**: {c['message']}")
            lines.append("")

        return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Git-to-Plane Bridge")
    parser.add_argument("--count", type=int, default=10, help="Number of recent commits to sync")
    parser.add_argument("--workspace", default="omega", help="Target Plane workspace")
    parser.add_argument("--changelog", action="store_true", help="Print structured release changelog")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run in simulation mode")
    parser.add_argument("--sync", action="store_true", help="Execute sync against Plane")

    args = parser.parse_args()
    is_dry_run = args.dry_run or (not args.sync)

    print("===============================================================================")
    print("                     OMEGA GIT-TO-PLANE BRIDGE                                 ")
    print(f"  Mode: {'DRY-RUN SIMULATION' if is_dry_run else 'LIVE'} | Workspace: {args.workspace}")
    print("===============================================================================")

    bridge = PlaneGitBridge(dry_run=is_dry_run)
    commits = bridge.get_git_commits(count=args.count)
    print(f"[*] Retrieved {len(commits)} commits from repository history.")

    if args.changelog:
        print("\n" + bridge.generate_release_changelog(commits))
        return

    res = bridge.sync_commits_to_plane(commits, workspace_slug=args.workspace)
    print(f"[+] Processed {res['total_processed']} commits.")
    for entry in res["synced_entries"][:5]:
        print(f"    - [{entry['project_id']}] {entry['commit_hash']} -> {entry['message'][:50]} ({entry['status']})")


if __name__ == "__main__":
    main()
