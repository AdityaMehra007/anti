# Global Trade, Incoterms 2020 & UCP 600 Compliance Engine

An analytical computational engine verifying International Chamber of Commerce (ICC) UCP 600 Documentary Credit compliance and calculating landed customs duties under the Indian Customs Act, 1962 (Section 14).

## Business Context & Target Requisitions
- **HSBC EDPI**: Global Trade & Receivables Finance Operations (`BLR-JOB-014`)
- **Accenture**: Regulatory Compliance New Associate (`AIOC-S01667647`)
- **TE Connectivity**: Global Supply Chain & EXIM Operations (`BLR-JOB-010`)
- **Deloitte US-India**: Risk & Commercial Advisory Analyst (`BLR-JOB-002`)

## Core Capabilities
1. **ICC UCP 600 Documentary Credit Verification**:
   - **Art 14c**: 21-Day presentation rule after transport document issuance date.
   - **Art 18a**: Exact beneficiary alignment on Commercial Invoices.
   - **Art 20a / 27**: Clean on Board Bill of Lading verification and port matching.
   - **Art 30b**: Permitted drawdown tolerance validation (+/- 5%).
2. **Indian Customs Landed Cost Calculation**:
   - Assessable Value (CIF) computation: $(FOB + Freight + Insurance) \times Exchange Rate$.
   - Basic Customs Duty (BCD) computation.
   - Social Welfare Surcharge (SWS at 10% of BCD, Finance Act 2018).
   - Integrated Goods and Services Tax (IGST on landed base).
3. **Interactive Visual Cockpit**:
   - Generates standalone dashboard `exim_compliance_cockpit.html`.

## Execution & Test Suite
```bash
# Run Pytest Suite (100% Green)
python -m pytest test_exim_validator.py -v

# Run Demonstration Batch
python demo_cases.py

# Export Visual Cockpit
python export_cockpit.py
```
