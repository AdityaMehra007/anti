"""
Multi-Asset Monte Carlo & Macroeconomic Crisis Stress Engine
Simulates institutional balance sheet resilience across historical crisis regimes:
1970s Great Stagflation, 2008 Global Financial Crisis, 2020 Supply Chain Fracture, and Geopolitical Sanctions.
"""
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Tuple


class StressScenario(Enum):
    GREAT_STAGFLATION_1970S = "1970s Great Stagflation (Rates +400bps, Oil +120%, Equities -28%)"
    GFC_2008_LIQUIDITY_CRUNCH = "2008 Global Financial Crisis (Spreads +450bps, Equities -45%, Cash Run)"
    SUPPLY_CHAIN_FRACTURE_2020 = "2020 Supply Chain Fracture (Freight Rates 4x, Port Delays +18d)"
    SOVEREIGN_SANCTIONS_CHOKEPOINT = "Geopolitical Sanctions & Strait Blockade (Suez Reroute, FX -15%)"


@dataclass
class EnterpriseBalanceSheet:
    equities_portfolio_usd: float = 25_000_000.0
    bond_portfolio_usd: float = 16_000_000.0
    bond_modified_duration_years: float = 7.6
    money_market_cash_usd: float = 18_000_000.0
    exim_trade_receivables_usd: float = 13_000_000.0

    @property
    def total_balance_sheet_usd(self) -> float:
        return (
            self.equities_portfolio_usd +
            self.bond_portfolio_usd +
            self.money_market_cash_usd +
            self.exim_trade_receivables_usd
        )


@dataclass
class StressTestResult:
    scenario_name: str
    initial_total_usd: float
    stressed_total_usd: float
    dollar_loss_usd: float
    percentage_drawdown_pct: float
    equities_loss_usd: float
    bonds_loss_usd: float
    trade_working_cap_loss_usd: float
    liquidity_survival_status: str
    stress_var_99_usd: float
    expected_shortfall_99_usd: float


