"""
Unit Tests for Global Trade & Customs Compliance Engine
Verifies UCP 600 Letter of Credit rules, tolerance margins, and Indian Customs valuation.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from validator import EximCustomsEngine, LetterOfCredit, PresentationDocuments


@pytest.fixture
def engine():
    return EximCustomsEngine(inr_usd_fx_rate=85.0)


def test_clean_ucp600_presentation(engine):
    lc = LetterOfCredit(
        lc_number="LC-2026-BLR-001",
        issuing_bank="State Bank of India - Overseas Branch",
        beneficiary="Aerospace Avionics GmbH",
        applicant="Hindustan Aeronautics Limited (HAL)",
        lc_amount_usd=100000.0,
        tolerance_pct=5.0,
        expiry_date="2026-06-30",
        latest_shipment_date="2026-06-15",
        port_of_loading="Hamburg Port",
        port_of_discharge="Chennai Port",
        incoterm="CIF"
    )

    docs = PresentationDocuments(
        doc_id="DOC-001",
        lc_number="LC-2026-BLR-001",
        commercial_invoice_amount_usd=102000.0,  # Within +5% tolerance ($95k - $105k)
        invoice_beneficiary="Aerospace Avionics GmbH",
        bill_of_lading_number="BOL-HH-9921",
        shipped_on_board_date="2026-06-10",      # Before latest shipment date
        bol_port_of_loading="Hamburg Port",
        bol_port_of_discharge="Chennai Port",
        is_clean_on_board=True
    )

    # Presented 5 days after shipment (well within 21 days)
    res = engine.verify_ucp600_presentation(lc, docs, presentation_date="2026-06-15")

    assert res.is_compliant is True
    assert res.status == "CLEAN_COMPLIANT"
    assert len(res.discrepancies) == 0
    assert res.max_permitted_drawdown == 105000.0
    assert res.min_permitted_drawdown == 95000.0


def test_ucp600_overdrawn_and_stale_documents(engine):
    lc = LetterOfCredit(
        lc_number="LC-2026-BLR-002",
        issuing_bank="Deutsche Bank Frankfurt",
        beneficiary="Precision Sensors Corp",
        applicant="Tata Advanced Systems",
        lc_amount_usd=50000.0,
        tolerance_pct=5.0,
        expiry_date="2026-07-31",
        latest_shipment_date="2026-07-01",
        port_of_loading="Rotterdam",
        port_of_discharge="Nhava Sheva",
        incoterm="FOB"
    )

    # 1. Invoiced at $55,000 (exceeds $52,500 max tolerance)
    # 2. Presented on July 28 for shipment on July 1 (27 days later -> stale > 21 days)
    # 3. Claused bill of lading
    docs = PresentationDocuments(
        doc_id="DOC-002",
        lc_number="LC-2026-BLR-002",
        commercial_invoice_amount_usd=55000.0,
        invoice_beneficiary="Precision Sensors Corp",
        bill_of_lading_number="BOL-ROT-1142",
        shipped_on_board_date="2026-07-01",
        bol_port_of_loading="Rotterdam",
        bol_port_of_discharge="Nhava Sheva",
        is_clean_on_board=False
    )

    res = engine.verify_ucp600_presentation(lc, docs, presentation_date="2026-07-28")

    assert res.is_compliant is False
    assert res.status == "DISCREPANT"
    assert len(res.discrepancies) >= 3
    discrepancy_text = " ".join(res.discrepancies)
    assert "Overdrawn LC" in discrepancy_text
    assert "Stale Documents" in discrepancy_text
    assert "Claused Transport Document" in discrepancy_text


def test_indian_customs_landed_cost_assessment(engine):
    """
    Evaluates:
    - CIF = $10,000 * 85 = INR 850,000
    - BCD (10%) = INR 85,000
    - SWS (10% of BCD) = INR 8,500
    - IGST Base = 850,000 + 85,000 + 8,500 = 943,500
    - IGST (18%) = 170,000 * 0.999... = INR 169,830.00
    - Total Duty = 85,000 + 8,500 + 169,830 = INR 263,330.00
    - Total Landed = 850,000 + 263,330 = INR 1,113,330.00
    """
    assessment = engine.calculate_indian_customs_duty(
        shipment_id="SHP-IN-9001",
        fob_value_usd=8500.0,
        freight_usd=1200.0,
        insurance_usd=300.0,
        bcd_rate_pct=10.0,
        igst_rate_pct=18.0
    )

    assert assessment.cif_value_inr == 850000.00
    assert assessment.bcd_amount_inr == 85000.00
    assert assessment.sws_amount_inr == 8500.00
    assert assessment.igst_amount_inr == 169830.00
    assert assessment.total_customs_duty_inr == 263330.00
    assert assessment.total_landed_cost_inr == 1113330.00
