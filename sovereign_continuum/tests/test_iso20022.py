"""
Unit tests for ISO 20022 Financial Messaging & Real-Time Gross Settlement (RTGS) Gateway.
"""

import pytest
from sovereign_continuum.banking.iso20022 import (
    ISO20022Gateway,
    PaymentStatus,
    TransferPriority,
    validate_bic,
    validate_iban,
)


def test_bic_validation():
    assert validate_bic("CHASUS33") is True
    assert validate_bic("CHASUS33XXX") is True
    assert validate_bic("CONTUS33XXX") is True
    assert validate_bic("CONTUS33") is True
    assert validate_bic("DEUTDEDD") is True
    # Invalid
    assert validate_bic("SHORT") is False
    assert validate_bic("INVALID_BIC_CODE_TOO_LONG") is False
    assert validate_bic("12345678") is False


def test_iban_validation():
    # Valid sample IBANs (Germany, GB)
    assert validate_iban("DE89370400440532013000") is True
    assert validate_iban("GB82WEST12345698765432") is True
    # Invalid checksum
    assert validate_iban("DE89370400440532013001") is False
    assert validate_iban("INVALID_IBAN") is False
    assert validate_iban("123") is False


def test_pacs008_building_and_xml_serialization():
    gw = ISO20022Gateway(institution_bic="CONTUS33XXX")

    tx = gw.build_pacs008_transfer(
        debtor_name="Acme Industrial Corp",
        debtor_iban="GB82WEST12345698765432",
        debtor_bic="BARCGB22",
        creditor_name="Terra Kinetics Robotics Corp",
        creditor_iban="DE89370400440532013000",
        creditor_bic="DEUTDEDD",
        amount=25_000_000.0,
        currency="USD",
        priority=TransferPriority.HIGH,
    )

    assert tx.amount == 25_000_000.0
    assert tx.currency == "USD"
    assert tx.uetr is not None
    assert tx.status == PaymentStatus.ACTC

    # XML serialization
    xml_data = gw.to_xml(tx)
    assert "<Document" in xml_data
    assert "25000000.00" in xml_data
    assert "BARCGB22" in xml_data
    assert "DEUTDEDD" in xml_data

    # Parse XML back
    parsed = gw.parse_xml_to_dict(xml_data)
    assert parsed["amount"] == 25_000_000.0
    assert parsed["currency"] == "USD"
    assert parsed["debtor_bic"] == "BARCGB22"
    assert parsed["creditor_bic"] == "DEUTDEDD"


def test_pacs009_treasury_transfer():
    gw = ISO20022Gateway(institution_bic="CONTUS33XXX")

    tx = gw.build_pacs009_financial_institution_transfer(
        instructing_agent_bic="CONTUS33XXX",
        instructed_agent_bic="CHASUS33",
        amount=150_000_000.0,
        currency="USD",
    )

    assert tx.message_type == "pacs.009.001.10"
    assert tx.amount == 150_000_000.0
    assert tx.priority == TransferPriority.HIGH


def test_rtgs_settlement_and_camt053():
    gw = ISO20022Gateway(institution_bic="CONTUS33XXX")

    # Set initial balances
    gw.account_balances["BARCGB22"] = 100_000_000.0
    gw.account_balances["DEUTDEDD"] = 50_000_000.0

    tx = gw.build_pacs008_transfer(
        debtor_name="Origin Corp",
        debtor_iban="GB82WEST12345698765432",
        debtor_bic="BARCGB22",
        creditor_name="Destination Ltd",
        creditor_iban="DE89370400440532013000",
        creditor_bic="DEUTDEDD",
        amount=40_000_000.0,
    )

    # Execute RTGS
    res = gw.execute_rtgs_settlement(tx)
    assert res["status"] == "ACCP"
    assert res["debtor_new_balance"] == 60_000_000.0
    assert res["creditor_new_balance"] == 90_000_000.0

    # Insufficient funds test
    large_tx = gw.build_pacs008_transfer(
        debtor_name="Origin Corp",
        debtor_iban="GB82WEST12345698765432",
        debtor_bic="BARCGB22",
        creditor_name="Destination Ltd",
        creditor_iban="DE89370400440532013000",
        creditor_bic="DEUTDEDD",
        amount=100_000_000.0,  # exceeds 60M balance
    )
    res_fail = gw.execute_rtgs_settlement(large_tx)
    assert res_fail["status"] == "RJCT"

    # Statement generation
    camt_barc = gw.generate_camt053_statement("BARCGB22")
    assert camt_barc["closing_available_balance"] == 60_000_000.0
    assert camt_barc["number_of_entries"] == 1
    assert camt_barc["statement_lines"][0]["type"] == "DBIT"
    assert camt_barc["statement_lines"][0]["amount"] == -40_000_000.0
