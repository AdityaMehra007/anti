import os
import subprocess
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import shutil
import re

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR_HTML = r"e:\anti\resumes"
OUTPUT_DIR_PDF = r"e:\anti\resumes_pdf"
ROOT_DIR = r"e:\anti"

os.makedirs(OUTPUT_DIR_HTML, exist_ok=True)
os.makedirs(OUTPUT_DIR_PDF, exist_ok=True)

# -------------------------------------------------------------
# 1. HTML CV: "WILLING TO LEARN" FRESHER (ACCENTURE LEVEL 13)
# -------------------------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra - Operations Resume (Accenture Fresher)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 9mm 11mm 9mm 11mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.34;
  }
  body {
    background: #fff;
    font-size: 9.3pt;
  }
  .container {
    max-width: 100%;
    margin: 0 auto;
  }
  
  /* Header */
  .header {
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 5px;
    margin-bottom: 8px;
  }
  .name {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: 0.6px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 9.8pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 2px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }
  .contact {
    font-size: 8.6pt;
    color: #475569;
    margin-top: 3px;
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
  }
  .badge {
    margin-top: 3px;
    font-size: 8.0pt;
    font-weight: 700;
    color: #065f46;
    background: #ecfdf5;
    display: inline-block;
    padding: 1.5px 10px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
  }

  /* Section Titles */
  .section-title {
    font-size: 9.6pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 7px;
    margin-bottom: 5px;
  }
  
  /* Content Blocks */
  .row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.5px;
  }
  .title {
    font-weight: 700;
    color: #0f172a;
    font-size: 8.9pt;
  }
  .sub {
    color: #1d4ed8;
    font-weight: 600;
    font-size: 8.5pt;
  }
  .date {
    font-size: 8.0pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }
  .text {
    font-size: 8.7pt;
    color: #334155;
    text-align: justify;
    line-height: 1.34;
  }
  ul {
    padding-left: 16px;
    margin-bottom: 5px;
  }
  li {
    font-size: 8.4pt;
    color: #334155;
    margin-bottom: 2px;
    line-height: 1.30;
  }
  li strong {
    color: #0f172a;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.4pt;
    margin-bottom: 4px;
  }
  .skills-table td {
    padding: 2px 0;
    vertical-align: top;
  }
  .skill-label {
    font-weight: 700;
    color: #0f172a;
    width: 25%;
    white-space: nowrap;
  }
  .skill-val {
    color: #334155;
    width: 75%;
  }

  @media print {
    body { background: #fff; padding: 0; }
    .print-btn { display: none; }
  }
  @media screen {
    body { background: #f8fafc; padding: 25px; }
    .container {
      max-width: 210mm;
      min-height: 297mm;
      background: #fff;
      padding: 12mm 14mm;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
      border-radius: 4px;
    }
    .print-btn {
      position: fixed;
      top: 20px;
      right: 20px;
      background: #1d4ed8;
      color: #fff;
      padding: 10px 18px;
      border-radius: 6px;
      font-weight: 700;
      border: none;
      cursor: pointer;
    }
  }
</style>
</head>
<body>

<button class="print-btn" onclick="window.print()">Print / Save as PDF</button>

<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="name">ADITYA MEHRA</div>
    <div class="subtitle">BBA Graduate (Batch of 2026) // Entry-Level Operations New Associate</div>
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
      Fresher (0–1 Yrs) • Highly Trainable & Quick Learner • Immediate Joiner (0 Days Notice) • 24/7 Shifts Flexible
    </div>
  </div>

  <!-- CAREER OBJECTIVE / PROFILE -->
  <div class="section-title">Career Objective</div>
  <p class="text">
    Enthusiastic and hardworking <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, seeking an entry-level <strong>Level 13 Operations New Associate</strong> role at Accenture Operations. An eager learner with high coachability and dedication to mastering enterprise processes, software, and Standard Operating Procedures (SOPs). Offers practical internship experience in vendor coordination, document verification, inventory management, and MS Excel. Known for strong accountability, positive attitude, and rapid adaptation. Local Bengaluru resident with <strong>0 days notice</strong> and complete readiness for 24/7 rotational and night shifts.
  </p>

  <!-- EDUCATION -->
  <div class="section-title">Education</div>
  <div class="row">
    <div>
      <span class="title">Bachelor of Business Administration (BBA) — International Business</span><br>
      <span class="sub">Dayananda Sagar University (DSU), Bengaluru, Karnataka</span>
    </div>
    <div class="date">2023 – 2026 | Fresh Graduate (Immediate Joining)</div>
  </div>
  <p style="font-size: 8.0pt; color: #475569; margin-top: 1.5px; margin-bottom: 3px;">
    <strong>Relevant Coursework:</strong> Global Logistics & Supply Chain Management, International Trade Finance & Documentation, Commercial Contract Law, Business Statistics, Managerial Communication.
  </p>

  <!-- SKILLS & LEARNING AGILITY -->
  <div class="section-title">Skills & Capabilities</div>
  <table class="skills-table">
    <tr>
      <td class="skill-label">Learning & Adaptability:</td>
      <td class="skill-val">High Coachability, Rapid Software & Process Adoption, Strict SOP Execution, Active Listening, Positive Team Attitude.</td>
    </tr>
    <tr>
      <td class="skill-label">Operations Support:</td>
      <td class="skill-val">Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Basic Invoice & 3-Way Matching, Record Verification.</td>
    </tr>
    <tr>
      <td class="skill-label">Inventory & Logistics:</td>
      <td class="skill-val">Physical Stock Counting, Stock Ledger Auditing, Dual-Custody Inventory Governance, Zero Shrinkage Control, Shipping Invoices.</td>
    </tr>
    <tr>
      <td class="skill-label">Computer & Tools:</td>
      <td class="skill-val">MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Entry), Google Workspace, MS Word, PowerPoint.</td>
    </tr>
    <tr>
      <td class="skill-label">Workplace Readiness:</td>
      <td class="skill-val">Attention to Detail, Reliable Ownership, Time Management, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Onboarding.</td>
    </tr>
  </table>

  <!-- INTERNSHIPS & PRACTICAL FIELD EXPOSURE -->
  <div class="section-title">Internships & Practical Field Exposure</div>

  <div class="row">
    <div><span class="title">Commercial Operations Intern</span> — <span class="sub">Pencil Mark Interior Solutions LLP</span></div>
    <div class="date">July 2024 – Aug 2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Quickly learned commercial estimation workflows and maintained supplier vendor quote comparison sheets in MS Excel.</li>
    <li>Tracked purchase orders against delivery dates and site completion notes, helping avoid billing discrepancies and delays.</li>
    <li>Assisted the commercial team in preparing client proposals and scopes of work, supporting the closure of corporate B2B contracts.</li>
  </ul>

  <div class="row">
    <div><span class="title">Operations & Data Verification Intern</span> — <span class="sub">Instawork Services India Pvt. Ltd.</span></div>
    <div class="date">2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Rapidly trained on operational verification checklists, reviewing incoming partner and user profile documentation.</li>
    <li>Maintained an audited <strong>99.4% accuracy rating</strong> across high-speed review queues, catching irregular submissions before database entry.</li>
    <li>Demonstrated high coachability, applying supervisor feedback quickly to improve daily review turnaround time by <strong>12%</strong>.</li>
  </ul>

  <div class="row">
    <div><span class="title">Event Operations & Logistics Lead</span> — <span class="sub">Salt in My Cocoa (Aero India 2025)</span></div>
    <div class="date">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
  </div>
  <ul>
    <li>Managed on-ground stall logistics and inventory replenishment across 5 peak days for <strong>100,000+ public and defense visitors</strong>.</li>
    <li>Maintained disciplined dual-custody stock counts before and after every shift, achieving <strong>0% stock loss / shrinkage</strong>.</li>
    <li>Balanced daily digital UPI payments and cashier registers against physical stock counts with <strong>100% financial accuracy</strong>.</li>
  </ul>

  <div class="row">
    <div><span class="title">Community Operations Volunteer</span> — <span class="sub">Non-Profit Social Initiative</span></div>
    <div class="date">2024 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Checked participant registration details and verified student identity records in compliance with event guidelines.</li>
    <li>Coordinated volunteer schedules and maintained organized participant rosters in Google Sheets.</li>
  </ul>

  <!-- PROJECT / SELF-INITIATIVE -->
  <div class="section-title">Academic & Self-Learning Project</div>
  <div class="row">
    <div><span class="title">Job Portal Automation & Requisition Tracker</span> — <span class="sub">Student Initiative</span></div>
    <div class="date">2026 | Python & Spreadsheets</div>
  </div>
  <ul>
    <li>Demonstrated self-directed learning by creating a Python script to gather and organize corporate job postings into structured spreadsheets.</li>
    <li>Automated repetitive manual sorting and tracking tasks, ensuring accurate data organization with zero manual overhead.</li>
  </ul>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="text">
    <strong>Certifications:</strong> Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL) • Enterprise Operational Excellence<br>
    <strong>Languages:</strong> English (Fluent Professional Proficiency), Hindi (Native / Bilingual)
  </p>

