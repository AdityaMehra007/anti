from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — Simple Fresher CV</title>
<style>
  :root {
    --primary: #0f172a;
    --teal: #0d9488;
    --slate: #475569;
    --text: #1e293b;
    --border: #cbd5e1;
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
    padding-bottom: 10px;
    margin-bottom: 14px;
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
    color: var(--teal);
    letter-spacing: 0.4px;
    margin-bottom: 5px;
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
    font-size: 10.5pt;
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
    <div class="subtitle">BBA Graduate &bull; Operations, Business Development & Growth</div>
    <div class="contact-bar">
      <span>Bengaluru, India</span>
      <span>+91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Objective</h2>
    <p class="obj">
      Recent BBA graduate in International Business seeking an entry-level position in Business Operations, Business Development, or General Management. Brings practical experience in client communication, event logistics, and modern digital tools. Eager to learn, quick to adapt, and ready to contribute to a growing team.
    </p>
  </section>

  <section>
    <h2>Education</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong><br>
      <em>Dayananda Sagar University, Bengaluru</em> — Key Subjects: International Trade, Supply Chain Management, Marketing, Business Statistics.
    </div>
  </section>

  <section>
    <h2>Experience & Internships</h2>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions LLP</span></span>
      </div>
      <ul class="bullets">
        <li>Handled corporate client outreach, initial introductions, and follow-ups for interior design projects.</li>
        <li>Assisted in preparing commercial proposals and client meetings.</li>
        <li>Received a written management commendation for active initiative and sales drive.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">AI Data Operations Intern</strong> | <span class="job-company">Instawork Services India Pvt. Ltd.</span></span>
      </div>
      <ul class="bullets">
        <li>Supported data collection, verification, and annotation for robotics machine learning models.</li>
        <li>Followed quality standards to ensure accurate and clean dataset submissions.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Exhibition Operations Lead</strong> | <span class="job-company">Salt in My Coca — AERO India</span></span>
      </div>
      <ul class="bullets">
        <li>Managed stall setup, product inventory, and visitor coordination at a major aerospace show.</li>
        <li>Interacted with corporate and international visitors under strict venue protocols.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Event Coordinator & Operations Lead</strong> | <span class="job-company">Commercial Event Operations</span></span>
      </div>
      <ul class="bullets">
        <li>Coordinated on-ground logistics, vendor arrangements, and crew support for corporate events.</li>
        <li>Assisted in vendor negotiations to reduce costs while maintaining quality standards.</li>
        <li>Coordinated artist logistics and equipment setup for live musical performances.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations & Sales Assistant</strong> | <span class="job-company">Mehra's Kitchen & Family Retail</span></span>
      </div>
      <ul class="bullets">
        <li>Handled daily store operations, supplier orders, inventory tracking, and customer billing.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Key Skills</h2>
    <div class="skills-row">
      <p><strong>Operations & Business:</strong> Vendor Coordination, Client Communication, Event Logistics, Store Operations, Inventory Handling.</p>
      <p><strong>Tools & Software:</strong> MS Excel, Google Workspace, CRM Basics, AI Tools (ChatGPT, Claude, Notion).</p>
      <p><strong>Languages:</strong> English, Hindi, Punjabi, Bengali, French.</p>
    </div>
  </section>

  <section>
    <h2>Certifications & Honors</h2>
    <div class="cert-row">
      &bull; Written Management Commendation (Pencil Mark) &bull; Google Digital Marketing Professional Certificate &bull; Service Marketing (NPTEL, IIT Kharagpur) &bull; Generative AI Mastermind (Outskill)
    </div>
  </section>
</main>

</body>
</html>
"""

md_content = """# ADITYA MEHRA
**Bengaluru, India** | **+91 7003456624** | **adityamehra799@gmail.com**  
**LinkedIn:** [linkedin.com/in/aditya-mehra-b8644b326](https://linkedin.com/in/aditya-mehra-b8644b326) | **Portfolio & Code:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## OBJECTIVE
Recent BBA graduate in International Business seeking an entry-level position in Business Operations, Business Development, or General Management. Brings practical experience in client communication, event logistics, and modern digital tools. Eager to learn, quick to adapt, and ready to contribute to a growing team.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business**  
*Dayananda Sagar University, Bengaluru* — Key Subjects: International Trade, Supply Chain Management, Marketing, Business Statistics.

---

## EXPERIENCE & INTERNSHIPS

### Business Development Intern | Pencil Mark Interior Solutions LLP
- Handled corporate client outreach, initial introductions, and follow-ups for interior design projects.
- Assisted in preparing commercial proposals and client meetings.
- Received a written management commendation for active initiative and sales drive.

### AI Data Operations Intern | Instawork Services India Pvt. Ltd.
- Supported data collection, verification, and annotation for robotics machine learning models.
- Followed quality standards to ensure accurate and clean dataset submissions.

### Exhibition Operations Lead | Salt in My Coca — AERO India
- Managed stall setup, product inventory, and visitor coordination at a major aerospace show.
- Interacted with corporate and international visitors under strict venue protocols.

### Event Coordinator & Operations Lead | Commercial Event Operations
- Coordinated on-ground logistics, vendor arrangements, and crew support for corporate events.
- Assisted in vendor negotiations to reduce costs while maintaining quality standards.
- Coordinated artist logistics and equipment setup for live musical performances.

### Operations & Sales Assistant | Mehra's Kitchen & Family Retail
- Handled daily store operations, supplier orders, inventory tracking, and customer billing.

---

## KEY SKILLS
- **Operations & Business:** Vendor Coordination, Client Communication, Event Logistics, Store Operations, Inventory Handling.
- **Tools & Software:** MS Excel, Google Workspace, CRM Basics, AI Tools (ChatGPT, Claude, Notion).
- **Languages:** English, Hindi, Punjabi, Bengali, French.

---

## CERTIFICATIONS & HONORS
- Written Management Commendation for Business Development (Pencil Mark)
- Google Digital Marketing Professional Certificate (Google)
- Service Marketing: A Practical Approach (NPTEL, IIT Kharagpur)
- Generative AI Mastermind (Outskill)
"""

with open(BASE_DIR / "ADITYA_MEHRA_VERY_SIMPLE_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_VERY_SIMPLE_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Generated HTML and Markdown for Very Simple CV.")
