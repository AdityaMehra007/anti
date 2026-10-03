#!/usr/bin/env python3
"""
TradeNexus Autonomous Tax & GST Accounting Engine
Calculates GST (GSTR-1, GSTR-3B) and corporate advance tax liabilities.
"""

import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from typing import Dict, Any

class TaxEngine:
    GST_RATE = 0.18
    CORPORATE_TAX_RATE = 0.22 # Section 115BAA new domestic manufacturing/service co

    @classmethod
    def compute_invoice_taxes(cls, taxable_value: float, is_interstate: bool = False) -> Dict[str, float]:
        total_gst = round(taxable_value * cls.GST_RATE, 2)
        if is_interstate:
            return {"taxable_value": taxable_value, "igst": total_gst, "cgst": 0.0, "sgst": 0.0, "total_invoice": taxable_value + total_gst}
        else:
            half = round(total_gst / 2.0, 2)
            return {"taxable_value": taxable_value, "igst": 0.0, "cgst": half, "sgst": half, "total_invoice": taxable_value + total_gst}

    @classmethod
    def compute_net_burn_and_profit(cls, gross_revenue: float, direct_costs: float) -> Dict[str, float]:
        gross_profit = gross_revenue - direct_costs
        margin_pct = round((gross_profit / gross_revenue) * 100.0, 2) if gross_revenue > 0 else 0.0
        return {
            "gross_revenue": gross_revenue,
            "direct_costs": direct_costs,
            "gross_profit": gross_profit,
            "gross_margin_pct": margin_pct
        }

if __name__ == "__main__":
    t = TaxEngine.compute_invoice_taxes(25000.0, is_interstate=False)
    print("Tax Calculation for ₹25,000 Invoice:", t)
