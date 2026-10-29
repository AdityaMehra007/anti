import os

def build_defense_matrix():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>STAR Interview Defense Matrix & Objection Annihilator | Aditya Mehra</title>
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
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.25);
      --emerald: #10b981;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --rose: #f43f5e;
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
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Nav */
    nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(5, 8, 17, 0.88);
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
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand span { color: var(--cyan); }

    .nav-btn {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .nav-btn:hover {
      color: #fff;
      border-color: var(--cyan);
    }

    /* Container */
    .container {
      max-width: 1250px;
      margin: 0 auto;
      padding: 40px 36px 0;
    }

    /* Hero */
    .hero {
      margin-bottom: 40px;
    }
    .eyebrow {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--cyan);
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }
    .hero h1 {
      font-size: 38px;
      font-weight: 800;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      font-size: 15px;
      color: var(--text-muted);
      max-width: 820px;
    }

    /* Filter Bar */
    .filter-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 30px;
    }
    .filter-btn {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .filter-btn:hover, .filter-btn.active {
      background: rgba(0, 242, 254, 0.1);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    /* Defense Cards Grid */
    .card-list {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .defense-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 28px;
      transition: all 0.25s ease;
    }
    .defense-card:hover {
      border-color: rgba(0, 242, 254, 0.4);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
      gap: 16px;
    }
    .category-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.1);
      color: var(--cyan);
      display: inline-block;
    }
    .category-badge.rose { background: rgba(244, 63, 94, 0.1); color: var(--rose); }
    .category-badge.purple { background: rgba(139, 92, 246, 0.1); color: var(--purple); }
    .category-badge.emerald { background: rgba(16, 185, 129, 0.1); color: var(--emerald); }
    .category-badge.amber { background: rgba(245, 158, 11, 0.1); color: var(--amber); }

    .question-title {
      font-size: 19px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }

    .hidden-test {
      font-size: 13px;
      color: var(--amber);
      font-style: italic;
      margin-bottom: 18px;
      background: rgba(245, 158, 11, 0.06);
      padding: 8px 12px;
      border-left: 3px solid var(--amber);
      border-radius: 0 6px 6px 0;
    }

    /* STAR Breakdown Grid */
    .star-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      margin-bottom: 20px;
    }

    .star-block {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
    }
    .star-label {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--cyan);
      margin-bottom: 6px;
      text-transform: uppercase;
    }
    .star-label.t { color: var(--purple); }
    .star-label.a { color: var(--emerald); }
    .star-label.r { color: var(--amber); }

    .star-content {
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.5;
    }

    /* Flip Question */
    .counter-question {
      background: #04060c;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 14px;
    }
    .counter-icon {
      font-size: 16px;
      color: var(--cyan);
    }
    .counter-text {
      font-size: 13px;
      color: var(--text-muted);
    }
    .counter-text strong {
      color: #fff;
    }

    /* Copy Button */
    .btn-copy {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.2s ease;
    }
    .btn-copy:hover {
      border-color: var(--cyan);
      color: #fff;
    }
  </style>
