# Antigravity LinkedIn Connections Intelligence Data Dictionary

## Overview
This document defines the schema, field definitions, and architectural taxonomy of the processed LinkedIn Network dataset for **Aditya Mehra** (9,223 total records).

---

## Dataset Schema

| Field Name | Type | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier for the connection record | 1, 42, 9223 |
| `first_name` | String | Connection's given name | Syed Sumbul, Mariam |
| `last_name` | String | Connection's family name | Shahbaz, Mathew |
| `full_name` | String | Combined first and last name | Syed Sumbul Shahbaz |
| `company` | String | Current employer / organization name | Goldman Sachs, EY, Deloitte |
| `position` | String | Current professional title / role | Senior Executive HR, Business Consulting Intern |
| `department` | Category | Classified business domain / function | HR & Talent Acquisition, Finance & Banking |
| `seniority` | Category | Hierarchy level derived from title | C-Suite / Founder, Manager / Lead, Executive / VP / Director |
| `company_tier` | Category | Tier categorization of the employer | Tier 1 Consulting / Big 4, Tier 1 Tech MNC |
| `email` | String | Direct email address (if publicly shared) | name@company.com |
| `url` | URL | LinkedIn public profile URL | https://www.linkedin.com/in/... |
| `connected_on` | Date | Date connection was established | 24 Aug 2026, 15 Jun 2025 |
| `is_recruiter` | Binary (0/1) | Flag indicating HR, Recruiter, or Talent Acquisition | 1 (Yes), 0 (No) |
| `is_decision_maker` | Binary (0/1) | Flag indicating hiring manager / leadership seniority | 1 (Yes), 0 (No) |

---

## Dataset Statistics & Metrics

- **Total Network Records:** 9,223
- **Unique Organizations / Companies:** 5,226
- **Unique Position Titles:** 4,221
- **Direct Recruiter & HR Contacts:** 1,449 (15.7%)
- **C-Suite, Founders & Directors:** 736 (8.0%)
- **Managers & Team Leads:** 1,117 (12.1%)
- **Tier 1 Global MNC & Big 4 Connections:** 1,078 (11.7%)
- **Direct LinkedIn URLs:** 9,174 (99.5%)
