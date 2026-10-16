#!/usr/bin/env python3
"""
update_nexus_live_search.py - Updates omega_master_nexus.html with live in-browser multi-domain search
"""

import json
from pathlib import Path

nexus_file = Path(r"e:\anti\omega_master_nexus.html")
content = nexus_file.read_text(encoding="utf-8")

with open(r"e:\anti\data\nexus_live_search_sample.json", "r", encoding="utf-8") as f:
    sample_entities = json.load(f)

# Pick balanced entities across all domains
domains = {}
for e in sample_entities:
    d = e["domain"]
    if d not in domains:
        domains[d] = []
    domains[d].append(e)

balanced_sample = []
for d, items in domains.items():
    balanced_sample.extend(items[:35])

print(f"Total balanced sample entities selected: {len(balanced_sample)}")

js_code = f"""
const masterEntities = {json.dumps(balanced_sample)};
let activeDomain = 'All';

function getDomainBadge(dom) {{
  if (dom.includes('Summer')) return 'badge-summer';
  if (dom.includes('New Grad 2026')) return 'badge-newgrad';
  if (dom.includes('New Grad 2027')) return 'badge-newgrad27';
  if (dom.includes('AI')) return 'badge-ai';
  if (dom.includes('React')) return 'badge-react';
  if (dom.includes('n8n')) return 'badge-n8n';
  if (dom.includes('Whiteboard')) return 'badge-hww';
  if (dom.includes('Challenges')) return 'badge-challenges';
  if (dom.includes('JustHireMe')) return 'badge-jhm';
  if (dom.includes('JobFunnel')) return 'badge-funnel';
  return 'badge-ai';
}}

function getDomainLink(dom) {{
  if (dom.includes('Summer')) return 'summer_2027_dashboard.html';
  if (dom.includes('New Grad 2026')) return 'new_grad_dashboard.html';
  if (dom.includes('New Grad 2027')) return 'new_grad_2027_dashboard.html';
  if (dom.includes('AI')) return 'ai_college_jobs_dashboard.html';
  if (dom.includes('React')) return 'react_interview_command_center.html';
  if (dom.includes('n8n')) return 'n8n_command_center.html';
  if (dom.includes('Whiteboard')) return 'hiring_without_whiteboards_dashboard.html';
  if (dom.includes('Challenges')) return 'frontend_challenges_dashboard.html';
  if (dom.includes('JustHireMe')) return 'justhireme_dashboard.html';
  if (dom.includes('JobFunnel')) return 'jobfunnel_dashboard.html';
  return 'omega_master_nexus.html';
}}

function handleSearch() {{
  const query = document.getElementById('omnibar-input').value.toLowerCase().trim();
  const grid = document.getElementById('results-grid');
  
  if (!query) {{
    grid.innerHTML = '<div style="color:var(--text-dim); font-size:0.9rem; grid-column:1/-1; text-align:center; padding:3rem 0;">Type any keyword into the Omnibar to query the unified SQLite FTS5 index.</div>';
    return;
  }}

  const matches = masterEntities.filter(e => {{
    if (activeDomain !== 'All' && e.domain !== activeDomain) return false;
    return (
      e.title.toLowerCase().includes(query) ||
      e.text.toLowerCase().includes(query) ||
      e.category.toLowerCase().includes(query)
    );
  }});

  if (!matches.length) {{
    grid.innerHTML = '<div style="color:var(--text-dim); font-size:0.9rem; grid-column:1/-1; text-align:center; padding:3rem 0;">No matches in visual cache for "' + query + '". Run <code>python omega_master_engine.py --search "' + query + '"</code> in console to query all 17,657 records.</div>';
    return;
  }}

  grid.innerHTML = matches.slice(0, 15).map(m => `
    <div class="result-card">
      <div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
          <span class="badge ${{getDomainBadge(m.domain)}}">${{m.domain}}</span>
          <span style="font-size:0.75rem; color:var(--text-dim); font-family:'JetBrains Mono';">${{m.id}}</span>
        </div>
        <div style="font-weight:700; font-size:1.02rem; margin-bottom:0.25rem;">${{m.title}}</div>
        <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.45;">${{m.text}}...</div>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.75rem;">
        <span style="font-size:0.75rem; color:var(--text-dim);">${{m.category}}</span>
        <a href="${{getDomainLink(m.domain)}}" class="btn" style="padding:0.3rem 0.75rem; font-size:0.75rem;">Open Dashboard →</a>
      </div>
    </div>
  `).join('');
}}

function setDomain(dom, btn) {{
  activeDomain = dom;
  document.querySelectorAll('.domain-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  handleSearch();
}}

document.getElementById('omnibar-input').value = 'Intern';
handleSearch();
"""

script_idx = content.find("<script>")
if script_idx != -1:
    new_html = content[:script_idx] + "<script>" + js_code + "</script>\n</body>\n</html>\n"
    nexus_file.write_text(new_html, encoding="utf-8")
    print("[OK] Successfully upgraded omega_master_nexus.html with live search!")
else:
    print("[!] Could not find script tag in nexus file.")
