"""
NEXUS AUTOPILOT - Demo Company Seeder (ABC Distributors)
Populates the database with a high-fidelity synthetic SMB business dataset.
"""
import sqlite3
import json
import time
from pathlib import Path

DB_PATH = Path(r"e:\anti\nexus_autopilot\data\nexus.db")

def seed_demo_company():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    org_id = "ORG-ABC-001"
    now = time.time()

    # 1. Organization
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?,?,?)",
                (org_id, "ABC Packaging & Industrial Distributors", "Distributor", "29AAACA1234A1Z5", "INR", now - 86400*90, "PRO", "ACTIVE"))

    # 2. Customers
    customers = [
        ("CUST-001", org_id, "Ramesh Traders", "+919845012345", "ramesh@traders.in", "29AABCR1234A1Z1", "Peenya Industrial Area, Bengaluru", 450000.0, 310000.0, 140000.0, 19.5, 78.0, now - 86400*2, "2026-08-28", now - 86400*60),
        ("CUST-002", org_id, "Kumar Enterprises", "+919845023456", "kumar@ent.in", "29AABCK2345B1Z2", "Whitefield EPIP, Bengaluru", 820000.0, 700000.0, 120000.0, 5.2, 22.0, now - 86400*1, "2026-08-25", now - 86400*75),
        ("CUST-003", org_id, "Apex Logistics Hub", "+919845034567", "ops@apexlogistics.in", "29AABCA3456C1Z3", "Electronic City, Bengaluru", 1250000.0, 1250000.0, 0.0, 2.1, 8.0, now - 86400*5, None, now - 86400*80),
        ("CUST-004", org_id, "Shree Balaji Manufacturing", "+919845045678", "balaji@mfg.in", "29AABCS4567D1Z4", "Yeshwanthpur, Bengaluru", 640000.0, 480000.0, 160000.0, 14.0, 65.0, now - 86400*3, "2026-08-30", now - 86400*45),
        ("CUST-005", org_id, "Kiran Event Organizers", "+919845056789", "kiran@events.in", "29AABCK5678E1Z5", "Indiranagar, Bengaluru", 280000.0, 180000.0, 100000.0, 28.0, 85.0, now - 86400*10, None, now - 86400*30)
    ]
    cur.executemany("INSERT OR REPLACE INTO customers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", customers)

    # 3. Invoices
    invoices = [
        ("INV-1001", org_id, "CUST-001", "Ramesh Traders", "INV/2026/1001", "2026-08-01", "2026-08-15", 118644.0, 21356.0, 140000.0, 0.0, "OVERDUE", json.dumps([{"item": "Heavy Duty Corrugated Boxes (3-Ply)", "qty": 300, "rate": 420.0, "amount": 126000.0}]), "plink_ramesh_01", "https://rzp.io/i/nexus_ramesh_01", now - 86400*24, now),
        ("INV-1002", org_id, "CUST-002", "Kumar Enterprises", "INV/2026/1002", "2026-08-18", "2026-08-25", 101695.0, 18305.0, 120000.0, 0.0, "SENT", json.dumps([{"item": "Industrial Stretch Film Rolls", "qty": 200, "rate": 600.0, "amount": 120000.0}]), "plink_kumar_02", "https://rzp.io/i/nexus_kumar_02", now - 86400*6, now),
        ("INV-1003", org_id, "CUST-004", "Shree Balaji Manufacturing", "INV/2026/1003", "2026-08-05", "2026-08-19", 135593.0, 24407.0, 160000.0, 0.0, "OVERDUE", json.dumps([{"item": "Printed Carton Packaging", "qty": 400, "rate": 400.0, "amount": 160000.0}]), "plink_balaji_03", "https://rzp.io/i/nexus_balaji_03", now - 86400*20, now),
        ("INV-1004", org_id, "CUST-005", "Kiran Event Organizers", "INV/2026/1004", "2026-07-20", "2026-08-04", 84746.0, 15254.0, 100000.0, 0.0, "OVERDUE", json.dumps([{"item": "Custom Branded Gift Packaging", "qty": 250, "rate": 400.0, "amount": 100000.0}]), "plink_kiran_04", "https://rzp.io/i/nexus_kiran_04", now - 86400*35, now),
        ("INV-1005", org_id, "CUST-003", "Apex Logistics Hub", "INV/2026/1005", "2026-08-10", "2026-08-17", 211864.0, 38136.0, 250000.0, 250000.0, "PAID", json.dumps([{"item": "Bulk Wooden Pallets", "qty": 250, "rate": 1000.0, "amount": 250000.0}]), "plink_apex_05", "https://rzp.io/i/nexus_apex_05", now - 86400*14, now - 86400*10)
    ]
    cur.executemany("INSERT OR REPLACE INTO invoices VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", invoices)

    # 4. Payments
    payments = [
        ("PAY-001", org_id, "INV-1005", "CUST-003", 250000.0, "INR", "RAZORPAY", "pay_apex_987654", "order_apex_1234", "SUCCESS", now - 86400*10, 1)
    ]
    cur.executemany("INSERT OR REPLACE INTO payments VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", payments)

    # 5. Collections Queue
    collections = [
        ("TASK-COL-001", org_id, "INV-1001", "CUST-001", 2, "2026-08-25", "Hi Ramesh ji, a gentle reminder that invoice INV/2026/1001 of ₹1,40,000 was due on Aug 15. Please pay via Razorpay: https://rzp.io/i/nexus_ramesh_01", "PENDING_APPROVAL", now),
        ("TASK-COL-002", org_id, "INV-1003", "CUST-004", 2, "2026-08-25", "Dear Balaji Mfg, invoice INV/2026/1003 of ₹1,60,000 is 6 days overdue. Kindly settle at: https://rzp.io/i/nexus_balaji_03", "PENDING_APPROVAL", now),
        ("TASK-COL-003", org_id, "INV-1004", "CUST-005", 3, "2026-08-25", "URGENT: Kiran Events invoice INV/2026/1004 of ₹1,00,000 is 21 days overdue. Please review immediately or call us.", "PENDING_APPROVAL", now)
    ]
    cur.executemany("INSERT OR REPLACE INTO collections_queue VALUES (?,?,?,?,?,?,?,?,?)", collections)

    # 6. Audit Logs
    audit = [
        ("LOG-001", org_id, "INVOICE_GENERATION", "Sales Agent", "Generated Invoice INV/2026/1002 for Kumar Enterprises (₹1,20,000)", json.dumps({"invoice_id": "INV-1002"}), now - 86400*6),
        ("LOG-002", org_id, "COLLECTIONS_RADAR", "Collections Agent", "Detected 3 overdue invoices totaling ₹4,00,000. Prepared WhatsApp collection plan.", json.dumps({"overdue_count": 3}), now)
    ]
    cur.executemany("INSERT OR REPLACE INTO audit_logs VALUES (?,?,?,?,?,?,?)", audit)

    conn.commit()
    conn.close()
    print("[DEMO_SEED] Successfully seeded ABC Distributors demo environment with 5 customers, 5 invoices, and collections queue!")

if __name__ == "__main__":
    seed_demo_company()
