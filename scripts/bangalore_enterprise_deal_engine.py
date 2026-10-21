"""
Bengaluru Enterprise & Unicorn Commercial Deal Engine
Automated generation of enterprise proposals, procurement bypass strategies,
ROI calculators, and cold outreach sequences for Fortune 500 GCCs and top Bangalore startups.
"""

import json
import os
from pathlib import Path

TARGETS = [
    {
        "name": "Walmart Global Tech India",
        "category": "Fortune 500 GCC",
        "campus": "Cessna Business Park, Kadubeesanahalli, Bengaluru",
        "target_persona": "VP of Engineering & Global Vendor Governance Lead",
        "domain": "Retail Tech & Supply Chain AI",
        "deal_type": "Vendor SLA & SOW Leakage Audit + LLM Evaluation Harness",
        "typical_contract_inr": 8500000,
        "entry_po_inr": 485000,
        "procurement_bypass": "Sub-Threshold Discretionary PO (< ₹5 Lakhs) for 14-day diagnostic",
        "leakage_surface": "Phantom billing across 450+ external vendor resources and unmonitored ticket SLA roll-overs",
        "est_annual_leakage_inr": 32000000,
        "pilot_days": 14,
    },
    {
        "name": "Goldman Sachs Global Strategic Center (GSC)",
        "category": "Fortune 500 GCC (Financial)",
        "campus": "Helios Business Park, Outer Ring Road, Bengaluru",
        "target_persona": "Managing Director, Global Trade Operations & Nostro/Vostro Middle Office",
        "domain": "Investment Banking & Cross-Border Clearing",
        "deal_type": "Automated UCP 600 Letter of Credit Scrutiny & Nostro Break Balancer",
        "typical_contract_inr": 12000000,
        "entry_po_inr": 490000,
        "procurement_bypass": "CoE Innovation Sandbox Grant / Retrospective Trade Audit",
        "leakage_surface": "Manual document examination delays (2.5 hrs/LC) causing missed value-dates and FX discrepancy penalties",
        "est_annual_leakage_inr": 48000000,
        "pilot_days": 21,
    },
    {
        "name": "Cisco Systems India",
        "category": "Fortune 500 GCC (Networking/Tech)",
        "campus": "Cessna Business Park, Outer Ring Road, Bengaluru",
        "target_persona": "Director of Cloud Operations & AI Platform Engineering",
        "domain": "Enterprise Cloud & AI Infra",
        "deal_type": "AI Inference FinOps & LLM Guardrails Testing Harness",
        "typical_contract_inr": 9500000,
        "entry_po_inr": 475000,
        "procurement_bypass": "Sub-Threshold PO (< $6k USD) + Pass-Through Tier-1 Partner",
        "leakage_surface": "Unoptimized token burn across internal AI assistant clusters and missing automated eval CI/CD",
        "est_annual_leakage_inr": 28000000,
        "pilot_days": 14,
    },
    {
        "name": "CRED",
        "category": "Bengaluru Unicorn",
        "campus": "Indiranagar, Bengaluru",
        "target_persona": "Founder / CTO / Head of Platform Infrastructure",
        "domain": "FinTech & Premium Member Commerce",
        "deal_type": "LLM Inference Cost Compression & Semantic Caching Layer",
        "typical_contract_inr": 4500000,
        "entry_po_inr": 350000,
        "procurement_bypass": "14-Day Zero-Risk Contingency Trial (30% of verified API cost reduction)",
        "leakage_surface": "High daily token burn on GPT-4/Claude for member assistance and fraud scoring",
        "est_annual_leakage_inr": 18000000,
        "pilot_days": 7,
    },
    {
        "name": "Swiggy",
        "category": "Bengaluru Unicorn / Listed Enterprise",
        "campus": "Marathahalli - Sarjapur Outer Ring Road, Bengaluru",
        "target_persona": "VP of Engineering & Head of Quick Commerce Tech",
        "domain": "Food Delivery, Instamart & Logistics Intelligence",
        "deal_type": "Special Projects Tiger Team & Real-Time Logistics Routing Optimization",
        "typical_contract_inr": 6500000,
        "entry_po_inr": 490000,
        "procurement_bypass": "Founder's Office Direct Sprint Mandate",
        "leakage_surface": "Delivery partner idle latency and unoptimized search cache misses",
        "est_annual_leakage_inr": 24000000,
        "pilot_days": 14,
    },
    {
        "name": "Razorpay",
        "category": "Bengaluru FinTech Unicorn",
        "campus": "SJR Cyber, Koramangala, Bengaluru",
        "target_persona": "Head of Enterprise Merchant Solutions / VP Engineering",
        "domain": "Payment Gateway & Neobanking",
        "deal_type": "Autonomous B2B Enterprise Meeting Machine & Cross-Border Settlement",
        "typical_contract_inr": 5500000,
        "entry_po_inr": 450000,
        "procurement_bypass": "Pay-per-Meeting Pilot + 30-Day Sandbox Module",
        "leakage_surface": "Long enterprise sales cycles for large global cross-border merchant acquisition",
        "est_annual_leakage_inr": 35000000,
        "pilot_days": 14,
    }
]

