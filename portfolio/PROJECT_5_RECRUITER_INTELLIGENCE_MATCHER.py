#!/usr/bin/env python3
"""
========================================================================================
PORTFOLIO PROJECT 5: RECRUITER & ACTIVE REQUISITION INTELLIGENCE MATCHING ENGINE
========================================================================================
Author: Aditya Mehra (BBA International Business '26)
Context: Automated Matching Engine pairing 525+ Active Requisitions with 1,449 Verified
         Gatekeepers & Recruiters from Aditya's 9,223-Node LinkedIn Network.
Core Functionality:
  1. Searches & Filters Requisitions by Target Track (Operations, Procurement, PMO)
  2. Scores Requisitions against Candidate Core Competencies
  3. Matches with Verified Gatekeepers at Target Employers
  4. Generates 1-Click Tailored LinkedIn Outreach Messages
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
import os
from typing import Dict, List, Any

# Primary Target Track Keywords
TRACK_KEYWORDS = {
    "OPERATIONS": ["Operations", "Process", "Analyst", "Associate", "Quality", "Workflow"],
    "PROCUREMENT": ["Procurement", "Supply Chain", "P2P", "Buyer", "Vendor", "Sourcing"],
    "RISK_FINANCE": ["Risk", "Compliance", "Controls", "Billing", "Financial", "Underwriting"]
}

# Verified Key Gatekeepers & Recruiters
VERIFIED_GATEKEEPERS = {
    "Accenture": [
        {"name": "Darshana Mahesh", "title": "Human Resources Associate", "linkedin": "https://www.linkedin.com/in/darshana-mahesh-6906b6104"},
        {"name": "Swati Bhattacharya", "title": "Talent Acquisition Specialist", "linkedin": "https://www.linkedin.com/search/results/people/?keywords=Accenture%20Recruiter"}
    ],
    "Deloitte": [
        {"name": "Sinchana B", "title": "Business Recruiting Coordinator", "linkedin": "https://www.linkedin.com/in/sinchana-b-730413256"}
    ],
    "EY": [
        {"name": "Jaya Singh", "title": "Senior Talent Acquisition Partner", "linkedin": "https://www.linkedin.com/in/jaya-singh-1aa347171"}
    ],
    "Amazon": [
        {"name": "Sreeja Govindankutty", "title": "Senior HRBP - Operations", "linkedin": "https://www.linkedin.com/in/sreeja-govindankutty"}
    ],
    "Goldman Sachs": [
        {"name": "Akshitha R", "title": "Senior HR Coordinator", "linkedin": "https://www.linkedin.com/in/akshitha-r-737228240"}
    ]
}

def load_accenture_catalog() -> Dict[str, Any]:
    file_path = os.path.join(os.path.dirname(__file__), "..", "all_accenture_job_ids_master.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def run_recruiter_matcher(target_track: str = "PROCUREMENT") -> List[Dict[str, Any]]:
    print("=" * 96)
    print("  PROJECT 5: RECRUITER & ACTIVE REQUISITION INTELLIGENCE MATCHING ENGINE")
    print("  Candidate: Aditya Mehra | Network Scale: 9,223 Connections (1,449 HR / Gatekeepers)")
    print("=" * 96)

    catalog = load_accenture_catalog()
    keywords = TRACK_KEYWORDS.get(target_track, TRACK_KEYWORDS["OPERATIONS"])
    matches = []

    for req_id, data in catalog.items():
        title = data.get("title", "")
        if any(kw.lower() in title.lower() for kw in keywords):
            score = sum(15 for kw in keywords if kw.lower() in title.lower())
            if "Bengaluru" in data.get("location", ""):
                score += 30
            if "New Associate" in title or "Associate" in title:
                score += 40
            matches.append({
                "req_id": req_id,
                "title": title,
                "location": data.get("location", "Bengaluru"),
                "posted": data.get("posted", "Recent"),
                "link": data.get("link", ""),
                "score": score
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    top_matches = matches[:5]

    print(f"\n[+] TOP VERIFIED REQUISITIONS MATCHED FOR TRACK: [{target_track}]")
    print(f"{'Requisition ID':<18} {'Role Title':<38} {'Location':<18} {'Fit Score':<10}")
    print("-" * 96)

    for m in top_matches:
        print(f"{m['req_id']:<18} {m['title'][:36]:<38} {m['location'][:16]:<18} {m['score']:>3}/100")

    if top_matches:
        top_req = top_matches[0]
        gatekeeper = VERIFIED_GATEKEEPERS["Accenture"][0]
        print(f"\n[+] GENERATED 1-CLICK HIGH-CONVERSION OUTREACH DOSSIER:")
        print(f"    • Target Recruiter   : {gatekeeper['name']} ({gatekeeper['title']})")
        print(f"    • Profile URL        : {gatekeeper['linkedin']}")
        print(f"    • Targeted Requisition: {top_req['req_id']} — {top_req['title']}")
        print(f"    • Official Apply URL : {top_req['link']}")
        print("\n--- [PRE-FORMATTED INMAIL COPY READY TO SEND] ---")
        inmail = (
            f"Hi {gatekeeper['name'].split()[0]},\n\n"
            f"Hope your week is off to a great start.\n"
            f"I noticed Accenture is currently hiring for the {top_req['title']} "
            f"(Req ID: {top_req['req_id']}) in Bengaluru.\n"
            f"As an International Business graduate with hands-on experience in workflow reconciliation, "
            f"auditing 5,000+ data entries at Instawork with 99.4% precision and building Excel/Python automated pipelines, "
            f"I have already submitted my application via the Workday portal.\n\n"
            f"My live project portfolio: https://adi-digital-universe.ai.studio/\n"
            f"Would you be open to a 2-minute check on whether my profile fits your team's active shortlisting slate?\n\n"
            f"Best regards,\nAditya Mehra | +91 7003456624"
        )
        print(inmail)
        print("-------------------------------------------------")
    print("=" * 96)
    return top_matches

if __name__ == "__main__":
    run_recruiter_matcher("PROCUREMENT")
