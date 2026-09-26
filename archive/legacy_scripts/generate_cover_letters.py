"""
Script: generate_cover_letters.py
Generates 50 company-specific cover letters for top target companies.
Candidate: Aditya Mehra (BBA International Business, DSU Class of 2026)
Outputs:
- e:/anti/cover_letters/ directory with 50 individual .txt files
- e:/anti/Cover_Letters_Master_Collection.md (Master Markdown document)
"""

import sys
import os

# Set stdout encoding to utf-8 for Windows PowerShell
sys.stdout.reconfigure(encoding='utf-8')

CANDIDATE_NAME = "Aditya Mehra"
CANDIDATE_EMAIL = "adityamehra799@gmail.com"
CANDIDATE_PHONE = "+91-7003456624"
CANDIDATE_LINKEDIN = "https://www.linkedin.com/in/adityamehra"
CANDIDATE_EDU = "Bachelor of Business Administration (BBA) in International Business, Dayananda Sagar University (DSU), Bengaluru (Class of 2026)"
CANDIDATE_LOCATION = "Bengaluru, Karnataka, India"

# 50 Company Definitions with customized role, track, value hook, proof points, and specific department
COMPANIES_DATA = [
    {
        "id": 1,
        "company": "Walmart Global Tech India",
        "role": "Operations Analyst (Supply Chain & Omnichannel)",
        "track": "Operations & SCM",
        "location": "Ecospace ORR / Sarjapur, Bengaluru",
        "hiring_mgr": "Talent Acquisition & Early Careers Team",
        "company_hook": "Walmart's unmatched scale in global retail supply chains and omnichannel fulfillment",
        "proof_points": [
            "Orchestrated 300+ live operations deployments with zero budget overruns and 15% cost optimization through direct vendor negotiations.",
            "Deep coursework in International Supply Chain Management, Incoterms 2020, and logistics bottleneck analysis at DSU.",
            "Advanced analytical toolkit in MS Excel (Pivot Tables, VLOOKUP, data modeling) and Power BI for tracking operational SLAs."
        ],
        "fit_pitch": "Walmart Global Tech requires analysts who can bridge on-ground execution with algorithmic efficiency. My dual background in leading high-stakes on-ground operations (AERO India 2025, Puma) and quantitative coursework in international supply chains positions me to drive immediate cost and SLA improvements for Walmart's global retail network."
    },
    {
        "id": 2,
        "company": "Amazon India",
        "role": "Operations Analyst (Fulfillment & Vendor Performance)",
        "track": "Operations & SCM",
        "location": "WTC Rajajinagar / RMZ Ecoworld, Bengaluru",
        "hiring_mgr": "Amazon Operations University Recruiting Team",
        "company_hook": "Amazon's customer-obsessed logistics infrastructure and high-velocity fulfillment centers",
        "proof_points": [
            "Delivered 15% operational cost reduction by restructuring vendor contracts and eliminating middleman markups across complex staging operations.",
            "Led cross-functional teams of 20+ members across multi-day deployments including AERO India 2025 (100,000+ attendees).",
            "Proficient in inventory tracking, root-cause analysis, and end-to-end milestone tracking under strict Amazonian operational standards."
        ],
        "fit_pitch": "Having managed live, high-pressure environments with tight SLAs and multi-vendor dependencies, I bring the bias for action, frugality, and ownership required to optimize Amazon's middle-mile and fulfillment workflows."
    },
    {
        "id": 3,
        "company": "Deloitte US-India (USI)",
        "role": "Business Operations & Advisory Analyst",
        "track": "Operations Consulting",
        "location": "RMZ Ecoworld, Outer Ring Road, Bengaluru",
        "hiring_mgr": "Deloitte US-India Campus Talent Acquisition",
        "company_hook": "Deloitte's market-leading advisory practice driving enterprise transformation and operational rigor",
        "proof_points": [
            "Generated INR 1.5L+ B2B revenue and handled 15+ concurrent corporate pipelines at Pencil Mark Interior Solutions, earning written leadership commendation.",
            "Managed multi-tiered project budgets and procurement restructuring, achieving a 15% recurring overhead reduction.",
            "Strong academic foundation in International Business, financial modeling, and risk mitigation frameworks."
        ],
        "fit_pitch": "Deloitte's consulting teams demand structured problem-solving, stakeholder empathy, and meticulous execution. My proven ability to convert ambiguous business requirements into high-margin outcomes makes me an immediate value-add for client engagements."
    },
    {
        "id": 4,
        "company": "Ernst & Young (EY GDS)",
        "role": "Global Operations & Business Analyst",
        "track": "Operations Consulting",
        "location": "Manyata Tech Park, Hebbal, Bengaluru",
        "hiring_mgr": "EY Global Delivery Services Early Careers Team",
        "company_hook": "EY GDS's international delivery footprint helping Fortune 500 enterprises optimize global shared services",
        "proof_points": [
            "Comprehensive grounding in International Business, EXIM frameworks, Incoterms 2020, and cross-border commercial compliance.",
            "Executed 300+ multi-stakeholder operational deployments across high-profile corporate accounts (Tata Communications, Puma India).",
            "Certified in Google Digital Marketing & NPTEL Service Marketing (IIT Kharagpur) with proven B2B stakeholder coordination."
        ],
        "fit_pitch": "I bring the perfect blend of global business academic acumen and battle-tested operational discipline to EY GDS, ready to streamline cross-border business workflows and support senior advisory leadership."
    },
    {
        "id": 5,
        "company": "A.P. Moller - Maersk",
        "role": "EXIM & Ocean Freight Logistics Coordinator",
        "track": "EXIM & Global Logistics",
        "location": "Outer Ring Road / Whitefield, Bengaluru",
        "hiring_mgr": "Maersk Global Service Centres Talent Team",
        "company_hook": "Maersk's integrated container logistics ecosystem connecting and simplifying global trade",
        "proof_points": [
            "Specialized academic mastery in International Trade & EXIM procedures, Incoterms 2020, HS Code classification, and UCP 600 Letter of Credit compliance.",
            "Hands-on experience in freight vendor negotiations, bonded warehousing logistics, and customs clearance workflows.",
            "Track record of achieving 15% cost savings in supply chain operations through consolidated logistics planning."
        ],
        "fit_pitch": "As a dedicated BBA International Business graduate with deep exposure to trade documentation and maritime supply chains, I am eager to apply my knowledge of freight forwarding, customs workflows, and SLA management to Maersk's end-to-end integrator mission."
    },
    {
        "id": 6,
        "company": "DHL Supply Chain India",
        "role": "Global Supply Chain & EXIM Operations Coordinator",
        "track": "EXIM & Global Logistics",
        "location": "Whitefield / Airport Logistics Hub, Bengaluru",
        "hiring_mgr": "DHL Supply Chain Talent Acquisition",
        "company_hook": "DHL's unmatched global contract logistics excellence and green supply chain initiatives",
        "proof_points": [
            "In-depth command of international trade documentation: Bills of Lading, Shipping Bills, Certificates of Origin, and Letters of Credit (UCP 600).",
            "Managed on-ground logistics for large-scale operations including 7-day aerospace stall management at AERO India 2025.",
            "Analytical capability in route optimization, freight benchmarking, and multi-tier vendor management."
        ],
        "fit_pitch": "My rigorous education in cross-border trade at DSU combined with practical on-ground logistics leadership will allow me to hit the ground running in DHL's fast-moving freight forwarding and supply chain operations."
    },
    {
        "id": 7,
        "company": "Goldman Sachs India",
        "role": "Operations Analyst (Global Markets & Trade Operations)",
        "track": "Financial Operations",
        "location": "Helios Business Park, Outer Ring Road, Bengaluru",
        "hiring_mgr": "Goldman Sachs University Relations & Operations Recruiting",
        "company_hook": "Goldman Sachs' industry-defining operations division ensuring seamless global market trade settlement and risk management",
        "proof_points": [
            "High-precision data operations experience at Instawork AI, maintaining 99%+ accuracy in structured data workflows under strict audit standards.",
            "Managed multi-million rupee event budgets and family business cash flows with zero reconciliation errors.",
            "Academic coursework in Financial Management, International Trade Finance, and quantitative modeling using Advanced Excel."
        ],
        "fit_pitch": "Goldman Sachs Operations demands zero-defect execution, analytical rigor, and risk consciousness. My proven track record of handling high-stakes logistics and flawless data integrity ensures I will uphold the firm's exacting operational standards."
    },
    {
        "id": 8,
        "company": "JPMorgan Chase & Co.",
        "role": "Corporate Operations Analyst (Trade & Treasury Ops)",
        "track": "Financial Operations",
        "location": "Kadubeesanahalli, Outer Ring Road, Bengaluru",
        "hiring_mgr": "JPMorgan Chase Campus Recruitment",
        "company_hook": "JPMorgan's foundational role in global financial infrastructure, trade finance, and treasury services",
        "proof_points": [
            "Extensive knowledge of international trade financing instruments, Letters of Credit, Bank Guarantees, and UCP 600 governance.",
            "Proven ability to streamline workflows and reduce operational costs by 15% through meticulous process re-engineering.",
            "Exceeded performance benchmarks in B2B client management with formal written commendation for precision and accountability."
        ],
        "fit_pitch": "I am excited to bring my knowledge of international trade documentation, quantitative analysis, and rigorous process execution to JPMorgan's Corporate & Investment Bank Operations group in Bengaluru."
    },
    {
        "id": 9,
        "company": "Google India",
        "role": "AI Data Operations Associate (Multimodal & Knowledge Systems)",
        "track": "AI Data Operations",
        "location": "RMZ Infinity, Old Madras Road, Bengaluru",
        "hiring_mgr": "Google People Operations & AI Talent Team",
        "company_hook": "Google's groundbreaking frontier AI models (Gemini) and large-scale data systems powering ambient intelligence",
        "proof_points": [
            "Executed AI Data Operations at Instawork AI, structuring and validating complex multimodal datasets with 99%+ quality scores.",
            "Certified in Generative AI (Outskill) and Prompt Engineering, mastering dataset benchmarking and human-in-the-loop evaluation.",
            "BBA in International Business providing cross-cultural semantic understanding and structured taxonomy development."
        ],
        "fit_pitch": "Building state-of-the-art AI requires pristine training data pipelines and relentless operational quality. My hands-on experience in ML data validation combined with structured analytical workflows ensures immediate contribution to Google's AI data infrastructure."
    },
    {
        "id": 10,
        "company": "Microsoft India R&D",
        "role": "AI Data Operations & Platform Associate",
        "track": "AI Data Operations",
        "location": "Prestige Ferns Galaxy, Bellandur, Bengaluru",
        "hiring_mgr": "Microsoft University Recruiting Team",
        "company_hook": "Microsoft's enterprise AI leadership across Copilot, Azure AI, and large-scale foundation model deployments",
        "proof_points": [
            "Maintained 99%+ accuracy in annotating and structuring high-dimensional dataset pipelines for ML applications at Instawork AI.",
            "Strong foundation in data schema design, quality auditing, and workflow automation using Excel and Power BI.",
            "Experience managing 15+ concurrent operational threads under stringent SLA constraints."
        ],
        "fit_pitch": "I combine operational discipline with specialized AI data operations experience, ready to empower Microsoft's engineering teams by maintaining world-class data quality standards for enterprise AI workloads."
    },
    {
        "id": 11,
        "company": "The Boeing Company (Boeing India)",
        "role": "Global Supply Chain & Trade Compliance Analyst",
        "track": "Aerospace & SCM",
        "location": "Boeing India Engineering & Technology Center (BIETC), Bengaluru",
        "hiring_mgr": "Boeing Global Supply Chain Talent Acquisition",
        "company_hook": "Boeing's cutting-edge aerospace engineering campus in Bengaluru and global supplier ecosystem",
        "proof_points": [
            "Led on-ground exhibition and visitor operations at AERO India 2025 at Yelahanka Air Force Station across 7 high-security days.",
            "In-depth knowledge of aerospace defense procurement guidelines, Incoterms 2020, and dual-use export control compliance.",
            "Achieved 15% cost savings through supplier rationalization and primary vendor contract negotiations."
        ],
        "fit_pitch": "Having operated directly inside the high-security environment of AERO India 2025 coupled with my specialized BBA in International Business and trade compliance training, I offer the ideal blend of aerospace context and supply chain rigor for Boeing's BIETC operations."
    },
    {
        "id": 12,
        "company": "Schneider Electric India",
        "role": "Supply Chain & Procurement Operations Specialist",
        "track": "Industrial Operations",
        "location": "Bearys Global Research Triangle, Whitefield, Bengaluru",
        "hiring_mgr": "Schneider Electric Early Talent Acquisition",
        "company_hook": "Schneider Electric's global leadership in energy management, industrial automation, and sustainable supply chains",
        "proof_points": [
            "Engineered procurement workflows reducing overheads by 15% through primary vendor consolidation.",
            "Mastery of international logistics, HS codes, freight forwarding, and inventory optimization frameworks.",
            "Successfully coordinated 300+ operational deployments with multi-tier vendor SLAs and zero timeline slippages."
        ],
        "fit_pitch": "Schneider Electric's focus on digitized, resilient supply chains aligns perfectly with my analytical problem-solving and hands-on procurement experience. I am prepared to drive cost efficiencies and supplier reliability across Schneider's manufacturing and distribution hubs."
    },
    {
        "id": 13,
        "company": "Razorpay",
        "role": "B2B Business Development Specialist (Enterprise Merchant Growth)",
        "track": "B2B Business Development",
        "location": "Koramangala / SJR Cyber LXP, Bengaluru",
        "hiring_mgr": "Razorpay Talent Acquisition Team",
        "company_hook": "Razorpay's market-defining financial technology ecosystem powering millions of Indian businesses",
        "proof_points": [
            "Generated INR 1.5L+ in direct B2B revenue and qualified enterprise leads at Pencil Mark Interior Solutions, receiving formal commendation.",
            "Spearheaded end-to-end sales outreach, merchant discovery calls, and multi-threaded contract negotiations.",
            "Certified in Digital Marketing (Google) with deep understanding of fintech onboarding funnels and merchant unit economics."
        ],
        "fit_pitch": "Razorpay's aggressive growth requires hungry, data-backed BD specialists who can command B2B conversations and close deals. Having delivered direct revenue and managed enterprise client relationships, I am ready to accelerate Razorpay's merchant adoption."
    },
    {
        "id": 14,
        "company": "Swiggy (Bundl Technologies)",
        "role": "Operations Analyst (Instamart & City Logistics)",
        "track": "Quick Commerce Operations",
        "location": "Devarabisanahalli, Outer Ring Road, Bengaluru",
        "hiring_mgr": "Swiggy Campus & Operations Hiring Team",
        "company_hook": "Swiggy's hyper-efficient on-demand delivery network and rapid expansion of Instamart quick commerce",
        "proof_points": [
            "Orchestrated 300+ real-time ops deployments under intense timeline constraints with 100% on-time milestone delivery.",
            "Co-founded and operated a cloud kitchen venture, mastering dark store unit economics, spoilage control, and inventory replenishment.",
            "Reduced operational overhead by 15% through hands-on vendor restructuring and route streamlining."
        ],
        "fit_pitch": "Quick commerce is a game of minutes and unit economics. My firsthand experience running food/retail operations and managing 300+ on-ground live deployments makes me uniquely qualified to optimize Swiggy Instamart's dark store throughput and delivery SLAs."
    },
    {
        "id": 15,
        "company": "CRED",
        "role": "Strategic Partnerships & B2B Business Development Associate",
        "track": "B2B Business Development",
        "location": "Indiranagar / HAL 2nd Stage, Bengaluru",
        "hiring_mgr": "CRED Talent Experience Team",
        "company_hook": "CRED's high-trust community of creditworthy individuals and premium merchant monetization ecosystem",
        "proof_points": [
            "Proven track record of managing enterprise relationships with premier luxury and corporate brands (Tata Communications, Puma, VH1).",
            "Generated INR 1.5L+ B2B revenue with written commendation for excellence in client pitch design and partnership negotiation.",
            "Expertise in brand activation and experiential marketing, having coordinated the prestigious TRILOGY Indo-Jazz concert at Bangalore Club."
        ],
        "fit_pitch": "CRED's brand ethos centers on taste, premium curation, and frictionless commerce. Having closed corporate B2B contracts and executed VIP brand activations, I am ready to forge high-converting merchant partnerships for CRED's commerce engine."
    },
    {
        "id": 16,
        "company": "Flipkart",
        "role": "Supply Chain & Logistics Operations Analyst",
        "track": "Operations & SCM",
        "location": "Embassy Tech Village, Outer Ring Road, Bengaluru",
        "hiring_mgr": "Flipkart University & Early Careers Team",
        "company_hook": "Flipkart's homegrown e-commerce supply chain giant (Ekart) delivering to every corner of India",
        "proof_points": [
            "Delivered 15% cost savings through rigorous vendor consolidation and logistics workflow restructuring.",
            "Command of Excel data modeling, capacity planning, and fulfillment center KPI dashboards.",
            "Hands-on leadership of 20+ member ground teams under high-pressure festive/event conditions."
        ],
        "fit_pitch": "Ekart's scale requires obsessive operational discipline and cost consciousness. My demonstrated ability to lead ground teams, eliminate logistics bottlenecks, and manage vendor SLAs fits seamlessly into Flipkart's supply chain operations."
    },
    {
        "id": 17,
        "company": "Zomato / Blinkit",
        "role": "Quick Commerce Operations & Supply Lead",
        "track": "Quick Commerce Operations",
        "location": "Bengaluru Hub / Gurugram HQ",
        "hiring_mgr": "Zomato & Blinkit Operations Recruitment",
        "company_hook": "Blinkit's category-defining 10-minute delivery model transforming Indian urban retail",
        "proof_points": [
            "Direct entrepreneurial background running food and cloud kitchen operations, managing daily procurement and unit economics.",
            "Led on-ground execution for 300+ live event setups, troubleshooting real-time crises with zero downtime.",
            "Optimized vendor pricing models to extract a verified 15% cost reduction."
        ],
        "fit_pitch": "Blinkit's dark store speed depends on relentless on-ground execution and rapid inventory turnover. I bring the entrepreneurial grit and operational battle-testing required to scale store throughput and reduce fulfillment friction."
    },
    {
        "id": 18,
        "company": "McKinsey & Company (McKinsey Capability Center)",
        "role": "Business Operations & Research Analyst",
        "track": "Operations Consulting",
        "location": "Prestige Trade Tower, Palace Road / Bengaluru Hub",
        "hiring_mgr": "McKinsey Talent Acquisition India",
        "company_hook": "McKinsey's world-class strategic counsel and institutional capability building for global industry leaders",
        "proof_points": [
            "BBA in International Business with top-tier academic foundation in global strategy, trade economics, and financial analysis.",
            "Demonstrated commercial acumen by closing INR 1.5L+ B2B contracts with 15+ concurrent corporate stakeholders.",
            "Structured problem-solving skills honed across 300+ operational projects, achieving 15% verified cost reductions."
        ],
        "fit_pitch": "I bring an analytical mindset, high-velocity work ethic, and professional stakeholder poise to McKinsey, eager to assist global client studies and synthesize operational benchmarks with precision."
    },
    {
        "id": 19,
        "company": "Boston Consulting Group (BCG)",
        "role": "Management Consulting Operations Associate",
        "track": "Operations Consulting",
        "location": "UB City / RMZ Ecoworld, Bengaluru",
        "hiring_mgr": "BCG India Recruiting Team",
        "company_hook": "BCG's transformational impact on business strategy, digital innovation, and operational excellence",
        "proof_points": [
            "Strong quantitative foundation in business economics, cross-border supply chain models, and profitability benchmarking.",
            "Recognized with formal written commendation at Pencil Mark for exceptional B2B client acquisition and outreach.",
            "Proven leadership under pressure, directing multi-stakeholder operations at AERO India 2025."
        ],
        "fit_pitch": "BCG's client mandates require razor-sharp insight and execution stamina. My unique combination of entrepreneurial accountability, international business theory, and practical operational leadership makes me an agile asset for BCG consulting teams."
    },
    {
        "id": 20,
        "company": "PricewaterhouseCoopers (PwC Acceleration Center)",
        "role": "Business Operations & Advisory Analyst",
        "track": "Operations Consulting",
        "location": "PwC AC Bangalore, Outer Ring Road, Bengaluru",
        "hiring_mgr": "PwC Acceleration Center Campus Recruitment",
        "company_hook": "PwC's global network delivering trust and sustained business outcomes across enterprise consulting",
        "proof_points": [
            "Excellence in process documentation, vendor management, and contract negotiation delivering 15% cost savings.",
            "Comprehensive training in International Business, EXIM compliance, and corporate financial structures.",
            "Experience managing 15+ concurrent client engagements with structured CRM tracking and rigorous milestone delivery."
        ],
        "fit_pitch": "I offer the analytical rigor, client servicing maturity, and process-driven execution needed to deliver immediate value to PwC AC's global operations advisory practice."
    },
    {
        "id": 21,
        "company": "KPMG India",
        "role": "Management Consulting & Operations Analyst",
        "track": "Operations Consulting",
        "location": "Embassy GolfLinks Business Park, Bengaluru",
        "hiring_mgr": "KPMG India Early Careers Recruitment",
        "company_hook": "KPMG's deep industry expertise in supply chain transformation, business advisory, and operational risk",
        "proof_points": [
            "Deep coursework in International Business Strategy, Supply Chain Optimization, and EXIM Regulatory Frameworks.",
            "Demonstrated cost-reduction capabilities (15% overhead reduction) through direct supplier restructuring.",
            "Successfully coordinated logistics and client relations for enterprise brands including Tata Communications and Puma."
        ],
        "fit_pitch": "My background in International Business, on-ground project management, and cost optimization directly matches KPMG's consulting mandate to unlock operational efficiencies for enterprise clients."
    },
    {
        "id": 22,
        "company": "Cisco Systems India",
        "role": "Global Supply Chain & Vendor Operations Specialist",
        "track": "Tech Supply Chain",
        "location": "Cisco Campus, Cessna Business Park, Bengaluru",
        "hiring_mgr": "Cisco University Talent Acquisition",
        "company_hook": "Cisco's world-leading resilient and digital supply chain network powering global internet infrastructure",
        "proof_points": [
            "In-depth command of global logistics, trade compliance, Incoterms 2020, and customs tariff classification.",
            "Proven track record of managing multi-tier vendor networks and executing 300+ operational deployments with zero SLA breaches.",
            "Proficient in data analytics (Advanced Excel, Power BI) for vendor scorecarding and lead-time tracking."
        ],
        "fit_pitch": "Cisco's award-winning supply chain relies on proactive risk management and strong vendor governance. My blend of international trade education and on-ground logistics execution prepares me to contribute immediately to Cisco's global procurement and supply chain teams."
    },
    {
        "id": 23,
        "company": "Uber India",
        "role": "City Operations & Driver Logistics Analyst",
        "track": "Operations & SCM",
        "location": "Outer Ring Road / Koramangala Hub, Bengaluru",
        "hiring_mgr": "Uber Operations Talent Team",
        "company_hook": "Uber's algorithmic marketplace moving millions of people and goods seamlessly across Indian cities",
        "proof_points": [
            "Managed on-ground deployment logistics for 300+ events with real-time crowd and vendor flow optimization.",
            "Reduced procurement expenses by 15% through primary supplier negotiations and strict cost controls.",
            "Analytical skills in marketplace supply-demand matching, dashboard tracking, and driver partner onboarding."
        ],
        "fit_pitch": "Uber's city operations demand real-time problem solving and data-driven marketplace interventions. Having led high-stress live deployments and analyzed operational bottlenecks, I am primed to optimize Uber's driver supply and ride reliability."
    },
    {
        "id": 24,
        "company": "Ola (ANI Technologies / Ola Electric)",
        "role": "Supply Chain & Operations Associate",
        "track": "Operations & SCM",
        "location": "Regent Insignia, Koramangala / Futurefactory Hub, Bengaluru",
        "hiring_mgr": "Ola Talent Acquisition Team",
        "company_hook": "Ola Electric's mission to drive sustainable mobility through mega-scale vertically integrated manufacturing",
        "proof_points": [
            "Hands-on experience in vendor contract negotiation, achieving 15% recurring cost savings.",
            "Knowledge of automotive component EXIM procedures, customs duties, and inventory buffering.",
            "Led teams of 20+ personnel across multi-day operations with strict quality and safety compliance."
        ],
        "fit_pitch": "Ola's high-speed scale requires scrappy, data-backed operational leaders. My track record of vendor management, cost reduction, and on-ground team leadership will help streamline Ola's supply chain and distribution operations."
    },
    {
        "id": 25,
        "company": "PhonePe",
        "role": "B2B Merchant Acquisition & Growth Specialist",
        "track": "B2B Business Development",
        "location": "Prism Tech Park, Bellandur, Bengaluru",
        "hiring_mgr": "PhonePe University & Sales Hiring Team",
        "company_hook": "PhonePe's digital payments leadership driving financial inclusion and merchant digitization across India",
        "proof_points": [
            "Generated INR 1.5L+ in direct B2B sales revenue with formal written commendation for outstanding conversion.",
            "Managed 15+ concurrent client accounts, orchestrating cold outreach, value demonstration, and final closing.",
            "Certified in Google Digital Marketing with deep knowledge of merchant lifetime value and digital payment workflows."
        ],
        "fit_pitch": "PhonePe's merchant network expansion requires relentless B2B drive and relationship-building capabilities. Having proven my ability to hunt, negotiate, and close enterprise contracts, I am ready to accelerate PhonePe's merchant adoption."
    },
    {
        "id": 26,
        "company": "Zepto (KiranaKart)",
        "role": "Dark Store & Supply Chain Operations Lead",
        "track": "Quick Commerce Operations",
        "location": "Bengaluru Operations Hub / HSR Layout",
        "hiring_mgr": "Zepto Talent Acquisition Team",
        "company_hook": "Zepto's hyper-growth quick commerce model revolutionizing grocery delivery through micro-warehouse density",
        "proof_points": [
            "Hands-on entrepreneurial experience founding and running cloud kitchen operations with daily perishables management.",
            "Delivered 300+ operational deployments on-time and with zero budget overruns.",
            "Restructured procurement pipelines to secure a 15% direct cost reduction."
        ],
        "fit_pitch": "Zepto's dark store efficiency hinges on flawless picking, inventory turnover, and vendor reliability. My frontline experience managing food operations, real-time crisis resolution, and inventory unit economics ensures maximum dark store throughput."
    },
    {
        "id": 27,
        "company": "Tata Motors",
        "role": "Global Sourcing & Supply Chain Operations Analyst",
        "track": "Automotive SCM",
        "location": "Whitefield / Pune / Bengaluru SCM Hub",
        "hiring_mgr": "Tata Motors Early Careers & SCM Recruitment",
        "company_hook": "Tata Motors' pioneering leadership in EV transformation and world-class automotive engineering",
        "proof_points": [
            "Strong academic expertise in International Trade, Incoterms 2020, customs tariffs, and global procurement strategies.",
            "Negotiated directly with industrial vendors to achieve 15% cost optimization.",
            "Executed high-profile corporate activations for Tata Communications with zero execution defects."
        ],
        "fit_pitch": "Tata Motors' aggressive EV roadmap requires resilient global sourcing and lean supply chain workflows. My International Business training, procurement negotiation skills, and proven familiarity with the Tata Group's high ethical standards make me an ideal fit."
    },
    {
        "id": 28,
        "company": "Reliance Retail (JioMart)",
        "role": "Retail Operations & Vendor Management Specialist",
        "track": "Retail Operations",
        "location": "Reliance Corporate Park / Bengaluru Regional Office",
        "hiring_mgr": "Reliance Retail Talent Acquisition Team",
        "company_hook": "Reliance Retail's powerhouse omnichannel ecosystem serving millions of Indian households daily",
        "proof_points": [
            "Managed multi-tier supplier networks, achieving 15% overhead cost reductions through direct vendor negotiations.",
            "Directed on-ground teams of 20+ members across high-footfall activations, including 100,000+ attendee environments.",
            "Proficient in inventory replenishment tracking, vendor SLA governance, and category analytics."
        ],
        "fit_pitch": "Reliance Retail's vast physical and digital network demands ground-level operational mastery and rigorous cost control. My proven experience in vendor management, team leadership, and cost optimization prepares me to drive measurable retail efficiency."
    },
    {
        "id": 29,
        "company": "Infosys",
        "role": "Global Delivery & Business Operations Associate",
        "track": "Global Business Services",
        "location": "Electronics City, Bengaluru",
        "hiring_mgr": "Infosys Campus Recruitment & GBS Hiring",
        "company_hook": "Infosys' iconic global technology consulting footprint enabling enterprise digital transformation worldwide",
        "proof_points": [
            "BBA in International Business from DSU with comprehensive knowledge of cross-border operations and IT governance.",
            "Managed 15+ concurrent corporate client communication pipelines with formal written commendation for stakeholder excellence.",
            "Certified in Google Digital Marketing, NPTEL Service Marketing (IIT Kharagpur), and Generative AI tools."
        ],
        "fit_pitch": "Infosys' global delivery model requires proactive operations coordinators who understand international business dynamics and cross-functional project management. I am prepared to deliver operational consistency and client satisfaction across Infosys' global business units."
    },
    {
        "id": 30,
        "company": "Wipro",
        "role": "Business Operations Analyst (Enterprise SCM)",
        "track": "Global Business Services",
        "location": "Sarjapur Road / Electronics City, Bengaluru",
        "hiring_mgr": "Wipro Early Careers Talent Acquisition",
        "company_hook": "Wipro's technology services and consulting driving digital resilience for Fortune 500 enterprises",
        "proof_points": [
            "Trained in International Supply Chain Management, Incoterms 2020, and global enterprise procurement workflows.",
            "Delivered 15% cost savings through rigorous supplier negotiations and process streamlining.",
            "High-precision data operations background at Instawork AI (99%+ accuracy score)."
        ],
        "fit_pitch": "I bring a rigorous analytical approach, cross-border business understanding, and proven operational discipline to support Wipro's enterprise consulting and supply chain practice."
    },
    {
        "id": 31,
        "company": "HCLTech",
        "role": "Global Infrastructure & Operations Associate",
        "track": "Global Business Services",
        "location": "Jigani Industrial Area / Manyata Tech Park, Bengaluru",
        "hiring_mgr": "HCLTech Campus Talent Acquisition",
        "company_hook": "HCLTech's supercharged engineering services and global IT infrastructure management",
        "proof_points": [
            "Specialized in International Business operations, cross-cultural vendor coordination, and SLA enforcement.",
            "Successfully coordinated 300+ operational events with 100% on-time delivery across corporate enterprise accounts.",
            "Proficient in Microsoft Excel data analysis, workflow automation, and structured process reporting."
        ],
        "fit_pitch": "HCLTech's commitment to flawless delivery aligns with my proven operational leadership and process optimization track record. I look forward to supporting global enterprise delivery operations."
    },
    {
        "id": 32,
        "company": "Larsen & Toubro (L&T)",
        "role": "Supply Chain & Procurement Coordinator (Heavy Engineering)",
        "track": "Industrial SCM",
        "location": "L&T Campus, Bellary Road / Hebbal, Bengaluru",
        "hiring_mgr": "L&T Corporate HR & Supply Chain Talent",
        "company_hook": "L&T's nation-building engineering prowess executing mega infrastructure and defense projects",
        "proof_points": [
            "Deep grounding in EXIM regulations, customs bonded warehousing, Letters of Credit (UCP 600), and Incoterms 2020.",
            "Achieved 15% cost optimization through direct primary supplier negotiations and contract restructuring.",
            "Directed on-ground operations at AERO India 2025 under stringent defense facility security protocols."
        ],
        "fit_pitch": "Having managed operations at AERO India 2025 and mastered international trade compliance, I am fully equipped to handle L&T's high-stakes industrial procurement, vendor governance, and logistics workflows."
    },
    {
        "id": 33,
        "company": "Kuehne + Nagel India",
        "role": "EXIM Customs Compliance & Sea Freight Coordinator",
        "track": "EXIM & Global Logistics",
        "location": "Prestige Polygon / MG Road / Airport Logistics Hub, Bengaluru",
        "hiring_mgr": "Kuehne + Nagel HR & Logistics Talent",
        "company_hook": "Kuehne + Nagel's status as the global #1 seafreight forwarding powerhouse",
        "proof_points": [
            "BBA in International Business with comprehensive knowledge of Ocean Bills of Lading, HS Codes, and customs valuation.",
            "Mastery of UCP 600 Letter of Credit compliance and cross-border commercial invoicing.",
            "Proven track record of managing multi-vendor logistics pipelines and negotiating carrier rates."
        ],
        "fit_pitch": "Seafreight logistics demands zero-defect documentation and relentless carrier coordination. With my specialized international trade degree and practical vendor negotiation skills, I am prepared to streamline Kuehne + Nagel's forwarding and customs operations."
    },
    {
        "id": 34,
        "company": "DB Schenker India",
        "role": "Global Freight Forwarding & EXIM Operations Specialist",
        "track": "EXIM & Global Logistics",
        "location": "Outer Ring Road / Airport Cargo Complex, Bengaluru",
        "hiring_mgr": "DB Schenker Talent Acquisition India",
        "company_hook": "DB Schenker's world-leading integrated logistics network connecting global manufacturing hubs",
        "proof_points": [
            "Complete fluency in Incoterms 2020, customs clearance, freight documentation, and bonded transit procedures.",
            "Delivered verified 15% cost savings through primary vendor rate rationalization.",
            "Coordinated on-ground logistics for 300+ complex deployments with zero delivery delays."
        ],
        "fit_pitch": "My International Business education and practical logistics execution experience give me the precise foundation required to optimize DB Schenker's air and ocean freight forwarding operations."
    },
    {
        "id": 35,
        "company": "FedEx Express India",
        "role": "International Trade & Air Cargo Operations Coordinator",
        "track": "EXIM & Global Logistics",
        "location": "Kempegowda International Airport Hub / Bengaluru",
        "hiring_mgr": "FedEx Express Early Careers Talent Team",
        "company_hook": "FedEx's time-definite global express network connecting 220+ countries and territories",
        "proof_points": [
            "Trained in air cargo documentation, IATA compliance basics, airway bills, and customs clearance protocols.",
            "Experienced in high-velocity operations with tight cut-off times, managing 300+ live event setups.",
            "Maintained 99%+ accuracy in structured data workflows under strict audit conditions at Instawork AI."
        ],
        "fit_pitch": "FedEx's express operations require extreme precision and strict customs compliance. My strong grounding in EXIM regulations combined with my ability to execute under time pressure makes me an immediate contributor to FedEx express operations."
    },
    {
        "id": 36,
        "company": "Bosch India (Robert Bosch)",
        "role": "Supply Chain Operations & Logistics Analyst",
        "track": "Industrial Operations",
        "location": "Bosch Spark.NXT Campus, Adugodi, Bengaluru",
        "hiring_mgr": "Bosch India Talent Acquisition & Campus Relations",
        "company_hook": "Bosch's cutting-edge smart mobility and industrial technology manufacturing ecosystem",
        "proof_points": [
            "Engineered procurement workflows reducing operating costs by 15% through supplier consolidation.",
            "Mastery of supply chain KPI tracking, inventory buffer management, and Incoterms 2020 compliance.",
            "Led on-ground teams of 20+ members across multi-stakeholder operational projects."
        ],
        "fit_pitch": "Bosch's manufacturing excellence demands analytical rigor and lean supply chain governance. My international business training, vendor management track record, and cost reduction experience position me to add immediate value to Bosch's logistics operations."
    },
    {
        "id": 37,
        "company": "Siemens India",
        "role": "Industrial SCM & Procurement Operations Analyst",
        "track": "Industrial Operations",
        "location": "Siemens Technology Campus, Electronic City, Bengaluru",
        "hiring_mgr": "Siemens HR Talent Acquisition",
        "company_hook": "Siemens' pioneering technology in smart infrastructure, digital enterprise, and industrial electrification",
        "proof_points": [
            "Extensive coursework in global procurement, EXIM procedures, and vendor risk assessment.",
            "Achieved 15% cost optimization by eliminating intermediary vendor margins in event logistics.",
            "Recognized for outstanding client communication and project tracking with formal leadership commendation."
        ],
        "fit_pitch": "Siemens' commitment to digitized and efficient supply chain networks matches my operational problem-solving capabilities. I am eager to apply my procurement and data analysis skills to Siemens' industrial operations."
    },
    {
        "id": 38,
        "company": "Apple India",
        "role": "Operations & Channel Partner Management Associate",
        "track": "Retail & Channel Operations",
        "location": "Minsk Square / UB City, Bengaluru",
        "hiring_mgr": "Apple India Talent Acquisition",
        "company_hook": "Apple's extraordinary brand standards and rapidly expanding retail and manufacturing footprint in India",
        "proof_points": [
            "Led end-to-end brand activation and VIP operations for premier brands including Puma India and AERO India 2025.",
            "Achieved 15% operational cost reduction while upholding uncompromising visual and execution standards.",
            "Managed 15+ concurrent B2B partner accounts with written commendation for flawless stakeholder engagement."
        ],
        "fit_pitch": "Apple represents the gold standard in brand excellence and operational perfection. Having executed 300+ events with zero tolerance for defects, I am ready to uphold Apple's exacting standards across channel operations and retail partner management."
    },
    {
        "id": 39,
        "company": "Salesforce India",
        "role": "B2B Business Development Representative (Commercial Sales)",
        "track": "B2B Business Development",
        "location": "RMZ Infinity / Outer Ring Road, Bengaluru",
        "hiring_mgr": "Salesforce Early Career & BDR Talent Team",
        "company_hook": "Salesforce's #1 CRM platform and revolutionary Agentforce AI driving enterprise customer success",
        "proof_points": [
            "Generated INR 1.5L+ in closed B2B sales revenue during internship at Pencil Mark, with written management commendation.",
            "Managed 15+ concurrent client pipelines, mastering outbound discovery, objection handling, and executive pitching.",
            "Certified in Google Digital Marketing and Generative AI, utilizing tech-enabled workflows for high-conversion prospecting."
        ],
        "fit_pitch": "Salesforce BDRs must be tenacious, consultative, and data-driven. Having closed revenue and managed executive B2B pipelines, I bring the energy, pipeline discipline, and communication skills to exceed quota at Salesforce."
    },
    {
        "id": 40,
        "company": "Morgan Stanley India",
        "role": "Global Operations Analyst (Institutional Securities)",
        "track": "Financial Operations",
        "location": "Outer Ring Road / Bengaluru Hub",
        "hiring_mgr": "Morgan Stanley Campus Recruiting",
        "company_hook": "Morgan Stanley's premier global investment bank and institutional securities trade processing architecture",
        "proof_points": [
            "Maintained 99%+ accuracy score in data operations at Instawork AI, operating under strict SLA and audit requirements.",
            "Strong academic grounding in International Trade Finance, corporate accounting, and quantitative modeling.",
            "Managed financial reconciliation and project budgets for 300+ deployments with zero audit discrepancies."
        ],
        "fit_pitch": "Institutional operations require uncompromising attention to detail, risk management, and process discipline. My proven track record of handling high-stakes budgets and zero-defect data operations ensures I will thrive in Morgan Stanley's global operations team."
    },
    {
        "id": 41,
        "company": "Accenture India",
        "role": "Management Consulting & Global Operations Analyst",
        "track": "Operations Consulting",
        "location": "IBC Knowledge Park, Bannerghatta Road / Manyata, Bengaluru",
        "hiring_mgr": "Accenture Early Careers Recruitment Team",
        "company_hook": "Accenture's unmatched global leadership in digital transformation, operations reinvention, and business consulting",
        "proof_points": [
            "BBA in International Business from DSU with comprehensive training in operational strategy and cross-border commerce.",
            "Delivered 15% recurring cost savings through strategic vendor consolidation and procurement restructuring.",
            "Managed multi-stakeholder operations for enterprise clients including Tata Communications and Puma India."
        ],
        "fit_pitch": "Accenture's focus on total enterprise reinvention requires analysts who can analyze complex workflows and drive tangible cost and productivity gains. I offer the problem-solving mindset and execution stamina to add immediate value to Accenture client engagements."
    },
    {
        "id": 42,
        "company": "Adobe Systems India",
        "role": "AI Operations & Digital Experience Analyst",
        "track": "AI Data Operations",
        "location": "Prestige Platina Tech Park, Marathahalli-Sarjapur ORR, Bengaluru",
        "hiring_mgr": "Adobe Talent Acquisition India",
        "company_hook": "Adobe's industry-standard creative and digital marketing cloud powered by Adobe Firefly and Sensei AI",
        "proof_points": [
            "Delivered 99%+ accuracy in AI data structuring and taxonomy validation workflows at Instawork AI.",
            "Certified in Google Digital Marketing & Generative AI, combining creative marketing insight with data operations.",
            "Coordinated high-profile multimedia brand activations for major enterprise accounts."
        ],
        "fit_pitch": "Adobe's leadership in creative AI requires operational rigor in data curation and customer experience analytics. My dual background in AI data operations and experiential marketing allows me to bridge technical data workflows with digital user experience."
    },
    {
        "id": 43,
        "company": "Intuit India",
        "role": "Business Operations & Data Analyst",
        "track": "Operations & Data",
        "location": "EcoSpace, Outer Ring Road, Bengaluru",
        "hiring_mgr": "Intuit India University Recruiting Team",
        "company_hook": "Intuit's mission to power prosperity around the world through TurboTax, QuickBooks, and Credit Karma",
        "proof_points": [
            "Maintained 99%+ accuracy in AI data structuring at Instawork AI, ensuring flawless audit compliance.",
            "Restructured family business financial and operational workflows, cutting recurring overhead by 15%.",
            "Advanced analytical toolkit in MS Excel (Data Modeling, Pivot Tables) and Power BI for tracking business health metrics."
        ],
        "fit_pitch": "Intuit values customer obsession, data-driven decision making, and operational simplicity. My background in business data analysis, cost optimization, and meticulous data governance matches Intuit's operational philosophy."
    },
    {
        "id": 44,
        "company": "Meesho",
        "role": "Category Operations & Supplier Growth Associate",
        "track": "E-Commerce Operations",
        "location": "060, Outer Ring Road, Mahadevapura, Bengaluru",
        "hiring_mgr": "Meesho Talent Acquisition Team",
        "company_hook": "Meesho's democratization of internet commerce for Bharat, empowering millions of small business suppliers",
        "proof_points": [
            "Generated INR 1.5L+ B2B revenue and onboarded corporate clients with formal commendation at Pencil Mark.",
            "Achieved 15% cost optimization by negotiating directly with primary manufacturers and suppliers.",
            "Managed 300+ operational deployments with hands-on logistics and vendor problem-solving."
        ],
        "fit_pitch": "Meesho's mission to empower MSME suppliers requires passionate category operators who understand ground realities and supplier unit economics. Having personally driven B2B sales and negotiated supplier margins, I am ready to accelerate supplier onboarding and category growth."
    },
    {
        "id": 45,
        "company": "Delhivery",
        "role": "Express Logistics & Network Operations Coordinator",
        "track": "Operations & SCM",
        "location": "Bengaluru Mega Gateway Hub / Bommasandra",
        "hiring_mgr": "Delhivery Early Careers Recruitment",
        "company_hook": "Delhivery's integrated express logistics network moving over 2 billion parcels across India",
        "proof_points": [
            "Comprehensive training in supply chain network design, freight forwarding, and logistics bottleneck analysis.",
            "Delivered 15% cost optimization through vendor contract restructuring and logistics route consolidation.",
            "Led on-ground teams of 20+ personnel across 300+ live deployments under strict SLA timelines."
        ],
        "fit_pitch": "Delhivery's nationwide automated mesh network requires operations leaders with grit, technical acumen, and on-ground execution capabilities. My experience managing high-pressure logistics and optimizing vendor costs prepares me to drive network efficiency at Delhivery."
    },
    {
        "id": 46,
        "company": "Urban Company",
        "role": "Service Operations & Category Partner Manager",
        "track": "Service Operations",
        "location": "Bengaluru Hub / HSR Layout",
        "hiring_mgr": "Urban Company Talent Acquisition",
        "company_hook": "Urban Company's technology-driven home services marketplace empowering tens of thousands of service professionals",
        "proof_points": [
            "Managed 300+ live service deployments, overseeing partner quality, scheduling, and on-ground crisis resolution.",
            "Earned formal commendation for B2B client relationship management, handling 15+ concurrent accounts.",
            "Certified in Service Marketing (NPTEL, IIT Kharagpur) with deep grounding in service quality frameworks (SERVQUAL)."
        ],
        "fit_pitch": "Urban Company relies on standardized service delivery and partner enablement. With formal academic certification in Service Marketing from IIT Kharagpur and hands-on experience leading 300+ on-ground service activations, I am equipped to elevate partner quality and category NPS."
    },
    {
        "id": 47,
        "company": "Ather Energy",
        "role": "EV Supply Chain & Distribution Operations Associate",
        "track": "Automotive SCM",
        "location": "IBC Knowledge Park, Bannerghatta Road, Bengaluru",
        "hiring_mgr": "Ather Energy Talent Acquisition Team",
        "company_hook": "Ather Energy's pioneering intelligent electric scooters built and engineered in India",
        "proof_points": [
            "Mastery of International Trade, component EXIM regulations, customs tariffs, and Incoterms 2020.",
            "Achieved 15% cost optimization through direct primary vendor negotiations and procurement consolidation.",
            "Led 7-day aerospace exhibition operations at AERO India 2025 under strict security and visitor SLAs."
        ],
        "fit_pitch": "Ather's rapid retail expansion and EV production scale demand agile, data-backed supply chain operations. My international trade background, vendor management experience, and hands-on operational leadership make me an immediate asset to Ather's distribution network."
    },
    {
        "id": 48,
        "company": "InMobi / Glance",
        "role": "B2B Growth & Strategic Partnerships Associate",
        "track": "B2B Business Development",
        "location": "Embassy GolfLinks Business Park, Bengaluru",
        "hiring_mgr": "InMobi Group Talent Acquisition",
        "company_hook": "InMobi Group's global advertising cloud and Glance's revolutionary smart lock screen content platform",
        "proof_points": [
            "Generated INR 1.5L+ in direct B2B sales revenue with written leadership commendation for client conversion.",
            "Certified in Google Digital Marketing with expertise in adtech metrics, digital funnels, and publisher monetization.",
            "Managed 15+ concurrent enterprise client accounts with structured pipeline tracking."
        ],
        "fit_pitch": "InMobi's global adtech platform requires consultative, metrics-driven BD professionals. With certified digital marketing expertise and a proven record of closing B2B revenue and managing corporate partnerships, I am ready to drive publisher and brand monetization at InMobi."
    },
    {
        "id": 49,
        "company": "Titan Company Limited (Tata Group)",
        "role": "Brand Activation & Retail Operations Specialist",
        "track": "Event & Brand Activation",
        "location": "Titan Corporate Office, Electronic City, Bengaluru",
        "hiring_mgr": "Titan Company Early Careers Recruitment",
        "company_hook": "Titan's legendary consumer trust across Watches, Tanishq Jewellery, and Fastrack lifestyle retail",
        "proof_points": [
            "Orchestrated 300+ live brand activations and corporate deployments (Puma India, Tata Communications, TRILOGY Concert).",
            "Directed 7-day stall operations at AERO India 2025 for 100,000+ visitors with zero SLA breaches.",
            "Certified in IIT Kharagpur Service Marketing and Google Digital Marketing with 15% verified cost savings track record."
        ],
        "fit_pitch": "Titan's retail dominance relies on flawless consumer touchpoints and elevated brand activations. Having led 300+ live events and represented premier lifestyle brands, I am prepared to deliver exceptional retail activations and operational excellence across Titan's flagship brands."
    },
    {
        "id": 50,
        "company": "Airbus India",
        "role": "Aerospace Supply Chain & Trade Logistics Coordinator",
        "track": "Aerospace & SCM",
        "location": "Airbus India Campus, Mahadevapura / Whitefield, Bengaluru",
        "hiring_mgr": "Airbus Early Careers & Supply Chain Talent Acquisition",
        "company_hook": "Airbus's pioneering aerospace leadership and expanding industrial procurement footprint in India",
        "proof_points": [
            "Managed on-ground exhibition and VIP logistics at AERO India 2025 at Yelahanka Air Force Station.",
            "Specialized academic mastery in International Trade, Incoterms 2020, customs valuation, and cross-border aerospace logistics.",
            "Achieved 15% cost optimization through direct supplier restructuring and primary contract negotiations."
        ],
        "fit_pitch": "Having operated directly inside AERO India 2025 coupled with my specialized BBA in International Business and trade compliance training, I offer the ideal blend of aerospace context, vendor governance, and customs documentation rigor for Airbus's India supply chain."
    }
]

