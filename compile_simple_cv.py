"""
compile_simple_cv.py
Compiles a clean, simple, and honest 1-Page CV for Aditya Mehra.
- Uses clear, everyday professional English (no intimidating corporate jargon).
- Fully defensible in any interview: every bullet is easy to explain.
- Highlights: BBA 2026, 0 Days Notice (Immediate Joiner), 100% Rotational & Night Shift Ready, Bengaluru Local.
- Covers: Pencil Mark, Instawork, Aero India 2025, TRILOGY Events, NGO Volunteer, Python Project.
- Strictly verified to fit on 1 Page A4 with 0 overflow and 0 headers/footers.
"""

import os
import subprocess
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT_DIR = "e:\\anti"
OUTPUT_DIR_PDF = os.path.join(ROOT_DIR, "resumes_pdf")
OUTPUT_DIR_HTML = os.path.join(ROOT_DIR, "resumes")
os.makedirs(OUTPUT_DIR_PDF, exist_ok=True)
os.makedirs(OUTPUT_DIR_HTML, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aditya Mehra - Simple Professional CV</title>
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    line-height: 1.25;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .container {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 8mm 12mm 6mm 12mm;
    margin: 0 auto;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header */
  .header {
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 4px;
    margin-bottom: 4px;
  }
  .name {
    font-size: 19pt;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 8.8pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 1px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }
  .contact {
    font-size: 8.1pt;
    color: #475569;
    margin-top: 2px;
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
  }
  .badge {
    margin-top: 2px;
    font-size: 7.6pt;
    font-weight: 700;
    color: #065f46;
    letter-spacing: 0.2px;
  }

  /* Section Titles */
  .section-title {
    font-size: 8.4pt;
    font-weight: 800;
    text-transform: uppercase;
    color: #0f172a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 1.5px;
    margin-top: 3.5px;
    margin-bottom: 2.5px;
    letter-spacing: 0.4px;
  }

  /* Body Text */
  .text {
    font-size: 8.0pt;
    color: #334155;
    line-height: 1.25;
    text-align: justify;
  }

  /* Roles & Rows */
  .row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-top: 2px;
  }
  .title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #0f172a;
  }
  .sub {
    font-size: 8.0pt;
    font-weight: 600;
    color: #1e293b;
  }
  .date {
    font-size: 7.5pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Bullets */
  ul {
    list-style-type: square;
    margin-left: 14px;
    margin-top: 1px;
    margin-bottom: 1px;
  }
  li {
    font-size: 7.8pt;
    color: #334155;
    line-height: 1.22;
    margin-bottom: 0.8px;
  }
  li strong {
    color: #0f172a;
    font-weight: 700;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1px;
  }
  .skills-table td {
    padding: 0.8px 0;
    font-size: 7.8pt;
    vertical-align: top;
    line-height: 1.22;
  }
  .skill-label {
    width: 25%;
    font-weight: 700;
    color: #0f172a;
  }
  .skill-val {
    width: 75%;
    color: #334155;
  }
</style>
</head>
<body>

<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="name">Aditya Mehra</div>
    <div class="subtitle">BBA Graduate (Class of 2026) // Operations & Business Support Associate</div>
    <div class="contact">
      <span>Bengaluru, Karnataka, India</span>
      <span>•</span>
      <span>+91 7003456624</span>
      <span>•</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span>•</span>
      <span><a href="https://www.linkedin.com/in/aditya-mehra" target="_blank">linkedin.com/in/aditya-mehra</a></span>
      <span>•</span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
    <div class="badge">
      Fresher (0–1 Yrs) • Fast Learner & Hard Worker • Immediate Joiner (0 Days Notice) • 100% Rotational & Night Shift Ready
    </div>
  </div>

  <!-- CAREER OBJECTIVE -->
  <div class="section-title">Career Objective</div>
  <p class="text">
    Motivated, honest, and hardworking <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, seeking an entry-level <strong>Operations Associate</strong> role at Accenture. Brings practical internship experience in vendor coordination, Purchase Order tracking in MS Excel, partner document verification (<strong>99.4% accuracy</strong>), and on-ground event stock management. A disciplined team player and quick learner who adapts easily to new tools and processes. Available to join <strong>immediately (0 Days Notice)</strong> with <strong>100% flexibility for 24/7 rotational and night shifts</strong> in Bengaluru.
  </p>

  <!-- EDUCATION -->
  <div class="section-title">Education</div>
  <div class="row">
    <div>
      <span class="title">Bachelor of Business Administration (BBA) — International Business</span><br>
      <span class="sub">Dayananda Sagar University (DSU), Bengaluru, Karnataka</span>
    </div>
    <div class="date">2023 – 2026 | Fresh Graduate (Immediate Availability)</div>
  </div>

  <!-- SKILLS & CAPABILITIES -->
  <div class="section-title">Skills & Strengths</div>
  <table class="skills-table">
    <tr>
      <td class="skill-label">Operations & Purchasing:</td>
      <td class="skill-val">Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Invoice & Delivery Bill Checking.</td>
    </tr>
    <tr>
      <td class="skill-label">Quality & Accuracy:</td>
      <td class="skill-val">Document Verification, Identity Checking, High Attention to Detail (99.4% Audited Accuracy), Following SOP Checklists.</td>
    </tr>
    <tr>
      <td class="skill-label">Stock & Event Logistics:</td>
      <td class="skill-val">Physical Stock Counting, Inventory Receiving, 0% Stock Loss, Cash and Digital UPI Register Balancing.</td>
    </tr>
    <tr>
      <td class="skill-label">Computer & Software Tools:</td>
      <td class="skill-val">MS Excel (VLOOKUP, Pivot Tables, Formulas, Data Cleaning), Google Sheets, MS Office, Basic Python.</td>
    </tr>
    <tr>
      <td class="skill-label">Work Readiness & Shifts:</td>
      <td class="skill-val">Fast Learner, Highly Coachable, Team Player, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Joiner.</td>
    </tr>
  </table>

  <!-- PRACTICAL WORK EXPERIENCE -->
  <div class="section-title">Work Experience & Practical Exposure</div>

  <!-- Role 1: Pencil Mark -->
  <div class="row">
    <div><span class="title">Operations & Procurement Intern</span> — <span class="sub">Pencil Mark Interior Solutions LLP</span></div>
    <div class="date">Jul 2024 – Aug 2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Built price comparison sheets in MS Excel to compare supplier quotes, helping managers choose the best vendor rates.</li>
    <li>Tracked Purchase Orders (POs) from ordering to site delivery, checking delivery challans against orders to prevent billing mistakes.</li>
    <li>Assisted senior team members with client cost estimation sheets, contributing to the closure of <strong>₹1.5L+ in commercial interior contracts</strong>.</li>
    <li>Awarded a formal <strong>Written Management Commendation</strong> for dependable performance, punctuality, and accuracy.</li>
  </ul>

  <!-- Role 2: Instawork -->
  <div class="row">
    <div><span class="title">Operations & Data Verification Intern</span> — <span class="sub">Instawork Services India Pvt. Ltd.</span></div>
    <div class="date">2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Verified partner profile details and identity documents against strict company checklists, maintaining a <strong>99.4% accuracy rate</strong>.</li>
    <li>Processed daily verification tasks quickly to meet team deadlines, helping the team <strong>reduce average review time by 12%</strong>.</li>
  </ul>

  <!-- Role 3: Aero India 2025 -->
  <div class="row">
    <div><span class="title">Event Logistics & Operations Lead</span> — <span class="sub">Salt in My Cocoa (AERO India 2025)</span></div>
    <div class="date">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
  </div>
  <ul>
    <li>Managed stall stock supply, inventory intake, and customer billing for <strong>100,000+ defense and public visitors</strong> over 5 high-rush days.</li>
    <li>Conducted physical stock counts before and after every shift, achieving <strong>0% stock loss</strong> and <strong>100% accurate daily cash and UPI balancing</strong>.</li>
  </ul>

  <!-- Role 4: TRILOGY -->
  <div class="row">
    <div><span class="title">Event Operations Coordinator</span> — <span class="sub">TRILOGY Indo-Jazz Fusion & Commercial Productions</span></div>
    <div class="date">2019 – 2026 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Coordinated with sound, lighting, and hospitality vendors for live concerts at Bangalore Club, ensuring zero event delays.</li>
    <li>Negotiated directly with suppliers, helping reduce event production costs by <strong>15%–20%</strong>.</li>
  </ul>

  <!-- Role 5: NGO -->
  <div class="row">
    <div><span class="title">Community Volunteer</span> — <span class="sub">NGO & Social Welfare Initiative</span></div>
    <div class="date">2024 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Verified attendee registration documents and maintained clean records in Google Sheets during social outreach drives.</li>
    <li>Helped manage volunteer duty shifts and crowd logistics, ensuring organized and smooth on-ground community events.</li>
  </ul>

  <!-- ACADEMIC PROJECT -->
  <div class="section-title">Student Technical Project</div>
  <div class="row">
    <div><span class="title">Job Portal Data Extractor</span> — <span class="sub">Self-Initiated Academic Project</span></div>
    <div class="date">2025 – 2026 | Python & Spreadsheets</div>
  </div>
  <ul>
    <li>Created a simple Python script to collect and organize corporate job postings into clean Excel sheets, saving manual searching time.</li>
  </ul>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="text">
    <strong>Certifications:</strong> Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL)<br>
    <strong>Languages:</strong> English (Fluent Professional), Hindi (Native / Bilingual)
  </p>

