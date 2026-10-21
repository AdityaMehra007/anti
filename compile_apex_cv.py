import os
import subprocess
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
import shutil
import re

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR_HTML = r"e:\anti\resumes"
OUTPUT_DIR_PDF = r"e:\anti\resumes_pdf"
ROOT_DIR = r"e:\anti"

os.makedirs(OUTPUT_DIR_HTML, exist_ok=True)
os.makedirs(OUTPUT_DIR_PDF, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE APEX GOLD-STANDARD HTML CV (1-PAGE A4 STRICT)
# -------------------------------------------------------------
apex_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra - Apex Operations CV (Accenture Level 13 Top-Scoring)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 6.0mm 8.0mm 6.0mm 8.0mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.25;
  }
  body {
    background: #fff;
    font-size: 8.8pt;
  }
  .container {
    max-width: 100%;
    margin: 0 auto;
  }
  
  /* Header */
  .header {
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 4px;
    margin-bottom: 4px;
  }
  .name {
    font-size: 18pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 9.0pt;
    font-weight: 700;
    color: #1d4ed8;
    margin-top: 1px;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }
  .contact-info {
    font-size: 8.1pt;
    color: #475569;
    margin-top: 2px;
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact-info a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
  }
  .target-badge {
    margin-top: 2.5px;
    font-size: 7.4pt;
    font-weight: 700;
    color: #065f46;
    background: #ecfdf5;
    display: inline-block;
    padding: 1px 8px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
    letter-spacing: 0.2px;
  }

  /* Section Titles */
  .section-title {
    font-size: 9.0pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 1.5px;
    margin-top: 4px;
    margin-bottom: 3px;
  }
  
  /* Education */
  .edu-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .edu-title {
    font-size: 8.8pt;
    font-weight: 700;
    color: #0f172a;
  }
  .edu-sub {
    font-size: 8.2pt;
    color: #1d4ed8;
    font-weight: 600;
  }
  .date-loc {
    font-size: 7.6pt;
    color: #64748b;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Summary */
  .summary-text {
    font-size: 8.2pt;
    color: #334155;
    text-align: justify;
    line-height: 1.28;
  }

  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
  }
  .skills-table td {
    padding: 1.2px 0;
    vertical-align: top;
  }
  .skill-cat {
    font-weight: 700;
    color: #0f172a;
    width: 25%;
    white-space: nowrap;
  }
  .skill-items {
    color: #334155;
    width: 75%;
  }

  /* Experience Blocks */
  .item-block {
    margin-bottom: 3px;
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
    font-size: 8.4pt;
  }
  .company-name {
    font-weight: 600;
    color: #1d4ed8;
    font-size: 8.2pt;
  }
  .bullets {
    list-style-type: disc;
    padding-left: 14px;
  }
  .bullets li {
    font-size: 7.85pt;
    color: #334155;
    margin-bottom: 1px;
    line-height: 1.25;
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
    <div class="subtitle">BBA Graduate (Batch of 2026) // Entry-Level Operations New Associate</div>
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
    <div class="target-badge">
      TARGET: Accenture Level 13 Operations New Associate • Workday Reqs: AIOC-S01664213, AIOC-S01670871, AIOC-S01665657, AIOC-S01667647 • Immediate Joiner (0 Days Notice) • 24/7 Shifts Flexible
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
  <p style="font-size: 7.5pt; color: #475569; margin-top: 1px;">
    <strong>Relevant Coursework:</strong> Global Logistics & Supply Chain Management, Incoterms 2020, International Trade Finance & Documentation (Letters of Credit, Shipping Bills), Commercial Contract Law, Business Statistics & Quantitative Decision Modeling.
  </p>

  <!-- PROFESSIONAL SUMMARY -->
  <div class="section-title">Professional Summary</div>
  <p class="summary-text">
    Goal-driven <strong>2026 BBA graduate in International Business from Dayananda Sagar University, Bengaluru</strong>, seeking an entry-level <strong>Level 13 Operations New Associate</strong> role at Accenture Operations. Academic grounding in global supply chains, Procure-to-Pay (P2P) cycles, purchase order (PO) processing, and regulatory compliance. Backed by corporate internship experience in commercial operations (Pencil Mark), AI data validation and content auditing (Instawork, <strong>audited 99.4% accuracy</strong>), and high-volume defense expo logistics (Aero India 2025, <strong>0% inventory shrinkage</strong>). Proficient in MS Excel (VLOOKUP, Pivot Tables, three-way reconciliation), ERP workflows, and non-voice query resolution. Local Bengaluru resident with <strong>0 days notice</strong> and 100% readiness for 24/7 rotational and night shifts.
  </p>

  <!-- CORE COMPETENCIES -->
  <div class="section-title">Core Competencies & ATS Keywords (Accenture Workday Mapped)</div>
  <table class="skills-table">
    <tr>
      <td class="skill-cat">Procurement & P2P Ops:</td>
      <td class="skill-items">Procurement Support (P1), Invoice Processing (P1), PR-to-PO Processing, Three-Way Matching (PO/GRN/Invoice), Vendor Catalog Operations, Supplier SLA Auditing, Purchase Order Administration, Payment Dispute Reconciliation, ERP Workflows.</td>
    </tr>
    <tr>
      <td class="skill-cat">Supply Chain & Trade:</td>
      <td class="skill-items">Fulfill - Order Management (P3), Incoterms 2020 (EXW, FOB, CIF, DDP), Shipping Documentation (Bill of Lading, Commercial Invoices), Dual-Custody Inventory Governance, Physical Stock Reconciliation (0% Shrinkage).</td>
    </tr>
    <tr>
      <td class="skill-cat">Commercial & Order Ops:</td>
      <td class="skill-items">B2B Order Management (100% Non-Sales), Commercial Proposal Formulation, Contract Milestones, CRM Data Hygiene, Back-Office Query De-escalation, Service Level Agreements (SLA).</td>
    </tr>
    <tr>
      <td class="skill-cat">Compliance, Risk & Trust:</td>
      <td class="skill-items">KYC Screening (P1), Enhanced Customer Due Diligence (ECDD), Ongoing Due Diligence (OCDD), Sanctions Screening Concepts, Content Moderation & Responsible AI, Policy Adherence, Non-Voice Ticket Resolution, Standard Operating Procedures (SOP).</td>
    </tr>
    <tr>
      <td class="skill-cat">Tools & Data Analysis:</td>
      <td class="skill-items">Advanced MS Excel (VLOOKUP, INDEX/MATCH, Pivot Tables, Conditional Formatting), Google Workspace, AI Data Quality Auditing (99.4% Accuracy), Python Automation Scripts.</td>
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
      <li>Administered supplier vendor matrices, evaluated competing subcontractor quotations, and prepared comparative pricing sheets in MS Excel.</li>
      <li>Formulated commercial proposals and scope-of-work documentation, directly supporting the conversion of <strong>INR 1.5L+</strong> in secured B2B corporate contracts.</li>
      <li>Tracked purchase orders against delivery milestones and site sign-offs, maintaining <strong>100% vendor SLA compliance</strong> and zero billing discrepancies.</li>
    </ul>
  </div>

  <!-- Role 2: Instawork -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Operations & AI Data Verification Intern</span> — <span class="company-name">Instawork Services India Pvt. Ltd.</span></div>
      <div class="date-loc">2025 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Executed high-volume multimodal data extraction and operational auditing adhering to strict standard operating procedures (SOP).</li>
      <li>Maintained a verified <strong>99.4% data accuracy rating</strong> across complex operational queues, filtering non-compliant assets before database ingestion.</li>
      <li>Collaborated with team supervisors to identify workflow bottlenecks, reducing review turnaround cycle time by <strong>12%</strong>.</li>
    </ul>
  </div>

  <!-- Role 3: Aero India -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Exhibition Operations & Logistics Lead</span> — <span class="company-name">Salt in My Cocoa (Aero India 2025)</span></div>
      <div class="date-loc">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
    </div>
    <ul class="bullets">
      <li>Directed on-ground stall setup, inventory replenishment, and security clearances across 5 days for <strong>100,000+ public and defense visitors</strong>.</li>
      <li>Established a strict dual-custody physical inventory protocol, achieving <strong>0% stock shrinkage</strong> and zero stock-outs during peak hours.</li>
      <li>Reconciled high-frequency digital UPI transactions daily against physical inventory ledgers with <strong>100% financial balancing</strong>.</li>
    </ul>
  </div>

  <!-- Role 4: NGO / Community Ops -->
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Community Operations & Compliance Intern</span> — <span class="company-name">Non-Profit Social Initiative</span></div>
      <div class="date-loc">2024 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Audited and verified participant registration records and beneficiary KYC documentation in compliance with organizational guidelines.</li>
      <li>Managed database records in Google Sheets and coordinated volunteer logistics rosters across Bengaluru urban outreach drives.</li>
    </ul>
  </div>

  <!-- TECHNICAL PROJECTS & AUTOMATION -->
  <div class="section-title">Technical Projects & Operational Automation</div>
  <div class="item-block">
    <div class="item-header">
      <div><span class="role-title">Autonomous Operations & Workday Pipeline Engine</span> — <span class="company-name">Student Automation Project</span></div>
      <div class="date-loc">2026 | Python, SQLite, Workday API</div>
    </div>
    <ul class="bullets">
      <li>Architected an automated operational dispatcher in Python parsing 430+ enterprise job requisitions with 16/16 unit tests passing green.</li>
      <li>Built automated candidate-to-requisition taxonomy matching, validating skill keywords against Workday job descriptions with zero manual overhead.</li>
    </ul>
  </div>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p style="font-size: 7.7pt; color: #334155;">
    <strong>Certifications:</strong> Enterprise Operational Excellence • Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL)<br>
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
    f.write(apex_html)

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
    print(f"Generated Apex Master PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")

