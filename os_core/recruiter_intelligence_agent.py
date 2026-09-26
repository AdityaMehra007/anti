from path_resolver import resolve_data_path
import os, csv

class RecruiterIntelligenceAgent:
    """Specialist Recruiter Profiling & Outreach Readiness Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.rec_csv = resolve_data_path(workspace, "recruiter_evidence.csv")

    def get_top_recruiters_for_company(self, canonical_company):
        if not os.path.exists(self.rec_csv): return []
        with open(self.rec_csv, "r", encoding="utf-8", errors="replace") as f:
            records = list(csv.DictReader(f))
        matches = [r for r in records if canonical_company.lower() in r.get("Canonical Company", "").lower()]
        matches.sort(key=lambda x: int(x.get("Total Recruiter Opportunity Score (100)", 0)), reverse=True)
        return matches[:5]
