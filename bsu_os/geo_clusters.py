"""BSU OS Bengaluru Geospatial & Micro-Cluster Engine.

Aggregates regional metrics across Bengaluru's tech corridors:
Koramangala, HSR Layout, Indiranagar, Outer Ring Road (ORR), Whitefield, Electronic City, and CBD.
"""

import json
from typing import List, Dict, Any
from bsu_os.config import BENGALURU_CLUSTERS
from bsu_os.database import get_connection


def get_cluster_intelligence() -> List[Dict[str, Any]]:
    """Calculates live ecosystem density metrics for all Bengaluru micro-clusters."""
    conn = get_connection()
    clusters_output = []

    for cluster_id, meta in BENGALURU_CLUSTERS.items():
        # Aggregate startups in this cluster
        s_rows = conn.execute("""
            SELECT id, name, slug, sector, stage, power_score, total_funding_usd, logo_url
            FROM startups
            WHERE cluster_id = ?
            ORDER BY power_score DESC
        """, (cluster_id,)).fetchall()

        # Aggregate jobs in this cluster
        job_count = conn.execute("""
            SELECT COUNT(*) AS cnt FROM jobs WHERE location_cluster_id = ? AND is_active = 1
        """, (cluster_id,)).fetchone()["cnt"]

        # Aggregate events in this cluster
        event_count = conn.execute("""
            SELECT COUNT(*) AS cnt FROM events WHERE location_cluster_id = ?
        """, (cluster_id,)).fetchone()["cnt"]

        startups_list = [dict(r) for r in s_rows]
        startup_count = len(startups_list)
        total_funding = sum(s["total_funding_usd"] for s in startups_list)
        avg_power = round(sum(s["power_score"] for s in startups_list) / startup_count, 1) if startup_count > 0 else 0.0

        clusters_output.append({
            "id": cluster_id,
            "name": meta["name"],
            "description": meta["description"],
            "vibe": meta["vibe"],
            "lat": meta["lat"],
            "lng": meta["lng"],
            "zoom": meta["zoom"],
            "primary_sectors": meta["primary_sectors"],
            "startup_count": startup_count,
            "active_job_count": job_count,
            "event_count": event_count,
            "total_funding_usd": total_funding,
            "average_power_score": avg_power,
            "key_startups": startups_list[:5]  # Top 5 flagship companies
        })

    conn.close()
    return clusters_output


def get_cluster_details(cluster_id: str) -> Dict[str, Any]:
    """Retrieves detailed intelligence for a specific micro-cluster."""
    all_clusters = get_cluster_intelligence()
    for c in all_clusters:
        if c["id"] == cluster_id:
            return c
    return {}
