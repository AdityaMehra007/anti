# SOURCE REGISTRY & DATA ACQUISITION DICTIONARY
**Domain:** Bangalore Enterprise Sourcing & Public Business Intelligence  
**Compliance Standard:** 100% Publicly Available Professional/Business Information Only  

---

## 1. Verified Primary Data Sources

| Source Identifier | Source Category | Access Method | Target Fields Extracted | Verification Frequency | Privacy Classification |
|:---|:---|:---|:---|:---:|:---:|
| **SRC-BLR-01** | **Tech Park Tenant Directories** | Physical Directory / Official Web Portals | Company Name, Building/Tower, SEZ Status, Facility Desk Line | Monthly | Public Corporate |
| **SRC-BLR-02** | **Corporate Career Portals** | Automated Crawlers (`jobspy_market_scraper.py`) | Requisition ID, Job Title, Dept, Experience, Location, Job Specs | Hourly (Active Cron) | Public Corporate |
| **SRC-BLR-03** | **MCA (Ministry of Corporate Affairs)** | Public Corporate Filings | Registered Entity Name, CIN, Registered Office Address, Directors | Quarterly | Public Statutory |
| **SRC-BLR-04** | **BSE / NSE Listed Filings** | Exchange Corporate Disclosures | Market Cap, Corporate Headquarters, Key Management Personnel (KMP) | Daily Market Hours | Public Financial |
| **SRC-BLR-05** | **Public HR Directory Ledger** | `ALL_HR_NAMES_AND_NUMBERS...csv` (7,501 entries) | Recruiter Name, Title, Corporate Desk Phone, Official Corporate Email | Real-time ACID DB | Public Professional |
| **SRC-BLR-06** | **Unicorn Valuation Database** | Verified Financial Reporting & Venture Trajectory | Valuation, Funding Velocity, Time to \$1B, Bengaluru Operations | Real-time DB | Public Commercial |

---

## 2. Field Schema & Validation Rules

```json
{
  "company_name": "Official Registered Business Entity",
  "tech_corridor": "One of: ORR, Whitefield, Manyata, Koramangala, E-City, CBD",
  "industry_sector": "GCC, FinTech, E-Commerce, SCM/Logistics, AI/Cloud, Aerospace",
  "corporate_desk_phone": "+91-80-XXXX-XXXX (Official Switchboard/Desk only)",
  "official_hr_email": "first.last@company.com or careers@company.com",
  "strategic_role_fit": "Founder's Office, BizOps, SCM & EXIM Governance, AI Data Ops",
  "salary_benchmark_lpa": "₹7.0L to ₹18.0L LPA",
  "privacy_rating": "STRICT_PUBLIC_BUSINESS_ONLY"
}
```

---

## 3. Disallowed Sourcing Protocols

- ❌ Scraping personal WhatsApp numbers or private mobile phones.
- ❌ Extracting private personal addresses or personal Gmail/Yahoo accounts for executives.
- ❌ Purchasing third-party scraped lead databases.
- ❌ Automated crawling behind authenticated paywalls without explicit session authorization.
