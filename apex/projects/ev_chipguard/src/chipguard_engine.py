"""
EV-CHIPGUARD: Dynamic Parametric Safety Stock & Stockout Risk Algorithm
"""
import math
from typing import Dict, Any, List

class ChipGuardEngine:
    def __init__(self, daily_usage: float = 2500.0, avg_lead_time_days: float = 120.0, lead_time_std_dev: float = 25.0):
        self.daily_usage = daily_usage
        self.avg_lead_time_days = avg_lead_time_days
        self.lead_time_std_dev = lead_time_std_dev
        self.z_score_99_5 = 2.576 # 99.5% Service Level Confidence

    def calculate_optimal_buffer(self, chip_unit_cost: float = 25.0, annual_carrying_rate: float = 0.18, stockout_hourly_cost: float = 20000.0) -> Dict[str, Any]:
        # Safety Stock = Z * sqrt(LeadTime * Var(Demand) + Demand^2 * Var(LeadTime))
        demand_std_dev = self.daily_usage * 0.15
        
        variance_term = (self.avg_lead_time_days * (demand_std_dev ** 2)) + ((self.daily_usage ** 2) * (self.lead_time_std_dev ** 2))
        safety_stock_units = self.z_score_99_5 * math.sqrt(variance_term)
        
        reorder_point = (self.daily_usage * self.avg_lead_time_days) + safety_stock_units
        annual_holding_cost = safety_stock_units * chip_unit_cost * annual_carrying_rate
        
        # Expected unmitigated risk cost: 48h downtime across 3 plants with 42% historical lead-time spike frequency
        unmitigated_risk_cost = 0.42 * 48 * stockout_hourly_cost * 3
        net_annual_savings = unmitigated_risk_cost - annual_holding_cost

        return {
            "daily_consumption_units": self.daily_usage,
            "avg_lead_time_days": self.avg_lead_time_days,
            "optimal_safety_stock_units": round(safety_stock_units, 0),
            "reorder_point_units": round(reorder_point, 0),
            "buffer_days_coverage": round(safety_stock_units / self.daily_usage, 1),
            "annual_holding_cost_usd": round(annual_holding_cost, 2),
            "unmitigated_downtime_risk_usd": round(unmitigated_risk_cost, 2),
            "net_annual_value_generated_usd": round(net_annual_savings, 2),
            "stockout_probability_pct": 0.5 # 99.5% SLA
        }
