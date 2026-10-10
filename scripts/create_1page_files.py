from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_1page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — High-Impact Executive CV (1-Page)</title>
<style>
  :root {
    --primary: #0f172a;
    --accent: #1e3a8a;
    --teal: #0d9488;
    --text: #1e293b;
    --muted: #475569;
    --border: #cbd5e1;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: Calibri, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: var(--text);
    background-color: #f8fafc;
    line-height: 1.35;
    font-size: 9pt;
    padding: 20px;
    -webkit-font-smoothing: antialiased;
  }

  .cv-container {
    max-width: 800px;
    margin: 0 auto;
    background: #ffffff;
    padding: 32px 40px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  }

  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 10px;
    margin-bottom: 10px;
  }

  h1 {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: var(--primary);
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .subtitle {
    font-size: 9.5pt;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  .contact-bar {
    font-size: 8.5pt;
    color: var(--muted);
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
  }

  .contact-bar a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
  }

  section { margin-bottom: 10px; }

  h2 {
    font-size: 9.8pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 2px;
    margin-bottom: 6px;
  }

  .summary-text {
    font-size: 8.5pt;
    text-align: justify;
    color: var(--text);
    line-height: 1.4;
  }

  .competency-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 3px;
    font-size: 8.5pt;
  }

  .competency-title { font-weight: 700; color: var(--primary); }

  .job-block { margin-bottom: 8px; }
  .job-header { display: flex; justify-content: space-between; align-items: baseline; }
  .job-title { font-size: 9.2pt; font-weight: 700; color: var(--primary); }
  .job-date { font-size: 8.5pt; font-weight: 700; color: var(--teal); }
  .job-company { font-size: 8.5pt; font-style: italic; color: var(--accent); margin-bottom: 2px; }

  ul.job-bullets { list-style-type: disc; padding-left: 16px; font-size: 8.5pt; color: var(--text); }
  ul.job-bullets li { margin-bottom: 2px; line-height: 1.35; text-align: justify; }
  ul.job-bullets li strong { color: var(--primary); }

  .edu-box {
    font-size: 8.5pt;
    line-height: 1.35;
  }

  .action-bar {
    max-width: 800px;
    margin: 0 auto 12px auto;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }

  .btn {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 6px 14px;
    font-size: 8.5pt;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
  }

  @media print {
    body { background: #ffffff; padding: 0; font-size: 8.5pt; }
    .action-bar { display: none; }
    .cv-container { box-shadow: none; padding: 8mm 10mm; max-width: 100%; }
    .job-block { page-break-inside: avoid; }
    @page { margin: 8mm 10mm; size: A4 portrait; }
  }
</style>
</head>
<body>

<div class="action-bar">
  <button class="btn" onclick="window.print()">Print / Save PDF</button>
</div>

<main class="cv-container">
  <header>
    <h1>Aditya Mehra</h1>
    <div class="subtitle">Business Operations &bull; Commercial Growth &bull; AI Automation</div>
    <div class="contact-bar">
      <span>Bengaluru, India</span>
      <span>+91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Professional Summary</h2>
    <p class="summary-text">
      Results-driven <strong>Business Operations & Commercial Growth Specialist</strong> with extensive hands-on experience directing <strong>300+ commercial activations</strong>, governing high-stakes operations at <strong>AERO India 2025</strong> (100k+ attendees, 0 shrinkage), and training robotics AI data pipelines at <strong>Instawork</strong> (99%+ QA benchmark). Combines BBA International Business credentials (DSU '26) with proven execution across vendor SLA governance, 15–20% procurement cost reduction, B2B pipeline acquisition, and modern AI automation. Commended in writing for outstanding commercial drive.
    </p>
  </section>

  <section>
    <h2>Core Competencies</h2>
    <div class="competency-list">
      <div><span class="competency-title">Operations & Cost Control:</span> Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, 15–20% Landed Cost Reduction, Crisis Triage.</div>
      <div><span class="competency-title">Commercial & B2B Growth:</span> Corporate Client Outreach (Tata Communications, Puma India), Pipeline Management (15+ Threads), High-Ticket Deal Negotiation.</div>
      <div><span class="competency-title">AI & Trade Systems:</span> Robotics Data Curation (99%+ QA), GenAI Workflows, Incoterms 2020, Advanced Excel (XLOOKUP, Power Query), CRM (Salesforce/Zoho).</div>
    </div>
  </section>

  <section>
    <h2>Key Professional Experience</h2>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Independent Event Director & Commercial Operations Lead</span>
        <span class="job-date">2019 – Present</span>
      </div>
      <div class="job-company">Independent Commercial Operations &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Scaled Commercial Execution:</strong> Directed end-to-end production for <strong>300+ commercial events</strong> and brand activations for marquee clients including <strong>Tata Communications</strong>, <strong>Puma India</strong>, <strong>VH1 Supersonic</strong>, and <strong>Apollo Marketing</strong>.</li>
        <li><strong>Procurement & Cost Savings:</strong> Delivered consistent <strong>15% to 20% cost savings</strong> per engagement by eliminating intermediary contractor markups, establishing direct supplier rate cards, and enforcing strict vendor SLAs.</li>
        <li><strong>Client Retention & Resilience:</strong> Maintained a <strong>30%+ repeat-client rate</strong> and 100% on-time execution through rapid crisis triage (venue re-allocations and technical transfers under zero client SLA breach).</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">AI Data Operations Intern</span>
        <span class="job-date">Dec 2025</span>
      </div>
      <div class="job-company">Instawork Services India Pvt. Ltd. &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Robotics & Vision Datasets:</strong> Supported ML training pipelines for enterprise robotics and human activity recognition, curating multi-modal sensor and video data streams.</li>
        <li><strong>Quality Assurance Benchmark:</strong> Maintained a verified <strong>99%+ quality assurance benchmark</strong>, performing granular schema validation and edge-case classification to eliminate training drift.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Business Development Intern</span>
        <span class="job-date">Jul 2025 – Aug 2025</span>
      </div>
      <div class="job-company">Pencil Mark Interior Solutions LLP &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Revenue & Pipeline Drive:</strong> Accelerated B2B client acquisition across Bengaluru commercial interior projects, managing 15+ concurrent prospect threads and closing <strong>₹1.5L+ in initial contract revenue</strong> (18% conversion rate).</li>
        <li><strong>Executive Commendation:</strong> Awarded a formal <strong>written management commendation</strong> for exemplary lead pipeline expansion, proactive client negotiation, and sales drive.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Exhibition Operations & Commercial Lead</span>
        <span class="job-date">Feb 2025</span>
      </div>
      <div class="job-company">Salt in My Coca — AERO India 2025 &bull; Yelahanka Air Force Station, Bengaluru</div>
      <ul class="job-bullets">
        <li><strong>High-Density Expo Logistics:</strong> Commanded 7 full days of on-ground stall operations, contractor logistics, and visitor flows at Asia's premier defense expo (<strong>100,000+ attendees</strong>) with <strong>zero inventory shrinkage or asset loss</strong> under strict military clearances.</li>
        <li><strong>Stakeholder Lead Capture:</strong> Interfaced with international military delegations, corporate CXOs, and institutional buyers, qualifying high-value commercial leads.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Education & Credentials</h2>
    <div class="edu-box">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong> | 2023 – 2026<br>
      <em>Dayananda Sagar University, Bengaluru</em> — Focus: International Trade & EXIM Policies, Incoterms 2020, Supply Chain Architecture, Business Statistics.<br>
      <span style="color: var(--muted); font-size: 8.2pt;"><strong>Certifications:</strong> Written Commendation (Pencil Mark, 2025) &bull; Google Digital Marketing (2024) &bull; Service Marketing (IIT Kharagpur NPTEL, 2025) &bull; GenAI Mastermind (Outskill, 2025)</span>
    </div>
  </section>
</main>

</body>
</html>
"""

md_1page = """# ADITYA MEHRA
**Bengaluru, India** | **+91 7003456624** | **adityamehra799@gmail.com**  
**LinkedIn:** [linkedin.com/in/aditya-mehra-b8644b326](https://linkedin.com/in/aditya-mehra-b8644b326) | **Portfolio & Code:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## PROFESSIONAL SUMMARY
Results-driven **Business Operations & Commercial Growth Specialist** with extensive hands-on experience directing **300+ commercial activations**, governing high-stakes operations at **AERO India 2025** (100k+ attendees, 0 shrinkage), and training robotics AI data pipelines at **Instawork** (99%+ QA benchmark). Combines BBA International Business credentials (DSU '26) with proven execution across vendor SLA governance, 15–20% procurement cost reduction, B2B pipeline acquisition, and modern AI automation. Commended in writing for outstanding commercial drive.

---

## CORE COMPETENCIES
- **Operations & Cost Control:** Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, 15–20% Landed Cost Reduction, Crisis Triage.
- **Commercial & B2B Growth:** Corporate Client Outreach (Tata Communications, Puma India), Pipeline Management (15+ Threads), High-Ticket Deal Negotiation.
- **AI & Trade Systems:** Robotics Data Curation (99%+ QA), GenAI Workflows, Incoterms 2020, Advanced Excel (XLOOKUP, Power Query), CRM (Salesforce/Zoho).

---

## KEY PROFESSIONAL EXPERIENCE

### INDEPENDENT EVENT DIRECTOR & COMMERCIAL OPERATIONS LEAD
**Independent Commercial Operations** | *Bengaluru, India* | **2019 – Present**
- **Scaled Commercial Execution:** Directed end-to-end production for **300+ commercial events** and brand activations for marquee clients including **Tata Communications**, **Puma India**, **VH1 Supersonic**, and **Apollo Marketing**.
- **Procurement & Cost Savings:** Delivered consistent **15% to 20% cost savings** per engagement by eliminating intermediary contractor markups, establishing direct supplier rate cards, and enforcing strict vendor SLAs.
- **Client Retention & Resilience:** Maintained a **30%+ repeat-client rate** and 100% on-time execution through rapid crisis triage (venue re-allocations and technical transfers under zero client SLA breach).

### AI DATA OPERATIONS INTERN
**Instawork Services India Pvt. Ltd.** | *Bengaluru, India* | **Dec 2025**
- **Robotics & Vision Datasets:** Supported ML training pipelines for enterprise robotics and human activity recognition, curating multi-modal sensor and video data streams.
- **Quality Assurance Benchmark:** Maintained a verified **99%+ quality assurance benchmark**, performing granular schema validation and edge-case classification to eliminate training drift.

### BUSINESS DEVELOPMENT INTERN
**Pencil Mark Interior Solutions LLP** | *Bengaluru, India* | **Jul 2025 – Aug 2025**
- **Revenue & Pipeline Drive:** Accelerated B2B client acquisition across Bengaluru commercial interior projects, managing 15+ concurrent prospect threads and closing **₹1.5L+ in initial contract revenue** (18% conversion rate).
- **Executive Commendation:** Awarded a formal **written management commendation** for exemplary lead pipeline expansion, proactive client negotiation, and sales drive.

### EXHIBITION OPERATIONS & COMMERCIAL LEAD
**Salt in My Coca — AERO India 2025** | *Yelahanka Air Force Station, Bengaluru* | **Feb 2025**
- **High-Density Expo Logistics:** Commanded 7 full days of on-ground stall operations, contractor logistics, and visitor flows at Asia's premier defense expo (**100,000+ attendees**) with **zero inventory shrinkage or asset loss** under strict military clearances.
- **Stakeholder Lead Capture:** Interfaced with international military delegations, corporate CXOs, and institutional buyers, qualifying high-value commercial leads.

---

## EDUCATION & CREDENTIALS
**Bachelor of Business Administration (BBA) — International Business** | **2023 – 2026**  
Dayananda Sagar University, Bengaluru — Focus: International Trade & EXIM Policies, Incoterms 2020, Supply Chain Architecture, Business Statistics.  
**Certifications:** Written Commendation (Pencil Mark, 2025) • Google Digital Marketing (2024) • Service Marketing (IIT Kharagpur NPTEL, 2025) • GenAI Mastermind (Outskill, 2025)
"""

with open(BASE_DIR / "ADITYA_MEHRA_EXECUTIVE_1PAGE_CV.html", "w", encoding="utf-8") as f:
    f.write(html_1page)

with open(BASE_DIR / "ADITYA_MEHRA_EXECUTIVE_1PAGE_CV.md", "w", encoding="utf-8") as f:
    f.write(md_1page)

print("Generated 1-Page HTML and Markdown CVs.")
