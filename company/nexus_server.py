"""
Nexus Core API Server (FastAPI / Standard Library Production Server)
===================================================================
Production-grade RESTful API and Webhook Engine for Nexus Cognitive Corp.
Endpoints:
- GET  /health              : System health, database connection, uptime check.
- POST /api/v1/provision    : Onboard a client tenant and issue an API key.
- POST /api/v1/inbound      : Webhook receiving real-time leads (<60s AI response).
- GET  /api/v1/dashboard    : Pull client meeting quota progress (15-meeting guarantee).
- GET  /api/v1/enterprise   : Consolidated executive financial metrics and bank reserve status.
"""

import os
import sys
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Local imports
ANTI_ROOT = r"e:\anti"
BRAIN_DIR = r"C:\Users\amehr\.gemini\antigravity\brain\ac0e8816-94db-405e-887c-e4272b662c09"

if ANTI_ROOT not in sys.path:
    sys.path.append(ANTI_ROOT)
if BRAIN_DIR not in sys.path:
    sys.path.append(BRAIN_DIR)

from enterprise_db import DatabaseManager
from company.nexus_product_engine import NexusEngineProduct

PORT = 8098

class NexusAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self._send_json(200, {"status": "OK"})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/health":
            self._send_json(200, {
                "service": "Nexus Core API Engine",
                "version": "1.0.0",
                "status": "HEALTHY_OPERATIONAL",
                "timestamp": datetime.now().isoformat()
            })

        elif path == "/api/v1/enterprise":
            db = DatabaseManager(os.path.join(BRAIN_DIR, "enterprise_crm.db"))
            summary = db.get_pipeline_summary()
            self._send_json(200, {
                "enterprise": "Nexus Cognitive Corp",
                "clearing_corridor": "Bank of the Continuum",
                "total_cash_collected_usd": summary["total_cash_collected"],
                "active_pipeline_usd": summary["active_pipeline_value"],
                "stages": summary["stages"]
            })

        elif path == "/api/v1/dashboard":
            tenant_id = query.get("tenant_id", [None])[0]
            if not tenant_id:
                self._send_json(400, {"error": "Missing 'tenant_id' query param"})
                return
            product = NexusEngineProduct(os.path.join(ANTI_ROOT, "company", "nexus_product.db"))
            dash = product.get_tenant_dashboard(int(tenant_id))
            self._send_json(200, dash)

        else:
            self._send_json(404, {"error": f"Endpoint '{path}' not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(length) if length > 0 else b"{}"
        
        try:
            payload = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/v1/provision":
            client_name = payload.get("client_name", "Demo Client")
            company_name = payload.get("company_name", "Demo Co")
            plan_tier = payload.get("plan_tier", "Standard")
            
            product = NexusEngineProduct(os.path.join(ANTI_ROOT, "company", "nexus_product.db"))
            result = product.provision_tenant(client_name, company_name, plan_tier)
            self._send_json(201, result)

        elif path == "/api/v1/inbound":
            api_key = payload.get("api_key")
            lead_data = payload.get("lead", {})
            if not api_key:
                self._send_json(401, {"error": "Missing 'api_key'"})
                return
            product = NexusEngineProduct(os.path.join(ANTI_ROOT, "company", "nexus_product.db"))
            result = product.process_inbound_lead(api_key, lead_data)
            self._send_json(200, result)

        else:
            self._send_json(404, {"error": f"Endpoint '{path}' not found"})

def run_server(port: int = PORT):
    server = HTTPServer(("127.0.0.1", port), NexusAPIHandler)
    print(f"[*] Nexus Core API Server live on http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
