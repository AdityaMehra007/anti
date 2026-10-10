from pathlib import Path
import pypdf

BASE_DIR = Path(r"e:\anti")

# Verify PDF page count
reader = pypdf.PdfReader(BASE_DIR / "ADITYA_MEHRA_NO_NUMBERS_1PAGE_CV.pdf")
print("PDF Page count:", len(reader.pages))

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — BBA Graduate Executive CV</title>
<style>
  :root {
    --primary: #0f172a;       /* Dark Navy */
    --teal: #0d9488;          /* Accent Teal */
    --slate: #334155;         /* Secondary Slate */
    --text: #1e293b;          /* Charcoal Body */
    --muted: #64748b;         /* Muted Metadata */
    --border: #cbd5e1;        /* Divider */
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: Calibri, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: var(--text);
    background-color: #f8fafc;
    line-height: 1.32;
    font-size: 8.5pt;
    padding: 16px;
    -webkit-font-smoothing: antialiased;
  }

  .cv-card {
    max-width: 820px;
    margin: 0 auto;
    background: #ffffff;
    padding: 24px 32px;
    border-radius: 6px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
  }

  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 6px;
    margin-bottom: 8px;
  }

  h1 {
    font-size: 19pt;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 1px;
  }

  .subtitle {
    font-size: 8.8pt;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.4px;
    margin-bottom: 3px;
    text-transform: uppercase;
  }

  .contact-bar {
    font-size: 8pt;
    color: var(--muted);
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .contact-bar a {
    color: var(--slate);
    text-decoration: none;
    font-weight: 600;
  }

  .contact-bar a:hover { text-decoration: underline; }

  section { margin-bottom: 7px; }

  h2 {
    font-size: 9pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1px;
    margin-bottom: 4px;
  }

  .summary-p {
    font-size: 8pt;
    text-align: justify;
    line-height: 1.32;
    color: var(--text);
  }

  .skills-list {
    font-size: 7.8pt;
    line-height: 1.3;
  }

  .skills-list p {
    margin-bottom: 1.5px;
  }

  .job-row { margin-bottom: 4.5px; }
  .job-title-bar {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 8.2pt;
  }
  .job-title { font-weight: 700; color: var(--primary); }
  .job-company { font-style: italic; color: var(--slate); font-weight: 600; font-size: 7.8pt; }
  .job-date { font-weight: 700; color: var(--teal); font-size: 7.6pt; }

  ul.bullets {
    list-style-type: disc;
    padding-left: 14px;
    font-size: 7.7pt;
    margin-top: 1px;
  }

  ul.bullets li {
    margin-bottom: 1px;
    line-height: 1.28;
    text-align: justify;
  }

  ul.bullets li strong { color: var(--primary); }

  .edu-row {
    font-size: 7.8pt;
    line-height: 1.3;
  }

  .cert-row {
    font-size: 7.6pt;
    color: var(--text);
    margin-top: 2px;
    line-height: 1.28;
  }

  .action-bar {
    max-width: 820px;
    margin: 0 auto 10px auto;
    display: flex;
    justify-content: flex-end;
    gap: 8px;
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
    body { background: #ffffff; padding: 0; font-size: 7.8pt; }
    .action-bar { display: none; }
    .cv-card { box-shadow: none; padding: 6mm 8mm; max-width: 100%; }
    .job-row { page-break-inside: avoid; }
    @page { margin: 6mm 8mm; size: A4 portrait; }
  }
</style>
</head>
<body>

<div class="action-bar">
  <button class="btn" onclick="window.print()">Print / Save to PDF</button>
</div>

<main class="cv-card">
  <header>
    <h1>Aditya Mehra</h1>
    <div class="subtitle">BBA Graduate (International Business) &bull; Operations, Growth & AI Automation</div>
    <div class="contact-bar">
      <span>Bengaluru, Karnataka, India</span>
      <span>+91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Profile & Career Objective</h2>
    <p class="summary-p">
      Execution-driven BBA graduate in International Business from Dayananda Sagar University seeking an entry-level role in Business Operations, Business Development, or General Management. Brings practical experience directing large-scale commercial events and brand activations, managing high-profile exhibition operations at AERO India, and supporting robotics AI data operations at Instawork. Proven background in corporate B2B client outreach, vendor negotiations, procurement cost optimization, and modern AI workflow automation. Commended in writing by management for sales excellence and proactive execution.
    </p>
  </section>

  <section>
    <h2>Core Competencies & Technical Skills</h2>
    <div class="skills-list">
      <p><strong>Business & Operations:</strong> Commercial Event Operations, Direct Supplier SLA Governance, Vendor Negotiation, Procurement Cost Optimization, On-Ground Crisis Triage.</p>
      <p><strong>Commercial & B2B Growth:</strong> Outbound B2B Outreach, Client Relationship Management, Multi-Thread Communication, Deal Qualification, Commercial Contract Closing.</p>
      <p><strong>AI & Workflow Automation:</strong> Robotics Data Curation, Multi-Modal Annotation QA, Generative AI Prompting, Autonomous Workflow Design, Python Data Processing.</p>
      <p><strong>Analytics, Trade & Systems:</strong> Advanced MS Excel (XLOOKUP, Power Query, Pivot Tables), Incoterms Frameworks, Supply Chain Coordination, CRM (Salesforce, Zoho).</p>
      <p><strong>Languages:</strong> English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).</p>
    </div>
  </section>

  <section>
    <h2>Work Experience & Practical Projects</h2>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Independent Event Director & Commercial Operations Lead</strong> | <span class="job-company">Commercial Event Operations, Bengaluru</span></span>
        <span class="job-date">Ongoing</span>
      </div>
      <ul class="bullets">
        <li><strong>Scaled Event Delivery:</strong> Managed on-ground production, stage management, and logistics for major corporate events and brand activations for marquee clients including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing.</li>
        <li><strong>Vendor Governance & Cost Control:</strong> Delivered substantial procurement cost savings through direct supplier contracting and milestone-based vendor agreements; maintained strong repeat-client relationships.</li>
        <li><strong>Live Showcase Management:</strong> Directed full event logistics, artist transit, and technical riders for the TRILOGY Indo-Jazz Fusion live concert at Bangalore Club with seamless execution and zero live delays.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions LLP, Bengaluru</span></span>
        <span class="job-date">Completed</span>
      </div>
      <ul class="bullets">
        <li><strong>B2B Pipeline & Revenue:</strong> Drove corporate B2B lead generation across commercial workspace interior projects, managing multiple concurrent client threads from initial pitch to proposal submission.</li>
        <li><strong>Deal Closing & Executive Commendation:</strong> Assisted executive leadership in client presentations and contract discussions to close commercial interior contracts; awarded a formal written management commendation for sales drive and proactive pipeline expansion.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">AI Data Operations Intern</strong> | <span class="job-company">Instawork Services India Pvt. Ltd., Bengaluru</span></span>
        <span class="job-date">Completed</span>
      </div>
      <ul class="bullets">
        <li><strong>Robotics & Vision Datasets:</strong> Curated and validated high-density multi-modal datasets supporting machine learning models for enterprise robotics and human activity recognition.</li>
        <li><strong>Quality Assurance Standards:</strong> Maintained high-accuracy quality assurance standards across all data streams, authoring standardized capture guidelines for operational teams.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Exhibition Operations & Commercial Lead</strong> | <span class="job-company">Salt in My Coca — AERO India, Yelahanka AFB</span></span>
        <span class="job-date">Completed</span>
      </div>
      <ul class="bullets">
        <li><strong>High-Density Expo Logistics:</strong> Led on-ground stall operations, visitor engagement, and inventory logistics at Asia's premier defense exposition, achieving complete asset protection and zero inventory loss under strict military security protocols.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations, Unit Economics & Retail Lead</strong> | <span class="job-company">Mehra's Kitchen & Family Commercial Enterprise, BLR/CCU</span></span>
        <span class="job-date">Experienced</span>
      </div>
      <ul class="bullets">
        <li><strong>Ground Operations Mastery:</strong> Managed raw material procurement, unit cost economics, menu pricing, inventory turnover, supplier negotiations, and daily cash reconciliation across retail and food operations.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Project: Automated Market Intelligence Engine</strong> | <span class="job-company">Independent Workflow System, Bengaluru</span></span>
        <span class="job-date">Current</span>
      </div>
      <ul class="bullets">
        <li><strong>Data & Automation Architecture:</strong> Engineered automated data extraction and enrichment workflows analyzing commercial corporate entities and professional networks using Python, LLM structured processing, and Power Query.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Education & Certifications</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong><br>
      <em>Dayananda Sagar University, Bengaluru</em> — Focus: International Trade Policies, Incoterms Frameworks, Global Supply Chain, Business Statistics.
    </div>
    <div class="cert-row">
      <strong>Certifications & Honors:</strong> Written Management Commendation (Pencil Mark) &bull; Google Digital Marketing Professional Certificate &bull; Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur) &bull; Generative AI Mastermind (Outskill) &bull; AI Tools & ChatGPT for Business (be10x)
    </div>
  </section>
