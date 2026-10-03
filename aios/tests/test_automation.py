#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Automation & Workflow Integration Test Suite
Zero-dependency Python Standard Library test suite verifying:
- n8n engine connection and health check
- Workflow discovery across local pipeline definitions
- Webhook dispatching and payload acknowledgement
- Scheduler execution cycles and WAL optimizations
- Master SQLite audit logging
"""

import sys
import os
import json
import time
import threading
import unittest
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "automation"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

from automation_bridge import AutomationBridge
from scheduler import AutomationScheduler
import db

TEST_N8N_PORT = 5679

class MockN8nHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/webhook/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ACKNOWLEDGED", "received": true}')
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass


class TestAutomationPipeline(unittest.TestCase):
    mock_server = None

    @classmethod
    def setUpClass(cls):
        cls.bridge = AutomationBridge()
        cls.scheduler = AutomationScheduler(check_interval_sec=60)
        
        # If live n8n is offline, boot mock server on TEST_N8N_PORT
        if not cls.bridge.is_healthy():
            cls.mock_server = HTTPServer(("127.0.0.1", TEST_N8N_PORT), MockN8nHandler)
            cls.server_thread = threading.Thread(target=cls.mock_server.serve_forever, daemon=True)
            cls.server_thread.start()
            time.sleep(0.1)
            cls.bridge = AutomationBridge(base_url=f"http://127.0.0.1:{TEST_N8N_PORT}")

    @classmethod
    def tearDownClass(cls):
        if cls.mock_server:
            cls.mock_server.shutdown()
            cls.mock_server.server_close()

    def test_01_engine_health(self):
        """Verifies connection to automation engine on port 5678 or test mock."""
        self.assertTrue(self.bridge.is_healthy(), "Automation engine should be online")

    def test_02_workflow_discovery(self):
        """Verifies discovery of registered automation workflows."""
        workflows = self.bridge.list_workflows()
        self.assertIsInstance(workflows, list)
        self.assertGreater(len(workflows), 0, "Should discover at least 1 registered workflow")
        wf_ids = [w.get("id") for w in workflows]
        self.assertTrue(any("health" in wid or "webhook" in wid or "email" in wid for wid in wf_ids))

    def test_03_webhook_dispatch(self):
        """Verifies dispatching an event to the inbound webhook pipeline."""
        res = self.bridge.trigger_webhook("omega-events", {
            "source": "UNIT_TEST_AGENT",
            "action": "TEST_PIPELINE",
            "test_flag": True
        })
        self.assertEqual(res.get("status"), "SUCCESS")
        self.assertIn("response", res)
        self.assertEqual(res["response"].get("status"), "ACKNOWLEDGED")

    def test_04_scheduler_cycle(self):
        """Verifies scheduler single step executes without errors."""
        try:
            self.scheduler.step()
        except Exception as e:
            self.fail(f"Scheduler step raised unexpected exception: {e}")

    def test_05_audit_trail_recorded(self):
        """Verifies automation triggers write structured entries into master.db."""
        with db.get_connection() as con:
            cur = con.execute(
                "SELECT * FROM audit_logs WHERE actor = 'AUTOMATION_BRIDGE' ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
            self.assertIsNotNone(row, "Audit log should contain AUTOMATION_BRIDGE records")
            self.assertEqual(row["category"], "AUTOMATION")


if __name__ == "__main__":
    unittest.main()
