"""
Bond Market & Fixed Income Analytics Engine
Provides Nelson-Siegel Yield Curve fitting, bond pricing, Macaulay/Modified Duration,
Convexity hedging, DV01/PV01, and Credit Default Spread / Hazard Rate modeling.
"""
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class NelsonSiegelCurve:
    """
    Parametric Nelson-Siegel Yield Curve:
    y(m) = beta_0 + beta_1 * ((1 - e^(-m/tau)) / (m/tau)) + beta_2 * (((1 - e^(-m/tau)) / (m/tau)) - e^(-m/tau))
    beta_0: Level (long term asymptotic rate)
    beta_1: Slope (short term component)
    beta_2: Curvature (medium term hump)
    tau: Decay parameter
    """
    beta_0: float = 0.048  # 4.80% long-term rate
    beta_1: float = -0.012 # Initial upward slope
    beta_2: float = 0.015  # Curvature hump around 2-5Y
    tau: float = 2.5       # Peak curvature around 2.5 years

    def get_zero_rate(self, maturity_years: float) -> float:
        if maturity_years <= 0.001:
            return self.beta_0 + self.beta_1
        m_tau = maturity_years / self.tau
        factor1 = (1.0 - math.exp(-m_tau)) / m_tau
        factor2 = factor1 - math.exp(-m_tau)
        rate = self.beta_0 + (self.beta_1 * factor1) + (self.beta_2 * factor2)
        return round(rate, 6)

    def generate_tenor_ladder(self) -> Dict[str, float]:
        tenors = {
            "3M": 0.25,
            "6M": 0.50,
            "1Y": 1.0,
            "2Y": 2.0,
            "3Y": 3.0,
            "5Y": 5.0,
            "7Y": 7.0,
            "10Y": 10.0,
            "20Y": 20.0,
            "30Y": 30.0
        }
        return {k: round(self.get_zero_rate(v) * 100.0, 3) for k, v in tenors.items()}

    def check_curve_inversion(self) -> Dict[str, any]:
        r_2y = self.get_zero_rate(2.0)
        r_10y = self.get_zero_rate(10.0)
        spread_bps = round((r_10y - r_2y) * 10_000.0, 1)
        is_inverted = spread_bps < 0
        return {
            "2y_rate_pct": round(r_2y * 100.0, 3),
            "10y_rate_pct": round(r_10y * 100.0, 3),
            "spread_10y_2y_bps": spread_bps,
            "is_inverted": is_inverted,
            "signal": "RECESSION_WARNING" if is_inverted else "NORMAL_EXPANSION"
        }


