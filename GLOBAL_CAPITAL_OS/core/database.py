"""SQLite WAL Database Engine for GLOBAL CAPITAL OS.

Maintains normalized financial truth, foreign key constraints,
atomic ledger integrity, and automatic data initialization.
"""

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
from .config import settings
from .models import (
    CurrencyCode, AccountCategory, TransactionCategory,
    TransactionStatus, SalesStage, OpportunityTier, ApprovalStatus
)

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Entities
CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    jurisdiction TEXT NOT NULL DEFAULT 'India',
    entity_type TEXT NOT NULL DEFAULT 'Sole Proprietorship',
    pan_gst TEXT,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT (datetime('now'))
);

-- 2. Bank Accounts & Treasury Vaults
CREATE TABLE IF NOT EXISTS bank_accounts (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    institution TEXT NOT NULL,
    account_name TEXT NOT NULL,
    account_number_masked TEXT NOT NULL,
    currency TEXT NOT NULL,
    category TEXT NOT NULL,
    balance REAL DEFAULT 0.0 CHECK(balance >= 0.0),
    balance_inr REAL DEFAULT 0.0 CHECK(balance_inr >= 0.0),
    purpose TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 3. Double-Entry / Master Ledger Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    source_account_id TEXT REFERENCES bank_accounts(id) ON DELETE SET NULL,
    destination_account_id TEXT REFERENCES bank_accounts(id) ON DELETE SET NULL,
    counterparty_name TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    tax_reserve_amount_inr REAL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'PENDING_APPROVAL',
    reconciliation_id TEXT,
    approval_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 4. 500-Opportunity Database Funnel
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    target_customer TEXT NOT NULL,
    core_problem TEXT NOT NULL,
    price_usd REAL DEFAULT 0.0,
    price_inr REAL DEFAULT 0.0,
    delivery_cost_inr REAL DEFAULT 0.0,
    gross_margin_pct REAL DEFAULT 0.0,
    time_to_first_money_days INTEGER DEFAULT 0,
    founder_hours_week REAL DEFAULT 0.0,
    automation_pct REAL DEFAULT 0.0,
    recurring_pct REAL DEFAULT 0.0,
    capital_requirement_inr REAL DEFAULT 0.0,
    zero_capital_score REAL DEFAULT 0.0,
    funnel_tier TEXT DEFAULT 'DATABASE',
    status TEXT DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT (datetime('now'))
);

-- 5. Ethical B2B Leads
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    website TEXT,
    contact_name TEXT NOT NULL,
    contact_title TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    buying_trigger TEXT NOT NULL,
    custom_icebreaker TEXT NOT NULL,
    lead_score TEXT DEFAULT 'Hot',
    icp_fit_score REAL DEFAULT 80.0,
    status TEXT DEFAULT 'NEW',
    created_at TEXT DEFAULT (datetime('now'))
);

