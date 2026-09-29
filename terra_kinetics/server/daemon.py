"""
Terra Kinetics: Real-Time Telemetry Streaming Daemon.
Provides lightweight HTTP & SSE/JSON telemetry server for Mission Control Dashboard.
Uses Python standard library to ensure zero runtime dependencies.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import threading
import time
import math
from typing import Dict, Any
from terra_kinetics.runtime.terra_edge_kernel import TerraEdgeKernel
from terra_kinetics.protocol.ukp_schema import RobotMorphology, SensorTelemetryPacket, JointState
from terra_kinetics.adapters.ur_adapter import UniversalRobotsAdapter
from terra_kinetics.model.vla_policy_engine import VLAPolicyEngine


class TelemetryStateStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.step_count = 0
        self.active_robots = 28_000_000
        self.current_torque = 18.4
        self.current_latency_ms = 1.4
        self.current_confidence = 0.985
        self.kernel_state = "NOMINAL"
        self.interventions_total = 0
        self.recent_incidents = []

    def tick(self):
        with self.lock:
            self.step_count += 1
            phase = (self.step_count % 100) / 100.0 * 2 * math.pi
            self.current_torque = round(16.0 + 4.0 * math.sin(phase), 2)
            self.current_latency_ms = round(1.2 + 0.4 * math.cos(phase), 2)

    def trigger_hazard(self):
        with self.lock:
            self.kernel_state = "INTERVENTION_REQUIRED"
            self.current_confidence = 0.325
            self.interventions_total += 1
            incident = {
                "timestamp": time.time_ns(),
                "reason": "Out-of-distribution reflective geometry detected",
                "confidence": 0.325,
            }
            self.recent_incidents.append(incident)
            return incident

    def reset_nominal(self):
        with self.lock:
            self.kernel_state = "NOMINAL"
            self.current_confidence = 0.985

    def get_snapshot(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "step_count": self.step_count,
                "active_robots": self.active_robots,
                "current_torque_nm": self.current_torque,
                "current_latency_ms": self.current_latency_ms,
                "model_confidence": self.current_confidence,
                "kernel_state": self.kernel_state,
                "interventions_total": self.interventions_total,
                "timestamp_ns": time.time_ns(),
            }


telemetry_store = TelemetryStateStore()


class MissionControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file("index.html", "text/html")
        elif self.path == "/digital_twin.html" or self.path == "/twin":
            self._serve_file("digital_twin.html", "text/html")
        elif self.path == "/api/telemetry":
            self._send_json(telemetry_store.get_snapshot())
        elif self.path == "/api/status":
            self._send_json({
                "status": "ONLINE",
                "version": "0.1.0",
                "active_fleet": telemetry_store.active_robots,
                "control_frequency_hz": 200,
            })
        elif self.path == "/api/atlas":
            from sovereign_continuum.global_gdp_atlas import GlobalGdpAtlas
            atlas = GlobalGdpAtlas()
            self._send_json({
                "total_nominal_gdp_t": atlas.TOTAL_GLOBAL_GDP_NOMINAL_T,
                "total_ppp_gdp_t": atlas.TOTAL_GLOBAL_GDP_PPP_T,
                "total_debt_t": atlas.TOTAL_GLOBAL_DEBT_T,
                "top_economies": [c.__dict__ for c in atlas.TOP_20_ECONOMIES[:10]],
                "sectors": [s.__dict__ for s in atlas.GLOBAL_SECTORS],
                "debt_stack": atlas.GLOBAL_DEBT_STACK,
                "blocs": atlas.get_bloc_comparison(),
            })
        elif self.path == "/api/empire":
            from sovereign_continuum.empire_orchestrator import SovereignEmpireOrchestrator
            orch = SovereignEmpireOrchestrator()
            report = orch.execute_planetary_cycle(year=5, quarter=20)
            self._send_json(report.__dict__)
        elif self.path == "/api/skills":
            skills = [
                "empire-capital-allocator",
                "sovereign-chokehold-architect",
                "planetary-fleet-ops",
                "m2m-settlement-clearing",
                "energy-compute-coupling",
                "geopolitical-sovereign-shield",
                "biomanufacturing-scaling",
                "antifragile-red-team",
                "sovereign-wealth-syndication",
                "sovereign-banking-engine",
            ]
            skills_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".agent", "skills")
            skill_status = []
            for s in skills:
                p = os.path.join(skills_dir, s, "SKILL.md")
                skill_status.append({
                    "skill_name": s,
                    "verified": os.path.exists(p),
                    "size_bytes": os.path.getsize(p) if os.path.exists(p) else 0,
                })
            self._send_json({"total_skills": len(skills), "skills": skill_status})
        elif self.path == "/api/banking":
            from sovereign_continuum.banking.autonomous_sovereign_bank import BankOfTheContinuum
            bank = BankOfTheContinuum()
            self._send_json(bank.generate_consolidated_banking_audit())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/hazard":
            incident = telemetry_store.trigger_hazard()
            self._send_json({"status": "HAZARD_TRIGGERED", "incident": incident})
        elif self.path == "/api/reset":
            telemetry_store.reset_nominal()
            self._send_json({"status": "RESET_NOMINAL"})
        else:
            self.send_error(404, "Not Found")

    def _serve_file(self, filename: str, content_type: str):
        dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "dashboard")
        filepath = os.path.join(dashboard_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, f"File {filename} not found")

    def _send_json(self, data: Dict[str, Any]):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Suppress noisy standard request logging in testing/daemon
        pass


def run_daemon(host: str = "127.0.0.1", port: int = 8088) -> HTTPServer:
    # Start background telemetry state ticking thread
    def ticker_worker():
        while True:
            telemetry_store.tick()
            time.sleep(0.05)  # 20 Hz state updates

    t = threading.Thread(target=ticker_worker, daemon=True)
    t.start()

    server = HTTPServer((host, port), MissionControlHandler)
    return server


if __name__ == "__main__":
    port = 8088
    print(f"[*] Starting Terra Kinetics Telemetry Daemon at http://127.0.0.1:{port}")
    print("[*] Press Ctrl+C to terminate.")
    server = run_daemon("127.0.0.1", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down daemon gracefully.")
        server.server_close()