class MonteCarloStressEngine:
    """Institutional stress-testing engine combining deterministic historical shocks with stochastic Monte Carlo paths."""

    @staticmethod
    def run_deterministic_shock(
        sheet: EnterpriseBalanceSheet,
        scenario: StressScenario = StressScenario.GFC_2008_LIQUIDITY_CRUNCH
    ) -> StressTestResult:
        initial_val = sheet.total_balance_sheet_usd

        if scenario == StressScenario.GREAT_STAGFLATION_1970S:
            # Equities -28%, 10Y Yields +400 bps (bonds lose duration * delta_y = 7.6 * 4% = ~30.4%)
            eq_loss = sheet.equities_portfolio_usd * 0.28
            bond_loss = sheet.bond_portfolio_usd * (sheet.bond_modified_duration_years * 0.04)
            trade_loss = sheet.exim_trade_receivables_usd * 0.08  # Cost-of-carry inflation
        elif scenario == StressScenario.GFC_2008_LIQUIDITY_CRUNCH:
            # Equities -45%, Credit spreads +450 bps, Trade counterparty defaults -15%
            eq_loss = sheet.equities_portfolio_usd * 0.45
            bond_loss = sheet.bond_portfolio_usd * (sheet.bond_modified_duration_years * 0.045)
            trade_loss = sheet.exim_trade_receivables_usd * 0.15
        elif scenario == StressScenario.SUPPLY_CHAIN_FRACTURE_2020:
            # Equities -15%, Bonds +5% (flight to safety), Trade D&D demurrage / delays -25%
            eq_loss = sheet.equities_portfolio_usd * 0.15
            bond_loss = -sheet.bond_portfolio_usd * 0.05  # Bond gain
            trade_loss = sheet.exim_trade_receivables_usd * 0.25
        else: # SOVEREIGN_SANCTIONS_CHOKEPOINT
            # Equities -12%, Bonds flat, Trade rerouting / FX loss -18%
            eq_loss = sheet.equities_portfolio_usd * 0.12
            bond_loss = sheet.bond_portfolio_usd * 0.02
            trade_loss = sheet.exim_trade_receivables_usd * 0.18

        total_loss = eq_loss + bond_loss + trade_loss
        stressed_val = initial_val - total_loss
        pct_loss = (total_loss / initial_val) * 100.0

        # Cash buffer adequacy: Does cash cover immediate stressed losses?
        survived = (sheet.money_market_cash_usd > (total_loss * 0.35))
        status = "SOLVENT_PRUDENT" if survived else "VULNERABLE_LIQUIDITY_STRAIN"

        # Analytical Stress-VaR (99% confidence multiplier ~ 1.25 of scenario shock)
        s_var_99 = total_loss * 1.15
        cvar_99 = total_loss * 1.28

        return StressTestResult(
            scenario_name=scenario.value,
            initial_total_usd=round(initial_val, 2),
            stressed_total_usd=round(stressed_val, 2),
            dollar_loss_usd=round(total_loss, 2),
            percentage_drawdown_pct=round(pct_loss, 2),
            equities_loss_usd=round(eq_loss, 2),
            bonds_loss_usd=round(bond_loss, 2),
            trade_working_cap_loss_usd=round(trade_loss, 2),
            liquidity_survival_status=status,
            stress_var_99_usd=round(s_var_99, 2),
            expected_shortfall_99_usd=round(cvar_99, 2)
        )

    @staticmethod
    def run_stochastic_monte_carlo(
        sheet: EnterpriseBalanceSheet,
        num_simulations: int = 2000,
        horizon_days: int = 30,
        seed: int = 101
    ) -> Dict[str, Any]:
        """
        Runs Monte Carlo paths using geometric Brownian motion across equity, bond, and trade assets.
        Calculates empirical distribution quantiles (p1, p5, median, p95).
        """
        random.seed(seed)
        initial_val = sheet.total_balance_sheet_usd
        dt = horizon_days / 365.0
        sqrt_dt = math.sqrt(dt)

        # Asset parameters (annual drift, annual vol)
        eq_mu, eq_vol = 0.10, 0.22
        bond_mu, bond_vol = 0.045, 0.08
        cash_mu, cash_vol = 0.052, 0.005
        trade_mu, trade_vol = 0.08, 0.12

        terminal_values: List[float] = []

        for _ in range(num_simulations):
            z1 = random.gauss(0, 1)
            z2 = 0.5 * z1 + math.sqrt(1 - 0.25) * random.gauss(0, 1)  # 0.5 correlation
            z3 = random.gauss(0, 1)
            z4 = random.gauss(0, 1)

            eq_term = sheet.equities_portfolio_usd * math.exp((eq_mu - 0.5 * eq_vol**2) * dt + eq_vol * sqrt_dt * z1)
            bond_term = sheet.bond_portfolio_usd * math.exp((bond_mu - 0.5 * bond_vol**2) * dt + bond_vol * sqrt_dt * z2)
            cash_term = sheet.money_market_cash_usd * math.exp((cash_mu - 0.5 * cash_vol**2) * dt + cash_vol * sqrt_dt * z3)
            trade_term = sheet.exim_trade_receivables_usd * math.exp((trade_mu - 0.5 * trade_vol**2) * dt + trade_vol * sqrt_dt * z4)

            sim_total = eq_term + bond_term + cash_term + trade_term
            terminal_values.append(sim_total)

        terminal_values.sort()

        p1_idx = int(0.01 * num_simulations)
        p5_idx = int(0.05 * num_simulations)
        p50_idx = int(0.50 * num_simulations)
        p95_idx = int(0.95 * num_simulations)

        p1_val = terminal_values[p1_idx]
        p5_val = terminal_values[p5_idx]
        median_val = terminal_values[p50_idx]
        p95_val = terminal_values[p95_idx]

        # 1-month 99% Monte Carlo VaR
        mc_var_99_usd = initial_val - p1_val
        mc_var_95_usd = initial_val - p5_val

        # Expected Shortfall 99% (average of worst 1% runs)
        tail_99 = terminal_values[:max(1, p1_idx)]
        cvar_99_val = sum(tail_99) / len(tail_99)
        mc_cvar_99_usd = initial_val - cvar_99_val

        return {
            "initial_balance_sheet_usd": round(initial_val, 2),
            "num_simulations": num_simulations,
            "horizon_days": horizon_days,
            "median_terminal_value_usd": round(median_val, 2),
            "percentile_1st_worst_usd": round(p1_val, 2),
            "percentile_5th_worst_usd": round(p5_val, 2),
            "percentile_95th_best_usd": round(p95_val, 2),
            "mc_var_95_usd": round(max(0.0, mc_var_95_usd), 2),
            "mc_var_99_usd": round(max(0.0, mc_var_99_usd), 2),
            "mc_cvar_99_usd": round(max(0.0, mc_cvar_99_usd), 2)
        }
