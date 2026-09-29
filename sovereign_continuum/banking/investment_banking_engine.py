"""
Sovereign Banking Core: Investment Banking, Capital Markets & Structured Finance Engine.

Models the engine of multi-trillion institutional capital deployment:
1. Debt Capital Markets (DCM): Sovereign & Corporate Mega-Bonds, Greenium, Bookbuilding
2. Syndicated Lending: Revolvers, Term Loan A/B, Covenant Checks (DSCR, Debt/EBITDA)
3. Securitization & Structured Credit: Physical cash-flow pooling (Robotics & SMR PPAs), Tranche Waterfalls (AAA/BBB/Equity)
4. M&A Advisory & Leveraged Buyout (LBO): Debt-to-Equity bridging, 5-year debt paydown, IRR & MoIC calculation
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import math


@dataclass
class BondTranche:
    isin_code: str
    issuer_name: str
    principal_amount_b: float
    tenor_years: int
    coupon_rate_pct: float
    benchmark_yield_pct: float
    credit_spread_bps: float
    is_green_bond: bool
    underwriting_fee_pct: float = 0.75  # 75 bps institutional fee


@dataclass
class SecuritizedPool:
    pool_id: str
    total_collateral_value_b: float
    annual_cashflow_b: float
    senior_aaa_share: float = 0.80      # 80% Senior AAA
    mezzanine_bbb_share: float = 0.15   # 15% Mezzanine BBB
    equity_first_loss_share: float = 0.05  # 5% First-Loss Equity


class DebtCapitalMarketsDesk:
    """
    Underwrites and prices mega-scale sovereign, green, and corporate debt issuances.
    """

    def price_and_bookbuild_bond(
        self,
        issuer: str,
        principal_b: float,
        tenor_years: int,
        benchmark_yield_pct: float,
        rating: str = "AAA",
        is_green: bool = True,
    ) -> Dict[str, Any]:
        spread_map = {"AAA": 45.0, "AA": 75.0, "A": 110.0, "BBB": 165.0, "BB": 320.0}
        base_spread_bps = spread_map.get(rating, 150.0)

        # Greenium: Green bonds enjoy ~8 bps concessionary discount in secondary markets
        greenium_bps = 8.0 if is_green else 0.0
        final_spread_bps = max(10.0, base_spread_bps - greenium_bps)
        final_coupon_pct = benchmark_yield_pct + (final_spread_bps / 100.0)

        # Standard closed-form Modified Duration for par bond: ModD = (1/r) * (1 - (1+r)^(-tenor))
        r = final_coupon_pct / 100.0
        if r > 0:
            modified_duration = (1.0 / r) * (1.0 - ((1.0 + r) ** (-tenor_years)))
        else:
            modified_duration = float(tenor_years)

        underwriting_fee_usd = (principal_b * 1e9) * 0.0075  # 75 bps
        net_proceeds_b = principal_b - (underwriting_fee_usd / 1e9)

        return {
            "issuer": issuer,
            "principal_b": principal_b,
            "tenor_years": tenor_years,
            "rating": rating,
            "is_green_bond": is_green,
            "final_coupon_pct": round(final_coupon_pct, 3),
            "final_spread_bps": round(final_spread_bps, 1),
            "greenium_savings_bps": greenium_bps,
            "modified_duration_years": round(modified_duration, 2),
            "underwriting_fee_usd_m": round(underwriting_fee_usd / 1e6, 2),
            "net_proceeds_b": round(net_proceeds_b, 3),
            "status": "OVERSUBSCRIBED_3.4X",
        }


class SyndicatedLendingDesk:
    """
    Structures multi-bank syndicated loan facilities for infrastructure and industrial scale.
    """

    def structure_syndicated_facility(
        self,
        borrower_name: str,
        facility_amount_b: float,
        ebitda_b: float,
        annual_debt_service_b: float,
        sofr_base_rate_pct: float = 4.85,
    ) -> Dict[str, Any]:
        # Tranche Split: 30% Revolver (RCF), 70% Term Loan B (TLB)
        rcf_amount_b = facility_amount_b * 0.30
        tlb_amount_b = facility_amount_b * 0.70

        # Margin: RCF SOFR+175 bps, TLB SOFR+275 bps
        rcf_rate = sofr_base_rate_pct + 1.75
        tlb_rate = sofr_base_rate_pct + 2.75

        # Covenant Health Checks
        leverage_ratio = facility_amount_b / ebitda_b if ebitda_b > 0 else 99.0
        dscr = (ebitda_b * 0.80) / annual_debt_service_b if annual_debt_service_b > 0 else 0.0

        covenants_pass = (leverage_ratio <= 4.5) and (dscr >= 1.5)

        return {
            "borrower": borrower_name,
            "total_facility_b": facility_amount_b,
            "rcf_tranche_b": round(rcf_amount_b, 2),
            "rcf_pricing": f"SOFR + 175 bps ({rcf_rate:.2f}%)",
            "tlb_tranche_b": round(tlb_amount_b, 2),
            "tlb_pricing": f"SOFR + 275 bps ({tlb_rate:.2f}%)",
            "leverage_ratio_debt_to_ebitda": round(leverage_ratio, 2),
            "debt_service_coverage_ratio_dscr": round(dscr, 2),
            "covenants_compliant": covenants_pass,
            "syndicate_lead": "Planetary_Continuum_Capital_Markets",
        }


class SecuritizationDesk:
    """
    Packages recurring physical robotic tolls and nuclear PPAs into rated asset-backed securities (ABS/CLO).
    """

    def structure_tranche_waterfall(self, pool: SecuritizedPool, default_shock_pct: float = 0.0) -> Dict[str, Any]:
        net_cashflow_b = pool.annual_cashflow_b * (1.0 - default_shock_pct)

        senior_notional = pool.total_collateral_value_b * pool.senior_aaa_share
        mezz_notional = pool.total_collateral_value_b * pool.mezzanine_bbb_share
        equity_notional = pool.total_collateral_value_b * pool.equity_first_loss_share

        # Senior coupon: 5.5%, Mezzanine coupon: 8.5%
        senior_interest_req = senior_notional * 0.055
        mezz_interest_req = mezz_notional * 0.085

        # Waterfall Payment:
        senior_paid = min(net_cashflow_b, senior_interest_req)
        remaining_after_senior = max(0.0, net_cashflow_b - senior_paid)

        mezz_paid = min(remaining_after_senior, mezz_interest_req)
        remaining_for_equity = max(0.0, remaining_after_senior - mezz_paid)

        equity_yield_pct = (remaining_for_equity / equity_notional) * 100.0 if equity_notional > 0 else 0.0

        senior_loss_occurred = senior_paid < senior_interest_req
        mezz_loss_occurred = mezz_paid < mezz_interest_req

        return {
            "pool_id": pool.pool_id,
            "collateral_value_b": pool.total_collateral_value_b,
            "gross_cashflow_b": pool.annual_cashflow_b,
            "net_cashflow_after_shock_b": round(net_cashflow_b, 3),
            "senior_aaa": {
                "notional_b": round(senior_notional, 2),
                "interest_due_b": round(senior_interest_req, 3),
                "interest_paid_b": round(senior_paid, 3),
                "loss_absorbed": senior_loss_occurred,
            },
            "mezzanine_bbb": {
                "notional_b": round(mezz_notional, 2),
                "interest_due_b": round(mezz_interest_req, 3),
                "interest_paid_b": round(mezz_paid, 3),
                "loss_absorbed": mezz_loss_occurred,
            },
            "equity_first_loss": {
                "notional_b": round(equity_notional, 2),
                "residual_cash_received_b": round(remaining_for_equity, 3),
                "realized_dividend_yield_pct": round(equity_yield_pct, 2),
            },
        }


class MAndAAdvisoryDesk:
    """
    Models multi-billion corporate M&A, divestitures, and Leveraged Buyouts (LBO).
    """

    def model_lbo_acquisition(
        self,
        target_name: str,
        entry_ebitda_b: float,
        entry_multiple: float = 12.0,
        debt_financing_pct: float = 0.65,
        exit_multiple: float = 12.0,
        holding_years: int = 5,
        annual_fcf_b: float = 2.5,
    ) -> Dict[str, Any]:
        enterprise_value_b = entry_ebitda_b * entry_multiple
        debt_initial_b = enterprise_value_b * debt_financing_pct
        equity_sponsor_initial_b = enterprise_value_b - debt_initial_b

        # 5-Year Debt Paydown: 70% of FCF goes to sweep debt
        cumulative_debt_repaid_b = (annual_fcf_b * 0.70) * holding_years
        debt_at_exit_b = max(0.0, debt_initial_b - cumulative_debt_repaid_b)

        # Exit Enterprise Value (assuming 5% EBITDA expansion/year)
        exit_ebitda_b = entry_ebitda_b * (1.05 ** holding_years)
        exit_ev_b = exit_ebitda_b * exit_multiple
        equity_sponsor_exit_b = exit_ev_b - debt_at_exit_b

        moic = equity_sponsor_exit_b / equity_sponsor_initial_b if equity_sponsor_initial_b > 0 else 0.0
        irr_pct = ((moic ** (1.0 / holding_years)) - 1.0) * 100.0 if moic > 0 else 0.0

        return {
            "target": target_name,
            "entry_enterprise_value_b": round(enterprise_value_b, 2),
            "initial_debt_b": round(debt_initial_b, 2),
            "sponsor_equity_check_b": round(equity_sponsor_initial_b, 2),
            "debt_repaid_over_hold_b": round(cumulative_debt_repaid_b, 2),
            "debt_remaining_at_exit_b": round(debt_at_exit_b, 2),
            "exit_enterprise_value_b": round(exit_ev_b, 2),
            "sponsor_exit_equity_value_b": round(equity_sponsor_exit_b, 2),
            "multiple_on_invested_capital_moic": round(moic, 2),
            "net_internal_rate_of_return_irr_pct": round(irr_pct, 2),
        }
