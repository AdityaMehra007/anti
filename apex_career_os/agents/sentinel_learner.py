"""
sentinel_learner.py - Agent 1: Apex Market Sentinel & Web Learner
==================================================================
Discovers active job postings across multi-channel scrapers, analyzes market dynamics,
extracts high-frequency ATS skills, and continuously updates the KnowledgeLearningVault.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault
from apex_career_os.scrapers.multi_portal_harvester import MultiPortalHarvester

class SentinelLearnerAgent:
    def __init__(self, vault: Optional[KnowledgeLearningVault] = None):
        self.vault = vault or KnowledgeLearningVault()
        self.harvester = MultiPortalHarvester(learning_vault=self.vault)

    def run_harvest_and_learn_cycle(self, limit: int = 100) -> Dict[str, Any]:
        """Runs an end-to-end harvest and continuous learning cycle."""
        start_time = datetime.now()
        jobs = self.harvester.harvest_all(limit_per_source=limit // 2)
        
        learned_count = 0
        company_set = set()
        for j in jobs:
            res = self.vault.learn_from_job_posting(j)
            if res.get("status") == "learned":
                learned_count += 1
                company_set.add(j["company"])

        trending_skills = self.vault.get_top_trending_keywords(limit=15)
        
        return {
            "agent": "SentinelLearnerAgent",
            "cycle_status": "SUCCESS",
            "total_jobs_mined": len(jobs),
            "new_learnings_ingested": learned_count,
            "unique_companies_profiled": len(company_set),
            "top_trending_ats_skills": trending_skills,
            "duration_seconds": round((datetime.now() - start_time).total_seconds(), 2),
            "timestamp": datetime.now().isoformat(),
            "sample_jobs": jobs[:10]
        }

    def learn_company_deep_dive(self, company_name: str, web_snippets: List[str]) -> Dict[str, Any]:
        """Performs deep-dive learning on a specific company from text snippets."""
        total_questions = 0
        for snip in web_snippets:
            res = self.vault.learn_from_online_snippet(company_name, snip, source="Deep Dive Intelligence")
            total_questions += res.get("questions_learned", 0)

        intel = self.vault.get_company_intelligence(company_name)
        return {
            "company": company_name,
            "questions_cataloged": total_questions,
            "intelligence_card": intel
        }
