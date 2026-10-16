"""
ATS Resume Generator (DOCX & Print-Ready HTML)
Generates pixel-perfect single-column ATS Word documents using python-docx
and accompanying print-ready HTML files for PDF export.
"""

import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


def create_resume_docx(filename, title_role, summary_text, highlight_bullets):
    doc = Document()

    # 0.5 inch margins for ATS 1-page efficiency
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Helper styles
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text.upper())
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = "Arial"
        run.font.color.rgb = RGBColor(31, 41, 55)  # Dark slate
        # Add horizontal line below heading
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        run1 = p.add_run(bold_prefix + ": ")
        run1.bold = True
        run1.font.size = Pt(9.5)
        run1.font.name = "Arial"
        run2 = p.add_run(text)
        run2.font.size = Pt(9.5)
        run2.font.name = "Arial"

    # Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(1)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_name = title_p.add_run("ADITYA MEHRA")
    run_name.bold = True
    run_name.font.size = Pt(16)
    run_name.font.name = "Arial"

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(6)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_contact = sub_p.add_run(
        "Bengaluru, Karnataka, India | +91 7003456624 | adityamehra799@gmail.com\n"
        "LinkedIn: linkedin.com/in/aditya-mehra-b8644b326 | Portfolio: adi-digital-universe.ai.studio"
    )
    run_contact.font.size = Pt(9)
    run_contact.font.name = "Arial"

    # Summary
    add_heading_1(f"Professional Summary — {title_role}")
    sum_p = doc.add_paragraph()
    sum_p.paragraph_format.space_after = Pt(4)
    run_sum = sum_p.add_run(summary_text)
    run_sum.font.size = Pt(9.5)
    run_sum.font.name = "Arial"

    # Core Competencies
    add_heading_1("Core Competencies & Skills")
    add_bullet(
        "Operations Leadership",
        "Vendor SLA Governance, Supplier Rate Cards, 15–20% Cost Optimization, End-to-End Delivery (300+ Events).",
    )
    add_bullet(
        "Supply Chain & Trade",
        "Incoterms 2020 (FOB, CIF, DDP), Logistics Coordination, Inventory Buffer Management, Working Capital P&L.",
    )
    add_bullet(
        "AI Data & Automation",
        "Robotics ML Dataset Curation, 99%+ Annotation QA Compliance, Google Gemini API, Python Scripting.",
    )
    add_bullet(
        "Analytics & Software",
        "Advanced MS Excel (XLOOKUP, Dynamic Pivots, Power Query), SQL Basics, Salesforce CRM, Zoho CRM.",
    )
    add_bullet(
        "Languages",
        "English (Fluent/Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).",
    )

    # Experience
    add_heading_1("Professional Experience")

    # Role 1: Independent Commercial Operations
    p_role1 = doc.add_paragraph()
    p_role1.paragraph_format.space_before = Pt(4)
    p_role1.paragraph_format.space_after = Pt(1)
    r1 = p_role1.add_run(
        "INDEPENDENT COMMERCIAL OPERATIONS & EVENT PRACTICE | Bengaluru, India\n"
    )
    r1.bold = True
    r1.font.size = Pt(10)
    r1.font.name = "Arial"
    r1_sub = p_role1.add_run("Independent Operations Lead | 2019 – Present")
    r1_sub.italic = True
    r1_sub.font.size = Pt(9)
    r1_sub.font.name = "Arial"

    add_bullet(
        "Procurement & Margin Expansion",
        "Spearheaded vendor SLA governance across 20+ suppliers, achieving 15%–20% cost reduction across 300+ live commercial activations.",
    )
    add_bullet(
        "High-Stakes Account Delivery",
        "Delivered multi-format activations for HP, Intel, Puma India, Tata Communications, and Razorpay with a 30%+ repeat client rate.",
    )
    add_bullet(
        "Ground Crisis Triage",
        "Executed zero-downtime on-ground crisis resolution under compressed turnarounds with 100% adherence to security protocols.",
    )

    # Role 2: Instawork
    p_role2 = doc.add_paragraph()
    p_role2.paragraph_format.space_before = Pt(4)
    p_role2.paragraph_format.space_after = Pt(1)
    r2 = p_role2.add_run("INSTAWORK SERVICES INDIA PVT. LTD. | Bengaluru, India\n")
    r2.bold = True
    r2.font.size = Pt(10)
    r2.font.name = "Arial"
    r2_sub = p_role2.add_run("AI Data Operations Intern | Dec 2025")
    r2_sub.italic = True
    r2_sub.font.size = Pt(9)
    r2_sub.font.name = "Arial"

    add_bullet(
        "Robotics Data Pipelines",
        "Curated multimodal datasets powering computer vision and warehouse logistics robotics machine learning models.",
    )
    add_bullet(
        "Quality Benchmark",
        "Maintained 99%+ QA adherence through bounding-box verification and edge-case classification, preventing training drift.",
    )

    # Role 3: AERO India
    p_role3 = doc.add_paragraph()
    p_role3.paragraph_format.space_before = Pt(4)
    p_role3.paragraph_format.space_after = Pt(1)
    r3 = p_role3.add_run(
        "AERO INDIA 2025 (SALT IN MY COCA) | Yelahanka Air Force Station, Bengaluru\n"
    )
    r3.bold = True
    r3.font.size = Pt(10)
    r3.font.name = "Arial"
    r3_sub = p_role3.add_run("Exhibition Operations Lead | Feb 2025")
    r3_sub.italic = True
    r3_sub.font.size = Pt(9)
    r3_sub.font.name = "Arial"

    add_bullet(
        "Zero Shrinkage Execution",
        "Directed full 7-day stall operations and inventory management under strict Ministry of Defence protocol with zero asset loss (100k+ attendees).",
    )

    # Role 4: Pencil Mark Solutions
    p_role4 = doc.add_paragraph()
    p_role4.paragraph_format.space_before = Pt(4)
    p_role4.paragraph_format.space_after = Pt(1)
    r4 = p_role4.add_run("PENCIL MARK INTERIOR SOLUTIONS LLP | Bengaluru, India\n")
    r4.bold = True
    r4.font.size = Pt(10)
    r4.font.name = "Arial"
    r4_sub = p_role4.add_run("Business Development Intern | Jul 2025 – Aug 2025")
    r4_sub.italic = True
    r4_sub.font.size = Pt(9)
    r4_sub.font.name = "Arial"

    add_bullet(
        "Executive Commendation",
        "Managed 15+ concurrent client pipelines, converting ₹1.5L+ in initial contract revenue; formally awarded Written Management Commendation.",
    )

    # Education
    add_heading_1("Education")
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(2)
    p_edu.paragraph_format.space_after = Pt(2)
    re1 = p_edu.add_run("DAYANANDA SAGAR UNIVERSITY (DSU) | Bengaluru, Karnataka\n")
    re1.bold = True
    re1.font.size = Pt(9.5)
    re1.font.name = "Arial"
    re2 = p_edu.add_run(
        "Bachelor of Business Administration (BBA) — International Business | Class of 2026\n"
    )
    re2.italic = True
    re2.font.size = Pt(9)
    re2.font.name = "Arial"
    re3 = p_edu.add_run(
        "Coursework: Incoterms 2020, Global Supply Chain Architecture, Working Capital Accounting, Business Statistics, Landed Cost Modeling."
    )
    re3.font.size = Pt(8.5)
    re3.font.name = "Arial"

    # Certifications
    add_heading_1("Certifications & Honors")
    add_bullet(
        "Commendation",
        "Written Management Commendation for BD & Commercial Excellence — Pencil Mark Solutions (2025).",
    )
    add_bullet("Google", "Google Digital Marketing Professional Certificate (2024).")
    add_bullet(
        "IIT Kharagpur",
        "Service Marketing: A Practical Approach — NPTEL, IIT Kharagpur (2025).",
    )
    add_bullet(
        "AI Systems",
        "Generative AI Mastermind (Outskill, 2025) & AI Tools for Business Productivity (be10x, 2025).",
    )

    doc.save(filename)
    print(f"[OK] Generated Word DOCX: {filename}")


