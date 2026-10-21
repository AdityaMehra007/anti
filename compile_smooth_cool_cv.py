"""
compile_smooth_cool_cv.py
Compiles an "Easy, Smooth, Nice, and Cool" 1-Page CV for Aditya Mehra.
- Modern, sleek tech-minimalist styling (Inter / Segoe UI, subtle badge pills, fresh indigo accents).
- Easy to read: plenty of breathing room, zero intimidating jargon, conversational yet professional.
- Highlights what makes Aditya stand out:
  * Bangalore local, BBA 2026, 0 Days Notice (Immediate Joiner), 100% Rotational & Night Shift Ready.
  * Live concert ops at Bangalore Club (TRILOGY), 100k+ crowd at Aero India 2025 (0% loss, 100% balancing).
  * 99.4% accuracy at Instawork, vendor PO tracking at Pencil Mark, Python automation script.
- Strictly 1 Page A4 with 0 overflow and 0 browser headers/footers.
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
<title>Aditya Mehra - Modern & Smooth Operations CV</title>
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
    color: #1e293b;
    background: #ffffff;
    line-height: 1.28;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .container {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 8.5mm 12mm 6mm 12mm;
    margin: 0 auto;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header Section */
  .header {
    text-align: center;
    padding-bottom: 5px;
    border-bottom: 1.5px solid #e2e8f0;
    margin-bottom: 4px;
  }
  .name {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 9.2pt;
    font-weight: 700;
    color: #4f46e5;
    margin-top: 1px;
    letter-spacing: 0.4px;
  }
  .contact {
    font-size: 8.1pt;
    color: #64748b;
    margin-top: 3px;
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact a {
    color: #4f46e5;
    text-decoration: none;
    font-weight: 600;
  }
  
  /* Cool Pill Badges */
  .pills-row {
    margin-top: 4px;
    display: flex;
    justify-content: center;
    gap: 6px;
    flex-wrap: wrap;
  }
  .pill {
    background: #f1f5f9;
    color: #334155;
    font-size: 7.2pt;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 9999px;
    border: 1px solid #e2e8f0;
  }
  .pill.highlight {
    background: #ecfdf5;
    color: #047857;
    border-color: #a7f3d0;
  }

  /* Section Titles */
  .section-title {
    font-size: 8.4pt;
    font-weight: 800;
    text-transform: uppercase;
    color: #0f172a;
    letter-spacing: 0.6px;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 4px;
    margin-bottom: 2.5px;
  }
  .section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #e2e8f0;
  }

  /* About Me Text */
  .summary {
    font-size: 8.0pt;
    color: #334155;
    line-height: 1.28;
    text-align: justify;
  }

  /* Skills Grid */
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 3px 12px;
    margin-top: 1px;
  }
  .skill-box {
    font-size: 7.8pt;
    line-height: 1.24;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 4px;
    padding: 2px 6px;
  }
  .skill-title {
    font-weight: 700;
    color: #0f172a;
  }
  .skill-desc {
    color: #475569;
  }

  /* Job & Experience Rows */
  .job {
    margin-top: 2px;
  }
  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .job-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #0f172a;
  }
  .job-company {
    font-size: 8.0pt;
    font-weight: 600;
    color: #4f46e5;
  }
  .job-date {
    font-size: 7.4pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Clean Bullets */
  ul {
    list-style-type: none;
    margin-top: 1px;
    margin-bottom: 1px;
    padding-left: 0;
  }
  li {
    font-size: 7.8pt;
    color: #334155;
    line-height: 1.24;
    position: relative;
    padding-left: 11px;
    margin-bottom: 0.8px;
  }
  li::before {
    content: "•";
    position: absolute;
    left: 2px;
    color: #4f46e5;
    font-size: 9pt;
    line-height: 1;
  }
  li strong {
    color: #0f172a;
    font-weight: 700;
  }

  /* Education & Footer */
  .edu-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 8.0pt;
  }
  .edu-degree {
    font-weight: 700;
    color: #0f172a;
  }
  .edu-school {
    color: #475569;
  }
  .edu-date {
    font-size: 7.4pt;
    color: #64748b;
    font-weight: 600;
  }

  .footer-text {
    font-size: 7.7pt;
    color: #475569;
    line-height: 1.25;
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
    <div class="subtitle">Operations & Business Support Associate</div>
    <div class="contact">
      <span>Bengaluru, Karnataka</span>
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
      <span class="pill highlight">Available Immediately (0 Days Notice)</span>
      <span class="pill highlight">100% 24/7 Rotational & Night Shifts Ready</span>
      <span class="pill">BBA Class of 2026</span>
      <span class="pill">Bengaluru Resident</span>
    </div>
  </div>

  <!-- ABOUT ME -->
  <div class="section-title">About Me</div>
  <p class="summary">
    Energetic, detail-oriented, and dependable <strong>2026 BBA graduate in International Business from Dayananda Sagar University</strong>, seeking an entry-level <strong>Operations Associate</strong> role at Accenture. Brings proven hands-on experience in vendor coordination, Purchase Order (PO) tracking in MS Excel, partner document verification (<strong>99.4% accuracy</strong>), and on-ground event stock management. Known for calm execution under high pressure, fast learning speed, and reliable teamwork. Ready to start <strong>immediately (0 Days Notice)</strong> with <strong>100% flexibility for rotational and night shifts</strong>.
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

  <!-- CORE SKILLS -->
  <div class="section-title">Core Strengths & Skills</div>
  <div class="skills-grid">
    <div class="skill-box">
      <span class="skill-title">Operations & Purchasing:</span>
      <span class="skill-desc">Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Delivery Bill Checking.</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">Quality & Accuracy:</span>
      <span class="skill-desc">Document Verification, Checklist Audits, High Detail Focus (99.4% Audited Accuracy), Standard Operating Procedures (SOP).</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">Stock & Crowd Logistics:</span>
      <span class="skill-desc">Physical Stock Counting, Receiving & Inventory Audits, 0% Stock Loss, Cash and Digital UPI Register Balancing.</span>
    </div>
    <div class="skill-box">
      <span class="skill-title">Computer & Software Tools:</span>
      <span class="skill-desc">MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Formulas, Data Cleaning), Google Sheets, MS Office, Basic Python.</span>
    </div>
  </div>

  <!-- EXPERIENCE -->
  <div class="section-title">Practical Experience</div>

  <!-- Role 1: Pencil Mark -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Operations & Procurement Intern — <span class="job-company">Pencil Mark Interior Solutions</span></span>
      <span class="job-date">Jul 2024 – Aug 2025 | Bengaluru</span>
    </div>
    <ul>
      <li>Built price comparison sheets in MS Excel to evaluate supplier quotes, helping managers select the most cost-effective vendors.</li>
      <li>Monitored Purchase Orders (POs) from ordering to site delivery, matching delivery challans against orders to prevent billing mistakes.</li>
      <li>Assisted with commercial cost estimation sheets, helping close <strong>₹1.5L+ in commercial interior contracts</strong>.</li>
      <li>Awarded a written <strong>Management Commendation</strong> for dependable execution, punctuality, and accuracy.</li>
    </ul>
  </div>

  <!-- Role 2: Instawork -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Operations & Data Verification Intern — <span class="job-company">Instawork Services India</span></span>
      <span class="job-date">2025 | Bengaluru</span>
    </div>
    <ul>
      <li>Audited partner profiles and ID documents against verification checklists, maintaining an audited <strong>99.4% accuracy score</strong>.</li>
      <li>Processed daily verification tasks quickly to meet team deadlines, helping the team <strong>reduce review cycle time by 12%</strong>.</li>
    </ul>
  </div>

  <!-- Role 3: Aero India 2025 -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Event Operations & Stock Lead — <span class="job-company">Salt in My Cocoa (AERO India 2025)</span></span>
      <span class="job-date">Feb 2025 | Yelahanka Air Force Station</span>
    </div>
    <ul>
      <li>Managed stall stock supply, daily intake, and customer billing for <strong>100,000+ defense and public visitors</strong> across 5 high-rush days.</li>
      <li>Conducted physical stock counts before and after every shift, achieving <strong>0% stock loss</strong> and <strong>100% daily cash/UPI balancing</strong>.</li>
    </ul>
  </div>

  <!-- Role 4: TRILOGY -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Event Operations Coordinator — <span class="job-company">TRILOGY Concerts & Commercial Productions</span></span>
      <span class="job-date">2019 – 2026 | Bengaluru</span>
    </div>
    <ul>
      <li>Coordinated with sound, lighting, and stage vendors for live concerts at Bangalore Club, delivering zero event delays.</li>
      <li>Negotiated supplier rates directly, saving <strong>15%–20% on event production costs</strong>.</li>
    </ul>
  </div>

  <!-- Role 5: NGO -->
  <div class="job">
    <div class="job-header">
      <span class="job-title">Community Operations Volunteer — <span class="job-company">NGO & Social Welfare Initiative</span></span>
      <span class="job-date">2024 | Bengaluru</span>
    </div>
    <ul>
      <li>Verified attendee registration documents and maintained clean records in Google Sheets during social outreach drives.</li>
      <li>Coordinated volunteer shift schedules and on-ground logistics for smooth community event execution.</li>
    </ul>
  </div>

  <!-- PROJECT -->
  <div class="section-title">Technical Project</div>
  <div class="job">
    <div class="job-header">
      <span class="job-title">Job Portal Data Automation — <span class="job-company">Self-Initiated Academic Project</span></span>
      <span class="job-date">2025 – 2026 | Python & Excel</span>
    </div>
    <ul>
      <li>Created a Python script to collect and organize corporate job postings into clean, searchable Excel sheets, eliminating manual searching.</li>
    </ul>
  </div>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p class="footer-text">
    <strong>Certifications:</strong> Written Management Commendation (Pencil Mark) • Google Digital Marketing Fundamentals • Service Marketing (NPTEL)<br>
    <strong>Languages:</strong> English (Fluent Professional), Hindi (Native / Bilingual)
  </p>

</div>
</body>
</html>
"""

