"""
Test Suite for Terra Kinetics Pilots and Open-Source SDK.
"""

import pytest
import os
from terra_kinetics.pilots.pilot_orchestrator import PilotDeploymentOrchestrator, SitePreflightCriteria
from terra_kinetics.pilots.bmw_automotive_pilot import BMWAutomotivePilot
from terra_kinetics.pilots.dhl_logistics_pilot import DHLLogisticsPilot


def test_bmw_pilot_full_shift_execution():
    pilot = BMWAutomotivePilot()
    res = pilot.launch_pilot()
    assert res["sla_passed"] is True
    assert res["autonomy_rate_pct"] >= 99.5
    assert res["picks_per_hour"] == 400.0
    assert res["customer_net_savings_usd"] > 100.0  # Demonstrates immediate ROI


def test_dhl_pilot_full_shift_execution():
    pilot = DHLLogisticsPilot()
    res = pilot.launch_pilot()
    assert res["sla_passed"] is True
    assert res["autonomy_rate_pct"] >= 99.5
    assert res["picks_per_hour"] == 1200.0
    assert res["customer_net_savings_usd"] > 100.0


def test_preflight_audit_fails_on_poor_environment():
    orchestrator = PilotDeploymentOrchestrator(
        facility_name="Substandard_Warehouse",
        site_criteria=SitePreflightCriteria(min_lighting_lux=300.0, max_network_jitter_ms=5.0),
    )
    # Poor lighting
    passed_lux, msg_lux = orchestrator.run_preflight_audit(measured_lux=180.0, measured_jitter_ms=2.0)
    assert not passed_lux
    assert "Lighting below threshold" in msg_lux

    # Excessive jitter
    passed_jitter, msg_jitter = orchestrator.run_preflight_audit(measured_lux=400.0, measured_jitter_ms=12.5)
    assert not passed_jitter
    assert "Network latency jitter too high" in msg_jitter


def test_sdk_packaging_integrity():
    sdk_dir = os.path.join(os.path.dirname(__file__), "..", "sdk")
    assert os.path.exists(os.path.join(sdk_dir, "pyproject.toml"))
    assert os.path.exists(os.path.join(sdk_dir, "LICENSE"))
    assert os.path.exists(os.path.join(sdk_dir, "README.md"))
