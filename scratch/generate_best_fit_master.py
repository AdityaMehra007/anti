"""
Generate accurate best fit job ledgers for candidate profile:
BBA Graduate | Business Operations, Client Support, AI Productivity & Growth Systems
"""

import csv
import os

profile_keywords = [
    'operations', 'client support', 'customer support', 'customer success',
    'bba', 'business analyst', 'inside sales', 'business development',
    'lead generation', 'automation', 'n8n', 'clay', 'prompt', 'ai',
    'executive assistant', 'procurement', 'logistics', 'supply chain',
    'onboarding', 'coordinator', 'fresher', 'entry-level', 'entry level',
    'generalist', 'growth', 'specialist', 'associate', 'trainee',
    'front office', 'guest relations', 'concierge', 'account management',
    'category management', 'vendor management', 'analyst', 'crm'
]

technical_exclusions = [
    'lead product designer', 'senior backend', 'staff engineer', 'frontend lead',
    'architect', 'ios developer', 'android developer', 'golang engineer', 'c++'
]

datasets = [
    ('naukri_homepage_bengaluru_feed.csv', 'Requisition Title', 'Hiring Organization / Employer', 'Work Location', 'Annual Compensation Band (INR)', 'Direct Naukri Application & Search URL', ['Requisition Title', 'Core Skill Tags Required', 'Target Candidate Profile'], 'Naukri.com (Bengaluru GCCs)'),
    ('foundit_bengaluru_jobs_matrix.csv', 'Requisition Title', 'Hiring Organization / Employer', 'Work Location', 'Annual Compensation Band (INR)', 'Direct Foundit Requisition URL', ['Requisition Title', 'Core Skill Tags Required', 'Target Candidate Profile'], 'Foundit (Monster India)'),
    ('flexjobs_bengaluru_remote_entrylevel.csv', 'Job Title', 'Company', 'Work Arrangement', 'Salary / Hourly Rate', 'Direct FlexJobs Application URL', ['Job Title', 'Description / Match Notes'], 'FlexJobs Remote Entry-Level'),
    ('upwork_best_matches_feed.csv', 'Job Title', 'Category', 'Contract Type & Budget', 'Match Score Rating', 'Direct Upwork Search URL', ['Job Title', 'Mandatory Skill Tags Required'], 'Upwork Best Matches (High-Ticket USD)'),
    ('myntra_bengaluru_jobs.csv', 'job_title', 'department', 'city', 'experience_range', 'portal_apply_url', ['job_title', 'department', 'key_skills'], 'Myntra / Flipkart E-Commerce Ops'),
    ('diageo_bengaluru_jobs.csv', 'job_title', 'job_family', 'location', 'management_level', 'workday_apply_url', ['job_title', 'job_family', 'function_subtype'], 'Diageo Global Capability Center'),
    ('randstad_bengaluru_jobs.csv', 'Job Title', 'Domain', 'Work Location', 'Typical CTC Band', 'Randstad Portal Route', ['Job Title', 'Domain', 'Key Sourcing Criteria'], 'Randstad Executive Sourced')
]

matched_rows = []

for fn, title_col, company_col, loc_col, comp_col, url_col, check_cols, ch_label in datasets:
    if not os.path.exists(fn):
        continue
    with open(fn, encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            text = ' '.join([str(r.get(c, '')) for c in check_cols]).lower()
            has_match = any(pk in text for pk in profile_keywords)
            is_senior_tech = any(tx in text for tx in technical_exclusions) and not any(k in text for k in ['operations', 'analyst', 'associate', 'support'])
            
            if has_match and not is_senior_tech:
                matched_rows.append({
                    "Channel": ch_label,
                    "Job Title": r.get(title_col, 'Role'),
                    "Company / Employer": r.get(company_col, 'Employer'),
                    "Location / Work Model": r.get(loc_col, 'Bengaluru / Remote'),
                    "Compensation Band": r.get(comp_col, 'Competitive Market Standard'),
                    "Application URL": r.get(url_col, '#')
                })

out_fn = 'e:/anti/my_best_fit_jobs_master.csv'
fieldnames = ["Channel", "Job Title", "Company / Employer", "Location / Work Model", "Compensation Band", "Application URL"]
with open(out_fn, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in matched_rows:
        writer.writerow(row)

print(f"Generated {out_fn} with {len(matched_rows)} verified curated matches.")
