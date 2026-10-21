"""
Scale Bangalore Enterprise CRM to 500+ Accounts (Startups & Fortune 500 GCCs).
Integrates:
  1. Bangalore Top 500 Startups Master DB
  2. Bangalore Fortune 500 Global Capability Centers (GCCs)
  3. 8,215 LinkedIn Connections for Warm Referral Anchoring
  4. 7 High-Margin Commercial Service Vectors & Sub-Threshold (< INR 5L) Entry POs
"""

import csv
import json
import os
import re
from pathlib import Path

BASE_DIR = Path("E:/anti")
STARTUPS_JSON = BASE_DIR / "data/BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json"
CONNECTIONS_CSV = BASE_DIR / "linkedin_export/Connections.csv"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "docs/contracts_and_sows"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 7 Battle-Tested High-Margin Monetization Models
SERVICE_VECTORS = [
    {
        "vector": "Enterprise LLM Evaluation, Adversarial Red-Teaming & Guardrail Harness",
        "leakage": "PII leakage risk, benchmark noise, and unverified hallucinations stalling enterprise AI rollout",
        "contract_val": 8500000,
        "entry_po": 485000,
        "bypass": "Sub-Threshold PO (< INR 5L)",
        "annual_leakage": 32000000
    },
    {
        "vector": "GCC Vendor SLA & SOW Leakage Audit & Recovery",
        "leakage": "Phantom billing across vendor pods, ghost sprint hours, and uncredited vendor SLA breaches",
        "contract_val": 7500000,
        "entry_po": 480000,
        "bypass": "Contingency Shared-Savings (25%)",
        "annual_leakage": 28000000
    },
    {
        "vector": "Automated UCP 600 Trade Finance & Nostro Balance Reconciliation",
        "leakage": "Manual documentary discrepancy resolution delays and Nostro/Vostro multi-currency FX breaks",
        "contract_val": 12000000,
        "entry_po": 490000,
        "bypass": "Sub-Threshold Discretionary PO",
        "annual_leakage": 48000000
    },
    {
        "vector": "Founder's Office & CXO Tiger Team on Demand",
        "leakage": "Bandwidth deficit in C-Suite, delayed zero-to-one special projects, and operational drag",
        "contract_val": 6500000,
        "entry_po": 490000,
        "bypass": "Founder Direct 14-Day Sprint Mandate",
        "annual_leakage": 24000000
    },
    {
        "vector": "Autonomous B2B Outbound Deal Machine & Pipeline Engine",
        "leakage": "High outbound CAC, cold outbound deliverability failures, and slow enterprise pipeline growth",
        "contract_val": 5500000,
        "entry_po": 450000,
        "bypass": "Pay-per-Qualified-Meeting Pilot",
        "annual_leakage": 22000000
    },
    {
        "vector": "Cloud & LLM Inference FinOps (Compute Cost Arbitrage)",
        "leakage": "Unoptimized token burn, redundant embedding lookups, and GPU cluster idle time",
        "contract_val": 6000000,
        "entry_po": 420000,
        "bypass": "Contingency Shared-Savings (30%)",
        "annual_leakage": 25000000
    },
    {
        "vector": "Specialized Build-Operate-Transfer (BOT) Engineering Pods",
        "leakage": "6 to 9-month vacancy lead times for specialized low-latency Rust/eBPF/CUDA engineers",
        "contract_val": 11000000,
        "entry_po": 495000,
        "bypass": "Build-Operate-Transfer (BOT) SOW",
        "annual_leakage": 38000000
    }
]

