"""
Unit and Integration Test Suite for Plane Advanced Board Engine and Webhook Reactor.
Validates departmental board provisioning, sprint cycle calculations, and webhook event processing.
"""

import json
import threading
from datetime import datetime, timedelta
from http.server import HTTPServer
import unittest
from urllib.request import Request, urlopen

try:
    from omega.integrations.plane_connector import PlaneClient
    from omega.orchestration.plane_boards import PlaneBoardEngine, DEPARTMENT_PROJECTS
    from omega.orchestration.plane_webhook_server import PlaneWebhookServer, WebhookHandler
except ImportError:
    PlaneClient = None
    PlaneBoardEngine = None
    DEPARTMENT_PROJECTS = []
    PlaneWebhookServer = None
    WebhookHandler = None


class PlaneAdvancedTestCase(unittest.TestCase):
    """Test case for PlaneBoardEngine and PlaneWebhookServer."""

    def test_imports_available(self):
        self.assertIsNotNone(PlaneBoardEngine, "PlaneBoardEngine should be importable")
        self.assertIsNotNone(PlaneWebhookServer, "PlaneWebhookServer should be importable")
        self.assertGreater(len(DEPARTMENT_PROJECTS), 0, "Department projects should be configured")

    def test_sprint_cycle_date_generation(self):
        if PlaneBoardEngine is None:
            self.skipTest("PlaneBoardEngine not yet implemented")

        client = PlaneClient(dry_run=True)
        engine = PlaneBoardEngine(client=client)

        now = datetime.now()
        cycles = engine.calculate_sprint_cycles(sprint_count=3, sprint_days=14, start_date=now)

        self.assertEqual(len(cycles), 3)
        self.assertEqual(cycles[0]["name"], "Sprint 1")
        self.assertEqual(cycles[1]["name"], "Sprint 2")
        self.assertEqual(cycles[2]["name"], "Sprint 3")

        # Verify start & end dates
        s1_start = datetime.strptime(cycles[0]["start_date"], "%Y-%m-%d").date()
        s1_end = datetime.strptime(cycles[0]["end_date"], "%Y-%m-%d").date()
        self.assertEqual((s1_end - s1_start).days, 14)

        s2_start = datetime.strptime(cycles[1]["start_date"], "%Y-%m-%d").date()
        self.assertEqual(s2_start, s1_end)

    def test_provision_department_projects_dry_run(self):
        if PlaneBoardEngine is None:
            self.skipTest("PlaneBoardEngine not yet implemented")

        client = PlaneClient(dry_run=True)
        engine = PlaneBoardEngine(client=client)

        results = engine.provision_department_projects(workspace_slug="omega")
        self.assertEqual(len(results), len(DEPARTMENT_PROJECTS))
        for res in results:
            self.assertTrue(res.get("dry_run"))
            self.assertIn("identifier", res)

    def test_webhook_event_processing(self):
        if PlaneWebhookServer is None:
            self.skipTest("PlaneWebhookServer not yet implemented")

        events_received = []

        def test_callback(event_type, payload):
            events_received.append((event_type, payload))

        server = PlaneWebhookServer(port=0, host="127.0.0.1", callback=test_callback)
        server.start_in_thread()
        port = server.server_port
        base_url = f"http://127.0.0.1:{port}"

        try:
            # 1. Test health endpoint
            req = Request(f"{base_url}/health", method="GET")
            with urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertEqual(data.get("status"), "healthy")

            # 2. Test webhook event delivery
            payload = {
                "event": "issue.updated",
                "data": {
                    "issue_id": "iss-42",
                    "title": "Quantum Execution Engine",
                    "state": "In Progress"
                }
            }
            req = Request(
                f"{base_url}/webhook",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                resp_data = json.loads(resp.read().decode())
                self.assertEqual(resp_data.get("status"), "processed")

            self.assertEqual(len(events_received), 1)
            self.assertEqual(events_received[0][0], "issue.updated")
            self.assertEqual(events_received[0][1]["data"]["issue_id"], "iss-42")

        finally:
            server.stop()

    def test_empire_orchestrator_plane_sync(self):
        from sovereign_continuum.empire_orchestrator import SovereignEmpireOrchestrator
        orch = SovereignEmpireOrchestrator()
        result = orch.sync_to_plane_hub(workspace_slug="omega", dry_run=True)
        self.assertEqual(result["workspace"], "omega")
        self.assertEqual(result["status"], "synchronized")
        self.assertTrue(result["dry_run"])
        self.assertGreaterEqual(result["total_synced"], 1)


if __name__ == "__main__":
    unittest.main()
