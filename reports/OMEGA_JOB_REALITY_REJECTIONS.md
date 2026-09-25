# OMEGA JOB REALITY REJECTIONS REPORT

**Audit Date**: 2026-08-26  
**Auditor**: Sovereign Antigravity Reality Auditor  
**Scope**: Forensic Analysis of all 20 Initial Job Records  

---

## Complete Audit & Rejection Matrix

| Job ID | Company | Claimed Role | Source URL Probed | Probe Result | Forensic Verdict & Rejection Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `JOB-AMZN-001` | Amazon Global Ops | Global Trade Analyst | `amazon.jobs/.../2648192` | **HTTP 404 (Not Found)** | Synthetic template requisition ID. Requisition does not exist on Amazon portal. |
| `JOB-TGT-004` | Target in India | Inventory Specialist | `india.target.com/careers/...` | **HTTP 200 (Redirect to Home)** | Generic careers landing page. No specific active vacancy matched. |
| `JOB-MAERSK-002` | A.P. Moller - Maersk | Logistics Specialist | `maersk.com/.../logistics-specialist-blr` | **HTTP 404 (Not Found)** | Synthetic slug. Requisition does not exist on Maersk careers portal. |
| `JOB-SCHN-003` | Schneider Electric | Supply Chain Analyst | `se.com/careers/in/...` | **HTTP 403 (Forbidden)** | Blocked automated verification / synthetic slug. Cannot be confirmed without live browser session. |
| `JOB-DHL-005` | DHL Global Forwarding | Freight Coordinator | `careers.dhl.com/...` | **HTTP 410 (Gone)** | Requisition has expired or synthetic path does not exist. |
| `JOB-ACCN-006` | Accenture Solutions | Operations Analyst | `accenture.com/...` | **HTTP 200 (Generic Search)** | Generic portal root. Individual requisition not corroborated. |
| `JOB-MSFT-007` | Microsoft IDC | Commercial Operations | `careers.microsoft.com/.../1682910` | **HTTP 200 (Job Portal Root)** | Requisition ID was a seed template. Must be extracted live. |
| `JOB-GOOG-008` | Google India GCC | Customer Solutions | `google.com/.../98217340` | **HTTP 404 on Apply URL** | Apply URL failed resolution. Synthetic requisition ID. |
| `JOB-DELL-009` | Dell Technologies | Supply Chain Planner | `jobs.dell.com/.../592819` | **HTTP 200 (Generic Portal)** | Template path; individual posting requires live search. |
| `JOB-WMT-010` | Walmart Global Tech | Retail Tech Ops | `careers.walmart.com/...` | **HTTP 200 (Generic Portal)** | Seed template slug. |
| `JOB-CSCO-011` | Cisco Systems | Global Trade Specialist | `jobs.cisco.com/.../140291` | **HTTP 200 (Generic Portal)** | Seed template requisition. |
| `JOB-GS-012` | Goldman Sachs | Trade Analyst | `goldmansachs.com/...` | **HTTP 404 (Not Found)** | Synthetic URL path. |
| `JOB-JPMC-013` | JPMorgan Chase | Operations Analyst | `jpmc.fa.oraclecloud.com/...` | **HTTP 200 (Oracle HCM Root)** | Generic candidate experience root; no specific req ID verified. |
| `JOB-BOSCH-014` | Bosch Global Tech | Procurement Specialist | `careers.smartrecruiters.com/...` | **HTTP 404 on Apply URL** | Apply endpoint broken/synthetic. |
| `JOB-SHELL-015` | Shell Business Ops | Trade Operations Specialist | `jobs.shell.com/...` | **HTTP 200 (Generic Portal)** | Seed template path. |
| `JOB-STAN-016` | Standard Chartered | Trade Finance Analyst | `scb.taleo.net/...` | **DNS Failure (getaddrinfo)** | Domain has migrated/changed. URL is broken. |
| `JOB-UL-017` | Unilever Global Ops | Supply Chain Customer Ops | `unilever.taleo.net/...` | **DNS Failure (getaddrinfo)** | Domain has migrated/changed. URL is broken. |
| `JOB-FDX-018` | FedEx Express India | Customs Specialist | `fedex.wd1.myworkdayjobs.com/...` | **HTTP 404 (Not Found)** | Synthetic Workday slug. |
| `JOB-IBM-019` | IBM India | Procurement Analyst | `ibm.com/careers/...` | **HTTP 200 (Generic Portal)** | Seed template path. |
| `JOB-FK-020` | Flipkart | Logistics Strategy | `flipkartcareers.com/...` | **Connection Timeout** | Host unreachable during probe. |
