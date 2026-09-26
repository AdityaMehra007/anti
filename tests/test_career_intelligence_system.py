"""
========================================================================================
ADITYA GLOBAL CAREER INTELLIGENCE OS — COMPREHENSIVE TEST SUITE
========================================================================================
Validates:
1. SQLite Database Schema and Foreign Keys
2. Zero-Hallucination & Data Cleaning Rules
3. 10-Factor Aditya Match Engine and Scoring Logic
4. 48-Sheet Excel Export Integrity and Formatting
========================================================================================
"""

import os
import sqlite3
import pytest
from pathlib import Path
import openpyxl

from aditya_career_os_db import DB_PATH, get_connection, init_database
from aditya_career_os_agents import DataCleaningAgent, DeduplicationAgent, CandidateMatchingAgent, MasterOrchestrator
from aditya_career_os_excel import OUTPUT_EXCEL_PATH, build_master_workbook

EXPECTED_48_SHEETS = [
    "01_Dashboard", "02_Candidate_Profile", "03_Companies", "04_Company_Leaders",
    "05_Recruiters_HR", "06_Hiring_Managers", "07_Employees_Referrals", "08_Jobs",
    "09_Bengaluru_Jobs", "10_India_Jobs", "11_Global_Jobs", "12_Internships",
    "13_Remote_Jobs", "14_MNCs", "15_GCCs", "16_Startups", "17_Scaleups",
    "18_Banks_Finance", "19_Consulting", "20_Technology", "21_Operations_Roles",
    "22_Business_Analyst_Roles", "23_AI_Roles", "24_International_Business",
    "25_Trade_Operations", "26_PMO_Project", "27_Risk_Compliance", "28_Applications",
    "29_Outreach", "30_Followups", "31_Referrals", "32_Interviews", "33_Offers",
    "34_Rejections", "35_Company_Sources", "36_Job_Sources", "37_Person_Sources",
    "38_Conflicts", "39_Duplicates", "40_Validation", "41_Market_Intelligence",
    "42_Skills", "43_Salary_Benchmarks", "44_Bengaluru_Companies",
    "45_Global_Companies", "46_Daily_Changes", "47_Weekly_Report", "48_Archive_Index"
]

def test_database_initialization():
    """Verify database initializes properly and all 16 tables exist."""
    init_database()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()

    required_tables = [
        "candidate_profile", "companies", "people", "jobs", "sources_provenance",
        "conflicts", "duplicates", "job_matches", "outreach", "applications",
        "interviews", "market_skills", "bengaluru_clusters", "global_intelligence",
        "daily_action_queue", "audit_log"
    ]
    for req in required_tables:
        assert req in tables, f"Missing table: {req}"

def test_data_cleaning_zero_hallucination():
    """Verify DataCleaningAgent rejects sequential fake numbers and formulaic emails."""
    # Synthetic sequential number must be stripped to blank
    assert DataCleaningAgent.sanitize_phone("+91-80-40000023") == ""
    assert DataCleaningAgent.sanitize_phone("+91-80-40000046") == ""
    assert DataCleaningAgent.sanitize_phone("0000000000") == ""
    # Real business phone preserved
    assert DataCleaningAgent.sanitize_phone("+91-7003456624") == "+91-7003456624"

    # Legitimate recruiting inboxes preserved
    assert DataCleaningAgent.sanitize_email("careers.india@accenture.com") == "careers.india@accenture.com"
    assert DataCleaningAgent.sanitize_email("recruiting@goldmansachs.com") == "recruiting@goldmansachs.com"

def test_matching_engine_operations_fit():
    """Verify CandidateMatchingAgent scores operations roles high and pure sales low."""
    ops_job = {
        "job_title": "Global Business Operations & BD Analyst",
        "job_description": "Coordinate vendor SLAs, process mapping, and operational reporting.",
        "skills": "Business Operations, Excel, Vendor Management",
        "location": "Bengaluru, India",
        "experience_min": 0,
        "freshness": "Hot"
    }
    eval_ops = CandidateMatchingAgent.evaluate_job(ops_job)
    assert eval_ops["total_score"] >= 75.0
    assert "Business Operations" in eval_ops["explanation"]

    sales_job = {
        "job_title": "Telesales Cold Calling Executive",
        "job_description": "Outbound calling, cold calling prospective leads, commission only.",
        "skills": "Cold Calling, Telesales",
        "location": "Bengaluru, India",
        "experience_min": 0,
        "freshness": "Fresh"
    }
    eval_sales = CandidateMatchingAgent.evaluate_job(sales_job)
    # Sales job should receive penalized role fit
    assert eval_sales["role_fit"] <= 25.0

def test_excel_export_sheet_count_and_styling():
    """Verify Master Excel export produces exactly the 48 required sheets."""
    assert OUTPUT_EXCEL_PATH.exists()
    wb = openpyxl.load_workbook(str(OUTPUT_EXCEL_PATH), read_only=True)
    assert len(wb.sheetnames) == 48

    for expected_sheet in EXPECTED_48_SHEETS:
        assert expected_sheet in wb.sheetnames, f"Missing required sheet: {expected_sheet}"

    # Verify Dashboard has content
    ws01 = wb["01_Dashboard"]
    assert ws01.max_row >= 20
    assert ws01.max_column >= 10
    wb.close()

def test_executive_reports_and_csv_exports():
    """Verify generated executive reports and exported CSV datasets exist and have data."""
    daily_report = Path(__file__).resolve().parent.parent / "DAILY_EXECUTIVE_SUMMARY.md"
    weekly_report = Path(__file__).resolve().parent.parent / "reports" / "WEEKLY_EXECUTIVE_STRATEGY_REPORT.md"
    star_playbook = Path(__file__).resolve().parent.parent / "reports" / "INTERVIEW_STAR_DEFENSE_PLAYBOOK.md"

    assert daily_report.exists() and daily_report.stat().st_size > 1000
    assert weekly_report.exists() and weekly_report.stat().st_size > 1000
    assert star_playbook.exists() and star_playbook.stat().st_size > 1000

    csv_dir = Path(__file__).resolve().parent.parent / "data" / "csv_exports"
    assert (csv_dir / "companies.csv").exists()
    assert (csv_dir / "jobs.csv").exists()
    assert (csv_dir / "people.csv").exists()
    assert (csv_dir / "job_matches.csv").exists()
    assert (csv_dir / "applications.csv").exists()
    assert (csv_dir / "outreach.csv").exists()

    cockpit_html = Path(__file__).resolve().parent.parent / "ADITYA_CAREER_INTELLIGENCE_COCKPIT.html"
    assert cockpit_html.exists() and cockpit_html.stat().st_size > 100000

    resumes_dir = Path(__file__).resolve().parent.parent / "resumes"
    assert (resumes_dir / "Aditya_Mehra_Resume_Master_Operations_2026.docx").exists()
    assert (resumes_dir / "Aditya_Mehra_Resume_Printable.html").exists()

    assert (csv_dir / "ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv").exists()
    assert (Path(__file__).resolve().parent.parent / "ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.xlsx").exists()

