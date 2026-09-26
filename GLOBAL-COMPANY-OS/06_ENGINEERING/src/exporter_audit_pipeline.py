"""
TradeNexus Batch Exporter Audit Pipeline (ANTIGRAVITY Ω∞)
Generates high-signal pre-shipment compliance audits and demurrage risk valuations
for target Indian mid-market exporters shipping to the EU and US.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from src.models import CommercialInvoice, LineItem, ComplianceAuditReport
from src.compliance_auditor import ComplianceAuditor

@dataclass
class ExporterProfile:
    company_name: str
    iec_code: str
    gstin: str
    destination_country: str
    destination_port: str
    sample_items: List[Dict[str, Any]]

class ExporterAuditPipeline:
    AVERAGE_DEMURRAGE_DAILY_RATE_USD = 450.0 # Standard port demurrage + detention penalty
    AVERAGE_PORT_HOLD_DAYS = 8               # Average duration of regulatory customs hold

    @classmethod
    def run_cohort_audit(cls, profiles: List[ExporterProfile]) -> List[Dict[str, Any]]:
        results = []

        for idx, profile in enumerate(profiles):
            line_items = []
            total_inv_amount = 0.0

            for itm_idx, itm in enumerate(profile.sample_items):
                val = itm.get("quantity", 100.0) * itm.get("unit_price", 50.0)
                total_inv_amount += val
                line_items.append(LineItem(
                    item_id=f"ITEM-{itm_idx+1}",
                    description=itm.get("description", "Manufactured Export Component"),
                    quantity=itm.get("quantity", 100.0),
                    unit=itm.get("unit", "NOS"),
                    unit_price=itm.get("unit_price", 50.0),
                    total_value=val,
                    currency="USD",
                    declared_hs_code=itm.get("declared_hs_code"),
                    weight_kg=itm.get("weight_kg", 500.0)
                ))

            invoice = CommercialInvoice(
                invoice_number=f"EXP-AUDIT-2026-{idx+1:03d}",
                exporter_name=profile.company_name,
                exporter_iec=profile.iec_code,
                exporter_gstin=profile.gstin,
                consignee_name="European Tier-1 Industrial Distribution BV",
                consignee_country=profile.destination_country,
                port_of_loading="INMAA1", # Chennai port
                port_of_discharge=profile.destination_port,
                items=line_items,
                total_amount=total_inv_amount,
                incoterm="FOB"
            )

            audit_report: ComplianceAuditReport = ComplianceAuditor.audit_invoice(invoice)

            # Demurrage Risk Valuation
            demurrage_at_risk = 0.0
            if audit_report.overall_status in ("REQUIRES_REVIEW", "REJECTED"):
                demurrage_at_risk = cls.AVERAGE_DEMURRAGE_DAILY_RATE_USD * cls.AVERAGE_PORT_HOLD_DAYS

            results.append({
                "exporter_name": profile.company_name,
                "iec_code": profile.iec_code,
                "destination": f"{profile.destination_port}, {profile.destination_country}",
                "audit_id": audit_report.report_id,
                "overall_status": audit_report.overall_status,
                "risk_score": audit_report.total_risk_score,
                "demurrage_exposure_usd": demurrage_at_risk,
                "recommendations_count": len(audit_report.recommendations),
                "certificate_seal": audit_report.certificate_seal,
                "recommendations": audit_report.recommendations
            })

        return results