# Top Fortune 500 GCCs in Bengaluru
FORTUNE_500_GCCS = [
    ("Walmart Global Tech India", "Cessna Business Park, Kadubeesanahalli, ORR", "Retail Tech, AI Supply Chain & Omnichannel", 0),
    ("Target in India (Target Tech)", "Manyata Embassy Business Park, Hebbal", "Enterprise Cloud & Inventory Forecasting", 1),
    ("Goldman Sachs Services (GSC)", "Helios Business Park, Outer Ring Road", "Global Trade Middle Office & Nostro/Vostro Clearing", 2),
    ("JPMorgan Chase Global Service Center", "Prestige Tech Park, Marathahalli-Sarjapur ORR", "Wholesale Payments & Trade Finance Settlement", 2),
    ("Cisco Systems India", "Cessna Business Park, Outer Ring Road", "Enterprise Networking & Observability AI", 0),
    ("Intel India Technology Center", "SRR Campus, Outer Ring Road, Bellandur", "Semiconductor CAD, Firmware & AI Accelerator Software", 6),
    ("Bosch Global Software Technologies (BGSW)", "Adugodi & Electronic City", "Mobility Tech, IoT & Embedded Automotive AI", 0),
    ("Microsoft India Development Center (IDC)", "Prestige Ferns Galaxy, Bellandur, ORR", "Azure Cloud Infrastructure & Enterprise Copilot Ops", 0),
    ("Google India (Alphabet)", "RMZ Infinity, Old Madras Road & Bagmane Tech Park", "Global Search AI & Cloud Data Governance", 0),
    ("Boeing India Engineering & Technology Center", "Aerospace SEZ, Devanahalli", "Avionics Software, Digital Aviation & Supply Logistics", 1),
    ("Shell Technology Center Bangalore (STCB)", "Shell Tech Park, Devanahalli", "Energy Transition Analytics & Subsurface Modeling AI", 5),
    ("Dell Technologies India", "Divyasree Greens, Koramangala / Domlur", "Server Firmware, Edge Computing & Supply Operations", 1),
    ("Wells Fargo Enterprise Global Services", "Embassy TechVillage, Outer Ring Road", "Commercial Banking Middle Office & Compliance Automation", 2),
    ("AstraZeneca India Global Operations", "Manyata Embassy Business Park", "Clinical Trial Data Science & Regulatory Submissions", 0),
    ("Standard Chartered Global Business Services", "Prestige Park Square, Bannerghatta Road", "Trade Finance Operations & Cross-Border Clearing", 2),
    ("Morgan Stanley Advantage Services", "Prestige Trade Tower, Palace Road", "Institutional Equity Algorithmic Execution Systems", 2),
    ("HSBC Electronic Data Processing India", "Prestige Shantiniketan, Whitefield", "Global Commercial Banking Settlement & Swift Rail", 2),
    ("Deutsche Bank CIB Center", "Prestige Tech Park, Outer Ring Road", "Corporate Bank Clearing & Custody Infrastructure", 2),
    ("Fidelity Investments India", "Embassy GolfLinks, Domlur / Koramangala", "Wealth Advisory Platform & Asset Management Cloud", 1),
    ("Honeywell Technology Solutions", "Devarabisanahalli, Outer Ring Road", "Industrial Automation, Aerospace Avionics & Edge IoT", 6),
    ("SAP Labs India", "EPIP Zone, Whitefield", "Enterprise ERP Core & Supply Chain Cloud", 0),
    ("Schneider Electric India R&D", "Prestige Tech Park, Bellandur", "Smart Grid Energy Management & Industrial IoT", 5),
    ("Siemens Technology India", "Electronic City Phase 1", "Medical Imaging, Industrial Automation & Digital Twin", 6),
    ("Novartis Healthcare Corporate", "Outer Ring Road, Kadubeesanahalli", "Biomedical Data Engineering & Global Regulatory AI", 0),
    ("American Express India", "Prestige Technostar, Brookefield, Whitefield", "Global Risk Scoring, Merchant Settlement & Fraud AI", 2),
    ("Citigroup Global Services", "Manyata Embassy Business Park", "Treasury & Trade Solutions Middle Office", 2),
    ("Mercedes-Benz R&D India (MBRDI)", "Whitefield & Manyata Business Park", "Autonomous Driving Stack & Connected Telematics", 6),
    ("Volvo Group Connected Solutions", "Bagmane Tech Park, CV Raman Nagar", "Commercial Vehicle Fleet Telemetry & Battery BMS", 5),
    ("Qualcomm India", "Bagmane Constellation Business Park, Marathahalli", "Modem DSP Firmware & Neural Processing Edge SDK", 6),
    ("Applied Materials India", "Whitefield & ITPL", "Semiconductor Process Diagnostics & Metrology Algorithms", 6),
    ("Oracle India Development Center", "Prestige Technology Park, Marathahalli ORR", "Autonomous Database Kernel & Cloud Infrastructure", 5),
    ("IBM India Systems & Cloud", "Manyata Embassy Business Park", "Enterprise Hybrid Cloud & Mainframe AI Modernization", 1),
    ("Salesforce India", "Bagmane Capital, Doddanekkundi, ORR", "CRM Einstein AI Platform & Distributed Data Cloud", 0),
    ("Adobe India Systems", "Prestige Platina, Marathahalli Ring Road", "Creative Cloud Generative AI & Digital Experience", 0),
    ("Texas Instruments India", "Bagmane Tech Park, CV Raman Nagar", "Embedded DSP Microcontrollers & Analog Sensor Arrays", 6),
    ("Broadcom India", "Prestige Tech Cloud, Devanahalli", "Optical Network Switch Silicon & Data Center Fabrics", 6),
    ("Nike Technology India", "Embassy TechVillage, ORR", "Digital Commerce Personalization & Demand Forecasting", 4),
    ("Lowe's India (Lowe's Tech)", "Manyata Embassy Business Park", "Home Improvement Omnichannel & Autonomous Inventory", 1),
    ("Tesco Bengaluru Tech", "Prestige Shantiniketan, Whitefield", "Retail Supermarket Chain Optimization & Micro-Logistics", 1),
    ("Optum Global Solutions (UnitedHealth)", "Manyata Embassy Business Park", "Healthcare Claim Adjudication & Clinical Knowledge Graphs", 0),
    ("MetLife Global Operations Support", "Prestige Tech Park, ORR", "Actuarial Risk Modeling & Life Insurance Automation", 1),
    ("Prudential Global Services", "Manyata Business Park, Hebbal", "Retirement Portfolio Wealth Core & Annuity Processing", 1),
    ("Barclays Global Service Centre", "Prestige Shantiniketan, Whitefield", "Investment Banking Syndication & Capital Markets Core", 2),
    ("BNY Mellon Technology India", "Embassy TechZone, Outer Ring Road", "Global Custody Clearing & Securities Settlement Rails", 2),
    ("State Street Global Advisors India", "Prestige Tech Park, Marathahalli", "Quantitative Multi-Asset Portfolio Balancing", 2),
    ("UBS Business Solutions India", "Prestige Tech Park, Bellandur", "Wealth Management Client Lifecycle & Prime Brokerage", 2)
]

