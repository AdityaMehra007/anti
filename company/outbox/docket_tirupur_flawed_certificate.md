# VECTIS TRADE PRE-SUBMISSION AUDIT CERTIFICATE
**Certificate ID**: `VECTIS-LC-TIRUPUR-2027-104-20260914181646`  
**Verification Date**: 2026-09-14T18:16:46Z  
**Governing Rules**: ICC UCP 600 / ISBP 745 Compliance Standard  
**Cryptographic Seal (SHA-256)**: `8e5330b4ba5223a42a640fbad1abb8bb244ba8ceb878fad5d820fdcd455e1449`  

---

## 1. Compliance Determination
### Status: **🔴 REJECT (DISCREPANCIES DETECTED)**
- **Total Discrepancies Found**: 2
- **Fatal Rejection Discrepancies**: 2

---

## 2. Trade Docket Summary
| Parameter | Value |
| :--- | :--- |
| **Letter of Credit No.** | `LC-TIRUPUR-2027-104` |
| **Issuing Bank** | BNP Paribas, Paris |
| **Beneficiary (Exporter)** | Tirupur Premier Apparel Exports |
| **Applicant (Buyer)** | Galeries de Mode SAS |
| **Commercial Invoice** | TPA/2027/412 (EUR 95,000.00) |
| **Bill of Lading** | MAEU88192031 (Shipped: 2027-03-28) |
| **Audited Gross Weight** | 6,850.00 KG |

---

## 3. Discrepancy Diagnostics & Remediation

### Discrepancy #1: [DISC-INV-005] description_of_goods
- **Severity**: **FATAL (BANK WILL REJECT)**
- **Governing Rule**: `UCP 600 Art 18(c)`
- **Affected Document**: Commercial Invoice
- **Defect Description**: Invoice goods description does not match LC Field 45A verbatim. Found: 'Cotton Knitted T-Shirts Style TK-90', Required: '100% Organic Combed Cotton Knitted T-Shirts Style TK-90'.
- **Required Remediation**: Update invoice goods description to match LC verbatim: '100% Organic Combed Cotton Knitted T-Shirts Style TK-90'.

---

### Discrepancy #2: [DISC-XDOC-002] gross_weight_kg
- **Severity**: **FATAL (BANK WILL REJECT)**
- **Governing Rule**: `ISBP 745 Para E28 / UCP 600 Art 14(d)`
- **Affected Document**: Packing List vs Bill of Lading
- **Defect Description**: Gross weight conflict exceeds tolerance: Packing List shows 6,200.00 KG, while BL shows 6,850.00 KG (10.48% variance).
- **Required Remediation**: Amend Bill of Lading shipping instruction to reflect exact gross weight: 6,200.00 KG.

---

## 4. Legal & Verification Disclaimer
*This audit was executed deterministically by VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED. Certificate hash `8e5330b4ba5223a4...` is registered in the VECTIS immutable verification ledger.*
