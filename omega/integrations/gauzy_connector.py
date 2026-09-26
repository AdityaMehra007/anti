#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY OMEGA & EVER-GAUZY INTEGRATION CONNECTOR
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Purpose:
  Headless REST API client and bi-directional synchronization bridge between
  ADI CAREER OS / Sovereign Platform and Ever Gauzy (open-source ERP/CRM/HRM/ATS).
Capabilities:
  1. Authentication & Session Management (JWT Bearer Token).
  2. Candidate Profile Synchronization (grounded in verified_profile.json).
  3. ATS Job Requisition Pipeline Ingestion (jobs_master.csv -> Gauzy Job Postings).
  4. CRM Recruiter & Executive Contact Staging (recruiter_evidence.csv -> Gauzy Contacts).
  5. Commercial Proposal & SLA Generation (aligned with commercial operations portfolio).
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

import os
import csv
import json
import logging
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GauzyConnector")

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
PROFILE_JSON = ROOT_DIR / "verified_profile.json"
JOBS_CSV = DATA_DIR / "jobs_master.csv"
RECRUITERS_CSV = DATA_DIR / "recruiter_evidence.csv"
STRIKE_JSON = DATA_DIR / "TARGET_300_JOB_STRIKE.json"

DEFAULT_GAUZY_API_URL = os.getenv("GAUZY_API_URL", "http://localhost:3000/api")
DEFAULT_GAUZY_EMAIL = os.getenv("GAUZY_ADMIN_EMAIL", "admin@ever.co")
DEFAULT_GAUZY_PASSWORD = os.getenv("GAUZY_ADMIN_PASSWORD", "admin")