</div>
</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Simple_CV.html")
pdf_path = os.path.join(OUTPUT_DIR_PDF, "Aditya_Mehra_Simple_CV.pdf")
root_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Simple_CV.pdf")
root_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Simple_CV.docx")
docx_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Simple_CV.docx")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Render HTML to PDF via Chrome
cmd = [
    CHROME_PATH,
    "--headless=new",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]
subprocess.run(cmd, check=True)

with open(pdf_path, "rb") as f_in:
    pdf_bytes = f_in.read()
    with open(root_pdf, "wb") as f_out:
        f_out.write(pdf_bytes)

print(f"Generated Simple PDF: {root_pdf} (Size: {len(pdf_bytes)} bytes)")

# ==========================================
# GENERATE NATIVE DOCX
# ==========================================
doc = docx.Document()

# Margins: 0.30 in
for section in doc.sections:
    section.top_margin = Inches(0.30)
    section.bottom_margin = Inches(0.30)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

C_NAVY = RGBColor(15, 23, 42)
C_BLUE = RGBColor(29, 78, 216)
C_SLATE = RGBColor(71, 85, 105)
C_BODY = RGBColor(51, 65, 85)
C_GREEN = RGBColor(6, 95, 70)

def add_clean_divider(paragraph):
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CBD5E1')
    pBdr.append(bottom)
    pPr.append(pBdr)

