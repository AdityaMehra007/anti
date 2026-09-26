#!/usr/bin/env python3
"""
================================================================================
GLOBAL DOLLAR ECONOMY OS -- WEB APPLICATION SERVER & REST API
================================================================================
Founder: Adi | Location: Bangalore, India
Mission: Local, dependency-free full-stack server hosting the interactive
         Global Dollar OS Command Center web app on http://localhost:8000.
================================================================================
"""

import sys
import os
import json
import csv
import http.server
import socketserver
import webbrowser
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
REPORTS_DIR = BASE_DIR / "reports"
PIPELINE_CSV = BASE_DIR / "pipeline_tracker.csv"
PORT = 8000

class GlobalDollarRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Inspect actual live ledgers
            tracked_apps = []
            apps_csv = BASE_DIR / "job_applications.csv"
            if apps_csv.exists():
                try:
                    with open(apps_csv, "r", encoding="utf-8", errors="ignore") as f:
                        tracked_apps = list(csv.DictReader(f))
                except Exception:
                    pass

            active_jobs = []
            jobs_csv = BASE_DIR / "data" / "jobs_master.csv"
            if jobs_csv.exists():
                try:
                    with open(jobs_csv, "r", encoding="utf-8", errors="ignore") as f:
                        active_jobs = list(csv.DictReader(f))
                except Exception:
                    pass

            ready_count = sum(1 for a in tracked_apps if a.get("Status") == "READY_TO_APPLY")
            applied_count = sum(1 for a in tracked_apps if a.get("Status") == "APPLIED")
            sales_excluded_count = sum(1 for j in active_jobs if j.get("Priority") == "EXCLUDED_SALES_RISK")
            immediate_target_count = sum(1 for j in active_jobs if "Immediate Target" in j.get("Priority", ""))

            data = {
                "system": "ADI OMNI CAREER OS",
                "version": "OMNI-X / PRODUCTION",
                "candidate": "Aditya Mehra (Adi)",
                "positioning": "AI-enabled Business Operations / Business Analyst / Strategy & Operations",
                "location": "Bengaluru, Karnataka, India",
                "metrics": {
                    "total_tracked_applications": len(tracked_apps),
                    "ready_to_apply_count": ready_count,
                    "applied_count": applied_count,
                    "active_verified_jobs": len(active_jobs),
                    "immediate_p0_targets": immediate_target_count,
                    "sales_excluded_roles": sales_excluded_count,
                    "verified_network_connections": 9223,
                    "matched_gatekeepers": 96
                },
                "status": "OPERATIONAL",
                "timestamp": str(datetime.now().isoformat())
            }
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
        elif self.path == "/api/career":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            apps_csv = BASE_DIR / "job_applications.csv"
            tracked_apps = []
            if apps_csv.exists():
                try:
                    with open(apps_csv, "r", encoding="utf-8", errors="ignore") as f:
                        tracked_apps = list(csv.DictReader(f))
                except Exception as e:
                    tracked_apps = [{"error": str(e)}]
            self.wfile.write(json.dumps({"applications": tracked_apps}, indent=2).encode("utf-8"))
        else:
            super().do_GET()

def start_server():
    print("=" * 78)
    print("  GLOBAL DOLLAR ECONOMY OS -- WEB APPLICATION SERVER")
    print("=" * 78)
    print(f"  Hosting Dashboard on: http://localhost:{PORT}")
    print(f"  Serving Static UI from: {STATIC_DIR}")
    print("=" * 78)
    print("  Press Ctrl+C to stop the web server.")
    
    with socketserver.TCPServer(("", PORT), GlobalDollarRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down web application server...")

if __name__ == "__main__":
    start_server()
