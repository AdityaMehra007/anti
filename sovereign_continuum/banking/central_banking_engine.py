"""
Sovereign Banking Core: Central Banking & Planetary Liquidity Engine.

Models the supreme tier of monetary architecture ($30+ Trillion aggregate central bank balance sheets):
1. Interest Rate Corridor Dynamics (Floor / Target / Ceiling)
2. Open Market Operations (Quantitative Easing / Tightening)
3. Discount Window (Primary Credit / Lender of Last Resort)
4. Overnight Reverse Repo Facility (ON RRP)
5. Sovereign Bilateral FX Swap Lines (C6 Network: Fed, ECB, BOJ, BOE, SNB, BOC)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time


@dataclass
class LiquidityCorridor:
    floor_rate_pct: float       # Interest on Reserve Balances (IORB / ON RRP)
    target_policy_rate_pct: float  # Central policy target (e.g. Fed Funds / SOFR)
    ceiling_discount_rate_pct: float  # Primary Credit / Lombard rate


@dataclass
class CentralBankBalanceSheet:
    # Assets ($B)
    sovereign_treasuries_b: float
    mbs_and_agency_debt_b: float
    discount_window_loans_b: float
    foreign_exchange_reserves_b: float
    swap_line_claims_b: float

    # Liabilities ($B)
    currency_in_circulation_b: float
    commercial_bank_reserves_b: float
    overnight_reverse_repo_b: float
    treasury_general_account_b: float

    @property
    def total_assets_b(self) -> float:
        return (
            self.sovereign_treasuries_b
            + self.mbs_and_agency_debt_b
            + self.discount_window_loans_b
            + self.foreign_exchange_reserves_b
            + self.swap_line_claims_b
        )

    @property
    def total_liabilities_b(self) -> float:
        return (
            self.currency_in_circulation_b
            + self.commercial_bank_reserves_b
            + self.overnight_reverse_repo_b
            + self.treasury_general_account_b
        )


class CentralBankingFacility:
    """
    Simulates sovereign central bank liquidity mechanisms and balance sheet expansion.
    """

    def __init__(
        self,
        name: str = "Planetary_Continuum_Reserve_Bank",
        corridor: Optional[LiquidityCorridor] = None,
        balance_sheet: Optional[CentralBankBalanceSheet] = None,
    ):
        self.name = name
        self.corridor = corridor or LiquidityCorridor(
            floor_rate_pct=4.80,
            target_policy_rate_pct=5.00,
            ceiling_discount_rate_pct=5.25,
        )
        self.balance_sheet = balance_sheet or CentralBankBalanceSheet(
            sovereign_treasuries_b=4500.0,
            mbs_and_agency_debt_b=2200.0,
            discount_window_loans_b=15.0,
            foreign_exchange_reserves_b=450.0,
            swap_line_claims_b=120.0,
            currency_in_circulation_b=2300.0,
            commercial_bank_reserves_b=3200.0,
            overnight_reverse_repo_b=1100.0,
            treasury_general_account_b=685.0,
        )
        self.swap_lines_active: Dict[str, float] = {}

    def execute_open_market_operation(self, amount_b: float, is_qe: bool = True) -> Dict[str, float]:
        """
        Executes Quantitative Easing (asset purchase funded by reserves) or Quantitative Tightening (redemption).
        """
        if is_qe:
            self.balance_sheet.sovereign_treasuries_b += amount_b
            self.balance_sheet.commercial_bank_reserves_b += amount_b
            action = "QUANTITATIVE_EASING_PURCHASE"
        else:
            self.balance_sheet.sovereign_treasuries_b -= amount_b
            self.balance_sheet.commercial_bank_reserves_b -= amount_b
            action = "QUANTITATIVE_TIGHTENING_DRAIN"

        return {
            "action": action,
            "delta_b": amount_b,
            "new_total_assets_b": round(self.balance_sheet.total_assets_b, 2),
            "new_bank_reserves_b": round(self.balance_sheet.commercial_bank_reserves_b, 2),
        }

    def access_discount_window(
        self,
        borrowing_bank_id: str,
        collateral_market_value_b: float,
        haircut_pct: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Provides emergency primary credit liquidity against pledged eligible collateral.
        """
        advance_limit_b = collateral_market_value_b * (1.0 - haircut_pct)
        # Lend at the discount rate ceiling
        rate_charged = self.corridor.ceiling_discount_rate_pct

        self.balance_sheet.discount_window_loans_b += advance_limit_b
        self.balance_sheet.commercial_bank_reserves_b += advance_limit_b

        return {
            "borrower_id": borrowing_bank_id,
            "collateral_pledged_b": collateral_market_value_b,
            "haircut_pct": haircut_pct * 100.0,
            "credit_advanced_b": round(advance_limit_b, 3),
            "interest_rate_pct": rate_charged,
            "facility": "PRIMARY_CREDIT_DISCOUNT_WINDOW",
        }

    def conduct_overnight_reverse_repo(self, counterparty_id: str, amount_b: float) -> Dict[str, Any]:
        """
        Moots excess cash from non-bank financial institutions (money market funds) to defend floor rate.
        """
        self.balance_sheet.overnight_reverse_repo_b += amount_b
        self.balance_sheet.commercial_bank_reserves_b -= amount_b

        return {
            "counterparty": counterparty_id,
            "amount_absorbed_b": amount_b,
            "floor_rate_paid_pct": self.corridor.floor_rate_pct,
            "facility": "OVERNIGHT_REVERSE_REPO_FACILITY",
        }

    def activate_c6_currency_swap_line(
        self,
        partner_central_bank: str,  # "ECB", "BOJ", "BOE", "SNB", "BOC"
        usd_draw_amount_b: float,
        spot_fx_rate: float,
    ) -> Dict[str, Any]:
        """
        Activates bilateral central bank currency swap line preventing offshore USD shortages.
        """
        self.balance_sheet.swap_line_claims_b += usd_draw_amount_b
        self.balance_sheet.commercial_bank_reserves_b += usd_draw_amount_b
        self.swap_lines_active[partner_central_bank] = usd_draw_amount_b

        return {
            "partner_central_bank": partner_central_bank,
            "usd_liquidity_injected_b": usd_draw_amount_b,
            "foreign_currency_held_b": round(usd_draw_amount_b * spot_fx_rate, 2),
            "interest_rate_pct": self.corridor.target_policy_rate_pct + 0.25,
            "status": "SWAP_LINE_ACTIVE",
        }
