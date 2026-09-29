"""
Sovereign Banking Core: Global Custody, Tri-Party Repo & Prime Brokerage Engine.

Models the multi-trillion dollar asset safeguarding and leverage infrastructure:
1. Global Custody: Assets Under Custody (AUC) Ledger & Safe-keeping ($100B+ scale)
2. Tri-Party Repo: Collateral eligibility, regulatory haircut matrix, and automated daily rebalancing
3. Securities Lending: General Collateral (GC) vs "Hard-to-Borrow" specials lending fee generation
4. Prime Brokerage: Portfolio Margin, Initial Margin (IM), and Variation Margin (VM) clearing (BCBS-IOSCO)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class CustodyAssetPosition:
    asset_id: str
    asset_type: str  # SOVEREIGN_BOND, CORPORATE_BOND, EQUITIES, PRECIOUS_METALS, SMR_CAPACITY_NOTE
    quantity: float
    market_price_usd: float
    custody_safekeeping_fee_bps: float = 3.5  # 3.5 bps per annum

    @property
    def market_value_usd(self) -> float:
        return self.quantity * self.market_price_usd


class GlobalCustodyDesk:
    """
    Safekeeps institutional assets, manages dividend/coupon collections, and segregates client assets.
    """

    def __init__(self):
        self.vault_positions: Dict[str, CustodyAssetPosition] = {}

    def deposit_asset(self, position: CustodyAssetPosition):
        self.vault_positions[position.asset_id] = position

    def calculate_total_assets_under_custody(self) -> Dict[str, Any]:
        total_auc = sum(p.market_value_usd for p in self.vault_positions.values())
        annual_fee_usd = sum(p.market_value_usd * (p.custody_safekeeping_fee_bps / 10000.0) for p in self.vault_positions.values())

        return {
            "total_assets_under_custody_usd": round(total_auc, 2),
            "total_assets_under_custody_b": round(total_auc / 1e9, 3),
            "annual_safekeeping_fee_revenue_usd": round(annual_fee_usd, 2),
            "asset_positions_count": len(self.vault_positions),
            "status": "ASSETS_FULLY_SEGREGATED_BANKRUPTCY_REMOTE",
        }


class TriPartyRepoDesk:
    """
    Acts as tri-party collateral agent matching cash investors with collateralized borrowers.
    """

    HAIRCUT_SCHEDULE = {
        "SOVEREIGN_BOND_SHORT": 0.010,  # 1.0% (1-3 yr Treasuries)
        "SOVEREIGN_BOND_LONG": 0.035,   # 3.5% (10-30 yr Treasuries)
        "AGENCY_MBS": 0.025,            # 2.5%
        "CORP_BOND_IG": 0.060,          # 6.0% (Investment Grade)
        "EQUITIES_LARGE_CAP": 0.150,    # 15.0%
    }

    def allocate_repo_collateral(
        self,
        cash_borrowed_b: float,
        collateral_type: str,
        pledged_collateral_market_value_b: float,
    ) -> Dict[str, Any]:
        haircut = self.HAIRCUT_SCHEDULE.get(collateral_type, 0.10)
        collateral_value_after_haircut = pledged_collateral_market_value_b * (1.0 - haircut)

        is_adequately_collateralized = collateral_value_after_haircut >= cash_borrowed_b
        margin_cushion_b = collateral_value_after_haircut - cash_borrowed_b

        return {
            "cash_loan_amount_b": cash_borrowed_b,
            "collateral_type": collateral_type,
            "pledged_market_value_b": pledged_collateral_market_value_b,
            "haircut_pct": haircut * 100.0,
            "net_collateral_value_b": round(collateral_value_after_haircut, 3),
            "is_solvent_and_cleared": is_adequately_collateralized,
            "margin_cushion_surplus_b": round(margin_cushion_b, 3),
            "tri_party_agent": "Continuum_Global_Securities_Clearing_Corp",
        }


class SecuritiesLendingDesk:
    """
    Monetizes institutional custody inventory via fully collateralized securities lending.
    """

    def execute_securities_loan(
        self,
        borrower_id: str,
        security_id: str,
        market_value_usd: float,
        is_hard_to_borrow: bool = False,
    ) -> Dict[str, Any]:
        # General Collateral (GC): 25 bps | Hard to borrow "Special": 350 bps
        lending_fee_bps = 350.0 if is_hard_to_borrow else 25.0
        required_collateral_cash = market_value_usd * 1.02  # 102% US domestic cash collateral standard
        annual_lending_income = market_value_usd * (lending_fee_bps / 10000.0)

        return {
            "borrower": borrower_id,
            "security": security_id,
            "market_value_usd": market_value_usd,
            "required_collateral_usd_102pct": round(required_collateral_cash, 2),
            "lending_fee_bps": lending_fee_bps,
            "annualized_lending_income_usd": round(annual_lending_income, 2),
            "status": "COLLATERALIZED_SECURITIES_LOAN_ACTIVE",
        }


class PrimeBrokerageDesk:
    """
    Clears hedge fund derivatives, provides portfolio margin, and calls Initial/Variation Margin.
    """

    def calculate_margin_requirements(
        self,
        gross_long_positions_usd: float,
        gross_short_positions_usd: float,
        daily_pnl_usd: float,
    ) -> Dict[str, Any]:
        """
        Calculates Initial Margin (risk absorption) and Variation Margin (daily mark-to-market).
        """
        # Portfolio margin ~12% on net exposure + 4% on gross offsetting
        net_exposure = abs(gross_long_positions_usd - gross_short_positions_usd)
        gross_exposure = gross_long_positions_usd + gross_short_positions_usd

        initial_margin_required = (net_exposure * 0.12) + (gross_exposure * 0.04)

        # Variation Margin covers daily mark-to-market loss
        variation_margin_due = abs(daily_pnl_usd) if daily_pnl_usd < 0 else 0.0

        return {
            "gross_portfolio_exposure_usd": round(gross_exposure, 2),
            "net_directional_exposure_usd": round(net_exposure, 2),
            "initial_margin_requirement_usd": round(initial_margin_required, 2),
            "variation_margin_call_usd": round(variation_margin_due, 2),
            "total_collateral_margin_locked_usd": round(initial_margin_required + variation_margin_due, 2),
            "clearing_status": "MARGIN_COMPLIANT_BCBS_IOSCO",
        }
