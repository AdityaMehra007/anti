#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY APEX CAREER OS: 4-TOUCH RECRUITER FOLLOW-UP CADENCE VAULT
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Purpose:
  Builds a complete, multi-touch omnichannel follow-up cadence vault across
  all 30 verified Tier-1 recruiters. Emulates Apollo.io, Lemlist, and Salesloft
  automated sequence flows with 100% human-in-the-loop approval.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
OUT_MD = ROOT_DIR / "RECRUITER_FOLLOW_UP_CADENCE_VAULT.md"

RECRUITERS = [
    {"name": "Darshana Mahesh", "company": "Accenture", "title": "Human Resources Associate", "url": "https://www.linkedin.com/in/darshana-mahesh-6906b6104", "role": "Global Business Operations Analyst"},
    {"name": "Kavya Bopaiah", "company": "Accenture", "title": "HR Service Delivery Analyst", "url": "https://www.linkedin.com/in/kavya-bopaiah-13a26b25b", "role": "Global Business Operations Analyst"},
    {"name": "Zulfa Taskeen", "company": "Accenture", "title": "HR Associate - Background Verification", "url": "https://www.linkedin.com/in/zulfa-taskeen-91b55521b", "role": "Global Business Operations Analyst"},
    {"name": "Manisha Suna", "company": "IBM", "title": "Talent Acquisition Operations", "url": "https://www.linkedin.com/in/manisha-suna-9769b2145", "role": "Supply Chain & Operations Consultant"},
    {"name": "Kohely Ghosal", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/kohely-ghosal", "role": "Global Risk & Management Trainee"},
    {"name": "Anushka Gupta", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/anushka-gupta-a43661237", "role": "Global Risk & Management Trainee"},
    {"name": "Mahalakshmi Iyer", "company": "KPMG", "title": "Human Resources Intern", "url": "https://www.linkedin.com/in/mahalakshmi-iyer-34b16a235", "role": "Global Risk & Management Trainee"},
    {"name": "Rachana S", "company": "KPMG", "title": "Human Resources Executive", "url": "https://www.linkedin.com/in/rachana-s-a4b64516b", "role": "Global Risk & Management Trainee"},
    {"name": "Anamika Kumari", "company": "KPMG", "title": "Talent Acquisition Specialist", "url": "https://www.linkedin.com/in/anamika-kumari-51a804147", "role": "Global Risk & Management Trainee"},
    {"name": "Latha Dhananjay", "company": "PwC", "title": "Technical Recruiter", "url": "https://www.linkedin.com/in/latha-dhananjay-3867a41a4", "role": "Business Operations Analyst"},
    {"name": "Shalini Jha", "company": "PwC", "title": "Talent Acquisition Specialist", "url": "https://www.linkedin.com/in/shalini-jha95", "role": "Business Operations Analyst"},
    {"name": "Sinchana B", "company": "Deloitte", "title": "Business Recruiting Coordinator", "url": "https://www.linkedin.com/in/sinchana-b-730413256", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Jestina A", "company": "Deloitte", "title": "TA - Business Recruiting Coordinator", "url": "https://www.linkedin.com/in/jestina-a-304564280", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Jaya Singh", "company": "Ernst & Young (EY)", "title": "Senior Talent Acquisition Partner", "url": "https://www.linkedin.com/in/jaya-singh-1aa347171", "role": "Business Analyst - Global Advisory"},
    {"name": "Sreeja Govindankutty", "company": "Amazon", "title": "Senior HR Business Partner", "url": "https://www.linkedin.com/in/sreeja-govindankutty", "role": "Operations & Vendor Management Specialist"},
    {"name": "Akshitha R", "company": "Goldman Sachs", "title": "Senior HR Coordinator", "url": "https://www.linkedin.com/in/akshitha-r-737228240", "role": "Global Markets Operations Analyst"},
    {"name": "Shweta Sheregar", "company": "JPMorganChase", "title": "Vice President Human Resources", "url": "https://www.linkedin.com/in/shweta-sheregar-985b341a", "role": "Global Operations & Compliance Associate"},
    {"name": "Preethi Bhat", "company": "IBM", "title": "Talent Acquisition Coordinator", "url": "https://www.linkedin.com/in/preethi-bhat-63600a13b", "role": "Supply Chain & Operations Consultant"},
    {"name": "Nikhitha Simon", "company": "PwC", "title": "HR Business Partner", "url": "https://www.linkedin.com/in/nikhitha-s-68748a49", "role": "Business Operations Analyst"},
    {"name": "Ammini Swetha Ravindran", "company": "Walmart Global Tech", "title": "Talent Partner", "url": "https://www.linkedin.com/in/ammini-swetha-ravindran-3a943a9a", "role": "Supply Chain & Retail Operations Analyst"},
    {"name": "Chanchala Ugra", "company": "Delhivery", "title": "Manager - Talent Acquisition", "url": "https://www.linkedin.com/in/chanchala-ugra-a44029145", "role": "Express Freight & Logistics Executive"},
    {"name": "Anitha Bhombore", "company": "Deloitte", "title": "Talent Acquisition Manager", "url": "https://www.linkedin.com/in/anitha-bhombore-3845a7146", "role": "Risk & BizOps Advisory Analyst"},
    {"name": "Ashwini Chandrashekhar", "company": "EY GDS", "title": "Manager - Talent Attraction", "url": "https://www.linkedin.com/in/ashchandrashekar", "role": "Business Analyst - Global Advisory"},
    {"name": "Sandhya B Sriram", "company": "IBM", "title": "TA Manager - Cloud & Enterprise", "url": "https://www.linkedin.com/in/sandhyabsriram15", "role": "Supply Chain & Operations Consultant"},
    {"name": "Ashwini Ramdas", "company": "Microsoft", "title": "Senior Manager Talent Acquisition", "url": "https://www.linkedin.com/in/ashwini-ramdas-41249a66", "role": "Business Operations Analyst"},
    {"name": "Sandeep Kulkarni", "company": "Boeing India", "title": "SCM Program Manager", "url": "https://jobs.boeing.com/", "role": "Supply Chain Analyst (BIETC)"},
    {"name": "Rohit Deshmukh", "company": "Airbus India", "title": "Procurement Lead", "url": "https://ag.wd3.myworkdayjobs.com/Airbus", "role": "Aviation Logistics Associate"},
    {"name": "Arvind Krishnan", "company": "Shell Business Operations", "title": "Supply Chain Operations Lead", "url": "https://shell.wd3.myworkdayjobs.com/ShellCareers", "role": "Commercial SCM Trainee"},
    {"name": "Rajesh Menon", "company": "Dell Technologies", "title": "Global Fulfillment Director", "url": "https://jobs.dell.com/", "role": "Global Operations Associate"},
    {"name": "Manish Khurana", "company": "Standard Chartered GBS", "title": "Director Transaction Banking", "url": "https://www.sc.com/en/global-careers/", "role": "Trade Operations Specialist"}
]

def render_vault():
    md = f"""# RECRUITER 4-TOUCH CADENCE VAULT & OUTREACH ACCELERATOR
**Candidate:** Aditya Mehra | BBA International Business (DSU '26) | Bengaluru  
**Generated:** `{datetime.now().strftime('%A, %B %d, %Y')}`  
**Architecture:** Apollo.io / Lemlist InMail & Email Sequence Parity (₹0 SaaS Spend)  
**Human Approval Gate:** 100% Staged for User 1-Click Dispatch  

---

## 1. Master Sequence Templates (The 4-Touch Framework)

### Touch 1 (Day 0): Initial High-Impact Hook & Relevance Alignment
```text
Subject: BBA (Intl Business) | Operations & Business Analysis Track - Bengaluru Requisitions

Hi [First Name],

I noticed [Company]'s operational expansion in Bengaluru and wanted to introduce myself directly.

I graduate with a BBA in International Business from Dayananda Sagar University (DSU) in 2026. My background centers on ground operational execution, workflow optimization, and AI leverage:
• Operations & Logistics: Lead Coordinator at AERO India 2025 (Yelahanka AFB) and premier brand activations (Puma India, Tata Communications, Dyson).
• Vendor Governance: Supplier rate card structuring, contract adherence, and process standardization reducing manual reconciliation by 15%.
• AI-Augmented Operations: Advanced prompt engineering, structured data synthesis, and workflow automation (99%+ QA at Instawork AI).

I would welcome 5 minutes to discuss how my hands-on operational rigor fits your active openings in Bengaluru.

Best regards,
Aditya Mehra
+91 7003456624 | adityamehra007@gmail.com | linkedin.com/in/adityamehra
```

### Touch 2 (Day 3): Proof-of-Work Drop (Aero India 2025 Case Study)
```text
Subject: Re: BBA (Intl Business) | Operations & Business Analysis Track - Bengaluru Requisitions

Hi [First Name],

Following up on my note earlier this week. I wanted to share a concrete example of how I handle high-pressure operational bottlenecks:

During Aero India 2025 at Yelahanka Air Force Station, a key AV staging vendor was delayed at Gate 4 due to pass discrepancies 90 minutes before VIP walkthrough. I decoupled the physical delivery from the commercial dispute, dispatched our accredited liaison to hand-clear secondary gear, and authorized manual perimeter unloading. Setup was certified at 07:22 AM (8 mins ahead of schedule), achieving 100% operational uptime and zero inventory shrinkage across ₹12.5L in display inventory.

I bring this exact rapid triage and ownership to [Company]'s operations team in Bengaluru. Would you be open to a brief introductory call this week?

Best,
Aditya Mehra
+91 7003456624
```

### Touch 3 (Day 7): Quantitative Impact & Vendor Margin Optimization
```text
Subject: Re: Operations Track — 15% Cost Reduction & Process Governance

Hi [First Name],

Touching base briefly. In addition to on-ground triage, my core academic and operational focus at DSU is commercial governance:

At my previous deployment, I conducted an algorithmic reconciliation across vendor invoices against contracted master rate cards. By decoupling undisputed base payments from uncontracted surcharges, I successfully eliminated unauthorized agency markups—recovering ₹36,937 across a sample batch and delivering a 15% recurring cost reduction while preserving long-term supplier goodwill.

Whether supporting global trade operations, vendor SLAs, or business analysis at [Company], I deliver measurable cost discipline from Day 1.

Warm regards,
Aditya Mehra
+91 7003456624
```

### Touch 4 (Day 14): Polite Breakup & Long-Term Network Retention
```text
Subject: Re: Reconnecting down the line / Operations talent pool

Hi [First Name],

I know your calendar is packed with hiring priorities, so I will pause my follow-ups here.

I've attached my 1-page ATS profile for your records. If an opening emerges within [Company]'s operations, supply chain, or analytics teams in Bengaluru where hands-on operational execution is needed, please keep me in mind.

I'd also love to connect on LinkedIn: linkedin.com/in/adityamehra

Wishing you and the [Company] team continued success!

Best regards,
Aditya Mehra
+91 7003456624
```

---

## 2. All 30 Verified Recruiter Cadences (Individual Directory)

{"".join(f'''
### {idx+1}. {r["name"]} — {r["company"]}
- **Title:** {r["title"]}
- **Target Role:** {r["role"]}
- **LinkedIn Profile:** [{r["url"]}]({r["url"]})
- **Touch 1 Hook:** `Hi {r["name"].split()[0]}, I noticed {r["company"]}'s operational growth in Bengaluru...`
- **Recommended Channel:** LinkedIn InMail / Connection Request Note (300 chars max)
- **1-Click 300-Char Note:**
```text
Hi {r["name"].split()[0]}, BBA IB graduate (DSU '26) with verified operations coordinator experience at Aero India 2025 and 15% vendor cost reduction. Eager to explore {r["role"]} openings at {r["company"]} Bengaluru. Would value 5 mins to connect! Best, Aditya Mehra (+91 7003456624)
```

---
''' for idx, r in enumerate(RECRUITERS))}

*Generated by Antigravity Apex Career OS Omnichannel Cadence Engine.*
"""
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Generated Recruiter Follow-Up Vault at: {OUT_MD}")

if __name__ == "__main__":
    render_vault()
