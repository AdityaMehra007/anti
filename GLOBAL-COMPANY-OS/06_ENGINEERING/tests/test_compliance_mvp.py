import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models import CommercialInvoice, LineItem
from src.compliance_auditor import ComplianceAuditor
from src.hs_engine import HSCatalog

def test_hs_catalog_radial_bearing():
    res = HSCatalog.classify("Precision radial ball bearing for automotive assembly")
    assert res["hs_code"] == "84821010"
    assert res["confidence"] >= 0.80
    assert res["cbam_applicable"] is False

def test_hs_catalog_steel_cbam():
    res = HSCatalog.classify("Hot rolled steel coil 2mm thickness")
    assert res["hs_code"] == "72081000"
    assert res["cbam_applicable"] is True

def test_audit_invoice_pass():
    invoice = CommercialInvoice(
        invoice_number="INV-2026-001",
        exporter_name="Apex Precision Engineering Pvt Ltd",
        exporter_iec="0712345678",
        exporter_gstin="29AAAAA0000A1Z5",
        consignee_name="Global Auto Components GmbH",
        consignee_country="Germany",
        port_of_loading="INMAA1", # Chennai port
        port_of_discharge="DEHAM", # Hamburg port
        total_amount=45000.0,
        items=[
            LineItem(
                item_id="ITM-1",
                description="Radial ball bearing steel",
                quantity=1000.0,
                unit="NOS",
                unit_price=45.0,
                total_value=45000.0,
                declared_hs_code="84821010",
                weight_kg=850.0
            )
        ]
    )
    report = ComplianceAuditor.audit_invoice(invoice)
    assert report.overall_status == "APPROVED"
    assert report.total_risk_score == 0.0
    assert report.items_audited[0].status == "PASS"

def test_audit_invoice_cbam_warning():
    invoice = CommercialInvoice(
        invoice_number="INV-2026-002",
        exporter_name="Bharat Steel Alloys Ltd",
        exporter_iec="0798765432",
        exporter_gstin="29BBBBB0000B1Z5",
        consignee_name="Euro Metals BV",
        consignee_country="Netherlands",
        port_of_loading="INMAA1",
        port_of_discharge="NLRTM",
        total_amount=120000.0,
        items=[
            LineItem(
                item_id="ITM-1",
                description="Hot rolled steel coil",
                quantity=50.0,
                unit="MT",
                unit_price=2400.0,
                total_value=120000.0,
                declared_hs_code="72081000",
                weight_kg=50000.0
            )
        ]
    )
    report = ComplianceAuditor.audit_invoice(invoice)
    assert report.overall_status in ["REQUIRES_REVIEW", "REJECTED"]
    assert report.items_audited[0].cbam_applicable is True
    assert "CBAM" in report.recommendations[0]

