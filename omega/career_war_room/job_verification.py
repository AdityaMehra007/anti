"""
JOB VERIFICATION ENGINE
Strict truth classification: CONFIRMED_OPENING, LIKELY_HIRING_SIGNAL, UNVERIFIED, EXPIRED, REMOVED.
Only CONFIRMED_OPENING may enter the priority application queue.
"""
import time
import hashlib
from enum import Enum
from typing import Dict, Any, Optional

class VerificationStatus(str, Enum):
    CONFIRMED_OPENING = "CONFIRMED_OPENING"
    LIKELY_HIRING_SIGNAL = "LIKELY_HIRING_SIGNAL"
    UNVERIFIED = "UNVERIFIED"
    EXPIRED = "EXPIRED"
    REMOVED = "REMOVED"

class JobVerificationEngine:
    @staticmethod
    def generate_dedup_hash(company: str, role: str, location: str, application_url: str) -> str:
        clean = f"{company.strip().lower()}|{role.strip().lower()}|{location.strip().lower()}|{application_url.strip().lower()}"
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_job_record(job_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates whether a job record has legitimate primary/secondary source proof.
        """
        app_url = job_dict.get("application_url", "").strip()
        source = job_dict.get("source", "").strip()
        role = job_dict.get("role_title", "").strip()
        company = job_dict.get("company_name", "").strip()

        if not (role and company and app_url):
            return {
                "status": VerificationStatus.UNVERIFIED.value,
                "is_confirmed": False,
                "reason": "Missing mandatory role title, company name, or application URL."
            }

        # Check official domain evidence
        is_official = any(domain in app_url.lower() for domain in [
            "amazon.jobs", "microsoft.com", "google.com", "maersk.com",
            "se.com", "dhl.com", "accenture.com", "target.com", "myworkdayjobs.com",
            "taleo.net", "greenhouse.io", "lever.co", "smartrecruiters.com", "icims.com"
        ])

        if is_official:
            return {
                "status": VerificationStatus.CONFIRMED_OPENING.value,
                "is_confirmed": True,
                "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source_evidence": f"Confirmed on authoritative portal: {source}"
            }

        return {
            "status": VerificationStatus.LIKELY_HIRING_SIGNAL.value,
            "is_confirmed": False,
            "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source_evidence": f"Aggregator / Secondary source detected ({source}). Requires official portal check."
        }

job_verifier = JobVerificationEngine()