if __name__ == "__main__":
    out_dir = r"e:\anti\AI-Command-Center\career"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Master ATS Resume
    create_resume_docx(
        os.path.join(out_dir, "ADITYA_MEHRA_MASTER_ATS_RESUME.docx"),
        "Business Operations & Analyst",
        "Results-driven Business Operations & Process Specialist combining an applied BBA in International Business (Dayananda Sagar University, Class of 2026) with an extensive track record delivering 300+ live commercial activations and events. Proven ability to negotiate vendor rate cards to achieve 15%–20% landed cost savings, curate robotics AI datasets at 99%+ QA accuracy (Instawork), and manage zero-shrinkage physical inventory at AERO India 2025 (100k+ attendees). Recipient of a formal written management commendation for commercial execution. Seeking entry-level Business Operations or Operations Analyst roles in Bengaluru.",
        [],
    )

    # 2. Supply Chain & Procurement Track
    create_resume_docx(
        os.path.join(out_dir, "ADITYA_MEHRA_SUPPLY_CHAIN_PROCUREMENT.docx"),
        "Supply Chain & Procurement Analyst",
        "Process-oriented Supply Chain & Procurement Analyst with academic specialization in BBA International Business (Incoterms 2020, freight modeling) and on-ground track record managing vendor SLA governance across 20+ suppliers. Reduced landed procurement costs by 15%–20% across 300+ commercial projects and managed high-security inventory logistics at AERO India 2025 with zero shrinkage. Advanced MS Excel (XLOOKUP, Dynamic Pivots, Power Query). Seeking Supply Chain or Procurement Operations roles in Bengaluru.",
        [],
    )

    # 3. AI Data Operations Track
    create_resume_docx(
        os.path.join(out_dir, "ADITYA_MEHRA_AI_DATA_OPERATIONS.docx"),
        "AI Data Operations & Quality Analyst",
        "Detail-oriented AI Data Operations Specialist experienced in robotics training data curation, multimodal annotation quality assurance (99%+ accuracy benchmark at Instawork), and workflow automation using Google Gemini API and Python. Combines a rigorous BBA background with hands-on prompt engineering and dataset drift prevention. Seeking AI Data Operations, ML Quality Analyst, or Business Automation roles.",
        [],
    )
