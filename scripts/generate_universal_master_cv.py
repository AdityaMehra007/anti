import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import subprocess

BASE_DIR = Path(r"e:\anti")

# 1. GENERATE MASTER MARKDOWN CV
md_content = """# ADITYA MEHRA
**Bengaluru, Karnataka, India** | **+91 7003456624** | **adityamehra799@gmail.com**  
**LinkedIn:** [linkedin.com/in/aditya-mehra-b8644b326](https://linkedin.com/in/aditya-mehra-b8644b326) | **Portfolio & Code:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## PROFESSIONAL SUMMARY
High-performing **Business Operations & Commercial Growth Specialist** with an extensive track record delivering **300+ live events and commercial activations**, managing mission-critical operations at **AERO India 2025** (100k+ attendees, 0 shrinkage), and training robotics AI data pipelines at **Instawork** with **99%+ QA accuracy**. Combines a rigorous **BBA in International Business** (Dayananda Sagar University, 2026) with proven capabilities in vendor SLA governance, 15–20% procurement cost reduction, B2B pipeline conversion, and modern AI process automation. Recognized with a formal written management commendation for exceptional business development performance. Seeking to drive operational excellence and enterprise value in high-growth MNCs, GCCs, and modern technology enterprises.

---

## CORE COMPETENCIES

- **Business & Operational Leadership:** End-to-End Project Delivery (300+ Events), Vendor SLA Governance, Rate Card Modeling, 15–20% Landed Cost Optimization, On-Ground Crisis Triage.
- **Commercial & B2B Growth:** Pipeline Qualification, Enterprise Client Pitching (Tata Communications, Puma India), Multi-Thread Deal Management (15+ Threads), High-Ticket Negotiation.
- **AI & Process Automation:** Robotics Data Curation & Multi-Modal Annotation, Prompt Engineering, Autonomous Workflow Design, Python & LLM Data Synthesis, Clay & Notion AI.
- **Global Trade & Supply Chain:** Incoterms 2020 (FOB, CIF, DDP), Letter of Credit (UCP 600) Principles, 3PL Freight Coordination, Inventory Buffer Modeling, Regulatory Compliance.
- **Analytics & Systems:** Advanced MS Excel (XLOOKUP, Power Query, Dynamic Pivot Tables), Salesforce & Zoho CRM, SQL Basics, P&L & Margin Economics.
- **Languages:** English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).

---

## PROFESSIONAL EXPERIENCE

### INDEPENDENT EVENT DIRECTOR & COMMERCIAL OPERATIONS LEAD
**Independent Commercial Operations** | *Bengaluru, India* | **2019 – Present**
- **Scaled Multi-Format Operations:** Spearheaded and delivered **300+ live events**, corporate conferences, and brand activations for marquee clients including **Tata Communications**, **Puma India**, **VH1 Supersonic**, and **Apollo Marketing**.
- **Procurement & Margin Expansion:** Achieved consistent **15% to 20% cost savings** per engagement by eliminating intermediary markups, structuring standardized direct supplier rate cards, and enforcing milestone-driven SLAs across 20+ vendors.
- **Sustained Account Retention:** Maintained an exceptional **30%+ repeat-client rate** through high-touch client servicing, transparent budget reconciliation, and flawless on-ground delivery under compressed turnaround times.
- **Crisis Leadership & Rapid Triage:** Executed zero-downtime crisis management during adverse operational situations (including venue re-allocations and technical equipment triage), ensuring 100% on-time execution without client SLA breach.

### AI DATA OPERATIONS INTERN
**Instawork Services India Pvt. Ltd.** | *Bengaluru, India* | **Dec 2025**
- **Robotics & Vision Data Pipeline:** Supported machine learning training pipelines for enterprise robotics and human activity recognition, capturing and structuring high-volume multi-modal datasets.
- **Flawless Quality Assurance:** Maintained a **99%+ quality assurance benchmark**, performing granular annotation validation, schema adherence checks, and edge-case classification to eliminate model training drift.
- **Cross-Functional Standardization:** Bridged ground operational execution with machine learning engineering priorities, establishing standardized dataset capture protocols that cut reporting latency.

### BUSINESS DEVELOPMENT INTERN
**Pencil Mark Interior Solutions LLP** | *Bengaluru, India* | **Jul 2025 – Aug 2025**
- **Pipeline Acceleration:** Drove B2B client acquisition across Bengaluru commercial interior and corporate workspace projects, expanding the active commercial lead pipeline and closing **₹1.5L+ in initial contract revenue**.
- **Multi-Thread Account Servicing:** Orchestrated **15+ concurrent client communication workflows**, slashing inquiry turnaround time and achieving an **18% lead-to-opportunity conversion rate**.
- **Executive Commendation:** Awarded a formal **written management commendation** by executive leadership for outstanding pipeline expansion, proactive client negotiation, and exceptional commercial drive.

### EXHIBITION OPERATIONS & COMMERCIAL LEAD
**Salt in My Coca — AERO India 2025** | *Yelahanka Air Force Station, Bengaluru* | **Feb 2025**
- **High-Stakes Operational Execution:** Directed full 7-day stall setup, high-value client engagement, and inventory logistics at Asia's premier aerospace defense exposition (**100,000+ attendees**).
- **Strict Protocol Compliance:** Governed supply logistics and physical assets under stringent Ministry of Defence security clearances, access schedules, and active flight display windows with **zero asset loss or inventory shrinkage**.
- **Executive Engagement:** Interfaced directly with global aerospace executives, military liaisons, and enterprise delegates to qualify commercial leads and elevate brand presence.

### EVENT OPERATIONS COORDINATOR
**TRILOGY: Indo-Jazz Instrumental Fusion** | *Bangalore Club, Bengaluru* | **Jan 2026**
- **Live Showcase Governance:** Coordinated end-to-end production for an elite live instrumental performance, managing artist transit logistics, hospitality, technical riders, and AV acoustic crew timelines.
- **Real-Time Technical Coordination:** Resolved live venue acoustics and multi-team schedule constraints with zero disruption to stage performance, earning unanimous praise from venue patrons.

### CO-FOUNDER & OPERATIONS MANAGER
**Mehra's Kitchen** | *Bengaluru, India* | **2025**
- **Unit Economics & P&L Oversight:** Established commercial operational workflows for food-stall and cloud-kitchen operations, overseeing ingredient procurement, supplier negotiations, and daily cash flow reconciliation.
- **Process Optimization:** Modeled landed ingredient costs and optimized supplier turnaround times to protect operating margins and ensure consistent quality standards.

### OPERATIONS & SALES ASSOCIATE
**Family Enterprise** | *Kolkata & Bengaluru, India* | **2018 – 2020**
- **Foundational Commercial Discipline:** Began commercial career at age 17 managing retail customer relationships, inventory turnover, daily sales transactions, and supplier logistics in a high-velocity trading business.

---

## EDUCATION

### BACHELOR OF BUSINESS ADMINISTRATION (BBA) — INTERNATIONAL BUSINESS
**Dayananda Sagar University**, *Bengaluru, India* | **2023 – 2026**
- **Core Focus:** International Trade Policy, Incoterms 2020, Global Supply Chain Architecture, Foreign Exchange Management, Financial Accounting, Business Statistics.
- **Applied Project Work:** Landed cost modeling, cross-border freight risk mitigation, and automated supplier intelligence pipelines.

---

## CERTIFICATIONS & HONORS

- **Written Management Commendation for BD Excellence** — Pencil Mark Interior Solutions LLP (2025)
- **Google Digital Marketing Professional Certificate** — Google (2024)
- **Service Marketing: A Practical Approach** — NPTEL, IIT Kharagpur (2025)
- **Generative AI Mastermind** — Outskill (2025)
- **AI Tools & ChatGPT for Business Productivity** — be10x (2025)
"""

