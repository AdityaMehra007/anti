"""
Global Business Empire Architecture & Capital Allocation Engine
Models, benchmarks, and projects the economics, moats, and capital compounding 
of the world's most elite business models.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class BusinessCategory(Enum):
    COGNITIVE_AI_PLATFORM = "Cognitive AI & Hyperscale Cloud"
    SOVEREIGN_FOUNDRY = "Critical Semiconductor & Deep Tech Foundry"
    PERMANENT_CAPITAL_ALLOCATOR = "Sovereign Merchant Bank & Float Compounder"
    GLOBAL_LOGISTICS_CONGLOMERATE = "Multi-Modal Freight & Resource Logistics"
    ECOSYSTEM_CONSUMER_MONOLITH = "Global Consumer Platform & Hardware Ecosystem"


@dataclass
class StrategicMoat:
    network_effects: float       # 0.0 to 10.0
    switching_costs: float       # 0.0 to 10.0
    cost_advantage: float        # 0.0 to 10.0
    intangible_ip_assets: float  # 0.0 to 10.0
    geopolitical_barrier: float  # 0.0 to 10.0

    @property
    def composite_score(self) -> float:
        """Normalized 0 to 100 strategic moat durability score."""
        raw = (
            self.network_effects * 0.25 +
            self.switching_costs * 0.25 +
            self.cost_advantage * 0.20 +
            self.intangible_ip_assets * 0.15 +
            self.geopolitical_barrier * 0.15
        )
        return round(raw * 10.0, 2)


@dataclass
class FinancialProfile:
    revenue_usd_bn: float
    gross_margin_pct: float
    ebitda_margin_pct: float
    net_margin_pct: float
    roic_pct: float                 # Return on Invested Capital
    fcf_conversion_pct: float       # FCF as % of Net Income
    capex_intensity_pct: float      # Capex as % of Revenue
    rd_intensity_pct: float         # R&D as % of Revenue
    debt_to_equity: float

    @property
    def free_cash_flow_usd_bn(self) -> float:
        net_income = self.revenue_usd_bn * (self.net_margin_pct / 100.0)
        return round(net_income * (self.fcf_conversion_pct / 100.0), 3)


@dataclass
class EnterpriseArchetype:
    name: str
    category: BusinessCategory
    benchmark_peers: List[str]
    description: str
    moat: StrategicMoat
    financials: FinancialProfile
    pricing_power_index: float      # 1.0 to 10.0
    reinvestment_runway_years: int

    def calculate_dcf_valuation(
        self,
        wacc: float = 0.09,
        terminal_growth: float = 0.035,
        projected_5yr_cagr: float = 0.15
    ) -> Dict[str, float]:
        """
        Calculates a Discounted Cash Flow (DCF) enterprise valuation based on
        free cash flow compounding and terminal multiple.
        """
        current_fcf = self.financials.free_cash_flow_usd_bn
        pv_fcf = 0.0
        fcf_series = []

        for yr in range(1, 6):
            compounded_fcf = current_fcf * ((1.0 + projected_5yr_cagr) ** yr)
            discount_factor = (1.0 + wacc) ** yr
            pv_fcf += compounded_fcf / discount_factor
            fcf_series.append(round(compounded_fcf, 3))

        # Terminal Value via Gordon Growth Model
        fcf_year_5 = fcf_series[-1]
        terminal_value = (fcf_year_5 * (1.0 + terminal_growth)) / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1.0 + wacc) ** 5)
        enterprise_value = pv_fcf + pv_terminal

        return {
            "current_fcf_bn": current_fcf,
            "projected_year_5_fcf_bn": round(fcf_year_5, 3),
            "pv_fcf_5yr_bn": round(pv_fcf, 2),
            "pv_terminal_value_bn": round(pv_terminal, 2),
            "enterprise_value_bn": round(enterprise_value, 2),
            "implied_fcf_multiple": round(enterprise_value / max(current_fcf, 0.01), 2)
        }

    def allocate_capital_5yr(
        self,
        growth_cagr: float = 0.15,
        reinvestment_ratio: float = 0.40,
        ma_ratio: float = 0.25,
        shareholder_yield_ratio: float = 0.35
    ) -> Dict[str, float]:
        """
        Executes a 5-year capital allocation model across organic reinvestment,
        strategic acquisitions (M&A), and capital returns.
        """
        total_fcf_generated = 0.0
        curr_fcf = self.financials.free_cash_flow_usd_bn
        for yr in range(1, 6):
            curr_fcf *= (1.0 + growth_cagr)
            total_fcf_generated += curr_fcf

        organic_capex_rd = total_fcf_generated * reinvestment_ratio
        ma_warchest = total_fcf_generated * ma_ratio
        shareholder_returns = total_fcf_generated * shareholder_yield_ratio

        return {
            "total_5yr_fcf_pool_bn": round(total_fcf_generated, 2),
            "organic_reinvestment_bn": round(organic_capex_rd, 2),
            "ma_warchest_bn": round(ma_warchest, 2),
            "shareholder_returns_bn": round(shareholder_returns, 2)
        }


class GlobalBusinessEmpireCatalog:
    """Standard authoritative benchmarks for the world's highest-performing business archetypes."""

    @staticmethod
    def get_tier_one_archetypes() -> List[EnterpriseArchetype]:
        return [
            EnterpriseArchetype(
                name="Hyperscale AI & Computing Cloud",
                category=BusinessCategory.COGNITIVE_AI_PLATFORM,
                benchmark_peers=["NVIDIA", "Microsoft Azure", "Alphabet Cloud", "AWS"],
                description="Massive compute infrastructure layer monopolizing foundational inference APIs, silicon architecture, and enterprise workflows.",
                moat=StrategicMoat(
                    network_effects=9.5,
                    switching_costs=9.8,
                    cost_advantage=9.0,
                    intangible_ip_assets=9.9,
                    geopolitical_barrier=8.8
                ),
                financials=FinancialProfile(
                    revenue_usd_bn=130.0,
                    gross_margin_pct=74.5,
                    ebitda_margin_pct=61.0,
                    net_margin_pct=52.0,
                    roic_pct=48.5,
                    fcf_conversion_pct=92.0,
                    capex_intensity_pct=14.0,
                    rd_intensity_pct=11.5,
                    debt_to_equity=0.18
                ),
                pricing_power_index=9.7,
                reinvestment_runway_years=15
            ),
            EnterpriseArchetype(
                name="Critical Advanced Semiconductor Foundry",
                category=BusinessCategory.SOVEREIGN_FOUNDRY,
                benchmark_peers=["TSMC", "ASML", "Synopsys"],
                description="Sub-2nm extreme ultraviolet lithography and packaging fabricator underpinning every advanced chip on Earth.",
                moat=StrategicMoat(
                    network_effects=7.5,
                    switching_costs=9.9,
                    cost_advantage=9.7,
                    intangible_ip_assets=9.9,
                    geopolitical_barrier=10.0
                ),
                financials=FinancialProfile(
                    revenue_usd_bn=85.0,
                    gross_margin_pct=54.2,
                    ebitda_margin_pct=68.0,
                    net_margin_pct=39.5,
                    roic_pct=29.0,
                    fcf_conversion_pct=82.0,
                    capex_intensity_pct=38.0,
                    rd_intensity_pct=8.5,
                    debt_to_equity=0.25
                ),
                pricing_power_index=9.5,
                reinvestment_runway_years=20
            ),
            EnterpriseArchetype(
                name="Sovereign Merchant Bank & Float Compounder",
                category=BusinessCategory.PERMANENT_CAPITAL_ALLOCATOR,
                benchmark_peers=["Berkshire Hathaway", "Blackstone", "Brookfield"],
                description="Institutional balance sheet compounding zero-cost insurance float and private credit into infrastructure and arterial monopolies.",
                moat=StrategicMoat(
                    network_effects=8.2,
                    switching_costs=8.0,
                    cost_advantage=9.8,
                    intangible_ip_assets=8.5,
                    geopolitical_barrier=8.5
                ),
                financials=FinancialProfile(
                    revenue_usd_bn=360.0,
                    gross_margin_pct=42.0,
                    ebitda_margin_pct=32.0,
                    net_margin_pct=26.0,
                    roic_pct=18.5,
                    fcf_conversion_pct=98.0,
                    capex_intensity_pct=4.5,
                    rd_intensity_pct=0.5,
                    debt_to_equity=0.35
                ),
                pricing_power_index=8.8,
                reinvestment_runway_years=30
            ),
            EnterpriseArchetype(
                name="Global Multi-Modal Freight & Energy Chokehold",
                category=BusinessCategory.GLOBAL_LOGISTICS_CONGLOMERATE,
                benchmark_peers=["Maersk", "Vitol", "Trafigura", "DP World"],
                description="Physical trade arteries controlling container terminals, VLCC supertankers, pipeline junctions, and critical maritime straits.",
                moat=StrategicMoat(
                    network_effects=8.8,
                    switching_costs=7.8,
                    cost_advantage=9.2,
                    intangible_ip_assets=7.5,
                    geopolitical_barrier=9.5
                ),
                financials=FinancialProfile(
                    revenue_usd_bn=140.0,
                    gross_margin_pct=28.5,
                    ebitda_margin_pct=22.0,
                    net_margin_pct=14.5,
                    roic_pct=21.0,
                    fcf_conversion_pct=88.0,
                    capex_intensity_pct=12.0,
                    rd_intensity_pct=1.0,
                    debt_to_equity=0.45
                ),
                pricing_power_index=8.2,
                reinvestment_runway_years=12
            ),
            EnterpriseArchetype(
                name="Global Ecosystem Consumer Monolith",
                category=BusinessCategory.ECOSYSTEM_CONSUMER_MONOLITH,
                benchmark_peers=["Apple", "Amazon Prime", "LVMH"],
                description="High-affinity consumer touchpoints with vertical silicon, proprietary OS, captive digital payments, and sticky luxury margins.",
                moat=StrategicMoat(
                    network_effects=9.4,
                    switching_costs=9.5,
                    cost_advantage=8.8,
                    intangible_ip_assets=9.8,
                    geopolitical_barrier=7.5
                ),
                financials=FinancialProfile(
                    revenue_usd_bn=390.0,
                    gross_margin_pct=46.2,
                    ebitda_margin_pct=34.0,
                    net_margin_pct=25.5,
                    roic_pct=56.0,
                    fcf_conversion_pct=104.0,
                    capex_intensity_pct=3.0,
                    rd_intensity_pct=7.8,
                    debt_to_equity=0.85
                ),
                pricing_power_index=9.6,
                reinvestment_runway_years=15
            )
        ]