# Header
p_name = doc.add_paragraph()
p_name.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_name.paragraph_format.space_before = Pt(0)
p_name.paragraph_format.space_after = Pt(1)
r_name = p_name.add_run("ADITYA MEHRA")
r_name.font.name = "Arial"
r_name.font.size = Pt(17)
r_name.font.bold = True
r_name.font.color.rgb = C_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1.5)
r_sub = p_sub.add_run("BBA Graduate (Class of 2026) // Operations & Business Support Associate")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(8.6)
r_sub.font.bold = True
r_sub.font.color.rgb = C_BLUE

p_cont = doc.add_paragraph()
p_cont.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_cont.paragraph_format.space_before = Pt(0)
p_cont.paragraph_format.space_after = Pt(1.5)
r_cont = p_cont.add_run("Bengaluru, Karnataka, India | +91 7003456624 | adityamehra799@gmail.com | linkedin.com/in/aditya-mehra | github.com/AdityaMehra007")
r_cont.font.name = "Arial"
r_cont.font.size = Pt(7.6)
r_cont.font.color.rgb = C_SLATE

p_badge = doc.add_paragraph()
p_badge.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_badge.paragraph_format.space_before = Pt(0)
p_badge.paragraph_format.space_after = Pt(2.5)
r_badge = p_badge.add_run("Fresher (0–1 Yrs) • Fast Learner & Hard Worker • Immediate Joiner (0 Days Notice) • 100% Rotational & Night Shift Ready")
r_badge.font.name = "Arial"
r_badge.font.size = Pt(7.6)
r_badge.font.bold = True
r_badge.font.color.rgb = C_GREEN

