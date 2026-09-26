from path_resolver import resolve_data_path
import os, csv

class ReferralEngine:
    """1st-Degree Referral Opportunity Ranking and Target Generation Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.matches_csv = resolve_data_path(workspace, "job_to_connection_matches.csv")
        self.referral_targets_csv = resolve_data_path(workspace, "referral_targets.csv")

    def generate_referral_targets(self):
        if not os.path.exists(self.matches_csv):
            return {"error": "job_to_connection_matches.csv not found"}
        with open(self.matches_csv, "r", encoding="utf-8", errors="replace") as f:
            matches = list(csv.DictReader(f))
            
        targets = []
        for m in matches:
            if int(m.get("Total Contact Opportunity Score (100)", 0)) >= 70:
                targets.append({
                    "Job ID": m.get("Job ID"),
                    "Company": m.get("Canonical Company"),
                    "Role": m.get("Job Title"),
                    "Contact Name": m.get("Contact Name"),
                    "Contact Position": m.get("Contact Position"),
                    "LinkedIn URL": m.get("Contact LinkedIn URL"),
                    "Match Type": m.get("Match Type"),
                    "Opportunity Score": m.get("Total Contact Opportunity Score (100)"),
                    "Referral Status": "OPPORTUNITY_STAGED",
                    "Outreach Channel": "LinkedIn 1st-Degree InMail",
                    "Human Approval": "PENDING_APPROVAL"
                })
                
        if targets:
            with open(self.referral_targets_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(targets[0].keys()))
                writer.writeheader()
                writer.writerows(targets)
                
        return {"total_referral_targets": len(targets), "file": self.referral_targets_csv}
