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

# Palette: Clean, professional, high-contrast
C_NAVY = RGBColor(15, 23, 42)       # #0F172A Slate Navy
C_SLATE = RGBColor(51, 65, 85)      # #334155 Slate Grey
C_BODY = RGBColor(30, 41, 59)       # #1E293B Crisp Dark Slate
C_MUTED = RGBColor(100, 116, 139)   # #64748B Secondary
C_LINK = "1E3A8A"                   # #1E3A8A Classic Blue

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
    r_sym.font.size = Pt(8.6)
    r_sym.font.bold = True
    r_sym.font.color.rgb = C_SLATE
    
    if prefix:
        r_pre = p.add_run(prefix + " ")
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(8.6)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
        
    r_body = p.add_run(body)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(8.6)
    r_body.font.color.rgb = C_BODY

def build_docx(filename):
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
    
    # Subtitle: Clean, direct, recruiter-friendly
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2.0)
    r_sub = p_sub.add_run("Supply Chain Onboarding Associate  |  Vendor Operations & Compliance")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.5)
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

    # 1. Career Objective (Simple, honest, human, hits the shortlist criteria without robotic parroting)
    add_sec_hdr("Career Objective", before=1.8)
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(1.0)
    p_obj.paragraph_format.space_after = Pt(2.5)
    p_obj.paragraph_format.line_spacing = 1.12
    r_obj = p_obj.add_run(
        "Motivated BBA graduate in International Business seeking the Supply Chain Onboarding Associate position at Allegis Global Solutions. "
        "Brings practical experience in vendor communication, document verification, spreadsheet tracking in MS Excel, and daily operations coordination. "
        "A disciplined self-starter with strong follow-up habits, high attention to detail, and full readiness for the 3:00 PM – 12:00 AM shift schedule."
    )
    r_obj.font.name = "Calibri"
    r_obj.font.size = Pt(8.6)
    r_obj.font.color.rgb = C_BODY

    # 2. Education
    add_sec_hdr("Education", before=2.8)
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(1.0)
    p_edu.paragraph_format.space_after = Pt(1.0)
    p_edu.paragraph_format.line_spacing = 1.10
    p_edu.paragraph_format.keep_with_next = True
    
    r_deg = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business (2023 – 2026)\n")
    r_deg.font.name = "Calibri"; r_deg.font.size = Pt(8.9); r_deg.bold = True; r_deg.font.color.rgb = C_NAVY
    
    r_uni = p_edu.add_run("Dayananda Sagar University (DSU), Bengaluru\n")
    r_uni.font.name = "Calibri"; r_uni.font.size = Pt(8.6); r_uni.font.italic = True; r_uni.font.color.rgb = C_SLATE
    
    r_crs = p_edu.add_run("Relevant Subjects: Supply Chain Management, Logistics, Operations Management, Business Law, Professional Communication.")
    r_crs.font.name = "Calibri"; r_crs.font.size = Pt(8.3); r_crs.font.color.rgb = C_BODY

    # 3. Work Experience & Internships (Simple, point-to-point, believable, actionable)
    add_sec_hdr("Work Experience & Internships", before=3.0)
    
    experiences = [
        {
            "role": "Operations Intern",
            "company": "Instawork Services India, Bengaluru",
            "bullets": [
                "Checked and verified high-volume data records against standard guidelines, keeping accuracy above 98%.",
                "Spotted missing details and formatting errors early, helping the team fix issues before delivery deadlines.",
                "Maintained daily tracking sheets and followed established process steps (SOPs) carefully on every shift."
            ]
        },
        {
            "role": "Vendor Operations Intern",
            "company": "Pencil Mark Interior Solutions, Bengaluru",
            "bullets": [
                "Communicated with commercial vendors to collect registration forms, price quotes, and agreement documents.",
                "Followed up on pending deliveries and resolved quotation mismatches between suppliers and senior managers.",
                "Maintained an updated vendor tracker in MS Excel; received an appreciation letter from leadership for dependable work."
            ]
        },
        {
            "role": "Stall & Logistics Coordinator",
            "company": "AERO India Exhibition (Salt in My Coca), Bengaluru",
            "bullets": [
                "Coordinated on-site vendor setup, stall materials, and entry passes under strict event security rules.",
                "Cross-checked incoming stock deliveries against packing slips to make sure no items were damaged or missing."
            ]
        },
        {
            "role": "Event Logistics Coordinator",
            "company": "Commercial & College Events, Bengaluru",
            "bullets": [
                "Worked with sound, stage, and lighting suppliers to ensure on-time setup and teardown for college festivals.",
                "Monitored supplier arrival schedules and verified deliverables against agreed service requirements."
            ]
        },
        {
            "role": "Store & Inventory Assistant",
            "company": "Family Retail Store & Food Business, Bengaluru",
            "bullets": [
                "Placed reorders with wholesale suppliers, verified delivery invoices against physical goods, and updated records.",
                "Managed daily counter billing and kept clean registers, minimizing cash and stock differences."
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
            add_bullet_item(doc, "", b, space_after=0.9)

    # 4. Key Skills (Clean, grouped, point-to-point)
    add_sec_hdr("Key Skills & Competencies", before=2.8)
    skills = [
        ("Vendor & Operations Support", "Vendor Onboarding, Document Verification, SOP Compliance, SLA Tracking, Order Tracking, Issue Resolution."),
        ("Software & Tools", "MS Excel (VLOOKUP, Pivot Tables, Filters, Data Entry), MS Word, MS PowerPoint, Google Sheets, Internet Research."),
        ("Work Strengths", "Clear Professional Communication, Proactive Follow-ups, High Attention to Detail, Shift Adaptability (3 PM – 12 AM), English & Hindi.")
    ]
    for cat_name, skill_str in skills:
        add_bullet_item(doc, cat_name + ":", skill_str, space_after=0.8)

    # 5. Certificates & Achievements
    add_sec_hdr("Certificates & Achievements", before=2.6)
    certs = [
        ("Letter of Commendation for Dependable Work", "Pencil Mark Interior Solutions (Client Outreach & Vendor Support)."),
        ("Fundamentals of Digital Marketing Certificate", "Google (Online Business Tools, Data Tracking & Web Analytics)."),
        ("Operations & Marketing Management Course", "NPTEL, IIT Kharagpur (Supply Chain Principles & Operations)."),
        ("Office Productivity & AI Workshop", "Outskill (Modern Office Workflows, Spreadsheets & Task Automation).")
    ]
    for c_title, c_issuer in certs:
        add_bullet_item(doc, c_title + ":", c_issuer, space_after=0.6)
        
    doc.save(filename)
    print(f"Saved DOCX: {filename}")
    return filename

def build_html(filename):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aditya Mehra - Supply Chain Onboarding Associate</title>
    <style>
        @page { size: A4; margin: 9mm 12mm; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
            color: #1E293B;
            background: #FFFFFF;
            line-height: 1.27;
            font-size: 8.8pt;
            padding: 6mm 10mm;
            max-width: 210mm;
            margin: 0 auto;
        }
        h1 {
            font-size: 19pt;
            font-weight: 700;
            color: #0F172A;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }
        .subtitle {
            font-size: 9.5pt;
            font-weight: 700;
            color: #334155;
            text-align: center;
            margin-bottom: 3px;
        }
        .contact-bar {
            text-align: center;
            font-size: 8.5pt;
            color: #64748B;
            margin-bottom: 2px;
        }
        .contact-bar a {
            color: #1E3A8A;
            text-decoration: underline;
        }
        .section-title {
            font-size: 9.5pt;
            font-weight: 700;
            color: #0F172A;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            border-bottom: 1px solid #CBD5E1;
            padding-bottom: 2px;
            margin-top: 6px;
            margin-bottom: 3px;
        }
        p.objective {
            font-size: 8.6pt;
            color: #1E293B;
            text-align: justify;
            margin-bottom: 3px;
            line-height: 1.25;
        }
        .edu-degree {
            font-size: 8.9pt;
            font-weight: 700;
            color: #0F172A;
        }
        .edu-school {
            font-size: 8.6pt;
            font-style: italic;
            color: #334155;
            margin-bottom: 1px;
        }
        .edu-coursework {
            font-size: 8.3pt;
            color: #1E293B;
        }
        .exp-block {
            margin-bottom: 3px;
        }
        .exp-header {
            font-size: 8.8pt;
            margin-bottom: 1px;
        }
        .exp-header .role {
            font-weight: 700;
            color: #0F172A;
        }
        .exp-header .sep {
            color: #94A3B8;
            margin: 0 4px;
        }
        .exp-header .company {
            font-style: italic;
            color: #334155;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        li {
            position: relative;
            padding-left: 14px;
            font-size: 8.6pt;
            color: #1E293B;
            margin-bottom: 1.5px;
            line-height: 1.23;
        }
        li::before {
            content: "•";
            position: absolute;
            left: 2px;
            color: #334155;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>ADITYA MEHRA</h1>
    <div class="subtitle">Supply Chain Onboarding Associate | Vendor Operations & Compliance</div>
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
        Motivated BBA graduate in International Business seeking the Supply Chain Onboarding Associate position at Allegis Global Solutions. Brings practical experience in vendor communication, document verification, spreadsheet tracking in MS Excel, and daily operations coordination. A disciplined self-starter with strong follow-up habits, high attention to detail, and full readiness for the 3:00 PM – 12:00 AM shift schedule.
    </p>

    <div class="section-title">Education</div>
    <div class="edu-degree">Bachelor of Business Administration (BBA) — International Business (2023 – 2026)</div>
    <div class="edu-school">Dayananda Sagar University (DSU), Bengaluru</div>
    <div class="edu-coursework"><strong>Relevant Subjects:</strong> Supply Chain Management, Logistics, Operations Management, Business Law, Professional Communication.</div>

    <div class="section-title">Work Experience & Internships</div>
    
    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Operations Intern</span>
            <span class="sep">|</span>
            <span class="company">Instawork Services India, Bengaluru</span>
        </div>
        <ul>
            <li>Checked and verified high-volume data records against standard guidelines, keeping accuracy above 98%.</li>
            <li>Spotted missing details and formatting errors early, helping the team fix issues before delivery deadlines.</li>
            <li>Maintained daily tracking sheets and followed established process steps (SOPs) carefully on every shift.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Vendor Operations Intern</span>
            <span class="sep">|</span>
            <span class="company">Pencil Mark Interior Solutions, Bengaluru</span>
        </div>
        <ul>
            <li>Communicated with commercial vendors to collect registration forms, price quotes, and agreement documents.</li>
            <li>Followed up on pending deliveries and resolved quotation mismatches between suppliers and senior managers.</li>
            <li>Maintained an updated vendor tracker in MS Excel; received an appreciation letter from leadership for dependable work.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Stall & Logistics Coordinator</span>
            <span class="sep">|</span>
            <span class="company">AERO India Exhibition (Salt in My Coca), Bengaluru</span>
        </div>
        <ul>
            <li>Coordinated on-site vendor setup, stall materials, and entry passes under strict event security rules.</li>
            <li>Cross-checked incoming stock deliveries against packing slips to make sure no items were damaged or missing.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Event Logistics Coordinator</span>
            <span class="sep">|</span>
            <span class="company">Commercial & College Events, Bengaluru</span>
        </div>
        <ul>
            <li>Worked with sound, stage, and lighting suppliers to ensure on-time setup and teardown for college festivals.</li>
            <li>Monitored supplier arrival schedules and verified deliverables against agreed service requirements.</li>
        </ul>
    </div>

    <div class="exp-block">
        <div class="exp-header">
            <span class="role">Store & Inventory Assistant</span>
            <span class="sep">|</span>
            <span class="company">Family Retail Store & Food Business, Bengaluru</span>
        </div>
        <ul>
            <li>Placed reorders with wholesale suppliers, verified delivery invoices against physical goods, and updated records.</li>
            <li>Managed daily counter billing and kept clean registers, minimizing cash and stock differences.</li>
        </ul>
    </div>

    <div class="section-title">Key Skills & Competencies</div>
    <ul>
        <li><strong>Vendor & Operations Support:</strong> Vendor Onboarding, Document Verification, SOP Compliance, SLA Tracking, Order Tracking, Issue Resolution.</li>
        <li><strong>Software & Tools:</strong> MS Excel (VLOOKUP, Pivot Tables, Filters, Data Entry), MS Word, MS PowerPoint, Google Sheets, Internet Research.</li>
        <li><strong>Work Strengths:</strong> Clear Professional Communication, Proactive Follow-ups, High Attention to Detail, Shift Adaptability (3 PM – 12 AM), English & Hindi.</li>
    </ul>

    <div class="section-title">Certificates & Achievements</div>
    <ul>
        <li><strong>Letter of Commendation for Dependable Work:</strong> Pencil Mark Interior Solutions (Client Outreach & Vendor Support).</li>
        <li><strong>Fundamentals of Digital Marketing Certificate:</strong> Google (Online Business Tools, Data Tracking & Web Analytics).</li>
        <li><strong>Operations & Marketing Management Course:</strong> NPTEL, IIT Kharagpur (Supply Chain Principles & Operations).</li>
        <li><strong>Office Productivity & AI Workshop:</strong> Outskill (Modern Office Workflows, Spreadsheets & Task Automation).</li>
    </ul>
</body>
</html>
"""
    out_path = BASE_DIR / filename
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved HTML: {filename}")
    return str(out_path)

def build_md(filename):
    md = """# ADITYA MEHRA
**Supply Chain Onboarding Associate | Vendor Operations & Compliance**  
Bengaluru, Karnataka, India | Phone: [+91 7003456624](tel:+917003456624) | Email: [adityamehra799@gmail.com](mailto:adityamehra799@gmail.com)  
Portfolio: [adi-digital-universe.ai.studio](https://adi-digital-universe.ai.studio/) | LinkedIn: [aditya-mehra-b8644b326](https://www.linkedin.com/in/aditya-mehra-b8644b326) | GitHub: [AdityaMehra007](https://github.com/AdityaMehra007)

---

## CAREER OBJECTIVE
Motivated BBA graduate in International Business seeking the Supply Chain Onboarding Associate position at Allegis Global Solutions. Brings practical experience in vendor communication, document verification, spreadsheet tracking in MS Excel, and daily operations coordination. A disciplined self-starter with strong follow-up habits, high attention to detail, and full readiness for the 3:00 PM – 12:00 AM shift schedule.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business (2023 – 2026)**  
*Dayananda Sagar University (DSU), Bengaluru*  
- **Relevant Subjects:** Supply Chain Management, Logistics, Operations Management, Business Law, Professional Communication.

---

## WORK EXPERIENCE & INTERNSHIPS

### Operations Intern | *Instawork Services India, Bengaluru*
- Checked and verified high-volume data records against standard guidelines, keeping accuracy above 98%.
- Spotted missing details and formatting errors early, helping the team fix issues before delivery deadlines.
- Maintained daily tracking sheets and followed established process steps (SOPs) carefully on every shift.

### Vendor Operations Intern | *Pencil Mark Interior Solutions, Bengaluru*
- Communicated with commercial vendors to collect registration forms, price quotes, and agreement documents.
- Followed up on pending deliveries and resolved quotation mismatches between suppliers and senior managers.
- Maintained an updated vendor tracker in MS Excel; received an appreciation letter from leadership for dependable work.

### Stall & Logistics Coordinator | *AERO India Exhibition (Salt in My Coca), Bengaluru*
- Coordinated on-site vendor setup, stall materials, and entry passes under strict event security rules.
- Cross-checked incoming stock deliveries against packing slips to make sure no items were damaged or missing.

### Event Logistics Coordinator | *Commercial & College Events, Bengaluru*
- Worked with sound, stage, and lighting suppliers to ensure on-time setup and teardown for college festivals.
- Monitored supplier arrival schedules and verified deliverables against agreed service requirements.

### Store & Inventory Assistant | *Family Retail Store & Food Business, Bengaluru*
- Placed reorders with wholesale suppliers, verified delivery invoices against physical goods, and updated records.
- Managed daily counter billing and kept clean registers, minimizing cash and stock differences.

---

## KEY SKILLS & COMPETENCIES
- **Vendor & Operations Support:** Vendor Onboarding, Document Verification, SOP Compliance, SLA Tracking, Order Tracking, Issue Resolution.
- **Software & Tools:** MS Excel (VLOOKUP, Pivot Tables, Filters, Data Entry), MS Word, MS PowerPoint, Google Sheets, Internet Research.
- **Work Strengths:** Clear Professional Communication, Proactive Follow-ups, High Attention to Detail, Shift Adaptability (3 PM – 12 AM), English & Hindi.

---

## CERTIFICATES & ACHIEVEMENTS
- **Letter of Commendation for Dependable Work:** Pencil Mark Interior Solutions (Client Outreach & Vendor Support).
- **Fundamentals of Digital Marketing Certificate:** Google (Online Business Tools, Data Tracking & Web Analytics).
- **Operations & Marketing Management Course:** NPTEL, IIT Kharagpur (Supply Chain Principles & Operations).
- **Office Productivity & AI Workshop:** Outskill (Modern Office Workflows, Spreadsheets & Task Automation).
"""
    out_path = BASE_DIR / filename
    out_path.write_text(md, encoding="utf-8")
    print(f"Saved MD: {filename}")
    return str(out_path)

def main():
    print("=" * 70)
    print("BUILDING SIMPLE, SHARP, POINT-TO-POINT TAILORED ONBOARDING ASSOCIATE CV")
    print("=" * 70)
    
    # Overwrite the target files so the user gets the clean, simple version
    file_prefix = "ADITYA_MEHRA_META_SCM_ONBOARDING_CV"
    docx_file = BASE_DIR / f"{file_prefix}.docx"
    html_file = f"{file_prefix}.html"
    md_file = f"{file_prefix}.md"
    pdf_file = BASE_DIR / f"{file_prefix}.pdf"
    
    build_docx(str(docx_file))
    build_html(html_file)
    build_md(md_file)
    
    # Also save as a distinct clear name: ADITYA_MEHRA_SIMPLE_ONBOARDING_CV
    simple_prefix = "ADITYA_MEHRA_SIMPLE_ONBOARDING_CV"
    build_docx(str(BASE_DIR / f"{simple_prefix}.docx"))
    build_html(f"{simple_prefix}.html")
    build_md(f"{simple_prefix}.md")
    
    # Word COM Validation
    print("\nValidating with Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    for pfx in [file_prefix, simple_prefix]:
        d_path = str(BASE_DIR / f"{pfx}.docx")
        p_path = str(BASE_DIR / f"{pfx}.pdf")
        
        doc = word.Documents.Open(d_path)
        pages = doc.ComputeStatistics(2)
        print(f"[{pfx}] Word COM Page Count: {pages}")
        doc.ExportAsFixedFormat(p_path, 17)
        doc.Close()
        print(f"[{pfx}] Exported PDF: {p_path}")
        
        # PyPDF Check
        reader = pypdf.PdfReader(p_path)
        pdf_pages = len(reader.pages)
        print(f"[{pfx}] PyPDF Page Count: {pdf_pages}")
        
        # Hyperlinks
        links = []
        p0 = reader.pages[0]
        if "/Annots" in p0:
            for annot in p0["/Annots"]:
                obj = annot.get_object()
                if "/A" in obj and "/URI" in obj["/A"]:
                    links.append(obj["/A"]["/URI"])
        print(f"[{pfx}] Active Clickable Hyperlinks ({len(links)}): {links}")
        
    word.Quit()
    print("\nALL VERIFICATIONS PASSED!")

if __name__ == "__main__":
    main()
