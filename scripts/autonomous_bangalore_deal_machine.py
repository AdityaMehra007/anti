"""
Autonomous Bengaluru Enterprise Deal & CRM Orchestrator
Processes Fortune 500 GCCs and Top Unicorns in Bangalore,
cross-referencing LinkedIn connections, mapping service vectors,
generating cold outreach pipelines, and building an interactive Deal Cockpit.
"""

import csv
import json
import os
import re
from pathlib import Path

BASE_DIR = Path("e:/anti")
COMPANIES_CSV = BASE_DIR / "BANGALORE_5000_COMPANIES_WEBSITES_CAREERS_MASTER.csv"
CONNECTIONS_CSV = BASE_DIR / "linkedin_export/Connections.csv"
OUTPUT_DIR = BASE_DIR / "docs/generated_enterprise_deals"
DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Curated High-Value Target Profiles
FORTUNE_500_GCCS = [
    {"name": "Walmart Global Tech India", "tech_park": "Cessna Business Park, Kadubeesanahalli, ORR", "domain": "Retail Tech, AI Supply Chain & Omnichannel", "vector": "Vendor SLA & SOW Leakage Audit + LLM Eval Harness", "leakage": "Phantom billing across vendor pods and unmonitored ticket SLA rollovers", "annual_leakage": 32000000, "contract_val": 8500000, "entry_po": 485000, "bypass": "Sub-Threshold PO (< INR 5 Lakhs)"},
    {"name": "Target in India (Target Tech)", "tech_park": "Manyata Embassy Business Park, Hebbal", "domain": "Enterprise Cloud & Inventory Forecasting", "vector": "Vendor SLA & SOW Leakage Audit", "leakage": "Uncredited vendor downtime and ghost sprint hours", "annual_leakage": 28000000, "contract_val": 7500000, "entry_po": 480000, "bypass": "Sub-Threshold PO (< INR 5 Lakhs)"},
    {"name": "Goldman Sachs Services (GSC)", "tech_park": "Helios Business Park, Outer Ring Road", "domain": "Global Trade Middle Office & Nostro/Vostro Clearing", "vector": "Automated UCP 600 LC Scrutiny & Nostro Balancer", "leakage": "Manual documentary credit review latency and FX trade breaks", "annual_leakage": 48000000, "contract_val": 12000000, "entry_po": 490000, "bypass": "Retrospective Contingency Audit (25% fee)"},
    {"name": "JPMorgan Chase Global Service Center", "tech_park": "Prestige Tech Park, Marathahalli-Sarjapur ORR", "domain": "Wholesale Payments & Trade Finance Settlement", "vector": "Automated UCP 600 LC Scrutiny & SWIFT Clearing", "leakage": "Documentary discrepancy resolution delays under UCP 600", "annual_leakage": 52000000, "contract_val": 13500000, "entry_po": 490000, "bypass": "Sub-Threshold Discretionary PO"},
    {"name": "Cisco Systems India", "tech_park": "Cessna Business Park, Outer Ring Road", "domain": "Enterprise Networking & Observability AI", "vector": "AI Inference FinOps & LLM Guardrails Testing Harness", "leakage": "Exploding token burn and missing model regression CI/CD", "annual_leakage": 26000000, "contract_val": 9500000, "entry_po": 475000, "bypass": "Tier-1 Empaneled Pass-Through Partner"},
    {"name": "Intel India Technology Center", "tech_park": "SRR Campus, Outer Ring Road, Bellandur", "domain": "Semiconductor CAD, Firmware & AI Accelerator Software", "vector": "Specialized BOT Engineering Pods (Rust & CUDA)", "leakage": "12-month vacancy cycle for specialized distributed systems engineers", "annual_leakage": 35000000, "contract_val": 11000000, "entry_po": 495000, "bypass": "Build-Operate-Transfer (BOT) Pilot SOW"},
    {"name": "Bosch Global Software Technologies (BGSW)", "tech_park": "Adugodi & Electronic City", "domain": "Mobility Tech, IoT & Embedded Automotive AI", "vector": "LLM Evaluation & Agentic Safety Harness", "leakage": "Safety refusal anomalies and prompt drift in automotive diagnostic agents", "annual_leakage": 30000000, "contract_val": 8000000, "entry_po": 485000, "bypass": "Innovation CoE Sandbox Grant"},
    {"name": "Microsoft India Development Center (IDC)", "tech_park": "Prestige Ferns Galaxy, Bellandur, ORR", "domain": "Azure Cloud Infrastructure & Enterprise Copilot Ops", "vector": "AI Eval Benchmarking & Prompt Regression Harness", "leakage": "Model drift across multilingual enterprise copilots in Indian regional dialects", "annual_leakage": 42000000, "contract_val": 12500000, "entry_po": 490000, "bypass": "Discretionary Sub-Threshold PO"},
    {"name": "Google India (Alphabet)", "tech_park": "RMZ Infinity, Old Madras Road & Bagmane Tech Park", "domain": "Global Search AI & Cloud Data Governance", "vector": "Synthetic Data Curation & LLM Reliability Harness", "leakage": "HITL annotation quality bottlenecks and benchmark noise", "annual_leakage": 45000000, "contract_val": 13000000, "entry_po": 495000, "bypass": "Sub-Threshold PO (< $6k USD)"},
    {"name": "Boeing India Engineering & Technology Center (BIETC)", "tech_park": "Aerospace SEZ, Devanahalli", "domain": "Avionics Software, Digital Aviation & Supply Logistics", "vector": "Vendor SOW Leakage Audit & Mission-Critical Code QA", "leakage": "Unverified vendor sprint completions and documentation debt", "annual_leakage": 38000000, "contract_val": 9000000, "entry_po": 490000, "bypass": "Sub-Threshold PO (< INR 5L)"},
    {"name": "Shell Technology Center Bangalore (STCB)", "tech_park": "Shell Tech Park, Devanahalli", "domain": "Energy Transition Analytics & Subsurface Modeling AI", "vector": "Cloud FinOps & Heavy Compute GPU Scheduling", "leakage": "Unused GPU cluster idle time and unoptimized batch pipeline runs", "annual_leakage": 34000000, "contract_val": 8200000, "entry_po": 475000, "bypass": "Contingency Shared-Savings (30%)"},
    {"name": "Dell Technologies India", "tech_park": "Divyasree Greens, Koramangala / Domlur", "domain": "Server Firmware, Edge Computing & Supply Operations", "vector": "Vendor SLA Audit & Hardware Firmware QA Pods", "leakage": "Duplicate vendor milestone billings across legacy systems", "annual_leakage": 25000000, "contract_val": 7000000, "entry_po": 460000, "bypass": "Sub-Threshold PO"},
    {"name": "Wells Fargo Enterprise Global Services", "tech_park": "Embassy TechVillage, Outer Ring Road", "domain": "Commercial Banking Middle Office & Compliance Automation", "vector": "Automated AML Scrutiny & Nostro Break Balancer", "leakage": "Manual OFAC/AML screening false-positive backlogs", "annual_leakage": 39000000, "contract_val": 10500000, "entry_po": 490000, "bypass": "Innovation Lab Sandbox Fund"},
    {"name": "AstraZeneca India Global Operations", "tech_park": "Manyata Embassy Business Park", "domain": "Clinical Trial Data Science & Regulatory Submissions", "vector": "LLM Eval for Clinical Protocol Summarization", "leakage": "Regulatory submission drafting cycle delays and terminology drift", "annual_leakage": 31000000, "contract_val": 8500000, "entry_po": 485000, "bypass": "Sub-Threshold Discretionary PO"},
    {"name": "Standard Chartered Global Business Services", "tech_park": "Prestige Park Square, Bannerghatta Road", "domain": "Trade Finance Operations & Cross-Border Clearing", "vector": "UCP 600 Documentary Credit Discrepancy Engine", "leakage": "Documentary discrepancy dispute delays with issuing banks", "annual_leakage": 41000000, "contract_val": 11500000, "entry_po": 490000, "bypass": "Retrospective Contingency Audit"}
]

