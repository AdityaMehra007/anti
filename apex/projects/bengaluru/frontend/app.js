// APEX BENGALURU Dashboard Controller

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    const target = document.getElementById(`${tabId}-tab`);
    if (target) target.classList.add('active');
    
    event.currentTarget.classList.add('active');
}

// Mock/Initial Data
const initialSignals = [
    { cat: 'GCC_EXPANSION', title: 'Boeing India inaugurates ₹1,600 Cr R&D Campus in North Bengaluru', time: '1h ago', status: 'VERIFIED' },
    { cat: 'STARTUP_FUNDING', title: 'Sarvam AI secures $41M Series A for sovereign Indic LLMs', time: '2h ago', status: 'VERIFIED' },
    { cat: 'HIRING_SPIKE', title: 'Walmart Global Tech adds 1,200 supply chain & AI roles in ORR', time: '3h ago', status: 'VERIFIED' },
    { cat: 'POLICY_UPDATE', title: 'Karnataka launches 25% power tariff rebate for DeepTech GCCs', time: '4h ago', status: 'VERIFIED' }
];

const gccData = [
    { name: 'Walmart Global Tech', origin: 'USA', headcount: '8,500', loc: 'Kadubeesanahalli (ORR)', score: '93.5', ownership: 'HIGH' },
    { name: 'Goldman Sachs Services', origin: 'USA', headcount: '9,000', loc: 'Helios Tech Park (ORR)', score: '94.0', ownership: 'HIGH' },
    { name: 'Boeing India (BIETC)', origin: 'USA', headcount: '5,500', loc: 'KIADB Aerospace Park', score: '97.0', ownership: 'HIGH' },
    { name: 'Target in India', origin: 'USA', headcount: '4,200', loc: 'Manyata Tech Park', score: '89.5', ownership: 'HIGH' }
];

const startupData = [
    { name: 'Zerodha', founders: 'Nithin & Nikhil Kamath', sector: 'Fintech', stage: 'BOOTSTRAPPED', funding: '$0 (Profitable)', loc: 'JP Nagar', score: '98.0' },
    { name: 'Swiggy', founders: 'Sriharsha Majety', sector: 'Quick Commerce', stage: 'UNICORN', funding: '$3.6B', loc: 'Koramangala', score: '93.0' },
    { name: 'Pixxel', founders: 'Awais & Kshitij', sector: 'SpaceTech', stage: 'SERIES_B', funding: '$71M', loc: 'Indiranagar', score: '95.0' },
    { name: 'Sarvam AI', founders: 'Vivek & Pratyush', sector: 'Generative AI', stage: 'SERIES_A', funding: '$41M', loc: 'Koramangala', score: '96.0' }
];

const marketsData = [
    { name: 'Outer Ring Road (ORR)', type: 'TECH_CORRIDOR', rent: '₹95/sqft', res: '₹48,000', cong: '8.8', metro: 'Blue Line (2026)' },
    { name: 'Whitefield & ITPL', type: 'TECH_CORRIDOR', rent: '₹68/sqft', res: '₹35,000', cong: '7.5', metro: 'Purple Line (Active)' },
    { name: 'Koramangala', type: 'STARTUP_HUB', rent: '₹85/sqft', res: '₹45,000', cong: '7.0', metro: 'Yellow Line Vicinity' },
    { name: 'Hebbal & North Corridor', type: 'AIRPORT_NORTH', rent: '₹75/sqft', res: '₹38,000', cong: '6.2', metro: 'Airport Blue Line (2026)' }
];

