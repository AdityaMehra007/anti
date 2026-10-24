"""Tests for ApexFlow 3-Way Reconciliation Engine."""

import pytest
from projects.apex_enterprise_orchestrator.reconciliation.matcher import ThreeWayMatcher
from projects.apex_enterprise_orchestrator.reconciliation.models import (
    GoodsReceipt,
    Invoice,
    MatchVerdict,
    PurchaseOrder,
    RecommendedAction,
    ToleranceConfig,
)


def test_exact_three_way_match():
    matcher = ThreeWayMatcher()
    po = PurchaseOrder(po_id="PO-001", vendor_id="VEND-01", sku="SKU-100", quantity_ordered=50, unit_price=200.0)
    grn = GoodsReceipt(grn_id="GRN-001", po_id="PO-001", sku="SKU-100", quantity_received=50, received_timestamp="2026-10-21T08:00:00Z")
    inv = Invoice(invoice_id="INV-001", po_id="PO-001", vendor_id="VEND-01", sku="SKU-100", billed_quantity=50, billed_unit_price=200.0)

    result = matcher.reconcile(po=po, grn=grn, invoice=inv)
    assert result.verdict == MatchVerdict.EXACT_MATCH
    assert result.action == RecommendedAction.AUTO_APPROVE
    assert result.financial_exposure == 0.0


def test_quantity_mismatch_overbilling():
    matcher = ThreeWayMatcher()
    po = PurchaseOrder(po_id="PO-002", vendor_id="VEND-01", sku="SKU-100", quantity_ordered=50, unit_price=100.0)
    grn = GoodsReceipt(grn_id="GRN-002", po_id="PO-002", sku="SKU-100", quantity_received=50, received_timestamp="2026-10-21T08:00:00Z")
    # Vendor billed 60 units instead of 50 received
    inv = Invoice(invoice_id="INV-002", po_id="PO-002", vendor_id="VEND-01", sku="SKU-100", billed_quantity=60, billed_unit_price=100.0)

    result = matcher.reconcile(po=po, grn=grn, invoice=inv)
    assert result.verdict == MatchVerdict.QUANTITY_MISMATCH
    assert result.action == RecommendedAction.REJECT
    assert result.quantity_diff == 10.0
    assert result.financial_exposure == 1000.0  # 10 excess * 100


def test_price_mismatch_tolerance_exceeded():
    matcher = ThreeWayMatcher(tolerance=ToleranceConfig(max_price_variance_pct=0.5, max_price_variance_absolute=5.0))
    po = PurchaseOrder(po_id="PO-003", vendor_id="VEND-01", sku="SKU-100", quantity_ordered=100, unit_price=100.0)
    grn = GoodsReceipt(grn_id="GRN-003", po_id="PO-003", sku="SKU-100", quantity_received=100, received_timestamp="2026-10-21T08:00:00Z")
    # Vendor billed 110 unit price (+10% overage)
    inv = Invoice(invoice_id="INV-003", po_id="PO-003", vendor_id="VEND-01", sku="SKU-100", billed_quantity=100, billed_unit_price=110.0)

    result = matcher.reconcile(po=po, grn=grn, invoice=inv)
    assert result.verdict == MatchVerdict.PRICE_MISMATCH
    assert result.action == RecommendedAction.HOLD_FOR_REVIEW
    assert result.price_diff == 10.0
    assert result.variance_pct == 10.0
    assert result.financial_exposure == 1000.0


def test_missing_grn_holds_invoice():
    matcher = ThreeWayMatcher()
    po = PurchaseOrder(po_id="PO-004", vendor_id="VEND-01", sku="SKU-100", quantity_ordered=25, unit_price=400.0)
    inv = Invoice(invoice_id="INV-004", po_id="PO-004", vendor_id="VEND-01", sku="SKU-100", billed_quantity=25, billed_unit_price=400.0)

    # GRN is None (goods not received in warehouse)
    result = matcher.reconcile(po=po, grn=None, invoice=inv)
    assert result.verdict == MatchVerdict.MISSING_GRN
    assert result.action == RecommendedAction.HOLD_FOR_REVIEW
    assert result.financial_exposure == 10000.0
