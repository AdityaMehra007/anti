from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — BBA Graduate Fresher CV</title>
<style>
  :root {
    --primary: #0f172a;       /* Dark Charcoal / Navy */
    --slate: #475569;         /* Slate Secondary */
    --text: #1e293b;          /* Body Text */
    --border: #cbd5e1;        /* Divider */
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: Calibri, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    color: var(--text);
    background-color: #f8fafc;
    line-height: 1.4;
    font-size: 9.5pt;
    padding: 24px;
    -webkit-font-smoothing: antialiased;
  }

  .cv-card {
    max-width: 780px;
    margin: 0 auto;
    background: #ffffff;
    padding: 36px 44px;
    border-radius: 8px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
  }

  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 8px;
    margin-bottom: 12px;
  }

  h1 {
    font-size: 22pt;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .subtitle {
    font-size: 10pt;
    font-weight: 700;
    color: var(--slate);
    letter-spacing: 0.4px;
    margin-bottom: 4px;
  }

  .contact-bar {
    font-size: 9pt;
    color: var(--slate);
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
  }

  .contact-bar a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
  }

  .contact-bar a:hover { text-decoration: underline; }

  section { margin-bottom: 12px; }

  h2 {
    font-size: 10pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 2px;
    margin-bottom: 6px;
  }

  p.obj {
    font-size: 9.2pt;
    text-align: justify;
    line-height: 1.45;
  }

  .edu-row {
    font-size: 9.2pt;
    line-height: 1.4;
  }

  .job-block { margin-bottom: 7px; }
  .job-title-bar {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 9.2pt;
    margin-bottom: 2px;
  }
  .job-title { font-weight: 700; color: var(--primary); }
  .job-company { font-style: italic; color: var(--slate); font-weight: 600; }

  ul.bullets {
    list-style-type: disc;
    padding-left: 18px;
    font-size: 9pt;
  }

  ul.bullets li {
    margin-bottom: 2px;
    line-height: 1.38;
    text-align: justify;
  }

  .skills-row {
    font-size: 9pt;
    line-height: 1.42;
  }

  .skills-row p { margin-bottom: 2px; }

  .cert-row {
    font-size: 8.8pt;
    color: var(--text);
    line-height: 1.4;
  }

  .action-bar {
    max-width: 780px;
    margin: 0 auto 12px auto;
    display: flex;
    justify-content: flex-end;
  }

  .btn {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 7px 16px;
    font-size: 9pt;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
  }

  @media print {
    body { background: #ffffff; padding: 0; font-size: 9pt; }
    .action-bar { display: none; }
    .cv-card { box-shadow: none; padding: 8mm 12mm; max-width: 100%; }
    @page { margin: 8mm 12mm; size: A4 portrait; }
  }
</style>
</head>
<body>

<div class="action-bar">
  <button class="btn" onclick="window.print()">Print / Save PDF</button>
</div>

<main class="cv-card">
  <header>
    <h1>Aditya Mehra</h1>
    <div class="subtitle">BBA Graduate &bull; Fresher</div>
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
    <p class="obj">
      Motivated BBA graduate in International Business seeking an entry-level opportunity in Business Operations, Sales, Business Development, or Management Support. Quick learner with hands-on internship experience in client communication, event coordination, and modern computer tools. Eager to start my career and contribute positively to the organization.
    </p>
  </section>

  <section>
    <h2>Education</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong><br>
      <em>Dayananda Sagar University, Bengaluru</em><br>
      Relevant Subjects: International Business, Marketing Management, Supply Chain Management, Business Communication, Financial Accounting.
    </div>
  </section>

  <section>
    <h2>Internships & Practical Experience</h2>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions LLP, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Handled corporate client outreach, introduced design services to prospective businesses, and followed up on active inquiries.</li>
        <li>Assisted senior management in preparing proposals, presentations, and client quotation reviews.</li>
        <li>Received an official written letter of commendation from management for good performance and sales initiative.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations Intern</strong> | <span class="job-company">Instawork Services India Pvt. Ltd., Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Assisted the team in data collection, categorization, and quality checking for robotics training models.</li>
        <li>Followed guidelines closely to maintain high accuracy and consistency in daily task submissions.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Stall & Exhibition Coordinator</strong> | <span class="job-company">Salt in My Coca — AERO India Expo, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Managed retail stall setup, product displays, and customer service at a premier aerospace exhibition.</li>
        <li>Handled product inventory and coordinated with diverse visitors while following event safety protocols.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Event Coordinator & Operations Support</strong> | <span class="job-company">Commercial & Cultural Events, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Coordinated on-ground arrangements, local vendor supplies, and stage setups for corporate and music events.</li>
        <li>Assisted in daily operations and customer billing for retail family business activities.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Key Skills</h2>
    <div class="skills-row">
      <p><strong>Computer & Software:</strong> MS Office (Word, Excel, PowerPoint), Google Workspace, Basic CRM, Internet Research, AI Tools (ChatGPT).</p>
      <p><strong>Professional & Personal:</strong> Client Communication, Problem Solving, Vendor Coordination, Teamwork, Time Management.</p>
      <p><strong>Languages:</strong> English (Fluent), Hindi (Fluent), Punjabi (Native), Bengali (Conversational).</p>
    </div>
  </section>

  <section>
    <h2>Certifications</h2>
    <div class="cert-row">
      &bull; Certificate of Commendation for Business Development (Pencil Mark) &bull; Google Digital Marketing Professional Certificate (Google) &bull; Service Marketing Certification (NPTEL, IIT Kharagpur) &bull; Generative AI Certification (Outskill)
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
Motivated BBA graduate in International Business seeking an entry-level opportunity in Business Operations, Sales, Business Development, or Management Support. Quick learner with hands-on internship experience in client communication, event coordination, and modern computer tools. Eager to start my career and contribute positively to the organization.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business**  
*Dayananda Sagar University, Bengaluru*  
- **Relevant Subjects:** International Business, Marketing Management, Supply Chain Management, Business Communication, Financial Accounting.

---

## INTERNSHIPS & PRACTICAL EXPERIENCE

### Business Development Intern | Pencil Mark Interior Solutions LLP, Bengaluru
- Handled corporate client outreach, introduced design services to prospective businesses, and followed up on active inquiries.
- Assisted senior management in preparing proposals, presentations, and client quotation reviews.
- Received an official written letter of commendation from management for good performance and sales initiative.

### Operations Intern | Instawork Services India Pvt. Ltd., Bengaluru
- Assisted the team in data collection, categorization, and quality checking for robotics training models.
- Followed guidelines closely to maintain high accuracy and consistency in daily task submissions.

### Stall & Exhibition Coordinator | Salt in My Coca — AERO India Expo, Bengaluru
- Managed retail stall setup, product displays, and customer service at a premier aerospace exhibition.
- Handled product inventory and coordinated with diverse visitors while following event safety protocols.

### Event Coordinator & Operations Support | Commercial & Cultural Events, Bengaluru
- Coordinated on-ground arrangements, local vendor supplies, and stage setups for corporate and music events.
- Assisted in daily operations and customer billing for retail family business activities.

---

## KEY SKILLS
- **Computer & Software:** MS Office (Word, Excel, PowerPoint), Google Workspace, Basic CRM, Internet Research, AI Tools (ChatGPT).
- **Professional & Personal:** Client Communication, Problem Solving, Vendor Coordination, Teamwork, Time Management.
- **Languages:** English (Fluent), Hindi (Fluent), Punjabi (Native), Bengali (Conversational).

---

## CERTIFICATIONS
- Certificate of Commendation for Business Development (Pencil Mark)
- Google Digital Marketing Professional Certificate (Google)
- Service Marketing Certification (NPTEL, IIT Kharagpur)
- Generative AI Certification (Outskill)
"""

with open(BASE_DIR / "ADITYA_MEHRA_BASIC_FRESHER_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_BASIC_FRESHER_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Generated Basic Fresher HTML and Markdown files.")
