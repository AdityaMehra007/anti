#!/usr/bin/env python3
"""
Apache Airflow Autonomous REST API Server & Cockpit Bridge
=========================================================
High-speed HTTP daemon serving Airflow v1 REST API endpoints and hosting
the interactive Airflow Mission Control Cockpit.

Default Port: 8775
Usage:
    python airflow_api_server.py [--port 8775]
"""

from __future__ import annotations

import os
import sys
import json
import socket
import argparse
import logging
from typing import Any, Dict
from dataclasses import asdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from airflow_orchestrator import AirflowClient, AirflowConfig, AirflowOrchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("airflow_api_server")

client = AirflowClient()
COCKPIT_HTML_FILE = "airflow_control_cockpit.html"


class AirflowApiHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler for Airflow API endpoints and Cockpit UI."""

    def _json_response(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Cockpit UI route
        if path in ("/", "/cockpit"):
            cockpit_path = os.path.join(os.path.dirname(__file__), COCKPIT_HTML_FILE)
            if os.path.exists(cockpit_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cockpit_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self._json_response({"error": "Cockpit HTML file not found."}, status=404)
                return

        # REST API Routes
        if path == "/api/v1/health":
            self._json_response(client.get_health())
        elif path == "/api/v1/version":
            self._json_response({
                "version": client.mock_engine.version,
                "executor": client.mock_engine.executor_type,
                "metadb": client.mock_engine.metadb_version,
                "python": sys.version
            })
        elif path == "/api/v1/dags":
            self._json_response({"dags": client.list_dags(), "total_entries": len(client.mock_engine.dags)})
        elif path.startswith("/api/v1/dags/") and "/dagRuns" in path:
            parts = path.strip("/").split("/")
            dag_id = parts[3]
            runs = client.list_dag_runs(dag_id)
            self._json_response({"dag_runs": runs, "total_entries": len(runs)})
        elif path.startswith("/api/v1/dags/"):
            dag_id = path.strip("/").split("/")[3]
            try:
                dag = client.get_dag(dag_id)
                dag["topological_order"] = client.mock_engine.topological_sort_dag(dag_id)
                self._json_response(dag)
            except Exception as e:
                self._json_response({"error": str(e)}, status=404)
        elif path == "/api/v1/variables":
            self._json_response({"variables": client.list_variables()})
        elif path == "/api/v1/connections":
            self._json_response({"connections": client.list_connections()})
        elif path == "/api/v1/pools":
            self._json_response({"pools": client.list_pools()})
        elif path == "/api/v1/datasets":
            self._json_response({"datasets": client.list_datasets()})
        elif path == "/api/v1/xcom":
            entries = [asdict(x) for x in client.mock_engine.xcom_store]
            self._json_response({"xcom_entries": entries, "total_entries": len(entries)})
        elif path == "/api/telemetry":
            active_dags = [d for d in client.mock_engine.dags.values() if not d.is_paused]
            total_runs = sum(len(r) for r in client.mock_engine.dag_runs.values())
            self._json_response({
                "status": "ONLINE",
                "version": client.mock_engine.version,
                "executor": client.mock_engine.executor_type,
                "scheduler_heartbeat": client.mock_engine.scheduler_heartbeat,
                "active_workers": client.mock_engine.active_workers_count,
                "active_dags": len(active_dags),
                "total_dags": len(client.mock_engine.dags),
                "total_dag_runs": total_runs,
                "total_pools": len(client.mock_engine.pools),
                "total_datasets": len(client.mock_engine.datasets),
                "pools": client.list_pools()
            })
        elif path == "/api/audit":
            audit = client.mock_engine.audit_security_and_best_practices()
            self._json_response(audit)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if path.startswith("/api/v1/dags/") and path.endswith("/dagRuns"):
            dag_id = path.strip("/").split("/")[3]
            conf = data.get("conf", {})
            try:
                run = client.trigger_dag(dag_id, conf=conf)
                self._json_response(run, status=201)
            except Exception as e:
                self._json_response({"error": str(e)}, status=400)
        elif path == "/api/v1/variables":
            k = data.get("key", "")
            v = data.get("val", "")
            desc = data.get("description", "")
            if not k:
                self._json_response({"error": "Missing variable key"}, status=400)
                return
            res = client.set_variable(k, v, description=desc)
            self._json_response(res, status=201)
        elif path == "/api/v1/datasets/events":
            uri = data.get("uri", "")
            source = data.get("source", "api")
            if not uri:
                self._json_response({"error": "Missing dataset uri"}, status=400)
                return
            client.emit_dataset_event(uri, source=source)
            self._json_response({"status": "EMITTED", "uri": uri, "source": source}, status=200)
        elif path == "/api/lifecycle/do-everything":
            orchestrator = AirflowOrchestrator()
            manifest = orchestrator.run_lifecycle()
            self._json_response(manifest)
        else:
            self._json_response({"error": f"Endpoint '{path}' not found."}, status=404)

    def do_PATCH(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if path.startswith("/api/v1/dags/"):
            dag_id = path.strip("/").split("/")[3]
            is_paused = data.get("is_paused", True)
            try:
                dag = client.mock_engine.toggle_dag_pause(dag_id, is_paused)
                self._json_response(asdict(dag))
            except Exception as e:
                self._json_response({"error": str(e)}, status=400)
        else:
            self._json_response({"error": f"Endpoint '{path}' not found."}, status=404)


def is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(preferred: int = 8775, max_attempts: int = 10) -> int:
    for p in range(preferred, preferred + max_attempts):
        if is_port_free(p):
            return p
    return preferred


def run_server(port: int = 8775):
    chosen_port = find_free_port(port)
    server_address = ("127.0.0.1", chosen_port)
    httpd = HTTPServer(server_address, AirflowApiHandler)
    print("=" * 70)
    print("  APACHE AIRFLOW AUTONOMOUS REST API SERVER & COCKPIT ONLINE")
    print("=" * 70)
    print(f"  Local Endpoint:   http://localhost:{chosen_port}")
    print(f"  Mission Cockpit:  http://localhost:{chosen_port}/cockpit")
    print(f"  API Health:       http://localhost:{chosen_port}/api/v1/health")
    print(f"  Telemetry Feed:   http://localhost:{chosen_port}/api/telemetry")
    print("=" * 70)
    print("  Press Ctrl+C to stop server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down Airflow API server gracefully.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apache Airflow Autonomous API Server")
    parser.add_argument("--port", type=int, default=8775, help="HTTP Server Port (default: 8775)")
    args = parser.parse_args()
    run_server(args.port)
