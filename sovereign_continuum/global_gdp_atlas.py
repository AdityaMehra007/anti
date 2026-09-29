"""
Global GDP & Planetary Balance Sheet Atlas (Comprehensive Macro Ledger).

Maps the totality of human economic activity:
1. Global GDP (Nominal $108.5T, PPP $185.0T) across Top 20 Nations & Economic Blocs (G7 vs BRICS+).
2. Global Value Added by Sector (Agriculture 4%, Industry 28%, Services 68%).
3. Global Debt Pyramid ($315.0T: Sovereign, Corporate, Household, Financial).
4. Global Asset Class Wealth Hierarchy ($450T+ Net Wealth, $380T Real Estate, $140T Bonds, $118T Equities).
5. Global Physical Commodity & Resource Throughput (Oil, Power, Grains, Semiconductors).
6. Monetary Aggregates & Daily Velocity (M2, Foreign Exchange $7.5T/day, Eurodollar rails).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class CountryEconomicProfile:
    rank: int
    name: str
    iso_code: str
    nominal_gdp_t: float
    ppp_gdp_t: float
    share_of_world_nominal_pct: float
    debt_to_gdp_pct: float
    primary_exports: List[str]


@dataclass
class SectorContribution:
    sector_name: str
    annual_gdp_t: float
    share_of_global_gdp_pct: float
    primary_drivers: List[str]


@dataclass
class AssetClassValuation:
    asset_class: str
    total_valuation_t: float
    share_of_global_wealth_pct: float
    liquidity_profile: str


@dataclass
class PhysicalCommodityThroughput:
    commodity_name: str
    annual_physical_volume: str
    annual_dollar_value_t: float
    strategic_chokehold: str


class GlobalGdpAtlas:
    """
    Exhaustive empirical database and analytical model of planetary wealth and money flows.
    """

    # World Bank / IMF / BIS Standardized Aggregates (2024-2026)
    TOTAL_GLOBAL_GDP_NOMINAL_T = 108.5
    TOTAL_GLOBAL_GDP_PPP_T = 185.0
    TOTAL_GLOBAL_DEBT_T = 315.0
    TOTAL_GLOBAL_PRIVATE_WEALTH_T = 475.0
    TOTAL_DERIVATIVES_NOTIONAL_T = 640.0
    DAILY_FX_TURNOVER_T = 7.5

    TOP_20_ECONOMIES = [
        CountryEconomicProfile(1, "United States", "USA", 28.8, 28.8, 26.54, 122.5, ["Tech/Software", "Financial Services", "Energy/LNG", "Aerospace"]),
        CountryEconomicProfile(2, "China", "CHN", 18.6, 35.3, 17.14, 83.0, ["Consumer Electronics", "EV/Batteries", "Solar/Renewables", "Industrial Machinery"]),
        CountryEconomicProfile(3, "Germany", "DEU", 4.6, 5.7, 4.24, 63.5, ["Automotive", "Precision Engineering", "Chemicals", "Industrial Automation"]),
        CountryEconomicProfile(4, "Japan", "JPN", 4.1, 6.7, 3.78, 260.0, ["Automotive", "Semiconductors/Robotics", "Electronics", "Precision Optics"]),
        CountryEconomicProfile(5, "India", "IND", 4.1, 14.6, 3.78, 81.0, ["IT/Software Services", "Pharmaceuticals", "Refined Petroleum", "Textiles"]),
        CountryEconomicProfile(6, "United Kingdom", "GBR", 3.5, 4.0, 3.23, 101.0, ["Financial/Legal Services", "Pharmaceuticals", "Aerospace", "Consulting"]),
        CountryEconomicProfile(7, "France", "FRA", 3.1, 3.9, 2.86, 110.0, ["Aerospace/Defense", "Luxury Goods", "Nuclear Energy", "Agriculture"]),
        CountryEconomicProfile(8, "Brazil", "BRA", 2.3, 4.3, 2.12, 74.0, ["Soybeans", "Iron Ore", "Crude Oil", "Biofuels/Sugar"]),
        CountryEconomicProfile(9, "Italy", "ITA", 2.3, 3.2, 2.12, 137.0, ["Specialized Machinery", "Luxury Apparel", "Automotive", "Food Products"]),
        CountryEconomicProfile(10, "Canada", "CAN", 2.2, 2.5, 2.03, 106.0, ["Crude Bitumen/Oil", "Lumber/Paper", "Automotive Parts", "Critical Minerals"]),
        CountryEconomicProfile(11, "Russia", "RUS", 2.0, 5.5, 1.84, 19.5, ["Crude Oil & Refined Products", "Natural Gas", "Wheat/Fertilizers", "Nickel/Palladium"]),
        CountryEconomicProfile(12, "Mexico", "MEX", 1.9, 3.3, 1.75, 50.0, ["Automotive Assembly", "Electronics", "Medical Equipment", "Oil"]),
        CountryEconomicProfile(13, "South Korea", "KOR", 1.8, 3.0, 1.66, 54.0, ["Memory Chips (DRAM/NAND)", "Automotive", "Displays", "Shipbuilding"]),
        CountryEconomicProfile(14, "Australia", "AUS", 1.7, 1.8, 1.57, 56.0, ["Iron Ore", "Coal", "LNG", "Gold/Lithium"]),
        CountryEconomicProfile(15, "Spain", "ESP", 1.6, 2.4, 1.47, 105.0, ["Tourism", "Automotive", "Renewable Energy", "Agri-food"]),
        CountryEconomicProfile(16, "Indonesia", "IDN", 1.5, 4.7, 1.38, 39.0, ["Nickel/Batteries", "Palm Oil", "Coal", "Textiles"]),
        CountryEconomicProfile(17, "Saudi Arabia", "SAU", 1.1, 2.3, 1.01, 26.0, ["Crude Petroleum", "Petrochemicals", "Plastics"]),
        CountryEconomicProfile(18, "Netherlands", "NLD", 1.1, 1.3, 1.01, 46.0, ["EUV Lithography (ASML)", "Refined Fuels", "Chemicals", "Agri-Tech"]),
        CountryEconomicProfile(19, "Turkey", "TUR", 1.1, 3.6, 1.01, 34.0, ["Automotive Parts", "Steel", "Textiles", "Defense Drones"]),
        CountryEconomicProfile(20, "Switzerland", "CHE", 0.9, 0.8, 0.83, 38.0, ["Pharmaceuticals", "Financial Wealth Management", "Precision Watches", "Gold Refining"]),
    ]

    GLOBAL_SECTORS = [
        SectorContribution("Services & Financialization", 73.78, 68.0, ["Banking & Capital Markets", "SaaS & Cloud Computing", "Healthcare", "Professional Services"]),
        SectorContribution("Industry & Manufacturing", 30.38, 28.0, ["Semiconductor Fabrication", "Automotive & Heavy Industry", "Chemicals & Plastics", "Energy Generation"]),
        SectorContribution("Agriculture & Extraction", 4.34, 4.0, ["Grain & Livestock", "Forestry & Fishing", "Mining & Rare Earth Metallurgy"]),
    ]

    GLOBAL_DEBT_STACK = {
        "Sovereign / Government Debt": 94.0,   # US ($34T), Japan ($10T), China ($14T), EU ($15T)
        "Non-Financial Corporate Debt": 91.0,
        "Financial Sector Debt": 67.0,
        "Household / Consumer Debt": 63.0,     # Mortgages, Auto loans, Student & Credit cards
    }

    ASSET_CLASSES = [
        AssetClassValuation("Global Real Estate (Residential, Commercial, Land)", 380.0, 48.0, "Illiquid physical titles, mortgaged collateral"),
        AssetClassValuation("Global Fixed Income & Debt Securities", 140.0, 17.7, "High liquidity sovereign & corporate bonds"),
        AssetClassValuation("Global Public Equities", 118.0, 14.9, "Very high liquidity public shares"),
        AssetClassValuation("Physical Gold & Precious Metals", 16.5, 2.1, "Sovereign reserve tier-1 collateral"),
        AssetClassValuation("Digital Assets & Cryptocurrencies", 2.8, 0.35, "24/7 high-beta programmatic liquidity"),
        AssetClassValuation("Private Equity & Venture Capital AUM", 13.5, 1.7, "Illiquid locked-up institutional LP stakes"),
    ]

    PHYSICAL_COMMODITIES = [
        PhysicalCommodityThroughput("Crude Oil & Liquids", "102.5 Million barrels/day (~37.4B bbls/yr)", 3.10, "Strait of Hormuz, Malacca, Suez"),
        PhysicalCommodityThroughput("Baseload Electricity", "29,500 Terawatt-hours/year", 3.85, "High-voltage transmission interconnects"),
        PhysicalCommodityThroughput("Cereal Grains (Corn, Wheat, Rice)", "2.85 Billion metric tons/year", 0.95, "Black Sea ports, Mississippi river, Panama Canal"),
        PhysicalCommodityThroughput("Semiconductors & Silicon", "1.15 Trillion chips/year", 0.65, "Taiwan Strait, ASML Veldhoven, TSMC Fab clusters"),
        PhysicalCommodityThroughput("Global Maritime Container Freight", "860 Million TEUs/year", 0.88, "Shanghai, Singapore, Rotterdam, LA/Long Beach"),
    ]

    def get_bloc_comparison(self) -> Dict[str, Dict[str, float]]:
        """
        Compares G7 vs BRICS+ (expanded 10 members).
        """
        # G7: USA, DEU, JPN, GBR, FRA, ITA, CAN
        g7_nominal = sum(c.nominal_gdp_t for c in self.TOP_20_ECONOMIES if c.iso_code in ["USA", "DEU", "JPN", "GBR", "FRA", "ITA", "CAN"])
        g7_ppp = sum(c.ppp_gdp_t for c in self.TOP_20_ECONOMIES if c.iso_code in ["USA", "DEU", "JPN", "GBR", "FRA", "ITA", "CAN"])

        # BRICS subset in Top 20: CHN, IND, BRA, RUS, SAU
        brics_top_nominal = sum(c.nominal_gdp_t for c in self.TOP_20_ECONOMIES if c.iso_code in ["CHN", "IND", "BRA", "RUS", "SAU"])
        brics_top_ppp = sum(c.ppp_gdp_t for c in self.TOP_20_ECONOMIES if c.iso_code in ["CHN", "IND", "BRA", "RUS", "SAU"])

        return {
            "G7_Bloc": {
                "nominal_gdp_t": round(g7_nominal, 2),
                "ppp_gdp_t": round(g7_ppp, 2),
                "share_world_nominal_pct": round((g7_nominal / self.TOTAL_GLOBAL_GDP_NOMINAL_T) * 100.0, 1),
            },
            "BRICS_Bloc_Core": {
                "nominal_gdp_t": round(brics_top_nominal, 2),
                "ppp_gdp_t": round(brics_top_ppp, 2),
                "share_world_nominal_pct": round((brics_top_nominal / self.TOTAL_GLOBAL_GDP_NOMINAL_T) * 100.0, 1),
            },
        }

    def format_macro_summary_table(self) -> str:
        lines = []
        lines.append("GLOBAL ECONOMIC LEDGER (NOMINAL vs PPP)")
        lines.append("=" * 80)
        lines.append(f"{'Rank':<4} | {'Country':<16} | {'Nominal ($T)':<13} | {'PPP ($T)':<10} | {'World Share':<11} | {'Debt/GDP'}")
        lines.append("-" * 80)
        for c in self.TOP_20_ECONOMIES:
            lines.append(f"{c.rank:<4} | {c.name:<16} | ${c.nominal_gdp_t:<12.1f} | ${c.ppp_gdp_t:<9.1f} | {c.share_of_world_nominal_pct:<10.1f}% | {c.debt_to_gdp_pct:.1f}%")
        lines.append("=" * 80)
        return "\n".join(lines)
