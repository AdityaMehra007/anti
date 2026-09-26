---
name: omega-capital-allocation
description: FP&A modeling, unit economics evaluation, and risk-adjusted capital allocation enforcing Section 33 and Section 34 of OMEGA Constitution.
---

# OMEGA Capital Allocation Skill

This skill operationalizes Section 33 (Financial Engine) and Section 34 (Capital Allocation Engine) of [`OMEGA_CONSTITUTION.md`](../../OMEGA_CONSTITUTION.md).

## 1. Core Financial Invariants
- **Revenue ≠ Profit**: Never optimize for gross volume at negative margins.
- **Profit ≠ Cash Flow**: Working capital and payment terms dictate true solvency.
- **Valuation ≠ Cash**: Paper net worth cannot pay operational bills.
- **Growth ≠ Value**: Scaling an unvalidated, cash-burning model destroys equity.

## 2. Resource Allocation Protocol (Section 34)
Allocate capital and compute strictly based on risk-adjusted Expected Value (EV):
$$EV = \sum (P_i \times Upside_i) - Downside$$

Distribute among:
1. Core Business (cash-flow foundation)
2. Growth & Distribution (proven CAC/LTV channels)
3. R&D & Engineering (deepening moats)
4. Strategic Reserves (minimum 6 months runway buffer)

## 3. High-Impact Approval Safeguard (Section 77)
Autonomous agents may NEVER trigger:
- Financial wire transfers, bank account transactions, or credit card charges.
- Legally binding investment agreements or equity promises.
All financial transactions require explicit human sign-off.
