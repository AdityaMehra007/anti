"""
MEGA UNIFIED JOB REQUISITIONS & JD OMNI-DATABASE BUILDER
Consolidates all crawled job boards into a single master database:
e:/anti/ALL_BENGALURU_AND_GLOBAL_JOBS_MASTER_DATABASE.csv

Schema:
- Universal Requisition ID (JOB-BLR-XXXX / ATS ID)
- Requisition Title / Role
- Employer / Organization Name
- Portal / Source Platform
- Industry Sector / Practice Area
- Work Location & Bangalore Tech Corridor
- Work Model (In-Office / Hybrid / Remote)
- Experience Level / Target Batch
- Compensation Band (INR / USD)
- Key Skills & Tech Stack Required
- Job Description Summary & Core Deliverables
- Direct Application URL
"""

import csv
import os
import glob
import re

job_files_config = [
    {
        "file": "naukri_homepage_bengaluru_feed.csv",
        "portal": "Naukri.com (Bengaluru GCC Feed)",
        "sector": "GCCs & Tech Parks",
        "title_col": "Requisition Title",
        "company_col": "Hiring Organization / Employer",
        "loc_col": "Work Location",
        "exp_col": "Target Candidate Profile",
        "comp_col": "Annual Compensation Band (INR)",
        "skills_col": "Core Skill Tags Required",
        "jd_col": "Corporate Pillar",
        "url_col": "Direct Naukri Application & Search URL",
        "id_col": None
    },
    {
        "file": "foundit_bengaluru_jobs_matrix.csv",
        "portal": "Foundit (Monster India)",
        "sector": "Enterprise Shared Services",
        "title_col": "Requisition Title",
        "company_col": "Hiring Organization / Employer",
        "loc_col": "Work Location",
        "exp_col": "Target Candidate Profile",
        "comp_col": "Annual Compensation Band (INR)",
        "skills_col": "Core Skill Tags Required",
        "jd_col": "Foundit Industry / Function Track",
        "url_col": "Direct Foundit Requisition URL",
        "id_col": None
    },
    {
        "file": "instahyre_cutshort_hirist_jobs.csv",
        "portal_col": "Platform",
        "sector": "Startups, Product & FinTech",
        "title_col": "Requisition Title",
        "company_col": "Company / Startup",
        "loc_col": "Work Location",
        "exp_col": "Experience Level",
        "comp_col": "Compensation Band",
        "skills_col": "Core Skills Required",
        "jd_col": "Domain / Track",
        "url_col": "Direct Portal Route URL",
        "id_col": None
    },
    {
        "file": "weworkremotely_support_jobs.csv",
        "portal": "WeWorkRemotely",
        "sector": "Global Remote SaaS",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Work Model",
        "exp_col": None,
        "comp_col": None,
        "skills_col": "Category",
        "jd_col": "Category",
        "url_col": "Direct Application URL",
        "id_col": None
    },
    {
        "file": "upwork_best_matches_feed.csv",
        "portal": "Upwork USD Contracts",
        "sector": "AI Automation & Outbound Growth",
        "title_col": "Job Title",
        "company_col": "Client Quality Tier",
        "loc_col": None,
        "exp_col": "Match Score Rating",
        "comp_col": "Contract Type & Budget",
        "skills_col": "Mandatory Skill Tags Required",
        "jd_col": "Client Problem / Bottleneck",
        "url_col": "Direct Upwork Search URL",
        "id_col": None
    },
    {
        "file": "upwork_bengaluru_contracts.csv",
        "portal": "Upwork Bengaluru Hub",
        "sector": "Consulting & Research Contracts",
        "title_col": "Project Title",
        "company_col": "Client Origin",
        "loc_col": "Target Location",
        "exp_col": "Contract Type",
        "comp_col": "Budget / Rate",
        "skills_col": "Category",
        "jd_col": "Scope & Deliverables",
        "url_col": "Upwork Job URL",
        "id_col": None
    },
    {
        "file": "jobspresso_remote_jobs.csv",
        "portal": "Jobspresso Curated Remote",
        "sector": "Global Tech & Operations",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Location",
        "exp_col": None,
        "comp_col": None,
        "skills_col": "Category",
        "jd_col": "Category",
        "url_col": "Application Link / ATS URL",
        "id_col": None
    },
    {
        "file": "jobspresso_master_all_remote_jobs.csv",
        "portal": "Jobspresso Master ATS Crawl",
        "sector": "Global Remote Operations",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Location",
        "exp_col": None,
        "comp_col": None,
        "skills_col": "Category",
        "jd_col": "Category",
        "url_col": "Apply / ATS URL",
        "id_col": None
    },
    {
        "file": "flexjobs_bengaluru_remote_entrylevel.csv",
        "portal": "FlexJobs Remote Entry-Level",
        "sector": "Global Corporate Operations",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Work Arrangement",
        "exp_col": "Eligibility",
        "comp_col": "Salary / Hourly Rate",
        "skills_col": "Benefits Included",
        "jd_col": "Description / Match Notes",
        "url_col": "Direct FlexJobs Application URL",
        "id_col": None
    },
    {
        "file": "remoteok_bengaluru_global_jobs.csv",
        "portal": "RemoteOK Worldwide",
        "sector": "International Tech Startups",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Eligible Location",
        "exp_col": "Geographic Scope",
        "comp_col": "Compensation",
        "skills_col": "Tags / Skills",
        "jd_col": "Tags / Skills",
        "url_col": "Apply URL",
        "id_col": None
    },
    {
        "file": "dice_bengaluru_jobs.csv",
        "portal": "Dice Enterprise",
        "sector": "IT & CRM Operations",
        "title_col": "Job Title",
        "company_col": "Sourcing Portal",
        "loc_col": "Location",
        "exp_col": None,
        "comp_col": None,
        "skills_col": "Specialization",
        "jd_col": "Specialization",
        "url_col": "Direct Apply URL",
        "id_col": "Job ID"
    },
    {
        "file": "yc_workatastartup_bengaluru_jobs.csv",
        "portal": "Y Combinator Work at a Startup",
        "sector": "YC Venture Startups",
        "title_col": "Job Title",
        "company_col": "Company",
        "loc_col": "Location / Work Model",
        "exp_col": "Experience Level",
        "comp_col": "Compensation (INR / Equity)",
        "skills_col": "Job Family",
        "jd_col": "YC Batch",
        "url_col": "Direct YC Apply URL",
        "id_col": None
    },
    {
        "file": "wellfound_bengaluru_jobs.csv",
        "portal": "Wellfound (AngelList)",
        "sector": "Funded Tech Startups",
        "title_col": "title",
        "company_col": "startup_name",
        "loc_col": "locations",
        "exp_col": "experience_min",
        "comp_col": "compensation",
        "skills_col": "primary_role",
        "jd_col": "primary_role",
        "url_col": "job_url",
        "id_col": "id"
    },
    {
        "file": "linkedin_bengaluru_jobs.csv",
        "portal": "LinkedIn Jobs India",
        "sector": "Tier-1 Tech Parks & GCCs",
        "title_col": "Job Title",
        "company_col": "Company Name",
        "loc_col": "Location",
        "exp_col": None,
        "comp_col": "Salary Band",
        "skills_col": "Domain / Category",
        "jd_col": "Domain / Category",
        "url_col": "Direct Apply Link",
        "id_col": "Job ID"
    },
    {
        "file": "bengaluru_hospitality_jobs.csv",
        "portal": "IHCL / Luxury Hospitality",
        "sector": "Luxury Hospitality & Lifestyle",
        "title_col": "title",
        "company_col": "brand_division",
        "loc_col": "city",
        "exp_col": None,
        "comp_col": None,
        "skills_col": "conglomerate",
        "jd_col": "conglomerate",
        "url_col": "url",
        "id_col": "req_id"
    },
    {
        "file": "the_hoxton_bengaluru_preopening_jobs.csv",
        "portal": "The Hoxton Pre-Opening Hub",
        "sector": "Luxury Lifestyle Hospitality",
        "title_col": "Job Title",
        "company_col": "Department",
        "loc_col": "Location",
        "exp_col": "Experience Level",
        "comp_col": "CTC Band (INR)",
        "skills_col": "Key Skills",
        "jd_col": "Department",
        "url_col": "Direct Apply URL",
        "id_col": "Req ID"
    },
    {
        "file": "diageo_bengaluru_jobs.csv",
        "portal": "Diageo Global Capability Center",
        "sector": "Global Business Services",
        "title_col": "job_title",
        "company_col": "job_family",
        "loc_col": "location",
        "exp_col": "management_level",
        "comp_col": None,
        "skills_col": "function_subtype",
        "jd_col": "job_family_group",
        "url_col": "workday_apply_url",
        "id_col": "reference_id"
    },
    {
        "file": "myntra_bengaluru_jobs.csv",
        "portal": "Myntra / Flipkart E-Commerce",
        "sector": "E-Commerce Supply Chain",
        "title_col": "job_title",
        "company_col": "department",
        "loc_col": "city",
        "exp_col": "experience_range",
        "comp_col": None,
        "skills_col": "key_skills",
        "jd_col": "employment_type",
        "url_col": "portal_apply_url",
        "id_col": "display_id"
    },
    {
        "file": "randstad_bengaluru_jobs.csv",
        "portal": "Randstad Executive Sourced",
        "sector": "Corporate Staffing",
        "title_col": "Job Title",
        "company_col": "Domain",
        "loc_col": "Work Location",
        "exp_col": "Experience Level",
        "comp_col": "Typical CTC Band",
        "skills_col": "Key Sourcing Criteria",
        "jd_col": "Domain",
        "url_col": "Randstad Portal Route",
        "id_col": "Job ID"
    },
    {
        "file": "michaelpage_bangalore_jobs.csv",
        "portal": "Michael Page India",
        "sector": "Executive Search & Ops",
        "title_col": "title",
        "company_col": None,
        "loc_col": "work_mode",
        "exp_col": None,
        "comp_col": "salary",
        "skills_col": None,
        "jd_col": "title",
        "url_col": "url",
        "id_col": "ref_code"
    },
    {
        "file": "abc_consultants_leadership_practice.csv",
        "portal": "ABC Consultants",
        "sector": "Leadership & Executive Search",
        "title_col": "role",
        "company_col": "name",
        "loc_col": None,
        "exp_col": None,
        "comp_col": None,
        "skills_col": "practice_area",
        "jd_col": "practice_area",
        "url_col": "profile_url",
        "id_col": None
    },
    {
        "file": "indeed_scrumconnect_bengaluru_jobs.csv",
        "portal": "Indeed / Scrumconnect",
        "sector": "Technology Consulting",
        "title_col": "job_title",
        "company_col": "client",
        "loc_col": "location",
        "exp_col": "experience",
        "comp_col": "salary",
        "skills_col": "key_skills",
        "jd_col": "key_skills",
        "url_col": "apply_url",
        "id_col": None
    }
]

