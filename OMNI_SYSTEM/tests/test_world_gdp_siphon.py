"""
Pytest test suite for World GDP Daily Siphon engine.
Verifies macroeconomic calculations, corridor coverage, and terminal encoding safety.
"""

import pytest
from OMNI_SYSTEM.world_gdp_siphon import (
    WORLD_GDP_USD_ANNUAL,
    DAILY_WORLD_GDP_USD,
    SECOND_WORLD_GDP_USD,
    USD_TO_INR_BENCHMARK,
    CORRIDORS,
    siphon_engine,
    WorldGDPSiphon
)
from OMNI_SYSTEM.cli import cmd_siphon


def test_world_gdp_constants():
    """Verify global economic velocity constants."""
    assert WORLD_GDP_USD_ANNUAL == 110_000_000_000_000.0
    assert DAILY_WORLD_GDP_USD > 300_000_000_000.0
    assert SECOND_WORLD_GDP_USD > 3_000_000.0
    assert USD_TO_INR_BENCHMARK == 83.50


def test_corridors_integrity():
    """Ensure all 5 economic corridors are properly defined with valid rails."""
    assert len(CORRIDORS) == 5
    corridor_ids = [c.corridor_id for c in CORRIDORS]
    assert "CORR-US-CAN" in corridor_ids
    assert "CORR-EU-UK" in corridor_ids
    assert "CORR-GCC-UAE" in corridor_ids
    assert "CORR-APAC-SG" in corridor_ids
    assert "CORR-IN-DOM" in corridor_ids

    total_share = sum(c.share_of_world_gdp_pct for c in CORRIDORS)
    assert total_share >= 70.0

    for c in CORRIDORS:
        assert c.annual_gdp_usd > 0
        assert c.daily_gdp_usd > 0
        assert len(c.target_offering) > 10
        assert len(c.settlement_rail) > 5


def test_siphon_metrics_calculation():
    """Verify micro-share calculations for daily quotas."""
    # Test base daily target (₹14,500)
    metrics_target = WorldGDPSiphon.calculate_siphon_metrics(14500.0, 14500.0)
    assert metrics_target["pacing_pct"] == 100.0
    assert metrics_target["global_status"] == "SIPHON_ACTIVE"
    assert "0.000000" in metrics_target["share_of_daily_world_gdp_pct"]

    # Test today's actual recognized gross inflow
    metrics_today = WorldGDPSiphon.calculate_siphon_metrics(47131.33, 14500.0)
    assert metrics_today["pacing_pct"] > 300.0
    assert metrics_today["current_inflow_usd"] > 500.0
    assert metrics_today["seconds_of_world_gdp_equivalent"] > 0.0


def test_format_siphon_briefing_encoding_safety():
    """Ensure formatting produces clean output and survives ASCII/cp1252 encoding."""
    brief = siphon_engine.format_siphon_briefing(47131.33)
    assert "WORLD GDP DAILY EXTRACTION RADAR" in brief
    assert "GLOBAL ECONOMIC VELOCITY" in brief
    assert "THE 5 WORLD EXTRACTION CORRIDORS" in brief
    assert "Aditya Mehra" in brief

    # Must survive encoding to ascii
    encoded = brief.encode("ascii", errors="replace")
    assert len(encoded) > 500


def test_cli_cmd_siphon_runs_cleanly(capsys):
    """Ensure CLI cmd_siphon can be called without error."""
    cmd_siphon()
    captured = capsys.readouterr()
    assert "WORLD GDP DAILY EXTRACTION RADAR" in captured.out
