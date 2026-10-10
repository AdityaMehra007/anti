"""BSU OS Relational SQLite Storage Engine.

Handles schema migrations, transactional persistence, foreign key integrity,
and optimized index access for Bengaluru tech entities.
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional
from bsu_os.config import DATABASE_PATH


def get_connection(db_path=None) -> sqlite3.Connection:
    """Creates a configured connection with row factory and foreign keys enabled."""
    target_path = db_path or DATABASE_PATH
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db(db_path=None) -> None:
    """Initializes tables, indices, and constraints."""
    conn = get_connection(db_path)
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS clusters (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            zoom INTEGER NOT NULL,
            primary_sectors TEXT NOT NULL, -- JSON array
            vibe TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS startups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE,
            sector TEXT NOT NULL,
            sub_sector TEXT NOT NULL,
            stage TEXT NOT NULL,
            founded_year INTEGER NOT NULL,
            cluster_id TEXT NOT NULL,
            location_address TEXT NOT NULL,
            website_url TEXT NOT NULL,
            logo_url TEXT,
            elevator_pitch TEXT NOT NULL,
            full_description TEXT NOT NULL,
            headcount INTEGER NOT NULL,
            hiring_status INTEGER NOT NULL DEFAULT 1,
            tech_stack TEXT NOT NULL, -- JSON array
            tags TEXT NOT NULL,       -- JSON array
            verified_status INTEGER NOT NULL DEFAULT 1,
            power_score REAL NOT NULL DEFAULT 0.0,
            career_score REAL NOT NULL DEFAULT 0.0,
            momentum_score REAL NOT NULL DEFAULT 0.0,
            risk_score REAL NOT NULL DEFAULT 0.0,
            future_potential_score REAL NOT NULL DEFAULT 0.0,
            total_funding_usd REAL NOT NULL DEFAULT 0.0,
            latest_valuation_usd REAL,
            FOREIGN KEY (cluster_id) REFERENCES clusters (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS founders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            bio TEXT NOT NULL,
            linkedin_url TEXT,
            twitter_url TEXT,
            prior_exits INTEGER NOT NULL DEFAULT 0,
            educational_background TEXT,
            verified_status INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (startup_id) REFERENCES startups (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS investors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            firm_name TEXT NOT NULL,
            investor_type TEXT NOT NULL,
            thesis TEXT NOT NULL,
            aum_usd REAL,
            key_investments TEXT NOT NULL, -- JSON array
            cluster_id TEXT NOT NULL,
            website_url TEXT,
            verified_status INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (cluster_id) REFERENCES clusters (id)
        );

        CREATE TABLE IF NOT EXISTS funding_rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            round_name TEXT NOT NULL,
            amount_usd REAL NOT NULL,
            round_date TEXT NOT NULL,
            lead_investors TEXT NOT NULL, -- JSON array
            valuation_usd REAL,
            source_url TEXT,
            FOREIGN KEY (startup_id) REFERENCES startups (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            employment_type TEXT NOT NULL DEFAULT 'Full-time',
            experience_level TEXT NOT NULL DEFAULT 'Mid-Senior',
            location_cluster_id TEXT NOT NULL,
            remote_policy TEXT NOT NULL DEFAULT 'In-office / Hybrid',
            min_salary_lpa REAL,
            max_salary_lpa REAL,
            skills_required TEXT NOT NULL, -- JSON array
            description TEXT NOT NULL,
            apply_url TEXT,
            career_score REAL NOT NULL DEFAULT 75.0,
            posted_date TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (startup_id) REFERENCES startups (id) ON DELETE CASCADE,
            FOREIGN KEY (location_cluster_id) REFERENCES clusters (id)
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_type TEXT NOT NULL,
            date_time TEXT NOT NULL,
            location_cluster_id TEXT NOT NULL,
            venue_name TEXT NOT NULL,
            organizer TEXT NOT NULL,
            registration_url TEXT,
            tags TEXT NOT NULL, -- JSON array
            is_featured INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (location_cluster_id) REFERENCES clusters (id)
        );

        CREATE TABLE IF NOT EXISTS watchlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL DEFAULT 'guest_default',
            entity_type TEXT NOT NULL, -- 'startup', 'job', 'investor'
            entity_id INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, entity_type, entity_id)
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT NOT NULL,
            headline TEXT NOT NULL,
            summary TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            cluster_id TEXT,
            severity TEXT NOT NULL DEFAULT 'HIGH',
            created_at TEXT NOT NULL
        );

        -- Performance Indices
        CREATE INDEX IF NOT EXISTS idx_startups_cluster ON startups (cluster_id);
        CREATE INDEX IF NOT EXISTS idx_startups_sector ON startups (sector);
        CREATE INDEX IF NOT EXISTS idx_startups_stage ON startups (stage);
        CREATE INDEX IF NOT EXISTS idx_startups_power_score ON startups (power_score DESC);
        CREATE INDEX IF NOT EXISTS idx_jobs_startup ON jobs (startup_id);
        CREATE INDEX IF NOT EXISTS idx_jobs_cluster ON jobs (location_cluster_id);
        CREATE INDEX IF NOT EXISTS idx_founders_startup ON founders (startup_id);
        CREATE INDEX IF NOT EXISTS idx_funding_startup ON funding_rounds (startup_id);
        """)
    conn.close()


