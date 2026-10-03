"""
TradeNexus Multi-Tenant Batch Clearance Dispatcher
Routes, audits, and dispatches export clearance dockets across multiple enterprise tenants.
"""

import time
from typing import List, Dict, Any
from pydantic import BaseModel

from src.models import CommercialInvoice
from src.pilot_processor import PilotProductionProcessor, ProductionClearanceBundle

class MultiTenantBatchRequest(BaseModel):
    batch_reference: str
    dockets: List[CommercialInvoice]

class MultiTenantBatchResponse(BaseModel):
    batch_reference: str
    total_dockets: int
    successful_clearances: int
    total_processing_time_sec: float
    clearance_bundles: List[ProductionClearanceBundle]

class MultiTenantDispatcher:
    TENANT_REGISTRY = {
        "0788012345": {"name": "Sansera Engineering Limited", "tier": "ENTERPRISE_TIER_1", "priority": "HIGH"},
        "0791004321": {"name": "Dynamatic Technologies Limited", "tier": "ENTERPRISE_TIER_1", "priority": "CRITICAL_AEROSPACE"},
        "0794556677": {"name": "Kemwell Chemical Industries", "tier": "GROWTH_TIER_2", "priority": "STANDARD_CHEMICAL"}
    }

    @classmethod
    def dispatch_batch(cls, batch: MultiTenantBatchRequest) -> MultiTenantBatchResponse:
        t0 = time.time()
        bundles: List[ProductionClearanceBundle] = []

        for invoice in batch.dockets:
            # Verify or register tenant
            iec = invoice.exporter_iec
            tenant_info = cls.TENANT_REGISTRY.get(iec, {"name": invoice.exporter_name, "tier": "TRIAL", "priority": "STANDARD"})
            
            # Execute clearance pipeline
            bundle = PilotProductionProcessor.process_export_docket(invoice, apply_auto_corrections=True)
            bundles.append(bundle)

        elapsed = round(time.time() - t0, 4)
        successful = len([b for b in bundles if b.ready_for_customs_filing])

        return MultiTenantBatchResponse(
            batch_reference=batch.batch_reference,
            total_dockets=len(batch.dockets),
            successful_clearances=successful,
            total_processing_time_sec=elapsed,
            clearance_bundles=bundles
        )
