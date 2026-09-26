"""
OMNIMONEY OS - Production FastAPI REST API Server
Exposes complete economic intelligence, CRM pipelines, agent swarm, and morning brief.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine, LeadStatus, Prospect
from omnimoney.agent_workforce import AgentWorkforceSwarm
from omnimoney.morning_brief import MorningBriefEngine
from omnimoney.business_generator import BusinessGenerator
from omnimoney.prospect_miner import ProspectMiner
from omnimoney.outreach_vault import OutreachVault
from omnimoney.invoicing_engine import InvoicingEngine
from omnimoney.dispatcher import OutreachDispatcher

app = FastAPI(
    title="OMNIMONEY OS API",
    description="Economic Opportunity, B2B Cash Flow & Capital Compounding Engine",
    version="1.0.0"
)

# Enable CORS for local dashboards and browser automations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
engine = OmniMoneyEngine()
sales = B2BSalesEngine()
swarm = AgentWorkforceSwarm()
brief_engine = MorningBriefEngine(engine, sales)
biz_gen = BusinessGenerator()
miner = ProspectMiner()
vault = OutreachVault()
invoicing = InvoicingEngine()
dispatcher = OutreachDispatcher()

# Pydantic Request Models
class NewLeadRequest(BaseModel):
    business_name: str
    category: str
    location: str
    contact_person: str
    phone: str
    email: str
    website: str
    notes: str
    deal_value_inr: float

class UpdateLeadStatusRequest(BaseModel):
    lead_id: str
    new_status: str
    notes: Optional[str] = None

class GenerateAuditRequest(BaseModel):
    template_type: str
    prospect_name: str
    business_name: str

class GenerateBusinessRequest(BaseModel):
    vertical: str

@app.get("/")
def read_root():
    return {
        "system": "OMNIMONEY OS",
        "version": "1.0.0",
        "docs_url": "/docs",
        "cockpit_file": "OMNIMONEY_RADAR_BENGALURU.html",
        "status": "ONLINE"
    }

@app.get("/api/status")
def get_system_status():
    db_stats = engine.get_db_stats()
    swarm_status = swarm.run_swarm_cycle()
    return {
        "database": db_stats,
        "swarm": swarm_status
    }

@app.get("/api/today")
def get_today_action():
    """Answers Section 153 directive."""
    action = engine.get_highest_probability_action()
    return action.__dict__

@app.get("/api/opportunities")
def get_opportunities(limit: int = 10):
    opps = engine.get_ranked_opportunities(limit=limit)
    return [o.__dict__ for o in opps]

@app.get("/api/services")
def get_services():
    return engine.get_monetizable_services()

@app.get("/api/categories")
def get_categories():
    return engine.get_bengaluru_customer_categories()

@app.get("/api/crm/prospects")
def get_crm_prospects():
    summary = sales.get_pipeline_summary()
    prospects = [p.__dict__ for p in sales.get_prospects()]
    return {
        "summary": summary,
        "prospects": prospects
    }

@app.post("/api/crm/prospects")
def create_crm_prospect(req: NewLeadRequest):
    import datetime
    new_id = f"LEAD-{len(sales.get_prospects()) + 1:03d}"
    p = Prospect(
        id=new_id,
        business_name=req.business_name,
        category=req.category,
        location=req.location,
        contact_person=req.contact_person,
        phone=req.phone,
        email=req.email,
        website=req.website,
        status=LeadStatus.NEW,
        notes=req.notes,
        deal_value_inr=req.deal_value_inr,
        last_activity=datetime.date.today().isoformat()
    )
    sales._prospects.append(p)
    return {"success": True, "lead": p.__dict__}

@app.post("/api/crm/update-status")
def update_lead_status(req: UpdateLeadStatusRequest):
    try:
        st = LeadStatus(req.new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {req.new_status}")

    updated = sales.update_status(req.lead_id, st, req.notes)
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"success": True, "lead_id": req.lead_id, "new_status": req.new_status}

@app.post("/api/generate-audit")
def generate_audit(req: GenerateAuditRequest):
    script = sales.generate_outreach_script(req.template_type, req.prospect_name, req.business_name)
    return {"success": True, "script": script}

@app.get("/api/agents")
def get_agents():
    return swarm.get_all_agents()

@app.post("/api/agents/cycle")
def run_agent_cycle():
    return swarm.run_swarm_cycle()

@app.get("/api/morning-brief")
def get_morning_brief():
    return brief_engine.generate_brief()

@app.post("/api/business/generate")
def generate_business_blueprint(req: GenerateBusinessRequest):
    bp = biz_gen.generate_blueprint(req.vertical)
    return bp.__dict__

@app.get("/api/prospects/mine")
def api_prospects_mine(limit: int = 50, sector: Optional[str] = None, corridor: Optional[str] = None):
    if sector:
        return miner.mine_by_sector(sector, limit)
    elif corridor:
        return miner.mine_by_corridor(corridor, limit)
    else:
        return miner.mine_high_value_prospects(limit)

@app.get("/api/prospects/sectors")
def api_prospects_sectors():
    return miner.get_available_sectors()

@app.get("/api/outreach/stats")
def get_outreach_stats():
    return vault.get_vault_stats()

@app.get("/api/outreach/queue")
def get_outreach_queue(batch_size: int = 10):
    return vault.get_daily_dispatch_queue(batch_size)

@app.get("/api/outreach/metrics")
def get_outreach_metrics():
    return vault.get_conversion_metrics()

@app.get("/api/outreach/drafted")
def get_drafted_outreach(limit: int = 20):
    return vault.get_drafted_outreach(limit)

class MarkSentRequest(BaseModel):
    record_id: str

class MarkResponseRequest(BaseModel):
    record_id: str
    response: str
    notes: str = ""

@app.post("/api/outreach/mark-sent")
def mark_outreach_sent(req: MarkSentRequest):
    success = vault.mark_sent(req.record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"success": True, "record_id": req.record_id, "new_status": "SENT"}

@app.post("/api/outreach/mark-response")
def mark_outreach_response(req: MarkResponseRequest):
    success = vault.mark_response(req.record_id, req.response, req.notes)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"success": True, "record_id": req.record_id, "response": req.response}

class GenerateInvoiceRequest(BaseModel):
    client_name: str
    client_company: str
    client_email: str
    service_name: str
    amount_inr: float
    gst_included: bool = False
    upi_id: str = "adityamehra@okaxis"

@app.post("/api/invoicing/generate")
def api_generate_invoice(req: GenerateInvoiceRequest):
    return invoicing.generate_b2b_invoice(
        client_name=req.client_name,
        client_company=req.client_company,
        client_email=req.client_email,
        service_name=req.service_name,
        amount_inr=req.amount_inr,
        gst_included=req.gst_included,
        upi_id=req.upi_id
    )

@app.post("/api/dispatch/prepare")
def api_prepare_dispatch(batch_size: int = 10):
    return dispatcher.prepare_daily_dispatch_batch(batch_size=batch_size)

@app.get("/api/scorecard")
def api_get_scorecard():
    from omnimoney.scoring_system import compute_master_scorecard
    return compute_master_scorecard()


