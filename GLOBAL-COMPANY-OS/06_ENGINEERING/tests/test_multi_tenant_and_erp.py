import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models import CommercialInvoice, LineItem
from src.multi_tenant_dispatcher import MultiTenantDispatcher, MultiTenantBatchRequest
from src.erp_connector import ERPConnector
from src.audit_ledger import CryptographicAuditLedger

@pytest.fixture(autouse=True)
def clean_ledger():
    CryptographicAuditLedger.reset_ledger()

def test_multi_tenant_batch_processing():
    inv1 = CommercialInvoice(
        invoice_number="EXP-SANSERA-002",
        exporter_name="Sansera Engineering Limited",
        exporter_iec="0788012345",
        exporter_gstin="29AAACS1234F1Z5",
        consignee_name="Robert Bosch GmbH",
        consignee_country="DE",
        port_of_loading="INBLR4",
        port_of_discharge="DEHAM",
        total_amount=35000.0,
        incoterm="CIF",
        items=[
            LineItem(
                item_id="ITM-SAN-03",
                description="Precision Forged Steel Connecting Rods",
                quantity=1000,
                unit="NOS",
                unit_price=35.0,
                total_value=35000.0,
                currency="EUR",
                declared_hs_code="73269099",
                weight_kg=1200.0
            )
        ]
    )

    inv2 = CommercialInvoice(
        invoice_number="EXP-DYN-001",
        exporter_name="Dynamatic Technologies Limited",
        exporter_iec="0791004321",
        exporter_gstin="29AAACD9876E1Z2",
        consignee_name="Airbus Commercial Aircraft",
        consignee_country="FR",
        port_of_loading="INBLR4",
        port_of_discharge="FRTLS",
        total_amount=75000.0,
        incoterm="FOB",
        items=[
            LineItem(
                item_id="DYN-AERO-01",
                description="Aircraft Flap Track Structural Beam",
                quantity=2,
                unit="NOS",
                unit_price=37500.0,
                total_value=75000.0,
                currency="EUR",
                declared_hs_code="88033000",
                weight_kg=320.0
            )
        ]
    )

    req = MultiTenantBatchRequest(batch_reference="BATCH-OCT-01", dockets=[inv1, inv2])
    res = MultiTenantDispatcher.dispatch_batch(req)

    assert res.total_dockets == 2
    assert res.successful_clearances == 2
    assert len(res.clearance_bundles) == 2
    assert res.total_processing_time_sec < 2.0

def test_erp_connector_sap_idoc_parsing():
    sample_sap_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <INVOIC02>
        <INV_NUMBER>SAP-998877</INV_NUMBER>
        <EXPORTER_NAME>Kemwell Chemical Industries</EXPORTER_NAME>
        <EXPORTER_IEC>0794556677</EXPORTER_IEC>
        <EXPORTER_GSTIN>29AAACK1122F1Z8</EXPORTER_GSTIN>
        <CONSIGNEE_NAME>BASF SE</CONSIGNEE_NAME>
        <DEST_COUNTRY>DE</DEST_COUNTRY>
        <PORT_OF_LOADING>INBLR4</PORT_OF_LOADING>
        <PORT_OF_DISCHARGE>DEHAM</PORT_OF_DISCHARGE>
        <INCOTERM>CIF</INCOTERM>
        <LINE_ITEMS>
            <LINE_ITEM>
                <ITEM_ID>CHEM-01</ITEM_ID>
                <DESCRIPTION>Organic Esters of Acetic Acid</DESCRIPTION>
                <QUANTITY>500</QUANTITY>
                <UNIT>KGS</UNIT>
                <UNIT_PRICE>40.0</UNIT_PRICE>
                <TOTAL_VALUE>20000.0</TOTAL_VALUE>
                <HS_CODE>29153990</HS_CODE>
                <WEIGHT_KG>500.0</WEIGHT_KG>
            </LINE_ITEM>
        </LINE_ITEMS>
    </INVOIC02>
    """
    invoice = ERPConnector.parse_sap_idoc_xml(sample_sap_xml)
    assert invoice.invoice_number == "SAP-998877"
    assert invoice.exporter_name == "Kemwell Chemical Industries"
    assert invoice.total_amount == 20000.0
    assert len(invoice.items) == 1
    assert invoice.items[0].declared_hs_code == "29153990"
