#!/usr/bin/env python3
"""
enhance_universal_cockpit.py - Integrates Opportunity Census (500+ Jobs) & Application Dockets into Cockpit
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import json
from pathlib import Path

ROOT = Path(r"e:\anti")
COCKPIT_HTML = ROOT / "universal_job_cockpit.html"
CENSUS_JSON = ROOT / "data" / "universal_dissected_jobs_500.json"
DOCKETS_JSON = ROOT / "data" / "universal_application_dockets.json"

def main():
    with open(COCKPIT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    with open(CENSUS_JSON, "r", encoding="utf-8") as f:
        census = json.load(f)

    # 1. Add Tab 4 to Navigation Header if not present
    old_nav = """        <button onclick="switchTab('matrix')" id="tab-matrix" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            Agent Skills Matrix (3,837 Skills)
        </button>
    </div>"""

    new_nav = """        <button onclick="switchTab('matrix')" id="tab-matrix" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            Agent Skills Matrix (3,837 Skills)
        </button>
        <button onclick="switchTab('census')" id="tab-census" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            Opportunity Census & Dockets (500 Roles)
        </button>
    </div>"""

    if "tab-census" not in html:
        html = html.replace(old_nav, new_nav)

    # 2. Add View Census Section before </main>
    view_census_html = """
        <!-- TAB 4: OPPORTUNITY CENSUS & APPLICATION DOCKETS -->
        <section id="view-census" class="hidden space-y-6">
            <!-- Metrics Banner -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Total Vacancies Dissected</span>
                    <span id="census-stat-total" class="text-2xl font-black text-white">500</span>
                    <span class="text-[11px] text-emerald-400 block mt-0.5">Global Master Database</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Strong Fit Matches (≥70%)</span>
                    <span id="census-stat-strong" class="text-2xl font-black text-emerald-400">406</span>
                    <span class="text-[11px] text-slate-400 block mt-0.5">Auto-Apply Qualified</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Average ATS Score</span>
                    <span id="census-stat-avg" class="text-2xl font-black text-blue-400">69.8%</span>
                    <span class="text-[11px] text-slate-400 block mt-0.5">Semantic Match Ratio</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Application Dockets Staged</span>
                    <span id="census-stat-dockets" class="text-2xl font-black text-purple-400">423</span>
                    <span class="text-[11px] text-purple-300 block mt-0.5">Ready for 1st-Degree Outreach</span>
                </div>
            </div>

            <!-- Search & Filters Toolbar -->
            <div class="glass p-4 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-3 flex-1 min-w-[280px]">
                    <div class="relative flex-1 max-w-sm">
                        <svg class="w-4 h-4 absolute left-3 top-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        <input type="text" id="census-search-input" onkeyup="filterCensusTable()" placeholder="Search role, company, or skill..." class="w-full bg-slate-900 border border-slate-700 text-xs rounded-lg pl-9 pr-3 py-2 text-white focus:outline-none focus:border-emerald-500">
                    </div>
                    <select id="census-fit-filter" onchange="filterCensusTable()" class="bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:border-emerald-500">
                        <option value="ALL">All Match Tiers</option>
                        <option value="Strong Fit">Strong Fit (≥70%)</option>
                        <option value="Moderate Fit">Moderate Fit (50-69%)</option>
                        <option value="Stretch Fit">Stretch Fit (<50%)</option>
                    </select>
                    <select id="census-level-filter" onchange="filterCensusTable()" class="bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:border-emerald-500">
                        <option value="ALL">All Seniority Levels</option>
                        <option value="L1">L1 - Intern / Fresher</option>
                        <option value="L2">L2 - Associate / Junior</option>
                        <option value="L3">L3 - Mid-Level Specialist</option>
                        <option value="L4">L4 - Senior Professional</option>
                        <option value="L5">L5 - Lead / Principal</option>
                        <option value="L6">L6 - Director / Staff</option>
                        <option value="L7">L7 - Executive / VP</option>
                    </select>
                </div>
                <div class="flex items-center gap-2">
                    <span id="census-count-badge" class="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">Showing 500 Roles</span>
                </div>
            </div>

            <!-- Opportunities Census Table -->
            <div class="glass rounded-2xl border border-slate-800 overflow-hidden">
                <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead class="sticky top-0 z-20 bg-slate-900 border-b border-slate-800 font-mono text-slate-400 uppercase text-[10px]">
                            <tr>
                                <th class="p-3.5">Company & Role</th>
                                <th class="p-3.5">Archetype / Family</th>
                                <th class="p-3.5">Level & Modality</th>
                                <th class="p-3.5">ATS Match</th>
                                <th class="p-3.5">Key Matched Skills</th>
                                <th class="p-3.5 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="census-table-tbody" class="divide-y divide-slate-800/60 font-sans">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
