#!/usr/bin/env python3
"""
NSA Ghidra Autonomous Local API Server & Cockpit Bridge
=======================================================
Zero-dependency HTTP REST & Static Server serving the NSA Ghidra Mission Control Cockpit
and exposing real-time endpoints for binary dissection, Sleigh disassembly, P-Code microcode,
control flow graph decompilation, vulnerability hunting, and 12-phase sovereign lifecycle.

Default Port: 8771
Usage:
    python ghidra_api_server.py [--port 8771]
"""

import os
import sys
import json
import argparse
import socket
from typing import Any
import dataclasses
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from ghidra_orchestrator import (
    GhidraConfig,
    GhidraOrchestrator,
    BinaryDissector
)

orchestrator: GhidraOrchestrator = None


class GhidraApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for NSA Ghidra REST API and Cockpit."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Serve Cockpit HTML
        if path in ("/", "/cockpit", "/ghidra_control_cockpit.html"):
            cockpit_path = os.path.join(os.path.dirname(__file__), "ghidra_control_cockpit.html")
            if os.path.exists(cockpit_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cockpit_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self._send_json({"error": "Cockpit HTML not found"}, 404)
                return

        # Health endpoint
        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "service": "nsa-ghidra-autonomous-api",
                "version": "11.1.2_PUBLIC",
                "port": 8771
            })
            return

        # Info endpoint
        if path == "/api/info":
            self._send_json(orchestrator.get_info())
            return

        # Target sample helper
        target_bin = qs.get("path", [os.path.abspath("ghidra/samples/vulnerable_service.exe")])[0]
        if not os.path.exists(target_bin):
            sample_candidate = os.path.abspath("ghidra/samples/vulnerable_service.exe")
            if os.path.exists(sample_candidate):
                target_bin = sample_candidate

        # Analyze endpoint
        if path == "/api/analyze":
            try:
                report = orchestrator.analyze_binary(target_bin)
                self._send_json(dataclasses.asdict(report))
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Disassemble endpoint
        if path == "/api/disassemble":
            try:
                addr = int(qs.get("addr", ["0"])[0], 16) if "addr" in qs else None
                cnt = int(qs.get("count", ["25"])[0])
                instrs = orchestrator.disassemble(target_bin, address=addr, count=cnt)
                self._send_json([dataclasses.asdict(i) for i in instrs])
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Decompile endpoint
        if path == "/api/decompile":
            try:
                func_name = qs.get("func", ["main"])[0]
                decomp = orchestrator.decompile_function(target_bin, func_name)
                self._send_json(dataclasses.asdict(decomp))
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # P-Code endpoint
        if path == "/api/pcode":
            try:
                cnt = int(qs.get("count", ["25"])[0])
                pcode_list = orchestrator.get_pcode(target_bin, count=cnt)
                self._send_json(pcode_list)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Strings endpoint
        if path == "/api/strings":
            try:
                min_len = int(qs.get("min_len", ["4"])[0])
                cat = qs.get("category", [None])[0]
                strings = orchestrator.extract_strings(target_bin, min_len=min_len, category_filter=cat)
                self._send_json([dataclasses.asdict(s) for s in strings])
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Sections endpoint
        if path == "/api/sections":
            try:
                report = orchestrator.analyze_binary(target_bin)
                self._send_json([dataclasses.asdict(s) for s in report.sections])
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Functions endpoint
        if path == "/api/functions":
            try:
                report = orchestrator.analyze_binary(target_bin)
                self._send_json([dataclasses.asdict(fn) for fn in report.functions])
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Vulnerabilities endpoint
        if path == "/api/vulns":
            try:
                audit = orchestrator.audit_vulnerabilities(target_bin)
                self._send_json(audit)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return

        # Scripts endpoint
        if path == "/api/scripts":
            scripts_dir = os.path.abspath("ghidra/scripts")
            files = [f for f in os.listdir(scripts_dir) if f.endswith(".py")] if os.path.exists(scripts_dir) else []
            self._send_json({"scripts": files})
            return

        # Default static file fallback
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        target_bin = body.get("path") if body else None
        if not target_bin or not os.path.exists(target_bin):
            sample_candidate = os.path.abspath("ghidra/samples/vulnerable_service.exe")
            if os.path.exists(sample_candidate):
                target_bin = sample_candidate

        # Run Script
        if path == "/api/run-script":
            script_path = body.get("script", "ghidra/scripts/find_dangerous_apis.py")
            res = orchestrator.run_script(script_path, target_bin)
            self._send_json(res)
            return

        # Do Everything 12-Phase Lifecycle
        if path == "/api/do-everything":
            res = orchestrator.do_everything(target_bin)
            self._send_json(res)
            return

        # Analyze
        if path == "/api/analyze":
            report = orchestrator.analyze_binary(target_bin)
            self._send_json(dataclasses.asdict(report))
            return

        self._send_json({"error": "Unknown POST route"}, 404)

    def _read_json_body(self) -> dict:
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        try:
            raw = self.rfile.read(content_len)
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(port: int = 8771):
    global orchestrator
    orchestrator = GhidraOrchestrator()
    server_address = ("", port)
    httpd = HTTPServer(server_address, GhidraApiHandler)
    print(f"[+] NSA Ghidra Autonomous API Server & Cockpit Bridge listening on http://localhost:{port}")
    print(f"[+] Cockpit UI: http://localhost:{port}/")
    print(f"[+] Health:     http://localhost:{port}/api/health")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down NSA Ghidra API server.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NSA Ghidra Local API Server")
    parser.add_argument("--port", type=int, default=8771, help="Port to listen on (default: 8771)")
    args = parser.parse_args()
    run_server(args.port)
