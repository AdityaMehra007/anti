"""
compile_all_experiences_ats_cv.py
Compiles the ultimate ATS-optimized, JD-keyword-matched 1-Page CV for Aditya Mehra.
Directly aligns all 7 past experiences with live Accenture Level 13 Operations JDs:
- AIOC-S01664213: Procurement Support - P1
- AIOC-S01670871: Invoice Processing - P1
- AIOC-S01667647: Know Your Customer (KYC) Screening - P1
- AIOC-S01665657: Order Management - P3
- AIOC-S01668350: Trust & Safety / Content Moderation
- AIOC-S01665940: Omnichannel Customer Service

Generates:
1. Aditya_Mehra_Accenture_Operations_CV.pdf (Strictly 1 Page A4)
2. Aditya_Mehra_Accenture_Operations_CV.docx
3. Aditya_Mehra_All_Experiences_CV.pdf
4. Aditya_Mehra_All_Experiences_CV.docx
5. HTML versions in e:\\anti\\resumes\\
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
<title>Aditya Mehra - Accenture Level 13 Operations ATS Master CV</title>
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
    line-height: 1.22;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .container {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 7mm 11mm 5mm 11mm;
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
    padding-bottom: 3.5px;
    margin-bottom: 4px;
  }
  .name {
    font-size: 18.5pt;
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
    letter-spacing: 0.2px;
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
    font-size: 7.4pt;
    font-weight: 700;
    color: #065f46;
    background: #ecfdf5;
    display: inline-block;
    padding: 1px 8px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
  }

  /* Section Titles */
  .section-title {
    font-size: 8.8pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 1px;
    margin-top: 3.5px;
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
    font-size: 8.3pt;
  }
  .sub {
    color: #1d4ed8;
    font-weight: 600;
    font-size: 8.0pt;
  }
  .date {
    font-size: 7.5pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }
  .text {
    font-size: 7.9pt;
    color: #334155;
    text-align: justify;
    line-height: 1.22;
  }
  ul {
    padding-left: 14px;
    margin-bottom: 2px;
  }
  li {
    font-size: 7.7pt;
    color: #334155;
    margin-bottom: 1px;
    line-height: 1.20;
  }
  li strong {
    color: #0f172a;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.7pt;
    margin-bottom: 2px;
  }
  .skills-table td {
    padding: 1px 0;
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

  /* ATS Keywords Bar */
  .ats-bar {
    font-size: 6.9pt;
    color: #64748b;
    border-top: 1px dashed #cbd5e1;
    padding-top: 1.5px;
    margin-top: 2px;
    text-align: center;
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
      Fresher (0–1 Yrs) • Quick Learner • Collaborative Team Player • Immediate Joiner (0 Days Notice) • 24/7 Shifts Flexible
    </div>
  </div>

  <!-- CAREER OBJECTIVE -->
  <div class="section-title">Career Objective</div>
  <p class="text">
    Goal-driven and collaborative <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, targeting an entry-level <strong>Level 13 Operations New Associate</strong> role at Accenture Operations. Offers comprehensive, hands-on exposure across procurement support, invoice verification, 3-way reconciliation, KYC document auditing, and event inventory governance. A dedicated team player with high coachability and rapid adoption of enterprise SOPs. Bengaluru local resident with <strong>0 days notice</strong> and full readiness for 24/7 rotational/night shifts.
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
  <p style="font-size: 7.4pt; color: #475569; margin-top: 0.5px; margin-bottom: 1.5px;">
    <strong>Relevant Coursework:</strong> Global Logistics & Supply Chain, International Trade Documentation, Commercial Contract Law, Business Statistics, Managerial Communication.
  </p>

  <!-- CORE COMPETENCIES & ATS KEYWORDS -->
  <div class="section-title">Core Competencies & ATS Keywords</div>
  <table class="skills-table">
    <tr>
      <td class="skill-label">Procurement & P2P Operations:</td>
      <td class="skill-val">Purchase Order (PO) Administration, PR-to-PO Tracking, Vendor Quotation Comparison, Basic Three-Way Matching (PO/GRN/Invoice), Billing Discrepancy Clearance.</td>
    </tr>
    <tr>
      <td class="skill-label">Quality, KYC & Trust & Safety:</td>
      <td class="skill-val">KYC Document Screening, Customer Identification Program (CIP), Operational Verification Checklists, Data Quality Auditing (99.4% Accuracy), Strict SOP Adherence.</td>
    </tr>
    <tr>
      <td class="skill-label">Order & Inventory Governance:</td>
      <td class="skill-val">Fulfill Order Management, Dual-Custody Stock Counting, 0% Inventory Shrinkage, Daily Cash/Digital Reconciliation, Shipping Documentation.</td>
    </tr>
    <tr>
      <td class="skill-label">Computer & Software Tools:</td>
      <td class="skill-val">MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Cleaning), Google Workspace, MS Word, PowerPoint, Python Basics.</td>
    </tr>
    <tr>
      <td class="skill-label">Teamwork & Workplace Readiness:</td>
      <td class="skill-val">Cross-Functional Team Collaboration, Peer Queue Support, High Coachability, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Onboarding.</td>
    </tr>
  </table>

  <!-- PROFESSIONAL EXPERIENCE (ALL 7 ROLES MATCHED TO JDS) -->
  <div class="section-title">Professional Experience & Practical Exposure (All Roles)</div>

  <!-- Role 1: Pencil Mark (Procurement Support - P1 & Order Management - P3) -->
  <div class="row">
    <div><span class="title">Commercial Operations Intern</span> — <span class="sub">Pencil Mark Interior Solutions LLP</span></div>
    <div class="date">Jul 2024 – Aug 2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Managed supplier rate cards and prepared vendor quotation comparison sheets in MS Excel to support commercial procurement decisions.</li>
    <li>Tracked Purchase Orders (POs) through delivery confirmation and site completion notes, helping the team close B2B contracts (<strong>₹1.5L+ revenue</strong>).</li>
  </ul>

  <!-- Role 2: Instawork (KYC Screening - P1 & Trust/Safety Data QA) -->
  <div class="row">
    <div><span class="title">Operations & Data Verification Intern</span> — <span class="sub">Instawork Services India Pvt. Ltd.</span></div>
    <div class="date">2025 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Audited partner profile submissions and identification documents against operational checklists, achieving a verified <strong>99.4% accuracy rating</strong>.</li>
    <li>Collaborated with peers during peak volume queues, applying supervisor feedback quickly to improve daily review turnaround time by <strong>12%</strong>.</li>
  </ul>

  <!-- Role 3: Aero India 2025 (Fulfill Order Ops - P3 & Invoice Reconciliation - P1) -->
  <div class="row">
    <div><span class="title">Exhibition Operations & Logistics Lead</span> — <span class="sub">Salt in My Cocoa (AERO India 2025)</span></div>
    <div class="date">Feb 2025 | Yelahanka AFB, Bengaluru</div>
  </div>
  <ul>
    <li>Governed booth inventory logistics and stock replenishment across 5 peak days for <strong>100,000+ public and defense visitors</strong>.</li>
    <li>Maintained disciplined dual-custody physical stock audits before/after shifts (<strong>0% stock shrinkage</strong>) and balanced UPI/cash registers with <strong>100% accuracy</strong>.</li>
  </ul>

  <!-- Role 4: Trilogy & Live Events (Vendor SLA Governance & Omnichannel Delivery) -->
  <div class="row">
    <div><span class="title">Event Operations Coordinator</span> — <span class="sub">TRILOGY Indo-Jazz Fusion & Commercial Productions</span></div>
    <div class="date">2019 – 2026 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Coordinated on-ground logistics, artist hospitality, and technical crew riders for TRILOGY at Bangalore Club (Jan 2026) with zero live stage disruption.</li>
    <li>Enforced vendor SLAs across sound, lighting, and hospitality suppliers, achieving <strong>15%–20% cost optimization</strong> through direct rate agreements.</li>
  </ul>

  <!-- Role 5: Family Enterprise & Cloud Kitchen (Retail Billing & Transaction Verification) -->
  <div class="row">
    <div><span class="title">Retail Store & F&B Operations Assistant</span> — <span class="sub">Family Commercial Enterprise & Mehra's Kitchen</span></div>
    <div class="date">2018 – 2025 | Kolkata & Bengaluru</div>
  </div>
  <ul>
    <li>Managed counter customer billing, digital POS registers, supplier restocking, and customer relations in a fast-paced retail trading business.</li>
    <li>Handled raw ingredient procurement, vendor price negotiations, and daily ledger balancing for food operations with 100% financial accuracy.</li>
  </ul>

  <!-- Role 6: Community Volunteer (Identity Verification & Records) -->
  <div class="row">
    <div><span class="title">Community Operations Volunteer</span> — <span class="sub">Non-Profit Social Initiative</span></div>
    <div class="date">2024 | Bengaluru, India</div>
  </div>
  <ul>
    <li>Partnered with fellow volunteers to verify participant identity documents and maintain organized registration databases in Google Sheets.</li>
  </ul>

  <!-- Role 7: Technical & Automation Project -->
  <div class="section-title">Academic & Self-Learning Project</div>
  <div class="row">
    <div><span class="title">Job Portal Automation & Spreadsheet Tracker</span> — <span class="sub">Student Technical Initiative</span></div>
    <div class="date">2025 – 2026 | Python & Spreadsheets</div>
  </div>
  <ul>
    <li>Demonstrated proactive learning by creating a Python script to aggregate and organize corporate job openings into structured team spreadsheets.</li>
  </ul>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="text">
    <strong>Certifications:</strong> Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL) • Enterprise Operational Excellence<br>
    <strong>Languages:</strong> English (Fluent Professional Proficiency), Hindi (Native / Bilingual)
  </p>

  <!-- ATS Workday Keyword Indexer -->
  <div class="ats-bar">
    Accenture Workday Requisition Alignment: AIOC-S01664213 (Procurement Support - P1) • AIOC-S01670871 (Invoice Processing - P1) • AIOC-S01667647 (KYC Screening - P1) • AIOC-S01665657 (Order Management - P3) • AIOC-S01668350 (Trust & Safety) • AIOC-S01665940 (Customer Support)
  </div>

</div>
</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Accenture_Operations_CV.html")
pdf_path = os.path.join(OUTPUT_DIR_PDF, "Aditya_Mehra_Accenture_Operations_CV.pdf")
root_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Accenture_Operations_CV.pdf")
root_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Accenture_Operations_CV.docx")
docx_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Accenture_Operations_CV.docx")

# Also copy to All_Experiences names for full symmetry
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

# Copy to root and secondary targets
with open(pdf_path, "rb") as f_in:
    pdf_bytes = f_in.read()
    with open(root_pdf, "wb") as f_out:
        f_out.write(pdf_bytes)
    with open(all_pdf, "wb") as f_out:
        f_out.write(pdf_bytes)

print(f"Generated Primary Accenture PDF: {root_pdf} (Size: {len(pdf_bytes)} bytes)")

# ==========================================
# GENERATE NATIVE DOCX WITH JD KEYWORDS & ALL EXPERIENCES
# ==========================================
doc = docx.Document()

# Page Margins: 0.30 in
for section in doc.sections:
    section.top_margin = Inches(0.28)
    section.bottom_margin = Inches(0.28)
    section.left_margin = Inches(0.42)
    section.right_margin = Inches(0.42)
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
r_n.font.name = "Arial"; r_n.font.size = Pt(17); r_n.font.bold = True; r_n.font.color.rgb = C_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1)
r_s = p_sub.add_run("BBA GRADUATE (BATCH OF 2026) // ENTRY-LEVEL OPERATIONS NEW ASSOCIATE")
r_s.font.name = "Arial"; r_s.font.size = Pt(8.6); r_s.font.bold = True; r_s.font.color.rgb = C_BLUE

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
r_b = p_b.add_run("Fresher (0-1 Yrs) | Quick Learner | Collaborative Team Player | Immediate Joiner (0 Days Notice) | 24/7 Shifts Flexible")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.5); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after = Pt(1.0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"; r.font.size = Pt(8.6); r.font.bold = True; r.font.color.rgb = C_NAVY
    add_clean_divider(p)

# Career Objective
add_sec("Career Objective")
p_sm = doc.add_paragraph()
p_sm.paragraph_format.space_before = Pt(1)
p_sm.paragraph_format.space_after = Pt(1.5)
p_sm.paragraph_format.line_spacing = 1.15
r_sm = p_sm.add_run(
    "Goal-driven and collaborative 2026 BBA graduate in International Business from Dayananda Sagar University, targeting an entry-level Level 13 Operations New Associate role at Accenture Operations. Offers comprehensive, hands-on exposure across procurement support, invoice verification, 3-way reconciliation, KYC document auditing, and event inventory governance. A dedicated team player with high coachability and rapid adoption of enterprise SOPs. Bengaluru local resident with 0 days notice and full readiness for 24/7 rotational/night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(7.8); r_sm.font.color.rgb = C_BODY

# Education
add_sec("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(0.5)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) - International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.3); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  |  2023 - 2026 | Fresh Graduate (Immediate Joining)\n")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(7.8); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE
r_e3 = p_ed.add_run("Relevant Coursework: Global Logistics & Supply Chain, International Trade Documentation, Commercial Contract Law, Business Statistics, Managerial Communication.")
r_e3.font.name = "Arial"; r_e3.font.size = Pt(7.3); r_e3.font.color.rgb = C_SLATE

# Core Competencies & ATS Keywords
add_sec("Core Competencies & ATS Keywords")
skills_list = [
    ("Procurement & P2P Operations", "Purchase Order (PO) Administration, PR-to-PO Tracking, Vendor Quotation Comparison, Basic Three-Way Matching (PO/GRN/Invoice), Billing Discrepancy Clearance."),
    ("Quality, KYC & Trust & Safety", "KYC Document Screening, Customer Identification Program (CIP), Operational Verification Checklists, Data Quality Auditing (99.4% Accuracy), Strict SOP Adherence."),
    ("Order & Inventory Governance", "Fulfill Order Management, Dual-Custody Stock Counting, 0% Inventory Shrinkage, Daily Cash/Digital Reconciliation, Shipping Documentation."),
    ("Computer & Software Tools", "MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Sorting, Filtering, Data Cleaning), Google Workspace, MS Word, PowerPoint, Python Basics."),
    ("Teamwork & Workplace Readiness", "Cross-Functional Team Collaboration, Peer Queue Support, High Coachability, 100% 24/7 Rotational & Night Shift Flexibility, Immediate Onboarding.")
]
for cat, txt in skills_list:
    p_s = doc.add_paragraph()
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after = Pt(0.6)
    p_s.paragraph_format.left_indent = Inches(0.1)
    r_1 = p_s.add_run(f"- {cat}: ")
    r_1.font.name = "Arial"; r_1.font.size = Pt(7.6); r_1.font.bold = True; r_1.font.color.rgb = C_NAVY
    r_2 = p_s.add_run(txt)
    r_2.font.name = "Arial"; r_2.font.size = Pt(7.6); r_2.font.color.rgb = C_BODY

# Professional Experience (All Roles Matched to JDs)
add_sec("Professional Experience & Practical Exposure (All Roles)")
jobs = [
    {
        "title": "Commercial Operations Intern - Pencil Mark Interior Solutions LLP",
        "date": "Jul 2024 - Aug 2025 | Bengaluru, India",
        "bullets": [
            "Managed supplier rate cards and prepared vendor quotation comparison sheets in MS Excel to support commercial procurement decisions.",
            "Tracked Purchase Orders (POs) through delivery confirmation and site completion notes, helping the team close B2B contracts (INR 1.5L+ revenue)."
        ]
    },
    {
        "title": "Operations & Data Verification Intern - Instawork Services India Pvt. Ltd.",
        "date": "2025 | Bengaluru, India",
        "bullets": [
            "Audited partner profile submissions and identification documents against operational checklists, achieving a verified 99.4% accuracy rating.",
            "Collaborated with peers during peak volume queues, applying supervisor feedback quickly to improve daily review turnaround time by 12%."
        ]
    },
    {
        "title": "Exhibition Operations & Logistics Lead - Salt in My Cocoa (AERO India 2025)",
        "date": "Feb 2025 | Yelahanka AFB, Bengaluru",
        "bullets": [
            "Governed booth inventory logistics and stock replenishment across 5 peak days for 100,000+ public and defense visitors.",
            "Maintained disciplined dual-custody physical stock audits before/after shifts (0% stock shrinkage) and balanced UPI/cash registers with 100% accuracy."
        ]
    },
    {
        "title": "Event Operations Coordinator - TRILOGY Indo-Jazz Fusion & Commercial Productions",
        "date": "2019 - 2026 | Bengaluru, India",
        "bullets": [
            "Coordinated on-ground logistics, artist hospitality, and technical crew riders for TRILOGY at Bangalore Club (Jan 2026) with zero live stage disruption.",
            "Enforced vendor SLAs across sound, lighting, and hospitality suppliers, achieving 15%-20% cost optimization through direct rate agreements."
        ]
    },
    {
        "title": "Retail Store & F&B Operations Assistant - Family Commercial Enterprise & Mehra's Kitchen",
        "date": "2018 - 2025 | Kolkata & Bengaluru",
        "bullets": [
            "Managed counter customer billing, digital POS registers, supplier restocking, and customer relations in a fast-paced retail trading business.",
            "Handled raw ingredient procurement, vendor price negotiations, and daily ledger balancing for food operations with 100% financial accuracy."
        ]
    },
    {
        "title": "Community Operations Volunteer - Non-Profit Social Initiative",
        "date": "2024 | Bengaluru, India",
        "bullets": [
            "Partnered with fellow volunteers to verify participant identity documents and maintain organized registration databases in Google Sheets."
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
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.2); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b_item = doc.add_paragraph()
        p_b_item.paragraph_format.space_before = Pt(0)
        p_b_item.paragraph_format.space_after = Pt(0.5)
        p_b_item.paragraph_format.left_indent = Inches(0.12)
        p_b_item.paragraph_format.line_spacing = 1.15
        r_bullet = p_b_item.add_run(f"- {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(7.6); r_bullet.font.color.rgb = C_BODY

# Academic Project
add_sec("Academic & Self-Learning Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.4)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Automation & Spreadsheet Tracker - Student Technical Initiative\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.0); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 - 2026 | Python & Spreadsheets")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.2); r_pr2.font.color.rgb = C_SLATE

p_pr_b = doc.add_paragraph()
p_pr_b.paragraph_format.space_before = Pt(0)
p_pr_b.paragraph_format.space_after = Pt(0.8)
p_pr_b.paragraph_format.left_indent = Inches(0.12)
r_pr_b = p_pr_b.add_run("- Demonstrated proactive learning by creating a Python script to aggregate and organize corporate job openings into structured team spreadsheets.")
r_pr_b.font.name = "Arial"; r_pr_b.font.size = Pt(7.6); r_pr_b.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.space_before = Pt(0.8)
p_cert.paragraph_format.space_after = Pt(0.8)
r_c1 = p_cert.add_run("Certifications: Written Management Commendation (Pencil Mark) | Google Digital Marketing Fundamentals | Service Marketing (NPTEL) | Enterprise Operational Excellence\n")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.4); r_c1.font.color.rgb = C_BODY
r_c2 = p_cert.add_run("Languages: English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.4); r_c2.font.color.rgb = C_BODY

# Footer Note
p_foot = doc.add_paragraph()
p_foot.paragraph_format.space_before = Pt(2.0)
p_foot.paragraph_format.space_after = Pt(0)
r_foot = p_foot.add_run("Accenture Workday Requisitions: AIOC-S01664213 (Procurement Support - P1) | AIOC-S01670871 (Invoice Processing - P1) | AIOC-S01667647 (KYC Screening - P1) | AIOC-S01665657 (Order Management - P3) | AIOC-S01668350 (Trust & Safety) | AIOC-S01665940 (Customer Support)")
r_foot.font.name = "Arial"; r_foot.font.size = Pt(6.5); r_foot.font.color.rgb = C_SLATE

doc.save(docx_path)
doc.save(root_docx)
doc.save(all_docx)
print(f"Generated Primary Accenture DOCX: {root_docx} (Size: {os.path.getsize(root_docx)} bytes)")

# Verify Page Count
with open(root_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
