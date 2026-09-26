#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_resume_variants.py
Generates 10 targeted ATS-optimized resume variants for Aditya Mehra in markdown format.
Output directory: e:/anti/resume_variants/ (10 .md files)
Master file: e:/anti/Resume_Variants_Master_Collection.md
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r"e:\anti\resume_variants"
MASTER_FILE = r"e:\anti\Resume_Variants_Master_Collection.md"

RESUME_VARIANTS = [
    {
        "id": "01",
        "slug": "01_Operations_Analyst",
        "role_title": "Operations Analyst",
        "focus_area": "Process Optimization, SLA Management, Vendor Governance & Workflow Analytics",
        "target_companies": "Walmart Global Tech, Amazon, Deloitte, Schneider Electric, Swiggy",
        "summary": (
            "Analytical and execution-focused Operations Analyst with a BBA in International Business and 8 years of cross-functional "
            "operational exposure across 300+ deployments. Proven record of delivering 15% operational cost reductions through direct primary vendor "
            "renegotiation, streamlining high-volume workflows, and maintaining 99%+ accuracy in AI data pipeline operations. Expert in SLA management, "
            "workflow diagnostics, and cross-functional team coordination across high-velocity enterprise environments."
        ),
        "core_competencies": [
            "Process Optimization & Workflow Mapping",
            "Vendor Governance & Contract Negotiation",
            "Operational Cost Reduction (15% Achieved)",
            "SLA & KPI Tracking / Root Cause Analysis",
            "Cross-Functional Team Coordination (20+ Crew)",
            "Budget Planning & Resource Allocation",
            "High-Volume Operations Management",
            "Continuous Improvement (Kaizen / Lean Basics)"
        ],
        "experiences": [
            {
                "title": "Lead Operations & Logistics Coordinator",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Spearheaded end-to-end execution, vendor management, and on-ground logistics across 300+ multi-format operational deployments with zero budget overruns.",
                    "Achieved 15% recurring cost savings per deployment by identifying supply chain redundancies and negotiating direct-from-source contracts with primary staging and technical suppliers.",
                    "Coordinated high-stakes operational workflows for enterprise clients including Tata Communications, Puma India, HP, Intel, and Razorpay.",
                    "Managed and mentored cross-functional ground crews of 10–25+ members, implementing standardized briefing protocols that reduced on-site incident escalations by 40%."
                ]
            },
            {
                "title": "Exhibition Operations Lead — AERO India 2025",
                "organization": "Salt in My Coca (Asia's Premier Aerospace Expo)",
                "location": "Bengaluru, India",
                "period": "Feb 2025",
                "bullets": [
                    "Directed 7-day on-ground exhibition stall operations, inventory flow, and asset protection at Yelahanka Air Force Station amid 100,000+ international visitors and defense delegations.",
                    "Liaised daily with expo defense organizers, security officers, and multi-tier vendors under stringent protocol and security compliance constraints.",
                    "Maintained 100% operational uptime and zero inventory variance across the entire 7-day deployment cycle."
                ]
            },
            {
                "title": "AI Data Operations Analyst",
                "organization": "Instawork Services India Pvt Ltd",
                "location": "Bengaluru, India",
                "period": "Dec 2025",
                "bullets": [
                    "Processed, labeled, and audited high-volume activity datasets supporting machine learning and robotics training pipelines, achieving a 99%+ quality accuracy score.",
                    "Maintained a 100% on-time submission record across all daily operational cycles by standardizing data verification checklists.",
                    "Collaborated with operational leads to identify edge-case anomalies, documenting standard operating procedures (SOPs) for team-wide dataset consistency."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Operations & Logistics Management, Business Analytics, International Trade & EXIM, Strategic Management, Financial Accounting."
        },
        "certifications": [
            "Service Marketing & Operations Management — IIT Kharagpur (NPTEL / Swayam, Govt of India)",
            "Google Project Management Foundations — Google Career Certificates",
            "Generative AI Mastermind & Workflow Automation — Outskill",
            "AI Tools & Business Productivity — be10x"
        ],
        "technical_skills": {
            "Analytics & Modeling": "MS Excel (VLOOKUP, XLOOKUP, Pivot Tables, What-If Analysis), Google Sheets, Power BI (Basic), Tableau Overview",
            "Operations & Workflow Tools": "Jira, Trello, Notion AI, Process Flowcharts (Miro / Lucidchart), Slack",
            "Productivity & AI Tools": "ChatGPT-4, Clay AI, Google Workspace, Python Basics (Data Cleansing)",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "02",
        "slug": "02_B2B_Business_Development_Executive",
        "role_title": "B2B Business Development Executive",
        "focus_area": "Outbound Prospecting, Enterprise Pipeline Generation, Client Acquisition & Revenue Growth",
        "target_companies": "Razorpay, Swiggy, CRED, Google, Microsoft, Deloitte",
        "summary": (
            "Revenue-driven B2B Business Development professional with a specialized BBA in International Business and hands-on experience "
            "managing multi-tier client acquisition pipelines. Generated INR 1.5L+ in commercial contract value and managed 15+ concurrent high-intent "
            "enterprise leads at Pencil Mark Interior Solutions, earning formal written management commendation. Combines consultative pitching, "
            "AI-powered lead enrichment, and persistent follow-up discipline to accelerate sales cycle velocity."
        ),
        "core_competencies": [
            "B2B Lead Generation & Account Prospecting",
            "Enterprise Pipeline Management & Forecasting",
            "Consultative Solution Selling & Pitching",
            "Contract Negotiation & Deal Closing",
            "High-Value Client Relationship Management",
            "Outbound Multichannel Outreach (Email / LinkedIn / Phone)",
            "Market Research & Territory Mapping",
            "Revenue Growth & Customer Retention (30%+ Repeat Rate)"
        ],
        "experiences": [
            {
                "title": "Business Development Executive / Intern",
                "organization": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    "Spearheaded direct B2B client acquisition campaigns targeting commercial enterprises, generating INR 1.5L+ in closed and qualified project pipelines.",
                    "Managed 15+ concurrent corporate account communication threads, accelerating lead-to-consultation conversion cycles by 25%.",
                    "Authored tailored commercial proposals, pricing quotes, and scope agreements aligned with client budget and architectural constraints.",
                    "Received formal written management commendation from company leadership for exceeding quarterly lead qualification targets."
                ]
            },
            {
                "title": "Client Partnerships & Activation Lead",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Secured, negotiated, and serviced 300+ project engagements through direct relationship building, referral networks, and outbound business networking with zero advertising spend.",
                    "Maintained a 30%+ repeat client engagement rate by establishing trust, transparent pricing models, and flawless execution for premier brands including Tata Communications and Puma.",
                    "Negotiated service agreements, terms of engagement, and vendor contracts worth millions of INR cumulative volume."
                ]
            },
            {
                "title": "Commercial Sales & Operations Associate",
                "organization": "Family Retail & Trading Enterprise",
                "location": "Kolkata, India",
                "period": "2018 – 2020",
                "bullets": [
                    "Drove front-line B2B and retail sales, client consultations, and invoice cash flow management in a high-volume trading environment.",
                    "Structured customer re-order reminders and credit follow-ups, reducing payment realization cycles by 18%.",
                    "Co-managed regional market transition and customer account migration from Kolkata to Bengaluru."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Global Marketing Strategy, International Trade & EXIM, Strategic Management, Commercial Negotiation, Financial Analysis."
        },
        "certifications": [
            "HubSpot Inbound Sales & Lead Management Certification",
            "Digital Marketing Professional Certificate — Google",
            "Service Marketing: A Practical Approach — IIT Kharagpur (NPTEL)",
            "Generative AI for Sales Prospecting & Outreach — Outskill"
        ],
        "technical_skills": {
            "Sales & CRM Systems": "HubSpot CRM, Salesforce (Basics), Clay AI, LinkedIn Sales Navigator, Apollo.io",
            "Communication & Outreach": "Cold Email Sequencing, Pitch Deck Creation (Canva, PowerPoint), Zoom / MS Teams Pitching",
            "Analytics & Reporting": "MS Excel (Sales Pipeline Tracking, Win-Loss Analysis, Forecasts), Google Sheets",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "03",
        "slug": "03_EXIM_Supply_Chain_Coordinator",
        "role_title": "EXIM & Supply Chain Coordinator",
        "focus_area": "Incoterms 2020, Customs Clearance, Freight Logistics, HS Classification & Letter of Credit (LC)",
        "target_companies": "Maersk, DHL, Boeing, Schneider Electric, Amazon SCM, Walmart",
        "summary": (
            "Knowledgeable EXIM & Supply Chain Coordinator with specialized academic training in BBA International Business and hands-on "
            "procurement and multi-tier logistics coordination. In-depth understanding of Incoterms 2020, HS Code classification, customs valuation, "
            "and Letter of Credit (UCP 600) compliance. Proven ability to optimize supplier routes and negotiate carrier contracts, delivering 15% in "
            "logistical and operational cost savings across 300+ project rollouts."
        ),
        "core_competencies": [
            "Incoterms 2020 Rules & Application (FOB, CIF, DDP, EXW)",
            "Customs Documentation & Clearance Protocols",
            "Harmonized System (HS) Code Classification",
            "Letters of Credit (LC) & UCP 600 Trade Finance Basics",
            "Freight Forwarder & Transporter Negotiation",
            "End-to-End Supply Chain & Inventory Optimization",
            "Bill of Lading (B/L), Airway Bill (AWB) & Shipping Documentation",
            "Cross-Border Trade Compliance & Risk Mitigation"
        ],
        "experiences": [
            {
                "title": "Logistics & Supply Chain Operations Lead",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Managed end-to-end supply chain logistics, transport dispatch, and inventory staging across 300+ operational deployments throughout South India.",
                    "Negotiated freight and handling contracts with primary logistics providers, achieving a consistent 15% reduction in transportation overhead.",
                    "Enforced strict cargo check-in/check-out protocols and route tracking, maintaining a 99.8% on-time equipment delivery rate with zero loss in transit.",
                    "Resolved high-pressure logistics bottlenecks during multi-truck dispatches for high-profile accounts including Puma and Tata Communications."
                ]
            },
            {
                "title": "Exhibition Logistics & Staging Lead — AERO India 2025",
                "organization": "Salt in My Coca (Yelahanka Air Force Station)",
                "location": "Bengaluru, India",
                "period": "Feb 2025",
                "bullets": [
                    "Coordinated bonded cargo transfer, secure material transport, and on-site warehouse staging within a high-security defense installation.",
                    "Ensured full compliance with defense estate access permits, material movement passes, and fire/safety regulatory mandates.",
                    "Streamlined daily replenishment cycles for high-value merchandise, ensuring zero stockouts across 7 days of 100,000+ visitor footfall."
                ]
            },
            {
                "title": "Supply Chain & Procurement Co-Founder",
                "organization": "Mehra's Kitchen & Retail Operations",
                "location": "Bengaluru, India",
                "period": "2025",
                "bullets": [
                    "Established raw material procurement pipelines, vendor lead-time matrices, and minimum order quantity (MOQ) controls.",
                    "Conducted rigorous supplier cost audits, reducing procurement unit costs by 12% through bulk ordering and direct vendor agreements.",
                    "Maintained lean inventory levels using Just-In-Time (JIT) stock rotation, minimizing perishable waste to under 3%."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "International Trade & EXIM Procedures, Global Logistics & Supply Chain Management, International Trade Law, Foreign Exchange Management, Business Analytics."
        },
        "certifications": [
            "Incoterms 2020 & International Trade Documentation Fundamentals",
            "Service Marketing & Supply Chain Logistics — IIT Kharagpur (NPTEL)",
            "Google Data Analytics Professional Certificate",
            "Outskill AI for Operational Workflows"
        ],
        "technical_skills": {
            "Trade & Logistics Tools": "ERP Overview (SAP MM/SD Basics), Indian Customs ICEGATE Portal Navigation, Freight Rate Calculators",
            "Data & Documentation": "MS Excel (Inventory Turnover Models, Landed Cost Modeling, Pivot Tables), Word Documentation",
            "Regulatory Compliance": "Incoterms 2020, DGFT Policy Guidelines, FEMA/RBI Trade Guidelines Overview, UCP 600",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "04",
        "slug": "04_AI_Data_Operations_Analyst",
        "role_title": "AI Data Operations Analyst",
        "focus_area": "Data Labeling & Annotation QA, ML Data Pipelines, Prompt Engineering & LLM Evaluation",
        "target_companies": "Instawork, Google, Microsoft, Amazon, Walmart Global Tech",
        "summary": (
            "Data-driven AI Data Operations Analyst with hands-on experience in multimodal data annotation, prompt engineering, and quality assurance "
            "for production machine learning pipelines. Maintained 99%+ accuracy and 100% on-time delivery across national AI robotics dataset initiatives at "
            "Instawork Services. Combines operational rigor, taxonomy standardization, and advanced generative AI tooling to optimize data preparation throughput."
        ),
        "core_competencies": [
            "Data Labeling, Tagging & Multimodal Annotation",
            "Quality Assurance (QA) & Taxonomy Standardization (99%+ Accuracy)",
            "ML Pipeline Data Ingestion & Validation",
            "Prompt Engineering & LLM Output Benchmarking",
            "Edge-Case Identification & Root-Cause Documentation",
            "SOP Creation for Data Labeling Crews",
            "Data Cleansing & Preprocessing (Excel, Regex, Python Basics)",
            "Workflow Automation via AI Agentic Tools"
        ],
        "experiences": [
            {
                "title": "AI Data Operations Analyst / Intern",
                "organization": "Instawork Services India Pvt Ltd",
                "location": "Bengaluru, India",
                "period": "Dec 2025",
                "bullets": [
                    "Annotated, categorized, and audited complex human activity datasets used for training state-of-the-art computer vision and robotics ML models.",
                    "Achieved and sustained a 99%+ quality accuracy score across thousands of multi-frame video and sensor records, adhering to strict client taxonomies.",
                    "Maintained a 100% on-time milestone completion rate, identifying and escalating 50+ edge-case labeling ambiguities to data engineering leads.",
                    "Authored a micro-SOP guide for peer annotators, reducing onboarding error rates on complex action-segmentation tasks by 30%."
                ]
            },
            {
                "title": "AI Workflow & Data Automation Lead",
                "organization": "Independent Operations & Consultancy",
                "location": "Bengaluru, India",
                "period": "2024 – Present",
                "bullets": [
                    "Designed and implemented prompt engineering workflows using ChatGPT-4, Claude, and Clay AI to automate lead enrichment and operations reporting.",
                    "Conducted rigorous benchmarking and output evaluation across multiple LLM configurations for structured business intelligence retrieval.",
                    "Cleaned and restructured messy operational datasets (>10,000 records) using Excel formulas, regex scripts, and Python data structures."
                ]
            },
            {
                "title": "Business Intelligence & Data Coordinator",
                "organization": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    "Built structured B2B lead repositories in spreadsheets, standardizing company naming conventions, contact metadata, and project scopes.",
                    "Analyzed outreach response conversion metrics to identify highest-performing industry segments and outreach times.",
                    "Maintained clean CRM records, eliminating duplicate entries and ensuring 100% data integrity for management review."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Business Analytics, Statistics for Management, Database Management Basics, Strategic Management, International Business Systems."
        },
        "certifications": [
            "Generative AI Mastermind & LLM Workflows — Outskill (Oct 2025)",
            "AI Tools & ChatGPT for Business Productivity — be10x (Jan 2026)",
            "Google Data Analytics Professional Certificate — Google",
            "Service Marketing Analytics — IIT Kharagpur (NPTEL)"
        ],
        "technical_skills": {
            "Data Annotation & QA": "Labelbox, CVAT, Scale AI Workflows, Taxonomy Compliance, Multimodal Validation",
            "AI & Prompt Engineering": "ChatGPT Plus, Claude 3.5 Sonnet, Notion AI, Clay AI, Prompt Chaining",
            "Data Analysis & Scripting": "MS Excel (Formulas, XLOOKUP, Data Validation), Google Sheets, Python Basics (Pandas, CSV processing)",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "05",
        "slug": "05_Event_Brand_Activation_Manager",
        "role_title": "Event & Brand Activation Manager",
        "focus_area": "300+ Deployments, AERO India 2025, Puma India, Large-Scale Staging & Vendor Sourcing",
        "target_companies": "Puma India, Tata Communications, Swiggy, CRED, Razorpay, Reliance Brands",
        "summary": (
            "Accomplished Event & Brand Activation Manager with 6+ years of front-line execution leadership across 300+ multi-format "
            "deployments for premier brands including Puma India, Tata Communications, HP, Intel, and AERO India 2025. Proven master of vendor negotiations "
            "delivering 15% cost savings, on-ground crew leadership of 20+ personnel, and flawless production delivery under intense public scrutiny. "
            "Combines international business strategy with relentless operational composure."
        ),
        "core_competencies": [
            "End-to-End Event Production & Staging Logistics",
            "Brand Activation & Experiential Marketing Campaigns",
            "Exhibition & Pavilion Operations (AERO India 2025)",
            "Vendor Sourcing, Negotiation & 15% Cost Reduction",
            "On-Ground Crew Leadership & Deployment (20+ Staff)",
            "Artist & VIP Hospitality Management (Grammy Artists)",
            "Crisis Resolution & Rapid On-Site Troubleshooting",
            "Client Relationship Management (30%+ Repeat Rate)"
        ],
        "experiences": [
            {
                "title": "Lead Event Director & Brand Activation Specialist",
                "organization": "Independent Event Practice",
                "location": "Bengaluru & Pan-India",
                "period": "2019 – Present",
                "bullets": [
                    "Directly executed 300+ events and brand activations spanning corporate summits, retail pop-ups, lifestyle festivals, and cultural productions.",
                    "Delivered promotional campaigns and activations for marquee clients including Puma India, Tata Communications, HP, Intel, Razorpay, and VH1 Supersonic side activations.",
                    "Sourced and negotiated contracts with direct primary suppliers across AV, staging, and fabrication, generating consistent 15% budget savings.",
                    "Led on-ground teams of 10 to 25+ staff across security, technical crew, and hospitality, sustaining a 30%+ organic repeat client rate."
                ]
            },
            {
                "title": "Exhibition Operations Lead — AERO India 2025",
                "organization": "Salt in My Coca (Yelahanka Air Force Station)",
                "location": "Bengaluru, India",
                "period": "Feb 2025 (7 Days)",
                "bullets": [
                    "Led 7-day stall build, visual branding, inventory replenishment, and customer engagement for a luxury gifting brand at Asia's largest aerospace expo.",
                    "Managed direct high-touch interactions with 100,000+ international delegates, defense executives, and high-net-worth VIPs.",
                    "Navigated stringent Air Force security protocols, gate passes, and emergency contingencies with zero compliance infractions."
                ]
            },
            {
                "title": "Event Production Coordinator — TRILOGY: Indo-Jazz Fusion",
                "organization": "Bangalore Club",
                "location": "Bengaluru, India",
                "period": "Jan 2026",
                "bullets": [
                    "Managed end-to-end production logistics for a high-profile live concert headlined by Grammy Award Winner Pt. Vishwa Mohan Bhatt, Amyt Datta, and Pt. Subhen Chatterjee.",
                    "Oversaw technical sound riders, stage lighting choreography, acoustic balancing, and VVIP hospitality for 500+ elite attendees.",
                    "Executed flawless 3-hour live delivery under strict time constraints, resolving acoustic and scheduling adjustments on the fly."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Event Management & Promotion, Global Marketing Strategy, Strategic Brand Management, Consumer Behavior, Business Communication."
        },
        "certifications": [
            "Service Marketing: A Practical Approach — IIT Kharagpur (NPTEL)",
            "Digital Marketing Professional Certificate — Google",
            "Generative AI for Content & Visual Media — Outskill",
            "AI Productivity & Automation Tools — be10x"
        ],
        "technical_skills": {
            "Event Management Tools": "AV Technical Rider Coordination, Stage Staging Diagrams, Gantt Schedule Planning, Floorplan Layouts",
            "Creative & Digital Media": "Photography & Video Production, Canva AI, Adobe Premiere Pro (Basic), Social Media Coverage",
            "Productivity & Budgeting": "MS Excel (Event P&L, Vendor Rate Sheets, Asset Inventories), Google Workspace",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "06",
        "slug": "06_Management_Trainee_General",
        "role_title": "Management Trainee — General Management",
        "focus_area": "Rotational Business Operations, Cross-Functional Strategy, Financial Modeling & Commercial Execution",
        "target_companies": "Deloitte, EY, Goldman Sachs, JPMorgan, Amazon, Tata Group",
        "summary": (
            "High-agility Management Trainee candidate with a comprehensive BBA in International Business and 8 years of entrepreneurial and corporate "
            "operational experience. Demonstrated cross-functional mastery spanning B2B business development (written commendation at Pencil Mark), AI data "
            "operations (Instawork), and 300+ successful project deliveries. Highly analytical, commercially astute, and ready to drive rapid value across "
            "cross-departmental rotational programs."
        ),
        "core_competencies": [
            "Cross-Functional Operational Leadership",
            "Financial Modeling & Unit Economics Analysis",
            "Strategic Planning & Market Intelligence",
            "B2B Commercial Strategy & Client Management",
            "Process Mapping & Continuous Improvement",
            "Data-Driven Problem Solving & Root Cause Analysis",
            "Stakeholder Presentation & Executive Communication",
            "Rapid Learning Agility & Execution Discipline"
        ],
        "experiences": [
            {
                "title": "Lead Operations & Project Director",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Orchestrated 300+ end-to-end multi-disciplinary projects, managing budget allocations, procurement, risk mitigation, and team execution.",
                    "Negotiated primary vendor contracts cutting operational overhead by 15%, reinvesting savings to boost delivery quality and client satisfaction.",
                    "Maintained a 30%+ client retention rate through systematic account governance and transparent milestone reporting for clients like Tata Communications and Puma."
                ]
            },
            {
                "title": "Business Development & Strategy Intern",
                "organization": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    "Conducted competitive market mapping and executed outbound B2B lead campaigns, building a qualified INR 1.5L+ commercial project pipeline.",
                    "Managed 15+ concurrent corporate account threads with rigorous SLA follow-up, earning written commendation from the executive leadership.",
                    "Synthesized client requirements into standardized commercial proposals, speeding up executive deal approvals by 20%."
                ]
            },
            {
                "title": "AI Data Operations Analyst",
                "organization": "Instawork Services India Pvt Ltd",
                "location": "Bengaluru, India",
                "period": "Dec 2025",
                "bullets": [
                    "Structured and audited high-velocity ML activity datasets with 99%+ quality compliance and 100% on-time milestone delivery.",
                    "Collaborated across operations and technology interfaces to refine data guidelines, standardizing SOPs for high-volume execution."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Strategic Management, Corporate Finance, International Trade & EXIM, Organizational Behavior, Business Analytics, Marketing Management."
        },
        "certifications": [
            "Service Marketing: A Practical Approach — IIT Kharagpur (NPTEL / Swayam)",
            "Google Project Management Foundations — Google",
            "Generative AI Mastermind — Outskill",
            "Digital Marketing Professional Certificate — Google"
        ],
        "technical_skills": {
            "Business & Financial Analytics": "MS Excel (Financial Modeling, Scenario Analysis, Pivot Tables), Power BI Basics, Financial Ratios",
            "Workflow & Collaboration": "Jira, Notion AI, Trello, Google Workspace, MS PowerPoint (Executive Deck Design)",
            "AI & Automation": "ChatGPT-4, Claude, Clay AI, Prompt Engineering, Workflow Automation",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "07",
        "slug": "07_Global_Operations_Strategy",
        "role_title": "Global Operations & Strategy Analyst",
        "focus_area": "Cross-Border Business Strategy, International Trade Architecture, Operating Model Optimization",
        "target_companies": "Deloitte, EY, Maersk, Goldman Sachs, Schneider Electric, Boeing",
        "summary": (
            "Strategically minded Global Operations Analyst with specialized academic rigor in BBA International Business and practical experience "
            "navigating complex multi-stakeholder and cross-regional operating environments. Strong foundation in international trade policy, Incoterms 2020, "
            "operating model design, and cross-border vendor governance. Adept at leveraging quantitative analysis and AI workflows to identify operational "
            "inefficiencies and execute scalable expansion strategies."
        ),
        "core_competencies": [
            "Global Operating Model Analysis & Design",
            "Cross-Border Trade & EXIM Regulatory Strategy",
            "International Vendor & Supplier Governance",
            "Operational Risk Mitigation & Compliance",
            "Cost-Benefit Analysis & Financial Modeling",
            "Interstate / Cross-Regional Operations Migration",
            "Quantitative Research & Market Sizing",
            "Strategic Stakeholder Alignment & Presentation"
        ],
        "experiences": [
            {
                "title": "Global Operations & Logistics Lead",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Architected operational logistics frameworks for 300+ complex deployments, balancing multi-tier supply networks, localized regulations, and tight SLA schedules.",
                    "Achieved 15% recurring cost savings by eliminating intermediary layers and establishing direct supply networks across South India.",
                    "Successfully delivered brand activations and operations for global multinational corporations including Tata Communications, Puma, HP, and Intel."
                ]
            },
            {
                "title": "Exhibition Operations Lead — AERO India 2025",
                "organization": "Salt in My Coca (Defense & Aerospace Expo)",
                "location": "Bengaluru, India",
                "period": "Feb 2025",
                "bullets": [
                    "Represented executive operations at Asia's premier aerospace expo, managing stall logistics amidst 700+ global defense contractors and international delegations.",
                    "Ensured 100% adherence to rigorous defense export exhibition guidelines, security protocols, and international visitor management standards.",
                    "Maintained flawless asset integrity and continuous supply chain flow throughout the 7-day high-density trade exhibition."
                ]
            },
            {
                "title": "Operations & Market Expansion Associate",
                "organization": "Family Trading Enterprise",
                "location": "Kolkata & Bengaluru, India",
                "period": "2018 – 2020",
                "bullets": [
                    "Coordinated the strategic cross-regional operational transfer of business inventory and vendor relations from Kolkata to Bengaluru.",
                    "Conducted local market feasibility studies, supplier mapping, and competitive pricing analysis to establish sustainable regional operations.",
                    "Restructured supplier credit terms and inventory holding cycles, improving operating cash flow by 15%."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "International Trade Policy & EXIM, Global Strategic Management, Foreign Exchange & International Finance, International Marketing, Business Research Methods."
        },
        "certifications": [
            "Incoterms 2020 & International Trade Architecture — International Trade Frameworks",
            "Service Marketing & Strategic Delivery — IIT Kharagpur (NPTEL)",
            "Google Data Analytics Professional Certificate — Google",
            "Generative AI Mastermind — Outskill"
        ],
        "technical_skills": {
            "Strategy & Analytics": "MS Excel (Scenario Analysis, Sensitivity Modeling, Pivot Tables), Power BI (Dashboards), Google Sheets",
            "Research & Mapping": "Miro (Process & Value Stream Mapping), Market Sizing Models, PESTLE / Porter's Five Forces Frameworks",
            "AI & Workflow Automation": "ChatGPT-4, Claude 3.5, Clay AI, Notion AI, Google Workspace",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "08",
        "slug": "08_Customer_Success_Account_Management",
        "role_title": "Customer Success & Account Management Associate",
        "focus_area": "Client Retention (30%+ Repeat Rate), Account Onboarding, Escalation Resolution & Upselling",
        "target_companies": "Razorpay, Swiggy, CRED, Google, Amazon, Salesforce ecosystem",
        "summary": (
            "Client-centric Customer Success & Account Management professional with a proven track record of maintaining a 30%+ organic repeat "
            "client rate across 300+ project engagements. Managed 15+ concurrent enterprise client accounts at Pencil Mark Interior Solutions, accelerating "
            "delivery cycles and receiving written commendation from management. Highly skilled in stakeholder communication, proactive issue resolution, "
            "and maximizing customer lifetime value (LTV)."
        ),
        "core_competencies": [
            "Enterprise Account Management & Retention",
            "Client Onboarding & Stakeholder Communication",
            "30%+ Repeat Client Rate / Customer Loyalty",
            "Churn Prevention & Proactive Health Scoring",
            "Escalation Management & Rapid Crisis Resolution",
            "Consultative Upselling & Cross-Selling",
            "Customer Satisfaction (CSAT / NPS) Optimization",
            "SLA Adherence & Cross-Team Coordination"
        ],
        "experiences": [
            {
                "title": "Client Account & Business Development Intern",
                "organization": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    "Managed end-to-end communication for 15+ commercial client accounts, serving as the primary bridge between clients and design execution teams.",
                    "Conducted milestone review calls and resolved project scope adjustments, accelerating contract sign-offs and generating INR 1.5L+ in project value.",
                    "Received formal written management commendation for exceptional client relationship management, empathy, and responsiveness."
                ]
            },
            {
                "title": "Lead Account & Client Relations Director",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Built and nurtured a loyal portfolio of corporate and private clients, achieving a 30%+ repeat engagement rate without paid advertising.",
                    "Serviced high-profile enterprise accounts including Tata Communications, Puma, HP, and Intel, ensuring 100% SLA satisfaction on live deployments.",
                    "Conducted post-delivery retrospectives and feedback sessions, implementing service improvements that elevated NPS ratings."
                ]
            },
            {
                "title": "VIP Client & Artist Hospitality Coordinator",
                "organization": "TRILOGY Concert / AERO India 2025",
                "location": "Bengaluru, India",
                "period": "2025 – 2026",
                "bullets": [
                    "Delivered personalized, high-touch account management for international dignitaries, corporate executives, and Grammy-winning artists.",
                    "Anticipated client friction points in advance, providing immediate troubleshooting that maintained 100% stakeholder satisfaction."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Customer Relationship Management, Service Marketing, Consumer Behavior, Professional Communication, Business Analytics."
        },
        "certifications": [
            "HubSpot Customer Service & CRM Certification",
            "Service Marketing: A Practical Approach — IIT Kharagpur (NPTEL)",
            "Digital Marketing Professional Certificate — Google",
            "Generative AI for Client Communication — Outskill"
        ],
        "technical_skills": {
            "CRM & Success Platforms": "HubSpot CRM, Salesforce Basics, Zendesk Overview, Notion Client Portals",
            "Analytics & Health Tracking": "MS Excel (Account Tracking, Renewal Forecasts, NPS Metrics), Google Sheets",
            "Communication & Collaboration": "Slack, MS Teams, Zoom, Executive Email Sequencing, Presentation Pitch Decks",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "09",
        "slug": "09_Procurement_Vendor_Management_Specialist",
        "role_title": "Procurement & Vendor Management Specialist",
        "focus_area": "Strategic Sourcing, Contract Negotiation, 15% Cost Savings, Vendor Scorecards & TCO",
        "target_companies": "Schneider Electric, Amazon, Boeing, Walmart, Maersk, Tata Group",
        "summary": (
            "Commercially astute Procurement & Vendor Management Specialist with proven experience driving 15% recurring cost reductions "
            "across 300+ operational deployments. Expert in direct supplier sourcing, contract rate negotiations, SLA governance, and Total Cost of "
            "Ownership (TCO) optimization. Combines BBA International Business trade fundamentals with sharp commercial negotiation skills to protect margins "
            "and eliminate supply chain risk."
        ),
        "core_competencies": [
            "Strategic Sourcing & Category Management",
            "Vendor Contract & Price Negotiation (15% Cost Savings)",
            "Supplier Quality & SLA Performance Scorecarding",
            "RFP / RFQ Preparation & Bid Evaluation",
            "Total Cost of Ownership (TCO) Analysis",
            "Purchase Order (PO) Lifecycle & Payment Terms",
            "Supply Chain Risk Mitigation & Alternate Sourcing",
            "Commercial Terms & Dispute Resolution"
        ],
        "experiences": [
            {
                "title": "Lead Procurement & Vendor Operations Specialist",
                "organization": "Independent Operations & Event Practice",
                "location": "Bengaluru, India",
                "period": "2019 – Present",
                "bullets": [
                    "Built and governed a verified network of 50+ primary suppliers across AV technology, staging, fabrication, and freight logistics in South India.",
                    "Systematically eliminated intermediary agency markups, delivering a documented 15% per-deployment cost reduction across 300+ projects.",
                    "Implemented vendor performance scorecards assessing on-time delivery, technical quality, and rate competitiveness.",
                    "Negotiated extended credit terms and volume discount tiers, optimizing operating cash flow and budget predictability."
                ]
            },
            {
                "title": "Sourcing & Operations Co-Founder",
                "organization": "Mehra's Kitchen & Food Operations",
                "location": "Bengaluru, India",
                "period": "2025",
                "bullets": [
                    "Managed end-to-end raw material and packaging procurement, benchmarking supplier quotes to reduce unit food costs by 12%.",
                    "Established backup supplier relationships for critical inventory categories, mitigating single-source supply chain vulnerabilities.",
                    "Monitored daily inventory wastage and pricing fluctuations, maintaining strict food-cost margins under 32%."
                ]
            },
            {
                "title": "Commercial Procurement & Sales Associate",
                "organization": "Family Trading Business",
                "location": "Kolkata, India",
                "period": "2018 – 2020",
                "bullets": [
                    "Managed vendor purchase orders, inventory stocking thresholds, and supplier invoice reconciliation in a high-turnover retail business.",
                    "Negotiated seasonal bulk purchase rebates with commercial distributors, increasing gross trading margins by 8%."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Supply Chain Management, Cost Accounting, International Trade & EXIM, Commercial Law & Contracts, Strategic Sourcing."
        },
        "certifications": [
            "Strategic Sourcing & Procurement Foundations — Online / Professional Module",
            "Service Marketing & Supply Chain — IIT Kharagpur (NPTEL)",
            "Google Data Analytics Professional Certificate — Google",
            "AI Tools for Commercial Negotiation & Data Analysis — be10x"
        ],
        "technical_skills": {
            "Procurement & Sourcing Tools": "ERP Basics (SAP MM Overview, Purchase Orders, Goods Receipt), Vendor Rate Databases",
            "Financial & Cost Modeling": "MS Excel (Cost Breakdown Structures, TCO Models, Pivot Tables, Spend Analysis), Google Sheets",
            "Contracting & Compliance": "Incoterms 2020, RFP / RFQ Documentation, Master Service Agreements (MSA) Overview",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    },
    {
        "id": "10",
        "slug": "10_Product_Operations_Associate",
        "role_title": "Product Operations Associate",
        "focus_area": "Tech + Ops Hybrid, AI Pipeline Optimization, Workflow Automation, QA & Cross-Functional Execution",
        "target_companies": "Google, Microsoft, Amazon, Razorpay, Swiggy, CRED, Instawork",
        "summary": (
            "Technically savvy Product Operations Associate bridging software/AI capabilities with rigorous on-ground execution. Handled "
            "ML activity datasets with 99%+ quality accuracy at Instawork AI and engineered generative AI automated workflows across multiple business "
            "ventures. Proficient in cross-functional coordination, operational metric instrumentation, feature feedback loops, and building agile standard "
            "operating procedures (SOPs) for high-scale environments."
        ),
        "core_competencies": [
            "Product & AI Operations Bridge (Tech + Ops)",
            "ML Data Pipeline QA & Annotation Workflows (99%+ Accuracy)",
            "Operational Metrics Instrumentation (TAT, Error Rate, SLA)",
            "Workflow Automation via Generative AI & Low-Code Tools",
            "User Feedback Synthesis & Feature Backlog Triage",
            "Cross-Functional Coordination (Engineering, Operations, Business)",
            "Standard Operating Procedure (SOP) Documentation",
            "Root Cause Analysis & Agile Iteration"
        ],
        "experiences": [
            {
                "title": "AI Product Operations & Data Analyst",
                "organization": "Instawork Services India Pvt Ltd",
                "location": "Bengaluru, India",
                "period": "Dec 2025",
                "bullets": [
                    "Managed high-throughput data labeling and verification cycles for robotics and activity-recognition models, achieving a 99%+ QA benchmark.",
                    "Identified edge cases and workflow bottlenecks, collaborating directly with engineering and ops leads to refine model ingestion taxonomies.",
                    "Maintained 100% on-time milestone delivery across all assigned data sprints, reducing sprint review cycle times."
                ]
            },
            {
                "title": "Operations & Workflow Automation Lead",
                "organization": "Independent Operations & Consultancy",
                "location": "Bengaluru, India",
                "period": "2024 – Present",
                "bullets": [
                    "Automated end-to-end lead qualification, document generation, and customer communication workflows using ChatGPT-4, Claude, and Clay AI.",
                    "Created structured knowledge repositories and project tracking boards in Notion and Jira, reducing operational ramp-up times for new team members.",
                    "Monitored and iterated on process performance metrics across 300+ deployments, driving continuous productivity gains."
                ]
            },
            {
                "title": "Business Intelligence & Operations Intern",
                "organization": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    "Mapped the customer lifecycle journey, diagnosing operational handoff delays between sales outreach and architectural design execution.",
                    "Built centralized project tracking sheets that improved multi-department visibility on 15+ concurrent commercial client deliverables.",
                    "Recognized with formal written commendation for operational leadership, process discipline, and cross-functional agility."
                ]
            }
        ],
        "education": {
            "degree": "Bachelor of Business Administration (BBA) — International Business",
            "institution": "Dayananda Sagar University",
            "location": "Bengaluru, Karnataka",
            "period": "2023 – May 2026 (Class of 2026)",
            "coursework": "Business Analytics, Information Systems, Strategic Management, International Business Systems, Project Management."
        },
        "certifications": [
            "Generative AI Mastermind & Prompt Engineering — Outskill (Oct 2025)",
            "AI Tools & Workflow Automation — be10x (Jan 2026)",
            "Google Data Analytics Professional Certificate — Google",
            "Google Project Management Foundations — Google"
        ],
        "technical_skills": {
            "Product & Project Tools": "Jira, Confluence, Trello, Notion AI, Linear Overview, Miro (User Journey Mapping)",
            "AI & Low-Code Systems": "ChatGPT-4, Claude 3.5 Sonnet, Clay AI, Prompt Engineering, Make / Zapier Basics",
            "Data & Scripting": "MS Excel / Google Sheets (Advanced Formulas, Pivot Tables), Python Basics (Data Processing, Automation), SQL Basics",
            "Languages": "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational)"
        }
    }
]

def generate_resume_markdown(variant):
    lines = []
    lines.append(f"# ADITYA MEHRA")
    lines.append(f"**Target Role: {variant['role_title']}**  ")
    lines.append(f"**Focus Area:** {variant['focus_area']}  ")
    lines.append(f"Bengaluru, Karnataka, India | Phone: +91 7003456624 | Email: adityamehra799@gmail.com | LinkedIn: linkedin.com/in/aditya-mehra-b8644b326")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## PROFESSIONAL SUMMARY")
    lines.append(variant['summary'])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## CORE COMPETENCIES")
    for comp in variant['core_competencies']:
        lines.append(f"- **{comp}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## PROFESSIONAL EXPERIENCE")
    lines.append("")
    for exp in variant['experiences']:
        lines.append(f"### {exp['title']} — {exp['organization']}")
        lines.append(f"*{exp['location']} | {exp['period']}*")
        lines.append("")
        for bullet in exp['bullets']:
            lines.append(f"- {bullet}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## EDUCATION")
    lines.append("")
    edu = variant['education']
    lines.append(f"### {edu['degree']}")
    lines.append(f"**{edu['institution']}**, {edu['location']} | *{edu['period']}*")
    lines.append(f"- **Key Coursework**: {edu['coursework']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## CERTIFICATIONS & PROFESSIONAL CREDENTIALS")
    for cert in variant['certifications']:
        lines.append(f"- **{cert}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## TECHNICAL SKILLS & TOOLS")
    for cat, tools in variant['technical_skills'].items():
        lines.append(f"- **{cat}**: {tools}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## TARGET ALIGNMENT")
    lines.append(f"- **Target Companies**: {variant['target_companies']}")
    lines.append(f"- **ATS Keyword Optimization**: Fully optimized for automated applicant tracking parsing and scoring across {variant['role_title']} requisitions.")
    lines.append("")
    return "\n".join(lines)

def generate_master_collection(variants):
    lines = []
    lines.append("# ADITYA MEHRA — MASTER RESUME VARIANTS COLLECTION")
    lines.append("## 10 Targeted, ATS-Optimized Career Profiles")
    lines.append("**Candidate:** Aditya Mehra | BBA International Business (Dayananda Sagar University, Class of 2026)")
    lines.append("**Contact:** +91 7003456624 | adityamehra799@gmail.com | Bengaluru, India")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### Executive Overview & Strategic Directory")
    lines.append("")
    lines.append("| # | Role Variant | Primary Focus Area | Target Companies | Key Differentiator |")
    lines.append("|---|---|---|---|---|")
    for v in variants:
        lines.append(f"| {v['id']} | [{v['role_title']}](#{v['slug'].lower().replace('_', '-')}) | {v['focus_area']} | {v['target_companies']} | 300+ Deployments, 15% Cost Savings, 99%+ Accuracy |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for i, v in enumerate(variants):
        lines.append(f"<a name=\"{v['slug'].lower().replace('_', '-')}\"></a>")
        lines.append(f"## Variant {v['id']}: {v['role_title']}")
        lines.append("")
        resume_md = generate_resume_markdown(v)
        lines.append(resume_md)
        lines.append("\n\n" + "="*80 + "\n\n")
        
    return "\n".join(lines)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating 10 role-specific resume variants into {OUTPUT_DIR}...")
    
    for variant in RESUME_VARIANTS:
        file_path = os.path.join(OUTPUT_DIR, f"{variant['slug']}.md")
        content = generate_resume_markdown(variant)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [+] Created: {file_path}")
        
    print(f"\nGenerating Master Collection at {MASTER_FILE}...")
    master_content = generate_master_collection(RESUME_VARIANTS)
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        f.write(master_content)
    print(f"  [+] Created: {MASTER_FILE}")
    
    print("\nAll 10 Resume Variants and Master Collection generated successfully!")

if __name__ == "__main__":
    main()
