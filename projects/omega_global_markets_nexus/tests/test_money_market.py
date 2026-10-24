"""
Unit Tests for Money Market Instruments, Repo Facility, Cash Sweeps, and Basel III LCR
"""
import pytest
from projects.omega_global_markets_nexus.core.money_market_engine import (
    TBillInstrument, CommercialPaper, RepoContract, CollateralTier,
    TreasuryCashSweepDesk, Basel3LiquidityAuditor
)


def test_tbill_pricing_and_yield():
    tbill = TBillInstrument(
        cusip="US912797AB1",
        tenor_days=91,
        face_value_usd=1000.0,
        discount_rate_pct=5.0
    )
    # Price = 1000 * (1 - 0.05 * 91 / 360) = 1000 * (1 - 0.0126388) = ~987.36
    assert 985.0 < tbill.purchase_price < 990.0
    assert tbill.bond_equivalent_yield_pct > 5.0


def test_repo_contract_haircut_and_repurchase():
    repo = RepoContract(
        contract_id="REPO-001",
        counterparty="Goldman Sachs",
        collateral_tier=CollateralTier.LEVEL_1_SOVEREIGN,
        collateral_market_value_usd=10_000_000.0,
        repo_rate_pct=5.30,
        term_days=7
    )
    assert repo.haircut_pct == 2.0
    assert repo.loan_amount_usd == 9_800_000.0
    assert repo.interest_payable_usd > 0
    assert repo.repurchase_price_usd > repo.loan_amount_usd


def test_treasury_cash_sweep():
    sweep = TreasuryCashSweepDesk.execute_sweep(
        total_cash_usd=20_000_000.0,
        overnight_buffer_target_usd=5_000_000.0
    )
    assert sweep["overnight_operational_cash"] == 5_000_000.0
    assert sweep["swept_to_sofr_repo"] == 6_000_000.0  # 40% of 15M
    assert sweep["swept_to_30d_tbills"] == 5_250_000.0 # 35% of 15M
    assert sweep["weighted_blended_yield_pct"] > 3.5


def test_basel3_lcr_audit():
    lcr = Basel3LiquidityAuditor.audit_lcr(
        level_1_assets_usd=30_000_000.0,
        level_2a_assets_usd=10_000_000.0,
        level_2b_assets_usd=5_000_000.0,
        operational_deposits_outflow_usd=10_000_000.0,
        non_operational_deposits_outflow_usd=20_000_000.0,
        contractual_cash_inflows_30d_usd=2_000_000.0
    )
    assert lcr["lcr_ratio_pct"] >= 100.0
    assert lcr["compliance_status"] == "COMPLIANT_PRUDENT"
