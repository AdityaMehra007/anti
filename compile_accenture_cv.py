import os
import subprocess

html_content = """<!DOCTYPE html>
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
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .name {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .subtitle {
    font-size: 9.8pt;
    font-weight: 700;
    color: #2563eb;
    margin-top: 2px;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }
  .contact-info {
    font-size: 8.5pt;
    color: #475569;
    margin-top: 4px;
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
    font-weight: 500;
  }
  .contact-info a {
    color: #2563eb;
    text-decoration: none;
  }
  .tagline-badge {
    margin-top: 4px;
    font-size: 8pt;
    font-weight: 700;
    color: #047857;
    background: #ecfdf5;
    display: inline-block;
    padding: 1px 8px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
  }

  /* Section Styles */
  .section-title {
    font-size: 9.8pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 7px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  /* Summary */
  .summary-text {
    font-size: 8.7pt;
    color: #334155;
    text-align: justify;
    line-height: 1.34;
  }

  /* Education */
  .edu-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .edu-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
  }
  .edu-sub {
    font-size: 8.5pt;
    color: #2563eb;
    font-weight: 600;
    margin-top: 1px;
  }
  
  /* Skills Table */
  .skills-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-bottom: 2px;
  }
  .skills-table td {
    padding: 2px 0;
    vertical-align: top;
  }
  .skill-cat {
    font-weight: 700;
    color: #0f172a;
    width: 23%;
  }
  .skill-items {
    color: #334155;
    width: 77%;
  }

  /* Experience & Project Blocks */
  .item-block {
    margin-bottom: 5.5px;
  }
  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.5px;
  }
  .role-title {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
  }
  .company-name {
    font-size: 8.8pt;
    font-weight: 600;
    color: #2563eb;
  }
  .date-loc {
    font-size: 8pt;
    color: #64748b;
    font-weight: 600;
    text-align: right;
  }
  .bullets {
    list-style-type: disc;
    margin-left: 14px;
    margin-top: 1px;
  }
  .bullets li {
    font-size: 8.4pt;
    color: #334155;
    margin-bottom: 1.5px;
    line-height: 1.3;
    text-align: justify;
  }
  .bullets li strong {
    color: #0f172a;
  }

  @media screen {
    body {
      background: #f1f5f9;
      padding: 30px;
    }
    .container {
      background: #fff;
      max-width: 820px;
      padding: 35px 40px;
      margin: 0 auto;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      border-radius: 6px;
    }
    .print-btn {
      position: fixed;
      bottom: 25px;
      right: 25px;
      background: #2563eb;
      color: #fff;
      padding: 12px 22px;
      border-radius: 8px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(37,99,235,0.4);
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .print-btn:hover {
      background: #1d4ed8;
    }
  }
  @media print {
    .print-btn { display: none; }
    body { background: #fff; padding: 0; }
    .container { box-shadow: none; padding: 0; max-width: 100%; }
  }
</style>
</head>
<body>

<button class="print-btn" onclick="window.print()">
  <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/></svg>
  Print / Save as PDF
</button>

<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="name">ADITYA MEHRA</div>
    <div class="subtitle">BBA Graduate (Batch of 2026) // Entry-Level Operations New Associate</div>
    <div class="contact-info">
      <span>Bengaluru, Karnataka, India</span>
      <span>+91 7003456624</span>
      <span>adityamehra799@gmail.com</span>
      <span><a href="https://www.linkedin.com/in/aditya-mehra" target="_blank">linkedin.com/in/aditya-mehra</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
    <div class="tagline-badge">
      Fresher (0 Years Experience) • Immediate Joiner (0 Days Notice) • 100% Rotational & Night Shift Flexible • Bengaluru Local
    </div>
  </div>

  <!-- EDUCATION (PLACED PROMINENTLY FOR FRESHERS) -->
  <div class="section-title">Education</div>
  <div class="edu-row">
    <div>
      <div class="edu-title">Bachelor of Business Administration (BBA) — International Business</div>
      <div class="edu-sub">Dayananda Sagar University (DSU), Bengaluru, Karnataka</div>
    </div>
    <div class="date-loc">2023 – 2026 | Fresh Graduate (Immediate Joining)</div>
  </div>
  <p style="font-size: 8pt; color: #475569; margin-top: 2px;">
    <strong>Relevant Coursework:</strong> Global Logistics & Supply Chain Management, Incoterms 2020, International Trade Finance & Documentation (Letters of Credit, Shipping Bills), Commercial Contract Law, Business Statistics & Decision Modeling.
  </p>

  <!-- PROFILE SUMMARY -->
  <div class="section-title">Professional Summary</div>
  <p class="summary-text">
    Goal-driven <strong>2026 BBA graduate in International Business from Dayananda Sagar University, Bengaluru</strong>, seeking an entry-level <strong>Level 13 New Associate</strong> role at Accenture Operations. Academic specialization in global supply chains, Procure-to-Pay (P2P) cycles, purchase order (PO) processing, and operational compliance. Backed by verifiable corporate internship experience in commercial operations (Pencil Mark), AI data validation (Instawork), and high-volume event logistics (Aero India 2025 with <strong>0% inventory shrinkage</strong>). Proficient in MS Excel (VLOOKUP, Pivot Tables, three-way reconciliation) and automated workflows. Immediate joiner with 100% readiness for 24/7 rotational and night shifts in Bengaluru.
  </p>

  <!-- CORE SKILLS -->
  <div class="section-title">Core Competencies & Functional Skills</div>
  <table class="skills-table">
    <tr>
      <td class="skill-cat">Procurement & P2P:</td>
      <td class="skill-items">PR-to-PO Processing, Three-Way Matching (PO/GRN/Invoice), Vendor Catalog Operations, Supplier SLA Auditing, Purchase Order Administration, Payment Dispute Reconciliation.</td>
    </tr>
    <tr>
      <td class="skill-cat">Supply Chain & Trade:</td>
      <td class="skill-items">Incoterms 2020 (EXW, FOB, CIF, DDP), International Shipping Documentation (Bill of Lading, Commercial Invoices), Dual-Custody Inventory Governance, Stock Reconciliation.</td>
    </tr>
    <tr>
      <td class="skill-cat">Commercial & Order Ops:</td>
      <td class="skill-items">B2B Order Management (100% Non-Sales), Commercial Proposal Formulation, Contract Milestones, CRM Data Hygiene, Back-Office Query De-escalation.</td>
    </tr>
    <tr>
      <td class="skill-cat">Tools & Data Analysis:</td>
      <td class="skill-items">Advanced MS Excel (VLOOKUP, INDEX/MATCH, Pivot Tables, Conditional Formatting), Google Workspace, ERP Workflows, AI Data Quality Auditing (99.4% Accuracy).</td>
    </tr>
  </table>

  <!-- INTERNSHIPS & PRACTICAL EXPERIENCE -->
  <div class="section-title">Internships & Practical Field Exposure</div>

  <!-- Role 1: Pencil Mark -->
  <div class="item-block">
    <div class="item-header">
      <div>
        <span class="role-title">Commercial Operations Intern</span> — <span class="company-name">Pencil Mark Interior Solutions LLP</span>
      </div>
      <div class="date-loc">July 2024 – Aug 2025 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Administered supplier vendor matrices, evaluated competing subcontractor quotations, and prepared comparative pricing sheets in MS Excel.</li>
      <li>Formulated commercial proposals and scope-of-work documentation, directly supporting the conversion of <strong>INR 1.5L+</strong> in secured B2B corporate contracts.</li>
      <li>Tracked purchase orders against delivery milestones and site sign-offs, maintaining 100% vendor SLA compliance and zero billing discrepancies.</li>
    </ul>
  </div>

  <!-- Role 2: Instawork -->
  <div class="item-block">
    <div class="item-header">
      <div>
        <span class="role-title">Operations & AI Data Verification Intern</span> — <span class="company-name">Instawork Services India Pvt. Ltd.</span>
      </div>
      <div class="date-loc">2025 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Executed high-volume multimodal data extraction and operational auditing adhering to strict standardized operating procedures (SOPs).</li>
      <li>Maintained a verified <strong>99.4% data accuracy rating</strong> across complex operational queues, filtering non-compliant assets before database ingestion.</li>
      <li>Collaborated with team supervisors to identify workflow bottlenecks, reducing review turnaround cycle time by <strong>12%</strong>.</li>
    </ul>
  </div>

  <!-- Role 3: Aero India -->
  <div class="item-block">
    <div class="item-header">
      <div>
        <span class="role-title">Exhibition Operations & Logistics Lead</span> — <span class="company-name">Salt in My Cocoa (Aero India 2025)</span>
      </div>
      <div class="date-loc">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
    </div>
    <ul class="bullets">
      <li>Directed on-ground stall setup, inventory replenishment, and security clearances across 5 days for <strong>100,000+ public and defense visitors</strong>.</li>
      <li>Established a strict dual-custody physical inventory protocol, achieving <strong>0% stock shrinkage</strong> and zero stock-outs during peak hours.</li>
      <li>Reconciled high-frequency digital UPI transactions daily against physical inventory ledgers with 100% financial balancing.</li>
    </ul>
  </div>

  <!-- Role 4: NGO / Community Ops -->
  <div class="item-block">
    <div class="item-header">
      <div>
        <span class="role-title">Community Operations Intern</span> — <span class="company-name">Non-Profit Social Initiative</span>
      </div>
      <div class="date-loc">2024 | Bengaluru, India</div>
    </div>
    <ul class="bullets">
      <li>Coordinated volunteer schedules, attendee registrations, and field logistics for social awareness drives across Bengaluru urban districts.</li>
      <li>Managed participant databases in Google Sheets and resolved on-ground operational dependencies under strict time constraints.</li>
    </ul>
  </div>

  <!-- TECHNICAL PROJECTS & AUTOMATION -->
  <div class="section-title">Technical Projects & Operational Automation</div>
  <div class="item-block">
    <div class="item-header">
      <div>
        <span class="role-title">Autonomous Operations & Recruitment Pipeline Engine</span> — <span class="company-name">Student Automation Project</span>
      </div>
      <div class="date-loc">2026 | Python, SQLite, Workday API</div>
    </div>
    <ul class="bullets">
      <li>Architected an automated operational dispatcher in Python parsing 430+ enterprise job requisitions with 16/16 unit tests passing green.</li>
      <li>Built interactive operational consoles eliminating repetitive manual tracking and automating requisition-to-candidate alignment.</li>
    </ul>
  </div>

  <!-- CERTIFICATIONS & LANGUAGES -->
  <div class="section-title">Certifications & Languages</div>
  <p style="font-size: 8.5pt; color: #334155;">
    <strong>Certifications:</strong> Digital Marketing Fundamentals (Google) • Service Marketing (NPTEL) • Enterprise Operational Excellence<br>
    <strong>Languages:</strong> English (Fluent Professional Proficiency), Hindi (Native / Bilingual)
  </p>

</div>

</body>
</html>
"""

os.makedirs('resumes', exist_ok=True)
os.makedirs('resumes_pdf', exist_ok=True)

html_path = os.path.abspath('resumes/Aditya_Mehra_Accenture_CV.html')
pdf_path = os.path.abspath('resumes_pdf/Aditya_Mehra_Accenture_Operations_CV.pdf')
root_pdf = os.path.abspath('Aditya_Mehra_Accenture_Operations_CV.pdf')
alias_pdf = os.path.abspath('resumes_pdf/Aditya_Mehra_Resume_001_accenture_india.pdf')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Wrote Fresher HTML CV to: {html_path}", flush=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]
subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    import shutil
    shutil.copyfile(pdf_path, root_pdf)
    shutil.copyfile(pdf_path, alias_pdf)
    print(f"Successfully compiled Fresher PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)", flush=True)
