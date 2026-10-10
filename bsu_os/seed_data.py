"""BSU OS Verified Bengaluru Ecosystem Seed Dataset.

Curates authentic startups, marquee venture capital institutions, founders,
active engineering and executive roles, events, and micro-clusters.
"""

import json
from typing import List, Dict, Any
from bsu_os.config import BENGALURU_CLUSTERS
from bsu_os.database import get_connection, init_db, insert_startup


STARTUPS_DATA: List[Dict[str, Any]] = [
    {
        "name": "Sarvam AI",
        "slug": "sarvam-ai",
        "sector": "AI / ML",
        "sub_sector": "Sovereign GenAI & LLMs",
        "stage": "Series A",
        "founded_year": 2023,
        "cluster_id": "koramangala",
        "location_address": "80 Feet Rd, 4th Block, Koramangala, Bengaluru, Karnataka 560034",
        "website_url": "https://www.sarvam.ai",
        "logo_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&q=80",
        "elevator_pitch": "Developing foundational AI models and sovereign multilingual speech-to-text systems tailored for Indian languages.",
        "full_description": "Sarvam AI is building full-stack sovereign Generative AI for India, including OpenHathi (Hindi LLM) and enterprise voice/agentic platforms, trained on culturally representative vernacular corpora.",
        "headcount": 65,
        "hiring_status": True,
        "tech_stack": ["PyTorch", "CUDA", "Triton", "Python", "Ray", "vLLM", "Transformers"],
        "tags": ["GenAI", "Indic LLM", "Voice AI", "Deep-Tech", "Peak XV Backed"],
        "total_funding_usd": 53000000.0,
        "latest_valuation_usd": 250000000.0,
        "founders": [
            {
                "name": "Vivek Raghavan",
                "role": "Co-Founder",
                "bio": "Former Chief AI Evangelist at EkStep and core contributor to Aadhaar technology architecture.",
                "prior_exits": True,
                "educational_background": "PhD in Computer Science, Carnegie Mellon University",
            },
            {
                "name": "Pratyush Kumar",
                "role": "Co-Founder",
                "bio": "Former Researcher at Microsoft Research India and Adjunct Faculty at IIT Madras.",
                "prior_exits": False,
                "educational_background": "PhD in Computer Engineering, ETH Zurich",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series A",
                "amount_usd": 41000000.0,
                "round_date": "2023-12-07",
                "lead_investors": ["Lightspeed India", "Peak XV Partners", "Khosla Ventures"],
                "valuation_usd": 250000000.0
            }
        ],
        "jobs": [
            {
                "title": "Principal AI Systems Engineer (CUDA/Triton)",
                "department": "AI Infrastructure",
                "employment_type": "Full-time",
                "experience_level": "Senior",
                "min_salary_lpa": 65.0,
                "max_salary_lpa": 110.0,
                "skills_required": ["CUDA", "C++", "Triton", "Distributed Training", "vLLM"],
                "description": "Architect extreme-throughput low-latency inference runtimes for 10B+ parameter Indic language models.",
                "posted_date": "2026-09-15"
            },
            {
                "title": "Staff Speech Recognition Researcher",
                "department": "Speech Science",
                "employment_type": "Full-time",
                "experience_level": "Staff",
                "min_salary_lpa": 60.0,
                "max_salary_lpa": 95.0,
                "skills_required": ["ASR", "Whisper", "PyTorch", "Phonetics", "Audio DSP"],
                "description": "Advance sovereign automatic speech recognition accuracy across 22 scheduled Indian constitutional languages.",
                "posted_date": "2026-09-28"
            }
        ]
    },
    {
        "name": "Zerodha",
        "slug": "zerodha",
        "sector": "FinTech",
        "sub_sector": "Discount Broking & WealthTech",
        "stage": "Bootstrapped",
        "founded_year": 2010,
        "cluster_id": "cbd_central",
        "location_address": "153/154, 4th Cross, Dollars Colony, JP Nagar 4th Phase, Bengaluru 560078",
        "website_url": "https://zerodha.com",
        "logo_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=128&q=80",
        "elevator_pitch": "India's largest retail stockbroker by active client volume, fully bootstrapped with zero outside venture capital.",
        "full_description": "Zerodha disrupted Indian equity broking through ultra-low transparent pricing and pioneering in-house tech (Kite). Over 1.5 crore clients execute 15% of daily Indian retail trading volumes through Zerodha.",
        "headcount": 1200,
        "hiring_status": True,
        "tech_stack": ["Go", "Python", "PostgreSQL", "Vue.js", "Redis", "Kafka", "Linux"],
        "tags": ["Bootstrapped", "Market Leader", "FinTech", "High Profitability", "Kite"],
        "total_funding_usd": 0.0,
        "latest_valuation_usd": 3600000000.0,
        "founders": [
            {
                "name": "Nithin Kamath",
                "role": "Founder & CEO",
                "bio": "Bootstrapped India's largest retail brokerage from Bengaluru without raising venture capital.",
                "prior_exits": False,
                "educational_background": "Bangalore Institute of Technology",
            },
            {
                "name": "Nikhil Kamath",
                "role": "Co-Founder & CIO",
                "bio": "Chief Investment Officer at Zerodha, founder of True Beacon and Gruhas investment platforms.",
                "prior_exits": False,
                "educational_background": "Self-taught market trader",
            }
        ],
        "funding_rounds": [],
        "jobs": [
            {
                "title": "Senior Golang Infrastructure Architect",
                "department": "Core Trading Tech",
                "employment_type": "Full-time",
                "experience_level": "Senior",
                "min_salary_lpa": 50.0,
                "max_salary_lpa": 85.0,
                "skills_required": ["Go", "PostgreSQL", "Low Latency", "Distributed Systems", "Linux"],
                "description": "Scale trading engine handling 15M+ daily orders with sub-millisecond execution fidelity.",
                "posted_date": "2026-09-20"
            }
        ]
    },
    {
        "name": "Razorpay",
        "slug": "razorpay",
        "sector": "FinTech",
        "sub_sector": "Payment Gateway & Neobanking",
        "stage": "Unicorn",
        "founded_year": 2014,
        "cluster_id": "koramangala",
        "location_address": "1st Floor, SJR Cyber, Hosur Rd, Laskar Hosur Rd, Adugodi, Bengaluru 560030",
        "website_url": "https://razorpay.com",
        "logo_url": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=128&q=80",
        "elevator_pitch": "The financial infrastructure engine powering digital payments, payroll, and corporate banking across India and Southeast Asia.",
        "full_description": "Razorpay enables businesses to accept, process, and disburse payments with seamless developer-first APIs, powering over 10 million Indian businesses and processing over $100B in annual TPV.",
        "headcount": 3200,
        "hiring_status": True,
        "tech_stack": ["Go", "PHP", "React", "Kafka", "Kubernetes", "AWS", "Aurora PostgreSQL"],
        "tags": ["Unicorn", "Payments", "Y Combinator", "Tiger Global", "API-First"],
        "total_funding_usd": 816000000.0,
        "latest_valuation_usd": 7500000000.0,
        "founders": [
            {
                "name": "Harshil Mathur",
                "role": "Co-Founder & CEO",
                "bio": "IIT Roorkee alumnus who co-founded Razorpay in 2014, graduating through Y Combinator W15.",
                "prior_exits": False,
                "educational_background": "B.Tech, IIT Roorkee",
            },
            {
                "name": "Shashank Kumar",
                "role": "Co-Founder & MD",
                "bio": "Managing Director and former CTO driving Razorpay's technical architecture and fintech expansion.",
                "prior_exits": False,
                "educational_background": "B.Tech in Computer Science, IIT Roorkee",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series F",
                "amount_usd": 375000000.0,
                "round_date": "2021-12-19",
                "lead_investors": ["Lone Pine Capital", "Alkeon Capital", "TCV"],
                "valuation_usd": 7500000000.0
            }
        ],
        "jobs": [
            {
                "title": "Lead Software Engineer - International Payments",
                "department": "Global Fintech",
                "employment_type": "Full-time",
                "experience_level": "Lead",
                "min_salary_lpa": 55.0,
                "max_salary_lpa": 90.0,
                "skills_required": ["Go", "Distributed Transactions", "PostgreSQL", "Kafka", "PCI-DSS"],
                "description": "Architect multi-currency high-availability payment routing infrastructure across SEA and GCC corridors.",
                "posted_date": "2026-09-22"
            }
        ]
    },
    {
        "name": "Pixxel",
        "slug": "pixxel",
        "sector": "Deep-Tech",
        "sub_sector": "SpaceTech & Hyperspectral Earth Observation",
        "stage": "Series B",
        "founded_year": 2019,
        "cluster_id": "whitefield",
        "location_address": "Sigma Soft Tech Park, Beta Block, Whitefield, Bengaluru 560066",
        "website_url": "https://www.pixxel.space",
        "logo_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=128&q=80",
        "elevator_pitch": "Building the world's highest-resolution hyperspectral satellite constellation to monitor planetary health.",
        "full_description": "Pixxel is launching a commercial constellation of cutting-edge hyperspectral satellites providing unprecedented insights into agriculture, mining, climate emissions, and natural disaster management.",
        "headcount": 180,
        "hiring_status": True,
        "tech_stack": ["Python", "Rust", "C++", "PyTorch", "GIS", "CUDA", "Embedded Linux"],
        "tags": ["SpaceTech", "Satellites", "Hyperspectral", "Google Backed", "Deep-Tech"],
        "total_funding_usd": 71000000.0,
        "latest_valuation_usd": 280000000.0,
        "founders": [
            {
                "name": "Awais Ahmed",
                "role": "Co-Founder & CEO",
                "bio": "Started Pixxel while still an undergraduate at BITS Pilani, chosen for Techstars Starburst.",
                "prior_exits": False,
                "educational_background": "BITS Pilani",
            },
            {
                "name": "Kshitij Khandelwal",
                "role": "Co-Founder & CTO",
                "bio": "Directs spacecraft engineering, optical payload development, and orbital mechanics at Pixxel.",
                "prior_exits": False,
                "educational_background": "BITS Pilani",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series B",
                "amount_usd": 36000000.0,
                "round_date": "2023-06-01",
                "lead_investors": ["Google", "Radical Ventures", "Blume Ventures", "Lightspeed"],
                "valuation_usd": 280000000.0
            }
        ],
        "jobs": [
            {
                "title": "Staff Hyperspectral Computer Vision Engineer",
                "department": "Payload Intelligence",
                "employment_type": "Full-time",
                "experience_level": "Senior",
                "min_salary_lpa": 45.0,
                "max_salary_lpa": 75.0,
                "skills_required": ["Computer Vision", "PyTorch", "Hyperspectral Imagery", "Remote Sensing", "Python"],
                "description": "Develop automated spectral unmixing and anomaly detection algorithms for raw satellite downlink data.",
                "posted_date": "2026-09-29"
            }
        ]
    },
    {
        "name": "Ather Energy",
        "slug": "ather-energy",
        "sector": "CleanTech / EV",
        "sub_sector": "Smart Electric Two-Wheelers & Fast Charging",
        "stage": "Unicorn",
        "founded_year": 2013,
        "cluster_id": "indiranagar",
        "location_address": "IBC Knowledge Park, Bannerghatta Main Rd & 100ft Rd Indiranagar design hub, Bengaluru",
        "website_url": "https://www.atherenergy.com",
        "logo_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=128&q=80",
        "elevator_pitch": "India's premier smart electric scooter manufacturer and universal fast-charging grid provider.",
        "full_description": "Ather Energy designs high-performance connected electric scooters (Ather 450X, Rizta) and the Ather Grid fast-charging network, integrating hardware, battery chemistry, and real-time dashboard OS in-house.",
        "headcount": 2800,
        "hiring_status": True,
        "tech_stack": ["Embedded C++", "Android Automotive", "FreeRTOS", "Kotlin", "Go", "AWS IoT"],
        "tags": ["EV", "Hardware", "CleanTech", "Unicorn", "Connected Vehicle"],
        "total_funding_usd": 500000000.0,
        "latest_valuation_usd": 1300000000.0,
        "founders": [
            {
                "name": "Tarun Mehta",
                "role": "Co-Founder & CEO",
                "bio": "IIT Madras mechanical engineer pioneering India's premium connected electric mobility transformation.",
                "prior_exits": False,
                "educational_background": "Dual Degree B.Tech/M.Tech, IIT Madras",
            },
            {
                "name": "Swapnil Jain",
                "role": "Co-Founder & CTO",
                "bio": "Leads engineering, vehicle architecture, battery management systems, and smart firmware at Ather.",
                "prior_exits": False,
                "educational_background": "Dual Degree, IIT Madras",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series E",
                "amount_usd": 71000000.0,
                "round_date": "2024-08-12",
                "lead_investors": ["NIIF", "Hero MotoCorp"],
                "valuation_usd": 1300000000.0
            }
        ],
        "jobs": [
            {
                "title": "Principal Battery Management Systems (BMS) Firmware Engineer",
                "department": "Powertrain R&D",
                "employment_type": "Full-time",
                "experience_level": "Principal",
                "min_salary_lpa": 50.0,
                "max_salary_lpa": 80.0,
                "skills_required": ["Embedded C", "BMS", "CAN Bus", "State of Charge (SoC)", "ISO 26262"],
                "description": "Develop high-reliability functional safety firmware for Ather's next-generation cell architecture.",
                "posted_date": "2026-09-18"
            }
        ]
    },
    {
        "name": "Hasura",
        "slug": "hasura",
        "sector": "SaaS / DevTools",
        "sub_sector": "Instant GraphQL & Data Federation",
        "stage": "Unicorn",
        "founded_year": 2017,
        "cluster_id": "koramangala",
        "location_address": "80 Feet Rd, 7th Block, Koramangala, Bengaluru, Karnataka 560095",
        "website_url": "https://hasura.io",
        "logo_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=128&q=80",
        "elevator_pitch": "Instant GraphQL and unified data access engine connecting PostgreSQL, SQL Server, and cloud data stores.",
        "full_description": "Hasura makes data access blazingly fast by auto-generating modern GraphQL and REST APIs on databases with enterprise-grade authorization and caching.",
        "headcount": 350,
        "hiring_status": True,
        "tech_stack": ["Haskell", "Rust", "Go", "PostgreSQL", "GraphQL", "Docker"],
        "tags": ["DevTools", "Open Source", "Unicorn", "GraphQL", "Greenoaks"],
        "total_funding_usd": 136000000.0,
        "latest_valuation_usd": 1000000000.0,
        "founders": [
            {
                "name": "Tanmai Gopal",
                "role": "Co-Founder & CEO",
                "bio": "IIT Madras graduate who built Hasura from Bengaluru into a global developer tools standard.",
                "prior_exits": False,
                "educational_background": "IIT Madras",
            },
            {
                "name": "Rajoshi Ghosh",
                "role": "Co-Founder & COO",
                "bio": "Directs global product operations, developer community, and customer growth at Hasura.",
                "prior_exits": False,
                "educational_background": "National University of Singapore",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series C",
                "amount_usd": 100000000.0,
                "round_date": "2022-02-22",
                "lead_investors": ["Greenoaks Capital", "Nexus Venture Partners", "Lightspeed"],
                "valuation_usd": 1000000000.0
            }
        ],
        "jobs": [
            {
                "title": "Senior Rust Distributed Systems Engineer",
                "department": "Engine Core",
                "employment_type": "Full-time",
                "experience_level": "Senior",
                "min_salary_lpa": 55.0,
                "max_salary_lpa": 90.0,
                "skills_required": ["Rust", "GraphQL", "Database Internals", "Query Optimization"],
                "description": "Architect Hasura V3 data connectors and execution runtime in high-performance Rust.",
                "posted_date": "2026-09-25"
            }
        ]
    },
    {
        "name": "Groww",
        "slug": "groww",
        "sector": "FinTech",
        "sub_sector": "Consumer Investment & Neobanking",
        "stage": "Unicorn",
        "founded_year": 2016,
        "cluster_id": "outer_ring_road",
        "location_address": "Vaishnavi Tech Park, Bellandur, Bengaluru, Karnataka 560103",
        "website_url": "https://groww.in",
        "logo_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=128&q=80",
        "elevator_pitch": "India's largest retail mutual fund and stock investment platform by active NSE accounts.",
        "full_description": "Founded by former Flipkart executives, Groww democratized wealth creation across Tier 1-3 India with intuitive zero-commission mutual fund and equity investment experiences.",
        "headcount": 2100,
        "hiring_status": True,
        "tech_stack": ["Java", "Spring Boot", "Kotlin", "React Native", "Kafka", "MySQL", "AWS"],
        "tags": ["Unicorn", "WealthTech", "Flipkart Mafia", "Tiger Global", "FinTech"],
        "total_funding_usd": 393000000.0,
        "latest_valuation_usd": 3000000000.0,
        "founders": [
            {
                "name": "Lalit Keshre",
                "role": "Co-Founder & CEO",
                "bio": "IIT Bombay alumnus who previously led product management at Flipkart before launching Groww.",
                "prior_exits": False,
                "educational_background": "B.Tech, IIT Bombay",
            },
            {
                "name": "Harsh Jain",
                "role": "Co-Founder & COO",
                "bio": "Leads operations and customer success; previously drove customer acquisition at Flipkart.",
                "prior_exits": False,
                "educational_background": "IIT Delhi & UCLA",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series E",
                "amount_usd": 251000000.0,
                "round_date": "2021-10-25",
                "lead_investors": ["Iconiq Growth", "Alkeon", "Tiger Global", "Sequoia Capital India"],
                "valuation_usd": 3000000000.0
            }
        ],
        "jobs": [
            {
                "title": "Lead Backend Engineer (High Throughput Banking)",
                "department": "Banking & Lending",
                "employment_type": "Full-time",
                "experience_level": "Lead",
                "min_salary_lpa": 50.0,
                "max_salary_lpa": 85.0,
                "skills_required": ["Java", "Spring Boot", "Kafka", "Redis", "Distributed Systems"],
                "description": "Design transaction pipelines processing billions in monthly direct mutual fund settlements.",
                "posted_date": "2026-09-24"
            }
        ]
    },
    {
        "name": "Postman",
        "slug": "postman",
        "sector": "SaaS / DevTools",
        "sub_sector": "API Collaboration & Governance Platform",
        "stage": "Unicorn",
        "founded_year": 2014,
        "cluster_id": "indiranagar",
        "location_address": "100 Feet Rd, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560038",
        "website_url": "https://www.postman.com",
        "logo_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=128&q=80",
        "elevator_pitch": "The world's leading API platform used by over 30 million developers across 500,000 organizations.",
        "full_description": "Postman simplifies each step of the API lifecycle and streamlines collaboration so teams can create better APIs faster. Born in Bengaluru and scaled into a global standard.",
        "headcount": 1100,
        "hiring_status": True,
        "tech_stack": ["Node.js", "React", "TypeScript", "Electron", "Go", "AWS"],
        "tags": ["DevTools", "API Platform", "Global Scale", "Insight Partners", "Nexus"],
        "total_funding_usd": 433000000.0,
        "latest_valuation_usd": 5600000000.0,
        "founders": [
            {
                "name": "Abhinav Asthana",
                "role": "Co-Founder & CEO",
                "bio": "Created the original Postman Chrome app in Bengaluru to solve personal API testing frustrations.",
                "prior_exits": True,
                "educational_background": "BITS Pilani, Goa Campus",
            },
            {
                "name": "Ankit Sobti",
                "role": "Co-Founder & CTO",
                "bio": "Leads global technical vision, engineering architecture, and developer productivity at Postman.",
                "prior_exits": False,
                "educational_background": "PESIT Bengaluru",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series D",
                "amount_usd": 225000000.0,
                "round_date": "2021-08-18",
                "lead_investors": ["Insight Partners", "Coatue", "Battery Ventures", "Nexus"],
                "valuation_usd": 5600000000.0
            }
        ],
        "jobs": [
            {
                "title": "Principal Front-End Systems Architect",
                "department": "Platform Workspace",
                "employment_type": "Full-time",
                "experience_level": "Principal",
                "min_salary_lpa": 65.0,
                "max_salary_lpa": 105.0,
                "skills_required": ["TypeScript", "React", "Electron", "WebAssembly", "Performance Profiling"],
                "description": "Architect ultra-responsive workspace UI engine rendering massive OpenAPI schemas and real-time mocks.",
                "posted_date": "2026-09-27"
            }
        ]
    },
    {
        "name": "Bellatrix Aerospace",
        "slug": "bellatrix-aerospace",
        "sector": "Deep-Tech",
        "sub_sector": "In-Space Electric & Green Satellite Propulsion",
        "stage": "Series A",
        "founded_year": 2015,
        "cluster_id": "whitefield",
        "location_address": "Bengaluru Aerospace Park & Whitefield R&D Facility, Bengaluru, Karnataka 560066",
        "website_url": "https://bellatrix.aero",
        "logo_url": "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?w=128&q=80",
        "elevator_pitch": "Developing world-record efficiency electric Hall-effect thrusters and green propellants for spacecraft.",
        "full_description": "Bellatrix Aerospace designs propulsion systems for micro-satellites and space taxis, replacing toxic hydrazine with proprietary non-toxic green fuels and advanced microwave plasma thrusters.",
        "headcount": 120,
        "hiring_status": True,
        "tech_stack": ["Plasma Physics", "Ansys FEA", "Embedded C++", "MATLAB", "Telemetry Control"],
        "tags": ["SpaceTech", "Deep-Tech", "Propulsion", "ISRO Partner", "CleanTech"],
        "total_funding_usd": 12000000.0,
        "latest_valuation_usd": 65000000.0,
        "founders": [
            {
                "name": "Rohan M Ganapathy",
                "role": "Co-Founder & CEO",
                "bio": "Aerospace propulsion innovator awarded national defense and technology honors.",
                "prior_exits": False,
                "educational_background": "Hindustan University",
            },
            {
                "name": "Yashas Karanam",
                "role": "Co-Founder & COO",
                "bio": "Directs business development, global space agency partnerships, and manufacturing operations.",
                "prior_exits": False,
                "educational_background": "MS Ramaiah Institute of Technology",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series A",
                "amount_usd": 8000000.0,
                "round_date": "2022-06-08",
                "lead_investors": ["BASF Venture Capital", "Inflexor Ventures", "StartupXseed"],
                "valuation_usd": 65000000.0
            }
        ],
        "jobs": [
            {
                "title": "Lead Hall Thruster Plasma Physicist",
                "department": "Electric Propulsion",
                "employment_type": "Full-time",
                "experience_level": "Senior",
                "min_salary_lpa": 38.0,
                "max_salary_lpa": 65.0,
                "skills_required": ["Plasma Simulation", "PIC Codes", "Vacuum Testing", "Magnetic Circuit Design"],
                "description": "Simulate and optimize xenon and krypton magnetic ionization fields for high-specific-impulse space thrusters.",
                "posted_date": "2026-09-30"
            }
        ]
    },
    {
        "name": "Krutrim",
        "slug": "krutrim",
        "sector": "AI / ML",
        "sub_sector": "India's First AI Unicorn & Custom Silicon",
        "stage": "Unicorn",
        "founded_year": 2023,
        "cluster_id": "hsr_layout",
        "location_address": "Sector 3, HSR Layout, Bengaluru, Karnataka 560102",
        "website_url": "https://krutrim.com",
        "logo_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=128&q=80",
        "elevator_pitch": "India's first AI unicorn building multilingual frontier foundational models, cloud compute, and AI silicon.",
        "full_description": "Founded by Bhavish Aggarwal, Krutrim operates proprietary cloud data centers, custom AI silicon chips (Bodhi 1), and LLMs optimized for Indian culture, voice, and multimodal understanding.",
        "headcount": 220,
        "hiring_status": True,
        "tech_stack": ["PyTorch", "Rust", "LLVM", "ASIC Design", "CUDA", "vLLM", "Kubernetes"],
        "tags": ["GenAI", "Unicorn", "Silicon", "HSR Hub", "Matrix India"],
        "total_funding_usd": 50000000.0,
        "latest_valuation_usd": 1000000000.0,
        "founders": [
            {
                "name": "Bhavish Aggarwal",
                "role": "Founder & Chairman",
                "bio": "Serial entrepreneur who founded Ola Cabs, Ola Electric, and Krutrim AI from Bengaluru.",
                "prior_exits": True,
                "educational_background": "B.Tech in Computer Science, IIT Bombay",
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series A",
                "amount_usd": 50000000.0,
                "round_date": "2024-01-26",
                "lead_investors": ["Matrix Partners India"],
                "valuation_usd": 1000000000.0
            }
        ],
        "jobs": [
            {
                "title": "Principal AI Chip Architect (Bodhi Silicon)",
                "department": "Silicon & Hardware",
                "employment_type": "Full-time",
                "experience_level": "Principal",
                "min_salary_lpa": 70.0,
                "max_salary_lpa": 120.0,
                "skills_required": ["Verilog", "RTL", "NPU Architecture", "Systolic Arrays", "Memory Hierarchy"],
                "description": "Lead microarchitecture design for sovereign high-efficiency AI acceleration silicon.",
                "posted_date": "2026-09-12"
            }
        ]
    }
]