html_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Cool_Smooth_CV.html")
pdf_path = os.path.join(OUTPUT_DIR_PDF, "Aditya_Mehra_Cool_Smooth_CV.pdf")
root_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Cool_Smooth_CV.pdf")
friendly_pdf = os.path.join(ROOT_DIR, "Aditya_Mehra_Smooth_CV.pdf")

root_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Cool_Smooth_CV.docx")
friendly_docx = os.path.join(ROOT_DIR, "Aditya_Mehra_Smooth_CV.docx")
docx_path = os.path.join(OUTPUT_DIR_HTML, "Aditya_Mehra_Cool_Smooth_CV.docx")

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
    with open(friendly_pdf, "wb") as f_out:
        f_out.write(pdf_bytes)

print(f"Generated Cool & Smooth PDF: {friendly_pdf} (Size: {len(pdf_bytes)} bytes)")

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
C_INDIGO = RGBColor(79, 70, 229)
C_SLATE = RGBColor(100, 116, 139)
C_BODY = RGBColor(51, 65, 85)
C_EMERALD = RGBColor(4, 120, 87)

def add_clean_divider(paragraph):
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'E2E8F0')
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
r_sub = p_sub.add_run("Operations & Business Support Associate")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(9.0)
r_sub.font.bold = True
r_sub.font.color.rgb = C_INDIGO

