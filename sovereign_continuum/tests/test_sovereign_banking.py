"""
Comprehensive Automated Test Suite for Sovereign Banking & Multi-Trillion Dollar Financial Architecture.
"""

import pytest
from sovereign_continuum.banking.central_banking_engine import CentralBankingFacility, LiquidityCorridor, CentralBankBalanceSheet
from sovereign_continuum.banking.investment_banking_engine import (
    DebtCapitalMarketsDesk,
    SyndicatedLendingDesk,
    SecuritizationDesk,
    MAndAAdvisoryDesk,
    SecuritizedPool,
)
from sovereign_continuum.banking.transaction_banking_engine import (
    GlobalCashManagementDesk,
    TradeFinanceDesk,
    WholesalePaymentRails,
)
from sovereign_continuum.banking.custody_prime_brokerage import (
    GlobalCustodyDesk,
    TriPartyRepoDesk,
    SecuritiesLendingDesk,
    PrimeBrokerageDesk,
    CustodyAssetPosition,
)
from sovereign_continuum.banking.derivatives_clearing_engine import (
    DerivativesClearingDesk,
    InterestRateSwap,
    FXForwardContract,
    CreditDefaultSwap,
)
from sovereign_continuum.banking.autonomous_sovereign_bank import BankOfTheContinuum


def test_central_banking_facility():
    cb = CentralBankingFacility()
    
    # 1. Open Market Operation (QE)
    qe_result = cb.execute_open_market_operation(amount_b=150.0, is_qe=True)
    assert qe_result["action"] == "QUANTITATIVE_EASING_PURCHASE"
    assert qe_result["delta_b"] == 150.0

    # 2. Discount Window
    dw_result = cb.access_discount_window(
        borrowing_bank_id="MEMBER_BANK_01",
        collateral_market_value_b=10.0,
        haircut_pct=0.05,
    )
    assert dw_result["credit_advanced_b"] == 9.5
    assert dw_result["interest_rate_pct"] == 5.25

    # 3. Overnight Reverse Repo
    rrp_result = cb.conduct_overnight_reverse_repo("MONEY_MARKET_FUND_01", amount_b=50.0)
    assert rrp_result["amount_absorbed_b"] == 50.0
    assert rrp_result["floor_rate_paid_pct"] == 4.80

    # 4. Bilateral C6 Swap Line
    swap_result = cb.activate_c6_currency_swap_line("ECB", usd_draw_amount_b=25.0, spot_fx_rate=0.92)
    assert swap_result["status"] == "SWAP_LINE_ACTIVE"
    assert swap_result["foreign_currency_held_b"] == 23.0


def test_investment_banking_and_dcm():
    dcm = DebtCapitalMarketsDesk()
    bond = dcm.price_and_bookbuild_bond(
        issuer="Terra_Kinetics_Sovereign_Holdings",
        principal_b=15.0,
        tenor_years=10,
        benchmark_yield_pct=4.20,
        rating="AAA",
        is_green=True,
    )
    assert bond["is_green_bond"] is True
    assert bond["greenium_savings_bps"] == 8.0
    assert bond["final_coupon_pct"] < (4.20 + 0.45)  # Enjoys greenium savings
    assert bond["modified_duration_years"] > 5.0

    lending = SyndicatedLendingDesk()
    facility = lending.structure_syndicated_facility(
        borrower_name="Aether_Energy_Infrastructure_SPV",
        facility_amount_b=20.0,
        ebitda_b=6.0,
        annual_debt_service_b=1.8,
    )
    assert facility["covenants_compliant"] is True
    assert facility["leverage_ratio_debt_to_ebitda"] <= 4.5

    securitization = SecuritizationDesk()
    pool = SecuritizedPool(
        pool_id="POOL_ROBOT_HOURLY_TOLLS_01",
        total_collateral_value_b=10.0,
        annual_cashflow_b=1.2,
    )
    waterfall = securitization.structure_tranche_waterfall(pool, default_shock_pct=0.05)
    assert waterfall["senior_aaa"]["loss_absorbed"] is False
    assert waterfall["equity_first_loss"]["realized_dividend_yield_pct"] > 10.0

    mna = MAndAAdvisoryDesk()
    lbo = mna.model_lbo_acquisition(
        target_name="Precision_Robotics_Actuators_GmbH",
        entry_ebitda_b=1.5,
        entry_multiple=12.0,
    )
    assert lbo["multiple_on_invested_capital_moic"] > 1.5
    assert lbo["net_internal_rate_of_return_irr_pct"] > 10.0


