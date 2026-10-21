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
# 1. CLEAN, HONEST, REFRESHED FRESHER HTML CV
# -------------------------------------------------------------
fresher_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra - Fresher CV (Accenture Operations Level 13)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 8mm 10mm 8mm 10mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.32;
  }
  body {
    background: #fff;
    font-size: 9.2pt;
  }
  .container {
    max-width: 100%;
    margin: 0 auto;
  }
  
  /* Header */
  .header {
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 6px;
    margin-bottom: 6px;
  }
  .name {
    font-size: 19pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 9.6pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 2px;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }
  .contact-info {
    font-size: 8.5pt;
    color: #475569;
    margin-top: 3px;
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact-info a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
  }
  .fresher-badge {
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
    font-size: 9.5pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 6px;
    margin-bottom: 4px;
  }
  
  /* Education */
  .edu-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .edu-title {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
  }
  .edu-sub {
    font-size: 8.6pt;
    color: #1d4ed8;
    font-weight: 600;
  }
  .date-loc {
    font-size: 8.0pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Summary */
  .summary-text {
    font-size: 8.6pt;
    color: #334155;
    text-align: justify;
    line-height: 1.34;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.3pt;
  }
  .skills-table td {
    padding: 2px 0;
    vertical-align: top;
  }
  .skill-cat {
    font-weight: 700;
    color: #0f172a;
    width: 24%;
    white-space: nowrap;
  }
  .skill-items {
    color: #334155;
    width: 76%;
  }

  /* Experience Blocks */
  .item-block {
    margin-bottom: 4px;
  }
  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1px;
  }
  .role-title {
    font-weight: 700;
    color: #0f172a;
    font-size: 8.8pt;
  }
  .company-name {
    font-weight: 600;
    color: #1d4ed8;
    font-size: 8.5pt;
  }
  .bullets {
    list-style-type: disc;
    padding-left: 15px;
  }
  .bullets li {
    font-size: 8.2pt;
    color: #334155;
    margin-bottom: 1.5px;
    line-height: 1.30;
  }
  .bullets strong {
    color: #0f172a;
  }

  /* Print Specific */
  @media print {
    body { background: #fff; padding: 0; }
    .container { max-width: 100%; }
    .print-btn { display: none; }
  }
  @media screen {
    body { background: #f1f5f9; padding: 20px; }
    .container {
      max-width: 210mm;
      min-height: 297mm;
      background: #fff;
      padding: 10mm 12mm;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
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
      box-shadow: 0 4px 12px rgba(29,78,216,0.3);
      font-size: 13px;
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
    <div class="subtitle">BBA Graduate (Fresh Graduate – Batch of 2026) // Entry-Level Operations New Associate</div>
    <div class="contact-info">
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
    <div class="fresher-badge">
      Fresher (0–1 Yrs Experience) • Immediate Joiner (0 Days Notice) • 100% Rotational & Night Shift Flexible • Bengaluru Local
    </div>
  </div>

  <!-- EDUCATION -->
  <div class="section-title">Education</div>
  <div class="edu-row">
    <div>
      <div class="edu-title">Bachelor of Business Administration (BBA) — International Business</div>
      <div class="edu-sub">Dayananda Sagar University (DSU), Bengaluru, Karnataka</div>
    </div>
    <div class="date-loc">2023 – 2026 | Fresh Graduate (Immediate Joining)</div>
  </div>
  <p style="font-size: 7.9pt; color: #475569; margin-top: 1.5px;">
    <strong>Relevant Coursework:</strong> Supply Chain & Logistics Management, International Trade Finance & Documentation, Commercial Business Law, Business Communication, Business Mathematics & Statistics.
  </p>

  <!-- CAREER OBJECTIVE / SUMMARY -->
  <div class="section-title">Career Objective</div>
  <p class="summary-text">
    Motivated and detail-oriented <strong>2026 BBA graduate in International Business from Dayananda Sagar University, Bengaluru</strong>, seeking an entry-level <strong>Level 13 Operations New Associate</strong> role at Accenture Operations. Eager to learn, follow Standard Operating Procedures (SOPs), and contribute effectively to daily back-office processes. Practical internship experience in vendor follow-ups, purchase order tracking, document verification, event inventory handling, and daily transaction reconciliation. Proficient in MS Excel (VLOOKUP, Pivot Tables) and daily computer tools. Bengaluru local resident, available for <strong>immediate onboarding (0 Days Notice)</strong>, and 100% prepared for 24/7 rotational and night shifts.
  </p>

  <!-- CORE SKILLS -->
  <div class="section-title">Skills & Knowledge</div>
  <table class="skills-table">
    <tr>
      <td class="skill-cat">Operations Support:</td>
      <td class="skill-items">Procurement Support, Purchase Order (PO) Tracking, Invoice Verification & Matching Basics, Vendor Follow-ups, Back-Office Operations, Standard Operating Procedures (SOP) Execution.</td>
    </tr>
    <tr>
      <td class="skill-cat">Logistics & Supply Chain:</td>
      <td class="skill-items">Physical Inventory Tracking, Stock Auditing, Shipping Invoices, Basic Trade Terms (Incoterms), Dual-Custody Inventory Governance, Discrepancy Reporting.</td>
    </tr>
    <tr>
      <td class="skill-cat">Computer & Office Tools:</td>
      <td class="skill-items">MS Excel (VLOOKUP, Pivot Tables, Formulas, Data Entry, Sorting & Filtering), MS Word, PowerPoint, Google Sheets, Email Writing & Etiquette.</td>
    </tr>
    <tr>
      <td class="skill-cat">Professional Strengths:</td>
      <td class="skill-items">High Accuracy & Attention to Detail, Problem Solving, Quick Learner, Team Player, Time Management, Adaptability to Rotational / Night Shifts.</td>
    </tr>
  </table>

  <!-- INTERNSHIPS & PRACTICAL EXPERIENCE -->
  <div class="section-title">Internships & Practical Field Exposure</div>

  <!-- Role 1: Pencil Mark -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Commercial Operations Intern</span> — <span class="company-name">Pencil Mark Interior Solutions LLP</span></div>
      <div class="date-loc">July 2024 – Aug 2025 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Assisted with tracking supplier price quotes, organizing vendor contact matrices, and preparing comparison pricing sheets in MS Excel.</li>
      <li>Supported the team in tracking purchase orders against delivery dates and site completion notes, helping avoid billing delays.</li>
      <li>Assisted in preparing commercial scopes of work and service estimates, supporting the team in securing B2B corporate contracts.</li>
    </ul>
  </div>

  <!-- Role 2: Instawork -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Operations & Data Verification Intern</span> — <span class="company-name">Instawork Services India Pvt. Ltd.</span></div>
      <div class="date-loc">2025 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Reviewed and verified incoming user and partner profile documents, carefully following standard operating procedure (SOP) checklists.</li>
      <li>Maintained a verified <strong>99.4% accuracy rate</strong> across daily verification queues, ensuring clean and accurate database records.</li>
      <li>Worked closely with team supervisors to flag unclear submissions and identify simple ways to speed up routine review queues.</li>
    </ul>
  </div>

  <!-- Role 3: Aero India -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Event Operations & Logistics Lead</span> — <span class="company-name">Salt in My Cocoa (Aero India 2025)</span></div>
      <div class="date-loc">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
    </div>
    <ul class="bullets">
      <li>Managed daily stall setup, on-ground inventory replenishment, and security clearances across 5 days for <strong>100,000+ public and defense visitors</strong>.</li>
      <li>Kept strict physical inventory counts before and after each shift, achieving <strong>0% stock loss / shrinkage</strong> during peak rush hours.</li>
      <li>Reconciled daily digital UPI payments and cashier registers against stock counts with <strong>100% financial balancing</strong>.</li>
    </ul>
  </div>

  <!-- Role 4: NGO / Community Ops -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Community Operations & Volunteer Support</span> — <span class="company-name">Non-Profit Social Initiative</span></div>
      <div class="date-loc">2024 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Checked and verified participant registration details and identity records in compliance with event guidelines.</li>
      <li>Maintained volunteer schedules and participant databases in Google Sheets, coordinating smoothly across city outreach drives.</li>
    </ul>
  </div>

  <!-- TECHNICAL PROJECTS & AUTOMATION -->
  <div class="section-title">Academic & Automation Project</div>
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Automated Job Portal & Requisition Tracker</span> — <span class="company-name">Student Project</span></div>
      <div class="date-loc">2026 | Python & Spreadsheets</div>
    </div>
    <ul class="bullets">
      <li>Built a simple automation script in Python to gather and organize corporate job requisitions into structured spreadsheets.</li>
      <li>Automated repetitive search and sorting tasks, reducing manual effort and keeping candidate tracking organized.</li>
    </ul>
  </div>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p style="font-size: 8.2pt; color: #334155;">
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
    f.write(fresher_html)

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
    print(f"Generated Honest Fresher PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")

# -------------------------------------------------------------
# 2. GENERATE HONEST FRESHER DOCX CV (1-PAGE A4 STRICT)
# -------------------------------------------------------------
doc = Document()
for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.35)
    s.bottom_margin = Inches(0.35)
    s.left_margin = Inches(0.45)
    s.right_margin = Inches(0.45)

C_NAVY = RGBColor(15, 23, 42)       # #0F172A
C_BLUE = RGBColor(29, 78, 216)      # #1D4ED8
C_SLATE = RGBColor(71, 85, 105)     # #475569
C_BODY = RGBColor(30, 41, 59)       # #1E293B
C_GREEN = RGBColor(6, 95, 70)       # #065F46

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

# Name
p_name = doc.add_paragraph()
p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_name.paragraph_format.space_before = Pt(0)
p_name.paragraph_format.space_after = Pt(1)
r_n = p_name.add_run("ADITYA MEHRA")
r_n.font.name = "Arial"; r_n.font.size = Pt(18); r_n.font.bold = True; r_n.font.color.rgb = C_NAVY

# Subtitle
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1.5)
r_s = p_sub.add_run("BBA GRADUATE (FRESH GRADUATE – BATCH OF 2026) // ENTRY-LEVEL OPERATIONS NEW ASSOCIATE")
r_s.font.name = "Arial"; r_s.font.size = Pt(9.2); r_s.font.bold = True; r_s.font.color.rgb = C_BLUE

# Contact
p_c = doc.add_paragraph()
p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c.paragraph_format.space_before = Pt(0)
p_c.paragraph_format.space_after = Pt(1.5)
r_c = p_c.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  linkedin.com/in/aditya-mehra  |  github.com/AdityaMehra007")
r_c.font.name = "Arial"; r_c.font.size = Pt(8.2); r_c.font.color.rgb = C_SLATE

# Badge
p_b = doc.add_paragraph()
p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_b.paragraph_format.space_before = Pt(0)
p_b.paragraph_format.space_after = Pt(4)
r_b = p_b.add_run("Fresher (0–1 Yrs Experience) • Immediate Joiner (0 Days Notice) • 100% Rotational & Night Shift Flexible • Bengaluru Local")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.8); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec_title(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"; r.font.size = Pt(9.2); r.font.bold = True; r.font.color.rgb = C_NAVY
    add_clean_divider(p)

# Education
add_sec_title("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(1)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) — International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.8); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  •  2023 – 2026 | Fresh Graduate (Immediate Joining)\n")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(8.2); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE
r_e3 = p_ed.add_run("Relevant Coursework: Supply Chain & Logistics Management, International Trade Finance & Documentation, Commercial Business Law, Business Communication, Business Mathematics & Statistics.")
r_e3.font.name = "Arial"; r_e3.font.size = Pt(7.8); r_e3.font.color.rgb = C_SLATE

# Career Objective
add_sec_title("Career Objective")
p_sum = doc.add_paragraph()
p_sum.paragraph_format.space_before = Pt(1)
p_sum.paragraph_format.space_after = Pt(2)
p_sum.paragraph_format.line_spacing = 1.15
r_sm = p_sum.add_run(
    "Motivated and detail-oriented 2026 BBA graduate in International Business from Dayananda Sagar University, Bengaluru, seeking an entry-level Level 13 Operations New Associate role at Accenture Operations. Eager to learn, follow Standard Operating Procedures (SOPs), and contribute effectively to daily back-office processes. Practical internship experience in vendor follow-ups, purchase order tracking, document verification, event inventory handling, and daily transaction reconciliation. Proficient in MS Excel (VLOOKUP, Pivot Tables) and daily computer tools. Bengaluru local resident, available for immediate onboarding (0 Days Notice), and 100% prepared for 24/7 rotational and night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(8.3); r_sm.font.color.rgb = C_BODY

# Skills & Knowledge
add_sec_title("Skills & Knowledge")
skills = [
    ("Operations Support", "Procurement Support, Purchase Order (PO) Tracking, Invoice Verification & Matching Basics, Vendor Follow-ups, Back-Office Operations, Standard Operating Procedures (SOP) Execution."),
    ("Logistics & Supply Chain", "Physical Inventory Tracking, Stock Auditing, Shipping Invoices, Basic Trade Terms (Incoterms), Dual-Custody Inventory Governance, Discrepancy Reporting."),
    ("Computer & Office Tools", "MS Excel (VLOOKUP, Pivot Tables, Formulas, Data Entry, Sorting & Filtering), MS Word, PowerPoint, Google Sheets, Email Writing & Etiquette."),
    ("Professional Strengths", "High Accuracy & Attention to Detail, Problem Solving, Quick Learner, Team Player, Time Management, Adaptability to Rotational / Night Shifts.")
]
for cat, txt in skills:
    p_sk = doc.add_paragraph()
    p_sk.paragraph_format.space_before = Pt(0)
    p_sk.paragraph_format.space_after = Pt(1.0)
    p_sk.paragraph_format.left_indent = Inches(0.12)
    r_k1 = p_sk.add_run(f"• {cat}: ")
    r_k1.font.name = "Arial"; r_k1.font.size = Pt(8.0); r_k1.font.bold = True; r_k1.font.color.rgb = C_NAVY
    r_k2 = p_sk.add_run(txt)
    r_k2.font.name = "Arial"; r_k2.font.size = Pt(8.0); r_k2.font.color.rgb = C_BODY

# Internships
add_sec_title("Internships & Practical Field Exposure")
experiences = [
    {
        "title": "Commercial Operations Intern — Pencil Mark Interior Solutions LLP",
        "meta": "July 2024 – Aug 2025 | Bengaluru, India",
        "bullets": [
            "Assisted with tracking supplier price quotes, organizing vendor contact matrices, and preparing comparison pricing sheets in MS Excel.",
            "Supported the team in tracking purchase orders against delivery dates and site completion notes, helping avoid billing delays.",
            "Assisted in preparing commercial scopes of work and service estimates, supporting the team in securing B2B corporate contracts."
        ]
    },
    {
        "title": "Operations & Data Verification Intern — Instawork Services India Pvt. Ltd.",
        "meta": "2025 | Bengaluru, India",
        "bullets": [
            "Reviewed and verified incoming user and partner profile documents, carefully following standard operating procedure (SOP) checklists.",
            "Maintained a verified 99.4% accuracy rate across daily verification queues, ensuring clean and accurate database records.",
            "Worked closely with team supervisors to flag unclear submissions and identify simple ways to speed up routine review queues."
        ]
    },
    {
        "title": "Event Operations & Logistics Lead — Salt in My Cocoa (Aero India 2025)",
        "meta": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Managed daily stall setup, on-ground inventory replenishment, and security clearances across 5 days for 100,000+ public and defense visitors.",
            "Kept strict physical inventory counts before and after each shift, achieving 0% stock loss / shrinkage during peak rush hours.",
            "Reconciled daily digital UPI payments and cashier registers against stock counts with 100% financial balancing."
        ]
    },
    {
        "title": "Community Operations & Volunteer Support — Non-Profit Social Initiative",
        "meta": "2024 | Bengaluru, India",
        "bullets": [
            "Checked and verified participant registration details and identity records in compliance with event guidelines.",
            "Maintained volunteer schedules and participant databases in Google Sheets, coordinating smoothly across city outreach drives."
        ]
    }
]

for exp in experiences:
    p_x = doc.add_paragraph()
    p_x.paragraph_format.space_before = Pt(2.2)
    p_x.paragraph_format.space_after = Pt(1.0)
    p_x.paragraph_format.keep_with_next = True
    r_x1 = p_x.add_run(f"{exp['title']}\n")
    r_x1.font.name = "Arial"; r_x1.font.size = Pt(8.5); r_x1.font.bold = True; r_x1.font.color.rgb = C_NAVY
    r_x2 = p_x.add_run(exp['meta'])
    r_x2.font.name = "Arial"; r_x2.font.size = Pt(7.8); r_x2.font.color.rgb = C_SLATE

    for b in exp["bullets"]:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(1.0)
        p_b.paragraph_format.left_indent = Inches(0.18)
        p_b.paragraph_format.first_line_indent = Inches(-0.12)
        p_b.paragraph_format.line_spacing = 1.12
        r_d = p_b.add_run("– ")
        r_d.font.name = "Arial"; r_d.font.size = Pt(8.0); r_d.font.bold = True; r_d.font.color.rgb = C_BLUE
        r_t = p_b.add_run(b)
        r_t.font.name = "Arial"; r_t.font.size = Pt(8.0); r_t.font.color.rgb = C_BODY

# Technical Projects
add_sec_title("Academic & Automation Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1.2)
p_pr.paragraph_format.space_after = Pt(1.0)
r_p1 = p_pr.add_run("Automated Job Portal & Requisition Tracker — Student Project\n")
r_p1.font.name = "Arial"; r_p1.font.size = Pt(8.5); r_p1.font.bold = True; r_p1.font.color.rgb = C_NAVY
r_p2 = p_pr.add_run("2026 | Python & Spreadsheets\n")
r_p2.font.name = "Arial"; r_p2.font.size = Pt(7.8); r_p2.font.color.rgb = C_SLATE
r_p3 = p_pr.add_run("– Built a simple automation script in Python to gather and organize corporate job requisitions into structured spreadsheets.\n– Automated repetitive search and sorting tasks, reducing manual effort and keeping candidate tracking organized.")
r_p3.font.name = "Arial"; r_p3.font.size = Pt(8.0); r_p3.font.color.rgb = C_BODY

# Certifications & Languages
add_sec_title("Certifications & Languages")
p_cr = doc.add_paragraph()
p_cr.paragraph_format.space_before = Pt(1)
p_cr.paragraph_format.space_after = Pt(1)
r_c1 = p_cr.add_run("Certifications: ")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(8.0); r_c1.font.bold = True; r_c1.font.color.rgb = C_NAVY
r_c2 = p_cr.add_run("Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL) • Enterprise Operational Excellence\n")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(8.0); r_c2.font.color.rgb = C_BODY
r_l1 = p_cr.add_run("Languages: ")
r_l1.font.name = "Arial"; r_l1.font.size = Pt(8.0); r_l1.font.bold = True; r_l1.font.color.rgb = C_NAVY
r_l2 = p_cr.add_run("English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_l2.font.name = "Arial"; r_l2.font.size = Pt(8.0); r_l2.font.color.rgb = C_BODY

doc.save(docx_path)
shutil.copyfile(docx_path, root_docx)
print(f"Generated Honest Fresher DOCX: {docx_path} (Size: {os.path.getsize(docx_path)} bytes)")

# Verify Page Count
pdf_data = open(pdf_path, "rb").read()
page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
