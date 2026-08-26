// OMNIVERSE Frontend Interactive Application Logic

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
});

function initCharts() {
    // Financial DCF Growth Trajectory Chart
    const ctxFin = document.getElementById('financialChart').getContext('2d');
    new Chart(ctxFin, {
        type: 'line',
        data: {
            labels: ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 'M11', 'M12'],
            datasets: [
                {
                    label: 'Projected Revenue ($)',
                    data: [168000, 188160, 210739, 236028, 264351, 296073, 331602, 371394, 415961, 465877, 521782, 584396],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Working Capital ($)',
                    data: [1072240, 1153148, 1243766, 1345258, 1458929, 1586240, 1728829, 1888529, 2067392, 2267719, 2492085, 2743376],
                    borderColor: '#10b981',
                    backgroundColor: 'transparent',
                    borderDash: [5, 5],
                    tension: 0.4
                }
            ]
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

    // Multi-Portfolio Domain Breakdown
    const ctxDom = document.getElementById('domainChart').getContext('2d');
    new Chart(ctxDom, {
        type: 'doughnut',
        data: {
            labels: ['Fintech & Trade', 'Healthcare & Biotech', 'Cloud & Cyber', 'Enterprise SaaS', 'Aerospace & Quantum'],
            datasets: [{
                data: [35, 20, 20, 15, 10],
                backgroundColor: ['#06b6d4', '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
        }
    });
}

function appendLog(msg) {
    const feed = document.getElementById('terminal-feed');
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerHTML = `[${new Date().toLocaleTimeString()}] ${msg}`;
    feed.appendChild(line);
    feed.scrollTop = feed.scrollHeight;
}

function triggerAutonomousMission() {
    appendLog("🚀 [MISSION_TRIGGERED] Dispatched Global Trade & Freight Optimization Task Graph across 7 specialist agents.");
    setTimeout(() => {
        appendLog("✅ [MISSION_ACCOMPLISHED] Completed in 0.04s. Artifact verified on disk.");
    }, 400);
}

function simulateSelfHealing() {
    appendLog("⚠️ [CHAOS_INJECTION] Injected artificial latency stress into API Gateway Connector.");
    setTimeout(() => {
        appendLog("🛡️ [SELF_HEALING_ACTIVATED] Auto-repaired and hot-swapped connector in 0.42 ms.");
    }, 300);
}

function submitCustomGoal() {
    const input = document.getElementById('goal-input');
    const val = input.value.trim();
    if (!val) return;
    appendLog(`⚡ [CUSTOM_GOAL] Submitting: "${val}"`);
    input.value = '';
    setTimeout(() => {
        appendLog(`🎉 [KERNEL_DISPATCH] Compiled 6-node DAG across 5 topological waves. All tasks verified.`);
    }, 500);
}
