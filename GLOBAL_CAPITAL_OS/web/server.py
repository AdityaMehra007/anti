"""FastAPI Backend Server for GLOBAL CAPITAL OS Command Center.

Exposes REST APIs for financial telemetry, treasury maps, sales CRM pipelines,
consequential action approvals, and 13-dimension master health scores.
"""

from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..core.config import settings
from ..core.models import CurrencyCode, SalesStage
from ..core.security import security
from ..core.database import db
from ..agents.capital_commander import capital_commander
from ..agents.revenue_commander import revenue_commander
from ..agents.treasury_commander import treasury_commander
from ..agents.cfo_agent import cfo_agent
from ..agents.risk_agent import risk_agent
from ..agents.audit_agent import audit_agent
from ..agents.founder_chief_of_staff import founder_chief_of_staff
from ..agents.security_agent import security_agent
from ..engines.opportunity_database import opportunity_db
from ..engines.first_rupee_ladder import rupee_ladder
from ..engines.global_money_map import global_money_map
from ..engines.reconciliation_engine import reconciliation_engine
from ..engines.scoring_engine import scoring_engine
from ..experiments.exp01_b2b_intelligence import exp01

app = FastAPI(
    title="GLOBAL CAPITAL OS",
    description="Founder Capital Engine - Autonomous Revenue, Treasury & Wealth Operating System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class DecisionPayload(BaseModel):
    decision: str
    notes: Optional[str] = None


class DealAdvancePayload(BaseModel):
    new_stage: str
    notes: Optional[str] = None


class RevenueRecordPayload(BaseModel):
    client_name: str
    amount_usd: float = 0.0
    amount_inr: float
    service_description: str


class FreezePayload(BaseModel):
    reason: str


class UnfreezePayload(BaseModel):
    founder_override: str


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>GLOBAL CAPITAL OS Active</h1><p>Dashboard UI loading...</p>")


@app.get("/api/telemetry")
async def get_telemetry():
    posture = capital_commander.get_master_financial_posture()
    scores = scoring_engine.compute_all_scores()
    ladder = rupee_ladder.get_current_stage(posture["revenue_mtd_inr"])
    is_frozen = security.is_system_frozen()

    return {
        "posture": posture,
        "scores": scores,
        "ladder": ladder,
        "is_system_frozen": is_frozen,
        "operator": settings.FOUNDER_NAME,
        "home_base": settings.BASE_CITY
    }


@app.get("/api/treasury")
async def get_treasury():
    return treasury_commander.get_treasury_map()


@app.get("/api/revenue/pipeline")
async def get_revenue_pipeline():
    return revenue_commander.get_pipeline_summary()


@app.get("/api/revenue/deals")
async def get_active_deals():
    with db.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.id, d.lead_id, d.deal_name, d.stage, d.deal_value_inr, d.deal_value_usd,
                   d.win_probability, d.expected_value_inr, d.next_step, l.company_name, l.contact_name
            FROM deals d
            LEFT JOIN leads l ON d.lead_id = l.id
            ORDER BY d.expected_value_inr DESC
        """)
        return [dict(r) for r in cur.fetchall()]


@app.post("/api/revenue/deals/{deal_id}/advance")
async def advance_deal(deal_id: str, payload: DealAdvancePayload):
    try:
        stage_enum = SalesStage(payload.new_stage.upper())
        return revenue_commander.advance_deal_stage(deal_id, stage_enum, payload.notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/revenue/collect")
async def collect_revenue(payload: RevenueRecordPayload):
    try:
        return revenue_commander.record_collected_revenue(
            client_name=payload.client_name,
            amount_usd=payload.amount_usd,
            amount_inr=payload.amount_inr,
            service_description=payload.service_description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/approvals")
async def get_approvals():
    return founder_chief_of_staff.get_pending_approvals()


@app.post("/api/approvals/{approval_id}/decide")
async def decide_approval(approval_id: str, payload: DecisionPayload):
    try:
        return founder_chief_of_staff.resolve_approval(approval_id, payload.decision, payload.notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/daily-brief")
async def get_daily_brief():
    return founder_chief_of_staff.generate_daily_brief()


@app.get("/api/pl-statement")
async def get_pl_statement(period_days: int = 30):
    return cfo_agent.generate_pl_statement(period_days=period_days)


@app.get("/api/daily-profit")
async def get_daily_profit():
    return cfo_agent.generate_pl_statement(period_days=1)


@app.get("/api/stress-scenarios")
async def get_stress_scenarios():
    return risk_agent.run_stress_scenarios()


@app.get("/api/opportunities")
async def get_top_opportunities():
    return opportunity_db.get_top_opportunities(limit=15)


@app.get("/api/global-money-map")
async def get_money_map():
    return global_money_map.get_all_infrastructure()


@app.get("/api/reconciliation")
async def get_reconciliation():
    return reconciliation_engine.execute_three_way_reconciliation()


@app.get("/api/experiment-01")
async def get_experiment_details():
    details = exp01.get_experiment_details()
    prospects = exp01.get_priority_campaign_prospects()
    return {"details": details, "prospects": prospects}


@app.post("/api/security/freeze")
async def trigger_freeze(payload: FreezePayload):
    return security_agent.emergency_freeze(payload.reason)


@app.post("/api/security/unfreeze")
async def release_freeze(payload: UnfreezePayload):
    try:
        return security.release_emergency_freeze(payload.founder_override)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
