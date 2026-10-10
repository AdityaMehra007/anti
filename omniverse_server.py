"""
OMNIVERSE LOCAL REST API SERVER
FastAPI backend powering the Omniverse Executive Cockpit, ATS Resumes,
Live Vacancies, 4,500 Company Census, Merkle Dispatch Ledger, and Net Salary Calculator.

Directives: OMEGA CONSTITUTION & CONTEXT.md
"""

import os
import json
import sqlite3
import datetime
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

DB_PATH = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
COCKPIT_HTML_PATH = r"e:\anti\OMNIVERSE_INFINITY_COCKPIT.html"
DOCKETS_JSON_PATH = r"e:\anti\OMNIVERSE_APPLICATION_DOCKETS.json"
RESUMES_DIR = r"e:\anti\resumes"
OUTBOX_DIR = r"e:\anti\outbox"
DELIVERABLES_DIR = r"e:\anti\omniverse_deliverables"
CALENDAR_JSON_PATH = r"e:\anti\OMNIVERSE_12_MONTH_HIRING_CALENDAR.json"
PORTFOLIO_JSON_PATH = r"e:\anti\OMNIVERSE_SKILLS_PORTFOLIO.json"
ALUMNI_JSON_PATH = r"e:\anti\dsu_alumni_network_matrix.json"

app = FastAPI(
    title="Omniverse Infinity API Server",
    description="Career Intelligence & Execution Operating System for Aditya Mehra",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the executive cockpit dashboard."""
    if os.path.exists(COCKPIT_HTML_PATH):
        with open(COCKPIT_HTML_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Omniverse API Server is Running</h1><p><a href='/docs'>Swagger API Docs</a></p>")


@app.get("/cockpit", response_class=HTMLResponse)
def read_cockpit():
    """Serves the interactive 7-tab cockpit dashboard."""
    if os.path.exists(COCKPIT_HTML_PATH):
        with open(COCKPIT_HTML_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    raise HTTPException(status_code=404, detail="Cockpit file not found.")


@app.get("/api/status")
def get_system_status():
    """Returns database and ecosystem health status."""
    if not os.path.exists(DB_PATH):
        return {"status": "ERROR", "message": "Database not found"}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    table_counts = {}
    for tbl in [
        "omniverse_companies", "omniverse_live_vacancies", "omniverse_recruiters",
        "omniverse_corporate_relationships", "omniverse_mail_outbox", "omniverse_dispatch_ledger",
        "omniverse_audit_log"
    ]:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
            table_counts[tbl] = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            table_counts[tbl] = 0
    conn.close()
    
    return {
        "status": "HEALTHY",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": DB_PATH,
        "table_counts": table_counts
    }


@app.get("/api/summary")
def get_summary_metrics():
    """Returns top-level KPIs for executive cards."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM omniverse_companies")
    total_companies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM omniverse_live_vacancies WHERE non_sales_verified = 1")
    total_vacancies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM omniverse_recruiters")
    total_recruiters = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM omniverse_corporate_relationships")
    total_corps = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_companies": total_companies,
        "live_non_sales_vacancies": total_vacancies,
        "verified_recruiters": total_recruiters,
        "corporate_parent_subsidiaries": total_corps,
        "network_connections": 9223,
        "dsu_alumni_companies": 5171,
        "candidate": "Aditya Mehra",
        "target_graduation": "DSU BBA-IB '26"
    }


@app.get("/api/vacancies")
def get_vacancies(
    search: Optional[str] = None,
    department: Optional[str] = None,
    min_score: int = Query(default=80, ge=0, le=100)
):
    """Retrieves verified non-sales live vacancies with optional filters."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT job_id, company_name, job_title, department, blr_location, 
           work_model, experience_req, fresher_fit, bba_ib_suitability_score, 
           est_ctc_lpa, apply_url, ats_type, freshness_tag
    FROM omniverse_live_vacancies
    WHERE non_sales_verified = 1 AND bba_ib_suitability_score >= ?
    """
    params = [min_score]
    
    if search:
        query += " AND (company_name LIKE ? OR job_title LIKE ? OR blr_location LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
        
    if department:
        query += " AND department LIKE ?"
        params.append(f"%{department}%")
        
    query += " ORDER BY bba_ib_suitability_score DESC"
    
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"total": len(rows), "vacancies": rows}


