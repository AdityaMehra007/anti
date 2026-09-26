"""
TradeNexus Autonomous CRM & Pipeline Tracker (ANTIGRAVITY Ω∞)
Manages the B2B sales pipeline for Indian mid-market exporters, tracking
accounts from automated regulatory audit generation to pilot onboarding and MRR realization.
"""

import os
import json
import sqlite3
import time
from typing import Dict, Any, List, Optional

STAGE_PROBABILITIES = {
    "DOSSIER_GENERATED": 0.10,
    "OUTREACH_READY": 0.15,
    "OUTREACH_SENT": 0.25,
    "REPLIED_INTERESTED": 0.50,
    "DEMO_COMPLETED": 0.70,
    "PILOT_AGREED": 0.90,
    "ACTIVE_PAID_CUSTOMER": 1.00,
    "CHURNED_OR_LOST": 0.00
}

class PipelineCRM:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            db_path = os.path.join(base_dir, "aqua", "crm_pipeline.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    hub_location TEXT,
                    contact_title TEXT,
                    key_products TEXT,
                    destination TEXT,
                    declared_hs TEXT,
                    demurrage_exposure_usd REAL DEFAULT 0.0,
                    target_monthly_inr REAL DEFAULT 30000.0,
                    stage TEXT DEFAULT 'DOSSIER_GENERATED',
                    probability REAL DEFAULT 0.10,
                    audit_seal TEXT,
                    dossier_html_path TEXT,
                    last_action_timestamp REAL,
                    notes TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interaction_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id TEXT NOT NULL,
                    timestamp REAL,
                    action_type TEXT,
                    details TEXT,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                )
            """)
            conn.commit()

    def upsert_account(self, account_data: Dict[str, Any]) -> None:
        stage = account_data.get("stage", "DOSSIER_GENERATED")
        prob = STAGE_PROBABILITIES.get(stage, 0.10)
        now = time.time()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accounts (
                    account_id, company_name, hub_location, contact_title,
                    key_products, destination, declared_hs, demurrage_exposure_usd,
                    target_monthly_inr, stage, probability, audit_seal,
                    dossier_html_path, last_action_timestamp, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(account_id) DO UPDATE SET
                    company_name=excluded.company_name,
                    hub_location=excluded.hub_location,
                    contact_title=excluded.contact_title,
                    key_products=excluded.key_products,
                    destination=excluded.destination,
                    declared_hs=excluded.declared_hs,
                    demurrage_exposure_usd=excluded.demurrage_exposure_usd,
                    stage=excluded.stage,
                    probability=excluded.probability,
                    audit_seal=excluded.audit_seal,
                    dossier_html_path=excluded.dossier_html_path,
                    last_action_timestamp=excluded.last_action_timestamp,
                    notes=excluded.notes
            """, (
                account_data["account_id"],
                account_data["company_name"],
                account_data.get("hub_location", ""),
                account_data.get("contact_title", ""),
                account_data.get("key_products", ""),
                account_data.get("destination", ""),
                account_data.get("declared_hs", ""),
                account_data.get("demurrage_exposure_usd", 0.0),
                account_data.get("target_monthly_inr", 30000.0),
                stage,
                prob,
                account_data.get("audit_seal", ""),
                account_data.get("dossier_html_path", ""),
                now,
                account_data.get("notes", "")
            ))
            conn.commit()

    def update_stage(self, account_id: str, new_stage: str, notes: str = "") -> bool:
        if new_stage not in STAGE_PROBABILITIES:
            raise ValueError(f"Invalid CRM stage: {new_stage}")

        prob = STAGE_PROBABILITIES[new_stage]
        now = time.time()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts
                SET stage = ?, probability = ?, last_action_timestamp = ?, notes = notes || ' | ' || ?
                WHERE account_id = ?
            """, (new_stage, prob, now, notes, account_id))

            cursor.execute("""
                INSERT INTO interaction_log (account_id, timestamp, action_type, details)
                VALUES (?, ?, 'STAGE_CHANGE', ?)
            """, (account_id, now, f"Moved to {new_stage}: {notes}"))
            conn.commit()
            return cursor.rowcount > 0

    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_accounts(self, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if stage:
                cursor.execute("SELECT * FROM accounts WHERE stage = ? ORDER BY demurrage_exposure_usd DESC", (stage,))
            else:
                cursor.execute("SELECT * FROM accounts ORDER BY demurrage_exposure_usd DESC")
            return [dict(r) for r in cursor.fetchall()]

    def calculate_pipeline_metrics(self) -> Dict[str, Any]:
        accounts = self.list_accounts()
        total_accounts = len(accounts)
        if total_accounts == 0:
            return {
                "total_accounts": 0,
                "total_demurrage_identified_usd": 0.0,
                "potential_pipeline_mrr_inr": 0.0,
                "potential_pipeline_arr_usd": 0.0,
                "weighted_arr_usd": 0.0,
                "stage_counts": {}
            }

        total_demurrage = sum(a["demurrage_exposure_usd"] for a in accounts)
        potential_mrr_inr = sum(a["target_monthly_inr"] for a in accounts)
        potential_arr_usd = (potential_mrr_inr * 12) / 85.0 # Conversion ~85 INR/USD

        weighted_arr_usd = sum(
            ((a["target_monthly_inr"] * 12) / 85.0) * a["probability"]
            for a in accounts
        )

        stage_counts: Dict[str, int] = {}
        for a in accounts:
            s = a["stage"]
            stage_counts[s] = stage_counts.get(s, 0) + 1

        return {
            "total_accounts": total_accounts,
            "total_demurrage_identified_usd": round(total_demurrage, 2),
            "potential_pipeline_mrr_inr": round(potential_mrr_inr, 2),
            "potential_pipeline_arr_usd": round(potential_arr_usd, 2),
            "weighted_arr_usd": round(weighted_arr_usd, 2),
            "stage_counts": stage_counts
        }

    def seed_from_batches(self, workspace_root: str = "e:/anti") -> int:
        """
        Seeds CRM pipeline with accounts from Batch 1 and Batch 2 sales dossiers.
        """
        sales_dir = os.path.join(workspace_root, "GLOBAL-COMPANY-OS", "09_SALES")
        audits_dir = os.path.join(sales_dir, "audits")
        count = 0

        # Batch 2 JSON
        b2_file = os.path.join(sales_dir, "LIVE_OUTREACH_BATCH_2.json")
        if os.path.isfile(b2_file):
            with open(b2_file, "r", encoding="utf-8") as f:
                b2_targets = json.load(f)
            for tgt in b2_targets:
                clean_name = tgt["company"].split("/")[0].strip()
                safe_name = clean_name.replace(" ", "_").replace("&", "_").upper()
                html_path = os.path.join(audits_dir, f"AUDIT_{safe_name}.html")
                
                # Parse numeric demurrage from string if present
                dem_usd = 4500.0
                if "€" in tgt.get("potential_penalty", ""):
                    dem_usd = 5500.0
                elif "$" in tgt.get("potential_penalty", ""):
                    dem_usd = 7500.0

                self.upsert_account({
                    "account_id": tgt["id"],
                    "company_name": clean_name,
                    "hub_location": tgt.get("hub", "Bengaluru"),
                    "contact_title": tgt.get("contact_title", "Export Director"),
                    "key_products": tgt.get("key_product", ""),
                    "destination": tgt.get("destination", "EU/US"),
                    "declared_hs": tgt.get("declared_hs", ""),
                    "demurrage_exposure_usd": dem_usd,
                    "target_monthly_inr": 35000.0,
                    "stage": "OUTREACH_READY",
                    "audit_seal": f"TN-SEAL-{tgt['id']}",
                    "dossier_html_path": html_path if os.path.isfile(html_path) else "",
                    "notes": tgt.get("vulnerability", "")
                })
                count += 1

        # Batch 1 Core Targets
        batch_1_targets = [
            {"id": "TGT-01", "name": "Sansera Engineering Limited", "hub": "Bommasandra, Bengaluru", "contact": "VP - Supply Chain & Logistics", "product": "Connecting rods & rocker arms", "dest": "Germany", "hs": "87082900", "demurrage": 4500.0},
            {"id": "TGT-02", "name": "Bharat Steel Tubing Corp", "hub": "Peenya, Bengaluru", "contact": "Head of International Exports", "product": "Hot rolled steel coil", "dest": "Netherlands", "hs": "72081000", "demurrage": 3600.0},
            {"id": "TGT-03", "name": "Centum Electronics Limited", "hub": "Yelahanka, Bengaluru", "contact": "Director - Global Shipping", "product": "Aerospace microelectronics", "dest": "France", "hs": "85423100", "demurrage": 6500.0},
            {"id": "TGT-04", "name": "Dynamatic Technologies Limited", "hub": "Dynamatic Park, Bengaluru", "contact": "VP - Aerospace Operations", "product": "Hydraulic gear pumps", "dest": "UK", "hs": "84136000", "demurrage": 5200.0},
            {"id": "TGT-05", "name": "Gokaldas Exports Limited", "hub": "Yeshwanthpur, Bengaluru", "contact": "Head - Trade & Customs Compliance", "product": "Cotton garments & apparel", "dest": "USA", "hs": "62052000", "demurrage": 3200.0},
            {"id": "TGT-06", "name": "Kavika Precision Engineering", "hub": "Peenya, Bengaluru", "contact": "General Manager - Export Sales", "product": "Automotive stamping dies", "dest": "Germany", "hs": "84807100", "demurrage": 4000.0},
            {"id": "TGT-07", "name": "Kemwell Specialty Chemicals", "hub": "Peenya, Bengaluru", "contact": "Director - Regulatory & EXIM", "product": "Pure benzene & organic chemicals", "dest": "Germany", "hs": "29022000", "demurrage": 7500.0},
            {"id": "TGT-08", "name": "Maini Precision Products Limited", "hub": "Bommasandra, Bengaluru", "contact": "Senior VP - Global Business", "product": "Precision transmission components", "dest": "USA", "hs": "84831099", "demurrage": 4800.0},
            {"id": "TGT-09", "name": "Suprajit Engineering Limited", "hub": "Bommasandra, Bengaluru", "contact": "Head of Logistics", "product": "Automotive mechanical cables", "dest": "Germany", "hs": "87082900", "demurrage": 3800.0},
            {"id": "TGT-10", "name": "Yukon Precision Gears", "hub": "Peenya, Bengaluru", "contact": "Managing Director", "product": "Spur gears & helical bevel pinions", "dest": "Sweden", "hs": "84834000", "demurrage": 4200.0}
        ]

        for t in batch_1_targets:
            safe_name = t["name"].replace(" ", "_").upper()
            html_path = os.path.join(audits_dir, f"AUDIT_{safe_name}.html")
            self.upsert_account({
                "account_id": t["id"],
                "company_name": t["name"],
                "hub_location": t["hub"],
                "contact_title": t["contact"],
                "key_products": t["product"],
                "destination": t["dest"],
                "declared_hs": t["hs"],
                "demurrage_exposure_usd": t["demurrage"],
                "target_monthly_inr": 30000.0,
                "stage": "OUTREACH_READY",
                "audit_seal": f"TN-SEAL-{t['id']}",
                "dossier_html_path": html_path if os.path.isfile(html_path) else "",
                "notes": f"High demurrage vulnerability identified on {t['dest']} corridor."
            })
            count += 1

        return count

if __name__ == "__main__":
    crm = PipelineCRM()
    seeded = crm.seed_from_batches()
    metrics = crm.calculate_pipeline_metrics()
    print(f"CRM Seeded with {seeded} accounts.")
    print("Pipeline Metrics:", json.dumps(metrics, indent=2))
