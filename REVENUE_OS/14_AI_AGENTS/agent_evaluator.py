"""
Agent Evaluator for REVENUE OS
Adheres strictly to Directives 118, 119, 120.
Tracks: revenue contribution, time saved, error rate, cost, and ROI.
Recommends retirement ('KILL AGENT RULE') for any agent failing to provide positive leverage.
"""

from typing import Any, Dict

class AgentEvaluator:
    """
    Evaluates agent productivity, accuracy, and return on compute investment.
    """
    def evaluate_agent(
        self,
        agent_name: str,
        revenue_attributed_inr: float,
        hours_saved: float,
        error_count: int,
        total_tasks: int,
        agent_cost_usd: float,
        founder_hourly_rate_inr: float = 1000.0,
        fx_usd_to_inr: float = 87.0
    ) -> Dict[str, Any]:
        agent_cost_inr = max(agent_cost_usd * fx_usd_to_inr, 1.0)
        value_created_inr = revenue_attributed_inr + (hours_saved * founder_hourly_rate_inr)
        roi_ratio = round(value_created_inr / agent_cost_inr, 1)
        
        accuracy_pct = round(((total_tasks - error_count) / max(total_tasks, 1)) * 100.0, 1)
        
        # Directive 120: Kill Agent Rule
        # If ROI is below 2.0x or accuracy is below 70%, mark for retirement
        status = "HEALTHY"
        recommendation = "RETAIN"
        if roi_ratio < 2.0 or accuracy_pct < 70.0:
            status = "UNDERPERFORMING"
            recommendation = "RETIRE_OR_REFACTOR (Kill Agent Rule: insufficient economic return)"
            
        return {
            "agent_name": agent_name,
            "value_created_inr": value_created_inr,
            "agent_cost_inr": agent_cost_inr,
            "roi_ratio": roi_ratio,
            "accuracy_pct": accuracy_pct,
            "status": status,
            "recommendation": recommendation
        }
