import os

def build_tycoon_os():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADITYA MEHRA | JOB TYCOON EMPIRE OS — Career Capital & Multi-Offer Command Center</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #03050c;
      --bg-surface: #070b16;
      --bg-card: #0d1222;
      --bg-card-hover: #141c33;
      --border: #1a233a;
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.25);
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.25);
      --emerald: #10b981;
      --purple: #8b5cf6;
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
      line-height: 1.5;
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Glow */
    .glow-gold {
      position: fixed;
      top: -200px;
      right: -200px;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.08) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }
    .glow-cyan {
      position: fixed;
      bottom: -200px;
      left: -200px;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(0, 242, 254, 0.08) 0%, transparent 70%);
      z-index: 0;
      pointer-events: none;
    }

    /* Top Nav */
    nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(3, 5, 12, 0.9);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 16px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .brand {
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand span { color: var(--gold); }

    .badge-tycoon {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--gold);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .badge-tycoon::before {
      content: '👑';
      font-size: 11px;
    }

    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 30px 40px 0;
      position: relative;
      z-index: 1;
    }

    /* Tycoon Hero Header */
    .tycoon-banner {
      background: linear-gradient(135deg, rgba(20, 28, 48, 0.95), rgba(10, 15, 28, 0.95));
      border: 1px solid var(--gold-glow);
      border-radius: 18px;
      padding: 36px 40px;
      margin-bottom: 36px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 28px;
    }}

    .tycoon-info h1 {
      font-size: 38px;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 8px;
      background: linear-gradient(135deg, #ffffff 0%, #fde68a 50%, #f59e0b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .tycoon-info p {
      font-size: 15px;
      color: var(--text-muted);
      max-width: 780px;
    }

    .tycoon-kpis {
      display: flex;
      gap: 18px;
      flex-wrap: wrap;
    }
    .kpi-tile {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 22px;
      min-width: 150px;
      text-align: center;
    }
    .kpi-num {
      font-size: 28px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--gold);
    }
    .kpi-num.cyan { color: var(--cyan); }
    .kpi-num.emerald { color: var(--emerald); }
    .kpi-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-sub);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Section Headers */
    .sec-head {
      margin: 40px 0 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .sec-head h2 {
      font-size: 24px;
      font-weight: 800;
      color: #fff;
    }
    .sec-head p {
      font-size: 13px;
      color: var(--text-muted);
    }

    /* 3 Pillars Grid */
    .pillars-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .pillar-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 28px;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }
    .pillar-card:hover {
      border-color: var(--gold);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px var(--gold-glow);
    }
    .pillar-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--gold);
    }
    .pillar-card.cyan::before { background: var(--cyan); }
    .pillar-card.emerald::before { background: var(--emerald); }

    .pillar-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--gold);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }
    .pillar-card.cyan .pillar-tag { color: var(--cyan); }
    .pillar-card.emerald .pillar-tag { color: var(--emerald); }

    .pillar-title {
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }
    .pillar-income {
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      color: var(--emerald);
      margin-bottom: 12px;
    }
    .pillar-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 16px;
    }

    .pillar-actions {
      list-style: none;
    }
    .pillar-actions li {
      font-size: 12px;
      color: #cbd5e1;
      margin-bottom: 6px;
      padding-left: 16px;
      position: relative;
    }
    .pillar-actions li::before {
      content: '✔';
      position: absolute;
      left: 0;
      color: var(--emerald);
      font-size: 10px;
    }

    /* Bidding War Simulator */
    .bidding-simulator {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 50px;
    }
    .auction-table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 13px;
    }
    .auction-table th {
      background: var(--bg-card);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 12px 16px;
      text-transform: uppercase;
    }
    .auction-table td {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }
    .auction-table tr:hover td {
      background: var(--bg-card-hover);
    }

    .btn-counter {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--gold);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .btn-counter:hover {
      background: var(--gold);
      color: #03050c;
    }

    /* 5-Year Net Worth Ladder */
    .ladder-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 40px;
    }
    .ladder-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      position: relative;
      transition: all 0.2s ease;
    }
    .ladder-card:hover {
      border-color: var(--cyan);
      transform: translateY(-2px);
    }
    .ladder-yr {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--cyan);
      margin-bottom: 6px;
    }
    .ladder-title {
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }
    .ladder-comp {
      font-family: var(--font-mono);
      font-size: 18px;
      font-weight: 800;
      color: var(--gold);
      margin-bottom: 10px;
    }
    .ladder-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* Modal for Counter-Offer Pitch */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      z-index: 200;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }
    .modal-box {
      background: var(--bg-surface);
      border: 1px solid var(--gold-glow);
      border-radius: 14px;
      width: 100%;
      max-width: 800px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 30px;
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 16px;
      right: 18px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
    }
    .modal-pre {
      background: #020409;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: #cbd5e1;
      white-space: pre-wrap;
      line-height: 1.6;
      margin-top: 14px;
    }

    footer {
      border-top: 1px solid var(--border);
      padding-top: 30px;
      text-align: center;
      color: var(--text-sub);
      font-size: 13px;
      font-family: var(--font-mono);
      margin-top: 60px;
    }
  </style>
