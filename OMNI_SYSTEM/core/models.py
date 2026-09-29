"""
Data models and telemetry definitions for OMNI_SYSTEM.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SystemHealth:
    name: str
    port: int
    url: str
    is_live: bool
    status_code: int = 0
    response_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CurrencyPosture:
    currency: str
    symbol: str
    fx_rate_to_inr: float
    pipeline_amount: float
    inr_equivalent: float
    settlement_rail: str

@dataclass
class OmniTelemetry:
    timestamp: str
    operator: str
    today_gross_inr: float
    today_net_profit_inr: float
    today_profit_margin_pct: float
    daily_target_inr: float
    target_achievement_pct: float
    active_pipeline_inr: float
    weighted_pipeline_inr: float
    qualified_leads_count: int
    deals_count: int
    global_rails_count: int
    bangalore_targets_count: int
    ai_assets_grand_total: int
    subsystems_status: Dict[str, bool] = field(default_factory=dict)
    top_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "operator": self.operator,
            "financials": {
                "today_gross_inr": self.today_gross_inr,
                "today_net_profit_inr": self.today_net_profit_inr,
                "today_profit_margin_pct": self.today_profit_margin_pct,
                "daily_target_inr": self.daily_target_inr,
                "target_achievement_pct": self.target_achievement_pct,
                "active_pipeline_inr": self.active_pipeline_inr,
                "weighted_pipeline_inr": self.weighted_pipeline_inr
            },
            "scale": {
                "qualified_leads_count": self.qualified_leads_count,
                "deals_count": self.deals_count,
                "global_rails_count": self.global_rails_count,
                "bangalore_targets_count": self.bangalore_targets_count,
                "ai_assets_grand_total": self.ai_assets_grand_total
            },
            "subsystems_status": self.subsystems_status,
            "top_actions": self.top_actions
        }
