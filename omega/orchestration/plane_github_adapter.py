"""
GitHub & GitLab Event Adapter for Plane Community Edition (CE).
Translates incoming Git webhook payloads (push, pull_request, issues, merge_request)
into Plane CE task updates, automated verification comments, and Kanban state transitions.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega.integrations.plane_connector import PlaneClient

EVENT_LOG_PATH = REPO_ROOT / "omega" / "data" / "plane_git_events.jsonl"


class GitWebhookAdapter:
    """Translates GitHub/GitLab webhook payloads into Plane CE board actions."""

    def __init__(self, client: Optional[PlaneClient] = None, dry_run: bool = False) -> None:
        self.client = client or PlaneClient(dry_run=dry_run)
        EVENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, source: str, event_type: str, result: Dict[str, Any]) -> None:
        """Appends translated git event to persistent audit trail."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "event_type": event_type,
            "result": result,
            "dry_run": self.client.dry_run,
        }
        with open(EVENT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def extract_issue_keys(self, text: str) -> List[str]:
        """Extracts issue identifiers like CORE-12, CAP-45, #123, or iss-101."""
        if not text:
            return []
        patterns = [
            r"\b([A-Z]{2,6}-\d+)\b",   # CORE-101
            r"#(\d+)",                 # #101
            r"\b(iss-[\w-]+)\b"        # iss-101
        ]
        keys = []
        for pat in patterns:
            for match in re.finditer(pat, text, re.IGNORECASE):
                val = match.group(1) if match.groups() else match.group(0)
                if val not in keys:
                    keys.append(val)
        return keys

    def handle_github_push(
        self, payload: Dict[str, Any], workspace_slug: str = "omega", default_project: str = "CORE"
    ) -> Dict[str, Any]:
        """Translates GitHub push event into Plane issue commit comments."""
        commits = payload.get("commits", [])
        ref = payload.get("ref", "refs/heads/master")
        branch = ref.split("/")[-1] if "/" in ref else ref
        sender = payload.get("sender", {}).get("login", "git-author")

        updates: List[Dict[str, Any]] = []

        for c in commits:
            commit_id = c.get("id", "")[:8]
            message = c.get("message", "")
            author = c.get("author", {}).get("name", sender)

            issue_keys = self.extract_issue_keys(message)
            if not issue_keys:
                issue_keys = [f"auto-{commit_id}"]

            for k in issue_keys:
                comment_html = (
                    f"<p><strong>[GitHub Push]</strong> Commit <code>{commit_id}</code> "
                    f"pushed to <code>{branch}</code> by <strong>{author}</strong></p>\n"
                    f"<blockquote>{message}</blockquote>"
                )
                try:
                    res = self.client.create_issue_comment(
                        workspace_slug=workspace_slug,
                        project_id=default_project,
                        issue_id=k,
                        comment_html=comment_html,
                    )
                    updates.append({
                        "commit_id": commit_id,
                        "issue_key": k,
                        "status": "COMMENT_CREATED",
                        "response": res,
                    })
                except Exception as ex:
                    updates.append({
                        "commit_id": commit_id,
                        "issue_key": k,
                        "status": "ERROR",
                        "error": str(ex),
                    })

        result = {
            "action": "github_push",
            "branch": branch,
            "commits_processed": len(commits),
            "updates": updates,
        }
        self.log_event("github", "push", result)
        return result

    def handle_github_pull_request(
        self, payload: Dict[str, Any], workspace_slug: str = "omega", default_project: str = "CORE"
    ) -> Dict[str, Any]:
        """Translates GitHub PR events (opened, closed, merged) into Plane state transitions."""
        action = payload.get("action", "opened")
        pr = payload.get("pull_request", {})
        pr_number = pr.get("number", payload.get("number", 0))
        pr_title = pr.get("title", "")
        pr_body = pr.get("body", "")
        merged = pr.get("merged", False)
        sender = payload.get("sender", {}).get("login", "contributor")

        full_text = f"{pr_title} {pr_body}"
        issue_keys = self.extract_issue_keys(full_text)
        if not issue_keys:
            issue_keys = [f"PR-{pr_number}"]

        status_label = "MERGED" if (action == "closed" and merged) else action.upper()

        updates: List[Dict[str, Any]] = []
        for k in issue_keys:
            comment_html = (
                f"<p><strong>[GitHub Pull Request #{pr_number}]</strong> Status: <strong>{status_label}</strong></p>\n"
                f"<p>Title: <em>{pr_title}</em> | Actor: <strong>{sender}</strong></p>"
            )
            try:
                res = self.client.create_issue_comment(
                    workspace_slug=workspace_slug,
                    project_id=default_project,
                    issue_id=k,
                    comment_html=comment_html,
                )
                updates.append({
                    "pr_number": pr_number,
                    "issue_key": k,
                    "pr_action": action,
                    "is_merged": merged,
                    "comment_res": res,
                })
            except Exception as ex:
                updates.append({
                    "pr_number": pr_number,
                    "issue_key": k,
                    "status": "ERROR",
                    "error": str(ex),
                })

        result = {
            "action": "github_pull_request",
            "pr_action": action,
            "pr_number": pr_number,
            "merged": merged,
            "updates": updates,
        }
        self.log_event("github", f"pull_request.{action}", result)
        return result

    def handle_gitlab_merge_request(
        self, payload: Dict[str, Any], workspace_slug: str = "omega", default_project: str = "CORE"
    ) -> Dict[str, Any]:
        """Translates GitLab MR event into Plane comment and status update."""
        oa = payload.get("object_attributes", {})
        action = oa.get("action", "open")
        mr_id = oa.get("iid", 0)
        title = oa.get("title", "")
        state = oa.get("state", "opened")
        user = payload.get("user", {}).get("username", "gitlab-user")

        issue_keys = self.extract_issue_keys(title)
        if not issue_keys:
            issue_keys = [f"MR-{mr_id}"]

        updates: List[Dict[str, Any]] = []
        for k in issue_keys:
            comment_html = (
                f"<p><strong>[GitLab Merge Request !{mr_id}]</strong> State: <strong>{state.upper()}</strong></p>\n"
                f"<p>Title: <em>{title}</em> | By: <strong>{user}</strong></p>"
            )
            try:
                res = self.client.create_issue_comment(
                    workspace_slug=workspace_slug,
                    project_id=default_project,
                    issue_id=k,
                    comment_html=comment_html,
                )
                updates.append({
                    "mr_id": mr_id,
                    "issue_key": k,
                    "state": state,
                    "comment_res": res,
                })
            except Exception as ex:
                updates.append({
                    "mr_id": mr_id,
                    "issue_key": k,
                    "status": "ERROR",
                    "error": str(ex),
                })

        result = {
            "action": "gitlab_merge_request",
            "mr_id": mr_id,
            "state": state,
            "updates": updates,
        }
        self.log_event("gitlab", "merge_request", result)
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Git Webhook Adapter for Plane CE")
    parser.add_argument("--event-type", choices=["push", "pr", "mr"], default="push", help="Simulate git event")
    parser.add_argument("--sync", action="store_true", help="Send to live Plane instance")
    parser.add_argument("--issue", type=str, default="CORE-101", help="Target issue identifier")

    args = parser.parse_args()
    adapter = GitWebhookAdapter(dry_run=not args.sync)

    print("===============================================================================")
    print("                OMEGA GIT WEBHOOK ADAPTER (GITHUB / GITLAB)                    ")
    print(f"  Mode: {'LIVE' if args.sync else 'SIMULATION / DRY-RUN'} | Event: {args.event_type.upper()}")
    print("===============================================================================")

    if args.event_type == "push":
        sample_push = {
            "ref": "refs/heads/master",
            "sender": {"login": "ApexEngineer"},
            "commits": [
                {
                    "id": "c1a2b3c4d5e6",
                    "message": f"feat: implement resilient git-webhook adapter for Plane [{args.issue}]",
                    "author": {"name": "ApexEngineer"},
                }
            ],
        }
        res = adapter.handle_github_push(sample_push)
        print(f"[+] Push Output: {json.dumps(res, indent=2)}")
    elif args.event_type == "pr":
        sample_pr = {
            "action": "closed",
            "pull_request": {
                "number": 42,
                "title": f"Merge: Sovereign Treasury M2M Rails ({args.issue})",
                "body": f"Resolves {args.issue} with full test coverage.",
                "merged": True,
            },
            "sender": {"login": "ApexLead"},
        }
        res = adapter.handle_github_pull_request(sample_pr)
        print(f"[+] PR Output: {json.dumps(res, indent=2)}")
    elif args.event_type == "mr":
        sample_mr = {
            "object_attributes": {
                "iid": 88,
                "title": f"Resolve {args.issue} via automated pipelines",
                "state": "merged",
            },
            "user": {"username": "OmniBot"},
        }
        res = adapter.handle_gitlab_merge_request(sample_mr)
        print(f"[+] MR Output: {json.dumps(res, indent=2)}")


if __name__ == "__main__":
    main()
