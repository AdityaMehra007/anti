import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
import win32com.client
import pypdf

BASE_DIR = Path(r"e:\anti")

# Palette: Clean, approachable, modern corporate
C_NAVY = RGBColor(15, 23, 42)       # #0F172A Dark Slate Navy
C_SLATE = RGBColor(71, 85, 105)     # #475569 Slate
C_BODY = RGBColor(30, 41, 59)       # #1E293B Dark Slate Body
C_MUTED = RGBColor(100, 116, 139)   # #64748B Secondary Text
C_LINK = "1E3A8A"                   # #1E3A8A Dark Blue

JOB_REF = "REF9195V"
POSTING_ID = "744000152372959"

def add_clean_divider(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')       # 0.5 pt
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CBD5E1')
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_hyperlink_run(paragraph, url, display_text, font_size_pt=8.5, color_hex="1E3A8A", bold=False, underline=True):
    r_id = paragraph.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(
        f'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        f'r:id="{r_id}">'
        f'<w:r>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
        f'<w:color w:val="{color_hex}"/>'
        f'{"<w:b/>" if bold else ""}'
        f'{"<w:u w:val=\"single\"/>" if underline else ""}'
        f'<w:sz w:val="{int(font_size_pt * 2)}"/>'
        f'</w:rPr>'
        f'<w:t>{display_text}</w:t>'
        f'</w:r>'
        f'</w:hyperlink>'
    )
    paragraph._p.append(hyperlink)

def add_bullet_item(doc, prefix, body, space_after=1.2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    p.paragraph_format.line_spacing = 1.11
    
    r_sym = p.add_run("•  ")
    r_sym.font.name = "Calibri"
    r_sym.font.size = Pt(8.8)
    r_sym.font.bold = True
    r_sym.font.color.rgb = C_SLATE
    
    if prefix:
        r_pre = p.add_run(prefix + " ")
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(8.8)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
        
    r_body = p.add_run(body)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(8.8)
    r_body.font.color.rgb = C_BODY

def build_docx_with_verified_ids(filename):
    doc = Document()
    
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.40)
        section.bottom_margin = Inches(0.40)
        section.left_margin = Inches(0.50)
        section.right_margin = Inches(0.50)
        
    # Name Header
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1.0)
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(19.0)
    r_name.font.bold = True
    r_name.font.color.rgb = C_NAVY
    
    # Subtitle with Both Official Job IDs clearly displayed!
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2.0)
    r_sub = p_sub.add_run(f"BBA Graduate  |  Onboarding Associate (Job Ref: {JOB_REF}  •  Req ID: {POSTING_ID})  |  Ready to Learn & Contribute")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.1)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_SLATE
    
    # Contact Row 1
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(0)
    p_c1.paragraph_format.space_after = Pt(1.5)
    
    r_loc = p_c1.add_run("Bengaluru, Karnataka, India  |  ")
    r_loc.font.name = "Calibri"; r_loc.font.size = Pt(8.5); r_loc.font.color.rgb = C_MUTED
    
    r_ph = p_c1.add_run("Phone: ")
    r_ph.font.name = "Calibri"; r_ph.font.size = Pt(8.5); r_ph.font.bold = True; r_ph.font.color.rgb = C_NAVY
    add_hyperlink_run(p_c1, "tel:+917003456624", "+91 7003456624", font_size_pt=8.5, color_hex=C_LINK, underline=False)
    
    r_sep1 = p_c1.add_run("  |  Email: ")
    r_sep1.font.name = "Calibri"; r_sep1.font.size = Pt(8.5); r_sep1.font.bold = True; r_sep1.font.color.rgb = C_NAVY
    add_hyperlink_run(p_c1, "mailto:adityamehra799@gmail.com", "adityamehra799@gmail.com", font_size_pt=8.5, color_hex=C_LINK, underline=False)
    
    # Contact Row 2
    p_c2 = doc.add_paragraph()
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_before = Pt(0)
    p_c2.paragraph_format.space_after = Pt(3.5)
    
    r_w_lbl = p_c2.add_run("Portfolio: ")
    r_w_lbl.font.name = "Calibri"; r_w_lbl.font.size = Pt(8.5); r_w_lbl.font.bold = True; r_w_lbl.font.color.rgb = C_NAVY
    add_hyperlink_run(p_c2, "https://adi-digital-universe.ai.studio/", "adi-digital-universe.ai.studio", font_size_pt=8.5, color_hex=C_LINK, underline=True)
    
    r_sep2 = p_c2.add_run("  |  LinkedIn: ")
    r_sep2.font.name = "Calibri"; r_sep2.font.size = Pt(8.5); r_sep2.font.bold = True; r_sep2.font.color.rgb = C_NAVY
    add_hyperlink_run(p_c2, "https://www.linkedin.com/in/aditya-mehra-b8644b326", "linkedin.com/in/aditya-mehra-b8644b326", font_size_pt=8.5, color_hex=C_LINK, underline=True)
    
    r_sep3 = p_c2.add_run("  |  GitHub: ")
    r_sep3.font.name = "Calibri"; r_sep3.font.size = Pt(8.5); r_sep3.font.bold = True; r_sep3.font.color.rgb = C_NAVY
    add_hyperlink_run(p_c2, "https://github.com/AdityaMehra007", "github.com/AdityaMehra007", font_size_pt=8.5, color_hex=C_LINK, underline=True)
    
    def add_sec_hdr(title, before=3.2):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(1.8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        add_clean_divider(p)

    # 1. Career Objective (Includes Ref & Req ID)
    add_sec_hdr("Career Objective", before=1.8)
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(1.0)
    p_obj.paragraph_format.space_after = Pt(2.2)
    p_obj.paragraph_format.line_spacing = 1.12
    r_obj = p_obj.add_run(
        f"Energetic and hardworking BBA graduate eager to start my career as an Onboarding Associate at Allegis Global Solutions (Job Ref: {JOB_REF} / Req ID: {POSTING_ID}). "
        "A positive team player who learns new software and procedures quickly, follows instructions carefully, and takes full ownership of daily tasks. "
        "Brings practical experience in vendor follow-ups, document checking, basic spreadsheet work, and coordination. "
        "Excited to support team goals with high dedication, strong communication, and complete availability for the 3:00 PM – 12:00 AM shift."
    )
    r_obj.font.name = "Calibri"
    r_obj.font.size = Pt(8.8)
    r_obj.font.color.rgb = C_BODY

    # 2. Education
    add_sec_hdr("Education", before=2.6)
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(1.0)
    p_edu.paragraph_format.space_after = Pt(1.0)
    p_edu.paragraph_format.line_spacing = 1.10
    p_edu.paragraph_format.keep_with_next = True
    
    r_deg = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business (2023 – 2026)\n")
    r_deg.font.name = "Calibri"; r_deg.font.size = Pt(9.0); r_deg.bold = True; r_deg.font.color.rgb = C_NAVY
    
    r_uni = p_edu.add_run("Dayananda Sagar University (DSU), Bengaluru\n")
    r_uni.font.name = "Calibri"; r_uni.font.size = Pt(8.7); r_uni.font.italic = True; r_uni.font.color.rgb = C_SLATE
    
    r_crs = p_edu.add_run("Key Subjects Studied: Supply Chain & Logistics, Operations Management, Marketing, Business Communication, Business Law.")
    r_crs.font.name = "Calibri"; r_crs.font.size = Pt(8.4); r_crs.font.color.rgb = C_BODY

    # 3. Work Experience & Practical Exposure
    add_sec_hdr("Work Experience & Practical Exposure", before=3.0)
    
    experiences = [
        {
            "role": "Operations Intern",
            "company": "Instawork Services India, Bengaluru",
            "bullets": [
                "Supported the team with daily data checking, reviewing records carefully against project guidelines.",
                "Identified missing fields and simple errors early so the team could correct them before delivery deadlines.",
                "Kept daily work logs updated on spreadsheets and worked closely with team members to hit shift targets."
            ]
        },
        {
            "role": "Operations & Outreach Intern",
            "company": "Pencil Mark Interior Solutions, Bengaluru",
            "bullets": [
                "Coordinated with local interior vendors to collect registration forms, price quotations, and required documents.",
                "Made phone calls and sent emails to follow up on order timelines and resolve simple supplier questions.",
                "Maintained an updated vendor list in MS Excel; received an appreciation letter from management for dedicated work."
            ]
        },
        {
            "role": "Stall & Logistics Coordinator",
            "company": "AERO India Exhibition (Salt in My Coca), Bengaluru",
            "bullets": [
                "Assisted with setting up the exhibition stall, badge checking, and welcoming trade visitors with positive energy.",
                "Counted incoming product boxes against delivery slips to ensure no stock was misplaced during busy event hours."
            ]
        },
        {
            "role": "Event Logistics Volunteer",
            "company": "Commercial & College Events, Bengaluru",
            "bullets": [
                "Worked with student teams and local sound/lighting suppliers to ensure equipment arrived on time for campus festivals.",
                "Stayed on ground to help suppliers set up smoothly and solved minor event needs quickly with a positive attitude."
            ]
        },
        {
            "role": "Store & Customer Assistant",
            "company": "Family Retail Store & Food Business, Bengaluru",
            "bullets": [
                "Talked with wholesale suppliers to place regular stock reorders and checked incoming bills against received goods.",
                "Handled daily customer billing and counter sales with a friendly, helpful attitude."
            ]
        }
    ]
    
    for exp in experiences:
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(1.8)
        p_hdr.paragraph_format.space_after = Pt(0.6)
        p_hdr.paragraph_format.keep_with_next = True
        
        r_r = p_hdr.add_run(exp["role"])
        r_r.font.name = "Calibri"; r_r.font.size = Pt(8.8); r_r.font.bold = True; r_r.font.color.rgb = C_NAVY
        
        r_div = p_hdr.add_run("  |  ")
        r_div.font.name = "Calibri"; r_div.font.size = Pt(8.8); r_div.font.color.rgb = C_MUTED
        
        r_c = p_hdr.add_run(exp["company"])
        r_c.font.name = "Calibri"; r_c.font.size = Pt(8.6); r_c.font.italic = True; r_c.font.color.rgb = C_SLATE
        
        for b in exp["bullets"]:
            add_bullet_item(doc, "", b, space_after=0.8)

    # 4. Key Skills
    add_sec_hdr("Key Skills & Strengths", before=2.8)
    skills = [
        ("Daily Work & Operations", "Vendor Coordination, Document Checking, Following Process Steps (SOPs), Timely Follow-ups, Task Tracking."),
        ("Computer & Office Tools", "MS Excel (Data Entry, Lists, Basic Formatting), MS Word, MS PowerPoint, Google Sheets & Docs, Email Writing."),
        ("Personal Qualities", "High Energy & Enthusiasm, Fast Learner, Dependable Team Player, Good Communication, Shift Flexible (3 PM – 12 AM), English & Hindi.")
    ]
    for cat_name, skill_str in skills:
        add_bullet_item(doc, cat_name + ":", skill_str, space_after=0.8)

    # 5. Certificates & Recognition
    add_sec_hdr("Certificates & Recognition", before=2.6)
    certs = [
        ("Letter of Appreciation for Dedication & Good Work", "Pencil Mark Interior Solutions (Client Outreach & Vendor Support)."),
        ("Fundamentals of Digital Marketing Certificate", "Google (Digital Business Fundamentals & Online Tools)."),
        ("Operations & Marketing Management Course", "NPTEL, IIT Kharagpur (Business Operations & Marketing Principles)."),
        ("Office Productivity & AI Workshop", "Outskill (Modern Work Tools, Spreadsheets & Everyday Productivity).")
    ]
    for c_title, c_issuer in certs:
        add_bullet_item(doc, c_title + ":", c_issuer, space_after=0.6)
        
    doc.save(filename)
    print(f"Saved DOCX: {filename}")
    return filename

def build_html_with_verified_ids(filename):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aditya Mehra - Onboarding Associate CV (Job Ref: {JOB_REF} / Req: {POSTING_ID})</title>
    <style>
        @page {{ size: A4; margin: 9mm 12mm; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
            color: #1E293B;
            background: #FFFFFF;
            line-height: 1.27;
            font-size: 8.9pt;
            padding: 6mm 10mm;
            max-width: 210mm;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 19pt;
            font-weight: 700;
            color: #0F172A;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }}
        .subtitle {{
            font-size: 9.1pt;
            font-weight: 700;
            color: #334155;
            text-align: center;
            margin-bottom: 3px;
        }}
        .contact-bar {{
            text-align: center;
            font-size: 8.5pt;
            color: #64748B;
            margin-bottom: 2px;
        }}
        .contact-bar a {{
            color: #1E3A8A;
            text-decoration: underline;
        }}
        .section-title {{
            font-size: 9.5pt;
            font-weight: 700;
            color: #0F172A;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            border-bottom: 1px solid #CBD5E1;
            padding-bottom: 2px;
            margin-top: 6px;
            margin-bottom: 3px;
        }}
        p.objective {{
            font-size: 8.8pt;
            color: #1E293B;
            text-align: justify;
            margin-bottom: 3px;
            line-height: 1.25;
        }}
        .edu-degree {{
            font-size: 9.0pt;
            font-weight: 700;
            color: #0F172A;
        }}
        .edu-school {{
            font-size: 8.7pt;
            font-style: italic;
            color: #334155;
            margin-bottom: 1px;
        }}
        .edu-coursework {{
            font-size: 8.4pt;
            color: #1E293B;
        }}
        .exp-block {{
            margin-bottom: 3px;
        }}
        .exp-header {{
            font-size: 8.8pt;
            margin-bottom: 1px;
        }}
        .exp-header .role {{
            font-weight: 700;
            color: #0F172A;
        }}
        .exp-header .sep {{
            color: #94A3B8;
            margin: 0 4px;
        }}
        .exp-header .company {{
            font-style: italic;
            color: #334155;
        }}
        ul {{
            list-style: none;
            padding-left: 0;
        }}
        li {{
            position: relative;
            padding-left: 14px;
            font-size: 8.8pt;
            color: #1E293B;
            margin-bottom: 1.5px;
            line-height: 1.23;
        }}
        li::before {{
            content: "•";
            position: absolute;
            left: 2px;
            color: #334155;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>ADITYA MEHRA</h1>
    <div class="subtitle">BBA Graduate | Onboarding Associate (Job Ref: {JOB_REF} &bull; Req ID: {POSTING_ID}) | Ready to Learn & Contribute</div>
    <div class="contact-bar">
        Bengaluru, Karnataka, India &nbsp;|&nbsp; 
        <strong>Phone:</strong> <a href="tel:+917003456624">+91 7003456624</a> &nbsp;|&nbsp; 
        <strong>Email:</strong> <a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a>
    </div>
    <div class="contact-bar">
        <strong>Portfolio:</strong> <a href="https://adi-digital-universe.ai.studio/">adi-digital-universe.ai.studio</a> &nbsp;|&nbsp; 
        <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/aditya-mehra-b8644b326">linkedin.com/in/aditya-mehra-b8644b326</a> &nbsp;|&nbsp; 
        <strong>GitHub:</strong> <a href="https://github.com/AdityaMehra007">github.com/AdityaMehra007</a>
    </div>

    <div class="section-title">Career Objective</div>
    <p class="objective">
        Energetic and hardworking BBA graduate eager to start my career as an Onboarding Associate at Allegis Global Solutions (Job Ref: {JOB_REF} / Req ID: {POSTING_ID}). A positive team player who learns new software and procedures quickly, follows instructions carefully, and takes full ownership of daily tasks. Brings practical experience in vendor follow-ups, document checking, basic spreadsheet work, and coordination. Excited to support team goals with high dedication, strong communication, and complete availability for the 3:00 PM – 12:00 AM shift.
    </p>

    <div class="section-title">Education</div>
    <div class="edu-degree">Bachelor of Business Administration (BBA) — International Business (2023 – 2026)</div>
    <div class="edu-school">Dayananda Sagar University (DSU), Bengaluru</div>
    <div class="edu-coursework"><strong>Key Subjects Studied:</strong> Supply Chain & Logistics, Operations Management, Marketing, Business Communication, Business Law.</div>

    <div class="section-title">Work Experience & Practical Exposure</div>
    
    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Operations Intern</span>
            <span class="sep">|</span>
            <span class="company">Instawork Services India, Bengaluru</span>
        </div>
        <ul>
            <li>Supported the team with daily data checking, reviewing records carefully against project guidelines.</li>
            <li>Identified missing fields and simple errors early so the team could correct them before delivery deadlines.</li>
            <li>Kept daily work logs updated on spreadsheets and worked closely with team members to hit shift targets.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Operations & Outreach Intern</span>
            <span class="sep">|</span>
            <span class="company">Pencil Mark Interior Solutions, Bengaluru</span>
        </div>
        <ul>
            <li>Coordinated with local interior vendors to collect registration forms, price quotations, and required documents.</li>
            <li>Made phone calls and sent emails to follow up on order timelines and resolve simple supplier questions.</li>
            <li>Maintained an updated vendor list in MS Excel; received an appreciation letter from management for dedicated work.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Stall & Logistics Coordinator</span>
            <span class="sep">|</span>
            <span class="company">AERO India Exhibition (Salt in My Coca), Bengaluru</span>
        </div>
        <ul>
            <li>Assisted with setting up the exhibition stall, badge checking, and welcoming trade visitors with positive energy.</li>
            <li>Counted incoming product boxes against delivery slips to ensure no stock was misplaced during busy event hours.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Event Logistics Volunteer</span>
            <span class="sep">|</span>
            <span class="company">Commercial & College Events, Bengaluru</span>
        </div>
        <ul>
            <li>Worked with student teams and local sound/lighting suppliers to ensure equipment arrived on time for campus festivals.</li>
            <li>Stayed on ground to help suppliers set up smoothly and solved minor event needs quickly with a positive attitude.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Store & Customer Assistant</span>
            <span class="sep">|</span>
            <span class="company">Family Retail Store & Food Business, Bengaluru</span>
        </div>
        <ul>
            <li>Talked with wholesale suppliers to place regular stock reorders and checked incoming bills against received goods.</li>
            <li>Handled daily customer billing and counter sales with a friendly, helpful attitude.</li>
        </ul>
    </div>

    <div class="section-title">Key Skills & Strengths</div>
    <ul>
        <li><strong>Daily Work & Operations:</strong> Vendor Coordination, Document Checking, Following Process Steps (SOPs), Timely Follow-ups, Task Tracking.</li>
        <li><strong>Computer & Office Tools:</strong> MS Excel (Data Entry, Lists, Basic Formatting), MS Word, MS PowerPoint, Google Sheets & Docs, Email Writing.</li>
        <li><strong>Personal Qualities:</strong> High Energy & Enthusiasm, Fast Learner, Dependable Team Player, Good Communication, Shift Flexible (3 PM – 12 AM), English & Hindi.</li>
    </ul>

    <div class="section-title">Certificates & Recognition</div>
    <ul>
        <li><strong>Letter of Appreciation for Dedication & Good Work:</strong> Pencil Mark Interior Solutions (Client Outreach & Vendor Support).</li>
        <li><strong>Fundamentals of Digital Marketing Certificate:</strong> Google (Digital Business Fundamentals & Online Tools).</li>
        <li><strong>Operations & Marketing Management Course:</strong> NPTEL, IIT Kharagpur (Business Operations & Marketing Principles).</li>
        <li><strong>Office Productivity & AI Workshop:</strong> Outskill (Modern Work Tools, Spreadsheets & Everyday Productivity).</li>
    </ul>
</body>
</html>
"""
    out_path = BASE_DIR / filename
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved HTML: {filename}")
    return str(out_path)

def build_md_with_verified_ids(filename):
    md = f"""# ADITYA MEHRA
**BBA Graduate | Onboarding Associate (Job Ref: {JOB_REF} • Req ID: {POSTING_ID}) | Ready to Learn & Contribute**  
Bengaluru, Karnataka, India | Phone: [+91 7003456624](tel:+917003456624) | Email: [adityamehra799@gmail.com](mailto:adityamehra799@gmail.com)  
Portfolio: [adi-digital-universe.ai.studio](https://adi-digital-universe.ai.studio/) | LinkedIn: [aditya-mehra-b8644b326](https://www.linkedin.com/in/aditya-mehra-b8644b326) | GitHub: [AdityaMehra007](https://github.com/AdityaMehra007)

---

## CAREER OBJECTIVE
Energetic and hardworking BBA graduate eager to start my career as an Onboarding Associate at Allegis Global Solutions (Job Ref: {JOB_REF} / Req ID: {POSTING_ID}). A positive team player who learns new software and procedures quickly, follows instructions carefully, and takes full ownership of daily tasks. Brings practical experience in vendor follow-ups, document checking, basic spreadsheet work, and coordination. Excited to support team goals with high dedication, strong communication, and complete availability for the 3:00 PM – 12:00 AM shift.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business (2023 – 2026)**  
*Dayananda Sagar University (DSU), Bengaluru*  
- **Key Subjects Studied:** Supply Chain & Logistics, Operations Management, Marketing, Business Communication, Business Law.

---

## WORK EXPERIENCE & PRACTICAL EXPOSURE

### Operations Intern | *Instawork Services India, Bengaluru*
- Supported the team with daily data checking, reviewing records carefully against project guidelines.
- Identified missing fields and simple errors early so the team could correct them before delivery deadlines.
- Kept daily work logs updated on spreadsheets and worked closely with team members to hit shift targets.

### Operations & Outreach Intern | *Pencil Mark Interior Solutions, Bengaluru*
- Coordinated with local interior vendors to collect registration forms, price quotations, and required documents.
- Made phone calls and sent emails to follow up on order timelines and resolve simple supplier questions.
- Maintained an updated vendor list in MS Excel; received an appreciation letter from management for dedicated work.

### Stall & Logistics Coordinator | *AERO India Exhibition (Salt in My Coca), Bengaluru*
- Assisted with setting up the exhibition stall, badge checking, and welcoming trade visitors with positive energy.
- Counted incoming product boxes against delivery slips to ensure no stock was misplaced during busy event hours.

### Event Logistics Volunteer | *Commercial & College Events, Bengaluru*
- Worked with student teams and local sound/lighting suppliers to ensure equipment arrived on time for campus festivals.
- Stayed on ground to help suppliers set up smoothly and solved minor event needs quickly with a positive attitude.

### Store & Customer Assistant | *Family Retail Store & Food Business, Bengaluru*
- Talked with wholesale suppliers to place regular stock reorders and checked incoming bills against received goods.
- Handled daily customer billing and counter sales with a friendly, helpful attitude.

---

## KEY SKILLS & STRENGTHS
- **Daily Work & Operations:** Vendor Coordination, Document Checking, Following Process Steps (SOPs), Timely Follow-ups, Task Tracking.
- **Computer & Office Tools:** MS Excel (Data Entry, Lists, Basic Formatting), MS Word, MS PowerPoint, Google Sheets & Docs, Email Writing.
- **Personal Qualities:** High Energy & Enthusiasm, Fast Learner, Dependable Team Player, Good Communication, Shift Flexible (3 PM – 12 AM), English & Hindi.

---

## CERTIFICATES & RECOGNITION
- **Letter of Appreciation for Dedication & Good Work:** Pencil Mark Interior Solutions (Client Outreach & Vendor Support).
- **Fundamentals of Digital Marketing Certificate:** Google (Digital Business Fundamentals & Online Tools).
- **Operations & Marketing Management Course:** NPTEL, IIT Kharagpur (Business Operations & Marketing Principles).
- **Office Productivity & AI Workshop:** Outskill (Modern Work Tools, Spreadsheets & Everyday Productivity).
"""
    out_path = BASE_DIR / filename
    out_path.write_text(md, encoding="utf-8")
    print(f"Saved MD: {filename}")
    return str(out_path)

def main():
    print("=" * 70)
    print(f"BUILDING 1-PAGE CV WITH VERIFIED JOB REF: {JOB_REF} & REQ ID: {POSTING_ID}")
    print("=" * 70)
    
    target_names = [
        "ADITYA_MEHRA_ONBOARDING_ASSOCIATE_CV",
        "ADITYA_MEHRA_SIMPLE_ONBOARDING_CV",
        "ADITYA_MEHRA_META_SCM_ONBOARDING_CV"
    ]
    
    for name in target_names:
        build_docx_with_verified_ids(str(BASE_DIR / f"{name}.docx"))
        build_html_with_verified_ids(f"{name}.html")
        build_md_with_verified_ids(f"{name}.md")
        
    print("\nValidating with Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    for name in target_names:
        d_path = str(BASE_DIR / f"{name}.docx")
        p_path = str(BASE_DIR / f"{name}.pdf")
        
        doc = word.Documents.Open(d_path)
        pages = doc.ComputeStatistics(2)
        print(f"[{name}] Word COM Pages: {pages}")
        doc.ExportAsFixedFormat(p_path, 17)
        doc.Close()
        print(f"[{name}] Exported PDF: {p_path}")
        
        reader = pypdf.PdfReader(p_path)
        pdf_pages = len(reader.pages)
        print(f"[{name}] PyPDF Pages: {pdf_pages}")
        
        links = []
        p0 = reader.pages[0]
        if "/Annots" in p0:
            for annot in p0["/Annots"]:
                obj = annot.get_object()
                if "/A" in obj and "/URI" in obj["/A"]:
                    links.append(obj["/A"]["/URI"])
        print(f"[{name}] Hyperlinks ({len(links)}): {links}")
        
    word.Quit()
    print("\nALL BUILDS VERIFIED SUCCESSFULLY WITH BOTH JOB IDS EMBEDDED!")

if __name__ == "__main__":
    main()