@dataclass
class FixedCouponBond:
    cusip: str
    issuer: str
    par_value: float            # typically 1,000.0
    coupon_rate_pct: float      # e.g., 5.0 for 5.0%
    maturity_years: float
    frequency: int = 2          # 2 for semi-annual, 1 for annual
    seniority: str = "Senior Unsecured"

    def price_at_yield(self, ytm_pct: float) -> float:
        """Computes clean price of bond given an annual Yield to Maturity."""
        y = ytm_pct / 100.0
        k = self.frequency
        n = int(round(self.maturity_years * k))
        coupon_payment = (self.par_value * (self.coupon_rate_pct / 100.0)) / k

        if y <= 0:
            return round((coupon_payment * n) + self.par_value, 4)

        pv_coupons = sum(coupon_payment / ((1.0 + y / k) ** t) for t in range(1, n + 1))
        pv_par = self.par_value / ((1.0 + y / k) ** n)
        return round(pv_coupons + pv_par, 4)

    def solve_ytm(self, target_price: float, max_iter: int = 100, tol: float = 1e-6) -> float:
        """Solves for YTM percentage using Newton-Raphson root finding."""
        y = self.coupon_rate_pct / 100.0  # Initial guess
        for _ in range(max_iter):
            p = self.price_at_yield(y * 100.0)
            diff = p - target_price
            if abs(diff) < tol:
                return round(y * 100.0, 4)
            # Derivative dp/dy
            k = self.frequency
            n = int(round(self.maturity_years * k))
            coupon = (self.par_value * (self.coupon_rate_pct / 100.0)) / k
            dp_dy = sum(- (t / k) * coupon / ((1.0 + y / k) ** (t + 1)) for t in range(1, n + 1))
            dp_dy += - (n / k) * self.par_value / ((1.0 + y / k) ** (n + 1))

            if abs(dp_dy) < 1e-12:
                break
            y = y - diff / dp_dy

        return round(y * 100.0, 4)

    def calculate_duration_convexity(self, ytm_pct: float) -> Dict[str, float]:
        """
        Calculates:
        - Macaulay Duration (years)
        - Modified Duration (years)
        - Dollar Duration (DV01 / PV01 per $1,000,000 face value)
        - Convexity
        """
        y = ytm_pct / 100.0
        k = self.frequency
        n = int(round(self.maturity_years * k))
        coupon = (self.par_value * (self.coupon_rate_pct / 100.0)) / k
        price = self.price_at_yield(ytm_pct)

        weighted_time_cf = sum((t / k) * coupon / ((1.0 + y / k) ** t) for t in range(1, n + 1))
        weighted_time_cf += (n / k) * self.par_value / ((1.0 + y / k) ** n)

        macaulay_duration = weighted_time_cf / price
        modified_duration = macaulay_duration / (1.0 + y / k)

        # DV01 (Dollar change per 1 basis point change in yield per bond)
        dv01_per_bond = modified_duration * price * 0.0001
        dv01_per_million = (1_000_000.0 / self.par_value) * dv01_per_bond

        # Convexity
        convexity_sum = sum((t * (t + 1) / (k ** 2)) * coupon / ((1.0 + y / k) ** (t + 2)) for t in range(1, n + 1))
        convexity_sum += (n * (n + 1) / (k ** 2)) * self.par_value / ((1.0 + y / k) ** (n + 2))
        convexity = convexity_sum / price

        return {
            "price": price,
            "ytm_pct": ytm_pct,
            "macaulay_duration_years": round(macaulay_duration, 3),
            "modified_duration_years": round(modified_duration, 3),
            "dv01_per_bond_usd": round(dv01_per_bond, 4),
            "dv01_per_million_usd": round(dv01_per_million, 2),
            "convexity": round(convexity, 3)
        }

    def estimate_price_impact(self, current_ytm_pct: float, yield_shift_bps: float) -> Dict[str, float]:
        """Estimates percentage price change using 1st order (Duration) and 2nd order (Convexity) Taylor approximation."""
        metrics = self.calculate_duration_convexity(current_ytm_pct)
        mod_dur = metrics["modified_duration_years"]
        conv = metrics["convexity"]
        delta_y = yield_shift_bps / 10_000.0  # 1 bp = 0.0001

        duration_impact = -mod_dur * delta_y
        convexity_impact = 0.5 * conv * (delta_y ** 2)
        total_estimated_pct = (duration_impact + convexity_impact) * 100.0

        actual_new_price = self.price_at_yield(current_ytm_pct + (yield_shift_bps / 100.0))
        actual_pct_change = ((actual_new_price - metrics["price"]) / metrics["price"]) * 100.0

        return {
            "yield_shift_bps": yield_shift_bps,
            "duration_impact_pct": round(duration_impact * 100.0, 3),
            "convexity_impact_pct": round(convexity_impact * 100.0, 3),
            "total_estimated_pct_change": round(total_estimated_pct, 3),
            "actual_pct_change": round(actual_pct_change, 3)
        }


class CorporateCreditSpreadAnalyzer:
    """Evaluates corporate bond credit spreads against risk-free sovereign benchmarks and computes implied default hazard rates."""

    @staticmethod
    def analyze_spread(
        corporate_ytm_pct: float,
        benchmark_sovereign_ytm_pct: float,
        expected_recovery_rate_pct: float = 40.0
    ) -> Dict[str, float]:
        spread_bps = (corporate_ytm_pct - benchmark_sovereign_ytm_pct) * 100.0
        recovery_fraction = expected_recovery_rate_pct / 100.0

        # Hazard rate approximation: lambda = spread / (1 - R)
        loss_given_default = 1.0 - recovery_fraction
        hazard_rate_annual = (spread_bps / 10_000.0) / loss_given_default if loss_given_default > 0 else 0.0

        # Cumulative probability of default over 5 years: PD_5 = 1 - exp(-lambda * 5)
        cumulative_pd_5yr = (1.0 - math.exp(-hazard_rate_annual * 5.0)) * 100.0

        return {
            "corporate_ytm_pct": corporate_ytm_pct,
            "benchmark_ytm_pct": benchmark_sovereign_ytm_pct,
            "credit_spread_bps": round(spread_bps, 1),
            "loss_given_default_pct": round(loss_given_default * 100.0, 1),
            "annual_hazard_rate_pct": round(hazard_rate_annual * 100.0, 3),
            "cumulative_5yr_default_prob_pct": round(cumulative_pd_5yr, 2)
        }