md_path = BASE_DIR / "ADITYA_MEHRA_UNIVERSAL_MASTER_CV.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Generated Markdown CV: {md_path}")

# 2. GENERATE STANDALONE EXECUTIVE HTML CV (Interactive & Print-Perfect)
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — Universal Master Executive CV</title>
<style>
  :root {
    --primary: #0f172a;       /* Deep Slate / Midnight Navy */
    --accent: #1e3a8a;        /* Royal Navy */
    --teal: #0d9488;          /* Strategic Teal */
    --text: #1e293b;          /* Charcoal Body */
    --muted: #475569;         /* Slate Secondary */
    --border: #cbd5e1;        /* Clean Divider */
    --bg-badge: #f1f5f9;      /* Subtle Tag Background */
    --bg-badge-text: #0f172a;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--text);
    background-color: #f8fafc;
    line-height: 1.45;
    font-size: 10.5pt;
    padding: 24px;
    -webkit-font-smoothing: antialiased;
  }

  .cv-container {
    max-width: 860px;
    margin: 0 auto;
    background: #ffffff;
    padding: 44px 52px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  }

  /* Header Section */
  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 16px;
    margin-bottom: 18px;
  }

  h1 {
    font-size: 26pt;
    font-weight: 800;
    letter-spacing: 1px;
    color: var(--primary);
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .subtitle {
    font-size: 11pt;
    font-weight: 600;
    color: var(--teal);
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    text-transform: uppercase;
  }

  .contact-bar {
    font-size: 9.5pt;
    color: var(--muted);
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 14px;
  }

  .contact-bar a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
  }

  .contact-bar a:hover {
    text-decoration: underline;
  }

  .contact-bar span {
    color: var(--muted);
  }

  /* Section Styling */
  section {
    margin-bottom: 18px;
  }

  h2 {
    font-size: 11.5pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 3px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .summary-text {
    font-size: 10pt;
    text-align: justify;
    color: var(--text);
    line-height: 1.5;
  }

  /* Competencies Grid */
  .competency-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 6px;
    font-size: 9.8pt;
  }

  .competency-item {
    line-height: 1.4;
  }

  .competency-title {
    font-weight: 700;
    color: var(--primary);
  }

  /* Experience Cards */
  .job-block {
    margin-bottom: 13px;
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }

  .job-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: var(--primary);
  }

  .job-date {
    font-size: 9pt;
    font-weight: 600;
    color: var(--teal);
    white-space: nowrap;
  }

  .job-company {
    font-size: 9.5pt;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 4px;
  }

  ul.job-bullets {
    list-style-type: disc;
    padding-left: 18px;
    font-size: 9.7pt;
    color: var(--text);
  }

  ul.job-bullets li {
    margin-bottom: 3.5px;
    line-height: 1.42;
    text-align: justify;
  }

  ul.job-bullets li strong {
    color: var(--primary);
  }

  /* Education & Creds */
  .edu-block {
    margin-bottom: 8px;
  }

  .cert-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 16px;
    font-size: 9.5pt;
  }

  .cert-item {
    display: flex;
    align-items: flex-start;
    gap: 6px;
  }

  .cert-bullet {
    color: var(--teal);
    font-weight: bold;
  }

  /* Action Buttons for Browser View */
  .action-bar {
    max-width: 860px;
    margin: 0 auto 16px auto;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }

  .btn {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 8px 18px;
    font-size: 9.5pt;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    transition: all 0.15s ease;
  }

  .btn:hover {
    background: var(--accent);
  }

  /* Print Optimization */
  @media print {
    body {
      background: #ffffff;
      padding: 0;
      font-size: 9.5pt;
    }
    .action-bar {
      display: none;
    }
    .cv-container {
      box-shadow: none;
      padding: 18px 24px;
      max-width: 100%;
    }
    h1 {
      font-size: 22pt;
    }
    .subtitle {
      font-size: 10pt;
    }
    h2 {
      font-size: 10.5pt;
      margin-bottom: 6px;
      padding-bottom: 2px;
    }
    .job-block {
      margin-bottom: 9px;
      page-break-inside: avoid;
    }
    ul.job-bullets li {
      margin-bottom: 2.5px;
    }
    @page {
      margin: 12mm 14mm;
      size: A4 portrait;
    }
  }
