"""
VECTIS TRADE — Upgraded Full-Featured Web Server & API
Provides Compliance Auditor, SWIFT MT700 Parser, Lead CRM API, Outbox Certificates, and CBAM Engine.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vectis_core import (
    VectisComplianceEngine,
    LetterOfCredit,
    CommercialInvoice,
    PackingList,
    BillOfLading,
    CertificateOfOrigin
)
from vectis_swift_parser import parse_swift_mt700
from vectis_cbam import CBAMCalculator, ProductionData
from vectis_outreach_dispatcher import generate_cadence

PORT = 8080
STATIC_DIR = os.path.join(BASE_DIR, "static")
LEADS_FILE = os.path.join(BASE_DIR, "leads", "master_verified_leads.json")
OUTBOX_DIR = os.path.join(BASE_DIR, "outbox")

class VectisRequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html", "/portal"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(STATIC_DIR, "portal.html"), "rb") as f:
                self.wfile.write(f.read())

        elif self.path == "/api/leads":
            if os.path.exists(LEADS_FILE):
                with open(LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
                self.send_json(200, leads)
            else:
                self.send_json(200, [])

        elif self.path == "/api/certificates":
            certs = []
            if os.path.exists(OUTBOX_DIR):
                for f in os.listdir(OUTBOX_DIR):
                    if f.endswith("_audit_result.json"):
                        try:
                            with open(os.path.join(OUTBOX_DIR, f), "r", encoding="utf-8") as jf:
                                cdata = json.load(jf)
                            certs.append({
                                "filename": f,
                                "status": cdata.get("status", "UNKNOWN"),
                                "fatal_discrepancies": cdata.get("fatal_discrepancies", 0),
                                "sha256_hash": cdata.get("sha256_hash", "")
                            })
                        except Exception:
                            pass
            self.send_json(200, certs)

        elif self.path.startswith("/api/certificates/"):
            filename = self.path.replace("/api/certificates/", "").strip()
            # If asking for md cert
            md_name = filename.replace("_audit_result.json", "_certificate.md")
            target_path = os.path.join(OUTBOX_DIR, md_name)
            if os.path.exists(target_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                with open(target_path, "rb") as mf:
                    self.wfile.write(mf.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Certificate not found.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        if self.path == "/api/audit":
            try:
                data = json.loads(body)
                lc = LetterOfCredit(**data["lc"])
                inv = CommercialInvoice(**data["invoice"])
                pl = PackingList(**data["packing_list"])
                bl = BillOfLading(**data["bl"])
                coo = CertificateOfOrigin(**data["coo"]) if data.get("coo") else None

                engine = VectisComplianceEngine()
                result = engine.audit_trade_docket(lc, inv, pl, bl, coo)

                self.send_json(200, {
                    "docket_id": result.docket_id,
                    "timestamp": result.timestamp,
                    "status": result.status,
                    "discrepancy_count": result.discrepancy_count,
                    "fatal_discrepancies": result.fatal_discrepancies,
                    "sha256_hash": result.sha256_hash,
                    "docket_summary": result.docket_summary,
                    "discrepancies": [
                        {
                            "code": d.code,
                            "rule_reference": d.rule_reference,
                            "severity": d.severity,
                            "affected_document": d.affected_document,
                            "field_name": d.field_name,
                            "description": d.description,
                            "correction_suggestion": d.correction_suggestion
                        }
                        for d in result.discrepancies
                    ]
                })
            except Exception as e:
                self.send_json(400, {"error": str(e)})

        elif self.path == "/api/audit/swift":
            try:
                data = json.loads(body)
                swift_text = data.get("swift_text", "")
                lc = parse_swift_mt700(swift_text)

                # Use paired sample or synthesized invoice
                inv = CommercialInvoice(
                    invoice_number="PAM/EXP/2027/9941",
                    invoice_date="2027-04-05",
                    beneficiary=lc.beneficiary,
                    applicant=lc.applicant,
                    amount=lc.amount,
                    currency=lc.currency,
                    description_of_goods=lc.description_of_goods,
                    incoterms="CIF Hamburg"
                )
                pl = PackingList(
                    packing_list_number="PL-9941",
                    invoice_number="PAM/EXP/2027/9941",
                    total_packages=12,
                    package_type="Pallets",
                    gross_weight_kg=14240.0,
                    net_weight_kg=13800.0,
                    shipping_marks="MULLER/HAMBURG"
                )
                bl = BillOfLading(
                    bl_number="MEDU994100",
                    carrier_name="MSC",
                    shipper=lc.beneficiary,
                    consignee=f"To Order of {lc.issuing_bank}",
                    notify_party=lc.applicant,
                    port_of_loading=lc.port_of_loading,
                    port_of_discharge=lc.port_of_discharge,
                    shipped_on_board_date=lc.latest_shipment_date,
                    freight_status="Freight Prepaid",
                    clean_on_board=True,
                    total_packages=12,
                    gross_weight_kg=14240.0,
                    shipping_marks="MULLER/HAMBURG"
                )

                engine = VectisComplianceEngine()
                result = engine.audit_trade_docket(lc, inv, pl, bl)

                self.send_json(200, {
                    "docket_id": result.docket_id,
                    "timestamp": result.timestamp,
                    "status": result.status,
                    "discrepancy_count": result.discrepancy_count,
                    "fatal_discrepancies": result.fatal_discrepancies,
                    "sha256_hash": result.sha256_hash,
                    "docket_summary": result.docket_summary,
                    "discrepancies": [
                        {
                            "code": d.code,
                            "rule_reference": d.rule_reference,
                            "severity": d.severity,
                            "affected_document": d.affected_document,
                            "field_name": d.field_name,
                            "description": d.description,
                            "correction_suggestion": d.correction_suggestion
                        }
                        for d in result.discrepancies
                    ]
                })
            except Exception as e:
                self.send_json(400, {"error": str(e)})

        elif self.path == "/api/cbam/calculate":
            try:
                data = json.loads(body)
                prod = ProductionData(**data)
                calc = CBAMCalculator()
                res = calc.calculate_emissions(prod)
                self.send_json(200, {
                    "goods_name": res.goods_name,
                    "cn_code": res.cn_code,
                    "production_volume_tonnes": res.production_volume_tonnes,
                    "specific_direct_emissions": res.specific_direct_emissions,
                    "specific_indirect_emissions": res.specific_indirect_emissions,
                    "specific_total_emissions": res.specific_total_emissions,
                    "total_embedded_emissions_tco2": res.total_embedded_emissions_tco2,
                    "estimated_cbam_tariff_eur": res.estimated_cbam_tariff_eur,
                    "estimated_cbam_tariff_inr": res.estimated_cbam_tariff_inr,
                    "compliance_recommendation": res.compliance_recommendation
                })
            except Exception as e:
                self.send_json(400, {"error": str(e)})

        elif self.path == "/api/outreach/generate":
            try:
                generate_cadence()
                self.send_json(200, {"status": "SUCCESS", "message": "Cadence generated in company/outreach_queue/"})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
        else:
            self.send_response(404)
            self.end_headers()

def run(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, VectisRequestHandler)
    print(f"VECTIS TRADE Full-Featured Server running at http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down VECTIS server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
