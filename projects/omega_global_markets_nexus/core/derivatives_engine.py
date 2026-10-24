"""
Multi-Asset Derivatives & Cross-Market Hedging Desk
Provides Black-Scholes-Merton option pricing, analytical Greeks, Implied Volatility root-solving,
Fixed-for-Floating SOFR Interest Rate Swaps (IRS), Garman-Kohlhagen FX Options, and Freight Forward Agreements (FFA).
"""
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional


class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"


def _norm_cdf(x: float) -> float:
    """Standard Normal Cumulative Distribution Function via erf."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    """Standard Normal Probability Density Function."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * (x ** 2))


@dataclass
class OptionGreeks:
    price: float
    delta: float
    gamma: float
    vega: float      # Per 1.0% (0.01) change in vol
    theta: float     # Per 1 calendar day decay
    rho: float       # Per 1.0% (0.01) change in rate


class BlackScholesEngine:
    """Institutional Black-Scholes-Merton European option pricer and Greeks engine."""

    @staticmethod
    def price_option(
        spot: float,
        strike: float,
        maturity_years: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
        option_type: OptionType = OptionType.CALL
    ) -> OptionGreeks:
        S = spot
        K = strike
        T = max(maturity_years, 1e-5)
        r = risk_free_rate
        q = dividend_yield
        sigma = max(volatility, 1e-5)

        sqrt_T = math.sqrt(T)
        d1 = (math.log(S / K) + (r - q + 0.5 * (sigma ** 2)) * T) / (sigma * sqrt_T)
        d2 = d1 - sigma * sqrt_T

        pdf_d1 = _norm_pdf(d1)
        exp_minus_qT = math.exp(-q * T)
        exp_minus_rT = math.exp(-r * T)

        if option_type == OptionType.CALL:
            price = S * exp_minus_qT * _norm_cdf(d1) - K * exp_minus_rT * _norm_cdf(d2)
            delta = exp_minus_qT * _norm_cdf(d1)
            rho = K * T * exp_minus_rT * _norm_cdf(d2) * 0.01
            theta = (
                -(S * exp_minus_qT * pdf_d1 * sigma) / (2.0 * sqrt_T)
                - r * K * exp_minus_rT * _norm_cdf(d2)
                + q * S * exp_minus_qT * _norm_cdf(d1)
            ) / 365.0
        else:
            price = K * exp_minus_rT * _norm_cdf(-d2) - S * exp_minus_qT * _norm_cdf(-d1)
            delta = -exp_minus_qT * _norm_cdf(-d1)
            rho = -K * T * exp_minus_rT * _norm_cdf(-d2) * 0.01
            theta = (
                -(S * exp_minus_qT * pdf_d1 * sigma) / (2.0 * sqrt_T)
                + r * K * exp_minus_rT * _norm_cdf(-d2)
                - q * S * exp_minus_qT * _norm_cdf(-d1)
            ) / 365.0

        gamma = (exp_minus_qT * pdf_d1) / (S * sigma * sqrt_T)
        vega = S * exp_minus_qT * sqrt_T * pdf_d1 * 0.01  # 1% vol change

        return OptionGreeks(
            price=round(price, 4),
            delta=round(delta, 4),
            gamma=round(gamma, 6),
            vega=round(vega, 4),
            theta=round(theta, 4),
            rho=round(rho, 4)
        )

    @staticmethod
    def solve_implied_volatility(
        target_price: float,
        spot: float,
        strike: float,
        maturity_years: float,
        risk_free_rate: float,
        option_type: OptionType = OptionType.CALL,
        max_iter: int = 100,
        tol: float = 1e-5
    ) -> float:
        """Solves for Black-Scholes implied volatility via Newton-Raphson."""
        sigma = 0.25  # Initial 25% guess
        for _ in range(max_iter):
            res = BlackScholesEngine.price_option(
                spot, strike, maturity_years, risk_free_rate, sigma, 0.0, option_type
            )
            diff = res.price - target_price
            if abs(diff) < tol:
                return round(sigma, 4)
            # Vega is derivative dPrice/dSigma (scaled by 100 back to raw units)
            raw_vega = res.vega * 100.0
            if abs(raw_vega) < 1e-10:
                break
            sigma = sigma - diff / raw_vega
            if sigma <= 0.001:
                sigma = 0.001

        return round(sigma, 4)