</head>
<body>

  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ INTERVIEW DEFENSE MATRIX</span>
    </div>
    <div style="display: flex; gap: 10px;">
      <a href="aditya_mehra_executive_portfolio.html" class="nav-btn">Executive Portfolio ↗</a>
      <a href="../bangalore_360_visual_world.html" class="nav-btn">Bengaluru 360° ↗</a>
    </div>
  </nav>

  <main class="container">

    <div class="hero">
      <div class="eyebrow">OBJECTION ANNIHILATION & STAR RESPONSE PROTOCOLS</div>
      <h1>High-Yield Executive Interview Defense Matrix</h1>
      <p>
        Verified answers to the hardest recruiter curveballs, grounding every response in Aditya's real-world proof-of-work: 
        Aero India high-footfall logistics, Instawork AI data quality audits, Pencil Mark commercial interiors, and Python/SQLite autonomous tooling.
      </p>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <button class="filter-btn active" onclick="filterCards('all')">All Questions (5)</button>
      <button class="filter-btn" onclick="filterCards('tech')">BBA in Tech & AI</button>
      <button class="filter-btn" onclick="filterCards('crisis')">High-Pressure Crisis</button>
      <button class="filter-btn" onclick="filterCards('data')">Data Quality & Ops</button>
      <button class="filter-btn" onclick="filterCards('trade')">Global EXIM & Trade</button>
      <button class="filter-btn" onclick="filterCards('salary')">CTC & Value</button>
    </div>

    <!-- Card List -->
    <div class="card-list">

      <!-- Question 1 -->
      <div class="defense-card" data-category="tech">
        <div class="card-top">
          <div>
            <span class="category-badge purple">THE ACADEMIC BACKGROUND CURVEBALL</span>
            <div class="question-title">"You have a BBA in International Business, but this role works closely with data systems and engineers. Why shouldn't we hire a B.Tech graduate instead?"</div>
          </div>
          <button class="btn-copy" onclick="copyCard(this)">Copy STAR 📋</button>
        </div>

        <div class="hidden-test">
          Recruiter's Hidden Test: Are you intimidated by technology? Can you bridge commercial business logic with technical execution without getting bogged down in jargon?
        </div>

        <div class="star-grid">
          <div class="star-block">
            <div class="star-label">Situation</div>
            <div class="star-content">Throughout my International Business degree and internships, I observed that purely technical hires often build complex systems disconnected from gross margins, customer SLAs, or vendor contracts.</div>
          </div>
          <div class="star-block">
            <div class="star-label t">Task</div>
            <div class="star-content">I needed to prove that business professionals can build and operate technical workflows faster, cleaner, and with 100% commercial grounding.</div>
          </div>
          <div class="star-block">
            <div class="star-label a">Action</div>
            <div class="star-content">I built an autonomous operations platform prototype (github.com/AdityaMehra007/anti) in Python and SQLite with 16/16 unit tests passing green. Concurrently at Instawork, I audited precision AI/robotics data collections under strict millimeter tolerances.</div>
          </div>
          <div class="star-block">
            <div class="star-label r">Result</div>
            <div class="star-content">I bring the best of both worlds: fluent in Python, SQLite, and AI agent frameworks, while being natively trained in P&L, Incoterms, and vendor negotiation.</div>
          </div>
        </div>

        <div class="counter-question">
          <span class="counter-icon">⚡</span>
          <div class="counter-text">
            <strong>Power Counter-Question to Flip the Table:</strong> 
            "In your current operations sprint, is the primary friction point writing raw code, or translating ambiguous business requirements into flawless operational execution?"
          </div>
        </div>
      </div>

      <!-- Question 2 -->
      <div class="defense-card" data-category="crisis">
        <div class="card-top">
          <div>
            <span class="category-badge rose">HIGH-PRESSURE LOGISTICS CRISIS</span>
            <div class="question-title">"Tell me about a high-pressure situation where your operational plan failed, and how you handled it."</div>
          </div>
          <button class="btn-copy" onclick="copyCard(this)">Copy STAR 📋</button>
        </div>

        <div class="hidden-test">
          Recruiter's Hidden Test: Do you panic when systems crash? Can you think on your feet, improvise under pressure, and maintain financial and inventory integrity?
        </div>

        <div class="star-grid">
          <div class="star-block">
            <div class="star-label">Situation</div>
            <div class="star-content">During Aero India at Yelahanka Air Force Station, managing high-footfall field retail for artisanal brand 'Salt in My Cocoa' with hundreds of military and international delegates.</div>
          </div>
          <div class="star-block">
            <div class="star-label t">Task</div>
            <div class="star-content">On Day 2 peak afternoon, cellular network towers failed, instantly disabling all digital UPI machines while floor inventory hit zero amidst a 30-person queue.</div>
          </div>
          <div class="star-block">
            <div class="star-label a">Action</div>
            <div class="star-content">Immediately instituted a double-entry physical receipt ledger, established a designated phone-tethered hotspot for secondary validation, and executed an emergency cold-storage restocking run prioritizing top 3 fastest-moving SKUs.</div>
          </div>
          <div class="star-block">
            <div class="star-label r">Result</div>
            <div class="star-content">Cleared the queue in under 12 minutes with zero dropped sales. Closed the 5-day defense expo with 100% balance reconciliation between cash/UPI collected and inventory depleted.</div>
          </div>
        </div>

        <div class="counter-question">
          <span class="counter-icon">⚡</span>
          <div class="counter-text">
            <strong>Power Counter-Question to Flip the Table:</strong> 
            "What redundancy protocols does your team maintain when tier-1 infrastructure or cloud providers experience unexpected regional downtime?"
          </div>
        </div>
      </div>

      <!-- Question 3 -->
      <div class="defense-card" data-category="data">
        <div class="card-top">
          <div>
            <span class="category-badge emerald">DATA QUALITY & PRECISION AUDITS</span>
            <div class="question-title">"How do you ensure zero errors when managing large volumes of operational data and vendor contracts?"</div>
          </div>
          <button class="btn-copy" onclick="copyCard(this)">Copy STAR 📋</button>
        </div>

        <div class="hidden-test">
          Recruiter's Hidden Test: Do you cut corners when tired? Do you rely on casual assumptions, or do you have a systematic, deterministic verification methodology?
        </div>

        <div class="star-grid">
          <div class="star-block">
            <div class="star-label">Situation</div>
            <div class="star-content">At Instawork Services India and Pencil Mark Interior Solutions, tasked with verifying multi-parameter AI robotics dataset records and commercial vendor billing matrices.</div>
          </div>
          <div class="star-block">
            <div class="star-label t">Task</div>
            <div class="star-content">Prevent faulty data points from corrupting machine learning pipelines and eliminate cost variances in contractor invoices before site execution.</div>
          </div>
          <div class="star-block">
            <div class="star-label a">Action</div>
            <div class="star-content">Implemented deterministic 3-tier validation checklists: input type constraints, range boundary checks, and cross-reference reconciliation against source purchase orders in Excel.</div>
          </div>
          <div class="star-block">
            <div class="star-label r">Result</div>
            <div class="star-content">Achieved a 99.2% verified accuracy rate at Instawork and flagged 14 critical vendor billing anomalies at Pencil Mark, saving capital and avoiding site delays.</div>
          </div>
        </div>

        <div class="counter-question">
          <span class="counter-icon">⚡</span>
          <div class="counter-text">
            <strong>Power Counter-Question to Flip the Table:</strong> 
            "What automated quality gates does your operations team currently enforce before ingestion into production databases?"
          </div>
        </div>
      </div>

      <!-- Question 4 -->
      <div class="defense-card" data-category="trade">
        <div class="card-top">
          <div>
            <span class="category-badge">CROSS-BORDER EXIM & TRADE LOGISTICS</span>
            <div class="question-title">"How would you manage supply chain and cost exposure when maritime shipping lanes are disrupted?"</div>
          </div>
          <button class="btn-copy" onclick="copyCard(this)">Copy STAR 📋</button>
        </div>

        <div class="hidden-test">
          Recruiter's Hidden Test: Do you truly understand international business, Incoterms, and freight economics, or did you just memorize textbooks?
        </div>

        <div class="star-grid">
          <div class="star-block">
            <div class="star-label">Situation</div>
            <div class="star-content">Global maritime bottlenecks (such as the Red Sea / Cape of Good Hope reroutings) adding 14-21 transit days and skyrocketing freight surcharges.</div>
          </div>
          <div class="star-block">
            <div class="star-label t">Task</div>
            <div class="star-content">Protect the buyer's landing cost, minimize demurrage risk at arrival ports, and ensure factory production schedules remain unblocked.</div>
          </div>
          <div class="star-block">
            <div class="star-label a">Action</div>
            <div class="star-content">Analyze Incoterms 2020 transfer of risk (FOB vs CIF vs DAP), request expedited amendment of ocean bills of lading, and model split-shipment air-sea multimodal solutions for critical-path SKUs.</div>
          </div>
          <div class="star-block">
            <div class="star-label r">Result</div>
            <div class="star-content">Prevented production line starvation, capped detention penalties, and preserved commercial contract margins.</div>
          </div>
        </div>

        <div class="counter-question">
          <span class="counter-icon">⚡</span>
          <div class="counter-text">
            <strong>Power Counter-Question to Flip the Table:</strong> 
            "How has your organization adjusted its freight procurement strategy to hedge against carrier blank sailings and canal surcharges this quarter?"
          </div>
        </div>
      </div>

      <!-- Question 5 -->
      <div class="defense-card" data-category="salary">
        <div class="card-top">
          <div>
            <span class="category-badge amber">COMPENSATION & IMMEDIATE VALUE</span>
            <div class="question-title">"Your expected compensation is in the top bracket for a fresher. Why should we invest ₹12.5 - 18 LPA in you?"</div>
          </div>
          <button class="btn-copy" onclick="copyCard(this)">Copy STAR 📋</button>
        </div>

        <div class="hidden-test">
          Recruiter's Hidden Test: Can you articulate ROI? Do you understand what you cost versus what value you produce for the department?
        </div>

        <div class="star-grid">
          <div class="star-block">
            <div class="star-label">Situation</div>
            <div class="star-content">Most fresh graduates require 3 to 6 months of basic orientation before contributing net positive output to the team.</div>
          </div>
          <div class="star-block">
            <div class="star-label t">Task</div>
            <div class="star-content">Deliver immediate, Day-1 operational velocity that offsets the compensation investment within the first 60 days.</div>
          </div>
          <div class="star-block">
            <div class="star-label a">Action</div>
            <div class="star-content">I come with 3 completed internships, real high-stress event logistics experience, immediate working proficiency in Python/SQLite automation, and immediate joining readiness with zero notice period.</div>
          </div>
          <div class="star-block">
            <div class="star-label r">Result</div>
            <div class="star-content">I immediately relieve your senior managers of manual operational bottlenecks, automate repetitive tracking sheets, and deliver measurable SLA improvements from Week 1.</div>
          </div>
        </div>

        <div class="counter-question">
          <span class="counter-icon">⚡</span>
          <div class="counter-text">
            <strong>Power Counter-Question to Flip the Table:</strong> 
            "What are the top 2 operational bottlenecks currently consuming your team's bandwidth that you would like me to eliminate within my first 30 days?"
          </div>
        </div>
      </div>

    </div>

  </main>

  <script>
    function filterCards(category) {
      const buttons = document.querySelectorAll('.filter-btn');
      buttons.forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');

      const cards = document.querySelectorAll('.defense-card');
      cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function copyCard(btn) {
      const card = btn.closest('.defense-card');
      const text = card.innerText;
      navigator.clipboard.writeText(text);
      btn.innerText = 'Copied! ✓';
      setTimeout(() => { btn.innerText = 'Copy STAR 📋'; }, 2000);
    }
  </script>

</body>
</html>
'''

    out_file_1 = 'e:/anti/apps/job_application_studio/star_interview_defense_matrix.html'
    out_file_2 = 'e:/anti/STAR_INTERVIEW_DEFENSE_MATRIX.html'

    with open(out_file_1, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(out_file_2, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated STAR Interview Defense Matrix at {out_file_1} and {out_file_2}")

if __name__ == '__main__':
    build_defense_matrix()
