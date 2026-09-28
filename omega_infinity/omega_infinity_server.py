"""
OMEGA INFINITY (Ω-OS) — UNIFIED GLASS COCKPIT WEB SERVER
Fast, zero-dependency standard library HTTP server delivering REST APIs
and serving the real-time Sovereign Enterprise Glass Cockpit.
"""

import os
import sys
import json
import time
import urllib.parse
from dataclasses import asdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel, CONSTITUTIONAL_MODES
from omega_infinity.omega_vectis_adapter import VectisEnterpriseAdapter
from omega_infinity.omega_intel_engine import IntelSearchEngine
from omega_infinity.omega_swarm_matrix import SwarmMatrix
from omega_infinity.omega_temporal_learner import TemporalLearningEngine
from omega_infinity.omega_all_agents import get_fleet
from omega_infinity.omega_enterprise_erp import get_erp, EnterpriseClient, EnterpriseOrder
from omega_infinity.omega_red_team_engine import get_red_team
from omega_infinity.omega_valuation_compounding import get_valuation_engine
from omega_infinity.omega_hyper_orchestrator import get_orchestrator
from omega_infinity.omega_autonomous_daemon_247 import get_autonomous_daemon
from omega_infinity.omega_startup_mnc_matrix import get_playbook_engine
from omega_infinity.omega_trillion_dollar_engine import get_trillion_engine
from omega_infinity.omega_planetary_gdp_asi_engine import get_planetary_gdp_asi_engine
from omega_infinity.omega_workflow_engine import get_workflow_engine

# Initialize singleton subsystems
kernel = get_kernel()
vectis_adapter = VectisEnterpriseAdapter()
intel_engine = IntelSearchEngine()
swarm_matrix = SwarmMatrix()
temporal_learner = TemporalLearningEngine()
fleet = get_fleet()
erp = get_erp()
red_team = get_red_team()
valuation = get_valuation_engine()
orchestrator = get_orchestrator()
autopilot = get_autonomous_daemon()
playbook_engine = get_playbook_engine()
trillion_engine = get_trillion_engine()
asi_engine = get_planetary_gdp_asi_engine()
workflow_engine = get_workflow_engine()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)


