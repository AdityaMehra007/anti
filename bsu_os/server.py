"""BSU OS Production FastAPI Web Server & REST API.

Provides unified endpoints for the Bengaluru Startup Universe Super-App,
serving JSON API responses and mounting the interactive client dashboard.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bsu_os.config import STATIC_DIR
from bsu_os.database import (
    get_connection,
    get_all_startups,
    get_startup_by_id,
    init_db
)
from bsu_os.search_engine import super_search
from bsu_os.geo_clusters import get_cluster_intelligence, get_cluster_details
from bsu_os.copilot_engine import CopilotEngine
from bsu_os.war_rooms import (
    get_founder_war_room,
    get_investor_war_room,
    get_career_war_room,
    get_recruiter_war_room,
    get_ecosystem_command_center
)
from bsu_os.alerts_engine import (
    add_to_watchlist,
    remove_from_watchlist,
    get_user_watchlist,
    get_recent_alerts,
    generate_daily_brief
)
from bsu_os.scoring_engine import recompute_all_scores

app = FastAPI(
    title="Bengaluru Startup Universe (BSU OS)",
    description="The complete digital operating system and intelligence layer for Bengaluru's startup ecosystem.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

copilot = CopilotEngine()

# Mount Static directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def on_startup():
    """Ensure database schema is verified upon startup."""
    init_db()


@app.get("/")
def serve_index():
    """Serves the main application dashboard."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "BSU OS Server Running. Static dashboard not yet built."}


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "BSU OS", "version": "1.0.0"}


# Startups & Directory Endpoints

@app.get("/api/startups")
def list_startups(
    sector: Optional[str] = None,
    stage: Optional[str] = None,
    cluster_id: Optional[str] = None,
    min_power_score: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
):
    """Lists startups with optional filters, sorted by Power Score."""
    return get_all_startups(
        sector=sector,
        stage=stage,
        cluster_id=cluster_id,
        min_power_score=min_power_score,
        limit=limit,
        offset=offset
    )


@app.get("/api/startups/{startup_id}")
def get_startup(startup_id: int):
    """Retrieves single startup with founders, funding rounds, and jobs."""
    startup = get_startup_by_id(startup_id, hydrate=True)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup


# Jobs & Career Endpoints

@app.get("/api/jobs")
def list_jobs(
    department: Optional[str] = None,
    cluster_id: Optional[str] = None,
    limit: int = 50
):
    """Lists open jobs across Bengaluru startups."""
    conn = get_connection()
    clauses = ["j.is_active = 1"]
    params: Dict[str, Any] = {"limit": limit}

    if department:
        clauses.append("j.department = :department")
        params["department"] = department
    if cluster_id:
        clauses.append("j.location_cluster_id = :cluster_id")
        params["cluster_id"] = cluster_id

    where_sql = " AND ".join(clauses)
    query = f"""
    SELECT j.*, s.name AS startup_name, s.slug AS startup_slug, s.logo_url, s.power_score
    FROM jobs j
    JOIN startups s ON j.startup_id = s.id
    WHERE {where_sql}
    ORDER BY j.career_score DESC, j.max_salary_lpa DESC
    LIMIT :limit
    """
    rows = conn.execute(query, params).fetchall()
    jobs = []
    import json
    for r in rows:
        d = dict(r)
        d["skills_required"] = json.loads(d["skills_required"]) if d["skills_required"] else []
        jobs.append(d)
    conn.close()
    return jobs


# Investors & Events Endpoints

@app.get("/api/investors")
def list_investors():
    """Lists marquee venture funds and institutional investors."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM investors ORDER BY aum_usd DESC").fetchall()
    conn.close()
    import json
    results = []
    for r in rows:
        d = dict(r)
        d["key_investments"] = json.loads(d["key_investments"]) if d["key_investments"] else []
        results.append(d)
    return results


@app.get("/api/events")
def list_events():
    """Lists ecosystem meetups, hackathons, and conferences."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM events ORDER BY date_time ASC").fetchall()
    conn.close()
    import json
    results = []
    for r in rows:
        d = dict(r)
        d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        results.append(d)
    return results


# Clusters & Spatial Intelligence

@app.get("/api/clusters")
def list_clusters():
    """Returns spatial metrics for all Bengaluru micro-clusters."""
    return get_cluster_intelligence()


@app.get("/api/clusters/{cluster_id}")
def get_cluster(cluster_id: str):
    """Retrieves deep profile for a specific micro-cluster."""
    details = get_cluster_details(cluster_id)
    if not details:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return details


# Super Search Endpoint

@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = 25):
    """Global Super Search across all entities."""
    return super_search(q, limit=limit)


# Multi-Agent Copilot Endpoint

class CopilotQueryRequest(BaseModel):
    query: str
    mode: str = "general"


@app.post("/api/copilot/query")
def copilot_query_endpoint(req: CopilotQueryRequest):
    """Submits a natural language ecosystem query to the Multi-Agent Copilot."""
    return copilot.query(req.query, mode=req.mode)


# War Rooms Telemetry

@app.get("/api/war-rooms/{room_name}")
def get_war_room(room_name: str):
    """Retrieves real-time intelligence for the specified War Room."""
    room = room_name.lower().strip()
    if room == "founder":
        return get_founder_war_room()
    elif room == "investor":
        return get_investor_war_room()
    elif room == "career":
        return get_career_war_room()
    elif room == "recruiter":
        return get_recruiter_war_room()
    elif room in ["command", "ecosystem"]:
        return get_ecosystem_command_center()
    else:
        raise HTTPException(status_code=400, detail=f"Unknown war room '{room_name}'. Valid: founder, investor, career, recruiter, command")


# Daily Brief & Alerts

@app.get("/api/daily-brief")
def get_daily_brief_endpoint():
    """Returns today's Daily Intelligence Briefing."""
    return generate_daily_brief()


@app.get("/api/alerts")
def get_alerts_endpoint(limit: int = 20):
    """Returns recent ecosystem alerts."""
    return get_recent_alerts(limit=limit)


# Watchlists

class WatchlistRequest(BaseModel):
    user_id: str = "guest_default"
    entity_type: str
    entity_id: int
    notes: Optional[str] = ""


@app.get("/api/watchlists")
def get_watchlists_endpoint(user_id: str = "guest_default"):
    """Returns user watchlist."""
    return get_user_watchlist(user_id=user_id)


@app.post("/api/watchlists")
def add_watchlist_endpoint(req: WatchlistRequest):
    """Adds entity to watchlist."""
    ok = add_to_watchlist(req.user_id, req.entity_type, req.entity_id, req.notes or "")
    return {"success": ok}


@app.delete("/api/watchlists/{entity_type}/{entity_id}")
def delete_watchlist_endpoint(entity_type: str, entity_id: int, user_id: str = "guest_default"):
    """Removes entity from watchlist."""
    ok = remove_from_watchlist(user_id, entity_type, entity_id)
    return {"success": ok}


@app.post("/api/recompute-scores")
def recompute_scores_endpoint():
    """Triggers re-calculation of all mathematical ecosystem scores."""
    count = recompute_all_scores()
    return {"recomputed_count": count}
