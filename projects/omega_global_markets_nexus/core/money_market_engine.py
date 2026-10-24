"""
Money Market & Short-Term Liquidity Desk Engine
Models Treasury Bills (T-Bills), Commercial Paper (CP), SOFR-benchmarked Repo/Reverse Repo facilities,
Automated Corporate Cash Sweeps, and Basel III Liquidity Coverage Ratio (LCR) compliance.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class CollateralTier(Enum):
    LEVEL_1_SOVEREIGN = "Level 1 Sovereign (G10 T-Bills / Notes)"
    LEVEL_2A_AGENCY = "Level 2A Agency / Supranational Debt"
    LEVEL_2B_CORPORATE = "Level 2B Investment Grade Corporate Paper"


@dataclass
class TBillInstrument:
    cusip: str
    tenor_days: int             # e.g., 28, 91, 182, 364
    face_value_usd: float
    discount_rate_pct: float    # e.g., 5.15%

    @property
    def purchase_price(self) -> float:
        """Computes clean purchase price using standard money-market 360-day year convention."""
        discount_fraction = (self.discount_rate_pct / 100.0) * (self.tenor_days / 360.0)
        return round(self.face_value_usd * (1.0 - discount_fraction), 4)

    @property
    def bond_equivalent_yield_pct(self) -> float:
        """Converts discount rate to 365-day Bond Equivalent Yield (BEY)."""
        price = self.purchase_price
        if price == 0:
            return 0.0
        bey = ((self.face_value_usd - price) / price) * (365.0 / self.tenor_days) * 100.0
        return round(bey, 3)


@dataclass
class CommercialPaper:
    issuer: str
    credit_tier: str            # A-1/P-1 (Prime) or A-2/P-2
    face_value_usd: float
    maturity_days: int
    yield_pct: float

    @property
    def price_usd(self) -> float:
        discount = (self.yield_pct / 100.0) * (self.maturity_days / 360.0)
        return round(self.face_value_usd * (1.0 - discount), 2)


@dataclass
class RepoContract:
    contract_id: str
    counterparty: str
    collateral_tier: CollateralTier
    collateral_market_value_usd: float
    repo_rate_pct: float        # SOFR + spread
    term_days: int              # 1 for overnight, 7, 30, etc.

    @property
    def haircut_pct(self) -> float:
        haircuts = {
            CollateralTier.LEVEL_1_SOVEREIGN: 2.0,
            CollateralTier.LEVEL_2A_AGENCY: 5.0,
            CollateralTier.LEVEL_2B_CORPORATE: 12.0
        }
        return haircuts[self.collateral_tier]

    @property
    def loan_amount_usd(self) -> float:
        """Maximum cash lent/borrowed against the collateral after applying the regulatory haircut."""
        return round(self.collateral_market_value_usd * (1.0 - (self.haircut_pct / 100.0)), 2)

    @property
    def interest_payable_usd(self) -> float:
        """Repo interest computed on actual cash borrowed using 360-day day-count convention."""
        return round(self.loan_amount_usd * (self.repo_rate_pct / 100.0) * (self.term_days / 360.0), 2)

    @property
    def repurchase_price_usd(self) -> float:
        return round(self.loan_amount_usd + self.interest_payable_usd, 2)


class TreasuryCashSweepDesk:
    """
    Automated Institutional Cash Sweeper.
    Allocates idle operational cash balances into optimal short-term yield tiers
    while maintaining target liquidity reserves.
    """

    @staticmethod
    def execute_sweep(
        total_cash_usd: float,
        overnight_buffer_target_usd: float = 5_000_000.0,
        sofr_overnight_rate_pct: float = 5.30,
        tbill_30d_rate_pct: float = 5.20,
        cp_90d_rate_pct: float = 5.45
    ) -> Dict[str, any]:
        if total_cash_usd <= overnight_buffer_target_usd:
            return {
                "total_cash_usd": total_cash_usd,
                "overnight_operational_cash": total_cash_usd,
                "swept_to_sofr_repo": 0.0,
                "swept_to_30d_tbills": 0.0,
                "swept_to_90d_cp": 0.0,
                "weighted_blended_yield_pct": 0.50, # Nominal checking account rate
                "annualized_interest_income_usd": round(total_cash_usd * 0.005, 2)
            }

        surplus_cash = total_cash_usd - overnight_buffer_target_usd
        # Allocation strategy: 40% SOFR Overnight Repo, 35% 30-Day T-Bills, 25% 90-Day Prime CP
        repo_alloc = surplus_cash * 0.40
        tbill_alloc = surplus_cash * 0.35
        cp_alloc = surplus_cash * 0.25

        interest_buffer = overnight_buffer_target_usd * 0.005
        interest_repo = repo_alloc * (sofr_overnight_rate_pct / 100.0)
        interest_tbill = tbill_alloc * (tbill_30d_rate_pct / 100.0)
        interest_cp = cp_alloc * (cp_90d_rate_pct / 100.0)

        total_annual_interest = interest_buffer + interest_repo + interest_tbill + interest_cp
        blended_yield = (total_annual_interest / total_cash_usd) * 100.0

        return {
            "total_cash_usd": total_cash_usd,
            "overnight_operational_cash": overnight_buffer_target_usd,
            "swept_to_sofr_repo": round(repo_alloc, 2),
            "swept_to_30d_tbills": round(tbill_alloc, 2),
            "swept_to_90d_cp": round(cp_alloc, 2),
            "weighted_blended_yield_pct": round(blended_yield, 3),
            "annualized_interest_income_usd": round(total_annual_interest, 2)
        }


class Basel3LiquidityAuditor:
    """Evaluates institutional Liquidity Coverage Ratio (LCR) under Basel III standard."""

    @staticmethod
    def audit_lcr(
        level_1_assets_usd: float,
        level_2a_assets_usd: float,
        level_2b_assets_usd: float,
        operational_deposits_outflow_usd: float,
        non_operational_deposits_outflow_usd: float,
        contractual_cash_inflows_30d_usd: float
    ) -> Dict[str, any]:
        """
        Total HQLA = Level 1 (0% haircut) + Level 2A (15% haircut) + Level 2B (50% haircut).
        Level 2 cannot exceed 40% of total HQLA; Level 2B cannot exceed 15%.
        Net Cash Outflows = Outflows - Min(Inflows, 75% of Outflows).
        """
        # HQLA computation
        hqla_l1 = level_1_assets_usd * 1.00
        hqla_l2a = level_2a_assets_usd * 0.85
        hqla_l2b = level_2b_assets_usd * 0.50

        # Cap checks for Basel III
        total_raw_hqla = hqla_l1 + hqla_l2a + hqla_l2b
        capped_l2b = min(hqla_l2b, total_raw_hqla * 0.15)
        capped_l2 = min(hqla_l2a + capped_l2b, total_raw_hqla * 0.40)
        total_hqla = round(hqla_l1 + capped_l2, 2)

        # Run-offs: 25% on non-operational, 5% on operational
        expected_outflows = (operational_deposits_outflow_usd * 0.05) + (non_operational_deposits_outflow_usd * 0.25)
        max_inflow_credit = expected_outflows * 0.75
        effective_inflows = min(contractual_cash_inflows_30d_usd, max_inflow_credit)
        net_cash_outflows = max(1.0, expected_outflows - effective_inflows)

        lcr_ratio_pct = (total_hqla / net_cash_outflows) * 100.0
        status = "COMPLIANT_PRUDENT" if lcr_ratio_pct >= 110.0 else (
            "COMPLIANT_BORDERLINE" if lcr_ratio_pct >= 100.0 else "NON_COMPLIANT_BREACH"
        )

        return {
            "total_hqla_usd": total_hqla,
            "level_1_usd": round(hqla_l1, 2),
            "level_2_usd": round(capped_l2, 2),
            "net_30d_outflows_usd": round(net_cash_outflows, 2),
            "lcr_ratio_pct": round(lcr_ratio_pct, 2),
            "regulatory_minimum_pct": 100.0,
            "compliance_status": status
        }
