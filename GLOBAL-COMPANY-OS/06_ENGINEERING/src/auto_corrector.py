"""
TradeNexus Autonomous Discrepancy Auto-Corrector Engine
Identifies and automatically remediates regulatory, tariff, and clerical defects in export dockets.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DocketCorrectionSuggestion(BaseModel):
    field_name: str
    original_value: Any
    suggested_value: Any
    issue_type: str
    confidence: float
    regulatory_reference: str
    remediation_rationale: str

class AutoCorrectionReport(BaseModel):
    invoice_number: str
    total_issues_found: int
    auto_correctable: int
    suggestions: List[DocketCorrectionSuggestion]
    clean_status: bool

class DocketAutoCorrector:
    @classmethod
    def analyze_and_correct(cls, invoice_data: Dict[str, Any], packing_data: Optional[Dict[str, Any]] = None) -> AutoCorrectionReport:
        suggestions: List[DocketCorrectionSuggestion] = []
        inv_num = invoice_data.get("invoice_number", "UNKNOWN")
        line_items = invoice_data.get("items") or invoice_data.get("line_items", [])
        buyer_tax_id = invoice_data.get("buyer_tax_id", "")
        destination_country = invoice_data.get("consignee_country") or invoice_data.get("destination_country", "")

        eu_countries = ["DE", "FR", "IT", "NL", "BE", "ES", "PL", "SE", "AT", "GERMANY", "FRANCE", "NETHERLANDS"]
        if destination_country.upper() in eu_countries:
            if not buyer_tax_id or not (buyer_tax_id.startswith("NL") or buyer_tax_id.startswith("DE") or buyer_tax_id.startswith("FR")):
                suggestions.append(DocketCorrectionSuggestion(
                    field_name="buyer_tax_id",
                    original_value=buyer_tax_id or "MISSING",
                    suggested_value="REQUIRED_VALID_EU_EORI",
                    issue_type="EORI_MISSING",
                    confidence=0.98,
                    regulatory_reference="Union Customs Code (UCC) Regulation (EU) No 952/2013 Art 9",
                    remediation_rationale="Consignee EORI number is mandatory for EU import declaration and CBAM carbon clearance."
                ))

        for idx, item in enumerate(line_items):
            hs = str(item.get("declared_hs_code") or item.get("hs_code", "")).strip()
            digits = "".join(c for c in hs if c.isdigit())
            if len(digits) == 6:
                suffix_map = {
                    "848210": "84821010",
                    "732690": "73269099",
                    "880330": "88033000",
                    "291539": "29153990"
                }
                suggested_hs = suffix_map.get(digits, digits + "00")
                suggestions.append(DocketCorrectionSuggestion(
                    field_name=f"items[{idx}].declared_hs_code",
                    original_value=hs,
                    suggested_value=suggested_hs,
                    issue_type="TARIFF_PREFIX",
                    confidence=0.95,
                    regulatory_reference="DGFT ITC (HS) 2022 Schedule 1 (Export Policy)",
                    remediation_rationale="Indian ICEGATE shipping bills strictly require 8-digit ITC(HS) codes. 6-digit WCO subheading will cause EDI rejection SB002."
                ))

            uom = str(item.get("unit") or item.get("unit_of_measure", "")).upper().strip()
            if uom in ["PCS", "PIECES", "EACH"]:
                suggestions.append(DocketCorrectionSuggestion(
                    field_name=f"items[{idx}].unit",
                    original_value=uom,
                    suggested_value="NOS",
                    issue_type="UNIT_OF_MEASURE",
                    confidence=0.99,
                    regulatory_reference="CBIC Standard Unit Quantity Code (UQC) Directory",
                    remediation_rationale="Customs Electronic Data Interchange mandates CBIC standard UQC. 'PCS' must be normalized to 'NOS'."
                ))
            elif uom in ["KG", "KILOGRAM", "KILOGRAMS"]:
                suggestions.append(DocketCorrectionSuggestion(
                    field_name=f"items[{idx}].unit",
                    original_value=uom,
                    suggested_value="KGS",
                    issue_type="UNIT_OF_MEASURE",
                    confidence=0.99,
                    regulatory_reference="CBIC Standard Unit Quantity Code (UQC) Directory",
                    remediation_rationale="'KG' must be normalized to CBIC standard 3-letter UQC code 'KGS'."
                ))

            qty = float(item.get("quantity", 0))
            rate = float(item.get("unit_price", 0))
            claimed_total = float(item.get("total_value") if "total_value" in item else item.get("total_price", 0))
            expected_total = round(qty * rate, 2)
            if abs(claimed_total - expected_total) > 0.05:
                suggestions.append(DocketCorrectionSuggestion(
                    field_name=f"items[{idx}].total_value",
                    original_value=claimed_total,
                    suggested_value=expected_total,
                    issue_type="VALUE_MISMATCH",
                    confidence=1.0,
                    regulatory_reference="Customs Valuation Rules 2007",
                    remediation_rationale=f"Arithmetic discrepancy detected. Quantity ({qty}) * Unit Price ({rate}) equals {expected_total}, but line declared {claimed_total}."
                ))

        if packing_data:
            inv_weight = float(invoice_data.get("total_net_weight_kg", 0) or 0)
            pack_weight = float(packing_data.get("total_net_weight_kg", 0) or 0)
            if inv_weight > 0 and pack_weight > 0 and abs(inv_weight - pack_weight) > 0.5:
                suggestions.append(DocketCorrectionSuggestion(
                    field_name="total_net_weight_kg",
                    original_value=inv_weight,
                    suggested_value=pack_weight,
                    issue_type="WEIGHT_DISCREPANCY",
                    confidence=0.92,
                    regulatory_reference="Customs Act 1962 Section 50",
                    remediation_rationale=f"Commercial Invoice weight ({inv_weight} kg) differs from verified Packing List tally ({pack_weight} kg)."
                ))

        return AutoCorrectionReport(
            invoice_number=inv_num,
            total_issues_found=len(suggestions),
            auto_correctable=len([s for s in suggestions if s.confidence >= 0.90]),
            suggestions=suggestions,
            clean_status=(len(suggestions) == 0)
        )
