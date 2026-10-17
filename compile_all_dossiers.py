#!/usr/bin/env python3
"""
Compiles all 10 Summer 2027 Application Dossiers into:
- Styled, printable HTML Resumes (RESUME.html)
- Styled, printable HTML Cover Letters (COVER_LETTER.html)
- Word Documents (ATS_RESUME.docx)
- High-resolution, ATS-formatted PDFs (ATS_RESUME.pdf) using Playwright (if browser available)
"""

import os
import json
import glob
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

PACKAGES_DIR = Path(r"e:\anti\applications_generated")

HTML_RESUME_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Aditya Mehra - Resume ({company} - {role})</title>
  <style>
    @page {{
      size: letter;
      margin: 0.5in;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #111827;
      line-height: 1.35;
      font-size: 10pt;
      margin: 0;
      padding: 24px;
    }}
    .header {{
      text-align: center;
      border-bottom: 2px solid #1e3a8a;
      padding-bottom: 8px;
      margin-bottom: 12px;
    }}
    .header h1 {{
      font-size: 18pt;
      margin: 0 0 4px 0;
      color: #0f172a;
      letter-spacing: 0.5px;
    }}
    .contact {{
      font-size: 9pt;
      color: #475569;
    }}
    .contact span {{
      margin: 0 5px;
    }}
    h2 {{
      font-size: 11pt;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #1e3a8a;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 2px;
      margin: 12px 0 6px 0;
    }}
    .job-title-row {{
      display: flex;
      justify-content: space-between;
      font-weight: 700;
      font-size: 10pt;
      color: #0f172a;
    }}
    .job-sub {{
      display: flex;
      justify-content: space-between;
      font-style: italic;
      font-size: 9pt;
      color: #475569;
      margin-bottom: 4px;
    }}
    ul {{
      margin: 0 0 8px 18px;
      padding: 0;
    }}
    li {{
      margin-bottom: 2px;
    }}
    .skills-block {{
      font-size: 9.5pt;
    }}
    .skills-block strong {{
      color: #0f172a;
    }}
  </style>
</head>
<body>

<div class="header">
  <h1>ADITYA MEHRA</h1>
  <div class="contact">
    Bangalore, India &bull; adityamehra007@gmail.com &bull; +91-7003456624 &bull; Open to Relocation ({locations})
  </div>
</div>

<h2>Professional Summary</h2>
<p style="margin: 0 0 10px 0;">
  Results-driven Operations & Systems Analyst with formal education in International Business (BBA 2026) and a verified track record orchestrating high-stakes ground logistics, multi-tier supply chains, and high-precision data workflows. Proven ability to bridge cross-functional teams, implement predictive operational models, and deliver 99%+ accuracy benchmarks. Targeted for the <strong>{role}</strong> at <strong>{company}</strong>.
</p>

<h2>Core Competencies</h2>
<div class="skills-block">
  <p style="margin: 0 0 3px 0;"><strong>Technical & Data:</strong> {skills}</p>
  <p style="margin: 0 0 3px 0;"><strong>Operations & Logistics:</strong> Supply Chain Planning, Vendor Management, Incident Response, Workflow Optimization, EXIM Compliance</p>
  <p style="margin: 0 0 8px 0;"><strong>Strategy & Governance:</strong> KPI Tracking, SLA Enforcement, Risk Auditing, Cross-Functional Leadership</p>
</div>

<h2>Verified Professional Experience</h2>

<div class="job-title-row">
  <span>Operations Lead — Ground Logistics & Staging</span>
  <span>Feb 2025</span>
</div>
<div class="job-sub">
  <span>Aero India 2025</span>
  <span>Bangalore, India</span>
</div>
<ul>
  <li>Orchestrated ground logistics and operational staging for 450+ international defense delegates and aerospace exhibitions under zero-failure parameters.</li>
  <li>Managed time-sensitive transport scheduling, security access control, and incident triage with 100% on-time execution.</li>
  <li>Designed dynamic dispatch tracking workflows to coordinate multi-vehicle motorcades across high-security corridors.</li>
</ul>

<div class="job-title-row">
  <span>Brand Activation & Logistics Operations Associate</span>
  <span>2024 – 2025</span>
</div>
<div class="job-sub">
  <span>Puma Sports India</span>
  <span>Bangalore, India</span>
</div>
<ul>
  <li>Managed end-to-end inventory staging, material flow, and supply chain logistics for major national brand activation campaigns.</li>
  <li>Coordinated with external suppliers and venue managers ensuring zero-defect asset deployment across 15+ activation sites.</li>
  <li>Reduced operational turnaround friction by 25% through standardized pre-event checklists and vendor SLA verification.</li>