def generate_deal_dossier(target: dict) -> str:
    roi_multiple = round(target["est_annual_leakage_inr"] / target["typical_contract_inr"], 1)
    
    dossier = f"""# ENTERPRISE DEAL DOSSIER: {target['name'].upper()}
**Classification:** {target['category']} | **Campus:** {target['campus']}
**Target Decision Maker:** {target['target_persona']}
**Domain:** {target['domain']}

---

## 1. Commercial Structure & Economics
- **Core Deal Model:** {target['deal_type']}
- **Full Contract Value (Annualized):** ₹{target['typical_contract_inr']:,} INR (~${target['typical_contract_inr'] / 83.5:,.0f} USD)
- **Initial Entry Sprint (Trojan Horse):** ₹{target['entry_po_inr']:,} INR (~${target['entry_po_inr'] / 83.5:,.0f} USD)
- **Procurement Bypass Mechanism:** {target['procurement_bypass']}
- **Identified Leakage / Friction Surface:** {target['leakage_surface']}
- **Estimated Annual Client Leakage:** ₹{target['est_annual_leakage_inr']:,} INR
- **Projected ROI for Client:** **{roi_multiple}x Return on Investment** within 12 months.

---

## 2. 14-Day Trojan Horse Sprint Roadmap
- **Days 1–4 (Ingestion & Setup):** Deploy containerized agent harness inside client VPC / secure sandbox. Ingest historical logs and establish baseline performance metrics.
- **Days 5–9 (Discrepancy & Performance Audit):** Execute automated scanning and identify exact points of inefficiency, unbilled credits, or latency bottlenecks.
- **Days 10–12 (Synthesis & Validation):** Generate executive report detailing verifiable cash savings or latency drops.
- **Days 13–14 (Executive Presentation & Close):** Deliver the audit report to the {target['target_persona']}. Transition the engagement into the annualized ₹{target['typical_contract_inr']:,} INR retainer.

---

## 3. High-Converting Cold Outreach Copy

### LinkedIn Executive Direct Message (Under 100 words)
> Hi [First Name],  
>
> Noticed your team is scaling the {target['domain']} division at {target['campus'].split(',')[0]}.  
>
> In our audit of similar systems in Bengaluru, between 10% and 18% of efficiency leaks through {target['leakage_surface'].lower().split(' and ')[0]}.  
>
> We built a specialized harness that identifies and resolves these discrepancies within {target['pilot_days']} days. We recently unlocked over ₹1.5 Cr in savings for an enterprise team on Outer Ring Road.  
>
> Could I share a 1-page breakdown of the diagnostic framework with you this Thursday?  
>
> Best regards,  
> Aditya Mehra

### Cold Email (Executive Teardown)
> **Subject:** Eliminating {target['domain']} inefficiencies at {target['name']}  
>
> Hi [First Name],  
>
> As {target['name']} expands its technology leadership from Bengaluru, one quiet operational drain many leaders face is {target['leakage_surface']}.  
>
> We help enterprise leaders eliminate this leakage using our automated diagnostic engine. Rather than requiring a lengthy 6-month vendor onboarding cycle, we execute a rapid {target['pilot_days']}-day retrospective diagnostic under discretionary departmental spend (₹{target['entry_po_inr']:,}).  
>
> If our diagnostic identifies less than ₹50 Lakhs in verified operational waste or recovery potential, there is zero continuing obligation.  
>
> Would you be open to reviewing a redacted sample audit from a fellow Bengaluru enterprise?  
>
> Sincerely,  
> Aditya Mehra  
> Bengaluru, India

---

## 4. Legal, Tax & Invoicing Specifications
- **Entity:** Private Limited / LLP registered in Karnataka.
- **SAC Code:** 998313 (IT Consulting) / 998314 (IT Design & Development).
- **GST Rate:** 18% (domestic supply) OR 0% (Export with Letter of Undertaking if billed to US/EU parent).
- **Payment Milestones:** 30% advance on SOW signature, 40% on mid-sprint demonstration, 30% upon final deliverable sign-off (Net-15 terms).
"""
    return dossier

def main():
    output_dir = Path("e:/anti/docs/generated_enterprise_deals")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating enterprise deal dossiers for {len(TARGETS)} top Bengaluru targets...")
    for target in TARGETS:
        filename = f"{target['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')}_deal_dossier.md"
        filepath = output_dir / filename
        content = generate_deal_dossier(target)
        filepath.write_text(content, encoding="utf-8")
        print(f"Generated: {filepath.name} (Value: INR {target['typical_contract_inr']:,})")
    
    print(f"\nAll dossiers successfully compiled to: {output_dir}")

if __name__ == "__main__":
    main()