def generate_cover_letter_text(data):
    """Generates the full text of a tailored cover letter."""
    lines = []
    lines.append(f"ADITYA MEHRA")
    lines.append(f"Bengaluru, Karnataka, India | Phone: {CANDIDATE_PHONE} | Email: {CANDIDATE_EMAIL}")
    lines.append(f"LinkedIn: {CANDIDATE_LINKEDIN}")
    lines.append("-" * 75)
    lines.append(f"Date: August 26, 2026")
    lines.append("")
    lines.append(f"To,")
    lines.append(f"{data['hiring_mgr']}")
    lines.append(f"{data['company']}")
    lines.append(f"{data['location']}")
    lines.append("")
    lines.append(f"Subject: Application for {data['role']} - Aditya Mehra")
    lines.append("")
    lines.append(f"Dear {data['hiring_mgr']},")
    lines.append("")
    lines.append(f"I am writing to express my strong interest in the {data['role']} position at {data['company']}. Currently completing my {CANDIDATE_EDU}, I bring a proven track record across operational execution, international business strategy, and data-driven process optimization. I am particularly drawn to {data['company']} because of {data['company_hook']}.")
    lines.append("")
    lines.append(f"Throughout my academic and professional journey, I have built verified capabilities directly relevant to this role:")
    lines.append("")
    for pt in data['proof_points']:
        lines.append(f"• {pt}")
    lines.append("")
    lines.append(f"{data['fit_pitch']}")
    lines.append("")
    lines.append(f"What distinguishes my profile is my hands-on accountability: whether leading on-ground logistics for 100,000+ visitors at AERO India 2025, maintaining 99%+ data accuracy for AI datasets at Instawork AI, closing INR 1.5L+ B2B revenue at Pencil Mark, or securing 15% operational cost reductions through direct vendor negotiations, I treat every operational problem as my personal responsibility to resolve.")
    lines.append("")
    lines.append(f"I welcome the opportunity to discuss how my international business training, operational rigor, and bias for action can support {data['company']}'s strategic goals in Bengaluru. Thank you for your time and consideration.")
    lines.append("")
    lines.append(f"Sincerely,")
    lines.append("")
    lines.append(f"Aditya Mehra")
    lines.append(f"BBA International Business | Class of 2026")
    lines.append(f"Dayananda Sagar University, Bengaluru")
    lines.append(f"Phone: {CANDIDATE_PHONE} | Email: {CANDIDATE_EMAIL}")
    lines.append(f"LinkedIn: {CANDIDATE_LINKEDIN}")
    return "\n".join(lines)

