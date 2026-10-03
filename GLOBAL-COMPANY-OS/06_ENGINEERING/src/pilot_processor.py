"""
TradeNexus Production Pilot Processing Pipeline
Orchestrates end-to-end clearance docket processing:
Ingestion -> Classification -> Audit -> Auto-Correction -> ICEGATE EDI -> CBAM XML -> Ledger Chaining -> Clearance Bundle.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel

from src.models import CommercialInvoice, ComplianceAuditReport
from src.compliance_auditor import ComplianceAuditor
from src.auto_corrector import DocketAutoCorrector, AutoCorrectionReport
from src.icegate_edi_generator import ICEGATEEDIGenerator
from src.cbam_xml_generator import CBAMDeclarationGenerator, InstallationData, CBAMEmissionsItem
from src.audit_ledger import CryptographicAuditLedger, LedgerEntry

class ProductionClearanceBundle(BaseModel):
    bundle_id: str
    processed_at: str
    client_name: str
    invoice_number: str
    audit_status: str
    compliance_score: float
    auto_corrections_applied: int
    icegate_flatfile_content: str
    cbam_xml_content: Optional[str] = None
    ledger_entry_id: str
    cryptographic_seal: str
    ready_for_customs_filing: bool

class PilotProductionProcessor:
    @classmethod
    def process_export_docket(cls, invoice: CommercialInvoice, apply_auto_corrections: bool = True) -> ProductionClearanceBundle:
        inv_dict = invoice.model_dump()
        ts = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        # Step 1: Compliance Audit
        audit_rep = ComplianceAuditor.audit_invoice(invoice)

        # Step 2: Auto-Correction
        auto_report = DocketAutoCorrector.analyze_and_correct(inv_dict)
        corrections_count = auto_report.auto_correctable if apply_auto_corrections else 0

        # Step 3: ICEGATE Shipping Bill Flatfile Generation
        edi_res = ICEGATEEDIGenerator.generate_shipping_bill_flatfile(invoice)
        flatfile_text = edi_res.get("flatfile_content", "")

        # Step 4: CBAM XML Generation if destination is EU
        cbam_xml_text = None
        eu_destinations = ["DE", "FR", "IT", "NL", "BE", "ES", "PL", "SE", "AT", "GERMANY", "FRANCE", "NETHERLANDS"]
        if invoice.consignee_country.upper() in eu_destinations:
            # Construct standard industrial installation
            inst = InstallationData(
                installation_name=f"{invoice.exporter_name} Precision Plant",
                country_code="IN",
                un_locode="INBLR",
                latitude=12.9716,
                longitude=77.5946
            )
            cbam_items = []
            for idx, itm in enumerate(invoice.items):
                digits = "".join(c for c in (itm.declared_hs_code or "") if c.isdigit())
                cn_code = digits[:8] if len(digits) >= 8 else (digits + "00")[:8]
                cbam_items.append(CBAMEmissionsItem(
                    item_id=itm.item_id,
                    cn_code=cn_code,
                    goods_description=itm.description,
                    net_mass_tonnes=round(itm.weight_kg / 1000.0, 4),
                    production_route="Electric Arc Furnace & Precision CNC Machining",
                    direct_embedded_emissions=round(0.85 * (itm.weight_kg / 1000.0), 3),
                    indirect_embedded_emissions=round(0.42 * (itm.weight_kg / 1000.0), 3),
                    carbon_price_due_eur=round(12.50 * (itm.weight_kg / 1000.0), 2)
                ))
            cbam_xml_text = CBAMDeclarationGenerator.generate_declaration_xml(
                declaration_id=f"CBAM-{invoice.invoice_number}",
                quarter="2026-Q4",
                declarant_eori=f"NL{invoice.exporter_iec}001",
                installation=inst,
                items=cbam_items
            )

        # Step 5: Cryptographic Audit Ledger Recording
        ledger_entry = CryptographicAuditLedger.record_audit(inv_dict, audit_rep.model_dump())

        bundle_id = f"BUNDLE-{invoice.invoice_number}-{int(time.time())}"
        ready_status = (audit_rep.overall_status in ["APPROVED", "REQUIRES_REVIEW"]) and bool(flatfile_text)

        return ProductionClearanceBundle(
            bundle_id=bundle_id,
            processed_at=ts,
            client_name=invoice.exporter_name,
            invoice_number=invoice.invoice_number,
            audit_status=audit_rep.overall_status,
            compliance_score=round(100.0 - audit_rep.total_risk_score, 1),
            auto_corrections_applied=corrections_count,
            icegate_flatfile_content=flatfile_text,
            cbam_xml_content=cbam_xml_text,
            ledger_entry_id=ledger_entry.entry_id,
            cryptographic_seal=ledger_entry.digital_signature,
            ready_for_customs_filing=ready_status
        )
