"""
Database schema and storage operations for Hiring Intelligence OS.
Uses SQLite with WAL mode for speed and zero external dependencies.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).parent / "startups_intelligence.db"


def get_connection(db_file: Optional[Path] = None) -> sqlite3.Connection:
    target = db_file or DB_PATH
    conn = sqlite3.connect(str(target))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_file: Optional[Path] = None) -> None:
    conn = get_connection(db_file)
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS startups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE,
            domain TEXT NOT NULL,
            industry TEXT NOT NULL,
            stage TEXT NOT NULL,
            total_funding_usd INTEGER NOT NULL DEFAULT 0,
            last_round_type TEXT,
            valuation_usd INTEGER DEFAULT 0,
            lead_investors TEXT,
            headcount INTEGER DEFAULT 0,
            headcount_growth_6m_pct REAL DEFAULT 0.0,
            hq_location TEXT NOT NULL,
            remote_friendly INTEGER NOT NULL DEFAULT 1,
            careers_url TEXT NOT NULL,
            ats_provider TEXT NOT NULL,
            ats_endpoint TEXT NOT NULL,
            verified_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS open_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            seniority_level TEXT NOT NULL,
            salary_min_usd INTEGER DEFAULT 0,
            salary_max_usd INTEGER DEFAULT 0,
            equity_note TEXT,
            tech_stack TEXT NOT NULL,
            location TEXT NOT NULL,
            remote_type TEXT NOT NULL,
            direct_apply_url TEXT NOT NULL,
            urgency_score REAL DEFAULT 5.0,
            active_status INTEGER NOT NULL DEFAULT 1,
            batch_eligibility TEXT DEFAULT '2024 / 2025 / 2026 Batch',
            min_cgpa TEXT DEFAULT '60% or 6.0+ CGPA',
            test_pattern TEXT DEFAULT 'Aptitude + Technical DSA Coding + Technical Interview',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (startup_id) REFERENCES startups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS decision_makers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            linkedin_url TEXT,
            twitter_handle TEXT,
            verified_email TEXT,
            direct_pitch_hook TEXT,
            FOREIGN KEY (startup_id) REFERENCES startups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS hiring_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER NOT NULL,
            signal_type TEXT NOT NULL,
            source TEXT NOT NULL,
            signal_date TEXT NOT NULL,
            description TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            FOREIGN KEY (startup_id) REFERENCES startups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS outreach_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL,
            decision_maker_id INTEGER NOT NULL,
            channel TEXT NOT NULL,
            subject TEXT NOT NULL,
            message_body TEXT NOT NULL,
            status TEXT DEFAULT 'DRAFTED',
            follow_up_step INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES open_roles(id) ON DELETE CASCADE,
            FOREIGN KEY (decision_maker_id) REFERENCES decision_makers(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_startups_industry ON startups(industry);
        CREATE INDEX IF NOT EXISTS idx_startups_stage ON startups(stage);
        CREATE INDEX IF NOT EXISTS idx_startups_funding ON startups(total_funding_usd DESC);
        CREATE INDEX IF NOT EXISTS idx_roles_title ON open_roles(title);
        CREATE INDEX IF NOT EXISTS idx_roles_urgency ON open_roles(urgency_score DESC);
        CREATE INDEX IF NOT EXISTS idx_roles_tech ON open_roles(tech_stack);
        """)

        # Migration helper for existing databases
        for col, col_def in [
            ("batch_eligibility", "TEXT DEFAULT '2024, 2025, 2026 Batch'"),
            ("min_cgpa", "TEXT DEFAULT '60% or 6.0+ CGPA'"),
            ("test_pattern", "TEXT DEFAULT 'Aptitude + Technical DSA Coding'"),
        ]:
            try:
                conn.execute(f"ALTER TABLE open_roles ADD COLUMN {col} {col_def};")
            except sqlite3.OperationalError:
                pass
    conn.close()