def generate_cover_letter_markdown(data):
    """Generates markdown formatted representation of a tailored cover letter."""
    md = []
    md.append(f"## {data['id']}. {data['company']} — {data['role']}")
    md.append(f"**Track:** `{data['track']}` | **Location:** `{data['location']}` | **Target Team:** `{data['hiring_mgr']}`")
    md.append("")
    md.append("```text")
    md.append(generate_cover_letter_text(data))
    md.append("```")
    md.append("")
    md.append("---")
    return "\n".join(md)

def main():
    output_dir = "e:/anti/cover_letters"
    os.makedirs(output_dir, exist_ok=True)
    
    master_md_path = "e:/anti/Cover_Letters_Master_Collection.md"
    
    print(f"[START] Generating 50 Tailored Cover Letters...")
    
    master_md_lines = [
        "# ADITYA MEHRA — MASTER COLLECTION OF 50 TAILORED COVER LETTERS",
        f"**Candidate:** {CANDIDATE_NAME} | **Contact:** {CANDIDATE_PHONE} | {CANDIDATE_EMAIL} | [LinkedIn Profile]({CANDIDATE_LINKEDIN})",
        f"**Education:** {CANDIDATE_EDU}",
        f"**Total Letters Generated:** {len(COMPANIES_DATA)} Dedicated MNC & Enterprise Applications",
        f"**Date:** August 26, 2026",
        "",
        "---",
        "",
        "## EXECUTIVE SUMMARY & ROLE DISTRIBUTION",
        "",
        "This collection contains 50 tailored cover letters engineered for tier-1 multinational corporations, consulting giants, GCCs, tech unicorns, and logistics leaders in Bengaluru. Each cover letter is customized with company-specific hooks, exact role alignment, verified proof points (300+ event deployments, 15% cost savings, INR 1.5L+ B2B revenue, 99%+ AI data ops accuracy, and EXIM compliance), and a direct call to action.",
        "",
        "| ID | Target Company | Target Role | Domain Track | Location Hub |",
        "| :---: | :--- | :--- | :--- | :--- |"
    ]
    
    for item in COMPANIES_DATA:
        master_md_lines.append(f"| {item['id']} | **{item['company']}** | [{item['role']}](#{item['id']}-{item['company'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('&', '').replace('/', '').replace('.', '')}-{item['role'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('&', '').replace('/', '').replace('.', '')}) | `{item['track']}` | {item['location'].split(',')[0]} |")
        
        # Generate individual text file
        slug = item['company'].replace(' ', '_').replace('/', '_').replace('&', 'and').replace('.', '').replace('(', '').replace(')', '')
        role_slug = item['role'].split('(')[0].strip().replace(' ', '_').replace('/', '_')
        filename = f"{item['id']:02d}_{slug}_{role_slug}.txt"
        file_path = os.path.join(output_dir, filename)
        
        letter_text = generate_cover_letter_text(item)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(letter_text)
            
    master_md_lines.append("")
    master_md_lines.append("---")
    master_md_lines.append("")
    master_md_lines.append("## COMPLETE COVER LETTERS (FULL TEXT)")
    master_md_lines.append("")
    
    for item in COMPANIES_DATA:
        master_md_lines.append(generate_cover_letter_markdown(item))
        
    with open(master_md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(master_md_lines))
        
    print(f"[SUCCESS] 50 Individual Cover Letters written to: {output_dir}")
    print(f"[SUCCESS] Master Collection written to: {master_md_path}")
    print(f"[METRIC] Total Cover Letters: {len(COMPANIES_DATA)}")

if __name__ == '__main__':
    main()