</main>

</body>
</html>
"""

md_content = """# ADITYA MEHRA
**Bengaluru, Karnataka, India** | **+91 7003456624** | **adityamehra799@gmail.com**  
**LinkedIn:** [linkedin.com/in/aditya-mehra-b8644b326](https://linkedin.com/in/aditya-mehra-b8644b326) | **Portfolio & Code:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## PROFILE & CAREER OBJECTIVE
Execution-driven BBA graduate in International Business from Dayananda Sagar University seeking an entry-level role in Business Operations, Business Development, or General Management. Brings practical experience directing large-scale commercial events and brand activations, managing high-profile exhibition operations at AERO India, and supporting robotics AI data operations at Instawork. Proven background in corporate B2B client outreach, vendor negotiations, procurement cost optimization, and modern AI workflow automation. Commended in writing by management for sales excellence and proactive execution.

---

## CORE COMPETENCIES & TECHNICAL SKILLS
- **Business & Operations:** Commercial Event Operations, Direct Supplier SLA Governance, Vendor Negotiation, Procurement Cost Optimization, On-Ground Crisis Triage.
- **Commercial & B2B Growth:** Outbound B2B Outreach, Client Relationship Management, Multi-Thread Communication, Deal Qualification, Commercial Contract Closing.
- **AI & Workflow Automation:** Robotics Data Curation, Multi-Modal Annotation QA, Generative AI Prompting, Autonomous Workflow Design, Python Data Processing.
- **Analytics, Trade & Systems:** Advanced MS Excel (XLOOKUP, Power Query, Pivot Tables), Incoterms Frameworks, Supply Chain Coordination, CRM (Salesforce, Zoho).
- **Languages:** English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).

