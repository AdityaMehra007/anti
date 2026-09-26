from path_resolver import resolve_data_path
import os, csv, re
from collections import Counter, defaultdict

class NetworkIntelligenceAgent:
    """9,223-Node LinkedIn Network Clustering, Recruiter & Seniority Analysis Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.master_csv = resolve_data_path(workspace, "linkedin_network_master.csv")

    def analyze_network(self):
        if not os.path.exists(self.master_csv):
            return {"error": "linkedin_network_master.csv not found"}
        with open(self.master_csv, "r", encoding="utf-8", errors="replace") as f:
            records = list(csv.DictReader(f))
        
        recruiters = [r for r in records if r.get("Recruiter Match") == "1" or "HR & Talent" in r.get("Functional Area", "")]
        founders = [r for r in records if r.get("Seniority") in ["Founder", "C-Suite"]]
        managers = [r for r in records if r.get("Seniority") in ["Manager / Lead", "VP / Director"]]
        
        return {
            "total_connections": len(records),
            "heuristic_recruiters": len(recruiters),
            "founders_c_suite": len(founders),
            "operational_managers": len(managers),
            "top_companies": Counter(r.get("Canonical Company") for r in records).most_common(10)
        }
