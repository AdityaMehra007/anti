import os
from pathlib import Path

resumes_dir = Path(r"e:\anti\resumes")
pdf_dir = Path(r"e:\anti\resumes_pdf")
resumes_dir.mkdir(parents=True, exist_ok=True)
pdf_dir.mkdir(parents=True, exist_ok=True)

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# -------------------------------------------------------------
# 1. HTML STYLING (Flawless ATS + Modern Clean Typography)
# -------------------------------------------------------------
def get_html_wrapper(title, header_subtitle, content_body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} — Aditya Mehra</title>
<style>
    @page {{
        size: A4;
        margin: 12mm 14mm 12mm 14mm;
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
        font-size: 13px;
        line-height: 1.45;
    }}
    .page-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 10px 15px;
    }}
    header {{
        text-align: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }}
    h1 {{
        margin: 0 0 2px 0;
        font-size: 24px;
        letter-spacing: 0.5px;
        color: #0f172a;
        font-weight: 800;
        text-transform: uppercase;
    }}
    .subtitle {{
        font-size: 13.5px;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}
    .contact-bar {{
        font-size: 11.5px;
        color: #475569;
        font-weight: 500;
    }}
    .contact-bar a {{
        color: #2563eb;
        text-decoration: none;
    }}
    .section-title {{
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #0f172a;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 2px;
        margin-top: 10px;
        margin-bottom: 6px;
    }}
    p {{
        margin: 0 0 6px 0;
        color: #334155;
    }}
    .entry {{
        margin-bottom: 8px;
    }}
    .entry-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 1px;
    }}
    .entry-title {{
        font-weight: 700;
        color: #0f172a;
        font-size: 13px;
    }}
    .entry-company {{
        font-weight: 600;
        color: #2563eb;
    }}
    .entry-meta {{
        font-size: 11px;
        color: #64748b;
        font-weight: 500;
        text-align: right;
    }}
    ul {{
        margin: 2px 0 6px 0;
        padding-left: 18px;
    }}
    li {{
        margin-bottom: 2.5px;
        color: #334155;
    }}
    li strong {{
        color: #0f172a;
    }}
    .skills-block {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        margin-bottom: 6px;
    }}
    .skills-row {{
        font-size: 12px;
    }}
    .skills-row strong {{
        color: #0f172a;
        display: inline-block;
        min-width: 170px;
    }}
</style>
</head>
<body>
<div class="page-container">
    <header>
        <h1>ADITYA MEHRA</h1>
        <div class="subtitle">{header_subtitle}</div>
        <div class="contact-bar">
            Bengaluru, Karnataka, India &nbsp;|&nbsp; 
            +91-7003456624 &nbsp;|&nbsp; 
            <a href="mailto:adityamehra799@gmail.com">adityamehra799@gmail.com</a> &nbsp;|&nbsp; 
            <a href="https://www.linkedin.com/in/aditya-mehra-b8644b326">linkedin.com/in/aditya-mehra-b8644b326</a> &nbsp;|&nbsp; 
            <a href="https://github.com/AdityaMehra007">github.com/AdityaMehra007</a>
        </div>
    </header>
    {content_body}