@app.get("/api/companies")
def get_companies(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: Optional[str] = None,
    corridor: Optional[str] = None,
    industry: Optional[str] = None
):
    """Paginated search across 4,500 verified Bengaluru employers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    where_clauses = ["1=1"]
    params = []
    
    if search:
        where_clauses.append("(canonical_name LIKE ? OR legal_name LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])
        
    if corridor:
        where_clauses.append("blr_corridor LIKE ?")
        params.append(f"%{corridor}%")
        
    if industry:
        where_clauses.append("industry_sector LIKE ?")
        params.append(f"%{industry}%")
        
    where_sql = " AND ".join(where_clauses)
    
    cursor.execute(f"SELECT COUNT(*) FROM omniverse_companies WHERE {where_sql}", params)
    total_count = cursor.fetchone()[0]
    
    offset = (page - 1) * page_size
    query = f"""
    SELECT company_id, canonical_name, legal_name, parent_name, industry_sector,
           company_tier, blr_corridor, tech_park, careers_url, ats_platform,
           target_role_archetype, bba_fit_score, sales_risk, verified_status
    FROM omniverse_companies
    WHERE {where_sql}
    ORDER BY bba_fit_score DESC, canonical_name ASC
    LIMIT ? OFFSET ?
    """
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_count,
        "total_pages": (total_count + page_size - 1) // page_size,
        "companies": rows
    }


@app.get("/api/corporate-tree")
def get_corporate_tree():
    """Returns mapped relationships between global parents and Bangalore GCCs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT rel_id, global_parent, hq_country, blr_entity, tier, corridor,
           strategic_mandate, non_sales_scope, career_portal, proof_source
    FROM omniverse_corporate_relationships
    ORDER BY global_parent ASC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"total": len(rows), "relationships": rows}


