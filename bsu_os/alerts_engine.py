"""BSU OS Watchlists, Notification Dispatcher, and Daily Ecosystem Briefing Engine.

Generates the Daily Intelligence Brief ('What Changed Today?') and handles
user watchlists and ecosystem alerts (Sections 73, 113, and 204 of the master blueprint).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from bsu_os.database import get_connection


def add_to_watchlist(user_id: str, entity_type: str, entity_id: int, notes: str = "") -> bool:
    """Adds an entity to user's watchlist."""
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO watchlists (user_id, entity_type, entity_id, notes)
            VALUES (?, ?, ?, ?)
        """, (user_id, entity_type, entity_id, notes))
        conn.commit()
        return True
    finally:
        conn.close()


def remove_from_watchlist(user_id: str, entity_type: str, entity_id: int) -> bool:
    """Removes an entity from user's watchlist."""
    conn = get_connection()
    try:
        conn.execute("""
            DELETE FROM watchlists WHERE user_id = ? AND entity_type = ? AND entity_id = ?
        """, (user_id, entity_type, entity_id))
        conn.commit()
        return True
    finally:
        conn.close()


def get_user_watchlist(user_id: str = "guest_default") -> List[Dict[str, Any]]:
    """Retrieves all items in user's watchlist hydrated with entity details."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM watchlists WHERE user_id = ? ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    items = []
    for r in rows:
        item = dict(r)
        e_type = item["entity_type"]
        e_id = item["entity_id"]
        if e_type == "startup":
            s = conn.execute("SELECT name, slug, sector, stage, power_score, logo_url FROM startups WHERE id = ?", (e_id,)).fetchone()
            if s:
                item["details"] = dict(s)
        elif e_type == "job":
            j = conn.execute("""
                SELECT j.title, j.min_salary_lpa, j.max_salary_lpa, j.career_score, s.name AS startup_name
                FROM jobs j JOIN startups s ON j.startup_id = s.id WHERE j.id = ?
            """, (e_id,)).fetchone()
            if j:
                item["details"] = dict(j)
        items.append(item)

    conn.close()
    return items


def get_recent_alerts(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves recent ecosystem alerts."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def generate_daily_brief() -> Dict[str, Any]:
    """Generates the Section 204 Personal Daily Command Center Ecosystem Brief.

    Contains:
    - 3 High-Impact Opportunities
    - 3 Critical Ecosystem Updates
    - 3 Recommended Actions
    - 1 Emerging Trend
    """
    conn = get_connection()
    
    # 3 High-Impact Opportunities (Highest Career Score jobs or high-momentum early stage startups)
    job_rows = conn.execute("""
        SELECT j.id, j.title, j.max_salary_lpa, j.career_score, s.name AS startup_name, s.cluster_id
        FROM jobs j JOIN startups s ON j.startup_id = s.id
        ORDER BY j.career_score DESC LIMIT 3
    """).fetchall()
    opportunities = [
        f"Apply to {j['startup_name']} for '{j['title']}' ({j['max_salary_lpa']} LPA max, {j['cluster_id']})"
        for j in job_rows
    ]

    # 3 Critical Updates from alerts
    alert_rows = conn.execute("SELECT headline FROM alerts ORDER BY created_at DESC LIMIT 3").fetchall()
    updates = [a["headline"] for a in alert_rows]

    conn.close()

    return {
        "date": datetime.now().strftime("%A, %B %d, %Y"),
        "theme": "Sovereign AI Acceleration & SpaceTech Constellations",
        "opportunities": opportunities,
        "critical_updates": updates,
        "recommended_actions": [
            "Benchmark your engineering compensation against the HSR/Koramangala 90th percentile.",
            "Attend the upcoming Bengaluru Tech Summit registration before founder badges close.",
            "Review your portfolio or startup tech stack for vLLM & CUDA inference optimizations."
        ],
        "emerging_trend": {
            "title": "On-Device & Sovereign Multilingual Indic AI",
            "summary": "Surging venture interest and government public-digital infrastructure grants are shifting capital from generic wrappers to sovereign vernacular models.",
            "hot_clusters": ["Koramangala", "HSR Layout"]
        }
    }
