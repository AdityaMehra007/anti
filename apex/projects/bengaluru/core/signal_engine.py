"""
APEX BENGALURU - Real-Time Intelligence & Signal Engine
Processes high-velocity signals across hiring, expansions, investments, and policies.
"""
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path(r"e:\anti\apex\projects\bengaluru\data\bengaluru.db")

class BengaluruSignalEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_latest_signals(self, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM intelligence_signals ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def emit_signal(self, signal_id: str, category: str, entity_name: str, headline: str, details: str, impact_score: float, classification: str = "VERIFIED") -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        ts = time.time()
        cur.execute(
            "INSERT OR REPLACE INTO intelligence_signals VALUES (?,?,?,?,?,?,?,?)",
            (signal_id, ts, category, entity_name, headline, details, impact_score, classification)
        )
        conn.commit()
        conn.close()
        return {
            "signal_id": signal_id,
            "timestamp": ts,
            "category": category,
            "entity": entity_name,
            "headline": headline,
            "classification": classification,
            "status": "EMITTED_AND_LOGGED"
        }

    def compute_momentum_radar(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT name, momentum_score, category FROM companies ORDER BY momentum_score DESC LIMIT 5")
        top_companies = [dict(r) for r in cur.fetchall()]

        cur.execute("SELECT parent_company, gcc_momentum_score FROM gccs ORDER BY gcc_momentum_score DESC LIMIT 5")
        top_gccs = [dict(r) for r in cur.fetchall()]

        cur.execute("SELECT name, startup_momentum_score, sector FROM startups ORDER BY startup_momentum_score DESC LIMIT 5")
        top_startups = [dict(r) for r in cur.fetchall()]

        conn.close()

        return {
            "top_companies_by_momentum": top_companies,
            "top_gccs_by_momentum": top_gccs,
            "top_startups_by_momentum": top_startups,
            "calculated_at": time.time()
        }

if __name__ == "__main__":
    sig = BengaluruSignalEngine()
    radar = sig.compute_momentum_radar()
    print(f"[SIGNAL_ENGINE] Momentum Radar Computed:\n{radar}")
