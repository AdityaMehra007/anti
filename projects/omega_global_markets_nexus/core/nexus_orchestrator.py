"""
OMEGA Global Markets & EXIM Nexus Orchestrator
Master macro engine integrating:
1. Elite Global Business Operations & Capital Allocation
2. International Cross-Border EXIM Trade & UCP 600 Settlements
3. Money Market Short-Term Liquidity Sweeps & Basel III LCR
4. Bond Market Fixed Income Debt Issuances & Nelson-Siegel Yield Curves
5. Stock Market Quantitative Alpha Compounding & Risk Controls
"""
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .business_empire import GlobalBusinessEmpireCatalog, EnterpriseArchetype
from .stock_market_engine import (
    LimitOrderBook, Order, OrderSide, OrderType,
    EquityFactorProfile, PortfolioRiskOptimizer, AlgorithmicExecutionSlicer
)
from .money_market_engine import (
    TBillInstrument, CommercialPaper, RepoContract, CollateralTier,
    TreasuryCashSweepDesk, Basel3LiquidityAuditor
)
from .bond_market_engine import (
    NelsonSiegelCurve, FixedCouponBond, CorporateCreditSpreadAnalyzer
)
from .global_exim_engine import (
    GlobalEximEngine, TradeContract, Incoterm, LetterOfCreditSpec, ShippingDocuments
)


@dataclass
class NexusCycleReport:
    business_archetype: str
    annual_fcf_generated_bn: float
    enterprise_value_bn: float
    exim_trade_volume_usd: float
    exim_settlement_status: str
    money_market_blended_yield_pct: float
    basel3_lcr_pct: float
    bond_10y_yield_pct: float
    curve_inversion_status: str
    corporate_debt_spread_bps: float
    stock_portfolio_expected_return_pct: float
    stock_portfolio_sharpe: float
    stock_portfolio_daily_var_95_usd: float
    nexus_macro_verdict: str


