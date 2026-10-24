"""
ApexFlow Enterprise - Reconciliation Domain Models.
Strict Pydantic schemas adhering to global ISO/EDIFACT P2P procurement standards.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class MatchVerdict(str, Enum):
    EXACT_MATCH = "EXACT_MATCH"
    PRICE_MISMATCH = "PRICE_MISMATCH"
    QUANTITY_MISMATCH = "QUANTITY_MISMATCH"
    MISSING_GRN = "MISSING_GRN"
    MISSING_PO = "MISSING_PO"
    SHRINKAGE_DETECTED = "SHRINKAGE_DETECTED"
    TOTAL_DISCREPANCY = "TOTAL_DISCREPANCY"


class RecommendedAction(str, Enum):
    AUTO_APPROVE = "AUTO_APPROVE"
    HOLD_FOR_REVIEW = "HOLD_FOR_REVIEW"
    REJECT = "REJECT"


class PurchaseOrder(BaseModel):
    po_id: str = Field(..., description="Unique Purchase Order identifier")
    vendor_id: str = Field(..., description="Vendor/Supplier Code")
    sku: str = Field(..., description="Stock Keeping Unit / Material Code")
    quantity_ordered: float = Field(..., gt=0, description="Authorized quantity")
    unit_price: float = Field(..., gt=0, description="Agreed contractual unit price")
    currency: str = Field(default="INR", description="Transaction currency code")

    @property
    def total_expected_cost(self) -> float:
        return round(self.quantity_ordered * self.unit_price, 2)


class GoodsReceipt(BaseModel):
    grn_id: str = Field(..., description="Goods Receipt Note ID")
    po_id: str = Field(..., description="Referenced Purchase Order ID")
    sku: str = Field(..., description="Received SKU")
    quantity_received: float = Field(..., ge=0, description="Physically inspected quantity")
    received_timestamp: str = Field(..., description="ISO 8601 warehouse receipt timestamp")
    inspector_id: str = Field(default="SYSTEM_AUDITOR", description="Auditor/Staff employee ID")


class Invoice(BaseModel):
    invoice_id: str = Field(..., description="Vendor Tax Invoice Number")
    po_id: str = Field(..., description="Referenced Purchase Order ID")
    vendor_id: str = Field(..., description="Supplier Vendor Code")
    sku: str = Field(..., description="Invoiced SKU")
    billed_quantity: float = Field(..., gt=0, description="Billed quantity on invoice")
    billed_unit_price: float = Field(..., gt=0, description="Billed unit price on invoice")
    tax_amount: float = Field(default=0.0, ge=0, description="Applicable GST / VAT")
    
    @property
    def billed_total(self) -> float:
        return round((self.billed_quantity * self.billed_unit_price) + self.tax_amount, 2)


class ToleranceConfig(BaseModel):
    max_price_variance_pct: float = Field(default=0.5, description="Max acceptable price variance % (e.g. 0.5%)")
    max_price_variance_absolute: float = Field(default=10.0, description="Max acceptable flat difference")
    allow_quantity_variance: bool = Field(default=False, description="Strict zero shrinkage requirement")


class ReconciliationResult(BaseModel):
    po_id: str
    vendor_id: str
    sku: str
    verdict: MatchVerdict
    action: RecommendedAction
    variance_pct: float = 0.0
    quantity_diff: float = 0.0
    price_diff: float = 0.0
    financial_exposure: float = 0.0
    audit_notes: str
    reconciled_at: str