p_cont = doc.add_paragraph()
p_cont.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_cont.paragraph_format.space_before = Pt(0)
p_cont.paragraph_format.space_after = Pt(1.5)
r_cont = p_cont.add_run("Bengaluru, Karnataka | +91 7003456624 | adityamehra799@gmail.com | linkedin.com/in/aditya-mehra | github.com/AdityaMehra007")
r_cont.font.name = "Arial"
r_cont.font.size = Pt(7.6)
r_cont.font.color.rgb = C_SLATE

p_badge = doc.add_paragraph()
p_badge.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
p_badge.paragraph_format.space_before = Pt(0)
p_badge.paragraph_format.space_after = Pt(2.5)
r_badge = p_badge.add_run("Available Immediately (0 Days Notice) • 100% 24/7 Rotational & Night Shifts Ready • BBA 2026 • Bengaluru Resident")
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

# About Me
add_sec("About Me")
p_obj = doc.add_paragraph()
p_obj.paragraph_format.space_before = Pt(1)
p_obj.paragraph_format.space_after = Pt(2)
p_obj.paragraph_format.line_spacing = 1.15
r_obj = p_obj.add_run(
    "Energetic, detail-oriented, and dependable 2026 BBA graduate in International Business from Dayananda Sagar University, seeking an entry-level Operations Associate role at Accenture. Brings proven hands-on experience in vendor coordination, Purchase Order (PO) tracking in MS Excel, partner document verification (99.4% accuracy), and on-ground event stock management. Known for calm execution under high pressure, fast learning speed, and reliable teamwork. Ready to start immediately (0 Days Notice) with 100% flexibility for rotational and night shifts."
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

# Core Strengths & Skills
add_sec("Core Strengths & Skills")
skills = [
    ("Operations & Purchasing:", "Purchase Order (PO) Tracking, Vendor Follow-ups, Quotation Comparison Sheets, Delivery Bill Checking."),
    ("Quality & Accuracy:", "Document Verification, Checklist Audits, High Detail Focus (99.4% Audited Accuracy), Standard Operating Procedures (SOP)."),
    ("Stock & Crowd Logistics:", "Physical Stock Counting, Receiving & Inventory Audits, 0% Stock Loss, Cash and Digital UPI Register Balancing."),
    ("Computer & Software Tools:", "MS Excel (VLOOKUP, Pivot Tables, SUMIFS, Formulas, Data Cleaning), Google Sheets, MS Office, Basic Python.")
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

# Practical Experience
add_sec("Practical Experience")

jobs = [
    {
        "title": "Operations & Procurement Intern — Pencil Mark Interior Solutions",
        "date": "Jul 2024 – Aug 2025 | Bengaluru",
        "bullets": [
            "Built price comparison sheets in MS Excel to evaluate supplier quotes, helping managers select the most cost-effective vendors.",
            "Monitored Purchase Orders (POs) from ordering to site delivery, matching delivery challans against orders to prevent billing mistakes.",
            "Assisted with commercial cost estimation sheets, helping close ₹1.5L+ in commercial interior contracts.",
            "Awarded a written Management Commendation for dependable execution, punctuality, and accuracy."
        ]
    },
    {
        "title": "Operations & Data Verification Intern — Instawork Services India",
        "date": "2025 | Bengaluru",
        "bullets": [
            "Audited partner profiles and ID documents against verification checklists, maintaining an audited 99.4% accuracy score.",
            "Processed daily verification tasks quickly to meet team deadlines, helping the team reduce review cycle time by 12%."
        ]
    },
    {
        "title": "Event Operations & Stock Lead — Salt in My Cocoa (AERO India 2025)",
        "date": "Feb 2025 | Yelahanka Air Force Station",
        "bullets": [
            "Managed stall stock supply, daily intake, and customer billing for 100,000+ defense and public visitors across 5 high-rush days.",
            "Conducted physical stock counts before and after every shift, achieving 0% stock loss and 100% daily cash/UPI balancing."
        ]
    },
    {
        "title": "Event Operations Coordinator — TRILOGY Concerts & Commercial Productions",
        "date": "2019 – 2026 | Bengaluru",
        "bullets": [
            "Coordinated with sound, lighting, and stage vendors for live concerts at Bangalore Club, delivering zero event delays.",
            "Negotiated supplier rates directly, saving 15%–20% on event production costs."
        ]
    },
    {
        "title": "Community Operations Volunteer — NGO & Social Welfare Initiative",
        "date": "2024 | Bengaluru",
        "bullets": [
            "Verified attendee registration documents and maintained clean records in Google Sheets during social outreach drives.",
            "Coordinated volunteer shift schedules and on-ground logistics for smooth community event execution."
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
        r_bullet = p_b_item.add_run(f"• {b}")
        r_bullet.font.name = "Arial"; r_bullet.font.size = Pt(7.7); r_bullet.font.color.rgb = C_BODY

# Technical Project
add_sec("Technical Project")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.4)
p_pr.paragraph_format.keep_with_next = True
r_pr1 = p_pr.add_run("Job Portal Data Automation — Self-Initiated Academic Project\n")
r_pr1.font.name = "Arial"; r_pr1.font.size = Pt(8.0); r_pr1.font.bold = True; r_pr1.font.color.rgb = C_NAVY
r_pr2 = p_pr.add_run("2025 – 2026 | Python & Excel")
r_pr2.font.name = "Arial"; r_pr2.font.size = Pt(7.3); r_pr2.font.color.rgb = C_SLATE

p_pr_b = doc.add_paragraph()
p_pr_b.paragraph_format.space_before = Pt(0)
p_pr_b.paragraph_format.space_after = Pt(0.8)
p_pr_b.paragraph_format.left_indent = Inches(0.12)
r_pr_b = p_pr_b.add_run("• Created a Python script to collect and organize corporate job postings into clean, searchable Excel sheets, eliminating manual searching.")
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
doc.save(friendly_docx)
print(f"Generated Cool & Smooth DOCX: {friendly_docx} (Size: {os.path.getsize(friendly_docx)} bytes)")

# Verify Page Count
with open(friendly_pdf, "rb") as f:
    pdf_data = f.read()
    page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
    print(f"Verified Cool Master PDF Page Count: {page_count} (Strictly 1 Page)")