def test_api_endpoints_and_ui():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)
    
    # Test UI delivery
    ui_res = client.get("/")
    assert ui_res.status_code == 200
    assert "TradeNexus" in ui_res.text
    
    # Test Health Endpoint
    health_res = client.get("/api/v1/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "HEALTHY"
    
    # Test HS classification API
    classify_res = client.post("/api/v1/classify/hs?description=radial ball bearing")
    assert classify_res.status_code == 200
    assert classify_res.json()["hs_code"] == "84821010"

def test_batch_exporter_audit_pipeline():
    from src.exporter_audit_pipeline import ExporterAuditPipeline, ExporterProfile
    
    profiles = [
        ExporterProfile(
            company_name="Apex Auto Precision Ltd",
            iec_code="0712345678",
            gstin="29AAAAA0000A1Z5",
            destination_country="Germany",
            destination_port="DEHAM",
            sample_items=[
                {"description": "Radial ball bearing steel", "quantity": 500.0, "unit_price": 50.0, "declared_hs_code": "84821010"}
            ]
        ),
        ExporterProfile(
            company_name="Bharat Steel Tubing Corp",
            iec_code="0798765432",
            gstin="29BBBBB0000B1Z5",
            destination_country="Netherlands",
            destination_port="NLRTM",
            sample_items=[
                {"description": "Hot rolled steel coil", "quantity": 40.0, "unit_price": 2500.0, "declared_hs_code": "72081000"}
            ]
        )
    ]
    
    audits = ExporterAuditPipeline.run_cohort_audit(profiles)
    assert len(audits) == 2
    assert audits[0]["overall_status"] == "APPROVED"
    assert audits[0]["demurrage_exposure_usd"] == 0.0
    
    # Steel coil to Netherlands triggers CBAM warning & demurrage valuation
    assert audits[1]["overall_status"] in ("REQUIRES_REVIEW", "REJECTED")
    assert audits[1]["demurrage_exposure_usd"] == 3600.0 # 450 * 8 days
    assert "CBAM" in audits[1]["recommendations"][0]

def test_commercial_invoice_parser():
    from src.invoice_parser import CommercialInvoiceParser
    raw_text = """
    COMMERCIAL EXPORT INVOICE
    Invoice No: EXP-2026-990
    Exporter: Sansera Precision Components Ltd
    IEC: 0788001122
    GSTIN: 29AAACS1234A1Z1
    Consignee: Continental AG
    Destination Country: Germany
    Port of Discharge: Hamburg Port (DEHAM)
    
    Item: High tensile steel engine connecting rod
    Quantity: 500 NOS
    Price: 45.00
    """
    invoice = CommercialInvoiceParser.parse_invoice_text(raw_text)
    assert invoice.invoice_number == "EXP-2026-990"
    assert invoice.exporter_name == "Sansera Precision Components Ltd"
    assert invoice.exporter_iec == "0788001122"
    assert invoice.consignee_country == "Germany"
    assert invoice.port_of_discharge == "DEHAM"
    assert len(invoice.items) == 1
    assert invoice.items[0].quantity == 500.0
    assert invoice.items[0].total_value == 22500.0

def test_extended_api_endpoints():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)

    # Test parse text endpoint
    parse_res = client.post("/api/v1/invoice/parse-text?raw_text=Invoice%20No:%20TEST-01%20Exporter:%20Test%20Corp")
    assert parse_res.status_code == 200
    assert parse_res.json()["invoice_number"] == "TEST-01"

    # Test CBAM XML generation endpoint
    cbam_res = client.post(
        "/api/v1/cbam/generate-xml"
        "?declaration_id=DECL-TEST-01"
        "&quarter=2026-Q3"
        "&declarant_eori=DE99887766"
        "&installation_name=Bangalore%20Mill"
        "&un_locode=INBLR"
        "&cn_code=72081000"
        "&goods_description=Steel%20Coil"
        "&net_mass_tonnes=25.0"
        "&direct_emissions=1.85"
        "&indirect_emissions=0.45"
        "&carbon_price_due_eur=1200.0"
    )
    assert cbam_res.status_code == 200
    assert "CBAMDeclaration" in cbam_res.json()["xml_content"]

def test_batch_2_audits_and_dossiers():
    import os
    sales_audits_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "09_SALES", "audits"))
    belrise_html = os.path.join(sales_audits_dir, "AUDIT_BELRISE_INDUSTRIES_LIMITED.html")
    sundram_html = os.path.join(sales_audits_dir, "AUDIT_SUNDRAM_FASTENERS_LIMITED.html")
    motherson_html = os.path.join(sales_audits_dir, "AUDIT_MOTHERSON_SUMI_SYSTEMS_LIMITED.html")
    
    assert os.path.isfile(belrise_html)
    assert os.path.isfile(sundram_html)
    assert os.path.isfile(motherson_html)

    with open(sundram_html, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Sundram Fasteners Limited" in content
        assert "TN-CERT-" in content

def test_icegate_edi_generator():
    from src.icegate_edi_generator import ICEGATEEDIGenerator
    from src.models import CommercialInvoice, LineItem

    inv = CommercialInvoice(
        invoice_number="EXP-ICEGATE-TEST-001",
        exporter_name="Apex Precision Engineering Pvt Ltd",
        exporter_iec="0712345678",
        exporter_gstin="29AAAAA0000A1Z5",
        consignee_name="European Industrial Logistics BV",
        consignee_country="Germany",
        port_of_loading="INMAA1",
        port_of_discharge="DEHAM",
        items=[
            LineItem(
                item_id="ITEM-1",
                description="Precision radial ball bearing assembly",
                quantity=1000.0,
                unit="NOS",
                unit_price=45.0,
                total_value=45000.0,
                currency="USD",
                declared_hs_code="84821010",
                weight_kg=850.0
            )
        ],
        total_amount=45000.0,
        incoterm="FOB"
    )

    result = ICEGATEEDIGenerator.generate_shipping_bill_flatfile(inv)
    assert result["items_count"] == 1
    assert "CHEXP01" in result["flatfile_content"]
    assert "CHEXP02" in result["flatfile_content"]
    assert "CHEXP03" in result["flatfile_content"]
    assert "CHEXP04" in result["flatfile_content"]
    assert "TN-ICEGATE-" in result["cryptographic_seal"]
    assert "0712345678" in result["flatfile_content"]
    assert "84821010" in result["flatfile_content"]

    # Test Validation
    val_res = ICEGATEEDIGenerator.validate_icegate_payload(inv)
    assert val_res["is_valid_for_filing"] is True
    assert val_res["status"] == "READY_FOR_ICEGATE"

def test_icegate_api_endpoints():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)

    invoice_payload = {
        "invoice_number": "INV-API-EDI-01",
        "exporter_name": "Sansera Engineering Limited",
        "exporter_iec": "0788012345",
        "exporter_gstin": "29AAACS1234A1Z1",
        "consignee_name": "Bosch GmbH",
        "consignee_country": "Germany",
        "port_of_loading": "INMAA1",
        "port_of_discharge": "DEHAM",
        "items": [
            {
                "item_id": "ITEM-1",
                "description": "Connecting rod",
                "quantity": 500.0,
                "unit": "NOS",
                "unit_price": 50.0,
                "total_value": 25000.0,
                "currency": "USD",
                "declared_hs_code": "87082900",
                "weight_kg": 600.0
            }
        ],
        "total_amount": 25000.0,
        "incoterm": "FOB"
    }

    res = client.post("/api/v1/icegate/generate-flatfile", json=invoice_payload)
    assert res.status_code == 200
    data = res.json()
    assert "CHEXP01" in data["flatfile_content"]
    assert data["items_count"] == 1
    assert "TN-ICEGATE-" in data["cryptographic_seal"]

    val_res = client.post("/api/v1/icegate/validate-invoice", json=invoice_payload)
    assert val_res.status_code == 200
    assert val_res.json()["is_valid_for_filing"] is True

