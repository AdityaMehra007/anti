# PORTFOLIO PROJECT 2: TIER-1 VENDOR SLA GOVERNANCE & RATE CARD RECONCILIATION
**Author & Model Architect**: Aditya Mehra  
**Curriculum & Practical Context**: BBA in International Business | Commercial Operations & Vendor Management  
**Application Field**: Enterprise Procurement, Event Production Governance, Supply Chain Discrepancy Auditing  
**Executable Code**: [`portfolio/PROJECT_2_VENDOR_SLA_COST_MODEL.py`](file:///e:/anti/portfolio/PROJECT_2_VENDOR_SLA_COST_MODEL.py)  

---

## 1. The Core Business Problem
In high-velocity event deployments, retail rollouts, and operations activations (e.g. Tata Communications, Puma, Dyson, Aero India), vendors often submit invoices containing:
1. **Rate Card Creep**: Billing above contracted master service rates.
2. **Unpenalized Operational Delays**: Failure to deliver staging, cold-chain catering, or merchandise within contracted turnaround times.
3. **Absence of Audit Trail**: Approving invoices blindly without mathematical validation against run-of-show timestamps.

---

## 2. The Solution: Automated Reconciliation & Margin Recovery Engine
The Python engine performs a dual-pass reconciliation across every vendor disbursement:
- **Pass 1: Master Rate Card Audit**: Matches invoiced line items against agreed rate cards. Any rate variance overcharge is automatically disallowed.
- **Pass 2: Timestamp SLA Verification**: Compares delivery gate-pass timestamps against scheduled handover deadlines. Beyond a 15-minute operational grace window, contractually defined liquidated damages (3% to 15% per hour) are systematically deducted from the disbursement.

---

## 3. Sample Live Test Output & Metrics

```
Invoice ID      Vendor                         Billed (INR)   Approved       Savings    Status
───────────────────────────────────────────────────────────────────────────────────────────────────
INV-2025-0891   Bangalore AudioVisuals & Sta   ₹85,000.00     ₹79,687.50     ₹5,312.50  ADJUSTED_PENALTY
INV-2025-0892   Apex Print & Apparel Works     ₹135,000.00    ₹120,000.00    ₹15,000.00 ADJUSTED_OVERCHARGE
INV-2025-0893   Yelahanka Fresh Logistics      ₹95,000.00     ₹78,375.00     ₹16,625.00 ADJUSTED_PENALTY
INV-2025-0894   Silicon Cabs & Fleet Ops       ₹45,000.00     ₹45,000.00     ₹0.00      APPROVED_CLEAN
───────────────────────────────────────────────────────────────────────────────────────────────────

EXECUTIVE RECONCILIATION SUMMARY:
  • Total Gross Invoiced Amount : ₹360,000.00
  • Disallowed Rate Overcharges : ₹15,000.00
  • SLA Delay Penalties Enforced : ₹21,937.50
  • Net Approved Disbursements  : ₹323,062.50
  • Total Capital Preserved     : ₹36,937.50 (10.26% Margin Protection Gain)
```

---

## 4. Relevance to Target Employers
- **Accenture & Deloitte (Operations Advisory / PMO)**: Shows direct competence in contract governance, risk registers, and financial variance modeling.
- **Amazon (Vendor Management)**: Demonstrates strict supplier SLA enforcement and metrics-driven vendor scorecards.
- **Puma / Retail Enterprises**: Proves protection of gross margins across commercial partner networks.
