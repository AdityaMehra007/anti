"""
network_strike.py - Agent 3: Recruiter & 9,223 Network Strike Agent
===================================================================
Taps into the verified directory of Bangalore recruiters, HR directors,
and 9,223 professional connections. Matches any target company or job
with direct decision makers and drafts high-conversion outreach cadences.
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from apex_career_os.core.truth_layer import get_candidate_profile

DATA_DIR = Path(r"e:\anti\data")
HR_DIR_CSV = DATA_DIR / "All_Bangalore_Companies_HR_Directory_Master.csv"
RECRUITER_CSV = DATA_DIR / "Recruiter_and_Hiring_Contacts_Master_Database.csv"

class NetworkStrikeAgent:
    def __init__(self):
        self.candidate = get_candidate_profile()

    def find_recruiters_for_company(self, company_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Searches verified recruiter directories for matching company contacts."""
        results = []
        clean_target = company_name.strip().lower()
        
        # Primary search in HR directory
        if HR_DIR_CSV.exists():
            try:
                with open(HR_DIR_CSV, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        comp = row.get("Company Name", "").lower()
                        if clean_target in comp or comp in clean_target:
                            results.append({
                                "source": "All Bangalore Companies HR Master",
                                "name": row.get("HR / TA Lead Name", "Talent Acquisition Lead"),
                                "title": row.get("Designation / Title", "HR Lead"),
                                "company": row.get("Company Name", company_name),
                                "email": row.get("Direct HR Work Email", ""),
                                "dept_email": row.get("Department Careers Inbox", ""),
                                "phone": row.get("Official Desk / Board Phone", ""),
                                "corridor": row.get("Bangalore Tech Corridor", "Bengaluru"),
                                "linkedin_url": row.get("LinkedIn Search Profile", "")
                            })
                            if len(results) >= limit:
                                return results
            except Exception as e:
                print(f"[NetworkStrike] Error reading HR Directory: {e}")

        # Secondary search in Recruiter Database
        if len(results) < limit and RECRUITER_CSV.exists():
            try:
                with open(RECRUITER_CSV, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        comp = row.get("Company Name", "").lower()
                        if clean_target in comp or comp in clean_target:
                            results.append({
                                "source": "Recruiter & Hiring Contacts Database",
                                "name": row.get("Contact Person Name", "Campus Recruiter"),
                                "title": row.get("Designation", "Recruitment Lead"),
                                "company": row.get("Company Name", company_name),
                                "email": row.get("Official Email", ""),
                                "dept_email": row.get("Recruitment Desk Email", ""),
                                "phone": row.get("Direct / Desk Phone", ""),
                                "corridor": row.get("Location Hub", "Bengaluru"),
                                "linkedin_url": row.get("LinkedIn Search Link", "")
                            })
                            if len(results) >= limit:
                                break
            except Exception as e:
                print(f"[NetworkStrike] Error reading Recruiter CSV: {e}")

        # Fallback synthetic contact if firm not explicitly listed
        if not results:
            results.append({
                "source": "Synthesized Recruiter Pattern",
                "name": f"Hiring Manager / TA Lead",
                "title": f"Talent Acquisition Lead - {company_name}",
                "company": company_name,
                "email": f"careers@{company_name.lower().replace(' ', '')}.com",
                "dept_email": f"talent@{company_name.lower().replace(' ', '')}.com",
                "phone": "+91-80-Bengaluru-Desk",
                "corridor": "Bengaluru Innovation Hub",
                "linkedin_url": f"https://www.linkedin.com/search/results/people/?keywords={company_name.replace(' ', '%20')}%20recruiter%20bangalore"
            })

        return results

    def generate_outreach_dossier(self, job: Dict[str, Any], contact: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generates a complete multi-channel recruiter strike pack."""
        company = job.get("company", "Target Employer")
        title = job.get("title", "Operations & Growth Associate")
        recruiter_name = contact.get("name", "Talent Acquisition Team") if contact else "Talent Acquisition Team"
        first_name = recruiter_name.split()[0] if recruiter_name != "Talent Acquisition Team" else "Hiring Team"
        
        # 1. Direct Cold Email / InMail (Stage 1)
        stage_1_email = f"""Subject: Application / Direct Query: {title} — Aditya Mehra (Immediate Joiner • DSU BBA '26)

Dear {first_name},

I hope this message finds you well.

I am writing directly to express my high-conviction interest in the {title} role at {company}. As an International Business graduate (Dayananda Sagar University, Bengaluru) with immediate joining availability, I combine high-stakes ground operations with production-grade distributed systems engineering:

• High-Concurrency Systems Engineering: Architected ApexFlow, an asynchronous 3-way reconciliation and pipeline engine processing 56,179 transactions/sec at sub-18 microsecond latency with cryptographic SHA-256 idempotency and self-healing circuit breakers to eliminate enterprise procurement leakage.
• High-Stakes Ground Operations: Led exhibition logistics for 100,000+ defense & commercial visitors at AERO INDIA 2025 (Yelahanka Air Force Station) enforcing 0.0% inventory shrinkage and 100% on-time daily security openings.
• Quality & Compliance Audit: Audited high-throughput partner onboarding records maintaining a 99.4% audited accuracy rate at Instawork while cutting review cycle times by 12%.
• Commercial Procurement Impact: Negotiated tier-1 vendor rate cards across 300+ deployments (15% recurring cost savings) and closed INR 1.5L+ in commercial interior contracts with a written Management Commendation.

I have deployed a verified live portfolio showcase with interactive telemetry here: https://github.com/AdityaMehra007

Would you or the hiring lead be open to a brief 10-minute introductory conversation this week?

Warm regards,

Aditya Mehra
Phone: {self.candidate.phone}
LinkedIn: {self.candidate.linkedin_url}
GitHub: https://github.com/AdityaMehra007
Bengaluru, India (Available Immediately)"""

        # 2. Value-Add Follow-up (Stage 2 - Day 4)
        stage_2_followup = f"""Subject: Re: {title} — Aditya Mehra (System architecture & benchmark proof)

Hi {first_name},

Following up on my previous note regarding the {title} opening at {company}.

I wanted to share a quick technical and operational case study on how I approach automated financial integrity and cost discipline:

In addition to managing large-scale physical logistics, I recently engineered a distributed 3-way reconciliation platform (PO vs Goods Receipt vs Tax Invoice) with strict tolerance gating. In automated load testing, the engine clocked 56,179 records/sec with sub-millisecond p99 latency, protected over INR 14.8L in simulated procurement overages, and passed a 54/54 test quality gateway.

Whether governing complex multi-vendor logistics, scaling B2B client pipelines, or automating data operations, I bring relentless ownership and zero-ramp-up velocity to your team.

I would welcome the opportunity to connect briefly. Looking forward to your thoughts!

Best regards,

Aditya Mehra
{self.candidate.phone} | {self.candidate.linkedin_url}"""

        # 3. Alumni / Connection Warm Referral Request
        warm_referral_request = f"""Hi {first_name},

Hope you are doing great!

I noticed that you are currently with {company}—congratulations on the incredible momentum your team is driving!

I am currently applying for the {title} position at {company} (Req ID: {job.get('id', 'ACTIVE-REQ')}). As a fellow professional in Bangalore with a background in International Business from DSU and hands-on experience leading operations for 100,000+ attendees at Aero India 2025 and 300+ deployments, I believe my execution profile is a great fit for your team.

Would you be open to submitting an internal referral or introducing me to the hiring manager for this role? I have an ATS-tailored resume and portfolio ready to share right away.

Really appreciate your time and support!

Best regards,
Aditya Mehra
{self.candidate.phone} | {self.candidate.linkedin_url}"""

        return {
            "stage_1_cold_email": stage_1_email,
            "stage_2_followup": stage_2_followup,
            "warm_referral_request": warm_referral_request
        }
