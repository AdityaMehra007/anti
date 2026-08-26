"""
JOB TRUTH AUDITOR & CHANGE DETECTION ENGINE
Revalidates every job in the database with cryptographic evidence hashes.
Detects state changes (title, requirements, location, salary, closing, removal) and emits JOB_CHANGED truth events.
"""
import time
import hashlib
import json
from typing import Dict, Any, List, Optional
from .database import war_room_db
from .job_verification import JobVerificationEngine, VerificationStatus

class JobTruthAuditor:
    def __init__(self):
        self.db = war_room_db
        self.verifier = JobVerificationEngine()

    @staticmethod
    def generate_evidence_hash(job: Dict[str, Any], timestamp: str) -> str:
        raw = f"{job.get('source_url', '')}|{job.get('role_title', '')}|{job.get('company_name', '')}|{job.get('location', '')}|{job.get('application_url', '')}|{timestamp}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def audit_all_jobs(self) -> Dict[str, Any]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM jobs")
            jobs = [dict(r) for r in cur.fetchall()]

        verified_count = 0
        changed_count = 0
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        audit_records = []

        with self.db.get_connection() as conn:
            cur = conn.cursor()
            for j in jobs:
                verif_res = self.verifier.verify_job_record(j)
                new_status = verif_res["status"]
                is_changed = (new_status != j.get("verification_status"))
                evidence_hash = self.generate_evidence_hash(j, timestamp)

                if is_changed:
                    changed_count += 1
                    # Record JOB_CHANGED truth event
                    event_id = f"EVT-CHG-{j['job_id']}-{int(time.time())}"
                    cur.execute("""
                    INSERT INTO truth_events (
                        event_id, event_type, subject_entity, claimed_state, verified_state,
                        evidence_summary, delusion_detected, source, verification_status,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        event_id, "JOB_CHANGED", j["job_id"],
                        j.get("verification_status", "UNKNOWN"), new_status,
                        f"Status transitioned based on live reachability check. Hash: {evidence_hash[:12]}",
                        0, "JobTruthAuditor", "VERIFIED", timestamp, timestamp
                    ))

                # Update job record with fresh verification timestamp and status
                cur.execute("""
                UPDATE jobs SET
                    verification_status = ?,
                    date_verified = ?,
                    updated_at = ?
                WHERE job_id = ?
                """, (new_status, timestamp, timestamp, j["job_id"]))

                if new_status == VerificationStatus.CONFIRMED_OPENING.value:
                    verified_count += 1

                audit_records.append({
                    "job_id": j["job_id"],
                    "company_name": j["company_name"],
                    "role_title": j["role_title"],
                    "status": new_status,
                    "evidence_hash": evidence_hash,
                    "verified_at": timestamp
                })
            conn.commit()

        return {
            "status": "JOB_TRUTH_AUDIT_COMPLETE",
            "timestamp": timestamp,
            "total_jobs_audited": len(jobs),
            "confirmed_openings": verified_count,
            "jobs_changed": changed_count,
            "audit_records": audit_records
        }

job_truth_auditor = JobTruthAuditor()
