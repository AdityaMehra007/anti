from path_resolver import resolve_data_path
import os, csv

class CommunicationsAgent:
    """Outreach Drafting, Approval Queue Staging & E-mail Asset Manager."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.approval_csv = resolve_data_path(workspace, "approval_queue.csv")

    def get_pending_communications(self):
        if not os.path.exists(self.approval_csv): return []
        with open(self.approval_csv, "r", encoding="utf-8", errors="replace") as f:
            records = list(csv.DictReader(f))
        return [r for r in records if r.get("Status") == "PENDING_APPROVAL"]
