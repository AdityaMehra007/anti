import os, sys, glob, csv, json, re, time, subprocess
from datetime import datetime
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE = r'e:\anti'
os.environ['PYTHONIOENCODING'] = 'utf-8'


# 1. READ RAW LINKEDIN EXPORT
raw_path = os.path.join(WORKSPACE, 'linkedin_export', 'Connections.csv')
if not os.path.exists(raw_path):
    raw_path = r'C:\Users\amehr\Downloads\New folder\Complete_LinkedInDataExport_08-25-2026.zip\Connections.csv'

raw_rows = []
with open(raw_path, 'r', encoding='utf-8-sig', errors='replace') as fp:
    for line in fp:
        if line.startswith('First Name'):
            header = line.strip().split(',')
            break
    reader = csv.DictReader(fp, fieldnames=header)
    for r in reader:
        raw_rows.append(r)

print(f'Ingested {len(raw_rows)} raw LinkedIn connection rows.')

# 2. VALIDATE & NORMALIZE
seen_urls = set()
dup_urls = 0
missing_names = 0
missing_companies = 0
missing_positions = 0
malformed_urls = 0
malformed_emails = 0

normalized_records = []
email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

for idx, r in enumerate(raw_rows):
    first = r.get('First Name', '').strip()
    last = r.get('Last Name', '').strip()
    full_name = f'{first} {last}'.strip()
    company = r.get('Company', '').strip()
    position = r.get('Position', '').strip()
    url = r.get('URL', '').strip()
    email = r.get('Email Address', '').strip()
    connected_on = r.get('Connected On', '').strip()
    
    if not full_name: missing_names += 1
    if not company: missing_companies += 1
    if not position: missing_positions += 1
    
    if url:
        if url in seen_urls: dup_urls += 1
        seen_urls.add(url)
        if not url.startswith('http'): malformed_urls += 1
            
    if email and not email_regex.match(email): malformed_emails += 1
        
    norm_co = re.sub(r'\s+', ' ', company.strip())
    pos_lower = position.lower()
    
    seniority = 'Individual Contributor'
    founder_flag = 0
    c_suite_flag = 0
    recruiter_flag = 0
    hiring_mgr_flag = 0
    
    if any(w in pos_lower for w in ['founder', 'co-founder', 'founding partner']):
        seniority = 'Founder'
        founder_flag = 1
    elif any(w in pos_lower for w in ['ceo', 'cto', 'cfo', 'coo', 'cmo', 'cxo', 'chief', 'managing director', 'president', 'partner']):
        seniority = 'C-Suite'
        c_suite_flag = 1
    elif any(w in pos_lower for w in ['vice president', 'vp', 'director', 'head of', 'principal', 'general manager']):
        seniority = 'VP / Director'
    elif any(w in pos_lower for w in ['manager', 'lead', 'team lead', 'supervisor', 'architect', 'head']):
        seniority = 'Manager / Lead'
    elif any(w in pos_lower for w in ['intern', 'trainee', 'apprentice', 'student', 'fellow']):
        seniority = 'Intern / Trainee'
    elif any(w in pos_lower for w in ['senior', 'sr.', 'lead', 'specialist', 'consultant', 'analyst']):
        seniority = 'Senior IC'
        
    func = 'Other / General'
    if any(w in pos_lower for w in ['hr', 'human resources', 'talent acquisition', 'recruiter', 'recruiting', 'staffing', 'people operations', 'talent partner', 'talent advisor']):
        func = 'HR & Talent Acquisition'
        recruiter_flag = 1
    elif any(w in pos_lower for w in ['operations', 'supply chain', 'logistics', 'procurement', 'exim', 'export', 'import', 'shipping', 'customs', 'freight']):
        func = 'Operations, Logistics & Trade'
    elif any(w in pos_lower for w in ['consulting', 'consultant', 'advisory', 'strategy', 'transformation', 'business analyst']):
        func = 'Management & Strategy Consulting'
    elif any(w in pos_lower for w in ['sales', 'business development', 'bde', 'bda', 'account executive', 'account manager', 'commercial']):
        func = 'Sales & Business Development'
    elif any(w in pos_lower for w in ['marketing', 'brand', 'growth', 'seo', 'digital marketing', 'content', 'pr', 'communications']):
        func = 'Marketing & Growth'
    elif any(w in pos_lower for w in ['finance', 'financial', 'audit', 'tax', 'accounting', 'investment', 'banking', 'equity', 'treasury']):
        func = 'Finance & Banking'
    elif any(w in pos_lower for w in ['software', 'engineer', 'developer', 'full stack', 'frontend', 'backend', 'devops', 'cloud', 'data scientist', 'ai', 'ml', 'tech']):
        func = 'Engineering & Technology'
    elif any(w in pos_lower for w in ['product manager', 'product owner', 'product design', 'ui', 'ux']):
        func = 'Product & Design'
    elif any(w in pos_lower for w in ['legal', 'lawyer', 'counsel', 'compliance']):
        func = 'Legal & Compliance'

    if seniority in ['Manager / Lead', 'VP / Director', 'C-Suite', 'Founder'] and recruiter_flag == 0:
        hiring_mgr_flag = 1
        
    co_lower = company.lower()
    company_domain = 'Enterprise / Mid-Market'
    if any(k in co_lower for k in ['ey', 'deloitte', 'pwc', 'kpmg', 'accenture', 'mckinsey', 'bcg', 'bain']):
        company_domain = 'Big 4 / Strategy Consulting'
    elif any(k in co_lower for k in ['goldman', 'jpmorgan', 'morgan stanley', 'hsbc', 'citi', 'barclays', 'standard chartered', 'hdfc', 'icici']):
        company_domain = 'Investment Banking & Financial Services'
    elif any(k in co_lower for k in ['google', 'microsoft', 'amazon', 'apple', 'meta', 'nvidia', 'salesforce', 'oracle', 'cisco', 'intel', 'ibm', 'tcs', 'infosys', 'wipro', 'capgemini']):
        company_domain = 'Global Tech & IT Majors'
    elif any(k in co_lower for k in ['university', 'college', 'institute', 'school']):
        company_domain = 'Education / Academic'
        
    job_rel_score = 30
    if func in ['Operations, Logistics & Trade', 'Management & Strategy Consulting', 'Sales & Business Development', 'HR & Talent Acquisition']:
        job_rel_score += 35
    elif func in ['Finance & Banking', 'Marketing & Growth']:
        job_rel_score += 20
    elif func in ['Product & Design', 'Engineering & Technology']:
        job_rel_score += 10
        
    if company_domain in ['Big 4 / Strategy Consulting', 'Global Tech & IT Majors', 'Investment Banking & Financial Services']:
        job_rel_score += 25
        
    job_rel_score = min(100, job_rel_score)
    
    if recruiter_flag == 1 or (hiring_mgr_flag == 1 and job_rel_score >= 70):
        ref_pot = 'High'
    elif hiring_mgr_flag == 1 or job_rel_score >= 60:
        ref_pot = 'Medium'
    else:
        ref_pot = 'Low'
        
    rec = {
        'First Name': first,
        'Last Name': last,
        'Full Name': full_name,
        'Company': company,
        'Position': position,
        'LinkedIn URL': url,
        'Connected On': connected_on,
        'Email': email,
        'Company Domain': company_domain,
        'Normalized Company': norm_co,
        'Seniority': seniority,
        'Functional Area': func,
        'Recruiter Flag': recruiter_flag,
        'Founder Flag': founder_flag,
        'C-Suite Flag': c_suite_flag,
        'Hiring Manager Flag': hiring_mgr_flag,
        'Referral Potential': ref_pot,
        'Job-Relevance Score': job_rel_score,
        'Geography': 'Bengaluru / India',
        'Notes': '1st-degree connection | Indexed from LinkedIn archive'
    }
    normalized_records.append(rec)

