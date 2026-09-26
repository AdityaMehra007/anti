#!/usr/bin/env python3
"""
========================================================================================
OMEGA OPPORTUNITY ENGINE & DEDUPLICATION FABRIC (v8.0)
========================================================================================
Ingests, scores, cross-references network graph, deduplicates, and stores opportunities.
========================================================================================
"""

import os, sys, csv, json, sqlite3, re
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.join(r"e:\anti", "omega", "core"))
sys.path.insert(0, r"e:\anti")

try:
    from career_brain import OmegaCareerBrain
except ImportError:
    from omega.core.career_brain import OmegaCareerBrain


class OmegaOpportunityEngine:
    def __init__(
        self,
        db_path: str = r"e:\anti\omega\omega_platform.db",
        network_csv: str = r"e:\anti\linkedin_network_master.csv",
        recruiter_csv: str = r"e:\anti\recruiter_evidence.csv",
        jobs_audit_csv: str = r"e:\anti\61_job_complete_referral_audit.csv"
    ):
        self.db_path = db_path
        self.network_csv = network_csv
        self.recruiter_csv = recruiter_csv
        self.jobs_audit_csv = jobs_audit_csv
        self.brain = OmegaCareerBrain()
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS opportunities (
                    job_id TEXT PRIMARY KEY,
                    target_company TEXT NOT NULL,
                    canonical_company TEXT NOT NULL,
                    job_role TEXT NOT NULL,
                    location TEXT DEFAULT 'Bengaluru, India',
                    job_url TEXT,
                    employee_matches INTEGER DEFAULT 0,
                    recruiter_matches INTEGER DEFAULT 0,
                    hiring_manager_matches INTEGER DEFAULT 0,
                    opportunity_score REAL NOT NULL,
                    strategic_leverage_index REAL NOT NULL,
                    priority_tier TEXT NOT NULL,
                    status TEXT DEFAULT 'DISCOVERED',
                    ingested_at TEXT NOT NULL
                );
            """)
            conn.commit()

    def load_network_indexes(self):
        company_conns = {}
        company_recruiters = {}

        if os.path.exists(self.network_csv):
            with open(self.network_csv, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    comp = row.get("Canonical Company") or row.get("Normalized Company") or row.get("Raw Company", "")
                    comp_key = comp.strip().lower()
                    if comp_key:
                        company_conns[comp_key] = company_conns.get(comp_key, 0) + 1
                        if str(row.get("Recruiter Match", "")).strip() in ["1", "True", "true"]:
                            company_recruiters[comp_key] = company_recruiters.get(comp_key, 0) + 1

        return company_conns, company_recruiters

    def run_ingestion_and_scoring(self, output_json: str = r"e:\anti\omega_opportunity_master.json") -> List[Dict[str, Any]]:
        company_conns, company_recruiters = self.load_network_indexes()
        opportunities = []
        seen_keys = set()

        if os.path.exists(self.jobs_audit_csv):
            with open(self.jobs_audit_csv, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    job_id = row.get("Job ID", "").strip()
                    target_comp = row.get("Target Company", "").strip()
                    canonical_comp = row.get("Canonical Company", "").strip()
                    role = row.get("Job Role", "").strip()
                    url = row.get("Job Application Link", "").strip()

                    # Deduplication key: Normalized (Canonical Company + Role)
                    dedup_key = f"{canonical_comp.lower()}_{re.sub(r'[^a-z0-9]', '', role.lower())}"
                    if dedup_key in seen_keys:
                        continue
                    seen_keys.add(dedup_key)

                    comp_key = canonical_comp.lower()
                    conn_count = company_conns.get(comp_key, int(row.get("Employee Match Count") or 0))
                    rec_count = company_recruiters.get(comp_key, int(row.get("Recruiter Match Count") or 0))
                    hm_count = int(row.get("Hiring Manager Candidates Count") or 0)

                    # Score via Career Brain
                    score_res = self.brain.score_opportunity(
                        job_title=role,
                        company_name=canonical_comp,
                        location="Bengaluru, India",
                        network_connections=conn_count,
                        recruiter_count=rec_count,
                        hiring_manager_count=hm_count
                    )

                    opp_record = {
                        "job_id": job_id,
                        "target_company": target_comp,
                        "canonical_company": canonical_comp,
                        "job_role": role,
                        "location": "Bengaluru, India",
                        "job_url": url,
                        "network_connections": conn_count,
                        "recruiter_matches": rec_count,
                        "hiring_manager_matches": hm_count,
                        "opportunity_score": score_res["overall_opportunity_score"],
                        "strategic_leverage_index": score_res["strategic_leverage_index"],
                        "score_breakdown": score_res["score_breakdown"],
                        "priority_tier": "HIGH" if score_res["overall_opportunity_score"] >= 78.0 else ("MEDIUM" if score_res["overall_opportunity_score"] >= 68.0 else "LOW"),
                        "recommendation": score_res["recommendation"],
                        "status": "QUALIFIED",
                        "ingested_at": datetime.now().isoformat()
                    }
                    opportunities.append(opp_record)

        # Sort opportunities by highest Strategic Leverage & Opportunity Score
        opportunities.sort(key=lambda x: (x["opportunity_score"], x["strategic_leverage_index"]), reverse=True)

        # Save to SQLite DB
        with sqlite3.connect(self.db_path) as conn:
            for opp in opportunities:
                conn.execute("""
                    INSERT OR REPLACE INTO opportunities (
                        job_id, target_company, canonical_company, job_role, location,
                        job_url, employee_matches, recruiter_matches, hiring_manager_matches,
                        opportunity_score, strategic_leverage_index, priority_tier, status, ingested_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    opp["job_id"], opp["target_company"], opp["canonical_company"], opp["job_role"],
                    opp["location"], opp["job_url"], opp["network_connections"], opp["recruiter_matches"],
                    opp["hiring_manager_matches"], opp["opportunity_score"], opp["strategic_leverage_index"],
                    opp["priority_tier"], opp["status"], opp["ingested_at"]
                ))
            conn.commit()

        # Export JSON master
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_opportunities": len(opportunities),
                "high_priority_count": sum(1 for o in opportunities if o["priority_tier"] == "HIGH"),
                "opportunities": opportunities
            }, f, indent=2)

        print(f"Successfully processed & stored {len(opportunities)} deduplicated opportunities in DB & {output_json}")
        return opportunities


if __name__ == "__main__":
    engine = OmegaOpportunityEngine()
    results = engine.run_ingestion_and_scoring()
