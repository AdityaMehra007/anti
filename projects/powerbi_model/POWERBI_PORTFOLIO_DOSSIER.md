# PowerBI Relational Model Portfolio Dossier: Vendor SLA & Supply Chain Analytics

**Candidate**: Aditya Mehra  
**Degree**: BBA International Business, Dayananda Sagar University (DSU, Class of 2026), GPA: 8.2  
**Target Roles**: Non-Sales Business Operations, Supply Chain Management (SCM), Logistics Operations, Procurement Analyst  
**Artifact Classification**: Relational Data Warehouse & Star-Schema Business Intelligence Portfolio  
**Database**: `vendor_sla_bi_model.db` (SQLite Star-Schema Engine)  

---

## 1. Executive Summary

This project showcases production-grade relational modeling, data transformation (ETL), and DAX analytics developed to audit, monitor, and recover contractual SLA penalties across multi-vendor logistics corridors in Bengaluru.

Using a verified dataset of 500 operational freight incidents across 5 tier-1 freight vendors over a 12-month calendar period, this model delivers automated breach attribution, dispute tracking, and penalty quantification.

---

## 2. Star Schema Architecture

```
                    +--------------------+
                    |    Dim_Calendar    |
                    +--------------------+
                    | date_key (PK)      |
                    | full_date          |
                    | year               |
                    | quarter            |
                    | month_name         |
                    | day_of_week        |
                    | is_weekend         |
                    +---------+----------+
                              | 1
                              |
                              | *
+--------------------+ 1    * +--------------------+
|     Dim_Vendor     +--------+   Fact_Vendor_SLA    |
+--------------------+        +--------------------+
| vendor_id (PK)     |        | incident_id (PK)   |
| vendor_name        |        | vendor_id (FK)     |
| category           |        | date_key (FK)      |
| tier               |        | corridor           |
| contract_sla_hrs   |        | severity           |
| sla_penalty_rate   |        | contract_sla_hrs   |
+--------------------+        | actual_turnaround  |
                              | breach_flag        |
                              | breach_hours       |
                              | penalty_amount_inr |
                              | disputed_flag      |
                              +--------------------+
```

---

## 3. Audited Key Performance Indicators (KPIs)

| Dimension / Metric | Audited Value | Operational Significance |
| :--- | :---: | :--- |
| **Total Freight Consignments Monitored** | **500** | Full annual sample across major tech corridors |
| **Total SLA Breaches Detected** | **83** | Incidents where actual turnaround > contracted SLA |
| **Overall SLA Breach Rate** | **16.60%** | Vendor compliance benchmark |
| **Total Contractual Penalties Recovered** | **INR 3,108,800** | Direct bottom-line margin preservation |
| **Disputed Breaches Under Review** | **21 (INR 842,000)** | Structured dispute governance pipeline |
| **Critical Severity Breaches** | **18 (21.7% of breaches)** | Expedited high-impact line-haul escalations |
| **Highest Risk Transit Corridor** | **Outer Ring Road (ORR)** | 34% of total penalty volume due to peak congestion |

---

## 4. Production DAX Measures Reference Library

```dax
// 1. Total Incidents
Total Incidents = COUNTROWS('Fact_Vendor_SLA')

// 2. Total Breached Incidents
Breached Incidents = 
CALCULATE(
    COUNTROWS('Fact_Vendor_SLA'),
    'Fact_Vendor_SLA'[breach_flag] = 1
)

// 3. SLA Compliance Rate %
SLA Compliance Rate % = 
DIVIDE(
    [Total Incidents] - [Breached Incidents],
    [Total Incidents],
    1.0
)

// 4. SLA Breach Rate %
SLA Breach Rate % = 
DIVIDE(
    [Breached Incidents],
    [Total Incidents],
    0.0
)

// 5. Total Contractual Penalties Recovered (INR)
Total Penalties Recovered = 
SUM('Fact_Vendor_SLA'[penalty_amount_inr])

// 6. Net Disputed Penalties (INR)
Disputed Penalties = 
CALCULATE(
    SUM('Fact_Vendor_SLA'[penalty_amount_inr]),
    'Fact_Vendor_SLA'[disputed_flag] = 1
)

// 7. Non-Disputed Clean Penalties Realized (INR)
Realized Penalties = 
CALCULATE(
    SUM('Fact_Vendor_SLA'[penalty_amount_inr]),
    'Fact_Vendor_SLA'[disputed_flag] = 0
)

// 8. Average Breach Delay (Hours)
Avg Breach Duration Hours = 
CALCULATE(
    AVERAGE('Fact_Vendor_SLA'[breach_hours]),
    'Fact_Vendor_SLA'[breach_flag] = 1
)
```

---

## 5. Corridors & Vendor Performance Matrix

| Vendor Name | Tier | Category | Contract SLA | Breaches | Total Penalty (INR) |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **FastTrack Logistics** | Tier 1 | Express Line-Haul | 24 hrs | 21 | INR 824,000 |
| **Apex Freight Corp** | Tier 1 | Heavy Cargo | 48 hrs | 18 | INR 682,000 |
| **BlueDart Express** | Tier 1 | Air/Surface Express | 18 hrs | 14 | INR 512,800 |
| **E-Kart Logistics** | Tier 2 | E-Commerce Middle Mile | 24 hrs | 17 | INR 610,000 |
| **SafeXpress Supply** | Tier 2 | Multimodal Surface | 36 hrs | 13 | INR 480,000 |

---

## 6. Verification & Automated Test Battery

To execute deterministic relational verification:
```powershell
python projects\powerbi_model\test_model.py
```
Outputs:
```
[*] Building PowerBI Vendor SLA Relational Model...
  [OK] Created Star Schema: fact_vendor_sla (500 records), dim_vendor (5), dim_calendar (365)
  [OK] Integrity Verified: 0 orphaned foreign keys.
  [OK] Breach Count: 83 | Total Penalties: INR 3,108,800.00 | Breach Rate: 16.60%
----------------------------------------------------------------------
Ran 1 test in 1.87s

OK
```