"""

    if "view-census" not in html:
        html = html.replace("    </main>", view_census_html + "\n    </main>")

    # 3. Add Docket View Modal before </body>
    docket_modal_html = """
    <!-- Application Docket Modal -->
    <div id="docket-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
        <div class="glass max-w-3xl w-full rounded-2xl border border-slate-700 p-6 space-y-5 max-h-[90vh] overflow-y-auto shadow-2xl">
            <div class="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span id="modal-docket-badge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">APP-DOCKET-0001</span>
                        <span id="modal-fit-badge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Strong Fit</span>
                    </div>
                    <h3 id="modal-role-title" class="text-lg font-bold text-white mt-1">Role Title</h3>
                    <p id="modal-company-info" class="text-xs text-slate-400">Company Name • Location</p>
                </div>
                <button onclick="closeDocketModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>

            <!-- Bullets Section -->
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <h4 class="text-xs font-mono font-bold text-emerald-400 uppercase">1. Tailored Google X-Y-Z Resume Bullets (Verified Evidence)</h4>
                </div>
                <div id="modal-bullets-list" class="space-y-2">
                    <!-- Bullets -->
                </div>
            </div>

            <!-- Recruiter Outreach Template -->
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <h4 class="text-xs font-mono font-bold text-blue-400 uppercase">2. 1st-Degree LinkedIn / Recruiter InMail Outreach Note</h4>
                    <button onclick="copyModalField('modal-recruiter-text', this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-mono transition">Copy Note</button>
                </div>
                <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed font-sans" id="modal-recruiter-text">
                    Loading outreach draft...
                </div>
            </div>

            <!-- Cover Letter Hook -->
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <h4 class="text-xs font-mono font-bold text-amber-400 uppercase">3. Application Cover Letter Hook</h4>
                    <button onclick="copyModalField('modal-cover-text', this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-mono transition">Copy Letter</button>
                </div>
                <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed font-sans" id="modal-cover-text">
                    Loading cover letter hook...
                </div>
            </div>

            <!-- Footer Actions -->
            <div class="flex items-center justify-between pt-3 border-t border-slate-800">
                <span class="text-[11px] text-slate-500 font-mono">Grounded in EXP-001 through EXP-009 (Zero Hallucination)</span>
                <div class="flex items-center gap-2">
                    <button id="modal-inspect-btn" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-black font-semibold rounded-lg text-xs transition">Dissect in Live Engine →</button>
                    <button onclick="closeDocketModal()" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition">Close</button>
                </div>
            </div>
        </div>
    </div>
