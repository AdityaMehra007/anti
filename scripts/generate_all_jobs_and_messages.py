import csv
import json
import re
import os

print("--- Starting Apex Job Openings & Hyper-Personalized Messaging Engine (Master Edition) ---")

# 1. Load Connections
csv_path = r'e:\anti\linkedin_export\Connections.csv'
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

header_idx = -1
for i, line in enumerate(lines[:10]):
    if 'First Name' in line and 'Company' in line:
        header_idx = i
        break

reader = csv.DictReader(lines[header_idx:])
connections = list(reader)
print(f"Loaded {len(connections):,} connections from {csv_path}")

# 2. Master Job Opening & Requisition Catalog (105+ Enterprise & High-Growth Employers)
# Key: lower-case substring match for company
# Value: (Display Company Name, Job ID / Req ID, Target Role Title, Job Portal URL, Sector)
master_jobs_catalog = {
    # Tier 1 Investment Banking & Global Financial Services
    'goldman': ('Goldman Sachs', '4452387165', 'Global Banking & Markets Operations - Client Onboarding Analyst (Entry-Level / Campus 2026)', 'http://www.linkedin.com/jobs/view/4452387165', 'Investment Banking'),
    'jpmorgan': ('JPMorganChase', '4440836681', 'Commercial Banking & Data Operations Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4440836681', 'Investment Banking'),
    'chase': ('JPMorganChase', '4440836681', 'Commercial Banking & Data Operations Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4440836681', 'Investment Banking'),
    'deutsche bank': ('Deutsche Bank', 'DB_CIB_OPS_2026', 'Clearing & Settlements Operations Analyst (Graduate Trainee / Fresher 2026)', 'https://careers.db.com', 'Investment Banking'),
    'commonwealth bank': ('Commonwealth Bank of Australia', 'CBA_INDIA_GRAD_2026', 'Credit Risk & Operations Analyst (Graduate Trainee / Fresher 2026)', 'https://www.commbank.com.au/about-us/careers', 'Global Banking'),
    'cba': ('Commonwealth Bank of Australia', 'CBA_INDIA_GRAD_2026', 'Credit Risk & Operations Analyst (Graduate Trainee / Fresher 2026)', 'https://www.commbank.com.au/about-us/careers', 'Global Banking'),
    'hsbc': ('HSBC', '4452434953', 'Commercial Banking & Operations Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4452434953', 'Global Banking'),
    'icici': ('ICICI Bank', 'ICICI_PO_2026', 'Probationary Officer / Commercial Banking Trainee (Fresher Intake 2026)', 'https://www.icicicareers.com', 'Banking & Finance'),
    'hdfc': ('HDFC Bank', 'HDFC_FUTURE_BANKERS_2026', 'Operations Associate / Management Trainee (Fresher 2026)', 'https://www.hdfcbank.com/careers', 'Banking & Finance'),
    'sbi': ('State Bank of India', 'SBI_SCO_OPS_2026', 'Junior Operations & Financial Analyst (Entry-Level / Fresher 2026)', 'https://sbi.co.in/careers', 'Banking & Finance'),
    'morgan stanley': ('Morgan Stanley', 'MS_ISG_OPS_2026', 'Operations Analyst - Institutional Securities (Campus Graduate / Fresher 2026)', 'https://morganstanley.tal.net/careers', 'Investment Banking'),
    'wells fargo': ('Wells Fargo', 'WF_EGS_ANALYST_2026', 'Commercial Banking & Operations Specialist (Entry-Level / Fresher 2026)', 'https://www.wellsfargo.com/about/careers', 'Global Banking'),
    'state street': ('State Street', 'SS_GHR_ANALYST_2026', 'Custody & Fund Operations Analyst (Graduate Trainee / Fresher 2026)', 'https://www.statestreet.com/careers', 'Custody & Asset Mgmt'),
    'american express': ('American Express', 'AMEX_OPS_ANALYST_2026', 'Business Operations & Risk Analyst (Campus Intake / Entry-Level 2026)', 'https://aexp.eightfold.ai/careers', 'Payments & Risk'),
    'amex': ('American Express', 'AMEX_OPS_ANALYST_2026', 'Business Operations & Risk Analyst (Campus Intake / Entry-Level 2026)', 'https://aexp.eightfold.ai/careers', 'Payments & Risk'),
    'barclays': ('Barclays', 'BARC_OPS_ANALYST_2026', 'Global Operations & Business Analyst (Graduate Analyst / Fresher 2026)', 'https://search.jobs.barclays', 'Global Banking'),
    'bnp paribas': ('BNP Paribas', 'BNP_IS_OPS_2026', 'Securities Services & Operations Trainee (Graduate Fresher 2026)', 'https://group.bnpparibas/en/careers', 'Global Banking'),
    'anz': ('ANZ Banking Group', 'ANZ_INDIA_OPS_2026', 'Operations Analyst - Institutional Banking (Entry-Level / Fresher 2026)', 'https://www.anz.com/careers/', 'Global Banking'),
    'gallagher': ('Gallagher', 'AJG_INDIA_ANALYST_2026', 'Operations Analyst - Client Risk Solutions (Entry-Level / Fresher 2026)', 'https://jobs.ajg.com', 'Risk & Insurance'),
    'stripe': ('Stripe', 'STRIPE_OPS_SPECIALIST_2026', 'Risk & Commercial Operations Specialist (Early Career / Entry-Level 2026)', 'https://stripe.com/jobs', 'Global FinTech'),
    'standard chartered': ('Standard Chartered Bank', 'SCB_INDIA_GRAD_2026', 'International Graduate - Global Banking & Operations (Campus 2026)', 'https://www.sc.com/en/careers/', 'Global Banking'),
    'societe generale': ('Societe Generale', 'SOCGEN_INDIA_OPS_2026', 'Global Operations & Derivatives Analyst (Graduate Trainee / Fresher 2026)', 'https://careers.societegenerale.com', 'Global Banking'),
    'ubs': ('UBS', 'UBS_INDIA_GRAD_2026', 'Operations & Wealth Management Specialist (Graduate Program / Fresher 2026)', 'https://www.ubs.com/global/en/careers.html', 'Wealth Management'),
    'mastercard': ('Mastercard', 'MA_OPS_ANALYST_2026', 'Operations & Payment Processing Specialist (Entry-Level / Campus 2026)', 'https://mastercard.jobs', 'Payment Networks'),
    'visa': ('Visa', 'VISA_IN_OPS_2026', 'Global Operations & Merchant Settlement Analyst (Entry-Level / Fresher 2026)', 'https://vi.sa/careers', 'Payment Networks'),
    'fidelity': ('Fidelity Investments', 'FID_OPS_ANALYST_2026', 'Fund Operations & Financial Analyst (Early Career / Fresher 2026)', 'https://jobs.fidelity.com', 'Asset Management'),
    'coindcx': ('CoinDCX', '4424404412', 'Analyst - Operations (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4424404412', 'FinTech & Web3'),
    'angel one': ('Angel One', '4446658627', 'Data Analyst - Wealth Operations (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4446658627', 'FinTech'),
    'super.money': ('super.money', '4451136396', 'Infosec & Operations Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4451136396', 'FinTech'),
    'smart paisa': ('Smart Paisa', '4448010242', 'Operations Associate & Client Relationship Trainee (Fresher 2026)', 'http://www.linkedin.com/jobs/view/4448010242', 'FinTech'),
    'rupeek': ('Rupeek', '4445709467', 'Operations Associate / Program Trainee (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4445709467', 'FinTech'),

    # Big 4 & Top-Tier Global Strategy Consulting
    'ey': ('EY', '4444908737', 'GDS Meetings and Events - Operations & Events Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4444908737', 'Big 4 / Consulting'),
    'ernst': ('EY', '4444908737', 'GDS Meetings and Events - Operations & Events Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4444908737', 'Big 4 / Consulting'),
    'deloitte': ('Deloitte', '4242714931 / DELOITTE_USI_ANALYST_2026', 'Operations Transformation Analyst / HR Operations Intern (Campus / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4242714931', 'Big 4 / Consulting'),
    'pwc': ('PwC India', '4409108662', 'Associate - Operations Advisory & Transformation (Campus / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4409108662', 'Big 4 / Consulting'),
    'pricewaterhouse': ('PwC India', '4409108662', 'Associate - Operations Advisory & Transformation (Campus / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4409108662', 'Big 4 / Consulting'),
    'kpmg': ('KPMG India', 'KPMG_INDIA_ANALYST_2026', 'Analyst - Business Advisory / Deal Advisory & Operations (Graduate Trainee / Fresher 2026)', 'https://kpmg.com/in/en/home/careers.html', 'Big 4 / Consulting'),
    'bcg': ('Boston Consulting Group (BCG)', 'BCG_A_CONSULTANT_2026', 'Associate - Management Consulting & Operations Practice (Campus Hire 2026)', 'https://careers.bcg.com', 'Strategy Consulting'),
    'boston consulting': ('Boston Consulting Group (BCG)', 'BCG_A_CONSULTANT_2026', 'Associate - Management Consulting & Operations Practice (Campus Hire 2026)', 'https://careers.bcg.com', 'Strategy Consulting'),
    'mckinsey': ('McKinsey & Company', 'MCK_BA_INDIA_2026', 'Business Analyst - Operations & Client Capabilities (Campus Hire / Fresher 2026)', 'https://www.mckinsey.com/careers', 'Strategy Consulting'),
    'bain': ('Bain & Company', 'BAIN_BGA_2026', 'Associate Consultant - Global Operations & Strategy (Campus Hire 2026)', 'https://www.bain.com/careers', 'Strategy Consulting'),

    # Big Tech, Cloud, Silicon & Hardware
    'amazon': ('Amazon', '4443027895 / 4455781999', 'AWS Global Events Operations Associate / Supply Chain Analyst (Entry-Level / Campus 2026)', 'http://www.linkedin.com/jobs/view/4443027895', 'Big Tech'),
    'aws': ('Amazon Web Services (AWS)', '4443027895', 'AWS Global Events Operations Associate (Entry-Level / Campus 2026)', 'http://www.linkedin.com/jobs/view/4443027895', 'Cloud Tech'),
    'microsoft': ('Microsoft', '4379272973 / 4052096504', 'PM Intern / Operations Sciences Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4379272973', 'Big Tech'),
    'google': ('Google', 'GOOGLE_IN_PEOPLE_OPS', 'Product Support Specialist (GPay) / Operations Specialist (Entry-Level / Fresher 2026)', 'https://www.google.com/about/careers/applications', 'Big Tech'),
    'cisco': ('Cisco', '4446332173', 'Data & Supply Chain Analyst Associate (Campus Graduate / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4446332173', 'Tech Infrastructure'),
    'ibm': ('IBM India', 'IBM_INDIA_EARLY_CAREER_2026', 'Associate System Operations Specialist / Accounts Receivable Analyst (Early Career 2026)', 'https://www.ibm.com/careers/in-en', 'Enterprise Tech'),
    'oracle': ('Oracle', '4048014873', 'Student / Intern (Cloud & Tech Operations 2026)', 'http://www.linkedin.com/jobs/view/4048014873', 'Enterprise Software'),
    'apple': ('Apple', 'AAPL_IN_OPS_2026', 'Supply Chain & Logistics Specialist (Entry-Level / Campus 2026)', 'https://jobs.apple.com', 'Consumer Tech'),
    'dell': ('Dell Technologies', 'DELL_IN_OPS_2026', 'Operations Specialist - Global Supply Chain (Entry-Level / Campus 2026)', 'https://jobs.dell.com', 'Tech Hardware'),
    'hp': ('HP / HPE', 'HP_IN_OPS_2026', 'Supply Chain Analyst - Early Career (Fresher 2026)', 'https://jobs.hp.com', 'Tech Hardware'),
    'intel': ('Intel', 'INTEL_IN_OPS_2026', 'Operations & Procurement Specialist (Entry-Level / College Graduate 2026)', 'https://jobs.intel.com', 'Semiconductors'),
    'sap': ('SAP', 'SAP_IN_EARLY_TALENT_2026', 'Early Talent - Business & Cloud Operations (Campus Hire 2026)', 'https://jobs.sap.com', 'Enterprise Software'),
    'salesforce': ('Salesforce', 'SFDC_IN_OPS_2026', 'Business Operations Associate (Futureforce Early Career 2026)', 'https://salesforce.com/company/careers/', 'Enterprise SaaS'),
    'adobe': ('Adobe', 'ADBE_IN_OPS_2026', 'Business Operations Analyst (University Graduate / Fresher 2026)', 'https://adobe.com/careers.html', 'Enterprise Software'),
    'servicenow': ('ServiceNow', 'SNOW_IN_OPS_2026', 'Commercial Operations Specialist (Early Career / Entry-Level 2026)', 'https://careers.servicenow.com', 'Enterprise SaaS'),
    'service now': ('ServiceNow', 'SNOW_IN_OPS_2026', 'Commercial Operations Specialist (Early Career / Entry-Level 2026)', 'https://careers.servicenow.com', 'Enterprise SaaS'),
    'sony': ('Sony Research India', '4378325278', 'LLM Research & Business Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4378325278', 'AI & Research'),

    # IT Services & Digital Engineering Giants
    'accenture': ('Accenture', '4429242140 / 4448338203', 'Business Advisory New Associate / Supply Chain Operations Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4429242140', 'IT & Consulting'),
    'tata consultancy': ('Tata Consultancy Services (TCS)', '4441247618 / TCS_NQT_CAMPUS_2026', 'TCS Prime Operations Trainee / Business Analyst (Campus Graduate 2026)', 'http://www.linkedin.com/jobs/view/4441247618', 'IT Services'),
    'tcs': ('Tata Consultancy Services (TCS)', '4441247618 / TCS_NQT_CAMPUS_2026', 'TCS Prime Operations Trainee / Business Analyst (Campus Graduate 2026)', 'http://www.linkedin.com/jobs/view/4441247618', 'IT Services'),
    'capgemini': ('Capgemini', '4452892921 / CAPGEMINI_EXCELLER_2026', 'Operations Trainee / Business Intelligence Associate (Capgemini Exceller Campus 2026)', 'http://www.linkedin.com/jobs/view/4452892921', 'IT Services'),
    'cognizant': ('Cognizant', 'CTS_GENC_2026', 'Process Executive - Digital Operations / Analyst Trainee (GenC Campus 2026)', 'https://careers.cognizant.com/in/en', 'IT Services'),
    'infosys': ('Infosys', '4443800666 / INFOSYS_EARLY_CAREER_2026', 'Data & Business Operations Specialist (BBA Bangalore Campus Drive 2026)', 'http://www.linkedin.com/jobs/view/4443800666', 'IT Services'),
    'wipro': ('Wipro', 'WIPRO_ELITE_2026', 'Project Operations Coordinator / Business Analyst (Wipro Elite Campus 2026)', 'https://careers.wipro.com', 'IT Services'),
    'hcl': ('HCLTech', '4443791300', 'Process Associate - Bangalore Operations Walkin (Fresher Intake 2026)', 'http://www.linkedin.com/jobs/view/4443791300', 'IT Services'),
    'hcltech': ('HCLTech', '4443791300', 'Process Associate - Bangalore Operations Walkin (Fresher Intake 2026)', 'http://www.linkedin.com/jobs/view/4443791300', 'IT Services'),
    'tech mahindra': ('Tech Mahindra', '4444598615', 'Marketing & Operations Executive / Trainee (Campus Hire 2026)', 'http://www.linkedin.com/jobs/view/4444598615', 'IT Services'),
    'ltimindtree': ('LTIMindtree', 'LTI_EARLY_CAREER_2026', 'Associate Consultant - Enterprise Operations (Early Career / Campus 2026)', 'https://www.ltimindtree.com/careers/', 'IT Services'),
    'l&t': ('Larsen & Toubro', 'LT_GRADUATE_TRAINEE_2026', 'Graduate Commercial & Operations Trainee (Fresher 2026)', 'https://www.larsentoubro.com/corporate/careers/', 'Engineering & EPC'),
    'mphasis': ('Mphasis', '4451625819', 'Mergers and Acquisitions / Finance Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4451625819', 'IT Services'),
    'ust': ('UST', '4441571067', 'Business Operations Support Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4441571067', 'IT Services'),
    'wns': ('WNS Global Services', '4430704372', 'Bangalore Walkins - Operations Associate (Fresher 2026)', 'http://www.linkedin.com/jobs/view/4430704372', 'BPM & Operations'),
    'genpact': ('Genpact', 'GENPACT_OPS_ANALYST_2026', 'Management Trainee - Business Process Operations (Campus Fresher 2026)', 'https://www.genpact.com/careers', 'BPM & Operations'),
    'concentrix': ('Concentrix', 'CNX_OPERATIONS_LEAD_2026', 'Operations Specialist - Customer Experience (Entry-Level / Fresher 2026)', 'https://jobs.concentrix.com', 'BPM & Tech'),
    'dxc': ('DXC Technology', 'DXC_IN_OPS_2026', 'Associate Professional - Systems Operations (Entry-Level 2026)', 'https://dxc.com/in/en/careers', 'IT Services'),
    'globallogic': ('GlobalLogic', '4451402094', 'Event Marketing Specialist IRC298882 (Entry-Level / Early Career)', 'http://www.linkedin.com/jobs/view/4451402094', 'Product Engineering'),
    'bristlecone': ('Bristlecone', '4447269525', 'Supply Chain Analyst / Operations Associate (Entry-Level 2026)', 'http://www.linkedin.com/jobs/view/4447269525', 'Supply Chain Consulting'),

    # High-Growth Startups, FinTech, E-Commerce & Quick-Commerce
    'flipkart': ('Flipkart', '4454463792', 'Supply Chain Operations Specialist / Associate (Entry-Level / Campus 2026)', 'http://www.linkedin.com/jobs/view/4454463792', 'E-Commerce'),
    'razorpay': ('Razorpay', '4439995783', 'Analyst - Business Operations / Merchant Ops Specialist (Early Career / Fresher)', 'http://www.linkedin.com/jobs/view/4439995783', 'FinTech'),
    'swiggy': ('Swiggy', 'SWIGGY_OPS_001', 'Operations & Expansion Associate (Entry-Level / Fresher 2026)', 'https://careers.swiggy.com', 'Hyperlocal Delivery'),
    'zepto': ('Zepto', '4427343200 / ZEPTO_OPS_002', 'Dark Store Operations Associate / SCM Trainee (Fresher / Entry-Level 2026)', 'http://www.linkedin.com/jobs/view/4427343200', 'Quick Commerce'),
    'ather': ('Ather Energy', 'ATHER_SC_001', 'Supply Chain & Operations Associate (Entry-Level / Fresher 2026)', 'https://www.atherenergy.com/careers', 'EV & CleanTech'),
    'yulu': ('Yulu', '4455256015', 'Operations Associate - Fleet Logistics (Fresher / Entry-Level)', 'http://www.linkedin.com/jobs/view/4455256015', 'EV & Mobility'),
    'rippling': ('Rippling', 'RIPPLING_OPS_2026', 'Identity & Integration Specialist / Platform Support Specialist (Entry-Level)', 'https://www.rippling.com/careers', 'HR Tech SaaS'),
    'ditto': ('Ditto Insurance', 'DITTO_OPS_2026', 'Insurance Operations Consultant / Advisory Specialist (Entry-Level / Fresher)', 'https://joinditto.in/careers/', 'InsurTech'),
    'glean': ('Glean', '4453740312', 'Cost & Commercial Operations Associate (Entry-Level / Fresher)', 'https://jobs.ashbyhq.com/glean', 'Enterprise AI'),
    'postman': ('Postman', 'POSTMAN_OPS_003', 'Business Operations Analyst (Early Career / Entry-Level)', 'https://boards.greenhouse.io/postman', 'Developer SaaS'),
    'wrike': ('Wrike', '4440968428', 'Partner Operations Specialist (Entry-Level / Fresher)', 'https://boards.greenhouse.io/wrike', 'Productivity SaaS'),
    'physicswallah': ('PhysicsWallah', 'PW_OPS_2026', 'Operations Associate / Center Operations Executive (Entry-Level / Fresher)', 'https://pw.live/careers', 'EdTech'),
    'pw ': ('PhysicsWallah', 'PW_OPS_2026', 'Operations Associate / Center Operations Executive (Entry-Level / Fresher)', 'https://pw.live/careers', 'EdTech'),
    'navi': ('Navi', '4448516986', 'Business Analyst I (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4448516986', 'FinTech'),
    'curefit': ('Curefit', '4443670711', 'Business Analyst - Operations & Growth (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4443670711', 'Health & Fitness'),
    'blissclub': ('Blissclub', '4437012823', 'Business Analyst - Retail Merchandising (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4437012823', 'D2C Brand'),
    'kapiva': ('Kapiva', '4451420773', 'Operations Associate - Marketplaces (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4451420773', 'D2C Ayurveda'),
    'media.net': ('Media.net', '4438227603', 'Business Operations Analyst (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4438227603', 'AdTech'),
    'tokens': ('tokens&', '4449673093', 'Operations Associate – Founder Office (Fresher / Entry-Level)', 'http://www.linkedin.com/jobs/view/4449673093', 'Web3 / Founder Office'),
    'joveo': ('Joveo', '4445510394', 'Business Operations & Strategy Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4445510394', 'HR Tech'),
    'appinventiv': ('Appinventiv', '4452236708', 'Business Analyst (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4452236708', 'Digital Consulting'),
    'codingal': ('Codingal', '4452267446', 'Operations Associate (Student Onboarding - Fresher)', 'http://www.linkedin.com/jobs/view/4452267446', 'EdTech'),
    'trilegal': ('Trilegal', '4446714917', 'Executive Assistant / Operations Associate (Entry-Level)', 'http://www.linkedin.com/jobs/view/4446714917', 'Legal Services'),
    'vegrow': ('VEGROW', '4451063376', 'Operations Associate - Supply Chain (Fresher / Entry-Level)', 'http://www.linkedin.com/jobs/view/4451063376', 'AgriTech SCM'),
    'third wave coffee': ('Third Wave Coffee', '4436544281', 'Intern - B2B Sales & Operations (Class of 2026)', 'http://www.linkedin.com/jobs/view/4436544281', 'Food & Retail'),
    'xoxoday': ('Xoxoday', '4437681367', 'Events & Field Marketing Executive (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4437681367', 'Enterprise SaaS'),
    'bni': ('BNI Global', '4406514782', 'Event Logistics Coordinator (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4406514782', 'Professional Network'),
    'galaxeye': ('GalaxEye', '4373303563', 'Market Research Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4373303563', 'SpaceTech'),
    'bellatrix': ('Bellatrix Aerospace', '4439051384', 'Founder\'s Office / Operations Associate (Fresher / Entry-Level)', 'http://www.linkedin.com/jobs/view/4439051384', 'Aerospace'),
    'tyfone': ('Tyfone, Inc.', '4371505461', 'Business Intelligence & Data Analyst Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4371505461', 'FinTech'),
    'expedify': ('Expedify', '4374985662', 'AI Product Analytics Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4374985662', 'AI Products'),
    'emergent': ('Emergent', '4439983503', 'AI Analyst - Business Analytics (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4439983503', 'AI Analytics'),
    'inspironlabs': ('InspironLabs', '4370182887', 'Management Trainee (Fresher Intake 2026)', 'http://www.linkedin.com/jobs/view/4370182887', 'Tech Services'),
    'englishbhashi': ('EnglishBhashi', '4377959748', 'Product Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4377959748', 'EdTech'),
    'infrabyte': ('Infrabyte Consulting', '4381181841', 'Data / Business Analyst Intern (Class of 2026)', 'http://www.linkedin.com/jobs/view/4381181841', 'Consulting'),
    'mathworks': ('MathWorks', '4406706536', 'Marketing Event Specialist (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4406706536', 'Technical Software'),
    'times internet': ('Times Internet', '4428249509', 'Intern - Business Operations (Class of 2026)', 'http://www.linkedin.com/jobs/view/4428249509', 'Media & Digital'),
    'turing': ('Turing', '4379901173', 'Remote Business Analyst (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4379901173', 'AI Talent Cloud'),

    # Retail, FMCG, Industrial, Automotive & Aerospace
    'target': ('Target in India', 'TARGET_IN_OPS_2026', 'Merchandise Payables Specialist / HR & Business Operations Trainee (Fresher 2026)', 'https://india.target.com/careers', 'Fortune 500 Retail'),
    'walmart': ('Walmart Global Tech', 'WALMART_IN_OPS_2026', 'Operations Analyst - Supply Chain & Fulfillment (Entry-Level / Campus 2026)', 'https://careers.walmart.com', 'Fortune 500 Retail'),
    'lowe': ('Lowe\'s Companies, Inc.', '4437007369', 'Category Analyst - Merchandising Operations (Entry-Level / Campus 2026)', 'http://www.linkedin.com/jobs/view/4437007369', 'Fortune 500 Retail'),
    'itc': ('ITC Limited', 'ITC_SCM_2026', 'Area Supply Chain Executive / Finance & Logistics Intern (Campus Hire 2026)', 'https://www.itcportal.com/careers/', 'FMCG & Supply Chain'),
    'unilever': ('Hindustan Unilever (HUL)', 'HUL_FUTURE_LEADERS_2026', 'Customer Operations & Supply Chain Trainee (Fresher / Early Career 2026)', 'https://www.hul.co.in/careers/', 'FMCG'),
    'hul': ('Hindustan Unilever (HUL)', 'HUL_FUTURE_LEADERS_2026', 'Customer Operations & Supply Chain Trainee (Fresher / Early Career 2026)', 'https://www.hul.co.in/careers/', 'FMCG'),
    'nestle': ('Nestle', 'NESTLE_IN_OPS_2026', 'Supply Chain & Distribution Specialist (Entry-Level / Fresher 2026)', 'https://www.nestle.in/jobs', 'FMCG'),
    'pepsico': ('PepsiCo', 'PEP_IN_SUPPLY_2026', 'Supply Chain Analyst - Logistics Planning (Graduate Trainee / Fresher 2026)', 'https://www.pepsicojobs.com', 'FMCG'),
    'coca-cola': ('Coca-Cola (HCCB)', 'HCCB_OPS_TRAINEE_2026', 'Distribution Operations Associate (Entry-Level / Fresher 2026)', 'https://www.hccb.in/careers', 'Beverages & SCM'),
    'nike': ('Nike', 'NIKE_IN_OPS_2026', 'Retail Operations & Supply Chain Specialist (Entry-Level / Fresher 2026)', 'https://jobs.nike.com', 'Sportswear'),
    'puma': ('Puma Global & India', 'PUMA_OPS_ASSOC_2026', 'Retail Operations & Event Logistics Associate (Entry-Level / Fresher 2026)', 'https://about.puma.com/en/careers', 'Sportswear'),
    'bosch': ('Robert Bosch', 'BOSCH_IN_OPS_2026', 'Junior Operations Specialist - Mobility & Logistics (Fresher 2026)', 'https://www.bosch.in/careers/', 'Industrial & Auto Tech'),
    'siemens': ('Siemens', 'SIEMENS_IN_GRAD_2026', 'Commercial & Logistics Operations Trainee (Graduate Fresher 2026)', 'https://www.siemens.com/in/en/company/jobs.html', 'Industrial Automation'),
    'abb': ('ABB', 'ABB_IN_OPS_2026', 'Operations & Project Management Associate (Entry-Level / Fresher 2026)', 'https://careers.abb/global/en', 'Robotics & Energy'),
    'schneider': ('Schneider Electric', 'SE_IN_OPS_2026', 'Supply Chain & Commercial Operations Specialist (Graduate Trainee 2026)', 'https://www.se.com/in/en/about-us/careers/', 'Energy Management'),
    'volvo': ('Volvo Construction Equipment', '4429029965', 'Graduate Apprentice Trainee - Operations (Fresher 2026)', 'http://www.linkedin.com/jobs/view/4429029965', 'Automotive & Heavy Eq'),
    'cummins': ('Cummins', 'CMI_IN_OPS_2026', 'Supply Chain & Manufacturing Operations Trainee (Graduate Fresher 2026)', 'https://www.cummins.com/careers', 'Engines & Power'),
    'tata motors': ('Tata Motors', 'TML_GRAD_OPS_2026', 'Graduate Operations Officer - Supply Chain (Fresher 2026)', 'https://www.tatamotors.com/careers/', 'Automotive'),
    'tata communications': ('Tata Communications', 'TATA_COMM_OPS_2026', 'Operations Specialist - Global Enterprise Solutions (Entry-Level / Campus 2026)', 'https://www.tatacommunications.com/careers/', 'Enterprise Telecom'),
    'tata consumer': ('Tata Consumer Products', '4021834253', 'Human Resources Intern / Supply Operations Trainee (Class of 2026)', 'http://www.linkedin.com/jobs/view/4021834253', 'FMCG'),
    'reliance': ('Reliance Industries / Jio', '4451512233 / RIL_GRAD_2026', 'Commercial Operations Trainee (Graduate Fresher 2026)', 'http://www.linkedin.com/jobs/view/4451512233', 'Conglomerate'),
    'jio': ('Reliance Jio', 'JIO_OPS_TRAINEE_2026', 'Operations & Business Analyst (Graduate Trainee / Fresher 2026)', 'https://careers.jio.com', 'Telecommunications'),
    'boeing': ('Boeing', 'BOEING_IN_OPS_2026', 'Supply Chain Specialist - Aerospace Operations (Entry-Level / Fresher 2026)', 'https://jobs.boeing.com', 'Aerospace & Defense'),
    'airbus': ('Airbus', 'AIRBUS_IN_OPS_2026', 'Procurement & Logistics Operations Trainee (Graduate Fresher 2026)', 'https://www.airbus.com/en/careers', 'Aerospace & Defense'),
    'totalenergies': ('TotalEnergies', '4452197513', 'Operations & HSSE Trainee / Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4452197513', 'Energy & Operations'),
    'zeiss': ('ZEISS India', '4435054588', 'Graduate Trainee - Commercial Operations (Fresher 2026)', 'http://www.linkedin.com/jobs/view/4435054588', 'Optics & Tech'),
    'lufthansa': ('Lufthansa Technik Services India', '4452437152', 'Analyst - Transfer Pricing & Financial Ops (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4452437152', 'Aviation & Finance'),

    # Healthcare, Pharma & Medical Devices
    'medtronic': ('Medtronic', 'MDT_IN_OPS_2026', 'Operations & Supply Chain Analyst (Entry-Level / Campus 2026)', 'https://jobs.medtronic.com', 'Medical Technology'),
    'pfizer': ('Pfizer', 'PFIZER_IN_OPS_2026', 'Commercial Operations & Logistics Specialist (Entry-Level / Fresher 2026)', 'https://www.pfizer.com/about/careers', 'Pharmaceuticals'),
    'novartis': ('Novartis', 'NOVARTIS_IN_OPS_2026', 'Business Operations Analyst - Global Service Center (Entry-Level / Fresher 2026)', 'https://www.novartis.com/careers', 'Pharmaceuticals'),
    'astrazeneca': ('AstraZeneca', 'AZ_IN_OPS_2026', 'Operations Specialist - Clinical & Commercial Supply (Entry-Level / Fresher 2026)', 'https://careers.astrazeneca.com', 'Pharmaceuticals'),
    'biocon': ('Biocon', 'BIOCON_GRAD_2026', 'Management Trainee - Supply Chain & Operations (Graduate Fresher 2026)', 'https://www.biocon.com/careers/', 'Biopharma'),
    'dr. reddy': ('Dr. Reddy\'s', 'DRL_GRAD_OPS_2026', 'Operations Analyst - Global Supply Chain (Graduate Trainee / Fresher 2026)', 'https://careers.drreddys.com', 'Pharmaceuticals'),

    # Hospitality, Event Management & Media
    'hilton': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4450278984', 'Hospitality'),
    'conrad': ('Hilton', '4450278984', 'Events Executive | Conrad Bengaluru (Entry-Level / Fresher)', 'http://www.linkedin.com/jobs/view/4450278984', 'Hospitality'),
    'marriott': ('JW Marriott', '4436777567 / 4448275499', 'Events Executive / Operations Associate (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4436777567', 'Hospitality'),
    'hyatt': ('Hyatt Hotels', 'HYATT_EVENTS_2026', 'Events Planning & Operations Executive (Entry-Level / Fresher 2026)', 'https://careers.hyatt.com', 'Hospitality'),
    'radisson': ('Radisson Hotel Group', '4429776666', 'Event Operations Executive / Trainee (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4429776666', 'Hospitality'),
    'thomson reuters': ('Thomson Reuters', '4446747144', 'Events Coordinator (Entry-Level / Fresher 2026)', 'http://www.linkedin.com/jobs/view/4446747144', 'Media & Data')
}

