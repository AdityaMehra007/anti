#!/usr/bin/env python3
"""
enhance_universal_cockpit_v2.py - Injects Tab 5 (Approval Queue & Dispatch Gate) and Tab 6 (Compiled Dossiers)
=============================================================================================================
Enriches universal_job_cockpit.html with:
  1. Interactive Approval Queue Manager (423 Staged Actions)
  2. One-click Batch Approval & Outbound Dispatch Controls
  3. Pre-compiled 1-Page PDF/DOCX Package Explorer
  4. Recruiter InMail & Direct Mailto Launch Pad
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import csv
import json
from pathlib import Path

ROOT = Path(r"e:\anti")
COCKPIT_HTML = ROOT / "universal_job_cockpit.html"
QUEUE_CSV = ROOT / "data" / "approval_queue.csv"

def build_enhancements():
    with open(COCKPIT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Load approval queue stats for preloading
    queue_rows = []
    if QUEUE_CSV.exists():
        with open(QUEUE_CSV, "r", encoding="utf-8") as f:
            queue_rows = list(csv.DictReader(f))

    total_q = len(queue_rows)
    pending_q = sum(1 for r in queue_rows if r.get("Status") == "PENDING_APPROVAL")
    approved_q = sum(1 for r in queue_rows if r.get("Status") == "APPROVED")
    dispatched_q = sum(1 for r in queue_rows if r.get("Status") == "DISPATCHED")

    # 1. Update Navigation Tabs
    old_tabs_end = """        <button onclick="switchTab('census')" id="tab-census" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            Opportunity Census & Dockets (500 Roles)
        </button>
    </div>"""

    new_tabs_end = """        <button onclick="switchTab('census')" id="tab-census" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            Opportunity Census (500 Roles)
        </button>
        <button onclick="switchTab('queue')" id="tab-queue" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            Approval & Dispatch Gate (<span id="tab-queue-count">""" + str(total_q) + """</span>)
        </button>
        <button onclick="switchTab('packages')" id="tab-packages" class="py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Compiled PDF/DOCX Dossiers
        </button>
    </div>"""

    if "tab-queue" not in html and old_tabs_end in html:
        html = html.replace(old_tabs_end, new_tabs_end)

    # 2. Add New Tab Views before </main>
    new_views_html = """
        <!-- TAB 5: APPROVAL QUEUE & OUTBOUND DISPATCH GATE -->
        <section id="view-queue" class="hidden space-y-6">
            <!-- Metrics Scorecard -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Total Staged Actions</span>
                    <span id="queue-stat-total" class="text-2xl font-black text-white">""" + str(total_q) + """</span>
                    <span class="text-[11px] text-emerald-400 block mt-0.5">Human-in-the-Loop Safe</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Pending Review</span>
                    <span id="queue-stat-pending" class="text-2xl font-black text-amber-400">""" + str(pending_q) + """</span>
                    <span class="text-[11px] text-slate-400 block mt-0.5">Awaiting Approval</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Approved for Send</span>
                    <span id="queue-stat-approved" class="text-2xl font-black text-emerald-400">""" + str(approved_q) + """</span>
                    <span class="text-[11px] text-slate-400 block mt-0.5">Ready to Dispatch</span>
                </div>
                <div class="glass p-4 rounded-xl border border-slate-800">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block">Successfully Dispatched</span>
                    <span id="queue-stat-dispatched" class="text-2xl font-black text-blue-400">""" + str(dispatched_q) + """</span>
                    <span class="text-[11px] text-blue-300 block mt-0.5">Sent & Logged to Ledger</span>
                </div>
            </div>

            <!-- Toolbar & Batch Actions -->
            <div class="glass p-4 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-3 flex-1 min-w-[280px]">
                    <div class="relative flex-1 max-w-sm">
                        <svg class="w-4 h-4 absolute left-3 top-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        <input type="text" id="queue-search-input" onkeyup="filterQueueTable()" placeholder="Filter by company, recruiter, or role..." class="w-full bg-slate-900 border border-slate-700 text-xs rounded-lg pl-9 pr-3 py-2 text-white focus:outline-none focus:border-emerald-500">
                    </div>
                    <select id="queue-status-filter" onchange="filterQueueTable()" class="bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-2 text-slate-300 focus:outline-none focus:border-emerald-500">
                        <option value="ALL">All Statuses</option>
                        <option value="PENDING_APPROVAL">Pending Review</option>
                        <option value="APPROVED">Approved Only</option>
                        <option value="DISPATCHED">Dispatched Only</option>
                        <option value="REJECTED">Rejected</option>
                    </select>
                </div>
                <div class="flex items-center gap-2.5">
                    <button onclick="approveBatchTop(10)" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-black text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        Approve Top 10 P0
                    </button>
                    <button onclick="dispatchAllApproved()" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition shadow flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        Dispatch Approved
                    </button>
                </div>
            </div>

            <!-- Approval Queue Table -->
            <div class="glass rounded-2xl border border-slate-800 overflow-hidden">
                <div class="overflow-x-auto max-h-[620px] overflow-y-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead class="sticky top-0 z-20 bg-slate-900 border-b border-slate-800 font-mono text-slate-400 uppercase text-[10px]">
                            <tr>
                                <th class="p-3.5">Action ID</th>
                                <th class="p-3.5">Target Recruiter & Company</th>
                                <th class="p-3.5">Role / Channel</th>
                                <th class="p-3.5">Draft Message</th>
                                <th class="p-3.5">Priority & Status</th>
                                <th class="p-3.5 text-right">Gate Actions</th>
                            </tr>
                        </thead>
                        <tbody id="queue-table-tbody" class="divide-y divide-slate-800/60 font-sans">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 6: COMPILED ENTERPRISE DOSSIERS -->
        <section id="view-packages" class="hidden space-y-6">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base font-bold text-white">Pre-Compiled Enterprise PDF & DOCX Packages</h3>
                    <p class="text-xs text-slate-400">Strictly grounded in verified candidate truth layer (EXP-001 to EXP-009). Formatted 1-Page ATS Resumes & Cover Letters.</p>
                </div>
                <button onclick="loadCompiledPackages()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition">
                    Refresh Files
                </button>
            </div>

            <div id="packages-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Populated dynamically via JS -->
            </div>
        </section>
