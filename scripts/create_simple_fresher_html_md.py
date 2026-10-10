from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — BBA Graduate CV</title>
<style>
  :root {
    --primary: #0f172a;       /* Slate / Dark Navy */
    --teal: #0d9488;          /* Accent Teal */
    --slate: #334155;         /* Muted Heading */
    --text: #1e293b;          /* Body Text */
    --muted: #64748b;         /* Subtext */
    --border: #cbd5e1;        /* Divider */
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

  .cv-card {
    max-width: 800px;
    margin: 0 auto;
    background: #ffffff;
    padding: 30px 38px;
    border-radius: 8px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
  }

  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 8px;
    margin-bottom: 10px;
  }

  h1 {
    font-size: 20pt;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 1px;
  }

  .subtitle {
    font-size: 9.5pt;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.4px;
    margin-bottom: 4px;
  }

  .contact-bar {
    font-size: 8.5pt;
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

  section { margin-bottom: 9px; }

  h2 {
    font-size: 9.5pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 2px;
    margin-bottom: 5px;
  }

  .summary-p {
    font-size: 8.5pt;
    text-align: justify;
    line-height: 1.38;
    color: var(--text);
  }

  .edu-row {
    font-size: 8.5pt;
    line-height: 1.35;
  }

  .job-row { margin-bottom: 6px; }
  .job-title-bar {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 8.8pt;
  }
  .job-title { font-weight: 700; color: var(--primary); }
  .job-company { font-style: italic; color: var(--slate); font-weight: 600; }
  .job-date { font-weight: 700; color: var(--teal); font-size: 8pt; }

  ul.bullets {
    list-style-type: disc;
    padding-left: 15px;
    font-size: 8.3pt;
    margin-top: 1px;
  }

  ul.bullets li {
    margin-bottom: 1.5px;
    line-height: 1.32;
    text-align: justify;
  }

  .skills-grid {
    font-size: 8.3pt;
    line-height: 1.35;
  }

  .skills-grid p {
    margin-bottom: 2px;
  }

  .cert-row {
    font-size: 8.2pt;
    color: var(--text);
    line-height: 1.35;
  }

  .action-bar {
    max-width: 800px;
    margin: 0 auto 12px auto;
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
    body { background: #ffffff; padding: 0; font-size: 8.5pt; }
    .action-bar { display: none; }
    .cv-card { box-shadow: none; padding: 8mm 10mm; max-width: 100%; }
    @page { margin: 8mm 10mm; size: A4 portrait; }
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
    <div class="subtitle">BBA Graduate (International Business) &bull; Operations, Business Development & Growth</div>
    <div class="contact-bar">
      <span>Bengaluru, Karnataka, India</span>
      <span>+91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Career Objective</h2>
    <p class="summary-p">
      Motivated BBA graduate in International Business (Dayananda Sagar University, 2026) seeking an entry-level role in Business Operations, Business Development, or General Management. Combines strong business foundations with hands-on experience managing B2B client pipelines, live event operations for major brands, and AI productivity tools. Commended in writing for outstanding sales performance and ready to contribute from Day 1.
    </p>
  </section>

  <section>
    <h2>Education</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong> | 2023 – 2026<br>
      <em>Dayananda Sagar University, Bengaluru</em> — Key Coursework: International Trade, Global Supply Chain, Marketing, Financial Accounting, Business Statistics.
    </div>
  </section>

  <section>
    <h2>Internships & Work Experience</h2>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions LLP, Bengaluru</span></span>
        <span class="job-date">Jul 2025 – Aug 2025</span>
      </div>
      <ul class="bullets">
        <li>Managed outbound B2B lead generation and client communications across 15+ concurrent commercial leads.</li>
        <li>Assisted in client presentations and contract discussions, helping close ₹1.5L+ in commercial interior contracts.</li>
        <li>Awarded a written management commendation for outstanding pipeline growth and proactive sales execution.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">AI Data Operations Intern</strong> | <span class="job-company">Instawork Services India Pvt. Ltd., Bengaluru</span></span>
        <span class="job-date">Dec 2025</span>
      </div>
      <ul class="bullets">
        <li>Assisted in AI data collection and annotation pipelines for robotics and human activity machine learning models.</li>
        <li>Maintained 99%+ quality accuracy on all submitted datasets following strict compliance guidelines.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Exhibition & Operations Lead</strong> | <span class="job-company">Salt in My Coca — AERO India 2025, Yelahanka AFB</span></span>
        <span class="job-date">Feb 2025</span>
      </div>
      <ul class="bullets">
        <li>Managed stall setup, product inventory, and visitor engagement over 7 days at Asia's largest aerospace show (100k+ attendees).</li>
        <li>Coordinated with high-profile visitors and defense delegates under strict security protocols with zero asset loss.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Event Coordinator & Operations Lead</strong> | <span class="job-company">Independent Commercial Events, Bengaluru</span></span>
        <span class="job-date">2019 – Present</span>
      </div>
      <ul class="bullets">
        <li>Coordinated on-ground operations and vendor logistics for 300+ events for clients including Tata Communications, Puma, and VH1 Supersonic.</li>
        <li>Negotiated with local vendors to deliver 15–20% cost savings while maintaining a 30%+ repeat-client rate.</li>
        <li>Handled live concert coordination for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero technical delays.</li>
      </ul>
    </div>

    <div class="job-row">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations & Sales Associate</strong> | <span class="job-company">Mehra's Kitchen & Family Business, Bengaluru/Kolkata</span></span>
        <span class="job-date">2018 – 2025</span>
      </div>
      <ul class="bullets">
        <li>Gained hands-on experience in daily retail operations, raw material procurement, inventory tracking, and cash reconciliation.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Key Skills</h2>
    <div class="skills-grid">
      <p><strong>Business & Operations:</strong> B2B Lead Generation, Client Relationship Management, Vendor Coordination, Inventory & Stock Tracking, On-Ground Event Execution.</p>
      <p><strong>Tools & Productivity:</strong> MS Excel (VLOOKUP, Pivot Tables), Google Sheets, CRM Basics (Salesforce, Zoho), AI Tools (ChatGPT, Claude, Notion AI).</p>
      <p><strong>Trade & Commercial:</strong> Incoterms 2020 basics, International Trade Documentation, Commercial Costing, Customer Service.</p>
      <p><strong>Languages:</strong> English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Basic).</p>
    </div>
  </section>

  <section>
    <h2>Certifications & Honors</h2>
    <div class="cert-row">
      &bull; Written Management Commendation for BD Excellence (Pencil Mark, 2025) &bull; Google Digital Marketing Professional Certificate (2024) &bull; Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur, 2025) &bull; Generative AI Mastermind (Outskill, 2025) &bull; AI Tools & ChatGPT for Business Productivity (be10x, 2025)
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

## CAREER OBJECTIVE
Motivated BBA graduate in International Business (Dayananda Sagar University, 2026) seeking an entry-level role in Business Operations, Business Development, or General Management. Combines strong business foundations with hands-on experience managing B2B client pipelines, live event operations for major brands, and AI productivity tools. Commended in writing for outstanding sales performance and ready to contribute from Day 1.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business** | **2023 – 2026**  
*Dayananda Sagar University, Bengaluru*  
- **Key Coursework:** International Trade, Global Supply Chain, Marketing, Financial Accounting, Business Statistics.

---

## INTERNSHIPS & WORK EXPERIENCE

### Business Development Intern | Pencil Mark Interior Solutions LLP, Bengaluru
*Jul 2025 – Aug 2025*
- Managed outbound B2B lead generation and client communications across 15+ concurrent commercial leads.
- Assisted in client presentations and contract discussions, helping close ₹1.5L+ in commercial interior contracts.
- Awarded a written management commendation for outstanding pipeline growth and proactive sales execution.

### AI Data Operations Intern | Instawork Services India Pvt. Ltd., Bengaluru
*Dec 2025*
- Assisted in AI data collection and annotation pipelines for robotics and human activity machine learning models.
- Maintained 99%+ quality accuracy on all submitted datasets following strict compliance guidelines.

### Exhibition & Operations Lead | Salt in My Coca — AERO India 2025, Yelahanka AFB
*Feb 2025*
- Managed stall setup, product inventory, and visitor engagement over 7 days at Asia's largest aerospace show (100k+ attendees).
- Coordinated with high-profile visitors and defense delegates under strict security protocols with zero asset loss.

### Event Coordinator & Operations Lead | Independent Commercial Events, Bengaluru
*2019 – Present*
- Coordinated on-ground operations and vendor logistics for 300+ events for clients including Tata Communications, Puma, and VH1 Supersonic.
- Negotiated with local vendors to deliver 15–20% cost savings while maintaining a 30%+ repeat-client rate.
- Handled live concert coordination for TRILOGY Indo-Jazz Fusion at Bangalore Club (Jan 2026) with zero technical delays.

### Operations & Sales Associate | Mehra's Kitchen & Family Business, Bengaluru/Kolkata
*2018 – 2025*
- Gained hands-on experience in daily retail operations, raw material procurement, inventory tracking, and cash reconciliation.

---

## KEY SKILLS
- **Business & Operations:** B2B Lead Generation, Client Relationship Management, Vendor Coordination, Inventory & Stock Tracking, On-Ground Event Execution.
- **Tools & Productivity:** MS Excel (VLOOKUP, Pivot Tables), Google Sheets, CRM Basics (Salesforce, Zoho), AI Tools (ChatGPT, Claude, Notion AI).
- **Trade & Commercial:** Incoterms 2020 basics, International Trade Documentation, Commercial Costing, Customer Service.
- **Languages:** English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Proficient), French (Basic).

---

## CERTIFICATIONS & HONORS
- Written Management Commendation for BD Excellence (Pencil Mark Interior Solutions, 2025)
- Google Digital Marketing Professional Certificate (Google, 2024)
- Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur, 2025)
- Generative AI Mastermind (Outskill, 2025)
- AI Tools & ChatGPT for Business Productivity (be10x, 2025)
"""

with open(BASE_DIR / "ADITYA_MEHRA_SIMPLE_FRESHER_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_SIMPLE_FRESHER_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Simple Fresher HTML and MD files written successfully.")
