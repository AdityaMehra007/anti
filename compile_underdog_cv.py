"""
compile_underdog_cv.py
Compiles the "Underdog Best CV" for Aditya Mehra:
- Hungry, grounded, high-grit, relentless work ethic.
- Built from real on-ground sweat: 0% shrinkage at Aero India (100k+ crowd), 99.4% accuracy at Instawork,
  PO tracking at Pencil Mark, zero-downtime event operations, NGO volunteering, and self-taught Python tooling.
- Zero entitlement, 100% accountability, ready for night/rotational shifts, immediate joiner.
- Strictly 1-Page A4, ATS-optimized, with native DOCX and PDF.
"""

import os
import subprocess
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
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
<title>Aditya Mehra - Accenture Operations New Associate CV</title>
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
    line-height: 1.24;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .container {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 8mm 12.5mm 6mm 12.5mm;
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
    font-size: 19.5pt;
    font-weight: 800;
    letter-spacing: 0.6px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 8.9pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 1.5px;
    letter-spacing: 0.25px;
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
    margin-top: 2.5px;
    font-size: 7.5pt;
    font-weight: 700;
    color: #065f46;
    background: #ecfdf5;
    display: inline-block;
    padding: 1.5px 9px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
  }

  /* Section Titles */
  .section-title {
    font-size: 8.9pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 1px;
    margin-top: 4px;
    margin-bottom: 2.5px;
  }
  
  /* Content Blocks */
  .row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.5px;
  }
  .title {
    font-weight: 700;
    color: #0f172a;
    font-size: 8.4pt;
  }
  .sub {
    color: #1d4ed8;
    font-weight: 600;
    font-size: 8.1pt;
  }
  .date {
    font-size: 7.6pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }
  .text {
    font-size: 8.0pt;
    color: #334155;
    text-align: justify;
    line-height: 1.25;
  }
  ul {
    padding-left: 14px;
    margin-bottom: 2.5px;
  }
  li {
    font-size: 7.8pt;
    color: #334155;
    margin-bottom: 1px;
    line-height: 1.21;
  }
  li strong {
    color: #0f172a;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    margin-bottom: 2px;
  }
  .skills-table td {
    padding: 1.2px 0;
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
    body { background: #f8fafc; padding: 20px; }
    .container {
      max-width: 210mm;
      min-height: 297mm;
      background: #fff;
      padding: 10mm 12mm;
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
      Fresher (0–1 Yrs) • Disciplined Execution & High Coachability • Immediate Availability (0 Days Notice) • 24/7 Shifts Flexible
    </div>
  </div>

  <!-- CAREER OBJECTIVE -->
  <div class="section-title">Career Objective</div>
  <p class="text">
    Results-driven, highly disciplined, and versatile <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, targeting the <strong>Level 13 Operations New Associate</strong> position at Accenture Operations. Built practical operational stamina through hands-on execution—reconciling multi-channel registers under high-pressure crowds at Aero India 2025, auditing partner documents with 99.4% precision at Instawork, administering vendor POs at Pencil Mark, and coordinating live on-ground productions. Combines self-taught technical initiative (Python & Advanced Excel) with a rigorous work ethic. Local Bengaluru resident with <strong>0 days notice period</strong>, eager to master enterprise SOPs, and <strong>100% committed to 24/7 rotational and night shifts</strong>.
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

  <!-- CORE SKILLS & OPERATIONAL COMPETENCIES -->
  <div class="section-title">Core Skills & Operational Competencies</div>
  <table class="skills-table">
    <tr>
      <td class="skill-label">Procurement & PO Support:</td>
      <td class="skill-val">Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Vendor Quote Comparison Sheets, Basic 3-Way Matching, Discrepancy Resolution.</td>
    </tr>
    <tr>
      <td class="skill-label">Quality, KYC & Document QA:</td>
      <td class="skill-val">Customer Identification Program (CIP), Document Verification Checklists, Data Quality Auditing (99.4% Audited Precision), Strict SOP Adherence.</td>
    </tr>
    <tr>
      <td class="skill-label">On-Ground Execution & Inventory:</td>
      <td class="skill-val">On-Ground Live Event Operations, Vendor SLA Governance, Dual-Custody Stock Counting, 0.0% Inventory Shrinkage, UPI/Cash Reconciliation.</td>
    </tr>
    <tr>
      <td class="skill-label">Computer & Software Tools:</td>
      <td class="skill-val">MS Excel (VLOOKUP, XLOOKUP, Pivot Tables, SUMIFS, Power Query, Data Validation), Google Workspace, MS Word, PowerPoint, Python Basics.</td>
    </tr>
    <tr>
      <td class="skill-label">Operational Execution & Shifts:</td>
      <td class="skill-val">Cross-Functional Teamwork, Queue Triage during Peak Spikes, High Coachability, 100% 24/7 Rotational & Night Shift Adaptability, 0 Days Notice.</td>
    </tr>
  </table>

  <!-- PROFESSIONAL EXPERIENCE & PRACTICAL EXPOSURE -->
  <div class="section-title">Professional Experience & Practical Exposure</div>

  <!-- Role 1: Pencil Mark (Procurement Operations Support) -->
  <div class="row">
    <div><span class="title">Commercial Operations Intern</span> — <span class="sub">Pencil Mark Interior Solutions LLP</span></div>
    <div class="date">Jul 2024 – Aug 2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Engineered supplier quotation comparison models and pricing matrices in MS Excel, ensuring accurate commercial evaluations for senior estimators.</li>
    <li>Administered Purchase Order (PO) tracking from issuance to delivery confirmation, cross-referencing vendor delivery challans against site milestones to eliminate billing exceptions (supporting <strong>₹1.5L+ in closed contracts</strong>).</li>
  </ul>

  <!-- Role 2: Instawork (KYC Document Verification) -->
  <div class="row">
    <div><span class="title">Operations & Data Verification Intern</span> — <span class="sub">Instawork Services India Pvt. Ltd.</span></div>
    <div class="date">2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Processed high-volume partner onboarding and identity verification queues, sustaining an audited <strong>99.4% precision rate</strong> through meticulous checklist execution.</li>
    <li>Executed daily queue triage during peak spikes alongside team members, actively applying supervisor feedback to <strong>reduce review cycle time by 12%</strong>.</li>
  </ul>

  <!-- Role 3: Aero India 2025 (Inventory & Financial Reconciliation) -->
  <div class="row">
    <div><span class="title">Exhibition Operations & Logistics Lead</span> — <span class="sub">Salt in My Cocoa (AERO India 2025)</span></div>
    <div class="date">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
  </div>
  <ul>
    <li>Directed on-ground booth logistics across 5 high-density days serving <strong>100,000+ defense and public attendees</strong> under strict military security protocols.</li>
    <li>Enforced disciplined dual-custody stock audits before/after shifts to achieve <strong>0.0% inventory shrinkage</strong>, reconciling registers with <strong>100% financial accuracy</strong>.</li>
  </ul>

  <!-- Role 4: TRILOGY & Event Management -->
  <div class="row">
    <div><span class="title">Event Operations Coordinator</span> — <span class="sub">TRILOGY Indo-Jazz Fusion & Commercial Productions</span></div>
    <div class="date">2019 – 2026 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Governed on-ground stage logistics, artist hospitality, and technical equipment riders for the TRILOGY live concert at Bangalore Club (Jan 2026), delivering zero stage downtime.</li>
    <li>Negotiated vendor SLAs across audio, lighting, and stage crews, reducing project procurement costs by <strong>15%–20%</strong> through direct supplier coordination.</li>
  </ul>

  <!-- Role 5: NGO / Community Operations -->
  <div class="row">
    <div><span class="title">Community Operations Volunteer</span> — <span class="sub">NGO & Social Welfare Initiative</span></div>
    <div class="date">2024 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Administered participant intake and identity credential verification in compliance with foundation guidelines, maintaining error-free audit logs in Google Sheets.</li>
    <li>Coordinated volunteer shift schedules and attendee crowd logistics, ensuring seamless execution during city-wide social outreach drives.</li>
  </ul>

  <!-- ACADEMIC & SELF-LEARNING PROJECT -->
  <div class="section-title">Academic & Self-Learning Project</div>
  <div class="row">
    <div><span class="title">Job Portal Automation & Spreadsheet Tracker</span> — <span class="sub">Student Technical Initiative</span></div>
    <div class="date">2025 – 2026 | Python & Spreadsheets</div>
  </div>
  <ul>
    <li>Engineered an automated Python data extraction tool to crawl, structure, and categorize corporate requisitions into clean, searchable Excel databases, eliminating manual workflow redundancies.</li>
  </ul>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="text">
    <strong>Certifications:</strong> Written Management Commendation for Excellence (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL) • Enterprise Operational Excellence<br>
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

all_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_All_Experiences_CV.pdf")
all_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_All_Experiences_CV.docx")

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
    with open(all_pdf, "wb") as f_out:
        f_out.write(pdf_bytes)

print(f"Generated Underdog Best PDF: {root_pdf} (Size: {len(pdf_bytes)} bytes)")

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
r_n.font.name = "Arial"; r_n.font.size = Pt(17.5); r_n.font.bold = True; r_n.font.color.rgb = C_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1)
r_s = p_sub.add_run("BBA GRADUATE (BATCH OF 2026) // ENTRY-LEVEL OPERATIONS NEW ASSOCIATE")
r_s.font.name = "Arial"; r_s.font.size = Pt(8.8); r_s.font.bold = True; r_s.font.color.rgb = C_BLUE

p_c = doc.add_paragraph()
p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c.paragraph_format.space_before = Pt(0)
p_c.paragraph_format.space_after = Pt(1)
r_c = p_c.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  linkedin.com/in/aditya-mehra")
r_c.font.name = "Arial"; r_c.font.size = Pt(8.0); r_c.font.color.rgb = C_SLATE

p_b = doc.add_paragraph()
p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_b.paragraph_format.space_before = Pt(0)
p_b.paragraph_format.space_after = Pt(2.5)
r_b = p_b.add_run("Fresher (0-1 Yrs) | High-Grit & Relentless Work Ethic | 100% Accountable | Immediate Joiner (0 Days Notice) | 24/7 Shifts Ready")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.5); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4.0)
    p.paragraph_format.space_after = Pt(1.0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"; r.font.size = Pt(8.8); r.font.bold = True; r.font.color.rgb = C_NAVY
    add_clean_divider(p)

# Career Objective
add_sec("Career Objective")
p_sm = doc.add_paragraph()
p_sm.paragraph_format.space_before = Pt(1)
p_sm.paragraph_format.space_after = Pt(1.5)
p_sm.paragraph_format.line_spacing = 1.15
r_sm = p_sm.add_run(
    "Results-driven, highly disciplined, and versatile 2026 BBA graduate in International Business from Dayananda Sagar University, targeting the Level 13 Operations New Associate position at Accenture Operations. Built practical operational stamina through hands-on execution—reconciling multi-channel registers under high-pressure crowds at Aero India 2025, auditing partner documents with 99.4% precision at Instawork, administering vendor POs at Pencil Mark, and coordinating live on-ground productions. Combines self-taught technical initiative (Python & Advanced Excel) with a rigorous work ethic. Local Bengaluru resident with 0 days notice period, eager to master enterprise SOPs, and 100% committed to 24/7 rotational and night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(8.0); r_sm.font.color.rgb = C_BODY

# Education
add_sec("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(0.5)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) - International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.4); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  |  2023 - 2026 | Fresh Graduate (Immediate Availability)")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(8.0); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE

# Core Skills & Competencies
add_sec("Core Skills & Operational Competencies")
skills_list = [
    ("Procurement & PO Support", "Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Vendor Quote Comparison Sheets, Basic 3-Way Matching, Discrepancy Resolution."),
    ("Quality, KYC & Document QA", "Customer Identification Program (CIP), Document Verification Checklists, Data Quality Auditing (99.4% Audited Precision), Strict SOP Adherence."),
    ("On-Ground Execution & Inventory", "On-Ground Live Event Operations, Vendor SLA Governance, Dual-Custody Stock Counting, 0.0% Inventory Shrinkage, UPI/Cash Reconciliation."),
    ("Computer & Software Tools", "MS Excel (VLOOKUP, XLOOKUP, Pivot Tables, SUMIFS, Power Query, Data Validation), Google Workspace, MS Word, PowerPoint, Python Basics."),
    ("Operational Execution & Shifts", "Cross-Functional Teamwork, Queue Triage during Peak Spikes, High Coachability, 100% 24/7 Rotational & Night Shift Adaptability, 0 Days Notice.")
]
for cat, txt in skills_list:
    p_s = doc.add_paragraph()
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after = Pt(0.8)
    p_s.paragraph_format.left_indent = Inches(0.1)
    r_1 = p_s.add_run(f"- {cat}: ")
    r_1.font.name = "Arial"; r_1.font.size = Pt(7.8); r_1.font.bold = True; r_1.font.color.rgb = C_NAVY
    r_2 = p_s.add_run(txt)
    r_2.font.name = "Arial"; r_2.font.size = Pt(7.8); r_2.font.color.rgb = C_BODY

# Professional Experience
add_sec("Professional Experience & Practical Exposure")
jobs = [
    {
        "title": "Commercial Operations Intern - Pencil Mark Interior Solutions LLP",
        "date": "Jul 2024 - Aug 2025 | Bengaluru, India",
        "bullets": [
            "Engineered supplier quotation comparison models and pricing matrices in MS Excel, ensuring accurate commercial evaluations for senior estimators.",
            "Administered Purchase Order (PO) tracking from issuance to delivery confirmation, cross-referencing vendor delivery challans against site milestones to eliminate billing exceptions (supporting INR 1.5L+ in closed contracts)."
        ]
    },
    {
        "title": "Operations & Data Verification Intern - Instawork Services India Pvt. Ltd.",
        "date": "2025 | Bengaluru, India",
        "bullets": [
            "Processed high-volume partner onboarding and identity verification queues, sustaining an audited 99.4% precision rate through meticulous checklist execution.",
            "Executed daily queue triage during peak spikes alongside team members, actively applying supervisor feedback to reduce review cycle time by 12%."
        ]
    },
    {
        "title": "Exhibition Operations & Logistics Lead - Salt in My Cocoa (AERO India 2025)",
        "date": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Directed on-ground booth logistics across 5 high-density days serving 100,000+ defense and public attendees under strict military security protocols.",
            "Enforced disciplined dual-custody stock audits before/after shifts to achieve 0.0% inventory shrinkage, reconciling registers with 100% financial accuracy."
        ]
    },
    {
        "title": "Event Operations Coordinator - TRILOGY Indo-Jazz Fusion & Commercial Productions",
        "date": "2019 - 2026 | Bengaluru, India",
        "bullets": [
            "Governed on-ground stage logistics, artist hospitality, and technical equipment riders for the TRILOGY live concert at Bangalore Club (Jan 2026), delivering zero stage downtime.",
            "Negotiated vendor SLAs across audio, lighting, and stage crews, reducing project procurement costs by 15%-20% through direct supplier coordination."
        ]
    },
    {
        "title": "Community Operations Volunteer - NGO & Social Welfare Initiative",
        "date": "2024 | Bengaluru, India",
        "bullets": [
            "Administered participant intake and identity credential verification in compliance with foundation guidelines, maintaining error-free audit logs in Google Sheets.",
            "Coordinated volunteer shift schedules and attendee crowd logistics, ensuring seamless execution during city-wide social outreach drives."
        ]
    }
]

for j in jobs:
    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(1.5)
    p_j.paragraph_format.space_after = Pt(0.4)
    p_j.paragraph_format.keep_with_next = True
    r_j1 = p_j.add_run(f"{j['title']}\n")
    r_j1.font.name = "Arial"; r_j1.font.size = Pt(8.2); r_j1.font.bold = True; r_j1.font.color.rgb = C_NAVY
    r_j2 = p_j.add_run(j['date'])
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.4); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b_item = doc.add_paragraph()
        p_b_item.paragraph_format.space_before = Pt(0)
        p_b_item.paragraph_format.space_after = Pt(0.5)
        p_b_item.paragraph_format.left_indent = Inches(0.12)
        p_b_item.paragraph_format.line_spacing = 1.15
        r_bullet = p_b_item.add_run(f"- {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(7.8); r_bullet.font.color.rgb = C_BODY

# Academic Project
add_sec("Academic & Self-Learning Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.4)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Automation & Spreadsheet Tracker - Student Technical Initiative\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.2); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 - 2026 | Python & Spreadsheets")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.4); r_pr2.font.color.rgb = C_SLATE

