"""BSU OS Super Search Engine.

Powers global multi-entity faceted search (Cmd/Ctrl + K), relevance ranking,
and unified autocomplete across Bengaluru tech entities.
"""

import json
from typing import List, Dict, Any, Optional
from bsu_os.database import get_connection


def super_search(query_str: str, entity_types: Optional[List[str]] = None, limit: int = 25) -> Dict[str, List[Dict[str, Any]]]:
    """Executes a unified multi-entity search across startups, founders, investors, jobs, and events.

    Returns grouped matching results with relevance highlights.
    """
    conn = get_connection()
    q = f"%{query_str.strip().lower()}%"
    clean_q = query_str.strip().lower()

    types = entity_types or ["startups", "founders", "investors", "jobs", "events", "clusters"]
    results: Dict[str, List[Dict[str, Any]]] = {
        "startups": [],
        "founders": [],
        "investors": [],
        "jobs": [],
        "events": [],
        "clusters": []
    }

    # 1. Startups Search
    if "startups" in types:
        s_query = """
        SELECT id, name, slug, sector, sub_sector, stage, cluster_id,
               elevator_pitch, power_score, career_score, logo_url, tags
        FROM startups
        WHERE LOWER(name) LIKE ?
           OR LOWER(sector) LIKE ?
           OR LOWER(sub_sector) LIKE ?
           OR LOWER(elevator_pitch) LIKE ?
           OR LOWER(tags) LIKE ?
           OR LOWER(tech_stack) LIKE ?
        ORDER BY
            CASE WHEN LOWER(name) = ? THEN 1
                 WHEN LOWER(name) LIKE ? THEN 2
                 ELSE 3 END,
            power_score DESC
        LIMIT ?
        """
        rows = conn.execute(s_query, (q, q, q, q, q, q, clean_q, f"{clean_q}%", limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["tags"] = json.loads(d["tags"]) if d["tags"] else []
            d["entity_type"] = "startup"
            results["startups"].append(d)

    # 2. Founders Search
    if "founders" in types:
        f_query = """
        SELECT f.id, f.name, f.role, f.bio, f.educational_background,
               s.name AS startup_name, s.slug AS startup_slug, s.cluster_id
        FROM founders f
        JOIN startups s ON f.startup_id = s.id
        WHERE LOWER(f.name) LIKE ? OR LOWER(f.bio) LIKE ? OR LOWER(f.educational_background) LIKE ?
        LIMIT ?
        """
        rows = conn.execute(f_query, (q, q, q, limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["entity_type"] = "founder"
            results["founders"].append(d)

    # 3. Investors Search
    if "investors" in types:
        inv_query = """
        SELECT id, name, firm_name, investor_type, thesis, key_investments, cluster_id
        FROM investors
        WHERE LOWER(name) LIKE ? OR LOWER(firm_name) LIKE ? OR LOWER(thesis) LIKE ? OR LOWER(key_investments) LIKE ?
        LIMIT ?
        """
        rows = conn.execute(inv_query, (q, q, q, q, limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["key_investments"] = json.loads(d["key_investments"]) if d["key_investments"] else []
            d["entity_type"] = "investor"
            results["investors"].append(d)

    # 4. Jobs Search
    if "jobs" in types:
        j_query = """
        SELECT j.id, j.title, j.department, j.experience_level, j.min_salary_lpa, j.max_salary_lpa,
               j.skills_required, j.career_score, j.location_cluster_id,
               s.name AS startup_name, s.slug AS startup_slug, s.logo_url
        FROM jobs j
        JOIN startups s ON j.startup_id = s.id
        WHERE j.is_active = 1 AND (
            LOWER(j.title) LIKE ? OR LOWER(j.department) LIKE ? OR LOWER(j.skills_required) LIKE ? OR LOWER(j.description) LIKE ?
        )
        ORDER BY j.career_score DESC
        LIMIT ?
        """
        rows = conn.execute(j_query, (q, q, q, q, limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["skills_required"] = json.loads(d["skills_required"]) if d["skills_required"] else []
            d["entity_type"] = "job"
            results["jobs"].append(d)

    # 5. Events Search
    if "events" in types:
        e_query = """
        SELECT id, title, event_type, date_time, location_cluster_id, venue_name, organizer, tags, is_featured
        FROM events
        WHERE LOWER(title) LIKE ? OR LOWER(organizer) LIKE ? OR LOWER(tags) LIKE ?
        LIMIT ?
        """
        rows = conn.execute(e_query, (q, q, q, limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["tags"] = json.loads(d["tags"]) if d["tags"] else []
            d["entity_type"] = "event"
            results["events"].append(d)

    # 6. Clusters Search
    if "clusters" in types:
        c_query = """
        SELECT id, name, description, vibe, lat, lng, primary_sectors
        FROM clusters
        WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(vibe) LIKE ?
        LIMIT ?
        """
        rows = conn.execute(c_query, (q, q, q, limit)).fetchall()
        for r in rows:
            d = dict(r)
            d["primary_sectors"] = json.loads(d["primary_sectors"]) if d["primary_sectors"] else []
            d["entity_type"] = "cluster"
            results["clusters"].append(d)

    conn.close()
    return results
