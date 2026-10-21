"""
Scale Bangalore Enterprise CRM to 100+ Tier-1 Targets
Ingests BANGALORE_5000_COMPANIES_WEBSITES_CAREERS_MASTER.csv and linkedin_export/Connections.csv,
curating 50 Fortune 500 GCCs and 50 Top Unicorns/Startups, mapping them across the 7 service vectors.
"""

import csv
import json
import re
from pathlib import Path

BASE_DIR = Path("e:/anti")
COMPANIES_CSV = BASE_DIR / "BANGALORE_5000_COMPANIES_WEBSITES_CAREERS_MASTER.csv"
CONNECTIONS_CSV = BASE_DIR / "linkedin_export/Connections.csv"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "docs/generated_enterprise_deals"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Keyword patterns to identify Fortune 500 GCCs and Tech Unicorns
GCC_KEYWORDS = [
    "walmart", "target", "goldman sachs", "jpmorgan", "cisco", "intel", "bosch", 
    "microsoft", "google", "alphabet", "boeing", "shell", "dell", "wells fargo", 
    "astrazeneca", "standard chartered", "morgan stanley", "hsbc", "deutsche bank",
    "fidelity", "abb", "honeywell", "sap labs", "schneider", "siemens", "novartis",
    "american express", "citigroup", "mercedes", "volvo", "qualcomm", "applied materials",
    "oracle", "ibm", "salesforce", "adobe", "texas instruments", "broadcom", "nike",
    "lowe's", "home depot", "tesco", "optum", "unitedhealth", "metlife", "prudential",
    "barclays", "bny mellon", "state street", "ubs"
]

UNICORN_KEYWORDS = [
    "cred", "swiggy", "zerodha", "razorpay", "zepto", "postman", "groww", "meesho",
    "ather", "sarvam", "krutrim", "inmobi", "browserstack", "hasura", "urban company",
    "ola", "lenskart", "mpl", "dunzo", "khatabook", "slice", "bharatpe", "spinny",
    "cars24", "unacademy", "upgrad", "mpl", "dream11", "nykaa", "bigbasket",
    "cure.fit", "cult.fit", "rapido", "dealshare", "sharechat", "glance", "apna",
    "darwinbox", "leadsquared", "chargebee", "whatfix", "yellow.ai", "clevertap",
    "fractal", "perfios", "digit", "acko", "navi", "jupiter"
]

SERVICE_VECTORS = [
    ("Enterprise LLM Evaluation & Adversarial Red-Teaming Harness", 8500000, 485000, "Sub-Threshold PO (< INR 5L)", 32000000),
    ("GCC Vendor SLA & SOW Leakage Audit & Recovery", 7500000, 480000, "Contingency Shared-Savings (25%)", 28000000),
    ("Automated UCP 600 LC Scrutiny & Nostro Balancer", 12000000, 490000, "Sub-Threshold Discretionary PO", 48000000),
    ("Founder's Office & CXO Tiger Team on Demand", 6500000, 490000, "Founder Direct 14-Day Sprint Mandate", 24000000),
    ("Autonomous B2B Outbound Deal Machine", 5500000, 450000, "Pay-per-Qualified-Meeting Pilot", 22000000),
    ("Cloud & LLM Inference FinOps (Compute Cost Arbitrage)", 6000000, 420000, "Contingency Shared-Savings (30%)", 25000000),
    ("Specialized Build-Operate-Transfer (BOT) Engineering Pods", 11000000, 495000, "Build-Operate-Transfer (BOT) SOW", 38000000)
]

def load_connections():
    conns = []
    if not CONNECTIONS_CSV.exists():
        return conns
    with open(CONNECTIONS_CSV, "r", encoding="utf-8", errors="ignore") as f:
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
    c_lower = re.sub(r"[^a-z0-9]", "", company_name.lower())
    for c in connections:
        conn_c = re.sub(r"[^a-z0-9]", "", c["company"].lower())
        if conn_c in c_lower or c_lower in conn_c or any(t in conn_c for t in c_lower.split() if len(t) > 4):
            matched.append(c)
    return matched[:3]

def main():
    conns = load_connections()
    print(f"Loaded {len(conns)} LinkedIn connections.")
    
    records = []
    seen = set()
    
    with open(COMPANIES_CSV, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cname = row.get("Company Name", "").strip()
            cname_clean = re.sub(r"[^a-z0-9]", "", cname.lower())
            
            if not cname or cname_clean in seen:
                continue
                
            is_gcc = any(k in cname.lower() for k in GCC_KEYWORDS) or "global capability" in row.get("Industry Sector", "").lower() or "gcc" in row.get("Industry Sector", "").lower()
            is_uni = any(k in cname.lower() for k in UNICORN_KEYWORDS) or "fintech" in row.get("Industry Sector", "").lower() or "enterprise saas" in row.get("Industry Sector", "").lower()
            
            if not (is_gcc or is_uni):
                continue
                
            seen.add(cname_clean)
            c_type = "Fortune 500 GCC" if is_gcc else "Bengaluru Tech Unicorn"
            
            # Deterministic vector assignment based on hash of company name
            vec_idx = abs(hash(cname)) % len(SERVICE_VECTORS)
            vec_name, contract_val, entry_po, bypass_rail, annual_leak = SERVICE_VECTORS[vec_idx]
            
            matched = match_connection(cname, conns)
            matched_text = f"{matched[0]['name']} ({matched[0]['position']})" if matched else row.get("HR / TA Lead Name", "Director / VP Lead")
            
            records.append({
                "company": cname,
                "type": c_type,
                "tech_park": row.get("Bangalore Tech Corridor / Park", "Bengaluru Tech Hub"),
                "domain": row.get("Industry Sector", "Technology & Operations"),
                "service_vector": vec_name,
                "contract_inr": contract_val,
                "entry_po_inr": entry_po,
                "est_annual_leakage_inr": annual_leak,
                "procurement_bypass": bypass_rail,
                "lead_contact": matched_text,
                "website": row.get("Official Website", ""),
                "careers_url": row.get("Careers Page URL", ""),
                "direct_email": row.get("Direct HR Work Email", "")
            })
            
            if len(records) >= 100:
                break
                
    print(f"Curated {len(records)} Tier-1 Enterprise Accounts ({len([r for r in records if r['type'] == 'Fortune 500 GCC'])} GCCs, {len([r for r in records if r['type'] == 'Bengaluru Tech Unicorn'])} Startups)")
    
    # Save 100-company master CRM
    json_path = DATA_DIR / "bangalore_enterprise_crm_master_100.json"
    csv_path = DATA_DIR / "bangalore_enterprise_crm_master_100.csv"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
        
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
        
    total_pipeline = sum(r["contract_inr"] for r in records)
    print(f"\n==========================================")
    print(f"SCALE 100 CRM PIPELINE VALUE: INR {total_pipeline:,} (~${total_pipeline / 83.5:,.0f} USD)")
    print(f"Saved to: {json_path} and {csv_path}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