TOP_STARTUPS = [
    {"name": "CRED", "tech_park": "100ft Road, Indiranagar", "domain": "FinTech & High-Trust Commerce", "vector": "LLM Inference FinOps & Semantic Caching Layer", "leakage": "High token burn on customer support and concierge agents", "annual_leakage": 18000000, "contract_val": 4500000, "entry_po": 350000, "bypass": "14-Day Zero-Risk Contingency Trial"},
    {"name": "Swiggy", "tech_park": "Embassy TechVillage / Devarabisanahalli, ORR", "domain": "Quick Commerce (Instamart) & Hyperlocal Logistics", "vector": "Founder's Office Tiger Team & Dark Store Routing FinOps", "leakage": "Rider idle latency and quick commerce inventory wastage", "annual_leakage": 24000000, "contract_val": 6500000, "entry_po": 490000, "bypass": "Founder's Office Sprint Mandate"},
    {"name": "Zerodha", "tech_park": "153/154 4th Cross, Dollars Colony, JP Nagar", "domain": "Discount Broking & High-Throughput Capital Markets", "vector": "Deterministic Trade Execution Audits & Low-Latency Infra", "leakage": "Edge-case OMS transaction dropouts during high volatility market open", "annual_leakage": 22000000, "contract_val": 5000000, "entry_po": 400000, "bypass": "14-Day Founder Direct Trial"},
    {"name": "Razorpay", "tech_park": "SJR Cyber, The Forum Mall Area, Koramangala", "domain": "Payment Gateway, Neobanking & International Payroll", "vector": "Autonomous B2B Enterprise Meeting Machine & FX Settlement", "leakage": "High CAC on outbound enterprise acquisition for international payments", "annual_leakage": 35000000, "contract_val": 5500000, "entry_po": 450000, "bypass": "Pay-per-Qualified-Meeting Pilot"},
    {"name": "Zepto", "tech_park": "HSR Layout & Bellandur corridor", "domain": "10-Minute Grocery Delivery & Dark Store Logistics", "vector": "Founder's Office Tiger Team for Dark Store Turnaround", "leakage": "Micro-fulfillment center picking bottlenecks and route delivery variance", "annual_leakage": 20000000, "contract_val": 6000000, "entry_po": 480000, "bypass": "Founder Direct 14-Day Work Trial"},
    {"name": "Postman", "tech_park": "Indiranagar / Koramangala", "domain": "API Platform & Developer Productivity Ecosystem", "vector": "Autonomous B2B Outbound Deal Machine for Fortune 500 GCCs", "leakage": "Untapped enterprise tier expansions inside Bangalore GCC campuses", "annual_leakage": 28000000, "contract_val": 5000000, "entry_po": 450000, "bypass": "Performance Incentive (Pay-per-Meeting)"},
    {"name": "Groww", "tech_park": "Vaishnavi Tech Park, Bellandur, ORR", "domain": "Wealth Management, Mutual Funds & Neobanking", "vector": "LLM Inference Cost Arbitrage & KYC Extraction Pipeline", "leakage": "High OCR and LLM document verification bills on user onboarding", "annual_leakage": 16000000, "contract_val": 4200000, "entry_po": 380000, "bypass": "Contingency Shared-Savings (30%)"},
    {"name": "Meesho", "tech_park": "06-105, Tower A, EGL, Domlur / Koramangala", "domain": "Social Commerce & Tier 2/3 Logistics Optimization", "vector": "Return-to-Origin (RTO) Fraud Detection & FinOps", "leakage": "High logistics RTO leakage and fraudulent returns in Tier 3 clusters", "annual_leakage": 32000000, "contract_val": 7000000, "entry_po": 485000, "bypass": "14-Day Work Trial on RTO Reductions"},
    {"name": "Ather Energy", "tech_park": "IBC Knowledge Park, Bannerghatta Road", "domain": "Electric Vehicles, Battery Telemetry & Fast-Charging Network", "vector": "Founder's Office Special Projects on Charging Grid SLA", "leakage": "Charging station downtime reconciliation and grid integration delays", "annual_leakage": 19000000, "contract_val": 5200000, "entry_po": 450000, "bypass": "Founder's Office Sprint SOW"},
    {"name": "Sarvam AI", "tech_park": "Indiranagar, Bengaluru", "domain": "Sovereign Indic Foundation Models & Enterprise Voice AI", "vector": "Indic LLM Evaluation Harness & Synthetic Benchmark Suite", "leakage": "Lack of automated adversarial guardrails across 10+ Indic languages", "annual_leakage": 25000000, "contract_val": 6000000, "entry_po": 490000, "bypass": "Fast-Track Research Pilot SOW"},
    {"name": "Krutrim (Ola AI)", "tech_park": "Regent Insignia, Koramangala", "domain": "Foundational AI Models & Sovereign Cloud Data Center", "vector": "LLM Eval Harness & Multi-Modal Benchmark Validation", "leakage": "High benchmark error variance and hallucination index on Indic queries", "annual_leakage": 27000000, "contract_val": 6500000, "entry_po": 490000, "bypass": "CoE Pilot Grant"},
    {"name": "InMobi", "tech_park": "Block Delta, Embassy TechSquare, Kadubeesanahalli, ORR", "domain": "AdTech, Mobile Advertising AI & Monetization Platforms", "vector": "Ad Inference Latency Compression & Bot Fraud Detection", "leakage": "Ad request auction latency over 50ms causing bid dropouts", "annual_leakage": 36000000, "contract_val": 7800000, "entry_po": 480000, "bypass": "Contingency Shared-Savings (30%)"},
    {"name": "BrowserStack", "tech_park": "Koramangala / Remote Bangalore Center", "domain": "Cloud Web & Mobile Software Testing Infrastructure", "vector": "Autonomous B2B Outbound Engine Targeting GCC QA Leads", "leakage": "Long procurement lead-times targeting Fortune 500 GCC test leaders", "annual_leakage": 29000000, "contract_val": 5500000, "entry_po": 450000, "bypass": "Pay-per-Meeting Pilot"},
    {"name": "Hasura", "tech_park": "Koramangala, Bengaluru", "domain": "GraphQL Engine & Instant Database APIs", "vector": "Enterprise GCC Architect Outreach & Solution Consulting", "leakage": "Incomplete penetration across Bangalore Fortune 500 GCC backend teams", "annual_leakage": 18000000, "contract_val": 4800000, "entry_po": 420000, "bypass": "Sub-Threshold PO (< INR 5L)"},
    {"name": "Urban Company (Bangalore Tech Hub)", "tech_park": "HSR Layout, Bengaluru", "domain": "On-Demand Home Services & Skilled Gig-Economy Marketplace", "vector": "Service Partner Quality Audit & Fraud Detection Harness", "leakage": "Service partner leakage, off-platform cash circumvention and warranty fraud", "annual_leakage": 21000000, "contract_val": 5200000, "entry_po": 450000, "bypass": "Founder's Office Sprint"}
]