master_records = []
counter = 1

for cfg in job_files_config:
    fn = cfg["file"]
    if not os.path.exists(fn):
        continue
    with open(fn, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for r in reader:
            title = r.get(cfg["title_col"], "").strip() if cfg["title_col"] else ""
            if not title:
                continue
            
            # Company
            if cfg.get("company_col"):
                company = r.get(cfg["company_col"], "").strip()
            else:
                company = "Corporate Employer"
            
            # Portal
            if cfg.get("portal_col"):
                portal = r.get(cfg["portal_col"], "").strip()
            else:
                portal = cfg.get("portal", "Job Portal")

            # Location
            if cfg.get("loc_col"):
                location = r.get(cfg["loc_col"], "").strip() or "Bengaluru / Global Remote"
            else:
                location = "Bengaluru / Global Remote"

            # Exp
            if cfg.get("exp_col"):
                exp = r.get(cfg["exp_col"], "").strip() or "Fresher / 0-2 Years"
            else:
                exp = "Fresher / 0-2 Years"

            # Comp
            if cfg.get("comp_col"):
                comp = r.get(cfg["comp_col"], "").strip() or "Competitive Market Standard"
            else:
                comp = "Competitive Market Standard"

            # Skills
            if cfg.get("skills_col"):
                skills = r.get(cfg["skills_col"], "").strip() or "Operations, Customer Support, Excel, AI Productivity"
            else:
                skills = "Operations, Customer Support, Excel, AI Productivity"

            # JD / Deliverables
            if cfg.get("jd_col"):
                jd = r.get(cfg["jd_col"], "").strip() or f"Execution of core responsibilities for {title}."
            else:
                jd = f"Execution of core responsibilities for {title}."

            # URL
            if cfg.get("url_col"):
                url = r.get(cfg["url_col"], "").strip() or "#"
            else:
                url = "#"

            # Job ID
            raw_id = r.get(cfg["id_col"], "").strip() if cfg.get("id_col") else ""
            if raw_id:
                job_id = raw_id
            else:
                job_id = f"JOB-BLR-{counter:05d}"

            master_records.append({
                "Universal Job ID": job_id,
                "Job Title / Role": title,
                "Company / Employer": company,
                "Portal Source Platform": portal,
                "Industry Sector": cfg["sector"],
                "Work Location": location,
                "Experience / Batch": exp,
                "Compensation Band": comp,
                "Key Skills Required": skills,
                "Job Description Summary & Deliverables": jd,
                "Direct Application URL": url
            })
            counter += 1

out_master_path = "e:/anti/ALL_BENGALURU_AND_GLOBAL_JOBS_MASTER_DATABASE.csv"
fieldnames = [
    "Universal Job ID",
    "Job Title / Role",
    "Company / Employer",
    "Portal Source Platform",
    "Industry Sector",
    "Work Location",
    "Experience / Batch",
    "Compensation Band",
    "Key Skills Required",
    "Job Description Summary & Deliverables",
    "Direct Application URL"
]

with open(out_master_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in master_records:
        writer.writerow(row)

print(f"SUCCESS: Generated {out_master_path} with {len(master_records)} comprehensive records.")
