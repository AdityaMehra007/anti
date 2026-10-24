#!/usr/bin/env python3
"""
========================================================================================
PORTFOLIO PROJECT 3: CROSS-BORDER EXIM CUSTOMS CLEARANCE & INCOTERMS 2020 AUDIT ENGINE
========================================================================================
Author: Aditya Mehra (BBA International Business '26)
Context: Cross-Border Trade Operations & Indian Customs ICEGATE 2.0 Automation
Target Hubs: Air Cargo Complex (BLR) & Nhava Sheva (JNPT) / Chennai Sea Ports
Core Modules:
  1. Customs Duty Mathematical Engine (Assessable Value, BCD, SWS, IGST, Compensation Cess)
  2. Incoterms 2020 Multi-Modal Risk & Cost Obligation Matrix
  3. UCP 600 Letter of Credit (LC) Documentary Discrepancy Validator
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from typing import Dict, List, Any

# Customs Tariff Master Data (Sample High-Tech & Industrial Shipments)
CUSTOMS_TARIFF_MASTER = {
    "8471.30.10": {
        "description": "Portable Digital Automatic Data Processing Machines (Laptops/Servers)",
        "bcd_rate": 0.00,  # ITA-1 Zero Duty Bound
        "sws_rate": 0.10,  # 10% on BCD
        "igst_rate": 0.18,
        "mode_preference": "AIR_CARGO_BLR"
    },
    "8504.40.90": {
        "description": "Static Converters & Industrial Power Supply Modules",
        "bcd_rate": 0.10,  # 10% BCD
        "sws_rate": 0.10,  # 10% of BCD = 1%
        "igst_rate": 0.18,
        "mode_preference": "AIR_CARGO_BLR"
    },
    "8708.29.00": {
        "description": "Components & Accessories of Motor Vehicles",
        "bcd_rate": 0.15,  # 15% BCD
        "sws_rate": 0.10,
        "igst_rate": 0.28,
        "mode_preference": "CHENNAI_SEA_PORT"
    }
}

# Incoming Commercial Consignments for Customs Filing (Bill of Entry)
CONSIGNMENTS = [
    {
        "shipment_id": "SHP-BLR-0941",
        "hs_code": "8471.30.10",
        "fob_value_usd": 120000.0,
        "freight_usd": 4500.0,
        "insurance_usd": 600.0,
        "exchange_rate_inr": 86.50,
        "incoterm": "FCA_SHENZHEN",
        "port_of_entry": "Air Cargo Complex, Bengaluru (BLR)"
    },
    {
        "shipment_id": "SHP-BLR-0942",
        "hs_code": "8504.40.90",
        "fob_value_usd": 45000.0,
        "freight_usd": 2800.0,
        "insurance_usd": 350.0,
        "exchange_rate_inr": 86.50,
        "incoterm": "CIF_CHENNAI",
        "port_of_entry": "Chennai Port (Sea)"
    },
    {
        "shipment_id": "SHP-BLR-0943",
        "hs_code": "8708.29.00",
        "fob_value_usd": 85000.0,
        "freight_usd": 6200.0,
        "insurance_usd": 850.0,
        "exchange_rate_inr": 86.50,
        "incoterm": "EXW_STUTTGART",
        "port_of_entry": "Nhava Sheva (JNPT)"
    }
]

# UCP 600 Letter of Credit (LC) Discrepancy Test Cases
LC_AUDIT_CASES = [
    {
        "lc_number": "LC-HSBC-2026-901",
        "beneficiary": "Apex Robotics Corp (Japan)",
        "documents_presented": ["Commercial Invoice", "Air Waybill (Original)", "Packing List", "Certificate of Origin"],
        "lc_expiry_date": "2026-11-15",
        "presentation_date": "2026-11-02",
        "invoice_amount_usd": 125100.0,
        "lc_credit_usd": 125100.0,
        "partial_shipment_allowed": False,
        "shipped_in_full": True
    },
    {
        "lc_number": "LC-SCB-2026-902",
        "beneficiary": "Precision Tooling AG (Germany)",
        "documents_presented": ["Commercial Invoice", "Ocean Bill of Lading (Copy)", "Packing List"],  # Missing Certificate of Origin & Original BL!
        "lc_expiry_date": "2026-10-25",
        "presentation_date": "2026-10-28",  # Late Presentation!
        "invoice_amount_usd": 92000.0,
        "lc_credit_usd": 90000.0,  # Overdrawing LC!
        "partial_shipment_allowed": False,
        "shipped_in_full": True
    }
]

def calculate_customs_duty(c: Dict[str, Any]) -> Dict[str, Any]:
    tariff = CUSTOMS_TARIFF_MASTER[c["hs_code"]]
    cif_usd = c["fob_value_usd"] + c["freight_usd"] + c["insurance_usd"]
    cif_inr = cif_usd * c["exchange_rate_inr"]

    # In Indian Customs under Section 14, Assessable Value (AV) = CIF Value INR
    assessable_value = cif_inr
    bcd = assessable_value * tariff["bcd_rate"]
    sws = bcd * tariff["sws_rate"]  # Social Welfare Surcharge is 10% of BCD
    igst_base = assessable_value + bcd + sws
    igst = igst_base * tariff["igst_rate"]

    total_duty = bcd + sws + igst
    total_landed_cost = assessable_value + total_duty
    effective_duty_rate = (total_duty / assessable_value) * 100.0

    return {
        "shipment_id": c["shipment_id"],
        "hs_code": c["hs_code"],
        "description": tariff["description"],
        "cif_usd": cif_usd,
        "assessable_value_inr": assessable_value,
        "bcd_inr": bcd,
        "sws_inr": sws,
        "igst_inr": igst,
        "total_duty_inr": total_duty,
        "total_landed_cost_inr": total_landed_cost,
        "effective_duty_pct": effective_duty_rate
    }

def audit_letter_of_credit(case: Dict[str, Any]) -> Dict[str, Any]:
    discrepancies = []
    required_docs = ["Commercial Invoice", "Air Waybill (Original)", "Packing List", "Certificate of Origin"]

    # Check missing docs
    for doc in required_docs:
        if not any(doc in d for d in case["documents_presented"]):
            discrepancies.append(f"Missing mandatory document: '{doc}'")

    # Check presentation timeline
    if case["presentation_date"] > case["lc_expiry_date"]:
        discrepancies.append(f"Late presentation: Presented on {case['presentation_date']} past LC expiry {case['lc_expiry_date']}")

    # Check amount overdrawn
    if case["invoice_amount_usd"] > case["lc_credit_usd"]:
        excess = case["invoice_amount_usd"] - case["lc_credit_usd"]
        discrepancies.append(f"Overdrawn credit: Invoice exceeds LC value by ${excess:,.2f} USD")

    compliant = len(discrepancies) == 0
    return {
        "lc_number": case["lc_number"],
        "compliant": compliant,
        "discrepancies": discrepancies,
        "status": "CLEAN_COMPLIANT" if compliant else "DISCREPANT_REFUSED"
    }

def run_exim_customs_suite():
    print("=" * 102)
    print("  PROJECT 3: CROSS-BORDER EXIM CUSTOMS CLEARANCE & INCOTERMS 2020 AUDIT SUITE")
    print("  Author: Aditya Mehra | Framework: Indian Customs ICEGATE 2.0 & ICC UCP 600 Rules")
    print("=" * 102)

    print(f"\n[+] MODULE 1: ICEGATE 2.0 BILL OF ENTRY DUTY ASSESSMENT LEDGER:")
    print(f"{'Shipment ID':<14} {'HS Code':<12} {'Assessable Val (INR)':<22} {'Total Duty (INR)':<18} {'Eff. Rate':<10} {'Landed Cost (INR)':<18}")
    print("-" * 102)

    total_cif_inr = 0.0
    total_customs_duty = 0.0

    for c in CONSIGNMENTS:
        d = calculate_customs_duty(c)
        total_cif_inr += d["assessable_value_inr"]
        total_customs_duty += d["total_duty_inr"]
        print(f"{d['shipment_id']:<14} {d['hs_code']:<12} ₹{d['assessable_value_inr']:>19,.2f} ₹{d['total_duty_inr']:>15,.2f} {d['effective_duty_pct']:>8.2f}% ₹{d['total_landed_cost_inr']:>16,.2f}")

    print("-" * 102)
    print(f"  • Cumulative Consignment Value  : ₹{total_cif_inr:,.2f}")
    print(f"  • Cumulative Statutory Duty Paid: ₹{total_customs_duty:,.2f} (Avg Effective Rate: {(total_customs_duty/total_cif_inr)*100:.2f}%)")

    print(f"\n[+] MODULE 2: ICC UCP 600 LETTER OF CREDIT (LC) AUDIT:")
    for case in LC_AUDIT_CASES:
        res = audit_letter_of_credit(case)
        print(f"    * LC Reference : {res['lc_number']} -> {res['status']}")
        if res["compliant"]:
            print(f"      Result: Zero Discrepancies. Documents cleared for immediate negotiating bank payout.")
        else:
            for disc in res["discrepancies"]:
                print(f"      [FLAGGED DISCREPANCY]: {disc}")
    print("=" * 102)

if __name__ == "__main__":
    run_exim_customs_suite()
