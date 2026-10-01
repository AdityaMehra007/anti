"""
Unit and Integration Test Suite for Plane CE REST API Connector & Autonomous Dispatcher.
Validates client methods, error codes, and dry-run behaviors using a mock HTTP server.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import unittest
from urllib.parse import urlparse

# Module under test (will be imported once written)
try:
    from omega.integrations.plane_connector import (
        PlaneClient,
        PlaneAPIError,
        PlaneAuthenticationError,
        PlaneNotFoundError,
    )
except ImportError:
    PlaneClient = None
    PlaneAPIError = Exception
    PlaneAuthenticationError = Exception
    PlaneNotFoundError = Exception

try:
    from omega.orchestration.plane_dispatcher import PlaneDispatcher
except ImportError:
    PlaneDispatcher = None


class MockPlaneHandler(BaseHTTPRequestHandler):
    """Mock HTTP handler returning realistic Plane CE API responses."""

    def log_message(self, format, *args):
        # Silence HTTP server logs during tests
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/instances/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"instance_id": "plane-test-instance", "version": "v1.4.2"}).encode())
            return

        if path == "/api/workspaces/":
            auth = self.headers.get("x-api-key") or self.headers.get("Authorization")
            if not auth:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Authentication credentials were not provided."}).encode())
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            workspaces = [{"id": "ws-1", "name": "OMEGA", "slug": "omega"}]
            self.wfile.write(json.dumps(workspaces).encode())
            return

        if path == "/api/workspaces/omega/projects/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            projects = [{"id": "proj-1", "name": "Autonomous Operations", "identifier": "AO"}]
            self.wfile.write(json.dumps(projects).encode())
            return

        if path == "/api/workspaces/omega/projects/proj-1/states/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            states = [
                {"id": "st-1", "name": "Backlog", "group": "backlog"},
                {"id": "st-2", "name": "In Progress", "group": "started"},
                {"id": "st-3", "name": "Done", "group": "completed"},
            ]
            self.wfile.write(json.dumps(states).encode())
            return

        if path == "/api/workspaces/omega/projects/proj-1/issues/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            issues = [{"id": "iss-1", "name": "Implement Core Gateway", "state": "st-1", "priority": "high"}]
            self.wfile.write(json.dumps(issues).encode())
            return

        if path == "/api/nonexistent/":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode()) if length > 0 else {}

        if path == "/api/workspaces/":
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": "ws-new", "name": body.get("name"), "slug": body.get("slug")}).encode())
            return

        if path == "/api/workspaces/omega/projects/":
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": "proj-new", "name": body.get("name"), "identifier": body.get("identifier")}).encode())
            return

        if path == "/api/workspaces/omega/projects/proj-1/issues/":
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": "iss-new",
                "name": body.get("name"),
                "description_html": body.get("description_html", ""),
                "state": body.get("state"),
                "priority": body.get("priority", "medium")
            }).encode())
            return

        if path == "/api/workspaces/omega/projects/proj-1/cycles/":
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": "cyc-new",
                "name": body.get("name"),
                "start_date": body.get("start_date"),
                "end_date": body.get("end_date")
            }).encode())
            return

        self.send_response(400)
        self.end_headers()

    def do_PATCH(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode()) if length > 0 else {}

        if path.startswith("/api/workspaces/omega/projects/proj-1/issues/iss-1"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": "iss-1",
                "name": body.get("name", "Implement Core Gateway"),
                "state": body.get("state", "st-3")
            }).encode())
            return

        self.send_response(404)
        self.end_headers()


class PlaneIntegrationTestCase(unittest.TestCase):
    """Validates the PlaneClient against the mock server."""

    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), MockPlaneHandler)
        cls.port = cls.server.server_port
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_imports_exist(self):
        self.assertIsNotNone(PlaneClient, "PlaneClient should be importable from omega.integrations.plane_connector")

    def test_health_check(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key")
        health = client.health_check()
        self.assertEqual(health.get("version"), "v1.4.2")

    def test_auth_failure(self):
        client = PlaneClient(base_url=self.base_url, api_key="")
        with self.assertRaises(PlaneAuthenticationError):
            client.list_workspaces()

    def test_list_and_create_workspaces(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key")
        ws_list = client.list_workspaces()
        self.assertEqual(len(ws_list), 1)
        self.assertEqual(ws_list[0]["slug"], "omega")

        created = client.create_workspace("Research Lab", "research-lab")
        self.assertEqual(created["id"], "ws-new")
        self.assertEqual(created["slug"], "research-lab")

    def test_list_and_create_projects(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key")
        projects = client.list_projects("omega")
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["identifier"], "AO")

        new_proj = client.create_project("omega", "Agent Fleet", "AF")
        self.assertEqual(new_proj["identifier"], "AF")

    def test_issue_lifecycle(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key")
        states = client.list_states("omega", "proj-1")
        self.assertEqual(len(states), 3)

        new_issue = client.create_issue("omega", "proj-1", "Deploy Container", "<p>Specs</p>", state_id="st-1", priority="urgent")
        self.assertEqual(new_issue["id"], "iss-new")
        self.assertEqual(new_issue["priority"], "urgent")

        updated = client.update_issue("omega", "proj-1", "iss-1", state="st-3")
        self.assertEqual(updated["state"], "st-3")

    def test_create_cycle(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key")
        cycle = client.create_cycle("omega", "proj-1", "Sprint 1", "2026-10-01", "2026-10-15")
        self.assertEqual(cycle["id"], "cyc-new")
        self.assertEqual(cycle["name"], "Sprint 1")

    def test_dry_run_mode(self):
        client = PlaneClient(base_url=self.base_url, api_key="test-key", dry_run=True)
        # In dry run mode, network mutations must return simulated objects without network errors
        sim_issue = client.create_issue("omega", "proj-1", "Simulated Issue", "Dry Run")
        self.assertTrue(sim_issue.get("dry_run"))
        self.assertEqual(sim_issue.get("name"), "Simulated Issue")

    def test_dispatcher_parse_tasks(self):
        if PlaneDispatcher is None:
            self.skipTest("PlaneDispatcher not yet implemented")
        client = PlaneClient(base_url=self.base_url, api_key="test-key", dry_run=True)
        dispatcher = PlaneDispatcher(client=client)
        sample_md = """
# Tasks
- [ ] Task Alpha: Build Core Gateway (Priority: high)
- [x] Task Beta: Setup Config Database
        """
        parsed = dispatcher.parse_markdown_tasks(sample_md)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["name"], "Task Alpha: Build Core Gateway")
        self.assertFalse(parsed[0]["completed"])
        self.assertEqual(parsed[0]["priority"], "high")
        self.assertTrue(parsed[1]["completed"])


if __name__ == "__main__":
    unittest.main()
