"""
Enterprise Demo Data Seeder for P2P Reconciliation Engine
Generates realistic multi-tier vendor orders, receipts, and invoices.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from engine import P2PReconciliationEngine, PurchaseOrder, GoodsReceiptNote, VendorInvoice

DB_PATH = os.path.join(os.path.dirname(__file__), "p2p_engine.db")

def seed_demo_data(db_path: str = DB_PATH):
    engine = P2PReconciliationEngine(db_path)

    scenarios = [
        # 1. Clean Match: Aviation Logistics Fabrication (Aero India Vendor)
        {
            "po": PurchaseOrder("PO-2026-001", "VEND-AERO-01", "AeroStruct Logistics Ltd", "STAGING-POD-01", 50.0, 12000.0, 600000.0, "2026-02-01", "2026-02-08"),
            "grn": GoodsReceiptNote("GRN-2026-001", "PO-2026-001", 50.0, 50.0, 0.0, "2026-02-07", "Yelahanka AFS Staging Bay 3"),
            "inv": VendorInvoice("INV-2026-001", "PO-2026-001", "VEND-AERO-01", 50.0, 12000.0, 600000.0, "2026-02-09")
        },
        # 2. SLA Late Delivery (Brand Activation Truss Supply - 15% Penalty Clause)
        {
            "po": PurchaseOrder("PO-2026-002", "VEND-EVENT-02", "Apex Display Engineering", "TRUSS-ALU-10M", 20.0, 15000.0, 300000.0, "2026-03-01", "2026-03-05"),
            "grn": GoodsReceiptNote("GRN-2026-002", "PO-2026-002", 20.0, 20.0, 0.0, "2026-03-07", "Indiranagar Event Hub"),  # 2 days late
            "inv": VendorInvoice("INV-2026-002", "PO-2026-002", "VEND-EVENT-02", 20.0, 15000.0, 300000.0, "2026-03-08")
        },
        # 3. Quantity Discrepancy (Damaged Goods Rejected at Receiving)
        {
            "po": PurchaseOrder("PO-2026-003", "VEND-PRINT-03", "Koramangala Print Craft", "VINYL-BACKLIT-200", 100.0, 1800.0, 180000.0, "2026-04-10", "2026-04-12"),
            "grn": GoodsReceiptNote("GRN-2026-003", "PO-2026-003", 100.0, 80.0, 20.0, "2026-04-12", "HSR Central Warehouse"), # 20 damaged
            "inv": VendorInvoice("INV-2026-003", "PO-2026-003", "VEND-PRINT-03", 100.0, 1800.0, 180000.0, "2026-04-13")  # Billed for 100 instead of 80
        },
        # 4. Price Variance (Rate Card Inflation Discrepancy)
        {
            "po": PurchaseOrder("PO-2026-004", "VEND-AUDIO-04", "Sonic Wave AV Systems", "LINE-ARRAY-SPEAKER", 8.0, 25000.0, 200000.0, "2026-05-01", "2026-05-03"),
            "grn": GoodsReceiptNote("GRN-2026-004", "PO-2026-004", 8.0, 8.0, 0.0, "2026-05-03", "Palace Grounds Main Arena"),
            "inv": VendorInvoice("INV-2026-004", "PO-2026-004", "VEND-AUDIO-04", 8.0, 28000.0, 224000.0, "2026-05-04")  # 28k instead of agreed 25k
        },
        # 5. Clean Enterprise Server Racks (IT GCC Procurement)
        {
            "po": PurchaseOrder("PO-2026-005", "VEND-TECH-05", "Bengaluru Tech Fabricators", "RACK-42U-COOLING", 10.0, 45000.0, 450000.0, "2026-06-15", "2026-06-20"),
            "grn": GoodsReceiptNote("GRN-2026-005", "PO-2026-005", 10.0, 10.0, 0.0, "2026-06-19", "RMZ Ecoworld Server Room B"),
            "inv": VendorInvoice("INV-2026-005", "PO-2026-005", "VEND-TECH-05", 10.0, 45000.0, 450000.0, "2026-06-20")
        }
    ]

    for item in scenarios:
        engine.add_purchase_order(item["po"])
        engine.add_grn(item["grn"])
        engine.add_invoice(item["inv"])
        engine.perform_3way_match(item["po"].po_id, item["inv"].invoice_id)

    metrics = engine.get_summary_metrics()
    print("[SUCCESS] Seeded P2P Reconciliation Database.")
    print(f"Total Invoiced: INR {metrics['total_invoiced_inr']:,.2f}")
    print(f"Total Approved/Payable: INR {metrics['total_payable_inr']:,.2f}")
    print(f"Penalties Recovered: INR {metrics['total_penalty_recovered_inr']:,.2f}")
    print(f"Match Rate: {metrics['match_rate_pct']}%")
    return engine

if __name__ == "__main__":
    seed_demo_data()