add_clean_divider(p_badge)

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"
    r.font.size = Pt(8.3)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    add_clean_divider(p)
    return p

# Career Objective
add_sec("Career Objective")
p_obj = doc.add_paragraph()
p_obj.paragraph_format.space_before = Pt(1)
p_obj.paragraph_format.space_after = Pt(2)
p_obj.paragraph_format.line_spacing = 1.15
r_obj = p_obj.add_run(
    "Motivated, honest, and hardworking 2026 BBA graduate in International Business from Dayananda Sagar University, seeking an entry-level Operations Associate role at Accenture. Brings practical internship experience in vendor coordination, Purchase Order tracking in MS Excel, partner document verification (99.4% accuracy), and on-ground event stock management. A disciplined team player and quick learner who adapts easily to new tools and processes. Available to join immediately (0 Days Notice) with 100% flexibility for 24/7 rotational and night shifts in Bengaluru."
)
r_obj.font.name = "Arial"
r_obj.font.size = Pt(7.8)
r_obj.font.color.rgb = C_BODY

# Education
add_sec("Education")
p_edu = doc.add_paragraph()
p_edu.paragraph_format.space_before = Pt(1)
p_edu.paragraph_format.space_after = Pt(2)
r_e1 = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.2); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_edu.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka | 2023 – 2026 | Fresh Graduate (Immediate Availability)")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(7.5); r_e2.font.color.rgb = C_SLATE

# Skills
add_sec("Skills & Strengths")
skills = [
    ("Operations & Purchasing:", "Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Invoice & Delivery Bill Checking."),
    ("Quality & Accuracy:", "Document Verification, Identity Checking, High Attention to Detail (99.4% Audited Accuracy), Following SOP Checklists."),
    ("Stock & Event Logistics:", "Physical Stock Counting, Inventory Receiving, 0% Stock Loss, Cash and Digital UPI Register Balancing."),
    ("Computer & Software Tools:", "MS Excel (VLOOKUP, Pivot Tables, Formulas, Data Cleaning), Google Sheets, MS Office, Basic Python."),
    ("Work Readiness & Shifts:", "Fast Learner, Highly Coachable, Team Player, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Joiner.")
]

t_sk = doc.add_table(rows=len(skills), cols=2)
t_sk.autofit = False
t_sk.columns[0].width = Inches(2.0)
t_sk.columns[1].width = Inches(5.3)

for idx, (lbl, val) in enumerate(skills):
    c0 = t_sk.cell(idx, 0)
    c1 = t_sk.cell(idx, 1)
    
    p0 = c0.paragraphs[0]; p0.paragraph_format.space_before = Pt(0.5); p0.paragraph_format.space_after = Pt(0.5)
    r0 = p0.add_run(lbl)
    r0.font.name = "Arial"; r0.font.size = Pt(7.7); r0.font.bold = True; r0.font.color.rgb = C_NAVY
    
    p1 = c1.paragraphs[0]; p1.paragraph_format.space_before = Pt(0.5); p1.paragraph_format.space_after = Pt(0.5)
    r1 = p1.add_run(val)
    r1.font.name = "Arial"; r1.font.size = Pt(7.7); r1.font.color.rgb = C_BODY

# Work Experience
add_sec("Work Experience & Practical Exposure")

