import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import sqlite3

conn = sqlite3.connect(r"e:\anti\omega\data\omega_master.db")
cursor = conn.cursor()
existing_cols = [c[1] for c in cursor.execute("PRAGMA table_info(companies);").fetchall()]

cols_to_add = [
    ("corridor", "TEXT"),
    ("gcc_tier", "TEXT"),
    ("headcount", "INTEGER DEFAULT 1000"),
    ("tier_rating", "REAL DEFAULT 1.0"),
    ("hq_location", "TEXT DEFAULT 'Bengaluru, India'"),
    ("tech_park", "TEXT"),
    ("verified_status", "TEXT DEFAULT 'VERIFIED'")
]

for col, col_type in cols_to_add:
    if col not in existing_cols:
        cursor.execute(f"ALTER TABLE companies ADD COLUMN {col} {col_type};")
        print(f"Added column {col} to companies table")

# Update corridor and gcc_tier from existing tier/bangalore_office if needed
cursor.execute("UPDATE companies SET corridor = bangalore_office WHERE corridor IS NULL AND bangalore_office IS NOT NULL;")
cursor.execute("UPDATE companies SET gcc_tier = tier WHERE gcc_tier IS NULL AND tier IS NOT NULL;")

conn.commit()
conn.close()
print("Database schema migration successful!")
