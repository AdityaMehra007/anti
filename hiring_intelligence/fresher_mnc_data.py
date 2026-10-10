"""
Database of global MNCs, Fortune 500, Big Tech, and Tier-1 IT/Finance giants
specifically hiring Freshers, New Grads, and Entry-Level Candidates (Batch 2024, 2025, 2026).
"""

MNC_FRESHER_DATA = [
    # -------------------------------------------------------------
    # 1. BIG TECH & PRODUCT MULTINATIONAL CORPORATIONS (MNCs)
    # -------------------------------------------------------------
    {
        "name": "Google",
        "slug": "google-alphabet",
        "domain": "careers.google.com",
        "industry": "Big Tech / Search, Cloud & AI",
        "stage": "Public (NASDAQ: GOOGL)",
        "total_funding_usd": 1800000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 2100000000000,
        "lead_investors": "Publicly Traded / Institutional",
        "headcount": 182000,
        "headcount_growth_6m_pct": 5.0,
        "hq_location": "Mountain View, CA / Global / India (BLR, HYD)",
        "remote_friendly": 1,
        "careers_url": "https://careers.google.com/students/",
        "ats_provider": "Internal Custom ATS",
        "ats_endpoint": "https://careers.google.com/jobs/results/?employment_type=FULL_TIME&experience_level=INTERN_AND_EARLY_CAREER",
        "verified_active": 1,
        "roles": [
            {
                "title": "Software Engineer, Early Career (Campus / Off-Campus)",
                "department": "Core Engineering / Google Cloud",
                "seniority_level": "Fresher / SDE-1 / L3",
                "salary_min_usd": 140000,
                "salary_max_usd": 185000,
                "equity_note": "INR 25 - 45 LPA (India) / $140k - $185k (US) + GSUs",
                "tech_stack": "C++, Java, Python, Go, DSA, Distributed Systems",
                "location": "Bangalore / Hyderabad / Bay Area / NYC / Remote US",
                "remote_type": "Hybrid (3 Days Office)",
                "direct_apply_url": "https://www.google.com/about/careers/applications/jobs/results/?target_level=EARLY",
                "urgency_score": 9.9,
                "batch_eligibility": "2024, 2025, 2026 Batch Graduates",
                "min_cgpa": "6.5 / 65% No active backlogs",
                "test_pattern": "Google Online Challenge (GOC): 2 Hard DSA Problems (Graphs, DP, Trees) + 3 Technical Rounds",
            }
        ],
        "decision_makers": [
            {
                "full_name": "University Programs Lead",
                "title": "Head of University Recruiting APAC & AMER",
                "department": "University Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/google/jobs",
                "twitter_handle": "@GoogleCareers",
                "verified_email": "universityrecruiting@google.com",
                "direct_pitch_hook": "Candidate with top 5% LeetCode/Codeforces rating and published distributed systems project.",
            }
        ],
        "signals": [
            {
                "signal_type": "CAMPUS_DRIVE_ACTIVE",
                "source": "Google Students Hub",
                "signal_date": "2026-09-01",
                "description": "Annual University Graduate Software Engineer hiring portal opened globally.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Microsoft",
        "slug": "microsoft",
        "domain": "careers.microsoft.com",
        "industry": "Enterprise Software, Cloud & AI",
        "stage": "Public (NASDAQ: MSFT)",
        "total_funding_usd": 3000000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 3100000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 221000,
        "headcount_growth_6m_pct": 6.0,
        "hq_location": "Redmond, WA / India (HYD, BLR, NOIDA)",
        "remote_friendly": 1,
        "careers_url": "https://careers.microsoft.com/students/us/en",
        "ats_provider": "Internal Microsoft ATS",
        "ats_endpoint": "https://jobs.careers.microsoft.com/global/en/search?q=university",
        "verified_active": 1,
        "roles": [
            {
                "title": "Software Engineer - University Graduate (Full Time)",
                "department": "Azure / Developer Division / Windows & AI",
                "seniority_level": "Fresher / Level 59-60",
                "salary_min_usd": 130000,
                "salary_max_usd": 170000,
                "equity_note": "INR 22 - 44 LPA (India) / $130k - $170k (US) + Stock Units",
                "tech_stack": "C#, C++, TypeScript, Python, Azure, Cloud Internals",
                "location": "Hyderabad / Bangalore / Noida / Redmond, WA",
                "remote_type": "Hybrid / Flexible",
                "direct_apply_url": "https://jobs.careers.microsoft.com/global/en/search?exp=Students%20and%20graduates",
                "urgency_score": 9.8,
                "batch_eligibility": "2024, 2025, 2026 Batch (B.Tech / M.Tech / MCA)",
                "min_cgpa": "7.0 CGPA",
                "test_pattern": "Codility OA (3 Coding Questions in 75 mins) + 3 Technical Rounds (OOPs, System Architecture, DSA)",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Microsoft Campus Talent Team",
                "title": "University Recruiting Program Manager",
                "department": "Global Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/microsoft/jobs",
                "twitter_handle": "@MicrosoftJobs",
                "verified_email": "msuniversity@microsoft.com",
                "direct_pitch_hook": "Strong hands-on cloud native project deployed on Azure/K8s with clean unit test coverage.",
            }
        ],
        "signals": [
            {
                "signal_type": "OFF_CAMPUS_DRIVE",
                "source": "Microsoft Careers Portal",
                "signal_date": "2026-08-15",
                "description": "Global student graduate batches opened for Azure and Copilot developer teams.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Amazon",
        "slug": "amazon",
        "domain": "amazon.jobs",
        "industry": "Cloud Infrastructure, E-Commerce & AI",
        "stage": "Public (NASDAQ: AMZN)",
        "total_funding_usd": 1900000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 1950000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 1500000,
        "headcount_growth_6m_pct": 4.0,
        "hq_location": "Seattle, WA / India (BLR, HYD, CHENNAI, DELHI)",
        "remote_friendly": 1,
        "careers_url": "https://www.amazon.jobs/en/business_categories/student-programs",
        "ats_provider": "Internal Amazon Portal",
        "ats_endpoint": "https://www.amazon.jobs/en/search?category[]=software-development&country[]=IND&country[]=USA&type[]=university-recruiting",
        "verified_active": 1,
        "roles": [
            {
                "title": "Software Development Engineer I (SDE-1 - University Recruiting)",
                "department": "AWS / Consumer / Prime Video / Alexa",
                "seniority_level": "Fresher / SDE-1 / L4",
                "salary_min_usd": 135000,
                "salary_max_usd": 180000,
                "equity_note": "INR 28 - 48 LPA (India) / $135k - $180k (US) + Sign-on Bonus",
                "tech_stack": "Java, Python, C++, AWS, DynamoDB, Microservices, DSA",
                "location": "Bangalore / Hyderabad / Chennai / Seattle / Arlington",
                "remote_type": "Onsite / Hybrid (3 Days)",
                "direct_apply_url": "https://www.amazon.jobs/en/landing_pages/software-development-topics",
                "urgency_score": 9.9,
                "batch_eligibility": "2024, 2025, 2026 Passed Out / Passing Batches",
                "min_cgpa": "6.5 / 65%",
                "test_pattern": "Amazon OA: 2 Coding Problems + Work Simulation Assessment + Amazon 16 Leadership Principles (LPs)",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Student Programs Lead",
                "title": "Head of University Recruiting APAC & Americas",
                "department": "University Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/amazon/jobs",
                "twitter_handle": "@AmazonJobs",
                "verified_email": "student-recruiting@amazon.com",
                "direct_pitch_hook": "Candidate demonstrates extreme Customer Obsession and high coding velocity with clean Java/C++ DSA.",
            }
        ],
        "signals": [
            {
                "signal_type": "AWS_HIRING_SURGE",
                "source": "Amazon Jobs Feed",
                "signal_date": "2026-09-12",
                "description": "AWS Generative AI infrastructure and core commerce SDE-1 university listings refreshed.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "NVIDIA",
        "slug": "nvidia",
        "domain": "nvidia.com",
        "industry": "GPU Computing, AI Hardware & CUDA Systems",
        "stage": "Public (NASDAQ: NVDA)",
        "total_funding_usd": 3200000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 3200000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 30000,
        "headcount_growth_6m_pct": 25.0,
        "hq_location": "Santa Clara, CA / India (BLR, PUNE, HYD)",
        "remote_friendly": 1,
        "careers_url": "https://www.nvidia.com/en-us/about-nvidia/careers/university-recruiting/",
        "ats_provider": "Workday",
        "ats_endpoint": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
        "verified_active": 1,
        "roles": [
            {
                "title": "System Software Engineer - New College Graduate",
                "department": "CUDA & Accelerated Computing",
                "seniority_level": "Fresher / Level IC-1",
                "salary_min_usd": 145000,
                "salary_max_usd": 195000,
                "equity_note": "INR 28 - 50 LPA (India) / $145k - $195k (US) + Generous ESPP",
                "tech_stack": "C, C++, CUDA, Linux Internals, Computer Architecture, PyTorch",
                "location": "Bangalore / Pune / Santa Clara, CA / Austin, TX",
                "remote_type": "Hybrid",
                "direct_apply_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q=University",
                "urgency_score": 9.9,
                "batch_eligibility": "2024, 2025, 2026 Batch",
                "min_cgpa": "7.5 CGPA / 75%",
                "test_pattern": "Technical Test: C/C++ Pointers, Memory Management, OS Semaphores, Computer Architecture + 3 Live Coding Rounds",
            }
        ],
        "decision_makers": [
            {
                "full_name": "NVIDIA Campus Hiring Team",
                "title": "Director of University Talent",
                "department": "Campus Recruiting",
                "linkedin_url": "https://linkedin.com/company/nvidia/jobs",
                "twitter_handle": "@NVIDIACareers",
                "verified_email": "universityrecruiting@nvidia.com",
                "direct_pitch_hook": "Kernel optimization experience, parallel programming with CUDA, and GPU memory understanding.",
            }
        ],
        "signals": [
            {
                "signal_type": "EXPANSION_MASSIVE",
                "source": "NVIDIA Press",
                "signal_date": "2026-08-20",
                "description": "Massive compute center expansion fueling hundreds of early career systems engineering positions.",
                "weight": 2.0,
            }
        ]
    },

    # -------------------------------------------------------------
    # 2. GLOBAL INVESTMENT BANKS & FINANCIAL MNCs (HIGH CTC FRESHER)
    # -------------------------------------------------------------
    {
        "name": "JPMorgan Chase & Co.",
        "slug": "jpmorgan-chase",
        "domain": "careers.jpmorgan.com",
        "industry": "Global Investment Banking & Financial Services",
        "stage": "Public (NYSE: JPM)",
        "total_funding_usd": 550000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 580000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 310000,
        "headcount_growth_6m_pct": 8.0,
        "hq_location": "New York, NY / India (BLR, HYD, MUMBAI)",
        "remote_friendly": 1,
        "careers_url": "https://careers.jpmorgan.com/global/en/students/programs",
        "ats_provider": "Oracle Cloud HCM",
        "ats_endpoint": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001",
        "verified_active": 1,
        "roles": [
            {
                "title": "Software Engineer Program (SEP) - Full Time Analyst",
                "department": "Corporate & Investment Bank Technology",
                "seniority_level": "Fresher / Analyst Level",
                "salary_min_usd": 115000,
                "salary_max_usd": 140000,
                "equity_note": "INR 18 - 25 LPA (India) / $115k - $140k (US) + Annual Bonus",
                "tech_stack": "Java, Spring Boot, Python, React, Cloud, SQL, Distributed Ledger",
                "location": "Bangalore / Hyderabad / Mumbai / New York / London",
                "remote_type": "Hybrid (Office Based)",
                "direct_apply_url": "https://careers.jpmorgan.com/global/en/students/programs/software-engineer-fulltime-program",
                "urgency_score": 9.7,
                "batch_eligibility": "2024, 2025, 2026 Batch Graduates",
                "min_cgpa": "7.0 CGPA / 70%",
                "test_pattern": "HackerRank OA (2 Coding Questions) + HireVue Video Interview + 'Code for Good' Hackathon or SuperDay Rounds",
            }
        ],
        "decision_makers": [
            {
                "full_name": "JPMC University Recruiting",
                "title": "Head of Campus Talent Acquisition",
                "department": "Global Technology Recruiting",
                "linkedin_url": "https://linkedin.com/company/jpmorganchase/jobs",
                "twitter_handle": "@JPMorganJobs",
                "verified_email": "sep.recruiting@jpmchase.com",
                "direct_pitch_hook": "High-throughput financial ledger processing simulation with robust concurrency and ACID semantics.",
            }
        ],
        "signals": [
            {
                "signal_type": "CODE_FOR_GOOD_DRIVE",
                "source": "JPMorgan Campus Bulletin",
                "signal_date": "2026-08-01",
                "description": "Annual SEP full-time analyst hiring launched across premier engineering institutions globally.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Goldman Sachs",
        "slug": "goldman-sachs",
        "domain": "goldmansachs.com",
        "industry": "Global Investment Banking & Asset Management",
        "stage": "Public (NYSE: GS)",
        "total_funding_usd": 160000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 170000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 48000,
        "headcount_growth_6m_pct": 5.0,
        "hq_location": "New York, NY / India (BLR, HYD)",
        "remote_friendly": 0,
        "careers_url": "https://www.goldmansachs.com/careers/students/programs",
        "ats_provider": "Internal Custom ATS",
        "ats_endpoint": "https://www.goldmansachs.com/careers/students/programs/new-analyst-program.html",
        "verified_active": 1,
        "roles": [
            {
                "title": "Engineering Campus Analyst (New Analyst Program)",
                "department": "Global Banking & Markets Engineering",
                "seniority_level": "Fresher / Analyst Level",
                "salary_min_usd": 125000,
                "salary_max_usd": 150000,
                "equity_note": "INR 22 - 32 LPA (India) / $125k - $150k (US) + Discretionary Performance Bonus",
                "tech_stack": "Java, C++, Python, Slang/SecDB, Distributed Caching, Kafka",
                "location": "Bangalore / Hyderabad / New York / London / Singapore",
                "remote_type": "In-Office (High Touch)",
                "direct_apply_url": "https://www.goldmansachs.com/careers/students/programs/new-analyst-program.html",
                "urgency_score": 9.8,
                "batch_eligibility": "2024, 2025, 2026 Batch Graduates",
                "min_cgpa": "6.8 / 68%",
                "test_pattern": "HackerRank Aptitude & Coding OA (Math, Probability, CS Core, 2 DSA Problems) + 3 Technical Video Interviews",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Goldman Sachs University Recruiting",
                "title": "Head of New Analyst Sourcing",
                "department": "Campus Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/goldman-sachs/jobs",
                "twitter_handle": "@GSCareers",
                "verified_email": "campusrecruiting@gs.com",
                "direct_pitch_hook": "Strong foundation in data structures, mathematical probability, and low-latency execution systems.",
            }
        ],
        "signals": [
            {
                "signal_type": "NEW_ANALYST_DRIVE",
                "source": "Goldman Sachs Portal",
                "signal_date": "2026-07-20",
                "description": "Global New Analyst Applications officially opened for incoming graduate cohorts.",
                "weight": 2.0,
            }
        ]
    },

    # -------------------------------------------------------------
    # 3. GLOBAL IT, CONSULTING & SERVICES MNCs (MASS & PRIME HIRING)
    # -------------------------------------------------------------
    {
        "name": "Tata Consultancy Services (TCS)",
        "slug": "tcs",
        "domain": "tcs.com",
        "industry": "Global IT Services & Digital Transformation",
        "stage": "Public (NSE: TCS)",
        "total_funding_usd": 160000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 165000000000,
        "lead_investors": "Tata Sons / Public",
        "headcount": 615000,
        "headcount_growth_6m_pct": 7.0,
        "hq_location": "Mumbai, India / Global Across 55 Countries",
        "remote_friendly": 0,
        "careers_url": "https://www.tcs.com/careers/india/entry-level",
        "ats_provider": "TCS iON Portal",
        "ats_endpoint": "https://www.tcs.com/careers/india/tcs-national-qualifier-test",
        "verified_active": 1,
        "roles": [
            {
                "title": "TCS Prime / Digital / Ninja Software Engineer",
                "department": "Cognitive Business Operations & Digital Labs",
                "seniority_level": "Fresher (3 Bands: Ninja, Digital, Prime)",
                "salary_min_usd": 45000,
                "salary_max_usd": 65000,
                "equity_note": "Ninja: 3.6 LPA | Digital: 7.2 LPA | Prime: 9.5 - 11.5 LPA (India) + Overseas Allowances",
                "tech_stack": "Java, Python, C++, SQL, Cloud, Web Technologies, GenAI Basics",
                "location": "Pan-India (Bangalore, Chennai, Hyderabad, Pune, Kolkata, Noida, Mumbai)",
                "remote_type": "Onsite / Hybrid (Office Mandate)",
                "direct_apply_url": "https://nextstep.tcs.com/campus/#/",
                "urgency_score": 9.6,
                "batch_eligibility": "2024, 2025, 2026 Batch (B.E / B.Tech / M.E / M.Tech / MCA / M.Sc)",
                "min_cgpa": "60% or 6.0 CGPA throughout 10th, 12th, and Degree / Max 1 Active Backlog",
                "test_pattern": "TCS National Qualifier Test (NQT): Cognitive (Verbal, Reasoning, Numerical) + Advanced Coding (2 DSA Questions)",
            }
        ],
        "decision_makers": [
            {
                "full_name": "TCS Talent Acquisition Lead",
                "title": "Head of Global Campus Recruitment",
                "department": "Human Resources / Campus Hiring",
                "linkedin_url": "https://linkedin.com/company/tata-consultancy-services/jobs",
                "twitter_handle": "@TCS_Careers",
                "verified_email": "careers@tcs.com",
                "direct_pitch_hook": "Candidate cleared advanced TCS NQT coding section with full marks in dynamic programming and string algorithms.",
            }
        ],
        "signals": [
            {
                "signal_type": "NATIONAL_QUALIFIER_DRIVE",
                "source": "TCS NextStep Portal",
                "signal_date": "2026-09-01",
                "description": "Massive National Qualifier Test (NQT) onboarding drive announced for 40,000+ freshers.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Accenture",
        "slug": "accenture",
        "domain": "accenture.com",
        "industry": "Global Management & Technology Consulting",
        "stage": "Public (NYSE: ACN)",
        "total_funding_usd": 220000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 230000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 750000,
        "headcount_growth_6m_pct": 6.0,
        "hq_location": "Dublin, Ireland / Pan-India & Global",
        "remote_friendly": 1,
        "careers_url": "https://www.accenture.com/in-en/careers/local/entry-level",
        "ats_provider": "Workday",
        "ats_endpoint": "https://indiacampus.accenture.com/",
        "verified_active": 1,
        "roles": [
            {
                "title": "Associate Software Engineer (ASE) & Advanced ASE (AASE)",
                "department": "Technology Delivery Centers",
                "seniority_level": "Fresher (ASE / AASE)",
                "salary_min_usd": 50000,
                "salary_max_usd": 75000,
                "equity_note": "ASE: INR 4.5 LPA | Advanced ASE: INR 6.5 - 11 LPA + Joining Bonus",
                "tech_stack": "Java, Cloud Platforms (AWS/Azure), Full Stack Web, SQL, Python",
                "location": "Bangalore / Hyderabad / Pune / Chennai / Gurgaon / Kolkata / Mumbai",
                "remote_type": "Hybrid",
                "direct_apply_url": "https://indiacampus.accenture.com/candidate-registration",
                "urgency_score": 9.5,
                "batch_eligibility": "2024, 2025, 2026 Batch (All Engineering Branches & MCA)",
                "min_cgpa": "65% or 6.5 CGPA throughout education",
                "test_pattern": "Assessment Stage 1: Cognitive & Technical (English, Reasoning, MS Office, Cloud basics, Pseudo Code) + Stage 2: Coding (2 Questions) + Communication Round",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Accenture Campus Operations",
                "title": "Lead Early Career Talent Acquisition",
                "department": "University & Fresher Hiring",
                "linkedin_url": "https://linkedin.com/company/accenture/jobs",
                "twitter_handle": "@AccentureJobs",
                "verified_email": "campus.queries@accenture.com",
                "direct_pitch_hook": "Candidate cleared both cognitive & pseudocode assessments with zero penalty in record time.",
            }
        ],
        "signals": [
            {
                "signal_type": "OFF_CAMPUS_MASS_DRIVE",
                "source": "Accenture India Campus Hub",
                "signal_date": "2026-08-25",
                "description": "Continuous pan-India registration open for Associate Software Engineer (ASE) cohorts.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Infosys",
        "slug": "infosys",
        "domain": "infosys.com",
        "industry": "Global IT Consulting & Next-Generation Digital Services",
        "stage": "Public (NSE: INFY / NYSE: INFY)",
        "total_funding_usd": 85000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 90000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 315000,
        "headcount_growth_6m_pct": 5.0,
        "hq_location": "Bangalore, India / Global Across 56 Countries",
        "remote_friendly": 1,
        "careers_url": "https://www.infosys.com/careers/graduates.html",
        "ats_provider": "Infosys Career Portal",
        "ats_endpoint": "https://career.infosys.com/joblist",
        "verified_active": 1,
        "roles": [
            {
                "title": "Specialist Programmer (SP) & Digital Specialist Engineer (DSE)",
                "department": "Infosys Center for Emerging Technology Solutions (ICETS)",
                "seniority_level": "Fresher (Systems Engineer, DSE, SP)",
                "salary_min_usd": 40000,
                "salary_max_usd": 70000,
                "equity_note": "Systems Engineer: 3.6 LPA | DSE: 6.25 LPA | Specialist Programmer (SP): 9.5 - 13.5 LPA",
                "tech_stack": "Competitive Programming, DSA, Java, Python, C++, Microservices, Full-Stack",
                "location": "Mysore (Training Campus) / Bangalore / Pune / Hyderabad / Chennai / Chandigarh",
                "remote_type": "Hybrid / Onsite",
                "direct_apply_url": "https://infytq.onwingspan.com/",
                "urgency_score": 9.4,
                "batch_eligibility": "2024, 2025, 2026 Batch (B.Tech / M.Tech / MCA)",
                "min_cgpa": "60% or 6.0 CGPA throughout academic career",
                "test_pattern": "InfyTQ / HackWithInfy: Advanced Algorithmic Coding Challenge (3 Complex DSA Questions: Greedy, Dynamic Programming, Graphs)",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Infosys Talent Sourcing Head",
                "title": "VP & Global Head of Campus Recruitment",
                "department": "Campus Recruitment",
                "linkedin_url": "https://linkedin.com/company/infosys/jobs",
                "twitter_handle": "@InfosysCareers",
                "verified_email": "talentacquisition@infosys.com",
                "direct_pitch_hook": "HackWithInfy finalist and active competitive programmer with verified profile on CodeChef/LeetCode.",
            }
        ],
        "signals": [
            {
                "signal_type": "HACKWITHINFY_LAUNCH",
                "source": "Infosys Springboard",
                "signal_date": "2026-08-10",
                "description": "HackWithInfy national flagship hackathon open offering direct Specialist Programmer (SP) job offers.",
                "weight": 2.0,
            }
        ]
    },
    {
        "name": "Cognizant",
        "slug": "cognizant",
        "domain": "cognizant.com",
        "industry": "IT Services, Cloud Modernization & Digital Engineering",
        "stage": "Public (NASDAQ: CTSH)",
        "total_funding_usd": 38000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 42000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 345000,
        "headcount_growth_6m_pct": 5.0,
        "hq_location": "Teaneck, NJ / Chennai / Bangalore / Hyderabad",
        "remote_friendly": 1,
        "careers_url": "https://careers.cognizant.com/student-hub",
        "ats_provider": "Superset / Cognizant Portal",
        "ats_endpoint": "https://app.joinsuperset.com/company/cognizant",
        "verified_active": 1,
        "roles": [
            {
                "title": "GenC Next / GenC Elevate / GenC Programmer Analyst Trainee",
                "department": "Digital Business & Technology",
                "seniority_level": "Fresher (GenC, Elevate, Next)",
                "salary_min_usd": 40000,
                "salary_max_usd": 65000,
                "equity_note": "GenC: 4.0 LPA | GenC Elevate: 5.5 LPA | GenC Next: 6.75 - 9.0 LPA",
                "tech_stack": "Java, Python, C#, Cloud Fundamentals, SQL, Web Technologies",
                "location": "Chennai / Bangalore / Coimbatore / Kolkata / Hyderabad / Pune",
                "remote_type": "Hybrid (3 Days Office)",
                "direct_apply_url": "https://careers.cognizant.com/global-en/jobs",
                "urgency_score": 9.3,
                "batch_eligibility": "2024, 2025, 2026 Batch Graduates",
                "min_cgpa": "60% or 6.0 CGPA / No backlogs at joining",
                "test_pattern": "AMCAT / Superset Platform: Quantitative, Analytical, Verbal, Technical Assessment (Coding in C/Java/Python) + Communication Test",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Cognizant Campus Recruitment Lead",
                "title": "Head of Early Career Sourcing",
                "department": "Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/cognizant/jobs",
                "twitter_handle": "@Cognizant",
                "verified_email": "campusrecruitment@cognizant.com",
                "direct_pitch_hook": "Top scorer in AMCAT technical and coding sections with clean problem-solving efficiency.",
            }
        ],
        "signals": [
            {
                "signal_type": "CAMPUS_ONBOARDING_SURGE",
                "source": "Cognizant Press Release",
                "signal_date": "2026-08-19",
                "description": "Onboarding 25,000+ engineering graduates across digital engineering cohorts.",
                "weight": 1.8,
            }
        ]
    },
    {
        "name": "IBM",
        "slug": "ibm",
        "domain": "ibm.com",
        "industry": "Hybrid Cloud, Enterprise Infrastructure & AI",
        "stage": "Public (NYSE: IBM)",
        "total_funding_usd": 200000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 210000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 280000,
        "headcount_growth_6m_pct": 4.0,
        "hq_location": "Armonk, NY / Bangalore / Kochi / Pune / Hyderabad",
        "remote_friendly": 1,
        "careers_url": "https://www.ibm.com/careers/us-en/entry-level/",
        "ats_provider": "BrassRing / IBM ATS",
        "ats_endpoint": "https://www.ibm.com/careers/search?field_keyword_19=Entry%20Level",
        "verified_active": 1,
        "roles": [
            {
                "title": "Associate Software Engineer / Application Developer (Entry Level)",
                "department": "IBM Consulting & Software Labs",
                "seniority_level": "Fresher / Band 6A",
                "salary_min_usd": 65000,
                "salary_max_usd": 95000,
                "equity_note": "INR 5.5 - 12.0 LPA (India) / $65k - $95k (US) + Benefits",
                "tech_stack": "Java, Python, Red Hat OpenShift, Linux, Cloud, Docker, Kubernetes, SQL",
                "location": "Bangalore / Hyderabad / Kochi / Pune / Austin, TX / Raleigh, NC",
                "remote_type": "Hybrid",
                "direct_apply_url": "https://www.ibm.com/careers/search?field_keyword_19=Entry%20Level",
                "urgency_score": 9.4,
                "batch_eligibility": "2024, 2025, 2026 Batch Graduates",
                "min_cgpa": "65% or 6.5 CGPA",
                "test_pattern": "IBM Cognitive Assessment (Games: Resemblance, Grid Challenge, Speed) + English Language Test + Technical Coding Assessment",
            }
        ],
        "decision_makers": [
            {
                "full_name": "IBM University Programs Director",
                "title": "Head of Early Professional Hiring",
                "department": "Human Resources",
                "linkedin_url": "https://linkedin.com/company/ibm/jobs",
                "twitter_handle": "@IBMCareers",
                "verified_email": "ibmuniversity@ibm.com",
                "direct_pitch_hook": "Linux system internals and OpenShift container orchestration certified credentials.",
            }
        ],
        "signals": [
            {
                "signal_type": "GLOBAL_ACQUISITION_DRIVE",
                "source": "IBM Newsroom",
                "signal_date": "2026-08-30",
                "description": "Massive scaling of IBM Consulting watsonx AI engineering hubs for early career talent.",
                "weight": 1.7,
            }
        ]
    },
    {
        "name": "Oracle",
        "slug": "oracle",
        "domain": "oracle.com",
        "industry": "Enterprise Database, Cloud Infrastructure & Applications",
        "stage": "Public (NYSE: ORCL)",
        "total_funding_usd": 380000000000,
        "last_round_type": "Public Mega-Cap",
        "valuation_usd": 400000000000,
        "lead_investors": "Publicly Traded",
        "headcount": 164000,
        "headcount_growth_6m_pct": 7.0,
        "hq_location": "Austin, TX / Bangalore / Hyderabad / Noida",
        "remote_friendly": 1,
        "careers_url": "https://www.oracle.com/careers/college-recruiting/",
        "ats_provider": "Oracle Cloud HCM",
        "ats_endpoint": "https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions?keyword=College",
        "verified_active": 1,
        "roles": [
            {
                "title": "Associate Software Engineer - Oracle Cloud Infrastructure (OCI)",
                "department": "OCI Engineering / Autonomous Database",
                "seniority_level": "Fresher / IC-1",
                "salary_min_usd": 110000,
                "salary_max_usd": 145000,
                "equity_note": "INR 18 - 32 LPA (India) / $110k - $145k (US) + RSUs",
                "tech_stack": "Java, C++, Python, Linux, Distributed Systems, SQL, Cloud Networks",
                "location": "Bangalore / Hyderabad / Noida / Austin / Seattle",
                "remote_type": "Hybrid",
                "direct_apply_url": "https://www.oracle.com/careers/college-recruiting/",
                "urgency_score": 9.6,
                "batch_eligibility": "2024, 2025, 2026 Batch",
                "min_cgpa": "7.0 CGPA",
                "test_pattern": "Oracle Online Test: CS Core (DBMS, OS, Computer Networks), DSA Coding (2 Problems), Aptitude + 3 Technical Rounds",
            }
        ],
        "decision_makers": [
            {
                "full_name": "Oracle College Hiring Team",
                "title": "Director of Campus Talent",
                "department": "Talent Acquisition",
                "linkedin_url": "https://linkedin.com/company/oracle/jobs",
                "twitter_handle": "@OracleCareers",
                "verified_email": "college_recruiting@oracle.com",
                "direct_pitch_hook": "Extensive mastery over SQL query execution plans, indexing strategies, and multi-threaded Java applications.",
            }
        ],
        "signals": [
            {
                "signal_type": "CLOUD_EXPANSION",
                "source": "Oracle OCI Press",
                "signal_date": "2026-09-05",
                "description": "OCI expanding data center regions globally; high-volume hiring of Associate Engineers.",
                "weight": 1.9,
            }
        ]
    }
]
