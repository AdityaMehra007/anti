"""
APEX BENGALURU - City Digital Twin & Knowledge Graph Engine
Coordinates all city-scale queries across Companies, GCCs, Startups, Talent, and Micro-Markets.
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

DB_PATH = Path(r"e:\anti\apex\projects\bengaluru\data\bengaluru.db")

class BengaluruDigitalTwin:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_city_macro_kpis(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM companies")
        total_companies = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM gccs")
        total_gccs = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM startups")
        total_startups = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM job_postings")
        total_jobs = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM intelligence_signals")
        total_signals = cur.fetchone()[0]

        conn.close()

        return {
            "city": "Bengaluru",
            "state": "Karnataka",
            "elevation_m": 920,
            "population_agg": "14.2 Million",
            "total_companies_indexed": total_companies,
            "total_gccs_tracked": total_gccs,
            "total_startups_tracked": total_startups,
            "active_job_postings": total_jobs,
            "live_intelligence_signals": total_signals,
            "national_it_export_share_pct": 38.5,
            "unicorns_count": 45
        }

    def query_companies(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        if category:
            cur.execute("SELECT * FROM companies WHERE category = ? ORDER BY momentum_score DESC LIMIT ?", (category, limit))
        else:
            cur.execute("SELECT * FROM companies ORDER BY momentum_score DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def query_gcc_momentum(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gccs ORDER BY gcc_momentum_score DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def query_startups(self, sector: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        if sector:
            cur.execute("SELECT * FROM startups WHERE sector = ? ORDER BY startup_momentum_score DESC", (sector,))
        else:
            cur.execute("SELECT * FROM startups ORDER BY startup_momentum_score DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def query_micro_markets(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM neighborhoods ORDER BY office_rent_sqft_inr DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

if __name__ == "__main__":
    twin = BengaluruDigitalTwin()
    kpis = twin.get_city_macro_kpis()
    print(f"[DIGITAL_TWIN] Loaded Bengaluru KPIs: {json.dumps(kpis, indent=2)}")