</head>
<body>

  <div class="glow-gold"></div>
  <div class="glow-cyan"></div>

  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ JOB TYCOON EMPIRE OS</span>
      <div class="badge-tycoon">Bidding War Engine Active</div>
    </div>
    <div style="display: flex; gap: 10px;">
      <a href="ADITYA_CAREER_CONQUEST_MISSION_CONTROL.html" style="color: var(--text-muted); text-decoration: none; font-size: 13px; border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px;">Mission Control ↗</a>
      <a href="ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html" style="color: var(--text-muted); text-decoration: none; font-size: 13px; border: 1px solid var(--border); padding: 6px 12px; border-radius: 6px;">Portfolio ↗</a>
    </div>
  </nav>

  <main class="container">

    <!-- Hero Tycoon Banner -->
    <div class="tycoon-banner">
      <div class="tycoon-info">
        <h1>The Sovereign Career & Wealth Tycoon OS</h1>
        <p>
          Transforming from an applicant asking for a job into an enterprise operator who commands multiple concurrent offer streams, 
          advisory retainers, and asymmetric compensation leverage across Bengaluru and global markets.
        </p>
      </div>
      <div class="tycoon-kpis">
        <div class="kpi-tile">
          <div class="kpi-num">₹1.85 Cr</div>
          <div class="kpi-label">Pipeline Deal Value</div>
        </div>
        <div class="kpi-tile">
          <div class="kpi-num cyan">₹18.0L</div>
          <div class="kpi-label">Anchor Base Target</div>
        </div>
        <div class="kpi-tile">
          <div class="kpi-num emerald">3</div>
          <div class="kpi-label">Wealth Streams</div>
        </div>
      </div>
    </div>

    <!-- Section 1: The 3 Wealth Streams -->
    <div class="sec-head">
      <div>
        <h2>The 3 Wealth Streams of a Career Tycoon</h2>
        <p>Never depend on a single salary: diversify operational income, advisory retainers, and equity upside</p>
      </div>
    </div>

    <div class="pillars-grid">
      <!-- Pillar 1 -->
      <div class="pillar-card">
        <div class="pillar-tag">Stream 01 • The Cashflow Foundation</div>
        <div class="pillar-title">Tier-1 Corporate Anchor Role</div>
        <div class="pillar-income">₹14.0L – ₹22.0L Annual Base CTC</div>
        <p class="pillar-desc">
          High-prestige GCC or Unicorn anchor position (Maersk, Boeing, Target, Goldman Sachs, Zepto) providing steady liquidity, corporate health insurance, and executive brand equity.
        </p>
        <ul class="pillar-actions">
          <li>Full-time Bengaluru on-site presence (ORR / Manyata / Whitefield).</li>
          <li>Acts as primary credit and proof-of-work credibility engine.</li>
          <li>Provides enterprise network with VPs, Directors, and Global Partners.</li>
        </ul>
      </div>

      <!-- Pillar 2 -->
      <div class="pillar-card cyan">
        <div class="pillar-tag">Stream 02 • High-Ticket Advisory</div>
        <div class="pillar-title">Cross-Border EXIM & Trade Advisory</div>
        <div class="pillar-income">₹50,000 – ₹1,50,000 / Month Retainers</div>
        <p class="pillar-desc">
          Off-hours advisory for emerging SMB exporters and family offices navigating Incoterms 2020 risk transfer, ICEGATE customs queries, and duty drawback recoveries.
        </p>
        <ul class="pillar-actions">
          <li>Audits HS Code classifications to legally lower import duty.</li>
          <li>Structures Free Trade Agreement (CEPA / ECTA) certificate filings.</li>
          <li>Assists family enterprises with inventory and freight reconciliations.</li>
        </ul>
      </div>

      <!-- Pillar 3 -->
      <div class="pillar-card emerald">
        <div class="pillar-tag">Stream 03 • Digital Equity & Micro-SaaS</div>
        <div class="pillar-title">Autonomous AI Operations Tooling</div>
        <div class="pillar-income">₹30,000 – ₹1,00,000 / Month Passive / Advisory</div>
        <p class="pillar-desc">
          Monetizing your verified Python/SQLite operations and recruiter dispatch codebase (anti repository) as automated operational tools for boutique recruitment agencies and founders.
        </p>
        <ul class="pillar-actions">
          <li>Custom automated lead extraction and outreach engines.</li>
          <li>SOP checklists and deterministic data validation pipelines.</li>
          <li>Consulting for non-tech founders on implementing Google Antigravity & AI agents.</li>
        </ul>
      </div>
    </div>

    <!-- Section 2: Multi-Offer Auction Simulator -->
    <div class="bidding-simulator">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 800; color: #fff;">Simultaneous Multi-Offer Auction Simulator</h2>
          <p style="font-size: 13px; color: var(--text-muted);">How a career tycoon turns 3 competing offers into a bidding escalation</p>
        </div>
      </div>

      <table class="auction-table">
        <thead>
          <tr>
            <th>Company</th>
            <th>Role Title</th>
            <th>Initial Offer</th>
            <th>Target Counter</th>
            <th>Bidding Leverage</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="font-weight: 700; color: #fff;">A.P. Moller - Maersk</td>
            <td style="color: var(--cyan);">Global EXIM Operations Specialist</td>
            <td style="font-family: var(--font-mono); color: var(--gold);">₹10.5 LPA</td>
            <td style="font-family: var(--font-mono); color: var(--emerald); font-weight: 700;">₹14.0 LPA</td>
            <td>Leverage Goldman Sachs & Boeing offers</td>
            <td><button class="btn-counter" onclick="openCounterPitch('Maersk', '₹10.5 LPA', '₹14.0 LPA', 'Goldman Sachs')">Generate Counter ✉</button></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">Boeing India (BIETC)</td>
            <td style="color: var(--cyan);">Corporate Operations & SCM Trainee</td>
            <td style="font-family: var(--font-mono); color: var(--gold);">₹12.0 LPA</td>
            <td style="font-family: var(--font-mono); color: var(--emerald); font-weight: 700;">₹16.5 LPA</td>
            <td>Leverage Zepto Founder's Office offer</td>
            <td><button class="btn-counter" onclick="openCounterPitch('Boeing India', '₹12.0 LPA', '₹16.5 LPA', 'Zepto')">Generate Counter ✉</button></td>
          </tr>
          <tr>
            <td style="font-weight: 700; color: #fff;">Zepto / Swiggy</td>
            <td style="color: var(--cyan);">Founder's Office & BizOps Associate</td>
            <td style="font-family: var(--font-mono); color: var(--gold);">₹14.0 LPA</td>
            <td style="font-family: var(--font-mono); color: var(--emerald); font-weight: 700;">₹19.5 LPA</td>
            <td>Leverage competing Unicorn & GCC bids</td>
            <td><button class="btn-counter" onclick="openCounterPitch('Zepto', '₹14.0 LPA', '₹19.5 LPA', 'Tier-1 GCC')">Generate Counter ✉</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Section 3: 5-Year Net Worth Trajectory -->
    <div class="sec-head">
      <div>
        <h2>The 5-Year Career Net Worth Trajectory Ladder</h2>
        <p>The mathematical progression of aggressive strategic jumps and multi-stream compounding</p>
      </div>
    </div>

    <div class="ladder-grid">
      <div class="ladder-card">
        <div class="ladder-yr">YEAR 01 (2026)</div>
        <div class="ladder-title">The Hyper-Operator</div>
        <div class="ladder-comp">₹14L – ₹18L</div>
        <p class="ladder-desc">Land Tier-1 GCC / BizOps anchor. Master internal ERP and automate team reporting using Python/SQLite. Immediate net positive contributor.</p>
      </div>

      <div class="ladder-card">
        <div class="ladder-yr">YEAR 02 (2027)</div>
        <div class="ladder-title">The Lateral Jump</div>
        <div class="ladder-comp">₹24L – ₹30L</div>
        <p class="ladder-desc">Execute first 45% lateral jump to competing MNC or high-growth Series C scaleup. Launch first trade advisory retainer.</p>
      </div>

      <div class="ladder-card">
        <div class="ladder-yr">YEAR 03 (2028)</div>
        <div class="ladder-title">Operations Team Lead</div>
        <div class="ladder-comp">₹38L – ₹48L</div>
        <p class="ladder-desc">Manage a 6-person operations pod. Oversee multi-million dollar cross-border shipments and enterprise vendor contracts.</p>
      </div>

      <div class="ladder-card">
        <div class="ladder-yr">YEAR 05 (2030)</div>
        <div class="ladder-title">Director / VP of Ops</div>
        <div class="ladder-comp">₹85L – ₹1.2 Cr+</div>
        <p class="ladder-desc">Lead global capability center division. Command substantial equity carry, global travel, and board advisory roles.</p>
      </div>
    </div>

  </main>

  <!-- Counter Offer Modal -->
  <div class="modal-overlay" id="counterModal" onclick="if(event.target === this) closeModal()">
    <div class="modal-box">
      <button class="modal-close" onclick="closeModal()">✕</button>
      <h3 style="font-size: 18px; font-weight: 700; color: #fff;" id="modalCompany">Counter-Offer Negotiation Pitch</h3>
      <div class="modal-pre" id="modalText">Loading...</div>
      <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
        <button class="btn-counter" onclick="navigator.clipboard.writeText(document.getElementById('modalText').innerText); alert('Counter-offer script copied to clipboard!');">Copy Script 📋</button>
      </div>
    </div>
  </div>

  <footer>
    ADITYA MEHRA • JOB TYCOON EMPIRE OS • BBA INTERNATIONAL BUSINESS '26 • DAYANANDA SAGAR UNIVERSITY
    <br>POWERED BY OMEGA ∞ SUPREME AUTONOMOUS CAREER SUITE
  </footer>

  <script>
    function openCounterPitch(comp, initial, target, compAlt) {
      document.getElementById('modalCompany').innerText = `Executive Bidding Counter: ${comp}`;
      const script = `Subject: Aditya Mehra — Appreciation of Offer & Compensation Scope (${comp})

Dear Talent Acquisition Lead,

Thank you sincerely for extending the formal offer for the operations role at ${comp}. I have thoroughly enjoyed our conversations with the leadership team, and ${comp} remains my top personal preference because of your operational excellence and global scale.

As we finalize the agreement, I wanted to discuss the base compensation structure. I am currently in advanced decision-stage discussions with another organization (${compAlt}) that has put forward an offer structured at ${target}.

Because ${comp} is my unambiguous first choice, if we can align the total compensation closer to ${target} (or bridge the difference via a joining/sign-on bonus), I am prepared to sign the acceptance immediately today, conclude all other discussions, and lock in my Day-1 start date.

I am deeply excited about contributing to your team's upcoming sprint deliverables and look forward to your thoughts.

Warm regards,
Aditya Mehra
Bengaluru, India | +91 7003456624 | adityamehra799@gmail.com`;

      document.getElementById('modalText').innerText = script;
      document.getElementById('counterModal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('counterModal').style.display = 'none';
    }
  </script>

</body>
</html>
'''

    out_file = 'e:/anti/ADITYA_JOB_TYCOON_EMPIRE_OS.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Job Tycoon Empire OS at {out_file}")

if __name__ == '__main__':
    build_tycoon_os()