---

## WORK EXPERIENCE & PRACTICAL PROJECTS

### Independent Event Director & Commercial Operations Lead | Commercial Event Operations, Bengaluru (Ongoing)
- **Scaled Event Delivery:** Managed on-ground production, stage management, and logistics for major corporate events and brand activations for marquee clients including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing.
- **Vendor Governance & Cost Control:** Delivered substantial procurement cost savings through direct supplier contracting and milestone-based vendor agreements; maintained strong repeat-client relationships.
- **Live Showcase Management:** Directed full event logistics, artist transit, and technical riders for the TRILOGY Indo-Jazz Fusion live concert at Bangalore Club with seamless execution and zero live delays.

### Business Development Intern | Pencil Mark Interior Solutions LLP, Bengaluru (Completed)
- **B2B Pipeline & Revenue:** Drove corporate B2B lead generation across commercial workspace interior projects, managing multiple concurrent client threads from initial pitch to proposal submission.
- **Deal Closing & Executive Commendation:** Assisted executive leadership in client presentations and contract discussions to close commercial interior contracts; awarded a formal written management commendation for sales drive and proactive pipeline expansion.

### AI Data Operations Intern | Instawork Services India Pvt. Ltd., Bengaluru (Completed)
- **Robotics & Vision Datasets:** Curated and validated high-density multi-modal datasets supporting machine learning models for enterprise robotics and human activity recognition.
- **Quality Assurance Standards:** Maintained high-accuracy quality assurance standards across all data streams, authoring standardized capture guidelines for operational teams.

### Exhibition Operations & Commercial Lead | Salt in My Coca — AERO India, Yelahanka AFB (Completed)
- **High-Density Expo Logistics:** Led on-ground stall operations, visitor engagement, and inventory logistics at Asia's premier defense exposition, achieving complete asset protection and zero inventory loss under strict military security protocols.

### Operations, Unit Economics & Retail Lead | Mehra's Kitchen & Family Commercial Enterprise, BLR/CCU (Experienced)
- **Ground Operations Mastery:** Managed raw material procurement, unit cost economics, menu pricing, inventory turnover, supplier negotiations, and daily cash reconciliation across retail and food operations.

### Project: Automated Market Intelligence Engine | Independent Workflow System, Bengaluru (Current)
- **Data & Automation Architecture:** Engineered automated data extraction and enrichment workflows analyzing commercial corporate entities and professional networks using Python, LLM structured processing, and Power Query.

---

## EDUCATION & CERTIFICATIONS
**Bachelor of Business Administration (BBA) — International Business**  
*Dayananda Sagar University, Bengaluru* — Focus: International Trade Policies, Incoterms Frameworks, Global Supply Chain, Business Statistics.  
**Certifications & Honors:** Written Management Commendation (Pencil Mark) • Google Digital Marketing Professional Certificate • Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur) • Generative AI Mastermind (Outskill) • AI Tools & ChatGPT for Business (be10x)
"""

with open(BASE_DIR / "ADITYA_MEHRA_NO_NUMBERS_1PAGE_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_NO_NUMBERS_1PAGE_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Generated HTML and Markdown for No-Numbers CV.")
