"""
OMEGA INFINITY (Ω-OS) — VECTIS TRADE ENTERPRISE ADAPTER
Bridges VECTIS Trade UCP 600 / ISBP 745 Discrepancy Engine, SWIFT MT700 Parser,
EU CBAM Calculator, and Outbox Audit Certificates into the Sovereign Kernel.
"""

import os
import sys
import json
import glob
from typing import Dict, Any, List, Optional

# Add repo root to sys.path so we can cleanly import company modules
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from company.vectis_core import (
    LetterOfCredit,
    CommercialInvoice,
    PackingList,
    BillOfLading,
    CertificateOfOrigin,
    Discrepancy,
    AuditResult,
    VectisComplianceEngine
)
from company.vectis_swift_parser import parse_swift_mt700, SAMPLE_SWIFT_MT700
from company.vectis_cbam import CBAMCalculator, ProductionData, CBAMDeclaration
from omega_infinity.omega_infinity_core import get_kernel


class VectisEnterpriseAdapter:
    """
    Unified enterprise bridge providing high-level trade operations to Ω-OS.
    """

    def __init__(self):
        self.engine = VectisComplianceEngine()
        self.cbam_calc = CBAMCalculator()
        self.kernel = get_kernel()
        self.outbox_dir = os.path.join(REPO_ROOT, "company", "outbox")
        os.makedirs(self.outbox_dir, exist_ok=True)

    def audit_docket(self, docket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comprehensive UCP 600 & ISBP 745 compliance check on arbitrary trade docket dict.
        """
        try:
            lc_raw = docket_data.get("letter_of_credit") or docket_data.get("lc")
            inv_raw = docket_data.get("commercial_invoice") or docket_data.get("invoice")
            bl_raw = docket_data.get("bill_of_lading") or docket_data.get("bl")
            pl_raw = docket_data.get("packing_list")
            coo_raw = docket_data.get("certificate_of_origin") or docket_data.get("coo")

            if not lc_raw or not inv_raw or not bl_raw:
                return {"success": False, "error": "Docket missing required 'lc', 'invoice', or 'bl' sections"}

            lc = LetterOfCredit(**lc_raw)
            inv = CommercialInvoice(**inv_raw)
            bl = BillOfLading(**bl_raw)
            pl = PackingList(**pl_raw) if pl_raw else PackingList(
                packing_list_number="PL-DEFAULT",
                invoice_number=inv.invoice_number,
                total_packages=bl.total_packages,
                package_type="Cartons",
                gross_weight_kg=bl.gross_weight_kg,
                net_weight_kg=bl.gross_weight_kg * 0.95,
                shipping_marks=bl.shipping_marks
            )
            co = CertificateOfOrigin(**coo_raw) if coo_raw else None

            report: AuditResult = self.engine.audit_trade_docket(lc, inv, pl, bl, co)
            passed = (report.status == "PASSED")

            # Update kernel state telemetry & append to ledger
            if passed:
                self.kernel.state.telemetry["trade_audits_passed"] += 1
            else:
                self.kernel.state.telemetry["trade_audits_failed"] += 1

            self.kernel.dispatch_event(
                event_name="TRADE_AUDIT_COMPLETED",
                actor="VECTIS_TRADE_ENGINE",
                data={
                    "docket_id": report.docket_id,
                    "passed": passed,
                    "discrepancies_count": report.discrepancy_count,
                    "seal_hash": report.sha256_hash
                }
            )

            return {
                "success": True,
                "docket_id": report.docket_id,
                "passed": passed,
                "discrepancy_count": report.discrepancy_count,
                "fatal_count": report.fatal_discrepancies,
                "discrepancies": [
                    {
                        "code": d.code,
                        "rule": d.rule_reference,
                        "description": d.description,
                        "document": d.affected_document,
                        "severity": d.severity,
                        "remediation": d.correction_suggestion
                    } for d in report.discrepancies
                ],
                "certificate_seal": report.sha256_hash,
                "audit_timestamp": report.timestamp
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def parse_swift_and_audit(self, raw_swift_text: str) -> Dict[str, Any]:
        """
        Parses raw SWIFT MT700 text, synthesizes matching clean shipping documents,
        and executes an audit cycle.
        """
        try:
            lc = parse_swift_mt700(raw_swift_text)

            inv = CommercialInvoice(
                invoice_number="INV-EXP-2027-001",
                invoice_date=lc.latest_shipment_date,
                beneficiary=lc.beneficiary,
                applicant=lc.applicant,
                amount=lc.amount,
                currency=lc.currency,
                description_of_goods=lc.description_of_goods,
                incoterms="CIF Hamburg Incoterms 2020"
            )

            bl = BillOfLading(
                bl_number="BL-MAERSK-99201",
                carrier_name="Maersk Line India",
                shipper=lc.beneficiary,
                consignee=f"TO ORDER OF {lc.issuing_bank}",
                notify_party=lc.applicant,
                port_of_loading=lc.port_of_loading,
                port_of_discharge=lc.port_of_discharge,
                shipped_on_board_date=lc.latest_shipment_date,
                freight_status="Freight Prepaid",
                clean_on_board=True,
                total_packages=50,
                gross_weight_kg=12500.0,
                shipping_marks="PRECISION-001/50"
            )

            pl = PackingList(
                packing_list_number="PL-EXP-2027-001",
                invoice_number=inv.invoice_number,
                total_packages=50,
                package_type="Wooden Crates",
                gross_weight_kg=12500.0,
                net_weight_kg=11800.0,
                shipping_marks="PRECISION-001/50"
            )

            report = self.engine.audit_trade_docket(lc, inv, pl, bl)
            passed = (report.status == "PASSED")

            self.kernel.dispatch_event(
                event_name="SWIFT_AUDIT_PROCESSED",
                actor="VECTIS_SWIFT_GATEWAY",
                data={
                    "lc_number": lc.lc_number,
                    "applicant": lc.applicant,
                    "beneficiary": lc.beneficiary,
                    "passed": passed,
                    "seal": report.sha256_hash
                }
            )

            return {
                "success": True,
                "lc_number": lc.lc_number,
                "applicant": lc.applicant,
                "beneficiary": lc.beneficiary,
                "amount": lc.amount,
                "currency": lc.currency,
                "passed": passed,
                "discrepancies": [d.description for d in report.discrepancies],
                "certificate_seal": report.sha256_hash
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_cbam(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates EU CBAM embedded emissions and carbon tariff liability.
        """
        try:
            prod = ProductionData(
                goods_name=payload.get("goods_name", "Finished Carbon Steel Flanges"),
                cn_code=payload.get("cn_code", "73071990"),
                quantity_metric_tonnes=float(payload.get("quantity_metric_tonnes", 50.0)),
                direct_fuel_emissions_tco2=float(payload.get("direct_fuel_emissions_tco2", 28.5)),
                electricity_consumed_mwh=float(payload.get("electricity_consumed_mwh", 32.0)),
                scrap_precursor_used_tonnes=float(payload.get("scrap_precursor_used_tonnes", 5.0))
            )
            fx = float(payload.get("fx_eur_inr", 90.0))
            decl: CBAMDeclaration = self.cbam_calc.calculate_emissions(prod, fx_eur_inr=fx)

            self.kernel.state.telemetry["cbam_assessments_completed"] += 1
            self.kernel.dispatch_event(
                event_name="CBAM_ASSESSMENT_COMPLETED",
                actor="VECTIS_CBAM_ENGINE",
                data={
                    "goods_name": decl.goods_name,
                    "cn_code": decl.cn_code,
                    "tonnes": decl.production_volume_tonnes,
                    "tariff_eur": decl.estimated_cbam_tariff_eur,
                    "tariff_inr": decl.estimated_cbam_tariff_inr
                }
            )

            return {
                "success": True,
                "goods_name": decl.goods_name,
                "cn_code": decl.cn_code,
                "production_volume_tonnes": decl.production_volume_tonnes,
                "specific_direct_emissions": decl.specific_direct_emissions,
                "specific_indirect_emissions": decl.specific_indirect_emissions,
                "specific_total_emissions": decl.specific_total_emissions,
                "total_embedded_emissions_tco2": decl.total_embedded_emissions_tco2,
                "estimated_cbam_tariff_eur": decl.estimated_cbam_tariff_eur,
                "estimated_cbam_tariff_inr": decl.estimated_cbam_tariff_inr,
                "compliance_recommendation": decl.compliance_recommendation
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_outbox_certificates(self) -> List[Dict[str, Any]]:
        """Lists sealed markdown certificates from outbox directory."""
        certs = []
        files = glob.glob(os.path.join(self.outbox_dir, "*_certificate.md"))
        for fpath in sorted(files, key=os.path.getmtime, reverse=True):
            fname = os.path.basename(fpath)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                seal = "VERIFIED_SHA256"
                for line in content.splitlines():
                    if "SHA-256 SEAL:" in line:
                        seal = line.split("`")[1] if "`" in line else line.split(":")[-1].strip()
                        break
                certs.append({
                    "filename": fname,
                    "filepath": fpath,
                    "seal": seal,
                    "size_bytes": len(content),
                    "modified": os.path.getmtime(fpath)
                })
            except Exception:
                continue
        return certs