# Startup CRUD Operations

def insert_startup(data: Dict[str, Any], conn: Optional[sqlite3.Connection] = None) -> int:
    """Inserts a startup and returns its autoincrement ID."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    query = """
    INSERT INTO startups (
        name, slug, sector, sub_sector, stage, founded_year, cluster_id,
        location_address, website_url, logo_url, elevator_pitch, full_description,
        headcount, hiring_status, tech_stack, tags, verified_status,
        power_score, career_score, momentum_score, risk_score, future_potential_score,
        total_funding_usd, latest_valuation_usd
    ) VALUES (
        :name, :slug, :sector, :sub_sector, :stage, :founded_year, :cluster_id,
        :location_address, :website_url, :logo_url, :elevator_pitch, :full_description,
        :headcount, :hiring_status, :tech_stack, :tags, :verified_status,
        :power_score, :career_score, :momentum_score, :risk_score, :future_potential_score,
        :total_funding_usd, :latest_valuation_usd
    )
    """
    row_data = dict(data)
    if isinstance(row_data.get("tech_stack"), list):
        row_data["tech_stack"] = json.dumps(row_data["tech_stack"])
    if isinstance(row_data.get("tags"), list):
        row_data["tags"] = json.dumps(row_data["tags"])

    cursor = conn.execute(query, row_data)
    startup_id = cursor.lastrowid
    if close_after:
        conn.commit()
        conn.close()
    return startup_id


def get_all_startups(
    sector: Optional[str] = None,
    stage: Optional[str] = None,
    cluster_id: Optional[str] = None,
    min_power_score: Optional[float] = None,
    limit: int = 100,
    offset: int = 0,
    conn: Optional[sqlite3.Connection] = None
) -> List[Dict[str, Any]]:
    """Retrieves startups with optional filters, sorted by Power Score descending."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    clauses = ["1=1"]
    params: Dict[str, Any] = {"limit": limit, "offset": offset}

    if sector:
        clauses.append("sector = :sector")
        params["sector"] = sector
    if stage:
        clauses.append("stage = :stage")
        params["stage"] = stage
    if cluster_id:
        clauses.append("cluster_id = :cluster_id")
        params["cluster_id"] = cluster_id
    if min_power_score is not None:
        clauses.append("power_score >= :min_power_score")
        params["min_power_score"] = min_power_score

    where_sql = " AND ".join(clauses)
    query = f"""
    SELECT * FROM startups
    WHERE {where_sql}
    ORDER BY power_score DESC, total_funding_usd DESC
    LIMIT :limit OFFSET :offset
    """
    rows = conn.execute(query, params).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["tech_stack"] = json.loads(d["tech_stack"]) if d["tech_stack"] else []
        d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        result.append(d)

    if close_after:
        conn.close()
    return result


def get_startup_by_id(startup_id: int, hydrate: bool = True, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    """Retrieves a single startup with nested founders, funding, and jobs."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    row = conn.execute("SELECT * FROM startups WHERE id = ?", (startup_id,)).fetchone()
    if not row:
        if close_after:
            conn.close()
        return None

    startup = dict(row)
    startup["tech_stack"] = json.loads(startup["tech_stack"]) if startup["tech_stack"] else []
    startup["tags"] = json.loads(startup["tags"]) if startup["tags"] else []

    if hydrate:
        # Founders
        f_rows = conn.execute("SELECT * FROM founders WHERE startup_id = ?", (startup_id,)).fetchall()
        startup["founders"] = [dict(f) for f in f_rows]
        # Funding Rounds
        fr_rows = conn.execute("SELECT * FROM funding_rounds WHERE startup_id = ? ORDER BY round_date DESC", (startup_id,)).fetchall()
        funding = []
        for fr in fr_rows:
            f_dict = dict(fr)
            f_dict["lead_investors"] = json.loads(f_dict["lead_investors"]) if f_dict["lead_investors"] else []
            funding.append(f_dict)
        startup["funding_rounds"] = funding
        # Jobs
        j_rows = conn.execute("SELECT * FROM jobs WHERE startup_id = ? AND is_active = 1", (startup_id,)).fetchall()
        jobs = []
        for j in j_rows:
            j_dict = dict(j)
            j_dict["skills_required"] = json.loads(j_dict["skills_required"]) if j_dict["skills_required"] else []
            jobs.append(j_dict)
        startup["open_jobs"] = jobs

    if close_after:
        conn.close()
    return startup


def update_startup_scores(startup_id: int, scores: Dict[str, float], conn: Optional[sqlite3.Connection] = None) -> None:
    """Updates computed scores for a startup."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    query = """
    UPDATE startups SET
        power_score = :power_score,
        career_score = :career_score,
        momentum_score = :momentum_score,
        risk_score = :risk_score,
        future_potential_score = :future_potential_score
    WHERE id = :startup_id
    """
    params = {
        "startup_id": startup_id,
        "power_score": scores.get("power_score", 0.0),
        "career_score": scores.get("career_score", 0.0),
        "momentum_score": scores.get("momentum_score", 0.0),
        "risk_score": scores.get("risk_score", 0.0),
        "future_potential_score": scores.get("future_potential_score", 0.0),
    }
    conn.execute(query, params)
    if close_after:
        conn.commit()
        conn.close()
