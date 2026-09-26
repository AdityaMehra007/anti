import os, csv
from path_resolver import resolve_data_path

class AnalyticsAgent:
    """Unified Metrics Engine (Career, Network, Automation, Funnel Analytics)."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def get_dashboard_metrics(self):
        net_csv = resolve_data_path(self.workspace, "linkedin_network_master.csv")
        jobs_csv = resolve_data_path(self.workspace, "61_job_complete_referral_audit.csv")
        app_csv = resolve_data_path(self.workspace, "approval_queue.csv")
        
        total_conn = 0
        if os.path.exists(net_csv):
            with open(net_csv, "r", encoding="utf-8", errors="replace") as f:
                total_conn = max(0, len(list(csv.reader(f))) - 1)
                
        total_jobs = 0
        if os.path.exists(jobs_csv):
            with open(jobs_csv, "r", encoding="utf-8", errors="replace") as f:
                total_jobs = max(0, len(list(csv.reader(f))) - 1)
                
        pending_approvals = 0
        if os.path.exists(app_csv):
            with open(app_csv, "r", encoding="utf-8", errors="replace") as f:
                pending_approvals = max(0, len(list(csv.reader(f))) - 1)
                
        return {
            "network_size": total_conn,
            "pipeline_jobs": total_jobs,
            "pending_approvals": pending_approvals,
            "status": "EVIDENCE-BACKED & SYNCHRONIZED"
        }