</div>
</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Accenture_Operations_CV.html")
pdf_path = os.path.join(OUTPUT_DIR_PDF, "Aditya_Mehra_Accenture_Operations_CV.pdf")
root_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Accenture_Operations_CV.pdf")
root_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Accenture_Operations_CV.docx")
docx_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Accenture_Operations_CV.docx")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]
subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    shutil.copyfile(pdf_path, root_pdf)
    print(f"Generated Fresher Willing-to-Learn PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")

# -------------------------------------------------------------
# 2. DOCX CV: "WILLING TO LEARN" FRESHER (1-PAGE A4 STRICT)
# -------------------------------------------------------------
doc = Document()
for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.35)
    s.bottom_margin = Inches(0.35)
    s.left_margin = Inches(0.48)
    s.right_margin = Inches(0.48)

C_NAVY = RGBColor(15, 23, 42)
C_BLUE = RGBColor(29, 78, 216)
C_SLATE = RGBColor(71, 85, 105)
C_BODY = RGBColor(30, 41, 59)
C_GREEN = RGBColor(6, 95, 70)

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

# Header
p_name = doc.add_paragraph()
p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_name.paragraph_format.space_before = Pt(0)
p_name.paragraph_format.space_after = Pt(1)
r_n = p_name.add_run("ADITYA MEHRA")
r_n.font.name = "Arial"; r_n.font.size = Pt(18); r_n.font.bold = True; r_n.font.color.rgb = C_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1.5)
r_s = p_sub.add_run("BBA GRADUATE (BATCH OF 2026) // ENTRY-LEVEL OPERATIONS NEW ASSOCIATE")
r_s.font.name = "Arial"; r_s.font.size = Pt(9.2); r_s.font.bold = True; r_s.font.color.rgb = C_BLUE

