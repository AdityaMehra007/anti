from path_resolver import resolve_data_path
import os, csv

class ApplicationAgent:
    """Application Lifecycle, Draft Staging & Submission Evidence Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.app_evidence_csv = resolve_data_path(workspace, "application_evidence.csv")

    def get_application_status(self):
        if not os.path.exists(self.app_evidence_csv):
            return {"error": "application_evidence.csv not found"}
        with open(self.app_evidence_csv, "r", encoding="utf-8", errors="replace") as f:
            records = list(csv.DictReader(f))
        return {
            "total_applications_tracked": len(records),
            "draft_ready": sum(1 for r in records if r.get("Submission Status") == "DRAFT_READY"),
            "submitted": sum(1 for r in records if r.get("Submission Status") == "SUBMITTED"),
            "confirmed": sum(1 for r in records if r.get("Submission Status") == "CONFIRMED")
        }
