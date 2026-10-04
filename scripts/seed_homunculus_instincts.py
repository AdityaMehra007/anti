import os
from pathlib import Path

target_dir = Path(r"C:\Users\amehr\.local\share\ecc-homunculus\projects\7ee25803e542\instincts\personal")
target_dir.mkdir(parents=True, exist_ok=True)

instincts = [
    # Cluster 1: Job Applications & Cold Outreach (recruiter-outreach)
    {
        "id": "outreach-run-of-show-protocol",
        "domain": "recruiter-outreach",
        "trigger": "when submitting job applications or recruiter outreach for global operations",
        "confidence": "0.95",
        "body": "Lead with 6:00 AM Run-of-Show logistics, tarmac clearance, and multi-tier vendor SLA governance from AERO India 2025."
    },
    {
        "id": "outreach-instawork-data-qa",
        "domain": "recruiter-outreach",
        "trigger": "when submitting job applications or recruiter outreach for high-volume data operations",
        "confidence": "0.97",
        "body": "Anchor operations credibility in Instawork 99.2% QA Precision standard across multi-pass validation pipelines."
    },
    {
        "id": "outreach-exim-bba-authority",
        "domain": "recruiter-outreach",
        "trigger": "when submitting job applications or recruiter outreach for international trade operations",
        "confidence": "0.94",
        "body": "Emphasize FCA / CIP Bengaluru Air Cargo customs clearance and DSU BBA International Business domain authority."
    },

    # Cluster 2: Workflow Commands (workflow domain)
    {
        "id": "workflow-batch-gmail-dispatch",
        "domain": "workflow",
        "trigger": "when applying to bangalore startups in bursts",
        "confidence": "0.98",
        "body": "Execute multi-tab pre-populated Gmail compose URLs in bursts of 5, 10, or 20 tabs via bangalore_startups_strike_studio.html."
    },
    {
        "id": "workflow-score-all-applications",
        "domain": "workflow",
        "trigger": "when evaluating candidate fit for 10000 global positions",
        "confidence": "0.96",
        "body": "Run scripts/score_all_applications_apex.py to compute 4-pillar fit scores and generate OMEGA_GLOBAL_CANDIDATE_SCORECARD.md."
    },
    {
        "id": "workflow-negotiate-ctc-offer",
        "domain": "workflow",
        "trigger": "when receiving an employment offer from bangalore gccs",
        "confidence": "0.95",
        "body": "Execute scripts/offer_negotiator.py to compare against Bangalore GCC benchmarks (Rs 6.5L - Rs 11.0L) and generate formal counter-offers."
    },

    # Cluster 3: Risk & Controls (risk-operations)
    {
        "id": "risk-zero-shrinkage-dual-custody",
        "domain": "risk-operations",
        "trigger": "when managing operational risk and high volume inventory audit",
        "confidence": "0.96",
        "body": "Enforce dual-custody barcode staging and military defense security protocols to sustain 0.0% inventory shrinkage."
    },
    {
        "id": "risk-vendor-margin-recovery",
        "domain": "risk-operations",
        "trigger": "when managing operational risk and vendor rate card variance",
        "confidence": "0.93",
        "body": "Run multi-pass discrepancy audit models to recover leakage and eliminate invoice drift under strict SLAs."
    }
]

for inst in instincts:
    file_path = target_dir / f"{inst['id']}.md"
    content = f"""---
id: {inst['id']}
domain: {inst['domain']}
trigger: "{inst['trigger']}"
confidence: {inst['confidence']}
---

# {inst['id']}

{inst['body']}
"""
    file_path.write_text(content, encoding="utf-8")
    print(f"Wrote {file_path.name}")

print("Successfully seeded clustered instincts.")