class OmegaCockpitHandler(BaseHTTPRequestHandler):
    """Handles REST API and static UI delivery for the Glass Cockpit."""

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content: str, status: int = 200):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Static Web Dashboard Delivery
        if path in ["/", "/index.html", "/cockpit"]:
            cockpit_file = os.path.join(STATIC_DIR, "cockpit.html")
            if os.path.exists(cockpit_file):
                with open(cockpit_file, "r", encoding="utf-8") as f:
                    self._send_html(f.read())
            else:
                self._send_html("<h1>OMEGA INFINITY: cockpit.html loading...</h1>")
            return

        # 2. Kernel State API
        if path == "/api/state":
            self._send_json(kernel.get_summary())
            return

        # 3. Swarm & Fleet Agents API
        if path == "/api/swarm/agents":
            self._send_json({
                "agents": swarm_matrix.get_agent_states(),
                "timestamp": time.time()
            })
            return

        if path == "/api/fleet/agents":
            self._send_json({
                "total": len(fleet.agents),
                "agents": fleet.get_all_agents(),
                "timestamp": time.time()
            })
            return

        if path == "/api/fleet/divisions":
            self._send_json({
                "divisions": fleet.get_divisions(),
                "timestamp": time.time()
            })
            return

        if path == "/api/temporal/matrix":
            self._send_json(temporal_learner.matrix)
            return

        # 4. Intelligence Engine APIs
        if path == "/api/intel/stats":
            self._send_json(intel_engine.get_stats())
            return

        if path == "/api/intel/companies":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [50])[0])
            self._send_json({
                "query": q,
                "count": len(intel_engine.companies),
                "results": intel_engine.search_companies(q, limit)
            })
            return

        if path == "/api/intel/network":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [50])[0])
            self._send_json({
                "query": q,
                "count": len(intel_engine.connections),
                "results": intel_engine.search_network(q, limit)
            })
            return

        if path == "/api/intel/leads":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [50])[0])
            self._send_json({
                "query": q,
                "count": len(intel_engine.trade_leads),
                "results": intel_engine.search_trade_leads(q, limit)
            })
            return

        # 5. Trade Certificates API
        if path == "/api/trade/certificates":
            self._send_json({
                "certificates": vectis_adapter.list_outbox_certificates()
            })
            return

        # 6. Cryptographic Ledger API
        if path == "/api/ledger":
            limit = int(query.get("limit", [50])[0])
            self._send_json({
                "verification": kernel.ledger.verify_integrity(),
                "blocks": kernel.ledger.get_recent(limit)
            })
            return

        # 7. Enterprise ERP & Financials APIs
        if path == "/api/erp/financials":
            self._send_json(asdict(erp.generate_financial_statement()))
            return

        if path == "/api/erp/clients":
            self._send_json({
                "total": len(erp.clients),
                "clients": [asdict(c) for c in erp.clients.values()]
            })
            return

        if path == "/api/erp/orders":
            self._send_json({
                "total": len(erp.orders),
                "orders": [asdict(o) for o in erp.orders.values()]
            })
            return

        if path == "/api/erp/summary":
            self._send_json(erp.get_portfolio_summary())
            return

        # 8. Adversarial Red Team Results API
        if path == "/api/redteam/results":
            self._send_json(red_team.run_all_12_probes())
            return

        # 9. Sovereign Valuation Compounding API
        if path == "/api/valuation/summary":
            self._send_json(valuation.compute_all_horizons())
            return

        # 10. Hyper-Orchestrator Execution Manifest API
        if path == "/api/orchestrator/manifest":
            manifest_file = os.path.join(REPO_ROOT, "omega", "data", "do_everything_execution_manifest.json")
            if os.path.exists(manifest_file):
                with open(manifest_file, "r", encoding="utf-8") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json({"message": "No manifest generated yet. Trigger /api/orchestrator/do-everything."})
            return

        # 11. 24/7 Autonomous Autopilot Status API
        if path == "/api/autopilot/status":
            self._send_json(autopilot.get_status())
            return

        # 12. Startup & MNC Playbook Matrix APIs
        if path == "/api/playbooks":
            pb_id = query.get("id", [""])[0]
            if pb_id:
                pb = playbook_engine.get_playbook(pb_id)
                if pb:
                    self._send_json(pb)
                else:
                    self._send_json({"error": f"Playbook '{pb_id}' not found"}, status=404)
            else:
                self._send_json({
                    "total": len(playbook_engine.playbooks),
                    "playbooks": playbook_engine.get_all_playbooks()
                })
            return

        # 13. Planetary Trillion-Dollar Architecture API
        if path == "/api/trillion":
            if "simulate" in query:
                try:
                    trade_pct = float(query.get("trade_pct", [12.5])[0]) / 100.0
                    nodes = int(query.get("nodes", [75000])[0])
                    float_bn = float(query.get("float_bn", [120.0])[0])
                    multiple = float(query.get("multiple", [30.0])[0])
                except Exception:
                    trade_pct, nodes, float_bn, multiple = 0.125, 75000, 120.0, 30.0
                self._send_json(trillion_engine.simulate_trillion_scenario(
                    global_trade_penetration_pct=trade_pct,
                    enterprise_agent_nodes=nodes,
                    escrow_float_usd_bn=float_bn,
                    multiple=multiple
                ))
            else:
                self._send_json(trillion_engine.generate_trillion_dollar_dossier())
            return

        # 14. Planetary World GDP & ASI Powers API
        if path == "/api/asi":
            if "simulate" in query:
                try:
                    year = int(query.get("year", [2050])[0])
                    gdp_trillion = float(query.get("gdp_trillion", [550.0])[0]) if "gdp_trillion" in query else None
                    ai_pct = float(query.get("ai_pct", [80.0])[0]) if "ai_pct" in query else None
                    capture_bps = float(query.get("capture_bps", [18.55])[0])
                    multiple = float(query.get("multiple", [25.5])[0])
                except Exception:
                    year, gdp_trillion, ai_pct, capture_bps, multiple = 2050, 550.0, 80.0, 18.55, 25.5
                self._send_json(asi_engine.simulate_asi_gdp_impact(
                    year=year,
                    custom_world_gdp_trillion=gdp_trillion,
                    ai_penetration_pct=ai_pct,
                    omega_gdp_capture_bps=capture_bps,
                    valuation_multiple=multiple
                ))
            else:
                self._send_json(asi_engine.generate_asi_gdp_dossier())
            return

        # 15. Autonomous Enterprise Workflows API (Section 27 & 28)
        if path == "/api/workflows":
            self._send_json({
                "total": len(workflow_engine.workflows),
                "workflows": workflow_engine.list_workflows(),
                "history": workflow_engine.execution_history
            })
            return

        # 404 Fallback
        self._send_json({"error": "Endpoint not found", "path": path}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception:
            body = {}

        # 1. Mode Transition
        if path == "/api/mode":
            mode = body.get("mode", "M")
            try:
                res = kernel.set_mode(mode)
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        # 2. Run Swarm Cycle
        if path == "/api/swarm/run":
            res = swarm_matrix.run_full_swarm_cycle()
            self._send_json(res)
            return

        # 3. Dispatch Specific Swarm Agent
        if path == "/api/swarm/agent":
            agent_id = body.get("agent_id", "")
            action = body.get("action", "Ad-hoc task execution")
            res = swarm_matrix.dispatch_agent_task(agent_id, action)
            self._send_json(res)
            return

        # 3b. 24-Agent Sovereign Fleet Routes
        if path == "/api/fleet/run":
            res = fleet.run_full_fleet_cycle()
            self._send_json(res)
            return

        if path == "/api/fleet/agent":
            agent_id = body.get("agent_id", "")
            action = body.get("action", "Ad-hoc fleet task execution")
            res = fleet.dispatch_agent_task(agent_id, action)
            self._send_json(res)
            return

        # 3c. Temporal Learning & Synthesis
        if path == "/api/temporal/learn":
            res = temporal_learner.learn_and_synthesize()
            self._send_json(res)
            return

        # 4. Trade Docket Audit
        if path == "/api/trade/audit":
            res = vectis_adapter.audit_docket(body)
            self._send_json(res)
            return

        # 5. SWIFT MT700 Parser & Audit
        if path == "/api/trade/swift":
            swift_text = body.get("swift_text", "")
            res = vectis_adapter.parse_swift_and_audit(swift_text)
            self._send_json(res)
            return

        # 6. EU CBAM Calculation
        if path == "/api/trade/cbam":
            res = vectis_adapter.calculate_cbam(body)
            self._send_json(res)
            return

        # 6b. Enterprise ERP Reports & Mutators
        if path == "/api/erp/reports":
            res = erp.generate_markdown_reports()
            self._send_json({"success": True, "reports": res})
            return

        if path == "/api/erp/client":
            try:
                res = erp.add_client(EnterpriseClient(**body))
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        if path == "/api/erp/order":
            try:
                res = erp.create_order(EnterpriseOrder(**body))
                self._send_json(res)
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, status=400)
            return

        # 6c. Hyper-Orchestrator & Red Team POST endpoints
        if path == "/api/orchestrator/do-everything":
            manifest = orchestrator.do_everything()
            self._send_json(manifest)
            return

        if path == "/api/redteam/run":
            res = red_team.run_all_12_probes()
            self._send_json(res)
            return

        # 6d. 24/7 Autonomous Autopilot Controls
        if path == "/api/autopilot/start":
            res = autopilot.start_background()
            self._send_json(res)
            return

        if path == "/api/autopilot/stop":
            res = autopilot.stop()
            self._send_json(res)
            return

        if path == "/api/autopilot/pulse":
            res = autopilot.step(force_all=True)
            self._send_json(res)
            return

        # 6e. Synthesize Custom Venture Blueprint from Startup & MNC Models
        if path == "/api/playbooks/synthesize":
            industry = body.get("industry", "Precision Engineering & Metal Fabrication")
            target_hub = body.get("target_hub", "Peenya Industrial Estate & Hosur Corridor")
            scale_goal = body.get("scale_goal", "Top-1% Sovereign Cross-Border Trade OS")
            blueprint = playbook_engine.synthesize_venture_blueprint(industry, target_hub, scale_goal)
            self._send_json(blueprint)
            return

        # 6f. Execute Deep Specialized Agent Mission
        if path == "/api/fleet/mission":
            agent_id = body.get("agent_id", "ceo")
            mission_res = fleet.execute_specialized_mission(agent_id, body)
            self._send_json(mission_res)
            return

        # 6g. Simulate Planetary Trillion-Dollar Scenario
        if path == "/api/trillion/simulate":
            try:
                trade_pct = float(body.get("trade_pct", 12.5)) / 100.0
                nodes = int(body.get("nodes", 75000))
                float_bn = float(body.get("float_bn", 120.0))
                multiple = float(body.get("multiple", 30.0))
            except Exception:
                trade_pct, nodes, float_bn, multiple = 0.125, 75000, 120.0, 30.0
            res = trillion_engine.simulate_trillion_scenario(
                global_trade_penetration_pct=trade_pct,
                enterprise_agent_nodes=nodes,
                escrow_float_usd_bn=float_bn,
                multiple=multiple
            )
            self._send_json(res)
            return

        # 6h. Simulate Planetary World GDP & ASI Scenario
        if path == "/api/asi/simulate":
            try:
                year = int(body.get("year", 2050))
                gdp_trillion = float(body.get("gdp_trillion", 550.0)) if "gdp_trillion" in body else None
                ai_pct = float(body.get("ai_pct", 80.0)) if "ai_pct" in body else None
                capture_bps = float(body.get("capture_bps", 18.55))
                multiple = float(body.get("multiple", 25.5))
            except Exception:
                year, gdp_trillion, ai_pct, capture_bps, multiple = 2050, 550.0, 80.0, 18.55, 25.5
            res = asi_engine.simulate_asi_gdp_impact(
                year=year,
                custom_world_gdp_trillion=gdp_trillion,
                ai_penetration_pct=ai_pct,
                omega_gdp_capture_bps=capture_bps,
                valuation_multiple=multiple
            )
            self._send_json(res)
            return

        # 7. Workflow Execution API (Section 27 & 28)
        if path == "/api/workflows/run":
            wf_id = body.get("workflow_id")
            if body.get("run_all", False) or not wf_id:
                res = workflow_engine.run_all_workflows()
                self._send_json(res)
            else:
                try:
                    record = workflow_engine.run_workflow(wf_id, body.get("input"))
                    self._send_json(asdict(record))
                except Exception as e:
                    self._send_json({"error": str(e)}, status=400)
            return

        # 8. Constitutional Command Interpreter (Section 6)
        if path == "/api/command":
            raw_cmd = body.get("command", "STATUS").strip().upper()
            kernel.dispatch_event(
                event_name="CONSTITUTIONAL_COMMAND",
                actor="FOUNDER_TERMINAL",
                data={"raw_command": raw_cmd}
            )

            # Map commands to actions
            if "WORKFLOW" in raw_cmd or "FLOW" in raw_cmd:
                res = workflow_engine.run_all_workflows()
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "message": "Executed all 10 canonical enterprise workflows through the 8-point universal standard.",
                    "workflow_batch": res
                })
                return
            if "ASI" in raw_cmd or "AGI" in raw_cmd or "GDP" in raw_cmd or "POWERS" in raw_cmd:
                dossier = asi_engine.generate_asi_gdp_dossier()
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "message": "Planetary World GDP, AGI/ASI Levels & Sovereign Powers Dossier loaded.",
                    "dossier": dossier
                })
                return

            if "TRILLION" in raw_cmd or "1T" in raw_cmd or "PLANETARY" in raw_cmd:
                dossier = trillion_engine.generate_trillion_dollar_dossier()
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "message": "Planetary Trillion-Dollar Sovereign Architecture loaded ($1.02T USD by 2050).",
                    "dossier": dossier
                })
                return

            if "PLAYBOOK" in raw_cmd or "BLUEPRINT" in raw_cmd or "STARTUP" in raw_cmd:
                bp = playbook_engine.synthesize_venture_blueprint(
                    industry="Precision Engineering & Metal Fabrication",
                    target_hub="Peenya Industrial Estate & Hosur Auto-Corridor",
                    scale_goal="Top-1% Sovereign Cross-Border Trade OS"
                )
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "message": "Synthesized Sovereign Venture Blueprint from Stripe, Flexport, Veeva, Berkshire, and ASML playbooks.",
                    "blueprint": bp
                })
                return

            if "AUTOPILOT" in raw_cmd or "24/7" in raw_cmd or "247" in raw_cmd:
                if "START" in raw_cmd or "ON" in raw_cmd or "ACTIVATE" in raw_cmd:
                    res = autopilot.start_background()
                    self._send_json({"success": True, "command": raw_cmd, "result": res})
                    return
                elif "STOP" in raw_cmd or "OFF" in raw_cmd or "DEACTIVATE" in raw_cmd:
                    res = autopilot.stop()
                    self._send_json({"success": True, "command": raw_cmd, "result": res})
                    return
                elif "PULSE" in raw_cmd or "STEP" in raw_cmd or "RUN" in raw_cmd:
                    res = autopilot.step(force_all=True)
                    self._send_json({"success": True, "command": raw_cmd, "result": res})
                    return
                else:
                    self._send_json({"success": True, "command": raw_cmd, "status": autopilot.get_status()})
                    return
            if "DO EVERYTHING" in raw_cmd or "FULL POWER" in raw_cmd or "EMPIRE" in raw_cmd:
                manifest = orchestrator.do_everything()
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "mode": "M (CEO)",
                    "message": "Full Sovereign MNC Power activated across all 13 modes, 24 agents, red team, and ERP platform.",
                    "manifest": manifest
                })
                return

            if "AUDIT" in raw_cmd:
                kernel.set_mode("G")
                audit_summary = kernel.ledger.verify_integrity()
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "mode": "G (AUDIT)",
                    "ledger_verification": audit_summary
                })
                return

            if "BUILD" in raw_cmd:
                kernel.set_mode("D")
                self._send_json({
                    "success": True,
                    "command": raw_cmd,
                    "mode": "D (BUILD)",
                    "message": "Deep module build pipeline armed."
                })
                return

            # Default status response
            self._send_json({
                "success": True,
                "command": raw_cmd,
                "active_mode": kernel.state.active_mode,
                "message": f"Command '{raw_cmd}' logged and processed."
            })
            return

        self._send_json({"error": "Unknown POST endpoint", "path": path}, status=404)

    def log_message(self, format, *args):
        # Quiet logger to keep terminal clean
        pass


def run_server(port: int = 8888):
    server_address = ("", port)
    httpd = HTTPServer(server_address, OmegaCockpitHandler)
    print(f"\n=======================================================")
    print(f"  OMEGA INFINITY (Ω-OS) SOVEREIGN SERVER IS ACTIVE")
    print(f"  Dashboard: http://localhost:{port}")
    print(f"  REST API:  http://localhost:{port}/api/state")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Ω-OS] Server gracefully stopped.")
        httpd.server_close()


if __name__ == "__main__":
    port = 8888
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port)
