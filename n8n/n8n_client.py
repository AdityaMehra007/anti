"""
n8n_client.py — Programmatic REST API Client & Automation Gateway for n8n

Provides full CRUD over workflows, execution monitoring, webhook dispatching,
and ecosystem bridges for the OMEGA autonomous execution loops.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error


class N8nClient:
    """Client for interacting with n8n's public REST API and webhook endpoints."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 15,
    ):
        self.base_url = (base_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")).rstrip("/")
        self.api_key = api_key or os.getenv("N8N_API_KEY", "")
        self.timeout = timeout

    @property
    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key
        return headers

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        is_api: bool = True,
    ) -> Dict[str, Any]:
        """Execute HTTP request against n8n API or webhook endpoints."""
        url = f"{self.base_url}/api/v1/{path.lstrip('/')}" if is_api else f"{self.base_url}/{path.lstrip('/')}"
        encoded_data = json.dumps(data).encode("utf-8") if data is not None else None

        req = urllib.request.Request(
            url=url,
            data=encoded_data,
            headers=self._headers,
            method=method.upper(),
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8")
                return json.loads(content) if content else {}
        except urllib.error.HTTPError as e:
            raw_body = e.read().decode("utf-8")
            try:
                err_json = json.loads(raw_body)
                err_msg = err_json.get("message", raw_body)
            except Exception:
                err_msg = raw_body or str(e)
            raise RuntimeError(f"n8n API Error [{e.code}] {err_msg}") from e
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to connect to n8n at {url}: {e.reason}") from e

    # -------------------------------------------------------------------------
    # Health & System Status
    # -------------------------------------------------------------------------
    def health_check(self) -> bool:
        """Verify whether n8n is online and responding."""
        try:
            url = f"{self.base_url}/healthz"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as res:
                return res.status in (200, 204)
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # Workflow Operations
    # -------------------------------------------------------------------------
    def list_workflows(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Retrieve all workflows, optionally filtering active ones."""
        res = self._request("GET", "workflows")
        workflows = res.get("data", [])
        if active_only:
            return [w for w in workflows if w.get("active")]
        return workflows

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Fetch full configuration of a specific workflow by ID."""
        return self._request("GET", f"workflows/{workflow_id}")

    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow inside n8n."""
        # Clean read-only properties if present in template
        payload = {
            "name": workflow_data.get("name", "Untitled Workflow"),
            "nodes": workflow_data.get("nodes", []),
            "connections": workflow_data.get("connections", {}),
            "settings": workflow_data.get("settings", {}),
        }
        return self._request("POST", "workflows", data=payload)

    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing workflow."""
        return self._request("PUT", f"workflows/{workflow_id}", data=workflow_data)

    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Delete workflow by ID."""
        return self._request("DELETE", f"workflows/{workflow_id}")

    def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Activate workflow trigger listeners."""
        return self._request("POST", f"workflows/{workflow_id}/activate")

    def deactivate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Deactivate workflow trigger listeners."""
        return self._request("POST", f"workflows/{workflow_id}/deactivate")

    # -------------------------------------------------------------------------
    # Execution History
    # -------------------------------------------------------------------------
    def list_executions(
        self,
        workflow_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """List recent workflow executions."""
        query_params = f"?limit={limit}"
        if workflow_id:
            query_params += f"&workflowId={workflow_id}"
        res = self._request("GET", f"executions{query_params}")
        return res.get("data", [])

    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get details for a single execution."""
        return self._request("GET", f"executions/{execution_id}")

    # -------------------------------------------------------------------------
    # Webhook Dispatcher
    # -------------------------------------------------------------------------
    def trigger_webhook(
        self,
        path: str,
        payload: Dict[str, Any],
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """
        Trigger an n8n webhook node with data payload.
        Path should be the webhook path defined in the n8n node (e.g. 'outreach-hook').
        """
        prefix = "webhook-test" if is_test else "webhook"
        endpoint = f"{prefix}/{path.lstrip('/')}"
        return self._request("POST", endpoint, data=payload, is_api=False)

    # -------------------------------------------------------------------------
    # Import / Export
    # -------------------------------------------------------------------------
    def import_workflow_file(self, file_path: str | Path, activate: bool = False) -> Dict[str, Any]:
        """Import a workflow JSON file into n8n."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Workflow file does not exist: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created = self.create_workflow(data)
        workflow_id = created.get("id")
        if activate and workflow_id:
            self.activate_workflow(workflow_id)
        return created

    def export_all_workflows(self, output_dir: str | Path) -> List[Path]:
        """Export all workflows to local directory as JSON files."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        saved = []

        workflows = self.list_workflows()
        for wf_meta in workflows:
            wf_id = wf_meta["id"]
            full_wf = self.get_workflow(wf_id)
            safe_name = "".join(c for c in full_wf.get("name", wf_id) if c.isalnum() or c in ("-", "_")).strip()
            dest = out / f"{safe_name}_{wf_id}.json"
            with open(dest, "w", encoding="utf-8") as f:
                json.dump(full_wf, f, indent=2)
            saved.append(dest)
        return saved


# -----------------------------------------------------------------------------
# CLI Entrypoint
# -----------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="n8n OMEGA Automation CLI")
    parser.add_argument("--url", default="http://localhost:5678", help="n8n base URL")
    parser.add_argument("--api-key", default=os.getenv("N8N_API_KEY", ""), help="n8n API Key")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status", help="Check n8n service connectivity")

    # list
    list_p = subparsers.add_parser("list", help="List registered workflows")
    list_p.add_argument("--active-only", action="store_true", help="Filter active only")

    # import
    import_p = subparsers.add_parser("import", help="Import a workflow JSON file")
    import_p.add_argument("file", help="Path to workflow JSON")
    import_p.add_argument("--activate", action="store_true", help="Activate after import")

    # trigger
    trigger_p = subparsers.add_parser("trigger", help="Send webhook event to n8n")
    trigger_p.add_argument("path", help="Webhook path")
    trigger_p.add_argument("--data", default="{}", help="JSON payload string")
    trigger_p.add_argument("--test", action="store_true", help="Use webhook-test endpoint")

    args = parser.parse_args()
    client = N8nClient(base_url=args.url, api_key=args.api_key)

    if args.command == "status":
        alive = client.health_check()
        print(f"[*] n8n Status at {client.base_url}: {'ONLINE (Health OK)' if alive else 'OFFLINE'}")
        sys.exit(0 if alive else 1)

    elif args.command == "list":
        try:
            wfs = client.list_workflows(active_only=args.active_only)
            print(f"[*] Found {len(wfs)} workflow(s):")
            for w in wfs:
                status = "ACTIVE" if w.get("active") else "INACTIVE"
                print(f"  - [{w.get('id')}] {w.get('name')} ({status})")
        except Exception as e:
            print(f"[!] Failed to list workflows: {e}")
            sys.exit(1)

    elif args.command == "import":
        try:
            res = client.import_workflow_file(args.file, activate=args.activate)
            print(f"[OK] Successfully imported workflow: ID={res.get('id')}, Name={res.get('name')}")
        except Exception as e:
            print(f"[!] Import failed: {e}")
            sys.exit(1)

    elif args.command == "trigger":
        try:
            payload = json.loads(args.data)
            res = client.trigger_webhook(args.path, payload, is_test=args.test)
            print(f"[OK] Webhook triggered successfully: {res}")
        except Exception as e:
            print(f"[!] Webhook trigger failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
