"""Unit tests for DailyProfitEngine in REVENUE_OS."""

import pytest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.finance.daily_profit_engine import DailyProfitEngine

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_revenue_os.db"
    db = DatabaseManager(db_file)
    db.initialize()
    return db

def test_daily_profit_engine_initialization_and_seeding(temp_db):
    engine = DailyProfitEngine(db=temp_db)
    summary = engine.get_daily_summary()
    assert summary["transaction_count"] >= 3
    assert summary["gross_revenue_inr"] > 0
    assert summary["net_profit_inr"] > 0
    assert summary["profit_margin_pct"] > 80.0

def test_daily_profit_record_income(temp_db):
    engine = DailyProfitEngine(db=temp_db)
    initial_summary = engine.get_daily_summary()
    initial_profit = initial_summary["net_profit_inr"]

    res = engine.record_income(
        client="Test Enterprise Ltd",
        source_type="B2B_RETAINER",
        description="AI Automation Monthly Retainer installment",
        gross_amount_inr=10000.0,
        variable_cost_inr=500.0,
        payment_rail="UPI_HDFC",
        notes="Verified test"
    )
    assert res["status"] == "SUCCESS"
    assert res["net_profit_inr"] == 9500.0

    new_summary = engine.get_daily_summary()
    assert new_summary["net_profit_inr"] == initial_profit + 9500.0
    assert new_summary["transaction_count"] == initial_summary["transaction_count"] + 1

def test_daily_profit_receipt_generation(temp_db):
    engine = DailyProfitEngine(db=temp_db)
    receipt = engine.generate_daily_pnl_receipt()
    assert "DAILY PROFIT & CASH RECEIPT" in receipt
    assert "Aditya Mehra" in receipt
    assert "NET PROFIT TODAY" in receipt