</style>
</head>
<body>

<div class="action-bar">
  <button class="btn" onclick="window.print()">🖨️ Print / Save to PDF</button>
</div>

<main class="cv-container">
  <header>
    <h1>Aditya Mehra</h1>
    <div class="subtitle">Business Operations &bull; Commercial Growth &bull; AI-Enabled Automation</div>
    <div class="contact-bar">
      <span>📍 Bengaluru, Karnataka, India</span>
      <span>📞 +91 7003456624</span>
      <span>✉️ <a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span>🔗 <a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span>💻 <a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Professional Summary</h2>
    <p class="summary-text">
      High-performing <strong>Business Operations & Commercial Growth Specialist</strong> with hands-on leadership delivering <strong>300+ live events and commercial activations</strong>, governing mission-critical operations at <strong>AERO India 2025</strong> (100k+ attendees, 0 shrinkage), and curating robotics AI data pipelines at <strong>Instawork</strong> with a verified <strong>99%+ QA benchmark</strong>. Combines an academic foundation in <strong>BBA International Business</strong> (Dayananda Sagar University, 2026) with proven execution across vendor SLA governance, 15–20% procurement cost reduction, B2B pipeline conversion, and modern AI process automation. Awarded a formal written management commendation for commercial excellence. Ready to deploy immediate operational rigor across top-tier MNCs, Global Capability Centers (GCCs), and high-growth technology enterprises.
    </p>
  </section>

  <section>
    <h2>Core Competencies</h2>
    <div class="competency-list">
      <div class="competency-item">
        <span class="competency-title">Operations & Vendor Governance:</span>
        End-to-End Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, Landed Cost Modeling, 15–20% Procurement Cost Optimization, High-Pressure Crisis Triage.
      </div>
      <div class="competency-item">
        <span class="competency-title">Commercial & B2B Growth:</span>
        Enterprise Client Engagement (Tata Communications, Puma India), Pipeline Management (15+ Concurrent Threads), Deal Qualification, Commercial Rate Structuring, Contract Negotiation.
      </div>
      <div class="competency-item">
        <span class="competency-title">AI & Process Automation:</span>
        Robotics Training Data Curation, Multi-Modal Annotation QA, Generative AI Prompt Engineering, Autonomous Workflow Design, Python & LLM Data Synthesis, Clay AI, Notion AI.
      </div>
      <div class="competency-item">
        <span class="competency-title">Global Trade & Supply Chain:</span>
        Incoterms 2020 (FOB, CIF, DDP), Letter of Credit (UCP 600) Principles, 3PL Freight Logistics, Inventory Buffer Management, Customs & EXIM Compliance Frameworks.
      </div>
      <div class="competency-item">
        <span class="competency-title">Analytics & Enterprise Tools:</span>
        Advanced MS Excel (XLOOKUP, Power Query, Dynamic Pivot Tables), Salesforce & Zoho CRM, SQL Querying Fundamentals, Unit Economics, Margin Modeling.
      </div>
      <div class="competency-item">
        <span class="competency-title">Multilingual Fluency:</span>
        English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).
      </div>
    </div>
  </section>

  <section>
    <h2>Professional Experience</h2>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Independent Event Director & Commercial Operations Lead</span>
        <span class="job-date">2019 – Present</span>
      </div>
      <div class="job-company">Independent Commercial Operations &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Scaled Multi-Format Operations:</strong> Directed end-to-end production and delivery for <strong>300+ commercial events</strong>, corporate launches, and experiential campaigns for premier brands including <strong>Tata Communications</strong>, <strong>Puma India</strong>, <strong>VH1 Supersonic</strong>, and <strong>Apollo Marketing</strong>.</li>
        <li><strong>Procurement Cost Optimization:</strong> Secured consistent <strong>15% to 20% cost savings</strong> per project by establishing direct supplier rate cards, eliminating contractor markups, and enforcing milestone-driven SLAs across 20+ vendors.</li>
        <li><strong>Client Retention & Account Growth:</strong> Maintained an exceptional <strong>30%+ repeat-client rate</strong> through transparent commercial accounting, rigorous quality standards, and high-velocity communication under compressed deadlines.</li>
        <li><strong>Crisis Leadership & Rapid Triage:</strong> Executed zero-downtime crisis management during unexpected operational disruptions (including weather-induced venue relocation and high-voltage technical transfers), safeguarding multi-lakh equipment and client SLA commitments.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">AI Data Operations Intern</span>
        <span class="job-date">Dec 2025</span>
      </div>
      <div class="job-company">Instawork Services India Pvt. Ltd. &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Robotics & Vision Data Collection:</strong> Supported machine learning pipelines training enterprise robotics and human activity recognition systems, managing high-density multi-modal data streams under strict capture protocols.</li>
        <li><strong>High-Fidelity QA Benchmark:</strong> Maintained a verified <strong>99%+ quality assurance benchmark</strong>, conducting rigorous schema validation, annotation audits, and edge-case classification to eliminate training distribution drift.</li>
        <li><strong>Cross-Functional Workflow Sync:</strong> Harmonized on-ground data collection procedures with ML engineering performance requirements, authoring standardized operational capture SOPs.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Business Development Intern</span>
        <span class="job-date">Jul 2025 – Aug 2025</span>
      </div>
      <div class="job-company">Pencil Mark Interior Solutions LLP &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Pipeline Expansion & Revenue Closing:</strong> Spearheaded B2B outbound acquisition across Bengaluru commercial interior and enterprise workspace projects, closing <strong>₹1.5L+ in initial contract revenue</strong>.</li>
        <li><strong>High-Velocity Deal Management:</strong> Managed <strong>15+ concurrent corporate prospect threads</strong>, optimizing follow-up turnaround times and achieving an <strong>18% lead-to-opportunity conversion rate</strong>.</li>
        <li><strong>Executive Commendation:</strong> Received an official <strong>written management commendation</strong> from executive leadership for exemplary lead pipeline expansion, structured sales drive, and commercial negotiation results.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Exhibition Operations & Commercial Lead</span>
        <span class="job-date">Feb 2025</span>
      </div>
      <div class="job-company">Salt in My Coca &bull; AERO India 2025 &bull; Yelahanka Air Force Station, Bengaluru</div>
      <ul class="job-bullets">
        <li><strong>Mission-Critical Expo Execution:</strong> Commanded 7 full days of on-ground exhibition stall operations, product display logistics, and high-density visitor flows at Asia's premier defense exposition (<strong>100,000+ attendees</strong>).</li>
        <li><strong>Strict Protocol & Security Governance:</strong> Managed inventory movements and contractor logistics under stringent Ministry of Defence clearance schedules and flight display windows, maintaining <strong>zero inventory shrinkage or asset loss</strong>.</li>
        <li><strong>High-Value Stakeholder Interaction:</strong> Engaged international military delegations, corporate CXOs, and institutional buyers, capturing qualified commercial leads and reinforcing brand positioning.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Event Operations Coordinator</span>
        <span class="job-date">Jan 2026</span>
      </div>
      <div class="job-company">TRILOGY: Indo-Jazz Instrumental Fusion &bull; Bangalore Club, Bengaluru</div>
      <ul class="job-bullets">
        <li><strong>End-to-End Production Coordination:</strong> Coordinated logistics for an elite instrumental live concert, overseeing international artist travel, hospitality, AV technical riders, and stage acoustic timelines.</li>
        <li><strong>Zero-Disruption Execution:</strong> Resolved live sound balance and schedule dependencies in real time, delivering a seamless performance experience for high-profile patrons.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Co-Founder & Operations Manager</span>
        <span class="job-date">2025</span>
      </div>
      <div class="job-company">Mehra's Kitchen &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Unit Economics & P&L Oversight:</strong> Designed operational and financial workflows for food-stall and cloud-kitchen operations, managing raw material procurement, vendor negotiation, and cash flow accounting.</li>
        <li><strong>Cost & Margin Control:</strong> Analyzed landed ingredient costs and optimized menu pricing structures to secure operational profitability.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Operations & Sales Associate</span>
        <span class="job-date">2018 – 2020</span>
      </div>
      <div class="job-company">Family Enterprise &bull; Kolkata & Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Commercial Foundation:</strong> Commenced commercial career at age 17 managing retail customer relations, inventory warehousing, order fulfillment, and cash reconciliation in a family trading business.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Education</h2>
    <div class="edu-block">
      <div class="job-header">
        <span class="job-title">Bachelor of Business Administration (BBA) — International Business</span>
        <span class="job-date">2023 – 2026</span>
      </div>
      <div class="job-company">Dayananda Sagar University &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Curriculum & Specialization:</strong> International Trade & EXIM Policies, Incoterms 2020, Global Supply Chain Logistics, Foreign Exchange Management, Financial Management, Managerial Economics, Business Statistics.</li>
        <li><strong>Applied Analytical Research:</strong> Landed cost variance modeling, cross-border freight risk mitigation, and automated supplier intelligence workflows.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Certifications & Honors</h2>
    <div class="cert-grid">
      <div class="cert-item">
        <span class="cert-bullet">✔</span>
        <div><strong>Written Performance Commendation</strong> — Pencil Mark Interior Solutions LLP (2025)</div>
      </div>
      <div class="cert-item">
        <span class="cert-bullet">✔</span>
        <div><strong>Google Digital Marketing Professional</strong> — Google (2024)</div>
      </div>
      <div class="cert-item">
        <span class="cert-bullet">✔</span>
        <div><strong>Service Marketing: A Practical Approach</strong> — NPTEL, IIT Kharagpur (2025)</div>
      </div>
      <div class="cert-item">
        <span class="cert-bullet">✔</span>
        <div><strong>Generative AI Mastermind</strong> — Outskill (2025)</div>
      </div>
      <div class="cert-item">
        <span class="cert-bullet">✔</span>
        <div><strong>AI Tools & ChatGPT for Business</strong> — be10x (2025)</div>
      </div>
    </div>
  </section>
