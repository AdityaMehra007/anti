"""
NEXUS-EXIM - Autonomous Cross-Border Trade & Customs Compliance Engine
Relational Schema Initializer & Demo Exporters Seeder.
"""
import sqlite3
import time
import json
from pathlib import Path

DB_PATH = Path(r"e:\anti\apex\projects\nexus_exim\data\exim.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_exim_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Exporters / Importers
    cur.execute('''CREATE TABLE IF NOT EXISTS entities (
        entity_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        iec_code TEXT NOT NULL, -- Import Export Code
        gstin TEXT NOT NULL,
        aeo_tier TEXT DEFAULT 'AEO_T1', -- AEO_T1, AEO_T2, AEO_T3
        category TEXT NOT NULL, -- SOLAR_MFG, AUTO_PARTS, ELECTRONICS
        city TEXT DEFAULT 'Bengaluru'
    )''')

    # 2. Shipments & Customs Filings
    cur.execute('''CREATE TABLE IF NOT EXISTS shipments (
        shipment_id TEXT PRIMARY KEY,
        entity_id TEXT NOT NULL,
        origin_port TEXT NOT NULL, -- e.g. Port of Da Nang, Shanghai
        destination_port TEXT NOT NULL, -- e.g. Nhava Sheva (JNPT), Chennai Port
        incoterm TEXT NOT NULL, -- FOB, CIF, DDP, EXW
        invoice_value_usd REAL NOT NULL,
        exchange_rate_inr REAL DEFAULT 83.50,
        assessable_value_inr REAL NOT NULL,
        bcd_rate_pct REAL DEFAULT 40.0, -- Basic Customs Duty
        igst_rate_pct REAL DEFAULT 18.0,
        total_customs_duty_inr REAL NOT NULL,
        icegate_status TEXT DEFAULT 'CLEARED', -- FILED, ICEGATE_VERIFIED, PENDING_QUERY, CLEARED, DEMURRAGE_ALERT
        demurrage_risk_days INT DEFAULT 0,
        estimated_demurrage_loss_inr REAL DEFAULT 0.0,
        created_at REAL,
        FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
    )''')

    # Seed Demo Exporters
    cur.execute("INSERT OR REPLACE INTO entities VALUES (?,?,?,?,?,?,?)",
                ("EXP-BLR-01", "Karnataka Solar Tech Exporters Ltd", "0712345678", "29AAACK1234A1Z1", "AEO_T2", "SOLAR_MFG", "Peenya, Bengaluru"))
    cur.execute("INSERT OR REPLACE INTO entities VALUES (?,?,?,?,?,?,?)",
                ("EXP-BLR-02", "Deccan Precision Auto Components", "0787654321", "29AAACD5678B1Z2", "AEO_T1", "AUTO_PARTS", "Whitefield, Bengaluru"))

    # Seed Shipments
    now = time.time()
    cur.execute("INSERT OR REPLACE INTO shipments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("SHP-9001", "EXP-BLR-01", "Shanghai Port", "Nhava Sheva (JNPT)", "CIF", 125000.0, 83.50, 10437500.0, 40.0, 18.0, 5907625.0, "CLEARED", 0, 0.0, now - 86400*5))
    cur.execute("INSERT OR REPLACE INTO shipments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("SHP-9002", "EXP-BLR-01", "Da Nang Port", "Chennai Port", "FOB", 85000.0, 83.50, 7097500.0, 40.0, 18.0, 4017185.0, "DEMURRAGE_ALERT", 4, 100000.0, now - 86400*2))

    conn.commit()
    conn.close()
    print(f"[NEXUS-EXIM] Initialized database at: {DB_PATH}")

if __name__ == "__main__":
    init_exim_db()
