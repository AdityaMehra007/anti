// NEXUS AUTOPILOT - Frontend Dashboard & WhatsApp Simulation Controller

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    const target = document.getElementById(`${tabId}-tab`);
    if (target) target.classList.add('active');
    
    event.currentTarget.classList.add('active');
}

const debtors = [
    { name: 'Ramesh Traders', phone: '+919845012345', out: '₹1,40,000', delay: '19.5 days', score: '78.0', promise: '28 Aug 2026', action: 'WhatsApp Reminder (Stage 2)' },
    { name: 'Shree Balaji Manufacturing', phone: '+919845045678', out: '₹1,60,000', delay: '14.0 days', score: '65.0', promise: '30 Aug 2026', action: 'WhatsApp Reminder (Stage 2)' },
    { name: 'Kiran Event Organizers', phone: '+919845056789', out: '₹1,00,000', delay: '28.0 days', score: '85.0', promise: 'None (Unresponsive)', action: 'Urgent Call Escalation' },
    { name: 'Kumar Enterprises', phone: '+919845023456', out: '₹1,20,000', delay: '5.2 days', score: '22.0', promise: '25 Aug 2026', action: 'Gentle Payment Link' }
];

const invoices = [
    { num: 'INV/2026/1001', cust: 'Ramesh Traders', date: '01 Aug', due: '15 Aug', amt: '₹1,40,000', status: 'OVERDUE', link: 'https://rzp.io/i/nexus_ramesh_01' },
    { num: 'INV/2026/1002', cust: 'Kumar Enterprises', date: '18 Aug', due: '25 Aug', amt: '₹1,20,000', status: 'SENT', link: 'https://rzp.io/i/nexus_kumar_02' },
    { num: 'INV/2026/1003', cust: 'Shree Balaji Mfg', date: '05 Aug', due: '19 Aug', amt: '₹1,60,000', status: 'OVERDUE', link: 'https://rzp.io/i/nexus_balaji_03' },
    { num: 'INV/2026/1004', cust: 'Kiran Event Organizers', date: '20 Jul', due: '04 Aug', amt: '₹1,00,000', status: 'OVERDUE', link: 'https://rzp.io/i/nexus_kiran_04' },
    { num: 'INV/2026/1005', cust: 'Apex Logistics Hub', date: '10 Aug', due: '17 Aug', amt: '₹2,50,000', status: 'PAID', link: 'Settled via Razorpay' }
];

document.addEventListener('DOMContentLoaded', () => {
    // Populate Debtors
    const dBody = document.getElementById('debtorTableBody');
    dBody.innerHTML = debtors.map(d => `
        <tr>
            <td><strong>${d.name}</strong></td>
            <td>${d.phone}</td>
            <td style="color:var(--warning); font-weight:bold;">${d.out}</td>
            <td>${d.delay}</td>
            <td><span class="badge ${parseFloat(d.score) > 70 ? 'badge-danger' : 'badge-warning'}">${d.score}</span></td>
            <td>${d.promise}</td>
            <td><span class="badge badge-accent">${d.action}</span></td>
        </tr>
    `).join('');

    // Populate Invoices
    const iBody = document.getElementById('invoiceTableBody');
    iBody.innerHTML = invoices.map(i => `
        <tr>
            <td><strong>${i.num}</strong></td>
            <td>${i.cust}</td>
            <td>${i.date}</td>
            <td>${i.due}</td>
            <td><strong>${i.amt}</strong></td>
            <td><span class="badge ${i.status === 'PAID' ? 'badge-success' : (i.status === 'OVERDUE' ? 'badge-danger' : 'badge-warning')}">${i.status}</span></td>
            <td><a href="#" style="color:var(--accent); font-size:11px;">${i.link.includes('http') ? 'Pay Link' : i.link}</a></td>
        </tr>
    `).join('');

    // Render Charts
    renderCashForecastChart();
    renderCashRunwayChart();
});

