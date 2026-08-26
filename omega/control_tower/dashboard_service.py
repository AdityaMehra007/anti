"""
CONTROL TOWER DASHBOARD SERVICE
Aggregates state for UI & CLI display.
"""
from typing import Dict, Any
from ..mcp.client import FirecrawlClient
from .health_monitor import FirecrawlHealthMonitor
from .cost_controller import FirecrawlCostController
from ..engines.company_intelligence import CompanyIntelligenceEngine
from ..engines.job_discovery import JobDiscoveryEngine
from ..brain.career_brain import CareerBrain

class ControlTowerDashboardService:
    def __init__(self):
        self.client = FirecrawlClient()
        self.health_monitor = FirecrawlHealthMonitor(self.client)
        self.cost_controller = FirecrawlCostController()
        self.company_engine = CompanyIntelligenceEngine(self.client)
        self.discovery_engine = JobDiscoveryEngine(self.client)
        self.career_brain = CareerBrain()

    def get_control_panel_state(self) -> Dict[str, Any]:
        health = self.health_monitor.get_status()
        costs = self.cost_controller.get_unit_economics()
        radars = self.company_engine.list_radar_items()
        jobs = self.discovery_engine.discover_bengaluru_opportunities(limit=5)
        scored_jobs = [self.career_brain.score_job(j).to_dict() for j in jobs]

        return {
            "firecrawl": {
                "server": health["server"],
                "health": health["health"],
                "mode": health["mode"],
                "latency_ms": health["latency_ms"],
                "searches": self.cost_controller.total_searches,
                "scrapes": self.cost_controller.total_scrapes,
                "crawls": self.cost_controller.total_crawls,
                "jobs_found": self.cost_controller.total_jobs_found,
                "jobs_verified": self.cost_controller.total_jobs_verified,
                "companies_updated": len(radars),
                "cost_usd": costs["total_cost_usd"],
                "cost_metrics": costs,
                "last_run": health["last_run"],
                "next_run": health["next_run"]
            },
            "top_radar_companies": [
                {"name": r.company_name, "cadence": r.hiring_cadence, "active_roles": r.active_roles_count}
                for r in radars[:5]
            ],
            "recent_top_jobs": scored_jobs
        }
