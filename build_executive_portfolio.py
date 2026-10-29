import os

def build_portfolio():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aditya Mehra | Executive Operations, Global Trade & AI Systems Portfolio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #050811;
      --bg-surface: #0a0f1e;
      --bg-card: #0f172a;
      --bg-card-hover: #162038;
      --border: #1e293b;
      --border-focus: #00f2fe;
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.25);
      --emerald: #10b981;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Lighting */
    .glow-1 {
      position: fixed;
      top: -150px;
      right: -150px;
      width: 650px;
      height: 650px;
      background: radial-gradient(circle, rgba(0, 242, 254, 0.09) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }
    .glow-2 {
      position: fixed;
      bottom: -150px;
      left: -150px;
      width: 650px;
      height: 650px;
      background: radial-gradient(circle, rgba(139, 92, 246, 0.09) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }

    /* Navigation */
    nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(5, 8, 17, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 16px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .brand {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand span { color: var(--cyan); }

    .status-badge {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--emerald);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .status-badge::before {
      content: '';
      width: 6px;
      height: 6px;
      background: var(--emerald);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--emerald);
    }

    .nav-actions {
      display: flex;
      gap: 14px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .btn-outline {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
    }
    .btn-outline:hover {
      color: #fff;
      border-color: var(--cyan);
      background: rgba(0, 242, 254, 0.05);
    }
    .btn-primary {
      background: var(--cyan);
      color: #050811;
      border: 1px solid var(--cyan);
      font-weight: 700;
    }
    .btn-primary:hover {
      box-shadow: 0 0 20px var(--cyan-glow);
      transform: translateY(-1px);
    }

    /* Container */
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 36px 80px;
      position: relative;
      z-index: 1;
    }

    /* Hero */
    .hero {
      padding: 70px 0 50px;
    }

    .hero-eyebrow {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--cyan);
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .hero h1 {
      font-size: 52px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 18px;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-tagline {
      font-size: 20px;
      color: var(--cyan);
      font-weight: 600;
      margin-bottom: 18px;
    }

    .hero-bio {
      font-size: 16px;
      color: var(--text-muted);
      max-width: 820px;
      line-height: 1.65;
      margin-bottom: 30px;
    }

    .contact-bar {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 36px;
    }

    .contact-item {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      color: var(--text-muted);
      text-decoration: none;
      font-family: var(--font-mono);
      transition: all 0.2s ease;
    }
    .contact-item:hover {
      border-color: var(--cyan);
      color: #fff;
    }

    /* Metric Grid */
    .hero-metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }

    .h-metric {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }
    .h-metric-val {
      font-size: 28px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #fff;
      margin-bottom: 4px;
    }
    .h-metric-lbl {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Section Styling */
    section {
      margin-top: 70px;
    }

    .section-head {
      margin-bottom: 30px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .section-head h2 {
      font-size: 26px;
      font-weight: 800;
      color: #fff;
    }
    .section-head p {
      font-size: 14px;
      color: var(--text-muted);
    }

    /* Proof of Work Grid */
    .pow-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 22px;
    }

    .pow-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
    }
    .pow-card:hover {
      border-color: var(--cyan);
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .pow-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.1);
      color: var(--cyan);
      display: inline-block;
      margin-bottom: 12px;
    }
    .pow-badge.emerald {
      background: rgba(16, 185, 129, 0.1);
      color: var(--emerald);
    }
    .pow-badge.purple {
      background: rgba(139, 92, 246, 0.1);
      color: var(--purple);
    }
    .pow-badge.amber {
      background: rgba(245, 158, 11, 0.1);
      color: var(--amber);
    }

    .pow-title {
      font-size: 19px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }

    .pow-org {
      font-size: 13px;
      color: var(--cyan);
      font-weight: 600;
      margin-bottom: 14px;
    }

    .pow-desc {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 18px;
    }

    .pow-bullets {
      list-style: none;
      margin-bottom: 20px;
    }
    .pow-bullets li {
      font-size: 13px;
      color: #cbd5e1;
      margin-bottom: 8px;
      padding-left: 18px;
      position: relative;
    }
    .pow-bullets li::before {
      content: '▹';
      position: absolute;
      left: 0;
      color: var(--cyan);
    }

    .pow-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }
    .pow-tag {
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }

    /* Core Competencies Matrix */
    .skills-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }

    .skill-block {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
    }
    .skill-block-title {
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .skill-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .skill-item {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: var(--text-muted);
      padding-bottom: 6px;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.06);
    }
    .skill-item span:first-child { color: #e2e8f0; font-weight: 500; }
    .skill-item span:last-child { color: var(--cyan); font-family: var(--font-mono); font-size: 11px; }

    /* Interactive Strike Pitch Drawer */
    .pitch-box {
      background: linear-gradient(145deg, var(--bg-surface), var(--bg-card));
      border: 1px solid var(--cyan-glow);
      border-radius: 14px;
      padding: 32px;
      margin-top: 24px;
      position: relative;
    }
    .pitch-text {
      background: #04060c;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: #cbd5e1;
      white-space: pre-wrap;
      line-height: 1.6;
      margin: 16px 0;
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border);
      padding: 40px 0;
      text-align: center;
      color: var(--text-sub);
      font-size: 13px;
      font-family: var(--font-mono);
      margin-top: 80px;
    }
  </style>
