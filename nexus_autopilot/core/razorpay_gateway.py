"""
NEXUS AUTOPILOT - Razorpay Payment Link Gateway & Webhook Reconciliation
Creates simulated/live Razorpay payment links and reconciles inbound webhook payments to invoices.
"""
import sqlite3
import time
import json
from pathlib import Path
from typing import Dict, Any

DB_PATH = Path(r"e:\anti\nexus_autopilot\data\nexus.db")

class RazorpayGateway:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def create_payment_link(self, org_id: str, invoice_id: str, customer_id: str, customer_name: str, phone: str, amount_inr: float, description: str) -> Dict[str, Any]:
        link_id = f"plink_{int(time.time()*1000)}"
        payment_url = f"https://rzp.io/i/nexus_{link_id[-8:]}"

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "UPDATE invoices SET payment_link_id = ?, payment_link_url = ?, status = 'SENT', updated_at = ? WHERE invoice_id = ?",
            (link_id, payment_url, time.time(), invoice_id)
        )
        conn.commit()
        conn.close()

        return {
            "payment_link_id": link_id,
            "invoice_id": invoice_id,
            "customer_name": customer_name,
            "amount_inr": amount_inr,
            "payment_url": payment_url,
            "status": "CREATED_AND_LINKED"
        }

    def process_webhook_payment(self, org_id: str, invoice_id: str, razorpay_payment_id: str, amount_inr: float) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # 1. Fetch invoice & customer
        cur.execute("SELECT customer_id, total_amount, amount_paid FROM invoices WHERE invoice_id = ?", (invoice_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return {"status": "ERROR", "reason": "INVOICE_NOT_FOUND"}

        cust_id, total_amt, prev_paid = row
        new_paid = prev_paid + amount_inr
        inv_status = "PAID" if new_paid >= total_amt else "PARTIAL"

        # 2. Record Payment
        pay_id = f"PAY-{int(time.time()*1000)}"
        cur.execute(
            "INSERT INTO payments VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (pay_id, org_id, invoice_id, cust_id, amount_inr, "INR", "RAZORPAY", razorpay_payment_id, f"order_{pay_id[-6:]}", "SUCCESS", time.time(), 1)
        )

        # 3. Update Invoice
        cur.execute("UPDATE invoices SET amount_paid = ?, status = ?, updated_at = ? WHERE invoice_id = ?", (new_paid, inv_status, time.time(), invoice_id))

        # 4. Update Customer Balance
        cur.execute("UPDATE customers SET total_paid = total_paid + ?, outstanding_balance = outstanding_balance - ? WHERE customer_id = ?", (amount_inr, amount_inr, cust_id))

        conn.commit()
        conn.close()

        return {
            "payment_id": pay_id,
            "invoice_id": invoice_id,
            "amount_paid": amount_inr,
            "invoice_status": inv_status,
            "reconciliation": "AUTOMATICALLY_RECONCILED",
            "audit": "LEDGER_MUTATED_SUCCESSFULLY"
        }

if __name__ == "__main__":
    rzp = RazorpayGateway()
    link = rzp.create_payment_link("ORG-ABC-001", "INV-1002", "CUST-002", "Kumar Enterprises", "+919845023456", 120000.0, "Stretch Film Packaging")
    print(f"[RAZORPAY] Payment link generated:\n{json.dumps(link, indent=2)}")
