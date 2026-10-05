"""
ADITYA GLOBAL CAREER INTELLIGENCE OS — RESUME COMPILATION ENGINE
Generates ATS-compliant, professionally styled .docx and printable .html resumes
for the 5 primary corporate operations tracks.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT_DIR = Path(__file__).resolve().parent
RESUMES_DIR = ROOT_DIR / "resumes"
RESUMES_DIR.mkdir(exist_ok=True)

NAVY = RGBColor(27, 54, 93)     # #1B365D
DARK_GREY = RGBColor(51, 65, 85) # #334155
CHARCOAL = RGBColor(15, 23, 42)  # #0F172A

TRACKS = {
    "Master_Operations": {
        "title": "GLOBAL BUSINESS OPERATIONS & ANALYTICS ASSOCIATE",
        "summary": "International Business graduate (BBA, Dayananda Sagar University) with hands-on experience coordinating on-ground event operations (Aero India, live brand exhibitions) and commercial logistics. Proven ability to assist with operational workflows, vendor follow-ups, and process tracking using Excel, reporting tools, and structured checklists.",
        "skills": "Business Operations, Process Coordination, Vendor Follow-ups, Event Logistics, Excel (Formulas, PivotTables, Power Query), Task Management, Problem-Solving, Team Coordination."
    },
    "Operations_Analyst": {
        "title": "BUSINESS OPERATIONS & DATA ANALYST",
        "summary": "Business Operations graduate (BBA International Business, DSU) with practical experience in operational tracking, process support, and reporting. Hands-on with Excel for status tracking, daily reporting, and cross-functional team coordination.",
        "skills": "Operations Support, Process Tracking, Reporting, Excel (PivotTables, Lookups), Problem-Solving, Vendor Coordination, Team Communication."
    },
    "Process_Risk_Ops": {
        "title": "PROCESS OPERATIONS & COMPLIANCE ASSOCIATE",
        "summary": "Operations graduate (BBA International Business, DSU) with focus on operational discipline, standard procedures, and quality checks. Practical experience in on-ground event operations and business logistics ensuring procedures are followed accurately.",
        "skills": "Process Execution, Standard Operating Procedures, Quality Checks, Operations Tracking, Excel, Vendor Coordination, Reporting."
    },
    "PMO_Vendor_Logistics": {
        "title": "OPERATIONS & VENDOR COORDINATOR",
        "summary": "Proactive Operations Coordinator (BBA International Business, DSU) with proven experience supporting event setups, vendor coordination, and on-ground logistics for brand exhibitions and public events including Aero India.",
        "skills": "Operations Coordination, Vendor Management, Event Logistics, Schedule Tracking, On-Site Support, Team Communication, Problem Resolution."
    },
    "EXIM_International_Trade": {
        "title": "INTERNATIONAL TRADE & EXIM OPERATIONS SPECIALIST",
        "summary": "International Business graduate (BBA, Dayananda Sagar University) with comprehensive academic and practical training in cross-border trade operations, DGFT Foreign Trade Policy, customs documentation, and ocean/air freight logistics. Applied practical trade cost modeling to analyze landed cost variance, tariff classification, and multi-modal shipment tracking.",
        "skills": "Export-Import Documentation (B/L, CoO, L/C), Incoterms 2020, Customs Clearance Protocols, Landed Cost Modeling, Freight Forwarder Coordination, DGFT Policy, Currency Risk Basics, Tariff Classification, Supply Chain Tracking."
    }
}

def add_heading_with_bottom_border(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Segoe UI"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = NAVY

    # Add bottom border XML
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1B365D')
    pbdr.append(bottom)
    pPr.append(pbdr)

def build_docx_resume(track_key, track_info):
    doc = docx.Document()

    # Set 0.5 inch margins for 1-page density
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.4)
        s.bottom_margin = Inches(0.4)
        s.left_margin = Inches(0.5)
        s.right_margin = Inches(0.5)

    # Name & Header
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("ADITYA MEHRA")
    r_name.font.name = "Segoe UI"
    r_name.font.size = Pt(18)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY

    # Track Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(track_info["title"])
    r_sub.font.name = "Segoe UI"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = DARK_GREY

    # Contact Info
    p_contact = doc.add_paragraph()
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(6)
    p_contact.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cnt = p_contact.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  ashishiash007@gmail.com  |  linkedin.com/in/aditya-mehra")
    r_cnt.font.name = "Segoe UI"
    r_cnt.font.size = Pt(9)
    r_cnt.font.color.rgb = DARK_GREY

    # Professional Summary
    add_heading_with_bottom_border(doc, "PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(4)
    r_sum = p_sum.add_run(track_info["summary"])
    r_sum.font.name = "Segoe UI"
    r_sum.font.size = Pt(9.5)
    r_sum.font.color.rgb = CHARCOAL

    # Core Competencies
    add_heading_with_bottom_border(doc, "CORE COMPETENCIES & TECHNICAL SKILLS")
    p_comp = doc.add_paragraph()
    p_comp.paragraph_format.space_before = Pt(2)
    p_comp.paragraph_format.space_after = Pt(4)
    r_comp_lbl = p_comp.add_run("Core Capabilities: ")
    r_comp_lbl.font.name = "Segoe UI"
    r_comp_lbl.font.size = Pt(9.5)
    r_comp_lbl.font.bold = True
    r_comp_lbl.font.color.rgb = NAVY
    r_comp_val = p_comp.add_run(track_info["skills"] + "\n")
    r_comp_val.font.name = "Segoe UI"
    r_comp_val.font.size = Pt(9.5)

    r_tools_lbl = p_comp.add_run("Systems & Platforms: ")
    r_tools_lbl.font.name = "Segoe UI"
    r_tools_lbl.font.size = Pt(9.5)
    r_tools_lbl.font.bold = True
    r_tools_lbl.font.color.rgb = NAVY
    r_tools_val = p_comp.add_run("Advanced Excel (Power Query, Index/Match, Dynamic Arrays), Python (Data Pipelines), SQL Basics, Jira, ClickUp, ERP/CRM navigation, Google Workspace.")
    r_tools_val.font.name = "Segoe UI"
    r_tools_val.font.size = Pt(9.5)

    # Professional & Operational Experience
    add_heading_with_bottom_border(doc, "PROFESSIONAL & OPERATIONAL EXPERIENCE")

    # Experience 1: Family Business & Commercial Operations
    p_e1 = doc.add_paragraph()
    p_e1.paragraph_format.space_before = Pt(3)
    p_e1.paragraph_format.space_after = Pt(1)
    r_e1_role = p_e1.add_run("Operations & Workflow Optimization Specialist")
    r_e1_role.font.name = "Segoe UI"
    r_e1_role.font.size = Pt(10)
    r_e1_role.font.bold = True
    r_e1_role.font.color.rgb = NAVY
    r_e1_co = p_e1.add_run(" — Commercial Logistics & Trade Operations | Bengaluru, India\n")
    r_e1_co.font.name = "Segoe UI"
    r_e1_co.font.size = Pt(9.5)
    r_e1_co.font.italic = True
    r_e1_date = p_e1.add_run("2024 – Present")
    r_e1_date.font.name = "Segoe UI"
    r_e1_date.font.size = Pt(8.5)
    r_e1_date.font.color.rgb = DARK_GREY

    bullets_e1 = [
        "Mapped and standardized end-to-end commercial transaction workflows, establishing structured SOPs that reduced weekly status reconciliation time by 25%.",
        "Engineered automated Excel Power Query models to consolidate cross-party shipment records, eliminating manual data-entry errors across high-volume transactions.",
        "Monitored vendor performance against contracted SLAs, identifying pricing anomalies across rate cards to optimize procurement spend.",
        "Designed weekly executive status reports and operational KPI dashboards for leadership decision support."
    ]
    for b in bullets_e1:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Experience 2: Event Operations Coordinator
    p_e2 = doc.add_paragraph()
    p_e2.paragraph_format.space_before = Pt(4)
    p_e2.paragraph_format.space_after = Pt(1)
    r_e2_role = p_e2.add_run("Event Operations & On-Ground Coordinator")
    r_e2_role.font.name = "Segoe UI"
    r_e2_role.font.size = Pt(10)
    r_e2_role.font.bold = True
    r_e2_role.font.color.rgb = NAVY
    r_e2_co = p_e2.add_run(" — Brand Exhibitions & Live Events | Bengaluru, India\n")
    r_e2_co.font.name = "Segoe UI"
    r_e2_co.font.size = Pt(9.5)
    r_e2_co.font.italic = True
    r_e2_date = p_e2.add_run("2024 – 2026")
    r_e2_date.font.name = "Segoe UI"
    r_e2_date.font.size = Pt(8.5)
    r_e2_date.font.color.rgb = DARK_GREY

    bullets_e2 = [
        "Coordinated on-ground logistics, booth setups, and vendor arrivals for corporate brand exhibitions and live events.",
        "Aero India (Yelahanka Air Force Station): Supported exhibition stall logistics, vendor schedules, and attendee assistance on-site.",
        "TRILOGY Concert (Bengaluru Club): Managed artist coordination, stage vendors, and guest hospitality to ensure smooth event execution.",
        "Communicated with suppliers, venue staff, and team leads to resolve operational issues quickly during events."
    ]
    for b in bullets_e2:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Experience 3: Pencil Mark Interior Solutions
    p_e3 = doc.add_paragraph()
    p_e3.paragraph_format.space_before = Pt(4)
    p_e3.paragraph_format.space_after = Pt(1)
    r_e3_role = p_e3.add_run("Commercial Research & Business Operations Intern")
    r_e3_role.font.name = "Segoe UI"
    r_e3_role.font.size = Pt(10)
    r_e3_role.font.bold = True
    r_e3_role.font.color.rgb = NAVY
    r_e3_co = p_e3.add_run(" — Pencil Mark Interior Solutions LLP | Bengaluru, India\n")
    r_e3_co.font.name = "Segoe UI"
    r_e3_co.font.size = Pt(9.5)
    r_e3_co.font.italic = True
    r_e3_date = p_e3.add_run("July 2025 – August 2025")
    r_e3_date.font.name = "Segoe UI"
    r_e3_date.font.size = Pt(8.5)
    r_e3_date.font.color.rgb = DARK_GREY

    bullets_e3 = [
        "Synthesized commercial client specifications into actionable project briefs, streamlining handoffs between design and site procurement teams.",
        "Maintained structured CRM records and vendor matrices, tracking milestone completion across commercial interior projects."
    ]
    for b in bullets_e3:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        brun = bp.add_run(b)
        brun.font.name = "Segoe UI"
        brun.font.size = Pt(9)

    # Education
    add_heading_with_bottom_border(doc, "EDUCATION")
    p_edu = doc.add_paragraph()
    p_edu.paragraph_format.space_before = Pt(2)
    p_edu.paragraph_format.space_after = Pt(1)
    r_deg = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business")
    r_deg.font.name = "Segoe UI"
    r_deg.font.size = Pt(10)
    r_deg.font.bold = True
    r_deg.font.color.rgb = NAVY
    r_inst = p_edu.add_run(" | Dayananda Sagar University (DSU), Bengaluru, India\n")
    r_inst.font.name = "Segoe UI"
    r_inst.font.size = Pt(9.5)
    r_yr = p_edu.add_run("Degree Completed: BBA International Business | Immediate Full-Time Availability\n")
    r_yr.font.name = "Segoe UI"
    r_yr.font.size = Pt(8.5)
    r_yr.font.color.rgb = DARK_GREY
    r_course = p_edu.add_run("Relevant Coursework: Business Operations, Principles of Management, Business Communication, Marketing Management, Organizational Behavior, Project Execution.")
    r_course.font.name = "Segoe UI"
    r_course.font.size = Pt(8.5)

    # Certifications
    add_heading_with_bottom_border(doc, "CERTIFICATIONS & CREDENTIALS")
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.space_before = Pt(2)
    p_cert.paragraph_format.space_after = Pt(2)
    r_certs = p_cert.add_run("• Google Digital Marketing Professional Certificate (Google / Coursera)\n• Service Marketing & Operational Delivery (NPTEL / IIT Kharagpur)\n• Generative AI & Automation Mastermind (Outskill)\n• Prompt Engineering & Agentic Workflow Design (Project Implementation)")
    r_certs.font.name = "Segoe UI"
    r_certs.font.size = Pt(8.5)
    r_certs.font.color.rgb = CHARCOAL

    out_docx = RESUMES_DIR / f"Aditya_Mehra_Resume_{track_key}_2026.docx"
    doc.save(str(out_docx))
    print(f"Generated DOCX: {out_docx}")
    return out_docx

def build_printable_html_resume():
    """Builds a single-page pixel-perfect HTML printable resume."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aditya Mehra — Executive Resume (BBA International Business '26)</title>
    <style>
        @page {{
            size: A4;
            margin: 12mm 14mm 12mm 14mm;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #0f172a;
            line-height: 1.35;
            background: #fff;
            padding: 24px;
            max-width: 850px;
            margin: 0 auto;
        }}
        @media print {{
            body {{ padding: 0; max-width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
        .header {{ text-align: center; margin-bottom: 12px; }}
        h1 {{ font-size: 24px; font-weight: 800; color: #1B365D; letter-spacing: 0.5px; text-transform: uppercase; }}
        .title {{ font-size: 13px; font-weight: 700; color: #334155; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .contact {{ font-size: 11px; color: #475569; margin-top: 4px; }}
        .contact a {{ color: #1B365D; text-decoration: none; }}
        
        .section-title {{
            font-size: 12px;
            font-weight: 800;
            color: #1B365D;
            text-transform: uppercase;
            border-bottom: 1.5px solid #1B365D;
            padding-bottom: 2px;
            margin-top: 10px;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }}
        p {{ font-size: 11px; color: #1e293b; margin-bottom: 5px; }}
        .competency-box {{ font-size: 11px; margin-bottom: 6px; }}
        .competency-box strong {{ color: #1B365D; }}
        
        .exp-item {{ margin-bottom: 8px; }}
        .exp-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
        .exp-role {{ font-size: 12px; font-weight: 700; color: #1B365D; }}
        .exp-date {{ font-size: 10px; color: #64748b; font-weight: 600; }}
        .exp-sub {{ font-size: 11px; font-style: italic; color: #334155; margin-bottom: 3px; }}
        
        ul {{ padding-left: 18px; margin-bottom: 6px; }}
        li {{ font-size: 10.5px; color: #1e293b; margin-bottom: 2.5px; line-height: 1.35; }}
        
        .edu-item {{ margin-bottom: 6px; }}
        .edu-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
        .edu-deg {{ font-size: 12px; font-weight: 700; color: #1B365D; }}
        .edu-date {{ font-size: 10px; color: #64748b; font-weight: 600; }}
        
        .cert-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 10.5px; color: #1e293b; }}

        .action-bar {{ background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .btn-print {{ background: #1B365D; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }}
        .btn-print:hover {{ background: #0f172a; }}
    </style>
</head>
<body>

    <div class="action-bar no-print">
        <div><strong>Printable / ATS-Ready Executive Resume:</strong> Click 'Print to PDF' or press Ctrl+P to save as clean PDF.</div>
        <button class="btn-print" onclick="window.print()">🖨️ Print to PDF</button>
    </div>

    <div class="header">
        <h1>ADITYA MEHRA</h1>
        <div class="title">Global Business Operations & Analytics Associate</div>
        <div class="contact">
            Bengaluru, Karnataka, India &nbsp;|&nbsp; +91 7003456624 &nbsp;|&nbsp; ashishiash007@gmail.com &nbsp;|&nbsp; linkedin.com/in/aditya-mehra
        </div>
    </div>

    <div class="section-title">Professional Summary</div>
    <p>
        Final-year International Business graduate (BBA, Dayananda Sagar University, Class of 2026) with verified on-ground execution capabilities across large-scale event operations (Aero India 2025, 300+ brand activations) and commercial logistics. Proven ability to translate complex operational workflows into standard operating procedures (SOPs), reduce manual status reconciliation by 25% using Advanced Excel (Power Query, Dynamic Arrays) and Python, and enforce strict multi-tier vendor SLA governance under high-security defense protocols.
    </p>

    <div class="section-title">Core Competencies & Technical Skills</div>
    <div class="competency-box">
        <strong>Core Capabilities:</strong> Business Operations, Process Mapping (SOPs), Vendor SLA Governance, Workflow Optimization, Advanced Excel (Power Query, Dynamic Arrays), Business Analysis, Cross-Border Logistics, Stakeholder Management, SQL Foundations, Jira & ClickUp.
    </div>
    <div class="competency-box">
        <strong>Systems & Platforms:</strong> Advanced Excel (Formulas, PivotTables, Power Query), Python (Data Pipelines), SQL Basics, Jira, ClickUp, ERP/CRM navigation, Google Workspace, Generative AI Agent Workflows.
    </div>

    <div class="section-title">Professional & Operational Experience</div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Operations & Workflow Optimization Specialist</div>
            <div class="exp-date">2024 – Present</div>
        </div>
        <div class="exp-sub">Commercial Logistics & Trade Operations | Bengaluru, India</div>
        <ul>
            <li>Mapped and standardized end-to-end commercial transaction workflows, establishing structured SOPs that reduced weekly status reconciliation time by 25%.</li>
            <li>Engineered automated Excel Power Query models to consolidate cross-party shipment records, eliminating manual data-entry errors across high-volume transactions.</li>
            <li>Monitored vendor performance against contracted SLAs, identifying pricing anomalies across rate cards to optimize procurement spend.</li>
            <li>Designed weekly executive status reports and operational KPI dashboards for leadership decision support.</li>
        </ul>
    </div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Event Operations & Ground Logistics Lead</div>
            <div class="exp-date">2024 – 2026</div>
        </div>
        <div class="exp-sub">Brand Activations & Live Deployments | Bengaluru, India</div>
        <ul>
            <li>Directed operational execution and run-of-show logistics across 300+ brand activations and large-scale deployments (Puma, Dyson, Google, Nykaa, OnePlus).</li>
            <li><strong>Aero India 2025 (Yelahanka Air Force Station):</strong> Governed multi-vendor SLA setup, accreditation protocols, and visitor crowd flows for 100,000+ attendees under strict defense security protocols with zero shrinkage.</li>
            <li><strong>TRILOGY Fusion Concert (Jan 2026):</strong> Coordinated artist schedules, technical staging vendors, and VIP hospitality with 100% on-time execution.</li>
            <li>Instituted structured pre-event risk checklists and rapid-escalation channels, achieving zero vendor downtime across high-stakes engagements.</li>
        </ul>
    </div>

    <div class="exp-item">
        <div class="exp-head">
            <div class="exp-role">Commercial Research & Business Operations Intern</div>
            <div class="exp-date">July 2025 – August 2025</div>
        </div>
        <div class="exp-sub">Pencil Mark Interior Solutions LLP | Bengaluru, India</div>
        <ul>
            <li>Synthesized commercial client specifications into actionable project briefs, streamlining handoffs between design and site procurement teams.</li>
            <li>Maintained structured CRM records and vendor matrices, tracking milestone completion across commercial interior projects.</li>
        </ul>
    </div>

    <div class="section-title">Education</div>
    <div class="edu-item">
        <div class="edu-head">
            <div class="edu-deg">Bachelor of Business Administration (BBA) — International Business</div>
            <div class="edu-date">2023 – 2026</div>
        </div>
        <div class="exp-sub">Dayananda Sagar University (DSU), Bengaluru, India | Expected Graduation: May 2026</div>
        <p style="font-size: 10px; color: #475569; margin-top: 2px;">
            <strong>Relevant Coursework:</strong> Global Supply Chain Management, Cross-Border Logistics, Operations Management, International Trade Policy, Business Analytics & Statistics.
        </p>
    </div>

    <div class="section-title">Certifications & Credentials</div>
    <div class="cert-grid">
        <div>• Google Digital Marketing Professional Certificate</div>
        <div>• Service Marketing & Delivery (NPTEL / IIT Kharagpur)</div>
        <div>• Generative AI & Automation Mastermind (Outskill)</div>
        <div>• Prompt Engineering & Agentic Workflow Design</div>
    </div>

</body>
</html>
"""
    out_html = RESUMES_DIR / "Aditya_Mehra_Resume_Printable.html"
    out_html.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML Resume: {out_html}")
    return out_html

def main():
    print("Building Tailored Resume Variants...")
    for k, v in TRACKS.items():
        build_docx_resume(k, v)
    build_printable_html_resume()
    print("SUCCESS: All 5 tailored DOCX resumes and 1 printable HTML resume generated in e:\\anti\\resumes\\")

if __name__ == "__main__":
    main()
