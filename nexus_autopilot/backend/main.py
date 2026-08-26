"""
NEXUS AUTOPILOT - FastAPI REST & WebSocket Backend Gateway
Exposes APIs for WhatsApp webhooks, Financial Snapshots, Invoices, Razorpay Payments, and Agent Control Plane.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "nexus_autopilot"))

from core.whatsapp_parser import WhatsAppCommandParser
from core.finance_engine import NexusFinanceEngine
from core.agent_system import NexusAgentSystem
from core.razorpay_gateway import RazorpayGateway

app = FastAPI(title="NEXUS AUTOPILOT Backend Gateway", version="26.0.0")

parser = WhatsAppCommandParser()
finance = NexusFinanceEngine()
agents = NexusAgentSystem()
razorpay = RazorpayGateway()

class WhatsAppMessageRequest(BaseModel):
    org_id: str = "ORG-ABC-001"
    sender_phone: str
    message_text: str

class WebhookPaymentRequest(BaseModel):
    org_id: str = "ORG-ABC-001"
    invoice_id: str
    razorpay_payment_id: str
    amount_inr: float

@app.get("/api/health")
def get_health() -> Dict[str, Any]:
    return {"status": "OPERATIONAL", "platform": "NEXUS_AUTOPILOT", "version": "26.0.0"}

@app.get("/api/finance/snapshot")
def get_financial_snapshot(org_id: str = "ORG-ABC-001") -> Dict[str, Any]:
    return finance.get_executive_financial_snapshot(org_id)

@app.get("/api/finance/receivables")
def get_receivables(org_id: str = "ORG-ABC-001") -> List[Dict[str, Any]]:
    return finance.get_receivables_risk_report(org_id)

@app.post("/api/whatsapp/command")
def post_whatsapp_command(req: WhatsAppMessageRequest) -> Dict[str, Any]:
    parsed = parser.parse_command(req.message_text)
    perm = agents.evaluate_action_permission("CEO_Agent", parsed["intent"], parsed.get("entities", {}).get("total_amount", 0.0))
    
    # Audit log
    agents.log_agent_audit_event(req.org_id, "CEO_Agent", parsed["intent"], f"Processed command: '{req.message_text}'", parsed)
    
    return {
        "input_text": req.message_text,
        "parsed_intent": parsed["intent"],
        "confidence": parsed["confidence"],
        "permission_check": perm,
        "entities": parsed.get("entities", {})
    }

@app.post("/api/payments/webhook")
def post_payment_webhook(req: WebhookPaymentRequest) -> Dict[str, Any]:
    res = razorpay.process_webhook_payment(req.org_id, req.invoice_id, req.razorpay_payment_id, req.amount_inr)
    agents.log_agent_audit_event(req.org_id, "Finance_Agent", "WEBHOOK_PAYMENT_RECONCILED", f"Reconciled ₹{req.amount_inr} for Invoice {req.invoice_id}", res)
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