def load_connections():
    conns = []
    if not CONNECTIONS_CSV.exists():
        return conns
    with open(CONNECTIONS_CSV, "r", encoding="utf-8", errors="ignore") as f:
        for _ in range(3):
            f.readline()
        reader = csv.DictReader(f)
        for r in reader:
            fn = r.get("First Name", "").strip()
            ln = r.get("Last Name", "").strip()
            co = r.get("Company", "").strip()
            pos = r.get("Position", "").strip()
            if fn and co:
                conns.append({
                    "name": f"{fn} {ln}".strip(),
                    "company": co,
                    "position": pos
                })
    return conns

def match_connections(company_name, conns):
    norm_target = re.sub(r'[^a-z0-9]', '', company_name.lower())
    matches = []
    for c in conns:
        norm_co = re.sub(r'[^a-z0-9]', '', c["company"].lower())
        if norm_target in norm_co or norm_co in norm_target:
            matches.append(c)
        elif any(part in norm_co for part in norm_target.split() if len(part) > 4):
            matches.append(c)
    return matches[:4]

def build_500_crm():
    print("Loading Top 500 Startups Database...")
    with open(STARTUPS_JSON, "r", encoding="utf-8") as f:
        startups = json.load(f)

    print("Loading LinkedIn Network Connections...")
    conns = load_connections()
    print(f"Loaded {len(conns)} LinkedIn connections.")

    crm_records = []
    total_pipeline_val = 0
    total_leakage_val = 0

    # 1. Add Fortune 500 GCCs (46 top centers)
    for idx, (name, park, domain, vec_idx) in enumerate(FORTUNE_500_GCCS, 1):
        vec = SERVICE_VECTORS[vec_idx]
        matched_people = match_connections(name, conns)
        warm_path = f"{len(matched_people)} 1st-degree connection(s)" if matched_people else "Alumni / 2nd-degree executive route"
        key_contact = f"{matched_people[0]['name']} ({matched_people[0]['position']})" if matched_people else "Head of Engineering / Global Director"

        rec = {
            "account_id": f"BLR-ENT-{idx:03d}",
            "company_name": name,
            "category": "Fortune 500 GCC",
            "tech_corridor": park,
            "business_domain": domain,
            "primary_vector": vec["vector"],
            "operational_leakage": vec["leakage"],
            "annual_leakage_inr": vec["annual_leakage"],
            "contract_value_inr": vec["contract_val"],
            "entry_pilot_po_inr": vec["entry_po"],
            "procurement_bypass": vec["bypass"],
            "warm_referral_path": warm_path,
            "target_decision_maker": key_contact,
            "account_status": "Ready for Executive Strike"
        }
        crm_records.append(rec)
        total_pipeline_val += vec["contract_val"]
        total_leakage_val += vec["annual_leakage"]

    # 2. Add Bangalore Top 500 Startups
    start_idx = len(crm_records) + 1
    for i, s in enumerate(startups):
        # Pick vector based on sector
        sec = s["sector"].lower()
        if "fintech" in sec or "banking" in sec:
            vec_idx = 2  # Trade/Nostro/Payment
        elif "deeptech" in sec or "ai" in sec or "robotics" in sec:
            vec_idx = 0  # LLM Eval
        elif "ev" in sec or "mobility" in sec or "cleantech" in sec:
            vec_idx = 3  # Founder's Office Tiger Team
        elif "commerce" in sec or "food" in sec or "marketplace" in sec:
            vec_idx = 5  # Cloud/Inference FinOps
        elif "saas" in sec or "cloud" in sec or "infra" in sec:
            vec_idx = 4  # Outbound Deal Machine
        elif "cybersecurity" in sec or "web3" in sec:
            vec_idx = 0  # Security / Red Team
        elif "industrial" in sec or "manufacturing" in sec:
            vec_idx = 6  # BOT Pods
        else:
            vec_idx = i % len(SERVICE_VECTORS)

        vec = SERVICE_VECTORS[vec_idx]
        matched_people = match_connections(s["company_name"], conns)
        warm_path = f"{len(matched_people)} 1st-degree connection(s)" if matched_people else "Founder / CXO Direct Network"
        key_contact = f"{matched_people[0]['name']} ({matched_people[0]['position']})" if matched_people else "Founder's Office / CTO"

        rec = {
            "account_id": f"BLR-ENT-{start_idx + i:03d}",
            "company_name": s["company_name"],
            "category": f"Startup ({s['stage']})",
            "tech_corridor": s["corridor"],
            "business_domain": s["sector"],
            "primary_vector": vec["vector"],
            "operational_leakage": vec["leakage"],
            "annual_leakage_inr": vec["annual_leakage"],
            "contract_value_inr": vec["contract_val"],
            "entry_pilot_po_inr": vec["entry_po"],
            "procurement_bypass": vec["bypass"],
            "warm_referral_path": warm_path,
            "target_decision_maker": key_contact,
            "flagship_project": s["biggest_project"]["project_name"],
            "account_status": "Ready for Pilot PO"
        }
        crm_records.append(rec)
        total_pipeline_val += vec["contract_val"]
        total_leakage_val += vec["annual_leakage"]

    # Save to JSON
    json_path = DATA_DIR / "bangalore_enterprise_crm_master_500.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(crm_records, f, indent=2, ensure_ascii=False)

    # Save to CSV
    csv_path = DATA_DIR / "bangalore_enterprise_crm_master_500.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "account_id", "company_name", "category", "tech_corridor", "business_domain",
            "primary_vector", "operational_leakage", "annual_leakage_inr", "contract_value_inr",
            "entry_pilot_po_inr", "procurement_bypass", "warm_referral_path", "target_decision_maker", "account_status"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(crm_records)

    usd_val = total_pipeline_val / 83.5
    print("\n" + "=" * 70)
    print(f"SCALE 546 BANGALORE ENTERPRISE CRM PIPELINE GENERATED")
    print(f"Total Accounts:             {len(crm_records)} (46 GCCs + 500 Startups)")
    print(f"Total Annual Contract Val:  INR {total_pipeline_val:,.0f} (~${usd_val:,.0f} USD)")
    print(f"Total Client Leakage Pool:  INR {total_leakage_val:,.0f}")
    print(f"Exported to: {json_path}")
    print(f"Exported to: {csv_path}")
    print("=" * 70)

    # Generate Top 15 SOWs & Proposals
    generate_flagship_sows(crm_records[:15])

