import csv
import json
import os

# 1. Load Connections
with open(r'e:\anti\linkedin_export\Connections.csv', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

header_idx = -1
for i, line in enumerate(lines[:10]):
    if 'First Name' in line:
        header_idx = i
        break

reader = csv.DictReader(lines[header_idx:])
connections = list(reader)

# 2. Define Open Roles Catalog with Job IDs
open_roles = [
    {
        "company": "Goldman Sachs",
        "job_id": "4452387165",
        "title": "Global Banking & Markets Operations - IB Ops Client Onboarding Analyst",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4452387165",
        "type": "Investment Banking Operations",
        "target_keywords": ["operations", "client onboarding", "compliance", "trade finance", "risk"]
    },
    {
        "company": "JPMorganChase",
        "job_id": "4440836681",
        "title": "Data Management Associate",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4440836681",
        "type": "Data & Operations Management",
        "target_keywords": ["data management", "operations", "governance", "process optimization"]
    },
    {
        "company": "EY",
        "job_id": "4444908737",
        "title": "GDS Meetings and Events - Events Manager",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4444908737",
        "type": "Event Operations & Program Management",
        "target_keywords": ["event operations", "logistics", "vendor SLAs", "run-of-show", "budget control"]
    },
    {
        "company": "Amazon Web Services (AWS)",
        "job_id": "4443027895",
        "title": "Event Program Manager, AWS Global Events",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4443027895",
        "type": "Global Event Programs",
        "target_keywords": ["program management", "global events", "enterprise activations", "cross-functional coordination"]
    },
    {
        "company": "Amazon",
        "job_id": "4455781999",
        "title": "Business Analyst Support, IN Supply Chain",
        "location": "Bengaluru, India",
        "url": "https://www.linkedin.com/jobs/view/4455781999",
        "type": "Supply Chain & Operations Analytics",
        "target_keywords": ["supply chain", "inventory shrinkage", "vendor SLAs", "logistics analytics"]
    },
    {
        "company": "Amazon",
        "job_id": "4051593590",
        "title": "Financial Analyst Intern, Stores Finance",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4051593590",
        "type": "Finance & Analytics",
        "target_keywords": ["stores finance", "cost modeling", "financial analysis"]
    },
    {
        "company": "Amazon",
        "job_id": "4055834186",
        "title": "Finance Analyst Intern, Devices and Services Finance",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4055834186",
        "type": "Finance & Analytics",
        "target_keywords": ["finance analyst", "variance analysis", "budgeting"]
    },
    {
        "company": "Accenture in India",
        "job_id": "4448338203",
        "title": "Supply Chain Operations Senior Analyst",
        "location": "Bengaluru, India",
        "url": "https://www.linkedin.com/jobs/view/4448338203",
        "type": "Supply Chain Consulting",
        "target_keywords": ["supply chain", "logistics", "SLA compliance", "process improvement"]
    },
    {
        "company": "Accenture in India",
        "job_id": "4429242140",
        "title": "Business Advisory New Associate",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4429242140",
        "type": "Business Advisory",
        "target_keywords": ["business advisory", "consulting", "client delivery", "operations"]
    },
    {
        "company": "Accenture in India",
        "job_id": "4440553796",
        "title": "Business Advisory New Associate",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4440553796",
        "type": "Business Advisory",
        "target_keywords": ["advisory", "management consulting", "analytics"]
    },
    {
        "company": "PwC India",
        "job_id": "4409108662",
        "title": "Associate",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4409108662",
        "type": "Consulting & Assurance",
        "target_keywords": ["consulting", "advisory", "assurance", "business operations"]
    },
    {
        "company": "Razorpay",
        "job_id": "4439995783",
        "title": "Analyst - Business Operations",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4439995783",
        "type": "FinTech Business Operations",
        "target_keywords": ["fintech", "merchant operations", "settlement", "escalations"]
    },
    {
        "company": "Razorpay",
        "job_id": "4434954818",
        "title": "Analyst, Business Operations",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4434954818",
        "type": "FinTech Business Operations",
        "target_keywords": ["operations", "analytics", "client onboarding"]
    },
    {
        "company": "Razorpay",
        "job_id": "RAZORPAY_MERCHANT_004",
        "title": "Merchant Operations Specialist",
        "location": "Bengaluru, India",
        "url": "https://jobs.ashbyhq.com/razorpay",
        "type": "Merchant Operations",
        "target_keywords": ["merchant operations", "trade finance", "SLA management"]
    },
    {
        "company": "Microsoft",
        "job_id": "4379272973",
        "title": "Research Sciences INTERN",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4379272973",
        "type": "Research & Technology",
        "target_keywords": ["research", "data analysis", "technology"]
    },
    {
        "company": "Microsoft",
        "job_id": "4052096504",
        "title": "Product Management Intern",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4052096504",
        "type": "Product Management",
        "target_keywords": ["product roadmap", "user empathy", "metrics"]
    },
    {
        "company": "Cisco",
        "job_id": "4446332173",
        "title": "Data Analyst",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4446332173",
        "type": "Data Analytics",
        "target_keywords": ["data analytics", "reporting", "dashboarding", "operations"]
    },
    {
        "company": "HSBC",
        "job_id": "4452434953",
        "title": "Business Analyst",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4452434953",
        "type": "Banking & Operations Analysis",
        "target_keywords": ["banking operations", "business analysis", "financial workflows"]
    },
    {
        "company": "Swiggy",
        "job_id": "SWIGGY_OPS_001",
        "title": "Operations & Expansion Associate",
        "location": "Bengaluru, India",
        "url": "https://careers.swiggy.com",
        "type": "Hyperlocal Operations",
        "target_keywords": ["city operations", "partner SLAs", "fleet logistics"]
    },
    {
        "company": "Zepto",
        "job_id": "ZEPTO_OPS_002",
        "title": "City Operations Lead (Dark Store SCM)",
        "location": "Bengaluru, India",
        "url": "https://www.zeptonow.com/careers",
        "type": "Quick Commerce Operations",
        "target_keywords": ["dark store", "inventory shrinkage", "turnaround time", "supply chain"]
    },
    {
        "company": "Ather Energy",
        "job_id": "ATHER_SC_001",
        "title": "Supply Chain & Operations Lead",
        "location": "Bengaluru, India",
        "url": "https://www.atherenergy.com/careers",
        "type": "EV Supply Chain",
        "target_keywords": ["procurement", "vendor logistics", "operations"]
    },
    {
        "company": "Glean",
        "job_id": "4453740312",
        "title": "Cost & Commercial Operations Associate",
        "location": "Bengaluru, India",
        "url": "https://jobs.ashbyhq.com/glean",
        "type": "Commercial Operations",
        "target_keywords": ["commercial operations", "contract analysis", "procurement"]
    },
    {
        "company": "Postman",
        "job_id": "POSTMAN_OPS_003",
        "title": "Business Operations Analyst",
        "location": "Bengaluru, India",
        "url": "https://boards.greenhouse.io/postman",
        "type": "SaaS Operations",
        "target_keywords": ["revops", "business operations", "analytics"]
    },
    {
        "company": "Wrike",
        "job_id": "4440968428",
        "title": "Partner Operations Specialist",
        "location": "Bengaluru, India",
        "url": "https://boards.greenhouse.io/wrike",
        "type": "Partner Operations",
        "target_keywords": ["partner operations", "SLA tracking", "enablement"]
    },
    {
        "company": "Hilton",
        "job_id": "4450278984",
        "title": "Events Executive | Conrad Bengaluru",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4450278984",
        "type": "Hospitality & Event Management",
        "target_keywords": ["events executive", "hospitality logistics", "guest coordination"]
    },
    {
        "company": "JW Marriott",
        "job_id": "4436777567",
        "title": "Assistant Events Manager",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4436777567",
        "type": "Event Management",
        "target_keywords": ["events management", "banquet logistics", "VIP coordination"]
    },
    {
        "company": "Thomson Reuters",
        "job_id": "4446747144",
        "title": "Events Coordinator",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4446747144",
        "type": "Corporate Events",
        "target_keywords": ["events coordinator", "logistics", "vendor management"]
    },
    {
        "company": "MathWorks",
        "job_id": "4406706536",
        "title": "Marketing Event Specialist",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4406706536",
        "type": "Event Marketing",
        "target_keywords": ["event marketing", "technical conferences", "brand activation"]
    },
    {
        "company": "GlobalLogic",
        "job_id": "4451402094",
        "title": "Event Marketing Specialist IRC298882",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4451402094",
        "type": "Event Marketing",
        "target_keywords": ["event specialist", "marketing operations", "conferences"]
    },
    {
        "company": "Oracle",
        "job_id": "4048014873",
        "title": "Student / Intern",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4048014873",
        "type": "Technology Internship",
        "target_keywords": ["internship", "cloud infrastructure", "database"]
    },
    {
        "company": "CoinDCX",
        "job_id": "4424404412",
        "title": "Analyst - Operations",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4424404412",
        "type": "FinTech Operations",
        "target_keywords": ["operations analyst", "reconciliation", "compliance"]
    },
    {
        "company": "UST",
        "job_id": "4441571067",
        "title": "Business Operations Support",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4441571067",
        "type": "Business Operations",
        "target_keywords": ["operations support", "process documentation", "SLA tracking"]
    },
    {
        "company": "WNS",
        "job_id": "4430704372",
        "title": "Bangalore Walkins",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4430704372",
        "type": "Business Process Operations",
        "target_keywords": ["operations associate", "client delivery", "analytics"]
    },
    {
        "company": "Blissclub",
        "job_id": "4437012823",
        "title": "Business Analyst",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4437012823",
        "type": "D2C & Retail Analytics",
        "target_keywords": ["business analyst", "e-commerce analytics", "merchandising"]
    },
    {
        "company": "tokens&",
        "job_id": "4449673093",
        "title": "Operations Associate – Founder's Office (Remote)",
        "location": "Remote, India",
        "url": "http://www.linkedin.com/jobs/view/4449673093",
        "type": "Founder's Office Operations",
        "target_keywords": ["founder's office", "cross-functional execution", "growth ops"]
    },
    {
        "company": "BNI Global",
        "job_id": "4406514782",
        "title": "Event Logistics Coordinator",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4406514782",
        "type": "Event Logistics",
        "target_keywords": ["event logistics", "registration", "onsite coordination"]
    },
    {
        "company": "GalaxEye",
        "job_id": "4373303563",
        "title": "Market Research Intern",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4373303563",
        "type": "SpaceTech Market Research",
        "target_keywords": ["market research", "aerospace", "data analysis"]
    },
    {
        "company": "Tyfone, Inc.",
        "job_id": "4371505461",
        "title": "Business Intelligence & Data Analyst Intern",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4371505461",
        "type": "BI & Analytics",
        "target_keywords": ["business intelligence", "sql", "dashboarding", "data analyst"]
    },
    {
        "company": "Expedify",
        "job_id": "4374985662",
        "title": "AI Product Analytics Intern",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4374985662",
        "type": "AI Product Analytics",
        "target_keywords": ["product analytics", "ai", "user funnel"]
    },
    {
        "company": "Emergent",
        "job_id": "4439983503",
        "title": "AI Analyst - Business Analytics and Product Intelligence",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4439983503",
        "type": "AI & Business Analytics",
        "target_keywords": ["product intelligence", "business analytics", "data models"]
    },
    {
        "company": "Volvo Construction Equipment",
        "job_id": "4429029965",
        "title": "Graduate Apprentice Trainee",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4429029965",
        "type": "Operations & Engineering Trainee",
        "target_keywords": ["apprentice trainee", "manufacturing operations", "supply chain"]
    },
    {
        "company": "InspironLabs",
        "job_id": "4370182887",
        "title": "Management Trainee",
        "location": "Bengaluru, India",
        "url": "http://www.linkedin.com/jobs/view/4370182887",
        "type": "Management Trainee",
        "target_keywords": ["management trainee", "cross-functional operations"]
    }
]

# 3. Specific High-Leverage Named Connections Matched to Open Roles
named_targets = [
    {
        "name": "Syed Sumbul Shahbaz",
        "title": "Senior Executive HR",
        "company": "Goldman Sachs",
        "role_matched": "Global Banking & Markets Operations - IB Ops Client Onboarding Analyst (Bengaluru)",
        "job_id": "4452387165",
        "job_url": "http://www.linkedin.com/jobs/view/4452387165",
        "message": (
            "Hi Syed Sumbul,\n\n"
            "Hope you are having a productive week. I am reaching out regarding the open Global Banking & Markets Operations - IB Ops Client Onboarding Analyst position at Goldman Sachs Bengaluru (Job ID: 4452387165).\n\n"
            "As a final-year International Business candidate at Dayananda Sagar University, I bring proven ground execution in high-stakes SLA compliance, audit adherence, and vendor contract operations. Most recently, as Operations Lead at AERO INDIA 2025 (Yelahanka Air Force Station), I managed complex operations for 100,000+ attendees with zero security breaches and 0.0% shrinkage, alongside managing run-of-show logistics for enterprise activations like Tata Communications.\n\n"
            "I have applied directly on the portal and would be deeply grateful if you could route my profile for internal consideration or direct referral. May I send my resume across for your review?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Amisha Jat",
        "title": "Senior Operations Analyst",
        "company": "Goldman Sachs",
        "role_matched": "Global Banking & Markets Operations - IB Ops Client Onboarding Analyst",
        "job_id": "4452387165",
        "job_url": "http://www.linkedin.com/jobs/view/4452387165",
        "message": (
            "Hi Amisha,\n\n"
            "Hope you are doing well! I noticed the open Global Banking & Markets Operations - IB Ops Client Onboarding Analyst role (Job ID: 4452387165) in your department at Goldman Sachs Bengaluru.\n\n"
            "I'm a final-year International Business student at Dayananda Sagar University with a strong background in operational workflows, trade finance documentation, and high-density execution (Operations Lead at AERO INDIA 2025 with 100k+ footfall, 0 breaches, 0.0% shrinkage; and activations for Tata Communications).\n\n"
            "Would you be open to submitting an internal referral or connecting for a quick 5-minute chat about the team's culture and onboarding process? Truly appreciate your guidance!\n\n"
            "Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "ASHWINI CHANDRASHEKHAR",
        "title": "Manager - Talent Acquisition/Attraction",
        "company": "EY",
        "role_matched": "GDS Meetings and Events - Events Manager",
        "job_id": "4444908737",
        "job_url": "http://www.linkedin.com/jobs/view/4444908737",
        "message": (
            "Hi Ashwini,\n\n"
            "I hope this message finds you well. I am reaching out to express my strong enthusiasm for the GDS Meetings and Events - Events Manager role at EY Bengaluru (Job ID: 4444908737).\n\n"
            "I specialize in high-density event logistics and end-to-end operational execution. At AERO INDIA 2025, I served as Operations Lead at Yelahanka Air Force Station, overseeing crowd management, multi-vendor coordination, and inventory integrity for 100,000+ delegates with zero security breaches. In addition, I have managed high-pressure enterprise activations and run-of-show schedules for Tata Communications and Puma Global.\n\n"
            "Given my hands-on background in vendor SLA enforcement and high-profile corporate activations, I am confident in adding immediate value to EY GDS Events. Could we connect for a brief conversation regarding this opening?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Kinjal Chauhan",
        "title": "Relationship Manager - Talent Acquisition and Attraction",
        "company": "EY",
        "role_matched": "GDS Meetings and Events - Events Manager",
        "job_id": "4444908737",
        "job_url": "http://www.linkedin.com/jobs/view/4444908737",
        "message": (
            "Hi Kinjal,\n\n"
            "Hope you are having a great week! I am writing to bring my candidacy to your attention for the GDS Meetings and Events - Events Manager opening at EY (Job ID: 4444908737).\n\n"
            "With demonstrated execution as Operations Lead at AERO INDIA 2025 (100,000+ attendees at Yelahanka Air Force Base, 0 breaches, 0.0% shrinkage) and enterprise activations for Tata Communications and Puma Global, I bring rigorous vendor SLA contract governance, run-of-show logistics, and crisis escalation management.\n\n"
            "I have applied online and would welcome the chance to share my CV directly for your team's consideration. Thank you for your time!\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Sangini Sahay",
        "title": "Sourcing Recruiter",
        "company": "Amazon",
        "role_matched": "Event Program Manager, AWS Global Events / Supply Chain BA",
        "job_id": "4443027895 / 4455781999",
        "job_url": "http://www.linkedin.com/jobs/view/4443027895",
        "message": (
            "Hi Sangini,\n\n"
            "Hope you are well! I am writing regarding the Event Program Manager, AWS Global Events role (Job ID: 4443027895) and Business Analyst Support, IN Supply Chain (Job ID: 4455781999) at Amazon Bengaluru.\n\n"
            "My background combines rigorous analytical education in International Business at Dayananda Sagar University with proven ground-level event and supply chain execution. As Operations Lead at AERO INDIA 2025 (100,000+ footfall, 0 security breaches, 0.0% shrinkage) and run-of-show lead for Tata Communications & Puma Global, I specialize in Bias for Action, Deliver Results, and zero-defect SLA compliance.\n\n"
            "I would be grateful for the opportunity to have my profile considered for an interview loop. I'd be delighted to share my resume if you have a moment.\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Dipali Sharma",
        "title": "Business Development Manager",
        "company": "Amazon Web Services (AWS)",
        "role_matched": "Event Program Manager, AWS Global Events",
        "job_id": "4443027895",
        "job_url": "http://www.linkedin.com/jobs/view/4443027895",
        "message": (
            "Hi Dipali,\n\n"
            "Hope all is well with you. I noticed the Event Program Manager opening for AWS Global Events (Job ID: 4443027895) based out of Bengaluru.\n\n"
            "Having led large-scale operations at AERO INDIA 2025 at Yelahanka Air Force Station (100,000+ delegates, multi-tier security coordination, 0 shrinkage) and executed high-touch corporate activations for Tata Communications and Puma Global, I am deeply passionate about enterprise-scale event logistics and stakeholder experiences.\n\n"
            "Would you be open to referring me internally or putting me in touch with the hiring manager for AWS Global Events? Appreciate your support!\n\n"
            "Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Varsha G",
        "title": "Team Lead",
        "company": "JPMorganChase",
        "role_matched": "Data Management Associate",
        "job_id": "4440836681",
        "job_url": "http://www.linkedin.com/jobs/view/4440836681",
        "message": (
            "Hi Varsha,\n\n"
            "Hope you are doing well! I am reaching out regarding the Data Management Associate opening at JPMorganChase Bengaluru (Job ID: 4440836681).\n\n"
            "As a final-year International Business student at Dayananda Sagar University, I have developed strict data governance discipline, audit tracking, and operational rigor. During AERO INDIA 2025, I handled real-time reconciliation and operational logistics across 100k+ attendees with 0.0% shrinkage and 0 unresolved escalations.\n\n"
            "I would love the opportunity to join your operations ecosystem at JPMC. Could you consider referring my application or taking a quick glance at my profile?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Himanshi Sahu",
        "title": "Senior Corporate Recruiter",
        "company": "Accenture",
        "role_matched": "Business Advisory New Associate / Supply Chain Ops Analyst",
        "job_id": "4429242140 / 4448338203",
        "job_url": "http://www.linkedin.com/jobs/view/4429242140",
        "message": (
            "Hi Himanshi,\n\n"
            "Hope you are having a wonderful week. I am reaching out regarding the Business Advisory New Associate (Job ID: 4429242140 / 4440553796) and Supply Chain Operations Senior Analyst (Job ID: 4448338203) roles at Accenture in India.\n\n"
            "I graduate this year in International Business from Dayananda Sagar University. My practical background includes leading field operations at AERO INDIA 2025 (100k+ attendees, 0 breaches, 0.0% shrinkage) and vendor SLA enforcement for enterprise activations with Tata Communications and Puma Global.\n\n"
            "I have registered on the Accenture candidate portal and would love to have my profile reviewed for these positions. May I forward my CV to your email for direct routing?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Nikhitha Simon",
        "title": "HR Business Partner",
        "company": "PwC",
        "role_matched": "Associate",
        "job_id": "4409108662",
        "job_url": "http://www.linkedin.com/jobs/view/4409108662",
        "message": (
            "Hi Nikhitha,\n\n"
            "Hope you are well! I am writing to share my application for the Associate position at PwC India (Job ID: 4409108662).\n\n"
            "I bring strong analytical and operational grounding from my International Business degree at Dayananda Sagar University, bolstered by high-accountability execution as Operations Lead at AERO INDIA 2025 (100k+ visitors, 0 security infractions, 0 shrinkage) and corporate logistics for Tata Communications.\n\n"
            "I would be honored to be considered for PwC's advisory/consulting practice. Could we connect or may I share my resume directly with you for review?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Pinki Kumari",
        "title": "Junior Analyst",
        "company": "Razorpay",
        "role_matched": "Analyst - Business Operations / Merchant Operations Specialist",
        "job_id": "4439995783 / RAZORPAY_MERCHANT_004",
        "job_url": "http://www.linkedin.com/jobs/view/4439995783",
        "message": (
            "Hi Pinki,\n\n"
            "Hope you're having a good week! I noticed Razorpay is hiring for the Analyst - Business Operations role (Job ID: 4439995783) and Merchant Operations Specialist in Bengaluru.\n\n"
            "I'm graduating in International Business from Dayananda Sagar University with hands-on experience in vendor contracts, operational reconciliation, and multi-stakeholder management (Operations Lead at AERO INDIA 2025 and activations for Tata Communications with zero unresolved escalations).\n\n"
            "Would you be open to referring me internally or sharing a word of advice on the team's interview process? Would really appreciate your help!\n\n"
            "Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Shimna M",
        "title": "Talent Advisor",
        "company": "Cisco",
        "role_matched": "Data Analyst",
        "job_id": "4446332173",
        "job_url": "http://www.linkedin.com/jobs/view/4446332173",
        "message": (
            "Hi Shimna,\n\n"
            "I hope you are well. I am reaching out regarding the Data Analyst opening at Cisco Bengaluru (Job ID: 4446332173).\n\n"
            "I am completing my International Business degree at Dayananda Sagar University, combining quantitative data analysis, SLA metrics tracking, and operational leadership (Operations Lead at AERO INDIA 2025 for 100,000+ delegates with 0 shrinkage and 0 breaches).\n\n"
            "I would welcome the opportunity to submit my resume for internal review. Could we connect briefly regarding this role?\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624 | Bengaluru"
        )
    },
    {
        "name": "Archana Rao Sarrgur",
        "title": "Manager - Leadership Hiring",
        "company": "HSBC",
        "role_matched": "Business Analyst",
        "job_id": "4452434953",
        "job_url": "http://www.linkedin.com/jobs/view/4452434953",
        "message": (
            "Hi Archana,\n\n"
            "Hope you are having a productive week! I am writing regarding the Business Analyst position at HSBC Bengaluru (Job ID: 4452434953).\n\n"
            "With an academic foundation in International Business from Dayananda Sagar University and field experience handling large-scale SLA execution, financial reconciliation, and vendor contract enforcement (AERO INDIA 2025 and Tata Communications activations), I am eager to contribute to HSBC's global operations.\n\n"
            "I have applied online and would be grateful if you could direct my profile to the relevant hiring team. Thank you for your consideration!\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Prerna Khedkar",
        "title": "Senior Executive Human Resources",
        "company": "Swiggy",
        "role_matched": "Operations & Expansion Associate",
        "job_id": "SWIGGY_OPS_001",
        "job_url": "https://careers.swiggy.com",
        "message": (
            "Hi Prerna,\n\n"
            "Hope all is well! I am reaching out to share my interest in Swiggy's Operations & Expansion Associate openings in Bengaluru.\n\n"
            "Having led mission-critical operations at AERO INDIA 2025 (managing high-density logistics for 100,000+ footfall with 0 breaches and 0.0% shrinkage) and driven vendor SLA enforcement for Tata Communications, I thrive in fast-paced operational ecosystems with strict delivery metrics.\n\n"
            "Could I share my CV with you for upcoming operations and expansion hiring batches? Would love to connect!\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Yashaswini L",
        "title": "Talent Acquisition Specialist",
        "company": "Zepto",
        "role_matched": "City Operations Lead / Dark Store SCM",
        "job_id": "ZEPTO_OPS_002",
        "job_url": "https://www.zeptonow.com/careers",
        "message": (
            "Hi Yashaswini,\n\n"
            "Hope you are having a great week! I am reaching out regarding operations and dark store management opportunities at Zepto Bengaluru.\n\n"
            "My experience is centered on fast-turnaround inventory control, loss prevention, and SLA compliance. As Operations Lead at AERO INDIA 2025, I handled high-throughput stock and delegate logistics for 100,000+ attendees with a proven 0.0% shrinkage record and zero unresolved escalations across multi-vendor contracts.\n\n"
            "I'm keen to bring this rigorous discipline to Zepto's quick commerce operations. May I share my resume with you for consideration?\n\n"
            "Warm regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    },
    {
        "name": "Nupur Niswan Pal",
        "title": "Assistant Manager Finance",
        "company": "Hilton",
        "role_matched": "Events Executive | Conrad Bengaluru",
        "job_id": "4450278984",
        "job_url": "http://www.linkedin.com/jobs/view/4450278984",
        "message": (
            "Hi Nupur,\n\n"
            "Hope you are doing well! I noticed the opening for Events Executive at Conrad Bengaluru by Hilton (Job ID: 4450278984).\n\n"
            "Having managed high-stakes event operations at AERO INDIA 2025 (100,000+ delegates, zero security infractions, 0.0% shrinkage) and enterprise activations for Puma Global and Tata Communications, I have deep respect for luxury guest experiences, run-of-show precision, and budget discipline.\n\n"
            "Would you be open to referring me internally or introducing me to the events hiring team? Appreciate your time and guidance!\n\n"
            "Best regards,\nAditya Mehra\nashishiash007@gmail.com | +91 7003456624"
        )
    }
]

# 4. Generate Interactive Web Hub
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Roles & LinkedIn Outreach Command Center</title>
<style>
  :root {{
    --bg: #090d16;
    --card: #131c2e;
    --card-hover: #1a2740;
    --border: #23324d;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.25);
    --green: #22c55e;
    --tag-bg: rgba(56, 189, 248, 0.12);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding: 24px; min-height: 100vh; }}
  .container {{ max-width: 1400px; margin: 0 auto; }}
  header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
  h1 {{ font-size: 24px; font-weight: 700; color: #fff; }}
  .subtitle {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
  
  .tabs {{ display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  .tab-btn {{ background: transparent; border: none; color: var(--text-muted); font-size: 15px; font-weight: 600; padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s; }}
  .tab-btn.active {{ background: var(--card); color: var(--accent); border: 1px solid var(--border); }}
  
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  
  .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 20px; }}
  .msg-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }}
  .card-header {{ margin-bottom: 14px; }}
  .contact-name {{ font-size: 18px; font-weight: 700; color: #fff; }}
  .contact-title {{ color: var(--accent); font-size: 13px; font-weight: 500; margin-top: 2px; }}
  .company-tag {{ display: inline-block; background: var(--tag-bg); color: var(--accent); padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; border: 1px solid rgba(56, 189, 248, 0.3); margin-top: 8px; }}
  .job-target {{ margin-top: 10px; font-size: 13px; color: var(--text-muted); }}
  .job-id-badge {{ background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); padding: 1px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; }}
  
  .message-box {{ background: #0c1322; border: 1px solid #1a2740; border-radius: 6px; padding: 14px; font-size: 13px; line-height: 1.5; color: #cbd5e1; white-space: pre-wrap; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 12px 0; max-height: 240px; overflow-y: auto; }}
  
  .action-bar {{ display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }}
  .copy-btn {{ background: #0284c7; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }}
  .copy-btn:hover {{ background: #0369a1; }}
  .copy-btn.copied {{ background: #16a34a; }}
  .job-link {{ color: var(--accent); text-decoration: none; font-size: 13px; font-weight: 500; }}
  .job-link:hover {{ text-decoration: underline; }}
  
  /* Table styling for roles */
  table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
  th {{ background: #0c1322; padding: 12px 16px; color: var(--text-muted); font-weight: 600; border-bottom: 1px solid var(--border); }}
  td {{ padding: 12px 16px; border-bottom: 1px solid var(--border); vertical-align: middle; }}
  tr:hover td {{ background: var(--card-hover); }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>Job Requisition & LinkedIn Outreach Command Center</h1>
      <div class="subtitle">Candidate: <strong>Aditya Mehra</strong> | Bengaluru | AERO INDIA 2025 Operations Lead & DSU Graduate</div>
    </div>
  </header>

  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tab-contacts')">Personalized Messages for Connections ({len(named_targets)})</button>
    <button class="tab-btn" onclick="switchTab('tab-roles')">All Open Roles with Job IDs ({len(open_roles)})</button>
    <button class="tab-btn" onclick="switchTab('tab-templates')">Plug-and-Play Outreach Templates</button>
  </div>

  <!-- Tab 1: Named Contacts -->
  <div id="tab-contacts" class="tab-content active">
    <div class="card-grid">
'''

for idx, target in enumerate(named_targets):
    escaped_msg = target["message"].replace('`', '\\`')
    html_template += f'''
      <div class="msg-card">
        <div class="card-header">
          <div class="contact-name">{target["name"]}</div>
          <div class="contact-title">{target["title"]}</div>
          <span class="company-tag">{target["company"]}</span>
          <div class="job-target">
            Role: <strong>{target["role_matched"]}</strong><br>
            Job ID: <span class="job-id-badge">{target["job_id"]}</span>
          </div>
        </div>
        <div class="message-box" id="msg-{idx}">{target["message"]}</div>
        <div class="action-bar">
          <a href="{target["job_url"]}" target="_blank" class="job-link">View Job Posting &nearr;</a>
          <button class="copy-btn" onclick="copyText('msg-{idx}', this)">Copy Outreach Message</button>
        </div>
      </div>
    '''

html_template += '''
    </div>
  </div>

  <!-- Tab 2: All Open Roles Table -->
  <div id="tab-roles" class="tab-content">
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>Job ID</th>
          <th>Job Title</th>
          <th>Domain / Type</th>
          <th>Location</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
'''

for role in open_roles:
    html_template += f'''
        <tr>
          <td style="font-weight:600; color:#fff;">{role["company"]}</td>
          <td><span class="job-id-badge">{role["job_id"]}</span></td>
          <td>{role["title"]}</td>
          <td style="color:var(--accent); font-size:13px;">{role["type"]}</td>
          <td style="color:var(--text-muted);">{role["location"]}</td>
          <td><a href="{role["url"]}" target="_blank" class="job-link">Apply / View &nearr;</a></td>
        </tr>
    '''

html_template += '''
      </tbody>
    </table>
  </div>

  <!-- Tab 3: Templates -->
  <div id="tab-templates" class="tab-content">
    <div class="card-grid">
      <div class="msg-card">
        <div class="card-header">
          <div class="contact-name">Template 1: Recruiter / Talent Acquisition Specialist</div>
          <div class="contact-title">Direct Job ID Application Referral</div>
        </div>
        <div class="message-box" id="tmpl-1">Hi [Recruiter Name],

Hope you are having a productive week! I recently submitted my application for the [Job Title] role at [Company] (Job ID: [Job ID]).

As an International Business graduate from Dayananda Sagar University, I combine analytical operations grounding with on-the-ground execution. Most recently, as Operations Lead at AERO INDIA 2025 (Yelahanka Air Base), I led high-density crowd logistics and vendor operations for 100,000+ delegates with zero security breaches and 0.0% shrinkage, alongside managing run-of-show logistics for Tata Communications and Puma Global.

Given my verified track record in strict SLA compliance and operational rigor, I would be grateful for the opportunity to have my profile considered for the interview loop. May I share my resume directly with you?

Best regards,
Aditya Mehra
ashishiash007@gmail.com | +91 7003456624 | Bengaluru</div>
        <div class="action-bar">
          <button class="copy-btn" onclick="copyText('tmpl-1', this)">Copy Template</button>
        </div>
      </div>

      <div class="msg-card">
        <div class="card-header">
          <div class="contact-name">Template 2: Hiring Manager / Operations Lead</div>
          <div class="contact-title">Direct Team Impact & 5-Min Coffee Chat</div>
        </div>
        <div class="message-box" id="tmpl-2">Hi [Manager Name],

Hope you're having a great week! I came across the open [Job Title] position (Job ID: [Job ID]) within your group at [Company].

My background is centered on high-accountability execution: leading operations at AERO INDIA 2025 across 100k+ attendees (0 breaches, 0.0% inventory shrinkage) and enforcing multi-vendor contract SLAs for Tata Communications with zero unresolved escalations.

I would love to learn more about the team's operational goals and explore how my execution rigor can take pressure off your team. Would you be open to a brief 5-minute conversation sometime this week?

Warm regards,
Aditya Mehra
ashishiash007@gmail.com | +91 7003456624 | Bengaluru</div>
        <div class="action-bar">
          <button class="copy-btn" onclick="copyText('tmpl-2', this)">Copy Template</button>
        </div>
      </div>

      <div class="msg-card">
        <div class="card-header">
          <div class="contact-name">Template 3: College Alumni (Christ Univ / DSU)</div>
          <div class="contact-title">Warm Internal Referral Ask</div>
        </div>
        <div class="message-box" id="tmpl-3">Hi [Alumni Name],

Hope you are doing well! As a fellow [Dayananda Sagar / Christ University] student, it's wonderful seeing your journey at [Company].

I'm currently applying for the [Job Title] role (Job ID: [Job ID]) at [Company] Bengaluru. My background includes leading operations at AERO INDIA 2025 (100k+ attendees, 0 security infractions, 0 shrinkage) and vendor logistics for Tata Communications.

If you have a quick minute, would you be comfortable submitting an internal employee referral for my application? I can send over my resume and the job requisition link right away.

Thank you so much for your support!

Best regards,
Aditya Mehra
ashishiash007@gmail.com | +91 7003456624</div>
        <div class="action-bar">
          <button class="copy-btn" onclick="copyText('tmpl-3', this)">Copy Template</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

function copyText(elementId, btn) {
  const text = document.getElementById(elementId).innerText;
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btn.innerText;
    btn.innerText = '✓ Copied to Clipboard!';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.innerText = originalText;
      btn.classList.remove('copied');
    }, 2000);
  });
}
</script>
</body>
</html>
'''

output_hub = r'e:\anti\linkedin_export\outreach_messages_hub.html'
with open(output_hub, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f'Successfully created {output_hub}')