p_c = doc.add_paragraph()
p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c.paragraph_format.space_before = Pt(0)
p_c.paragraph_format.space_after = Pt(1.5)
r_c = p_c.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  linkedin.com/in/aditya-mehra")
r_c.font.name = "Arial"; r_c.font.size = Pt(8.2); r_c.font.color.rgb = C_SLATE

p_b = doc.add_paragraph()
p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_b.paragraph_format.space_before = Pt(0)
p_b.paragraph_format.space_after = Pt(3.5)
r_b = p_b.add_run("Fresher (0–1 Yrs) • Highly Trainable & Quick Learner • Immediate Joiner (0 Days Notice) • 24/7 Shifts Flexible")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.8); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"; r.font.size = Pt(9.2); r.font.bold = True; r.font.color.rgb = C_NAVY
    add_clean_divider(p)

# Career Objective
add_sec("Career Objective")
p_sm = doc.add_paragraph()
p_sm.paragraph_format.space_before = Pt(1)
p_sm.paragraph_format.space_after = Pt(2)
p_sm.paragraph_format.line_spacing = 1.15
r_sm = p_sm.add_run(
    "Enthusiastic and hardworking 2026 BBA graduate in International Business from Dayananda Sagar University, seeking an entry-level Level 13 Operations New Associate role at Accenture Operations. An eager learner with high coachability and dedication to mastering enterprise processes, software, and Standard Operating Procedures (SOPs). Offers practical internship experience in vendor coordination, document verification, inventory management, and MS Excel. Known for strong accountability, positive attitude, and rapid adaptation. Local Bengaluru resident with 0 days notice and complete readiness for 24/7 rotational and night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(8.3); r_sm.font.color.rgb = C_BODY

# Education
add_sec("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(1)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) — International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.8); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  •  2023 – 2026 | Fresh Graduate (Immediate Joining)\n")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(8.2); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE
r_e3 = p_ed.add_run("Relevant Coursework: Global Logistics & Supply Chain Management, International Trade Finance & Documentation, Commercial Contract Law, Business Statistics, Managerial Communication.")
r_e3.font.name = "Arial"; r_e3.font.size = Pt(7.6); r_e3.font.color.rgb = C_SLATE

# Skills & Learning Agility
add_sec("Skills & Capabilities")
skills_list = [
    ("Learning & Adaptability", "High Coachability, Rapid Software & Process Adoption, Strict SOP Execution, Active Listening, Positive Team Attitude."),
    ("Operations Support", "Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Basic Invoice & 3-Way Matching, Record Verification."),
    ("Inventory & Logistics", "Physical Stock Counting, Stock Ledger Auditing, Dual-Custody Inventory Governance, Zero Shrinkage Control, Shipping Invoices."),
    ("Computer & Tools", "MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Entry), Google Workspace, MS Word, PowerPoint."),
    ("Workplace Readiness", "Attention to Detail, Reliable Ownership, Time Management, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Onboarding.")
]
for cat, txt in skills_list:
    p_s = doc.add_paragraph()
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after = Pt(1.0)
    p_s.paragraph_format.left_indent = Inches(0.12)
    r_1 = p_s.add_run(f"• {cat}: ")
    r_1.font.name = "Arial"; r_1.font.size = Pt(8.0); r_1.font.bold = True; r_1.font.color.rgb = C_NAVY
    r_2 = p_s.add_run(txt)
    r_2.font.name = "Arial"; r_2.font.size = Pt(8.0); r_2.font.color.rgb = C_BODY

# Internships
add_sec("Internships & Practical Field Exposure")
jobs = [
    {
        "title": "Commercial Operations Intern — Pencil Mark Interior Solutions LLP",
        "date": "July 2024 – Aug 2025 | Bengaluru, India",
        "bullets": [
            "Quickly learned commercial estimation workflows and maintained supplier vendor quote comparison sheets in MS Excel.",
            "Tracked purchase orders against delivery dates and site completion notes, helping avoid billing discrepancies and delays.",
            "Assisted the commercial team in preparing client proposals and scopes of work, supporting the closure of corporate B2B contracts."
        ]
    },
    {
        "title": "Operations & Data Verification Intern — Instawork Services India Pvt. Ltd.",
        "date": "2025 | Bengaluru, India",
        "bullets": [
            "Rapidly trained on operational verification checklists, reviewing incoming partner and user profile documentation.",
            "Maintained an audited 99.4% accuracy rating across high-speed review queues, catching irregular submissions before database entry.",
            "Demonstrated high coachability, applying supervisor feedback quickly to improve daily review turnaround time by 12%."
        ]
    },
    {
        "title": "Event Operations & Logistics Lead — Salt in My Cocoa (Aero India 2025)",
        "date": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Managed on-ground stall logistics and inventory replenishment across 5 peak days for 100,000+ public and defense visitors.",
            "Maintained disciplined dual-custody stock counts before and after every shift, achieving 0% stock loss / shrinkage.",
            "Balanced daily digital UPI payments and cashier registers against physical stock counts with 100% financial accuracy."
        ]
    },
    {
        "title": "Community Operations Volunteer — Non-Profit Social Initiative",
        "date": "2024 | Bengaluru, India",
        "bullets": [
            "Checked participant registration details and verified student identity records in compliance with event guidelines.",
            "Coordinated volunteer schedules and maintained organized participant rosters in Google Sheets."
        ]
    }
]

