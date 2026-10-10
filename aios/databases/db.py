"""
ANTIGRAVITY OMEGA: Master SQLite Database Engine
Provides WAL-mode ACID connection pooling and utility methods for the AIOS platform.
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

AIOS_ROOT = Path("E:/anti/aios")
DB_PATH = AIOS_ROOT / "data" / "master.db"
SCHEMA_PATH = AIOS_ROOT / "databases" / "init_schema.sql"

from contextlib import contextmanager

@contextmanager
def get_connection():
    """Returns a WAL-configured sqlite3 connection context with dict-like row factory and guaranteed close."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH), timeout=15.0)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode = WAL;")
    con.execute("PRAGMA synchronous = NORMAL;")
    con.execute("PRAGMA foreign_keys = ON;")
    try:
        yield con
    finally:
        con.close()

def init_database() -> bool:
    """Initializes tables and indices from init_schema.sql."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema not found at {SCHEMA_PATH}")
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_connection() as con:
        con.executescript(schema_sql)
        con.commit()
    return True

def log_audit(actor: str, action: str, category: str, details: str = "", severity: str = "INFO"):
    """Inserts a structured entry into the unified audit ledger."""
    with get_connection() as con:
        con.execute(
            """
            INSERT INTO audit_logs (actor, action, category, details, severity)
            VALUES (?, ?, ?, ?, ?)
            """,
            (actor, action, category, details, severity)
        )
        con.commit()

def record_metric(cpu: float, ram_pct: float, ram_free: float, gpu_vram: Optional[float],
                  disk_c: float, disk_e: float, status: str):
    """Stores a point-in-time system telemetry reading."""
    with get_connection() as con:
        con.execute(
            """
            INSERT INTO system_metrics (cpu_percent, ram_percent, ram_free_gb, gpu_vram_used_mb,
                                        disk_c_free_gb, disk_e_free_gb, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (cpu, ram_pct, ram_free, gpu_vram, disk_c, disk_e, status)
        )
        con.commit()

def get_latest_metrics(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches recent telemetry readings."""
    with get_connection() as con:
        cur = con.execute(
            """
            SELECT * FROM system_metrics
            ORDER BY id DESC LIMIT ?
            """,
            (limit,)
        )
        return [dict(row) for row in cur.fetchall()]

if __name__ == "__main__":
    init_database()
    log_audit("SYSTEM", "INIT_DB", "DATABASE", "Master SQLite database initialized with WAL mode", "INFO")
    print(f"[OK] Master database successfully initialized at {DB_PATH}")