</main>

</body>
</html>
"""

html_path = BASE_DIR / "ADITYA_MEHRA_UNIVERSAL_MASTER_CV.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated HTML CV: {html_path}")

# 3. GENERATE EXECUTIVE DOCX CV USING python-docx
doc = Document()

# Set professional margins (0.6 in)
for section in doc.sections:
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

# Styling palette
C_NAVY = RGBColor(15, 23, 42)      # #0F172A
C_ACCENT = RGBColor(30, 58, 138)   # #1E3A8A
C_TEAL = RGBColor(13, 148, 136)    # #0D9488
C_MUTED = RGBColor(71, 85, 105)    # #475569
C_BODY = RGBColor(30, 41, 59)      # #1E293B

def add_header(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("ADITYA MEHRA")
    run.font.name = "Calibri"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run("BUSINESS OPERATIONS  |  COMMERCIAL GROWTH  |  AI-ENABLED AUTOMATION")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = C_TEAL

    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(8)
    run_contact = p_contact.add_run("Bengaluru, Karnataka, India  |  +91 7003456624  |  adityamehra799@gmail.com\nLinkedIn: linkedin.com/in/aditya-mehra-b8644b326  |  GitHub: github.com/AdityaMehra007")
    run_contact.font.name = "Calibri"
    run_contact.font.size = Pt(9)
    run_contact.font.color.rgb = C_MUTED

def add_section_title(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title.upper())
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = C_NAVY
    
    # Add bottom border in XML
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), 'CBD5E1')
    pBdr.append(bottom)
    pPr.append(pBdr)

add_header(doc)

# SECTION: PROFESSIONAL SUMMARY
add_section_title(doc, "Professional Summary")
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(6)
p.paragraph_format.line_spacing = 1.15
r = p.add_run(
    "High-performing Business Operations & Commercial Growth Specialist with hands-on leadership delivering 300+ live events and commercial activations, "
    "governing mission-critical operations at AERO India 2025 (100k+ attendees, 0 shrinkage), and training robotics AI data pipelines at Instawork with a verified 99%+ QA benchmark. "
    "Combines an academic foundation in BBA International Business (Dayananda Sagar University, 2026) with proven execution across vendor SLA governance, 15–20% procurement cost reduction, "
    "B2B pipeline conversion, and modern AI process automation. Awarded a formal written management commendation for commercial excellence. "
    "Ready to deploy immediate operational rigor across top-tier MNCs, Global Capability Centers (GCCs), and high-growth technology enterprises."
)
r.font.name = "Calibri"
r.font.size = Pt(9.5)
r.font.color.rgb = C_BODY

# SECTION: CORE COMPETENCIES
add_section_title(doc, "Core Competencies")
competencies = [
    ("Operations & Vendor Governance: ", "End-to-End Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, Landed Cost Modeling, 15–20% Procurement Cost Optimization, High-Pressure Crisis Triage."),
    ("Commercial & B2B Growth: ", "Enterprise Client Engagement (Tata Communications, Puma India), Pipeline Management (15+ Concurrent Threads), Deal Qualification, Commercial Rate Structuring, Contract Negotiation."),
    ("AI & Process Automation: ", "Robotics Training Data Curation, Multi-Modal Annotation QA, Generative AI Prompt Engineering, Autonomous Workflow Design, Python & LLM Data Synthesis, Clay AI, Notion AI."),
    ("Global Trade & Supply Chain: ", "Incoterms 2020 (FOB, CIF, DDP), Letter of Credit (UCP 600) Principles, 3PL Freight Logistics, Inventory Buffer Management, Customs & EXIM Compliance Frameworks."),
    ("Analytics & Enterprise Tools: ", "Advanced MS Excel (XLOOKUP, Power Query, Dynamic Pivot Tables), Salesforce & Zoho CRM, SQL Querying Fundamentals, Unit Economics, Margin Modeling."),
    ("Multilingual Fluency: ", "English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).")
]
for title_prefix, details in competencies:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Calibri"
    r_bullet.font.size = Pt(9.5)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = C_TEAL

    r_bold = p.add_run(title_prefix)
    r_bold.font.name = "Calibri"
    r_bold.font.size = Pt(9.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = C_NAVY

    r_text = p.add_run(details)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = C_BODY

# SECTION: PROFESSIONAL EXPERIENCE
add_section_title(doc, "Professional Experience")

jobs = [
    {
        "role": "Independent Event Director & Commercial Operations Lead",
        "company": "Independent Commercial Operations | Bengaluru, India",
        "dates": "2019 – Present",
        "bullets": [
            ("Scaled Multi-Format Operations: ", "Directed end-to-end production and delivery for 300+ commercial events, corporate launches, and experiential campaigns for premier brands including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing."),
            ("Procurement Cost Optimization: ", "Secured consistent 15% to 20% cost savings per project by establishing direct supplier rate cards, eliminating contractor markups, and enforcing milestone-driven SLAs across 20+ vendors."),
            ("Client Retention & Account Growth: ", "Maintained an exceptional 30%+ repeat-client rate through transparent commercial accounting, rigorous quality standards, and high-velocity communication under compressed deadlines."),
            ("Crisis Leadership & Rapid Triage: ", "Executed zero-downtime crisis management during unexpected operational disruptions (including weather-induced venue relocation and high-voltage technical transfers), safeguarding multi-lakh equipment and client SLA commitments.")
        ]
    },
    {
        "role": "AI Data Operations Intern",
        "company": "Instawork Services India Pvt. Ltd. | Bengaluru, India",
        "dates": "Dec 2025",
        "bullets": [
            ("Robotics & Vision Data Collection: ", "Supported machine learning pipelines training enterprise robotics and human activity recognition systems, managing high-density multi-modal data streams under strict capture protocols."),
            ("High-Fidelity QA Benchmark: ", "Maintained a verified 99%+ quality assurance benchmark, conducting rigorous schema validation, annotation audits, and edge-case classification to eliminate training distribution drift."),
            ("Cross-Functional Workflow Sync: ", "Harmonized on-ground data collection procedures with ML engineering priorities, authoring standardized operational capture SOPs.")
        ]
    },
    {
        "role": "Business Development Intern",
        "company": "Pencil Mark Interior Solutions LLP | Bengaluru, India",
        "dates": "Jul 2025 – Aug 2025",
        "bullets": [
            ("Pipeline Expansion & Revenue Closing: ", "Spearheaded B2B outbound acquisition across Bengaluru commercial interior and enterprise workspace projects, closing ₹1.5L+ in initial contract revenue."),
            ("High-Velocity Deal Management: ", "Managed 15+ concurrent corporate prospect threads, optimizing follow-up turnaround times and achieving an 18% lead-to-opportunity conversion rate."),
            ("Executive Commendation: ", "Received an official written management commendation from executive leadership for exemplary lead pipeline expansion, structured sales drive, and commercial negotiation results.")
        ]
    },
    {
        "role": "Exhibition Operations & Commercial Lead",
        "company": "Salt in My Coca — AERO India 2025 | Yelahanka Air Force Station, Bengaluru",
        "dates": "Feb 2025",
        "bullets": [
            ("Mission-Critical Expo Execution: ", "Commanded 7 full days of on-ground exhibition stall operations, product display logistics, and high-density visitor flows at Asia's premier defense exposition (100,000+ attendees)."),
            ("Strict Protocol & Security Governance: ", "Managed inventory movements and contractor logistics under stringent Ministry of Defence clearance schedules and flight display windows, maintaining zero inventory shrinkage or asset loss."),
            ("High-Value Stakeholder Interaction: ", "Engaged international military delegations, corporate CXOs, and institutional buyers, capturing qualified commercial leads and reinforcing brand positioning.")
        ]
    },
    {
        "role": "Event Operations Coordinator",
        "company": "TRILOGY: Indo-Jazz Instrumental Fusion | Bangalore Club, Bengaluru",
        "dates": "Jan 2026",
        "bullets": [
            ("End-to-End Production Coordination: ", "Coordinated logistics for an elite instrumental live concert, overseeing international artist travel, hospitality, AV technical riders, and stage acoustic timelines."),
            ("Zero-Disruption Execution: ", "Resolved live sound balance and schedule dependencies in real time, delivering a seamless performance experience for high-profile patrons.")
        ]
    },
    {
        "role": "Co-Founder & Operations Manager",
        "company": "Mehra's Kitchen | Bengaluru, India",
        "dates": "2025",
        "bullets": [
            ("Unit Economics & P&L Oversight: ", "Designed operational and financial workflows for food-stall and cloud-kitchen operations, managing raw material procurement, vendor negotiation, and daily cash flow accounting."),
            ("Cost & Margin Control: ", "Analyzed landed ingredient costs and optimized menu pricing structures to secure operational profitability.")
        ]
    },
    {
        "role": "Operations & Sales Associate",
        "company": "Family Enterprise | Kolkata & Bengaluru, India",
        "dates": "2018 – 2020",
        "bullets": [
            ("Commercial Foundation: ", "Commenced commercial career at age 17 managing retail customer relations, inventory warehousing, order fulfillment, and cash reconciliation in a family trading business.")
        ]
    }
]

for job in jobs:
    p_head = doc.add_paragraph()
    p_head.paragraph_format.space_before = Pt(6)
    p_head.paragraph_format.space_after = Pt(1)
    p_head.paragraph_format.keep_with_next = True
    
    r_role = p_head.add_run(job["role"])
    r_role.font.name = "Calibri"
    r_role.font.size = Pt(10)
    r_role.font.bold = True
    r_role.font.color.rgb = C_NAVY

    r_dates = p_head.add_run(f"  |  {job['dates']}")
    r_dates.font.name = "Calibri"
    r_dates.font.size = Pt(9.5)
    r_dates.font.bold = True
    r_dates.font.color.rgb = C_TEAL

    p_comp = doc.add_paragraph()
    p_comp.paragraph_format.space_before = Pt(0)
    p_comp.paragraph_format.space_after = Pt(3)
    p_comp.paragraph_format.keep_with_next = True
    r_comp = p_comp.add_run(job["company"])
    r_comp.font.name = "Calibri"
    r_comp.font.size = Pt(9)
    r_comp.font.italic = True
    r_comp.font.color.rgb = C_ACCENT

    for b_prefix, b_text in job["bullets"]:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.left_indent = Inches(0.2)
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(2)
        p_b.paragraph_format.line_spacing = 1.15
        
        r_bullet = p_b.add_run("• ")
        r_bullet.font.name = "Calibri"
        r_bullet.font.size = Pt(9.5)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = C_TEAL

        r_bold = p_b.add_run(b_prefix)
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(9.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = C_NAVY

        r_text = p_b.add_run(b_text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = C_BODY

# SECTION: EDUCATION
add_section_title(doc, "Education")
p_edu = doc.add_paragraph()
p_edu.paragraph_format.space_before = Pt(4)
p_edu.paragraph_format.space_after = Pt(1)
p_edu.paragraph_format.keep_with_next = True
r_deg = p_edu.add_run("Bachelor of Business Administration (BBA) — International Business")
r_deg.font.name = "Calibri"
r_deg.font.size = Pt(10)
r_deg.font.bold = True
r_deg.font.color.rgb = C_NAVY
r_edates = p_edu.add_run("  |  2023 – 2026")
r_edates.font.name = "Calibri"
r_edates.font.size = Pt(9.5)
r_edates.font.bold = True
r_edates.font.color.rgb = C_TEAL

p_inst = doc.add_paragraph()
p_inst.paragraph_format.space_before = Pt(0)
p_inst.paragraph_format.space_after = Pt(3)
p_inst.paragraph_format.keep_with_next = True
r_inst = p_inst.add_run("Dayananda Sagar University | Bengaluru, India")
r_inst.font.name = "Calibri"
r_inst.font.size = Pt(9)
r_inst.font.italic = True
r_inst.font.color.rgb = C_ACCENT

p_edub1 = doc.add_paragraph()
p_edub1.paragraph_format.left_indent = Inches(0.2)
p_edub1.paragraph_format.space_before = Pt(1)
p_edub1.paragraph_format.space_after = Pt(2)
p_edub1.paragraph_format.line_spacing = 1.15
r_b = p_edub1.add_run("• ")
r_b.font.color.rgb = C_TEAL
r_b.font.bold = True
r_t = p_edub1.add_run("Curriculum & Specialization: International Trade & EXIM Policies, Incoterms 2020, Global Supply Chain Architecture, Foreign Exchange Management, Financial Management, Managerial Economics, Business Statistics.")
r_t.font.name = "Calibri"
r_t.font.size = Pt(9.5)
r_t.font.color.rgb = C_BODY

p_edub2 = doc.add_paragraph()
p_edub2.paragraph_format.left_indent = Inches(0.2)
p_edub2.paragraph_format.space_before = Pt(1)
p_edub2.paragraph_format.space_after = Pt(2)
p_edub2.paragraph_format.line_spacing = 1.15
r_b = p_edub2.add_run("• ")
r_b.font.color.rgb = C_TEAL
r_b.font.bold = True
r_t = p_edub2.add_run("Applied Analytical Projects: Landed cost variance modeling, cross-border freight risk mitigation, and automated supplier intelligence workflows.")
r_t.font.name = "Calibri"
r_t.font.size = Pt(9.5)
r_t.font.color.rgb = C_BODY

# SECTION: CERTIFICATIONS & HONORS
add_section_title(doc, "Certifications & Honors")
certs = [
    ("Written Performance Commendation for BD Excellence", "Pencil Mark Interior Solutions LLP (2025)"),
    ("Google Digital Marketing Professional Certificate", "Google (2024)"),
    ("Service Marketing: A Practical Approach", "NPTEL, IIT Kharagpur (2025)"),
    ("Generative AI Mastermind", "Outskill (2025)"),
    ("AI Tools & ChatGPT for Business Productivity", "be10x (2025)")
]
for cert_name, issuer in certs:
    p_c = doc.add_paragraph()
    p_c.paragraph_format.left_indent = Inches(0.2)
    p_c.paragraph_format.space_before = Pt(1)
    p_c.paragraph_format.space_after = Pt(2)
    p_c.paragraph_format.line_spacing = 1.15
    r_cb = p_c.add_run("✔ ")
    r_cb.font.color.rgb = C_TEAL
    r_cb.font.bold = True
    
    r_cn = p_c.add_run(f"{cert_name} ")
    r_cn.font.name = "Calibri"
    r_cn.font.size = Pt(9.5)
    r_cn.font.bold = True
    r_cn.font.color.rgb = C_NAVY

    r_iss = p_c.add_run(f"— {issuer}")
    r_iss.font.name = "Calibri"
    r_iss.font.size = Pt(9.5)
    r_iss.font.color.rgb = C_BODY

docx_path = BASE_DIR / "ADITYA_MEHRA_UNIVERSAL_MASTER_CV.docx"
doc.save(docx_path)
print(f"Generated DOCX CV: {docx_path}")

# 4. COMPILE TO EXECUTIVE PDF VIA HEADLESS EDGE / CHROME
pdf_path = BASE_DIR / "ADITYA_MEHRA_UNIVERSAL_MASTER_CV.pdf"
edge_cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    str(html_path)
]
try:
    res = subprocess.run(edge_cmd, capture_output=True, text=True, timeout=30)
    if res.returncode == 0 and pdf_path.exists():
        print(f"Successfully generated PDF: {pdf_path}")
    else:
        print(f"Edge print output: {res.stderr}")
except Exception as e:
    print(f"PDF generation error: {e}")
