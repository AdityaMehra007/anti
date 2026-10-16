"""
Pipeline CSV & Spreadsheet Exporter
Exports deduplicated opportunities from career_vault.db into a structured CSV file
"""

import json
import os
import sqlite3

import pandas as pd

VAULT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "projects",
        "flagship-career-engine",
        "career_vault.db",
    )
)
OUTPUT_CSV = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "career", "CAREER_PIPELINE_EXPORT.csv"
    )
)


def export_pipeline():
    conn = sqlite3.connect(VAULT_PATH)
    query = """
        SELECT fit_score, company, title, job_id, location, department, experience_min, experience_max, status, url, disqualification_flags, created_at
        FROM jobs
        ORDER BY fit_score DESC, created_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Clean flags
    df["flags"] = df["disqualification_flags"].apply(
        lambda x: ", ".join(json.loads(x)) if x else ""
    )
    df.drop(columns=["disqualification_flags"], inplace=True)

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"[OK] Exported {len(df)} opportunities to: {OUTPUT_CSV}")


if __name__ == "__main__":
    export_pipeline()