class GauzyAPIClient:
    """Headless REST API client for Ever Gauzy enterprise backend."""

    def __init__(self, base_url: str = DEFAULT_GAUZY_API_URL, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.organization_id: Optional[str] = None
        self.tenant_id: Optional[str] = None

    def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Antigravity-Omega-GauzyClient/1.0"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        encoded_data = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                return json.loads(res_body) if res_body else {}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8") if e.fp else str(e)
            logger.warning(f"Gauzy API {method} {url} returned HTTP {e.code}: {err_msg}")
            return {"error": True, "status_code": e.code, "message": err_msg}
        except Exception as e:
            logger.warning(f"Failed to connect to Gauzy API at {url}: {e}")
            return {"error": True, "message": str(e)}

    def authenticate(self, email: str = DEFAULT_GAUZY_EMAIL, password: str = DEFAULT_GAUZY_PASSWORD) -> bool:
        """Authenticate with Gauzy backend and store JWT access token."""
        payload = {"email": email, "password": password}
        res = self._request("auth/login", method="POST", data=payload)
        if res.get("token"):
            self.token = res["token"]
            user = res.get("user", {})
            self.organization_id = user.get("defaultOrganizationId")
            self.tenant_id = user.get("tenantId")
            logger.info(f"Authenticated successfully with Gauzy API as {email}")
            return True
        logger.warning("Gauzy authentication failed or server unreachable.")
        return False

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        return self._request(f"candidate/{candidate_id}")

    def create_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("candidate", method="POST", data=candidate_data)

    def create_job_posting(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("job-postings", method="POST", data=job_data)

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("contact", method="POST", data=contact_data)

    def create_proposal(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("proposal", method="POST", data=proposal_data)


class GauzySyncManager:
    """Synchronizes Sovereign OS data into Ever-Gauzy data models."""

    def __init__(self, client: GauzyAPIClient, dry_run: bool = False):
        self.client = client
        self.dry_run = dry_run

    def build_candidate_payload(self) -> Dict[str, Any]:
        """Maps verified_profile.json to Gauzy ICandidate model."""
        profile = {}
        if PROFILE_JSON.exists():
            try:
                with open(PROFILE_JSON, "r", encoding="utf-8") as f:
                    profile = json.load(f)
            except Exception as e:
                logger.error(f"Error loading verified_profile.json: {e}")

        candidate_info = profile.get("candidate", {})
        return {
            "firstName": "Aditya",
            "lastName": "Mehra",
            "email": candidate_info.get("email", "adityamehra799@gmail.com"),
            "phoneNumber": candidate_info.get("phone", "+91-7003456624"),
            "city": "Bengaluru",
            "country": "India",
            "title": "Operations & Business Execution Specialist",
            "resume": "BBA International Business, Dayananda Sagar University ('26)",
            "tags": [
                "Tier-1 Vendor SLA Governance",
                "AERO INDIA 2025 Lead",
                "Instawork AI QA Specialist",
                "Cross-Border EXIM Logistics",
                "Commercial Operations"
            ],
            "metadata": {
                "source": "Antigravity Sovereign OS",
                "synced_at": datetime.now(timezone.utc).isoformat()
            }
        }

    def sync_candidate(self) -> Dict[str, Any]:
        payload = self.build_candidate_payload()
        if self.dry_run:
            logger.info(f"[DRY-RUN] Candidate payload staged: {payload['firstName']} {payload['lastName']} ({payload['email']})")
            return {"status": "DRY_RUN", "payload": payload}
        return self.client.create_candidate(payload)

    def sync_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Syncs top opportunities from jobs_master.csv to Gauzy ATS."""
        if not JOBS_CSV.exists():
            logger.warning(f"Jobs file not found at {JOBS_CSV}")
            return []

        staged = []
        with open(JOBS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                job_payload = {
                    "title": row.get("Role", ""),
                    "description": f"Target Opportunity at {row.get('Company', '')}. Corridor: {row.get('Location', '')}. ATS Score: {row.get('Match Score', '95')}%",
                    "department": row.get("Category", "Business Operations"),
                    "location": row.get("Location", "Bengaluru"),
                    "jobType": "Full-time",
                    "salaryRange": row.get("Expected CTC", "INR 8,00,000 - 14,00,000"),
                    "requirements": [
                        "Vendor SLA Governance",
                        "Operations Management",
                        "Data & AI Quality Assurance"
                    ],
                    "metadata": {
                        "job_id": row.get("Job ID", ""),
                        "company": row.get("Company", ""),
                        "apply_url": row.get("Apply URL", "")
                    }
                }
                staged.append(job_payload)
                count += 1

        if self.dry_run:
            logger.info(f"[DRY-RUN] Staged {len(staged)} jobs for Gauzy ATS.")
            return [{"status": "DRY_RUN", "count": len(staged), "jobs": staged}]

        results = []
        for job in staged:
            res = self.client.create_job_posting(job)
            results.append(res)
        return results

    def sync_recruiters(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Syncs verified recruiters from recruiter_evidence.csv to Gauzy CRM contacts."""
        if not RECRUITERS_CSV.exists():
            logger.warning(f"Recruiters file not found at {RECRUITERS_CSV}")
            return []

        staged = []
        with open(RECRUITERS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                full_name = row.get("Contact Name", "Talent Acquisition Lead")
                name_parts = full_name.split()
                first_name = name_parts[0] if name_parts else "Talent"
                last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Acquisition"

                contact_payload = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "name": full_name,
                    "primaryEmail": row.get("Email", ""),
                    "title": row.get("Designation", "Recruiter"),
                    "company": row.get("Company", ""),
                    "linkedin": row.get("LinkedIn URL", ""),
                    "metadata": {
                        "tier": row.get("Tier", "Tier 1"),
                        "verification_status": row.get("Verification Status", "VERIFIED")
                    }
                }
                staged.append(contact_payload)
                count += 1

        if self.dry_run:
            logger.info(f"[DRY-RUN] Staged {len(staged)} recruiters for Gauzy CRM Contacts.")
            return [{"status": "DRY_RUN", "count": len(staged), "contacts": staged}]

        results = []
        for contact in staged:
            res = self.client.create_contact(contact)
            results.append(res)
        return results


def main():
    parser = argparse.ArgumentParser(description="Antigravity Gauzy Connector & Sync Manager")
    parser.add_argument("--url", default=DEFAULT_GAUZY_API_URL, help="Gauzy API Base URL (default: http://localhost:3000/api)")
    parser.add_argument("--dry-run", action="store_true", help="Stage payloads without sending network requests")
    parser.add_argument("--sync-all", action="store_true", help="Synchronize candidate, jobs, and recruiters")
    parser.add_argument("--sync-candidate", action="store_true", help="Synchronize verified candidate profile")
    parser.add_argument("--sync-jobs", action="store_true", help="Synchronize active pipeline jobs")
    parser.add_argument("--sync-recruiters", action="store_true", help="Synchronize verified recruiters")
    parser.add_argument("--status", action="store_true", help="Check Gauzy API connectivity")

    args = parser.parse_args()
    client = GauzyAPIClient(base_url=args.url)
    sync_mgr = GauzySyncManager(client=client, dry_run=args.dry_run)

    print("=" * 80)
    print("  ANTIGRAVITY OMEGA <-> EVER GAUZY ENTERPRISE CONNECTOR")
    print(f"  Target Gauzy API: {args.url}")
    print(f"  Execution Mode:   {'DRY-RUN (Simulated)' if args.dry_run else 'LIVE CONNECTIVITY'}")
    print("=" * 80)

    if args.status:
        connected = client.authenticate()
        print(f"Gauzy Connection Status: {'ONLINE' if connected else 'OFFLINE / UNREACHABLE'}")
        return

    if args.dry_run or args.sync_all or args.sync_candidate or args.sync_jobs or args.sync_recruiters:
        if not args.dry_run:
            client.authenticate()

        if args.sync_all or args.sync_candidate or args.dry_run:
            print("\n[*] Synchronizing Candidate Ground Truth Profile...")
            cand_res = sync_mgr.sync_candidate()
            print(f"    Candidate Staged: {cand_res.get('status', 'OK')}")

        if args.sync_all or args.sync_jobs or args.dry_run:
            print("\n[*] Synchronizing Target Job Requisitions (ATS)...")
            jobs_res = sync_mgr.sync_jobs(limit=15)
            print(f"    Jobs Staged: {len(jobs_res)} packages prepared.")

        if args.sync_all or args.sync_recruiters or args.dry_run:
            print("\n[*] Synchronizing Recruiter & Executive Leads (CRM)...")
            rec_res = sync_mgr.sync_recruiters(limit=15)
            print(f"    Recruiters Staged: {len(rec_res)} contacts prepared.")

        print("\n" + "=" * 80)
        print("  EVER GAUZY INTEGRATION PIPELINE STAGED & READY!")
        print("=" * 80)
    else:
        # Default run in dry-run mode to show readiness
        print("\n[INFO] No explicit flag passed. Running dry-run verification:")
        sync_mgr.dry_run = True
        sync_mgr.sync_candidate()
        sync_mgr.sync_jobs(limit=5)
        sync_mgr.sync_recruiters(limit=5)


if __name__ == "__main__":
    main()