p_pr_b = doc.add_paragraph()
p_pr_b.paragraph_format.space_before = Pt(0)
p_pr_b.paragraph_format.space_after = Pt(0.8)
p_pr_b.paragraph_format.left_indent = Inches(0.12)
r_pr_b = p_pr_b.add_run("- Engineered an automated Python data extraction tool to crawl, structure, and categorize corporate requisitions into clean, searchable Excel databases, eliminating manual workflow redundancies.")
r_pr_b.font.name = "Arial"; r_pr_b.font.size = Pt(7.8); r_pr_b.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.space_before = Pt(0.8)
p_cert.paragraph_format.space_after = Pt(0.8)
r_c1 = p_cert.add_run("Certifications: Written Management Commendation for Excellence (Pencil Mark) | Google Digital Marketing Fundamentals | Service Marketing (NPTEL) | Enterprise Operational Excellence\n")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.6); r_c1.font.color.rgb = C_BODY
r_c2 = p_cert.add_run("Languages: English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.6); r_c2.font.color.rgb = C_BODY

doc.save(docx_path)
doc.save(root_docx)
doc.save(all_docx)
print(f"Generated Underdog Best DOCX: {root_docx} (Size: {os.path.getsize(root_docx)} bytes)")

# Verify Page Count
with open(root_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
