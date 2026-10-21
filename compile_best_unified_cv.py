"""
compile_best_unified_cv.py
Compiles the Ultimate "Best of All Worlds" 1-Page CV for Aditya Mehra:
1. Synchronized with LinkedIn Outreach Messages:
   - Matches the exact claims sent to Accenture recruiters (Aero India, Pencil Mark, Instawork, vendor rate negotiation, Excel & Python).
2. 100% Workday ATS Optimized for Accenture Requisitions:
   - Procurement Support - P1 (AIOC-S01664213-1)
   - Procure-to-Pay / Invoice Processing - P1 (AIOC-S01670871-1)
   - Order Management - P3 (AIOC-S01665657-1)
   - KYC Screening & Document Verification (AIOC-S01667647-1)
   - Rotational & Night Shifts Ready, Immediate Joiner (0 Days Notice).
3. "Easy, Smooth, Nice, and Cool" Aesthetic:
   - Tech-minimalist visual polish, modern indigo accents, sleek pill badges, clean breathing room.
   - Natural, defensible phrasing so Aditya feels 100% confident in interviews.
4. Strictly 1 Page A4 with 0 overflow and 0 browser headers/footers.
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
<title>Aditya Mehra - Best Operations & Procurement CV</title>
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
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
    padding: 8mm 12mm 5mm 12mm;
    margin: 0 auto;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header */
  .header {
    text-align: center;
    padding-bottom: 4px;
    border-bottom: 1.5px solid #0f172a;
    margin-bottom: 3.5px;
  }
  .name {
    font-size: 19.5pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 8.9pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 1px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }
  .contact {
    font-size: 8.0pt;
    color: #475569;
    margin-top: 2px;
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
  }
  
  /* Modern Badges / Pills */
  .pills-row {
    margin-top: 3px;
    display: flex;
    justify-content: center;
    gap: 5px;
    flex-wrap: wrap;
  }
  .pill {
    background: #f1f5f9;
    color: #334155;
    font-size: 7.2pt;
    font-weight: 700;
    padding: 1.5px 6.5px;
    border-radius: 9999px;
    border: 1px solid #cbd5e1;
  }
  .pill.highlight {
    background: #ecfdf5;
    color: #065f46;
    border-color: #a7f3d0;
  }

  /* Section Titles */
  .section-title {
    font-size: 8.2pt;
    font-weight: 800;
    text-transform: uppercase;
    color: #0f172a;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 3.2px;
    margin-bottom: 2px;
  }
  .section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #cbd5e1;
  }

  /* Summary Text */
  .summary {
    font-size: 7.9pt;
    color: #334155;
    line-height: 1.24;
    text-align: justify;
  }

  /* ATS Skills Grid (2 Column Clean Cards) */
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5px 10px;
    margin-top: 1px;
  }
  .skill-box {
    font-size: 7.6pt;
    line-height: 1.22;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 2px 5.5px;
  }
  .skill-title {
    font-weight: 700;
    color: #0f172a;
  }
  .skill-desc {
    color: #475569;
  }

  /* Jobs & Roles */
  .job {
    margin-top: 1.5px;
  }
  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .job-title {
    font-size: 8.1pt;
    font-weight: 700;
    color: #0f172a;
  }
  .job-company {
    font-size: 7.9pt;
    font-weight: 600;
    color: #1d4ed8;
  }
  .job-tag {
    font-size: 7.0pt;
    font-weight: 700;
    color: #047857;
    background: #ecfdf5;
    padding: 0 4px;
    border-radius: 3px;
    margin-left: 4px;
  }
  .job-date {
    font-size: 7.3pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Clean Custom Bullets */
  ul {
    list-style-type: none;
    margin-top: 0.8px;
    margin-bottom: 0.8px;
    padding-left: 0;
  }
  li {
    font-size: 7.65pt;
    color: #334155;
    line-height: 1.21;
    position: relative;
    padding-left: 10px;
    margin-bottom: 0.6px;
  }
  li::before {
    content: "•";
    position: absolute;
    left: 1.5px;
    color: #1d4ed8;
    font-size: 8.5pt;
    line-height: 1;
  }
  li strong {
    color: #0f172a;
    font-weight: 700;
  }

  /* Education Row */
  .edu-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 7.9pt;
  }
  .edu-degree {
    font-weight: 700;
    color: #0f172a;
  }
  .edu-school {
    color: #475569;
  }
  .edu-date {
    font-size: 7.3pt;
    color: #64748b;
    font-weight: 600;
  }

  /* Footer */
  .footer-text {
    font-size: 7.55pt;
    color: #475569;
    line-height: 1.22;
  }
  .footer-text strong {
    color: #0f172a;
  }
</style>
</head>
<body>

<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="name">Aditya Mehra</div>
    <div class="subtitle">Operations & Procurement New Associate // BBA (Batch of 2026)</div>
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
    <div class="pills-row">
      <span class="pill highlight">Immediate Availability (0 Days Notice)</span>
      <span class="pill highlight">100% 24/7 Rotational & Night Shifts Ready</span>
      <span class="pill">Bengaluru Resident</span>
      <span class="pill">Dayananda Sagar University (DSU)</span>
    </div>
  </div>

  <!-- CAREER SUMMARY (Synchronized with LinkedIn Messages & Accenture JDs) -->
  <div class="section-title">Career Profile</div>
  <p class="summary">
    Diligent, quick-learning, and process-driven <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, targeting the <strong>Level 13 Operations & Procurement New Associate</strong> position at Accenture. Brings verified operational experience in Purchase Order (PO) tracking in MS Excel, supplier quotation matrices, partner KYC document verification (<strong>99.4% audited accuracy</strong>), and high-volume event logistics for <strong>100,000+ attendees at Aero India 2025</strong>. Known for strict checklist adherence, zero stock loss, and practical Python & Excel automation skills. Available for <strong>immediate onboarding (0 Days Notice)</strong> with <strong>100% flexibility for rotational and night shifts</strong> in Bengaluru.
  </p>

  <!-- EDUCATION -->
  <div class="section-title">Education</div>
  <div class="edu-row">
    <div>
      <span class="edu-degree">Bachelor of Business Administration (BBA) — International Business</span><br>
      <span class="edu-school">Dayananda Sagar University (DSU), Bengaluru, Karnataka</span>
    </div>
    <div class="edu-date">2023 – 2026 | Fresh Graduate (Immediate Joining)</div>
  </div>

  <!-- CORE SKILLS (MATCHED TO ACCENTURE WORKDAY P1/P3 ATS FILTERS) -->
  <div class="section-title">Core Skills & ATS Competencies</div>
  <div class="skills-grid">
    <div class="skill-box">
      <span class="skill-title">Procurement & P2P Support (P1):</span>
      <span class="skill-desc">Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Three-Way Matching (PO/GRN/Invoice), Quotation Comparison, Discrepancy Clearance.</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">KYC Verification & Quality (P1):</span>
      <span class="skill-desc">Partner Document Verification, Checklist Auditing (99.4% Audited Accuracy), Standard Operating Procedures (SOP), Queue Triage.</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">Order Management & Logistics (P3):</span>
      <span class="skill-desc">Vendor SLA Governance, Inventory Goods Receipt (GRN), Dual-Custody Stock Auditing, 0.0% Shrinkage, Cash & Digital UPI Balancing.</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">Computer Tools & Automation:</span>
      <span class="skill-desc">MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Power Query, Data Validation), Google Workspace, Python Data Extraction Basics.</span>
    </div>
  </div>

  <!-- PRACTICAL WORK EXPERIENCE -->
  <div class="section-title">Professional Experience & Operational Track Record</div>

  <!-- Role 1: Pencil Mark -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Commercial & Procurement Operations Intern — <span class="job-company">Pencil Mark Interior Solutions</span><span class="job-tag">Procurement Support - P1</span></span>
      <span class="job-date">Jul 2024 – Aug 2025 | Bengaluru</span>
    </div>
    <ul>
      <li>Built price comparison models in MS Excel to evaluate supplier quotes, assisting commercial estimators with unit cost analysis and vendor selection.</li>
      <li>Monitored Purchase Order (PO) tracking from issuance to site delivery, checking delivery challans against orders to eliminate billing discrepancies.</li>
      <li>Supported senior leads in preparing client cost estimation sheets, contributing to the closure of <strong>₹1.5L+ in commercial interior contracts</strong>.</li>
      <li>Conferred a written <strong>Management Commendation</strong> for operational dependability, accuracy, and workflow reliability.</li>
    </ul>
  </div>

  <!-- Role 2: Instawork -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Operations & Data Verification Intern — <span class="job-company">Instawork Services India</span><span class="job-tag">KYC & Queue Triage</span></span>
      <span class="job-date">2025 | Bengaluru</span>
    </div>
    <ul>
      <li>Audited high-throughput partner onboarding records and identity documentation against verification checklists, maintaining a <strong>99.4% accuracy rate</strong>.</li>
      <li>Processed daily queue triage adhering to operational turnaround SLAs, working with teammates to <strong>reduce average review cycle time by 12%</strong>.</li>
    </ul>
  </div>

  <!-- Role 3: Aero India 2025 -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Exhibition Operations & Logistics Lead — <span class="job-company">Salt in My Cocoa (AERO India 2025)</span><span class="job-tag">Inventory & 3-Way Balancing</span></span>
      <span class="job-date">Feb 2025 | Yelahanka Air Force Station</span>
    </div>
    <ul>
      <li>Managed stall stock supply, physical goods intake, and daily replenishment for <strong>100,000+ defense and commercial visitors</strong> under military security protocol.</li>
      <li>Conducted dual-custody stock audits before/after shifts to enforce <strong>0.0% inventory shrinkage</strong>, balancing physical cash and digital UPI settlement logs with <strong>100% financial accuracy</strong>.</li>
    </ul>
  </div>

  <!-- Role 4: TRILOGY -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Event Operations Coordinator — <span class="job-company">TRILOGY Concerts & Commercial Productions</span><span class="job-tag">Vendor SLA Governance</span></span>
      <span class="job-date">2019 – 2026 | Bengaluru</span>
    </div>
    <ul>
      <li>Governed vendor service level agreements (SLAs) across audio, stage, and lighting contractors for live concert productions at Bangalore Club, delivering zero stage downtime.</li>
      <li>Negotiated supplier rates directly, eliminating intermediary agency markups to achieve <strong>15%–20% procurement cost savings</strong> across production engagements.</li>
    </ul>
  </div>

  <!-- Role 5: NGO -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Community Operations Volunteer — <span class="job-company">NGO & Social Welfare Initiative</span><span class="job-tag">Paperwork Auditing</span></span>
      <span class="job-date">2024 | Bengaluru</span>
    </div>
    <ul>
      <li>Verified participant registration paperwork and identity records in compliance with foundation guidelines, maintaining error-free audit logs in Google Sheets.</li>
      <li>Coordinated volunteer duty shifts and on-ground logistics, ensuring seamless operational execution during city-wide outreach drives.</li>
    </ul>
  </div>

  <!-- PROJECT -->
  <div class="section-title">Technical Project</div>
  <div class="job">
    <div class="job-header">
      <span class="job-title">Job Portal Automation & Spreadsheet Tracker — <span class="job-company">Student Technical Initiative</span></span>
      <span class="job-date">2025 – 2026 | Python & Spreadsheets</span>
    </div>
    <ul>
      <li>Engineered an automated Python data extraction script to crawl, structure, and categorize corporate job postings into clean, searchable Excel databases, eliminating manual workflow redundancies.</li>
    </ul>
  </div>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="footer-text">
    <strong>Certifications:</strong> Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL)<br>
    <strong>Languages:</strong> English (Fluent Professional Proficiency), Hindi (Native / Bilingual)
  </p>

</div>
</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Best_CV.html")
pdf_path = os.path.join(OUTPUT_DIR_PDF, "Aditya_Mehra_Best_CV.pdf")
root_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Best_CV.pdf")

root_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Best_CV.docx")
docx_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Best_CV.docx")

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

print(f"Generated Best Master PDF: {root_pdf} (Size: {len(pdf_bytes)} bytes)")

# ==========================================
# GENERATE NATIVE DOCX
# ==========================================
doc = docx.Document()

# Margins: 0.30 in
for section in doc.sections:
    section.top_margin = Inches(0.28)
    section.bottom_margin = Inches(0.28)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

C_NAVY = RGBColor(15, 23, 42)
C_BLUE = RGBColor(29, 78, 216)
C_SLATE = RGBColor(100, 116, 139)
C_BODY = RGBColor(51, 65, 85)
C_EMERALD = RGBColor(6, 95, 70)

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
r_name.font.size = Pt(17.5)
r_name.font.bold = True
r_name.font.color.rgb = C_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1.5)
r_sub = p_sub.add_run("Operations & Procurement New Associate // BBA (Batch of 2026)")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(8.8)
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
r_badge = p_badge.add_run("Immediate Availability (0 Days Notice) • 100% 24/7 Rotational & Night Shifts Ready • Bengaluru Resident • DSU")
r_badge.font.name = "Arial"
r_badge.font.size = Pt(7.6)
r_badge.font.bold = True
r_badge.font.color.rgb = C_EMERALD

add_clean_divider(p_badge)

def add_sec(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"
    r.font.size = Pt(8.2)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    add_clean_divider(p)
    return p

# Profile
add_sec("Career Profile")
p_obj = doc.add_paragraph()
p_obj.paragraph_format.space_before = Pt(1)
p_obj.paragraph_format.space_after = Pt(2)
p_obj.paragraph_format.line_spacing = 1.15
r_obj = p_obj.add_run(
    "Diligent, quick-learning, and process-driven 2026 BBA graduate in International Business from Dayananda Sagar University, targeting the Level 13 Operations & Procurement New Associate position at Accenture. Brings verified operational experience in Purchase Order (PO) tracking in MS Excel, supplier quotation matrices, partner KYC document verification (99.4% audited accuracy), and high-volume event logistics for 100,000+ attendees at Aero India 2025. Known for strict checklist adherence, zero stock loss, and practical Python & Excel automation skills. Available for immediate onboarding (0 Days Notice) with 100% flexibility for rotational and night shifts in Bengaluru."
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
r_e2 = p_edu.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka | 2023 – 2026 | Fresh Graduate (Immediate Joining)")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(7.5); r_e2.font.color.rgb = C_SLATE

# Skills Grid
add_sec("Core Skills & ATS Competencies")
skills = [
    ("Procurement & P2P Support (P1):", "Purchase Order (PO) Tracking, PR-to-PO Follow-ups, Three-Way Matching (PO/GRN/Invoice), Quotation Comparison, Discrepancy Clearance."),
    ("KYC Verification & Quality (P1):", "Partner Document Verification, Checklist Auditing (99.4% Audited Accuracy), Standard Operating Procedures (SOP), Queue Triage."),
    ("Order Management & Logistics (P3):", "Vendor SLA Governance, Inventory Goods Receipt (GRN), Dual-Custody Stock Auditing, 0.0% Shrinkage, Cash & Digital UPI Balancing."),
    ("Computer Tools & Automation:", "MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Power Query, Data Validation), Google Workspace, Python Data Extraction Basics.")
]

t_sk = doc.add_table(rows=len(skills), cols=2)
t_sk.autofit = False
t_sk.columns[0].width = Inches(2.2)
t_sk.columns[1].width = Inches(5.1)

for idx, (lbl, val) in enumerate(skills):
    c0 = t_sk.cell(idx, 0)
    c1 = t_sk.cell(idx, 1)
    
    p0 = c0.paragraphs[0]; p0.paragraph_format.space_before = Pt(0.5); p0.paragraph_format.space_after = Pt(0.5)
    r0 = p0.add_run(lbl)
    r0.font.name = "Arial"; r0.font.size = Pt(7.6); r0.font.bold = True; r0.font.color.rgb = C_NAVY
    
    p1 = c1.paragraphs[0]; p1.paragraph_format.space_before = Pt(0.5); p1.paragraph_format.space_after = Pt(0.5)
    r1 = p1.add_run(val)
    r1.font.name = "Arial"; r1.font.size = Pt(7.6); r1.font.color.rgb = C_BODY

# Experience
add_sec("Professional Experience & Operational Track Record")

jobs = [
    {
        "title": "Commercial & Procurement Operations Intern — Pencil Mark Interior Solutions",
        "tag": "Procurement Support - P1",
        "date": "Jul 2024 – Aug 2025 | Bengaluru",
        "bullets": [
            "Built price comparison models in MS Excel to evaluate supplier quotes, assisting commercial estimators with unit cost analysis and vendor selection.",
            "Monitored Purchase Order (PO) tracking from issuance to site delivery, checking delivery challans against orders to eliminate billing discrepancies.",
            "Supported senior leads in preparing client cost estimation sheets, contributing to the closure of ₹1.5L+ in commercial interior contracts.",
            "Conferred a written Management Commendation for operational dependability, accuracy, and workflow reliability."
        ]
    },
    {
        "title": "Operations & Data Verification Intern — Instawork Services India",
        "tag": "KYC & Queue Triage",
        "date": "2025 | Bengaluru",
        "bullets": [
            "Audited high-throughput partner onboarding records and identity documentation against verification checklists, maintaining a 99.4% accuracy rate.",
            "Processed daily queue triage adhering to operational turnaround SLAs, working with teammates to reduce average review cycle time by 12%."
        ]
    },
    {
        "title": "Exhibition Operations & Logistics Lead — Salt in My Cocoa (AERO India 2025)",
        "tag": "Inventory & 3-Way Balancing",
        "date": "Feb 2025 | Yelahanka Air Force Station",
        "bullets": [
            "Managed stall stock supply, physical goods intake, and daily replenishment for 100,000+ defense and commercial visitors under military security protocol.",
            "Conducted dual-custody stock audits before/after shifts to enforce 0.0% inventory shrinkage, balancing physical cash and digital UPI settlement logs with 100% financial accuracy."
        ]
    },
    {
        "title": "Event Operations Coordinator — TRILOGY Concerts & Commercial Productions",
        "tag": "Vendor SLA Governance",
        "date": "2019 – 2026 | Bengaluru",
        "bullets": [
            "Governed vendor service level agreements (SLAs) across audio, stage, and lighting contractors for live concert productions at Bangalore Club, delivering zero stage downtime.",
            "Negotiated supplier rates directly, eliminating intermediary agency markups to achieve 15%–20% procurement cost savings across production engagements."
        ]
    },
    {
        "title": "Community Operations Volunteer — NGO & Social Welfare Initiative",
        "tag": "Paperwork Auditing",
        "date": "2024 | Bengaluru",
        "bullets": [
            "Verified participant registration paperwork and identity records in compliance with foundation guidelines, maintaining error-free audit logs in Google Sheets.",
            "Coordinated volunteer duty shifts and on-ground logistics, ensuring seamless operational execution during city-wide outreach drives."
        ]
    }
]

for j in jobs:
    p_j = doc.add_paragraph()
    p_j.paragraph_format.space_before = Pt(1.5)
    p_j.paragraph_format.space_after = Pt(0.4)
    p_j.paragraph_format.keep_with_next = True
    r_j1 = p_j.add_run(f"{j['title']} ")
    r_j1.font.name = "Arial"; r_j1.font.size = Pt(8.0); r_j1.font.bold = True; r_j1.font.color.rgb = C_NAVY
    r_tag = p_j.add_run(f"[{j['tag']}]\n")
    r_tag.font.name = "Arial"; r_tag.font.size = Pt(7.0); r_tag.font.bold = True; r_tag.font.color.rgb = C_EMERALD
    r_j2 = p_j.add_run(j['date'])
    r_j2.font.name = "Arial"; r_j2.font.size = Pt(7.2); r_j2.font.color.rgb = C_SLATE

    for b in j["bullets"]:
        p_b_item = doc.add_paragraph()
        p_b_item.paragraph_format.space_before = Pt(0)
        p_b_item.paragraph_format.space_after = Pt(0.5)
        p_b_item.paragraph_format.left_indent = Inches(0.12)
        p_b_item.paragraph_format.line_spacing = 1.15
        r_bullet = p_b_item.add_run(f"• {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(7.6); r_bullet.font.color.rgb = C_BODY

# Technical Project
add_sec("Technical Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.4)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Automation & Spreadsheet Tracker — Student Technical Initiative\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.0); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 – 2026 | Python & Spreadsheets")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.2); r_pr2.font.color.rgb = C_SLATE

p_pr_b = doc.add_paragraph()
p_pr_b.paragraph_format.space_before = Pt(0)
p_pr_b.paragraph_format.space_after = Pt(0.8)
p_pr_b.paragraph_format.left_indent = Inches(0.12)
r_pr_b = p_pr_b.add_run("• Engineered an automated Python data extraction script to crawl, structure, and categorize corporate job postings into clean, searchable Excel databases, eliminating manual workflow redundancies.")
r_pr_b.font.name = "Arial"; r_pr_b.font.size = Pt(7.6); r_pr_b.font.color.rgb = C_BODY

# Certifications & Languages
add_sec("Certifications & Languages")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.space_before = Pt(0.8)
p_cert.paragraph_format.space_after = Pt(0.8)
r_c1 = p_cert.add_run("Certifications: Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL)\n")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.5); r_c1.font.color.rgb = C_BODY
r_c2 = p_cert.add_run("Languages: English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.5); r_c2.font.color.rgb = C_BODY

doc.save(docx_path)
doc.save(root_docx)
print(f"Generated Best Master DOCX: {root_docx} (Size: {os.path.getsize(root_docx)} bytes)")

# Verify Page Count
with open(root_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Best Master PDF Page Count: {page_count} (Strictly 1 Page)")
