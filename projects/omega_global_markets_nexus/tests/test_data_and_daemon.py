"""
Unit Tests for Market Data Service and Autonomous Execution Daemon
"""
import os
import pytest
from projects.omega_global_markets_nexus.data_feeds.market_data_service import MarketDataService
from projects.omega_global_markets_nexus.daemon.autonomous_nexus_daemon import (
    NexusAuditLedger, AutonomousNexusDaemon
)


def test_market_data_service():
    service = MarketDataService()
    quotes = service.get_equity_quotes()
    assert len(quotes) >= 5
    assert quotes[0]["price"] > 0

    mm = service.get_money_market_benchmarks()
    assert mm["sofr_overnight_pct"] > 0

    yields = service.get_sovereign_yield_ladder()
    assert "10Y" in yields

    fx = service.get_fx_matrix()
    assert "USD_INR" in fx

    snapshot = service.get_unified_market_snapshot()
    assert "timestamp" in snapshot
    assert "equities" in snapshot


def test_nexus_audit_ledger_and_daemon(tmp_path):
    test_db = str(tmp_path / "test_nexus_ledger.db")
    ledger = NexusAuditLedger(db_path=test_db)

    metrics_init = ledger.get_ledger_metrics()
    assert metrics_init["total_macro_cycles_recorded"] == 0

    daemon = AutonomousNexusDaemon(db_path=test_db)
    # Execute single cycle
    cycle_res = daemon.execute_single_cycle(archetype_idx=0)
    assert "cycle_id" in cycle_res
    assert cycle_res["business_archetype"] == "Hyperscale AI & Computing Cloud"

    # Verify ledger recorded it
    history = ledger.get_latest_cycles(limit=5)
    assert len(history) == 1
    assert history[0]["cycle_id"] == cycle_res["cycle_id"]

    metrics_after = ledger.get_ledger_metrics()
    assert metrics_after["total_macro_cycles_recorded"] == 1
