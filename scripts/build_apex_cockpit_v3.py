"""
Build Supreme Version 3 of Bangalore Enterprise Deal Cockpit
Features:
- 100-Account Pipeline with LocalStorage Persistence for Pipeline Stages
- Direct CSV Export of the Outbound Dispatch Queue
- Interactive Collateral Library (All 7 Executive 1-Pagers viewable in modal)
- Live Interactive Diagnostic Calculators (Vendor SLA, LLM FinOps)
- Legal Contracts Viewer
- Apex Enterprise Prompt Terminal
"""

import json
from pathlib import Path

BASE_DIR = Path("e:/anti")
CRM_JSON = BASE_DIR / "data/bangalore_enterprise_crm_master_100.json"
QUEUE_CSV = BASE_DIR / "data/outbound_dispatch_queue.csv"
COLLATERAL_DIR = BASE_DIR / "docs/collateral"
COCKPIT_HTML = BASE_DIR / "bangalore_enterprise_deal_cockpit.html"

def load_collaterals():
    collaterals = {}
    for f in COLLATERAL_DIR.glob("*.md"):
        collaterals[f.stem] = f.read_text(encoding="utf-8")
    return collaterals

def build_cockpit_v3():
    with open(CRM_JSON, "r", encoding="utf-8") as f:
        crm_data = json.load(f)
        
    collaterals = load_collaterals()
    
    total_val = sum(r["contract_inr"] for r in crm_data)
    gcc_val = sum(r["contract_inr"] for r in crm_data if r["type"] == "Fortune 500 GCC")
    startup_val = sum(r["contract_inr"] for r in crm_data if r["type"] == "Bengaluru Tech Unicorn")
    gcc_count = len([r for r in crm_data if r["type"] == "Fortune 500 GCC"])
    startup_count = len([r for r in crm_data if r["type"] == "Bengaluru Tech Unicorn"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bengaluru Enterprise Commercial Command Platform (OMEGA ∞ v3)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        code, pre {{ font-family: 'JetBrains Mono', monospace; }}
        .tab-btn.active {{
            background-color: #4f46e5;
            color: #ffffff;
            border-color: #6366f1;
        }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
    <!-- Top Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40 px-6 py-4">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-2.5 py-0.5 text-[10px] font-black rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 uppercase tracking-wider">OMEGA ∞ Commercial OS v3</span>
                    <span class="text-xs text-slate-400">Bengaluru Fortune 500 GCC & Unicorn Operating System</span>
                </div>
                <h1 class="text-2xl font-black text-white tracking-tight mt-1">Bangalore Enterprise Commercial Command Cockpit</h1>
            </div>
            <!-- Global Tab Navigation -->
            <div class="flex flex-wrap items-center gap-2 bg-slate-950/80 p-1.5 rounded-xl border border-slate-800">
                <button onclick="switchTab('pipeline')" id="tab-nav-pipeline" class="tab-btn active px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-300 hover:text-white transition">📊 Deal Pipeline (100)</button>
                <button onclick="switchTab('collateral')" id="tab-nav-collateral" class="tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-300 hover:text-white transition">📑 Collateral Library (7)</button>
                <button onclick="switchTab('calculators')" id="tab-nav-calculators" class="tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-300 hover:text-white transition">🧮 Live Diagnostic Calculators</button>
                <button onclick="switchTab('contracts')" id="tab-nav-contracts" class="tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-300 hover:text-white transition">📜 Legal Contracts Hub</button>
                <button onclick="switchTab('apex-prompt')" id="tab-nav-apex-prompt" class="tab-btn px-3.5 py-1.5 text-xs font-semibold rounded-lg text-slate-300 hover:text-white transition">⚡ Apex Prompt</button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        <!-- Top Metrics Bar -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Tracked Pipeline</p>
                <h3 class="text-3xl font-extrabold text-emerald-400 mt-2">₹{total_val/10000000:.2f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">~${total_val/83.5:,.0f} USD (100 Tier-1 Accounts)</p>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Fortune 500 GCC Hubs</p>
                <h3 class="text-3xl font-extrabold text-blue-400 mt-2">₹{gcc_val/10000000:.2f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">{gcc_count} Global Capability Centers</p>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Top Tech Unicorns</p>
                <h3 class="text-3xl font-extrabold text-purple-400 mt-2">₹{startup_val/10000000:.2f} Cr</h3>
                <p class="text-xs text-slate-500 mt-1">{startup_count} High-Growth Tech Titans</p>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Sub-Threshold Entry POs</p>
                <h3 class="text-3xl font-extrabold text-amber-400 mt-2">&lt; ₹5.00 Lakhs</h3>
                <p class="text-xs text-slate-500 mt-1">14-Day Discretionary Sign-off</p>
            </div>
        </div>

        <!-- ================= TAB 1: DEAL PIPELINE ================= -->
        <section id="tab-pipeline" class="tab-content block">
            <!-- Filter & Search Controls -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 mb-6 flex flex-col md:flex-row items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
                    <button onclick="filterType('ALL')" id="btn-ALL" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white">All Targets (100)</button>
                    <button onclick="filterType('Fortune 500 GCC')" id="btn-GCC" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Fortune 500 GCCs ({gcc_count})</button>
                    <button onclick="filterType('Bengaluru Tech Unicorn')" id="btn-UNI" class="filter-btn px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Tech Unicorns ({startup_count})</button>
                    <a href="data/outbound_dispatch_queue.csv" download class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-600/30 transition flex items-center gap-1.5">
                        <span>📥</span> Export Dispatch CSV
                    </a>
                </div>
                <div class="relative w-full md:w-80">
                    <input type="text" id="search-box" oninput="searchTargets()" placeholder="Search company, tech park, domain, contact..." class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-4 py-2.5 focus:outline-none focus:border-indigo-500">
                </div>
            </div>

            <!-- Target Cards Grid -->
            <div id="cards-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Populated dynamically via JS -->
            </div>
        </section>

        <!-- ================= TAB 2: COLLATERAL LIBRARY ================= -->
        <section id="tab-collateral" class="tab-content hidden space-y-6">
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                <h3 class="text-lg font-bold text-white mb-2">Executive 1-Pager Teardowns & Collaterals</h3>
                <p class="text-xs text-slate-400 mb-6">High-converting 1-page PDF/Markdown attachments tailored to each of the 7 enterprise service vectors.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase">Vector 1</span>
                            <h4 class="text-base font-bold text-white mt-2">GCC Vendor SLA & SOW Leakage</h4>
                            <p class="text-xs text-slate-400 mt-2">Uncovering phantom developer hours, uncredited bench downtime, and SLA penalties.</p>
                        </div>
                        <button onclick="viewCollateral('GCC_VENDOR_SLA_AUDIT_EXECUTIVE_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase">Vector 2</span>
                            <h4 class="text-base font-bold text-white mt-2">Enterprise LLM Eval & Red-Teaming</h4>
                            <p class="text-xs text-slate-400 mt-2">Production reliability, regression gates, and EU AI Act / RBI compliance.</p>
                        </div>
                        <button onclick="viewCollateral('ENTERPRISE_LLM_EVAL_REDTEAM_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">Vector 3</span>
                            <h4 class="text-base font-bold text-white mt-2">Trade Finance UCP 600 Engine</h4>
                            <p class="text-xs text-slate-400 mt-2">Sub-minute documentary credit examination and Nostro/Vostro balancing.</p>
                        </div>
                        <button onclick="viewCollateral('UCP600_TRADE_FINANCE_AUTOMATION_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 uppercase">Vector 4</span>
                            <h4 class="text-base font-bold text-white mt-2">Founder's Office Tiger Team</h4>
                            <p class="text-xs text-slate-400 mt-2">Zero-risk special projects, operational drag elimination, and board updates.</p>
                        </div>
                        <button onclick="viewCollateral('FOUNDERS_OFFICE_TIGER_TEAM_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-pink-500/10 text-pink-400 border border-pink-500/20 uppercase">Vector 5</span>
                            <h4 class="text-base font-bold text-white mt-2">Autonomous B2B Outbound Engine</h4>
                            <p class="text-xs text-slate-400 mt-2">Guaranteed Fortune 500 VP discovery meetings for scaling B2B SaaS startups.</p>
                        </div>
                        <button onclick="viewCollateral('AUTONOMOUS_B2B_OUTBOUND_ENGINE_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase">Vector 6</span>
                            <h4 class="text-base font-bold text-white mt-2">Cloud & LLM FinOps Optimizer</h4>
                            <p class="text-xs text-slate-400 mt-2">Semantic caching and AWQ quantization cutting API bills by 40-70%.</p>
                        </div>
                        <button onclick="viewCollateral('CLOUD_LLM_FINOPS_ARBITRAGE_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 uppercase">Vector 7</span>
                            <h4 class="text-base font-bold text-white mt-2">BOT Engineering Pods</h4>
                            <p class="text-xs text-slate-400 mt-2">Pre-vetted senior pods (Rust, CUDA, AI Infra) with Month-12 enterprise absorption.</p>
                        </div>
                        <button onclick="viewCollateral('BOT_ENGINEERING_PODS_1PAGER')" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition">Read Teardown</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= TAB 3: LIVE DIAGNOSTIC CALCULATORS ================= -->
        <section id="tab-calculators" class="tab-content hidden space-y-8">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- Calculator 1: Vendor SLA & SOW Leakage -->
                <div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <span>🔍</span> GCC Vendor SLA & Leakage Calculator
                        </h3>
                        <span class="text-xs text-amber-400 font-semibold">25% Contingency Fee</span>
                    </div>
                    
                    <div class="space-y-4 text-xs">
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Contracted External Dev Headcount</label>
                                <span id="val-devs" class="text-indigo-400 font-bold">50 Devs</span>
                            </div>
                            <input type="range" id="input-devs" min="10" max="300" value="50" oninput="runSLACalc()" class="w-full accent-indigo-500">
                        </div>
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Blended Vendor Hourly Rate (INR)</label>
                                <span id="val-rate" class="text-indigo-400 font-bold">₹2,800/hr</span>
                            </div>
                            <input type="range" id="input-rate" min="1500" max="6000" step="100" value="2800" oninput="runSLACalc()" class="w-full accent-indigo-500">
                        </div>
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Estimated Bench / Ghost Hour Leakage (%)</label>
                                <span id="val-phantom" class="text-indigo-400 font-bold">15%</span>
                            </div>
                            <input type="range" id="input-phantom" min="5" max="35" value="15" oninput="runSLACalc()" class="w-full accent-indigo-500">
                        </div>
                        
                        <div class="mt-6 pt-4 border-t border-slate-800 bg-slate-950/70 rounded-xl p-4 space-y-2">
                            <div class="flex justify-between">
                                <span class="text-slate-400">Total Annual IT Vendor Spend:</span>
                                <span id="res-total-spend" class="font-bold text-slate-200">₹26.88 Cr</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-amber-400 font-semibold">Identified Annual SOW Leakage:</span>
                                <span id="res-leakage" class="font-bold text-amber-400">₹4.03 Cr</span>
                            </div>
                            <div class="flex justify-between pt-2 border-t border-slate-800/60">
                                <span class="text-emerald-400 font-bold">Your 25% Contingency Recovery Fee:</span>
                                <span id="res-fee" class="font-extrabold text-emerald-400 text-sm">₹1.01 Cr</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Calculator 2: Cloud & LLM Inference FinOps -->
                <div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <span>⚡</span> Cloud & LLM Inference FinOps Optimizer
                        </h3>
                        <span class="text-xs text-emerald-400 font-semibold">30% Contingency Fee</span>
                    </div>
                    
                    <div class="space-y-4 text-xs">
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Monthly LLM Queries (Customer + Internal)</label>
                                <span id="val-queries" class="text-indigo-400 font-bold">2,000,000</span>
                            </div>
                            <input type="range" id="input-queries" min="200000" max="10000000" step="200000" value="2000000" oninput="runFinOpsCalc()" class="w-full accent-indigo-500">
                        </div>
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Average Tokens per Query (Prompt + Output)</label>
                                <span id="val-tokens" class="text-indigo-400 font-bold">1,000 Tokens</span>
                            </div>
                            <input type="range" id="input-tokens" min="200" max="3000" step="100" value="1000" oninput="runFinOpsCalc()" class="w-full accent-indigo-500">
                        </div>
                        <div>
                            <div class="flex justify-between mb-1">
                                <label class="text-slate-300">Semantic Cache Hit Rate Potential (%)</label>
                                <span id="val-cache" class="text-indigo-400 font-bold">35%</span>
                            </div>
                            <input type="range" id="input-cache" min="15" max="60" value="35" oninput="runFinOpsCalc()" class="w-full accent-indigo-500">
                        </div>
                        
                        <div class="mt-6 pt-4 border-t border-slate-800 bg-slate-950/70 rounded-xl p-4 space-y-2">
                            <div class="flex justify-between">
                                <span class="text-slate-400">Current Annual LLM API Bill:</span>
                                <span id="res-finops-bill" class="font-bold text-slate-200">₹3.36 Cr</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-amber-400 font-semibold">Net Annual Cost Savings (Cache + Quantization):</span>
                                <span id="res-finops-savings" class="font-bold text-amber-400">₹1.85 Cr (55%)</span>
                            </div>
                            <div class="flex justify-between pt-2 border-t border-slate-800/60">
                                <span class="text-emerald-400 font-bold">Your 30% Shared-Savings Fee:</span>
                                <span id="res-finops-fee" class="font-extrabold text-emerald-400 text-sm">₹55.4 Lakhs</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= TAB 4: LEGAL CONTRACTS HUB ================= -->
        <section id="tab-contracts" class="tab-content hidden space-y-6">
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                <h3 class="text-lg font-bold text-white mb-2">Enterprise Legal & Fast-Track Contracting Hub</h3>
                <p class="text-xs text-slate-400 mb-6">Battle-tested contract templates customized for Bengaluru tech parks, SEZ units, and Indian tax laws (SAC 998313/998314, GST 18% domestic vs 0% Export with LUT).</p>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase">Master Agreement</span>
                            <h4 class="text-base font-bold text-white mt-2">Master Services Agreement (MSA)</h4>
                            <p class="text-xs text-slate-400 mt-2">Full enterprise tech consulting agreement with IP assignment, Net-15 terms, confidentiality, and SEZ zero-rated supply clauses.</p>
                        </div>
                        <a href="docs/contracts_and_sows/MASTER_SERVICES_AGREEMENT_TEMPLATE.md" target="_blank" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-center transition">View MSA Contract</a>
                    </div>
                    
                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase">Fast-Track SOW</span>
                            <h4 class="text-base font-bold text-white mt-2">Sub-Threshold Pilot SOW (&lt; ₹5L)</h4>
                            <p class="text-xs text-slate-400 mt-2">Priced at exactly ₹4,85,000 for a 14-day diagnostic. Bypasses multi-month enterprise vendor registration via discretionary PO.</p>
                        </div>
                        <a href="docs/contracts_and_sows/SUB_THRESHOLD_STATEMENT_OF_WORK_TEMPLATE.md" target="_blank" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-center transition">View Sub-Threshold SOW</a>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">Zero-Risk Contingency</span>
                            <h4 class="text-base font-bold text-white mt-2">Contingency Shared-Savings Agreement</h4>
                            <p class="text-xs text-slate-400 mt-2">Zero upfront cost for client. Formally guarantees 25% of recovered vendor leakage or 30% of verified monthly cloud savings.</p>
                        </div>
                        <a href="docs/contracts_and_sows/CONTINGENCY_SHARED_SAVINGS_AGREEMENT.md" target="_blank" class="mt-4 px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-center transition">View Contingency Contract</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= TAB 5: APEX PROMPT TERMINAL ================= -->
        <section id="tab-apex-prompt" class="tab-content hidden space-y-6">
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                    <div>
                        <h3 class="text-lg font-bold text-white">The OMEGA Apex Enterprise Deal Prompt</h3>
                        <p class="text-xs text-slate-400 mt-0.5">Engineered to produce turnkey enterprise proposals, ROI calculators, and outreach sequences in any frontier model.</p>
                    </div>
                    <button onclick="copyApexPrompt()" class="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center gap-1.5">
                        <span>📋</span> Copy Apex Prompt
                    </button>
                </div>
                <textarea id="apex-prompt-text" readonly class="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono rounded-xl p-4 h-[500px] focus:outline-none"></textarea>
            </div>
        </section>
    </main>

    <!-- Pitch Outreach Modal -->
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
                <div class="flex items-center justify-between">
                    <div>
                        <label class="text-[10px] font-semibold text-slate-400 uppercase">Lead Contact</label>
                        <p id="modal-lead" class="text-xs text-amber-400 font-bold"></p>
                    </div>
                    <div>
                        <label class="text-[10px] font-semibold text-slate-400 uppercase">Pipeline Stage</label>
                        <select id="modal-stage-select" onchange="updateStageFromModal()" class="block bg-slate-950 border border-slate-700 text-xs text-indigo-300 rounded px-2.5 py-1 focus:outline-none">
                            <option value="PROSPECT">Prospect (Identified)</option>
                            <option value="OUTREACH_DISPATCHED">Outreach Dispatched</option>
                            <option value="DISCOVERY_BOOKED">Discovery Call Booked</option>
                            <option value="SOW_SIGNED">Diagnostic SOW Signed</option>
                            <option value="RETAINER_ACTIVE">Master Retainer Active</option>
                        </select>
                    </div>
                </div>

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

    <!-- Collateral Viewer Modal -->
    <div id="collateral-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                <h3 id="collateral-title" class="text-lg font-bold text-white">Collateral Teardown</h3>
                <button onclick="closeCollateralModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <pre id="collateral-content" class="bg-slate-950 border border-slate-800 p-4 rounded-xl text-xs text-slate-300 font-mono whitespace-pre-wrap overflow-x-auto"></pre>
        </div>
    </div>

    <script>
        const CRM_DATA = {json.dumps(crm_data, indent=2)};
        const COLLATERALS = {json.dumps(collaterals, indent=2)};
        let currentFilter = 'ALL';
        let currentModalIdx = null;

        // LocalStorage Pipeline Status Management
        function getSavedStatus(company) {{
            const stages = JSON.parse(localStorage.getItem('deal_pipeline_stages') || '{{}}');
            return stages[company] || 'PROSPECT';
        }}

        function setSavedStatus(company, status) {{
            const stages = JSON.parse(localStorage.getItem('deal_pipeline_stages') || '{{}}');
            stages[company] = status;
            localStorage.setItem('deal_pipeline_stages', JSON.stringify(stages));
        }}

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            document.getElementById('tab-nav-' + tabId).classList.add('active');
        }}

        function renderCards(data) {{
            const container = document.getElementById('cards-container');
            container.innerHTML = '';
            
            data.forEach((item, idx) => {{
                const isGCC = item.type === 'Fortune 500 GCC';
                const badgeClass = isGCC ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-purple-500/10 text-purple-400 border-purple-500/20';
                const currentStatus = getSavedStatus(item.company);
                
                let statusBadge = '<span class="text-[9px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">Prospect</span>';
                if (currentStatus === 'OUTREACH_DISPATCHED') statusBadge = '<span class="text-[9px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">Dispatched</span>';
                if (currentStatus === 'DISCOVERY_BOOKED') statusBadge = '<span class="text-[9px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Call Booked</span>';
                if (currentStatus === 'SOW_SIGNED') statusBadge = '<span class="text-[9px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">SOW Signed</span>';
                if (currentStatus === 'RETAINER_ACTIVE') statusBadge = '<span class="text-[9px] px-2 py-0.5 rounded bg-emerald-600 text-white font-bold">Retainer Active</span>';

                const card = document.createElement('div');
                card.className = 'bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition rounded-2xl p-5 flex flex-col justify-between shadow-lg';
                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-2">
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded uppercase tracking-wide border ${{badgeClass}}">${{item.type}}</span>
                            <div class="flex items-center gap-1.5">
                                ${{statusBadge}}
                                <span class="text-xs font-extrabold text-emerald-400">₹${{(item.contract_inr/100000).toFixed(1)}}L</span>
                            </div>
                        </div>
                        <h4 class="text-base font-bold text-white tracking-tight">${{item.company}}</h4>
                        <p class="text-xs text-slate-400 mt-1 line-clamp-1">${{item.tech_park}}</p>
                        
                        <div class="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase font-semibold">Service Vector</span>
                                <p class="text-xs text-slate-300 font-medium">${{item.service_vector}}</p>
                            </div>
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase font-semibold">Lead Contact</span>
                                <p class="text-xs text-amber-300/90 font-medium">${{item.lead_contact}}</p>
                            </div>
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase font-semibold">Procurement Bypass</span>
                                <p class="text-xs text-slate-400 font-medium">${{item.procurement_bypass}}</p>
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
                                     item.tech_park.toLowerCase().includes(query) ||
                                     item.domain.toLowerCase().includes(query) ||
                                     item.service_vector.toLowerCase().includes(query) ||
                                     item.lead_contact.toLowerCase().includes(query);
                return matchesType && matchesQuery;
            }});
            renderCards(filtered);
        }}

        function openModal(idx) {{
            currentModalIdx = idx;
            const item = CRM_DATA[idx];
            document.getElementById('modal-title').textContent = item.company;
            document.getElementById('modal-subtitle').textContent = `${{item.type}} • ${{item.domain}}`;
            document.getElementById('modal-lead').textContent = item.lead_contact;
            document.getElementById('modal-stage-select').value = getSavedStatus(item.company);
            document.getElementById('modal-po').textContent = `₹${{item.entry_po_inr.toLocaleString('en-IN')}} (< ₹5L Sub-Threshold)`;
            document.getElementById('modal-retainer').textContent = `₹${{item.contract_inr.toLocaleString('en-IN')}} / Year`;
            
            const campusShort = item.tech_park.split(',')[0];
            const domainShort = item.domain.split('&')[0].trim();
            const contactName = item.lead_contact.split('(')[0].trim();
            
            const dmCopy = `Hi ${{contactName}},\\n\\nNoticed your leadership in directing ${{domainShort}} at ${{item.company}}'s ${{campusShort}} center.\\n\\nIn our audit of similar Bengaluru operations, between 10% and 18% of efficiency leaks through ${{item.service_vector.toLowerCase()}}.\\n\\nWe built a specialized diagnostic harness that resolves this in 14 days under discretionary departmental spend (₹${{(item.entry_po_inr/100000).toFixed(2)}}L). We recently unlocked ₹1.2 Cr in recovered credits for a peer team on Outer Ring Road.\\n\\nCould I share a 1-page sample framework this Thursday?\\n\\nBest,\\nAditya Mehra`;
            
            const emailCopy = `Subject: Eliminating ${{domainShort}} leakage at ${{item.company}}\\n\\nHi ${{contactName}},\\n\\nAs ${{item.company}} accelerates its Bengaluru center, one silent financial drain leaders regularly confront is ${{item.service_vector.toLowerCase()}}.\\n\\nRather than requiring a lengthy 6-month global vendor onboarding cycle, we execute a rapid 14-day retrospective diagnostic under discretionary departmental spend (₹${{item.entry_po_inr.toLocaleString('en-IN')}}).\\n\\nIf our diagnostic identifies less than ₹30 Lakhs in verified operational waste or recovery potential, there is zero continuing obligation.\\n\\nWould you be open to reviewing a 1-page sample diagnostic report from a fellow Bengaluru technology center?\\n\\nSincerely,\\nAditya Mehra\\nPrincipal Commercial Architect, Bengaluru`;
            
            document.getElementById('modal-dm').value = dmCopy;
            document.getElementById('modal-email').value = emailCopy;
            document.getElementById('pitch-modal').classList.remove('hidden');
        }}

        function updateStageFromModal() {{
            if (currentModalIdx !== null) {{
                const item = CRM_DATA[currentModalIdx];
                const stage = document.getElementById('modal-stage-select').value;
                setSavedStatus(item.company, stage);
                searchTargets();
            }}
        }}

        function closeModal() {{
            document.getElementById('pitch-modal').classList.add('hidden');
        }}

        function viewCollateral(key) {{
            document.getElementById('collateral-title').textContent = key.replace(/_/g, ' ');
            document.getElementById('collateral-content').textContent = COLLATERALS[key] || "Collateral document not found.";
            document.getElementById('collateral-modal').classList.remove('hidden');
        }}

        function closeCollateralModal() {{
            document.getElementById('collateral-modal').classList.add('hidden');
        }}

        function copyText(id) {{
            const el = document.getElementById(id);
            el.select();
            navigator.clipboard.writeText(el.value);
            alert("Copied to clipboard!");
        }}

        // Diagnostic Calculators
        function runSLACalc() {{
            const devs = parseInt(document.getElementById('input-devs').value);
            const rate = parseInt(document.getElementById('input-rate').value);
            const phantom = parseInt(document.getElementById('input-phantom').value);
            
            document.getElementById('val-devs').textContent = devs + " Devs";
            document.getElementById('val-rate').textContent = "₹" + rate.toLocaleString('en-IN') + "/hr";
            document.getElementById('val-phantom').textContent = phantom + "%";
            
            const annualHours = devs * 160 * 12;
            const annualSpend = annualHours * rate;
            const leakage = annualSpend * (phantom / 100);
            const fee = leakage * 0.25;
            
            document.getElementById('res-total-spend').textContent = "₹" + (annualSpend / 10000000).toFixed(2) + " Cr";
            document.getElementById('res-leakage').textContent = "₹" + (leakage / 10000000).toFixed(2) + " Cr";
            document.getElementById('res-fee').textContent = "₹" + (fee / 10000000).toFixed(2) + " Cr";
        }}

        function runFinOpsCalc() {{
            const queries = parseInt(document.getElementById('input-queries').value);
            const tokens = parseInt(document.getElementById('input-tokens').value);
            const cache = parseInt(document.getElementById('input-cache').value);
            
            document.getElementById('val-queries').textContent = queries.toLocaleString('en-IN');
            document.getElementById('val-tokens').textContent = tokens + " Tokens";
            document.getElementById('val-cache').textContent = cache + "%";
            
            const monthlyTokens = queries * tokens;
            const annualTokens = monthlyTokens * 12;
            const annualSpend = (annualTokens / 1000000) * 1400;
            const netSavings = annualSpend * ((cache + 20) / 100);
            const fee = netSavings * 0.30;
            
            document.getElementById('res-finops-bill').textContent = "₹" + (annualSpend / 10000000).toFixed(2) + " Cr";
            document.getElementById('res-finops-savings').textContent = "₹" + (netSavings / 10000000).toFixed(2) + " Cr (" + (cache + 20) + "%)";
            document.getElementById('res-finops-fee').textContent = "₹" + (fee / 100000).toFixed(1) + " Lakhs";
        }}

        function copyApexPrompt() {{
            const el = document.getElementById('apex-prompt-text');
            el.select();
            navigator.clipboard.writeText(el.value);
            alert("Apex Prompt copied to clipboard!");
        }}

        // Load prompt
        document.getElementById('apex-prompt-text').value = `<SYSTEM_PROMPT>
[ROLE & CONTEXT DEFINITION]
You are the APEX ENTERPRISE COMMERCIAL ARCHITECT & HIGH-TICKET DEAL MAKER. You possess elite dual-competency:
1. Fortune 500 Enterprise Strategy & Global Capability Center (GCC) Procurement Mastery (Ex-McKinsey Senior Partner / Head of Enterprise Procurement at Walmart Global Tech / Goldman Sachs GSC).
2. Silicon Valley & Bengaluru Unicorn Engineering & Growth Execution (CTO & Chief of Staff across Tier-1 startups like Swiggy, Zerodha, CRED, Razorpay, Postman).

You operate with zero fluff, zero generic boilerplate, and extreme mathematical and operational rigor. Your mission is to structure, pitch, negotiate, and execute high-margin (65-85% gross margin) enterprise service contracts, technical capability modules, and recurring retainers between ₹25 Lakhs and ₹2.5 Crores ($30,000 – $300,000 USD) with:
- Category A: Fortune 500 GCCs in Bengaluru (Walmart Global Tech, Target India, Goldman Sachs GSC, JPMorgan Chase India, Cisco, Intel, Microsoft IDC, Google India, Bosch, Boeing India, Wells Fargo).
- Category B: High-Velocity Tech Startups & Unicorns in Bengaluru (Zerodha, Swiggy, Flipkart, CRED, Razorpay, Meesho, Zepto, Postman, Groww, Ather Energy, Sarvam AI, Krutrim).
</SYSTEM_PROMPT>`;

        renderCards(CRM_DATA);
        runSLACalc();
        runFinOpsCalc();
    </script>
</body>
</html>
"""
    COCKPIT_HTML.write_text(html, encoding="utf-8")
    print(f"Compiled Cockpit v3 successfully at: {COCKPIT_HTML}")

if __name__ == "__main__":
    build_cockpit_v3()