</ul>

<div class="job-title-row">
  <span>Venue Operations Specialist</span>
  <span>2024</span>
</div>
<div class="job-sub">
  <span>Tata Communications</span>
  <span>Bangalore, India</span>
</div>
<ul>
  <li>Oversaw infrastructure readiness, media routing, and technical communications support during corporate summits.</li>
  <li>Triaged real-time operational bottlenecks, maintaining 99.9% uptime across presentation and networking infrastructure.</li>
</ul>

<div class="job-title-row">
  <span>AI Quality Benchmark Contributor</span>
  <span>2024 – Present</span>
</div>
<div class="job-sub">
  <span>Instawork</span>
  <span>Remote</span>
</div>
<ul>
  <li>Evaluated multi-turn reasoning and quality datasets, consistently attaining a verified <strong>99%+ accuracy rating</strong>.</li>
  <li>Audited model responses against structured criteria, providing actionable feedback for alignment pipelines.</li>
</ul>

<h2>Education</h2>
<div class="job-title-row">
  <span>Bachelor of Business Administration (BBA) — International Business</span>
  <span>Graduating 2026</span>
</div>
<div class="job-sub">
  <span>Dayananda Sagar University (DSU)</span>
  <span>Bangalore, India</span>
</div>
<p style="margin: 3px 0 0 0; font-size: 9pt; color: #475569;">
  Relevant Coursework: Global Supply Chain Management, Operations Research, International Trade Law, Business Statistics, Financial Modeling.
</p>

</body>
</html>
"""

HTML_COVER_LETTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cover Letter - Aditya Mehra ({company})</title>
  <style>
    @page {{
      size: letter;
      margin: 0.8in;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      line-height: 1.6;
      font-size: 11pt;
      margin: 0;
      padding: 40px;
      max-width: 800px;
    }}
    .header {{
      border-bottom: 2px solid #1e3a8a;
      padding-bottom: 12px;
      margin-bottom: 24px;
    }}
    .header h1 {{
      margin: 0;
      font-size: 20pt;
      color: #0f172a;
    }}
    .contact {{
      font-size: 9.5pt;
      color: #64748b;
      margin-top: 4px;
    }}
    .date {{
      margin: 20px 0;
      color: #64748b;
      font-size: 10pt;
    }}
    .recipient {{
      margin-bottom: 24px;
      line-height: 1.4;
    }}
    p {{
      margin-bottom: 16px;
    }}
    .highlight-box {{
      background: #f8fafc;
      border-left: 4px solid #1e3a8a;
      padding: 12px 16px;
      margin: 16px 0;
      font-size: 10pt;
    }}
    .sig {{
      margin-top: 32px;
    }}
  </style>
</head>
<body>

<div class="header">
  <h1>ADITYA MEHRA</h1>
  <div class="contact">
    Bangalore, India &bull; adityamehra007@gmail.com &bull; +91-7003456624 &bull; Open to Relocation ({locations})
  </div>
</div>

<div class="date">October 10, 2026</div>

<div class="recipient">
  <strong>Hiring Team & University Recruiting</strong><br>
  {company}<br>
  Re: Application for <strong>{role}</strong> ({locations})
</div>

<p>Dear Hiring Team at {company},</p>

<p>
  I am writing to express my strong enthusiasm for the <strong>{role}</strong> position at <strong>{company}</strong>. Having closely tracked {company}'s pioneering work in {sector}, I am eager to contribute my operational leadership, systems thinking, and data-driven discipline to your team during the Summer 2027 cohort.
</p>

<p>
  My background combines high-stakes operational execution with technical data analysis:
</p>

<div class="highlight-box">
  <p style="margin: 0 0 6px 0;"><strong>Key Qualifications & Verified Evidence:</strong></p>
  <ul style="margin: 0 0 0 18px; padding: 0;">
    <li><strong>Mission-Critical Execution:</strong> Led ground logistics at Aero India 2025 for 450+ international defense delegates with zero delays.</li>
    <li><strong>Quality & Accuracy Benchmark:</strong> Sustained a verified 99%+ accuracy rating on Instawork's AI evaluation platform.</li>
    <li><strong>Operational Optimization:</strong> Reduced vendor deployment friction by 25% managing supply chains for Puma Sports India.</li>
    <li><strong>Domain Capabilities:</strong> {skills}.</li>
  </ul>
</div>

<p>
  {mission}
</p>

<p>
  I am prepared to hit the ground running on Day 1, bringing high velocity, accountability, and rigor to {company}'s mission. Thank you for your consideration, and I look forward to speaking with your team.
</p>

<div class="sig">
  Sincerely,<br><br>
  <strong>Aditya Mehra</strong><br>
  BBA International Business (DSU 2026)<br>
  Bangalore, India
</div>

</body>
</html>
"""

