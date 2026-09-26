"""
Unit and behavioral tests for VECTIS TRADE Compliance Engine.
"""

import pytest
from company.vectis_core import (
    VectisComplianceEngine,
    LetterOfCredit,
    CommercialInvoice,
    PackingList,
    BillOfLading,
    CertificateOfOrigin
)

@pytest.fixture
def clean_docket():
    lc = LetterOfCredit(
        lc_number="LC-PEENYA-2027-001",
        issuing_bank="Deutsche Bank AG, Frankfurt",
        applicant="Muller Automobiltechnik GmbH",
        beneficiary="Precision Auto Machining Pvt Ltd",
        amount=180000.00,
        currency="EUR",
        tolerance_pct=5.0,
        latest_shipment_date="2027-03-31",
        expiry_date="2027-04-21",
        port_of_loading="Chennai Port, India",
        port_of_discharge="Hamburg, Germany",
        description_of_goods="CNC Machined Transmission Flanges Grade 316 as per PO 88412"
    )

    invoice = CommercialInvoice(
        invoice_number="PAM/EXP/2027/089",
        invoice_date="2027-03-15",
        beneficiary="Precision Auto Machining Pvt Ltd",
        applicant="Muller Automobiltechnik GmbH",
        amount=180000.00,
        currency="EUR",
        description_of_goods="CNC Machined Transmission Flanges Grade 316 as per PO 88412",
        incoterms="CIF Hamburg"
    )

    packing_list = PackingList(
        packing_list_number="PL/2027/089",
        invoice_number="PAM/EXP/2027/089",
        total_packages=12,
        package_type="Wooden Pallets",
        gross_weight_kg=14240.00,
        net_weight_kg=13800.00,
        shipping_marks="MULLER/HAMBURG/1-12"
    )

    bl = BillOfLading(
        bl_number="MEDUCN1899201",
        carrier_name="Mediterranean Shipping Company (MSC)",
        shipper="Precision Auto Machining Pvt Ltd",
        consignee="To Order of Deutsche Bank AG, Frankfurt",
        notify_party="Muller Automobiltechnik GmbH",
        port_of_loading="Chennai Port, India",
        port_of_discharge="Hamburg, Germany",
        shipped_on_board_date="2027-03-20",
        freight_status="Freight Prepaid",
        clean_on_board=True,
        total_packages=12,
        gross_weight_kg=14240.00,
        shipping_marks="MULLER/HAMBURG/1-12"
    )

    coo = CertificateOfOrigin(
        coo_number="COO-FIEO-2027-891",
        issuing_authority="Federation of Indian Export Organisations (FIEO)",
        exporter="Precision Auto Machining Pvt Ltd",
        consignee="Muller Automobiltechnik GmbH",
        origin_country="India",
        gross_weight_kg=14240.00,
        invoice_number="PAM/EXP/2027/089"
    )

    return lc, invoice, packing_list, bl, coo

def test_clean_docket_passes(clean_docket):
    engine = VectisComplianceEngine()
    lc, invoice, pl, bl, coo = clean_docket
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    assert result.status == "PASSED"
    assert result.fatal_discrepancies == 0
    assert result.discrepancy_count == 0
    assert len(result.sha256_hash) == 64

def test_goods_description_mismatch_fails_art_18c(clean_docket):
    engine = VectisComplianceEngine()
    lc, invoice, pl, bl, coo = clean_docket
    # Introduce typo: omits "Grade 316"
    invoice.description_of_goods = "CNC Machined Transmission Flanges as per PO 88412"
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    assert result.status == "DISCREPANCIES_FOUND"
    assert result.fatal_discrepancies >= 1
    codes = [d.code for d in result.discrepancies]
    assert "DISC-INV-005" in codes

def test_gross_weight_conflict_fails_isbp_745(clean_docket):
    engine = VectisComplianceEngine()
    lc, invoice, pl, bl, coo = clean_docket
    # Packing list says 14,240 KG, BL says 14,800 KG
    bl.gross_weight_kg = 14800.00
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    assert result.status == "DISCREPANCIES_FOUND"
    codes = [d.code for d in result.discrepancies]
    assert "DISC-XDOC-002" in codes

def test_late_shipment_fails_art_14c(clean_docket):
    engine = VectisComplianceEngine()
    lc, invoice, pl, bl, coo = clean_docket
    # Latest shipment allowed is 2027-03-31; BL is dated 2027-04-05
    bl.shipped_on_board_date = "2027-04-05"
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    assert result.status == "DISCREPANCIES_FOUND"
    codes = [d.code for d in result.discrepancies]
    assert "DISC-BL-004" in codes

def test_unclean_bl_fails_art_27(clean_docket):
    engine = VectisComplianceEngine()
    lc, invoice, pl, bl, coo = clean_docket
    bl.clean_on_board = False
    result = engine.audit_trade_docket(lc, invoice, pl, bl, coo)

    assert result.status == "DISCREPANCIES_FOUND"
    codes = [d.code for d in result.discrepancies]
    assert "DISC-BL-001" in codes
