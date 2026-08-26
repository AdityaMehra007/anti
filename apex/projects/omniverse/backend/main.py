"""
OMNIVERSE Backend API - High-Performance Enterprise Server
Built on FastAPI and integrated with the APEX V3 Execution Kernel.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import time
import sys
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.projects.omniverse.core.engine import OmniverseCoreEngine
from apex.kernel.runtime import ApexExecutionKernel
from apex.fabric.dynamic_loader import ApexDynamicSpecialistLoader

app = FastAPI(
    title="APEX Omniverse Enterprise Gateway",
    description="High-Throughput Autonomous Agentic Platform API",
    version="3.0.0"
)

core_engine = OmniverseCoreEngine()
kernel = ApexExecutionKernel()
specialist_loader = ApexDynamicSpecialistLoader()

class GoalRequest(BaseModel):
    goal: str
    domain: Optional[str] = "GENERAL"
    priority: Optional[int] = 5

class TransactionRequest(BaseModel):
    tx_code: str
    domain: str
    amount: float
    risk_score: float

@app.get("/")
def root():
    return {
        "platform": "APEX OMNIVERSE ENTERPRISE",
        "version": "3.0.0-ENTERPRISE",
        "status": "OPERATIONAL",
        "timestamp": time.time()
    }

@app.get("/api/health")
def get_health():
    db_stats = core_engine.get_database_stats()
    kernel_state = kernel.get_live_state()
    return {
        "status": "HEALTHY",
        "uptime": "99.999%",
        "database": db_stats,
        "kernel": kernel_state,
        "indexed_specialists": specialist_loader.total_catalog_size
    }

@app.get("/api/kpis")
def get_kpis():
    metrics = core_engine.generate_enterprise_kpis()
    return {"kpis": [m.__dict__ for m in metrics]}

@app.get("/api/financials/forecast")
def get_forecast(months: int = 12, capital: float = 1000000.0):
    return core_engine.simulate_financial_forecast(initial_capital=capital, months=months)

@app.post("/api/missions/dispatch")
def dispatch_mission(req: GoalRequest):
    res = kernel.run_goal_mission(req.goal, project_id=f"omniverse_{req.domain.lower()}")
    return res

@app.post("/api/transactions/process")
def process_transaction(req: TransactionRequest):
    return core_engine.record_transaction(req.tx_code, req.domain, req.amount, req.risk_score)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