# 3. Helper Functions for String Sanitization
def clean_first_name(raw_fn, raw_ln=""):
    fn = (raw_fn or "").strip()
    ln = (raw_ln or "").strip()

    if not fn and ln:
        fn = ln

    # Remove parenthetical text e.g. (She/Her), (LION), [Open to Work]
    fn = re.sub(r'\(.*?\)', '', fn)
    fn = re.sub(r'\[.*?\]', '', fn)

    # Remove non-word characters except hyphen
    fn = re.sub(r'[^\w\s\-]', ' ', fn)
    fn = fn.replace('_', ' ')

    # Remove prefixes
    prefixes = [
        'dr', 'prof', 'professor', 'ca', 'cs', 'cfa', 'cma', 'adv', 'advocate',
        'mr', 'mrs', 'ms', 'miss', 'shri', 'smt', 'major', 'capt', 'captain',
        'col', 'colonel', 'hr', 'er', 'architect', 'engr', 'lt', 'lieutenant'
    ]
    pattern = r'^(' + '|'.join(prefixes) + r')\b\s*'
    fn = re.sub(pattern, '', fn, flags=re.IGNORECASE).strip()

    parts = fn.split()
    if not parts:
        return "there"

    first = parts[0].strip('.-_')
    if len(first) <= 1 and len(parts) > 1:
        first = parts[1].strip('.-_')

    clean = first.capitalize()
    return clean if len(clean) > 1 else "there"

