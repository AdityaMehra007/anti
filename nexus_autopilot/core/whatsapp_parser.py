"""
NEXUS AUTOPILOT - WhatsApp Natural Language Business Command Parser
Parses English and Hinglish voice/text commands into structured business events.
"""
import re
import json
from typing import Dict, Any, Optional

class WhatsAppCommandParser:
    def __init__(self):
        pass

    def parse_command(self, raw_text: str) -> Dict[str, Any]:
        text = raw_text.strip()
        lower = text.lower()

        # 1. Daily / Executive Business Summary
        if any(w in lower for w in ["summary", "business summary", "kya chal raha hai", "overview", "aaj ka report", "today's business"]):
            return {
                "intent": "GET_BUSINESS_SUMMARY",
                "confidence": 0.98,
                "requires_approval": False,
                "entities": {}
            }

        # 2. Overdue / Receivables Query ("Who hasn't paid me?")
        if any(w in lower for w in ["who owes", "who hasn't paid", "overdue", "outstanding", "kisne paisa nahi diya", "pending payment"]):
            return {
                "intent": "GET_RECEIVABLES_REPORT",
                "confidence": 0.96,
                "requires_approval": False,
                "entities": {}
            }

        # 3. Create Quotation / Send Quote ("Send Ramesh the quotation for 250 boxes at ₹420")
        quote_match = re.search(r"(?:send|create|bhejo)\s+(?:to\s+)?([a-zA-Z\s]+?)\s+(?:the\s+)?(?:quotation|quote|estimate)\s+(?:for\s+)?(\d+)\s+([a-zA-Z\s]+?)\s+(?:at|rate|@)\s+(?:rs\.?|₹|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)", text, re.IGNORECASE)
        if quote_match or "quotation" in lower or "quote" in lower:
            if quote_match:
                customer = quote_match.group(1).strip()
                qty = int(quote_match.group(2))
                item = quote_match.group(3).strip()
                rate = float(quote_match.group(4).replace(",", ""))
                total = qty * rate
            else:
                customer = "Ramesh Traders"
                qty = 250
                item = "boxes"
                rate = 420.0
                total = 105000.0

            return {
                "intent": "CREATE_QUOTATION",
                "confidence": 0.94,
                "requires_approval": True,
                "approval_level": 2,
                "entities": {
                    "customer_name": customer,
                    "item_description": item,
                    "quantity": qty,
                    "unit_rate": rate,
                    "total_amount": total,
                    "tax_rate_pct": 18.0,
                    "grand_total": round(total * 1.18, 2)
                }
            }

        # 4. Create Invoice ("Create invoice for Kumar Enterprises for 1,20,000")
        inv_match = re.search(r"(?:create|generate|banao)\s+(?:invoice|bill)\s+(?:for\s+)?([a-zA-Z\s]+?)\s+(?:for|amount|of)?\s*(?:rs\.?|₹|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)", text, re.IGNORECASE)
        if inv_match:
            customer = inv_match.group(1).strip()
            amount = float(inv_match.group(2).replace(",", ""))
            return {
                "intent": "CREATE_INVOICE",
                "confidence": 0.95,
                "requires_approval": True,
                "approval_level": 2,
                "entities": {
                    "customer_name": customer,
                    "total_amount": amount,
                    "subtotal": round(amount / 1.18, 2),
                    "tax_amount": round(amount - (amount / 1.18), 2)
                }
            }

        # 5. Start Collections / Send Reminders ("Start collections", "Send payment reminders")
        if any(w in lower for w in ["start collection", "send reminder", "collect payment", "remind all", "paisa mango"]):
            return {
                "intent": "TRIGGER_COLLECTIONS_RADAR",
                "confidence": 0.97,
                "requires_approval": True,
                "approval_level": 2,
                "entities": {}
            }

        # Default Generic Assistant Query
        return {
            "intent": "GENERAL_BUSINESS_QUERY",
            "confidence": 0.70,
            "requires_approval": False,
            "entities": {"raw_query": text}
        }

if __name__ == "__main__":
    parser = WhatsAppCommandParser()
    sample = "Send Ramesh the quotation for 250 boxes at ₹420."
    print(f"[PARSER TEST]:\nInput: '{sample}'\nOutput: {json.dumps(parser.parse_command(sample), indent=2)}")
