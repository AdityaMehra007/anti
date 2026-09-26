"""
VECTIS TRADE — Automated Lead Outreach Dispatcher & Cadence Engine
Generates 3-touch personalized outreach sequences for the top 50 high-priority trade leads.
"""

import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(BASE_DIR, "leads", "master_verified_leads.json")
QUEUE_DIR = os.path.join(BASE_DIR, "outreach_queue")
os.makedirs(QUEUE_DIR, exist_ok=True)

OUT_QUEUE_JSON = os.path.join(QUEUE_DIR, "dispatch_queue.json")
OUT_QUEUE_CSV = os.path.join(QUEUE_DIR, "mail_merge_cadence.csv")

def generate_cadence():
    if not os.path.exists(LEADS_FILE):
        print(f"Error: {LEADS_FILE} not found. Run vectis_network_miner.py first.")
        return

    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        leads = json.load(f)

    # Filter top 50 high-priority leads
    high_priority = [l for l in leads if l["priority"] == "HIGH"][:50]
    if len(high_priority) < 50:
        high_priority = leads[:50]

    dispatch_records = []

    for lead in high_priority:
        first_name = lead["name"].split()[0]
        company = lead["company"]
        pos = lead["position"]

        # Touch 1: Direct Value Proposition & Zero-Risk Audit
        t1_subject = f"Zero-risk export document audit for {company}"
        t1_body = (
            f"Hi {first_name},\n\n"
            f"I noticed your work leading {pos} at {company}. "
            f"We built an autonomous compliance gateway (VECTIS TRADE) calibrated to ICC UCP 600 and ISBP 745 banking rules.\n\n"
            f"We know European and US banks routinely reject export shipping dockets over minor typographical differences in description or gross weight rounding, causing €150 refusal fees and 30-day payment delays.\n\n"
            f"We'd love to audit your upcoming export shipment docket for zero fee. "
            f"If your bank accepts the documents with zero discrepancy charges, you only pay us ₹1,500 on subsequent shipments. "
            f"If your bank rejects any document our system certified clean, we will pay your bank discrepancy penalty ourselves.\n\n"
            f"Could we review your draft documents for your upcoming shipment this week?\n\n"
            f"Best regards,\nAditya Mehra\nFounder, VECTIS TRADE (Bengaluru)"
        )

        # Touch 2: Social Proof & Case Study (Day 3)
        t2_subject = f"Quick case study on export LC discrepancy fees ({company})"
        t2_body = (
            f"Hi {first_name},\n\n"
            f"Following up on my previous note. We recently audited a €180,000 export shipment of precision parts to Germany where the Certificate of Origin stated 15,400 KG, but the draft Bill of Lading had rounded up to 15,850 KG.\n\n"
            f"Under ISBP 745 Para E28, this conflict guarantees an immediate SWIFT MT734 refusal notice and a €150 bank penalty fee, trapping working capital for 45 days. We caught it in 60 seconds before bank submission.\n\n"
            f"Happy to run a free pre-check on your next trade docket whenever convenient.\n\n"
            f"Best,\nAditya"
        )

        # Touch 3: UCP 600 Compliance Cheat-Sheet & Final Offer (Day 7)
        t3_subject = f"10-Point UCP 600 Checklist for {company} export documentation"
        t3_body = (
            f"Hi {first_name},\n\n"
            f"Sharing our 1-page ICC UCP 600 pre-submission checklist covering the top 10 discrepancies flagged by international negotiating banks (including Field 45A verbatim consistency and on-board notations).\n\n"
            f"Feel free to drop any draft docket into our free self-serve portal at any time to verify compliance in 60 seconds.\n\n"
            f"Best regards,\nAditya Mehra"
        )

        dispatch_records.append({
            "lead_id": lead["id"],
            "name": lead["name"],
            "company": lead["company"],
            "position": lead["position"],
            "linkedin_url": lead["linkedin_url"],
            "touch1_subject": t1_subject,
            "touch1_body": t1_body,
            "touch2_subject": t2_subject,
            "touch2_body": t2_body,
            "touch3_subject": t3_subject,
            "touch3_body": t3_body
        })

    with open(OUT_QUEUE_JSON, "w", encoding="utf-8") as f:
        json.dump(dispatch_records, f, indent=2)

    with open(OUT_QUEUE_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "lead_id", "name", "company", "position", "linkedin_url",
            "touch1_subject", "touch1_body", "touch2_subject", "touch2_body", "touch3_subject", "touch3_body"
        ])
        writer.writeheader()
        writer.writerows(dispatch_records)

    print(f"Generated 3-touch cadence queue for {len(dispatch_records)} high-priority leads!")
    print(f"Saved: {OUT_QUEUE_JSON}")
    print(f"Saved: {OUT_QUEUE_CSV}")

if __name__ == "__main__":
    generate_cadence()
