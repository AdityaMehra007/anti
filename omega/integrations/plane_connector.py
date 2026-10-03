"""
Zero-dependency Plane CE REST API Connector & Integration Client.
Supports Workspaces, Projects, States, Issues, Cycles, and Dry-Run simulations.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.parse
import urllib.request


class PlaneAPIError(Exception):
    """Base exception for Plane API interaction errors."""
    pass


class PlaneAuthenticationError(PlaneAPIError):
    """Raised when authentication credentials are invalid or missing."""
    pass


class PlaneNotFoundError(PlaneAPIError):
    """Raised when a requested resource (workspace, project, issue) is not found."""
    pass


class PlaneClient:
    """Standard-library HTTP client communicating with Plane CE REST API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8095",
        api_key: Optional[str] = None,
        dry_run: bool = False,
        timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.environ.get("PLANE_API_KEY", "")
        self.dry_run = dry_run
        self.timeout = timeout

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        if self.dry_run:
            print(f"[DRY-RUN] {method} {url} -> payload: {data}")
            if method == "GET":
                if "instances" in endpoint:
                    return {"dry_run": True, "instance_id": "dry-run-inst-001", "version": "v1.4.2", "status": "simulated_offline"}
                if "workspaces" in endpoint and "projects" not in endpoint:
                    return [{"id": "ws-omega", "name": "OMEGA", "slug": "omega"}]
                if "projects" in endpoint and "issues" not in endpoint and "cycles" not in endpoint and "states" not in endpoint:
                    return [
                        {"id": "proj-core", "identifier": "CORE", "name": "OMEGA Core Infrastructure"},
                        {"id": "proj-cap", "identifier": "CAP", "name": "Capital Allocator & Sovereign Treasury"},
                        {"id": "proj-fleet", "identifier": "FLEET", "name": "Autonomous Agent Fleet Operations"},
                        {"id": "proj-intel", "identifier": "INTEL", "name": "Market Intelligence & Global Radar"},
                    ]
                if "cycles" in endpoint:
                    return [
                        {"id": "cyc-1", "name": "Sprint 1", "start_date": "2026-10-01", "end_date": "2026-10-15"},
                        {"id": "cyc-2", "name": "Sprint 2", "start_date": "2026-10-15", "end_date": "2026-10-29"},
                    ]
                if "issues" in endpoint:
                    return [
                        {"id": "iss-1", "name": "Simulated Active Task", "priority": "high", "state": "started"},
                    ]
                if "states" in endpoint:
                    return [
                        {"id": "st-backlog", "name": "Backlog", "group": "backlog"},
                        {"id": "st-todo", "name": "Todo", "group": "unstarted"},
                        {"id": "st-in-progress", "name": "In Progress", "group": "started"},
                        {"id": "st-done", "name": "Done", "group": "completed"},
                    ]
                return []

            simulated_response = {
                "dry_run": True,
                "id": "dry-run-id",
                "name": data.get("name") if data else "dry-run-resource",
                "slug": data.get("slug") if data else "dry-run-slug",
                "identifier": data.get("identifier") if data else "DRY",
                "state": data.get("state") if data else "st-1",
                "priority": data.get("priority") if data else "medium",
                "status": "simulated",
            }
            if data:
                simulated_response.update(data)
            return simulated_response

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OMEGA-Autonomous-Plane-Client/1.0",
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key
            headers["Authorization"] = f"Bearer {self.api_key}"

        body_bytes = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content_type = response.headers.get("Content-Type", "")
                res_body = response.read().decode("utf-8")
                if "application/json" in content_type:
                    return json.loads(res_body) if res_body else {}
                return res_body
        except urllib.error.HTTPError as err:
            err_body = err.read().decode("utf-8", errors="replace")
            if self.dry_run:
                print(f"[DRY-RUN] HTTP {err.code} received, returning simulated response.")
                return {
                    "dry_run": True,
                    "instance_id": "dry-run-instance-001",
                    "version": "v1.4.2",
                    "status": "simulated_ok",
                }
            if err.code == 401:
                raise PlaneAuthenticationError(f"HTTP 401 Unauthorized: {err_body}") from err
            if err.code == 404:
                raise PlaneNotFoundError(f"HTTP 404 Not Found at {url}: {err_body}") from err
            raise PlaneAPIError(f"HTTP {err.code} from Plane: {err_body}") from err
        except urllib.error.URLError as err:
            if self.dry_run:
                print(f"[DRY-RUN] Network unreachable ({err.reason}), returning simulated response.")
                return {
                    "dry_run": True,
                    "instance_id": "dry-run-instance-001",
                    "version": "v1.4.2",
                    "status": "simulated_offline",
                }
            raise PlaneAPIError(f"Failed to connect to Plane at {self.base_url}: {err.reason}") from err

    def health_check(self) -> Dict[str, Any]:
        """Queries Plane instance info / health probe."""
        res = self._request("GET", "/api/instances/")
        if isinstance(res, dict):
            return res
        return {"instance": "ok"}

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """Lists available workspaces for the authenticated user/token."""
        res = self._request("GET", "/api/workspaces/")
        return res if isinstance(res, list) else []

    def create_workspace(self, name: str, slug: str) -> Dict[str, Any]:
        """Creates a new workspace."""
        payload = {"name": name, "slug": slug}
        return self._request("POST", "/api/workspaces/", payload)

    def list_projects(self, workspace_slug: str) -> List[Dict[str, Any]]:
        """Lists projects inside a workspace."""
        res = self._request("GET", f"/api/workspaces/{workspace_slug}/projects/")
        return res if isinstance(res, list) else []

    def create_project(
        self,
        workspace_slug: str,
        name: str,
        identifier: str,
        description: str = "",
    ) -> Dict[str, Any]:
        """Creates a new project within a workspace."""
        payload = {
            "name": name,
            "identifier": identifier,
            "description": description,
        }
        return self._request("POST", f"/api/workspaces/{workspace_slug}/projects/", payload)

    def list_states(self, workspace_slug: str, project_id: str) -> List[Dict[str, Any]]:
        """Retrieves workflow states (e.g. Backlog, Todo, In Progress, Done)."""
        res = self._request("GET", f"/api/workspaces/{workspace_slug}/projects/{project_id}/states/")
        return res if isinstance(res, list) else []

    def list_issues(self, workspace_slug: str, project_id: str) -> List[Dict[str, Any]]:
        """Lists issues in a project."""
        res = self._request("GET", f"/api/workspaces/{workspace_slug}/projects/{project_id}/issues/")
        return res if isinstance(res, list) else []

    def create_issue(
        self,
        workspace_slug: str,
        project_id: str,
        title: str,
        description: str = "",
        state_id: Optional[str] = None,
        priority: str = "medium",
    ) -> Dict[str, Any]:
        """Creates a new issue/task in the project."""
        payload = {
            "name": title,
            "description_html": description,
            "priority": priority,
        }
        if state_id:
            payload["state"] = state_id
        return self._request("POST", f"/api/workspaces/{workspace_slug}/projects/{project_id}/issues/", payload)

    def update_issue(
        self,
        workspace_slug: str,
        project_id: str,
        issue_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Updates issue fields (e.g. state, priority, title, description)."""
        return self._request("PATCH", f"/api/workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/", kwargs)

    def list_cycles(self, workspace_slug: str, project_id: str) -> List[Dict[str, Any]]:
        """Lists active and completed sprint cycles."""
        res = self._request("GET", f"/api/workspaces/{workspace_slug}/projects/{project_id}/cycles/")
        return res if isinstance(res, list) else []

    def create_cycle(
        self,
        workspace_slug: str,
        project_id: str,
        name: str,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """Creates a sprint cycle."""
        payload = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
        }
        return self._request("POST", f"/api/workspaces/{workspace_slug}/projects/{project_id}/cycles/", payload)

    def list_issue_comments(self, workspace_slug: str, project_id: str, issue_id: str) -> List[Dict[str, Any]]:
        """Lists comments on an issue."""
        res = self._request("GET", f"/api/workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/")
        return res if isinstance(res, list) else []

    def create_issue_comment(
        self,
        workspace_slug: str,
        project_id: str,
        issue_id: str,
        comment: str,
    ) -> Dict[str, Any]:
        """Creates an audit or progress comment on an issue."""
        payload = {"comment_html": f"<p>{comment}</p>"}
        return self._request(
            "POST",
            f"/api/workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/",
            payload,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Autonomous Plane CE API Connector")
    parser.add_argument("--base-url", default=os.environ.get("PLANE_BASE_URL", "http://localhost:8095"), help="Plane instance base URL")
    parser.add_argument("--api-key", default=os.environ.get("PLANE_API_KEY", ""), help="Plane API Token")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending mutating HTTP requests")
    parser.add_argument("--status", action="store_true", help="Check health and version of the Plane instance")
    parser.add_argument("--list-workspaces", action="store_true", help="List all accessible workspaces")
    parser.add_argument("--workspace", default="omega", help="Target workspace slug")
    parser.add_argument("--list-projects", action="store_true", help="List projects in target workspace")
    parser.add_argument("--project", default="", help="Target project identifier or ID")
    parser.add_argument("--create-issue", default="", help="Create issue title")
    parser.add_argument("--description", default="", help="Issue description")
    parser.add_argument("--priority", default="medium", choices=["urgent", "high", "medium", "low"], help="Issue priority")

    args = parser.parse_args()
    client = PlaneClient(base_url=args.base_url, api_key=args.api_key, dry_run=args.dry_run)

    print("===============================================================================")
    print("                 OMEGA AUTONOMOUS PLANE CE CONNECTOR                           ")
    print(f"  Target: {args.base_url} | Dry Run: {args.dry_run}")
    print("===============================================================================")

    if args.status:
        print("[*] Probing Plane instance health...")
        try:
            health = client.health_check()
            print(f"[+] Plane instance healthy! Details: {json.dumps(health, indent=2)}")
        except Exception as ex:
            print(f"[-] Plane health check failed: {ex}")
            sys.exit(1)
        return

    if args.list_workspaces:
        print("[*] Fetching workspaces...")
        try:
            ws = client.list_workspaces()
            print(f"[+] Found {len(ws)} workspaces:")
            for item in ws:
                print(f"    - {item.get('name')} (slug: {item.get('slug')})")
        except Exception as ex:
            print(f"[-] Failed to list workspaces: {ex}")
            sys.exit(1)
        return

    if args.list_projects:
        print(f"[*] Fetching projects in workspace '{args.workspace}'...")
        try:
            projs = client.list_projects(args.workspace)
            print(f"[+] Found {len(projs)} projects:")
            for item in projs:
                print(f"    - {item.get('name')} [{item.get('identifier')}] (id: {item.get('id')})")
        except Exception as ex:
            print(f"[-] Failed to list projects: {ex}")
            sys.exit(1)
        return

    if args.create_issue:
        if not args.project:
            print("[-] Error: --project must be specified to create an issue.")
            sys.exit(1)
        print(f"[*] Creating issue '{args.create_issue}' in project '{args.project}'...")
        try:
            res = client.create_issue(
                args.workspace,
                args.project,
                args.create_issue,
                args.description,
                priority=args.priority,
            )
            print(f"[+] Issue created successfully: {json.dumps(res, indent=2)}")
        except Exception as ex:
            print(f"[-] Failed to create issue: {ex}")
            sys.exit(1)
        return

    # Default action if no flag specified
    print("[INFO] No action specified. Use --status, --dry-run, --list-workspaces, or --help.")


if __name__ == "__main__":
    main()
