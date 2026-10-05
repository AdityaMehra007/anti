"""
ADITYA GLOBAL CAREER INTELLIGENCE OS — RESUME COMPILATION ENGINE
Generates ATS-compliant, professionally styled .docx and printable .html resumes
for the 5 primary corporate operations tracks.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT_DIR = Path(__file__).resolve().parent
RESUMES_DIR = ROOT_DIR / "resumes"
RESUMES_DIR.mkdir(exist_ok=True)

NAVY = RGBColor(27, 54, 93)     # #1B365D
DARK_GREY = RGBColor(51, 65, 85) # #334155
CHARCOAL = RGBColor(15, 23, 42)  # #0F172A

TRACKS = {
    "Master_Operations": {
        "title": "BUSINESS OPERATIONS ASSOCIATE (FRESHER)",
        "summary": "Recent BBA graduate from Dayananda Sagar University, Bengaluru. Looking to build a career in business operations, coordination, and general management. Hands-on exposure to practical operations through family business coordination and on-ground event support (including Aero India). Reliable, detail-oriented, and ready for immediate full-time corporate roles.",
        "skills": "Business Operations, Daily Coordination, Vendor Follow-ups, On-Ground Event Support, Microsoft Excel, Task Tracking, Team Communication, Problem Resolution."
    },
    "Operations_Analyst": {
        "title": "OPERATIONS SUPPORT & MANAGEMENT TRAINEE",
        "summary": "Motivated BBA graduate seeking an entry-level Operations Support or Management Trainee role. Practical experience assisting with daily billing, record keeping, and scheduling. Comfortable using Excel for daily tracking and documentation.",
        "skills": "Operations Support, Administrative Coordination, Excel (Data Entry & Formatting), Process Follow-through, Documentation, Communication."
    },
    "Process_Risk_Ops": {
        "title": "OPERATIONS & PROCESS ASSISTANT",
        "summary": "Detail-oriented BBA graduate with strong work ethic and focus on standard operating procedures. Practical on-ground event coordination experience ensuring checklists and venue guidelines are followed accurately.",
        "skills": "Process Support, Checklist Execution, Quality Checks, Operations Coordination, Excel, Communication, Teamwork."
    },
    "PMO_Vendor_Logistics": {
        "title": "OPERATIONS & VENDOR COORDINATOR",
        "summary": "Adaptable BBA graduate with hands-on experience in on-ground event logistics and vendor coordination. Able to manage multiple tasks calmly under pressure and coordinate effectively between on-site teams and external suppliers.",
        "skills": "Vendor Coordination, Event Logistics, Scheduling, Vendor Follow-ups, Basic Excel, Administrative Support."
    },
    "EXIM_International_Trade": {
        "title": "BUSINESS & LOGISTICS COORDINATOR (FRESHER)",
        "summary": "BBA graduate with foundational academic exposure to international business and logistics. Practical experience coordinating suppliers and transport in commercial settings. Fast learner eager to contribute to business operations.",
        "skills": "Business Coordination, Supplier Follow-ups, Logistics Support, Documentation, Basic Excel, Teamwork."
    }
}

def add_heading_with_bottom_border(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Segoe UI"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = NAVY

    # Add bottom border XML
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1B365D')
    pbdr.append(bottom)
    pPr.append(pbdr)

def build_docx_resume(track_key, track_info):
    doc = docx.Document()

    # Set 0.5 inch margins for 1-page density
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.4)
        s.bottom_margin = Inches(0.4)
        s.left_margin = Inches(0.5)
        s.right_margin = Inches(0.5)

    # Name & Header
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Segoe UI"
    r_name.font.size = Pt(18)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY

    # Track Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(track_info["title"])
    r_sub.font.name = "Segoe UI"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = DARK_GREY

    # Contact Info
    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(6)
    p_contact.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cnt = p_contact.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  ashishiash007@gmail.com  |  linkedin.com/in/aditya-mehra")
    r_cnt.font.name = "Segoe UI"
    r_cnt.font.size = Pt(9)
    r_cnt.font.color.rgb = DARK_GREY

    # Professional Summary
    add_heading_with_bottom_border(doc, "PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(4)
    r_sum = p_sum.add_run(track_info["summary"])
    r_sum.font.name = "Segoe UI"
    r_sum.font.size = Pt(9.5)
    r_sum.font.color.rgb = CHARCOAL

    # Core Competencies
    add_heading_with_bottom_border(doc, "CORE COMPETENCIES & TECHNICAL SKILLS")
    p_comp = doc.add_paragraph()
    p_comp.paragraph_format.space_before = Pt(2)
    p_comp.paragraph_format.space_after = Pt(4)
    r_comp_lbl = p_comp.add_run("Core Capabilities: ")
    r_comp_lbl.font.name = "Segoe UI"
    r_comp_lbl.font.size = Pt(9.5)
    r_comp_lbl.font.bold = True
    r_comp_lbl.font.color.rgb = NAVY
    r_comp_val = p_comp.add_run(track_info["skills"] + "\n")
    r_comp_val.font.name = "Segoe UI"
    r_comp_val.font.size = Pt(9.5)

    r_tools_lbl = p_comp.add_run("Systems & Platforms: ")
    r_tools_lbl.font.name = "Segoe UI"
    r_tools_lbl.font.size = Pt(9.5)
    r_tools_lbl.font.bold = True
    r_tools_lbl.font.color.rgb = NAVY
    r_tools_val = p_comp.add_run("Microsoft Excel (Data Entry, Basic Formulas, Tables), Microsoft Word, Google Workspace, Email Correspondence.")
    r_tools_val.font.name = "Segoe UI"
    r_tools_val.font.size = Pt(9.5)

    # Professional & Operational Experience
    add_heading_with_bottom_border(doc, "PROFESSIONAL & OPERATIONAL EXPERIENCE")

    # Experience 1: Family Business Operations
    p_e1 = doc.add_paragraph()
    p_e1.paragraph_format.space_before = Pt(3)
    p_e1.paragraph_format.space_after = Pt(1)
    r_e1_role = p_e1.add_run("Business Operations Assistant")
    r_e1_role.font.name = "Segoe UI"
    r_e1_role.font.size = Pt(10)
    r_e1_role.font.bold = True
    r_e1_role.font.color.rgb = NAVY
    r_e1_co = p_e1.add_run(" — Commercial Operations (Family Business) | Kolkata, India\n")
    r_e1_co.font.name = "Segoe UI"
    r_e1_co.font.size = Pt(9.5)
    r_e1_co.font.italic = True
    r_e1_date = p_e1.add_run("2019 – 2020")
    r_e1_date.font.name = "Segoe UI"
    r_e1_date.font.size = Pt(8.5)
    r_e1_date.font.color.rgb = DARK_GREY

    bullets_e1 = [
        "Supported day-to-day business operations, stock inventory tracking, and billing documentation.",
        "Coordinated with local suppliers and transport partners to ensure on-time order fulfillment.",
        "Maintained sales records and inventory sheets in Excel, keeping administrative records accurate and organized."
    ]
    for b in bullets_e1:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Experience 2: Event Operations Coordinator
    p_e2 = doc.add_paragraph()
    p_e2.paragraph_format.space_before = Pt(4)
    p_e2.paragraph_format.space_after = Pt(1)
    r_e2_role = p_e2.add_run("Event Operations & On-Ground Coordinator")
    r_e2_role.font.name = "Segoe UI"
    r_e2_role.font.size = Pt(10)
    r_e2_role.font.bold = True
    r_e2_role.font.color.rgb = NAVY
    r_e2_co = p_e2.add_run(" — Brand Exhibitions & Live Events | Bengaluru, India\n")
    r_e2_co.font.name = "Segoe UI"
    r_e2_co.font.size = Pt(9.5)
    r_e2_co.font.italic = True
    r_e2_date = p_e2.add_run("2024 – 2026")
    r_e2_date.font.name = "Segoe UI"
    r_e2_date.font.size = Pt(8.5)
    r_e2_date.font.color.rgb = DARK_GREY

    bullets_e2 = [
        "Coordinated on-ground logistics, booth setups, and vendor arrivals for corporate brand exhibitions and live events.",
        "Aero India (Yelahanka Air Force Station): Supported exhibition stall logistics, vendor schedules, and attendee assistance on-site.",
        "TRILOGY Concert (Bengaluru Club): Managed artist coordination, stage vendors, and guest hospitality to ensure smooth event execution.",
        "Communicated with suppliers, venue staff, and team leads to resolve operational issues quickly during events."
    ]
    for b in bullets_e2:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Experience 3: Pencil Mark Interior Solutions
    p_e3 = doc.add_paragraph()
    p_e3.paragraph_format.space_before = Pt(4)
    p_e3.paragraph_format.space_after = Pt(1)
    r_e3_role = p_e3.add_run("Commercial Research & Business Operations Intern")
    r_e3_role.font.name = "Segoe UI"
    r_e3_role.font.size = Pt(10)
    r_e3_role.font.bold = True
    r_e3_role.font.color.rgb = NAVY
    r_e3_co = p_e3.add_run(" — Pencil Mark Interior Solutions LLP | Bengaluru, India\n")
    r_e3_co.font.name = "Segoe UI"
    r_e3_co.font.size = Pt(9.5)
    r_e3_co.font.italic = True
    r_e3_date = p_e3.add_run("July 2025 – August 2025")
    r_e3_date.font.name = "Segoe UI"
    r_e3_date.font.size = Pt(8.5)
    r_e3_date.font.color.rgb = DARK_GREY

    bullets_e3 = [
        "Synthesized commercial client specifications into actionable project briefs, streamlining handoffs between design and site procurement teams.",
        "Maintained structured CRM records and vendor matrices, tracking milestone completion across commercial interior projects."
    ]
    for b in bullets_e3:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Education
    add_heading_with_bottom_border(doc, "EDUCATION")
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(2)
    p_edu.paragraph_format.space_after = Pt(1)
    r_deg = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business")
    r_deg.font.name = "Segoe UI"
    r_deg.font.size = Pt(10)
    r_deg.font.bold = True
    r_deg.font.color.rgb = NAVY
    r_inst = p_edu.add_run(" | Dayananda Sagar University (DSU), Bengaluru, India\n")
    r_inst.font.name = "Segoe UI"
    r_inst.font.size = Pt(9.5)
    r_yr = p_edu.add_run("Degree Completed: BBA International Business | Immediate Full-Time Availability\n")
    r_yr.font.name = "Segoe UI"
    r_yr.font.size = Pt(8.5)
    r_yr.font.color.rgb = DARK_GREY
    r_course = p_edu.add_run("Relevant Coursework: Business Operations, Principles of Management, Business Communication, Marketing Management, Organizational Behavior, Project Execution.")
    r_course.font.name = "Segoe UI"
    r_course.font.size = Pt(8.5)

    # Certifications
    add_heading_with_bottom_border(doc, "CERTIFICATIONS & CREDENTIALS")
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.space_before = Pt(2)
    p_cert.paragraph_format.space_after = Pt(2)
    r_certs = p_cert.add_run("• Google Digital Marketing Professional Certificate (Google / Coursera)\n• Service Marketing & Operational Delivery (NPTEL / IIT Kharagpur)\n• Generative AI & Automation Mastermind (Outskill)\n• Prompt Engineering & Agentic Workflow Design (Project Implementation)")
    r_certs.font.name = "Segoe UI"
    r_certs.font.size = Pt(8.5)
    r_certs.font.color.rgb = CHARCOAL

    out_docx = RESUMES_DIR / f"Aditya_Mehra_Resume_{track_key}_2026.docx"
    doc.save(str(out_docx))
    print(f"Generated DOCX: {out_docx}")
    return out_docx

def build_printable_html_resume():
    """Builds a single-page pixel-perfect HTML printable resume."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aditya Mehra — Executive Resume (BBA International Business '26)</title>
    <style>
        @page {{
            size: A4;
            margin: 12mm 14mm 12mm 14mm;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #0f172a;
            line-height: 1.35;
            background: #fff;
            padding: 24px;
            max-width: 850px;
            margin: 0 auto;
        }}
        @media print {{
            body {{ padding: 0; max-width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
        .header {{ text-align: center; margin-bottom: 12px; }}
        h1 {{ font-size: 24px; font-weight: 800; color: #1B365D; letter-spacing: 0.5px; text-transform: uppercase; }}
        .title {{ font-size: 13px; font-weight: 700; color: #334155; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .contact {{ font-size: 11px; color: #475569; margin-top: 4px; }}
        .contact a {{ color: #1B365D; text-decoration: none; }}
        
        .section-title {{
            font-size: 12px;
            font-weight: 800;
            color: #1B365D;
            text-transform: uppercase;
            border-bottom: 1.5px solid #1B365D;
            padding-bottom: 2px;
            margin-top: 10px;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }}
        p {{ font-size: 11px; color: #1e293b; margin-bottom: 5px; }}
        .competency-box {{ font-size: 11px; margin-bottom: 6px; }}
        .competency-box strong {{ color: #1B365D; }}
        
        .exp-item {{ margin-bottom: 8px; }}
        .exp-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
        .exp-role {{ font-size: 12px; font-weight: 700; color: #1B365D; }}
        .exp-date {{ font-size: 10px; color: #64748b; font-weight: 600; }}
        .exp-sub {{ font-size: 11px; font-style: italic; color: #334155; margin-bottom: 3px; }}
        
        ul {{ padding-left: 18px; margin-bottom: 6px; }}
        li {{ font-size: 10.5px; color: #1e293b; margin-bottom: 2.5px; line-height: 1.35; }}
        
        .edu-item {{ margin-bottom: 6px; }}
        .edu-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
        .edu-deg {{ font-size: 12px; font-weight: 700; color: #1B365D; }}
        .edu-date {{ font-size: 10px; color: #64748b; font-weight: 600; }}
        
        .cert-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 10.5px; color: #1e293b; }}

        .action-bar {{ background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .btn-print {{ background: #1B365D; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }}
        .btn-print:hover {{ background: #0f172a; }}
    </style>
</head>
<body>

    <div class="action-bar no-print">
        <div><strong>Printable / ATS-Ready Executive Resume:</strong> Click 'Print to PDF' or press Ctrl+P to save as clean PDF.</div>
        <button class="btn-print" onclick="window.print()">🖨️ Print to PDF</button>
    </div>

    <div class="header">
        <h1>ADITYA MEHRA</h1>
        <div class="title">BBA Graduate — Business Operations & Operations Support (Fresher)</div>
        <div class="contact">
            Bengaluru, Karnataka, India &nbsp;|&nbsp; +91 7003456624 &nbsp;|&nbsp; adityamehra007@gmail.com &nbsp;|&nbsp; linkedin.com/in/aditya-mehra
        </div>
    </div>

    <div class="section-title">Professional Summary</div>
    <p>
        Recent BBA (Bachelor of Business Administration) graduate from Dayananda Sagar University, Bengaluru. Motivated fresher looking to start an entry-level career in Business Operations, General Management, or Operations Support. Practical exposure to daily business coordination through family business operations and on-ground event assistance. Eager learner with strong communication skills, basic Excel knowledge, and immediate full-time corporate availability.
    </p>

    <div class="section-title">Core Competencies & Skills</div>
    <div class="competency-box">
        <strong>Operations & Coordination:</strong> Daily task scheduling, vendor follow-ups, operational checklists, basic administrative support, team communication.
    </div>
    <div class="competency-box">
        <strong>Computer & Office Tools:</strong> Microsoft Excel (Data Entry, Basic Formulas, Tables), Microsoft Word, Google Workspace, Email Correspondence.
    </div>

    <div class="section-title">Practical Experience & Exposure</div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Business Operations Assistant</div>
            <div class="exp-date">2019 – 2020</div>
        </div>
        <div class="exp-sub">Commercial Operations (Family Business) | Kolkata, India</div>
        <ul>
            <li>Assisted with day-to-day business operations, billing documentation, and customer order coordination.</li>
            <li>Maintained basic inventory and sales records using Excel.</li>
            <li>Coordinated with local suppliers and logistics partners for daily dispatches.</li>
        </ul>
    </div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Event Operations & On-Ground Coordinator</div>
            <div class="exp-date">2024 – 2026</div>
        </div>
        <div class="exp-sub">Brand Exhibitions & Live Events | Bengaluru, India</div>
        <ul>
            <li>Coordinated on-ground logistics, booth setups, and vendor arrivals for corporate brand exhibitions and live events.</li>
            <li><strong>Aero India (Yelahanka Air Force Station):</strong> Supported exhibition stall logistics, vendor schedules, and attendee assistance on-site.</li>
            <li><strong>TRILOGY Concert (Bengaluru Club):</strong> Managed artist coordination, stage vendors, and guest hospitality to ensure smooth event execution.</li>
            <li>Communicated with suppliers, venue staff, and team leads to resolve operational issues quickly during events.</li>
        </ul>
    </div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Commercial Research & Business Operations Intern</div>
            <div class="exp-date">July 2025 – August 2025</div>
        </div>
        <div class="exp-sub">Pencil Mark Interior Solutions LLP | Bengaluru, India</div>
        <ul>
            <li>Synthesized commercial client specifications into actionable project briefs, streamlining handoffs between design and site procurement teams.</li>
            <li>Maintained structured records and vendor matrices, tracking milestone completion across projects.</li>
        </ul>
    </div>

    <div class="section-title">Education</div>
    <div class="edu-item">
        <div class="edu-head">
            <div class="edu-deg">Bachelor of Business Administration (BBA) — International Business</div>
            <div class="edu-date">Completed (Fresher)</div>
        </div>
        <div class="exp-sub">Dayananda Sagar University (DSU), Bengaluru, India | Immediate Full-Time Availability</div>
        <p style="font-size: 10px; color: #475569; margin-top: 2px;">
            <strong>Relevant Coursework:</strong> Principles of Management, Business Operations, Business Communication, Marketing Management, Organizational Behavior, Project Execution.
        </p>
    </div>

    <div class="section-title">Certifications & Credentials</div>
    <div class="cert-grid">
        <div>• Digital Marketing Fundamentals (Google / Coursera)</div>
        <div>• Service Marketing & Operational Delivery (NPTEL / IIT Kharagpur)</div>
    </div>

</body>
</html>
"""
    out_html = RESUMES_DIR / "Aditya_Mehra_Resume_Printable.html"
    out_html.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML Resume: {out_html}")
    return out_html

def main():
    print("Building Tailored Resume Variants...")
    for k, v in TRACKS.items():
        build_docx_resume(k, v)
    build_printable_html_resume()
    print("SUCCESS: All 5 tailored DOCX resumes and 1 printable HTML resume generated in e:\\anti\\resumes\\")

if __name__ == "__main__":
    main()
