"""
Build standalone HTML Command Cockpit for Bangalore Enterprise & Unicorn Deals.
Scales to all 546 Accounts (Fortune 500 GCCs & Top Startups).
"""

import json
import re
from pathlib import Path

BASE_DIR = Path("E:/anti")
CRM_500_JSON = BASE_DIR / "data/bangalore_enterprise_crm_master_500.json"
CRM_BASE_JSON = BASE_DIR / "data/bangalore_enterprise_crm_master.json"
COCKPIT_HTML = BASE_DIR / "bangalore_enterprise_deal_cockpit.html"

def generate_cockpit():
    target_json = CRM_500_JSON if CRM_500_JSON.exists() else CRM_BASE_JSON
    print(f"Loading deal data from {target_json}...")
    
    with open(target_json, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    crm_data = []
    for r in raw_data:
        co = r.get("company") or r.get("company_name", "Enterprise Account")
        cat = r.get("type") or ("Fortune 500 GCC" if "GCC" in r.get("category", "") else "Bengaluru Tech Unicorn")
        campus = r.get("campus") or r.get("tech_corridor", "Bengaluru Tech Corridor")
        domain = r.get("domain") or r.get("business_domain", "Enterprise Systems")
        vector = r.get("service_vector") or r.get("primary_vector", "Enterprise LLM Evaluation Harness")
        contract = r.get("contract_inr") or r.get("contract_value_inr", 7500000)
        po = r.get("entry_po_inr") or r.get("entry_pilot_po_inr", 485000)
        leakage = r.get("est_annual_leakage_inr") or r.get("annual_leakage_inr", 28000000)
        bypass = r.get("procurement_bypass", "Sub-Threshold PO (< INR 5L)")
        safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', co).strip('_')
        dossier = r.get("dossier_file") or f"SOW_{safe_name}.md"

        crm_data.append({
            "company": co,
            "type": cat,
            "campus": campus,
            "domain": domain,
            "service_vector": vector,
            "contract_inr": contract,
            "entry_po_inr": po,
            "est_annual_leakage_inr": leakage,
            "procurement_bypass": bypass,
            "dossier_file": dossier
        })
        
    total_val = sum(r["contract_inr"] for r in crm_data)
    gcc_val = sum(r["contract_inr"] for r in crm_data if r["type"] == "Fortune 500 GCC")
    startup_val = sum(r["contract_inr"] for r in crm_data if r["type"] == "Bengaluru Tech Unicorn")
    gcc_count = sum(1 for r in crm_data if r["type"] == "Fortune 500 GCC")
    startup_count = sum(1 for r in crm_data if r["type"] == "Bengaluru Tech Unicorn")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bengaluru Enterprise & Unicorn Commercial Deal Cockpit ({len(crm_data)} Accounts)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        code, pre {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-30 px-6 py-4">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 tracking-wide uppercase">OMEGA ∞ Commercial OS</span>
                    <span class="text-xs text-slate-400">Bengaluru GCC & Unicorn Engine ({len(crm_data)} Targets)</span>
                </div>
                <h1 class="text-2xl font-black text-white tracking-tight mt-1">Bangalore Enterprise Deal & Outbound Cockpit</h1>
            </div>
            <div class="flex items-center gap-3">
                <a href="docs/APEX_BANGALORE_ENTERPRISE_REVENUE_PROMPT.md" target="_blank" class="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center gap-2">
                    <span>⚡ Apex Prompt</span>
                </a>
                <a href="docs/BANGALORE_FORTUNE500_STARTUP_COMMERCIAL_BLUEPRINT.md" target="_blank" class="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
                    <span>📘 Master Blueprint</span>
                </a>
                <a href="omega_supreme_command_center.html" class="px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-black font-bold transition">
                    <span>👑 Supreme Command</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">
        <!-- Top Stats Row -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Addressable Pipeline</span>
                <h3 class="text-2xl font-black text-emerald-400 mt-1">₹{(total_val/10000000):.1f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">{len(crm_data)} Curated Accounts</p>
            </div>
            <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Fortune 500 GCCs</span>
                <h3 class="text-2xl font-black text-blue-400 mt-1">₹{(gcc_val/10000000):.1f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">{gcc_count} Global Tech Hubs</p>
            </div>
            <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Bengaluru Unicorns</span>
                <h3 class="text-2xl font-black text-purple-400 mt-1">₹{(startup_val/10000000):.1f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">{startup_count} Tech Startups</p>
            </div>
            <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Discretionary Sub-PO Entry</span>
                <h3 class="text-2xl font-black text-amber-400 mt-1">&lt; ₹5,00,000</h3>
                <p class="text-xs text-slate-500 mt-1">Zero Procurement Gridlock</p>
            </div>
        </div>

        <!-- Filter & Search Controls -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 mb-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2 w-full md:w-auto overflow-x-auto">
                <button onclick="filterType('ALL')" id="btn-ALL" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white">All Targets ({len(crm_data)})</button>
                <button onclick="filterType('Fortune 500 GCC')" id="btn-GCC" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Fortune 500 GCCs ({gcc_count})</button>
                <button onclick="filterType('Bengaluru Tech Unicorn')" id="btn-UNI" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Tech Unicorns ({startup_count})</button>
            </div>
            <div class="relative w-full md:w-80">
                <input type="text" id="search-box" oninput="searchTargets()" placeholder="Search company, tech park, domain, vector..." class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-4 py-2.5 focus:outline-none focus:border-indigo-500">
            </div>
        </div>

        <!-- Deal Cards Grid -->
        <div id="cards-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Dynamically populated -->
        </div>
    </main>

    <!-- Pitch Modal -->
    <div id="pitch-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                <div>
                    <h3 id="modal-title" class="text-lg font-bold text-white">Company Name</h3>
                    <p id="modal-subtitle" class="text-xs text-indigo-400 mt-0.5">Vector</p>
                </div>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            
            <div class="space-y-4">
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <label class="text-xs font-semibold text-slate-300 uppercase">LinkedIn InMail / DM Copy</label>
                        <button onclick="copyText('modal-dm')" class="text-xs text-indigo-400 hover:text-indigo-300">Copy DM</button>
                    </div>
                    <textarea id="modal-dm" readonly class="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-lg p-3 h-28 focus:outline-none"></textarea>
                </div>
                
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <label class="text-xs font-semibold text-slate-300 uppercase">Executive Cold Email (Touch 1)</label>
                        <button onclick="copyText('modal-email')" class="text-xs text-indigo-400 hover:text-indigo-300">Copy Email</button>
                    </div>
                    <textarea id="modal-email" readonly class="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-lg p-3 h-40 focus:outline-none"></textarea>
                </div>
                
                <div class="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                    <div>
                        <p class="text-xs font-semibold text-slate-400">Sub-Threshold Entry PO</p>
                        <p id="modal-po" class="text-sm font-bold text-amber-400">₹4,85,000</p>
                    </div>
                    <div class="text-right">
                        <p class="text-xs font-semibold text-slate-400">Annual Retainer</p>
                        <p id="modal-retainer" class="text-sm font-bold text-emerald-400">₹85,00,000</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const CRM_DATA = {json.dumps(crm_data, indent=2)};
        let currentFilter = 'ALL';

        function renderCards(data) {{
            const container = document.getElementById('cards-container');
            container.innerHTML = '';
            
            data.forEach((item, idx) => {{
                const isGCC = item.type === 'Fortune 500 GCC';
                const badgeClass = isGCC ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-purple-500/10 text-purple-400 border-purple-500/20';
                
                const card = document.createElement('div');
                card.className = 'bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition rounded-2xl p-5 flex flex-col justify-between shadow-lg';
                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-2">
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded uppercase tracking-wide border ${{badgeClass}}">${{item.type}}</span>
                            <span class="text-xs font-extrabold text-emerald-400">₹${{(item.contract_inr/100000).toFixed(1)}}L Retainer</span>
                        </div>
                        <h4 class="text-base font-bold text-white tracking-tight">${{item.company}}</h4>
                        <p class="text-xs text-slate-400 mt-1 line-clamp-1">📍 ${{item.campus}}</p>
                        
                        <div class="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase font-semibold">Service Vector</span>
                                <p class="text-xs text-slate-300 font-medium">${{item.service_vector}}</p>
                            </div>
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase font-semibold">Procurement Bypass Rail</span>
                                <p class="text-xs text-amber-300/90 font-medium">${{item.procurement_bypass}}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-5 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                        <div>
                            <span class="text-[10px] text-slate-500 uppercase">Entry PO</span>
                            <p class="text-xs font-bold text-amber-400">₹${{(item.entry_po_inr/100000).toFixed(2)}}L</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <button onclick="openModal(${{idx}})" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Get Outreach</button>
                            <a href="docs/contracts_and_sows/${{item.dossier_file}}" target="_blank" class="px-2 py-1.5 text-xs text-slate-400 hover:text-slate-200 border border-slate-800 rounded-lg">Doc</a>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function filterType(type) {{
            currentFilter = type;
            document.querySelectorAll('.filter-btn').forEach(b => b.className = 'filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700');
            if (type === 'ALL') document.getElementById('btn-ALL').className = 'filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white';
            if (type === 'Fortune 500 GCC') document.getElementById('btn-GCC').className = 'filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white';
            if (type === 'Bengaluru Tech Unicorn') document.getElementById('btn-UNI').className = 'filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white';
            
            searchTargets();
        }}

        function searchTargets() {{
            const query = document.getElementById('search-box').value.toLowerCase();
            const filtered = CRM_DATA.filter(item => {{
                const matchesType = currentFilter === 'ALL' || item.type === currentFilter;
                const matchesQuery = item.company.toLowerCase().includes(query) ||
                                     item.campus.toLowerCase().includes(query) ||
                                     item.domain.toLowerCase().includes(query) ||
                                     item.service_vector.toLowerCase().includes(query);
                return matchesType && matchesQuery;
            }});
            renderCards(filtered);
        }}

        function openModal(idx) {{
            const item = CRM_DATA[idx];
            document.getElementById('modal-title').textContent = item.company;
            document.getElementById('modal-subtitle').textContent = `${{item.type}} • ${{item.domain}}`;
            document.getElementById('modal-po').textContent = `₹${{item.entry_po_inr.toLocaleString('en-IN')}} (< ₹5L Sub-Threshold)`;
            document.getElementById('modal-retainer').textContent = `₹${{item.contract_inr.toLocaleString('en-IN')}} / Year`;
            
            const campusShort = item.campus.split(',')[0];
            const domainShort = item.domain.split('&')[0].trim();
            
            const dmCopy = `Hi [First Name],\\n\\nNoticed your leadership in scaling ${{domainShort}} at ${{campusShort}}.\\n\\nIn our audit of similar Bengaluru operations, between 10% and 18% of efficiency leaks through ${{item.service_vector.toLowerCase()}}.\\n\\nWe built a specialized diagnostic harness that resolves this in 14 days under discretionary departmental spend (₹${{(item.entry_po_inr/100000).toFixed(2)}}L). We recently unlocked ₹1.2 Cr in recovered credits for a peer team on Outer Ring Road.\\n\\nCould I share a 1-page sample framework this Thursday?\\n\\nBest,\\nAditya Mehra`;
            
            const emailCopy = `Subject: Eliminating ${{domainShort}} leakage at ${{item.company}}\\n\\nHi [First Name],\\n\\nAs ${{item.company}} accelerates its Bengaluru center, one silent financial drain leaders regularly confront is ${{item.service_vector.toLowerCase()}}.\\n\\nRather than requiring a lengthy 6-month global vendor onboarding cycle, we execute a rapid 14-day retrospective diagnostic under discretionary departmental spend (₹${{item.entry_po_inr.toLocaleString('en-IN')}}).\\n\\nIf our diagnostic identifies less than ₹30 Lakhs in verified operational waste or recovery potential, there is zero continuing obligation.\\n\\nWould you be open to reviewing a 1-page sample diagnostic report from a fellow Bengaluru technology center?\\n\\nSincerely,\\nAditya Mehra\\nPrincipal Commercial Architect, Bengaluru`;
            
            document.getElementById('modal-dm').value = dmCopy;
            document.getElementById('modal-email').value = emailCopy;
            document.getElementById('pitch-modal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('pitch-modal').classList.add('hidden');
        }}

        function copyText(id) {{
            const el = document.getElementById(id);
            el.select();
            navigator.clipboard.writeText(el.value);
            alert("Copied to clipboard!");
        }}

        // Initial render
        renderCards(CRM_DATA);
    </script>
</body>
</html>
"""
    COCKPIT_HTML.write_text(html, encoding="utf-8")
    print(f"Generated standalone interactive Cockpit with {len(crm_data)} accounts: {COCKPIT_HTML}")

if __name__ == "__main__":
    generate_cockpit()
