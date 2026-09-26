"""
VECTIS TRADE — Peenya Exporter Outbound Strike Pipeline
Generates personalized zero-risk pilot proposals for Bengaluru manufacturing exporters.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTREACH_DIR = os.path.join(BASE_DIR, "outreach_dockets")
os.makedirs(OUTREACH_DIR, exist_ok=True)

TARGET_EXPORTERS = [
    {
        "id": "EXP-PEENYA-01",
        "company": "Precision Auto Machining Pvt Ltd",
        "location": "Peenya 2nd Stage, Bengaluru",
        "promoter": "Mr. Rajesh Sharma, Managing Director",
        "export_product": "CNC Machined Transmission Flanges Grade 316",
        "destination": "Hamburg, Germany",
        "bank": "Deutsche Bank AG",
        "estimated_monthly_export_eur": 180000
    },
    {
        "id": "EXP-PEENYA-02",
        "company": "Karnataka Valve Fabricators LLP",
        "location": "Peenya 3rd Phase, Bengaluru",
        "promoter": "Mr. K. N. Murthy, Partner",
        "export_product": "High-Pressure Industrial Gate Valves",
        "destination": "Rotterdam, Netherlands",
        "bank": "BNP Paribas",
        "estimated_monthly_export_eur": 145000
    },
    {
        "id": "EXP-PEENYA-03",
        "company": "Southern Aerospace Fasteners Pvt Ltd",
        "location": "Bommasandra Industrial Area, Bengaluru",
        "promoter": "Mr. Vikram Rao, CEO",
        "export_product": "Titanium Aircraft Fasteners & Rivets",
        "destination": "Toulouse, France",
        "bank": "Credit Agricole CIB",
        "estimated_monthly_export_eur": 220000
    },
    {
        "id": "EXP-PEENYA-04",
        "company": "Apex Die Castings & Forgings",
        "location": "Peenya 1st Stage, Bengaluru",
        "promoter": "Mr. Ananth Hegde, Managing Partner",
        "export_product": "Aluminium Die-Cast Gearbox Housings",
        "destination": "Bremen, Germany",
        "bank": "Commerzbank AG",
        "estimated_monthly_export_eur": 110000
    },
    {
        "id": "EXP-PEENYA-05",
        "company": "Bangalore Precision Tools & Dies",
        "location": "Peenya 4th Phase, Bengaluru",
        "promoter": "Mr. S. Chandrashekar, Director",
        "export_product": "Tungsten Carbide Stamping Dies",
        "destination": "Antwerp, Belgium",
        "bank": "KBC Bank",
        "estimated_monthly_export_eur": 95000
    }
]

def generate_proposals():
    print(f"Generating personalized outbound dockets for {len(TARGET_EXPORTERS)} target exporters...")

    for exp in TARGET_EXPORTERS:
        filename = f"{exp['id']}_{exp['company'].replace(' ', '_')}.md"
        filepath = os.path.join(OUTREACH_DIR, filename)

        docket_content = f"""# VECTIS ZERO-RISK TRADE AUDIT DOSSIER
**Target Account**: {exp['company']}  
**Location**: {exp['location']}  
**Primary Decision-Maker**: {exp['promoter']}  
**Product**: {exp['export_product']} -> {exp['destination']}  
**Issuing Bank Profile**: {exp['bank']}  

---

## 1. Direct WhatsApp / Phone Pitch Script
> *"Hello {exp['promoter'].split(',')[0]}, this is Aditya Mehra from VECTIS TRADE here in Bengaluru.*  
> *I saw that {exp['company']} exports {exp['export_product']} to Europe under documentary Letters of Credit.*  
> *We have built an autonomous pre-submission compliance engine calibrated to ICC UCP 600 and ISBP 745 banking rules.*  
> *We know European banks strictly reject shipping dockets over minor typographical differences in description or gross weight rounding, causing €150 refusal fees and 30-day payment delays.*  
> *We would like to audit your next export shipment docket for **zero cost**.*  
> *If your issuing bank accepts your documents with zero discrepancy charges, you pay us ₹1,500 on your subsequent shipments.*  
> *If your bank rejects any document our system certified clean, **we will pay your bank discrepancy penalty out of our own pocket**.*  
> *Can we review your draft documents for your upcoming shipment this week?"*

---

## 2. Customer Economics & Guaranteed Value Capture
- **Shipment Value**: €{exp['estimated_monthly_export_eur']:,} (~₹{exp['estimated_monthly_export_eur'] * 90 / 100000:,.1f} Lakhs)
- **Typical Bank Rejection Fee Avoided**: €150 (~₹13,500)
- **Pre-Shipment Credit Interest Saved (11% p.a. on 45 days delay)**: ~₹{int(exp['estimated_monthly_export_eur'] * 90 * 0.11 * (45/365)):,}
- **Total Immediate Cash Value to Exporter**: ~₹{int(13500 + (exp['estimated_monthly_export_eur'] * 90 * 0.11 * (45/365))):,}
- **VECTIS Fee**: ₹1,500 (Payable only after clean bank acceptance)
- **Net ROI to Customer**: **> 20× Instant ROI**
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(docket_content)
        print(f"Generated proposal docket: {filepath}")

    print(f"\nAll {len(TARGET_EXPORTERS)} outreach dockets generated successfully in {OUTREACH_DIR}")

if __name__ == "__main__":
    generate_proposals()