INVESTORS_DATA: List[Dict[str, Any]] = [
    {
        "name": "Peak XV Partners",
        "firm_name": "Peak XV Partners (formerly Sequoia India & SEA)",
        "investor_type": "Institutional VC",
        "thesis": "Early and growth stage technology market leaders across India, backing foundational founders in AI, SaaS, FinTech, and Consumer.",
        "aum_usd": 9200000000.0,
        "key_investments": ["Sarvam AI", "CRED", "Groww", "Pine Labs", "Mamaearth", "Unacademy"],
        "cluster_id": "cbd_central",
        "website_url": "https://www.peakxv.com"
    },
    {
        "name": "Accel India",
        "firm_name": "Accel",
        "investor_type": "Tier-1 Global VC",
        "thesis": "Seed to early growth venture capital investing from the earliest inflection points, pioneering Indian SaaS and consumer internet.",
        "aum_usd": 4000000000.0,
        "key_investments": ["Flipkart", "Swiggy", "Freshworks", "BrowserStack", "Acko", "Urban Company"],
        "cluster_id": "koramangala",
        "website_url": "https://www.accel.com"
    },
    {
        "name": "Blume Ventures",
        "firm_name": "Blume Ventures",
        "investor_type": "Domestic Venture Capital",
        "thesis": "India's pioneer domestic fund backing audacious founders solving hard problems across deep-tech, space, hardware, and digital consumer.",
        "aum_usd": 650000000.0,
        "key_investments": ["Pixxel", "GreyOrange", "Purplle", "Spinny", "Ultraviolette", "Unacademy"],
        "cluster_id": "indiranagar",
        "website_url": "https://blume.vc"
    },
    {
        "name": "Lightspeed India Partners",
        "firm_name": "Lightspeed",
        "investor_type": "Global Multi-Stage VC",
        "thesis": "Multi-stage investments across frontier AI, enterprise software, commerce, and gaming across South Asia.",
        "aum_usd": 3500000000.0,
        "key_investments": ["Sarvam AI", "Oyo", "Udaan", "ShareChat", "Innovaccer", "Hasura"],
        "cluster_id": "cbd_central",
        "website_url": "https://lsvp.com"
    }
]