</head>
<body>

  <div class="glow-1"></div>
  <div class="glow-2"></div>

  <!-- Navbar -->
  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ PORTFOLIO</span>
      <div class="status-badge">Immediate Joining • Bengaluru</div>
    </div>
    <div class="nav-actions">
      <a href="#proof-of-work" class="btn btn-outline">Proof of Work</a>
      <a href="#competencies" class="btn btn-outline">Skills Matrix</a>
      <a href="mailto:adityamehra799@gmail.com" class="btn btn-primary">Hire Aditya ✉</a>
    </div>
  </nav>

  <main class="container">

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-eyebrow">
        <span>●</span> BBA INTERNATIONAL BUSINESS • DAYANANDA SAGAR UNIVERSITY '26
      </div>
      <h1>Operations, International Trade & AI Systems Specialist</h1>
      <div class="hero-tagline">Turning complex business logic, cross-border workflows & modern AI tools into high-velocity operational execution.</div>
      <p class="hero-bio">
        Bengaluru-based operations graduate equipped with verified multi-sector proof-of-work across high-footfall event activations (Aero India), 
        commercial vendor management (Pencil Mark), robotics data quality assurance (Instawork), family business accounting/dispatch (Kolkata), 
        and autonomous software tools built with Python, SQLite, and Google Antigravity.
      </p>

      <!-- Contact Bar -->
      <div class="contact-bar">
        <a href="tel:+917003456624" class="contact-item">📞 +91 7003456624</a>
        <a href="mailto:adityamehra799@gmail.com" class="contact-item">✉ adityamehra799@gmail.com</a>
        <a href="https://linkedin.com/in/aditya-mehra" target="_blank" class="contact-item">💼 LinkedIn Profile ↗</a>
        <a href="https://github.com/AdityaMehra007" target="_blank" class="contact-item">🐙 GitHub: AdityaMehra007 ↗</a>
        <a href="BANGALORE_360_VISUAL_WORLD.html" target="_blank" class="contact-item" style="border-color: var(--cyan); color: var(--cyan);">🌐 Bengaluru 360° Console ↗</a>
      </div>

      <!-- Quick Metrics -->
      <div class="hero-metrics">
        <div class="h-metric">
          <div class="h-metric-val">100%</div>
          <div class="h-metric-lbl">Immediate Joining Readiness</div>
        </div>
        <div class="h-metric">
          <div class="h-metric-val">3</div>
          <div class="h-metric-lbl">Completed Internships (2 Corp + 1 NGO)</div>
        </div>
        <div class="h-metric">
          <div class="h-metric-val">16/16</div>
          <div class="h-metric-lbl">Unit Tests Passing Green on Python CLI</div>
        </div>
        <div class="h-metric">
          <div class="h-metric-val">5,000+</div>
          <div class="h-metric-lbl">Employer Ecosystem Mapped</div>
        </div>
      </div>
    </section>

    <!-- Proof of Work Section -->
    <section id="proof-of-work">
      <div class="section-head">
        <div>
          <h2>Verifiable Proof of Work</h2>
          <p>Real projects, corporate internships, and field operations with measurable outcomes</p>
        </div>
      </div>

      <div class="pow-grid">
        <!-- Project 1 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge">Tech Project & Automation</span>
            <div class="pow-title">Autonomous Operations & Recruiter Dispatch Engine</div>
            <div class="pow-org">Google Antigravity • Python • SQLite • Agentic Workflows</div>
            <p class="pow-desc">
              Engineered an autonomous career operations pipeline prototype linking 5,000+ verified corporate entities with dynamic InMail pitch synthesis, compensation filtering, and calendar event generation.
            </p>
            <ul class="pow-bullets">
              <li>Architected SQLite relational database containing 5,000 employers, 7,500 HR leads, and 20 tech parks.</li>
              <li>Integrated automated regression testing framework with 16/16 unit tests passing green.</li>
              <li>Eliminated 80% of repetitive outreach friction via automated CLI dispatchers.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">Python 3.12</span>
            <span class="pow-tag">SQLite3</span>
            <span class="pow-tag">Google Antigravity</span>
            <span class="pow-tag">REST APIs</span>
          </div>
        </div>

        <!-- Project 2 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge emerald">Corporate Internship</span>
            <div class="pow-title">Operations & AI Data Collection Intern</div>
            <div class="pow-org">Instawork Services India Pvt. Ltd. • Bengaluru (2025)</div>
            <p class="pow-desc">
              Executed rigorous real-world data collection and operational quality audits supporting advanced AI & robotics systems under strict time-to-deliver benchmarks.
            </p>
            <ul class="pow-bullets">
              <li>Verified input datasets against strict precision tolerances, achieving 99%+ accuracy ratings.</li>
              <li>Logged and reported edge-case data deviations to engineering leads for rapid protocol patches.</li>
              <li>Operated within standardized digital SOP checklists for high-throughput daily quotas.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">AI Data QA</span>
            <span class="pow-tag">Robotics Benchmarks</span>
            <span class="pow-tag">SOP Compliance</span>
            <span class="pow-tag">Operations Support</span>
          </div>
        </div>

        <!-- Project 3 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge purple">Corporate Internship</span>
            <div class="pow-title">Commercial Operations & Business Development Intern</div>
            <div class="pow-org">Pencil Mark Interior Solutions LLP • Bengaluru (July – Aug 2025)</div>
            <p class="pow-desc">
              Bridged client discovery meetings with vendor delivery schedules for high-value commercial interior and fit-out contracts across Bengaluru.
            </p>
            <ul class="pow-bullets">
              <li>Converted unstructured corporate client specifications into standardized BOM and project briefs.</li>
              <li>Maintained supplier and contractor delivery timelines in Excel, preventing site bottlenecks.</li>
              <li>Assisted senior project managers in resolving on-site material requisition variances.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">Vendor Management</span>
            <span class="pow-tag">MS Excel</span>
            <span class="pow-tag">Client Servicing</span>
            <span class="pow-tag">Procurement</span>
          </div>
        </div>

        <!-- Project 4 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge amber">High-Footfall Field Logistics</span>
            <div class="pow-title">Aero India & Major Event Coordination</div>
            <div class="pow-org">Aero India (Yelahanka) • Salt in My Cocoa • TRILOGY Concerts</div>
            <p class="pow-desc">
              Field operations coordinator handling rapid inventory replenishment, customer sampling queues, artist logistics, and UPI cashflow balancing during peak Asia-level footfalls.
            </p>
            <ul class="pow-bullets">
              <li>Managed end-to-end stall setup, product merchandising, and continuous restocking during Aero India.</li>
              <li>Executed 100% daily cash & digital UPI reconciliations with zero discrepancy across 5-day rush.</li>
              <li>Coordinated artist stage schedules, vendor hospitality, and emergency green-room logistics.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">High-Stress Execution</span>
            <span class="pow-tag">Cash Reconciliations</span>
            <span class="pow-tag">Inventory Flow</span>
            <span class="pow-tag">Brand Activation</span>
          </div>
        </div>

        <!-- Project 5 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge">Family Business Operations</span>
            <div class="pow-title">Operations & Logistics Assistant</div>
            <div class="pow-org">Family Enterprise • Kolkata (2018 – 2020)</div>
            <p class="pow-desc">
              Foundational grounding in commercial logistics: handled daily invoices, supplier follow-ups, inventory audit ledgers, and delivery dispatches.
            </p>
            <ul class="pow-bullets">
              <li>Audited physical stock vs recorded inventory in Excel sheets, detecting and resolving stock shrinkages.</li>
              <li>Maintained steady supplier relations and negotiated delivery lead times during supply tightness.</li>
              <li>Prepared daily dispatch manifests and monitored last-mile handoffs to local couriers.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">Inventory Ledgers</span>
            <span class="pow-tag">Order Dispatch</span>
            <span class="pow-tag">Supplier Relations</span>
            <span class="pow-tag">Cashflow Tracking</span>
          </div>
        </div>

        <!-- Project 6 -->
        <div class="pow-card">
          <div>
            <span class="pow-badge emerald">Social Operations</span>
            <div class="pow-title">Community Operations Intern</div>
            <div class="pow-org">Non-Profit Social Initiative • Bengaluru (2024)</div>
            <p class="pow-desc">
              Managed grassroots logistics, volunteer dispatch schedules, and on-ground attendee registration for social impact community drives.
            </p>
            <ul class="pow-bullets">
              <li>Organized field team rosters and material distribution kits for 50+ volunteers.</li>
              <li>Standardized attendee registration workflows, capturing verified contact databases.</li>
            </ul>
          </div>
          <div class="pow-tags">
            <span class="pow-tag">Volunteer Ops</span>
            <span class="pow-tag">Grassroots Logistics</span>
            <span class="pow-tag">Community Outreach</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Competencies & Skills Matrix -->
    <section id="competencies">
      <div class="section-head">
        <div>
          <h2>Core Competencies Matrix</h2>
          <p>Where academic business rigor intersects with modern technical agility</p>
        </div>
      </div>

      <div class="skills-grid">
        <div class="skill-block">
          <div class="skill-block-title">📦 Global Trade & EXIM Logistics</div>
          <div class="skill-list">
            <div class="skill-item"><span>Incoterms 2020 & Risk Transfer</span><span>Advanced</span></div>
            <div class="skill-item"><span>Bill of Lading & Documentation</span><span>Proficient</span></div>
            <div class="skill-item"><span>Customs Clearance Workflows</span><span>Proficient</span></div>
            <div class="skill-item"><span>Freight Forwarding SOPs</span><span>Working</span></div>
            <div class="skill-item"><span>Supply Chain Reconciliations</span><span>Advanced</span></div>
          </div>
        </div>

        <div class="skill-block">
          <div class="skill-block-title">⚙️ Business & Corporate Operations</div>
          <div class="skill-list">
            <div class="skill-item"><span>Vendor & Contractor Management</span><span>Advanced</span></div>
            <div class="skill-item"><span>Task Scheduling & SLA Tracking</span><span>Advanced</span></div>
            <div class="skill-item"><span>Inventory & Cash Reconciliations</span><span>Advanced</span></div>
            <div class="skill-item"><span>Commercial Brief Formulation</span><span>Proficient</span></div>
            <div class="skill-item"><span>Cross-Functional Stakeholder Sync</span><span>Proficient</span></div>
          </div>
        </div>

        <div class="skill-block">
          <div class="skill-block-title">💻 Tech & Modern AI Prototyping</div>
          <div class="skill-list">
            <div class="skill-item"><span>Google Antigravity & Agentic Ops</span><span>Expert</span></div>
            <div class="skill-item"><span>Python 3 Scripting & Automation</span><span>Proficient</span></div>
            <div class="skill-item"><span>SQLite Relational Database Design</span><span>Proficient</span></div>
            <div class="skill-item"><span>HTML5 / CSS3 Cyber Glass UI</span><span>Proficient</span></div>
            <div class="skill-item"><span>Git & GitHub Workflow</span><span>Working</span></div>
          </div>
        </div>

        <div class="skill-block">
          <div class="skill-block-title">📊 Analytics & Productivity Tools</div>
          <div class="skill-list">
            <div class="skill-item"><span>MS Excel (VLOOKUP, Pivots, Formulas)</span><span>Advanced</span></div>
            <div class="skill-item"><span>Google Workspace & Spreadsheets</span><span>Advanced</span></div>
            <div class="skill-item"><span>Google Digital Marketing Certified</span><span>Certified</span></div>
            <div class="skill-item"><span>NPTEL Service Marketing</span><span>Certified</span></div>
            <div class="skill-item"><span>Bilingual Communication (EN / HI)</span><span>Native</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 1-Click Executive Outreach Pitch Generator -->
    <section>
      <div class="section-head">
        <div>
          <h2>One-Click Recruiter InMail Pitch</h2>
          <p>Pre-synthesized, verified pitch ready to copy and send to hiring managers</p>
        </div>
        <button class="btn btn-primary" onclick="navigator.clipboard.writeText(document.getElementById('pitchCode').innerText); alert('Pitch copied to clipboard!');">Copy Pitch 📋</button>
      </div>

      <div class="pitch-box">
        <div style="font-size: 14px; font-weight: 700; color: #fff;">Subject: Aditya Mehra — BBA International Business (DSU '26) | Operations Trainee / Analyst</div>
        <div class="pitch-text" id="pitchCode">Dear Hiring Lead,

I came across your active operations requirements in Bengaluru.

As a final-year BBA International Business graduate from Dayananda Sagar University (DSU, 2026), I bring verifiable operational proof-of-work across high-footfall logistics (Aero India), commercial interior vendor operations (Pencil Mark), and AI robotics data collection (Instawork).

Key Highlights I bring on Day 1:
1. Operational Discipline: Zero discrepancy across high-stress event cash/UPI reconciliations and vendor procurement matrices.
2. Technical Agility: Built autonomous operations pipelines in Python & SQLite with 16/16 verified unit tests passing green.
3. Zero Notice Period: Available for immediate full-time joining in Bengaluru with complete schedule flexibility.

You can view my verified proof-of-work and project portfolio here:
https://github.com/AdityaMehra007/anti

I would welcome a brief 5-minute introductory call this week to demonstrate how I can immediately support your team's operational backlog.

Best regards,
Aditya Mehra
Bengaluru, India | +91 7003456624 | adityamehra799@gmail.com
LinkedIn: linkedin.com/in/aditya-mehra | GitHub: github.com/AdityaMehra007</div>
      </div>
    </section>

  </main>

  <footer>
    ADITYA MEHRA • BBA INTERNATIONAL BUSINESS '26 • DAYANANDA SAGAR UNIVERSITY, BENGALURU
    <br>POWERED BY OMEGA ∞ SUPREME AUTONOMOUS CAREER SUITE
  </footer>

</body>
</html>
'''

    out_file = 'e:/anti/ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Executive Portfolio at {out_file}")

if __name__ == '__main__':
    build_portfolio()
