import sqlite3
import urllib.parse
from pathlib import Path

def tailor_message(company: str, job_title: str, contact_name: str, corridor: str):
    co_lower = company.lower()
    title_lower = job_title.lower()
    
    # 1. BFSI / Global Capability Centers / Consulting MNCs
    if any(k in co_lower for k in ['goldman', 'jpmorgan', 'pwc', 'deloitte', 'ey', 'kpmg', 'barclays', 'hsbc', 'morgan stanley', 'citi', 'ubs', 'wells fargo', 'standard chartered', 'fidelity', 'deutsche']):
        sector_hook = (
            f"I am writing to express my strong interest in entry-level operations, business process, and execution roles "
            f"at {company} in Bengaluru. With your focus on institutional governance, audit accuracy, and operational risk mitigation, "
            f"I bring disciplined execution and attention to process details."
        )
        points = """• Process Discipline & Data Precision: Executed rigorous ground-level AI & robotics data collection at Instawork Services India Pvt. Ltd. (2025), strictly adhering to quality benchmarks and verification protocols.
• Structured Commercial Tracking: Converted commercial requirements into detailed execution briefs and managed vendor pricing matrices in MS Excel at Pencil Mark Interior Solutions LLP (2025).
• Ledger & Transaction Foundations: Managed billing registers, order dispatches, and Excel inventory records in our family business (2018–2020).
• Automation-Minded: Fast learning agility with AI tools (Google Antigravity, Cursor, Python) to build operational checklists and eliminate repetitive administrative overhead (GitHub: github.com/AdityaMehra007/anti with 16 passing unit tests)."""

    # 2. Logistics, Supply Chain & International Trade
    elif any(k in co_lower for k in ['maersk', 'dhl', 'fedex', 'delhivery', 'shadowfax', 'ecom express', 'bluedart', 'kuehne', 'db schenker', 'ups', 'supply', 'logistics', 'freight']):
        sector_hook = (
            f"I am writing to express my strong interest in logistics operations, vendor coordination, and supply chain execution "
            f"at {company} in Bengaluru. Having specialized in International Business during my BBA, I am keen to support your daily fulfillment and dispatch operations."
        )
        points = """• Academic & Trade Foundations: Completed BBA in International Business (DSU Bengaluru '26) with deep coursework in global trade flows, freight documentation, and operational logistics.
• High-Footfall Inventory & Stock Control: Managed live booth inventory restocking, customer sampling, and UPI transaction registers at Aero India (Yelahanka) for artisan chocolate brand Salt in My Cocoa.
• Commercial Vendor Coordination: Handled vendor quotation matrices and milestone tracking at Pencil Mark Interior Solutions LLP (2025).
• Order Dispatch & Daily Billing: 2 years hands-on experience handling daily supplier dispatches, billing ledgers, and stock tracking in MS Excel in family business operations (2018–2020)."""

    # 3. High-Growth Tech Startups / E-Commerce / Consumer Tech
    elif any(k in co_lower for k in ['swiggy', 'zomato', 'zepto', 'blinkit', 'meesho', 'cred', 'razorpay', 'flipkart', 'instawork', 'ola', 'uber', 'dunzo', 'urban company', 'phonepe', 'groww', 'zerodha']):
        sector_hook = (
            f"I am writing to express my strong interest in operations, city execution, and founder's office/ops associate roles "
            f"at {company} in Bengaluru. I thrive in fast-paced environments where ownership, hustle, and process automation move metrics quickly."
        )
        points = """• High-Velocity Field & Event Operations: Represented artisan chocolate brand Salt in My Cocoa at Aero India (Yelahanka)—managed booth setup, live sampling, customer conversion, and fast UPI billing under heavy footfall. Handled artist & vendor logistics for live concerts (TRILOGY Concert).
• Tech-First Mindset & Vibe Coding: I actively use Google Antigravity, Cursor, and Python to automate operational tracking, parse communications, and generate scheduling workflows (Proof of Work: github.com/AdityaMehra007/anti, 16/16 verified tests).
• Operations & Data Collection: Executed physical AI & robotics data collection adhering to tight operational quality standards at Instawork Services India (2025).
• Immediate Bengaluru Availability: BBA graduate (DSU '26) based in Bangalore, ready to join on day one."""

    # 4. Engineering, Aerospace & Industrial MNCs
    elif any(k in co_lower for k in ['boeing', 'airbus', 'schneider', 'siemens', 'ge', 'honeywell', 'bosch', 'caterpillar', 'abb', 'l&t']):
        sector_hook = (
            f"I am writing to express my strong interest in business operations, site coordination, and project execution roles "
            f"at {company} in Bengaluru. Having managed on-ground presence at Aero India and corporate vendor matrices, I bring structured execution to your operations."
        )
        points = """• On-Ground Presence at Aero India: Managed brand operations, customer liaison, inventory restocking, and booth coordination at Air Force Station Yelahanka during Aero India for Salt in My Cocoa.
• Operational Compliance & Quality: Maintained strict input protocols and data accuracy during AI & robotics data collection at Instawork Services India (2025).
• Vendor Management & Project Support: Maintained contractor milestone sheets and vendor pricing matrices in Excel at Pencil Mark Interior Solutions LLP (2025).
• Process & Tech Prototyping: Built automated workflow prototypes in Python and SQLite using Google Antigravity (GitHub: github.com/AdityaMehra007/anti)."""

    # 5. General Bengaluru Corporate & Operations Roles
    else:
        sector_hook = (
            f"I am writing to express my strong interest in entry-level operations, management trainee, and business execution opportunities "
            f"at {company} in Bengaluru. I recently completed my BBA in International Business from Dayananda Sagar University (DSU, Class of 2026) and am available for immediate joining."
        )
        points = """• Ground Operations & Event Activations: Managed brand booth setup, high-footfall sampling, inventory restocking, and UPI transactions at Aero India (Yelahanka) for Salt in My Cocoa; coordinated live concert logistics (TRILOGY Concert).
• Corporate Internships: Executed AI & robotics data collection adhering to strict quality protocols at Instawork Services India (2025); handled client briefs and vendor matrices in MS Excel at Pencil Mark Interior Solutions (2025).
• Family Business Rigor: 2 years managing customer billing, supplier follow-ups, and Excel inventory records in Kolkata (2018–2020).
• Tech & Automation Agility: Prototyped operations automation tools using Google Antigravity, Cursor, and Python (Proof of work: github.com/AdityaMehra007/anti with 16/16 passing unit tests)."""

    subject = f"Application: {job_title} - Aditya Mehra (BBA DSU Bengaluru | Immediate Joining)"
    body = f"""Dear {contact_name},

{sector_hook}

Here is how my verifiable execution background aligns with your operational priorities:

{points}

I would welcome 10 minutes to discuss how my execution discipline, problem-solving speed, and fast learning can support {company}.

Sincerely,

Aditya Mehra
Bengaluru, India | +91 7003456624 | adityamehra007@gmail.com
LinkedIn: linkedin.com/in/aditya-mehra-b8644b326 | GitHub: github.com/AdityaMehra007
"""
    return subject, body