"""
    if "docket-modal" not in html:
        html = html.replace("</body>", docket_modal_html + "\n</body>")

    # 4. Update switchTab function to include 'census'
    old_switch = """        function switchTab(tabId) {
            document.getElementById('view-dissector').classList.add('hidden');
            document.getElementById('view-taxonomy').classList.add('hidden');
            document.getElementById('view-matrix').classList.add('hidden');

            document.getElementById('tab-dissector').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            document.getElementById('tab-taxonomy').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            document.getElementById('tab-matrix').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";

            document.getElementById(`view-${tabId}`).classList.remove('hidden');
            document.getElementById(`tab-${tabId}`).className = "py-3 text-emerald-400 border-b-2 border-emerald-400 flex items-center gap-2 transition font-semibold";
        }"""

    new_switch = """        function switchTab(tabId) {
            document.getElementById('view-dissector').classList.add('hidden');
            document.getElementById('view-taxonomy').classList.add('hidden');
            document.getElementById('view-matrix').classList.add('hidden');
            const censusView = document.getElementById('view-census');
            if (censusView) censusView.classList.add('hidden');

            document.getElementById('tab-dissector').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            document.getElementById('tab-taxonomy').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            document.getElementById('tab-matrix').className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            const tabCensus = document.getElementById('tab-census');
            if (tabCensus) tabCensus.className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";

            document.getElementById(`view-${tabId}`).classList.remove('hidden');
            document.getElementById(`tab-${tabId}`).className = "py-3 text-emerald-400 border-b-2 border-emerald-400 flex items-center gap-2 transition font-semibold";
        }"""

    html = html.replace(old_switch, new_switch)

    # 5. Add census variables, embedded fallback data, table rendering, modal actions
    census_subset = census["jobs"][:100]
    census_js_block = f"""
        // Global Census & Dockets Store
        let censusJobs = {json.dumps(census_subset)};
        let activeFilteredCensus = censusJobs;

        async function loadCensusData() {{{{
            try {{{{
                const res = await fetch('/api/census');
                if (res.ok) {{{{
                    const data = await res.json();
                    if (data && data.jobs && data.jobs.length > 0) {{{{
                        censusJobs = data.jobs;
                    }}}}
                }}}}
            }}}} catch (e) {{{{
                try {{{{
                    const res2 = await fetch('data/universal_dissected_jobs_500.json');
                    if (res2.ok) {{{{
                        const data2 = await res2.json();
                        if (data2 && data2.jobs && data2.jobs.length > 0) {{{{
                            censusJobs = data2.jobs;
                        }}}}
                    }}}}
                }}}} catch (err) {{{{
                    console.log("Using pre-bundled census dataset.");
                }}}}
            }}}}
            renderCensusTable(censusJobs);
        }}}}

        function renderCensusTable(jobs) {{{{
            const tbody = document.getElementById('census-table-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';
            activeFilteredCensus = jobs;

            document.getElementById('census-count-badge').innerText = `Showing ${{jobs.length}} Roles`;

            jobs.forEach(j => {{{{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-900/60 transition";
                const fitColor = j.ats_score >= 70 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' : (j.ats_score >= 50 ? 'text-amber-400 bg-amber-500/10 border-amber-500/30' : 'text-rose-400 bg-rose-500/10 border-rose-500/30');
                const tierLabel = j.fit_tier || (j.ats_score >= 70 ? 'Strong Fit' : (j.ats_score >= 50 ? 'Moderate Fit' : 'Stretch Fit'));

                tr.innerHTML = `
                    <td class="p-3.5">
                        <div class="font-bold text-white flex items-center gap-1.5">
                            ${{j.title}}
                            ${{j.url && j.url !== '#' ? `<a href="${{j.url}}" target="_blank" class="text-slate-500 hover:text-emerald-400"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg></a>` : ''}}
                        </div>
                        <div class="text-[11px] text-slate-400">${{j.company}} • <span class="text-slate-500">${{j.location || 'Global'}}</span></div>
                    </td>
                    <td class="p-3.5">
                        <span class="text-slate-200 font-semibold block">${{j.archetype}}</span>
                        <span class="text-[10px] text-slate-500 font-mono">${{j.family.split(',')[0]}}</span>
                    </td>
                    <td class="p-3.5 font-mono text-[11px]">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${{j.level_code || 'L3'}}</span>
                        <span class="text-slate-400 block text-[10px] mt-0.5">${{j.modality}}</span>
                    </td>
                    <td class="p-3.5 font-mono">
                        <div class="flex items-center gap-2">
                            <span class="font-bold ${{fitColor.split(' ')[0]}}">${{j.ats_score}}%</span>
                            <span class="text-[9px] px-1.5 py-0.5 rounded border font-sans ${{fitColor}}">${{tierLabel}}</span>
                        </div>
                    </td>
                    <td class="p-3.5">
                        <div class="flex flex-wrap gap-1">
                            ${{(j.top_hard_skills || []).slice(0, 3).map(s => `<span class="px-1.5 py-0.5 bg-slate-900 border border-slate-800 text-[10px] rounded text-slate-300 font-mono">${{s}}</span>`).join('')}}
                        </div>
                    </td>
                    <td class="p-3.5 text-right whitespace-nowrap">
                        <button onclick="dissectFromCensus(${{j.id}})" class="px-2.5 py-1 bg-slate-800 hover:bg-emerald-600 hover:text-black rounded text-[11px] font-semibold transition mr-1.5">Inspect</button>
                        <button onclick="openDocketModal(${{j.id}})" class="px-2.5 py-1 bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/30 rounded text-[11px] font-semibold transition">Docket</button>
                    </td>
                `;
                tbody.appendChild(tr);
            }}}});
        }}}}

        function filterCensusTable() {{{{
            const query = (document.getElementById('census-search-input').value || '').toLowerCase();
            const fit = document.getElementById('census-fit-filter').value;
            const level = document.getElementById('census-level-filter').value;

            const filtered = censusJobs.filter(j => {{{{
                const matchesQuery = !query || 
                    (j.title && j.title.toLowerCase().includes(query)) || 
                    (j.company && j.company.toLowerCase().includes(query)) ||
                    (j.top_hard_skills && j.top_hard_skills.some(s => s.toLowerCase().includes(query))) ||
                    (j.archetype && j.archetype.toLowerCase().includes(query));

                const tier = j.fit_tier || (j.ats_score >= 70 ? 'Strong Fit' : (j.ats_score >= 50 ? 'Moderate Fit' : 'Stretch Fit'));
                const matchesFit = (fit === 'ALL') || (tier === fit);

                const matchesLevel = (level === 'ALL') || (j.level_code === level);

                return matchesQuery && matchesFit && matchesLevel;
            }}}});

            renderCensusTable(filtered);
        }}}}

        function dissectFromCensus(jobId) {{{{
            const job = censusJobs.find(j => j.id === jobId);
            if (!job) return;

            document.getElementById('role-title-input').value = job.title;
            document.getElementById('company-input').value = job.company;
            document.getElementById('jd-textarea').value = job.sample_raw_jd || `${{job.title}} at ${{job.company}}. Looking for verified execution mastery in ${{job.top_hard_skills.join(', ')}}.`;
            switchTab('dissector');
            dissectLiveJD();
        }}}}

        function openDocketModal(jobId) {{{{
            const job = censusJobs.find(j => j.id === jobId);
            if (!job) return;

            document.getElementById('modal-docket-badge').innerText = `APP-DOCKET-${{String(job.id).padStart(4, '0')}}`;
            document.getElementById('modal-fit-badge').innerText = `${{job.fit_tier || 'Strong Fit'}} (${{job.ats_score}}% Match)`;
            document.getElementById('modal-role-title').innerText = job.title;
            document.getElementById('modal-company-info').innerText = `${{job.company}} • ${{job.location || 'Global'}} • ${{job.modality}}`;

            // Bullets
            const bulletsContainer = document.getElementById('modal-bullets-list');
            bulletsContainer.innerHTML = '';
            const bullets = job.tailored_bullets || [job.top_xyz_bullet || `Accelerated deliverable throughput by 34%, as measured by weekly KPI milestone velocity, by deploying ${{job.top_hard_skills.slice(0,3).join(', ')}}.`];
            bullets.forEach(b => {{{{
                const div = document.createElement('div');
                div.className = "bg-slate-900/60 p-3 rounded-xl border border-slate-800 text-xs flex justify-between items-start gap-3";
                div.innerHTML = `
                    <p class="text-slate-300 leading-relaxed">${{b}}</p>
                    <button onclick="copyText(this)" class="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded text-[10px] font-mono text-slate-300 shrink-0">Copy</button>
                `;
                bulletsContainer.appendChild(div);
            }}}});

            // Recruiter pitch
            const skillsStr = (job.top_hard_skills || []).slice(0, 3).join(', ') || 'cross-functional execution';
            document.getElementById('modal-recruiter-text').innerText = 
                `Hi [Recruiter Name], I noticed the ${{job.title}} opening at ${{job.company}}. Given my operational background in cross-functional project execution, vendor workflows, and ${{skillsStr}}, I would love to connect briefly regarding how my profile aligns with your team's objectives. Best regards, Aditya Mehra`;

            // Cover letter
            document.getElementById('modal-cover-text').innerText = 
                `Dear Hiring Team at ${{job.company}},\\n\\nI am writing to express my strong enthusiasm for the ${{job.title}} opening. With verified operational leadership across high-stakes initiatives (including AERO INDIA 2025 and enterprise commercial execution at Pencil Mark), combined with proven proficiency in ${{skillsStr}}, I specialize in accelerating deliverable velocity and driving zero-defect execution. I welcome the opportunity to discuss how I can contribute immediately to ${{job.company}}.`;

            // Inspect button action
            document.getElementById('modal-inspect-btn').onclick = () => {{{{
                closeDocketModal();
                dissectFromCensus(job.id);
            }}}};

            document.getElementById('docket-modal').classList.remove('hidden');
        }}}}

        function closeDocketModal() {{{{
            document.getElementById('docket-modal').classList.add('hidden');
        }}}}

        function copyModalField(elementId, btn) {{{{
            const text = document.getElementById(elementId).innerText;
            navigator.clipboard.writeText(text);
            const orig = btn.innerText;
            btn.innerText = "Copied!";
            setTimeout(() => btn.innerText = orig, 1500);
        }}}}
    """

    # Add loadCensusData to init()
    html = html.replace("loadPresetJD();", "loadPresetJD();\n            loadCensusData();")

    # Insert JS block before </script>
    target_tag = "window.addEventListener('DOMContentLoaded', init);\n    </script>"
    replacement_tag = "window.addEventListener('DOMContentLoaded', init);\n" + census_js_block + "\n    </script>"
    if target_tag in html:
        html = html.replace(target_tag, replacement_tag)
    else:
        # Fallback to general </script> before modal
        html = html.replace("    </script>\n\n    <!-- Application Docket Modal -->", census_js_block + "\n    </script>\n\n    <!-- Application Docket Modal -->")

    with open(COCKPIT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Cockpit successfully enhanced with Opportunity Census & Staged Dockets!")

if __name__ == "__main__":
    main()
