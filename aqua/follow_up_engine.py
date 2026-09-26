"""
TradeNexus Multi-Step Enterprise Follow-Up Engine (ANTIGRAVITY Ω∞)
Generates high-conversion, timed follow-up sequences for Indian exporter accounts,
anchoring on regulatory filing deadlines (CBAM), ICEGATE query prevention, and demurrage ROI.
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from aqua.crm_tracker import PipelineCRM

class FollowUpEngine:
    def __init__(self, crm: Optional[PipelineCRM] = None):
        self.crm = crm or PipelineCRM()

    def generate_followup_message(self, account_id: str, step: int = 2) -> Dict[str, Any]:
        acc = self.crm.get_account(account_id)
        if not acc:
            raise ValueError(f"Account {account_id} not found in CRM.")

        company = acc["company_name"]
        contact_title = acc["contact_title"] or "Export Director"
        products = acc["key_products"] or "export consignments"
        dest = acc["destination"] or "US/EU"
        demurrage = acc["demurrage_exposure_usd"] or 4500.0

        if step == 2:
            # Step 2: Day 3 - Technical Proof & CBAM Submission Deadlines
            subject = f"Re: Regulatory filing deadline & ICEGATE EDI query prevention ({company})"
            body = f"""Dear {contact_title},

Following up on the pre-shipment compliance audit docket we generated for {company}'s {products} shipping to {dest}.

Under current European Commission enforcement mandates (CBAM Annex I), consignments arriving without pre-validated direct emissions XML filings face automatic customs quarantine and EUR 50/tonne penalties.

To eliminate this operational friction, TradeNexus AI generates:
1. EU-compliant CBAM XML declarations in 45 seconds from your invoice data.
2. Statutory ICEGATE Remote EDI System (RES) shipping bill flat-files (.sb) pre-validated with zero human re-keying errors.

Could we schedule a 10-minute live demonstration of the clearance portal with your export documentation desk this week?

Warm regards,

Aditya Mehra
Founder, TradeNexus AI | Global Company OS
Bengaluru, Karnataka | trade@tradenexus.ai
"""
        elif step == 3:
            # Step 3: Day 7 - Financial ROI & Demurrage Shield
            monthly_inr = acc["target_monthly_inr"] or 35000.0
            subject = f"Quantifying the ${demurrage:,.0f} demurrage risk vs INR {monthly_inr:,.0f}/mo pilot ({company})"
            body = f"""Dear {contact_title},

A quick economic note regarding {company}'s export operations on the {dest} corridor:

A single customs query or documentary hold at destination port typically incurs:
* 8 days average port detention & container demurrage: ${demurrage:,.0f} (~INR {int(demurrage * 85):,})
* Port terminal inspection and re-filing surcharges: EUR 1,200 - EUR 2,500
* Client delivery delay penalties and line-stoppage chargebacks

TradeNexus AI eliminates this exposure entirely through our INR {monthly_inr:,.0f}/month 30-Day Paid Pilot, backed by our direct INR 5,00,000 Demurrage Indemnity Shield.

If you are open to reviewing the pilot terms, I would be delighted to share the 1-page term sheet.

Warm regards,

Aditya Mehra
Founder, TradeNexus AI | Global Company OS
Bengaluru, Karnataka | trade@tradenexus.ai
"""
        elif step == 4:
            # Step 4: Day 14 - Breakup / Executive Escalation
            subject = f"Closing the audit file for {company} / TradeNexus AI"
            body = f"""Dear {contact_title},

I know you are exceptionally busy managing international logistics and high-volume export schedules for {company}.

I will assume that pre-shipment customs pre-clearance and CBAM automation are not immediate priorities for your desk right now, and I will close out your complimentary audit docket (Seal: {acc.get('audit_seal', 'TN-SEAL')}).

If tariff enforcement queries or overseas port demurrage costs become an issue later this quarter, you can access your verified docket anytime at trade@tradenexus.ai.

Wishing you continued smooth sailings and high export volumes.

Warm regards,

Aditya Mehra
Founder, TradeNexus AI | Global Company OS
Bengaluru, Karnataka | trade@tradenexus.ai
"""
        else:
            raise ValueError(f"Unsupported follow-up step: {step}. Must be 2, 3, or 4.")

        return {
            "account_id": account_id,
            "company_name": company,
            "step": step,
            "subject": subject,
            "body": body
        }

    def get_account_by_name_or_id(self, identifier: str) -> Optional[Dict[str, Any]]:
        acc = self.crm.get_account(identifier)
        if acc:
            return acc
        for a in self.crm.list_accounts():
            if identifier.lower() in a["company_name"].lower():
                return a
        return None

    def generate_outreach_sequence(self, identifier: str) -> Dict[str, Any]:
        acc = self.get_account_by_name_or_id(identifier)
        if not acc:
            raise ValueError(f"Account '{identifier}' not found in CRM.")
        acc_id = acc["account_id"]
        touches = [
            {"touch": "Step 2: Technical & CBAM Proof", "day_offset": 3, **self.generate_followup_message(acc_id, step=2)},
            {"touch": "Step 3: Economic ROI & Demurrage Shield", "day_offset": 7, **self.generate_followup_message(acc_id, step=3)},
            {"touch": "Step 4: Graceful Breakup / Docket Archival", "day_offset": 14, **self.generate_followup_message(acc_id, step=4)}
        ]
        return {
            "account_id": acc_id,
            "company_name": acc["company_name"],
            "demurrage_exposure_usd": acc["demurrage_exposure_usd"],
            "current_stage": acc["stage"],
            "touches": touches
        }

    def generate_batch_followups(self, step: int = 2, limit: int = 10) -> List[Dict[str, Any]]:
        accounts = self.crm.list_accounts()
        results = []
        for acc in accounts[:limit]:
            results.append(self.generate_followup_message(acc["account_id"], step=step))
        return results

if __name__ == "__main__":
    engine = FollowUpEngine()
    sample = engine.generate_followup_message("TGT-01", step=2)
    print("Subject:", sample["subject"])
    print("\nBody:\n", sample["body"])