def test_transaction_banking_and_trade_finance():
    cash = GlobalCashManagementDesk()
    sweep = cash.execute_zero_balance_sweep({
        "SUB_GERMANY_EUR": 25_000_000.0,
        "SUB_USA_USD": 80_000_000.0,
        "SUB_SINGAPORE_SGD": 12_000_000.0,
    })
    assert sweep["total_liquidity_concentrated_usd"] > 100_000_000.0

    netting = cash.execute_multilateral_netting([
        ("SUB_GERMANY", "SUB_USA", 40_000_000.0),
        ("SUB_USA", "SUB_SINGAPORE", 35_000_000.0),
        ("SUB_SINGAPORE", "SUB_GERMANY", 30_000_000.0),
    ])
    assert netting["compression_efficiency_pct"] > 60.0  # High netting efficiency

    trade = TradeFinanceDesk()
    lc = trade.issue_confirmed_letter_of_credit("BMW_AG", "Terra_Kinetics_Munich", amount_usd=50_000_000.0)
    assert lc.is_confirmed is True
    assert lc.governing_rules == "ICC UCP 600"

    reverse_factoring = trade.calculate_reverse_factoring_early_payment(
        invoice_face_value_usd=10_000_000.0,
        days_to_maturity=60,
    )
    assert reverse_factoring["net_cash_delivered_to_supplier_usd"] < 10_000_000.0
    assert reverse_factoring["early_payment_discount_usd"] > 0.0

    rails = WholesalePaymentRails()
    msg = rails.generate_iso20022_pacs008(
        instructing_bic="CONTUS33XXX",
        instructed_bic="CHASUS33XXX",
        debtor_account="ACC_001",
        creditor_account="ACC_002",
        amount=15_000_000.0,
    )
    assert msg.message_type == "pacs.008.001.10"
    assert len(msg.end_to_end_uetr) == 36


def test_custody_and_prime_brokerage():
    custody = GlobalCustodyDesk()
    custody.deposit_asset(CustodyAssetPosition("US_TREASURY_10Y", "SOVEREIGN_BOND", 500_000, 980.0))
    custody.deposit_asset(CustodyAssetPosition("GOLD_BULLION", "PRECIOUS_METALS", 10_000, 2650.0))
    auc = custody.calculate_total_assets_under_custody()
    assert auc["total_assets_under_custody_usd"] > 500_000_000.0
    assert auc["annual_safekeeping_fee_revenue_usd"] > 0.0

    repo = TriPartyRepoDesk()
    allocation = repo.allocate_repo_collateral(
        cash_borrowed_b=5.0,
        collateral_type="SOVEREIGN_BOND_SHORT",
        pledged_collateral_market_value_b=5.2,
    )
    assert allocation["is_solvent_and_cleared"] is True
    assert allocation["haircut_pct"] == 1.0

    seclend = SecuritiesLendingDesk()
    loan = seclend.execute_securities_loan("HEDGE_FUND_ALPHA", "SECURITY_SPECIAL_01", market_value_usd=100_000_000.0, is_hard_to_borrow=True)
    assert loan["lending_fee_bps"] == 350.0
    assert loan["required_collateral_usd_102pct"] == 102_000_000.0

    pb = PrimeBrokerageDesk()
    margin = pb.calculate_margin_requirements(gross_long_positions_usd=200_000_000.0, gross_short_positions_usd=150_000_000.0, daily_pnl_usd=-3_500_000.0)
    assert margin["initial_margin_requirement_usd"] > 0.0
    assert margin["variation_margin_call_usd"] == 3_500_000.0


def test_derivatives_clearing():
    desk = DerivativesClearingDesk()
    
    irs = InterestRateSwap("IRS_001", notional_amount_b=5.0, tenor_years=5, fixed_rate_pct=4.25)
    irs_val = desk.price_interest_rate_swap(irs, current_market_sofr_pct=4.85)
    assert irs_val["position_state"] == "IN_THE_MONEY"
    assert irs_val["dv01_sensitivity_usd"] > 1_000_000.0

    fx = FXForwardContract("FXF_001", "EUR/USD", 100_000_000.0, spot_fx_rate=1.0850, tenor_days=90, domestic_rate_pct=5.0, foreign_rate_pct=3.5)
    fx_val = desk.price_fx_forward_parity(fx)
    assert fx_val["forward_rate"] > fx_val["spot_rate"]  # Forward points positive when domestic > foreign

    cds = CreditDefaultSwap("CDS_001", "SOVEREIGN_ENTITY_X", notional_protected_b=2.0, cds_spread_bps=85.0)
    cds_eval = desk.evaluate_credit_default_swap(cds)
    assert cds_eval["implied_annual_default_hazard_pct"] > 0.10
    assert cds_eval["annual_protection_premium_usd"] == 17_000_000.0


def test_autonomous_sovereign_bank_integration():
    bank = BankOfTheContinuum()
    
    # 1. Verify Core Accounts
    assert "ACC_TERRA_FLEET_01" in bank.accounts
    assert "ACC_AETHER_SMR_01" in bank.accounts
    assert "ACC_SOVEREIGN_TREASURY_PRIME" in bank.accounts

    # 2. Transfer Liquidity (Robot Fleet paying SMR power cluster)
    tx = bank.transfer_liquidity(
        source_account_id="ACC_TERRA_FLEET_01",
        dest_account_id="ACC_AETHER_SMR_01",
        amount_usd=25_000_000.0,
    )
    assert tx["status"] == "SETTLED_REAL_TIME"
    assert bank.accounts["ACC_TERRA_FLEET_01"].fiat_balance_usd == 225_000_000.0
    assert bank.accounts["ACC_AETHER_SMR_01"].fiat_balance_usd == 525_000_000.0

    # 3. Consolidated Audit
    audit = bank.generate_consolidated_banking_audit()
    assert audit["total_fiat_deposits_b"] > 10.0
    assert len(audit["divisions_active"]) == 10
    assert "Basel IV" in audit["regulatory_framework"]
