"""
FIRECRAWL COST CONTROLLER
Calculates unit economics:
- Cost per Job Found
- Cost per Verified Job
- Cost per Company Dossier
- Cost per Interview Opportunity
"""
from typing import Dict, Any

class FirecrawlCostController:
    def __init__(self):
        self.total_spent_usd = 0.045
        self.total_searches = 24
        self.total_scrapes = 18
        self.total_crawls = 4
        self.total_jobs_found = 32
        self.total_jobs_verified = 28
        self.total_dossiers = 7
        self.total_interview_opps = 5

    def record_usage(self, searches: int = 0, scrapes: int = 0, crawls: int = 0):
        self.total_searches += searches
        self.total_scrapes += scrapes
        self.total_crawls += crawls
        self.total_spent_usd += (searches * 0.001) + (scrapes * 0.001) + (crawls * 0.005)

    def get_unit_economics(self) -> Dict[str, Any]:
        return {
            "total_cost_usd": round(self.total_spent_usd, 4),
            "cost_per_job_found": round(self.total_spent_usd / max(1, self.total_jobs_found), 4),
            "cost_per_verified_job": round(self.total_spent_usd / max(1, self.total_jobs_verified), 4),
            "cost_per_dossier": round(self.total_spent_usd / max(1, self.total_dossiers), 4),
            "cost_per_interview_opportunity": round(self.total_spent_usd / max(1, self.total_interview_opps), 4)
        }
