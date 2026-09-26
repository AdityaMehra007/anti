import json
from pathlib import Path

html_path = Path("e:/anti/apps/get_me_hired_dashboard/index.html")
data_path = Path("e:/anti/apps/get_me_hired_dashboard/data.json")

html = html_path.read_text(encoding="utf-8")
data_str = data_path.read_text(encoding="utf-8")

old_script_start = "<script>\nlet dashboardData = null;"

new_script_start = f"""<script>
window.EMBEDDED_DASHBOARD_DATA = {data_str};
let dashboardData = window.EMBEDDED_DASHBOARD_DATA;

async function loadData() {{
  try {{
    const res = await fetch('data.json');
    if (res.ok) {{
      dashboardData = await res.json();
    }}
  }} catch (err) {{
    console.warn("fetch('data.json') failed, using embedded data fallback:", err);
    dashboardData = window.EMBEDDED_DASHBOARD_DATA;
  }}
  render();
}}"""

if old_script_start in html:
    # Find up to "function render() {"
    end_marker = "function render() {"
    start_pos = html.find(old_script_start)
    end_pos = html.find(end_marker, start_pos)
    if start_pos != -1 and end_pos != -1:
        html = html[:start_pos] + new_script_start + "\n\n" + html[end_pos:]
        html_path.write_text(html, encoding="utf-8")
        print("[OK] Successfully embedded fallback data into index.html")
    else:
        print("[!] Could not locate end marker")
elif "window.EMBEDDED_DASHBOARD_DATA" in html:
    # Already embedded, let's refresh the embedded JSON
    start_marker = "window.EMBEDDED_DASHBOARD_DATA = "
    end_marker = ";\nlet dashboardData"
    s_idx = html.find(start_marker)
    e_idx = html.find(end_marker, s_idx)
    if s_idx != -1 and e_idx != -1:
        html = html[:s_idx + len(start_marker)] + data_str + html[e_idx:]
        html_path.write_text(html, encoding="utf-8")
        print("[OK] Successfully refreshed embedded data in index.html")
    else:
        print("[!] Markers for refresh not found")
else:
    print("[!] Neither marker found")
