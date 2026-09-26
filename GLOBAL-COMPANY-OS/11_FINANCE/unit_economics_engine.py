"""
TradeNexus Unit Economics & Financial Projections Engine (ANTIGRAVITY Ω∞)
Models software gross margins, customer acquisition economics, cohort retention,
and the ARR progression ladder from Beachhead ($1M) to Category Leadership ($100M+).
"""

from typing import Dict, Any, List

class UnitEconomicsEngine:
    USD_INR_EXCHANGE_RATE = 85.0

    @classmethod
    def calculate_unit_economics(
        cls,
        monthly_arpu_inr: float = 35000.0,
        cac_inr: float = 45000.0,
        annual_churn_rate: float = 0.08,
        expansion_nrr: float = 1.20,
        gross_margin: float = 0.89
    ) -> Dict[str, Any]:
        """
        Computes SaaS unit economics including LTV, CAC Payback, and LTV:CAC ratio.
        """
        acv_inr = monthly_arpu_inr * 12.0
        acv_usd = acv_inr / cls.USD_INR_EXCHANGE_RATE

        # LTV calculation factoring in net expansion
        effective_churn = max(0.01, annual_churn_rate - (expansion_nrr - 1.0) * 0.1)
        ltv_inr = (acv_inr * gross_margin) / effective_churn
        ltv_usd = ltv_inr / cls.USD_INR_EXCHANGE_RATE

        cac_usd = cac_inr / cls.USD_INR_EXCHANGE_RATE
        ltv_to_cac = ltv_inr / cac_inr if cac_inr > 0 else 999.0

        monthly_gross_profit = monthly_arpu_inr * gross_margin
        payback_months = cac_inr / monthly_gross_profit if monthly_gross_profit > 0 else 0.0

        return {
            "monthly_arpu_inr": monthly_arpu_inr,
            "monthly_arpu_usd": round(monthly_arpu_inr / cls.USD_INR_EXCHANGE_RATE, 2),
            "acv_inr": round(acv_inr, 2),
            "acv_usd": round(acv_usd, 2),
            "cac_inr": cac_inr,
            "cac_usd": round(cac_usd, 2),
            "gross_margin_percent": round(gross_margin * 100, 1),
            "annual_churn_percent": round(annual_churn_rate * 100, 1),
            "nrr_percent": round(expansion_nrr * 100, 1),
            "ltv_inr": round(ltv_inr, 2),
            "ltv_usd": round(ltv_usd, 2),
            "ltv_to_cac_ratio": round(ltv_to_cac, 2),
            "payback_period_months": round(payback_months, 2)
        }

    @classmethod
    def project_arr_ladder(cls) -> List[Dict[str, Any]]:
        """
        Projects milestones along the Trillion-Dollar enterprise ladder.
        """
        stages = [
            {
                "stage": "Beachhead Validation (Stage 1)",
                "paid_exporters": 25,
                "average_mrr_inr": 35000.0,
                "annual_arr_inr": 25 * 35000.0 * 12,
                "annual_arr_usd": (25 * 35000.0 * 12) / cls.USD_INR_EXCHANGE_RATE,
                "monthly_burn_usd": 1500.0,
                "runway_status": "Self-Sustaining & Profitable"
            },
            {
                "stage": "Growth Inflection (Stage 2)",
                "paid_exporters": 250,
                "average_mrr_inr": 42000.0,
                "annual_arr_inr": 250 * 42000.0 * 12,
                "annual_arr_usd": (250 * 42000.0 * 12) / cls.USD_INR_EXCHANGE_RATE,
                "monthly_burn_usd": 12000.0,
                "runway_status": "Series A Ready ($1.5M ARR)"
            },
            {
                "stage": "Market Dominance (Stage 3)",
                "paid_exporters": 1500,
                "average_mrr_inr": 50000.0,
                "annual_arr_inr": 1500 * 50000.0 * 12,
                "annual_arr_usd": (1500 * 50000.0 * 12) / cls.USD_INR_EXCHANGE_RATE,
                "monthly_burn_usd": 65000.0,
                "runway_status": "Enterprise Category Leader ($10.5M ARR)"
            },
            {
                "stage": "Global Customs Network (Stage 4)",
                "paid_exporters": 8000,
                "average_mrr_inr": 65000.0,
                "annual_arr_inr": 8000 * 65000.0 * 12,
                "annual_arr_usd": (8000 * 65000.0 * 12) / cls.USD_INR_EXCHANGE_RATE,
                "monthly_burn_usd": 350000.0,
                "runway_status": "Pre-IPO Scale ($73.4M ARR)"
            }
        ]
        return stages

if __name__ == "__main__":
    import json
    ue = UnitEconomicsEngine.calculate_unit_economics()
    ladder = UnitEconomicsEngine.project_arr_ladder()
    print("SaaS Unit Economics:")
    print(json.dumps(ue, indent=2))
    print("\nARR Ladder Progression:")
    print(json.dumps(ladder, indent=2))