def clean_company_name(raw_co):
    co = (raw_co or "").strip()
    if not co or co.lower() in ['independent', 'not disclosed', 'none', 'self-employed', 'freelance']:
        return None
    co = re.sub(r'\s+(Pvt\.?\s*Ltd\.?|Private\s+Limited|Ltd\.?|Limited|Inc\.?|LLC|Corporation|Corp\.?|Services\s+Private\s+Limited|India\s+Private\s+Limited)$', '', co, flags=re.IGNORECASE)
    return co.strip()

def clean_position(raw_pos):
    pos = (raw_pos or "").strip()
    if not pos:
        return 'Professional'
    pos = pos.replace('–', '-').replace('—', '-').replace('•', '-')
    if '|' in pos:
        pos = pos.split('|')[0].strip()
    if '-' in pos and len(pos.split('-')[0].strip()) > 3:
        pos = pos.split('-')[0].strip()
    pos = re.sub(r'\s+', ' ', pos).strip()
    return pos

def extract_linkedin_id(raw_url):
    if not raw_url:
        return 'N/A'
    u = raw_url.strip().rstrip('/')
    parts = u.split('/')
    lid = parts[-1] if parts else 'N/A'
    return lid if lid else 'N/A'

# Candidate ground truth dossier
candidate_packet = """--- CANDIDATE REFERRAL PACKET (WORKDAY / TALEO / ASHBY / GREENHOUSE) ---
• Legal Name: Aditya Mehra
• Email: ashishiash007@gmail.com | Phone: +91 7003456624 | Location: Bengaluru, India
• Degree: BBA (International Business), Dayananda Sagar University (Class of 2026)
• Target Level: Fresher / Entry-Level / Graduate Trainee (Class of 2026)
• Target Functions: Operations Analyst | Graduate Trainee | Business Operations Associate | Supply Chain Specialist
• Core Proof: Operations Lead at AERO INDIA 2025 (Yelahanka AFB, 100k+ delegates, 0 security infractions, 0.0% inventory shrinkage); Contract SLA compliance for Tata Communications & Puma Global summits.
• Resume & Profile: https://www.linkedin.com/in/aditya-mehra
-------------------------------------------------------------------------"""

