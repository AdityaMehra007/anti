from pathlib import Path

BASE_DIR = Path(r"e:\anti")

html_2page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aditya Mehra — Universal Master Executive CV (2-Page)</title>
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
    line-height: 1.4;
    font-size: 9.5pt;
    padding: 24px;
    -webkit-font-smoothing: antialiased;
  }

  .cv-container {
    max-width: 820px;
    margin: 0 auto;
    background: #ffffff;
    padding: 40px 48px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  }

  header {
    text-align: center;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 12px;
    margin-bottom: 14px;
  }

  h1 {
    font-size: 22pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: var(--primary);
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .subtitle {
    font-size: 10pt;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    text-transform: uppercase;
  }

  .contact-bar {
    font-size: 8.8pt;
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

  .contact-bar a:hover { text-decoration: underline; }

  section { margin-bottom: 14px; }

  h2 {
    font-size: 10.5pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 2px;
    margin-bottom: 8px;
  }

  .summary-text {
    font-size: 9pt;
    text-align: justify;
    color: var(--text);
    line-height: 1.45;
  }

  .competency-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 4px;
    font-size: 9pt;
  }

  .competency-item { line-height: 1.35; }
  .competency-title { font-weight: 700; color: var(--primary); }

  .job-block { margin-bottom: 10px; }
  .job-header { display: flex; justify-content: space-between; align-items: baseline; }
  .job-title { font-size: 9.8pt; font-weight: 700; color: var(--primary); }
  .job-date { font-size: 8.8pt; font-weight: 700; color: var(--teal); }
  .job-company { font-size: 9pt; font-style: italic; color: var(--accent); margin-bottom: 3px; }

  ul.job-bullets { list-style-type: disc; padding-left: 18px; font-size: 9pt; color: var(--text); }
  ul.job-bullets li { margin-bottom: 2.5px; line-height: 1.38; text-align: justify; }
  ul.job-bullets li strong { color: var(--primary); }

  .cert-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 16px;
    font-size: 8.8pt;
  }

  .cert-item { display: flex; align-items: baseline; gap: 6px; }
  .cert-item span.bullet { color: var(--teal); font-weight: bold; }

  .action-bar {
    max-width: 820px;
    margin: 0 auto 14px auto;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }

  .btn {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 8px 16px;
    font-size: 9pt;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }

  .btn:hover { background: var(--accent); }

  @media print {
    body { background: #ffffff; padding: 0; font-size: 9pt; }
    .action-bar { display: none; }
    .cv-container { box-shadow: none; padding: 12mm 14mm; max-width: 100%; }
    .job-block { page-break-inside: avoid; }
    @page { margin: 10mm 12mm; size: A4 portrait; }
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
    <div class="subtitle">Business Operations &bull; Commercial Growth &bull; AI-Enabled Automation</div>
    <div class="contact-bar">
      <span>Bengaluru, Karnataka, India</span>
      <span>+91 7003456624</span>
      <span><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></span>
      <span><a href="https://linkedin.com/in/aditya-mehra-b8644b326" target="_blank">linkedin.com/in/aditya-mehra-b8644b326</a></span>
      <span><a href="https://github.com/AdityaMehra007" target="_blank">github.com/AdityaMehra007</a></span>
    </div>
  </header>

  <section>
    <h2>Professional Summary</h2>
    <p class="summary-text">
      Results-oriented <strong>Business Operations & Commercial Growth Specialist</strong> with extensive hands-on experience directing <strong>300+ live commercial activations</strong>, governing high-stakes operations at <strong>AERO India 2025</strong> (100k+ visitors, 0 shrinkage), and curating enterprise robotics AI training pipelines at <strong>Instawork</strong> with a verified <strong>99%+ QA benchmark</strong>. Combines an international business foundation (BBA, Dayananda Sagar University '26) with proven execution across direct supplier SLA governance, 15–20% procurement cost reduction, multi-thread B2B deal negotiation, and AI-enabled process automation. Awarded an official written management commendation for commercial excellence. Ready to deploy immediate operational rigor across top-tier MNCs, Global Capability Centers (GCCs), and high-growth enterprises.
    </p>
  </section>

  <section>
    <h2>Core Competencies</h2>
    <div class="competency-list">
      <div class="competency-item">
        <span class="competency-title">Operations & Vendor Governance:</span>
        End-to-End Project Delivery (300+ Events), Direct Supplier SLA Governance, Landed Cost Modeling, 15–20% Procurement Cost Optimization, High-Pressure Crisis Triage.
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
        <span class="competency-title">Analytics & Systems:</span>
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
        <li><strong>Cross-Functional Workflow Sync:</strong> Harmonized on-ground data collection procedures with ML engineering priorities, authoring standardized operational capture SOPs.</li>
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
        <li><strong>End-to-End Production Coordination:</strong> Coordinated logistics for an elite instrumental live concert, overseeing artist travel, hospitality, AV technical riders, and stage acoustic timelines under tight schedules.</li>
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
        <li><strong>Unit Economics & P&L Oversight:</strong> Designed operational and financial workflows for food-stall and cloud-kitchen operations, managing raw material procurement, vendor negotiation, and daily cash flow accounting.</li>
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
    <div class="job-block">
      <div class="job-header">
        <span class="job-title">Bachelor of Business Administration (BBA) — International Business</span>
        <span class="job-date">2023 – 2026</span>
      </div>
      <div class="job-company">Dayananda Sagar University &bull; Bengaluru, India</div>
      <ul class="job-bullets">
        <li><strong>Specialization:</strong> International Trade Policy, Incoterms 2020, Global Supply Chain Architecture, Foreign Exchange Management, Financial Management, Business Statistics. Applied Projects: Landed cost modeling, cross-border freight risk analysis, and automated supplier intelligence.</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>Certifications & Honors</h2>
    <div class="cert-grid">
      <div class="cert-item"><span class="bullet">&bull;</span><div><strong>Written Management Commendation (BD)</strong> — Pencil Mark Interior Solutions (2025)</div></div>
      <div class="cert-item"><span class="bullet">&bull;</span><div><strong>Google Digital Marketing Professional</strong> — Google (2024)</div></div>
      <div class="cert-item"><span class="bullet">&bull;</span><div><strong>Service Marketing: A Practical Approach</strong> — NPTEL, IIT Kharagpur (2025)</div></div>
      <div class="cert-item"><span class="bullet">&bull;</span><div><strong>Generative AI Mastermind</strong> — Outskill (2025)</div></div>
      <div class="cert-item"><span class="bullet">&bull;</span><div><strong>AI Tools & ChatGPT for Business</strong> — be10x (2025)</div></div>
    </div>
  </section>
</main>

</body>
</html>
"""

with open(BASE_DIR / "ADITYA_MEHRA_UNIVERSAL_MASTER_CV.html", "w", encoding="utf-8") as f:
    f.write(html_2page)
print("Updated 2-Page HTML CV.")
