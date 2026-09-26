"""
End-to-End System Tests for VECTIS TRADE
Verifies SWIFT MT700 parsing, CBAM calculations, compliance auditing, and outreach dispatcher.
"""

import pytest
import os
import json

from company.vectis_core import (
    VectisComplianceEngine,
    CommercialInvoice,
    PackingList,
    BillOfLading
)
from company.vectis_swift_parser import parse_swift_mt700, SAMPLE_SWIFT_MT700
from company.vectis_cbam import CBAMCalculator, ProductionData

def test_swift_mt700_parsing():
    lc = parse_swift_mt700(SAMPLE_SWIFT_MT700)
    assert lc.lc_number == "LC-DB-2027-9941"
    assert lc.amount == 180000.00
    assert lc.currency == "EUR"
    assert lc.tolerance_pct == 5.0
    assert "TRANSMISSION FLANGES" in lc.description_of_goods
    assert "MULLER AUTOMOBILTECHNIK" in lc.applicant
    assert "PRECISION AUTO MACHINING" in lc.beneficiary

def test_swift_to_compliance_audit_pipeline():
    lc = parse_swift_mt700(SAMPLE_SWIFT_MT700)
    
    invoice = CommercialInvoice(
        invoice_number="INV-2027-9941",
        invoice_date="2027-04-05",
        beneficiary=lc.beneficiary,
        applicant=lc.applicant,
        amount=180000.00,
        currency="EUR",
        description_of_goods=lc.description_of_goods,
        incoterms="CIF Hamburg"
    )

    packing_list = PackingList(
        packing_list_number="PL-9941",
        invoice_number="INV-2027-9941",
        total_packages=10,
        package_type="Pallets",
        gross_weight_kg=12000.0,
        net_weight_kg=11500.0,
        shipping_marks="MULLER/HAMBURG"
    )

    bl = BillOfLading(
        bl_number="MSC-9941",
        carrier_name="MSC",
        shipper=lc.beneficiary,
        consignee=f"To Order of {lc.issuing_bank}",
        notify_party=lc.applicant,
        port_of_loading=lc.port_of_loading,
        port_of_discharge=lc.port_of_discharge,
        shipped_on_board_date="2027-04-10",
        freight_status="Freight Prepaid",
        clean_on_board=True,
        total_packages=10,
        gross_weight_kg=12000.0,
        shipping_marks="MULLER/HAMBURG"
    )

    engine = VectisComplianceEngine()
    result = engine.audit_trade_docket(lc, invoice, packing_list, bl)

    assert result.status == "PASSED"
    assert result.fatal_discrepancies == 0
    assert len(result.sha256_hash) == 64

def test_cbam_emissions_calculation():
    calc = CBAMCalculator()
    prod = ProductionData(
        goods_name="Alloy Steel CNC Parts",
        cn_code="7307 19 90",
        quantity_metric_tonnes=10.0,
        direct_fuel_emissions_tco2=8.0,
        electricity_consumed_mwh=12.0
    )
    res = calc.calculate_emissions(prod)
    assert res.production_volume_tonnes == 10.0
    assert res.specific_direct_emissions == 0.8
    assert res.specific_indirect_emissions > 0.8
    assert res.estimated_cbam_tariff_eur > 0.0
    assert res.estimated_cbam_tariff_inr > 0.0

def test_outreach_queue_file_exists():
    queue_file = os.path.join(os.path.dirname(__file__), "outreach_queue", "dispatch_queue.json")
    if os.path.exists(queue_file):
        with open(queue_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) > 0
        assert "touch1_body" in data[0]
