import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path('e:/anti')
WAR_CHEST_DIR = ROOT / 'WAR_CHEST'
WAR_CHEST_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. BUILD THE EXECUTIVE ONE-PAGER (A4 Printable Presentation)
# -------------------------------------------------------------
def build_executive_one_pager():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aditya Mehra | Executive One-Pager (Operations & Global Trade)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 10mm 12mm 10mm 12mm;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      color: #0f172a;
      background: #f8fafc;
      padding: 20px;
      line-height: 1.4;
      -webkit-font-smoothing: antialiased;
    }
    @media print {
      body { background: #fff; padding: 0; }
      .no-print { display: none !important; }
    }
    .sheet {
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 28px 32px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    @media print {
      .sheet { border: none; box-shadow: none; padding: 0; max-width: 100%; border-radius: 0; }
    }
    /* Header */
    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 14px;
      margin-bottom: 16px;
    }
    .name-block h1 {
      font-size: 26px;
      font-weight: 900;
      color: #0f172a;
      letter-spacing: -0.02em;
      line-height: 1.1;
    }
    .name-block .tagline {
      font-size: 13px;
      font-weight: 700;
      color: #2563eb;
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .contact-block {
      text-align: right;
      font-size: 11px;
      color: #475569;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1.5;
    }
    .contact-block a { color: #2563eb; text-decoration: none; }

    /* Summary */
    .exec-summary {
      background: #f1f5f9;
      border-left: 3px solid #2563eb;
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-size: 12px;
      color: #334155;
      margin-bottom: 18px;
      line-height: 1.5;
    }

    /* Section Styling */
    .sec-title {
      font-size: 12px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* 4 Proof of Work Cards Grid */
    .pow-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 18px;
    }
    .pow-box {
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px 14px;
      background: #fff;
    }
    .pow-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 4px;
    }
    .pow-title {
      font-size: 12px;
      font-weight: 750;
      color: #0f172a;
    }
    .pow-metric {
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #059669;
      background: #ecfdf5;
      padding: 1px 6px;
      border-radius: 4px;
    }
    .pow-org {
      font-size: 11px;
      color: #2563eb;
      font-weight: 600;
      margin-bottom: 6px;
    }
    .pow-desc {
      font-size: 11px;
      color: #475569;
      line-height: 1.45;
    }

    /* Skills & Core Competencies 3 Column Grid */
    .skills-row {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }
    .skill-col {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 10px 12px;
    }
    .skill-col-title {
      font-size: 11px;
      font-weight: 800;
      color: #0f172a;
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    .skill-col ul {
      list-style: none;
      font-size: 11px;
      color: #334155;
    }
    .skill-col li {
      margin-bottom: 3px;
      padding-left: 10px;
      position: relative;
    }
    .skill-col li::before {
      content: '▪';
      position: absolute;
      left: 0;
      color: #2563eb;
      font-size: 10px;
    }

    /* Bottom Value Strip */
    .value-strip {
      background: #0f172a;
      color: #fff;
      border-radius: 6px;
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
    }
    .value-strip strong { color: #38bdf8; }

    /* Print Button */
    .print-btn-bar {
      max-width: 820px;
      margin: 0 auto 16px;
      display: flex;
      justify-content: flex-end;
      gap: 10px;
    }
    .btn {
      background: #0f172a;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .btn:hover { background: #1e293b; }
  </style>
</head>
<body>

  <div class="print-btn-bar no-print">
    <button class="btn" onclick="window.print()">🖨️ Print to A4 PDF</button>
  </div>

  <div class="sheet">
    <!-- Header -->
    <div class="top-bar">
      <div class="name-block">
        <h1>ADITYA MEHRA</h1>
        <div class="tagline">Operations Specialist • Global EXIM Logistics • Autonomous AI Systems</div>
      </div>
      <div class="contact-block">
        <div>Bengaluru, India</div>
        <div>+91 7003456624</div>
        <div><a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a></div>
        <div><a href="https://github.com/AdityaMehra007/anti">github.com/AdityaMehra007</a></div>
        <div style="color: #059669; font-weight: 700;">Immediate Joining Available</div>
      </div>
    </div>

    <!-- Executive Summary -->
    <div class="exec-summary">
      <strong>EXECUTIVE PROFILE:</strong> Final-year <strong>BBA International Business</strong> graduate from <strong>Dayananda Sagar University (DSU '26)</strong>. Combines ground-level operational discipline (high-footfall retail logistics at Aero India with 0.0% cash/UPI variance, commercial vendor procurement at Pencil Mark, robotics data quality QA at Instawork) with technical capability in Python, SQLite, and autonomous AI agent workflows. Seeking high-velocity entry-level Operations Trainee, Global EXIM Logistics, or BizOps Associate roles in Bengaluru.
    </div>

    <!-- Proof of Work Grid -->
    <div class="sec-title">
      <span>Verifiable Operational Proof of Work</span>
      <span style="font-size: 10px; color: #64748b; font-weight: 600;">Documented Field Outcomes</span>
    </div>

    <div class="pow-grid">
      <!-- 1 -->
      <div class="pow-box">
        <div class="pow-head">
          <div class="pow-title">Autonomous Operations & Recruiter Engine</div>
          <span class="pow-metric">16/16 Unit Tests Green</span>
        </div>
        <div class="pow-org">Google Antigravity • Python • SQLite • Agentic Workflows</div>
        <div class="pow-desc">
          Architected relational database prototype indexing 5,000+ employers, 7,500 HR leads, and automated InMail pitch synthesis with automated regression testing.
        </div>
      </div>

      <!-- 2 -->
      <div class="pow-box">
        <div class="pow-head">
          <div class="pow-title">AI & Robotics Data Quality Assurance</div>
          <span class="pow-metric">99.2% Accuracy SLA</span>
        </div>
        <div class="pow-org">Instawork Services India Pvt. Ltd. • Bengaluru (2025)</div>
        <div class="pow-desc">
          Executed precision validation audits across thousands of high-density AI robotics data records, identifying 14 critical edge-case data deviations before model ingestion.
        </div>
      </div>

      <!-- 3 -->
      <div class="pow-box">
        <div class="pow-head">
          <div class="pow-title">Aero India & Major Event Logistics</div>
          <span class="pow-metric">0.0% Financial Variance</span>
        </div>
        <div class="pow-org">Aero India (Yelahanka) • Salt in My Cocoa (2025)</div>
        <div class="pow-desc">
          Coordinated field retail booth operations under peak footfall; resolved mid-event payment machine outages via manual double-entry ledgers with zero dropped sales.
        </div>
      </div>

      <!-- 4 -->
      <div class="pow-box">
        <div class="pow-head">
          <div class="pow-title">Commercial Operations & Vendor Procurement</div>
          <span class="pow-metric">100% On-Time BOM</span>
        </div>
        <div class="pow-org">Pencil Mark Interior Solutions LLP • Bengaluru (2025)</div>
        <div class="pow-desc">
          Converted client specifications into vendor delivery schedules and Excel procurement matrices, resolving on-site material requisition variances.
        </div>
      </div>
    </div>

    <!-- Core Competencies Matrix -->
    <div class="sec-title">
      <span>Core Operational Capabilities</span>
    </div>

    <div class="skills-row">
      <div class="skill-col">
        <div class="skill-col-title">Global EXIM & Trade</div>
        <ul>
          <li>Incoterms 2020 Risk Transfer</li>
          <li>Ocean Bill of Lading & BoE</li>
          <li>Customs Clearance Workflows</li>
          <li>Demurrage & Detention Hedging</li>
          <li>CEPA / ECTA FTA Compliance</li>
        </ul>
      </div>

      <div class="skill-col">
        <div class="skill-col-title">Corporate Operations</div>
        <ul>
          <li>Vendor Matrix & SLA Audits</li>
          <li>Double-Entry Reconciliation</li>
          <li>High-Stress Crisis Triage</li>
          <li>Process Mapping & SOP Creation</li>
          <li>Commercial Brief Formulation</li>
        </ul>
      </div>

      <div class="skill-col">
        <div class="skill-col-title">Modern Tech & Tooling</div>
        <ul>
          <li>Python 3 Scripting & Automation</li>
          <li>SQLite Relational Database</li>
          <li>Google Antigravity & Agentic Ops</li>
          <li>MS Excel (Pivots, VLOOKUP)</li>
          <li>Git / GitHub Workflow & CLI</li>
        </ul>
      </div>
    </div>

    <!-- Education & Value Strip -->
    <div class="sec-title">
      <span>Education & Certifications</span>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 12px; color: #334155;">
      <div><strong>Dayananda Sagar University (DSU), Bengaluru</strong> — BBA (International Business)</div>
      <div style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">2023 – 2026 (Final Year)</div>
    </div>
    <div style="font-size: 11px; color: #64748b; margin-bottom: 16px;">
      Certifications: Google Digital Marketing Fundamentals • NPTEL Service Marketing • Languages: English (Fluent), Hindi (Native)
    </div>

    <div class="value-strip">
      <div><strong>DAY-1 PROMISE:</strong> Zero notice period • Self-directed backlog clearance • Auditable accuracy</div>
      <div style="font-family: 'JetBrains Mono', monospace;">+91 7003456624 | Bengaluru</div>
    </div>

  </div>

</body>
</html>
'''
    out_file = WAR_CHEST_DIR / 'ADITYA_EXECUTIVE_ONE_PAGER.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(ROOT / 'ADITYA_EXECUTIVE_ONE_PAGER.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Executive One-Pager at {out_file}")

# -------------------------------------------------------------
# 2. BUILD THE 30-60-90 DAY EXECUTIVE OPERATIONAL BLUEPRINT
# -------------------------------------------------------------
def build_30_60_90_blueprint():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aditya Mehra | 30-60-90 Day Executive Operational Onboarding Blueprint</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    @page { size: A4 portrait; margin: 12mm 14mm; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #060913;
      color: #f8fafc;
      font-family: 'Plus Jakarta Sans', sans-serif;
      padding: 30px;
      line-height: 1.5;
    }
    @media print {
      body { background: #fff; color: #0f172a; padding: 0; }
      .no-print { display: none !important; }
      .sheet { border: none !important; box-shadow: none !important; }
      .phase-card { background: #f8fafc !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; }
      .phase-title { color: #0f172a !important; }
      .phase-desc { color: #334155 !important; }
      .kpi-box { background: #f1f5f9 !important; border: 1px solid #cbd5e1 !important; color: #0f172a !important; }
    }
    .sheet {
      max-width: 900px;
      margin: 0 auto;
      background: #0a0f1e;
      border: 1px solid #1e293b;
      border-radius: 14px;
      padding: 36px 40px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    .header-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }
    .eyebrow {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #00f2fe;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    h1 {
      font-size: 28px;
      font-weight: 800;
      color: #fff;
      line-height: 1.2;
    }
    .subhead {
      font-size: 13px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .contact-info {
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #94a3b8;
    }

    .phases-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .phase-card {
      background: #0f1629;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 22px 26px;
      position: relative;
    }
    .phase-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 8px;
    }
    .phase-badge.p1 { background: rgba(0, 242, 254, 0.15); color: #00f2fe; }
    .phase-badge.p2 { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .phase-badge.p3 { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }

    .phase-title {
      font-size: 17px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }
    .phase-desc {
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.5;
      margin-bottom: 12px;
    }
    .deliverables-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      font-size: 12px;
    }
    .deliv-item {
      padding-left: 14px;
      position: relative;
      color: #94a3b8;
    }
    .deliv-item::before {
      content: '▹';
      position: absolute;
      left: 0;
      color: #00f2fe;
    }

    .kpi-strip {
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px dashed #1e293b;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      color: #10b981;
    }

    .print-bar {
      max-width: 900px;
      margin: 0 auto 16px;
      display: flex;
      justify-content: flex-end;
    }
    .btn {
      background: #00f2fe;
      color: #050811;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <div class="print-bar no-print">
    <button class="btn" onclick="window.print()">🖨️ Print Blueprint to PDF</button>
  </div>

  <div class="sheet">
    <div class="header-row">
      <div>
        <div class="eyebrow">EXECUTIVE ONBOARDING ROADMAP • 90-DAY DELIVERABLE MATRIX</div>
        <h1>Aditya Mehra: 30-60-90 Day Operational Plan</h1>
        <div class="subhead">Framework for Immediate Net Positive Operational ROI • Corporate Operations & EXIM</div>
      </div>
      <div class="contact-info">
        <div>Aditya Mehra</div>
        <div>+91 7003456624</div>
        <div>adityamehra799@gmail.com</div>
        <div>Dayananda Sagar University '26</div>
      </div>
    </div>

    <div class="phases-list">
      <!-- Days 1-30 -->
      <div class="phase-card">
        <span class="phase-badge p1">DAYS 01 – 30 • THE INGESTION & AUDIT PHASE</span>
        <div class="phase-title">Objective: Master Internal Workflows, Map Bottlenecks & Achieve Flawless Baseline Execution</div>
        <div class="phase-desc">
          Absorb institutional knowledge without disrupting active delivery pipelines. Shadow senior operations leads, audit vendor SLAs, and document every upstream and downstream data dependency.
        </div>
        <div class="deliverables-grid">
          <div class="deliv-item">Map 100% of vendor matrices, freight forwarder contacts, and internal ERP login flows.</div>
          <div class="deliv-item">Audit historical reconciliation reports to identify recurring variance causes.</div>
          <div class="deliv-item">Execute daily administrative and scheduling tasks with zero-defect accuracy.</div>
          <div class="deliv-item">Conduct 15-minute alignment syncs with sibling finance and supply chain pods.</div>
        </div>
        <div class="kpi-strip">
          <span>Target Metric: 0 Delinquent Tasks</span>
          <span>SLA Adherence: 100%</span>
          <span>Zero Escaped Errors</span>
        </div>
      </div>

      <!-- Days 31-60 -->
      <div class="phase-card">
        <span class="phase-badge p2">DAYS 31 – 60 • THE PROCESS AUTOMATION PHASE</span>
        <div class="phase-title">Objective: Eliminate Managerial Drag & Automate Repetitive Tracking Spreadsheets</div>
        <div class="phase-desc">
          Identify the single most time-consuming manual data entry or reconciliation task in the team. Deploy lightweight Python/SQLite or advanced Excel PowerQuery models to compress reporting latency by 40%+.
        </div>
        <div class="deliverables-grid">
          <div class="deliv-item">Deliver the weekly operational status deck 24 hours prior to executive deadline.</div>
          <div class="deliv-item">Standardize automated validation checks for vendor invoicing and container manifests.</div>
          <div class="deliv-item">Draft formal Standard Operating Procedures (SOPs) for newly optimized flows.</div>
          <div class="deliv-item">Take ownership of mid-tier supplier escalations and resolution tracking.</div>
        </div>
        <div class="kpi-strip">
          <span>Reporting Latency: -40%</span>
          <span>Managerial Bandwidth Freed: 5 hrs/wk</span>
          <span>Documented SOPs: 3 Shipped</span>
        </div>
      </div>

      <!-- Days 61-90 -->
      <div class="phase-card">
        <span class="phase-badge p3">DAYS 61 – 90 • THE INDISPENSABLE SCALE PHASE</span>
        <div class="phase-title">Objective: Drive Measurable Gross Margin Improvements & Cross-Functional Scale</div>
        <div class="phase-desc">
          Operate with complete self-sufficiency. Present a 90-day executive performance review to directors, highlighting audit compliance, capital protected from demurrage/variance, and playbook readiness.
        </div>
        <div class="deliverables-grid">
          <div class="deliv-item">Execute full audit of Free Trade Agreement (CEPA) duty savings across active imports.</div>
          <div class="deliv-item">Present comprehensive Q1 operational review to Director of Operations.</div>
          <div class="deliv-item">Train incoming interns or junior contractors on standardized team checklists.</div>
          <div class="deliv-item">Formally establish 6-month growth objectives and KPI milestone agreements.</div>
        </div>
        <div class="kpi-strip">
          <span>Net Positive Operational Contribution: Verified</span>
          <span>Audit Compliance: 99.8%</span>
          <span>Promotion Fast-Track Locked</span>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
'''
    out_file = WAR_CHEST_DIR / 'ADITYA_30_60_90_DAY_BLUEPRINT.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(ROOT / 'ADITYA_30_60_90_DAY_BLUEPRINT.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated 30-60-90 Day Blueprint at {out_file}")

# -------------------------------------------------------------
# 3. BUILD THE SMARTPHONE BATTLE SHIELD (Mobile Offline App)
# -------------------------------------------------------------
def build_mobile_battle_shield():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>BATTLE SHIELD | Aditya Mehra Mobile Pocket Weapon</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #03050c;
      --card: #0a0f1d;
      --card-inner: #10172b;
      --border: #1a253d;
      --cyan: #00f2fe;
      --gold: #f59e0b;
      --emerald: #10b981;
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      padding: 16px 14px 80px;
      line-height: 1.45;
    }

    .top-header {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand { font-size: 15px; font-weight: 800; }
    .brand span { color: var(--cyan); }
    .status-dot {
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid var(--emerald);
      color: var(--emerald);
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }

    /* Section Tabs */
    .tab-pills {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 14px;
    }
    .pill {
      background: var(--card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
      cursor: pointer;
    }
    .pill.active {
      background: rgba(0, 242, 254, 0.15);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    /* Accordion Cards */
    .card-list { display: flex; flex-direction: column; gap: 10px; }
    .battle-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      transition: all 0.2s ease;
    }
    .card-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: var(--gold);
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .card-question {
      font-size: 14px;
      font-weight: 750;
      color: #fff;
      margin-bottom: 8px;
    }
    .card-body {
      background: var(--card-inner);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.5;
      margin-bottom: 8px;
    }
    .card-body strong { color: var(--cyan); }
    .flip-box {
      font-size: 11px;
      color: var(--gold);
      background: rgba(245, 158, 11, 0.08);
      border-left: 2px solid var(--gold);
      padding: 6px 10px;
      border-radius: 0 6px 6px 0;
    }

    /* Copy Button */
    .copy-btn {
      width: 100%;
      background: var(--card-inner);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px;
      border-radius: 6px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
      margin-top: 6px;
      text-align: center;
    }
    .copy-btn:active { background: var(--cyan); color: #000; }

    /* Sticky Bottom Quick Bar */
    .bottom-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      background: rgba(10, 15, 29, 0.95);
      backdrop-filter: blur(12px);
      border-top: 1px solid var(--border);
      padding: 10px 14px;
      display: flex;
      gap: 8px;
    }
    .btn-action {
      flex: 1;
      padding: 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
    }
    .btn-pri { background: var(--cyan); color: #050811; }
    .btn-sec { background: var(--card); border: 1px solid var(--border); color: #fff; }
  </style>
</head>
<body>

  <div class="top-header">
    <div class="brand">BATTLE SHIELD <span>/ ADITYA</span></div>
    <div class="status-dot">OFFLINE WEAPON ACTIVE</div>
  </div>

  <div class="tab-pills">
    <div class="pill active" onclick="showTab('pitch')">60s Pitch</div>
    <div class="pill" onclick="showTab('curveball')">5 Curveballs</div>
    <div class="pill" onclick="showTab('flips')">3 Counter Flips</div>
    <div class="pill" onclick="showTab('salary')">Salary Script</div>
  </div>

  <!-- Tab 1: 60s Elevator Pitch -->
  <div id="tab-pitch" class="card-list">
    <div class="battle-card">
      <div class="card-tag">MEMORIZE & RECITE IN 60 SECONDS</div>
      <div class="card-question">"Tell me about yourself."</div>
      <div class="card-body" id="pitch-text">
        "I am a final-year BBA International Business graduate from Dayananda Sagar University, Bengaluru. Over the past 3 years, I’ve grounded my business education in high-pressure operations: coordinating field retail logistics at Aero India with zero financial discrepancy, managing commercial vendor matrices at Pencil Mark, and executing AI robotics data quality audits at Instawork with a 99.2% accuracy benchmark.<br><br>
        On the technical side, I build autonomous workflow engines in Python and SQLite—including my 'anti' operations platform with 16 verified unit tests passing green. I bridge commercial trade logic with modern automation, and I am available to join immediately in Bengaluru with zero notice period."
      </div>
      <button class="copy-btn" onclick="copySnippet('pitch-text')">Copy 60s Pitch 📋</button>
    </div>
  </div>

  <!-- Tab 2: 5 Curveball Shields -->
  <div id="tab-curveball" class="card-list" style="display: none;">
    <!-- Q1 -->
    <div class="battle-card">
      <div class="card-tag">CURVEBALL 01 • BBA VS ENGINEERING</div>
      <div class="card-question">"Why hire a BBA instead of a software engineer?"</div>
      <div class="card-body">
        <strong>SHIELD:</strong> "Engineers often focus purely on technical architecture without understanding commercial trade margins or vendor contracts. I built my autonomous operations platform in Python/SQLite with 16 green tests, but I speak the language of profit and loss, Incoterms, and SLA delivery. I bridge business and tech without engineering friction."
      </div>
      <div class="flip-box">FLIP: "In your team, is the biggest drag writing raw code or translating business needs into operational execution?"</div>
    </div>

    <!-- Q2 -->
    <div class="battle-card">
      <div class="card-tag">CURVEBALL 02 • CRISIS MANAGEMENT</div>
      <div class="card-question">"Tell me about a time your plan failed."</div>
      <div class="card-body">
        <strong>SHIELD:</strong> "At Aero India, our digital UPI machines went down during peak afternoon footfall while inventory hit zero. I immediately instituted a double-entry physical receipt ledger, established a cellular hotspot redundancy, and ran an emergency cold-storage run for our top 3 SKUs. Cleared a 30-person queue in 12 minutes with 0.0% cash discrepancy over 5 days."
      </div>
    </div>

    <!-- Q3 -->
    <div class="battle-card">
      <div class="card-tag">CURVEBALL 03 • DATA INTEGRITY</div>
      <div class="card-question">"How do you ensure zero errors in data?"</div>
      <div class="card-body">
        <strong>SHIELD:</strong> "At Instawork, I audited AI robotics data points against strict millimeter tolerances. I used a 3-tier validation checklist: input type constraints, range boundary checks, and cross-reference reconciliation. Achieved a 99.2% accuracy score and caught 14 critical edge-case flaws before model training."
      </div>
    </div>
  </div>

  <!-- Tab 3: Counter Flips -->
  <div id="tab-flips" class="card-list" style="display: none;">
    <div class="battle-card">
      <div class="card-tag">COUNTER QUESTION 01 • THE BOTTLENECK DIAGNOSTIC</div>
      <div class="card-question">Ask the Director of Operations:</div>
      <div class="card-body">
        "What are the top 2 operational bottlenecks currently consuming your team's bandwidth that you would like me to eliminate within my first 30 days?"
      </div>
    </div>

    <div class="battle-card">
      <div class="card-tag">COUNTER QUESTION 02 • INFRASTRUCTURE REDUNDANCY</div>
      <div class="card-question">Ask the Supply Chain Lead:</div>
      <div class="card-body">
        "How has your team adjusted its freight procurement strategy to hedge against carrier blank sailings and Red Sea rerouting surcharges this quarter?"
      </div>
    </div>
  </div>

  <!-- Tab 4: Salary Script -->
  <div id="tab-salary" class="card-list" style="display: none;">
    <div class="battle-card">
      <div class="card-tag">SALARY SCRIPT • ANCHOR & DEFLECT</div>
      <div class="card-question">When asked: "What is your CTC expectation?"</div>
      <div class="card-body" id="sal-text">
        "Based on current Bengaluru GCC compensation benchmarks for operations analysts and my hands-on background in event logistics reconciliations and automated data pipeline development, I am targeting an overall compensation package in the <strong>₹12.5L to ₹16.0L bracket</strong>. That said, finding the right operational fit where I can immediately unblock backlog tickets on Day 1 is my top priority. What is the approved budget range for this role?"
      </div>
      <button class="copy-btn" onclick="copySnippet('sal-text')">Copy Salary Script 📋</button>
    </div>
  </div>

  <!-- Sticky Bottom Bar -->
  <div class="bottom-bar">
    <a href="ADITYA_EXECUTIVE_ONE_PAGER.html" class="btn-action btn-sec">One-Pager 📄</a>
    <a href="tel:+917003456624" class="btn-action btn-pri">Call Aditya 📞</a>
  </div>

  <script>
    function showTab(tab) {
      document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');

      document.getElementById('tab-pitch').style.display = tab === 'pitch' ? 'flex' : 'none';
      document.getElementById('tab-curveball').style.display = tab === 'curveball' ? 'flex' : 'none';
      document.getElementById('tab-flips').style.display = tab === 'flips' ? 'flex' : 'none';
      document.getElementById('tab-salary').style.display = tab === 'salary' ? 'flex' : 'none';
    }

    function copySnippet(id) {
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text);
      alert('Copied to clipboard!');
    }
  </script>

</body>
</html>
'''
    out_file = WAR_CHEST_DIR / 'ADITYA_POCKET_BATTLE_SHIELD_MOBILE.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(ROOT / 'ADITYA_POCKET_BATTLE_SHIELD_MOBILE.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Mobile Battle Shield at {out_file}")

# -------------------------------------------------------------
# 4. BUILD THE PORTABLE WAR CHEST MASTER LAUNCHER (Single Hub)
# -------------------------------------------------------------
def build_war_chest_master_hub():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADITYA MEHRA | THE PORTABLE CAREER WAR CHEST (Master Arsenal)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #03050c;
      --bg-surface: #070b16;
      --bg-card: #0d1324;
      --bg-card-hover: #151e36;
      --border: #1a2540;
      --cyan: #00f2fe;
      --cyan-glow: rgba(0, 242, 254, 0.25);
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.25);
      --emerald: #10b981;
      --purple: #8b5cf6;
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --font-sans: 'Plus Jakarta Sans', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.5;
      padding-bottom: 80px;
    }
    nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(3, 5, 12, 0.92);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 16px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand { font-size: 19px; font-weight: 800; display: flex; align-items: center; gap: 10px; }
    .brand span { color: var(--gold); }
    .status-badge {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--gold);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
    }

    .container { max-width: 1400px; margin: 0 auto; padding: 30px 40px 0; }
    
    .hero {
      background: linear-gradient(135deg, rgba(20, 28, 48, 0.95), rgba(8, 12, 24, 0.95));
      border: 1px solid var(--gold-glow);
      border-radius: 18px;
      padding: 36px 40px;
      margin-bottom: 36px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 24px;
    }
    .hero h1 { font-size: 36px; font-weight: 800; margin-bottom: 8px; }
    .hero p { color: var(--text-muted); font-size: 15px; max-width: 820px; }

    .sec-head {
      margin: 36px 0 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .sec-head h2 { font-size: 22px; font-weight: 800; color: #fff; }

    .arsenal-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
    }

    .weapon-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
    }
    .weapon-card:hover {
      border-color: var(--cyan);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 242, 254, 0.15);
    }

    .weapon-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--gold);
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    .weapon-title { font-size: 19px; font-weight: 700; color: #fff; margin-bottom: 8px; }
    .weapon-desc { font-size: 13px; color: var(--text-muted); line-height: 1.55; margin-bottom: 20px; }

    .weapon-actions {
      display: flex;
      gap: 10px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }
    .btn-act {
      flex: 1;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .btn-pri { background: var(--cyan); color: #03050c; }
    .btn-pri:hover { box-shadow: 0 0 12px var(--cyan-glow); }
    .btn-sec { background: transparent; border: 1px solid var(--border); color: var(--text-muted); }
    .btn-sec:hover { border-color: var(--cyan); color: #fff; }

    .download-strip {
      background: var(--bg-card);
      border: 1px solid var(--gold-glow);
      border-radius: 12px;
      padding: 22px 28px;
      margin-top: 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .download-strip h3 { font-size: 17px; font-weight: 700; color: #fff; }
    .download-strip p { font-size: 13px; color: var(--text-muted); }

    footer {
      border-top: 1px solid var(--border);
      padding-top: 30px;
      text-align: center;
      color: #64748b;
      font-size: 13px;
      font-family: var(--font-mono);
      margin-top: 60px;
    }
  </style>
</head>
<body>

  <nav>
    <div class="brand">
      ADITYA MEHRA <span>/ THE PORTABLE WAR CHEST</span>
    </div>
    <div class="status-badge">All 5 Weapons Armed & Verified</div>
  </nav>

  <main class="container">

    <div class="hero">
      <div>
        <h1>The Carry-Anywhere Career Arsenal</h1>
        <p>
          Every weapon engineered to dominate corporate interviews, boardrooms, recruiter screening calls, and salary negotiations. 
          Carry this folder on a flash drive, your phone, or an iPad—100% offline-ready.
        </p>
      </div>
      <div style="font-family: var(--font-mono); font-size: 13px; color: var(--gold); border: 1px solid var(--gold-glow); padding: 12px 18px; border-radius: 8px;">
        <div>PORTABLE PACKAGE: <strong>ADITYA_PORTABLE_WAR_CHEST.zip</strong></div>
        <div style="color: var(--emerald); font-size: 11px; margin-top: 4px;">✔ 100% Standalone & Offline Ready</div>
      </div>
    </div>

    <div class="sec-head">
      <div>
        <h2>Your 5 Lethal Career Weapons</h2>
        <p>Direct launch links to each specialized asset</p>
      </div>
    </div>

    <div class="arsenal-grid">
      <!-- Weapon 1 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 01 • Executive Presentation</div>
          <div class="weapon-title">The Executive One-Pager (A4)</div>
          <p class="weapon-desc">
            High-density, visual capability brief designed to be slid across the table to a VP or emailed as an executive summary. Summarizes all 4 proof-of-work pillars on a single page.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="ADITYA_EXECUTIVE_ONE_PAGER.html" target="_blank" class="btn-act btn-pri">Open One-Pager ↗</a>
          <a href="ADITYA_EXECUTIVE_ONE_PAGER.html" onclick="window.print()" class="btn-act btn-sec">Print A4 🖨️</a>
        </div>
      </div>

      <!-- Weapon 2 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 02 • Onboarding Blueprint</div>
          <div class="weapon-title">30-60-90 Day Operational Plan</div>
          <p class="weapon-desc">
            The ultimate hiring manager closer. A structured 3-phase roadmap showing how you will audit workflows, automate reporting latency by 40%, and achieve net positive ROI in 90 days.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="ADITYA_30_60_90_DAY_BLUEPRINT.html" target="_blank" class="btn-act btn-pri">Open 90-Day Plan ↗</a>
          <a href="ADITYA_30_60_90_DAY_BLUEPRINT.html" onclick="window.print()" class="btn-act btn-sec">Print Blueprint 🖨️</a>
        </div>
      </div>

      <!-- Weapon 3 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 03 • Smartphone Battle Shield</div>
          <div class="weapon-title">Pocket Battle Shield (Mobile)</div>
          <p class="weapon-desc">
            Mobile-optimized offline web app for your smartphone. Review the 60s elevator pitch, 5 curveball shields, counter-questions, and salary scripts 10 minutes before walking into an interview.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="ADITYA_POCKET_BATTLE_SHIELD_MOBILE.html" target="_blank" class="btn-act btn-pri">Launch Mobile Shield 📱</a>
        </div>
      </div>

      <!-- Weapon 4 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 04 • The Master ATS Resume</div>
          <div class="weapon-title">A4 Printable ATS Resume</div>
          <p class="weapon-desc">
            Standard single-column, 95%+ ATS scoring resume formatted with clean typography, verified metrics (Aero India, Instawork, Pencil Mark), and zero-margin parsing errors.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="resumes/Aditya_Mehra_Resume_Printable.html" target="_blank" class="btn-act btn-pri">Open ATS Resume ↗</a>
          <a href="resumes/Aditya_Mehra_Resume_Printable.html" onclick="window.print()" class="btn-act btn-sec">Print Resume 🖨️</a>
        </div>
      </div>

      <!-- Weapon 5 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 05 • Full Digital Portfolio</div>
          <div class="weapon-title">Executive Digital Portfolio</div>
          <p class="weapon-desc">
            Interactive dark-glass public portfolio showcase with live project walkthroughs, verifiable credentials, and 1-click recruiter InMail pitch generation.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html" target="_blank" class="btn-act btn-pri">Open Portfolio 🌐</a>
        </div>
      </div>

      <!-- Weapon 6 -->
      <div class="weapon-card">
        <div>
          <div class="weapon-tag">Weapon 06 • Objection Annihilator</div>
          <div class="weapon-title">STAR Interview Defense Matrix</div>
          <p class="weapon-desc">
            20+ pre-rehearsed STAR scripts answering non-tech BBA doubts, high-pressure logistics breakdowns, Red Sea supply chain reroutings, and compensation justifications.
          </p>
        </div>
        <div class="weapon-actions">
          <a href="STAR_INTERVIEW_DEFENSE_MATRIX.html" target="_blank" class="btn-act btn-pri">Open Defense Matrix 🛡️</a>
        </div>
      </div>
    </div>

    <!-- ZIP Download Strip -->
    <div class="download-strip">
      <div>
        <h3>📦 The Complete Offline ZIP War Chest Bundle</h3>
        <p>Contains all HTML files, resumes, blueprints, and offline scripts in a single portable archive.</p>
      </div>
      <div>
        <a href="WAR_CHEST/ADITYA_PORTABLE_WAR_CHEST.zip" download class="btn-act btn-pri" style="padding: 12px 24px; font-size: 14px;">Download ZIP Package (Flash Drive / Phone) 💾</a>
      </div>
    </div>

  </main>

  <footer>
    ADITYA MEHRA • BBA INTERNATIONAL BUSINESS '26 • DAYANANDA SAGAR UNIVERSITY, BENGALURU
    <br>POWERED BY OMEGA ∞ SUPREME PORTABLE CAREER ARSENAL
  </footer>

</body>
</html>
'''
    out_file = ROOT / 'ADITYA_PORTABLE_WAR_CHEST.html'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(WAR_CHEST_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated War Chest Master Hub at {out_file}")

# -------------------------------------------------------------
# 5. BUNDLE EVERYTHING INTO A PORTABLE ZIP ARCHIVE
# -------------------------------------------------------------
def package_zip():
    # Copy essential files to WAR_CHEST directory
    files_to_copy = [
        'ADITYA_EXECUTIVE_ONE_PAGER.html',
        'ADITYA_30_60_90_DAY_BLUEPRINT.html',
        'ADITYA_POCKET_BATTLE_SHIELD_MOBILE.html',
        'ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html',
        'STAR_INTERVIEW_DEFENSE_MATRIX.html',
        'ADITYA_APEX_SCORING_ENGINE.html',
        'ADITYA_JOB_TYCOON_EMPIRE_OS.html',
        'ADITYA_30_DAY_CAREER_CONQUEST_PLAYBOOK.md',
        'resume_adi.md'
    ]

    for f_name in files_to_copy:
        src = ROOT / f_name
        if src.exists():
            shutil.copy2(src, WAR_CHEST_DIR / f_name)

    # Copy printable resume
    resume_printable = ROOT / 'resumes' / 'Aditya_Mehra_Resume_Printable.html'
    if resume_printable.exists():
        shutil.copy2(resume_printable, WAR_CHEST_DIR / 'Aditya_Mehra_Resume_Printable.html')

    # Create zip
    zip_path = WAR_CHEST_DIR / 'ADITYA_PORTABLE_WAR_CHEST.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in WAR_CHEST_DIR.iterdir():
            if f.name != 'ADITYA_PORTABLE_WAR_CHEST.zip':
                zf.write(f, arcname=f.name)

    # Also copy zip to root for easy finding
    shutil.copy2(zip_path, ROOT / 'ADITYA_PORTABLE_WAR_CHEST.zip')
    print(f"Created portable zip archive at {zip_path} and {ROOT / 'ADITYA_PORTABLE_WAR_CHEST.zip'}")

if __name__ == '__main__':
    build_executive_one_pager()
    build_30_60_90_blueprint()
    build_mobile_battle_shield()
    build_war_chest_master_hub()
    package_zip()
