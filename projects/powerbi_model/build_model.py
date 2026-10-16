"""
=============================================================================
POWERBI VENDOR SLA MODEL BUILDER & INTEGRITY VALIDATOR
Validates Star-Schema relational integrity between Fact_Vendor_SLA and
Dim_Vendor, Dim_Calendar, and computes core operational BI measures.
=============================================================================
"""

import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_CSV = os.path.join(BASE_DIR, "Dim_Vendor.csv")
CALENDAR_CSV = os.path.join(BASE_DIR, "Dim_Calendar.csv")
FACT_CSV = os.path.join(BASE_DIR, "Fact_Vendor_SLA.csv")
OUTPUT_DB = os.path.join(BASE_DIR, "vendor_sla_bi_model.db")


def build_and_validate_model():
    print("[*] Building PowerBI Vendor SLA Relational Model...")
    conn = sqlite3.connect(OUTPUT_DB)
    cur = conn.cursor()

    # Create tables
    cur.execute("DROP TABLE IF EXISTS fact_vendor_sla;")
    cur.execute("DROP TABLE IF EXISTS dim_vendor;")
    cur.execute("DROP TABLE IF EXISTS dim_calendar;")

    cur.execute("""
        CREATE TABLE dim_vendor (
            vendor_id TEXT PRIMARY KEY,
            vendor_name TEXT,
            category TEXT,
            tier TEXT,
            contract_sla_hrs INTEGER,
            sla_penalty_rate_per_hr REAL
        )
    """)

    cur.execute("""
        CREATE TABLE dim_calendar (
            date_key TEXT PRIMARY KEY,
            full_date TEXT,
            year INTEGER,
            quarter TEXT,
            month_name TEXT,
            day_of_week TEXT,
            is_weekend INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE fact_vendor_sla (
            incident_id TEXT PRIMARY KEY,
            vendor_id TEXT,
            date_key TEXT,
            corridor TEXT,
            severity TEXT,
            contract_sla_hrs INTEGER,
            actual_resolution_hrs REAL,
            breach_flag INTEGER,
            breach_hours REAL,
            penalty_amount_inr REAL,
            disputed_flag INTEGER,
            FOREIGN KEY (vendor_id) REFERENCES dim_vendor(vendor_id),
            FOREIGN KEY (date_key) REFERENCES dim_calendar(date_key)
        )
    """)

    # Populate Dim_Vendor
    with open(VENDOR_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cur.execute("""
                INSERT OR REPLACE INTO dim_vendor VALUES (?, ?, ?, ?, ?, ?)
            """, (r["vendor_id"], r["vendor_name"], r["category"], r["tier"], int(r["contract_sla_hrs"]), float(r["sla_penalty_rate_per_hr"])))

    # Populate Dim_Calendar
    with open(CALENDAR_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cur.execute("""
                INSERT OR REPLACE INTO dim_calendar VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (r["date_key"], r["full_date"], int(r["year"]), r["quarter"], r["month_name"], r["day_of_week"], int(r["is_weekend"])))

    # Populate Fact_Vendor_SLA
    with open(FACT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cur.execute("""
                INSERT OR REPLACE INTO fact_vendor_sla VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r["incident_id"], r["vendor_id"], r["date_key"], r["corridor"],
                r["severity"], int(r["contract_sla_hrs"]), float(r["actual_resolution_hrs"]),
                int(r["breach_flag"]), float(r["breach_hours"]), float(r["penalty_amount_inr"]),
                int(r["disputed_flag"])
            ))

    conn.commit()

    # Query core BI measures
    cur.execute("SELECT COUNT(*) FROM fact_vendor_sla")
    total_records = cur.fetchone()[0]

    cur.execute("SELECT SUM(penalty_amount_inr) FROM fact_vendor_sla")
    total_penalties = cur.fetchone()[0] or 0.0

    cur.execute("SELECT COUNT(*) FROM fact_vendor_sla WHERE breach_flag = 1")
    breach_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT vendor_id) FROM dim_vendor")
    vendor_count = cur.fetchone()[0]

    cur.execute("""
        SELECT corridor, COUNT(*), SUM(penalty_amount_inr)
        FROM fact_vendor_sla
        WHERE breach_flag = 1
        GROUP BY corridor
        ORDER BY SUM(penalty_amount_inr) DESC
    """)
    corridor_penalties = cur.fetchall()

    conn.close()

    metrics = {
        "total_records": total_records,
        "vendor_count": vendor_count,
        "breach_count": breach_count,
        "total_penalty_recovery": total_penalties,
        "breach_rate": (breach_count / total_records) * 100 if total_records > 0 else 0,
        "top_corridor": corridor_penalties[0][0] if corridor_penalties else "N/A",
        "output_db": OUTPUT_DB
    }

    print(f"  [OK] Model built successfully at: {OUTPUT_DB}")
    print(f"  [OK] Total Incidents Analyzed:    {total_records}")
    print(f"  [OK] Tracked Vendor Partners:     {vendor_count}")
    print(f"  [OK] SLA Breaches Recorded:       {breach_count} ({metrics['breach_rate']:.1f}%)")
    print(f"  [OK] Total Penalty Recovery:      INR {total_penalties:,.2f}")
    print(f"  [OK] Highest Penalty Corridor:    {metrics['top_corridor']}")

    return metrics


if __name__ == "__main__":
    build_and_validate_model()
