"""
inject_52_week_tab_to_suite.py
==============================
Injects Tab 10 (52-Week Hiring Calendar & Automated Recruitment Roadmap)
into `ADITYA_APEX_CAREER_SUITE.html`.
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path("data/aditya_global_career_intelligence.db")
HTML_PATH = Path("ADITYA_APEX_CAREER_SUITE.html")

def fetch_calendar_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute("""
    SELECT week_number, month, quarter, hiring_season, week_title, target_companies, role_categories, cycle_stage, action_playbook, verified_seam
    FROM hiring_calendar_52_weeks
    ORDER BY week_number ASC
    """).fetchall()
    conn.close()

    calendar_list = []
    for r in rows:
        calendar_list.append({
            "week": r[0],
            "month": r[1],
            "quarter": r[2],
            "hiring_season": r[3],
            "week_title": r[4],
            "target_companies": json.loads(r[5]),
            "role_categories": json.loads(r[6]),
            "cycle_stage": r[7],
            "action_playbook": r[8],
            "verified_seam": r[9]
        })
    return calendar_list

def generate_tab_html(calendar_data):
    cal_json_str = json.dumps(calendar_data).replace("</script>", "<\\/script>")

    tab_btn = """<button class="tab-btn" onclick="switchTab('calendar-52')">📅 52-Week Hiring Calendar & Auto-Apply <span class="count-badge">52 WEEKS</span></button>"""

    tab_pane = f"""
        <!-- TAB 10: 52-WEEK HIRING CALENDAR & AUTO-APPLY ROADMAP -->
        <section id="tab-calendar-52" class="tab-content">
          <div style="background: rgba(16, 24, 39, 0.95); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
              <div>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #10b981; margin: 0 0 6px 0;">📅 52-Week Master Recruitment Calendar & Automated Application Engine</h2>
                <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">Exhaustive week-by-week hiring schedule across Bengaluru GCCs, MNCs, FMCGs, Consulting, Aerospace, and Unicorns. 104 applications pre-staged for 1-click execution.</p>
              </div>
              <div style="display: flex; gap: 12px; align-items: center;">
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 8px; padding: 8px 16px; text-align: right;">
                  <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Current Week</div>
                  <div style="font-size: 1.1rem; font-weight: 700; color: #10b981;">WEEK 42 • OCT (Q4)</div>
                </div>
                <button onclick="downloadAllCalendarPackages()" style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 0.9rem;">
                  ⬇️ Download Staged Packets
                </button>
              </div>
            </div>

            <!-- Filter & Search Controls -->
            <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;">
              <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                <button class="cal-quarter-btn active" onclick="filterCalendarQuarter('ALL', this)" style="background: #10b981; color: white; border: none; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer;">All 52 Weeks</button>
                <button class="cal-quarter-btn" onclick="filterCalendarQuarter('Q1', this)" style="background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer;">Q1 (Jan-Mar)</button>
                <button class="cal-quarter-btn" onclick="filterCalendarQuarter('Q2', this)" style="background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer;">Q2 (Apr-Jun)</button>
                <button class="cal-quarter-btn" onclick="filterCalendarQuarter('Q3', this)" style="background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer;">Q3 (Jul-Sep)</button>
                <button class="cal-quarter-btn" onclick="filterCalendarQuarter('Q4', this)" style="background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer;">Q4 (Oct-Dec)</button>
              </div>

              <div style="flex: 1; min-width: 240px; display: flex; gap: 8px;">
                <input type="text" id="calSearchInput" onkeyup="searchCalendarSchedule()" placeholder="Search company (e.g. Boeing, Maersk, Google, Target, Shell)..." style="flex: 1; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 8px 12px; color: white; font-size: 0.9rem;" />
                <select id="calMonthSelect" onchange="filterCalendarMonth(this.value)" style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 8px 12px; color: white; font-size: 0.9rem;">
                  <option value="ALL">All Months</option>
                  <option value="January">January</option>
                  <option value="February">February</option>
                  <option value="March">March</option>
                  <option value="April">April</option>
                  <option value="May">May</option>
                  <option value="June">June</option>
                  <option value="July">July</option>
                  <option value="August">August</option>
                  <option value="September">September</option>
                  <option value="October">October</option>
                  <option value="November">November</option>
                  <option value="December">December</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Live Current Week Alert Banner -->
          <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15)); border: 1px solid #10b981; border-radius: 10px; padding: 18px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 14px;">
              <div style="font-size: 2rem;">⚡</div>
              <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #10b981; letter-spacing: 0.05em; text-transform: uppercase;">CURRENT CALENDAR WINDOW: OCTOBER (WEEK 42)</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: white;">Big Tech Business Operations & Strategic Procurement Wave</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px;">Active targets: <strong>Google India</strong> (Bagmane Capital) & <strong>Microsoft India</strong> (Bagmane Constellation) • Seam: <strong>EXP-003</strong></div>
              </div>
            </div>
            <button onclick="scrollToWeek(42)" style="background: #10b981; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.85rem;">
              Jump to Week 42 Packets
            </button>
          </div>

          <!-- Calendar Weeks Grid Container -->
          <div id="calendarScheduleContainer" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 18px;">
            <!-- Dynamically rendered via JavaScript -->
          </div>
        </section>
    """

    tab_script = f"""
    // --- 52-WEEK CALENDAR SYSTEM LOGIC ---
    const CALENDAR_DATA = {cal_json_str};

    function renderCalendarSchedule(dataToRender) {{
      const container = document.getElementById('calendarScheduleContainer');
      if (!container) return;
      container.innerHTML = '';

      if (dataToRender.length === 0) {{
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: #94a3b8; font-size: 1.1rem;">No calendar weeks matched your search or filter.</div>';
        return;
      }}

      dataToRender.forEach(w => {{
        const isCurrentWeek = (w.week === 42);
        const cardBorder = isCurrentWeek ? 'border: 2px solid #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);' : 'border: 1px solid rgba(255,255,255,0.08);';
        
        let companiesHtml = '';
        w.target_companies.forEach(tc => {{
          companiesHtml += `
            <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                  <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">${{tc.company}}</div>
                  <div style="font-size: 0.8rem; color: #94a3b8;">📍 ${{tc.location}} • <span style="color: #60a5fa;">${{tc.ats}}</span></div>
                </div>
                <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">STAGED</span>
              </div>
              <div style="font-size: 0.85rem; color: #e2e8f0; margin-top: 6px; font-weight: 500;">🎯 ${{tc.role}}</div>
              
              <div style="display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap;">
                <button onclick="copyCalendarAutofillPayload(${{w.week}}, '${{tc.company}}', '${{tc.role}}', '${{tc.ats}}')" style="flex: 1; min-width: 120px; background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #93c5fd; padding: 5px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; cursor: pointer;">
                  📋 Copy Autofill
                </button>
                <button onclick="copyCalendarInMail(${{w.week}}, '${{tc.company}}', '${{tc.role}}', '${{w.verified_seam}}')" style="flex: 1; min-width: 120px; background: rgba(168, 85, 247, 0.2); border: 1px solid #a855f7; color: #d8b4fe; padding: 5px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; cursor: pointer;">
                  ✉️ Copy InMail
                </button>
                <a href="${{tc.portal}}" target="_blank" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: white; padding: 5px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-decoration: none; display: flex; align-items: center; justify-content: center;">
                  🔗 Portal
                </a>
              </div>
            </div>
          `;
        }});

        const card = `
          <div id="week-card-${{w.week}}" style="background: rgba(17, 24, 39, 0.85); ${{cardBorder}} border-radius: 10px; padding: 18px; display: flex; flex-direction: column;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="background: linear-gradient(135deg, #10b981, #059669); color: white; font-size: 0.75rem; font-weight: 800; padding: 3px 10px; border-radius: 12px;">WEEK ${{String(w.week).padStart(2, '0')}}</span>
              <span style="font-size: 0.8rem; font-weight: 600; color: #94a3b8;">${{w.month.toUpperCase()}} • ${{w.quarter}}</span>
              <span style="background: rgba(59, 130, 246, 0.15); color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;">${{w.cycle_stage}}</span>
            </div>

            <h3 style="font-size: 1.05rem; font-weight: 700; color: white; margin: 0 0 6px 0;">${{w.week_title}}</h3>
            <div style="font-size: 0.8rem; color: #10b981; font-weight: 600; margin-bottom: 12px;">🌊 ${{w.hiring_season}}</div>

            <div style="margin-bottom: 12px; flex: 1;">
              ${{companiesHtml}}
            </div>

            <div style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px; font-size: 0.75rem; color: #94a3b8; display: flex; justify-content: space-between; align-items: center;">
              <div>Verified Seam: <strong style="color: #f59e0b;">${{w.verified_seam}}</strong></div>
              <div style="font-style: italic; color: #cbd5e1;">2 Staged Packages</div>
            </div>
          </div>
        `;
        container.innerHTML += card;
      }});
    }}

    function filterCalendarQuarter(quarter, btnElement) {{
      document.querySelectorAll('.cal-quarter-btn').forEach(b => {{
        b.style.background = 'rgba(255,255,255,0.06)';
        b.style.color = '#94a3b8';
        b.style.border = '1px solid rgba(255,255,255,0.1)';
      }});
      if (btnElement) {{
        btnElement.style.background = '#10b981';
        btnElement.style.color = 'white';
        btnElement.style.border = 'none';
      }}

      if (quarter === 'ALL') {{
        renderCalendarSchedule(CALENDAR_DATA);
      }} else {{
        const filtered = CALENDAR_DATA.filter(w => w.quarter === quarter);
        renderCalendarSchedule(filtered);
      }}
    }}

    function filterCalendarMonth(month) {{
      if (month === 'ALL') {{
        renderCalendarSchedule(CALENDAR_DATA);
      }} else {{
        const filtered = CALENDAR_DATA.filter(w => w.month.toLowerCase() === month.toLowerCase());
        renderCalendarSchedule(filtered);
      }}
    }}

    function searchCalendarSchedule() {{
      const query = document.getElementById('calSearchInput').value.toLowerCase().trim();
      if (!query) {{
        renderCalendarSchedule(CALENDAR_DATA);
        return;
      }}
      const filtered = CALENDAR_DATA.filter(w => {{
        const inTitle = w.week_title.toLowerCase().includes(query);
        const inSeason = w.hiring_season.toLowerCase().includes(query);
        const inCompanies = w.target_companies.some(c => c.company.toLowerCase().includes(query) || c.role.toLowerCase().includes(query) || c.location.toLowerCase().includes(query));
        const inPlaybook = w.action_playbook.toLowerCase().includes(query);
        return inTitle || inSeason || inCompanies || inPlaybook;
      }});
      renderCalendarSchedule(filtered);
    }}

    function scrollToWeek(weekNum) {{
      filterCalendarQuarter('ALL', document.querySelector('.cal-quarter-btn'));
      setTimeout(() => {{
        const el = document.getElementById('week-card-' + weekNum);
        if (el) {{
          el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
          el.style.transform = 'scale(1.02)';
          el.style.transition = 'all 0.3s ease';
          setTimeout(() => el.style.transform = 'scale(1)', 1000);
        }}
      }}, 100);
    }}

    function copyCalendarAutofillPayload(weekNum, company, role, ats) {{
      const payload = {{
        candidate: "Aditya Mehra",
        email: "adityamehra.work@gmail.com",
        phone: "+91-9876543210",
        location: "Bengaluru, Karnataka, India",
        degree: "BBA International Business (DSU '26)",
        target: {{
          week: weekNum,
          company: company,
          role: role,
          ats: ats
        }},
        answers: {{
          notice_period: "Immediate / 2026 Batch",
          expected_ctc: "₹7.5 - ₹12 LPA",
          work_authorization: "Indian Citizen (No Visa Required)"
        }}
      }};
      navigator.clipboard.writeText(JSON.stringify(payload, null, 2)).then(() => {{
        alert(`Copied ${{company}} (${{role}}) ATS Autofill Payload to clipboard!`);
      }});
    }}

    function copyCalendarInMail(weekNum, company, role, seam) {{
      const text = `Hi [Hiring Manager / Recruiter],\\n\\nI noticed ${{company}}'s active intake for ${{role}} in Bengaluru (Calendar Week ${{weekNum}}).\\n\\nAs a final-year BBA International Business graduate from DSU Bengaluru with verified background in ${{seam}} and enterprise operations, I have pre-staged my application through your careers portal.\\n\\nWould welcome a brief 5-minute conversation to share my operational portfolio.\\n\\nBest regards,\\nAditya Mehra\\n+91-9876543210 | adityamehra.work@gmail.com`;
      navigator.clipboard.writeText(text).then(() => {{
        alert(`Copied Recruiter InMail for ${{company}} to clipboard!`);
      }});
    }}

    function downloadAllCalendarPackages() {{
      alert('All 104 application packages are locally staged at:\\napplications_generated/52_weeks_calendar/\\n\\nYou can access them directly or use the 1-click clipboard buttons on each card.');
    }}

    // Auto-initialize calendar on tab switch or page load
    document.addEventListener('DOMContentLoaded', () => {{
      if (document.getElementById('calendarScheduleContainer')) {{
        renderCalendarSchedule(CALENDAR_DATA);
      }}
    }});
    """

    return tab_btn, tab_pane, tab_script

def inject_tab():
    calendar_data = fetch_calendar_data()
    tab_btn, tab_pane, tab_script = generate_tab_html(calendar_data)

    content = HTML_PATH.read_text(encoding="utf-8")

    # 1. Ensure Tab Button exists
    if 'switchTab(\'calendar-52\')' not in content:
        btn_marker = """<button class="tab-btn" onclick="switchTab('comp-calc')">"""
        if btn_marker in content:
            content = content.replace(btn_marker, f"{tab_btn}\n      {btn_marker}")
            print("[OK] Tab Button injected.")

    # 2. Inject Tab Pane if not already there
    if 'id="tab-calendar-52"' not in content:
        pane_marker = """<section id="tab-comp-calc" class="tab-content">"""
        if pane_marker in content:
            content = content.replace(pane_marker, f"{tab_pane}\n\n        {pane_marker}")
            print("[OK] Tab Pane injected.")
        else:
            print("[WARN] Could not find section id=tab-comp-calc marker.")

    # 3. Ensure script logic exists
    if "CALENDAR_DATA =" not in content:
        script_marker = """</script>"""
        last_script_pos = content.rfind(script_marker)
        if last_script_pos != -1:
            content = content[:last_script_pos] + "\n\n" + tab_script + "\n" + content[last_script_pos:]
            print("[OK] JavaScript logic injected.")

    HTML_PATH.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Updated {HTML_PATH} with Tab 10 (52-Week Calendar & Auto-Apply)!")

if __name__ == "__main__":
    inject_tab()
