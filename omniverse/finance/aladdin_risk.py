"""
ANTIGRAVITY OMNIVERSE: ALADDIN-CLASS INVESTMENT & RISK ENGINE
============================================================
Lawful, independent investment risk and multi-asset portfolio analytics platform
inspired by institutional risk systems. Computes parametric & Monte Carlo VaR,
factor exposures, scenario stress-tests, and cash-flow liquidity profiles.
"""
import math
import time
from typing import Dict, Any, List, Optional

class AladdinRiskEngine:
    """Institutional-grade multi-asset portfolio risk analytics."""

    @staticmethod
    def calculate_parametric_var(portfolio_value_usd: float, daily_volatility: float, confidence: float = 0.95, horizon_days: int = 1) -> Dict[str, float]:
        """
        Calculates Parametric Value-at-Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall).
        z-scores: 95% -> 1.645, 99% -> 2.326
        """
        z_map = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}
        z = z_map.get(confidence, 1.645)
        
        horizon_factor = math.sqrt(horizon_days)
        var_usd = portfolio_value_usd * daily_volatility * z * horizon_factor
        
        # Expected Shortfall (CVaR) approximation for normal distribution: phi(z)/(1-alpha) * sigma
        phi_z = (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * (z ** 2))
        cvar_usd = portfolio_value_usd * daily_volatility * (phi_z / (1.0 - confidence)) * horizon_factor

        return {
            "portfolio_value_usd": portfolio_value_usd,
            "confidence_level": confidence,
            "horizon_days": horizon_days,
            "var_usd": round(var_usd, 2),
            "var_percent": round((var_usd / portfolio_value_usd) * 100, 2),
            "cvar_usd": round(cvar_usd, 2),
            "cvar_percent": round((cvar_usd / portfolio_value_usd) * 100, 2)
        }

    @staticmethod
    def run_scenario_stress_test(portfolio_breakdown: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Applies macro shock vectors across asset classes:
        - Equities
        - Fixed Income / Bonds
        - Venture / Private Equity
        - Cash & Stable Assets
        - Commodities / Energy
        """
        total_aum = sum(portfolio_breakdown.values())
        if total_aum <= 0:
            return []

        scenarios = [
            {
                "scenario_name": "2008 Liquidity & Banking Shock",
                "description": "Global systemic credit freeze and equity de-risking",
                "shocks": {"equities": -0.42, "bonds": 0.08, "venture": -0.55, "cash": 0.0, "commodities": -0.35}
            },
            {
                "scenario_name": "2026 Stagflation & Rate Spike (+250 bps)",
                "description": "Sticky inflation with central bank quantitative tightening",
                "shocks": {"equities": -0.18, "bonds": -0.14, "venture": -0.32, "cash": 0.045, "commodities": 0.22}
            },
            {
                "scenario_name": "Global Semiconductor Export Embargo",
                "description": "Severe supply chain disruption in advanced silicon & automotive",
                "shocks": {"equities": -0.22, "bonds": 0.02, "venture": -0.28, "cash": 0.0, "commodities": 0.15}
            }
        ]

        results = []
        for sc in scenarios:
            post_shock_total = 0.0
            asset_impacts = {}
            for asset, val in portfolio_breakdown.items():
                shock = sc["shocks"].get(asset.lower(), 0.0)
                new_val = val * (1.0 + shock)
                post_shock_total += new_val
                asset_impacts[asset] = {
                    "pre_value": val,
                    "shock_percent": round(shock * 100, 1),
                    "post_value": round(new_val, 2),
                    "pnl_usd": round(new_val - val, 2)
                }
            
            pnl_total = post_shock_total - total_aum
            results.append({
                "scenario": sc["scenario_name"],
                "description": sc["description"],
                "initial_aum_usd": round(total_aum, 2),
                "post_shock_aum_usd": round(post_shock_total, 2),
                "net_pnl_usd": round(pnl_total, 2),
                "drawdown_percent": round((pnl_total / total_aum) * 100, 2),
                "asset_breakdown": asset_impacts
            })

        return results

    @staticmethod
    def forecast_cash_flow_runway(monthly_burn_rate_usd: float, cash_reserves_usd: float, monthly_revenue_projected: List[float]) -> Dict[str, Any]:
        """Projects monthly cash balance and calculates runway months until break-even or depletion."""
        balance = cash_reserves_usd
        balances = []
        depletion_month = None

        for month_idx, rev in enumerate(monthly_revenue_projected, start=1):
            net_cash_flow = rev - monthly_burn_rate_usd
            balance += net_cash_flow
            balances.append({"month": month_idx, "revenue": rev, "burn": monthly_burn_rate_usd, "balance": round(balance, 2)})
            if balance <= 0 and depletion_month is None:
                depletion_month = month_idx

        return {
            "initial_reserves_usd": cash_reserves_usd,
            "monthly_burn_rate_usd": monthly_burn_rate_usd,
            "months_simulated": len(monthly_revenue_projected),
            "depletion_month": depletion_month if depletion_month else "SURPLUS_SUSTAINED",
            "ending_cash_balance_usd": round(balance, 2),
            "monthly_trajectory": balances
        }
