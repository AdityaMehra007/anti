"""
Unit Tests for Global EXIM Customs Tariff, UCP 600 Letter of Credit, and Sanctions Screening
"""
import pytest
from projects.omega_global_markets_nexus.core.global_exim_engine import (
    GlobalEximEngine, TradeContract, Incoterm, LetterOfCreditSpec, ShippingDocuments
)


def test_customs_landed_cost_calculation():
    engine = GlobalEximEngine(fx_rate_to_local=85.0)
    contract = TradeContract(
        contract_id="CNT-001",
        exporter_name="Apex Global Technologies",
        exporter_country="United States",
        importer_name="Indo Tech Ltd",
        importer_country="India",
        hs_code="8471.50.00",
        incoterm=Incoterm.CIF,
        cargo_quantity_units=100,
        unit_price_usd=10_000.0,
        freight_usd=15_000.0,
        marine_insurance_usd=5_000.0
    )
    cost = engine.compute_customs_landed_cost(contract)
    assert cost.cif_value_local == (1_000_000.0 + 15_000.0 + 5_000.0) * 85.0
    assert cost.total_landed_cost > cost.cif_value_local
    assert cost.igst_vat_amount > 0


def test_ucp600_compliant_presentation():
    engine = GlobalEximEngine()
    lc = LetterOfCreditSpec(
        lc_reference="LC-100",
        issuing_bank="Standard Chartered",
        applicant="Indo Tech Ltd",
        beneficiary="Apex Global Technologies",
        credit_amount_usd=100_000.0,
        tolerance_pct=5.0,
        expiry_date="2026-12-31",
        latest_shipment_date="2026-11-15",
        port_of_loading="Los Angeles",
        port_of_discharge="Nhava Sheva"
    )
    docs = ShippingDocuments(
        doc_reference="DOC-1",
        invoice_number="INV-100",
        invoice_amount_usd=102_000.0, # Within 5%
        invoice_beneficiary="Apex Global Technologies",
        invoice_applicant="Indo Tech Ltd",
        bill_of_lading_no="BOL-99",
        shipped_on_board_date="2026-10-15",
        bol_port_of_loading="Los Angeles",
        bol_port_of_discharge="Nhava Sheva",
        is_clean_on_board=True
    )
    audit = engine.audit_ucp600_presentation(lc, docs, presentation_date="2026-10-20")
    assert audit["is_compliant"] is True
    assert audit["status"] == "CLEAN_COMPLIANT_FOR_PAYMENT"


def test_ucp600_discrepant_presentation():
    engine = GlobalEximEngine()
    lc = LetterOfCreditSpec(
        lc_reference="LC-100",
        issuing_bank="Standard Chartered",
        applicant="Indo Tech Ltd",
        beneficiary="Apex Global Technologies",
        credit_amount_usd=100_000.0,
        tolerance_pct=5.0,
        expiry_date="2026-12-31",
        latest_shipment_date="2026-11-15",
        port_of_loading="Los Angeles",
        port_of_discharge="Nhava Sheva"
    )
    docs = ShippingDocuments(
        doc_reference="DOC-1",
        invoice_number="INV-100",
        invoice_amount_usd=120_000.0, # 20% over budget -> Discrepant
        invoice_beneficiary="Apex Global Technologies",
        invoice_applicant="Indo Tech Ltd",
        bill_of_lading_no="BOL-99",
        shipped_on_board_date="2026-11-20", # Late shipment
        bol_port_of_loading="Los Angeles",
        bol_port_of_discharge="Nhava Sheva",
        is_clean_on_board=False # Claused
    )
    audit = engine.audit_ucp600_presentation(lc, docs, presentation_date="2026-12-25")
    assert audit["is_compliant"] is False
    assert audit["discrepancies_count"] >= 3


def test_cirp_fx_forward():
    engine = GlobalEximEngine()
    fwd = engine.price_fx_forward_hedge(spot_rate=85.0, domestic_rate_pct=6.5, foreign_rate_pct=5.0, tenor_days=90)
    assert fwd["forward_rate"] > 85.0


def test_sanctions_screening():
    engine = GlobalEximEngine()
    # Clean entity
    clean_res = engine.screen_sanctions_and_embargo(
        "Apex Global", "United States", "Indo Tech", "India", "Consumer Electronics"
    )
    assert clean_res["cleared_for_export"] is True

    # Sanctioned entity
    sanctioned_res = engine.screen_sanctions_and_embargo(
        "GLOBAL_SHADOW_SHIPPING_LTD", "Panama", "Indo Tech", "North Korea", "Centrifuge parts"
    )
    assert sanctioned_res["cleared_for_export"] is False
    assert sanctioned_res["violations_count"] >= 2