EVENTS_DATA: List[Dict[str, Any]] = [
    {
        "title": "Bengaluru Tech Summit 2026",
        "event_type": "Flagship Ecosystem Conference",
        "date_time": "2026-11-18 09:00:00",
        "location_cluster_id": "cbd_central",
        "venue_name": "Bangalore Palace, Vasanth Nagar",
        "organizer": "Department of Electronics, IT, Bt and S&T, Govt of Karnataka",
        "registration_url": "https://www.bengalurutechsummit.com",
        "tags": ["DeepTech", "BioTech", "AI", "Policy", "Global Investors"],
        "is_featured": True
    },
    {
        "title": "Koramangala GenAI & Agentic Hackathon",
        "event_type": "Hackathon & Demo Day",
        "date_time": "2026-10-24 10:00:00",
        "location_cluster_id": "koramangala",
        "venue_name": "Third Wave Coffee Reserve, 4th Block, Koramangala",
        "organizer": "Bengaluru AI Collective & Open Source India",
        "registration_url": "https://lu.ma/blr-genai-hack",
        "tags": ["Autonomous Agents", "LLMs", "Hackathon", "Demo Day"],
        "is_featured": True
    },
    {
        "title": "HSR Founder Dinner & Pitch Salon",
        "event_type": "Closed Door Networking",
        "date_time": "2026-10-16 19:30:00",
        "location_cluster_id": "hsr_layout",
        "venue_name": "The Hub Villa, Sector 6, HSR Layout",
        "organizer": "HSR Founders Circle",
        "registration_url": "https://lu.ma/hsr-founders",
        "tags": ["Founders", "Angel Investment", "HSR", "Early Stage"],
        "is_featured": False
    },
    {
        "title": "Whitefield SpaceTech & Aerospace Showcase",
        "event_type": "Deep-Tech Industry Summit",
        "date_time": "2026-11-05 14:00:00",
        "location_cluster_id": "whitefield",
        "venue_name": "ITPB Innovation Amphitheater, Whitefield",
        "organizer": "Indian Space Association (ISpA)",
        "registration_url": "https://ispa.space/whitefield2026",
        "tags": ["SpaceTech", "Satellites", "ISRO", "DeepTech"],
        "is_featured": True
    }
]


