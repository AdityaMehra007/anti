"""
OMEGA INFINITY (Ω-OS) — TEMPORAL LEARNING & 24-AGENT FLEET TEST SUITE
Enforces 100% test coverage across:
- Universal Temporal Learning Engine (Past, Present, Future 2027-2050)
- 24-Agent Sovereign Autonomous Fleet across 6 Divisions
- Sovereign Notifier & Alert Dispatcher
- Daily Sovereign Executive Brief Generation
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_temporal_learner import TemporalLearningEngine
from omega_infinity.omega_all_agents import SovereignFleet, get_fleet
from omega_infinity.omega_notifier import SovereignNotifier
from omega_infinity.omega_daily_brief import generate_daily_brief, OUTPUT_BRIEF_PATH


def test_temporal_learner_initialization_and_synthesis():
    learner = TemporalLearningEngine()
    assert "past" in learner.matrix
    assert "present_2026_2027" in learner.matrix
    assert "future_horizons" in learner.matrix

    # Verify horizons
    horizons = learner.matrix["future_horizons"]
    assert "2027" in horizons
    assert "2030" in horizons
    assert "2035" in horizons
    assert "2040" in horizons
    assert "2050" in horizons

    # Execute synthesis cycle
    res = learner.learn_and_synthesize()
    assert res["success"] is True
    assert len(res["horizons"]) == 5


def test_temporal_learner_horizon_queries():
    learner = TemporalLearningEngine()
    h2027 = learner.get_horizon("2027")
    assert h2027 is not None
    assert h2027["target_arr_inr"] == 5400000.0
    assert len(h2027["capabilities"]) >= 3

    h2050 = learner.get_horizon("2050")
    assert h2050 is not None
    assert h2050["target_arr_inr"] == 5000000000.0


def test_sovereign_fleet_structure():
    fleet = SovereignFleet()
    assert len(fleet.agents) == 24

    divisions = fleet.get_divisions()
    assert len(divisions) == 6
    assert "Executive Council" in divisions
    assert "Global Trade & Supply Chain" in divisions
    assert "Growth & Market Intelligence" in divisions
    assert "Talent & Network Ecosystem" in divisions
    assert "Governance, Risk & Quality" in divisions
    assert "Autonomous Venture & SaaS Foundry" in divisions


def test_sovereign_fleet_single_dispatch():
    fleet = SovereignFleet()
    res = fleet.dispatch_agent_task("customs", "Verified ICEGATE single window submission clearance")
    assert res["success"] is True
    assert res["agent"]["id"] == "customs"
    assert res["agent"]["tasks_completed"] >= 1
    assert res["agent"]["status"] == "OPTIMAL"


def test_sovereign_fleet_full_cycle():
    fleet = SovereignFleet()
    res = fleet.run_full_fleet_cycle()
    assert res["success"] is True
    assert res["agents_executed"] == 24
    assert res["elapsed_seconds"] >= 0.0


def test_notifier_alert_dispatch():
    notifier = SovereignNotifier()
    alert = notifier.dispatch_alert(
        level="INFO",
        title="Test Executive Notification",
        message="Verifying alert dispatch to terminal and ledger",
        payload={"test": True}
    )
    assert alert["level"] == "INFO"
    assert len(alert["id"]) > 5
    assert len(notifier.alert_history) >= 1


def test_daily_brief_generation():
    path = generate_daily_brief()
    assert os.path.exists(path)
    assert path == OUTPUT_BRIEF_PATH

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "OMEGA ∞ SOVEREIGN DAILY EXECUTIVE BRIEF" in content
    assert "VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED" in content
    assert "Aditya Mehra" in content
