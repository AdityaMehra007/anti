"""
Windmill Production Script: Automated ERP Financial Ledger Reconciliation
==========================================================================
Category: Finance & Enterprise Automation
Language: Python 3.12 / 3.13 (Windmill Native / Docker Worker)

Reconciles client invoices against banking clearing ledgers, detects line-item
discrepancies, tax withholding variances (TDS Section 194C/194J), and flags exceptions.
"""

from typing import Dict, Any, List
import json
import uuid
from datetime import datetime, timezone


def main(
    batch_reference: str = "BATCH-RECON-2026-OCT",
    invoices: List[Dict[str, Any]] = None,
    tolerance_inr: float = 5.0
) -> Dict[str, Any]:
    """
    Process ledger entries, match against settlement corridors, and yield audit report.
    """
    if invoices is None:
        invoices = [
            {"inv_id": "INV-2026-001", "client": "Sansera Engineering", "amount": 720000.0, "settled": 648000.0, "tds_deducted": 72000.0},
            {"inv_id": "INV-2026-002", "client": "Bharat Steel Tubing", "amount": 480000.0, "settled": 432000.0, "tds_deducted": 48000.0},
            {"inv_id": "INV-2026-003", "client": "Peak Form Fitness", "amount": 125000.0, "settled": 125000.0, "tds_deducted": 0.0},
            {"inv_id": "INV-2026-004", "client": "Titan Watch Logistics", "amount": 890000.0, "settled": 801000.0, "tds_deducted": 89000.0}
        ]

    total_billed = sum(i["amount"] for i in invoices)
    total_settled = sum(i["settled"] for i in invoices)
    total_tds = sum(i.get("tds_deducted", 0.0) for i in invoices)

    discrepancies = []
    reconciled_count = 0

    for inv in invoices:
        effective_settlement = inv["settled"] + inv.get("tds_deducted", 0.0)
        diff = abs(inv["amount"] - effective_settlement)
        if diff <= tolerance_inr:
            reconciled_count += 1
        else:
            discrepancies.append({
                "invoice_id": inv["inv_id"],
                "client": inv["client"],
                "billed_amount": inv["amount"],
                "settled_amount": inv["settled"],
                "tds_amount": inv.get("tds_deducted", 0.0),
                "variance": round(inv["amount"] - effective_settlement, 2),
                "severity": "CRITICAL" if diff > 10000 else "WARNING"
            })

    reconciliation_pct = round((reconciled_count / len(invoices)) * 100, 2) if invoices else 100.0

    return {
        "batch_reference": batch_reference,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "total_invoices_audited": len(invoices),
        "reconciled_invoices": reconciled_count,
        "discrepancies_detected": len(discrepancies),
        "reconciliation_rate_pct": reconciliation_pct,
        "total_billed_inr": round(total_billed, 2),
        "total_settled_inr": round(total_settled, 2),
        "total_tds_withheld_inr": round(total_tds, 2),
        "net_unsettled_inr": round(total_billed - total_settled, 2),
        "flagged_discrepancies": discrepancies,
        "audit_verdict": "CLEAN" if len(discrepancies) == 0 else "MANUAL_REVIEW_REQUIRED"
    }


if __name__ == "__main__":
    res = main()
    print(json.dumps(res, indent=2))
