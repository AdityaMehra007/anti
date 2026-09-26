from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class LineItem(BaseModel):
    item_id: str
    description: str
    quantity: float
    unit: str
    unit_price: float
    total_value: float
    currency: str = "USD"
    declared_hs_code: Optional[str] = None
    weight_kg: float

class CommercialInvoice(BaseModel):
    invoice_number: str
    exporter_name: str
    exporter_iec: str # 10-digit DGFT Importer Exporter Code
    exporter_gstin: str
    consignee_name: str
    consignee_country: str
    port_of_loading: str
    port_of_discharge: str
    items: List[LineItem]
    total_amount: float
    incoterm: str = "FOB" # FOB, CIF, CFR, etc.

class AuditResultItem(BaseModel):
    item_id: str
    description: str
    declared_hs_code: Optional[str]
    verified_hs_code: str
    confidence: float
    tariff_rate_percent: float
    cbam_applicable: bool
    scomet_restricted: bool
    status: str # PASS, WARNING, REJECT
    reasoning: str

class ComplianceAuditReport(BaseModel):
    report_id: str
    invoice_number: str
    timestamp: str
    overall_status: str # APPROVED, REQUIRES_REVIEW, REJECTED
    total_risk_score: float # 0.0 (Safe) to 100.0 (Critical)
    items_audited: List[AuditResultItem]
    recommendations: List[str]
    certificate_seal: str

class PackingListPackage(BaseModel):
    package_id: str
    package_type: str = "WOODEN_PALLET" # PALLET, WOODEN_CRATE, CARTON, DRUM
    item_id: str
    quantity_packed: float
    net_weight_kg: float
    gross_weight_kg: float
    dimensions_cm: Optional[str] = "120x80x100"

class PackingList(BaseModel):
    packing_list_number: str
    invoice_reference: str
    exporter_name: str
    consignee_name: str
    total_packages: int
    total_net_weight_kg: float
    total_gross_weight_kg: float
    packages: List[PackingListPackage]

class DiscrepancyItem(BaseModel):
    discrepancy_type: str # QUANTITY_MISMATCH, WEIGHT_VARIATION, MISSING_ITEM, UNLISTED_ITEM
    severity: str # LOW, MEDIUM, CRITICAL
    description: str
    invoice_value: Any
    packing_list_value: Any

class ReconciliationReport(BaseModel):
    report_id: str
    invoice_number: str
    packing_list_number: str
    timestamp: str
    status: str # RECONCILED, DISCREPANCY_DETECTED, REJECTED
    discrepancy_count: int
    discrepancies: List[DiscrepancyItem]
    demurrage_risk_assessment_usd: float
    reconciliation_seal: str

class PackingReconciliationRequest(BaseModel):
    invoice: CommercialInvoice
    packing_list: PackingList

class IntegratedDocketAuditReport(BaseModel):
    report_id: str
    timestamp: str
    invoice_number: str
    packing_list_number: str
    composite_status: str # CLEARED_FOR_ICEGATE, REQUIRES_REVISION, CRITICAL_HOLD
    compliance_status: str
    reconciliation_status: str
    total_demurrage_exposure_usd: float
    recommendations: List[str]
    master_seal: str
    invoice: CommercialInvoice
    packing_list: PackingList
    compliance_audit: ComplianceAuditReport
    packing_reconciliation: ReconciliationReport

class DocketTextRequest(BaseModel):
    raw_docket_text: str