function renderCashForecastChart() {
    const ctx = document.getElementById('cashForecastChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Day 1 (Today)', 'Day 7', 'Day 14', 'Day 21', 'Day 30'],
            datasets: [
                { label: 'Base Scenario (75% Inflow Recovery)', data: [385000, 420000, 470000, 495000, 515000], borderColor: '#00ff88', tension: 0.3 },
                { label: 'Stress Scenario (30% Recovery + Delayed Payments)', data: [385000, 360000, 310000, 280000, 255000], borderColor: '#ff0055', borderDash: [5, 5], tension: 0.3 }
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
}

function renderCashRunwayChart() {
    const ctx = document.getElementById('cashRunwayChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Current Balance', 'Expected Inflows (30D)', 'Fixed Outflows (30D)', 'Projected Net Cash'],
            datasets: [{
                label: 'Cash Position (INR)',
                data: [385000, 390000, -260000, 515000],
                backgroundColor: ['#00f0ff', '#00ff88', '#ff0055', '#b026ff']
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

function handleChatKey(e) {
    if (e.key === 'Enter') sendChatCommand();
}

function sendChatCommand() {
    const input = document.getElementById('chatInput');
    const txt = input.value.trim();
    if (!txt) return;

    appendMsg(txt, 'user');
    input.value = '';

    setTimeout(() => {
        respondToCommand(txt);
    }, 400);
}

function runQuickPrompt(promptText) {
    appendMsg(promptText, 'user');
    setTimeout(() => {
        respondToCommand(promptText);
    }, 400);
}

function appendMsg(text, type) {
    const box = document.getElementById('chatBox');
    const div = document.createElement('div');
    div.className = `msg msg-${type}`;
    div.innerHTML = type === 'ai' ? `<strong>NEXUS Autopilot:</strong> ${text}` : `<strong>You (Owner):</strong> ${text}`;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

function respondToCommand(cmd) {
    const l = cmd.toLowerCase();
    if (l.includes('summary') || l.includes('overview')) {
        appendMsg(`📊 <strong>Today's Business Snapshot:</strong><br>
        • Total Invoiced: <strong>₹7.70L</strong><br>
        • Collections Realized: <strong>₹2.50L</strong><br>
        • Outstanding Balance: <strong>₹5.20L</strong><br>
        • Overdue Receivables: <strong style="color:var(--danger)">₹4.00L</strong> (3 Debtors)<br>
        • 30-Day Cash Forecast: <strong>₹5.15L (Healthy)</strong><br><br>
        <em>Recommended Action:</em> Would you like me to start the automated collection plan for the 3 overdue accounts?`, 'ai');
    } else if (l.includes('who') || l.includes('paid') || l.includes('overdue')) {
        appendMsg(`🚨 <strong>Receivables Risk Report:</strong><br>
        1. <strong>Ramesh Traders</strong>: ₹1,40,000 (10d overdue, Risk: 78)<br>
        2. <strong>Shree Balaji Mfg</strong>: ₹1,60,000 (6d overdue, Risk: 65)<br>
        3. <strong>Kiran Event Organizers</strong>: ₹1,00,000 (21d overdue, Risk: 85)<br><br>
        Total money at risk: <strong>₹4.00L</strong>. Say <em>'Start collections'</em> to draft reminders.`, 'ai');
    } else if (l.includes('quote') || l.includes('quotation')) {
        appendMsg(`📑 <strong>Quotation Generated [Level 2 Gate]:</strong><br>
        • Customer: <strong>Ramesh Traders</strong><br>
        • Item: 250 Boxes @ ₹420/unit<br>
        • Subtotal: ₹1,05,000 + 18% GST (₹18,900)<br>
        • <strong>Grand Total: ₹1,23,900</strong><br>
        • Razorpay link ready.<br><br>
        <button class="btn btn-sm btn-accent" onclick="alert('Quotation & Razorpay link dispatched to Ramesh on WhatsApp (+919845012345)!')">Approve & Send via WhatsApp</button>`, 'ai');
    } else if (l.includes('collection') || l.includes('remind')) {
        appendMsg(`🎯 <strong>Autonomous Collection Radar Initialized:</strong><br>
        Prepared 3 tailored WhatsApp reminder templates with Razorpay payment links for Ramesh Traders, Balaji Mfg, and Kiran Events.<br><br>
        <button class="btn btn-sm btn-primary" onclick="alert('3 WhatsApp Reminders dispatched successfully with audit logs recorded!')">Approve & Dispatch 3 Reminders</button>`, 'ai');
    } else {
        appendMsg(`Understood. I have parsed your command into a business task and logged it in the audit queue.`, 'ai');
    }
}

function simulateInboundWebhook() {
    alert('⚡ INBOUND RAZORPAY WEBHOOK RECEIVED: Payment ID pay_kumar_887766 of ₹1,20,000 for Invoice INV/2026/1002 (Kumar Enterprises). Automatically reconciled in database!');
    document.getElementById('stat-collected').innerText = '₹3.70L';
    document.getElementById('stat-outstanding').innerText = '₹4.00L';
}

function sendQuickReminder(custId) {
    alert(`WhatsApp payment reminder dispatched for ${custId} via Razorpay Link!`);
}
