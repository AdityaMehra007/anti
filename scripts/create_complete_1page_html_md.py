from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — Complete 1-Page Executive CV</title>
<style>
  :root {
    --primary: #0f172a;       /* Dark Navy */
    --teal: #0d9488;          /* Modern Teal */
    --slate: #334155;         /* Slate Secondary */
    --text: #1e293b;          /* Charcoal Body */
    --muted: #64748b;         /* Muted Metadata */
    --border: #cbd5e1;        /* Subtle Border */
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
      Execution-focused BBA International Business graduate (Dayananda Sagar University '26) combining hands-on leadership across 300+ commercial events/activations, mission-critical operations at AERO India 2025 (100k+ attendees, 0 shrinkage), and AI data operations at Instawork (99%+ QA benchmark). Experienced in B2B client acquisition (₹1.5L+ closed, written commendation), vendor SLA negotiations (15–20% cost savings), and building Python/AI-driven business automation workflows. Seeking entry-level roles in Business Operations, Growth/BD, or General Management.
    </p>
  </section>

  <section>
    <h2>Core Competencies & Technical Skills</h2>
    <div class="skills-list">
      <p><strong>Business & Operations:</strong> Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, Vendor Negotiation, 15–20% Cost Reduction, Crisis Triage.</p>
      <p><strong>Commercial & B2B Growth:</strong> B2B Outbound Outreach, Client Relationship Servicing (15+ Threads), Pitch Decks, Contract Closing, Lead Qualification.</p>
      <p><strong>AI, Automation & Tech:</strong> Python Data Workflows, LLM Prompt Engineering, AI Dataset Curation & QA (Instawork 99%+), Clay AI, Notion AI, Automation DAGs.</p>
      <p><strong>Analytics, Trade & Systems:</strong> Advanced MS Excel (XLOOKUP, Power Query, Pivot Tables), Incoterms 2020, Supply Chain Logistics, CRM (Salesforce, Zoho).</p>
      <p><strong>Languages:</strong> English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).</p>
    </div>
  </section>

  <section>
    <h2>Work Experience & Practical Projects</h2>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Independent Event Director & Commercial Operations Lead</strong> | <span class="job-company">Commercial Event Operations, Bengaluru</span></span>
        <span class="job-date">2019 – Present</span>
      </div>
      <ul class="bullets">
        <li><strong>Scaled Event Delivery:</strong> Managed on-ground production and logistics for 300+ corporate events and brand activations for marquee clients including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing.</li>
        <li><strong>Vendor Governance & Cost Savings:</strong> Achieved consistent 15% to 20% cost savings per project through direct supplier contracting and milestone-based SLA enforcement; maintained a 30%+ repeat-client rate.</li>
        <li><strong>Live Showcase Management:</strong> Directed full event logistics, artist travel, and technical riders for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero live performance disruption.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions LLP, Bengaluru</span></span>
        <span class="job-date">Jul 2025 – Aug 2025</span>
      </div>
      <ul class="bullets">
        <li><strong>B2B Pipeline & Revenue:</strong> Drove outbound corporate lead generation across commercial workspace projects, managing 15+ concurrent client threads and helping close ₹1.5L+ in commercial interior contracts (18% conversion rate).</li>
        <li><strong>Executive Commendation:</strong> Awarded a formal written management commendation by leadership for exceptional sales drive, client negotiation, and active pipeline expansion.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">AI Data Operations Intern</strong> | <span class="job-company">Instawork Services India Pvt. Ltd., Bengaluru</span></span>
        <span class="job-date">Dec 2025</span>
      </div>
      <ul class="bullets">
        <li><strong>Robotics & Vision Datasets:</strong> Curated and annotated high-density multi-modal datasets training enterprise robotics and human activity recognition machine learning models.</li>
        <li><strong>99%+ QA Benchmark:</strong> Maintained a verified 99%+ quality assurance accuracy rating across all data streams, authoring standardized capture SOPs.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Exhibition Operations & Commercial Lead</strong> | <span class="job-company">Salt in My Coca — AERO India 2025, Yelahanka AFB</span></span>
        <span class="job-date">Feb 2025</span>
      </div>
      <ul class="bullets">
        <li><strong>High-Density Expo Logistics:</strong> Led 7-day stall operations, visitor engagement, and inventory logistics at Asia's premier defense expo (100k+ attendees), achieving zero inventory shrinkage under strict military security protocols.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations, Unit Economics & Retail Lead</strong> | <span class="job-company">Mehra's Kitchen & Family Commercial Enterprise, BLR/CCU</span></span>
        <span class="job-date">2018 – 2025</span>
      </div>
      <ul class="bullets">
        <li><strong>Ground Operations Mastery:</strong> Managed raw material procurement, unit cost economics, menu pricing, inventory turnover, supplier negotiations, and daily cash reconciliation across retail and food operations.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Project: Automated Market Intelligence & Pipeline Engine</strong> | <span class="job-company">Independent System, Bengaluru</span></span>
        <span class="job-date">2025 – 2026</span>
      </div>
      <ul class="bullets">
        <li><strong>Data & Automation Architecture:</strong> Engineered automated data extraction and enrichment pipelines analyzing 4,500+ commercial entities and 9,200+ network records using Python, LLM structured outputs, and Power Query.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Education & Certifications</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong> | 2023 – 2026<br>
      <em>Dayananda Sagar University, Bengaluru</em> — Focus: International Trade & EXIM Policies, Incoterms 2020, Supply Chain, Business Statistics.
    </div>
    <div class="cert-row">
      <strong>Certifications & Honors:</strong> Written Management Commendation (Pencil Mark, 2025) &bull; Google Digital Marketing Professional (2024) &bull; Service Marketing (NPTEL, IIT Kharagpur, 2025) &bull; Generative AI Mastermind (Outskill, 2025) &bull; AI Tools & ChatGPT (be10x, 2025)
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
Execution-focused BBA International Business graduate (Dayananda Sagar University '26) combining hands-on leadership across 300+ commercial events/activations, mission-critical operations at AERO India 2025 (100k+ attendees, 0 shrinkage), and AI data operations at Instawork (99%+ QA benchmark). Experienced in B2B client acquisition (₹1.5L+ closed, written commendation), vendor SLA negotiations (15–20% cost savings), and building Python/AI-driven business automation workflows. Seeking entry-level roles in Business Operations, Growth/BD, or General Management.

---

## CORE COMPETENCIES & TECHNICAL SKILLS
- **Business & Operations:** Live Operations Delivery (300+ Events), Direct Supplier SLA Governance, Vendor Negotiation, 15–20% Cost Reduction, Crisis Triage.
- **Commercial & B2B Growth:** B2B Outbound Outreach, Client Relationship Servicing (15+ Threads), Pitch Decks, Contract Closing, Lead Qualification.
- **AI, Automation & Tech:** Python Data Workflows, LLM Prompt Engineering, AI Dataset Curation & QA (Instawork 99%+), Clay AI, Notion AI, Automation DAGs.
- **Analytics, Trade & Systems:** Advanced MS Excel (XLOOKUP, Power Query, Pivot Tables), Incoterms 2020, Supply Chain Logistics, CRM (Salesforce, Zoho).
- **Languages:** English (Fluent / Professional), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Conversational).

---

## WORK EXPERIENCE & PRACTICAL PROJECTS

### Independent Event Director & Commercial Operations Lead | Commercial Event Operations, Bengaluru
*2019 – Present*
- **Scaled Event Delivery:** Managed on-ground production and logistics for 300+ corporate events and brand activations for marquee clients including Tata Communications, Puma India, VH1 Supersonic, and Apollo Marketing.
- **Vendor Governance & Cost Savings:** Achieved consistent 15% to 20% cost savings per project through direct supplier contracting and milestone-based SLA enforcement; maintained a 30%+ repeat-client rate.
- **Live Showcase Management:** Directed full event logistics, artist travel, and technical riders for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero live performance disruption.

### Business Development Intern | Pencil Mark Interior Solutions LLP, Bengaluru
*Jul 2025 – Aug 2025*
- **B2B Pipeline & Revenue:** Drove outbound corporate lead generation across commercial workspace projects, managing 15+ concurrent client threads and helping close ₹1.5L+ in commercial interior contracts (18% conversion rate).
- **Executive Commendation:** Awarded a formal written management commendation by leadership for exceptional sales drive, client negotiation, and active pipeline expansion.

### AI Data Operations Intern | Instawork Services India Pvt. Ltd., Bengaluru
*Dec 2025*
- **Robotics & Vision Datasets:** Curated and annotated high-density multi-modal datasets training enterprise robotics and human activity recognition machine learning models.
- **99%+ QA Benchmark:** Maintained a verified 99%+ quality assurance accuracy rating across all data streams, authoring standardized capture SOPs.

### Exhibition Operations & Commercial Lead | Salt in My Coca — AERO India 2025, Yelahanka AFB
*Feb 2025*
- **High-Density Expo Logistics:** Led 7-day stall operations, visitor engagement, and inventory logistics at Asia's premier defense expo (100k+ attendees), achieving zero inventory shrinkage under strict military security protocols.

### Operations, Unit Economics & Retail Lead | Mehra's Kitchen & Family Commercial Enterprise, BLR/CCU
*2018 – 2025*
- **Ground Operations Mastery:** Managed raw material procurement, unit cost economics, menu pricing, inventory turnover, supplier negotiations, and daily cash reconciliation across retail and food operations.

### Project: Automated Market Intelligence & Pipeline Engine | Independent System, Bengaluru
*2025 – 2026*
- **Data & Automation Architecture:** Engineered automated data extraction and enrichment pipelines analyzing 4,500+ commercial entities and 9,200+ network records using Python, LLM structured outputs, and Power Query.

---

## EDUCATION & CERTIFICATIONS
**Bachelor of Business Administration (BBA) — International Business** | **2023 – 2026**  
*Dayananda Sagar University, Bengaluru* — Focus: International Trade & EXIM Policies, Incoterms 2020, Supply Chain, Business Statistics.  
**Certifications & Honors:** Written Management Commendation (Pencil Mark, 2025) • Google Digital Marketing Professional (2024) • Service Marketing (NPTEL, IIT Kharagpur, 2025) • Generative AI Mastermind (Outskill, 2025) • AI Tools & ChatGPT (be10x, 2025)
"""

with open(BASE_DIR / "ADITYA_MEHRA_COMPLETE_1PAGE_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_COMPLETE_1PAGE_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("HTML and MD written.")
