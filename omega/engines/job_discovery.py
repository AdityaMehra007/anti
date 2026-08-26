"""
JOB DISCOVERY ENGINE
Provides Bengaluru-First Mode (MNC, GCC, Startup, Scaleup) & Global Mode.
Domains: Operations, Supply Chain, Business Dev, Sales, Strategy, AI+Biz, Analytics, Tech.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from ..mcp.client import FirecrawlClient
from .job_extractor import JobExtractor, CanonicalJobRecord
from .job_verifier import JobVerifier
from .deduplicator import JobDeduplicator

@dataclass
class DiscoveryFilter:
    location_mode: str = "Bengaluru"  # Bengaluru, India, Remote, Europe, Ireland, UK, USA, APAC
    company_type: str = "ALL"          # MNC, GCC, Startup, Scaleup, ALL
    roles: List[str] = None
    min_confidence: float = 0.60
    limit: int = 20

class JobDiscoveryEngine:
    def __init__(self, client: Optional[FirecrawlClient] = None):
        self.client = client or FirecrawlClient()
        self.deduplicator = JobDeduplicator()

    def discover_bengaluru_opportunities(
        self,
        domain_category: str = "operations_and_strategy",
        limit: int = 20
    ) -> List[CanonicalJobRecord]:
        queries = [
            f"top MNC GCC tech careers Bengaluru operations supply chain strategy AI 2026",
            f"Bengaluru unicorn startup hiring operations lead business operations logistics",
            f"Walmart Global Tech Target India JPMorgan GCC Bengaluru open roles 2026"
        ]

        raw_jobs: List[CanonicalJobRecord] = []
        for q in queries:
            res = self.client.search(q, limit=limit)
            if res.get("success") and "data" in res:
                for item in res["data"]:
                    url = item.get("url", "")
                    md = item.get("markdown") or item.get("description", "")
                    job = JobExtractor.extract_from_markdown(md, url)
                    verified_job = JobVerifier.verify_job(job)
                    raw_jobs.append(verified_job)

        deduped = self.deduplicator.deduplicate(raw_jobs)
        return deduped[:limit]

    def discover_global_opportunities(
        self,
        target_location: str = "Remote",
        role_keyword: str = "Operations Lead",
        limit: int = 20
    ) -> List[CanonicalJobRecord]:
        query = f"{role_keyword} job openings {target_location} 2026"
        res = self.client.search(query, limit=limit)
        raw_jobs = []
        if res.get("success") and "data" in res:
            for item in res["data"]:
                url = item.get("url", "")
                md = item.get("markdown") or item.get("description", "")
                job = JobExtractor.extract_from_markdown(md, url)
                raw_jobs.append(JobVerifier.verify_job(job))
        return self.deduplicator.deduplicate(raw_jobs)[:limit]
