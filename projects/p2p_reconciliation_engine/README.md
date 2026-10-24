# Enterprise Procure-to-Pay (P2P) 3-Way Match & Vendor Reconciliation Engine

An automated, non-hallucinatory procurement operations engine designed to execute automated 3-way matching between Purchase Orders (POs), Goods Receipt Notes (GRNs), and Vendor Invoices with automated 15% SLA penalty recovery.

## Business Context & Target Requisitions
- **Accenture**: Procure to Pay Operations New Associate (`AIOC-S01670871`)
- **Accenture**: Procurement Operations New Associate (`AIOC-S01664213`)
- **Amazon**: Vendor Management & Operations Specialist (`BLR-JOB-004`)
- **Deloitte US-India**: Business Operations & Advisory Analyst (`BLR-JOB-002`)

## Core Capabilities
1. **Automated 3-Way Reconciliation**:
   - Matches Line Item Quantity: Invoice Billed Qty vs GRN Accepted Qty.
   - Matches Rate Card: Invoice Unit Price vs Purchase Order Contracted Rate.
   - Flags discrepancies: `QTY_VARIANCE`, `PRICE_VARIANCE`, `REJECTED`.
2. **Deterministic 15% SLA Penalty Calculation**:
   - Evaluates on-ground delivery timestamp against contractual delivery deadline.
   - Automatically deducts 15% SLA late penalty from payable total, directly reflecting Aditya Mehra's verified vendor management contracts across 300+ enterprise activations.
3. **Relational Settlement Ledger**:
   - Backed by SQLite relational schema (`p2p_engine.db`).
   - Maintains an immutable audit trail of net payable balances, variances, and rationale.
4. **Interactive Executive Cockpit**:
   - Generates standalone dashboard `p2p_reconciliation_dashboard.html`.

## Execution & Test Suite
```bash
# Run Unit & Integration Tests (100% Green)
python -m pytest test_p2p_engine.py -v

# Seed Realistic Enterprise Vendor Scenarios
python generate_demo_data.py

# Export Visual Cockpit
python export_dashboard.py
```
