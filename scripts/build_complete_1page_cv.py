import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import win32com.client

BASE_DIR = Path(r"e:\anti")

# Palette
C_NAVY = RGBColor(15, 23, 42)       # Primary Dark Navy
C_TEAL = RGBColor(13, 148, 136)     # Modern Teal Accent
C_SLATE = RGBColor(51, 65, 85)      # Slate Secondary
C_BODY = RGBColor(30, 41, 59)       # Body text
C_MUTED = RGBColor(100, 116, 139)   # Metadata

def add_clean_divider(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CBD5E1')
    pBdr.append(bottom)
    pPr.append(pBdr)

def build_complete_1page_cv():
    doc = Document()

    # Exact A4 page dimensions and calibrated margins (0.3" top/bottom, 0.45" left/right)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.28)
        section.bottom_margin = Inches(0.28)
        section.left_margin = Inches(0.45)
        section.right_margin = Inches(0.45)

    # 1. HEADER
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(0.5)
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(17)
    r_name.font.bold = True
    r_name.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(1.5)
    r_sub = p_sub.add_run("BBA GRADUATE (INTERNATIONAL BUSINESS)  |  OPERATIONS, GROWTH & AI AUTOMATION")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(8.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_TEAL

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(2.5)
    r_con = p_contact.add_run(
        "Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  "
        "linkedin.com/in/aditya-mehra-b8644b326  |  github.com/AdityaMehra007"
    )
    r_con.font.name = "Calibri"
    r_con.font.size = Pt(7.8)
    r_con.font.color.rgb = C_MUTED

    def add_sec(title, before=3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(8.8)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        add_clean_divider(p)

    # 2. PROFILE SUMMARY
    add_sec("Profile & Career Objective", before=1.5)
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(0.5)
    p_sum.paragraph_format.space_after = Pt(1.5)
    p_sum.paragraph_format.line_spacing = 1.05
    p_sum.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sum = p_sum.add_run(
        "Execution-focused BBA International Business graduate (Dayananda Sagar University '26) combining hands-on leadership "
        "across 300+ commercial events/activations, mission-critical operations at AERO India 2025 (100k+ attendees, 0 shrinkage), "
        "and AI data operations at Instawork (99%+ QA benchmark). Experienced in B2B client acquisition (₹1.5L+ closed, written commendation), "
        "vendor SLA negotiations (15–20% cost savings), and building Python/AI-driven business automation workflows. Seeking entry-level roles in "
        "Business Operations, Growth/BD, or General Management."
    )
    r_sum.font.name = "Calibri"
    r_sum.font.size = Pt(7.8)
    r_sum.font.color.rgb = C_BODY

    # 3. CORE SKILLS
    add_sec("Core Competencies & Technical Skills", before=2)
    skills_data = [
        ("Business & Operations: ", "Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, Vendor Negotiation, 15–20% Cost Reduction, Crisis Triage."),
        ("Commercial & B2B Growth: ", "B2B Outbound Outreach, Client Relationship Servicing (15+ Threads), Pitch Decks, Contract Closing, Lead Qualification."),
        ("AI, Automation & Tech: ", "Python Data Workflows, LLM Prompt Engineering, AI Dataset Curation & QA (Instawork 99%+), Clay AI, Notion AI, Automation DAGs."),
        ("Analytics, Trade & Systems: ", "Advanced MS Excel (XLOOKUP, Power Query, Pivot Tables), Incoterms 2020, Supply Chain Logistics, CRM (Salesforce, Zoho)."),
        ("Languages: ", "English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).")
    ]
    for s_pre, s_desc in skills_data:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.1)
        p_s.paragraph_format.space_before = Pt(0)
        p_s.paragraph_format.space_after = Pt(0.5)
        p_s.paragraph_format.line_spacing = 1.03

        rb = p_s.add_run("• ")
        rb.font.name = "Calibri"; rb.font.size = Pt(7.6); rb.bold = True; rb.font.color.rgb = C_TEAL

        rp = p_s.add_run(s_pre)
        rp.font.name = "Calibri"; rp.font.size = Pt(7.6); rp.bold = True; rp.font.color.rgb = C_NAVY

        rd = p_s.add_run(s_desc)
        rd.font.name = "Calibri"; rd.font.size = Pt(7.6); rd.font.color.rgb = C_BODY

    # 4. WORK EXPERIENCE & INTERNSHIPS
    add_sec("Work Experience & Practical Projects", before=2.5)

    experiences = [
        {
            "role": "Independent Event Director & Commercial Operations Lead",
            "company": "Commercial Event Operations",
            "location": "Bengaluru",
            "dates": "2019 – Present",
            "bullets": [
                ("Scaled Event Delivery: ", "Managed on-ground production and logistics for 300+ corporate events and brand activations for marquee clients including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing."),
                ("Vendor Governance & Cost Savings: ", "Achieved consistent 15% to 20% cost savings per project through direct supplier contracting and milestone-based SLA enforcement; maintained a 30%+ repeat-client rate."),
                ("Live Showcase Management: ", "Directed full event logistics, artist travel, and technical riders for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero live performance disruption.")
            ]
        },
        {
            "role": "Business Development Intern",
            "company": "Pencil Mark Interior Solutions LLP",
            "location": "Bengaluru",
            "dates": "Jul 2025 – Aug 2025",
            "bullets": [
                ("B2B Pipeline & Revenue: ", "Drove outbound corporate lead generation across commercial workspace projects, managing 15+ concurrent client threads and helping close ₹1.5L+ in commercial interior contracts (18% conversion rate)."),
                ("Executive Commendation: ", "Awarded a formal written management commendation by leadership for exceptional sales drive, client negotiation, and active pipeline expansion.")
            ]
        },
        {
            "role": "AI Data Operations Intern",
            "company": "Instawork Services India Pvt. Ltd.",
            "location": "Bengaluru",
            "dates": "Dec 2025",
            "bullets": [
                ("Robotics & Vision Datasets: ", "Curated and annotated high-density multi-modal datasets training enterprise robotics and human activity recognition machine learning models."),
                ("99%+ QA Benchmark: ", "Maintained a verified 99%+ quality assurance accuracy rating across all data streams, authoring standardized capture SOPs.")
            ]
        },
        {
            "role": "Exhibition Operations & Commercial Lead",
            "company": "Salt in My Coca — AERO India 2025",
            "location": "Yelahanka AFB, Bengaluru",
            "dates": "Feb 2025",
            "bullets": [
                ("High-Density Expo Logistics: ", "Led 7-day stall operations, visitor engagement, and inventory logistics at Asia's premier defense expo (100k+ attendees), achieving zero inventory shrinkage under strict military security protocols.")
            ]
        },
        {
            "role": "Operations, Unit Economics & Retail Lead",
            "company": "Mehra's Kitchen & Family Commercial Enterprise",
            "location": "Bengaluru & Kolkata",
            "dates": "2018 – 2025",
            "bullets": [
                ("Ground Operations Mastery: ", "Managed raw material procurement, unit cost economics, menu pricing, inventory turnover, supplier negotiations, and daily cash reconciliation across retail and food operations.")
            ]
        },
        {
            "role": "Project: Automated Market Intelligence & Pipeline Engine",
            "company": "Independent Engineering System",
            "location": "Bengaluru",
            "dates": "2025 – 2026",
            "bullets": [
                ("Data & Automation Architecture: ", "Engineered automated data extraction and enrichment pipelines analyzing 4,500+ commercial entities and 9,200+ network records using Python, LLM structured outputs, and Power Query.")
            ]
        }
    ]

    for exp in experiences:
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(1.5)
        p_h.paragraph_format.space_after = Pt(0)
        p_h.paragraph_format.keep_with_next = True

        r_r = p_h.add_run(exp["role"])
        r_r.font.name = "Calibri"; r_r.font.size = Pt(8.2); r_r.bold = True; r_r.font.color.rgb = C_NAVY

        r_c = p_h.add_run(f" | {exp['company']}, {exp['location']}")
        r_c.font.name = "Calibri"; r_c.font.size = Pt(7.6); r_c.font.italic = True; r_c.font.color.rgb = C_SLATE

        r_d = p_h.add_run(f" ({exp['dates']})")
        r_d.font.name = "Calibri"; r_d.font.size = Pt(7.5); r_d.bold = True; r_d.font.color.rgb = C_TEAL

        for b_pre, b_txt in exp["bullets"]:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.1)
            p_b.paragraph_format.space_before = Pt(0)
            p_b.paragraph_format.space_after = Pt(0.5)
            p_b.paragraph_format.line_spacing = 1.02
            p_b.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            rb = p_b.add_run("• ")
            rb.font.name = "Calibri"; rb.font.size = Pt(7.5); rb.bold = True; rb.font.color.rgb = C_TEAL

            rp = p_b.add_run(b_pre)
            rp.font.name = "Calibri"; rp.font.size = Pt(7.5); rp.bold = True; rp.font.color.rgb = C_NAVY

            rt = p_b.add_run(b_txt)
            rt.font.name = "Calibri"; rt.font.size = Pt(7.5); rt.font.color.rgb = C_BODY

    # 5. EDUCATION & CERTIFICATIONS
    add_sec("Education & Certifications", before=2)

    p_eb = doc.add_paragraph()
    p_eb.paragraph_format.space_before = Pt(1)
    p_eb.paragraph_format.space_after = Pt(0.5)
    p_eb.paragraph_format.line_spacing = 1.03
    
    r_deg = p_eb.add_run("Bachelor of Business Administration (BBA) — International Business  |  2023 – 2026\n")
    r_deg.bold = True; r_deg.font.color.rgb = C_NAVY; r_deg.font.size = Pt(8)
    
    r_uni = p_eb.add_run("Dayananda Sagar University, Bengaluru — Focus: International Trade & EXIM Policies, Incoterms 2020, Supply Chain, Business Statistics.\n")
    r_uni.font.color.rgb = C_SLATE; r_uni.font.size = Pt(7.6)

    r_cb = p_eb.add_run("Certifications & Honors: ")
    r_cb.bold = True; r_cb.font.color.rgb = C_NAVY; r_cb.font.size = Pt(7.6)
    
    r_cl = p_eb.add_run(
        "Written Management Commendation (Pencil Mark, 2025) • Google Digital Marketing Professional (2024) • "
        "Service Marketing (NPTEL, IIT Kharagpur, 2025) • Generative AI Mastermind (Outskill, 2025) • AI Tools & ChatGPT (be10x, 2025)"
    )
    r_cl.font.color.rgb = C_BODY; r_cl.font.size = Pt(7.5)

    docx_path = BASE_DIR / "ADITYA_MEHRA_COMPLETE_1PAGE_CV.docx"
    doc.save(docx_path)
    return docx_path

if __name__ == "__main__":
    out_docx = build_complete_1page_cv()
    print("Complete 1-Page DOCX built:", out_docx)

    # Verify page count in Word COM and export to PDF
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(str(out_docx))
    pages = doc.ComputeStatistics(2)
    print("Exact Word Page Count:", pages)
    pdf_path = BASE_DIR / "ADITYA_MEHRA_COMPLETE_1PAGE_CV.pdf"
    doc.ExportAsFixedFormat(str(pdf_path), 17)
    doc.Close()
    word.Quit()
    print("Exported PDF:", pdf_path)