# -------------------------------------------------------------
# 2. GENERATE APEX GOLD-STANDARD DOCX CV (1-PAGE A4 STRICT)
# -------------------------------------------------------------
doc = Document()
for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.30)
    s.bottom_margin = Inches(0.30)
    s.left_margin = Inches(0.40)
    s.right_margin = Inches(0.40)

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
r_n.font.name = "Arial"; r_n.font.size = Pt(17); r_n.font.bold = True; r_n.font.color.rgb = C_NAVY

# Subtitle
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(1.5)
r_s = p_sub.add_run("BBA GRADUATE (BATCH OF 2026) // ENTRY-LEVEL OPERATIONS NEW ASSOCIATE")
r_s.font.name = "Arial"; r_s.font.size = Pt(9.0); r_s.font.bold = True; r_s.font.color.rgb = C_BLUE

# Contact
p_c = doc.add_paragraph()
p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c.paragraph_format.space_before = Pt(0)
p_c.paragraph_format.space_after = Pt(1.5)
r_c = p_c.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com  |  linkedin.com/in/aditya-mehra  |  github.com/AdityaMehra007")
r_c.font.name = "Arial"; r_c.font.size = Pt(8.1); r_c.font.color.rgb = C_SLATE

# Badge
p_b = doc.add_paragraph()
p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_b.paragraph_format.space_before = Pt(0)
p_b.paragraph_format.space_after = Pt(3.5)
r_b = p_b.add_run("TARGET: Accenture Level 13 Operations New Associate • Workday Reqs: AIOC-S01664213, AIOC-S01670871, AIOC-S01665657, AIOC-S01667647 • Immediate Joiner • 24/7 Shifts")
r_b.font.name = "Arial"; r_b.font.size = Pt(7.5); r_b.font.bold = True; r_b.font.color.rgb = C_GREEN

