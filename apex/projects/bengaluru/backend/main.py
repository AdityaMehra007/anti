"""
APEX BENGALURU - FastAPI REST & WebSocket Backend Gateway
Serves City Digital Twin, Signals, GCCs, Startups, Career Matching, and Business Factory APIs.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "apex" / "projects" / "bengaluru"))

from core.digital_twin import BengaluruDigitalTwin
from core.signal_engine import BengaluruSignalEngine
from core.career_os import BengaluruCareerOS
from core.business_factory import BengaluruBusinessFactory

app = FastAPI(title="APEX Bengaluru City-Scale AI Platform", version="26.0.0")

twin = BengaluruDigitalTwin()
signals = BengaluruSignalEngine()
career = BengaluruCareerOS()
business = BengaluruBusinessFactory()

class CareerMatchRequest(BaseModel):
    degree: str
    skills: List[str]
    experience_level: str = "FRESHER"

class AutomationRoiRequest(BaseModel):
    process_name: str
    manual_hours_month: float
    hourly_cost_inr: float = 1200.0

@app.get("/api/health")
def get_health() -> Dict[str, Any]:
    return {"status": "OPERATIONAL", "platform": "APEX_BENGALURU", "version": "26.0.0"}

@app.get("/api/kpis")
def get_kpis() -> Dict[str, Any]:
    return twin.get_city_macro_kpis()

@app.get("/api/signals")
def get_signals(limit: int = 10) -> List[Dict[str, Any]]:
    return signals.get_latest_signals(limit=limit)

@app.get("/api/companies")
def get_companies(category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    return twin.query_companies(category=category, limit=limit)

@app.get("/api/gccs")
def get_gccs() -> List[Dict[str, Any]]:
    return twin.query_gcc_momentum()

@app.get("/api/startups")
def get_startups(sector: Optional[str] = None) -> List[Dict[str, Any]]:
    return twin.query_startups(sector=sector)

@app.get("/api/markets")
def get_markets() -> List[Dict[str, Any]]:
    return twin.query_micro_markets()

@app.post("/api/career/match")
def post_career_match(req: CareerMatchRequest) -> List[Dict[str, Any]]:
    return career.match_user_profile(req.degree, req.skills, req.experience_level)

@app.get("/api/career/interview-prep")
def get_interview_prep(company: str = "Walmart Global Tech", role: str = "International Supply Chain Analyst") -> Dict[str, Any]:
    return career.generate_interview_prep(company, role)

@app.get("/api/business/opportunity")
def get_business_opportunity(domain: str = "Cross-border trade logistics") -> Dict[str, Any]:
    return business.evaluate_startup_opportunity(domain)

@app.post("/api/automation/roi")
def post_automation_roi(req: AutomationRoiRequest) -> Dict[str, Any]:
    return business.compute_enterprise_automation_roi(req.process_name, req.manual_hours_month, req.hourly_cost_inr)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
