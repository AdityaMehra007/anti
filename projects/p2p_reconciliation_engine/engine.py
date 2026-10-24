"""
Enterprise Procure-to-Pay (P2P) 3-Way Match & Vendor Reconciliation Engine
Core logic for matching POs, GRNs, and Invoices with automated SLA penalty calculation.
"""
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Tuple, Optional


@dataclass
class PurchaseOrder:
    po_id: str
    vendor_id: str
    vendor_name: str
    item_code: str
    ordered_qty: float
    unit_price: float
    total_amount: float
    created_at: str
    expected_delivery: str


@dataclass
class GoodsReceiptNote:
    grn_id: str
    po_id: str
    received_qty: float
    accepted_qty: float
    rejected_qty: float
    delivery_date: str
    receiving_location: str


@dataclass
class VendorInvoice:
    invoice_id: str
    po_id: str
    vendor_id: str
    billed_qty: float
    billed_unit_price: float
    billed_total: float
    invoice_date: str


@dataclass
class ReconciliationResult:
    reconciliation_id: str
    po_id: str
    invoice_id: str
    vendor_name: str
    match_status: str  # APPROVED, PRICE_VARIANCE, QTY_VARIANCE, SLA_PENALTY_APPLIED, REJECTED
    po_amount: float
    invoice_amount: float
    variance_amount: float
    penalty_amount: float
    net_payable: float
    discrepancy_reason: str
    reconciled_at: str


