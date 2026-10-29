#!/usr/bin/env python3
r"""
Apache Arrow Autonomous Local REST API Server
=============================================
HTTP REST bridge on port 8775 exposing Apache Arrow telemetry, columnar table creation,
Acero vectorized compute queries, C Data Interface ABI verification, Arrow Flight RPC catalog,
Parquet optimization, microsecond benchmarks, and serving the interactive Mission Control Cockpit.

Default Port: 8775
Usage:
    python arrow_api_server.py [--port 8775]
"""

from __future__ import annotations

import os
import sys
import json
import socket
import argparse
import logging
from typing import Any, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from arrow_orchestrator import ArrowOrchestrator, PYARROW_VERSION

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("arrow_api_server")

orchestrator = ArrowOrchestrator()


class ArrowApiHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for Apache Arrow REST endpoints and Cockpit UI."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self._set_headers(204)

    def _read_json_body(self) -> Dict[str, Any]:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw_body = self.rfile.read(content_length)
                return json.loads(raw_body.decode("utf-8"))
        except Exception as e:
            logger.warning(f"Failed to parse request JSON: {e}")
        return {}

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Serve Cockpit UI at root or /cockpit
        if path in ["/", "/cockpit", "/index.html"]:
            cockpit_path = os.path.join(orchestrator.workspace_dir, "arrow_control_cockpit.html")
            if os.path.exists(cockpit_path):
                self._set_headers(200, "text/html; charset=utf-8")
                with open(cockpit_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"arrow_control_cockpit.html not found.")
                return

        # API Endpoints
        if path == "/api/arrow/info":
            res = orchestrator.get_telemetry()
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/schemas":
            res = {
                "registered_schemas": list(orchestrator.schemas_cache.keys()),
                "schemas": orchestrator.schemas_cache,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/tables":
            tables_summary = []
            for name, t in orchestrator.tables_cache.items():
                if hasattr(t, "schema"):
                    tables_summary.append({
                        "name": name,
                        "num_rows": t.num_rows,
                        "num_columns": t.num_columns,
                        "memory_bytes": t.nbytes,
                        "columns": [f.name for f in t.schema],
                    })
                else:
                    tables_summary.append({
                        "name": name,
                        "num_rows": len(t) if isinstance(t, list) else 0,
                    })
            self._set_headers(200)
            self.wfile.write(json.dumps({"tables": tables_summary}, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/flight":
            res = orchestrator.get_flight_catalog()
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/manifest":
            manifest_path = os.path.join(orchestrator.manifest_dir, "arrow_do_everything_manifest.json")
            if os.path.exists(manifest_path):
                self._set_headers(200)
                with open(manifest_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Manifest not found. Run do-everything first."}).encode("utf-8"))
            return

        # Default static file serving fallback
        super().do_GET()

    def do_POST(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        body = self._read_json_body()

        if path == "/api/arrow/create":
            dataset = body.get("dataset", "trades")
            rows = int(body.get("rows", 25000))
            if dataset == "trades":
                t = orchestrator.generate_trades_table(num_rows=rows)
                num_rows = t.num_rows if hasattr(t, "num_rows") else len(t)
            else:
                t = orchestrator.generate_iot_telemetry_table(num_rows=rows)
                num_rows = t.num_rows if hasattr(t, "num_rows") else len(t)

            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "dataset": dataset,
                "rows_created": num_rows,
                "cached": True,
            }, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/slice":
            offset = int(body.get("offset", 100))
            length = int(body.get("length", 500))
            res = orchestrator.demonstrate_zero_copy_slicing(offset=offset, length=length)
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/compute":
            table_name = body.get("table", "trades")
            filter_col = body.get("col", "price")
            filter_op = body.get("op", ">")
            filter_val = float(body.get("val", 200.0))
            group_col = body.get("group", "symbol")

            res = orchestrator.execute_vectorized_query(
                table_name=table_name,
                filter_col=filter_col,
                filter_op=filter_op,
                filter_val=filter_val,
                group_col=group_col,
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/c-data":
            res = orchestrator.run_c_data_interface_abi()
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/ipc":
            table_name = body.get("table", "trades")
            filename = body.get("filename")
            res = orchestrator.export_ipc_stream(table_name=table_name, filename=filename)
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/parquet":
            table_name = body.get("table", "trades")
            compression = body.get("compression", "snappy")
            filename = body.get("filename")
            res = orchestrator.export_parquet(table_name=table_name, filename=filename, compression=compression)
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/flight/do-get":
            ticket = body.get("ticket", "/datasets/trades")
            res = orchestrator.flight_do_get(ticket)
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/benchmark":
            rows = int(body.get("rows", 50000))
            res = orchestrator.run_benchmarks(num_rows=rows)
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        elif path == "/api/arrow/do-everything":
            res = orchestrator.run_all_phases()
            self._set_headers(200)
            self.wfile.write(json.dumps(res, default=str).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"Endpoint '{path}' not found."}).encode("utf-8"))


def find_free_port(preferred: int = 8775, max_attempts: int = 10) -> int:
    """Find available port if preferred port is already bound."""
    for port in range(preferred, preferred + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return preferred


def run_server(port: int = 8775) -> None:
    actual_port = find_free_port(port)
    server_address = ("127.0.0.1", actual_port)
    httpd = HTTPServer(server_address, ArrowApiHandler)
    logger.info(f"Apache Arrow API Server running on http://127.0.0.1:{actual_port}")
    logger.info(f"Interactive Cockpit available at http://127.0.0.1:{actual_port}/cockpit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopping Apache Arrow API Server...")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apache Arrow Autonomous API Server")
    parser.add_argument("--port", type=int, default=8775, help="Port to listen on (default: 8775)")
    args = parser.parse_args()
    run_server(args.port)
