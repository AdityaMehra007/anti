"""
VECTIS TRADE — Real Network Lead Mining & Outbound Enrichment Engine
Mines linkedin_export/Connections.csv and enterprise directories to isolate real trade decision-makers.
"""

import csv
import json
import os

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONNECTIONS_CSV = os.path.join(WORKSPACE_ROOT, "linkedin_export", "Connections.csv")
LEADS_DIR = os.path.join(os.path.dirname(__file__), "leads")
os.makedirs(LEADS_DIR, exist_ok=True)

OUT_JSON = os.path.join(LEADS_DIR, "master_verified_leads.json")
OUT_CSV = os.path.join(LEADS_DIR, "master_verified_leads.csv")

TRADE_KEYWORDS = [
    "export", "import", "logistics", "supply chain", "trade", "procurement",
    "operations", "freight", "customs", "shipping", "materials", "warehouse"
]

def mine_leads():
    print(f"Mining verified trade contacts from: {CONNECTIONS_CSV} ...")
    if not os.path.exists(CONNECTIONS_CSV):
        print(f"Error: {CONNECTIONS_CSV} not found!")
        return

    leads = []
    seen = set()

    with open(CONNECTIONS_CSV, "r", encoding="utf-8", errors="ignore") as f:
        # Skip top preamble lines if any
        for _ in range(3):
            f.readline()
        
        reader = csv.DictReader(f)
        for row in reader:
            first = row.get("First Name", "").strip()
            last = row.get("Last Name", "").strip()
            company = row.get("Company", "").strip()
            position = row.get("Position", "").strip()
            url = row.get("URL", "").strip()
            connected_on = row.get("Connected On", "").strip()

            if not first or not company or not position:
                continue

            full_name = f"{first} {last}".strip()
            key = (full_name.lower(), company.lower())
            if key in seen:
                continue

            pos_lower = position.lower()
            comp_lower = company.lower()

            matched_terms = [k for k in TRADE_KEYWORDS if k in pos_lower or k in comp_lower]
            if matched_terms:
                seen.add(key)

                # Prioritize seniority
                is_senior = any(s in pos_lower for s in ["senior", "lead", "head", "manager", "director", "vp", "chief", "partner", "founder"])
                priority = "HIGH" if is_senior else "STANDARD"

                # Draft personalized hook
                hook = (
                    f"Hi {first}, noticed your role as {position} at {company}. "
                    f"We built an autonomous pre-submission compliance audit for export LCs and shipping dockets under ICC UCP 600 rules. "
                    f"Would love to share a zero-risk 2-shipment audit pilot to eliminate bank discrepancy penalty fees."
                )

                leads.append({
                    "id": f"LEAD-{len(leads)+1:03d}",
                    "name": full_name,
                    "company": company,
                    "position": position,
                    "priority": priority,
                    "matched_keywords": matched_terms,
                    "linkedin_url": url,
                    "connected_on": connected_on,
                    "tailored_outreach_pitch": hook
                })

    # Sort high priority first
    leads.sort(key=lambda x: (0 if x["priority"] == "HIGH" else 1, x["company"]))

    # Write JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)

    # Write CSV
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "company", "position", "priority", "matched_keywords", "linkedin_url", "connected_on", "tailored_outreach_pitch"])
        writer.writeheader()
        for l in leads:
            row_copy = l.copy()
            row_copy["matched_keywords"] = ", ".join(l["matched_keywords"])
            writer.writerow(row_copy)

    print(f"Successfully mined and enriched {len(leads)} verified trade leads!")
    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")

if __name__ == "__main__":
    mine_leads()
