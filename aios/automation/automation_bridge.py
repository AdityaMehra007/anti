#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Automation & Workflow Engine Bridge
Bridges the AIOS command center with local n8n automation pipelines on port 5678.
Provides deterministic trigger handlers, audit logging into master.db, and scheduled jobs.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Optional

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

try:
    import db
except ImportError:
    db = None

N8N_BASE_URL = os.environ.get("N8N_BASE_URL", "http://127.0.0.1:5678")


class AutomationBridge:
    def __init__(self, base_url: str = N8N_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _http_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Performs a standard HTTP request to the automation engine."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        payload = json.dumps(data).encode("utf-8") if data is not None else None
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=payload, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=15) as res:
            resp_body = res.read().decode("utf-8")
            return json.loads(resp_body) if resp_body else {}

    def is_healthy(self) -> bool:
        """Checks if the automation engine is active."""
        try:
            res = self._http_request("GET", "healthz")
            return res.get("status") in ["ok", "healthy", "ONLINE"] or "healthy" in str(res).lower()
        except Exception:
            return False

    def list_workflows(self) -> List[Dict[str, Any]]:
        """Returns all registered automation workflows from API or local definitions."""
        try:
            res = self._http_request("GET", "api/v1/workflows")
            data = res.get("data", [])
            if data:
                return data
        except Exception:
            pass

        # Local workflow discovery fallback
        wf_dir = Path("E:/anti/n8n/workflows")
        discovered = []
        if wf_dir.exists():
            for p in sorted(wf_dir.glob("*.json")):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        discovered.append({
                            "id": p.stem,
                            "name": cfg.get("name", p.stem.replace("_", " ").title()),
                            "active": True,
                            "path": str(p)
                        })
                except Exception:
                    pass
        return discovered

    def trigger_webhook(self, webhook_path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Triggers a designated workflow webhook and records an audit log entry."""
        endpoint = f"webhook/{webhook_path.lstrip('/')}"
        try:
            res = self._http_request("POST", endpoint, payload)
            if db:
                db.log_audit(
                    "AUTOMATION_BRIDGE",
                    "TRIGGER_WEBHOOK",
                    "AUTOMATION",
                    f"Path: {webhook_path} | Status: Success",
                    "INFO"
                )
            return {"status": "SUCCESS", "response": res}
        except Exception as e:
            if db:
                db.log_audit(
                    "AUTOMATION_BRIDGE",
                    "TRIGGER_WEBHOOK",
                    "AUTOMATION",
                    f"Path: {webhook_path} | Error: {e}",
                    "ERROR"
                )
            return {"status": "ERROR", "error": str(e)}

    def execute_workflow(self, workflow_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Directly executes a registered workflow by identifier."""
        endpoint = f"workflows/{workflow_id}/execute"
        try:
            res = self._http_request("POST", endpoint, input_data or {})
            if db:
                db.log_audit(
                    "AUTOMATION_BRIDGE",
                    "EXECUTE_WORKFLOW",
                    "AUTOMATION",
                    f"Workflow: {workflow_id} | Status: Success",
                    "INFO"
                )
            return {"status": "SUCCESS", "response": res}
        except Exception as e:
            if db:
                db.log_audit(
                    "AUTOMATION_BRIDGE",
                    "EXECUTE_WORKFLOW",
                    "AUTOMATION",
                    f"Workflow: {workflow_id} | Error: {e}",
                    "ERROR"
                )
            return {"status": "ERROR", "error": str(e)}

    def run_health_sync_dag(self) -> Dict[str, Any]:
        """Syncs latest system telemetry from gateway into automation and audit trails."""
        return self.trigger_webhook("omega-events", {
            "source": "AIOS_HEALTH_SYNC",
            "action": "TELEMETRY_REFRESH",
            "timestamp": time.time(),
            "target": "master.db"
        })

    def run_lead_outreach_dag(self, recipient: str, company: str, source: str = "OMEGA_CRM") -> Dict[str, Any]:
        """Dispatches an autonomous outreach trigger."""
        return self.trigger_webhook("outreach-dispatch", {
            "recipient_email": recipient,
            "company": company,
            "source": source
        })


if __name__ == "__main__":
    bridge = AutomationBridge()
    print("Testing Automation Engine Bridge on", N8N_BASE_URL)
    healthy = bridge.is_healthy()
    print("Engine Health:", "[ONLINE]" if healthy else "[OFFLINE]")
    if healthy:
        wfs = bridge.list_workflows()
        print(f"Discovered {len(wfs)} active workflows:")
        for w in wfs:
            print(f"  * [{w.get('id')}] {w.get('name')}")
        
        # Test event sync trigger
        print("\nTriggering sample telemetry event DAG...")
        res = bridge.run_health_sync_dag()
        print("Result:", res)