def build_docx(pkg_dir, manifest):
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.5)
        s.right_margin = Inches(0.5)
        
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_name = p_name.add_run("ADITYA MEHRA")
    run_name.font.name = "Calibri"
    run_name.font.size = Pt(16)
    run_name.font.bold = True
    run_name.font.color.rgb = RGBColor(15, 23, 42)

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_contact = p_contact.add_run(f"Bangalore, India | adityamehra007@gmail.com | +91-7003456624 | Open to Relocation ({manifest['locations']})")
    run_contact.font.name = "Calibri"
    run_contact.font.size = Pt(9.5)
    run_contact.font.color.rgb = RGBColor(71, 85, 105)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)

    add_h2("Professional Summary")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_after = Pt(6)
    r_sum = p_sum.add_run(f"Results-driven Operations & Systems Analyst with formal education in International Business (BBA 2026) and hands-on track record executing mission-critical ground operations, supply chain logistics, and high-precision data workflows. Targeting {manifest['target_role']} at {manifest['company_name']}.")
    r_sum.font.name = "Calibri"
    r_sum.font.size = Pt(10)

    add_h2("Core Competencies")
    p_comp = doc.add_paragraph()
    p_comp.paragraph_format.space_after = Pt(6)
    r_c1 = p_comp.add_run(f"Technical: {manifest.get('category', 'Data & Analytics')}\nOperations: Global Logistics, Vendor SLA, EXIM Compliance\nLeadership: Stakeholder Coordination, KPI Dashboards, Incident Command")
    r_c1.font.name = "Calibri"
    r_c1.font.size = Pt(9.5)

    add_h2("Verified Professional Experience")
    
    exp_items = [
        ("Operations Lead — Ground Logistics & Staging", "Aero India 2025 | Feb 2025", [
            "Orchestrated ground logistics and operational staging for 450+ international defense delegates.",
            "Managed time-sensitive transport scheduling and access control with 100% on-time execution.",
            "Designed dynamic dispatch tracking workflows across high-security corridors."
        ]),
        ("Brand Activation & Logistics Operations Associate", "Puma Sports India | 2024 – 2025", [
            "Managed end-to-end inventory staging and supply chain logistics for major national brand activation campaigns.",
            "Ensured zero-defect asset deployment across 15+ activation sites.",
            "Reduced turnaround friction by 25% through standardized pre-event checklists."
        ]),
        ("Venue Operations Specialist", "Tata Communications | 2024", [
            "Oversaw infrastructure readiness and communications support during corporate summits.",
            "Maintained 99.9% uptime across presentation and networking infrastructure."
        ]),
        ("AI Quality Benchmark Contributor", "Instawork | 2024 – Present", [
            "Evaluated multi-turn reasoning and quality datasets, consistently attaining a verified 99%+ accuracy rating."
        ])
    ]

    for title, sub, bullets in exp_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(4)
        p_t.paragraph_format.space_after = Pt(0)
        r_t = p_t.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(10)
        r_sub = p_t.add_run(f" — {sub}")
        r_sub.font.italic = True
        r_sub.font.size = Pt(9.5)
        r_sub.font.color.rgb = RGBColor(100, 116, 139)

        for b in bullets:
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_after = Pt(1)
            p_b.paragraph_format.space_before = Pt(0)
            r_b = p_b.add_run(b)
            r_b.font.size = Pt(9.5)

    add_h2("Education")
    p_edu = doc.add_paragraph()
    r_edu = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business (Graduating 2026)\nDayananda Sagar University (DSU), Bangalore, India")
    r_edu.font.size = Pt(9.5)

    docx_path = os.path.join(pkg_dir, "ATS_RESUME.docx")
    doc.save(docx_path)
    return docx_path

