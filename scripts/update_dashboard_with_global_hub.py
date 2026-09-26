import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

html_path = Path("e:/anti/apps/get_me_hired_dashboard/index.html")
html = html_path.read_text(encoding="utf-8")

# 1. Add tab button if not present
tab_btn_target = '<button class="tab-btn" onclick="switchTab(\'agencies\')">🏢 Bangalore Placement Agencies (Top 15 Consultancies)</button>'
tab_btn_new = '<button class="tab-btn" onclick="switchTab(\'agencies\')">🏢 Bangalore Placement Agencies (Top 15 Consultancies)</button>\n    <button class="tab-btn" onclick="switchTab(\'global\')">🌐 Funded Startups & Global MNCs (USA/UK/Global)</button>'

if tab_btn_target in html and "switchTab('global')" not in html:
    html = html.replace(tab_btn_target, tab_btn_new, 1)
    print("[OK] Added tab button for global MNCs & Startups")

# 2. Add tab content if not present
tab_content_target = '<!-- TAB 6: Bangalore Placement Agencies -->'
tab_global_html = '''<!-- TAB 7: Funded Startups & Global MNCs -->
  <div id="tab-global" class="tab-content">
    <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 24px; margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
        <div>
          <h3 style="color: #38bdf8; font-size: 18px;">🌐 Bangalore Funded Startups & Global MNCs (USA, UK & Worldwide)</h3>
          <p style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Verified non-sales operations & supply chain matrix across 45 Unicorns, US Tech GCCs, UK Enterprises & European Leaders.</p>
        </div>
        <div style="display: flex; gap: 10px;">
          <a href="../../BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv" download class="btn-portal" style="color: #6ee7b7; border-color: #059669;">📥 Export Master CSV</a>
          <a href="../job_application_studio/global_mnc_and_startup_hub.html" target="_blank" class="btn-action" style="padding: 8px 18px; font-size: 13px;">Open Interactive Search Studio ↗</a>
        </div>
      </div>
      <div id="global-container" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px;"></div>
    </div>
  </div>

  '''

if tab_content_target in html and 'id="tab-global"' not in html:
    html = html.replace(tab_content_target, tab_global_html + tab_content_target, 1)
    print("[OK] Added tab-global HTML content block")

# 3. Add global rendering in render() function if not present
render_target = '// 3. Skills'
render_global_code = '''  // 2.6 Funded Startups & Global MNCs
  const globalContainer = document.getElementById('global-container');
  if (dashboardData.funded_startups_and_global_mncs && globalContainer) {
    globalContainer.innerHTML = dashboardData.funded_startups_and_global_mncs.slice(0, 20).map(c => `
      <div style="background: #07090e; border: 1px solid #1e293b; border-radius: 10px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
            <div style="font-size: 15px; font-weight: 700; color: #fff;">${c.company_name}</div>
            <span class="badge" style="font-size: 10px;">${c.origin_country}</span>
          </div>
          <div style="font-size: 12px; color: #38bdf8; font-weight: 600; margin-top: 4px;">${c.category}</div>
          <div style="font-size: 11px; color: #34d399; margin-top: 4px; font-family: monospace;">⚡ ${c.funding_status}</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">📍 ${c.bangalore_corridor}</div>
          <div style="margin-top: 10px; background: #0d121d; border: 1px solid #1e293b; border-radius: 6px; padding: 10px;">
            <div style="font-size: 12px; font-weight: 700; color: #e2e8f0;">🎯 ${c.target_role}</div>
            <div style="font-size: 11px; color: #38bdf8; margin-top: 2px;">CTC: ₹${c.total_ctc_min}L - ₹${c.total_ctc_max}L | In-Hand: ~₹${c.monthly_in_hand_est.toLocaleString()}/mo</div>
          </div>
        </div>
        <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center; gap: 8px;">
          <a href="mailto:${c.hr_email}?subject=Candidate%20Submission%20%7C%20Aditya%20Mehra%20%7C%20BBA%20International%20Business%20'26%20(DSU)&body=Dear%20Recruitment%20Team%2C%0D%0A%0D%0AI%20am%20writing%20to%20apply%20for%20the%20${encodeURIComponent(c.target_role)}%20mandate%20at%20${encodeURIComponent(c.company_name)}.%0D%0A%0D%0ASincerely%2C%0D%0AAditya%20Mehra%0D%0A%2B91%2070034%2056624" class="btn-portal" style="font-size: 11px;">✉️ Email HR</a>
          <a href="${c.direct_apply_url}" target="_blank" class="btn-portal" style="color: #93c5fd; font-size: 11px;">Portal ↗</a>
        </div>
      </div>
    `).join('');
  }

  '''

if render_target in html and 'globalContainer' not in html:
    html = html.replace(render_target, render_global_code + render_target, 1)
    print("[OK] Added globalContainer rendering inside render()")

html_path.write_text(html, encoding="utf-8")
print("[OK] Dashboard index.html updated successfully!")
