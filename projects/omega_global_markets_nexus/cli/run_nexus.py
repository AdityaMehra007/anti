"""
Interactive CLI Runner for OMEGA Global Markets & EXIM Nexus
Enables command-line simulation, risk stress-testing, and analytical generation.
"""
import argparse
import json
import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Ensure UTF-8 stdout encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from projects.omega_global_markets_nexus.core.business_empire import GlobalBusinessEmpireCatalog
from projects.omega_global_markets_nexus.core.nexus_orchestrator import OmegaNexusOrchestrator
from projects.omega_global_markets_nexus.core.bond_market_engine import NelsonSiegelCurve
from projects.omega_global_markets_nexus.core.money_market_engine import TreasuryCashSweepDesk, Basel3LiquidityAuditor
from projects.omega_global_markets_nexus.core.global_exim_engine import GlobalEximEngine, TradeContract, Incoterm
from projects.omega_global_markets_nexus.daemon.autonomous_nexus_daemon import AutonomousNexusDaemon
from projects.omega_global_markets_nexus.reports.report_generator import generate_executive_dossier


def format_currency(val: float, prefix="$") -> str:
    return f"{prefix}{val:,.2f}"


def run_cli():
    parser = argparse.ArgumentParser(description="OMEGA Global Markets, Business Empire & EXIM Nexus CLI")
    parser.add_argument("--mode", choices=["full-cycle", "businesses", "curve", "cash-sweep", "daemon", "report"], default="full-cycle", help="Execution mode")
    parser.add_argument("--archetype", type=int, default=0, help="Index of business archetype (0 to 4)")
    parser.add_argument("--cash-pool", type=float, default=50_000_000.0, help="Treasury cash pool in USD")
    parser.add_argument("--trade-units", type=int, default=500, help="Cargo units for EXIM trade")
    parser.add_argument("--unit-price", type=float, default=40_000.0, help="Cargo unit price in USD")
    parser.add_argument("--iterations", type=int, default=3, help="Iterations for daemon loop")
    parser.add_argument("--json", action="store_true", help="Output pure JSON")

    args = parser.parse_args()

    if args.mode == "full-cycle":
        orch = OmegaNexusOrchestrator()
        report = orch.run_full_macro_cycle(
            archetype_index=args.archetype,
            trade_units=args.trade_units,
            unit_price_usd=args.unit_price,
            treasury_cash_pool_usd=args.cash_pool,
            equity_portfolio_capital_usd=args.cash_pool * 0.5
        )

        if args.json:
            print(json.dumps(report.__dict__, indent=2))
            return

        print("=" * 80)
        print("🏛️  OMEGA GLOBAL MARKETS, BUSINESS EMPIRE & EXIM NEXUS REPORT")
        print("=" * 80)
        print(f"🏢 Selected Business Archetype:   {report.business_archetype}")
        print(f"💰 Projected Annual FCF:          ${report.annual_fcf_generated_bn:.2f} Billion")
        print(f"💎 Implied Enterprise Value:      ${report.enterprise_value_bn:,.2f} Billion")
        print("-" * 80)
        print("🌐 CROSS-BORDER EXIM & TRADE FINANCE:")
        print(f"   Trade Transaction Volume:      {format_currency(report.exim_trade_volume_usd)}")
        print(f"   Letter of Credit Status:       {report.exim_settlement_status}")
        print("-" * 80)
        print("💵 MONEY MARKET & TREASURY CASH DESK:")
        print(f"   Blended Yield on Swept Cash:   {report.money_market_blended_yield_pct:.3f}% APY")
        print(f"   Basel III Liquidity (LCR):     {report.basel3_lcr_pct:.1f}% (Regulatory Min: 100%)")
        print("-" * 80)
        print("📈 FIXED INCOME & BOND MARKETS:")
        print(f"   10-Year Benchmark Yield:       {report.bond_10y_yield_pct:.3f}%")
        print(f"   Yield Curve Inversion Signal:  {report.curve_inversion_status}")
        print(f"   Corporate Credit Spread:       +{report.corporate_debt_spread_bps:.1f} bps")
        print("-" * 80)
        print("📊 STOCK MARKET QUANTITATIVE ALPHA:")
        print(f"   Expected Annual Return:        {report.stock_portfolio_expected_return_pct:.2f}%")
        print(f"   Portfolio Sharpe Ratio:        {report.stock_portfolio_sharpe:.3f}")
        print(f"   Daily Value-at-Risk (95% VaR): {format_currency(report.stock_portfolio_daily_var_95_usd)}")
        print("=" * 80)
        print(f"👑 EXECUTIVE VERDICT:             {report.nexus_macro_verdict}")
        print("=" * 80)

    elif args.mode == "businesses":
        catalog = GlobalBusinessEmpireCatalog.get_tier_one_archetypes()
        print("=" * 80)
        print("🏆 TOP GLOBAL BUSINESS ARCHETYPES & COMPOSITE MOAT SCORES")
        print("=" * 80)
        for idx, arch in enumerate(catalog):
            print(f"[{idx}] {arch.name} ({arch.category.value})")
            print(f"    Peers: {', '.join(arch.benchmark_peers)}")
            print(f"    Composite Moat: {arch.moat.composite_score}/100 | Pricing Power: {arch.pricing_power_index}/10")
            print(f"    Revenue: ${arch.financials.revenue_usd_bn}B | Net Margin: {arch.financials.net_margin_pct}% | ROIC: {arch.financials.roic_pct}%")
            print(f"    Annual FCF: ${arch.financials.free_cash_flow_usd_bn}B")
            print("-" * 80)

    elif args.mode == "curve":
        curve = NelsonSiegelCurve()
        ladder = curve.generate_tenor_ladder()
        inversion = curve.check_curve_inversion()
        print("=" * 80)
        print("📈 SOVEREIGN BENCHMARK YIELD CURVE (NELSON-SIEGEL MODEL)")
        print("=" * 80)
        for tenor, rate in ladder.items():
            bar = "█" * int(rate * 10)
            print(f"   {tenor:>4}: {rate:5.3f}% | {bar}")
        print("-" * 80)
        print(f"   2Y: {inversion['2y_rate_pct']:.3f}% | 10Y: {inversion['10y_rate_pct']:.3f}% | 10Y-2Y Spread: {inversion['spread_10y_2y_bps']:+.1f} bps")
        print(f"   Curve State: {inversion['signal']}")
        print("=" * 80)

    elif args.mode == "cash-sweep":
        res = TreasuryCashSweepDesk.execute_sweep(args.cash_pool)
        print("=" * 80)
        print(f"💵 TREASURY CASH SWEEP OPTIMIZATION (${args.cash_pool:,.2f})")
        print("=" * 80)
        print(f"   Operational Checking Buffer:   {format_currency(res['overnight_operational_cash'])}")
        print(f"   Swept into Overnight SOFR:     {format_currency(res['swept_to_sofr_repo'])}")
        print(f"   Swept into 30-Day T-Bills:     {format_currency(res['swept_to_30d_tbills'])}")
        print(f"   Swept into 90-Day Prime CP:    {format_currency(res['swept_to_90d_cp'])}")
        print(f"   Weighted Blended Yield:        {res['weighted_blended_yield_pct']:.3f}% APY")
        print(f"   Estimated Annual Interest:     {format_currency(res['annualized_interest_income_usd'])}")
        print("=" * 80)

    elif args.mode == "daemon":
        daemon = AutonomousNexusDaemon()
        print("=" * 80)
        print(f"🤖 EXECUTING AUTONOMOUS NEXUS DAEMON ({args.iterations} iterations)")
        print("=" * 80)
        cycles = daemon.run_daemon_loop(iterations=args.iterations, interval_seconds=0.5)
        for c in cycles:
            print(f"   [{c['cycle_id']}] Archetype: {c['business_archetype'][:30]:<30} | Verdict: {c['nexus_macro_verdict']}")
        metrics = daemon.ledger.get_ledger_metrics()
        print("-" * 80)
        print(f"   Total Cycles in Audit Ledger: {metrics['total_macro_cycles_recorded']}")
        print("=" * 80)

    elif args.mode == "report":
        res = generate_executive_dossier()
        print("=" * 80)
        print("📑 GENERATED INSTITUTIONAL EXECUTIVE DOSSIER")
        print("=" * 80)
        print(f"   Cycle ID:    {res['cycle_id']}")
        print(f"   Report File: {res['markdown_report_path']}")
        print(f"   Status:      {res['status']}")
        print("=" * 80)


if __name__ == "__main__":
    run_cli()
