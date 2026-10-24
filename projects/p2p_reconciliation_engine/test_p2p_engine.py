"""
Unit & Integration Test Suite for P2P Reconciliation Engine
Tests 3-way matching, variance thresholds, late delivery penalties, and metrics calculation.
"""
import os
import sys
import pytest
import sqlite3

sys.path.insert(0, os.path.dirname(__file__))
from engine import P2PReconciliationEngine, PurchaseOrder, GoodsReceiptNote, VendorInvoice


@pytest.fixture
def test_engine():
    # In-memory database for clean test isolation
    engine = P2PReconciliationEngine(":memory:")
    return engine


def test_clean_3way_match(test_engine):
    po = PurchaseOrder("PO-101", "V-1", "Vendor One", "ITEM-A", 10.0, 1000.0, 10000.0, "2026-01-01", "2026-01-10")
    grn = GoodsReceiptNote("GRN-101", "PO-101", 10.0, 10.0, 0.0, "2026-01-09", "Location A")
    inv = VendorInvoice("INV-101", "PO-101", "V-1", 10.0, 1000.0, 10000.0, "2026-01-11")

    test_engine.add_purchase_order(po)
    test_engine.add_grn(grn)
    test_engine.add_invoice(inv)

    result = test_engine.perform_3way_match("PO-101", "INV-101")

    assert result.match_status == "APPROVED"
    assert result.variance_amount == 0.0
    assert result.penalty_amount == 0.0
    assert result.net_payable == 10000.0
    assert "Verified" in result.discrepancy_reason


def test_late_delivery_penalty_deduction(test_engine):
    # Delivery expected 2026-01-05, arrived 2026-01-08 (3 days late)
    po = PurchaseOrder("PO-102", "V-2", "Late Vendor", "ITEM-B", 20.0, 500.0, 10000.0, "2026-01-01", "2026-01-05")
    grn = GoodsReceiptNote("GRN-102", "PO-102", 20.0, 20.0, 0.0, "2026-01-08", "Location B")
    inv = VendorInvoice("INV-102", "PO-102", "V-2", 20.0, 500.0, 10000.0, "2026-01-09")

    test_engine.add_purchase_order(po)
    test_engine.add_grn(grn)
    test_engine.add_invoice(inv)

    # 15% standard SLA penalty
    result = test_engine.perform_3way_match("PO-102", "INV-102", late_penalty_rate_pct=15.0)

    assert result.match_status == "SLA_PENALTY_APPLIED"
    assert result.penalty_amount == 1500.0  # 15% of 10,000
    assert result.net_payable == 8500.0    # 10,000 - 1500
    assert "Late delivery penalty applied" in result.discrepancy_reason


def test_quantity_variance_rejected(test_engine):
    # PO: 50 units. Received: 50, but 10 damaged/rejected -> Accepted: 40. Invoice bills for 50!
    po = PurchaseOrder("PO-103", "V-3", "Short Supply Vendor", "ITEM-C", 50.0, 200.0, 10000.0, "2026-01-01", "2026-01-10")
    grn = GoodsReceiptNote("GRN-103", "PO-103", 50.0, 40.0, 10.0, "2026-01-10", "Location C")
    inv = VendorInvoice("INV-103", "PO-103", "V-3", 50.0, 200.0, 10000.0, "2026-01-10")

    test_engine.add_purchase_order(po)
    test_engine.add_grn(grn)
    test_engine.add_invoice(inv)

    result = test_engine.perform_3way_match("PO-103", "INV-103")

    assert result.match_status == "QTY_VARIANCE"
    # Net payable only based on accepted qty (40 * 200 = 8000)
    assert result.net_payable == 8000.0
    assert "exceeds Accepted GRN Qty" in result.discrepancy_reason


def test_price_variance_detected(test_engine):
    # Contract rate: ₹100/unit. Invoice billed at ₹120/unit.
    po = PurchaseOrder("PO-104", "V-4", "Price Markup Vendor", "ITEM-D", 100.0, 100.0, 10000.0, "2026-01-01", "2026-01-10")
    grn = GoodsReceiptNote("GRN-104", "PO-104", 100.0, 100.0, 0.0, "2026-01-10", "Location D")
    inv = VendorInvoice("INV-104", "PO-104", "V-4", 100.0, 120.0, 12000.0, "2026-01-10")

    test_engine.add_purchase_order(po)
    test_engine.add_grn(grn)
    test_engine.add_invoice(inv)

    result = test_engine.perform_3way_match("PO-104", "INV-104", price_tolerance_pct=0.0)

    assert result.match_status == "PRICE_VARIANCE"
    assert result.variance_amount == 2000.0
    assert "exceeds Contracted Rate" in result.discrepancy_reason


def test_aggregate_summary_metrics(test_engine):
    po1 = PurchaseOrder("PO-01", "V-1", "V1", "IT-1", 10.0, 100.0, 1000.0, "2026-01-01", "2026-01-10")
    grn1 = GoodsReceiptNote("GRN-01", "PO-01", 10.0, 10.0, 0.0, "2026-01-09", "Loc 1")
    inv1 = VendorInvoice("INV-01", "PO-01", "V-1", 10.0, 100.0, 1000.0, "2026-01-10")

    test_engine.add_purchase_order(po1)
    test_engine.add_grn(grn1)
    test_engine.add_invoice(inv1)
    test_engine.perform_3way_match("PO-01", "INV-01")

    metrics = test_engine.get_summary_metrics()
    assert metrics["total_reconciled"] == 1
    assert metrics["total_invoiced_inr"] == 1000.0
    assert metrics["total_payable_inr"] == 1000.0
    assert metrics["match_rate_pct"] == 100.0