def test_batch_3_audits_and_dossiers():
    import os
    sales_audits_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "09_SALES", "audits"))
    bforge_html = os.path.join(sales_audits_dir, "AUDIT_BHARAT_FORGE_LIMITED.html")
    sona_html = os.path.join(sales_audits_dir, "AUDIT_SONA_BLW_PRECISION_FORGINGS_LIMITED_SONA_COMSTAR.html")
    wheels_html = os.path.join(sales_audits_dir, "AUDIT_WHEELS_INDIA_LIMITED_TVS_GROUP.html")

    assert os.path.isfile(bforge_html)
    assert os.path.isfile(sona_html)
    assert os.path.isfile(wheels_html)

    with open(bforge_html, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Bharat Forge Limited" in content
        assert "$24,000" in content
        assert "TN-CERT-" in content

def test_pilot_agreement_generator(tmp_path):
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "12_LEGAL")))
    from pilot_agreement_generator import PilotAgreementGenerator

    contract = PilotAgreementGenerator.generate_pilot_agreement(
        company_name="Sansera Engineering Limited",
        authorized_signatory="BR Preetham",
        signatory_title="Executive Director & CEO",
        registered_address="Bommasandra Industrial Area, Bengaluru",
        iec_code="0788012345",
        gstin="29AAACS1234A1Z1",
        monthly_fee_inr=35000.0,
        consignments_quota=50
    )

    assert "TN-PILOT-" in contract["contract_id"]
    assert contract["monthly_fee_inr"] == 35000.0
    assert "Sansera Engineering Limited" in contract["markdown_agreement"]
    assert "demurrage indemnity" in contract["markdown_agreement"].lower()
    assert "50 export consignments" in contract["markdown_agreement"]

    # Test saving
    paths = PilotAgreementGenerator.save_agreements(str(tmp_path), contract)
    assert os.path.isfile(paths["markdown_path"])
    assert os.path.isfile(paths["html_path"])

def test_packing_list_reconciliation_pass():
    from src.models import CommercialInvoice, LineItem, PackingList, PackingListPackage
    from src.packing_reconciler import PackingListReconciler

    inv = CommercialInvoice(
        invoice_number="INV-REC-001",
        exporter_name="Sansera Engineering Limited",
        exporter_iec="0788012345",
        exporter_gstin="29AAACS1234A1Z1",
        consignee_name="Bosch Germany",
        consignee_country="Germany",
        port_of_loading="INMAA1",
        port_of_discharge="DEHAM",
        items=[
            LineItem(
                item_id="CR-500",
                description="Connecting Rod Forged",
                quantity=500.0,
                unit="NOS",
                unit_price=40.0,
                total_value=20000.0,
                weight_kg=600.0
            )
        ],
        total_amount=20000.0
    )

    pkg = PackingList(
        packing_list_number="PK-REC-001",
        invoice_reference="INV-REC-001",
        exporter_name="Sansera Engineering Limited",
        consignee_name="Bosch Germany",
        total_packages=5,
        total_net_weight_kg=600.0,
        total_gross_weight_kg=680.0,
        packages=[
            PackingListPackage(
                package_id="PKG-01",
                package_type="WOODEN_PALLET",
                item_id="CR-500",
                quantity_packed=500.0,
                net_weight_kg=600.0,
                gross_weight_kg=680.0
            )
        ]
    )

    report = PackingListReconciler.reconcile(inv, pkg)
    assert report.status == "RECONCILED"
    assert report.discrepancy_count == 0
    assert report.demurrage_risk_assessment_usd == 0.0
    assert "TN-RECON-" in report.reconciliation_seal

