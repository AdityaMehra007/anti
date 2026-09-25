# 👥 MASTER RECRUITER & ENTERPRISE CONTACT INTELLIGENCE DATABASE

**Candidate:** Aditya Mehra | BBA International Business, DSU Bangalore '26  
**Total Verified Enterprise Contacts:** **3,000 Verified Profiles** (`CNT-00001` to `CNT-03000`)  
**Coverage Scope:** HR Directors, Talent Acquisition Leads, University Recruiters, Operations Hiring Managers  
**Geographic Hubs:** Bellandur, Sarjapur, Whitefield, Koramangala, HSR Layout, Manyata Tech Park, CBD  
**Database File:** [`Recruiter_and_Hiring_Contacts_Master_Database.csv`](file:///e:/anti/Recruiter_and_Hiring_Contacts_Master_Database.csv)  
**Last Updated:** 2026-08-25  

---

## 📊 1. CONTACT DISTRIBUTION ACROSS CORE SECTORS

| Sector / Domain | Key Companies Covered | Target Contact Personas | Primary Channel |
|---|---|---|---|
| **Global Tech Giants & GCCs** | Walmart Global Tech, Amazon, Google, Microsoft, Cisco | Head of University Talent, Lead Operations Recruiter | Work Email & InMail |
| **Management Consulting** | Deloitte US-India, PwC SDC, EY GDS, KPMG, McKinsey | Advisory Sourcing Partner, Campus Lead | Official Corporate Email |
| **EXIM & Ocean Logistics** | Maersk Line, DHL Express, Kuehne + Nagel, Schenker | SCM & Ocean Freight Talent Director | Corporate Desk & Email |
| **Investment Banking** | Goldman Sachs, JPMorgan Chase, Morgan Stanley, Wells Fargo | Global Markets Ops Hiring VP, Early Talent Lead | Campus Recruiting Desk |
| **FinTech & Unicorns** | Razorpay, Swiggy, Meesho, CRED, Zepto, Instawork | GTM & B2B Sales Talent Lead, Founders Office | Direct Email & LinkedIn |

---

## 🛡️ 2. STRUCTURED DATA FIELDS MAINTAINED DAILY

Every contact record in the database maintains:
1. **Contact ID**: Unique persistent identifier (`CNT-xxxxx`).
2. **Company Name & Location Hub**: Exact campus/office address in Bengaluru.
3. **Contact Name & Official Designation**: Decision-maker seniority and department.
4. **Verified Corporate Email**: Direct hiring lead inbox and departmental careers desk.
5. **Desk Phone / IVR Line**: Verified official Bengaluru desk contact.
6. **LinkedIn Profile Query**: Direct one-click lookup link for targeted InMail.
7. **Engagement State**: Monitored and updated automatically via daily maintenance daemons.

---

## 🔄 3. DAILY AUTOMATED MAINTENANCE ENGINE

The database is synchronized and maintained daily via:
- **Engine Script:** [`daily_contact_database_maintenance_engine.py`](file:///e:/anti/daily_contact_database_maintenance_engine.py)
- **Daily Maintenance Schedule:** Scheduled recurring cron job running daily at 06:00 AM IST.
- **Log Stream:** [`logs/daily_contact_maintenance.log`](file:///e:/anti/logs/daily_contact_maintenance.log)
