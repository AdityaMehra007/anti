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

# Palette: Clean, professional, recruiter-friendly
C_NAVY = RGBColor(15, 23, 42)       # Primary Dark Navy
C_TEAL = RGBColor(13, 148, 136)     # Subtle Teal Accent
C_SLATE = RGBColor(51, 65, 85)      # Subheaders
C_BODY = RGBColor(30, 41, 59)       # Body text
C_MUTED = RGBColor(100, 116, 139)   # Metadata

def add_clean_divider(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CBD5E1')
    pBdr.append(bottom)
    pPr.append(pBdr)

def build_fresher_cv_docx():
    doc = Document()

    # Exact A4 page dimensions and tight, clean margins for a guaranteed 1-page fit
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.35)
        section.bottom_margin = Inches(0.35)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # 1. HEADER
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1)
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(18)
    r_name.font.bold = True
    r_name.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("BBA Graduate (International Business)  |  Operations, Business Development & Growth")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_TEAL

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(4)
    r_con = p_contact.add_run(
        "Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  "
        "linkedin.com/in/aditya-mehra-b8644b326  |  github.com/AdityaMehra007"
    )
    r_con.font.name = "Calibri"
    r_con.font.size = Pt(8.5)
    r_con.font.color.rgb = C_MUTED

    def add_sec(title, before=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        add_clean_divider(p)

    # 2. OBJECTIVE / SUMMARY
    add_sec("Career Objective", before=2)
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(1)
    p_obj.paragraph_format.space_after = Pt(3)
    p_obj.paragraph_format.line_spacing = 1.08
    r_obj = p_obj.add_run(
        "Motivated BBA graduate in International Business (Dayananda Sagar University, 2026) seeking an entry-level role in "
        "Business Operations, Business Development, or General Management. Combines strong business foundations with hands-on "
        "experience managing B2B client pipelines, live event operations for major brands, and AI productivity tools. "
        "Commended in writing for outstanding sales performance and ready to contribute from Day 1."
    )
    r_obj.font.name = "Calibri"
    r_obj.font.size = Pt(8.5)
    r_obj.font.color.rgb = C_BODY

    # 3. EDUCATION
    add_sec("Education", before=3)
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(1.5)
    p_edu.paragraph_format.space_after = Pt(0.5)
    p_edu.paragraph_format.line_spacing = 1.05
    p_edu.paragraph_format.keep_with_next = True

    r1 = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business")
    r1.font.name = "Calibri"; r1.font.size = Pt(9); r1.bold = True; r1.font.color.rgb = C_NAVY
    r2 = p_edu.add_run("  |  2023 – 2026\n")
    r2.font.name = "Calibri"; r2.font.size = Pt(8.5); r2.bold = True; r2.font.color.rgb = C_TEAL
    r3 = p_edu.add_run("Dayananda Sagar University, Bengaluru  ")
    r3.font.name = "Calibri"; r3.font.size = Pt(8.5); r3.font.italic = True; r3.font.color.rgb = C_SLATE
    r4 = p_edu.add_run("— Key Coursework: International Trade, Global Supply Chain, Marketing, Financial Accounting, Business Statistics.")
    r4.font.name = "Calibri"; r4.font.size = Pt(8.2); r4.font.color.rgb = C_BODY

    # 4. INTERNSHIPS & WORK EXPERIENCE
    add_sec("Internships & Work Experience", before=3.5)

    experiences = [
        {
            "role": "Business Development Intern",
            "company": "Pencil Mark Interior Solutions LLP",
            "location": "Bengaluru",
            "dates": "Jul 2025 – Aug 2025",
            "bullets": [
                "Managed outbound B2B lead generation and client communications across 15+ concurrent commercial leads.",
                "Assisted in client presentations and contract discussions, helping close ₹1.5L+ in commercial interior contracts.",
                "Awarded a written management commendation for outstanding pipeline growth and proactive sales execution."
            ]
        },
        {
            "role": "AI Data Operations Intern",
            "company": "Instawork Services India Pvt. Ltd.",
            "location": "Bengaluru",
            "dates": "Dec 2025",
            "bullets": [
                "Assisted in AI data collection and annotation pipelines for robotics and human activity machine learning models.",
                "Maintained 99%+ quality accuracy on all submitted datasets following strict compliance guidelines."
            ]
        },
        {
            "role": "Exhibition & Operations Lead",
            "company": "Salt in My Coca — AERO India 2025",
            "location": "Yelahanka Air Force Station, Bengaluru",
            "dates": "Feb 2025",
            "bullets": [
                "Managed stall setup, product inventory, and visitor engagement over 7 days at Asia's largest aerospace show (100k+ attendees).",
                "Coordinated with high-profile visitors and defense delegates under strict security protocols with zero asset loss."
            ]
        },
        {
            "role": "Event Coordinator & Operations Lead",
            "company": "Independent Commercial Events",
            "location": "Bengaluru",
            "dates": "2019 – Present",
            "bullets": [
                "Coordinated on-ground operations and vendor logistics for 300+ events for clients including Tata Communications, Puma, and VH1 Supersonic.",
                "Negotiated with local vendors to deliver 15–20% cost savings while maintaining a 30%+ repeat-client rate.",
                "Handled live concert coordination for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero technical delays."
            ]
        },
        {
            "role": "Operations & Sales Associate",
            "company": "Mehra's Kitchen & Family Business",
            "location": "Bengaluru & Kolkata",
            "dates": "2018 – 2025",
            "bullets": [
                "Gained hands-on experience in daily retail operations, raw material procurement, inventory tracking, and cash reconciliation."
            ]
        }
    ]

    for exp in experiences:
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(2.5)
        p_h.paragraph_format.space_after = Pt(0)
        p_h.paragraph_format.keep_with_next = True

        r_r = p_h.add_run(exp["role"])
        r_r.font.name = "Calibri"; r_r.font.size = Pt(8.8); r_r.bold = True; r_r.font.color.rgb = C_NAVY

        r_c = p_h.add_run(f"  |  {exp['company']}, {exp['location']}")
        r_c.font.name = "Calibri"; r_c.font.size = Pt(8.2); r_c.font.italic = True; r_c.font.color.rgb = C_SLATE

        r_d = p_h.add_run(f"  ({exp['dates']})")
        r_d.font.name = "Calibri"; r_d.font.size = Pt(8); r_d.bold = True; r_d.font.color.rgb = C_TEAL

        for b in exp["bullets"]:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.12)
            p_b.paragraph_format.space_before = Pt(0.5)
            p_b.paragraph_format.space_after = Pt(0.5)
            p_b.paragraph_format.line_spacing = 1.05

            rb = p_b.add_run("• ")
            rb.font.name = "Calibri"; rb.font.size = Pt(8.2); rb.bold = True; rb.font.color.rgb = C_TEAL

            rt = p_b.add_run(b)
            rt.font.name = "Calibri"; rt.font.size = Pt(8.2); rt.font.color.rgb = C_BODY

    # 5. KEY SKILLS
    add_sec("Key Skills", before=3)
    skills_data = [
        ("Business & Operations: ", "B2B Lead Generation, Client Relationship Management, Vendor Coordination, Inventory & Stock Tracking, On-Ground Event Execution."),
        ("Tools & Productivity: ", "MS Excel (VLOOKUP, Pivot Tables), Google Sheets, CRM Basics (Salesforce, Zoho), AI Tools (ChatGPT, Claude, Notion AI)."),
        ("Trade & Commercial: ", "Incoterms 2020 basics, International Trade Documentation, Commercial Costing, Customer Service."),
        ("Languages: ", "English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Basic).")
    ]
    for s_pre, s_desc in skills_data:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.12)
        p_s.paragraph_format.space_before = Pt(0.5)
        p_s.paragraph_format.space_after = Pt(0.5)
        p_s.paragraph_format.line_spacing = 1.05

        rb = p_s.add_run("• ")
        rb.font.name = "Calibri"; rb.font.size = Pt(8.2); rb.bold = True; rb.font.color.rgb = C_TEAL

        rp = p_s.add_run(s_pre)
        rp.font.name = "Calibri"; rp.font.size = Pt(8.2); rp.bold = True; rp.font.color.rgb = C_NAVY

        rd = p_s.add_run(s_desc)
        rd.font.name = "Calibri"; rd.font.size = Pt(8.2); rd.font.color.rgb = C_BODY

    # 6. CERTIFICATIONS & HONORS
    add_sec("Certifications & Honors", before=3)
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.left_indent = Inches(0.12)
    p_cert.paragraph_format.space_before = Pt(1)
    p_cert.paragraph_format.space_after = Pt(0)
    p_cert.paragraph_format.line_spacing = 1.08

    cert_items = [
        "Written Management Commendation for BD Excellence (Pencil Mark, 2025)",
        "Google Digital Marketing Professional Certificate (2024)",
        "Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur, 2025)",
        "Generative AI Mastermind (Outskill, 2025)",
        "AI Tools & ChatGPT for Business Productivity (be10x, 2025)"
    ]
    
    r_c_intro = p_cert.add_run("• ")
    r_c_intro.font.name = "Calibri"; r_c_intro.font.size = Pt(8.2); r_c_intro.bold = True; r_c_intro.font.color.rgb = C_TEAL

    r_c_body = p_cert.add_run("  |  ".join(cert_items))
    r_c_body.font.name = "Calibri"; r_c_body.font.size = Pt(8); r_c_body.font.color.rgb = C_BODY

    docx_path = BASE_DIR / "ADITYA_MEHRA_SIMPLE_FRESHER_CV.docx"
    doc.save(docx_path)
    return docx_path

if __name__ == "__main__":
    out_docx = build_fresher_cv_docx()
    print("DOCX built:", out_docx)

    # Verify page count in Word COM and export to PDF
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(str(out_docx))
    pages = doc.ComputeStatistics(2)
    print("Exact Word Page Count:", pages)
    pdf_path = BASE_DIR / "ADITYA_MEHRA_SIMPLE_FRESHER_CV.pdf"
    doc.ExportAsFixedFormat(str(pdf_path), 17)
    doc.Close()
    word.Quit()
    print("Exported PDF:", pdf_path)