for j in jobs:
    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(2.0)
    p_j.paragraph_format.space_after = Pt(0.8)
    p_j.paragraph_format.keep_with_next = True
    r_j1 = p_j.add_run(f"{j['title']}\n")
    r_j1.font.name = "Arial"; r_j1.font.size = Pt(8.4); r_j1.font.bold = True; r_j1.font.color.rgb = C_NAVY
    r_j2 = p_j.add_run(j['date'])
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.6); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(0.8)
        p_b.paragraph_format.left_indent = Inches(0.18)
        p_b.paragraph_format.first_line_indent = Inches(-0.12)
        r_dot = p_b.add_run("– ")
        r_dot.font.name = "Arial"; r_dot.font.size = Pt(8.0); r_dot.font.bold = True; r_dot.font.color.rgb = C_BLUE
        r_txt = p_b.add_run(b)
        r_txt.font.name = "Arial"; r_txt.font.size = Pt(8.0); r_txt.font.color.rgb = C_BODY

# Project
add_sec("Academic & Self-Learning Project")
p_p = doc.add_paragraph()
p_p.paragraph_format.space_before = Pt(1.2)
p_p.paragraph_format.space_after = Pt(0.8)
r_p1 = p_p.add_run("Job Portal Automation & Requisition Tracker — Student Initiative\n")
r_p1.font.name = "Arial"; r_p1.font.size = Pt(8.4); r_p1.font.bold = True; r_p1.font.color.rgb = C_NAVY
r_p2 = p_p.add_run("2026 | Python & Spreadsheets\n")
r_p2.font.name = "Arial"; r_p2.font.size = Pt(7.6); r_p2.font.color.rgb = C_SLATE
r_p3 = p_p.add_run("– Demonstrated self-directed learning by creating a Python script to gather and organize corporate job postings into structured spreadsheets.\n– Automated repetitive manual sorting and tracking tasks, ensuring accurate data organization with zero manual overhead.")
r_p3.font.name = "Arial"; r_p3.font.size = Pt(8.0); r_p3.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cl = doc.add_paragraph()
p_cl.paragraph_format.space_before = Pt(1)
p_cl.paragraph_format.space_after = Pt(1)
r_c1 = p_cl.add_run("Certifications: ")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(8.0); r_c1.font.bold = True; r_c1.font.color.rgb = C_NAVY
r_c2 = p_cl.add_run("Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL) • Enterprise Operational Excellence\n")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(8.0); r_c2.font.color.rgb = C_BODY
r_l1 = p_cl.add_run("Languages: ")
r_l1.font.name = "Arial"; r_l1.font.size = Pt(8.0); r_l1.font.bold = True; r_l1.font.color.rgb = C_NAVY
r_l2 = p_cl.add_run("English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_l2.font.name = "Arial"; r_l2.font.size = Pt(8.0); r_l2.font.color.rgb = C_BODY

doc.save(docx_path)
shutil.copyfile(docx_path, root_docx)
print(f"Generated Fresher Willing-to-Learn DOCX: {docx_path} (Size: {os.path.getsize(docx_path)} bytes)")

pdf_data = open(pdf_path, "rb").read()
page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
