"""
Demonstration Cases for EXIM & Customs Validator
Runs batch audit of real-world import/export shipments and generates summary ledger.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from validator import EximCustomsEngine, LetterOfCredit, PresentationDocuments

def run_demonstration():
    engine = EximCustomsEngine(inr_usd_fx_rate=85.0)

    shipments = [
        {
            "name": "Avionics Navigation Systems (HAL Bengaluru)",
            "lc": LetterOfCredit("LC-IND-2026-01", "SBI Overseas Branch", "Thales Avionics SA", "HAL Bengaluru", 250000.0, 5.0, "2026-08-31", "2026-08-15", "Le Havre", "Chennai Port", "CIF"),
            "docs": PresentationDocuments("DOC-01", "LC-IND-2026-01", 248000.0, "Thales Avionics SA", "BOL-TH-4412", "2026-08-10", "Le Havre", "Chennai Port", True),
            "pres_date": "2026-08-18",
            "fob": 230000.0, "freight": 15000.0, "ins": 3000.0, "bcd": 7.5, "igst": 18.0
        },
        {
            "name": "Precision Machine Tooling (Puma Manufacturing Hub)",
            "lc": LetterOfCredit("LC-IND-2026-02", "Deutsche Bank AG", "Kuka Robotics DE", "Puma India Logistics", 120000.0, 5.0, "2026-09-15", "2026-09-01", "Hamburg", "Nhava Sheva", "FOB"),
            "docs": PresentationDocuments("DOC-02", "LC-IND-2026-02", 132000.0, "Kuka Robotics DE", "BOL-KU-9981", "2026-09-01", "Hamburg", "Nhava Sheva", True),
            "pres_date": "2026-09-05",
            "fob": 120000.0, "freight": 8000.0, "ins": 1500.0, "bcd": 10.0, "igst": 18.0
        },
        {
            "name": "Commercial Display Structures (Aero India Pavilions)",
            "lc": LetterOfCredit("LC-IND-2026-03", "Standard Chartered Dubai", "Alumex International FZE", "Salt In My Coca / Aero Ops", 80000.0, 5.0, "2026-02-10", "2026-01-25", "Jebel Ali", "Mangalore Port", "CIF"),
            "docs": PresentationDocuments("DOC-03", "LC-IND-2026-03", 79500.0, "Alumex International FZE", "BOL-DXB-108", "2026-01-24", "Jebel Ali", "Mangalore Port", True),
            "pres_date": "2026-01-28",
            "fob": 72000.0, "freight": 6500.0, "ins": 1000.0, "bcd": 10.0, "igst": 18.0
        }
    ]

    results = []
    print("\n=== GLOBAL TRADE & CUSTOMS COMPLIANCE AUDIT BATCH ===")
    for item in shipments:
        comp = engine.verify_ucp600_presentation(item["lc"], item["docs"], item["pres_date"])
        cust = engine.calculate_indian_customs_duty(
            shipment_id=item["docs"].doc_id,
            fob_value_usd=item["fob"],
            freight_usd=item["freight"],
            insurance_usd=item["ins"],
            bcd_rate_pct=item["bcd"],
            igst_rate_pct=item["igst"]
        )
        results.append({"meta": item, "compliance": comp, "customs": cust})
        print(f"[*] Shipment: {item['name']}")
        print(f"    UCP 600 Status: {comp.status} | Compliant: {comp.is_compliant}")
        if comp.discrepancies:
            print(f"    Discrepancies: {', '.join(comp.discrepancies)}")
        print(f"    Assessable CIF: INR {cust.cif_value_inr:,.2f} | Total Duty: INR {cust.total_customs_duty_inr:,.2f}")
        print(f"    Total Landed Cost: INR {cust.total_landed_cost_inr:,.2f}\n")

    return results

if __name__ == "__main__":
    run_demonstration()
