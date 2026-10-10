import sqlite3
import json

conn = sqlite3.connect('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies.db')
c = conn.cursor()

# Create table for detailed deep dives
c.execute('''
CREATE TABLE IF NOT EXISTS enterprise_deep_dives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT UNIQUE,
    ticker TEXT,
    headquarters TEXT,
    bangalore_campuses TEXT,
    primary_pincodes TEXT,
    ats_platform TEXT,
    direct_careers_url TEXT,
    bba_fresher_roles TEXT,
    fresher_ctc_range TEXT,
    interview_process TEXT,
    referral_guidance TEXT
)
''')

# Populate with all 22 analyzed enterprises
enterprises = [
    {
        "company_name": "SAP Labs India",
        "ticker": "SAP (NYSE: SAP)",
        "headquarters": "Walldorf, Germany",
        "bangalore_campuses": "RMZ Ecoworld, Bellandur & EPIP Zone, Whitefield",
        "primary_pincodes": "560103, 560066",
        "ats_platform": "SAP SuccessFactors",
        "direct_careers_url": "https://jobs.sap.com/",
        "bba_fresher_roles": "Commercial Operations Associate, Cloud Delivery PMO, Sales Operations Trainee",
        "fresher_ctc_range": "₹6.5L – ₹9.5L LPA",
        "interview_process": "Online Aptitude + Technical / Business Case Round + Managerial & HR Discussion",
        "referral_guidance": "Search LinkedIn for 'Early Talent Recruiter SAP Labs India' or 'Commercial Operations Lead RMZ Ecoworld'."
    },
    {
        "company_name": "IBM India",
        "ticker": "IBM (NYSE: IBM)",
        "headquarters": "Armonk, New York, USA",
        "bangalore_campuses": "Manyata Tech Park, Hebbal & Embassy GolfLinks (EGL), Domlur",
        "primary_pincodes": "560045, 560071",
        "ats_platform": "BrassRing / IBM Careers",
        "direct_careers_url": "https://www.ibm.com/careers/in-en",
        "bba_fresher_roles": "Financial Analyst Trainee, Talent Acquisition Coordinator, Inside Sales Representative",
        "fresher_ctc_range": "₹4.2L – ₹6.5L LPA",
        "interview_process": "Cognitive Ability Assessment + Business Case Presentation + HR Behavioral Interview",
        "referral_guidance": "Target Manyata Embassy Business Park campus employees on LinkedIn."
    },
    {
        "company_name": "Adobe India",
        "ticker": "ADBE (NASDAQ: ADBE)",
        "headquarters": "San Jose, California, USA",
        "bangalore_campuses": "Prestige Platina Tech Park, Marathahalli-Sarjapur ORR, Bellandur",
        "primary_pincodes": "560103",
        "ats_platform": "Workday",
        "direct_careers_url": "https://adobe.wd5.myworkdayjobs.com/external_experienced",
        "bba_fresher_roles": "Customer Success Associate, Inside Sales SDR, Commercial Contracts Specialist",
        "fresher_ctc_range": "₹7.5L – ₹12.0L LPA",
        "interview_process": "Resume Screening + Video Intro + Case Study / Role-Play + Director Round",
        "referral_guidance": "Connect with Adobe Inside Sales Managers at Prestige Platina Tech Park."
    },
    {
        "company_name": "Intel India",
        "ticker": "INTC (NASDAQ: INTC)",
        "headquarters": "Santa Clara, California, USA",
        "bangalore_campuses": "SRR Mega Campus, Outer Ring Road, Bellandur",
        "primary_pincodes": "560103",
        "ats_platform": "Workday",
        "direct_careers_url": "https://intel.wd1.myworkdayjobs.com/External",
        "bba_fresher_roles": "Supply Chain Analyst, Global Procurement Specialist, Finance Analyst Trainee",
        "fresher_ctc_range": "₹7.0L – ₹10.5L LPA",
        "interview_process": "Online Quantitative Test + Supply Chain Operations Case Round + Behavioral Interview",
        "referral_guidance": "Reach out to Global Supply Chain Operations Managers at Intel SRR Campus."
    },
    {
        "company_name": "NVIDIA India",
        "ticker": "NVDA (NASDAQ: NVDA)",
        "headquarters": "Santa Clara, California, USA",
        "bangalore_campuses": "Salarpuria GR Tech Park, Whitefield",
        "primary_pincodes": "560066",
        "ats_platform": "Workday",
        "direct_careers_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
        "bba_fresher_roles": "Sales Operations Analyst, Supply Chain Operations Specialist, Business Ops Associate",
        "fresher_ctc_range": "₹8.0L – ₹13.0L LPA",
        "interview_process": "Take-Home Data Modeling Exercise + Operations Manager Case + Culture Interview",
        "referral_guidance": "Target Business Operations team members at Salarpuria GR Tech Park."
    },
    {
        "company_name": "Flipkart",
        "ticker": "Walmart Subsidiary",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Embassy TechVillage (ETV), Outer Ring Road, Bellandur",
        "primary_pincodes": "560103",
        "ats_platform": "Greenhouse / Flipkart Careers",
        "direct_careers_url": "https://www.flipkartcareers.com/",
        "bba_fresher_roles": "Category Associate, Supply Chain Operations Trainee, Merchandising Operations",
        "fresher_ctc_range": "₹5.5L – ₹8.5L LPA",
        "interview_process": "Online Business Aptitude + Category GTM Case Study + Category Director Interview",
        "referral_guidance": "Connect with Category Managers (M1/M2) at Embassy TechVillage."
    },
    {
        "company_name": "PhonePe",
        "ticker": "Walmart Subsidiary",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Salarpuria Softzone, Green Glen Layout, Bellandur",
        "primary_pincodes": "560103",
        "ats_platform": "Greenhouse / PhonePe Careers",
        "direct_careers_url": "https://www.phonepe.com/careers/",
        "bba_fresher_roles": "Merchant Operations Associate, Business Development Associate, Fraud & Risk Analyst",
        "fresher_ctc_range": "₹4.8L – ₹7.2L LPA",
        "interview_process": "Aptitude & Problem Solving Assessment + Operations Case Round + Culture Interview",
        "referral_guidance": "Search for Merchant Operations Leads at Salarpuria Softzone, Bellandur."
    },
    {
        "company_name": "Razorpay",
        "ticker": "Unicorn ($7.5B Valuation)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "SJR Cyber Linc, Koramangala 4th Block",
        "primary_pincodes": "560095",
        "ats_platform": "Lever",
        "direct_careers_url": "https://razorpay.com/jobs/",
        "bba_fresher_roles": "Sales Development Representative (SDR), Merchant Onboarding Associate, Partner Success",
        "fresher_ctc_range": "₹5.0L – ₹8.0L LPA (+ High Variable Incentives)",
        "interview_process": "Mock Cold Calling / Pitch Simulation + Sales Objection Handling + Culture Fit Round",
        "referral_guidance": "Connect with Inside Sales Leads at SJR Cyber Linc, Koramangala."
    },
    {
        "company_name": "Groww",
        "ticker": "Unicorn ($3B+ Valuation)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Vaishnavi Tech Park, Outer Ring Road, Bellandur",
        "primary_pincodes": "560103",
        "ats_platform": "Lever",
        "direct_careers_url": "https://groww.in/careers",
        "bba_fresher_roles": "Customer Operations Associate, Customer Success Specialist, Growth & Community Associate",
        "fresher_ctc_range": "₹4.5L – ₹6.5L LPA",
        "interview_process": "Aptitude & Stock Market Basics Test + Customer Empathy Simulation + HR Round",
        "referral_guidance": "Reach out to Operations Leads at Vaishnavi Tech Park, Bellandur."
    },
    {
        "company_name": "Swiggy",
        "ticker": "SWIGGY (NSE/BSE)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Embassy TechVillage (ETV), Bellandur & IBC Knowledge Park, Bannerghatta Road",
        "primary_pincodes": "560103, 560029",
        "ats_platform": "Greenhouse",
        "direct_careers_url": "https://www.swiggy.com/careers",
        "bba_fresher_roles": "Instamart Sourcing Associate, Restaurant Onboarding Lead, Category Executive",
        "fresher_ctc_range": "₹4.5L – ₹7.0L LPA",
        "interview_process": "Market Sizing Case Study + Negotiation Simulation Round + Operations Head Interview",
        "referral_guidance": "Target Instamart Supply Leads at Embassy TechVillage."
    },
    {
        "company_name": "Meesho",
        "ticker": "Unicorn ($5B Valuation)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Helios Business Park, Kadubeesanahalli, Outer Ring Road",
        "primary_pincodes": "560103",
        "ats_platform": "Greenhouse",
        "direct_careers_url": "https://www.meesho.io/jobs",
        "bba_fresher_roles": "Category Operations Associate, Seller Growth Executive, Logistics Planning Associate",
        "fresher_ctc_range": "₹5.0L – ₹7.5L LPA",
        "interview_process": "Business Problem Solving Challenge + Excel Case Study + Category Manager Round",
        "referral_guidance": "Connect with Business Managers at Helios Business Park, Kadubeesanahalli."
    },
    {
        "company_name": "Walmart Global Tech",
        "ticker": "WMT (NYSE: WMT)",
        "headquarters": "Bentonville, Arkansas, USA",
        "bangalore_campuses": "Prestige Tech Park & Cessna Business Park, Kadubeesanahalli",
        "primary_pincodes": "560103",
        "ats_platform": "Workday",
        "direct_careers_url": "https://careers.walmart.com/us/en/results?q=India",
        "bba_fresher_roles": "Replenishment Analyst, Global Merchandising Operations, Finance Shared Services",
        "fresher_ctc_range": "₹6.5L – ₹9.0L LPA",
        "interview_process": "Online Cognitive Test + Retail Operations Case + Managerial Interview",
        "referral_guidance": "Target Supply Chain & Replenishment Managers at Prestige Tech Park."
    },
    {
        "company_name": "Lowe's India",
        "ticker": "LOW (NYSE: LOW)",
        "headquarters": "Mooresville, North Carolina, USA",
        "bangalore_campuses": "Manyata Embassy Business Park, Nagavara, Hebbal",
        "primary_pincodes": "560045",
        "ats_platform": "Phenom People",
        "direct_careers_url": "https://talent.lowes.com/in/en/c/corporate-jobs",
        "bba_fresher_roles": "Merchandising Operations Analyst, Pricing & Promotion Associate, Store Support Specialist",
        "fresher_ctc_range": "₹5.5L – ₹7.5L LPA",
        "interview_process": "Retail Aptitude Test + Live Excel Merchandising Exercise + Manager Round",
        "referral_guidance": "Search Manyata Tech Park Lowe's employees on LinkedIn."
    },
    {
        "company_name": "Shell India",
        "ticker": "SHEL (LSE/NYSE)",
        "headquarters": "London, UK",
        "bangalore_campuses": "Shell Technology Centre (STCB), Aerospace Park Devanahalli & RMZ Ecoworld",
        "primary_pincodes": "562149, 560103",
        "ats_platform": "Workday",
        "direct_careers_url": "https://shell.wd3.myworkdayjobs.com/shellcareers",
        "bba_fresher_roles": "Trading & Supply Operations Associate, Contracting & Procurement Specialist, Finance Ops (FO-SBO)",
        "fresher_ctc_range": "₹5.5L – ₹8.5L LPA",
        "interview_process": "Shell Online Assessment (Cognitive & Behavioral) + Commercial Case Study + HR Round",
        "referral_guidance": "Connect with Contracting & Procurement Leads at STCB Devanahalli."
    },
    {
        "company_name": "The Boeing Company",
        "ticker": "BA (NYSE: BA)",
        "headquarters": "Arlington, Virginia, USA",
        "bangalore_campuses": "Boeing India Engineering & Technology Center (BIETC), Aerospace Park Devanahalli",
        "primary_pincodes": "562149",
        "ats_platform": "Workday",
        "direct_careers_url": "https://jobs.boeing.com/location/india-jobs/185/1269750/2",
        "bba_fresher_roles": "Supply Chain Specialist, Procurement Contracts Specialist, Financial Planning Analyst",
        "fresher_ctc_range": "₹6.5L – ₹9.5L LPA",
        "interview_process": "Structured Behavioral Interview (STAR Method) + Technical Case Round + Compliance Check",
        "referral_guidance": "Target Supply Chain & Contracts Specialists at BIETC Aerospace Park."
    },
    {
        "company_name": "Mercedes-Benz R&D India (MBRDI)",
        "ticker": "MBG (FWB: MBG)",
        "headquarters": "Stuttgart, Germany",
        "bangalore_campuses": "Brigade Tech Gardens, Brookefield & Whitefield",
        "primary_pincodes": "560037, 560066",
        "ats_platform": "Taleo / MBRDI Careers",
        "direct_careers_url": "https://www.mbrdi.co.in/careers/",
        "bba_fresher_roles": "Procurement Specialist, Project Management Office (PMO) Associate, Financial Controlling",
        "fresher_ctc_range": "₹5.0L – ₹7.5L LPA",
        "interview_process": "Domain Aptitude + PMO / Procurement Case Simulation + Department Head Round",
        "referral_guidance": "Connect with PMO Managers at Brigade Tech Gardens, Brookefield."
    },
    {
        "company_name": "AstraZeneca India",
        "ticker": "AZN (LSE/NASDAQ)",
        "headquarters": "Cambridge, UK",
        "bangalore_campuses": "Manyata Embassy Business Park, Nagavara, Hebbal",
        "primary_pincodes": "560045",
        "ats_platform": "Workday",
        "direct_careers_url": "https://careers.astrazeneca.com/location/bengaluru-jobs/7684/1269750-1277333-1277332/4",
        "bba_fresher_roles": "Commercial Operations Analyst, Global Procurement Specialist, HR Services Coordinator",
        "fresher_ctc_range": "₹5.2L – ₹8.0L LPA",
        "interview_process": "Online Aptitude & English Test + Business Operations Case Study + HR Round",
        "referral_guidance": "Reach out to Commercial Operations Leads at Manyata Tech Park."
    },
    {
        "company_name": "EXL Service",
        "ticker": "EXLS (NASDAQ: EXLS)",
        "headquarters": "New York, USA",
        "bangalore_campuses": "Prestige Tech Pacific Park, Kadubeesanahalli & Kalyani Tech Park, Whitefield",
        "primary_pincodes": "560103, 560066",
        "ats_platform": "Oracle Cloud HCM (CX_2)",
        "direct_careers_url": "https://fa-ewjt-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_2/jobs",
        "bba_fresher_roles": "Supply Chain Analyst (Req 20789), Accounts Payable Executive (Req 20546), O2C Billing Executive (Req 9980)",
        "fresher_ctc_range": "₹3.6L – ₹5.5L LPA",
        "interview_process": "Cognitive & Aptitude Test + Excel Practical Test + Technical/Operations Round + HR",
        "referral_guidance": "Cite exact Requisition IDs (e.g. 20789, 20546) to Prestige Tech Pacific Park leads."
    },
    {
        "company_name": "Genpact",
        "ticker": "G (NYSE: G)",
        "headquarters": "New York, USA",
        "bangalore_campuses": "Prestige Technology Park IV, Bellandur, Pritech Park SEZ & Surya Park Electronic City",
        "primary_pincodes": "560103, 560100",
        "ats_platform": "Workday",
        "direct_careers_url": "https://genpact.wd108.myworkdayjobs.com/External_Careers",
        "bba_fresher_roles": "Associate Procurement Ops (JR10026685), Analyst Data Services (JR10030642), Associate Underwriting (JR10024652)",
        "fresher_ctc_range": "₹3.6L – ₹5.5L LPA",
        "interview_process": "AMCAT Cognitive Test + Versant Voice Test + Operations Scenario Interview + HR",
        "referral_guidance": "Reference Requisition JR10026685 or JR10030642 when messaging Prestige Tech Park leads."
    },
    {
        "company_name": "Capgemini India",
        "ticker": "CAP (EPA: CAP)",
        "headquarters": "Paris, France",
        "bangalore_campuses": "EPIP Zone Mega Campus, Whitefield, RMZ Ecoworld Bellandur & Electronic City",
        "primary_pincodes": "560066, 560103, 560100",
        "ats_platform": "SAP SuccessFactors / Azure JobStream",
        "direct_careers_url": "https://www.capgemini.com/in-en/careers/",
        "bba_fresher_roles": "Junior Business Analyst, Record to Analyze Process Expert, Digital Procurement Associate",
        "fresher_ctc_range": "₹3.6L – ₹5.5L LPA",
        "interview_process": "AON CoCubes Aptitude + English Fluency + Business Operations Case + HR Discussion",
        "referral_guidance": "Connect with Business Services (BSV) Delivery Leads at EPIP Zone Whitefield."
    },
    {
        "company_name": "Cognizant (CTS)",
        "ticker": "CTSH (NASDAQ: CTSH)",
        "headquarters": "Teaneck, New Jersey, USA",
        "bangalore_campuses": "Manyata Embassy Business Park, Nagavara & Bagmane World Technology Center",
        "primary_pincodes": "560045, 560048",
        "ats_platform": "Phenom People / Workday",
        "direct_careers_url": "https://careers.cognizant.com/global-en/jobs",
        "bba_fresher_roles": "Process Executive - Data / Financial Services, Claims Adjudication Associate, SCM Associate",
        "fresher_ctc_range": "₹3.2L – ₹4.5L LPA",
        "interview_process": "AMCAT Aptitude Test + Operations Manager Scenario Interview + HR Round",
        "referral_guidance": "Target Digital Operations (BPS) Team Leads at Manyata Tech Park."
    },
    {
        "company_name": "Accenture India",
        "ticker": "ACN (NYSE: ACN)",
        "headquarters": "Dublin, Ireland",
        "bangalore_campuses": "Prestige Tech Park, Kadubeesanahalli, RMZ Ecoworld, Brigade Tech Gardens & Electronic City",
        "primary_pincodes": "560103, 560037, 560100",
        "ats_platform": "Accenture Elastic VectorSearch / AEM",
        "direct_careers_url": "https://www.accenture.com/in-en/careers/jobsearch",
        "bba_fresher_roles": "Associate - Intelligent Operations (Level 13), Consulting GDN Analyst (Level 11), SCM Associate",
        "fresher_ctc_range": "₹3.8L – ₹6.5L LPA",
        "interview_process": "Cognitive & Analytical Test + Versant Communication Test + Operations Round + HR",
        "referral_guidance": "Connect with Intelligent Operations Team Leads at Prestige Tech Park."
    },
    {
        "company_name": "Wipro Limited",
        "ticker": "WIT (NYSE: WIT)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Doddakannelli Corporate HQ, Sarjapur Road, Electronic City Phase 1 & Kaveri SEZ",
        "primary_pincodes": "560035, 560100, 560103",
        "ats_platform": "SAP SuccessFactors RMK",
        "direct_careers_url": "https://careers.wipro.com/search",
        "bba_fresher_roles": "Process Associate (Band AA), Banking Operations Associate, F&A P2P Specialist",
        "fresher_ctc_range": "₹3.1L – ₹4.2L LPA",
        "interview_process": "Online Aptitude Assessment + Operations Practical Case + HR Fitment",
        "referral_guidance": "Reach out to Digital Operations & Platforms (DOP) Leads at Doddakannelli HQ."
    },
    {
        "company_name": "Infosys / Infosys BPM",
        "ticker": "INFY (NYSE: INFY)",
        "headquarters": "Bengaluru, India",
        "bangalore_campuses": "Electronic City Phase 1 (81-Acre Mega Campus) & Phase 2",
        "primary_pincodes": "560100",
        "ats_platform": "Angular Single Page Application / Intap Gateway",
        "direct_careers_url": "https://career.infosys.com/jobs?companyhiringtype=IBPM&countrycode=IN",
        "bba_fresher_roles": "Process Associate (Band JL 2), Procurement Associate, KYC/AML Analyst",
        "fresher_ctc_range": "₹3.0L – ₹4.0L LPA",
        "interview_process": "Infosys Assessment Test (Math/Verbal/Reasoning) + Operations Case Round + HR Round",
        "referral_guidance": "Target Infosys BPM Talent Acquisition Leads at Electronic City Phase 1."
    }
]

for ent in enterprises:
    c.execute('''
    INSERT OR REPLACE INTO enterprise_deep_dives 
    (company_name, ticker, headquarters, bangalore_campuses, primary_pincodes, ats_platform, direct_careers_url, bba_fresher_roles, fresher_ctc_range, interview_process, referral_guidance)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ent["company_name"], ent["ticker"], ent["headquarters"], ent["bangalore_campuses"],
        ent["primary_pincodes"], ent["ats_platform"], ent["direct_careers_url"], ent["bba_fresher_roles"],
        ent["fresher_ctc_range"], ent["interview_process"], ent["referral_guidance"]
    ))

conn.commit()
c.execute('SELECT COUNT(*) FROM enterprise_deep_dives')
print('Total enterprise deep dives populated:', c.fetchone()[0])
conn.close()
