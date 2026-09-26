"""
ANTIGRAVITY OMNIVERSE: 7-TIER MEMORY ENGINE
===========================================
Decomposes cognitive state into Working, Project, Long-Term, Organizational,
Technical, Decision, and Failure memory stores.
"""
import time
import json
import sqlite3
from typing import Dict, Any, List, Optional
from pathlib import Path

class OmniverseMemoryEngine:
    def __init__(self, db_path: str = "data/omniverse_memory.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._working_memory: Dict[str, Any] = {}

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tier TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    metadata TEXT,
                    created_at REAL NOT NULL,
                    expires_at REAL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_tier_key ON memory_records(tier, key);")
            conn.commit()

    def set_working(self, key: str, value: Any):
        """Tier 1: In-process Working Memory."""
        self._working_memory[key] = value

    def get_working(self, key: str) -> Optional[Any]:
        return self._working_memory.get(key)

    def persist(self, tier: str, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None, ttl_seconds: Optional[float] = None):
        """Tiers 2-7: Persistent Memory (Project, Long-Term, Organizational, Tech, Decision, Failure)."""
        valid_tiers = {"PROJECT", "LONG_TERM", "ORGANIZATIONAL", "TECHNICAL", "DECISION", "FAILURE"}
        if tier not in valid_tiers:
            raise ValueError(f"Invalid memory tier '{tier}'. Must be one of {valid_tiers}")
        
        now = time.time()
        expires = (now + ttl_seconds) if ttl_seconds else None
        val_str = json.dumps(value) if not isinstance(value, str) else value
        meta_str = json.dumps(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO memory_records (tier, key, value, metadata, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
                (tier, key, val_str, meta_str, now, expires)
            )
            conn.commit()

    def query(self, tier: str, key: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            if key:
                cur = conn.execute(
                    "SELECT tier, key, value, metadata, created_at FROM memory_records WHERE tier = ? AND key = ? ORDER BY created_at DESC LIMIT ?",
                    (tier, key, limit)
                )
            else:
                cur = conn.execute(
                    "SELECT tier, key, value, metadata, created_at FROM memory_records WHERE tier = ? ORDER BY created_at DESC LIMIT ?",
                    (tier, limit)
                )
            rows = cur.fetchall()
            results = []
            for r in rows:
                try:
                    val = json.loads(r[2])
                except Exception:
                    val = r[2]
                results.append({
                    "tier": r[0],
                    "key": r[1],
                    "value": val,
                    "metadata": json.loads(r[3]),
                    "created_at": r[4]
                })
            return results
