"""
NEXUS-EXIM - FastAPI Backend & REST API Server
Exposes live endpoints for:
1. /api/exim/calculate-landed-cost
2. /api/exim/audit-documents
3. /api/exim/demurrage-risk
4. /api/exim/health
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from apex.projects.nexus_exim.core.customs_engine import NexusEximCustomsEngine
from apex.projects.nexus_exim.core.document_parser import NexusEximDocumentParser

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="NEXUS-EXIM Trade & Customs API",
        description="Autonomous Indian Customs (ICEGATE) EDI, 40% BCD Tariff & Demurrage Mitigation API",
        version="26.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    engine = NexusEximCustomsEngine()
    parser = NexusEximDocumentParser()

    class LandedCostRequest(BaseModel):
        invoice_value_usd: float
        exchange_rate_inr: float = 83.50
        incoterm: str = "FOB"
        freight_usd: float = 3200.0
        insurance_usd: float = 450.0
        bcd_rate_pct: float = 40.0
        igst_rate_pct: float = 18.0

    class DiscrepancyAuditRequest(BaseModel):
        invoice_text: str
        packing_list_quantity: int
        packing_list_hs_code: str

    @app.get("/api/exim/health")
    def health_check():
        return {"status": "OPERATIONAL", "service": "NEXUS-EXIM", "version": "26.0", "ports_monitored": ["INWFD6", "INBLR4", "INNSA1", "INMAA1"]}

    @app.post("/api/exim/calculate-landed-cost")
    def calculate_landed_cost(req: LandedCostRequest):
        return engine.calculate_customs_landed_cost(
            invoice_value_usd=req.invoice_value_usd,
            exchange_rate_inr=req.exchange_rate_inr,
            incoterm=req.incoterm,
            freight_usd=req.freight_usd,
            insurance_usd=req.insurance_usd,
            bcd_rate_pct=req.bcd_rate_pct,
            igst_rate_pct=req.igst_rate_pct
        )

    @app.post("/api/exim/audit-documents")
    def audit_documents(req: DiscrepancyAuditRequest):
        inv_data = parser.parse_shipping_bill_text(req.invoice_text)
        pack_data = {"quantity": req.packing_list_quantity, "hs_code": req.packing_list_hs_code}
        audit_result = parser.audit_trade_discrepancies(inv_data, pack_data)
        return {
            "parsed_invoice": inv_data,
            "audit_verdict": audit_result
        }

    @app.get("/api/exim/demurrage-risk")
    def get_demurrage_risk(days_at_port: int = 18, free_days: int = 14):
        return engine.evaluate_demurrage_risk(free_days_allowed=free_days, days_at_port=days_at_port)

def start_server(port: int = 8081):
    if FASTAPI_AVAILABLE:
        print(f"[NEXUS-EXIM] Starting REST API Gateway on http://127.0.0.1:{port}")
        uvicorn.run(app, host="127.0.0.1", port=port)
    else:
        print("[NEXUS-EXIM] FastAPI/Uvicorn not found. Native Python engine verified.")

if __name__ == "__main__":
    start_server()