-- 6. 12-Stage Sales CRM Deals
CREATE TABLE IF NOT EXISTS deals (
    id TEXT PRIMARY KEY,
    lead_id TEXT REFERENCES leads(id) ON DELETE SET NULL,
    deal_name TEXT NOT NULL,
    stage TEXT NOT NULL DEFAULT 'LEAD',
    deal_value_inr REAL DEFAULT 0.0,
    deal_value_usd REAL DEFAULT 0.0,
    currency TEXT DEFAULT 'INR',
    win_probability REAL DEFAULT 0.1,
    expected_value_inr REAL DEFAULT 0.0,
    owner_agent TEXT DEFAULT 'RevenueCommander',
    next_step TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 7. Debt Facilities (Strictly non-speculative, fully cost-accounted)
CREATE TABLE IF NOT EXISTS debt_facilities (
    id TEXT PRIMARY KEY,
    lender_name TEXT NOT NULL,
    facility_type TEXT NOT NULL,
    principal_inr REAL NOT NULL,
    interest_rate_apr REAL NOT NULL,
    monthly_service_inr REAL NOT NULL,
    maturity_date TEXT NOT NULL,
    collateral_description TEXT NOT NULL,
    covenants TEXT NOT NULL,
    is_compliant_rbi INTEGER DEFAULT 1,
    purpose TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 8. Investment Holdings (Paper / Authorized Treasury Holdings)
CREATE TABLE IF NOT EXISTS investments (
    id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    cost_basis_inr REAL NOT NULL,
    current_value_inr REAL NOT NULL,
    unrealized_pnl_inr REAL DEFAULT 0.0,
    allocation_pct REAL DEFAULT 0.0,
    thesis TEXT NOT NULL,
    kill_condition TEXT NOT NULL,
    downside_limit_pct REAL DEFAULT 5.0,
    is_authorized INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 9. Founder Approval Center (Consequential Action Queue)
CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    requester_agent TEXT NOT NULL,
    action_type TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    source_account TEXT NOT NULL,
    destination TEXT NOT NULL,
    purpose TEXT NOT NULL,
    expected_benefit TEXT NOT NULL,
    worst_case_loss TEXT NOT NULL,
    legal_status TEXT NOT NULL,
    tax_considerations TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    alternatives TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    decision_notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    resolved_at TEXT
);

-- 10. Cryptographic Event Log (Append-Only)
CREATE TABLE IF NOT EXISTS audit_chain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_time TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    details_json TEXT NOT NULL,
    previous_hash TEXT NOT NULL,
    current_hash TEXT NOT NULL
);

-- 11. System State & Emergency Freeze Flag
CREATE TABLE IF NOT EXISTS system_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT (datetime('now'))
);
"""


class DatabaseEngine:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()
        self.seed_defaults_if_empty()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    def init_schema(self) -> None:
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def seed_defaults_if_empty(self) -> None:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM entities")
            if cur.fetchone()[0] == 0:
                # Seed primary legal entity
                cur.execute("""
                    INSERT INTO entities (id, name, jurisdiction, entity_type, pan_gst, status)
                    VALUES ('ENT-01', 'Aditya Mehra Ventures', 'India', 'Sole Proprietorship', 'PAN-XXXXX-GST-PENDING', 'ACTIVE')
                """)

                # Seed standard legitimate bank accounts map
                accounts = [
                    ('ACC-IN-OPS-01', 'ENT-01', 'HDFC Bank', 'Operating Account', 'XXXX4821', 'INR', 'OPERATING', 50100.0, 50100.0, 'Day-to-day revenue receipt & primary vendor payments'),
                    ('ACC-IN-TAX-01', 'ENT-01', 'ICICI Bank', 'Tax Reserve Account', 'XXXX9123', 'INR', 'TAX_RESERVE', 9018.0, 9018.0, 'Mandatory 18% statutory tax and GST reserve buffer'),
                    ('ACC-IN-EMG-01', 'ENT-01', 'SBI Liquid Pool', 'Emergency Reserve Account', 'XXXX3310', 'INR', 'EMERGENCY_RESERVE', 25000.0, 25000.0, '6-month operational survival reserve'),
                    ('ACC-IN-GRO-01', 'ENT-01', 'Kotak Mahindra', 'Growth & Reinvestment', 'XXXX7702', 'INR', 'GROWTH', 10000.0, 10000.0, 'Approved customer acquisition & AI tooling allocation'),
                    ('ACC-IN-INV-01', 'ENT-01', 'HDFC Treasury Liquid', 'Treasury Cash Equivalents', 'XXXX5544', 'INR', 'INVESTMENT', 0.0, 0.0, 'Liquid mutual funds / Government T-Bills (no speculative risk)'),
                    ('ACC-GL-WISE-01', 'ENT-01', 'Wise Business', 'Global Inward Multi-Currency Vault', 'XXXX8829', 'USD', 'FOREIGN_CURRENCY', 600.0, 50100.0, 'Compliant inward export collection account with e-FIRC integration'),
                ]
                cur.executemany("""
                    INSERT INTO bank_accounts (id, entity_id, institution, account_name, account_number_masked, currency, category, balance, balance_inr, purpose)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, accounts)

                # Initialize System State
                cur.execute("INSERT OR REPLACE INTO system_state (key, value) VALUES ('EMERGENCY_FREEZE', 'FALSE')")
                cur.execute("INSERT OR REPLACE INTO system_state (key, value) VALUES ('SYSTEM_STATUS', 'OPERATIONAL')")
                conn.commit()

        # Seed real transaction data from data/money_dashboard.csv if exists
        self.import_money_dashboard_csv()
        # Seed verified leads from data/demo_lead_list.csv if exists
        self.import_demo_leads_csv()

    def import_money_dashboard_csv(self) -> None:
        csv_path = settings.DATA_DIR / "money_dashboard.csv"
        if not csv_path.exists():
            return
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM transactions")
            if cur.fetchone()[0] > 0:
                return  # already imported

            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                tx_id = 1
                for row in reader:
                    client = row.get("Client/Platform", "").strip()
                    if not client:
                        continue
                    rev_inr = float(row.get("Revenue (INR)") or 0.0)
                    rev_usd = float(row.get("Revenue (USD)") or 0.0)
                    cost_usd = float(row.get("Cost (USD)") or 0.0)
                    profit_usd = float(row.get("Profit (USD)") or 0.0)
                    status_raw = row.get("Payment Status", "Received").strip()
                    status = "RECONCILED" if status_raw == "Received" else "PENDING_APPROVAL"
                    tx_date = row.get("Date", datetime.utcnow().strftime("%Y-%m-%d")).strip()
                    service = row.get("Service/Product", "Services")
                    
                    # 18% statutory tax reservation
                    tax_res = rev_inr * settings.DEFAULT_TAX_RESERVE_PCT

                    cur.execute("""
                        INSERT INTO transactions (
                            id, timestamp, source_account_id, destination_account_id,
                            counterparty_name, amount, currency, amount_inr, category,
                            description, tax_reserve_amount_inr, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"TX-{tx_id:04d}",
                        tx_date,
                        "ACC-GL-WISE-01" if rev_usd > 0 else "ACC-IN-OPS-01",
                        "ACC-IN-OPS-01",
                        client,
                        rev_usd if rev_usd > 0 else rev_inr,
                        "USD" if rev_usd > 0 else "INR",
                        rev_inr,
                        "REVENUE_CUSTOMER",
                        f"{service} - {row.get('Notes', '')}",
                        tax_res,
                        status
                    ))
                    tx_id += 1
            conn.commit()

    def import_demo_leads_csv(self) -> None:
        csv_path = settings.DATA_DIR / "demo_lead_list.csv"
        if not csv_path.exists():
            return
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM leads")
            if cur.fetchone()[0] > 0:
                return

            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                lead_id = 1
                for row in reader:
                    company = row.get("Company Name", "").strip()
                    contact_name = row.get("Contact Name", "").strip()
                    if not company or not contact_name:
                        continue
                    cur.execute("""
                        INSERT INTO leads (
                            id, company_name, website, contact_name, contact_title,
                            contact_email, industry, location, buying_trigger,
                            custom_icebreaker, lead_score, icp_fit_score, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"LEAD-{lead_id:04d}",
                        company,
                        row.get("Website", ""),
                        contact_name,
                        row.get("Title", ""),
                        row.get("Verified Email", ""),
                        row.get("Industry", "B2B"),
                        row.get("Location", "USA"),
                        row.get("Recent Trigger Event", ""),
                        row.get("Custom AI Icebreaker", ""),
                        row.get("Lead Score", "Hot"),
                        92.0 if row.get("Lead Score") == "Hot" else 80.0,
                        "NEW"
                    ))

                    # Create corresponding deal in pipeline
                    cur.execute("""
                        INSERT INTO deals (
                            id, lead_id, deal_name, stage, deal_value_inr,
                            deal_value_usd, currency, win_probability, expected_value_inr,
                            owner_agent, next_step
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"DEAL-{lead_id:04d}",
                        f"LEAD-{lead_id:04d}",
                        f"{company} - Enterprise Account Intelligence & Competitor Audit",
                        "QUALIFIED" if lead_id <= 3 else "CONTACT",
                        75000.0,
                        900.0,
                        "USD",
                        0.35 if lead_id <= 3 else 0.15,
                        26250.0 if lead_id <= 3 else 11250.0,
                        "RevenueCommander",
                        "Dispatch tailored icebreaker and productized sample audit"
                    ))
                    lead_id += 1
            conn.commit()


# Singleton database instance
db = DatabaseEngine()
