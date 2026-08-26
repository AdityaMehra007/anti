"""
JOB DEDUPLICATION ENGINE
Merges redundant listings across career portals, LinkedIn, Indeed into a canonical record.
Preserves all source URLs and audit provenance.
"""
import re
from typing import List, Dict, Any
from .job_extractor import CanonicalJobRecord

class JobDeduplicator:
    def __init__(self):
        self._canonical_jobs: Dict[str, CanonicalJobRecord] = {}

    def _generate_dedup_key(self, company: str, role: str, location: str) -> str:
        c = re.sub(r"[^a-z0-9]", "", company.lower())
        r = re.sub(r"[^a-z0-9]", "", role.lower())
        l = "blr" if "bengaluru" in location.lower() or "bangalore" in location.lower() else re.sub(r"[^a-z0-9]", "", location.lower())
        return f"{c}_{r}_{l}"

    def deduplicate(self, jobs: List[CanonicalJobRecord]) -> List[CanonicalJobRecord]:
        for job in jobs:
            key = self._generate_dedup_key(job.company, job.role, job.location)
            if key in self._canonical_jobs:
                existing = self._canonical_jobs[key]
                if job.source_url not in existing.all_source_urls:
                    existing.all_source_urls.append(job.source_url)
                if not existing.salary and job.salary:
                    existing.salary = job.salary
                if not existing.public_recruiter and job.public_recruiter:
                    existing.public_recruiter = job.public_recruiter
                if job.verification_state == "VERIFIED_ACTIVE":
                    existing.verification_state = "VERIFIED_ACTIVE"
            else:
                self._canonical_jobs[key] = job

        return list(self._canonical_jobs.values())

    def get_all(self) -> List[CanonicalJobRecord]:
        return list(self._canonical_jobs.values())