def build_all_assets():
    pkg_dirs = sorted(glob.glob(os.path.join(str(PACKAGES_DIR), "APX-2027-*")))
    print(f"Found {len(pkg_dirs)} Summer 2027 target packages.")

    skills_map = {
        "APX-2027-001": "SQL, Python, PowerBI, Tableau, Predictive Modeling, Organizational Analytics",
        "APX-2027-002": "AI Governance, PRD Authoring, Risk Auditing, Feature Prioritization, A/B Testing",
        "APX-2027-003": "Supply Chain Analytics, Python, SQL, Power BI, EXIM Clearance, Vendor Risk Modeling",
        "APX-2027-004": "Financial Modeling, SQL, Python, Business Strategy, Unit Economics, Data Storytelling",
        "APX-2027-005": "API Diagnostics, Developer Workflow Operations, Incident Triage, SLA Governance",
        "APX-2027-006": "Python, C++, Bash/PowerShell, Automation Frameworks, Git, REST APIs, Telemetry",
        "APX-2027-007": "Python (pandas, numpy), SQL, Time-Series Analysis, Market Microstructure, Statistics",
        "APX-2027-008": "Product Management, FinTech Architecture, Regulatory Compliance, User Journey Mapping",
        "APX-2027-009": "Operations Telemetry, Python, Data Dashboards, SLA Tracking, Incident Command Systems",
        "APX-2027-010": "Semiconductor Supply Chain, MRP/ERP, Inventory Optimization, Python, EXIM Compliance"
    }

    mission_map = {
        "APX-2027-001": "Deliver real-time analytics, automated workforce forecasting models, and workflow tooling across Tesla's engineering and operations organization.",
        "APX-2027-002": "Design governance frameworks, risk taxonomy systems, and automated evaluation metrics for multi-modal AI ecosystems.",
        "APX-2027-003": "Build predictive lead-time trackers, multi-tier supplier disruption monitors, and automated cost variance models for assembly lines.",
        "APX-2027-004": "Conduct customer cohort retention analysis, unit economics modeling, and automated KPI reporting across financial software ecosystems.",
        "APX-2027-005": "Streamline partner developer onboarding, triage API feedback loops, and design operational playbooks for third-party platform partners.",
        "APX-2027-006": "Develop automation test scripts, CI/CD pipelines, and hardware diagnostic tools for next-generation engineering validation.",
        "APX-2027-007": "Clean, validate, and backtest high-frequency market data feeds, anomaly detection pipelines, and systematic trade execution analytics.",
        "APX-2027-008": "Define product requirements for digital payment authorization workflows, merchant fraud deterrence systems, and customer loyalty engines.",
        "APX-2027-009": "Optimize depot turnaround times, sensor calibration throughput, remote assistance dispatch telemetry, and fleet readiness KPIs.",
        "APX-2027-010": "Model fab allocation forecasts, wafer inventory buffers, substrate delivery tracking, and supplier risk metrics across AI accelerator product lines."
    }

    for p in pkg_dirs:
        m_file = os.path.join(p, "APPLICATION_MANIFEST.json")
        with open(m_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        app_id = manifest["application_id"]
        company = manifest["company_name"]
        role = manifest["target_role"]
        locations = manifest["locations"]
        sector = manifest["sector"]
        skills = skills_map.get(app_id, "Python, SQL, Operations Research, Workflow Automation")
        mission = mission_map.get(app_id, "Contribute to cutting-edge operations and technical systems.")

        # Build HTML Resume
        resume_html = HTML_RESUME_TEMPLATE.format(
            company=company,
            role=role,
            locations=locations,
            skills=skills
        )
        r_path = os.path.join(p, "RESUME.html")
        with open(r_path, "w", encoding="utf-8") as f:
            f.write(resume_html)

        # Build HTML Cover Letter
        cover_html = HTML_COVER_LETTER_TEMPLATE.format(
            company=company,
            role=role,
            locations=locations,
            sector=sector,
            skills=skills,
            mission=mission
        )
        c_path = os.path.join(p, "COVER_LETTER.html")
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(cover_html)

        # Build Word Document (.docx)
        docx_path = build_docx(p, manifest)

        print(f"[✓] Built HTML & DOCX for {app_id}: {company}")

    print("\n[+] Attempting PDF compilation using Playwright...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for p in pkg_dirs:
                r_html = Path(p) / "RESUME.html"
                r_pdf = Path(p) / "ATS_RESUME.pdf"
                page = browser.new_page()
                page.goto(r_html.as_uri())
                page.pdf(path=str(r_pdf), format="Letter", print_background=True, margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"})
                page.close()
                print(f"[✓] Compiled PDF: {r_pdf.name} for {Path(p).name}")
            browser.close()
        print("[✓] All PDFs compiled successfully!")
    except Exception as e:
        print(f"[!] Playwright PDF generation note: {e}")

if __name__ == "__main__":
    build_all_assets()
