"""
Sovereign Banking Core: Derivatives Clearing & Quantitative Risk Engine.

Models the multi-hundred trillion dollar OTC and cleared derivatives market ($650T+ notional):
1. Interest Rate Swaps (IRS): SOFR fixed-for-floating, Net Present Value (NPV), and DV01 delta risk
2. FX Forwards & Cross-Currency Basis Swaps: Covered Interest Rate Parity (CIP) pricing
3. Credit Default Swaps (CDS): Hazard rate default probabilities, protection premiums, and recovery modeling
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import math


@dataclass
class InterestRateSwap:
    swap_id: str
    notional_amount_b: float
    tenor_years: int
    fixed_rate_pct: float
    floating_benchmark: str = "SOFR_COMPOUNDED"
    fixed_payer: str = "TERRA_KINETICS_TREASURY"
    floating_payer: str = "INVESTMENT_BANK_COUNTERPARTY"


@dataclass
class FXForwardContract:
    contract_id: str
    currency_pair: str  # EUR/USD, USD/JPY, USD/AED
    notional_base_currency: float
    spot_fx_rate: float
    tenor_days: int
    domestic_rate_pct: float
    foreign_rate_pct: float


@dataclass
class CreditDefaultSwap:
    cds_id: str
    reference_entity: str
    notional_protected_b: float
    cds_spread_bps: float
    recovery_rate_pct: float = 40.0  # Senior unsecured bond market standard


class DerivativesClearingDesk:
    """
    Clears and values multi-trillion OTC derivatives and risk-hedging structures.
    """

    def price_interest_rate_swap(
        self,
        swap: InterestRateSwap,
        current_market_sofr_pct: float,
    ) -> Dict[str, Any]:
        """
        Calculates Net Present Value (NPV) and DV01 (Dollar Value of a Basis Point) for an IRS.
        """
        # Rate difference: (Fixed - Market SOFR)
        spread_diff_pct = (current_market_sofr_pct - swap.fixed_rate_pct)
        # Approximate NPV = Notional * (Current Floating - Fixed) * Annuity Factor
        # Annuity factor approximation ~ Tenor / (1 + r)^tenor
        r = current_market_sofr_pct / 100.0
        annuity = (1.0 - (1.0 + r) ** (-swap.tenor_years)) / r if r > 0 else float(swap.tenor_years)

        npv_b = swap.notional_amount_b * (spread_diff_pct / 100.0) * annuity
        # DV01: Profit/Loss change for 1 basis point (0.01%) move
        dv01_usd = (swap.notional_amount_b * 1e9) * (0.0001) * annuity

        return {
            "swap_id": swap.swap_id,
            "notional_b": swap.notional_amount_b,
            "tenor_years": swap.tenor_years,
            "fixed_rate_contracted_pct": swap.fixed_rate_pct,
            "current_floating_sofr_pct": current_market_sofr_pct,
            "mark_to_market_npv_usd_m": round(npv_b * 1000.0, 2),
            "dv01_sensitivity_usd": round(dv01_usd, 2),
            "position_state": "IN_THE_MONEY" if npv_b >= 0 else "OUT_OF_THE_MONEY",
        }

    def price_fx_forward_parity(self, contract: FXForwardContract) -> Dict[str, Any]:
        """
        Prices an FX Forward using Covered Interest Rate Parity:
        F = S * (1 + r_d * t / 360) / (1 + r_f * t / 360)
        """
        t = contract.tenor_days / 360.0
        r_d = contract.domestic_rate_pct / 100.0
        r_f = contract.foreign_rate_pct / 100.0

        forward_rate = contract.spot_fx_rate * ((1.0 + (r_d * t)) / (1.0 + (r_f * t)))
        forward_points = (forward_rate - contract.spot_fx_rate) * 10000.0  # in pips

        return {
            "contract_id": contract.contract_id,
            "currency_pair": contract.currency_pair,
            "spot_rate": contract.spot_fx_rate,
            "forward_rate": round(forward_rate, 5),
            "forward_points_pips": round(forward_points, 2),
            "settlement_tenor_days": contract.tenor_days,
            "settlement_notional_usd": round(contract.notional_base_currency * forward_rate, 2),
            "pricing_model": "COVERED_INTEREST_RATE_PARITY",
        }

    def evaluate_credit_default_swap(self, cds: CreditDefaultSwap) -> Dict[str, Any]:
        """
        Estimates implied hazard rate (default probability per year) and annual protection payment.
        Formula: lambda = Spread / (1 - Recovery)
        """
        loss_given_default = (100.0 - cds.recovery_rate_pct) / 100.0
        spread_decimal = cds.cds_spread_bps / 10000.0
        implied_annual_hazard_rate_pct = (spread_decimal / loss_given_default) * 100.0 if loss_given_default > 0 else 0.0

        annual_premium_usd = (cds.notional_protected_b * 1e9) * spread_decimal
        potential_default_payout_usd = (cds.notional_protected_b * 1e9) * loss_given_default

        return {
            "cds_id": cds.cds_id,
            "reference_entity": cds.reference_entity,
            "notional_protected_b": cds.notional_protected_b,
            "cds_spread_bps": cds.cds_spread_bps,
            "implied_annual_default_hazard_pct": round(implied_annual_hazard_rate_pct, 3),
            "annual_protection_premium_usd": round(annual_premium_usd, 2),
            "contingent_payout_on_default_usd": round(potential_default_payout_usd, 2),
            "clearing_house": "Continuum_Central_Counterparty_Clearinghouse",
        }
