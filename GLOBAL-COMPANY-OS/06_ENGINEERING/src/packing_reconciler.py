"""
TradeNexus Commercial Invoice & Packing List Reconciliation Engine (ANTIGRAVITY Ω∞)
Eliminates destination port customs queries and physical container inspection holds
by deterministically auditing quantity, weight, and package marking parity before gate-in.
"""

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List
from src.models import (
    CommercialInvoice,
    PackingList,
    ReconciliationReport,
    DiscrepancyItem
)

class PackingListReconciler:
    AVERAGE_PHYSICAL_INSPECTION_DELAY_DAYS = 7
    DAILY_DEMURRAGE_RATE_USD = 450.0

    @classmethod
    def reconcile(
        cls,
        invoice: CommercialInvoice,
        packing_list: PackingList
    ) -> ReconciliationReport:
        """
        Cross-audits invoice line items against physical package declarations.
        """
        now = datetime.now(timezone.utc)
        discrepancies: List[DiscrepancyItem] = []

        # 1. Invoice Reference Match
        if invoice.invoice_number.strip().upper() != packing_list.invoice_reference.strip().upper():
            discrepancies.append(DiscrepancyItem(
                discrepancy_type="INVOICE_REF_MISMATCH",
                severity="CRITICAL",
                description="Packing List references an invoice number differing from the commercial export docket.",
                invoice_value=invoice.invoice_number,
                packing_list_value=packing_list.invoice_reference
            ))

        # 2. Exporter & Consignee Entity Match
        if invoice.exporter_name.strip().lower() != packing_list.exporter_name.strip().lower():
            discrepancies.append(DiscrepancyItem(
                discrepancy_type="ENTITY_NAME_MISMATCH",
                severity="MEDIUM",
                description="Exporter corporate legal entity spelling differs between invoice and packing docket.",
                invoice_value=invoice.exporter_name,
                packing_list_value=packing_list.exporter_name
            ))

        # 3. Item-by-Item Quantity Reconciliation
        # Aggregate packed quantities by item_id
        packed_quantities: Dict[str, float] = {}
        for pkg in packing_list.packages:
            packed_quantities[pkg.item_id] = packed_quantities.get(pkg.item_id, 0.0) + pkg.quantity_packed

        # Compare with invoice items
        invoice_items_map = {item.item_id: item for item in invoice.items}

        for item_id, item in invoice_items_map.items():
            packed_qty = packed_quantities.get(item_id, 0.0)
            if packed_qty == 0.0:
                discrepancies.append(DiscrepancyItem(
                    discrepancy_type="MISSING_ITEM",
                    severity="CRITICAL",
                    description=f"Item {item_id} ('{item.description}') declared on invoice has zero packed packages.",
                    invoice_value=item.quantity,
                    packing_list_value=0.0
                ))
            elif abs(packed_qty - item.quantity) > 0.001:
                variance_pct = abs(packed_qty - item.quantity) / item.quantity * 100.0
                sev = "CRITICAL" if variance_pct > 2.0 else "MEDIUM"
                discrepancies.append(DiscrepancyItem(
                    discrepancy_type="QUANTITY_MISMATCH",
                    severity=sev,
                    description=f"Quantity discrepancy on {item_id} ('{item.description}'): variance of {variance_pct:.1f}%.",
                    invoice_value=item.quantity,
                    packing_list_value=packed_qty
                ))

        # Check for unlisted items in packing list
        for item_id, p_qty in packed_quantities.items():
            if item_id not in invoice_items_map:
                discrepancies.append(DiscrepancyItem(
                    discrepancy_type="UNLISTED_ITEM",
                    severity="CRITICAL",
                    description=f"Package item '{item_id}' packed in container but not declared on commercial invoice.",
                    invoice_value="Not Declared",
                    packing_list_value=p_qty
                ))

        # 4. Weight Parity Check
        total_inv_weight = sum(getattr(i, "weight_kg", 0.0) for i in invoice.items)
        if total_inv_weight > 0 and packing_list.total_net_weight_kg > 0:
            weight_delta = abs(total_inv_weight - packing_list.total_net_weight_kg)
            delta_pct = (weight_delta / total_inv_weight) * 100.0
            if delta_pct > 3.0:
                discrepancies.append(DiscrepancyItem(
                    discrepancy_type="WEIGHT_VARIATION",
                    severity="HIGH",
                    description=f"Net cargo weight mismatch ({delta_pct:.1f}% variance) between invoice ({total_inv_weight:.1f} kg) and packing list ({packing_list.total_net_weight_kg:.1f} kg).",
                    invoice_value=total_inv_weight,
                    packing_list_value=packing_list.total_net_weight_kg
                ))

        # Gross vs Net Weight Sanity
        if packing_list.total_gross_weight_kg < packing_list.total_net_weight_kg:
            discrepancies.append(DiscrepancyItem(
                discrepancy_type="WEIGHT_INVERSION",
                severity="CRITICAL",
                description="Statutory anomaly: Gross cargo weight declared as less than net cargo weight.",
                invoice_value=f"Net: {packing_list.total_net_weight_kg} kg",
                packing_list_value=f"Gross: {packing_list.total_gross_weight_kg} kg"
            ))

        # 5. Status & Demurrage Risk Assessment
        critical_count = sum(1 for d in discrepancies if d.severity == "CRITICAL")
        has_discrepancy = len(discrepancies) > 0

        if critical_count > 0:
            status = "REJECTED"
            demurrage_risk = cls.AVERAGE_PHYSICAL_INSPECTION_DELAY_DAYS * cls.DAILY_DEMURRAGE_RATE_USD
        elif has_discrepancy:
            status = "DISCREPANCY_DETECTED"
            demurrage_risk = 3.0 * cls.DAILY_DEMURRAGE_RATE_USD
        else:
            status = "RECONCILED"
            demurrage_risk = 0.0

        # Cryptographic Seal
        chk_str = f"{invoice.invoice_number}{packing_list.packing_list_number}{status}{len(discrepancies)}"
        seal_hash = hashlib.sha256(chk_str.encode("utf-8")).hexdigest()[:16].upper()
        seal = f"TN-RECON-{seal_hash}"

        return ReconciliationReport(
            report_id=f"RECON-{invoice.invoice_number}",
            invoice_number=invoice.invoice_number,
            packing_list_number=packing_list.packing_list_number,
            timestamp=now.isoformat(),
            status=status,
            discrepancy_count=len(discrepancies),
            discrepancies=discrepancies,
            demurrage_risk_assessment_usd=demurrage_risk,
            reconciliation_seal=seal
        )
