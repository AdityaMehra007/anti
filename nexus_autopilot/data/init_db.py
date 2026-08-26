"""
NEXUS AUTOPILOT - Normalized Multi-Tenant Relational Schema & Database Initializer
Creates the core ledger, tenant isolation tables, customers, invoices, payment links, and audit logs.
"""
import sqlite3
import time
import json
from pathlib import Path

DB_PATH = Path(r"e:\anti\nexus_autopilot\data\nexus.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_nexus_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Organizations (Tenants)
    cur.execute('''CREATE TABLE IF NOT EXISTS organizations (
        org_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        industry TEXT NOT NULL, -- Distributor, Agency, Event, Clinic, Contractor
        gstin TEXT,
        currency TEXT DEFAULT 'INR',
        created_at REAL,
        plan_tier TEXT DEFAULT 'GROWTH',
        status TEXT DEFAULT 'ACTIVE'
    )''')

    # 2. Customers
    cur.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        gstin TEXT,
        billing_address TEXT,
        total_invoiced REAL DEFAULT 0.0,
        total_paid REAL DEFAULT 0.0,
        outstanding_balance REAL DEFAULT 0.0,
        avg_payment_delay_days REAL DEFAULT 0.0,
        payment_risk_score REAL DEFAULT 10.0, -- 0-100 (Higher = Riskier)
        last_interaction_at REAL,
        promise_to_pay_date TEXT,
        created_at REAL,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )''')

    # 3. Invoices
    cur.execute('''CREATE TABLE IF NOT EXISTS invoices (
        invoice_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        invoice_number TEXT NOT NULL,
        invoice_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        subtotal REAL NOT NULL,
        tax_amount REAL NOT NULL,
        total_amount REAL NOT NULL,
        amount_paid REAL DEFAULT 0.0,
        status TEXT DEFAULT 'DRAFT', -- DRAFT, SENT, PARTIAL, PAID, OVERDUE, CANCELLED
        line_items_json TEXT,
        payment_link_id TEXT,
        payment_link_url TEXT,
        created_at REAL,
        updated_at REAL,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')

    # 4. Payments & Webhook Records
    cur.execute('''CREATE TABLE IF NOT EXISTS payments (
        payment_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        invoice_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT DEFAULT 'INR',
        method TEXT, -- RAZORPAY, UPI, BANK_TRANSFER, CASH
        razorpay_payment_id TEXT,
        razorpay_order_id TEXT,
        status TEXT DEFAULT 'SUCCESS',
        paid_at REAL,
        reconciled BOOLEAN DEFAULT 1,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )''')

    # 5. WhatsApp Conversations & Messages
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
        message_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        sender_phone TEXT NOT NULL,
        direction TEXT NOT NULL, -- INBOUND, OUTBOUND
        raw_text TEXT NOT NULL,
        intent TEXT,
        extracted_entities_json TEXT,
        action_triggered TEXT,
        approval_status TEXT, -- AUTO_APPROVED, PENDING_APPROVAL, APPROVED, REJECTED
        timestamp REAL,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )''')

    # 6. Collections & Action Queue
    cur.execute('''CREATE TABLE IF NOT EXISTS collections_queue (
        task_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        invoice_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        reminder_stage INT DEFAULT 1, -- 1=Gentle, 2=Firm, 3=Urgent, 4=Legal/Escalated
        scheduled_for TEXT NOT NULL,
        proposed_message TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING_APPROVAL', -- PENDING_APPROVAL, SENT, CANCELLED
        created_at REAL,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )''')

    # 7. Audit & Event Log
    cur.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
        log_id TEXT PRIMARY KEY,
        org_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        agent_role TEXT NOT NULL,
        description TEXT NOT NULL,
        data_payload_json TEXT,
        created_at REAL,
        FOREIGN KEY (org_id) REFERENCES organizations(org_id)
    )''')

    conn.commit()
    conn.close()
    print(f"[DB_INIT] Successfully initialized NEXUS AUTOPILOT Relational Database at: {DB_PATH}")

if __name__ == "__main__":
    init_nexus_database()
