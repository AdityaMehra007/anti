import hashlib
from datetime import datetime
from src.models import CommercialInvoice, ComplianceAuditReport, AuditResultItem
from src.hs_engine import HSCatalog

class ComplianceAuditor:
    EU_COUNTRIES = ["Germany", "France", "Italy", "Spain", "Netherlands", "Belgium", "Poland"]

    @classmethod
    def audit_invoice(cls, invoice: CommercialInvoice) -> ComplianceAuditReport:
        items_audited = []
        recommendations = []
        overall_status = "APPROVED"
        risk_score = 0.0

        is_eu_destination = invoice.consignee_country in cls.EU_COUNTRIES

        for item in invoice.items:
            classification = HSCatalog.classify(item.description)
            verified_hs = classification["hs_code"]
            conf = classification["confidence"]
            tariff = classification["tariff_rate"]
            cbam = classification["cbam_applicable"] and is_eu_destination
            scomet = classification["scomet_restricted"]

            status = "PASS"
            reasoning = classification["reasoning"]

            # Anomaly check: declared vs verified HS code
            if item.declared_hs_code and item.declared_hs_code != verified_hs:
                status = "WARNING"
                risk_score += 20.0
                reasoning += f" Warning: Declared HS {item.declared_hs_code} differs from verified standard {verified_hs}."
                recommendations.append(f"Reconcile HS code for item {item.item_id}: declared '{item.declared_hs_code}', recommend '{verified_hs}'.")

            # Check CBAM applicability
            if cbam:
                risk_score += 25.0
                status = "WARNING" if status == "PASS" else "REJECT"
                reasoning += " CRITICAL: Subject to EU Carbon Border Adjustment Mechanism (CBAM). Embedded emissions XML required."
                recommendations.append(f"Generate CBAM carbon intensity dossier for {item.description} to avoid EU port entry refusal.")

            # Check SCOMET dual-use restriction
            if scomet:
                risk_score += 35.0
                status = "REJECT"
                reasoning += " ALERT: SCOMET Dual-Use Category item detected. DGFT authorization license mandatory."
                recommendations.append(f"Verify DGFT SCOMET export license for item {item.item_id} before dispatching shipping bill.")

            items_audited.append(AuditResultItem(
                item_id=item.item_id,
                description=item.description,
                declared_hs_code=item.declared_hs_code,
                verified_hs_code=verified_hs,
                confidence=conf,
                tariff_rate_percent=tariff,
                cbam_applicable=cbam,
                scomet_restricted=scomet,
                status=status,
                reasoning=reasoning
            ))

        if risk_score >= 20.0 or any(i.status == "WARNING" for i in items_audited):
            overall_status = "REQUIRES_REVIEW"
        if any(i.status == "REJECT" for i in items_audited):
            overall_status = "REJECTED"

        cert_hash = hashlib.sha256(f"{invoice.invoice_number}{risk_score}{datetime.now().isoformat()}".encode('utf-8')).hexdigest()[:16]
        seal = f"TN-CERT-{cert_hash.upper()}"

        return ComplianceAuditReport(
            report_id=f"REP-{invoice.invoice_number}",
            invoice_number=invoice.invoice_number,
            timestamp=datetime.now().isoformat(),
            overall_status=overall_status,
            total_risk_score=min(100.0, risk_score),
            items_audited=items_audited,
            recommendations=recommendations,
            certificate_seal=seal
        )
