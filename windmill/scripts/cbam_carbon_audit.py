"""
Windmill Production Script: EU CBAM Carbon Tariff & Discrepancy Engine
=======================================================================
Category: Regulatory & Trade Compliance
Language: Python 3.12 / 3.13 (Windmill Native / Docker Sandbox)

Calculates EU Regulation 2023/956 carbon penalties for industrial steel/aluminum exports.
Validates direct & indirect embedded emissions, EU ETS default benchmarks,
and formats official XML CBAM declarations.
"""

from typing import Dict, Any, List
import json
import math

# CBAM Benchmark Carbon Prices (EUR per metric ton CO2e)
EU_ETS_CURRENT_PRICE_EUR = 72.50
EXEMPTION_THRESHOLD_EUR = 150.0

DEFAULT_EMISSION_BENCHMARKS = {
    "7307": {"name": "Tube or pipe fittings (iron/steel)", "direct_co2_factor": 2.14, "indirect_co2_factor": 0.42},
    "7326": {"name": "Other articles of iron or steel", "direct_co2_factor": 1.98, "indirect_co2_factor": 0.38},
    "7601": {"name": "Unwrought aluminum", "direct_co2_factor": 6.85, "indirect_co2_factor": 1.95},
    "7208": {"name": "Flat-rolled products of iron/steel", "direct_co2_factor": 2.25, "indirect_co2_factor": 0.45}
}


def main(
    docket_id: str = "DKT-CBAM-2026-091",
    exporter_name: str = "Bharat Steel Tubing Corp",
    cn_code: str = "7307",
    net_mass_kg: float = 24500.0,
    origin_country: str = "IN",
    carbon_price_paid_origin_eur: float = 0.0,
    destination_eu_country: str = "DE"
) -> Dict[str, Any]:
    """
    Execute CBAM carbon liability audit and compute export clearance tax.
    """
    net_mass_tonnes = net_mass_kg / 1000.0
    benchmark = DEFAULT_EMISSION_BENCHMARKS.get(cn_code, {
        "name": f"CN {cn_code} Industrial Product",
        "direct_co2_factor": 2.0,
        "indirect_co2_factor": 0.4
    })
    
    direct_emissions_t_co2 = round(net_mass_tonnes * benchmark["direct_co2_factor"], 3)
    indirect_emissions_t_co2 = round(net_mass_tonnes * benchmark["indirect_co2_factor"], 3)
    total_embedded_co2_tonnes = round(direct_emissions_t_co2 + indirect_emissions_t_co2, 3)
    
    gross_cbam_liability_eur = round(total_embedded_co2_tonnes * EU_ETS_CURRENT_PRICE_EUR, 2)
    effective_carbon_credit_eur = round(carbon_price_paid_origin_eur * net_mass_tonnes, 2)
    net_cbam_tariff_payable_eur = max(0.0, round(gross_cbam_liability_eur - effective_carbon_credit_eur, 2))
    
    # Check compliance status
    status = "CLEARED" if net_cbam_tariff_payable_eur < EXEMPTION_THRESHOLD_EUR else "PAYMENT_REQUIRED"
    
    xml_declaration = f"""<?xml version="1.0" encoding="UTF-8"?>
<CBAMDeclaration xmlns="urn:eu:cbam:v1" version="2026.1">
    <DocketID>{docket_id}</DocketID>
    <Declarant>{exporter_name}</Declarant>
    <OriginCountry>{origin_country}</OriginCountry>
    <DestinationEUCountry>{destination_eu_country}</DestinationEUCountry>
    <CommodityCNCode>{cn_code}</CommodityCNCode>
    <NetMassKg>{net_mass_kg}</NetMassKg>
    <TotalEmbeddedEmissionsTonnesCO2e>{total_embedded_co2_tonnes}</TotalEmbeddedEmissionsTonnesCO2e>
    <NetPayableEUR>{net_cbam_tariff_payable_eur}</NetPayableEUR>
    <Status>{status}</Status>
</CBAMDeclaration>"""

    return {
        "docket_id": docket_id,
        "exporter": exporter_name,
        "cn_code": cn_code,
        "commodity": benchmark["name"],
        "net_mass_tonnes": net_mass_tonnes,
        "direct_emissions_tco2e": direct_emissions_t_co2,
        "indirect_emissions_tco2e": indirect_emissions_t_co2,
        "total_embedded_emissions_tco2e": total_embedded_co2_tonnes,
        "eu_ets_benchmark_price_eur": EU_ETS_CURRENT_PRICE_EUR,
        "gross_liability_eur": gross_cbam_liability_eur,
        "carbon_credit_offset_eur": effective_carbon_credit_eur,
        "net_payable_eur": net_cbam_tariff_payable_eur,
        "compliance_status": status,
        "xml_declaration_snippet": xml_declaration.replace("\n", " ").strip()[:200] + "..."
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
