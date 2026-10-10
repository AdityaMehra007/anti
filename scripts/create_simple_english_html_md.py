from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — Simple Resume</title>
<style>
  :root {
    --primary: #0f172a;
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
    <div class="subtitle">BBA Graduate &bull; Looking for Entry-Level Roles</div>
    <div class="contact-bar">
      <span>Bengaluru, Karnataka, India</span>
      <span>Phone: +91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">Email: adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">LinkedIn</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">GitHub</a></span>
    </div>
  </header>

  <section>
    <h2>Career Objective</h2>
    <p class="obj">
      BBA graduate looking for an entry-level job in business operations, sales, or general management. Hardworking, quick to learn new tools, and ready to support the team with day-to-day work. Brings practical experience from internships and college events in client handling, vendor follow-ups, and computer work.
    </p>
  </section>

  <section>
    <h2>Education</h2>
    <div class="edu-row">
      <strong>Bachelor of Business Administration (BBA) — International Business</strong><br>
      <em>Dayananda Sagar University, Bengaluru</em><br>
      Subjects Studied: International Trade, Marketing, Supply Chain, Business Communication, Accounting.
    </div>
  </section>

  <section>
    <h2>Work Experience & Internships</h2>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Business Development Intern</strong> | <span class="job-company">Pencil Mark Interior Solutions, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Contacted new corporate clients through phone calls and emails to introduce office interior design services.</li>
        <li>Helped senior managers prepare simple proposals, price estimates, and meeting slides.</li>
        <li>Received a written appreciation letter from management for good performance and dedication to work.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Operations Intern</strong> | <span class="job-company">Instawork Services India, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Helped the operations team collect, sort, and double-check data for AI and robotics projects.</li>
        <li>Followed instructions carefully to make sure all data was correct and submitted on time.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Stall Coordinator</strong> | <span class="job-company">AERO India Exhibition (Salt in My Coca), Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Set up the display stall, arranged products, and helped visitors with their questions during the event.</li>
        <li>Kept track of stock items and ensured nothing was damaged or lost.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Event Coordinator</strong> | <span class="job-company">Commercial & College Events, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Helped organize live music shows and brand promotion events.</li>
        <li>Coordinated with local suppliers for stage setup, sound equipment, and lighting.</li>
        <li>Handled travel and stay arrangements for visiting artists.</li>
      </ul>
    </div>

    <div class="job-block">
      <div class="job-title-bar">
        <span><strong class="job-title">Store Assistant</strong> | <span class="job-company">Family Retail Store & Food Business, Bengaluru</span></span>
      </div>
      <ul class="bullets">
        <li>Handled daily customer billing, counter sales, and simple stock register updates.</li>
        <li>Talked to suppliers to order fresh stock and raw materials.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Key Skills</h2>
    <div class="skills-row">
      <p><strong>Computer Skills:</strong> MS Excel, MS Word, MS PowerPoint, Google Sheets, Internet Research, ChatGPT basics.</p>
      <p><strong>Work Skills:</strong> Client Communication, Customer Service, Teamwork, Vendor Follow-ups, Event Support, Problem Solving.</p>
      <p><strong>Languages Known:</strong> English, Hindi, Punjabi, Bengali.</p>
    </div>
  </section>

  <section>
    <h2>Certificates</h2>
    <div class="cert-row">
      &bull; Appreciation Letter for Good Work (Pencil Mark) &bull; Digital Marketing Certificate (Google) &bull; Service Marketing Certificate (NPTEL, IIT Kharagpur) &bull; Artificial Intelligence Tools Certificate (Outskill)
    </div>
  </section>
</main>

</body>
</html>
"""

md_content = """# ADITYA MEHRA
**Bengaluru, Karnataka, India** | **Phone:** +91 7003456624 | **Email:** adityamehra799@gmail.com  
**LinkedIn:** [linkedin.com/in/aditya-mehra-b8644b326](https://linkedin.com/in/aditya-mehra-b8644b326) | **GitHub:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## CAREER OBJECTIVE
BBA graduate looking for an entry-level job in business operations, sales, or general management. Hardworking, quick to learn new tools, and ready to support the team with day-to-day work. Brings practical experience from internships and college events in client handling, vendor follow-ups, and computer work.

---

## EDUCATION
**Bachelor of Business Administration (BBA) — International Business**  
*Dayananda Sagar University, Bengaluru*  
- **Subjects Studied:** International Trade, Marketing, Supply Chain, Business Communication, Accounting.

---

## WORK EXPERIENCE & INTERNSHIPS

### Business Development Intern | Pencil Mark Interior Solutions, Bengaluru
- Contacted new corporate clients through phone calls and emails to introduce office interior design services.
- Helped senior managers prepare simple proposals, price estimates, and meeting slides.
- Received a written appreciation letter from management for good performance and dedication to work.

### Operations Intern | Instawork Services India, Bengaluru
- Helped the operations team collect, sort, and double-check data for AI and robotics projects.
- Followed instructions carefully to make sure all data was correct and submitted on time.

### Stall Coordinator | AERO India Exhibition (Salt in My Coca), Bengaluru
- Set up the display stall, arranged products, and helped visitors with their questions during the event.
- Kept track of stock items and ensured nothing was damaged or lost.

### Event Coordinator | Commercial & College Events, Bengaluru
- Helped organize live music shows and brand promotion events.
- Coordinated with local suppliers for stage setup, sound equipment, and lighting.
- Handled travel and stay arrangements for visiting artists.

### Store Assistant | Family Retail Store & Food Business, Bengaluru
- Handled daily customer billing, counter sales, and simple stock register updates.
- Talked to suppliers to order fresh stock and raw materials.

---

## KEY SKILLS
- **Computer Skills:** MS Excel, MS Word, MS PowerPoint, Google Sheets, Internet Research, ChatGPT basics.
- **Work Skills:** Client Communication, Customer Service, Teamwork, Vendor Follow-ups, Event Support, Problem Solving.
- **Languages Known:** English, Hindi, Punjabi, Bengali.

---

## CERTIFICATES
- Appreciation Letter for Good Work (Pencil Mark Interior Solutions)
- Digital Marketing Certificate (Google)
- Service Marketing Certificate (NPTEL, IIT Kharagpur)
- Artificial Intelligence Tools Certificate (Outskill)
"""

with open(BASE_DIR / "ADITYA_MEHRA_SIMPLE_ENGLISH_CV.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(BASE_DIR / "ADITYA_MEHRA_SIMPLE_ENGLISH_CV.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Generated HTML and Markdown for Simple English CV.")