class OmegaNexusOrchestrator:
    """Master institutional controller harmonizing trade, treasury, fixed income, and equities."""

    def __init__(self, local_currency_fx: float = 85.0):
        self.exim_engine = GlobalEximEngine(fx_rate_to_local=local_currency_fx)
        self.yield_curve = NelsonSiegelCurve()
        self.order_book = LimitOrderBook(symbol="OMEGA-GLOBAL")

    def run_full_macro_cycle(
        self,
        archetype_index: int = 0,
        trade_units: int = 500,
        unit_price_usd: float = 40_000.0,
        treasury_cash_pool_usd: float = 50_000_000.0,
        equity_portfolio_capital_usd: float = 25_000_000.0
    ) -> NexusCycleReport:
        # 1. Global Business Empire Assessment
        catalog = GlobalBusinessEmpireCatalog.get_tier_one_archetypes()
        business = catalog[archetype_index]
        dcf = business.calculate_dcf_valuation()

        # 2. Global EXIM Trade Execution & LC Audit
        contract = TradeContract(
            contract_id="EXIM-NEXUS-2026-X1",
            exporter_name="Apex Global Technologies Corp",
            exporter_country="United States",
            importer_name="Indo-Pacific Advanced Foundries Ltd",
            importer_country="India",
            hs_code="8471.50.00",
            incoterm=Incoterm.CIF,
            cargo_quantity_units=trade_units,
            unit_price_usd=unit_price_usd,
            freight_usd=120_000.0,
            marine_insurance_usd=30_000.0
        )
        customs = self.exim_engine.compute_customs_landed_cost(contract)

        lc = LetterOfCreditSpec(
            lc_reference="LC-GLOBAL-998811",
            issuing_bank="Standard Chartered Bank Singapore",
            applicant="Indo-Pacific Advanced Foundries Ltd",
            beneficiary="Apex Global Technologies Corp",
            credit_amount_usd=contract.cif_value_usd,
            tolerance_pct=5.0,
            expiry_date="2026-12-31",
            latest_shipment_date="2026-11-15",
            port_of_loading="Port of Los Angeles",
            port_of_discharge="Nhava Sheva JNPT"
        )

        docs = ShippingDocuments(
            doc_reference="DOCS-INV-881",
            invoice_number="INV-2026-881",
            invoice_amount_usd=contract.cif_value_usd,
            invoice_beneficiary="Apex Global Technologies Corp",
            invoice_applicant="Indo-Pacific Advanced Foundries Ltd",
            bill_of_lading_no="BOL-MAERSK-9002",
            shipped_on_board_date="2026-10-18",
            bol_port_of_loading="Port of Los Angeles",
            bol_port_of_discharge="Nhava Sheva JNPT",
            is_clean_on_board=True
        )

        lc_audit = self.exim_engine.audit_ucp600_presentation(lc, docs, presentation_date="2026-10-21")
        sanctions = self.exim_engine.screen_sanctions_and_embargo(
            contract.exporter_name, contract.exporter_country,
            contract.importer_name, contract.importer_country,
            "High-Performance Computing Units & AI Servers"
        )

        # 3. Money Market Sweep & Basel III Audit
        sweep = TreasuryCashSweepDesk.execute_sweep(
            total_cash_usd=treasury_cash_pool_usd,
            overnight_buffer_target_usd=5_000_000.0,
            sofr_overnight_rate_pct=5.30,
            tbill_30d_rate_pct=5.20,
            cp_90d_rate_pct=5.45
        )

        lcr = Basel3LiquidityAuditor.audit_lcr(
            level_1_assets_usd=treasury_cash_pool_usd * 0.60,
            level_2a_assets_usd=treasury_cash_pool_usd * 0.25,
            level_2b_assets_usd=treasury_cash_pool_usd * 0.15,
            operational_deposits_outflow_usd=15_000_000.0,
            non_operational_deposits_outflow_usd=20_000_000.0,
            contractual_cash_inflows_30d_usd=5_000_000.0
        )

        # 4. Bond Market Yield Curve & Credit Issuance
        curve_status = self.yield_curve.check_curve_inversion()
        r_10y = curve_status["10y_rate_pct"]
        bond_issuance = FixedCouponBond(
            cusip="BND-APEX-2036",
            issuer="Apex Sovereign Corp",
            par_value=1_000.0,
            coupon_rate_pct=5.50,
            maturity_years=10.0,
            frequency=2
        )
        corporate_spread = CorporateCreditSpreadAnalyzer.analyze_spread(
            corporate_ytm_pct=5.75,
            benchmark_sovereign_ytm_pct=r_10y
        )

        # 5. Stock Market Multi-Factor Compounding & Risk
        weights = [0.35, 0.25, 0.20, 0.20]
        expected_returns = [0.18, 0.14, 0.11, 0.09]
        volatilities = [0.24, 0.19, 0.16, 0.14]
        corr = [
            [1.0, 0.55, 0.35, 0.20],
            [0.55, 1.0, 0.40, 0.25],
            [0.35, 0.40, 1.0, 0.30],
            [0.20, 0.25, 0.30, 1.0]
        ]
        portfolio_risk = PortfolioRiskOptimizer.evaluate_portfolio(
            weights=weights,
            expected_returns=expected_returns,
            volatilities=volatilities,
            correlation_matrix=corr,
            risk_free_rate=0.045,
            portfolio_value_usd=equity_portfolio_capital_usd
        )

        verdict = "SUPREME_GLOBAL_DOMINANCE" if (
            lc_audit["is_compliant"] and
            sanctions["cleared_for_export"] and
            lcr["compliance_status"] == "COMPLIANT_PRUDENT" and
            not curve_status["is_inverted"]
        ) else "OPERATIONALLY_SOUND_WITH_MONITORED_RISKS"

        return NexusCycleReport(
            business_archetype=business.name,
            annual_fcf_generated_bn=business.financials.free_cash_flow_usd_bn,
            enterprise_value_bn=dcf["enterprise_value_bn"],
            exim_trade_volume_usd=contract.cif_value_usd,
            exim_settlement_status=lc_audit["status"],
            money_market_blended_yield_pct=sweep["weighted_blended_yield_pct"],
            basel3_lcr_pct=lcr["lcr_ratio_pct"],
            bond_10y_yield_pct=r_10y,
            curve_inversion_status=curve_status["signal"],
            corporate_debt_spread_bps=corporate_spread["credit_spread_bps"],
            stock_portfolio_expected_return_pct=portfolio_risk["expected_annual_return_pct"],
            stock_portfolio_sharpe=portfolio_risk["sharpe_ratio"],
            stock_portfolio_daily_var_95_usd=portfolio_risk["daily_var_95_usd"],
            nexus_macro_verdict=verdict
        )
