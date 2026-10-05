# ⚡ OMEGA: Autonomous Career & Operations Intelligence Engine

> **Proof of Work & Autonomous Engineering Platform**  
> Built & Maintained by **Aditya Mehra** | Bengaluru, Karnataka, India  
> **GitHub:** [@AdityaMehra007](https://github.com/AdityaMehra007) | **Contact:** [+91 7003456624](tel:+917003456624) | [adityamehra007@gmail.com](mailto:adityamehra007@gmail.com)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/Tests-16%2F16%20Passed-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-Autonomous%20AI-blueviolet.svg)](https://github.com/AdityaMehra007/anti)

---

## 📌 Executive Summary & Proof of Work

This repository serves as the **verifiable Proof of Work (PoW) and live autonomous operational platform** developed by **Aditya Mehra**, a BBA graduate from **Dayananda Sagar University (DSU), Bengaluru**.

It showcases real, hands-on capabilities across:
1. **AI-Assisted Development ("Vibe Coding"):** Prototyping full-stack web applications, REST APIs, and automated tools using modern AI coding systems (**Google Antigravity**, Cursor, Claude, LLMs).
2. **Operations Automation:** Autonomous recruiter communication parsers, compensation filters (₹3.0 LPA floor), and calendar event dispatchers (`.ics` generation).
3. **Database & Data Management:** Structured SQLite schemas tracking company outreach, application events, and recruiter interactions.
4. **Hermetic Software Testing:** 100% test-driven Python test suite with green pytest execution.

---

## 👤 About the Author: Aditya Mehra

* **Education:** Bachelor of Business Administration (BBA) — International Business (2023–2026), Dayananda Sagar University (DSU), Bengaluru. *(Degree Completed / Fresher — Immediate Joining)*.
* **Core Career Interests:** Business Operations, Operations Support, Management Trainee, Process Coordination.
* **Practical Experience Highlights:**
  * **Event Operations & Brand Activations (Bengaluru | 2021–2026):** Aero India stall management & customer sampling for artisan chocolate brand *Salt in My Cocoa*, live concert coordination (TRILOGY Concert).
  * **Corporate Internships (Bengaluru):** Operations & Quality Intern at **Instawork** (2025) and Commercial Operations Intern at **Pencil Mark Interior Solutions** (2025).
  * **Community Outreach (Bengaluru | 2024):** Operations Intern at NGO / Non-Profit Social Initiative.
  * **Family Business Operations (Kolkata | 2018–2020):** Daily order dispatching, billing documentation, and Excel inventory records.
* **Resume Documents:**
  * Clean Markdown Resume: [`resume_adi.md`](resume_adi.md)
  * ATS Printable HTML Resume: [`resumes/Aditya_Mehra_Resume_Printable.html`](resumes/Aditya_Mehra_Resume_Printable.html)
  * Word Resume Package: [`resumes/`](resumes/)

---

## ⚡ Core Operational Modules in this Repository

### 1. Autonomous Inbound Recruiter & Calendar Dispatcher
* **File:** [`omega/orchestration/recruiter_dispatcher.py`](omega/orchestration/recruiter_dispatcher.py)
* **What it does:** Automatically parses inbound recruiter emails, detects proposed CTC and interview slots, compares offers against a ₹3.0 LPA floor, generates polite counter-negotiation responses, and saves event records to SQLite.

### 2. RFC 5545 Calendar Generator
* **File:** [`omega/orchestration/calendar_dispatcher.py`](omega/orchestration/calendar_dispatcher.py)
* **What it does:** Generates RFC 5545-compliant `.ics` calendar invitation files explicitly calibrated for the `Asia/Kolkata` time zone, including automated conflict detection for double bookings.

### 3. Automated Resume Compilation Engine
* **File:** [`build_resumes.py`](build_resumes.py)
* **What it does:** Programmatically generates 5 tailored, ATS-compliant Microsoft Word (`.docx`) resumes and 1 clean printable HTML resume from structured data models.

### 4. Enterprise Outreach Database & Tracker
* **File:** [`data/outreach_tracker.db`](data/outreach_tracker.db)
* **What it does:** SQLite database indexing company records, job requisitions, contact details, fit scores, and verification proof hashes.

---

## 🧪 Automated Verification & Test Suite

All core components are hermetically verified using `pytest`:

```bash
# Run unit tests for pipeline, recruiter dispatcher, and interview cockpit
pytest tests/test_auto_apply_pipeline.py tests/test_recruiter_dispatcher.py tests/test_interview_cockpit.py -v
```

```text
============================= test session starts =============================
collected 16 items

tests/test_auto_apply_pipeline.py::test_auto_applied_database_records PASSED
tests/test_auto_apply_pipeline.py::test_download_bundle_zip_integrity PASSED
tests/test_auto_apply_pipeline.py::test_auto_apply_launcher_html_rendered PASSED
tests/test_recruiter_dispatcher.py::TestRecruiterDispatcherParsing::test_email_parsing_and_field_extraction PASSED
tests/test_recruiter_dispatcher.py::TestRecruiterDispatcherParsing::test_ctc_extraction_varieties PASSED
tests/test_recruiter_dispatcher.py::TestCompensationFilteringAndCounterNegotiation::test_below_salary_floor_counter_offer PASSED
tests/test_recruiter_dispatcher.py::TestCompensationFilteringAndCounterNegotiation::test_acceptable_compensation_acceptance PASSED
tests/test_recruiter_dispatcher.py::TestCompensationFilteringAndCounterNegotiation::test_unspecified_ctc_qualification PASSED
tests/test_recruiter_dispatcher.py::TestCalendarDispatcherRFC5545::test_rfc5545_ics_generation_and_kolkata_timezone PASSED
tests/test_recruiter_dispatcher.py::TestCalendarDispatcherRFC5545::test_calendar_slot_conflict_detection PASSED
tests/test_recruiter_dispatcher.py::TestDatabasePersistenceAndCockpitWebhook::test_database_persistence_in_sqlite PASSED
tests/test_recruiter_dispatcher.py::TestDatabasePersistenceAndCockpitWebhook::test_cockpit_webhook_event_emission PASSED
tests/test_interview_cockpit.py::test_interview_round_classification PASSED
tests/test_interview_cockpit.py::test_interview_prep_dossier_synthesis PASSED
tests/test_interview_cockpit.py::test_offer_negotiator_evaluation PASSED
tests/test_interview_cockpit.py::test_counter_offer_letter_generation PASSED

============================= 16 passed in 2.41s ==============================
```

---

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/AdityaMehra007/anti.git
cd anti

# 2. Install dependencies
pip install pytest python-docx

# 3. Rebuild all resume formats
python build_resumes.py

# 4. Run test verification
pytest tests/test_recruiter_dispatcher.py
```

---

## 📬 Contact & Direct Connect

* **Author:** Aditya Mehra
* **Location:** Bengaluru, Karnataka, India
* **Phone:** `+91 7003456624`
* **Email:** `adityamehra007@gmail.com`
* **LinkedIn:** [linkedin.com/in/aditya-mehra](https://linkedin.com/in/aditya-mehra)
* **GitHub Profile:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)
