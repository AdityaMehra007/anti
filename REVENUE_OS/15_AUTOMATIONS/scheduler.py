"""
Task Scheduler for REVENUE OS
Adheres strictly to Directives 85, 86, 169.
Defines cron intervals (HOURLY, DAILY, WEEKLY, MONTHLY) and executes scheduled pipelines.
"""

from typing import Any, Dict, List, Optional
from REVENUE_OS.automations.automations import AutomationEngine

class TaskScheduler:
    """
    Manages recurring schedules for 24/7 background revenue monitoring.
    """
    def __init__(self, engine: Optional[AutomationEngine] = None):
        self.engine = engine or AutomationEngine()
        self._jobs: List[Dict[str, Any]] = [
            {
                "id": "JOB-01",
                "name": "daily_market_scan",
                "frequency": "DAILY",
                "cron": "0 6 * * *", # 6:00 AM daily
                "description": "Scans public market data and updates buying signals."
            },
            {
                "id": "JOB-02",
                "name": "lead_discovery",
                "frequency": "DAILY",
                "cron": "0 7 * * *",
                "description": "Identifies newly announced funding and executive transitions."
            },
            {
                "id": "JOB-03",
                "name": "lead_scoring",
                "frequency": "DAILY",
                "cron": "30 7 * * *",
                "description": "Scores new leads and queues top accounts to CRM."
            },
            {
                "id": "JOB-04",
                "name": "weekly_revenue_report",
                "frequency": "WEEKLY",
                "cron": "0 9 * * 1", # Monday 9:00 AM
                "description": "Compiles executive weekly P&L and channel conversion report."
            },
            {
                "id": "JOB-05",
                "name": "failed_payment_alert",
                "frequency": "HOURLY",
                "cron": "0 * * * *",
                "description": "Checks payment gateway status for transaction failures."
            },
            {
                "id": "JOB-06",
                "name": "expense_audit",
                "frequency": "MONTHLY",
                "cron": "0 0 1 * *",
                "description": "Audits recurring software subscriptions for unused tools."
            }
        ]

    def get_scheduled_jobs(self) -> List[Dict[str, Any]]:
        return self._jobs

    def trigger_job(self, job_name: str) -> Dict[str, Any]:
        return self.engine.run_automation(job_name)