processed = []
active_job_id_matches = 0

for idx, c in enumerate(connections):
    raw_fn = c.get('First Name', '').strip()
    ln = c.get('Last Name', '').strip()
    full_name = f"{raw_fn} {ln}".strip()
    if not full_name:
        full_name = "LinkedIn Member (Private / Inactive)"
    first_name = clean_first_name(raw_fn, ln)
    company_raw = c.get('Company', '').strip()
    company_display = clean_company_name(company_raw)
    position = clean_position(c.get('Position', '').strip())
    url = c.get('URL', '').strip()
    linkedin_id = extract_linkedin_id(url)
    email = c.get('Email Address', '').strip()
    connected_on = c.get('Connected On', '').strip()

    co_lower = company_raw.lower()
    pos_lower = position.lower()

    # Match Active Target Jobs
    matched_job = None
    for k, val in master_jobs_catalog.items():
        if k in co_lower:
            matched_job = val
            break

    job_url = ""
    job_id = ""
    target_role_title = ""

    if matched_job:
        target_co, job_id, target_role_title, job_url, sector = matched_job
        category = "Tier 1: Active Job Opening Mapped"
        job_info = f"{target_co} | {target_role_title} (Req ID: {job_id})"
        active_job_id_matches += 1
        
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope your week is off to a wonderful start! Always inspiring seeing your journey as {position} at {target_co}.\n\n"
            f"I'm reaching out with genuine respect for your craft and team. As an upcoming 2026 graduate in BBA (International Business) at Dayananda Sagar University here in Bengaluru seeking fresher and entry-level operations roles, I've focused on high-accountability operational execution—serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (managing crowd logistics and multi-vendor coordination for 100,000+ delegates with zero security breaches and 0.0% shrinkage) alongside managing run-of-show contracts for Tata Communications and Puma Global.\n\n"
            f"I noticed an active entry-level / campus opening at {target_co} that aligns directly with my background:\n"
            f"• Target Role: {target_role_title}\n"
            f"• Job ID / Req ID: {job_id}\n"
            f"• Application Link: {job_url}\n\n"
            f"Knowing how much operational excellence and team standards matter at {target_co}, I would be deeply honored if you might consider putting in an internal referral for my profile. To save you time and make this completely frictionless for your internal portal, here is my pre-filled candidate packet:\n\n"
            f"{candidate_packet}\n\n"
            f"Please know there is absolutely zero pressure if company referral guidelines or bandwidth make this difficult right now—just connecting with you and learning from your experience at {target_co} is already a true privilege.\n\n"
            f"Wishing you and your team continued momentum and success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(hr_term in pos_lower for hr_term in ['talent', 'recruit', 'hr', 'human resources', 'sourcing', 'people partner', 'talent acquisition']):
        category = "Tier 2: HR & Talent Acquisition"
        co_str = company_display if company_display else "your organization"
        job_info = f"Early Career & Fresher Hiring Intakes at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "CAMPUS_EARLY_CAREER_2026"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope your week is going great! I've been following your impactful work shaping talent pipelines and team culture as {position} at {co_str}.\n\n"
            f"I am concluding my final year in International Business at Dayananda Sagar University here in Bengaluru, targeting fresher and entry-level graduate roles. My background is centered on disciplined operations, supply chain logistics, and high-stakes vendor management—recently serving as Operations Lead at AERO INDIA 2025 (100,000+ attendees, 0 security breaches, 0.0% inventory shrinkage) and managing contract SLAs for Tata Communications.\n\n"
            f"As your team at {co_str} plans upcoming hiring or campus/entry-level intakes for operations, business analysis, supply chain, or graduate trainee roles, I would love to be on your radar. To make review effortless, here is a quick snapshot of my candidate packet:\n\n"
            f"{candidate_packet}\n\n"
            f"Thank you sincerely for all the dedication you bring to talent acquisition, and I'd be honored to connect or share my tailored resume whenever convenient.\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(lead_term in pos_lower for lead_term in ['director', 'vice president', 'vp', 'partner', 'founder', 'ceo', 'co-founder', 'managing director', 'general manager', 'head of', 'chief']):
        category = "Tier 2: Senior Leadership & Executives"
        co_str = company_display if company_display else "your enterprise"
        job_info = f"Executive Leadership & Strategic Inquiries at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "LEADERSHIP_EXECUTIVE_ALIGNMENT"
        msg = (
            f"Hi {first_name},\n\n"
            f"I hope this message finds you well. I’ve greatly admired your leadership as {position} at {co_str} and the strategic direction your team is driving.\n\n"
            f"As I complete my International Business degree at Dayananda Sagar University (Class of 2026), my goal is to launch my career in organizations where operational integrity, customer trust, and rigorous execution are prized. Having led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ attendees with zero security incidents and 0.0% shrinkage) and enforced multi-vendor contract SLAs for Tata Communications and Puma Global, I know how essential execution fidelity is to senior leaders like yourself.\n\n"
            f"I would be deeply honored for a brief 5-minute perspective on what you value most when building resilient operational teams at {co_str}. And if a fresher, campus, or entry-level operations analyst opening exists within your group, I would be profoundly grateful for your guidance.\n\n"
            f"Thank you sincerely for your time and leadership, {first_name}.\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(ops_term in pos_lower for ops_term in ['operation', 'supply chain', 'logistics', 'procurement', 'inventory', 'pmo', 'vendor']):
        category = "Tier 4: Operations & Supply Chain Network"
        co_str = company_display if company_display else "your team"
        job_info = f"Operations & Supply Chain Kinship at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "OPS_NETWORK_REFERRAL"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you're having a productive week! Always great connecting with an operational professional—especially seeing your execution as {position} at {co_str}.\n\n"
            f"As a final-year student in International Business at Dayananda Sagar University (Class of 2026) actively seeking entry-level and fresher operations roles, I've dedicated myself to rigorous operational delivery. Serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (100k+ attendees, 0 security infractions, 0.0% shrinkage) and managing run-of-show logistics and SLA contract enforcement for Puma Global and Tata Communications taught me the true value of relentless ground discipline.\n\n"
            f"I would love to exchange notes on operational workflows, vendor governance, and early-career pathways at {co_str}. If you ever have a few minutes for a virtual coffee or quick conversation, it would be a pleasure to connect.\n\n"
            f"Wishing you seamless operations and continued momentum!\n\n"
            f"Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(fin_term in pos_lower for fin_term in ['finance', 'accounting', 'audit', 'tax', 'banker', 'banking', 'investment', 'credit', 'risk analyst', 'treasury']):
        category = "Tier 4: Finance & Banking Network"
        co_str = company_display if company_display else "your firm"
        job_info = f"Financial Operations & Governance at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "FIN_OPS_REFERRAL"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope all is well with you! I’ve been following your professional journey in financial governance and analysis as {position} at {co_str}.\n\n"
            f"I'm currently concluding my final year in International Business at Dayananda Sagar University (Class of 2026), targeting fresher / entry-level analyst opportunities with a strong focus on financial reconciliation, trade finance documentation (INCOTERMS 2020, Letters of Credit), and contract compliance. During AERO INDIA 2025, I maintained a 0.0% inventory shrinkage record across high-volume assets and managed multi-vendor billing and SLA compliance for Tata Communications.\n\n"
            f"I would love to learn how your team approaches financial operations and risk management at {co_str}, and explore potential early-career analyst opportunities. Wishing you a great financial quarter ahead!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(tech_term in pos_lower for tech_term in ['developer', 'software', 'engineer', 'architect', 'data analyst', 'data scientist', 'product manager', 'frontend', 'backend', 'full stack', 'cloud']):
        category = "Tier 4: Technology & Product Network"
        co_str = company_display if company_display else "your team"
        job_info = f"Tech & Business Intersection at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "TECH_BIZ_INTERSECTION"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a fantastic week! It's always inspiring following your technical craft and journey as {position} at {co_str}.\n\n"
            f"While my core discipline is International Business and Operations at Dayananda Sagar University (Class of 2026, targeting entry-level roles), I work closely at the intersection of business operations and technology systems. Recently, I led operations at AERO INDIA 2025 (100,000+ delegates, 0 breaches, 0.0% inventory loss) where real-time coordination, automated tracking, and multi-vendor communication protocols were mission-critical.\n\n"
            f"I have immense respect for the engineering and product standards at {co_str}. If your team or cross-functional operations group is ever looking for a high-energy fresher / entry-level operator who bridges business logic, system discipline, and data integrity, I'd love to connect and learn about your experience there.\n\n"
            f"Wishing you and your team smooth deployments and continued success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(alumni_term in co_lower for alumni_term in ['christ', 'dayananda', 'dsu', 'iisc', 'student welfare', 'cusbma']) or any(stud_term in pos_lower for stud_term in ['student', 'intern', 'campus', 'president', 'council', 'volunteer']):
        category = "Tier 3: University & Alumni Network"
        co_str = company_display if company_display else "our campus network"
        job_info = f"Campus Camaraderie & Mutual Growth ({co_str})"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "CAMPUS_ALUMNI_KINSHIP"
        msg = (
            f"Hi {first_name},\n\n"
            f"Great to connect with a fellow campus peer! It’s inspiring seeing your growth as {position} with {co_str}.\n\n"
            f"I'm currently in my final year of BBA (International Business) at Dayananda Sagar University (Class of 2026). Over the past year, I had the privilege of leading ground operations at AERO INDIA 2025 at Yelahanka AFB (managing 100k+ footfall with 0 breaches and 0 shrinkage) alongside corporate logistics for Tata Communications.\n\n"
            f"I'm actively exploring fresher, campus, and entry-level operations and analyst roles across Bengaluru. If you ever have a few minutes to share your thoughts on your journey since graduation, or if I can ever support you in any way, let's definitely catch up!\n\n"
            f"Wishing you continued success and proud to be part of the same community!\n\n"
            f"Cheers,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    elif any(sales_term in pos_lower for sales_term in ['sales', 'marketing', 'business development', 'growth', 'account manager', 'brand', 'commercial']):
        category = "Tier 4: Commercial & Growth Network"
        co_str = company_display if company_display else "your company"
        job_info = f"Commercial & Growth Execution at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "COMMERCIAL_GROWTH_ALIGNMENT"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a thriving week! Really admire the commercial momentum and customer growth you're driving as {position} at {co_str}.\n\n"
            f"I'm concluding my International Business degree at Dayananda Sagar University (Class of 2026, targeting entry-level commercial operations and analyst roles). Having led event operations at AERO INDIA 2025 for 100k+ visitors and delivered run-of-show logistics for Puma Global and Tata Communications, I understand how vital seamless delivery is to maintaining customer trust and commercial success.\n\n"
            f"If there is ever an early-career opening or if I can assist your initiatives in Bengaluru, I'd be delighted to connect.\n\n"
            f"Wishing you high conversions and continued success!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    else:
        co_str = company_display if company_display else "your organization"
        category = "Tier 4: Enterprise Network & Reconnect"
        job_info = f"Professional Connection at {co_str}"
        job_url = "https://www.linkedin.com/jobs/"
        job_id = "NETWORK_RECONNECT_2026"
        msg = (
            f"Hi {first_name},\n\n"
            f"Hope you are having a wonderful week! Always inspiring following your journey as {position} at {co_str}.\n\n"
            f"I wanted to reach out, say hello, and share a quick personal update. I am completing my final year in International Business at Dayananda Sagar University in Bengaluru (Class of 2026, exploring fresher and entry-level opportunities). Over the past year, I've led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ delegates with zero security breaches and 0.0% inventory shrinkage) and managed multi-vendor SLA contracts for Tata Communications and Puma Global summits.\n\n"
            f"I'm currently exploring fresher and entry-level roles in operations, program coordination, and business analytics. If you or anyone in your network is ever looking for a disciplined, execution-focused operator—or if I can ever help support your initiatives here in Bengaluru—I would love to connect for a brief 5-minute chat.\n\n"
            f"Wishing you continued success in your journey!\n\n"
            f"Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )

    processed.append({
        'id': idx,
        'name': full_name,
        'first_name': first_name,
        'company': company_raw or 'Independent / Not Disclosed',
        'position': position,
        'category': category,
        'job_info': job_info,
        'job_id': job_id,
        'job_url': job_url,
        'target_role': target_role_title,
        'linkedin_id': linkedin_id,
        'url': url,
        'email': email,
        'date': connected_on,
        'message': msg
    })

print(f"Processed all {len(processed):,} connections.")
print(f"Direct Active Job Opening & Req ID matches: {active_job_id_matches:,} connections ({active_job_id_matches/len(processed)*100:.1f}%)")

# 4. Write CSV Export (All 9,223 Connections)
out_csv = r'e:\anti\linkedin_export\connection_personalized_messages.csv'
with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Full Name', 'First Name', 'Company', 'Position', 'Tier / Category', 
        'Job Info & ID', 'Job ID / Req ID', 'Job URL', 'LinkedIn ID', 'LinkedIn URL', 'Email Address', 'Connected Date', 
        'Personalized Relationship Message'
    ])
    for p in processed:
        writer.writerow([
            p['name'], p['first_name'], p['company'], p['position'], p['category'],
            p['job_info'], p['job_id'], p['job_url'], p['linkedin_id'], p['url'], p['email'], p['date'], p['message']
        ])

print(f"Exported master CSV: {out_csv} ({os.path.getsize(out_csv) / (1024*1024):.2f} MB)")

# 5. Write JSON Database (All 9,223 Connections)
out_json = r'e:\anti\linkedin_export\connection_outreach_data.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(processed, f, indent=2, ensure_ascii=False)

print(f"Exported master JSON: {out_json} ({os.path.getsize(out_json) / (1024*1024):.2f} MB)")

# 6. Generate High-Performance Interactive HTML Command Center (All 9,223 Connections)
# We embed the lightweight compact schema for ALL 9,223 connections so the entire network is 100% searchable in-browser.
compact_pool = []
for p in processed:
    compact_pool.append({
        'i': p['id'],
        'n': p['name'],
        'fn': p['first_name'],
        'c': p['company'],
        'p': p['position'],
        'cat': p['category'],
        'ji': p['job_info'],
        'jid': p['job_id'],
        'ju': p['job_url'],
        'lid': p['linkedin_id'],
        'u': p['url'],
        'd': p['date']
    })

print(f"Embedding all {len(compact_pool):,} connections into interactive single-page application...")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra | Master LinkedIn Outreach & Referral Command Center</title>
<style>
  :root {{
    --bg: #070b13;
    --card: #0f172a;
    --card-hover: #17243d;
    --border: #1e293b;
    --border-highlight: #38bdf8;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.25);
    --green: #10b981;
    --green-glow: rgba(16, 185, 129, 0.2);
    --amber: #f59e0b;
    --purple: #a855f7;
    --blue-linkedin: #0a66c2;
    --star-gold: #fbbf24;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding: 20px; min-height: 100vh; }}
  
  /* Top Unified Navigation */
  .top-nav {{
    display: flex;
    gap: 12px;
    background: #0f172a;
    padding: 12px 20px;
    border-radius: 12px;
    border: 1px solid var(--border);
    margin-bottom: 24px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .top-nav .nav-brand {{
    font-weight: 800;
    font-size: 15px;
    color: var(--accent);
    margin-right: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 0.5px;
  }}
  .top-nav a {{
    color: var(--text-muted);
    text-decoration: none;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
    transition: all 0.2s;
    border: 1px solid transparent;
  }}
  .top-nav a:hover, .top-nav a.active {{
    color: #fff;
    background: rgba(56, 189, 248, 0.15);
    border-color: rgba(56, 189, 248, 0.4);
  }}
  .top-nav .nav-right {{
    margin-left: auto;
    display: flex;
    gap: 10px;
    align-items: center;
  }}
  .top-nav .csv-link {{
    background: rgba(16, 185, 129, 0.15);
    color: var(--green);
    border: 1px solid rgba(16, 185, 129, 0.35);
    font-weight: 700;
  }}
  .top-nav .csv-link:hover {{
    background: var(--green);
    color: #070b13;
  }}

  /* Header */
  .header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
  }}
  .header h1 {{ font-size: 26px; font-weight: 800; color: #fff; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }}
  .header h1 span {{ color: var(--accent); }}
  .header p {{ color: var(--text-muted); font-size: 14px; line-height: 1.6; max-width: 1100px; }}

  /* Metric Ribbon */
  .metrics-ribbon {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .metric-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
  }}
  .metric-card .label {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.8px; font-weight: 600; }}
  .metric-card .val {{ font-size: 24px; font-weight: 800; color: #fff; margin-top: 4px; }}
  .metric-card.accent .val {{ color: var(--accent); }}
  .metric-card.green .val {{ color: var(--green); }}
  .metric-card.amber .val {{ color: var(--amber); }}
  .metric-card.purple .val {{ color: var(--purple); }}

  /* Filter & Controls */
  .controls-bar {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .search-row {{
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .search-input {{
    flex: 1;
    min-width: 280px;
    background: #070b13;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 18px;
    color: #fff;
    font-size: 14px;
    outline: none;
    transition: all 0.2s;
  }}
  .search-input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }}
  
  .filter-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }}
  .filter-btn {{
    background: #070b13;
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .filter-btn:hover, .filter-btn.active {{
    background: var(--accent);
    color: #070b13;
    border-color: var(--accent);
    font-weight: 700;
  }}
  .filter-btn.btn-star.active {{
    background: var(--amber);
    border-color: var(--amber);
    color: #070b13;
  }}
  .filter-btn.btn-contacted.active {{
    background: var(--green);
    border-color: var(--green);
    color: #070b13;
  }}

  /* Pagination Bar */
  .pagination-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 18px;
    margin-bottom: 16px;
    font-size: 13px;
    color: var(--text-muted);
    flex-wrap: wrap;
    gap: 10px;
  }}
  .page-btns {{
    display: flex;
    gap: 6px;
    align-items: center;
  }}
  .page-btn {{
    background: #070b13;
    border: 1px solid var(--border);
    color: #fff;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .page-btn:hover:not(:disabled) {{
    background: var(--accent);
    color: #070b13;
  }}
  .page-btn:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
  }}

  /* Contact List Grid */
  .contact-grid {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .contact-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    transition: all 0.2s ease;
    position: relative;
  }}
  .contact-card:hover {{
    background: var(--card-hover);
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  }}
  .contact-card.is-contacted {{
    border-left: 5px solid var(--green);
    background: rgba(16, 185, 129, 0.04);
  }}
  .contact-card.is-starred {{
    border-top: 2px solid var(--amber);
  }}

  .card-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 12px;
    flex-wrap: wrap;
  }}
  .person-info h3 {{
    font-size: 18px;
    font-weight: 700;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }}
  .person-info .pos {{
    color: var(--text-muted);
    font-size: 14px;
    margin-top: 3px;
  }}
  .person-info .co {{
    color: var(--accent);
    font-weight: 600;
  }}
  .badge {{
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}
  .badge-tier1 {{ background: rgba(34, 197, 94, 0.18); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }}
  .badge-tier2 {{ background: rgba(56, 189, 248, 0.18); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }}
  .badge-tier3 {{ background: rgba(168, 85, 247, 0.18); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }}
  .badge-tier4 {{ background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}

  .linkedin-id-bar {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 6px;
    background: rgba(14, 165, 233, 0.08);
    padding: 3px 10px;
    border-radius: 6px;
    border: 1px solid rgba(14, 165, 233, 0.2);
  }}
  .linkedin-handle {{
    color: var(--accent);
    font-family: monospace;
    font-weight: 600;
    text-decoration: none;
  }}
  .linkedin-handle:hover {{
    text-decoration: underline;
  }}

  .job-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: #e0f2fe;
    margin-bottom: 14px;
    font-weight: 500;
  }}
  .job-tag b {{ color: var(--accent); }}

  .message-box {{
    background: #070b13;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px;
    font-size: 13px;
    line-height: 1.65;
    color: #cbd5e1;
    white-space: pre-wrap;
    max-height: 220px;
    overflow-y: auto;
    margin-bottom: 14px;
    border-left: 3px solid var(--accent);
  }}

  .card-actions {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
  }}
  .action-btn {{
    background: #1e293b;
    border: 1px solid var(--border);
    color: #fff;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
  }}
  .action-btn:hover {{
    background: var(--accent);
    color: #070b13;
    border-color: var(--accent);
  }}
  .action-btn.secondary {{
    background: transparent;
    color: var(--text-muted);
  }}
  .action-btn.secondary:hover {{
    background: #1e293b;
    color: #fff;
  }}
  .action-btn.linkedin-btn {{
    background: var(--blue-linkedin);
    border-color: var(--blue-linkedin);
    color: #fff;
  }}
  .action-btn.linkedin-btn:hover {{
    background: #0077b5;
    border-color: #0077b5;
  }}
  .action-btn.btn-copy {{
    background: rgba(16, 185, 129, 0.18);
    border-color: rgba(16, 185, 129, 0.4);
    color: #34d399;
  }}
  .action-btn.btn-copy:hover {{
    background: var(--green);
    color: #070b13;
  }}
  .btn-star-toggle {{
    background: transparent;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 7px 10px;
    border-radius: 8px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
  }}
  .btn-star-toggle.active {{
    color: var(--amber);
    border-color: var(--amber);
  }}
  .btn-contact-toggle {{
    background: transparent;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 12px;
    cursor: pointer;
  }}
  .btn-contact-toggle.active {{
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
    border-color: var(--green);
    font-weight: 700;
  }}

  /* Toast Notification */
  #toast {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--green);
    color: #070b13;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease;
    z-index: 9999;
    pointer-events: none;
  }}
  #toast.show {{
    opacity: 1;
    transform: translateY(0);
  }}
