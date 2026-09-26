"""Sales Agent — B2B Lead Scoring & MEDDPICC Pipeline Velocity."""
from typing import Dict, Any

class SalesAgent:
    @staticmethod
    def calculate_pipeline_velocity(opportunities: int, win_rate: float, acv: float, cycle_days: int) -> float:
        if cycle_days <= 0:
            return 0.0
        return round((opportunities * win_rate * acv) / cycle_days, 2)