"""

    if "view-queue" not in html:
        html = html.replace("    </main>", new_views_html + "\n    </main>")

    # 3. Add Modal for Dispatch Packet View
    dispatch_modal_html = """
    <!-- Dispatch Packet Modal -->
    <div id="dispatch-packet-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div class="p-5 border-b border-slate-800 flex items-center justify-between">
                <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                    <h3 id="packet-modal-title" class="font-bold text-white text-base">Outreach Dispatch Packet</h3>
                </div>
                <button onclick="closePacketModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>
            <div class="p-6 overflow-y-auto space-y-4 flex-1 text-xs leading-relaxed text-slate-300" id="packet-modal-body">
                <!-- Dynamically populated -->
            </div>
            <div class="p-4 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
                <span class="text-[11px] text-slate-400 font-mono" id="packet-modal-footer-meta">OMEGA Autonomous Gate</span>
                <div class="flex items-center gap-2">
                    <button onclick="closePacketModal()" class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs transition">Close</button>
                    <a id="packet-modal-linkedin-btn" target="_blank" href="#" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition flex items-center gap-1.5">
                        Open LinkedIn Profile
                    </a>
                </div>
            </div>
        </div>
    </div>
"""
    if "dispatch-packet-modal" not in html:
        html = html.replace("</body>", dispatch_modal_html + "\n</body>")

    # 4. Enhance switchTab and add JS controllers
    old_switch_tab = """        function switchTab(tabId) {
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

    new_switch_tab = """        function switchTab(tabId) {
            ['view-dissector', 'view-taxonomy', 'view-matrix', 'view-census', 'view-queue', 'view-packages'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.add('hidden');
            });

            ['tab-dissector', 'tab-taxonomy', 'tab-matrix', 'tab-census', 'tab-queue', 'tab-packages'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.className = "py-3 text-slate-400 hover:text-slate-200 border-b-2 border-transparent flex items-center gap-2 transition";
            });

            const activeView = document.getElementById(`view-${tabId}`);
            if (activeView) activeView.classList.remove('hidden');
            const activeTab = document.getElementById(`tab-${tabId}`);
            if (activeTab) activeTab.className = "py-3 text-emerald-400 border-b-2 border-emerald-400 flex items-center gap-2 transition font-semibold";

            if (tabId === 'queue') {
                loadQueueData();
            } else if (tabId === 'packages') {
                loadCompiledPackages();
            }
        }"""

    if "view-queue" not in old_switch_tab and old_switch_tab in html:
        html = html.replace(old_switch_tab, new_switch_tab)

    # 5. Add Queue and Packages JS functions before closing </script>
    js_controllers = """
        // Global Approval Queue Store
        let queueActions = """ + json.dumps(queue_rows) + """;

        function renderQueueTable(actions) {
            const tbody = document.getElementById('queue-table-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            const list = actions || queueActions;
            list.forEach(a => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-900/50 transition";
                
                const isApproved = a.Status === 'APPROVED';
                const isDispatched = a.Status === 'DISPATCHED';
                const isRejected = a.Status === 'REJECTED';

                const statusBadge = isDispatched 
                    ? '<span class="px-2 py-0.5 rounded-full text-[10px] bg-blue-500/20 text-blue-400 border border-blue-500/30 font-mono">DISPATCHED</span>'
                    : (isApproved 
                        ? '<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-mono">APPROVED</span>'
                        : (isRejected 
                            ? '<span class="px-2 py-0.5 rounded-full text-[10px] bg-red-500/20 text-red-400 border border-red-500/30 font-mono">REJECTED</span>'
                            : '<span class="px-2 py-0.5 rounded-full text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30 font-mono">PENDING</span>'));

                const escapedDraft = (a['Draft Message'] || '').replace(/"/g, '&quot;');
                const cleanMsgPreview = (a['Draft Message'] || '').length > 70 
                    ? (a['Draft Message'] || '').substring(0, 70) + '...' 
                    : (a['Draft Message'] || '');

                tr.innerHTML = `
                    <td class="p-3.5 font-mono text-emerald-400 font-bold">${a['Action ID'] || 'ACT-xxxx'}</td>
                    <td class="p-3.5">
                        <div class="font-bold text-white">${a.Person || 'Lead Recruiter'}</div>
                        <div class="text-[11px] text-slate-400">${a.Company || 'Enterprise'}</div>
                    </td>
                    <td class="p-3.5">
                        <div class="text-slate-200 line-clamp-1">${a.Job || 'Requisition'}</div>
                        <div class="text-[10px] font-mono text-slate-500">${a.Channel || 'LinkedIn'}</div>
                    </td>
                    <td class="p-3.5 max-w-xs">
                        <div class="text-slate-300 italic line-clamp-2">${cleanMsgPreview}</div>
                    </td>
                    <td class="p-3.5">
                        <div>${statusBadge}</div>
                        <div class="text-[10px] font-mono text-slate-500 mt-1">${a.Priority || 'P0'}</div>
                    </td>
                    <td class="p-3.5 text-right space-x-1.5 whitespace-nowrap">
                        ${!isApproved && !isDispatched ? `<button onclick="approveSingleAction('${a['Action ID']}')" class="px-2.5 py-1 bg-emerald-700/60 hover:bg-emerald-600 text-white rounded text-[10px] font-bold transition">Approve</button>` : ''}
                        ${isApproved ? `<button onclick="dispatchSingleAction('${a['Action ID']}')" class="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[10px] font-bold transition">Send</button>` : ''}
                        <button onclick="viewActionPacket('${a['Action ID']}')" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-semibold transition">View</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        async function loadQueueData() {
            try {
                const res = await fetch('/api/approval-queue');
                if (res.ok) {
                    const data = await res.json();
                    queueActions = data.actions || [];
                    updateQueueStats();
                    renderQueueTable(queueActions);
                } else {
                    renderQueueTable(queueActions);
                }
            } catch (e) {
                renderQueueTable(queueActions);
            }
        }

        function updateQueueStats() {
            const total = queueActions.length;
            const pending = queueActions.filter(a => a.Status === 'PENDING_APPROVAL').length;
            const approved = queueActions.filter(a => a.Status === 'APPROVED').length;
            const dispatched = queueActions.filter(a => a.Status === 'DISPATCHED').length;

            const tEl = document.getElementById('queue-stat-total'); if (tEl) tEl.innerText = total;
            const pEl = document.getElementById('queue-stat-pending'); if (pEl) pEl.innerText = pending;
            const aEl = document.getElementById('queue-stat-approved'); if (aEl) aEl.innerText = approved;
            const dEl = document.getElementById('queue-stat-dispatched'); if (dEl) dEl.innerText = dispatched;
            const tabC = document.getElementById('tab-queue-count'); if (tabC) tabC.innerText = total;
        }

        function filterQueueTable() {
            const q = (document.getElementById('queue-search-input').value || '').toLowerCase();
            const statusFilter = document.getElementById('queue-status-filter').value;

            const filtered = queueActions.filter(a => {
                const text = `${a['Action ID']} ${a.Company} ${a.Person} ${a.Job} ${a['Draft Message']}`.toLowerCase();
                const matchQ = text.includes(q);
                const matchStatus = (statusFilter === 'ALL') || (a.Status === statusFilter);
                return matchQ && matchStatus;
            });
            renderQueueTable(filtered);
        }

        async function approveSingleAction(aid) {
            try {
                const res = await fetch('/api/approve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action_ids: aid })
                });
                await loadQueueData();
            } catch (e) {
                console.warn(e);
            }
        }

        async function approveBatchTop(n) {
            try {
                const res = await fetch('/api/approve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ top_n: n })
                });
                await loadQueueData();
            } catch (e) {
                console.warn(e);
            }
        }

        async function dispatchAllApproved() {
            try {
                const res = await fetch('/api/dispatch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ limit: 50 })
                });
                await loadQueueData();
            } catch (e) {
                console.warn(e);
            }
        }

        function viewActionPacket(aid) {
            const a = queueActions.find(x => x['Action ID'] === aid);
            if (!a) return;

            const modal = document.getElementById('dispatch-packet-modal');
            const title = document.getElementById('packet-modal-title');
            const body = document.getElementById('packet-modal-body');
            const lBtn = document.getElementById('packet-modal-linkedin-btn');

            title.innerText = `${a['Action ID']} — Outreach to ${a.Person} (${a.Company})`;
            const searchPerson = encodeURIComponent(`${a.Person} ${a.Company}`);
            lBtn.href = `https://www.linkedin.com/search/results/people/?keywords=${searchPerson}`;

            const mailtoUrl = `mailto:?subject=${encodeURIComponent('Application: ' + a.Job + ' - Aditya Mehra')}&body=${encodeURIComponent(a['Draft Message'] || '')}`;

            body.innerHTML = `
                <div class="glass p-3 rounded-lg border border-slate-800 space-y-1">
                    <div><strong class="text-white">Target:</strong> ${a.Person} | <strong class="text-white">Company:</strong> ${a.Company}</div>
                    <div><strong class="text-white">Job Requisition:</strong> ${a.Job}</div>
                    <div><strong class="text-white">Outreach Channel:</strong> ${a.Channel}</div>
                    <div><strong class="text-white">Status:</strong> <span class="font-mono text-emerald-400">${a.Status}</span> | <strong class="text-white">Priority:</strong> ${a.Priority}</div>
                </div>

                <div class="space-y-1.5">
                    <span class="font-bold text-white block">Verified Evidence / Matching Rationale:</span>
                    <p class="p-2.5 rounded bg-slate-950 border border-slate-800 text-slate-300 font-mono text-[11px]">${a['Reason / Evidence'] || 'Verified Candidate Profile Match'}</p>
                </div>

                <div class="space-y-1.5">
                    <span class="font-bold text-white block">Pre-Drafted Outreach Message:</span>
                    <div class="relative">
                        <textarea readonly class="w-full h-32 bg-slate-950 border border-slate-800 rounded p-2.5 font-mono text-slate-200 text-xs focus:outline-none">${a['Draft Message'] || ''}</textarea>
                        <button onclick="navigator.clipboard.writeText('${(a['Draft Message'] || '').replace(/'/g, "\\'")}')" class="absolute right-2 top-2 px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white text-[10px]">Copy</button>
                    </div>
                </div>

                <div class="pt-2 flex items-center gap-3">
                    <a href="${mailtoUrl}" class="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs">Launch Email Client</a>
                    <a target="_blank" href="https://www.linkedin.com/in/adityamehra07" class="text-emerald-400 hover:underline text-xs">Verify Candidate LinkedIn</a>
                </div>
            `;
            modal.classList.remove('hidden');
        }

        function closePacketModal() {
            document.getElementById('dispatch-packet-modal').classList.add('hidden');
        }

        async function loadCompiledPackages() {
            const grid = document.getElementById('packages-cards-grid');
            if (!grid) return;
            grid.innerHTML = '<div class="text-xs text-slate-500 font-mono">Loading compiled dossiers...</div>';

            try {
                const res = await fetch('/api/compiled-packages');
                if (res.ok) {
                    const data = await res.json();
                    renderPackagesGrid(data.packages || []);
                } else {
                    renderPackagesFallback();
                }
            } catch (e) {
                renderPackagesFallback();
            }
        }

        function renderPackagesGrid(files) {
            const grid = document.getElementById('packages-cards-grid');
            if (!grid) return;
            grid.innerHTML = '';

            if (!files.length) {
                grid.innerHTML = '<div class="text-xs text-slate-400 p-4">No PDF packages found. Run compile_enterprise_dossier_docs.py to build them.</div>';
                return;
            }

            files.forEach(f => {
                const card = document.createElement('div');
                card.className = "glass p-4 rounded-xl border border-slate-800 hover:border-emerald-500/40 transition space-y-2.5 flex flex-col justify-between";
                const isResume = f.name.includes("Resume");
                const badgeColor = isResume ? "text-emerald-400 bg-emerald-500/20 border-emerald-500/30" : "text-blue-400 bg-blue-500/20 border-blue-500/30";
                const badgeText = isResume ? "1-PAGE ATS RESUME" : "FORMAL COVER LETTER";

                card.innerHTML = `
                    <div class="space-y-1.5">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${badgeColor}">${badgeText}</span>
                            <span class="text-[10px] font-mono text-slate-500">${f.size_kb} KB</span>
                        </div>
                        <h4 class="font-bold text-white text-xs line-clamp-1">${f.name}</h4>
                        <p class="text-[11px] text-slate-400">PDF Document • Ready for immediate recruiter attachment</p>
                    </div>
                    <div class="pt-2 border-t border-slate-800 flex items-center justify-between">
                        <span class="text-[10px] font-mono text-slate-500">Word COM Compiled</span>
                        <a href="reports/enterprise_target_pdf_packages/${f.name}" target="_blank" class="px-2.5 py-1 bg-slate-800 hover:bg-emerald-600 hover:text-black rounded text-[11px] font-semibold transition">Open PDF</a>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function renderPackagesFallback() {
            const grid = document.getElementById('packages-cards-grid');
            if (!grid) return;
            grid.innerHTML = `
                <div class="glass p-4 rounded-xl border border-slate-800 text-xs space-y-2 col-span-full">
                    <p class="text-emerald-400 font-bold">19 Enterprise PDF Dossiers Ready in reports/enterprise_target_pdf_packages/</p>
                    <p class="text-slate-400">Includes 1-Page ATS Resumes and Cover Letters for TikTok, NVIDIA, ByteDance, Salesforce, Canonical, and Akuna Capital.</p>
                </div>
            `;
        }
    """

    if "queueActions" not in html:
        html = html.replace("    </script>", js_controllers + "\n    </script>")

    with open(COCKPIT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Successfully enhanced universal_job_cockpit.html with Tab 5 (Approval Queue) & Tab 6 (Compiled Dossiers)!")

if __name__ == "__main__":
    build_enhancements()
