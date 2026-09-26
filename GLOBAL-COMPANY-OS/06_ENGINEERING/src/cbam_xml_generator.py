"""
EU CBAM XML Declaration Generator (ANTIGRAVITY Ω∞ / TradeNexus)
Compiles verified production emissions data into EU-compliant CBAM Registry XML declarations
under Regulation (EU) 2023/956 for steel, aluminum, and chemical exporters.
"""

from dataclasses import dataclass
from typing import List, Optional
import xml.etree.ElementTree as ET
import hashlib
from datetime import datetime, timezone

@dataclass
class InstallationData:
    installation_name: str
    country_code: str          # e.g., "IN"
    un_locode: str              # e.g., "INBLR"
    latitude: float
    longitude: float

@dataclass
class CBAMEmissionsItem:
    item_id: str
    cn_code: str                # Combined Nomenclature (8-digit)
    goods_description: str
    net_mass_tonnes: float
    production_route: str       # e.g., "Electric Arc Furnace", "Blast Furnace - Basic Oxygen"
    direct_embedded_emissions: float   # t CO2e per tonne of good
    indirect_embedded_emissions: float # t CO2e per tonne of good
    carbon_price_due_eur: float

class CBAMDeclarationGenerator:
    CBAM_XML_NAMESPACE = "urn:eu:cbam:registry:v1"

    @classmethod
    def generate_declaration_xml(
        cls,
        declaration_id: str,
        quarter: str,           # e.g., "2026-Q3"
        declarant_eori: str,
        installation: InstallationData,
        items: List[CBAMEmissionsItem]
    ) -> str:
        root = ET.Element("CBAMDeclaration", attrib={
            "xmlns": cls.CBAM_XML_NAMESPACE,
            "id": declaration_id,
            "quarter": quarter,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })


        # Header Block
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "DeclarantEORI").text = declarant_eori
        ET.SubElement(header, "ReportingPeriod").text = quarter
        ET.SubElement(header, "Version").text = "1.2"

        # Installation Block
        inst_elem = ET.SubElement(root, "Installation")
        ET.SubElement(inst_elem, "Name").text = installation.installation_name
        ET.SubElement(inst_elem, "CountryCode").text = installation.country_code
        ET.SubElement(inst_elem, "UNLOCODE").text = installation.un_locode
        geo = ET.SubElement(inst_elem, "Coordinates")
        ET.SubElement(geo, "Latitude").text = str(installation.latitude)
        ET.SubElement(geo, "Longitude").text = str(installation.longitude)

        # Goods & Emissions Block
        goods_list = ET.SubElement(root, "ImportedGoodsList")
        total_direct_co2 = 0.0
        total_indirect_co2 = 0.0
        total_carbon_levy_eur = 0.0

        for itm in items:
            good_elem = ET.SubElement(goods_list, "GoodItem", attrib={"itemId": itm.item_id})
            ET.SubElement(good_elem, "CNCode").text = itm.cn_code
            ET.SubElement(good_elem, "Description").text = itm.goods_description
            ET.SubElement(good_elem, "NetMassMetricTonnes").text = f"{itm.net_mass_tonnes:.3f}"
            ET.SubElement(good_elem, "ProductionRoute").text = itm.production_route

            emissions_elem = ET.SubElement(good_elem, "EmbeddedEmissions")
            total_item_direct = itm.net_mass_tonnes * itm.direct_embedded_emissions
            total_item_indirect = itm.net_mass_tonnes * itm.indirect_embedded_emissions

            ET.SubElement(emissions_elem, "SpecificDirectIntensity").text = f"{itm.direct_embedded_emissions:.4f}"
            ET.SubElement(emissions_elem, "SpecificIndirectIntensity").text = f"{itm.indirect_embedded_emissions:.4f}"
            ET.SubElement(emissions_elem, "TotalDirectEmissionsTonnes").text = f"{total_item_direct:.3f}"
            ET.SubElement(emissions_elem, "TotalIndirectEmissionsTonnes").text = f"{total_item_indirect:.3f}"

            total_direct_co2 += total_item_direct
            total_indirect_co2 += total_item_indirect
            total_carbon_levy_eur += itm.carbon_price_due_eur

        # Summary Block
        summary = ET.SubElement(root, "Summary")
        ET.SubElement(summary, "TotalDirectCO2Tonnes").text = f"{total_direct_co2:.3f}"
        ET.SubElement(summary, "TotalIndirectCO2Tonnes").text = f"{total_indirect_co2:.3f}"
        ET.SubElement(summary, "TotalEmbeddedCO2Tonnes").text = f"{total_direct_co2 + total_indirect_co2:.3f}"
        ET.SubElement(summary, "TotalCarbonLevyDueEUR").text = f"{total_carbon_levy_eur:.2f}"

        # Cryptographic Integrity Seal
        xml_string_pre = ET.tostring(root, encoding="utf-8").decode("utf-8")
        seal_hash = hashlib.sha256(xml_string_pre.encode("utf-8")).hexdigest()
        ET.SubElement(summary, "CryptographicVerificationSeal").text = f"CBAM-SEAL-{seal_hash[:16].upper()}"

        return ET.tostring(root, encoding="utf-8").decode("utf-8")
