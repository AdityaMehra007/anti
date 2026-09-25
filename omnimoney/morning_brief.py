"""
OMNIMONEY OS - Morning CEO Briefing Engine
Compliant with ANTIGRAVITY OMNIMONEY OS Master Specification (Section 79).
"""

import datetime
from typing import Dict, Any
from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine

class MorningBriefEngine:
    """
    Generates high-leverage daily executive briefs to focus the operator on immediate economic execution.
    """

    def __init__(self, engine: OmniMoneyEngine, sales: B2BSalesEngine):
        self.engine = engine
        self.sales = sales

    def generate_brief(self) -> Dict[str, Any]:
        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        action = self.engine.get_highest_probability_action()
        pipeline = self.sales.get_pipeline_summary()
        opps = self.engine.get_ranked_opportunities(3)

        markdown_content = f"""# 🌅 OMNIMONEY OS: MORNING CEO BRIEF
**Date**: {today_str}
**Operator**: Aditya Mehra (Bengaluru, India)
**Operating Mode**: Mode M (CEO & Capital Allocation) + Mode F (Execution)

---

## 💰 1. MONEY & CASH FLOW RADAR
- **Current Active Pipeline**: ₹{pipeline['pipeline_value_inr']:,}
- **Closed / Won Revenue**: ₹{pipeline['won_revenue_inr']:,}
- **Immediate Target**: ₹20,000 (Day-7 Sprint)
- **Current Income Step**: Step 1 (₹500/day) ➔ Step 2 (₹1,000/day Target)

---

## ⚡ 2. SECTION 153 PRIORITY ACTION TODAY
> **"{action.opportunity}"**
- **Target Segment**: {action.customer}
- **The Acute Problem**: {action.problem}
- **The Core Offer**: {action.offer}
- **Price Point**: ₹{action.price_inr:,}
- **Acquisition Channel**: {action.acquisition_channel}

---

## 🎯 3. THREE NON-NEGOTIABLE ACTIONS TODAY
1. **Audit 10 Local Businesses**: Identify 10 active dermatology/aesthetic clinics running Meta Ads in Indiranagar/Koramangala.
2. **Record 1 Master Loom Demo**: Record a 60-second screen-share demonstrating the AI WhatsApp instant booking bot.
3. **Dispatch 10 Personalized Audits**: Send the tailored video audit via WhatsApp directly to business owners before 1:00 PM.

---

## 📈 4. TOP 3 OPPORTUNITIES MONITORED
"""
        for i, o in enumerate(opps):
            markdown_content += f"- **{i+1}. {o.title}** (Score: {o.score}/100) — Pricing: {o.pricing_model} (First ₹ in {o.time_to_first_rupee_days} days)\n"

        markdown_content += """
---

## 🛡️ 5. RISK & COMPLIANCE GUARDRAIL
- Zero spam: Send strictly 1-to-1 personalized audits showing real value.
- Never promise arbitrary revenue; guarantee appointment bookings and lead responsiveness.
"""

        return {
            "date": today_str,
            "pipeline_value_inr": pipeline["pipeline_value_inr"],
            "won_revenue_inr": pipeline["won_revenue_inr"],
            "priority_action": action.__dict__,
            "top_opportunities": [o.__dict__ for o in opps],
            "non_negotiable_actions": [
                "Audit 10 local clinics in Indiranagar/Koramangala running Meta Ads.",
                "Record 60-second screen-share demo of WhatsApp automated calendar booking.",
                "Dispatch 10 personalized value audits via WhatsApp Business before 1:00 PM."
            ],
            "markdown_brief": markdown_content
        }

    def save_brief_report(self, file_path: str = "reports/DAILY_CEO_BRIEF.md") -> str:
        brief = self.generate_brief()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(brief["markdown_brief"])
        return file_path