document.addEventListener('DOMContentLoaded', () => {
    // Populate Signals
    const feed = document.getElementById('signalFeed');
    feed.innerHTML = initialSignals.map(s => `
        <div class="signal-item">
            <h4>${s.title}</h4>
            <p><small style="color:var(--accent); font-weight:bold;">[${s.cat}]</small> • ${s.time} • <span style="color:var(--success);">${s.status}</span></p>
        </div>
    `).join('');

    // Populate GCC Table
    const gccBody = document.getElementById('gccTableBody');
    gccBody.innerHTML = gccData.map(g => `
        <tr>
            <td><strong>${g.name}</strong></td>
            <td>${g.origin}</td>
            <td>${g.headcount}</td>
            <td>${g.loc}</td>
            <td><span class="badge badge-accent">${g.score}</span></td>
            <td><span class="badge badge-success">${g.ownership}</span></td>
        </tr>
    `).join('');

    // Populate Startup Table
    const stpBody = document.getElementById('startupTableBody');
    stpBody.innerHTML = startupData.map(s => `
        <tr>
            <td><strong>${s.name}</strong></td>
            <td>${s.founders}</td>
            <td>${s.sector}</td>
            <td><span class="badge badge-purple">${s.stage}</span></td>
            <td>${s.funding}</td>
            <td>${s.loc}</td>
            <td><span class="badge badge-success">${s.score}</span></td>
        </tr>
    `).join('');

    // Populate Markets Table
    const mktBody = document.getElementById('marketsTableBody');
    mktBody.innerHTML = marketsData.map(m => `
        <tr>
            <td><strong>${m.name}</strong></td>
            <td>${m.type}</td>
            <td>${m.rent}</td>
            <td>${m.res}</td>
            <td>${m.cong}/10</td>
            <td>${m.metro}</td>
        </tr>
    `).join('');

    // Populate Business Opp
    const oppBox = document.getElementById('businessOppBox');
    oppBox.innerHTML = `
        <div style="background:#090e18; padding:20px; border-radius:6px; border:1px solid var(--border);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0; color:var(--accent);">NEXUS-EXIM: Autonomous AI Cross-Border Trade & Customs Compliance SaaS</h2>
                <span class="badge badge-success">SCORE: 94.5 / 100</span>
            </div>
            <p style="color:var(--text-muted); margin:10px 0 20px;">Targeting Mid-to-Large Clean Energy, Solar, and Auto Component Exporters in Bengaluru.</p>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:15px; margin-bottom:20px;">
                <div style="background:#121927; padding:15px; border-radius:4px;"><strong>Target Year 1 ARR</strong><div style="font-size:22px; color:var(--success); margin-top:5px;">₹2.55 Crores</div></div>
                <div style="background:#121927; padding:15px; border-radius:4px;"><strong>Govt Grant Eligibility</strong><div style="font-size:22px; color:var(--accent); margin-top:5px;">₹50 Lakhs (ELEVATE 100)</div></div>
                <div style="background:#121927; padding:15px; border-radius:4px;"><strong>Gross Margin</strong><div style="font-size:22px; color:#fff; margin-top:5px;">82.0%</div></div>
            </div>
            <p><strong>GTM Action:</strong> Direct pilot integration with 25 Logistics and Trade Managers across ORR & Peenya Industrial Hubs.</p>
        </div>
    `;

    // Render Charts
    renderGCCChart();
    renderSalaryChart();
});

function renderGCCChart() {
    const ctx = document.getElementById('gccFunctionChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['AI & Data Science (34%)', 'Core Software Engineering (28%)', 'Global SCM & Logistics (18%)', 'Quant Finance & Risk (12%)', 'Cybersecurity (8%)'],
            datasets: [{
                data: [34, 28, 18, 12, 8],
                backgroundColor: ['#00f0ff', '#00ff88', '#b026ff', '#ffaa00', '#ff0055'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'JetBrains Mono' } } } }
        }
    });
}

function renderSalaryChart() {
    const ctx = document.getElementById('salaryChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['BBA SCM Analyst', 'Trade Ops Exec', 'Fintech Risk Analyst', 'AI Strategy Lead', 'AI Systems Product'],
            datasets: [{
                label: 'Salary Benchmark Range (₹ LPA)',
                data: [12.0, 10.0, 14.0, 28.0, 45.0],
                backgroundColor: '#00f0ff'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#94a3b8' } } },
            scales: {
                x: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

function runCareerMatching() {
    const results = document.getElementById('careerMatchResults');
    results.innerHTML = `
        <div style="background:#090e18; border:1px solid var(--accent); padding:15px; border-radius:6px;">
            <div style="display:flex; justify-content:space-between;">
                <strong>1. International Supply Chain Analyst — Walmart Global Tech</strong>
                <span class="badge badge-success">88.5% MATCH</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); margin:6px 0;">Location: Kadubeesanahalli (ORR) | Salary: ₹8.5 - ₹12 LPA | Work Mode: HYBRID</p>
            <p style="font-size:11px; color:#fff;"><strong>Matched Skills:</strong> Incoterms, Supply Chain Analytics, SQL, Excel</p>
            <p style="font-size:11px; color:var(--warning);"><strong>Skill Gap to Prepare:</strong> Vendor Management & LLM Inventory Prompting</p>
            <button class="btn btn-primary" style="padding:6px 12px; font-size:11px; margin-top:8px;" onclick="alert('Generating 3-Page Executive Interview Prep Pack for Walmart Global Tech...')">Prepare Interview Strategy</button>
        </div>
        <div style="background:#090e18; border:1px solid var(--border); padding:15px; border-radius:6px; margin-top:10px;">
            <div style="display:flex; justify-content:space-between;">
                <strong>2. Global Trade Operations Executive — DP World Global Tech</strong>
                <span class="badge badge-accent">82.0% MATCH</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); margin:6px 0;">Location: Manyata Tech Park | Salary: ₹7.0 - ₹10 LPA | Work Mode: HYBRID</p>
            <p style="font-size:11px; color:#fff;"><strong>Matched Skills:</strong> Cross-Border Customs, Trade Settlement, Excel</p>
        </div>
    `;
}