</div>
</body>
</html>"""

# -------------------------------------------------------------
# 2. STARTUP BODY (HTML)
# -------------------------------------------------------------
startup_html_body = """
    <div class="section-title">Professional Summary</div>
    <p>
        Action-oriented, resourceful Business Operator with <strong>8 continuous years of real-world commercial experience</strong> starting at age 17 in retail. Demonstrated track record in high-volume B2B cold calling and lead generation (awarded written management commendation at Pencil Mark), directing 300+ on-ground event executions, and founding a food venture (Mehra's Kitchen). Proactive power-user of modern Generative AI and "vibe coding" (ChatGPT, Claude, AI Agents) to automate research, client pipelines, and documentation at 10x speed. Fluent in 5 languages with exceptional street-smart negotiation, crisis resolution, and zero-to-one ownership.
    </p>

    <div class="section-title">Core Capabilities & Toolkit</div>
    <div class="skills-block">
        <div class="skills-row"><strong>Outbound Growth & BD:</strong> Cold Calling, B2B Lead Generation, Commercial Pitching, Client Qualification, Pipeline Tracking, 15+ Active Thread Handling.</div>
        <div class="skills-row"><strong>On-Ground Operations:</strong> Event Logistics, Multi-Vendor Coordination, Stage Staging, Fast Crisis Triage, Zero Asset Loss, 100% On-Time Opening.</div>
        <div class="skills-row"><strong>AI Leverage & Vibe Coding:</strong> Generative AI for Business (Prompt Engineering, Automated Email & Report Generation via ChatGPT/Claude), Directing AI Agents for Rapid Tooling.</div>
        <div class="skills-row"><strong>Software & Spreadsheets:</strong> Microsoft Excel & Google Sheets (Data Entry, Sorting, Filtering, Daily Tracking Lists, Vendor Price Comparisons), Google Workspace.</div>
        <div class="skills-row"><strong>Languages (5):</strong> Hindi (Native), Punjabi (Native), Bengali (Fluent), English (Fluent), French (Conversational).</div>
    </div>

    <div class="section-title">Professional Experience & Operational Ventures</div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Business Development Intern</span> &nbsp;|&nbsp; <span class="entry-company">Pencil Mark Interior Solutions LLP</span></div>
            <div class="entry-meta">Jul 2025 – Aug 2025 | Bengaluru, India</div>
        </div>
        <ul>
            <li><strong>Outbound Calling & Prospecting:</strong> Executed daily outbound cold calls and commercial marketing campaigns targeting corporate prospects across Bengaluru office tech hubs.</li>
            <li><strong>Lead Qualification & Follow-up:</strong> Pitched interior fit-out solutions, qualified commercial requirements, and actively managed 15+ concurrent client follow-up threads.</li>
            <li><strong>Management Commendation:</strong> Recognized with a formal written letter of commendation from company leadership for outreach consistency, pipeline growth, and client relationship management.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Event Operations & Ground Logistics Lead</span> &nbsp;|&nbsp; <span class="entry-company">Independent Practice</span></div>
            <div class="entry-meta">2019 – Present | Bengaluru & Pan-India</div>
        </div>
        <ul>
            <li><strong>300+ Live Executions:</strong> Directed on-ground setups, vendor timelines, and crowd management across 300+ corporate brand activations (Puma India, Dyson, Tata Communications, Razorpay, Apollo, VH1 Supersonic).</li>
            <li><strong>Vendor Negotiation & Cost Control:</strong> Negotiated directly with local fabrication, lighting, sound, and venue suppliers, reducing procurement costs by ~15% while sustaining a 30%+ repeat client retention rate.</li>
            <li><strong>Live Crisis Triage:</strong> Resolved high-pressure on-site emergencies (bad weather, delayed suppliers, electrical failures) ensuring 100% on-time event launch with zero safety or security breaches.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Exhibition Operations Lead</span> &nbsp;|&nbsp; <span class="entry-company">Aero India 2025 (Salt in My Coca)</span></div>
            <div class="entry-meta">Feb 2025 | Yelahanka Air Force Station</div>
        </div>
        <ul>
            <li><strong>Defense Expo Staging:</strong> Managed 7-day stall setup, display layout, and visitor flow under strict Ministry of Defence security protocols at Asia's premier aerospace expo.</li>
            <li><strong>Crowd & Asset Protection:</strong> Managed high-density footfall engaging over 100,000 visitors and international delegates with zero security violations and zero inventory shrinkage.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Co-Founder & Operations Manager</span> &nbsp;|&nbsp; <span class="entry-company">Mehra's Kitchen</span></div>
            <div class="entry-meta">2025 | Bengaluru, India</div>
        </div>
        <ul>
            <li><strong>Zero-to-One Venture:</strong> Launched and operated a home-based cloud kitchen and physical pop-up food stall. Managed daily ingredient purchasing, recipe unit costing, food prep logistics, UPI/cash transactions, and customer service.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Event Coordinator</span> &nbsp;|&nbsp; <span class="entry-company">TRILOGY Concert (Bangalore Club)</span></div>
            <div class="entry-meta">Jan 2026 | Bengaluru, India</div>
        </div>
        <ul>
            <li>Coordinated logistics, technical riders, hospitality, and stage schedule for live concert headlined by Grammy Award winner Pt. Vishwa Mohan Bhatt. Managed multi-party AV and artist coordination ensuring zero stage delays.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">AI Data Operations Intern</span> &nbsp;|&nbsp; <span class="entry-company">Instawork Services India Pvt Ltd</span></div>
            <div class="entry-meta">Dec 2025 | Bengaluru, India</div>
        </div>
        <ul>
            <li>Collected and structured real-world ground-truth datasets for AI & Robotics machine learning pipelines under strict quality assurance benchmarks.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Retail Operations & Sales Associate</span> &nbsp;|&nbsp; <span class="entry-company">Family Business</span></div>
            <div class="entry-meta">2018 – 2020 | Kolkata & Bengaluru</div>
        </div>
        <ul>
            <li>Entered workforce at age 17; handled retail counter sales, daily cash drawer reconciliation, customer support, and assisted the cross-state business relocation from Kolkata to Bengaluru.</li>
        </ul>
    </div>

    <div class="section-title">Education & Credentials</div>
    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Bachelor of Business Administration (BBA)</span> &nbsp;|&nbsp; <span class="entry-company">Dayananda Sagar University (DSU)</span></div>
            <div class="entry-meta">Class of May 2026 | Bengaluru, India</div>
        </div>
        <p style="font-size:12px; margin-top:2px;">
            <strong>Certifications:</strong> Generative AI Mastermind (Outskill, 2025) &bull; AI Tools & ChatGPT for Business Productivity (be10x, 2026) &bull; Digital Marketing Professional Certificate (Google, 2024).
        </p>
    </div>
"""

# -------------------------------------------------------------
# 3. MNC BODY (HTML)
# -------------------------------------------------------------
mnc_html_body = """
    <div class="section-title">Professional Summary</div>
    <p>
        Disciplined, execution-focused Business Operations specialist holding a Bachelor of Business Administration (BBA) from Dayananda Sagar University, Bengaluru (Class of May 2026). Backed by <strong>8 continuous years of hands-on operational and commercial experience</strong>, including high-security coordination at Aero India 2025 under Ministry of Defence protocols and 300+ enterprise brand activations. Proven track record in supplier follow-up, process standardization, and professional client communications (awarded written management commendation at Pencil Mark). Proficient in leveraging modern AI productivity tools to accelerate operational reporting, track metrics, and maintain strict data integrity. Fluent in 5 languages with strong stakeholder alignment.
    </p>

    <div class="section-title">Core Professional Competencies</div>
    <div class="skills-block">
        <div class="skills-row"><strong>Operational Execution & Governance:</strong> Process Standardization, Standard Operating Procedures (SOPs), Checklists, On-Ground Logistics, Multi-Vendor Follow-ups, SLA Adherence.</div>
        <div class="skills-row"><strong>Commercial Communication & Relations:</strong> Outbound Lead Generation, Commercial Client Outreach, 15+ Concurrent Thread Tracking, Written Commendation (Pencil Mark).</div>
        <div class="skills-row"><strong>Risk Mitigation & Incident Management:</strong> Zero-Loss Asset Control, Security Protocol Compliance, Live Event Problem Resolution, Root Cause Analysis (RCA).</div>
        <div class="skills-row"><strong>Digital & Operational Tools:</strong> Microsoft Excel & Google Sheets (Data Organization, Tracking Sheets, Vendor Rate Checks), Google Workspace, AI Productivity Tools (ChatGPT, Claude).</div>
        <div class="skills-row"><strong>Languages (5):</strong> English (Fluent), Hindi (Native), Punjabi (Native), Bengali (Fluent), French (Conversational).</div>
    </div>

    <div class="section-title">Professional Experience</div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Exhibition Operations Lead</span> &nbsp;|&nbsp; <span class="entry-company">Aero India 2025 (Salt in My Coca)</span></div>
            <div class="entry-meta">Feb 2025 | Yelahanka Air Force Station, Bengaluru</div>
        </div>
        <ul>
            <li><strong>High-Security Defense Staging:</strong> Directed full 7-day exhibition stall setup, vendor schedules, display presentation, and visitor engagement under strict Ministry of Defence security parameters.</li>
            <li><strong>Vendor Protocol & Pass Coordination:</strong> Coordinated security gate clearances, access passes, and staging vehicle delivery under rigid military operating windows.</li>
            <li><strong>Zero-Loss Integrity:</strong> Successfully engaged over 100,000 attendees and international defense delegations with zero security breaches, zero damage, and zero inventory shrinkage.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Event Operations & Ground Logistics Lead</span> &nbsp;|&nbsp; <span class="entry-company">Independent Practice</span></div>
            <div class="entry-meta">2019 – Present | Bengaluru, India</div>
        </div>
        <ul>
            <li><strong>Enterprise Campaign Delivery:</strong> Directed end-to-end on-ground event operations across 300+ campaigns for marquee enterprise accounts (including Puma India, Tata Communications, Dyson, Apollo, Razorpay).</li>
            <li><strong>Standard Operating Procedures (SOPs):</strong> Established 25-point operational checklist and daily status templates, ensuring consistent, 100% on-time execution across multi-vendor teams.</li>
            <li><strong>Vendor SLA Governance:</strong> Benchmarked vendor rate cards, eliminated redundant cost markups, and tracked supplier delivery milestones, maintaining a 30%+ client retention rate.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Business Development Intern</span> &nbsp;|&nbsp; <span class="entry-company">Pencil Mark Interior Solutions LLP</span></div>
            <div class="entry-meta">Jul 2025 – Aug 2025 | Bengaluru, India</div>
        </div>
        <ul>
            <li><strong>Commercial Outreach & Prospecting:</strong> Conducted structured outbound calling and marketing campaigns engaging corporate decision-makers across Bengaluru commercial tech hubs.</li>
            <li><strong>Thread Management:</strong> Managed 15+ concurrent client communication and project follow-up threads, qualifying facility requirements and maintaining 100% data integrity.</li>
            <li><strong>Formal Management Commendation:</strong> Honored with a formal written letter of commendation from senior leadership for proactive outreach volume and consistent pipeline expansion.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Event Operations Coordinator</span> &nbsp;|&nbsp; <span class="entry-company">TRILOGY Concert (Bangalore Club)</span></div>
            <div class="entry-meta">Jan 2026 | Bengaluru, India</div>
        </div>
        <ul>
            <li>Coordinated full artist logistics pipeline, technical riders, travel, hospitality, and stage operations for live performance headlined by Grammy Award winner Pt. Vishwa Mohan Bhatt.</li>
            <li>Maintained real-time coordination between venue management, sound engineers, and security teams with zero scheduling delays.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">AI Data Operations Intern</span> &nbsp;|&nbsp; <span class="entry-company">Instawork Services India Pvt Ltd</span></div>
            <div class="entry-meta">Dec 2025 | Bengaluru, India</div>
        </div>
        <ul>
            <li>Participated in national AI & Robotics dataset initiative, validating ground-truth activity data for machine learning training models with 100% QA accuracy.</li>
        </ul>
    </div>

    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Operations & Sales Associate</span> &nbsp;|&nbsp; <span class="entry-company">Family Business</span></div>
            <div class="entry-meta">2018 – 2020 | Kolkata & Bengaluru</div>
        </div>
        <ul>
            <li>Commenced professional career at age 17; managed retail counter sales, daily cash reconciliation, inventory records, and assisted in relocating operations from Kolkata to Bengaluru.</li>
        </ul>
    </div>

    <div class="section-title">Education & Credentials</div>
    <div class="entry">
        <div class="entry-header">
            <div><span class="entry-title">Bachelor of Business Administration (BBA)</span> &nbsp;|&nbsp; <span class="entry-company">Dayananda Sagar University (DSU)</span></div>
            <div class="entry-meta">Class of May 2026 | Bengaluru, India</div>
        </div>
        <p style="font-size:12px; margin-top:2px;">
            <strong>Professional Certifications:</strong> Google Digital Marketing Professional Certificate (2024) &bull; Service Marketing: A Practical Approach (IIT Kharagpur / NPTEL, 2025) &bull; Generative AI Mastermind (Outskill, 2025) &bull; AI Tools for Business (be10x, 2026).
        </p>
    </div>
"""

# Assemble full HTMLs
startup_html = get_html_wrapper(
    "High-Velocity Business Operator & Outbound BD",
    "High-Velocity Business Operator & Outbound BD Specialist",
    startup_html_body
)
mnc_html = get_html_wrapper(
    "Business Operations & Project Execution Associate",
    "Business Operations & Project Execution Associate",
    mnc_html_body
)

startup_html_path = resumes_dir / "RESUME_ADITYA_MEHRA_STARTUP_OPERATOR.html"
mnc_html_path = resumes_dir / "RESUME_ADITYA_MEHRA_MNC_OPERATIONS.html"

with open(startup_html_path, "w", encoding="utf-8") as f:
    f.write(startup_html)

with open(mnc_html_path, "w", encoding="utf-8") as f:
    f.write(mnc_html)

print(f"[OK] Wrote HTML: {startup_html_path}")
print(f"[OK] Wrote HTML: {mnc_html_path}")

# Compile to PDF
startup_pdf_path = pdf_dir / "RESUME_ADITYA_MEHRA_STARTUP_OPERATOR.pdf"
mnc_pdf_path = pdf_dir / "RESUME_ADITYA_MEHRA_MNC_OPERATIONS.pdf"

if PLAYWRIGHT_AVAILABLE:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Startup PDF
        page = browser.new_page()
        page.goto(startup_html_path.resolve().as_uri())
        page.pdf(
            path=str(startup_pdf_path),
            format='A4',
            print_background=True,
            margin={'top': '10mm', 'bottom': '10mm', 'left': '12mm', 'right': '12mm'}
        )
        print(f"[OK] Compiled PDF: {startup_pdf_path}")
        
        # 2. MNC PDF
        page.goto(mnc_html_path.resolve().as_uri())
        page.pdf(
            path=str(mnc_pdf_path),
            format='A4',
            print_background=True,
            margin={'top': '10mm', 'bottom': '10mm', 'left': '12mm', 'right': '12mm'}
        )
        print(f"[OK] Compiled PDF: {mnc_pdf_path}")
        browser.close()
else:
    print("[!] Playwright not installed for PDF compile.")