master_csv_path = os.path.join(WORKSPACE, 'linkedin_network_master.csv')
with open(master_csv_path, 'w', encoding='utf-8', newline='') as fp:
    writer = csv.DictWriter(fp, fieldnames=list(normalized_records[0].keys()))
    writer.writeheader()
    writer.writerows(normalized_records)
print(f'Saved {master_csv_path}')

# 3. NETWORK INTELLIGENCE & SCORING
intelligence_records = []
for r in normalized_records:
    sen_score = 10
    if r['Seniority'] in ['Founder', 'C-Suite']: sen_score = 30
    elif r['Seniority'] == 'VP / Director': sen_score = 25
    elif r['Seniority'] == 'Manager / Lead': sen_score = 20
    elif r['Seniority'] == 'Senior IC': sen_score = 15
    elif r['Seniority'] == 'Individual Contributor': sen_score = 10
    elif r['Seniority'] == 'Intern / Trainee': sen_score = 5
    
    hire_score = 5
    if r['Recruiter Flag'] == 1: hire_score = 30
    elif r['Hiring Manager Flag'] == 1: hire_score = 25
    elif r['Functional Area'] in ['Operations, Logistics & Trade', 'Management & Strategy Consulting', 'Sales & Business Development']: hire_score = 18
    elif r['Functional Area'] in ['Finance & Banking', 'Marketing & Growth']: hire_score = 12
    
    co_score = 5
    if r['Company Domain'] in ['Big 4 / Strategy Consulting', 'Investment Banking & Financial Services']: co_score = 20
    elif r['Company Domain'] == 'Global Tech & IT Majors': co_score = 16
    elif r['Company Domain'] == 'Enterprise / Mid-Market': co_score = 10
    
    ref_score = 10 if r['LinkedIn URL'] else 5
    geo_score = 10 if 'Bengaluru' in r['Geography'] else 8
    
    total_network_score = sen_score + hire_score + co_score + ref_score + geo_score
    
    int_rec = dict(r)
    int_rec['Seniority Score (30)'] = sen_score
    int_rec['Hiring Relevance Score (30)'] = hire_score
    int_rec['Company Score (20)'] = co_score
    int_rec['Referral Strength Score (10)'] = ref_score
    int_rec['Geography Score (10)'] = geo_score
    int_rec['Composite Network Score (100)'] = total_network_score
    intelligence_records.append(int_rec)
    
