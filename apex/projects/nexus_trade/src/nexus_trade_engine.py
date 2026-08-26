"""
NEXUS-TRADE: Cross-Border Clean Energy Tariff Arbitrage & Landed-Cost Engine
"""
from typing import Dict, Any

class NexusTradeEngine:
    def __init__(self, volume_mw: float = 500.0): # 500MW utility scale project
        self.volume_watts = volume_mw * 1000000

    def compute_arbitrage(self, domestic_cost: float, pli_rebate: float, import_base: float, bcd_rate: float, freight_container: float, watts_container: int) -> Dict[str, Any]:
        # Domestic Net Cost
        net_domestic_cost_per_wp = domestic_cost - pli_rebate
        total_domestic_spend = self.volume_watts * net_domestic_cost_per_wp

        # Imported Landed Cost (Base + BCD + Freight)
        freight_per_wp = freight_container / watts_container
        landed_import_cost_per_wp = (import_base * (1 + bcd_rate)) + freight_per_wp
        total_import_spend = self.volume_watts * landed_import_cost_per_wp

        # Arbitrage calculation
        arbitrage_savings = total_import_spend - total_domestic_spend
        optimal_strategy = "DOMESTIC_PLI_PROCUREMENT" if arbitrage_savings > 0 else "IMPORT_WITH_DUTY"

        return {
            "project_scale_mw": self.volume_watts / 1000000,
            "domestic_net_per_wp": round(net_domestic_cost_per_wp, 4),
            "import_landed_per_wp": round(landed_import_cost_per_wp, 4),
            "total_domestic_spend_usd": round(total_domestic_spend, 2),
            "total_import_spend_usd": round(total_import_spend, 2),
            "net_arbitrage_savings_usd": round(abs(arbitrage_savings), 2),
            "recommended_strategy": optimal_strategy,
            "roi_margin_improvement_pct": round((abs(arbitrage_savings) / total_import_spend) * 100, 2)
        }
