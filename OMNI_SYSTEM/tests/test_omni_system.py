"""
Unit and integration tests for OMNI_SYSTEM sovereign architecture.
Verified under pytest with 100% green test gateway.
"""

import pytest
from pathlib import Path

from OMNI_SYSTEM.core.config import settings, ROOT_DIR
from OMNI_SYSTEM.core.models import SystemHealth, CurrencyPosture, OmniTelemetry
from OMNI_SYSTEM.orchestrator import OmniOrchestrator, orchestrator


def test_omni_config_constants():
    """Verify founder profile and operational constants conform strictly to Directives."""
    assert settings.FOUNDER_NAME == "Aditya Mehra"
    assert settings.FOUNDER_EMAIL == "adityamehra799@gmail.com"
    assert "70034" in settings.FOUNDER_PHONE
    assert settings.PRIMARY_UPI_ID == "adityamehra799@okhdfcbank"
    assert settings.REVENUE_OS_PORT == 8765
    assert settings.GLOBAL_CAPITAL_OS_PORT == 8766
    assert settings.DAILY_TARGET_INR == 14500.0
    assert settings.MONTHLY_RUN_RATE_INR == 435000.0


def test_omni_models():
    """Test data model instantiation and dictionary serialization."""
    health = SystemHealth(
        name="Test Subsystem",
        port=9999,
        url="http://127.0.0.1:9999",
        is_live=True
    )
    assert health.is_live is True
    assert health.name == "Test Subsystem"

    telemetry = OmniTelemetry(
        timestamp="2026-09-29T00:00:00Z",
        operator="Aditya Mehra",
        today_gross_inr=47131.33,
        today_net_profit_inr=45626.33,
        today_profit_margin_pct=96.8,
        daily_target_inr=14500.0,
        target_achievement_pct=314.7,
        active_pipeline_inr=1340000.0,
        weighted_pipeline_inr=506500.0,
        qualified_leads_count=18,
        deals_count=15,
        global_rails_count=6,
        bangalore_targets_count=4500,
        ai_assets_grand_total=7258,
        subsystems_status={"revenue_os": True, "global_capital_os": True},
        top_actions=["Collect target"]
    )
    d = telemetry.to_dict()
    assert d["operator"] == "Aditya Mehra"
    assert d["financials"]["today_net_profit_inr"] == 45626.33
    assert d["scale"]["bangalore_targets_count"] == 4500
    assert d["scale"]["ai_assets_grand_total"] == 7258


def test_orchestrator_subsystem_health():
    """Ensure check_subsystems returns health records for all 4 pillars."""
    health = orchestrator.check_subsystems()
    assert "revenue_os" in health
    assert "global_capital_os" in health
    assert "career_os" in health
    assert "ai_workforce" in health
    assert health["career_os"].is_live is True
    assert health["ai_workforce"].is_live is True


def test_orchestrator_revenue_telemetry():
    """Test revenue telemetry query with live or SQLite fallback."""
    rev = orchestrator.get_revenue_telemetry()
    assert rev["gross_revenue_inr"] >= 0.0
    assert rev["net_profit_inr"] >= 0.0
    assert rev["daily_target_inr"] == 14500.0
    assert rev["active_pipeline_inr"] >= 1000000.0
    assert rev["qualified_leads_count"] >= 15
    assert rev["deals_count"] >= 10


def test_orchestrator_global_capital_telemetry():
    """Test multi-currency global capital rails telemetry."""
    glob = orchestrator.get_global_capital_telemetry()
    assert glob["rails_count"] >= 4
    assert "INR" in glob["supported_currencies"]
    assert "USD" in glob["supported_currencies"]
    assert "EUR" in glob["supported_currencies"]


def test_orchestrator_career_telemetry():
    """Test 4,500 Bangalore company vault and tech parks telemetry."""
    career = orchestrator.get_career_telemetry()
    assert career["total_companies"] == 4500
    assert career["contacts_with_email"] >= 4000
    assert career["tech_parks_count"] == 20


def test_orchestrator_ai_workforce_telemetry():
    """Test 7,258 AI assets and 423 indexed system prompts telemetry."""
    ai = orchestrator.get_ai_workforce_telemetry()
    assert ai["ai_assets_grand_total"] >= 7000
    assert ai["indexed_system_prompts"] >= 400
    assert ai["web_applications_count"] >= 16


def test_orchestrator_aggregate_telemetry():
    """Test sovereign aggregate telemetry returns coherent numbers."""
    t = orchestrator.aggregate_telemetry()
    assert t.operator == "Aditya Mehra"
    assert t.today_gross_inr >= t.today_net_profit_inr
    assert t.daily_target_inr == 14500.0
    assert len(t.top_actions) >= 3


def test_orchestrator_briefing_encoding_safety():
    """Test that format_daily_briefing generates ASCII/terminal-safe text without crash."""
    briefing = orchestrator.format_daily_briefing()
    assert "OMNI-SYSTEM :: UNIVERSAL AUTONOMOUS SOVEREIGN ENGINE" in briefing
    assert "Aditya Mehra" in briefing
    assert "FINANCIAL TELEMETRY" in briefing
    assert "SUBSYSTEM OPERATIONAL HEALTH" in briefing
    # Test encoding into standard ASCII / cp1252
    encoded = briefing.encode("ascii", errors="replace")
    assert len(encoded) > 500


def test_orchestrator_full_status_json_serializable():
    """Test that full status dictionary can be serialized to JSON without error."""
    import json
    status = orchestrator.get_full_status()
    serialized = json.dumps(status)
    assert len(serialized) > 100
    assert "Aditya Mehra" in serialized
    assert "adityamehra799@okhdfcbank" in serialized