intelligence_records.sort(key=lambda x: x['Composite Network Score (100)'], reverse=True)

intel_csv_path = os.path.join(WORKSPACE, 'linkedin_referral_intelligence.csv')
with open(intel_csv_path, 'w', encoding='utf-8', newline='') as fp:
    writer = csv.DictWriter(fp, fieldnames=list(intelligence_records[0].keys()))
    writer.writeheader()
    writer.writerows(intelligence_records)
print(f'Saved {intel_csv_path}')

# 4. TARGET COMPANY ENGINE
co_groups = defaultdict(list)
for r in normalized_records:
    co = r['Normalized Company']
    if co: co_groups[co].append(r)
        
jobs_61_path = os.path.join(WORKSPACE, 'BBA_IB_Bengaluru_61_Job_Pipeline.csv')
jobs_61 = []
if os.path.exists(jobs_61_path):
    with open(jobs_61_path, 'r', encoding='utf-8-sig', errors='replace') as fp:
        jobs_61 = list(csv.DictReader(fp))
        
company_priority_rows = []
for co, members in co_groups.items():
    co_lower = co.lower()
    rec_count = sum(1 for m in members if m['Recruiter Flag'] == 1)
    founder_count = sum(1 for m in members if m['Founder Flag'] == 1 or m['C-Suite Flag'] == 1)
    hm_count = sum(1 for m in members if m['Hiring Manager Flag'] == 1)
    total_conn = len(members)
    
    matched_jobs = []
    for j in jobs_61:
        j_co = j.get('Company Name', '').lower()
        if (co_lower in j_co) or (j_co and j_co in co_lower):
            matched_jobs.append(j.get('Job Title', ''))
            
    openings_count = len(matched_jobs)
    best_roles = ' | '.join(matched_jobs[:3]) if matched_jobs else 'Business Operations / Management Analyst'
    
    ref_opp = min(100, (rec_count * 15) + (hm_count * 10) + (founder_count * 12) + (total_conn * 2) + (openings_count * 20))
    
    if ref_opp >= 70 or openings_count >= 1 or total_conn >= 50 or any(k in co_lower for k in ['ey', 'deloitte', 'accenture', 'goldman', 'ibm', 'amazon', 'jpmorgan', 'pwc', 'kpmg', 'walmart', 'google']):
        tier = 'Tier A (Extremely High Value)'
        app_priority = 'P0 - Immediate Multi-Channel Outreach'
    elif ref_opp >= 40 or total_conn >= 10:
        tier = 'Tier B (Strong Opportunity)'
        app_priority = 'P1 - Targeted Warm Referral'
    elif ref_opp >= 20 or total_conn >= 3:
        tier = 'Tier C (Useful / Moderate Probability)'
        app_priority = 'P2 - Secondary Sourcing'
    else:
        tier = 'Tier D (Low Relevance / Boutique)'
        app_priority = 'P3 - Ad-Hoc'
        
    company_priority_rows.append({
        'Company': co,
        'Total Connections': total_conn,
        'Recruiters Count': rec_count,
        'Founders / C-Suite Count': founder_count,
        'Hiring Managers Count': hm_count,
        'Active Pipeline Openings Count': openings_count,
        'Best Matching Job Roles': best_roles,
        'Referral Opportunity Score': ref_opp,
        'Tier': tier,
        'Application Priority': app_priority
    })

tier_order = {'Tier A (Extremely High Value)': 0, 'Tier B (Strong Opportunity)': 1, 'Tier C (Useful / Moderate Probability)': 2, 'Tier D (Low Relevance / Boutique)': 3}
company_priority_rows.sort(key=lambda x: (tier_order.get(x['Tier'], 4), -x['Referral Opportunity Score'], -x['Total Connections']))

co_priority_csv = os.path.join(WORKSPACE, 'target_company_priority.csv')
with open(co_priority_csv, 'w', encoding='utf-8', newline='') as fp:
    writer = csv.DictWriter(fp, fieldnames=list(company_priority_rows[0].keys()))
    writer.writeheader()
    writer.writerows(company_priority_rows)
print(f'Saved {co_priority_csv}')