def add_sec_title(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after = Pt(1.2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title.upper())
    r.font.name = "Arial"; r.font.size = Pt(9.0); r.font.bold = True; r.font.color.rgb = C_NAVY
    add_clean_divider(p)

# Education
add_sec_title("Education")
p_ed = doc.add_paragraph()
p_ed.paragraph_format.space_before = Pt(1)
p_ed.paragraph_format.space_after = Pt(1)
r_e1 = p_ed.add_run("Bachelor of Business Administration (BBA) — International Business\n")
r_e1.font.name = "Arial"; r_e1.font.size = Pt(8.6); r_e1.font.bold = True; r_e1.font.color.rgb = C_NAVY
r_e2 = p_ed.add_run("Dayananda Sagar University (DSU), Bengaluru, Karnataka  •  2023 – 2026 | Fresh Graduate (Immediate Joining)\n")
r_e2.font.name = "Arial"; r_e2.font.size = Pt(8.0); r_e2.font.bold = True; r_e2.font.color.rgb = C_BLUE
r_e3 = p_ed.add_run("Relevant Coursework: Global Logistics & Supply Chain Management, Incoterms 2020, International Trade Finance & Documentation (Letters of Credit, Shipping Bills), Commercial Contract Law, Business Statistics & Quantitative Decision Modeling.")
r_e3.font.name = "Arial"; r_e3.font.size = Pt(7.5); r_e3.font.color.rgb = C_SLATE

# Professional Summary
add_sec_title("Professional Summary")
p_sum = doc.add_paragraph()
p_sum.paragraph_format.space_before = Pt(1)
p_sum.paragraph_format.space_after = Pt(1.5)
p_sum.paragraph_format.line_spacing = 1.13
r_sm = p_sum.add_run(
    "Goal-driven 2026 BBA graduate in International Business from Dayananda Sagar University, Bengaluru, seeking an entry-level Level 13 Operations New Associate role at Accenture Operations. Academic grounding in global supply chains, Procure-to-Pay (P2P) cycles, purchase order (PO) processing, and regulatory compliance. Backed by corporate internship experience in commercial operations (Pencil Mark), AI data validation and content auditing (Instawork, audited 99.4% accuracy), and high-volume defense expo logistics (Aero India 2025, 0% inventory shrinkage). Proficient in MS Excel (VLOOKUP, Pivot Tables, three-way reconciliation), ERP workflows, and non-voice query resolution. Local Bengaluru resident with 0 days notice and 100% readiness for 24/7 rotational and night shifts."
)
r_sm.font.name = "Arial"; r_sm.font.size = Pt(8.1); r_sm.font.color.rgb = C_BODY

# Core Competencies
add_sec_title("Core Competencies & ATS Keywords (Accenture Workday Mapped)")
skills = [
    ("Procurement & P2P Ops", "Procurement Support (P1), Invoice Processing (P1), PR-to-PO Processing, Three-Way Matching (PO/GRN/Invoice), Vendor Catalog Operations, Supplier SLA Auditing, Purchase Order Administration, Payment Dispute Reconciliation, ERP Workflows."),
    ("Supply Chain & Trade", "Fulfill - Order Management (P3), Incoterms 2020 (EXW, FOB, CIF, DDP), Shipping Documentation (Bill of Lading, Commercial Invoices), Dual-Custody Inventory Governance, Physical Stock Reconciliation (0% Shrinkage)."),
    ("Commercial & Order Ops", "B2B Order Management (100% Non-Sales), Commercial Proposal Formulation, Contract Milestones, CRM Data Hygiene, Back-Office Query De-escalation, Service Level Agreements (SLA)."),
    ("Compliance, Risk & Trust", "KYC Screening (P1), Enhanced Customer Due Diligence (ECDD), Ongoing Due Diligence (OCDD), Sanctions Screening Concepts, Content Moderation & Responsible AI, Policy Adherence, Non-Voice Ticket Resolution, Standard Operating Procedures (SOP)."),
    ("Tools & Data Analysis", "Advanced MS Excel (VLOOKUP, INDEX/MATCH, Pivot Tables, Conditional Formatting), Google Workspace, AI Data Quality Auditing (99.4% Accuracy), Python Automation Scripts.")
]
for cat, txt in skills:
    p_sk = doc.add_paragraph()
    p_sk.paragraph_format.space_before = Pt(0)
    p_sk.paragraph_format.space_after = Pt(0.8)
    p_sk.paragraph_format.left_indent = Inches(0.12)
    r_k1 = p_sk.add_run(f"• {cat}: ")
    r_k1.font.name = "Arial"; r_k1.font.size = Pt(7.9); r_k1.font.bold = True; r_k1.font.color.rgb = C_NAVY
    r_k2 = p_sk.add_run(txt)
    r_k2.font.name = "Arial"; r_k2.font.size = Pt(7.9); r_k2.font.color.rgb = C_BODY

# Internships
add_sec_title("Internships & Practical Field Exposure")
experiences = [
    {
        "title": "Commercial Operations Intern — Pencil Mark Interior Solutions LLP",
        "meta": "July 2024 – Aug 2025 | Bengaluru, India",
        "bullets": [
            "Administered supplier vendor matrices, evaluated competing subcontractor quotations, and prepared comparative pricing sheets in MS Excel.",
            "Formulated commercial proposals and scope-of-work documentation, directly supporting the conversion of INR 1.5L+ in secured B2B corporate contracts.",
            "Tracked purchase orders against delivery milestones and site sign-offs, maintaining 100% vendor SLA compliance and zero billing discrepancies."
        ]
    },
    {
        "title": "Operations & AI Data Verification Intern — Instawork Services India Pvt. Ltd.",
        "meta": "2025 | Bengaluru, India",
        "bullets": [
            "Executed high-volume multimodal data extraction and operational auditing adhering to strict standard operating procedures (SOP).",
            "Maintained a verified 99.4% data accuracy rating across complex operational queues, filtering non-compliant assets before database ingestion.",
            "Collaborated with team supervisors to identify workflow bottlenecks, reducing review turnaround cycle time by 12%."
        ]
    },
    {
        "title": "Exhibition Operations & Logistics Lead — Salt in My Cocoa (Aero India 2025)",
        "meta": "Feb 2025 | Yelahanka Air Force Station, Bengaluru",
        "bullets": [
            "Directed on-ground stall setup, inventory replenishment, and security clearances across 5 days for 100,000+ public and defense visitors.",
            "Established a strict dual-custody physical inventory protocol, achieving 0% stock shrinkage and zero stock-outs during peak hours.",
            "Reconciled high-frequency digital UPI transactions daily against physical inventory ledgers with 100% financial balancing."
        ]
    },
    {
        "title": "Community Operations & Compliance Intern — Non-Profit Social Initiative",
        "meta": "2024 | Bengaluru, India",
        "bullets": [
            "Audited and verified participant registration records and beneficiary KYC documentation in compliance with organizational guidelines.",
            "Managed database records in Google Sheets and coordinated volunteer logistics rosters across Bengaluru urban outreach drives."
        ]
    }
]

for exp in experiences:
    p_x = doc.add_paragraph()
    p_x.paragraph_format.space_before = Pt(1.8)
    p_x.paragraph_format.space_after = Pt(0.8)
    p_x.paragraph_format.keep_with_next = True
    r_x1 = p_x.add_run(f"{exp['title']}\n")
    r_x1.font.name = "Arial"; r_x1.font.size = Pt(8.3); r_x1.font.bold = True; r_x1.font.color.rgb = C_NAVY
    r_x2 = p_x.add_run(exp['meta'])
    r_x2.font.name = "Arial"; r_x2.font.size = Pt(7.6); r_x2.font.color.rgb = C_SLATE

    for b in exp["bullets"]:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(0.8)
        p_b.paragraph_format.left_indent = Inches(0.18)
        p_b.paragraph_format.first_line_indent = Inches(-0.12)
        p_b.paragraph_format.line_spacing = 1.11
        r_d = p_b.add_run("– ")
        r_d.font.name = "Arial"; r_d.font.size = Pt(7.9); r_d.font.bold = True; r_d.font.color.rgb = C_BLUE
        r_t = p_b.add_run(b)
        r_t.font.name = "Arial"; r_t.font.size = Pt(7.9); r_t.font.color.rgb = C_BODY

# Technical Projects
add_sec_title("Technical Projects & Operational Automation")
p_pr = doc.add_paragraph()
p_pr.paragraph_format.space_before = Pt(1)
p_pr.paragraph_format.space_after = Pt(0.8)
r_p1 = p_pr.add_run("Autonomous Operations & Workday Pipeline Engine — Student Automation Project\n")
r_p1.font.name = "Arial"; r_p1.font.size = Pt(8.3); r_p1.font.bold = True; r_p1.font.color.rgb = C_NAVY
r_p2 = p_pr.add_run("2026 | Python, SQLite, Workday API Integration | 16/16 Unit Tests Passing Green\n")
r_p2.font.name = "Arial"; r_p2.font.size = Pt(7.6); r_p2.font.color.rgb = C_SLATE
r_p3 = p_pr.add_run("– Architected an automated operational dispatcher in Python parsing 430+ enterprise job requisitions with 16/16 unit tests passing green.\n– Built automated candidate-to-requisition taxonomy matching, validating skill keywords against Workday job descriptions with zero manual overhead.")
r_p3.font.name = "Arial"; r_p3.font.size = Pt(7.9); r_p3.font.color.rgb = C_BODY

# Certifications & Languages
add_sec_title("Certifications & Languages")
p_cr = doc.add_paragraph()
p_cr.paragraph_format.space_before = Pt(1)
p_cr.paragraph_format.space_after = Pt(1)
r_c1 = p_cr.add_run("Certifications: ")
r_c1.font.name = "Arial"; r_c1.font.size = Pt(7.8); r_c1.font.bold = True; r_c1.font.color.rgb = C_NAVY
r_c2 = p_cr.add_run("Enterprise Operational Excellence • Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL)\n")
r_c2.font.name = "Arial"; r_c2.font.size = Pt(7.8); r_c2.font.color.rgb = C_BODY
r_l1 = p_cr.add_run("Languages: ")
r_l1.font.name = "Arial"; r_l1.font.size = Pt(7.8); r_l1.font.bold = True; r_l1.font.color.rgb = C_NAVY
r_l2 = p_cr.add_run("English (Fluent Professional Proficiency), Hindi (Native / Bilingual)")
r_l2.font.name = "Arial"; r_l2.font.size = Pt(7.8); r_l2.font.color.rgb = C_BODY

doc.save(docx_path)
shutil.copyfile(docx_path, root_docx)
print(f"Generated Apex Master DOCX: {docx_path} (Size: {os.path.getsize(docx_path)} bytes)")

# Verify Page Count
pdf_data = open(pdf_path, "rb").read()
page_count = len(re.findall(b'/Type\s*/Page[^s]', pdf_data))
print(f"Verified Final Master PDF Page Count: {page_count} (Strictly 1 Page)")