def load_connections():
    conns = []
    if not CONNECTIONS_CSV.exists():
        return conns
    with open(CONNECTIONS_CSV, "r", encoding="utf-8", errors="ignore") as f:
        # Skip notes
        for _ in range(3):
            f.readline()
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Company"):
                conns.append({
                    "name": f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip(),
                    "company": row.get("Company", "").strip(),
                    "position": row.get("Position", "").strip(),
                    "url": row.get("URL", "").strip()
                })
    return conns

def match_connection(company_name, connections):
    matched = []
    comp_clean = re.sub(r"[^a-zA-Z0-9]", "", company_name.lower())
    for c in connections:
        c_clean = re.sub(r"[^a-zA-Z0-9]", "", c["company"].lower())
        if c_clean in comp_clean or comp_clean in c_clean or any(token in c_clean for token in comp_clean.split() if len(token) > 4):
            matched.append(c)
    return matched[:3]

def generate_target_dossier(t, category, connections):
    matched_conns = match_connection(t["name"], connections)
    conn_text = ""
    if matched_conns:
        conn_text = "\n### Matched 1st-Degree LinkedIn Connections:\n"
        for mc in matched_conns:
            conn_text += f"- **{mc['name']}** — {mc['position']} ([LinkedIn Profile]({mc['url']}))\n"
    else:
        conn_text = "\n### Direct Decision Maker Target:\n- VP of Engineering / Operations or Founder's Office Lead.\n"

    roi_x = round(t["annual_leakage"] / t["contract_val"], 1)

    content = f"""# ENTERPRISE COMMERCIAL SPECIFICATION: {t['name'].upper()}
**Sector Category:** {category}  
**Bangalore Campus:** {t['tech_park']}  
**Domain Focus:** {t['domain']}  

---

## 1. Commercial Structure & Economic Metrics
- **Assigned Service Vector:** {t['vector']}
- **Estimated Annual Client Leakage:** INR {t['annual_leakage']:,}
- **Annual Retainer Contract Value:** INR {t['contract_val']:,} (~${t['contract_val'] / 83.5:,.0f} USD)
- **14-Day Sub-Threshold Entry PO:** **INR {t['entry_po']:,}** (~${t['entry_po'] / 83.5:,.0f} USD)
- **Procurement Bypass Rail:** {t['bypass']}
- **Projected Client ROI:** **{roi_x}x Capital Recovery Multiple** within 12 months.

{conn_text}

---

## 2. Identified Operational & Technical Seam
- **Core Leakage Point:** {t['leakage']}
- **Root Cause:** Operational opacity between contracted SOW expectations and live sprint deliverables, or unoptimized prompt architectures causing compute bill runaway.
- **The Trojan Horse Fix:** A self-contained 14-day diagnostic deployment that executes inside the client's secure VPC/sandbox, extracting verifiable proof of recoverable cash or latency gains without disrupting live operations.

---

## 3. High-Converting Cold Outreach Copy

### LinkedIn Executive Direct Message (1st Connection / InMail)
> Hi [First Name],  
>
> Noticed your leadership in scaling {t['domain']} at {t['tech_park'].split(',')[0]}.  
>
> In analyzing similar Bengaluru operations, between 10% and 18% of efficiency leaks through {t['leakage'].lower().split(' and ')[0]}.  
>
> We built a specialized diagnostic harness that identifies and resolves these discrepancies within 14 days. We recently helped a peer team on Outer Ring Road recover over INR 1.2 Cr in uncredited leakage.  
>
> Could I share a 1-page sample audit framework with you this Thursday?  
>
> Best regards,  
> Aditya Mehra  
> Bengaluru, India

### Cold Email (3-Touch Sequence: Touch 1)
> **Subject:** Eliminating {t['domain'].split('&')[0].strip()} leakage at {t['name']}  
>
> Hi [First Name],  
>
> As {t['name']} accelerates its Bengaluru engineering center, one silent financial drain leaders regularly confront is {t['leakage']}.  
>
> We help enterprise leaders eliminate this leakage using our automated diagnostic engine. Rather than requiring a lengthy 6-month global vendor onboarding cycle, we execute a rapid 14-day retrospective diagnostic under discretionary departmental spend (INR {t['entry_po']:,}).  
>
> If our diagnostic identifies less than INR 30 Lakhs in verified operational waste or recovery potential, you owe us nothing.  
>
> Would you be open to reviewing a 1-page sample diagnostic report from a fellow Bengaluru technology center?  
>
> Sincerely,  
> Aditya Mehra  
> Principal Commercial Architect, Bengaluru

---

## 4. Invoicing, Legal & Compliance Specifications
- **Entity Type:** Private Limited / LLP registered in Karnataka.
- **SAC Code:** 998313 (IT Consulting) / 998314 (IT Design & Development).
- **GST Rate:** 18% for domestic invoicing; **0% GST (Export of Services)** with Letter of Undertaking (LUT) if billed to overseas parent entity.
- **SEZ Status:** Eligible for Zero-Rated SEZ invoice endorsement under Section 16 of the IGST Act if located in an SEZ zone.
- **Payment Terms:** 30% advance on SOW signing, 40% on mid-sprint demonstration, 30% upon final sign-off (Net-15 terms).
"""
    return content