class P2PReconciliationEngine:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        if db_path == ":memory:":
            self._persistent_conn = sqlite3.connect(":memory:")
        else:
            self._persistent_conn = None
        self._init_db()

    def _get_connection(self):
        if self._persistent_conn is not None:
            return self._persistent_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            po_id TEXT PRIMARY KEY,
            vendor_id TEXT,
            vendor_name TEXT,
            item_code TEXT,
            ordered_qty REAL,
            unit_price REAL,
            total_amount REAL,
            created_at TEXT,
            expected_delivery TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goods_receipt_notes (
            grn_id TEXT PRIMARY KEY,
            po_id TEXT,
            received_qty REAL,
            accepted_qty REAL,
            rejected_qty REAL,
            delivery_date TEXT,
            receiving_location TEXT,
            FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor_invoices (
            invoice_id TEXT PRIMARY KEY,
            po_id TEXT,
            vendor_id TEXT,
            billed_qty REAL,
            billed_unit_price REAL,
            billed_total REAL,
            invoice_date TEXT,
            FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reconciliation_ledger (
            reconciliation_id TEXT PRIMARY KEY,
            po_id TEXT,
            invoice_id TEXT,
            vendor_name TEXT,
            match_status TEXT,
            po_amount REAL,
            invoice_amount REAL,
            variance_amount REAL,
            penalty_amount REAL,
            net_payable REAL,
            discrepancy_reason TEXT,
            reconciled_at TEXT
        )
        """)
        conn.commit()
        if self._persistent_conn is None:
            conn.close()

    def add_purchase_order(self, po: PurchaseOrder):
        conn = self._get_connection()
        conn.execute(
            "INSERT OR REPLACE INTO purchase_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (po.po_id, po.vendor_id, po.vendor_name, po.item_code, po.ordered_qty,
             po.unit_price, po.total_amount, po.created_at, po.expected_delivery)
        )
        conn.commit()
        if self._persistent_conn is None:
            conn.close()

    def add_grn(self, grn: GoodsReceiptNote):
        conn = self._get_connection()
        conn.execute(
            "INSERT OR REPLACE INTO goods_receipt_notes VALUES (?, ?, ?, ?, ?, ?, ?)",
            (grn.grn_id, grn.po_id, grn.received_qty, grn.accepted_qty, grn.rejected_qty,
             grn.delivery_date, grn.receiving_location)
        )
        conn.commit()
        if self._persistent_conn is None:
            conn.close()

    def add_invoice(self, inv: VendorInvoice):
        conn = self._get_connection()
        conn.execute(
            "INSERT OR REPLACE INTO vendor_invoices VALUES (?, ?, ?, ?, ?, ?, ?)",
            (inv.invoice_id, inv.po_id, inv.vendor_id, inv.billed_qty, inv.billed_unit_price,
             inv.billed_total, inv.invoice_date)
        )
        conn.commit()
        if self._persistent_conn is None:
            conn.close()

    def perform_3way_match(
        self,
        po_id: str,
        invoice_id: str,
        qty_tolerance_pct: float = 0.0,
        price_tolerance_pct: float = 0.0,
        late_penalty_rate_pct: float = 15.0
    ) -> ReconciliationResult:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM purchase_orders WHERE po_id = ?", (po_id,))
        po_row = cursor.fetchone()
        if not po_row:
            if self._persistent_conn is None:
                conn.close()
            raise ValueError(f"PO {po_id} not found")

        cursor.execute("SELECT * FROM goods_receipt_notes WHERE po_id = ?", (po_id,))
        grn_row = cursor.fetchone()
        if not grn_row:
            if self._persistent_conn is None:
                conn.close()
            raise ValueError(f"GRN for PO {po_id} not found")

        cursor.execute("SELECT * FROM vendor_invoices WHERE invoice_id = ?", (invoice_id,))
        inv_row = cursor.fetchone()
        if not inv_row:
            if self._persistent_conn is None:
                conn.close()
            raise ValueError(f"Invoice {invoice_id} not found")

        # PO Fields: (po_id, vendor_id, vendor_name, item_code, ordered_qty, unit_price, total_amount, created_at, expected_delivery)
        vendor_name = po_row[2]
        po_qty = po_row[4]
        po_unit_price = po_row[5]
        po_total = po_row[6]
        expected_delivery = po_row[8]

        # GRN Fields: (grn_id, po_id, received_qty, accepted_qty, rejected_qty, delivery_date, receiving_location)
        accepted_qty = grn_row[3]
        delivery_date = grn_row[5]

        # Invoice Fields: (invoice_id, po_id, vendor_id, billed_qty, billed_unit_price, billed_total, invoice_date)
        billed_qty = inv_row[3]
        billed_unit_price = inv_row[4]
        billed_total = inv_row[5]

        discrepancies = []
        match_status = "APPROVED"
        penalty_amount = 0.0

        # 1. Quantity Matching (Invoice vs GRN Accepted Qty)
        if billed_qty > accepted_qty:
            discrepancies.append(f"Billed Qty ({billed_qty}) exceeds Accepted GRN Qty ({accepted_qty})")
            match_status = "QTY_VARIANCE"

        # 2. Price Matching (Invoice vs PO Rate Card)
        price_diff = billed_unit_price - po_unit_price
        if price_diff > (po_unit_price * (price_tolerance_pct / 100.0)):
            discrepancies.append(f"Billed Unit Price ({billed_unit_price}) exceeds Contracted Rate ({po_unit_price})")
            match_status = "PRICE_VARIANCE"

        # 3. Delivery SLA Check (Delivery Date vs Expected Date)
        d_exp = datetime.strptime(expected_delivery, "%Y-%m-%d")
        d_del = datetime.strptime(delivery_date, "%Y-%m-%d")
        if d_del > d_exp:
            penalty_amount = billed_total * (late_penalty_rate_pct / 100.0)
            discrepancies.append(f"Late delivery penalty applied ({late_penalty_rate_pct}% of invoice: -₹{penalty_amount:.2f})")
            if match_status == "APPROVED":
                match_status = "SLA_PENALTY_APPLIED"

        variance_amount = billed_total - po_total
        net_payable = max(0.0, (accepted_qty * po_unit_price) - penalty_amount)

        if len(discrepancies) > 1 and "QTY_VARIANCE" in match_status and "PRICE_VARIANCE" in match_status:
            match_status = "REJECTED"

        recon_id = f"REC-{po_id}-{invoice_id}"
        reason_str = " | ".join(discrepancies) if discrepancies else "3-Way Match Verified (100% SLA Adherence)"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = ReconciliationResult(
            reconciliation_id=recon_id,
            po_id=po_id,
            invoice_id=invoice_id,
            vendor_name=vendor_name,
            match_status=match_status,
            po_amount=po_total,
            invoice_amount=billed_total,
            variance_amount=variance_amount,
            penalty_amount=penalty_amount,
            net_payable=net_payable,
            discrepancy_reason=reason_str,
            reconciled_at=now_str
        )

        conn.execute(
            "INSERT OR REPLACE INTO reconciliation_ledger VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (result.reconciliation_id, result.po_id, result.invoice_id, result.vendor_name,
             result.match_status, result.po_amount, result.invoice_amount, result.variance_amount,
             result.penalty_amount, result.net_payable, result.discrepancy_reason, result.reconciled_at)
        )
        conn.commit()
        if self._persistent_conn is None:
            conn.close()

        return result

    def get_summary_metrics(self) -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(invoice_amount), SUM(net_payable), SUM(penalty_amount) FROM reconciliation_ledger")
        total_count, total_invoiced, total_payable, total_penalty = cursor.fetchone()

        cursor.execute("SELECT match_status, COUNT(*) FROM reconciliation_ledger GROUP BY match_status")
        status_counts = dict(cursor.fetchall())
        if self._persistent_conn is None:
            conn.close()

        total_invoiced = total_invoiced or 0.0
        total_payable = total_payable or 0.0
        total_penalty = total_penalty or 0.0
        approved_count = status_counts.get("APPROVED", 0) + status_counts.get("SLA_PENALTY_APPLIED", 0)
        match_rate = (approved_count / total_count * 100) if total_count else 0.0

        return {
            "total_reconciled": total_count or 0,
            "total_invoiced_inr": total_invoiced,
            "total_payable_inr": total_payable,
            "total_penalty_recovered_inr": total_penalty,
            "match_rate_pct": round(match_rate, 2),
            "breakdown": status_counts
        }
