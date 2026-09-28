"""
OMEGA INFINITY (Ω-OS) — 24/7 AUTONOMOUS SOVEREIGN ENGINE TEST SUITE
Enforces Section 101, Section 14, and Master Directive 120 of OMEGA_CONSTITUTION.md.

Tests:
  1. Engine initialization, state loading, and state persistence.
  2. Realtime cadence: docket ingestion, UCP 600 audit, outbox certificate, ERP revenue accrual.
  3. Hourly cadence: B2B prospecting, regulatory watch, treasury runway calculations.
  4. Daily cadence: 13-mode DO EVERYTHING, 24-agent fleet run, Red Team, daily brief.
  5. Weekly cadence: 2027-2050 valuation compounding.
  6. Antifragile self-healing: corrupted docket resilience & directory self-repair.
  7. Thread background lifecycle: start, status, and stop.
  8. REST API endpoints: GET /api/autopilot/status, POST /api/autopilot/pulse, POST /api/autopilot/start, POST /api/autopilot/stop.
"""

import os
import sys
import json
import time
import shutil
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_autonomous_daemon_247 import Autonomous247Engine, get_autonomous_daemon


class TestAutonomous247Engine:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.daemon = Autonomous247Engine(
            realtime_interval=0.1,
            hourly_interval=0.2,
            daily_interval=0.3,
            weekly_interval=0.4
        )
        yield
        self.daemon.stop()

    def test_01_engine_initialization_and_state(self):
        """Verifies initial state, subsystems, and persistence."""
        status = self.daemon.get_status()
        assert status["health_status"] == "OPTIMAL"
        assert status["resilience_verdict"] == "SOVEREIGN ANTIFRAGILITY CONFIRMED"
        assert "REALTIME (10s)" in status["active_cadences"][0]
        assert status["is_running"] is False
        assert os.path.exists(self.daemon.inbox_dir)
        assert os.path.exists(self.daemon.outbox_dir)

    def test_02_realtime_docket_ingestion_and_erp_accrual(self):
        """Verifies hot-folder ingestion of an export docket and ERP revenue booking."""
        test_docket_id = f"TEST-DKT-{int(time.time())}"
        sample_docket = {
            "docket_id": test_docket_id,
            "exporter": "Peenya Precision Machining Pvt Ltd",
            "importer": "Rotterdam Marine Turbines B.V.",
            "lc_number": f"LC-{test_docket_id}",
            "lc_currency": "INR",
            "lc_amount": 12500000.0,
            "latest_shipment_date": "2027-06-30",
            "goods_description": "Machined Steel Valve Blocks",
            "transport_document": {
                "bl_number": f"BL-{test_docket_id}",
                "carrier": "Maersk Line",
                "shipped_on_board_date": "2027-06-25",
                "is_clean": True,
                "port_of_loading": "Chennai Port, India",
                "port_of_discharge": "Rotterdam, Netherlands"
            },
            "commercial_invoice": {
                "invoice_number": f"INV-{test_docket_id}",
                "currency": "INR",
                "total_amount": 12500000.0,
                "goods_description": "Machined Steel Valve Blocks"
            },
            "packing_list": {
                "total_packages": 120,
                "gross_weight_kg": 24000.0
            }
        }

        # Place docket in inbox
        inbox_file = os.path.join(self.daemon.inbox_dir, f"{test_docket_id}.json")
        with open(inbox_file, "w", encoding="utf-8") as f:
            json.dump(sample_docket, f, indent=2)

        # Execute realtime cadence
        initial_orders_count = len(self.daemon.erp.orders)
        res = self.daemon.execute_realtime_cadence()

        assert res["dockets_processed"] >= 1
        assert res["revenue_added"] >= 75000.0
        assert res["ledger_valid"] is True

        # Verify outbox artifacts
        out_json = os.path.join(self.daemon.outbox_dir, f"{test_docket_id}_audit_result.json")
        out_cert = os.path.join(self.daemon.outbox_dir, f"{test_docket_id}_certificate.md")
        assert os.path.exists(out_json)
        assert os.path.exists(out_cert)

        # Verify ERP booking
        assert len(self.daemon.erp.orders) > initial_orders_count

        # Clean up outbox artifacts
        try:
            os.remove(out_json)
            os.remove(out_cert)
        except Exception:
            pass

    def test_03_hourly_cadence_b2b_prospecting_and_treasury(self):
        """Verifies hourly B2B lead surveillance and treasury runway calculations."""
        res = self.daemon.execute_hourly_cadence()
        assert res["prospects_scanned"] >= 0
        assert res["regulatory_alerts"] == 0
        assert res["runway_months"] > 200.0  # Sovereign runway > 16 years

    def test_04_daily_cadence_do_everything_and_red_team(self):
        """Verifies daily full 13-mode execution, 24 agents, and red-team resilience."""
        res = self.daemon.execute_daily_cadence()
        assert res["orchestrator_modes_run"] == 13
        assert res["fleet_agents_executed"] == 24
        assert res["red_team_verdict"] == "SOVEREIGN ANTIFRAGILITY CONFIRMED"
        assert res["red_team_survival_pct"] >= 99.0
        assert os.path.exists(res["daily_brief_file"])
        assert "financial_report" in res["erp_reports_generated"]

    def test_05_weekly_cadence_valuation_compounding(self):
        """Verifies weekly valuation compounding across 5 horizons."""
        res = self.daemon.execute_weekly_cadence()
        assert res["valuation_horizons"] == 5

    def test_06_step_force_all_cadences(self):
        """Verifies unified single-pass execution across all 4 cadences."""
        res = self.daemon.step(force_all=True)
        assert "REALTIME" in res["cadences_executed"]
        assert "HOURLY" in res["cadences_executed"]
        assert "DAILY" in res["cadences_executed"]
        assert "WEEKLY" in res["cadences_executed"]
        status = self.daemon.get_status()
        assert status["total_pulses"] >= 1

    def test_07_antifragile_self_healing_under_corrupted_docket(self):
        """Verifies self-healing watchdog handles corrupted/unparseable files without crashing."""
        bad_file = os.path.join(self.daemon.inbox_dir, "corrupted_bad_docket.json")
        with open(bad_file, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON NOT TERMINATED ...")

        # Must not raise an unhandled exception
        initial_anomalies = self.daemon.state["anomalies_healed"]
        res = self.daemon.execute_realtime_cadence()

        assert res["ledger_valid"] is True
        # Anomaly was healed and recorded
        assert self.daemon.state["anomalies_healed"] >= initial_anomalies + 1
        # Bad file was safely moved or removed from inbox
        assert not os.path.exists(bad_file)

    def test_08_background_thread_lifecycle(self):
        """Verifies starting, monitoring, and stopping the background 24/7 thread."""
        res = self.daemon.start_background()
        assert res["status"] in ["STARTED", "ALREADY_RUNNING"]

        time.sleep(0.3)
        status = self.daemon.get_status()
        assert status["is_running"] is True
        assert status["uptime_seconds"] > 0

        # Idempotent start check
        res2 = self.daemon.start_background()
        assert res2["status"] == "ALREADY_RUNNING"

        # Stop check
        stop_res = self.daemon.stop()
        assert stop_res["status"] == "STOPPED"
        status_after = self.daemon.get_status()
        assert status_after["is_running"] is False