def main():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT application_id, company, job_title, contact_name, contact_email, corridor FROM automated_applications")
    rows = cur.fetchall()

    print(f"Tailoring pitches for {len(rows)} applications based on target industry and role expectations...")
    updated = 0
    for app_id, company, job_title, contact_name, contact_email, corridor in rows:
        subject, body = tailor_message(company, job_title, contact_name, corridor)
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(contact_email)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        cur.execute("UPDATE automated_applications SET gmail_url = ? WHERE application_id = ?", (gmail_url, app_id))
        updated += 1

    conn.commit()
    print(f"Successfully tailored all {updated} applications in SQLite database!")

    # Also re-render top 50 in auto_apply_launcher.html
    import html
    cur.execute("""
        SELECT application_id, company, job_title, contact_name, contact_email, corridor, fit_score, gmail_url 
        FROM automated_applications 
        LIMIT 50
    """)
    top_50 = cur.fetchall()

    rows_html = ""
    for app_id, company, job_title, contact_name, contact_email, corridor, fit_score, gmail_url in top_50:
        rows_html += f"""
        <tr>
          <td><code>{html.escape(app_id)}</code></td>
          <td><strong>{html.escape(company)}</strong></td>
          <td>{html.escape(job_title)}</td>
          <td>{html.escape(contact_name)}<br><span style="color:#64748b; font-size:11px;">{html.escape(contact_email)}</span></td>
          <td>{html.escape(corridor or 'Bengaluru Corporate')}</td>
          <td><span class="score-pill">{fit_score:.1f}%</span></td>
          <td>
            <a href="{html.escape(gmail_url)}" target="_blank" class="action-btn">
              ⚡ 1-Click Tailored Apply
            </a>
          </td>
        </tr>
        """

    launcher_file = Path("apps/job_application_studio/auto_apply_launcher.html")
    content = launcher_file.read_text(encoding="utf-8")
    tbody_start = content.find("<tbody>") + len("<tbody>")
    tbody_end = content.find("</tbody>")
    if tbody_start != -1 and tbody_end != -1:
        new_content = content[:tbody_start] + "\n" + rows_html + "\n    " + content[tbody_end:]
        launcher_file.write_text(new_content, encoding="utf-8")
        print("Updated auto_apply_launcher.html with industry-tailored 1-click pitches!")
    else:
        print("Warning: Could not update launcher HTML table body.")

if __name__ == "__main__":
    main()
