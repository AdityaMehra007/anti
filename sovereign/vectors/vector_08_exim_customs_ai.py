"""Vector 8: EXIM Trade, Customs Automation & Cross-Border Supply Chain AI (30 Capabilities)."""
from typing import Dict, Any

class EXIMCustomsAutomationEngine:
    @staticmethod
    def calculate_customs_clearance(cif_value_inr: float, bcd_rate_pct: float = 10.0, igst_rate_pct: float = 18.0) -> Dict[str, Any]:
        bcd_amount = cif_value_inr * (bcd_rate_pct / 100.0)
        sws_amount = bcd_amount * 0.10  # 10% Social Welfare Surcharge on BCD
        assessable_for_igst = cif_value_inr + bcd_amount + sws_amount
        igst_amount = assessable_for_igst * (igst_rate_pct / 100.0)
        total_customs_duty = round(bcd_amount + sws_amount + igst_amount, 2)
        total_landed_cost = round(cif_value_inr + total_customs_duty, 2)
        
        return {
            "cif_value": cif_value_inr,
            "bcd_duty": round(bcd_amount, 2),
            "sws_surcharge": round(sws_amount, 2),
            "igst_duty": round(igst_amount, 2),
            "total_customs_duty": total_customs_duty,
            "total_landed_cost": total_landed_cost,
            "effective_tax_rate": f"{round((total_customs_duty / cif_value_inr) * 100, 2)}%"
        }
