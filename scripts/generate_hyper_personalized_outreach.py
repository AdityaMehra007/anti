import csv
import json
import re
import os

# 1. Load Connections
csv_path = r'e:\anti\linkedin_export\Connections.csv'
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

header_idx = -1
for i, line in enumerate(lines[:10]):
    if 'First Name' in line:
        header_idx = i
        break

reader = csv.DictReader(lines[header_idx:])
connections = list(reader)

# 2. Comprehensive Target Employer Catalog (50+ Companies with Active Requisitions)
target_jobs_map = {
    'goldman': ('Goldman Sachs', '4452387165', 'Global Banking & Markets Operations - IB Ops Client Onboarding Analyst', 'Aditya_Mehra_Resume_005_goldman_sachs.pdf', 'http://www.linkedin.com/jobs/view/4452387165'),
    'jpmorgan': ('JPMorganChase', '4440836681', 'Data Management Associate / Operations Analyst', 'Aditya_Mehra_Resume_006_jp_morgan_chase.pdf', 'http://www.linkedin.com/jobs/view/4440836681'),
    'chase': ('JPMorganChase', '4440836681', 'Data Management Associate / Operations Analyst', 'Aditya_Mehra_Resume_006_jp_morgan_chase.pdf', 'http://www.linkedin.com/jobs/view/4440836681'),
    'deutsche bank': ('Deutsche Bank', 'DB_CIB_OPS_2026', 'Clearing & Settlements Operations Analyst', 'Aditya_Mehra_Resume_EXIM_International_Trade_2026.pdf', 'https://careers.db.com'),
    'commonwealth bank': ('Commonwealth Bank of Australia', 'CBA_INDIA_GRAD_2026', 'Credit Risk & Operations Analyst', 'Aditya_Mehra_Resume_EXIM_International_Trade_2026.pdf', 'https://www.commbank.com.au/about-us/careers'),
    'cba': ('Commonwealth Bank of Australia', 'CBA_INDIA_GRAD_2026', 'Credit Risk & Operations Analyst', 'Aditya_Mehra_Resume_EXIM_International_Trade_2026.pdf', 'https://www.commbank.com.au/about-us/careers'),
    'hsbc': ('HSBC', '4452434953', 'Business Analyst - Commercial Banking & Operations', 'Aditya_Mehra_Resume_EXIM_International_Trade_2026.pdf', 'http://www.linkedin.com/jobs/view/4452434953'),
    'icici': ('ICICI Bank', 'ICICI_PO_2026', 'Deputy Manager - Commercial Banking & Relationship Ops', 'Aditya_Mehra_Resume_EXIM_International_Trade_2026.pdf', 'https://www.icicicareers.com'),
    'ey': ('EY', '4444908737', 'GDS Meetings and Events - Events Manager / Associate', 'Aditya_Mehra_Resume_003_ey_ernst_young_gds.pdf', 'http://www.linkedin.com/jobs/view/4444908737'),
    'ernst': ('EY', '4444908737', 'GDS Meetings and Events - Events Manager / Associate', 'Aditya_Mehra_Resume_003_ey_ernst_young_gds.pdf', 'http://www.linkedin.com/jobs/view/4444908737'),
    'deloitte': ('Deloitte', 'DELOITTE_USI_ANALYST_2026', 'Analyst / Associate Consultant - Operations Transformation', 'Aditya_Mehra_Resume_002_deloitte_us_india.pdf', 'https://jobsindia.deloitte.com'),
    'pwc': ('PwC India', '4409108662', 'Associate - Operations Advisory & Transformation', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4409108662'),
    'pricewaterhouse': ('PwC India', '4409108662', 'Associate - Operations Advisory & Transformation', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4409108662'),
    'kpmg': ('KPMG India', 'KPMG_INDIA_ANALYST_2026', 'Analyst - Business Advisory / Deal Advisory & Operations', 'Aditya_Mehra_Resume_012_kpmg_global_services.pdf', 'https://kpmg.com/in/en/home/careers.html'),
    'amazon': ('Amazon', '4443027895 / 4455781999', 'Event Program Manager, AWS Global Events / Supply Chain BA', 'Aditya_Mehra_Resume_004_amazon_bangalore.pdf', 'http://www.linkedin.com/jobs/view/4443027895'),
    'aws': ('Amazon Web Services', '4443027895', 'Event Program Manager, AWS Global Events', 'Aditya_Mehra_Resume_004_amazon_bangalore.pdf', 'http://www.linkedin.com/jobs/view/4443027895'),
    'microsoft': ('Microsoft', '4379272973', 'Research Sciences Intern / PM Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4379272973'),
    'google': ('Google', 'GOOGLE_IN_PEOPLE_OPS', 'Product Support Specialist (GPay) / Operations Specialist', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://www.google.com/about/careers/applications'),
    'cisco': ('Cisco', '4446332173', 'Data & Supply Chain Analyst Associate', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'http://www.linkedin.com/jobs/view/4446332173'),
    'ibm': ('IBM India', 'IBM_INDIA_EARLY_CAREER_2026', 'Associate System Operations Specialist / Accounts Receivable Analyst', 'Aditya_Mehra_Resume_009_ibm_india.pdf', 'https://www.ibm.com/careers/in-en'),
    'accenture': ('Accenture', '4429242140 / 4448338203', 'Business Advisory New Associate / Supply Chain Ops Senior Analyst', 'Aditya_Mehra_Resume_001_accenture_india.pdf', 'http://www.linkedin.com/jobs/view/4429242140'),
    'tata consultancy': ('Tata Consultancy Services', 'TCS_NQT_CAMPUS_2026', 'TCS Prime / Digital / Ninja Business Analyst', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://nextstep.tcs.com'),
    'tcs': ('Tata Consultancy Services', 'TCS_NQT_CAMPUS_2026', 'TCS Prime / Digital / Ninja Business Analyst', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://nextstep.tcs.com'),
    'capgemini': ('Capgemini', 'CAPGEMINI_EXCELLER_2026', 'Financial & Operations Analyst / Business Trainee', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://www.capgemini.com/in-en/careers'),
    'cognizant': ('Cognizant', 'CTS_GENC_2026', 'Process Executive - Digital Operations / Analyst Trainee', 'Aditya_Mehra_Resume_Process_Risk_Ops_2026.pdf', 'https://careers.cognizant.com/in/en'),
    'infosys': ('Infosys', 'INFOSYS_EARLY_CAREER_2026', 'Associate Consultant / Specialist Operations', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://www.infosys.com/careers.html'),
    'wipro': ('Wipro', 'WIPRO_ELITE_2026', 'Business Analyst / Project Operations Coordinator', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://careers.wipro.com'),
    'target': ('Target in India', 'TARGET_IN_OPS_2026', 'Merchandise Payables Specialist / HR & Business Operations', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://india.target.com/careers'),
    'razorpay': ('Razorpay', '4439995783', 'Analyst - Business Operations / Merchant Ops Specialist', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4439995783'),
    'rippling': ('Rippling', 'RIPPLING_OPS_2026', 'Identity & Integration Specialist / Platform Support Specialist', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://www.rippling.com/careers'),
    'ditto': ('Ditto Insurance', 'DITTO_OPS_2026', 'Insurance Operations Consultant / Advisory Specialist', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://joinditto.in/careers/'),
    'swiggy': ('Swiggy', 'SWIGGY_OPS_001', 'Operations & Expansion Associate', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://careers.swiggy.com'),
    'zepto': ('Zepto', 'ZEPTO_OPS_002', 'City Operations Lead - Dark Store SCM', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://www.zeptonow.com/careers'),
    'itc': ('ITC Limited', 'ITC_SCM_2026', 'Area Supply Chain Executive / Finance & Logistics Intern', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://www.itcportal.com/careers/'),
    'physicswallah': ('PhysicsWallah', 'PW_OPS_2026', 'Operations Associate / Center Operations Lead', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://pw.live/careers'),
    'pw ': ('PhysicsWallah', 'PW_OPS_2026', 'Operations Associate / Center Operations Lead', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://pw.live/careers'),
    'ather': ('Ather Energy', 'ATHER_SC_001', 'Supply Chain & Operations Lead', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://www.atherenergy.com/careers'),
    'glean': ('Glean', '4453740312', 'Cost & Commercial Operations Associate', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://jobs.ashbyhq.com/glean'),
    'postman': ('Postman', 'POSTMAN_OPS_003', 'Business Operations Analyst', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'https://boards.greenhouse.io/postman'),
    'wrike': ('Wrike', '4440968428', 'Partner Operations Specialist', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'https://boards.greenhouse.io/wrike'),
    'hilton': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4450278984'),
    'conrad': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4450278984'),
    'marriott': ('JW Marriott', '4436777567', 'Assistant Events Manager', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4436777567'),
    'thomson reuters': ('Thomson Reuters', '4446747144', 'Events Coordinator', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4446747144'),
    'mathworks': ('MathWorks', '4406706536', 'Marketing Event Specialist', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4406706536'),
    'globallogic': ('GlobalLogic', '4451402094', 'Event Marketing Specialist IRC298882', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4451402094'),
    'oracle': ('Oracle', '4048014873', 'Student / Intern (Cloud & Tech)', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4048014873'),
    'coindcx': ('CoinDCX', '4424404412', 'Analyst - Operations', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4424404412'),
    'ust': ('UST', '4441571067', 'Business Operations Support', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4441571067'),
    'wns': ('WNS', '4430704372', 'Bangalore Walkins - Operations', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4430704372'),
    'blissclub': ('Blissclub', '4437012823', 'Business Analyst', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'http://www.linkedin.com/jobs/view/4437012823'),
    'bni': ('BNI Global', '4406514782', 'Event Logistics Coordinator', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'http://www.linkedin.com/jobs/view/4406514782'),
    'galaxeye': ('GalaxEye', '4373303563', 'Market Research Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4373303563'),
    'tyfone': ('Tyfone, Inc.', '4371505461', 'Business Intelligence & Data Analyst Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4371505461'),
    'expedify': ('Expedify', '4374985662', 'AI Product Analytics Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4374985662'),
    'emergent': ('Emergent', '4439983503', 'AI Analyst', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4439983503'),
    'volvo': ('Volvo Construction Equipment', '4429029965', 'Graduate Apprentice Trainee', 'Aditya_Mehra_Resume_PMO_Vendor_Logistics_2026.pdf', 'http://www.linkedin.com/jobs/view/4429029965'),
    'inspironlabs': ('InspironLabs', '4370182887', 'Management Trainee', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4370182887'),
    'englishbhashi': ('EnglishBhashi', '4377959748', 'Product Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4377959748'),
    'tata consumer': ('Tata Consumer Products', '4021834253', 'Human Resources Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4021834253'),
    'infrabyte': ('Infrabyte Consulting', '4381181841', 'Data / Business Analyst Intern', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4381181841'),
    'tokens': ('tokens&', '4449673093', 'Operations Associate – Founder Office', 'Aditya_Mehra_Resume_Master_Operations_2026.pdf', 'http://www.linkedin.com/jobs/view/4449673093')
}

def clean_first_name(raw_fn):
    fn = raw_fn.strip()
    # Strip honorifics & titles
    fn = re.sub(r'^(Dr\.?|Prof\.?|CA\.?|CFA\.?|Adv\.?|Mr\.?|Ms\.?|Mrs\.?|Major|Col\.?)\s+', '', fn, flags=re.IGNORECASE)
    # Strip non-word characters at start
    fn = re.sub(r'^[^\w]+', '', fn)
    parts = fn.split()
    clean = parts[0] if parts else 'there'
    # Capitalize nicely
    return clean.capitalize() if len(clean) > 1 else 'there'

def clean_company_name(raw_co):
    co = raw_co.strip()
    if not co or co.lower() in ['independent', 'not disclosed', 'none', 'self-employed', 'freelance']:
        return None
    # Strip corporate legal suffixes for natural dialogue
    co = re.sub(r'\s+(Pvt\.?\s*Ltd\.?|Private\s+Limited|Ltd\.?|Limited|Inc\.?|LLC|Corporation|Corp\.?)$', '', co, flags=re.IGNORECASE)
    return co.strip()

def clean_position(raw_pos):
    pos = raw_pos.strip()
    if not pos:
        return 'Professional'
    # Trim excessive pipe suffixes
    if '|' in pos:
        pos = pos.split('|')[0].strip()
    if '•' in pos:
        pos = pos.split('•')[0].strip()
    return pos

processed = []
for c in connections:
    raw_fn = c.get('First Name', '').strip()
    ln = c.get('Last Name', '').strip()
    full_name = f"{raw_fn} {ln}".strip()
    first_name = clean_first_name(raw_fn)
    company_raw = c.get('Company', '').strip()
    company_display = clean_company_name(company_raw)
    position = clean_position(c.get('Position', '').strip())
    url = c.get('URL', '').strip()
    email = c.get('Email Address', '').strip()
    connected_on = c.get('Connected On', '').strip()

    co_lower = company_raw.lower()
    pos_lower = position.lower()

    # 1. Match Active Target Jobs
    matched_job = None
    for k, val in target_jobs_map.items():
        if k in co_lower:
            matched_job = val
            break

    packet_text = """--- CANDIDATE REFERRAL PACKET (WORKDAY / TALEO / ASHBY) ---
• Legal Name: Aditya Mehra
• Email: ashishiash007@gmail.com | Phone: +91 7003456624
• Degree: BBA International Business, Dayananda Sagar University (Batch 2026)
• Core Proof: Operations Lead at AERO INDIA 2025 (100k+ attendees, 0 security infractions, 0.0% shrinkage); Contract SLA compliance for Tata Communications & Puma Global.
• Resume & LinkedIn: https://www.linkedin.com/in/aditya-mehra
-----------------------------------------------------------"""

    if matched_job:
        target_co, jid, jtitle, jresume, jurl = matched_job
        category = "Tier 1: Active Job ID Mapped"
        job_info = f"{target_co} | {jtitle} (Job ID: {jid})"
        
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope your week is off to a wonderful start! Always inspiring seeing your journey as {position} at {target_co}.\n\n"
            f"I'm reaching out with genuine respect for your craft and team. As a final-year BBA (International Business) candidate at Dayananda Sagar University here in Bengaluru, I've focused on high-accountability operational execution—serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (managing crowd logistics and multi-vendor coordination for 100,000+ delegates with zero security breaches and 0.0% shrinkage) alongside managing run-of-show contracts for Tata Communications and Puma Global.\n\n"
            f"I noticed an active opening at {target_co} that aligns directly with my execution background:\n"
            f"• Target Role: {jtitle}\n"
            f"• Job ID / Req ID: {jid}\n\n"
            f"Knowing how much operational excellence and team standards matter at {target_co}, I would be deeply honored if you might consider putting in an internal referral for my profile. To save you time and make this completely frictionless for your internal portal, here is my pre-filled candidate packet:\n\n"
            f"{packet_text}\n\n"
            f"Please know there is absolutely zero pressure if company referral guidelines or bandwidth make this difficult right now—just connecting with you and learning from your experience at {target_co} is already a true privilege.\n\n"
            f"Wishing you and your team continued momentum and success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(hr_term in pos_lower for hr_term in ['talent', 'recruit', 'hr', 'human resources', 'sourcing', 'people partner', 'talent acquisition']):
        category = "Tier 2: HR & Talent Acquisition"
        co_str = company_display if company_display else "your organization"
        job_info = f"Early Career & Lateral Hiring at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope your week is going great! I've been following your impactful work shaping talent pipelines and team culture as {position} at {co_str}.\n\n"
            f"I am wrapping up my final year in International Business at Dayananda Sagar University here in Bengaluru. My background is centered on disciplined operations, supply chain logistics, and high-stakes vendor management—recently serving as Operations Lead at AERO INDIA 2025 (100,000+ attendees, 0 security breaches, 0.0% inventory shrinkage) and managing contract SLAs for Tata Communications.\n\n"
            f"As your team at {co_str} plans upcoming hiring or campus/entry-level intakes for operations, business analysis, supply chain, or program specialist roles, I would love to be on your radar. To make review effortless, here is a quick snapshot of my candidate packet:\n\n"
            f"{packet_text}\n\n"
            f"Thank you sincerely for all the dedication you bring to talent acquisition, and I'd be honored to connect or share my tailored resume whenever convenient.\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(lead_term in pos_lower for lead_term in ['director', 'vice president', 'vp', 'partner', 'founder', 'ceo', 'co-founder', 'managing director', 'general manager', 'head of', 'chief']):
        category = "Tier 2: Senior Leadership & Executives"
        co_str = company_display if company_display else "your enterprise"
        job_info = f"Executive Alignment & Leadership Insights at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"I hope this message finds you well. I’ve greatly admired your leadership as {position} at {co_str} and the strategic direction your team is driving.\n\n"
            f"As I complete my International Business degree at Dayananda Sagar University, my goal is to contribute to organizations where operational integrity, customer trust, and rigorous execution are prized. Having led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ attendees with zero security incidents and 0.0% shrinkage) and enforced multi-vendor contract SLAs for Tata Communications and Puma Global, I know how essential execution fidelity is to senior leaders like yourself.\n\n"
            f"I would be deeply honored for a brief 5-minute perspective on what you value most when building resilient operational teams at {co_str}. And if an early-career analyst or operations opening exists within your group, I would be profoundly grateful for your guidance.\n\n"
            f"Thank you sincerely for your time and leadership, {first_name}.\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(ops_term in pos_lower for ops_term in ['operation', 'supply chain', 'logistics', 'procurement', 'inventory', 'pmo', 'vendor']):
        category = "Tier 4: Operations & Supply Chain Network"
        co_str = company_display if company_display else "your team"
        job_info = f"Operations & Supply Chain Kinship at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you're having a productive week! Always great connecting with a fellow operational leader—especially seeing your execution as {position} at {co_str}.\n\n"
            f"As I complete my final year in International Business at Dayananda Sagar University, I've dedicated myself to rigorous operational delivery. Serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (100k+ attendees, 0 security infractions, 0.0% shrinkage) and managing run-of-show logistics and SLA contract enforcement for Puma Global and Tata Communications taught me the true value of relentless ground discipline.\n\n"
            f"I would love to exchange notes on operational workflows, vendor governance, and best practices at {co_str}. If you ever have a few minutes for a virtual coffee or quick conversation, it would be a pleasure to connect.\n\n"
            f"Wishing you seamless operations and continued momentum!\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(fin_term in pos_lower for fin_term in ['finance', 'accounting', 'audit', 'tax', 'banker', 'banking', 'investment', 'credit', 'risk analyst', 'treasury']):
        category = "Tier 4: Finance & Banking Network"
        co_str = company_display if company_display else "your firm"
        job_info = f"Financial Operations & Governance at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope all is well with you! I’ve been following your professional journey in financial governance and analysis as {position} at {co_str}.\n\n"
            f"I'm currently concluding my final year in International Business at Dayananda Sagar University, with a strong focus on financial reconciliation, trade finance documentation (INCOTERMS 2020, Letters of Credit), and contract compliance. During AERO INDIA 2025, I maintained a 0.0% inventory shrinkage record across high-volume assets and managed multi-vendor billing and SLA compliance for Tata Communications.\n\n"
            f"I would love to learn how your team approaches financial operations and risk management at {co_str}, and explore potential early-career analyst opportunities. Wishing you a great financial quarter ahead!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(tech_term in pos_lower for tech_term in ['developer', 'software', 'engineer', 'architect', 'data analyst', 'data scientist', 'product manager', 'frontend', 'backend', 'full stack', 'cloud']):
        category = "Tier 4: Technology & Product Network"
        co_str = company_display if company_display else "your team"
        job_info = f"Tech & Business Intersection at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a fantastic week! It's always inspiring following your technical craft and journey as {position} at {co_str}.\n\n"
            f"While my core discipline is International Business and Operations at Dayananda Sagar University, I work closely at the intersection of business operations and technology systems. Recently, I led operations at AERO INDIA 2025 (100,000+ delegates, 0 breaches, 0.0% inventory loss) where real-time coordination, automated tracking, and multi-vendor communication protocols were mission-critical.\n\n"
            f"I have immense respect for the engineering and product standards at {co_str}. If your team or cross-functional operations group is ever looking for an early-career operator who bridges business logic, system discipline, and data integrity, I'd love to connect and learn about your experience there.\n\n"
            f"Wishing you and your team smooth deployments and continued success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(alumni_term in co_lower for alumni_term in ['christ', 'dayananda', 'dsu', 'iisc', 'student welfare', 'cusbma']) or any(stud_term in pos_lower for stud_term in ['student', 'intern', 'campus', 'president', 'council', 'volunteer']):
        category = "Tier 3: University & Alumni Network"
        co_str = company_display if company_display else "our campus network"
        job_info = f"Campus Camaraderie & Mutual Growth ({co_str})"
        msg = (
            f"Hi {first_name},\n\n"
            f"Great to connect with a fellow campus peer! It’s inspiring seeing your growth as {position} with {co_str}.\n\n"
            f"I'm currently in my final year of BBA (International Business) at Dayananda Sagar University. Over the past year, I had the privilege of leading ground operations at AERO INDIA 2025 at Yelahanka AFB (managing 100k+ footfall with 0 breaches and 0 shrinkage) alongside corporate logistics for Tata Communications.\n\n"
            f"I'm actively exploring early-career analyst and operations roles across Bengaluru. If you ever have a few minutes to share your thoughts on your journey since graduation, or if I can ever support you in any way, let's definitely catch up!\n\n"
            f"Wishing you continued success and proud to be part of the same community!\n\n"
            f"Cheers,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(sales_term in pos_lower for sales_term in ['sales', 'marketing', 'business development', 'growth', 'account manager', 'brand', 'commercial']):
        category = "Tier 4: Commercial & Growth Network"
        co_str = company_display if company_display else "your company"
        job_info = f"Commercial & Growth Execution at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a thriving week! Really admire the commercial momentum and customer growth you're driving as {position} at {co_str}.\n\n"
            f"I'm concluding my International Business degree at Dayananda Sagar University, specializing in commercial operations, cross-border business, and high-touch brand activations. Having led event operations at AERO INDIA 2025 for 100k+ visitors and delivered run-of-show logistics for Puma Global and Tata Communications, I understand how vital seamless delivery is to maintaining customer trust and commercial success.\n\n"
            f"If there is ever any way I can assist your initiatives in Bengaluru, or if you're open to connecting about operational growth at {co_str}, I'd be delighted to chat.\n\n"
            f"Wishing you high conversions and continued success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    else:
        co_str = company_display if company_display else "your organization"
        category = "Tier 4: Enterprise Network & Reconnect"
        job_info = f"Professional Connection at {co_str}"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a wonderful week! Always inspiring following your journey as {position} at {co_str}.\n\n"
            f"I wanted to reach out, say hello, and share a quick personal update. I am completing my final year in International Business at Dayananda Sagar University in Bengaluru. Over the past year, I've led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ delegates with zero security breaches and 0.0% inventory shrinkage) and managed multi-vendor SLA contracts for Tata Communications and Puma Global summits.\n\n"
            f"I'm currently exploring opportunities in operations, program management, and business analytics. If you or anyone in your network is ever looking for a disciplined, execution-focused operator—or if I can ever help support your initiatives here in Bengaluru—I would love to connect for a brief 5-minute chat.\n\n"
            f"Wishing you continued success in your journey!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    processed.append({
        'name': full_name,
        'first_name': first_name,
        'company': company_raw or 'Independent / Not Disclosed',
        'position': position,
        'category': category,
        'job_info': job_info,
        'url': url,
        'email': email,
        'date': connected_on,
        'message': msg
    })

print(f"Processed all {len(processed)} connections with bespoke personalization.")

# Write CSV
out_csv = r'e:\anti\linkedin_export\connection_personalized_messages.csv'
with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Full Name', 'First Name', 'Company', 'Position', 'Tier / Category', 
        'Job Info & ID', 'LinkedIn URL', 'Email Address', 'Connected Date', 
        'Personalized Relationship Message'
    ])
    for p in processed:
        writer.writerow([
            p['name'], p['first_name'], p['company'], p['position'], p['category'],
            p['job_info'], p['url'], p['email'], p['date'], p['message']
        ])

print(f"Generated {out_csv} with {len(processed)} personalized messages.")

# Write JSON
out_json = r'e:\anti\linkedin_export\connection_outreach_data.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print(f"Generated {out_json} successfully.")