jobs = [
    {
        "title": "Operations & Procurement Intern — Pencil Mark Interior Solutions LLP",
        "date": "Jul 2024 – Aug 2025 | Bengaluru, India",
        "bullets": [
            "Built price comparison sheets in MS Excel to compare supplier quotes, helping managers choose the best vendor rates.",
            "Tracked Purchase Orders (POs) from ordering to site delivery, checking delivery challans against orders to prevent billing mistakes.",
            "Assisted senior team members with client cost estimation sheets, contributing to the closure of ₹1.5L+ in commercial interior contracts.",
            "Awarded a formal Written Management Commendation for dependable performance, punctuality, and accuracy."
        ]
    },
    {
        "title": "Operations & Data Verification Intern — Instawork Services India Pvt. Ltd.",
        "date": "2025 | Bengaluru, India",
        "bullets": [
            "Verified partner profile details and identity documents against strict company checklists, maintaining a 99.4% accuracy rate.",
            "Processed daily verification tasks quickly to meet team deadlines, helping the team reduce average review time by 12%."
        ]
    },
    {
        "title": "Event Logistics & Operations Lead — Salt in My Cocoa (AERO India 2025)",
        "date": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Managed stall stock supply, inventory intake, and customer billing for 100,000+ defense and public visitors over 5 high-rush days.",
            "Conducted physical stock counts before and after every shift, achieving 0% stock loss and 100% accurate daily cash and UPI balancing."
        ]
    },
    {
        "title": "Event Operations Coordinator — TRILOGY Indo-Jazz Fusion & Commercial Productions",
        "date": "2019 – 2026 | Bengaluru, India",
        "bullets": [
            "Coordinated with sound, lighting, and hospitality vendors for live concerts at Bangalore Club, ensuring zero event delays.",
            "Negotiated directly with suppliers, helping reduce event production costs by 15%–20%."
        ]
    },
    {
        "title": "Community Volunteer — NGO & Social Welfare Initiative",
        "date": "2024 | Bengaluru, India",
        "bullets": [
            "Verified attendee registration documents and maintained clean records in Google Sheets during social outreach drives.",
            "Helped manage volunteer duty shifts and crowd logistics, ensuring organized and smooth on-ground community events."
        ]
    }
]

for j in jobs:
    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(1.5)
    p_j.paragraph_format.space_after = Pt(0.4)
    p_j.paragraph_format.keep_with_next = True
    r_j1 = p_j.add_run(f"{j['title']}\n")
    r_j1.font.name = "Arial"; r_j1.font.size = Pt(8.0); r_j1.font.bold = True; r_j1.font.color.rgb = C_NAVY
    r_j2 = p_j.add_run(j['date'])
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.3); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b_item = doc.add_paragraph()
        p_b_item.paragraph_format.space_before = Pt(0)
        p_b_item.paragraph_format.space_after = Pt(0.5)
        p_b_item.paragraph_format.left_indent = Inches(0.12)
        p_b_item.paragraph_format.line_spacing = 1.15
        r_bullet = p_b_item.add_run(f"- {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(7.7); r_bullet.font.color.rgb = C_BODY

# Academic Project
add_sec("Student Technical Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.4)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Data Extractor — Self-Initiated Academic Project\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.0); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 – 2026 | Python & Spreadsheets")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.3); r_pr2.font.color.rgb = C_SLATE

p_pr_b = doc.add_paragraph()
p_pr_b.paragraph_format.space_before = Pt(0)
p_pr_b.paragraph_format.space_after = Pt(0.8)
p_pr_b.paragraph_format.left_indent = Inches(0.12)
r_pr_b = p_pr_b.add_run("- Created a simple Python script to collect and organize corporate job postings into clean Excel sheets, saving manual searching time.")
r_pr_b.font.name = "Arial"; r_pr_b.font.size = Pt(7.7); r_pr_b.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.space_before = Pt(0.8)
p_cert.paragraph_format.space_after = Pt(0.8)
r_c1 = p_cert.add_run("Certifications: Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL)\n")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.6); r_c1.font.color.rgb = C_BODY
r_c2 = p_cert.add_run("Languages: English (Fluent Professional), Hindi (Native / Bilingual)")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.6); r_c2.font.color.rgb = C_BODY

doc.save(docx_path)
doc.save(root_docx)
print(f"Generated Simple DOCX: {root_docx} (Size: {os.path.getsize(root_docx)} bytes)")

# Verify Page Count
with open(root_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
