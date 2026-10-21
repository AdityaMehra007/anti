"""
Bengaluru Trade Finance & Letter of Credit (LC) Scrutiny Harness
Validates documentary credit presentation documents under ICC UCP 600
and ISBP 745 international trade rules within 30 seconds.
"""

from datetime import datetime

SAMPLE_DOCUMENTARY_PRESENTATION = {
    "lc_number": "LC-2026-GS-BLR-9041",
    "issuing_bank": "Goldman Sachs International / JPMC",
    "beneficiary": "Precision Tech Exports Ltd, Bengaluru",
    "lc_amount_usd": 750000.00,
    "invoice_amount_usd": 750000.00,
    "expiry_date": "2026-11-15",
    "latest_shipment_date": "2026-10-31",
    "actual_bill_of_lading_date": "2026-11-02",  # Late shipment violation!
    "port_of_loading_lc": "Chennai / JNPT, India",
    "port_of_loading_bl": "Chennai, India",
    "partial_shipment_allowed": False,
    "is_partial_shipment": False,
    "description_of_goods_lc": "10,000 units of Industrial Micro-Controllers Model X7",
    "description_of_goods_invoice": "10,000 units of Industrial Micro-Controllers Model X7",
    "description_of_goods_bl": "Industrial Micro-Controllers Model X7"
}

def scrutinize_letter_of_credit(doc):
    discrepancies = []
    
    # Check 1: Late Shipment (UCP 600 Article 31)
    bl_date = datetime.strptime(doc["actual_bill_of_lading_date"], "%Y-%m-%d")
    latest_shipment = datetime.strptime(doc["latest_shipment_date"], "%Y-%m-%d")
    if bl_date > latest_shipment:
        discrepancies.append({
            "rule": "UCP 600 Art. 31 / ISBP 745 A11",
            "severity": "CRITICAL_FATAL",
            "description": f"Late shipment: B/L dated {doc['actual_bill_of_lading_date']} exceeds LC latest shipment date {doc['latest_shipment_date']}."
        })
        
    # Check 2: Expiry vs Presentation Date
    expiry = datetime.strptime(doc["expiry_date"], "%Y-%m-%d")
    if bl_date > expiry:
        discrepancies.append({
            "rule": "UCP 600 Art. 6",
            "severity": "CRITICAL_FATAL",
            "description": "Presentation after LC expiry date."
        })
        
    # Check 3: Invoice Amount vs LC Amount (UCP 600 Art. 18b)
    if doc["invoice_amount_usd"] > doc["lc_amount_usd"]:
        discrepancies.append({
            "rule": "UCP 600 Art. 18b",
            "severity": "CRITICAL_FATAL",
            "description": f"Commercial invoice amount (${doc['invoice_amount_usd']:,.2f}) exceeds credit amount (${doc['lc_amount_usd']:,.2f})."
        })
        
    # Check 4: Unauthorized Partial Shipment (UCP 600 Art. 31)
    if not doc["partial_shipment_allowed"] and doc["is_partial_shipment"]:
        discrepancies.append({
            "rule": "UCP 600 Art. 31",
            "severity": "CRITICAL_FATAL",
            "description": "Partial shipment effected when expressly prohibited in Credit field 43P."
        })
        
    # Check 5: Description of Goods Consistency (UCP 600 Art. 18c)
    if doc["description_of_goods_lc"].lower() != doc["description_of_goods_invoice"].lower():
        discrepancies.append({
            "rule": "UCP 600 Art. 18c",
            "severity": "MAJOR_DISCREPANCY",
            "description": "Description of goods in commercial invoice does not correspond precisely with that in Credit field 45A."
        })
        
    status = "COMPLIANT_CLEAN" if len(discrepancies) == 0 else "DISCREPANT_REFUSAL_NOTICE_REQUIRED"
    
    return {
        "lc_number": doc["lc_number"],
        "status": status,
        "discrepancy_count": len(discrepancies),
        "discrepancies": discrepancies,
        "swift_action": "ISSUE_MT734_REFUSAL" if discrepancies else "ISSUE_MT752_AUTHORIZATION"
    }

if __name__ == "__main__":
    result = scrutinize_letter_of_credit(SAMPLE_DOCUMENTARY_PRESENTATION)
    print("=== BENGALURU TRADE FINANCE UCP 600 SCRUTINY REPORT ===")
    print(f"LC Number: {result['lc_number']}")
    print(f"Presentation Status: {result['status']}")
    print(f"Total Discrepancies Flagged: {result['discrepancy_count']}")
    for d in result["discrepancies"]:
        print(f"  • [{d['severity']}] {d['rule']}: {d['description']}")
    print(f"Recommended SWIFT Message: {result['swift_action']}")