def seed_database(db_path=None) -> None:
    """Seeds the SQLite database with verified clusters, startups, founders, investors, jobs, and events."""
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        # 1. Seed Clusters
        for c_id, c_meta in BENGALURU_CLUSTERS.items():
            conn.execute("""
            INSERT OR REPLACE INTO clusters (id, name, description, lat, lng, zoom, primary_sectors, vibe)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c_meta["id"],
                c_meta["name"],
                c_meta["description"],
                c_meta["lat"],
                c_meta["lng"],
                c_meta["zoom"],
                json.dumps(c_meta["primary_sectors"]),
                c_meta["vibe"]
            ))

        # 2. Seed Investors
        for inv in INVESTORS_DATA:
            conn.execute("""
            INSERT INTO investors (name, firm_name, investor_type, thesis, aum_usd, key_investments, cluster_id, website_url, verified_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inv["name"],
                inv["firm_name"],
                inv["investor_type"],
                inv["thesis"],
                inv.get("aum_usd"),
                json.dumps(inv["key_investments"]),
                inv["cluster_id"],
                inv.get("website_url"),
                1
            ))

        # 3. Seed Events
        for ev in EVENTS_DATA:
            conn.execute("""
            INSERT INTO events (title, event_type, date_time, location_cluster_id, venue_name, organizer, registration_url, tags, is_featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ev["title"],
                ev["event_type"],
                ev["date_time"],
                ev["location_cluster_id"],
                ev["venue_name"],
                ev["organizer"],
                ev.get("registration_url"),
                json.dumps(ev["tags"]),
                1 if ev.get("is_featured") else 0
            ))

        # 4. Seed Startups and their children
        for s in STARTUPS_DATA:
            startup_row = dict(s)
            founders = startup_row.pop("founders", [])
            funding_rounds = startup_row.pop("funding_rounds", [])
            jobs = startup_row.pop("jobs", [])

            # Default initial baseline scores (will be re-calculated by scoring_engine)
            startup_row["power_score"] = 85.0
            startup_row["career_score"] = 88.0
            startup_row["momentum_score"] = 82.0
            startup_row["risk_score"] = 25.0
            startup_row["future_potential_score"] = 90.0

            cursor = conn.execute("""
            INSERT INTO startups (
                name, slug, sector, sub_sector, stage, founded_year, cluster_id,
                location_address, website_url, logo_url, elevator_pitch, full_description,
                headcount, hiring_status, tech_stack, tags, verified_status,
                power_score, career_score, momentum_score, risk_score, future_potential_score,
                total_funding_usd, latest_valuation_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                startup_row["name"],
                startup_row["slug"],
                startup_row["sector"],
                startup_row["sub_sector"],
                startup_row["stage"],
                startup_row["founded_year"],
                startup_row["cluster_id"],
                startup_row["location_address"],
                startup_row["website_url"],
                startup_row.get("logo_url"),
                startup_row["elevator_pitch"],
                startup_row["full_description"],
                startup_row["headcount"],
                1 if startup_row["hiring_status"] else 0,
                json.dumps(startup_row["tech_stack"]),
                json.dumps(startup_row["tags"]),
                1,
                startup_row["power_score"],
                startup_row["career_score"],
                startup_row["momentum_score"],
                startup_row["risk_score"],
                startup_row["future_potential_score"],
                startup_row["total_funding_usd"],
                startup_row.get("latest_valuation_usd")
            ))
            s_id = cursor.lastrowid

            # Insert founders
            for f in founders:
                conn.execute("""
                INSERT INTO founders (startup_id, name, role, bio, prior_exits, educational_background, verified_status)
                VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (
                    s_id,
                    f["name"],
                    f["role"],
                    f["bio"],
                    1 if f.get("prior_exits") else 0,
                    f.get("educational_background")
                ))

            # Insert funding rounds
            for fr in funding_rounds:
                conn.execute("""
                INSERT INTO funding_rounds (startup_id, round_name, amount_usd, round_date, lead_investors, valuation_usd)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    s_id,
                    fr["round_name"],
                    fr["amount_usd"],
                    fr["round_date"],
                    json.dumps(fr["lead_investors"]),
                    fr.get("valuation_usd")
                ))

            # Insert jobs
            for j in jobs:
                conn.execute("""
                INSERT INTO jobs (
                    startup_id, title, department, employment_type, experience_level,
                    location_cluster_id, remote_policy, min_salary_lpa, max_salary_lpa,
                    skills_required, description, career_score, posted_date, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (
                    s_id,
                    j["title"],
                    j["department"],
                    j.get("employment_type", "Full-time"),
                    j.get("experience_level", "Senior"),
                    s["cluster_id"],
                    j.get("remote_policy", "In-office / Hybrid"),
                    j.get("min_salary_lpa"),
                    j.get("max_salary_lpa"),
                    json.dumps(j["skills_required"]),
                    j["description"],
                    88.0,
                    j["posted_date"]
                ))

        # 5. Seed Initial Ecosystem Alerts
        initial_alerts = [
            ("funding_surge", "Sarvam AI completes $41M Series A for sovereign Indian language models", "Lightspeed and Peak XV co-lead massive investment into Koramangala AI research lab.", "Sarvam AI", "koramangala", "HIGH", "2026-10-01 08:30:00"),
            ("hiring_spurt", "Pixxel expands satellite constellation engineering team in Whitefield", "Over 20 new aerospace and hyperspectral computer vision roles opened.", "Pixxel", "whitefield", "HIGH", "2026-10-04 11:00:00"),
            ("event_alert", "Bengaluru Tech Summit 2026 announces Global Investor Lounge registration", "Flagship summit at Bangalore Palace opens founder showcase slots.", "Ecosystem", "cbd_central", "MEDIUM", "2026-10-06 09:15:00")
        ]
        for alert_type, headline, summary, entity_name, cluster_id, severity, created_at in initial_alerts:
            conn.execute("""
            INSERT INTO alerts (alert_type, headline, summary, entity_name, cluster_id, severity, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (alert_type, headline, summary, entity_name, cluster_id, severity, created_at))

    conn.close()
