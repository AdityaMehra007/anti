#!/usr/bin/env python3
"""Apply the latest init_schema.sql to master.db."""
import sqlite3
from pathlib import Path

AIOS_ROOT = Path("E:/anti/aios")
DB_PATH = AIOS_ROOT / "data" / "master.db"
SCHEMA_PATH = AIOS_ROOT / "databases" / "init_schema.sql"

con = sqlite3.connect(str(DB_PATH))
con.execute("PRAGMA journal_mode=WAL")
con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
print("[OK] Schema applied successfully.")

cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print(f"[OK] Tables ({len(tables)}): {', '.join(tables)}")
con.close()
