"""
build_apex_docx_suite.py - Automated ATS-Compliant DOCX Generator
==================================================================
Generates 5 tailored, single-column, ATS-optimized Word documents (.docx)
for Aditya Mehra across all 5 specialized career tracks.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_ats_resume_docx(filename: str, target_role: str, summary_text: str, core_competencies: list, experience_items: list, education_items: list, cert_items: list):
    doc = Document()

    # 0.5 in margins for maximum ATS 1-page efficiency
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    def add_section_header(title: str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.name = "Arial"
        run.font.color.rgb = RGBColor(17, 24, 39) # Dark Slate Gray

        # Add bottom border under heading for clean professional separation
        pBrd = OxmlElement('w:pBrd')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '9CA3AF') # Subtle Gray
        pBrd.append(bottom)
        p._p.get_or_add_pPr().append(pBrd)
        return p

    def add_bullet(bold_prefix: str, text: str):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.05
        run1 = p.add_run(bold_prefix + ": ")
        run1.bold = True
        run1.font.size = Pt(9.5)
        run1.font.name = "Arial"
        run1.font.color.rgb = RGBColor(31, 41, 55)
        run2 = p.add_run(text)
        run2.font.size = Pt(9.5)
        run2.font.name = "Arial"
        run2.font.color.rgb = RGBColor(55, 65, 81)

    # Header
    name_p = doc.add_paragraph()
    name_p.paragraph_format.space_before = Pt(0)
    name_p.paragraph_format.space_after = Pt(1)
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = name_p.add_run("ADITYA MEHRA")
    r_name.bold = True
    r_name.font.size = Pt(16)
    r_name.font.name = "Arial"
    r_name.font.color.rgb = RGBColor(17, 24, 39)

    contact_p = doc.add_paragraph()
    contact_p.paragraph_format.space_before = Pt(0)
    contact_p.paragraph_format.space_after = Pt(4)
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_contact = contact_p.add_run(
        "Bengaluru, Karnataka, India | +91 70034 56624 | adityamehra799@gmail.com\n"
        "LinkedIn: linkedin.com/in/aditya-mehra-b8644b326 | Portfolio: adi-digital-universe.ai.studio | GitHub: github.com/AdityaMehra007"
    )
    r_contact.font.size = Pt(9)
    r_contact.font.name = "Arial"
    r_contact.font.color.rgb = RGBColor(75, 85, 99)

    # Professional Summary
    add_section_header(f"Professional Summary — {target_role}")
    sum_p = doc.add_paragraph()
    sum_p.paragraph_format.space_before = Pt(2)
    sum_p.paragraph_format.space_after = Pt(4)
    sum_p.paragraph_format.line_spacing = 1.05
    r_sum = sum_p.add_run(summary_text)
    r_sum.font.size = Pt(9.5)
    r_sum.font.name = "Arial"
    r_sum.font.color.rgb = RGBColor(31, 41, 55)

    # Core Competencies
    add_section_header("Core Competencies & Technical Skills")
    for comp_category, comp_desc in core_competencies:
        add_bullet(comp_category, comp_desc)

    # Professional Experience
    add_section_header("Professional Experience & Proof of Work")
    for exp in experience_items:
        exp_p = doc.add_paragraph()
        exp_p.paragraph_format.space_before = Pt(5)
        exp_p.paragraph_format.space_after = Pt(1)
        exp_p.paragraph_format.keep_with_next = True
        
        # Org and location
        r_org = exp_p.add_run(exp["org"].upper() + " | " + exp["location"])
        r_org.bold = True
        r_org.font.size = Pt(9.5)
        r_org.font.name = "Arial"
        r_org.font.color.rgb = RGBColor(17, 24, 39)
        
        # Title and dates
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(2)
        title_p.paragraph_format.keep_with_next = True
        r_title = title_p.add_run(exp["title"])
        r_title.bold = True
        r_title.italic = True
        r_title.font.size = Pt(9)
        r_title.font.name = "Arial"
        r_title.font.color.rgb = RGBColor(75, 85, 99)
        
        r_period = title_p.add_run("  (" + exp["period"] + ")")
        r_period.font.size = Pt(9)
        r_period.font.name = "Arial"
        r_period.font.color.rgb = RGBColor(107, 114, 128)

        for bullet_prefix, bullet_body in exp["bullets"]:
            add_bullet(bullet_prefix, bullet_body)

    # Education
    add_section_header("Education & Academic Credentials")
    for edu in education_items:
        edu_p = doc.add_paragraph()
        edu_p.paragraph_format.space_before = Pt(3)
        edu_p.paragraph_format.space_after = Pt(1)
        r_deg = edu_p.add_run(edu["degree"] + " — " + edu["institution"])
        r_deg.bold = True
        r_deg.font.size = Pt(9.5)
        r_deg.font.name = "Arial"
        r_deg.font.color.rgb = RGBColor(17, 24, 39)

        r_yr = edu_p.add_run(f" ({edu['period']}) — {edu['status']}")
        r_yr.italic = True
        r_yr.font.size = Pt(9)
        r_yr.font.name = "Arial"
        r_yr.font.color.rgb = RGBColor(75, 85, 99)

        if "bullets" in edu:
            for b_pref, b_text in edu["bullets"]:
                add_bullet(b_pref, b_text)

    # Certifications & Honors
    add_section_header("Certifications, Commendations & Accreditations")
    for cert_title, cert_issuer in cert_items:
        add_bullet(cert_title, cert_issuer)

    filepath = os.path.join(OUTPUT_DIR, filename)
    doc.save(filepath)
    print(f"[SUCCESS] Generated: {filepath}")
    return filepath


def generate_all_tracks():
    # Common shared items
    dsu_edu = {
        "degree": "Bachelor of Business Administration (BBA) - International Business",
        "institution": "Dayananda Sagar University (DSU), Bengaluru",
        "period": "2023 - 2026",
        "status": "Degree Completed (Immediate Joiner, 0 Days Notice)",
        "bullets": [
            ("Key Coursework", "Global Supply Chain Architecture, Incoterms 2020, Multilateral Trade Law, Working Capital Finance, Business Analytics."),
            ("Applied Academic Modeling", "Landed cost calculation models, international freight route optimization simulations, and cross-border supplier intelligence.")
        ]
    }

    certs_common = [
        ("Written Management Commendation", "Awarded for exceptional commercial pipeline conversion & negotiation rigor — Pencil Mark Interior Solutions (2025)"),
        ("Services Marketing: A Practical Approach", "Certified by NPTEL & IIT Kharagpur (2025)"),
        ("Digital Marketing Professional Certificate", "Certified by Google (2024)"),
        ("Generative AI & Agentic Prompt Engineering", "Certified by Outskill (2025)"),
        ("AI Productivity & Automation Tools", "Certified by be10x (2026)")
    ]

    # TRACK 1: GLOBAL MNC OPERATIONS
    create_ats_resume_docx(
        filename="Aditya_Mehra_Global_MNC_Operations.docx",
        target_role="Business Operations & Process Analyst",
        summary_text="Analytical and execution-focused Business Operations & Process Specialist holding a BBA in International Business from Dayananda Sagar University (2026). Combines an 8-year foundation of commercial and inventory accountability with 300+ executed operations deployments. Proven track record in achieving 15%–20% procurement cost reductions via direct vendor rate card restructuring, governing high-security operations at AERO INDIA 2025 (100k+ attendees, 0% asset shrinkage), and auditing high-density AI data pipelines at 99%+ accuracy (Instawork AI). Recipient of a formal Written Management Commendation for commercial execution. Immediate joiner.",
        core_competencies=[
            ("Operations & Governance", "Vendor SLA Contracting, Rate Card Modeling, 15–20% Procurement Cost Optimization, Cross-Functional Scheduling, Run-of-Show Logistics, Crisis De-escalation."),
            ("Analytical Systems & Tools", "Advanced MS Excel (XLOOKUP, Dynamic Pivots, Power Query, Financial Models), Python Automation, SQLite Databases, Power BI & Tableau Dashboards, CRM (Salesforce, Zoho, HubSpot)."),
            ("Process & Risk Control", "Root-Cause Defect Resolution, Milestone SLA Compliance, SOP Documentation, High-Security Access Protocols, Quality Assurance Benchmarking."),
            ("Languages", "English (Fluent/Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient).")
        ],
        experience_items=[
            {
                "org": "Independent Commercial Operations & Event Practice",
                "location": "Bengaluru, India",
                "title": "Operations Lead",
                "period": "2019 – Present",
                "bullets": [
                    ("Production Leadership", "Commanded end-to-end operational workflows for 300+ live commercial deployments and corporate forums for major brands including Puma India, HP, Intel, Tata Communications, and Razorpay."),
                    ("Cost Optimization", "Reduced project procurement expenditures by 15% to 20% by eliminating intermediary broker markups and directly renegotiating SLA rate cards with tier-1 staging, fabrication, and audio suppliers."),
                    ("Quality & Retention", "Maintained a 30%+ organic repeat client rate by instituting transparent milestone budgets, strict post-event reconciliations, and zero-defect operational governance."),
                    ("Crowd & Safety Governance", "Governed on-ground safety, security protocols, and 25+ technical crew members under high-pressure live environments with zero unresolved incident escalations.")
                ]
            },
            {
                "org": "Instawork Services India Pvt. Ltd.",
                "location": "Bengaluru, India",
                "title": "AI Data Operations Intern",
                "period": "Dec 2025",
                "bullets": [
                    ("Data Pipeline Auditing", "Audited and curated high-density multimodal dataset pipelines powering warehouse robotics and autonomous computer vision models."),
                    ("Quality Benchmark", "Maintained a strict 99%+ quality assurance rating across 10,000+ data records through structured bounding-box validations and edge-case classification protocols."),
                    ("Taxonomy Standardization", "Standardized edge-case logging taxonomies, cutting annotation latency and preventing model classification drift.")
                ]
            },
            {
                "org": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "title": "Business Development & Commercial Operations Intern",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    ("Client Account Governance", "Managed 15+ concurrent corporate client accounts, developing commercial briefs, cost estimates, and interior fit-out proposals."),
                    ("Revenue & Conversion Lift", "Drove an 18% conversion lift from inquiry to closed contract, directly generating ₹1.5L+ in commercial revenue within an 8-week cycle."),
                    ("Executive Recognition", "Awarded a formal Written Management Commendation from executive leadership for proactive client negotiation and operational rigor.")
                ]
            },
            {
                "org": "AERO INDIA 2025 (Salt in My Coca)",
                "location": "Yelahanka Air Force Station, Bengaluru",
                "title": "Exhibition Operations Lead",
                "period": "Feb 2025",
                "bullets": [
                    ("High-Security Governance", "Managed 7-day high-throughput commercial pavilion logistics at Asia's premier aerospace expo (700+ exhibitors, 100,000+ total visitors)."),
                    ("Zero Asset Loss", "Enforced strict Ministry of Defence security clearances, access schedules, and physical inventory controls with 0% asset loss or stock shrinkage."),
                    ("Executive Engagement", "Interfaced with 5,000+ high-profile international enterprise delegates and defense officials with executive composure.")
                ]
            }
        ],
        education_items=[dsu_edu],
        cert_items=certs_common
    )

    # TRACK 2: AI & TECH OPERATIONS
    create_ats_resume_docx(
        filename="Aditya_Mehra_AI_Tech_Operations.docx",
        target_role="AI & Tech Operations Specialist",
        summary_text="High-velocity AI & Tech Operations Specialist with proven experience in machine learning dataset quality auditing, automated workflow engineering, and rapid on-ground deployment. Demonstrated track record at Instawork AI sustaining a 99%+ QA benchmark across 10,000+ multimodal robotics data points. Experienced in building Python/SQLite automation scripts, LLM agent workflows, and managing high-throughput physical operations across 300+ deployments. Graduating with a BBA in International Business from Dayananda Sagar University (2026). Immediate joiner eager to drive operational scalability in rapid-growth tech ecosystems.",
        core_competencies=[
            ("Tech & AI Operations", "Multimodal Data Quality Assurance, Robotics Annotation Auditing, Edge-Case Taxonomy Design, LLM Agent Workflow Automation, Prompt Engineering (Gemini, Claude, GPT)."),
            ("Systems & Scripting", "Python Scripting, SQLite Databases, GitHub Version Control, Advanced MS Excel / Google Sheets (Formulas, Pivot Tables, XLOOKUP), REST API Integrations."),
            ("Execution & Scalability", "Rapid Field Deployment, Cross-Functional Coordination, Vendor SLA Governance, Zero-Defect Incident Triage, Process Optimization."),
            ("Languages", "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient).")
        ],
        experience_items=[
            {
                "org": "Instawork Services India Pvt. Ltd.",
                "location": "Bengaluru, India",
                "title": "AI Data Operations & Quality Assurance Intern",
                "period": "Dec 2025",
                "bullets": [
                    ("Robotics Sensor QA", "Spearheaded quality verification protocols for large-scale multimodal sensor datasets utilized in training autonomous warehouse robotics models."),
                    ("Extreme Accuracy", "Audited 10,000+ data samples with a consistent 99%+ quality accuracy score, eliminating taxonomy boundary leaks."),
                    ("Process Standardization", "Authored structured QA guidelines that reduced annotation ambiguity, accelerating labeling turnaround time across distributed data teams."),
                    ("Engineering Collaboration", "Collaborated directly with machine learning engineering leads to resolve edge cases in object segmentation and activity recognition.")
                ]
            },
            {
                "org": "Independent Tech & Automation Projects",
                "location": "Bengaluru, India",
                "title": "Autonomous Operations & Dispatch Engine Developer",
                "period": "2025 – Present",
                "bullets": [
                    ("Platform Engineering", "Engineered an automated operational dispatch and candidate intelligence platform utilizing Python, SQLite, and AI agent frameworks (github.com/AdityaMehra007/anti)."),
                    ("Deterministic Testing", "Integrated automated calendar scheduling (.ics generator), contact validation pipelines, and data verification routines backed by 16/16 verified unit tests passing green."),
                    ("Operational Dashboards", "Built interactive single-page dashboards and operational status monitors to eliminate manual tracking overhead.")
                ]
            },
            {
                "org": "Independent Operations Practice",
                "location": "Bengaluru, India",
                "title": "On-Ground Operations Specialist",
                "period": "2019 – Present",
                "bullets": [
                    ("Field Operations", "Orchestrated on-ground production, technical setups, and vendor coordination across 300+ live commercial and tech brand events (Razorpay, Intel, HP, Puma)."),
                    ("Vendor Renegotiation", "Restructured supplier rate cards to drive 15% to 20% direct procurement cost reductions while maintaining 100% on-time milestone delivery."),
                    ("Crisis Containment", "Managed 25+ ground crew members during high-stress live rollouts, achieving zero SLA infractions or unresolved incidents.")
                ]
            },
            {
                "org": "AERO INDIA 2025 (Salt in My Coca)",
                "location": "Yelahanka Air Force Station, Bengaluru",
                "title": "Commercial Pavilion Operations Lead",
                "period": "Feb 2025",
                "bullets": [
                    ("High-Throughput Logistics", "Commanded a 7-day high-throughput commercial booth under strict military-level security clearances (100k+ total airshow attendees)."),
                    ("Zero Shrinkage", "Enforced real-time batch replenishment and cash reconciliation with 0% asset loss or inventory discrepancy across 5,000+ customer interactions.")
                ]
            }
        ],
        education_items=[dsu_edu],
        cert_items=certs_common
    )

    # TRACK 3: B2B COMMERCIAL & SALES
    create_ats_resume_docx(
        filename="Aditya_Mehra_B2B_Commercial_Sales.docx",
        target_role="B2B Commercial & Sales Specialist",
        summary_text="High-energy B2B Commercial & Sales Specialist with demonstrable success in lead prospecting, consultative proposal structuring, and revenue closing. Proven experience at Pencil Mark Interior Solutions driving ₹1.5L+ in closed contract revenue with an 18% pipeline conversion lift, recognized via a formal Written Management Commendation. Backed by 8+ years of commercial exposure dating back to family retail operations and 300+ executed client event activations. Possesses an international business background (BBA, DSU 2026), advanced CRM literacy, and rapid deal structuring capabilities. Immediate joiner.",
        core_competencies=[
            ("Commercial Sales & Pipeline", "B2B Account Prospecting, Consultative Selling, Commercial Proposal Structuring, Multi-Touch Follow-up Cadences, Contract Negotiations."),
            ("Client Relationship Management", "Enterprise Stakeholder Engagement, Account Expansion, 30%+ Client Retention Rate, Fast Quotation Turnaround."),
            ("Commercial Analytics & CRM", "Salesforce CRM, HubSpot, Zoho CRM, MS Excel Financial Modeling (P&L Reconciliations, Margin Structuring, Revenue Forecasting)."),
            ("Communication & Influence", "High-Stakes In-Person Pitching, Objections Handling, Executive Briefings, Fluent in English, Hindi, Punjabi, Bengali.")
        ],
        experience_items=[
            {
                "org": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "title": "Commercial Sales & Business Development Intern",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    ("Pipeline Management", "Managed an active pipeline of 15+ concurrent commercial interior fit-out prospects, executing stakeholder discovery calls and site requirement audits."),
                    ("Fast Proposal Turnaround", "Formulated structured, customized commercial proposals and bill-of-quantities (BOQ) estimates, reducing proposal turnaround time by 35%."),
                    ("Revenue Acceleration", "Boosted pipeline conversion velocity by 18%, closing ₹1.5L+ in enterprise contract revenue within an intensive 2-month engagement."),
                    ("Management Commendation", "Recognized with a formal Written Management Commendation from executive directors for exemplary commercial discipline and persistence.")
                ]
            },
            {
                "org": "Independent Commercial Operations & Events",
                "location": "Bengaluru, India",
                "title": "Commercial Practice Lead",
                "period": "2019 – Present",
                "bullets": [
                    ("Client Acquisition", "Acquired and serviced 300+ live commercial client engagements across corporate activations, product launches, and brand showcases."),
                    ("Compounding Retention", "Generated consistent 30%+ organic repeat business without paid marketing through high-touch client servicing and transparent accounting."),
                    ("Supplier Rate Negotiation", "Conducted aggressive supplier negotiations with audio, lighting, and fabrication vendors, securing 15%–20% margin improvements on project budgets."),
                    ("Corporate Brand Portfolio", "Pitched, contracted, and executed premium activations for brands including Puma, Intel, HP, Tata Communications, and Razorpay.")
                ]
            },
            {
                "org": "AERO INDIA 2025 (Salt in My Coca)",
                "location": "Yelahanka Air Force Station, Bengaluru",
                "title": "Commercial Lead — Exhibition Operations",
                "period": "Feb 2025",
                "bullets": [
                    ("High-Footfall Pitching", "Spearheaded frontline commercial engagement and sales at Asia's premier aerospace expo, directly interacting with 5,000+ delegates."),
                    ("Zero Defect Cash Flow", "Drove high-volume retail transactions via digital POS and UPI under intense footfall, reconciling daily gross revenue with zero discrepancy."),
                    ("B2B Lead Generation", "Secured qualified B2B distribution and gifting leads from corporate aviation delegates for subsequent follow-up.")
                ]
            },
            {
                "org": "Family Enterprise",
                "location": "Kolkata, India",
                "title": "Retail Sales & Inventory Associate",
                "period": "2018 – 2020",
                "bullets": [
                    ("Frontline Counter Sales", "Managed frontline customer counter sales, customer relationship development, and wholesale trade order fulfillment starting at age 17."),
                    ("Cash Reconciliation", "Oversaw daily cash register reconciliation, supplier billing verification, and working capital inventory turnover.")
                ]
            }
        ],
        education_items=[dsu_edu],
        cert_items=certs_common
    )

    # TRACK 4: EXIM & SUPPLY CHAIN
    create_ats_resume_docx(
        filename="Aditya_Mehra_EXIM_Supply_Chain.docx",
        target_role="International Trade, EXIM & Supply Chain Specialist",
        summary_text="Disciplined and mathematically rigorous International Business graduate (BBA, Dayananda Sagar University 2026) specializing in Global Supply Chain Architecture, Incoterms 2020, and Cross-Border Logistics. Demonstrates exceptional operational acumen verified by managing military-grade supply logistics at AERO INDIA 2025 (0% inventory shrinkage, 100k+ attendees), negotiating 15%–20% vendor cost reductions across 300+ live deployments, and 8+ years of business inventory accountability. Proficient in landed cost modeling, trade documentation, customs workflows, and supply chain analytics. Immediate joiner.",
        core_competencies=[
            ("Trade Rules & Documentation", "Incoterms 2020 (FOB, CIF, DDP, DAP, CFR), Bill of Lading (B/L), Commercial Invoices, Packing Lists, Certificates of Origin, Letters of Credit (UCP 600)."),
            ("Logistics & Clearance", "Freight Forwarder Governance, Customs Clearance Workflows, HS Tariff Classification, Demurrage & Detention Minimization, Port Operations."),
            ("Cost & Inventory Modeling", "Landed Cost Modeling, Working Capital Optimization, Buffer Stock Modeling, Supplier Rate Card Benchmarking, Zero-Shrinkage Audit."),
            ("Systems & Analytics", "Advanced MS Excel (Dynamic Pivot Tables, Power Query, What-If Analysis), Python Supply Chain Automation Scripts, ERP Basics.")
        ],
        experience_items=[
            {
                "org": "AERO INDIA 2025 (Salt in My Coca)",
                "location": "Yelahanka Air Force Station, Bengaluru",
                "title": "Exhibition Logistics & Supply Chain Lead",
                "period": "Feb 2025",
                "bullets": [
                    ("High-Security Cargo Logistics", "Directed end-to-end multi-echelon inventory supply operations for a high-volume exhibition pavilion inside a restricted Air Force station."),
                    ("Regulatory Protocol Compliance", "Coordinated secure daily cargo transit passes, timed vehicle entry windows, and Ministry of Defence compliance clearances with zero security violations."),
                    ("Buffer Stock Optimization", "Implemented a tight buffer-stock replenishment model that prevented stockouts during peak surges while maintaining 0% product loss across 7 days.")
                ]
            },
            {
                "org": "Independent Commercial Operations & Logistics",
                "location": "Bengaluru, India",
                "title": "Procurement & Logistics Lead",
                "period": "2019 – Present",
                "bullets": [
                    ("Supply Chain Governance", "Supervised multi-tier material logistics, warehousing staging, and equipment transport across 300+ time-critical projects."),
                    ("Freight & Asset Negotiation", "Lowered freight and staging equipment procurement expenses by 15% to 20% through direct negotiations with asset owners and vehicle fleet coordinators."),
                    ("Material Quality Control", "Instituted strict material inward/outward inspection protocols, eliminating transit damages and missing-item write-offs.")
                ]
            },
            {
                "org": "Family Enterprise",
                "location": "Kolkata, India",
                "title": "Wholesale Supply & Inventory Operations",
                "period": "2018 – 2020",
                "bullets": [
                    ("Wholesale Dispatch", "Oversaw daily inventory intake, vendor delivery reconciliations, and bulk order dispatch for regional distribution channels."),
                    ("Inventory Audit", "Maintained detailed manual and digital stock ledgers in MS Excel, resolving supplier shipment discrepancies and managing cash flow cycles.")
                ]
            },
            {
                "org": "Mehra's Kitchen",
                "location": "Bengaluru, India",
                "title": "Supply Chain & Operations Co-Founder",
                "period": "2025",
                "bullets": [
                    ("Cold Chain & Spoilage Control", "Managed perishable ingredient procurement, cold-chain holding schedules, and vendor payment credit cycles for a food business."),
                    ("Margin Protection", "Optimized daily batch quantities based on demand forecasts, keeping raw material spoilage below 2% and protecting operating gross margins.")
                ]
            }
        ],
        education_items=[dsu_edu],
        cert_items=certs_common
    )

    # TRACK 5: CHIEF OF STAFF / FOUNDER'S OFFICE
    create_ats_resume_docx(
        filename="Aditya_Mehra_Chief_of_Staff_Founders_Office.docx",
        target_role="Chief of Staff / Founder's Office Associate",
        summary_text="High-agency, execution-obsessed Generalist Operator seeking a Founder's Office or Chief of Staff Associate role. Combines 8+ years of hands-on commercial grit (family retail roots) with modern technological leverage (Python, AI agents, SQLite, GitHub) and 300+ completed field deployments. Proven ability to operate autonomously under extreme pressure—from orchestrating high-security operations at AERO INDIA 2025 and managing VIP logistics for Grammy-winning artists, to closing B2B commercial revenue (₹1.5L+, 18% lift) and auditing AI robotics datasets at 99%+ accuracy. Recipient of a formal Written Management Commendation for executive follow-through.",
        core_competencies=[
            ("Executive Execution", "Radical Follow-Through, Shadow Org-Chart Navigation, Meeting Synthesis & Action Tracking, Cross-Functional Alignment, Crisis Triage."),
            ("Technical & Modern Leverage", "AI Agent Workflows (Gemini, Claude), Python Scripting, SQLite Pipeline Building, Advanced Excel/Financial Modeling, Rapid Web Prototyping."),
            ("Commercial & Vendor Acumen", "B2B Pipeline Management, Aggressive Vendor Rate Card Renegotiation (15–20% Savings), P&L Reconciliation, Contract Drafting."),
            ("High-Stakes Composure", "Zero Panic in High-Pressure Scenarios, VIP Protocol Management, Military-Grade Facility Clearances.")
        ],
        experience_items=[
            {
                "org": "Founder's Office Execution & Tech Automation",
                "location": "Bengaluru, India",
                "title": "Autonomous Dispatch & Intelligence Platform Developer",
                "period": "2025 – Present",
                "bullets": [
                    ("Full-Stack Operations Engine", "Conceived, architected, and built an automated operations platform prototype using Python, SQLite, and AI agents (github.com/AdityaMehra007/anti)."),
                    ("Automated Pipeline Scoring", "Automated pipeline scoring, calendar invitation dispatch (.ics), and contact integrity verification with 16/16 passing unit tests."),
                    ("Executive Time Compression", "Built executive dashboards that compress 4 hours of daily recruiter and pipeline research into 10-minute automated briefs.")
                ]
            },
            {
                "org": "Pencil Mark Interior Solutions LLP",
                "location": "Bengaluru, India",
                "title": "Commercial Operations & Founder's Associate Intern",
                "period": "Jul 2025 – Aug 2025",
                "bullets": [
                    ("Executive Right-Hand", "Acted as direct executive right-hand on commercial sales: managed 15+ high-priority client accounts, prepared quotes, and resolved site-vendor blockers."),
                    ("Commercial Impact", "Drove an 18% conversion improvement that generated ₹1.5L+ in new revenue; awarded a formal Written Management Commendation from the leadership team.")
                ]
            },
            {
                "org": "AERO INDIA 2025 & TRILOGY Concert",
                "location": "Bengaluru, India",
                "title": "High-Stakes Operations Lead",
                "period": "2025 – 2026",
                "bullets": [
                    ("Air Force Base Operations", "Commanded commercial exhibition pavilion at AERO INDIA 2025 (Air Force Station Yelahanka): 100k+ visitors, 0% asset loss, full MoD security protocol compliance."),
                    ("VIP Artist Staging", "Orchestrated backstage operations, artist protocol, and sound vendor contracts at Bangalore Club for Grammy Winner Pt. Vishwa Mohan Bhatt.")
                ]
            },
            {
                "org": "Independent Practice & Mehra's Kitchen",
                "location": "Bengaluru, India",
                "title": "Entrepreneurial Operator",
                "period": "2019 – Present",
                "bullets": [
                    ("Bootstrapped P&L Ownership", "Bootstrapped and delivered 300+ on-ground client projects; cut 15%–20% out of vendor budgets through direct contracting; achieved 30%+ repeat rate."),
                    ("Unit Economics Discipline", "Co-founded cloud kitchen venture: managed unit economics, raw ingredient procurement, and daily cash reconciliations with profitable unit economics.")
                ]
            }
        ],
        education_items=[dsu_edu],
        cert_items=certs_common
    )

if __name__ == "__main__":
    generate_all_tracks()