@dataclass
class InterestRateSwapContract:
    """
    Fixed-for-Floating SOFR Interest Rate Swap.
    Payer receives floating SOFR, pays fixed coupon.
    """
    notional_usd: float
    tenor_years: int
    fixed_rate_pct: float
    floating_sofr_benchmark_pct: float
    payment_frequency: int = 2  # Semi-annual

    def calculate_swap_valuation(self, discount_curve_rates: Dict[int, float]) -> Dict[str, float]:
        """
        Computes Net Present Value (NPV) and Par Swap Rate.
        discount_curve_rates maps year index (e.g. 1, 2, 3...) to zero rate fraction.
        """
        n_periods = self.tenor_years * self.payment_frequency
        tau = 1.0 / self.payment_frequency
        fixed_coupon = (self.fixed_rate_pct / 100.0) * tau

        pv_fixed_leg = 0.0
        pv_float_leg = 0.0
        sum_discount_factors = 0.0

        for p in range(1, n_periods + 1):
            t = p * tau
            # Approximate zero rate at time t
            yr = max(1, int(round(t)))
            zero_rate = discount_curve_rates.get(yr, 0.045)
            df = math.exp(-zero_rate * t)
            sum_discount_factors += df * tau

            # Fixed leg cash flow
            pv_fixed_leg += self.notional_usd * fixed_coupon * df

        # Floating leg approximation: Notional * (1 - P(0, T))
        terminal_df = math.exp(-discount_curve_rates.get(self.tenor_years, 0.045) * self.tenor_years)
        pv_float_leg = self.notional_usd * (1.0 - terminal_df)

        par_swap_rate = ((1.0 - terminal_df) / sum_discount_factors) * 100.0 if sum_discount_factors > 0 else 0.0
        # NPV for fixed rate payer = PV(Float) - PV(Fixed)
        payer_npv = pv_float_leg - pv_fixed_leg
        dv01 = sum_discount_factors * (self.notional_usd / 10_000.0)

        return {
            "notional_usd": self.notional_usd,
            "pv_fixed_leg_usd": round(pv_fixed_leg, 2),
            "pv_floating_leg_usd": round(pv_float_leg, 2),
            "payer_npv_usd": round(payer_npv, 2),
            "par_swap_rate_pct": round(par_swap_rate, 3),
            "swap_dv01_usd": round(dv01, 2)
        }


class GarmanKohlhagenFXOption:
    """Garman-Kohlhagen European Option on Foreign Exchange currency pairs."""

    @staticmethod
    def price_fx_option(
        spot_fx: float,
        strike_fx: float,
        maturity_years: float,
        domestic_rate: float,
        foreign_rate: float,
        volatility: float,
        option_type: OptionType = OptionType.CALL
    ) -> OptionGreeks:
        # Domestic rate is r, foreign rate acts as dividend yield q
        return BlackScholesEngine.price_option(
            spot=spot_fx,
            strike=strike_fx,
            maturity_years=maturity_years,
            risk_free_rate=domestic_rate,
            volatility=volatility,
            dividend_yield=foreign_rate,
            option_type=option_type
        )


class FreightForwardAgreementPricer:
    """Freight Forward Agreement (FFA) pricing and hedging for ocean container routes."""

    @staticmethod
    def price_ffa_hedge(
        spot_freight_usd_teu: float,
        forward_contract_rate_usd_teu: float,
        contracted_teu_volume: int,
        settlement_spot_freight_usd_teu: float
    ) -> Dict[str, Any]:
        """
        Hedging calculation:
        Total Physical Freight Cost = Volume * Settlement Spot
        FFA PnL = Volume * (Settlement Spot - Forward Rate)
        Net Effective Freight Cost = Physical Cost - FFA PnL = Volume * Forward Rate
        """
        physical_cost = contracted_teu_volume * settlement_spot_freight_usd_teu
        ffa_gain_loss = contracted_teu_volume * (settlement_spot_freight_usd_teu - forward_contract_rate_usd_teu)
        net_effective_cost = physical_cost - ffa_gain_loss
        savings_vs_spot = physical_cost - net_effective_cost

        return {
            "contracted_teu_volume": contracted_teu_volume,
            "forward_locked_rate_usd": forward_contract_rate_usd_teu,
            "actual_spot_at_settlement_usd": settlement_spot_freight_usd_teu,
            "unhedged_physical_cost_usd": physical_cost,
            "ffa_hedging_pnl_usd": ffa_gain_loss,
            "net_effective_freight_cost_usd": net_effective_cost,
            "cost_variance_saved_usd": savings_vs_spot
        }