def generate_flagship_sows(top_records):
    print("\nGenerating Turnkey SOW & Commercial Contracts for Top 15 Flagship Accounts...")
    for r in top_records:
        safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', r["company_name"]).strip('_')
        sow_path = OUTPUT_DIR / f"SOW_{safe_name}.md"
        content = f"""# STATEMENT OF WORK (SOW) & PILOT COMMISSION DOCKET

**CLIENT ENTITY**: {r['company_name']}
**LOCATION**: {r['tech_corridor']}
**SPECIALIZED SERVICE VECTOR**: {r['primary_vector']}
**COMMERCIAL FORMAT**: {r['procurement_bypass']}
**PILOT COMMITMENT VALUE**: INR {r['entry_pilot_po_inr']:,} (Excl. GST)
**FULL ANNUAL CONTRACT VALUE**: INR {r['contract_value_inr']:,}

---

## 1. Executive Summary & Problem Formulation
{r['company_name']} currently experiences operational and capital drag estimated at **INR {r['annual_leakage_inr']:,} annually** resulting from:
> *"{r['operational_leakage']}"*

This Statement of Work establishes an expedited 14-day zero-risk implementation framework designed to immediately eradicate this friction and prove positive ROI before expanding into a full annual enterprise SLA.

## 2. Scope of Work & Deliverables
1. **Day 1 - 3**: Forensic Invariant & Baseline Audit (Zero disruption to production traffic).
2. **Day 4 - 8**: Deployment of Autonomous Engine & Synthetic Verification Harness.
3. **Day 9 - 12**: Chaos Testing & Latency/Accuracy Optimization under Peak Load.
4. **Day 13 - 14**: Executive Readout, Measurable ROI Scorecard & Long-Term Retainer Transition.

## 3. Commercial Terms & Expedited Sub-Threshold PO
- **Fixed Pilot Consideration**: INR {r['entry_pilot_po_inr']:,} (structured strictly beneath the standard INR 5,00,000 corporate procurement review threshold).
- **Payment Milestones**: 50% mobilization advance upon mutual execution; 50% upon verified sign-off of Deliverables Scorecard.
- **Governing Law**: Jurisdiction of Bengaluru, Karnataka, India.

---
**Prepared by**: OMEGA Autonomous Systems & Enterprise Commercial Syndicate
**Target Stakeholder**: {r['target_decision_maker']}
**Warm Pathway**: {r['warm_referral_path']}
"""
        with open(sow_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Successfully authored 15 comprehensive SOWs in {OUTPUT_DIR}/")

if __name__ == "__main__":
    build_500_crm()