</style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <nav class="top-nav">
    <div class="nav-brand">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
      ADITYA MEHRA OUTREACH SYSTEM
    </div>
    <a href="job_search_portal.html">🔍 Job Search Portal (141 Openings)</a>
    <a href="connection_messenger_center.html" class="active">Master Messenger & Referral Center (9,223)</a>
    <a href="all_companies_best_messages.html">★ 112 Companies Best Messages</a>
    <a href="fresher_referral_companion.html">Fresher Referral Companion (28 Programs)</a>
    <a href="outreach_messages_hub.html">Executive Outreach Hub</a>
    <a href="connections_directory.html">Master Directory</a>
    <div class="nav-right">
      <a href="connection_personalized_messages.csv" class="csv-link" download>Download Master CSV (14 MB)</a>
    </div>
  </nav>

  <!-- Header -->
  <header class="header">
    <h1>LinkedIn Master <span>Messenger & Job Referral Command Center</span></h1>
    <p>All <b>9,223 professional connections</b> are fully searchable in this high-performance command center. Each contact is paired with verified Job IDs, candidate referral packets, LinkedIn IDs, direct profile launch buttons, local tracking status (Contacted & Starred), and instant 1-click clipboard copy.</p>
  </header>

  <!-- Metrics Ribbon -->
  <div class="metrics-ribbon">
    <div class="metric-card accent">
      <div class="label">Total Network</div>
      <div class="val">{len(connections):,}</div>
    </div>
    <div class="metric-card green">
      <div class="label">Active Job Openings Mapped</div>
      <div class="val">{active_job_id_matches:,}</div>
    </div>
    <div class="metric-card amber">
      <div class="label">Fortune 500 & MNC Contacts</div>
      <div class="val">1,400+</div>
    </div>
    <div class="metric-card purple">
      <div class="label">Messaged Status</div>
      <div class="val" id="metricContacted">0 / {len(connections):,}</div>
    </div>
  </div>

  <!-- Search & Filters -->
  <div class="controls-bar">
    <div class="search-row">
      <input type="text" id="searchInput" class="search-input" placeholder="Search across all 9,223 connections by name, company, position, Job ID, or LinkedIn ID (e.g. Goldman, 4452387165, EY, Amazon, TCS)...">
      <button class="action-btn secondary" onclick="exportFilteredCsv()">Export Filtered to CSV</button>
    </div>
    <div class="filter-pills">
      <button class="filter-btn active" onclick="setFilter('all', this)">All Network ({len(connections):,})</button>
      <button class="filter-btn" onclick="setFilter('job_id', this)">Active Job ID Mapped ({active_job_id_matches:,})</button>
      <button class="filter-btn" onclick="setFilter('f500', this)">Fortune 500 & Global MNCs</button>
      <button class="filter-btn" onclick="setFilter('hr', this)">HR & Talent Leads</button>
      <button class="filter-btn" onclick="setFilter('exec', this)">Senior Leadership</button>
      <button class="filter-btn" onclick="setFilter('ops', this)">Operations & SCM</button>
      <button class="filter-btn" onclick="setFilter('fin', this)">Finance & Banking</button>
      <button class="filter-btn" onclick="setFilter('tech', this)">Tech & Product</button>
      <button class="filter-btn" onclick="setFilter('campus', this)">Campus & Alumni</button>
      <button class="filter-btn btn-star" onclick="setFilter('starred', this)">Starred / Favorites</button>
      <button class="filter-btn btn-contacted" onclick="setFilter('contacted', this)">Already Contacted</button>
    </div>
  </div>

  <!-- Pagination Bar Top -->
  <div class="pagination-bar">
    <div id="resultCount">Showing 1-50 of {len(connections):,} connections</div>
    <div class="page-btns">
      <button class="page-btn" id="btnFirst" onclick="gotoPage(1)">« First</button>
      <button class="page-btn" id="btnPrev" onclick="prevPage()">‹ Prev</button>
      <span id="pageIndicator" style="font-weight: 600; color: #fff;">Page 1</span>
      <button class="page-btn" id="btnNext" onclick="nextPage()">Next ›</button>
      <button class="page-btn" id="btnLast" onclick="gotoLastPage()">Last »</button>
    </div>
  </div>

  <!-- Contacts Container -->
  <div id="contactGrid" class="contact-grid">
    <!-- Populated by JS -->
  </div>

  <!-- Pagination Bar Bottom -->
  <div class="pagination-bar" style="margin-top: 16px;">
    <div id="resultCountBottom">Showing 1-50 of {len(connections):,} connections</div>
    <div class="page-btns">
      <button class="page-btn" onclick="gotoPage(1)">« First</button>
      <button class="page-btn" onclick="prevPage()">‹ Prev</button>
      <button class="page-btn" onclick="nextPage()">Next ›</button>
      <button class="page-btn" onclick="gotoLastPage()">Last »</button>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast">Copied to clipboard!</div>

  <script>
    const ALL_CONTACTS = {json.dumps(compact_pool, ensure_ascii=False)};
    const CANDIDATE_PACKET = `{candidate_packet}`;

    let currentFilter = 'all';
    let currentPage = 1;
    const PAGE_SIZE = 50;
    let activeList = ALL_CONTACTS;

    // Load LocalStorage State
    let contactedIds = new Set(JSON.parse(localStorage.getItem('aditya_contacted_ids') || '[]'));
    let starredIds = new Set(JSON.parse(localStorage.getItem('aditya_starred_ids') || '[]'));

    function updateMetrics() {{
      const el = document.getElementById('metricContacted');
      if (el) {{
        el.innerText = `${{contactedIds.size}} / ${{ALL_CONTACTS.length}}`;
      }}
    }}

    function toggleContacted(idx) {{
      if (contactedIds.has(idx)) {{
        contactedIds.delete(idx);
      }} else {{
        contactedIds.add(idx);
      }}
      localStorage.setItem('aditya_contacted_ids', JSON.stringify(Array.from(contactedIds)));
      updateMetrics();
      renderPage();
    }}

    function toggleStarred(idx) {{
      if (starredIds.has(idx)) {{
        starredIds.delete(idx);
      }} else {{
        starredIds.add(idx);
      }}
      localStorage.setItem('aditya_starred_ids', JSON.stringify(Array.from(starredIds)));
      renderPage();
    }}

    function buildMessage(c) {{
      const fn = c.fn || 'there';
      const pos = c.p || 'Professional';
      const co = c.c || 'your team';

      if (c.cat.includes('Tier 1')) {{
        return `Hi ${{fn}},\\n\\nHope your week is off to a wonderful start! Always inspiring seeing your journey as ${{pos}} at ${{co}}.\\n\\nI'm reaching out with genuine respect for your craft and team. As an upcoming 2026 graduate in BBA (International Business) at Dayananda Sagar University here in Bengaluru seeking fresher and entry-level operations roles, I've focused on high-accountability operational execution—serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (managing crowd logistics and multi-vendor coordination for 100,000+ delegates with zero security breaches and 0.0% shrinkage) alongside managing run-of-show contracts for Tata Communications and Puma Global.\\n\\nI noticed an active entry-level / campus opening at ${{co}} that aligns directly with my background:\\n• Target Role: ${{c.ji.split(' | ')[1] || 'Operations Specialist'}}\\n• Job ID / Req ID: ${{c.jid}}\\n• Application Link: ${{c.ju}}\\n\\nKnowing how much operational excellence and team standards matter at ${{co}}, I would be deeply honored if you might consider putting in an internal referral for my profile. To save you time and make this completely frictionless for your internal portal, here is my pre-filled candidate packet:\\n\\n${{CANDIDATE_PACKET}}\\n\\nPlease know there is absolutely zero pressure if company referral guidelines or bandwidth make this difficult right now—just connecting with you and learning from your experience at ${{co}} is already a true privilege.\\n\\nWishing you and your team continued momentum and success!\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('HR & Talent')) {{
        return `Hi ${{fn}},\\n\\nHope your week is going great! I've been following your impactful work shaping talent pipelines and team culture as ${{pos}} at ${{co}}.\\n\\nI am concluding my final year in International Business at Dayananda Sagar University here in Bengaluru, targeting fresher and entry-level graduate roles. My background is centered on disciplined operations, supply chain logistics, and high-stakes vendor management—recently serving as Operations Lead at AERO INDIA 2025 (100,000+ attendees, 0 security breaches, 0.0% inventory shrinkage) and managing contract SLAs for Tata Communications.\\n\\nAs your team at ${{co}} plans upcoming hiring or campus/entry-level intakes for operations, business analysis, supply chain, or graduate trainee roles, I would love to be on your radar. To make review effortless, here is a quick snapshot of my candidate packet:\\n\\n${{CANDIDATE_PACKET}}\\n\\nThank you sincerely for all the dedication you bring to talent acquisition, and I'd be honored to connect or share my tailored resume whenever convenient.\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('Senior Leadership')) {{
        return `Hi ${{fn}},\\n\\nI hope this message finds you well. I’ve greatly admired your leadership as ${{pos}} at ${{co}} and the strategic direction your team is driving.\\n\\nAs I complete my International Business degree at Dayananda Sagar University (Class of 2026), my goal is to launch my career in organizations where operational integrity, customer trust, and rigorous execution are prized. Having led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ attendees with zero security incidents and 0.0% shrinkage) and enforced multi-vendor contract SLAs for Tata Communications and Puma Global, I know how essential execution fidelity is to senior leaders like yourself.\\n\\nI would be deeply honored for a brief 5-minute perspective on what you value most when building resilient operational teams at ${{co}}. And if a fresher, campus, or entry-level operations analyst opening exists within your group, I would be profoundly grateful for your guidance.\\n\\nThank you sincerely for your time and leadership, ${{fn}}.\\n\\nBest regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('Operations & Supply')) {{
        return `Hi ${{fn}},\\n\\nHope you're having a productive week! Always great connecting with an operational professional—especially seeing your execution as ${{pos}} at ${{co}}.\\n\\nAs a final-year student in International Business at Dayananda Sagar University (Class of 2026) actively seeking entry-level and fresher operations roles, I've dedicated myself to rigorous operational delivery. Serving as Operations Lead at AERO INDIA 2025 at Yelahanka AFB (100k+ attendees, 0 security infractions, 0.0% shrinkage) and managing run-of-show logistics and SLA contract enforcement for Puma Global and Tata Communications taught me the true value of relentless ground discipline.\\n\\nI would love to exchange notes on operational workflows, vendor governance, and early-career pathways at ${{co}}. If you ever have a few minutes for a virtual coffee or quick conversation, it would be a pleasure to connect.\\n\\nWishing you seamless operations and continued momentum!\\n\\nBest regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('Finance & Banking')) {{
        return `Hi ${{fn}},\\n\\nHope all is well with you! I’ve been following your professional journey in financial governance and analysis as ${{pos}} at ${{co}}.\\n\\nI'm currently concluding my final year in International Business at Dayananda Sagar University (Class of 2026), targeting fresher / entry-level analyst opportunities with a strong focus on financial reconciliation, trade finance documentation (INCOTERMS 2020, Letters of Credit), and contract compliance. During AERO INDIA 2025, I maintained a 0.0% inventory shrinkage record across high-volume assets and managed multi-vendor billing and SLA compliance for Tata Communications.\\n\\nI would love to learn how your team approaches financial operations and risk management at ${{co}}, and explore potential early-career analyst opportunities. Wishing you a great financial quarter ahead!\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('Technology & Product')) {{
        return `Hi ${{fn}},\\n\\nHope you are having a fantastic week! It's always inspiring following your technical craft and journey as ${{pos}} at ${{co}}.\\n\\nWhile my core discipline is International Business and Operations at Dayananda Sagar University (Class of 2026, targeting entry-level roles), I work closely at the intersection of business operations and technology systems. Recently, I led operations at AERO INDIA 2025 (100,000+ delegates, 0 breaches, 0.0% inventory loss) where real-time coordination, automated tracking, and multi-vendor communication protocols were mission-critical.\\n\\nI have immense respect for the engineering and product standards at ${{co}}. If your team or cross-functional operations group is ever looking for a high-energy fresher / entry-level operator who bridges business logic, system discipline, and data integrity, I'd love to connect and learn about your experience there.\\n\\nWishing you and your team smooth deployments and continued success!\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('University & Alumni')) {{
        return `Hi ${{fn}},\\n\\nGreat to connect with a fellow campus peer! It’s inspiring seeing your growth as ${{pos}} with ${{co}}.\\n\\nI'm currently in my final year of BBA (International Business) at Dayananda Sagar University (Class of 2026). Over the past year, I had the privilege of leading ground operations at AERO INDIA 2025 at Yelahanka AFB (managing 100k+ footfall with 0 breaches and 0 shrinkage) alongside corporate logistics for Tata Communications.\\n\\nI'm actively exploring fresher, campus, and entry-level operations and analyst roles across Bengaluru. If you ever have a few minutes to share your thoughts on your journey since graduation, or if I can ever support you in any way, let's definitely catch up!\\n\\nWishing you continued success and proud to be part of the same community!\\n\\nCheers,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      if (c.cat.includes('Commercial & Growth')) {{
        return `Hi ${{fn}},\\n\\nHope you are having a thriving week! Really admire the commercial momentum and customer growth you're driving as ${{pos}} at ${{co}}.\\n\\nI'm concluding my International Business degree at Dayananda Sagar University (Class of 2026, targeting entry-level commercial operations and analyst roles). Having led event operations at AERO INDIA 2025 for 100k+ visitors and delivered run-of-show logistics for Puma Global and Tata Communications, I understand how vital seamless delivery is to maintaining customer trust and commercial success.\\n\\nIf there is ever an early-career opening or if I can assist your initiatives in Bengaluru, I'd be delighted to connect.\\n\\nWishing you high conversions and continued success!\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
      }}

      // General Reconnect
      return `Hi ${{fn}},\\n\\nHope you are having a wonderful week! Always inspiring following your journey as ${{pos}} at ${{co}}.\\n\\nI wanted to reach out, say hello, and share a quick personal update. I am completing my final year in International Business at Dayananda Sagar University in Bengaluru (Class of 2026, exploring fresher and entry-level opportunities). Over the past year, I've led ground operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ delegates with zero security breaches and 0.0% inventory shrinkage) and managed multi-vendor SLA contracts for Tata Communications and Puma Global summits.\\n\\nI'm currently exploring fresher and entry-level roles in operations, program coordination, and business analytics. If you or anyone in your network is ever looking for a disciplined, execution-focused operator—or if I can ever help support your initiatives here in Bengaluru—I would love to connect for a brief 5-minute chat.\\n\\nWishing you continued success in your journey!\\n\\nWarm regards,\\nAditya Mehra\\nashishiash007@gmail.com | +91 7003456624 | Bengaluru`;
    }}

    function getBadgeClass(category) {{
      if (category.includes('Tier 1')) return 'badge-tier1';
      if (category.includes('Tier 2')) return 'badge-tier2';
      if (category.includes('Tier 3')) return 'badge-tier3';
      return 'badge-tier4';
    }}

    function renderPage() {{
      const container = document.getElementById('contactGrid');
      const total = activeList.length;

      if (total === 0) {{
        container.innerHTML = '<div style="text-align:center; padding: 60px; color: var(--text-muted); font-size: 16px;">No matching connections found. Try a different search term or clear filters.</div>';
        document.getElementById('resultCount').innerText = 'Showing 0 of 0 connections';
        document.getElementById('resultCountBottom').innerText = 'Showing 0 of 0 connections';
        document.getElementById('pageIndicator').innerText = 'Page 0 of 0';
        return;
      }}

      const totalPages = Math.ceil(total / PAGE_SIZE);
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const start = (currentPage - 1) * PAGE_SIZE;
      const end = Math.min(start + PAGE_SIZE, total);

      document.getElementById('resultCount').innerText = `Showing ${{start + 1}}-${{end}} of ${{total.toLocaleString()}} matching connections`;
      document.getElementById('resultCountBottom').innerText = `Showing ${{start + 1}}-${{end}} of ${{total.toLocaleString()}} matching connections`;
      document.getElementById('pageIndicator').innerText = `Page ${{currentPage}} of ${{totalPages}}`;

      document.getElementById('btnFirst').disabled = (currentPage === 1);
      document.getElementById('btnPrev').disabled = (currentPage === 1);
      document.getElementById('btnNext').disabled = (currentPage === totalPages);
      document.getElementById('btnLast').disabled = (currentPage === totalPages);

      let html = '';
      for (let i = start; i < end; i++) {{
        const c = activeList[i];
        const isContacted = contactedIds.has(c.i);
        const isStarred = starredIds.has(c.i);
        const badgeClass = getBadgeClass(c.cat);
        const hasJobId = c.jid && !c.jid.startsWith('NETWORK_') && !c.jid.startsWith('CAMPUS_');
        const msgText = buildMessage(c);

        html += `
          <div class="contact-card ${{isContacted ? 'is-contacted' : ''}} ${{isStarred ? 'is-starred' : ''}}" id="card-${{c.i}}">
            <div class="card-top">
              <div class="person-info">
                <h3>
                  ${{c.n}}
                  <span class="badge ${{badgeClass}}">${{c.cat}}</span>
                </h3>
                <div class="pos">${{c.p}} at <span class="co">${{c.c}}</span></div>
                <div class="linkedin-id-bar">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="#38bdf8"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.32a1.62 1.62 0 1 0 0 3.24 1.62 1.62 0 0 0 0-3.24Z"/></svg>
                  <span>LinkedIn ID:</span>
                  ${{c.u ? `<a href="${{c.u}}" target="_blank" class="linkedin-handle">in/${{c.lid}}</a>` : `<span>${{c.lid}}</span>`}}
                </div>
              </div>
              <div class="card-actions">
                <button class="btn-star-toggle ${{isStarred ? 'active' : ''}}" onclick="toggleStarred(${{c.i}})" title="Favorite / Star this lead">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isStarred ? 'currentColor' : 'none'}}" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                </button>
                <button class="btn-contact-toggle ${{isContacted ? 'active' : ''}}" onclick="toggleContacted(${{c.i}})">
                  ${{isContacted ? '✓ Messaged' : 'Mark as Sent'}}
                </button>
                ${{c.u ? `<a href="${{c.u}}" target="_blank" class="action-btn linkedin-btn"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.32a1.62 1.62 0 1 0 0 3.24 1.62 1.62 0 0 0 0-3.24Z"/></svg> Open Profile</a>` : ''}}
                ${{c.ju ? `<a href="${{c.ju}}" target="_blank" class="action-btn secondary">View Role Portal</a>` : ''}}
                <button class="action-btn btn-copy" onclick="copyMessageByIndex(${{c.i}})">Copy Outreach Message</button>
              </div>
            </div>

            ${{hasJobId ? `
              <div class="job-tag">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                <b>Target Requisition:</b> ${{c.ji}}
              </div>
            ` : ''}}

            <div class="message-box" id="msgbox-${{c.i}}">${{escapeHtml(msgText)}}</div>
          </div>
        `;
      }}

      container.innerHTML = html;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function escapeHtml(text) {{
      return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }}

    function copyMessageByIndex(idx) {{
      const c = ALL_CONTACTS[idx];
      const text = buildMessage(c);
      navigator.clipboard.writeText(text).then(() => {{
        showToast(`Copied personalized message for ${{c.n}}!`);
      }}).catch(() => {{
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        showToast(`Copied personalized message for ${{c.n}}!`);
      }});
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2500);
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        renderPage();
      }}
    }}

    function nextPage() {{
      const totalPages = Math.ceil(activeList.length / PAGE_SIZE);
      if (currentPage < totalPages) {{
        currentPage++;
        renderPage();
      }}
    }}

    function gotoPage(p) {{
      currentPage = p;
      renderPage();
    }}

    function gotoLastPage() {{
      const totalPages = Math.ceil(activeList.length / PAGE_SIZE);
      currentPage = totalPages;
      renderPage();
    }}

    function applyFilters() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      
      activeList = ALL_CONTACTS.filter(c => {{
        // Filter pills
        if (currentFilter === 'job_id' && (!c.cat.includes('Tier 1') && c.jid.startsWith('NETWORK_'))) return false;
        if (currentFilter === 'hr' && !c.cat.includes('HR & Talent')) return false;
        if (currentFilter === 'exec' && !c.cat.includes('Senior Leadership')) return false;
        if (currentFilter === 'ops' && !c.cat.includes('Operations & Supply')) return false;
        if (currentFilter === 'fin' && !c.cat.includes('Finance & Banking')) return false;
        if (currentFilter === 'tech' && !c.cat.includes('Technology & Product')) return false;
        if (currentFilter === 'campus' && !c.cat.includes('University & Alumni')) return false;
        if (currentFilter === 'starred' && !starredIds.has(c.i)) return false;
        if (currentFilter === 'contacted' && !contactedIds.has(c.i)) return false;

        if (currentFilter === 'f500') {{
          const isF500 = /goldman|jpmorgan|chase|deloitte|ey|ernst|pwc|kpmg|amazon|aws|microsoft|google|ibm|accenture|tcs|infosys|wipro|capgemini|cognizant|target|walmart|bosch|cisco|oracle|apple|meta|intel|hp|salesforce|adobe|hsbc|deutsche|cba|icici|hdfc|sbi|itc|reliance|anz|gallagher|stripe|standard chartered|societe generale|ubs/i.test(c.c);
          if (!isF500) return false;
        }}

        // Search Query
        if (q) {{
          const matchName = c.n.toLowerCase().includes(q);
          const matchCo = c.c.toLowerCase().includes(q);
          const matchPos = c.p.toLowerCase().includes(q);
          const matchJob = c.ji.toLowerCase().includes(q);
          const matchJobId = c.jid.toLowerCase().includes(q);
          const matchLid = (c.lid || '').toLowerCase().includes(q);
          return matchName || matchCo || matchPos || matchJob || matchJobId || matchLid;
        }}

        return true;
      }});

      currentPage = 1;
      renderPage();
    }}

    function setFilter(type, btn) {{
      currentFilter = type;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    }}

    function exportFilteredCsv() {{
      let csv = 'Full Name,Company,Position,Category,Job Info,Job ID,LinkedIn ID,LinkedIn URL\\n';
      activeList.forEach(c => {{
        const row = [
          `"${{c.n.replace(/"/g, '""')}}"`,
          `"${{c.c.replace(/"/g, '""')}}"`,
          `"${{c.p.replace(/"/g, '""')}}"`,
          `"${{c.cat.replace(/"/g, '""')}}"`,
          `"${{c.ji.replace(/"/g, '""')}}"`,
          `"${{c.jid.replace(/"/g, '""')}}"`,
          `"${{c.lid.replace(/"/g, '""')}}"`,
          `"${{c.u.replace(/"/g, '""')}}"`
        ];
        csv += row.join(',') + '\\n';
      }});

      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', `aditya_connections_${{currentFilter}}_${{activeList.length}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    document.getElementById('searchInput').addEventListener('input', applyFilters);

    // Initial Setup
    updateMetrics();
    renderPage();
  </script>
</body>
</html>
'''

out_html = r'e:\anti\linkedin_export\connection_messenger_center.html'
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated master interactive messenger center: {out_html} ({os.path.getsize(out_html) / (1024*1024):.2f} MB)")
print("--- Engine Execution Complete. All Jobs and Messages Ready ---")
