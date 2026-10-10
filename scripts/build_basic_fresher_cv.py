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

# Palette: Traditional, clean, black & dark slate for a standard basic fresher CV
C_NAVY = RGBColor(15, 23, 42)       # Dark Navy / Charcoal
C_SLATE = RGBColor(71, 85, 105)     # Muted Slate
C_BODY = RGBColor(30, 41, 59)       # Body text
C_MUTED = RGBColor(100, 116, 139)   # Contact / Metadata

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

def build_basic_fresher_cv():
    doc = Document()

    # Standard clean margins (0.5" top/bottom, 0.6" left/right)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.45)
        section.bottom_margin = Inches(0.45)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # 1. HEADER
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(20)
    r_name.font.bold = True
    r_name.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    r_sub = p_sub.add_run("BBA Graduate  |  Fresher")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_SLATE

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(6)
    r_con = p_contact.add_run(
        "Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com\n"
        "LinkedIn: linkedin.com/in/aditya-mehra-b8644b326  |  GitHub: github.com/AdityaMehra007"
    )
    r_con.font.name = "Calibri"
    r_con.font.size = Pt(8.5)
    r_con.font.color.rgb = C_MUTED

    def add_sec(title, before=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        add_clean_divider(p)

    # 2. CAREER OBJECTIVE
    add_sec("Career Objective", before=3)
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(2)
    p_obj.paragraph_format.space_after = Pt(4)
    p_obj.paragraph_format.line_spacing = 1.15
    r_obj = p_obj.add_run(
        "Motivated BBA graduate in International Business seeking an entry-level opportunity in Business Operations, "
        "Sales, Business Development, or Management Support. Quick learner with hands-on internship experience in client "
        "communication, event coordination, and modern computer tools. Eager to start my career and contribute positively to the organization."
    )
    r_obj.font.name = "Calibri"
    r_obj.font.size = Pt(9)
    r_obj.font.color.rgb = C_BODY

    # 3. EDUCATION (Placed right near the top as expected for freshers)
    add_sec("Education", before=5)
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(2)
    p_edu.paragraph_format.space_after = Pt(1)
    p_edu.paragraph_format.line_spacing = 1.12
    p_edu.paragraph_format.keep_with_next = True

    r1 = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business\n")
    r1.font.name = "Calibri"; r1.font.size = Pt(9.5); r1.bold = True; r1.font.color.rgb = C_NAVY

    r2 = p_edu.add_run("Dayananda Sagar University, Bengaluru\n")
    r2.font.name = "Calibri"; r2.font.size = Pt(9); r2.font.italic = True; r2.font.color.rgb = C_SLATE

    r3 = p_edu.add_run("Relevant Subjects: International Business, Marketing Management, Supply Chain Management, Business Communication, Financial Accounting.")
    r3.font.name = "Calibri"; r3.font.size = Pt(8.5); r3.font.color.rgb = C_BODY

    # 4. INTERNSHIPS & PRACTICAL EXPERIENCE
    add_sec("Internships & Practical Experience", before=5)

    experiences = [
        {
            "role": "Business Development Intern",
            "company": "Pencil Mark Interior Solutions LLP, Bengaluru",
            "bullets": [
                "Handled corporate client outreach, introduced design services to prospective businesses, and followed up on active inquiries.",
                "Assisted senior management in preparing proposals, presentations, and client quotation reviews.",
                "Received an official written letter of commendation from management for good performance and sales initiative."
            ]
        },
        {
            "role": "Operations Intern",
            "company": "Instawork Services India Pvt. Ltd., Bengaluru",
            "bullets": [
                "Assisted the team in data collection, categorization, and quality checking for robotics training models.",
                "Followed guidelines closely to maintain high accuracy and consistency in daily task submissions."
            ]
        },
        {
            "role": "Stall & Exhibition Coordinator",
            "company": "Salt in My Coca — AERO India Expo, Bengaluru",
            "bullets": [
                "Managed retail stall setup, product displays, and customer service at a premier aerospace exhibition.",
                "Handled product inventory and coordinated with diverse visitors while following event safety protocols."
            ]
        },
        {
            "role": "Event Coordinator & Operations Support",
            "company": "Commercial & Cultural Events, Bengaluru",
            "bullets": [
                "Coordinated on-ground arrangements, local vendor supplies, and stage setups for corporate and music events.",
                "Assisted in daily operations and customer billing for retail family business activities."
            ]
        }
    ]

    for exp in experiences:
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(3)
        p_h.paragraph_format.space_after = Pt(1)
        p_h.paragraph_format.keep_with_next = True

        r_r = p_h.add_run(exp["role"])
        r_r.font.name = "Calibri"; r_r.font.size = Pt(9); r_r.bold = True; r_r.font.color.rgb = C_NAVY

        r_c = p_h.add_run(f"  |  {exp['company']}")
        r_c.font.name = "Calibri"; r_c.font.size = Pt(8.5); r_c.font.italic = True; r_c.font.color.rgb = C_SLATE

        for b in exp["bullets"]:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.15)
            p_b.paragraph_format.space_before = Pt(0.5)
            p_b.paragraph_format.space_after = Pt(1)
            p_b.paragraph_format.line_spacing = 1.08

            rb = p_b.add_run("• ")
            rb.font.name = "Calibri"; rb.font.size = Pt(8.5); rb.bold = True; rb.font.color.rgb = C_SLATE

            rt = p_b.add_run(b)
            rt.font.name = "Calibri"; rt.font.size = Pt(8.5); rt.font.color.rgb = C_BODY

    # 5. KEY SKILLS (Basic, understandable, standard fresher skills)
    add_sec("Key Skills", before=5)
    skills = [
        ("Computer & Software: ", "MS Office (Word, Excel, PowerPoint), Google Workspace, Basic CRM, Internet Research, AI Tools (ChatGPT)."),
        ("Professional & Personal: ", "Client Communication, Problem Solving, Vendor Coordination, Teamwork, Time Management."),
        ("Languages: ", "English (Fluent), Hindi (Fluent), Punjabi (Native), Bengali (Conversational).")
    ]
    for s_title, s_desc in skills:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.15)
        p_s.paragraph_format.space_before = Pt(0.5)
        p_s.paragraph_format.space_after = Pt(1)
        p_s.paragraph_format.line_spacing = 1.08

        rb = p_s.add_run("• ")
        rb.font.name = "Calibri"; rb.font.size = Pt(8.5); rb.bold = True; rb.font.color.rgb = C_SLATE

        rp = p_s.add_run(s_title)
        rp.font.name = "Calibri"; rp.font.size = Pt(8.5); rp.bold = True; rp.font.color.rgb = C_NAVY

        rd = p_s.add_run(s_desc)
        rd.font.name = "Calibri"; rd.font.size = Pt(8.5); rd.font.color.rgb = C_BODY

    # 6. CERTIFICATIONS
    add_sec("Certifications", before=5)
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.left_indent = Inches(0.15)
    p_cert.paragraph_format.space_before = Pt(1)
    p_cert.paragraph_format.space_after = Pt(2)
    p_cert.paragraph_format.line_spacing = 1.1

    certs = [
        "Certificate of Commendation for Business Development (Pencil Mark)",
        "Google Digital Marketing Professional Certificate (Google)",
        "Service Marketing Certification (NPTEL, IIT Kharagpur)",
        "Generative AI Certification (Outskill)"
    ]
    
    rb = p_cert.add_run("• ")
    rb.font.name = "Calibri"; rb.font.size = Pt(8.5); rb.bold = True; rb.font.color.rgb = C_SLATE
    rc = p_cert.add_run("  |  ".join(certs))
    rc.font.name = "Calibri"; rc.font.size = Pt(8.2); rc.font.color.rgb = C_BODY

    docx_path = BASE_DIR / "ADITYA_MEHRA_BASIC_FRESHER_CV.docx"
    doc.save(docx_path)
    return docx_path

if __name__ == "__main__":
    out_docx = build_basic_fresher_cv()
    print("DOCX built:", out_docx)

    # Verify page count in Word COM and export to PDF
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(str(out_docx))
    pages = doc.ComputeStatistics(2)
    print("Exact Word Page Count:", pages)
    pdf_path = BASE_DIR / "ADITYA_MEHRA_BASIC_FRESHER_CV.pdf"
    doc.ExportAsFixedFormat(str(pdf_path), 17)
    doc.Close()
    word.Quit()
    print("Exported PDF:", pdf_path)