def main():
    connections = load_connections()
    print(f"Loaded {len(connections)} LinkedIn connection records.")
    
    crm_records = []
    
    print("\n--- Processing Fortune 500 GCCs ---")
    for t in FORTUNE_500_GCCS:
        dossier_text = generate_target_dossier(t, "Fortune 500 GCC", connections)
        fname = f"{t['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')}_dossier.md"
        fpath = OUTPUT_DIR / fname
        fpath.write_text(dossier_text, encoding="utf-8")
        
        crm_records.append({
            "company": t["name"],
            "type": "Fortune 500 GCC",
            "campus": t["tech_park"],
            "domain": t["domain"],
            "service_vector": t["vector"],
            "contract_inr": t["contract_val"],
            "entry_po_inr": t["entry_po"],
            "est_annual_leakage_inr": t["annual_leakage"],
            "procurement_bypass": t["bypass"],
            "dossier_file": fname
        })
        print(f"  [GCC] {t['name']} -> INR {t['contract_val']:,}")
        
    print("\n--- Processing Top Bangalore Startups & Unicorns ---")
    for t in TOP_STARTUPS:
        dossier_text = generate_target_dossier(t, "Bengaluru Tech Unicorn", connections)
        fname = f"{t['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')}_dossier.md"
        fpath = OUTPUT_DIR / fname
        fpath.write_text(dossier_text, encoding="utf-8")
        
        crm_records.append({
            "company": t["name"],
            "type": "Bengaluru Tech Unicorn",
            "campus": t["tech_park"],
            "domain": t["domain"],
            "service_vector": t["vector"],
            "contract_inr": t["contract_val"],
            "entry_po_inr": t["entry_po"],
            "est_annual_leakage_inr": t["annual_leakage"],
            "procurement_bypass": t["bypass"],
            "dossier_file": fname
        })
        print(f"  [Startup] {t['name']} -> INR {t['contract_val']:,}")
        
    # Save Master CRM JSON & CSV
    json_path = DATA_DIR / "bangalore_enterprise_crm_master.json"
    csv_path = DATA_DIR / "bangalore_enterprise_crm_master.csv"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(crm_records, f, indent=2)
        
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=crm_records[0].keys())
        writer.writeheader()
        writer.writerows(crm_records)
        
    total_pipeline = sum(r["contract_inr"] for r in crm_records)
    print(f"\n==========================================")
    print(f"TOTAL ENTERPRISE CRM PIPELINE VALUE: INR {total_pipeline:,} (~${total_pipeline / 83.5:,.0f} USD)")
    print(f"CRM Database saved to: {json_path} and {csv_path}")
    print(f"Total Individual SOW Dossiers: {len(crm_records)} files in {OUTPUT_DIR}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
