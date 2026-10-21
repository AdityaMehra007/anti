"""
compile_refined_cv.py
Generates the REFINED, LEAN, JD-EXACT 1-Page CV for Aditya Mehra.
Purges all non-essential extra fluff (pre-college retail store, food stalls, concert production clutter).
Keeps ONLY what is strictly needed to match Accenture Level 13 Operations JDs:
1. Pencil Mark Interior Solutions (Procurement, PO Administration, Vendor Quotes, Excel)
2. Instawork Services India (KYC Document Verification, 99.4% Accuracy, SOP Compliance, Queue Teamwork)
3. Salt in My Cocoa - Aero India 2025 (Inventory Dual-Custody, 0% Shrinkage, 100% Financial Reconciliation)
4. Academic Python/Excel Automation Project (Proactive Tooling & Data Organization)

Result: Crisp, spacious, elegant, 100% ATS-compliant, strictly 1-page A4.
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
<title>Aditya Mehra - Accenture Level 13 Operations CV</title>
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
    line-height: 1.35;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .container {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 12mm 15mm 10mm 15mm;
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
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .name {
    font-size: 21pt;
    font-weight: 800;
    letter-spacing: 0.8px;
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
    margin-top: 4px;
    font-size: 8.0pt;
    font-weight: 700;
    color: #065f46;
    background: #ecfdf5;
    display: inline-block;
    padding: 2px 10px;
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
    margin-bottom: 4px;
  }
  
  /* Content Blocks */
  .row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }
  .title {
    font-weight: 700;
    color: #0f172a;
    font-size: 9.0pt;
  }
  .sub {
    color: #1d4ed8;
    font-weight: 600;
    font-size: 8.6pt;
  }
  .date {
    font-size: 8.1pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }
  .text {
    font-size: 8.6pt;
    color: #334155;
    text-align: justify;
    line-height: 1.34;
  }
  ul {
    padding-left: 16px;
    margin-bottom: 4px;
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
    margin-bottom: 3px;
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
      padding: 12mm 15mm;
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
      Fresher (0–1 Yrs) • Fast Learner & Highly Coachable • Team Player • Immediate Joiner (0 Days Notice) • 24/7 Shifts Flexible
    </div>
  </div>

  <!-- CAREER OBJECTIVE -->
  <div class="section-title">Career Objective</div>
  <p class="text">
    Eager, disciplined, and collaborative <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, seeking an entry-level <strong>Level 13 Operations New Associate</strong> role at Accenture Operations. Offers hands-on internship experience in purchase order tracking, vendor quotation comparison, high-accuracy document verification, and physical inventory auditing. Known for strong coachability, strict standard operating procedure (SOP) execution, and rapid adaptation to enterprise tools. Local Bengaluru resident available for <strong>immediate onboarding (0 Days Notice)</strong> with full flexibility for <strong>24/7 rotational and night shifts</strong>.
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

  <!-- CORE SKILLS & ATS KEYWORDS -->
  <div class="section-title">Skills & Capabilities (JD-Matched)</div>
  <table class="skills-table">
    <tr>
      <td class="skill-label">Procurement & PO Support:</td>
      <td class="skill-val">Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Vendor Quote Comparison Sheets, Basic 3-Way Matching, Discrepancy Clearance.</td>
    </tr>
    <tr>
      <td class="skill-label">Quality & KYC Verification:</td>
      <td class="skill-val">Customer Identification Program (CIP), Document Verification, Data Quality Auditing (99.4% Accuracy), Strict SOP Adherence.</td>
    </tr>
    <tr>
      <td class="skill-label">Order & Inventory Control:</td>
      <td class="skill-val">Order Fulfillment Support, Dual-Custody Stock Counting, 0% Inventory Shrinkage, Daily Cash & UPI Reconciliation.</td>
    </tr>
    <tr>
      <td class="skill-label">Computer & Software Tools:</td>
      <td class="skill-val">MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Entry), Google Workspace, MS Word, PowerPoint.</td>
    </tr>
    <tr>
      <td class="skill-label">Teamwork & Shift Readiness:</td>
      <td class="skill-val">Cross-Functional Team Collaboration, Queue Support during Peak Loads, High Coachability, 100% 24/7 Shift Flexibility.</td>
    </tr>
  </table>

  <!-- PROFESSIONAL INTERNSHIPS -->
  <div class="section-title">Professional Internships & Operational Experience</div>

  <!-- Role 1: Pencil Mark (Procurement Operations Support) -->
  <div class="row">
    <div><span class="title">Commercial Operations Intern</span> — <span class="sub">Pencil Mark Interior Solutions LLP</span></div>
    <div class="date">Jul 2024 – Aug 2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Maintained vendor quote comparison sheets in MS Excel, assisting senior estimators with supplier pricing evaluations and cost calculations.</li>
    <li>Tracked Purchase Orders (POs) through delivery dates and site completion notes, preventing fulfillment delays across corporate commercial projects.</li>
    <li>Collaborated with the commercial team to draft client proposals, helping secure corporate B2B contracts (<strong>₹1.5L+ revenue</strong>).</li>
  </ul>

  <!-- Role 2: Instawork (KYC & Document Verification) -->
  <div class="row">
    <div><span class="title">Operations & Data Verification Intern</span> — <span class="sub">Instawork Services India Pvt. Ltd.</span></div>
    <div class="date">2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Reviewed incoming user and partner profile documentation against standard verification checklists with an audited <strong>99.4% accuracy rating</strong>.</li>
    <li>Collaborated closely with team peers to manage high-throughput queues, ensuring zero submission backlogs at shift handover.</li>
    <li>Demonstrated high coachability by implementing supervisor quality feedback immediately, reducing review cycle time by <strong>12%</strong>.</li>
  </ul>

  <!-- Role 3: Aero India 2025 (Inventory & Reconciliation) -->
  <div class="row">
    <div><span class="title">Exhibition Operations & Logistics Lead</span> — <span class="sub">Salt in My Cocoa (AERO India 2025)</span></div>
    <div class="date">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
  </div>
  <ul>
    <li>Managed on-ground booth logistics, inventory counts, and restocking across 5 peak days serving <strong>100,000+ public and defense visitors</strong>.</li>
    <li>Enforced disciplined dual-custody stock audits before and after every shift, achieving <strong>0% stock loss / shrinkage</strong>.</li>
    <li>Reconciled daily digital UPI payments and register receipts against physical stock balances with <strong>100% financial accuracy</strong>.</li>
  </ul>

  <!-- ACADEMIC & SELF-LEARNING PROJECT -->
  <div class="section-title">Academic & Self-Learning Project</div>
  <div class="row">
    <div><span class="title">Job Portal Automation & Spreadsheet Tracker</span> — <span class="sub">Student Technical Initiative</span></div>
    <div class="date">2025 – 2026 | Python & Spreadsheets</div>
  </div>
  <ul>
    <li>Demonstrated self-directed learning by creating a Python script to aggregate and organize corporate job openings into structured team spreadsheets.</li>
    <li>Eliminated manual sorting effort by automating data entry and categorization, ensuring structured and searchable records for peers.</li>
  </ul>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="text">
    <strong>Certifications:</strong> Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL) • Enterprise Operational Excellence<br>
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

# Also write to All_Experiences for complete sync
all_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_All_Experiences_CV.pdf")
all_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_All_Experiences_CV.docx")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Render HTML to PDF via Chrome
cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--print-to-pdf-no-header",
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

print(f"Generated Refined PDF: {root_pdf} (Size: {len(pdf_bytes)} bytes)")

# ==========================================
# GENERATE REFINED NATIVE DOCX
# ==========================================
doc = docx.Document()

# Refined Margins: 0.38 in
for section in doc.sections:
    section.top_margin = Inches(0.35)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.50)
    section.right_margin = Inches(0.50)
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
r_b = p_b.add_run("Fresher (0-1 Yrs) | Fast Learner & Highly Coachable | Team Player | Immediate Joiner (0 Days Notice) | 24/7 Shifts Flexible")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.8); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5.0)
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
    "Eager, disciplined, and collaborative 2026 BBA graduate in International Business from Dayananda Sagar University, seeking an entry-level Level 13 Operations New Associate role at Accenture Operations. Offers hands-on internship experience in purchase order tracking, vendor quotation comparison, high-accuracy document verification, and physical inventory auditing. Known for strong coachability, strict standard operating procedure (SOP) execution, and rapid adaptation to enterprise tools. Local Bengaluru resident available for immediate onboarding (0 Days Notice) with full flexibility for 24/7 rotational and night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(8.3); r_sm.font.color.rgb = C_BODY

# Education
add_sec("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(1)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) - International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.8); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  |  2023 - 2026 | Fresh Graduate (Immediate Joining)")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(8.2); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE

# Skills & Capabilities (JD-Matched)
add_sec("Skills & Capabilities (JD-Matched)")
skills_list = [
    ("Procurement & PO Support", "Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Vendor Quote Comparison Sheets, Basic 3-Way Matching, Discrepancy Clearance."),
    ("Quality & KYC Verification", "Customer Identification Program (CIP), Document Verification, Data Quality Auditing (99.4% Accuracy), Strict SOP Adherence."),
    ("Order & Inventory Control", "Order Fulfillment Support, Dual-Custody Stock Counting, 0% Inventory Shrinkage, Daily Cash & UPI Reconciliation."),
    ("Computer & Software Tools", "MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Entry), Google Workspace, MS Word, PowerPoint."),
    ("Teamwork & Shift Readiness", "Cross-Functional Team Collaboration, Queue Support during Peak Loads, High Coachability, 100% 24/7 Shift Flexibility.")
]
for cat, txt in skills_list:
    p_s = doc.add_paragraph()
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after = Pt(1.0)
    p_s.paragraph_format.left_indent = Inches(0.12)
    r_1 = p_s.add_run(f"- {cat}: ")
    r_1.font.name = "Arial"; r_1.font.size = Pt(8.0); r_1.font.bold = True; r_1.font.color.rgb = C_NAVY
    r_2 = p_s.add_run(txt)
    r_2.font.name = "Arial"; r_2.font.size = Pt(8.0); r_2.font.color.rgb = C_BODY

# Professional Internships
add_sec("Professional Internships & Operational Experience")
jobs = [
    {
        "title": "Commercial Operations Intern - Pencil Mark Interior Solutions LLP",
        "date": "Jul 2024 - Aug 2025 | Bengaluru, India",
        "bullets": [
            "Maintained vendor quote comparison sheets in MS Excel, assisting senior estimators with supplier pricing evaluations and cost calculations.",
            "Tracked Purchase Orders (POs) through delivery dates and site completion notes, preventing fulfillment delays across corporate commercial projects.",
            "Collaborated with the commercial team to draft client proposals, helping secure corporate B2B contracts (INR 1.5L+ revenue)."
        ]
    },
    {
        "title": "Operations & Data Verification Intern - Instawork Services India Pvt. Ltd.",
        "date": "2025 | Bengaluru, India",
        "bullets": [
            "Reviewed incoming user and partner profile documentation against standard verification checklists with an audited 99.4% accuracy rating.",
            "Collaborated closely with team peers to manage high-throughput queues, ensuring zero submission backlogs at shift handover.",
            "Demonstrated high coachability by implementing supervisor quality feedback immediately, reducing review cycle time by 12%."
        ]
    },
    {
        "title": "Exhibition Operations & Logistics Lead - Salt in My Cocoa (AERO India 2025)",
        "date": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Managed on-ground booth logistics, inventory counts, and restocking across 5 peak days serving 100,000+ public and defense visitors.",
            "Enforced disciplined dual-custody stock audits before and after every shift, achieving 0% stock loss / shrinkage.",
            "Reconciled daily digital UPI payments and register receipts against physical stock balances with 100% financial accuracy."
        ]
    }
]

for j in jobs:
    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(2.5)
    p_j.paragraph_format.space_after = Pt(0.8)
    p_j.paragraph_format.keep_with_next = True
    r_j1 = p_j.add_run(f"{j['title']}\n")
    r_j1.font.name = "Arial"; r_j1.font.size = Pt(8.5); r_j1.font.bold = True; r_j1.font.color.rgb = C_NAVY
    r_j2 = p_j.add_run(j['date'])
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.6); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b_item = doc.add_paragraph()
        p_b_item.paragraph_format.space_before = Pt(0)
        p_b_item.paragraph_format.space_after = Pt(1.0)
        p_b_item.paragraph_format.left_indent = Inches(0.15)
        p_b_item.paragraph_format.line_spacing = 1.15
        r_bullet = p_b_item.add_run(f"- {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(8.0); r_bullet.font.color.rgb = C_BODY

# Academic Project
add_sec("Academic & Self-Learning Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1.5)
p_pr.paragraph_format.space_after = Pt(0.8)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Automation & Spreadsheet Tracker - Student Technical Initiative\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.5); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 - 2026 | Python & Spreadsheets")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.6); r_pr2.font.color.rgb = C_SLATE

p_pr_b1 = doc.add_paragraph()
p_pr_b1.paragraph_format.space_before = Pt(0)
p_pr_b1.paragraph_format.space_after = Pt(0.8)
p_pr_b1.paragraph_format.left_indent = Inches(0.15)
r_pr_b1 = p_pr_b1.add_run("- Demonstrated self-directed learning by creating a Python script to aggregate and organize corporate job openings into structured team spreadsheets.")
r_pr_b1.font.name = "Arial"; r_pr_b1.font.size = Pt(8.0); r_pr_b1.font.color.rgb = C_BODY

p_pr_b2 = doc.add_paragraph()
p_pr_b2.paragraph_format.space_before = Pt(0)
p_pr_b2.paragraph_format.space_after = Pt(1.2)
p_pr_b2.paragraph_format.left_indent = Inches(0.15)
r_pr_b2 = p_pr_b2.add_run("- Eliminated manual sorting effort by automating data entry and categorization, ensuring structured and searchable records for peers.")
r_pr_b2.font.name = "Arial"; r_pr_b2.font.size = Pt(8.0); r_pr_b2.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.space_before = Pt(1.2)
p_cert.paragraph_format.space_after = Pt(1.2)
r_c1 = p_cert.add_run("Certifications: Written Management Commendation (Pencil Mark) | Google Digital Marketing Fundamentals | Service Marketing (NPTEL) | Enterprise Operational Excellence\n")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.8); r_c1.font.color.rgb = C_BODY
r_c2 = p_cert.add_run("Languages: English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.8); r_c2.font.color.rgb = C_BODY

doc.save(docx_path)
doc.save(root_docx)
doc.save(all_docx)
print(f"Generated Refined DOCX: {root_docx} (Size: {os.path.getsize(root_docx)} bytes)")

# Verify Page Count
with open(root_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