@app.get("/api/dockets")
def get_all_dockets():
    """Returns all 14 application dockets."""
    if os.path.exists(DOCKETS_JSON_PATH):
        with open(DOCKETS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {"total": len(data), "dockets": data}
    raise HTTPException(status_code=404, detail="Dockets JSON not found.")


@app.get("/api/dockets/{job_id}")
def get_single_docket(job_id: str):
    """Returns tailored docket for specific vacancy."""
    if os.path.exists(DOCKETS_JSON_PATH):
        with open(DOCKETS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                if d["job_id"] == job_id:
                    return d
    raise HTTPException(status_code=404, detail=f"Docket {job_id} not found.")


@app.get("/api/outbox")
def get_outbox():
    """Returns all queued / dispatched RFC 5322 MIME messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT outbox_id, job_id, company_name, role_title, to_email, subject,
               eml_filepath, sha256_hash, spf_status, dkim_status, delivery_status, dispatched_at
        FROM omniverse_mail_outbox
        ORDER BY dispatched_at DESC
        """)
        rows = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    return {"total": len(rows), "outbox": rows}


@app.get("/api/salary")
def calculate_salary(ctc_lpa: float = Query(default=8.5, ge=1.0, le=100.0)):
    """Computes net monthly in-hand salary and tax breakdown for Bengaluru."""
    annual_ctc = ctc_lpa * 100000.0
    basic_annual = annual_ctc * 0.40
    epf_employee = min(basic_annual * 0.12, 1800.0 * 12)
    professional_tax = 200.0 * 12
    standard_deduction = 75000.0
    
    taxable_income = max(0.0, annual_ctc - standard_deduction)
    
    # New Tax Regime FY 2025-26 slabs
    income_tax = 0.0
    if taxable_income > 1500000:
        income_tax += (taxable_income - 1500000) * 0.30
        taxable_income = 1500000
    if taxable_income > 1200000:
        income_tax += (taxable_income - 1200000) * 0.20
        taxable_income = 1200000
    if taxable_income > 900000:
        income_tax += (taxable_income - 900000) * 0.15
        taxable_income = 900000
    if taxable_income > 600000:
        income_tax += (taxable_income - 600000) * 0.10
        taxable_income = 600000
    if taxable_income > 300000:
        income_tax += (taxable_income - 300000) * 0.05
        
    # Section 87A Rebate if taxable <= 7L
    if annual_ctc - standard_deduction <= 700000:
        income_tax = 0.0
    else:
        income_tax *= 1.04 # 4% health & education cess
        
    net_annual = annual_ctc - epf_employee - professional_tax - income_tax
    net_monthly = net_annual / 12.0
    
    return {
        "ctc_lpa": ctc_lpa,
        "annual_gross": round(annual_ctc, 2),
        "monthly_gross": round(annual_ctc / 12.0, 2),
        "epf_employee_annual": round(epf_employee, 2),
        "professional_tax_annual": round(professional_tax, 2),
        "income_tax_annual": round(income_tax, 2),
        "net_annual_take_home": round(net_annual, 2),
        "net_monthly_in_hand": round(net_monthly, 2)
    }


@app.get("/api/resumes")
def list_resumes():
    """Lists the 4 tailored ATS resume variants."""
    manifest_path = os.path.join(RESUMES_DIR, "RESUME_MANIFEST.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return {"resumes": json.load(f)}
    return {"resumes": []}


@app.get("/api/resumes/{track_id}", response_class=HTMLResponse)
def get_resume_html(track_id: str):
    """Serves the rendered HTML resume for the requested track."""
    filename = f"RESUME_ADITYA_MEHRA_{track_id.upper()}.html"
    filepath = os.path.join(RESUMES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    raise HTTPException(status_code=404, detail=f"Resume {filename} not found.")


@app.get("/api/audit-log")
def get_audit_log():
    """Returns automated quality audit records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT audit_id, category, finding, status, recommendation, logged_at
    FROM omniverse_audit_log
    ORDER BY audit_id DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"total": len(rows), "audit_entries": rows}


@app.get("/api/deliverables")
def get_deliverables_manifest():
    """Lists all 35 Section 43 database & intelligence deliverables."""
    manifest_path = os.path.join(DELIVERABLES_DIR, "MASTER_SECTION_43_DELIVERABLES_MANIFEST.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Deliverables manifest not found.")


@app.get("/api/deliverables/{item_id}")
def get_deliverable_item(item_id: str, format: str = "json"):
    """Serves a specific deliverable file (json, csv, or md)."""
    clean_id = item_id.replace(".csv", "").replace(".json", "").replace(".md", "")
    target_ext = format.lower().strip(".")
    if target_ext not in ["json", "csv", "md"]:
        target_ext = "json"
        
    filename = f"{clean_id}.{target_ext}"
    filepath = os.path.join(DELIVERABLES_DIR, filename)
    if not os.path.exists(filepath):
        for alt_ext in ["json", "csv", "md"]:
            alt_path = os.path.join(DELIVERABLES_DIR, f"{clean_id}.{alt_ext}")
            if os.path.exists(alt_path):
                filepath = alt_path
                target_ext = alt_ext
                break
                
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Deliverable {item_id} not found.")

    if target_ext == "json":
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    elif target_ext in ["csv", "md"]:
        return FileResponse(filepath, media_type="text/plain" if target_ext == "md" else "text/csv")


@app.get("/api/hiring-calendar")
def get_hiring_calendar():
    """Returns the rolling 12-month non-sales hiring calendar (Oct 2026 - Sep 2027)."""
    if os.path.exists(CALENDAR_JSON_PATH):
        with open(CALENDAR_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {"total_windows": len(data), "calendar": data}
    raise HTTPException(status_code=404, detail="Hiring calendar JSON not found.")


@app.get("/api/skills-portfolio")
def get_skills_portfolio():
    """Returns candidate 8-domain competency matrix and 5 verified portfolio projects."""
    if os.path.exists(PORTFOLIO_JSON_PATH):
        with open(PORTFOLIO_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Skills portfolio JSON not found.")


@app.get("/api/interview-drills")
def get_interview_drills():
    """Returns 10 verified STAR interview defense packs and role scenarios."""
    from omniverse_interview_defense import INTERVIEW_PACKS
    return {"total_packs": len(INTERVIEW_PACKS), "packs": INTERVIEW_PACKS}


@app.get("/api/referrals")
def get_referral_summary():
    """Returns warm alumni and connection clusters across 5,171 companies."""
    if os.path.exists(ALUMNI_JSON_PATH):
        with open(ALUMNI_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "total_nodes_indexed": data.get("total_nodes_indexed", 9223),
                "total_companies_represented": data.get("total_companies_represented", 5171),
                "top_clusters": data.get("top_25_enterprise_clusters", [])
            }
    raise HTTPException(status_code=404, detail="Alumni network JSON not found.")


if __name__ == "__main__":
    uvicorn.run("omniverse_server.py:app", host="127.0.0.1", port=8000, reload=False)