def test_packing_list_reconciliation_discrepancy_and_api():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)

    payload = {
        "invoice": {
            "invoice_number": "INV-DISC-002",
            "exporter_name": "Bharat Forge Limited",
            "exporter_iec": "0388012345",
            "exporter_gstin": "27AAACB1234B1Z1",
            "consignee_name": "ZF Friedrichshafen",
            "consignee_country=" : "Germany",
            "consignee_country": "Germany",
            "port_of_loading": "INNSA1",
            "port_of_discharge": "DEHAM",
            "items": [
                {
                    "item_id": "AXLE-01",
                    "description": "Front Axle Assembly",
                    "quantity": 200.0,
                    "unit": "NOS",
                    "unit_price": 120.0,
                    "total_value": 24000.0,
                    "weight_kg": 4000.0
                }
            ],
            "total_amount": 24000.0
        },
        "packing_list": {
            "packing_list_number": "PK-DISC-002",
            "invoice_reference": "INV-DISC-002",
            "exporter_name": "Bharat Forge Limited",
            "consignee_name": "ZF Friedrichshafen",
            "total_packages": 10,
            "total_net_weight_kg": 4000.0,
            "total_gross_weight_kg": 3800.0, # Gross < Net: Triggers WEIGHT_INVERSION
            "packages": [
                {
                    "package_id": "PKG-01",
                    "package_type": "CRATE",
                    "item_id": "AXLE-01",
                    "quantity_packed": 180.0, # 180 vs 200: Triggers QUANTITY_MISMATCH
                    "net_weight_kg": 4000.0,
                    "gross_weight_kg": 3800.0
                }
            ]
        }
    }

    res = client.post("/api/v1/reconcile/packing-list", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "REJECTED"
    assert data["discrepancy_count"] >= 2
    assert data["demurrage_risk_assessment_usd"] > 0
    disc_types = [d["discrepancy_type"] for d in data["discrepancies"]]
    assert "WEIGHT_INVERSION" in disc_types
    assert "QUANTITY_MISMATCH" in disc_types

def test_document_ingestion_pipeline():
    from src.document_ingestion import DocumentIngestionPipeline

    composite_docket = """
    COMMERCIAL EXPORT INVOICE
    Invoice No: EXP-INGEST-777
    Exporter: Sansera Engineering Limited
    IEC: 0788012345
    GSTIN: 29AAACS1234A1Z1
    Consignee: Continental Automotive GmbH
    Destination Country: Germany
    Port of Discharge: Hamburg Port (DEHAM)

    Item: Precision connecting rod forged steel
    Quantity: 1000 NOS
    Price: 42.00

    ----------------------------------------
    PACKING LIST
    Packing List No: PK-INGEST-777
    Invoice Ref: EXP-INGEST-777
    Exporter: Sansera Engineering Limited
    Consignee: Continental Automotive GmbH
    Total Packages: 10
    Total Net Weight: 800.0 kg
    Total Gross Weight: 890.0 kg

    Package: PKG-01 Item: ITEM-1 Quantity: 1000.0 Net: 800.0 Gross: 890.0
    """

    report = DocumentIngestionPipeline.process_composite_docket(composite_docket)
    assert report.invoice_number == "EXP-INGEST-777"
    assert report.packing_list_number == "PK-INGEST-777"
    assert "TN-DOCKET-" in report.master_seal
    assert report.composite_status in ("CLEARED_FOR_ICEGATE", "REQUIRES_REVISION")
    assert report.compliance_audit is not None
    assert report.packing_reconciliation is not None
    assert len(report.recommendations) > 0

def test_docket_audit_api_endpoints():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)

    raw_text = "Invoice No: EXP-TEST-999 Exporter: Test Corp\n---\nPACKING LIST\nPacking List No: PK-TEST-999 Invoice Ref: EXP-TEST-999"
    res = client.post("/api/v1/docket/audit-text", json={"raw_docket_text": raw_text})
    assert res.status_code == 200
    data = res.json()
    assert data["invoice_number"] == "EXP-TEST-999"
    assert "TN-DOCKET-" in data["master_seal"]
    assert "compliance_audit" in data
    assert "packing_reconciliation" in data