def insert_startup(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM startups WHERE name = :name", {"name": data["name"]}).fetchone()
    if row:
        update_query = """
        UPDATE startups SET
            stage = :stage,
            total_funding_usd = :total_funding_usd,
            headcount = :headcount,
            careers_url = :careers_url,
            ats_endpoint = :ats_endpoint
        WHERE id = :id;
        """
        update_data = {**data, "id": row[0]}
        cur.execute(update_query, update_data)
        return row[0]

    insert_query = """
    INSERT INTO startups (
        name, slug, domain, industry, stage, total_funding_usd, last_round_type,
        valuation_usd, lead_investors, headcount, headcount_growth_6m_pct,
        hq_location, remote_friendly, careers_url, ats_provider, ats_endpoint, verified_active
    ) VALUES (
        :name, :slug, :domain, :industry, :stage, :total_funding_usd, :last_round_type,
        :valuation_usd, :lead_investors, :headcount, :headcount_growth_6m_pct,
        :hq_location, :remote_friendly, :careers_url, :ats_provider, :ats_endpoint, :verified_active
    );
    """
    cur.execute(insert_query, data)
    return cur.lastrowid



def insert_role(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM open_roles WHERE startup_id = :startup_id AND title = :title",
        {"startup_id": data["startup_id"], "title": data["title"]}
    ).fetchone()

    clean_data = {
        **data,
        "batch_eligibility": data.get("batch_eligibility", "2024, 2025, 2026 Batch"),
        "min_cgpa": data.get("min_cgpa", "60% or 6.0+ CGPA"),
        "test_pattern": data.get("test_pattern", "Aptitude + Technical DSA Coding"),
    }

    if row:
        update_query = """
        UPDATE open_roles SET
            department = :department,
            seniority_level = :seniority_level,
            salary_min_usd = :salary_min_usd,
            salary_max_usd = :salary_max_usd,
            equity_note = :equity_note,
            tech_stack = :tech_stack,
            location = :location,
            remote_type = :remote_type,
            direct_apply_url = :direct_apply_url,
            urgency_score = :urgency_score,
            active_status = :active_status,
            batch_eligibility = :batch_eligibility,
            min_cgpa = :min_cgpa,
            test_pattern = :test_pattern
        WHERE id = :id;
        """
        cur.execute(update_query, {**clean_data, "id": row[0]})
        return row[0]

    insert_query = """
    INSERT INTO open_roles (
        startup_id, title, department, seniority_level, salary_min_usd, salary_max_usd,
        equity_note, tech_stack, location, remote_type, direct_apply_url, urgency_score, active_status,
        batch_eligibility, min_cgpa, test_pattern
    ) VALUES (
        :startup_id, :title, :department, :seniority_level, :salary_min_usd, :salary_max_usd,
        :equity_note, :tech_stack, :location, :remote_type, :direct_apply_url, :urgency_score, :active_status,
        :batch_eligibility, :min_cgpa, :test_pattern
    );
    """
    cur.execute(insert_query, clean_data)
    return cur.lastrowid or 0




def insert_decision_maker(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM decision_makers WHERE startup_id = :startup_id AND full_name = :full_name",
        {"startup_id": data["startup_id"], "full_name": data["full_name"]}
    ).fetchone()
    if row:
        update_query = """
        UPDATE decision_makers SET
            title = :title,
            department = :department,
            linkedin_url = :linkedin_url,
            twitter_handle = :twitter_handle,
            verified_email = :verified_email,
            direct_pitch_hook = :direct_pitch_hook
        WHERE id = :id;
        """
        cur.execute(update_query, {**data, "id": row[0]})
        return row[0]

    query = """
    INSERT INTO decision_makers (
        startup_id, full_name, title, department, linkedin_url, twitter_handle, verified_email, direct_pitch_hook
    ) VALUES (
        :startup_id, :full_name, :title, :department, :linkedin_url, :twitter_handle, :verified_email, :direct_pitch_hook
    );
    """
    cur.execute(query, data)
    return cur.lastrowid or 0


def insert_hiring_signal(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM hiring_signals WHERE startup_id = :startup_id AND signal_type = :signal_type AND description = :description",
        {"startup_id": data["startup_id"], "signal_type": data["signal_type"], "description": data["description"]}
    ).fetchone()
    if row:
        return row[0]

    query = """
    INSERT INTO hiring_signals (
        startup_id, signal_type, source, signal_date, description, weight
    ) VALUES (
        :startup_id, :signal_type, :source, :signal_date, :description, :weight
    );
    """
    cur.execute(query, data)
    return cur.lastrowid or 0


def insert_campaign(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM outreach_campaigns WHERE role_id = :role_id AND decision_maker_id = :decision_maker_id",
        {"role_id": data["role_id"], "decision_maker_id": data["decision_maker_id"]}
    ).fetchone()
    if row:
        return row[0]

    query = """
    INSERT INTO outreach_campaigns (
        role_id, decision_maker_id, channel, subject, message_body, status, follow_up_step
    ) VALUES (
        :role_id, :decision_maker_id, :channel, :subject, :message_body, :status, :follow_up_step
    );
    """
    cur.execute(query, data)
    return cur.lastrowid or 0



def get_all_startups(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute("SELECT * FROM startups ORDER BY total_funding_usd DESC").fetchall()


def get_top_ranked_roles(conn: sqlite3.Connection, limit: int = 50) -> List[sqlite3.Row]:
    query = """
    SELECT 
        r.id as role_id,
        r.title,
        r.department,
        r.seniority_level,
        r.salary_min_usd,
        r.salary_max_usd,
        r.equity_note,
        r.tech_stack,
        r.location,
        r.remote_type,
        r.direct_apply_url,
        r.urgency_score,
        s.name as company_name,
        s.stage,
        s.industry,
        s.total_funding_usd,
        s.ats_provider,
        s.careers_url,
        dm.full_name as dm_name,
        dm.title as dm_title,
        dm.verified_email as dm_email,
        dm.linkedin_url as dm_linkedin,
        dm.direct_pitch_hook
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    LEFT JOIN decision_makers dm ON dm.startup_id = s.id
    WHERE r.active_status = 1
    ORDER BY r.urgency_score DESC, s.total_funding_usd DESC
    LIMIT ?;
    """
    return conn.execute(query, (limit,)).fetchall()
