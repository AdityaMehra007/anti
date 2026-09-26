"""
VECTIS TRADE — EU CBAM (Carbon Border Adjustment Mechanism) Calculation Engine
Implements European Commission Regulation (EU) 2023/956 for metals and engineering exporters.
"""

from dataclasses import dataclass
from typing import Dict, Any

# Official EU Default & Baseline Grid Emission Factors
INDIA_GRID_FACTOR_TCO2_PER_MWH = 0.716  # CEA India Baseline Carbon Intensity
EU_ETS_BENCHMARK_PRICE_EUR_PER_TCO2 = 85.0  # Approx EU ETS Carbon Allowance Price (EUR)

@dataclass
class ProductionData:
    goods_name: str
    cn_code: str  # Combined Nomenclature (HS) 8-digit code e.g. 7307 19 90
    quantity_metric_tonnes: float
    direct_fuel_emissions_tco2: float  # Scope 1 emissions from gas/furnace
    electricity_consumed_mwh: float    # Scope 2 electricity
    scrap_precursor_used_tonnes: float = 0.0

@dataclass
class CBAMDeclaration:
    goods_name: str
    cn_code: str
    production_volume_tonnes: float
    specific_direct_emissions: float   # tCO2e / tonne of product
    specific_indirect_emissions: float # tCO2e / tonne of product
    specific_total_emissions: float    # tCO2e / tonne of product
    total_embedded_emissions_tco2: float
    estimated_cbam_tariff_eur: float
    estimated_cbam_tariff_inr: float
    compliance_recommendation: str

class CBAMCalculator:
    """
    Computes embedded greenhouse gas emissions pursuant to Annex IV of Regulation (EU) 2023/956.
    """

    def calculate_emissions(self, prod: ProductionData, fx_eur_inr: float = 90.0) -> CBAMDeclaration:
        if prod.quantity_metric_tonnes <= 0:
            raise ValueError("Production volume must be greater than zero.")

        # 1. Direct Specific Emissions (Scope 1)
        dir_specific = prod.direct_fuel_emissions_tco2 / prod.quantity_metric_tonnes

        # 2. Indirect Specific Emissions (Scope 2 electricity via Indian grid factor)
        indir_total = prod.electricity_consumed_mwh * INDIA_GRID_FACTOR_TCO2_PER_MWH
        indir_specific = indir_total / prod.quantity_metric_tonnes

        # 3. Total Specific Embedded Emissions
        total_specific = dir_specific + indir_specific
        total_embedded = total_specific * prod.quantity_metric_tonnes

        # 4. Financial Carbon Tariff Liability (EUR & INR)
        # Note: In transitional phase (2024-2025 reporting only; definitive phase financial surrender applies)
        tariff_eur = total_embedded * EU_ETS_BENCHMARK_PRICE_EUR_PER_TCO2
        tariff_inr = tariff_eur * fx_eur_inr

        # 5. Strategic Optimization Recommendation
        if total_specific > 2.5:
            remedy = "HIGH EMISSIONS: Switch to dedicated rooftop solar captive power to lower Scope 2 intensity by up to 65%."
        elif total_specific > 1.2:
            remedy = "MODERATE EMISSIONS: Procure Open Access Green Energy and optimize scrap ratio to minimize EU border carbon tax."
        else:
            remedy = "OPTIMAL LOW-CARBON INTENSITY: Pre-cleared for Tier-1 EU Green Procurement preference."

        return CBAMDeclaration(
            goods_name=prod.goods_name,
            cn_code=prod.cn_code,
            production_volume_tonnes=prod.quantity_metric_tonnes,
            specific_direct_emissions=round(dir_specific, 4),
            specific_indirect_emissions=round(indir_specific, 4),
            specific_total_emissions=round(total_specific, 4),
            total_embedded_emissions_tco2=round(total_embedded, 2),
            estimated_cbam_tariff_eur=round(tariff_eur, 2),
            estimated_cbam_tariff_inr=round(tariff_inr, 2),
            compliance_recommendation=remedy
        )

if __name__ == "__main__":
    calc = CBAMCalculator()
    sample = ProductionData(
        goods_name="Precision Machined Steel Flanges",
        cn_code="7307 19 90",
        quantity_metric_tonnes=15.4,
        direct_fuel_emissions_tco2=12.2,
        electricity_consumed_mwh=18.5
    )
    res = calc.calculate_emissions(sample)
    print("VECTIS EU CBAM Carbon Calculation Result:")
    print(f"  - Product: {res.goods_name} (CN Code: {res.cn_code})")
    print(f"  - Volume: {res.production_volume_tonnes} MT")
    print(f"  - Direct Intensity: {res.specific_direct_emissions} tCO2/MT")
    print(f"  - Indirect Intensity: {res.specific_indirect_emissions} tCO2/MT")
    print(f"  - Total Specific Carbon: {res.specific_total_emissions} tCO2/MT")
    print(f"  - Total Carbon Embedded: {res.total_embedded_emissions_tco2} tCO2e")
    print(f"  - Estimated EU Carbon Liability: €{res.estimated_cbam_tariff_eur:,.2f} (₹{res.estimated_cbam_tariff_inr:,.2f})")
    print(f"  - Recommendation: {res.compliance_recommendation}")
