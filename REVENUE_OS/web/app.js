// REVENUE OS Command Center Client Script

async function fetchState() {
  try {
    const res = await fetch("/api/state");
    if (!res.ok) throw new Error("Network error fetching state");
    const data = await res.json();
    renderDashboard(data);
  } catch (err) {
    console.error("Failed to fetch state:", err);
    document.getElementById("sys-status").innerText = "OFFLINE / SYNCING";
    document.getElementById("sys-status").className = "text-rose-400 font-semibold";
  }
}

function renderDashboard(data) {
  // Master Metrics
  document.getElementById("m-rev-today").innerText = data.revenue_today;
  document.getElementById("m-rev-month").innerText = data.revenue_month;
  document.getElementById("m-profit").innerText = data.profit;
  document.getElementById("m-pipeline").innerText = data.weighted_pipeline;
  document.getElementById("m-raw-pipeline").innerText = "Raw: " + data.pipeline_value;
  document.getElementById("m-leads").innerText = data.qualified_leads_count;
  document.getElementById("m-total-leads").innerText = "Total: " + data.leads_count;
  document.getElementById("m-rev-hr").innerText = data.revenue_per_founder_hour;
  document.getElementById("m-founder-hours").innerText = "Logged: " + data.founder_hours;

  // Operational Metrics
  document.getElementById("m-cac").innerText = data.cac;
  document.getElementById("m-ltv").innerText = data.ltv;
  document.getElementById("m-conversion").innerText = data.conversion_rate;
  document.getElementById("m-ai-cost").innerText = data.ai_cost;

  // Priorities
  document.getElementById("m-biggest-opp").innerText = data.biggest_opportunity;
  document.getElementById("m-biggest-risk").innerText = data.biggest_risk;
  document.getElementById("m-biggest-bottleneck").innerText = data.biggest_bottleneck;

  // Top 3 Actions
  const actionsList = document.getElementById("top-3-actions-list");
  actionsList.innerHTML = "";
  data.top_3_actions.forEach((act, idx) => {
    const li = document.createElement("li");
    li.className = "p-2.5 bg-slate-950/80 border border-slate-800 rounded-lg flex items-start gap-2";
    li.innerHTML = `<span class="font-mono text-emerald-400 font-bold">${idx + 1}.</span> <span>${act}</span>`;
    actionsList.appendChild(li);
  });

  // Pending Approvals (Directive 88)
  const approvalContainer = document.getElementById("approval-cards-container");
  const badge = document.getElementById("approval-count-badge");
  const pending = data.pending_approvals || [];
  badge.innerText = `${pending.length} PENDING`;
  badge.className = pending.length > 0
    ? "text-xs font-mono px-2 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800 animate-pulse"
    : "text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700";

  approvalContainer.innerHTML = "";
  if (pending.length === 0) {
    approvalContainer.innerHTML = `
      <div class="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center text-xs text-slate-500">
        No pending approval requests. All autonomous workflows are bounded and operating safely.
      </div>
    `;
  } else {
    pending.forEach(card => {
      const cardEl = document.createElement("div");
      cardEl.className = "p-4 bg-slate-950 border border-amber-800/60 rounded-xl space-y-3";
      cardEl.innerHTML = `
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-amber-950 text-amber-400 border border-amber-800">${card.request_type}</span>
            <span class="text-xs font-mono text-slate-400">From: ${card.requester_agent}</span>
          </div>
          <span class="text-xs font-bold text-emerald-400 font-mono">+₹${Number(card.upside_inr).toLocaleString()} upside</span>
        </div>
        <h4 class="text-sm font-semibold text-white">${card.title}</h4>
        <p class="text-xs text-slate-300">${card.reason}</p>
        <div class="text-[11px] text-slate-400 p-2 bg-slate-900 rounded border border-slate-800">
          <strong class="text-slate-300">Recommendation:</strong> ${card.recommendation}
        </div>
        <div class="flex items-center justify-end gap-2 pt-1">
          <button onclick="rejectApproval(${card.id})" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
            Reject
          </button>
          <button onclick="approveApproval(${card.id})" class="px-4 py-1.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-500 text-white font-semibold transition shadow-lg shadow-emerald-900/30">
            Approve & Dispatch
          </button>
        </div>
      `;
      approvalContainer.appendChild(cardEl);
    });
  }

  // 10 Specialist Agents
  const agentsGrid = document.getElementById("agents-grid");
  agentsGrid.innerHTML = "";
  (data.agents || []).forEach(agent => {
    const div = document.createElement("div");
    div.className = "p-3 bg-slate-950 border border-slate-800/80 rounded-xl flex items-center justify-between";
    div.innerHTML = `
      <div>
        <div class="font-semibold text-slate-200">${agent.name}</div>
        <div class="text-[10px] text-slate-400">${agent.role}</div>
      </div>
      <div class="text-right font-mono">
        <span class="px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-emerald-400 border border-slate-700">${agent.max_permission_tier}</span>
      </div>
    `;
    agentsGrid.appendChild(div);
  });

  // 10 Automations
  const automationsGrid = document.getElementById("automations-grid");
  automationsGrid.innerHTML = "";
  (data.automations || []).forEach(aut => {
    const div = document.createElement("div");
    div.className = "p-2.5 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between hover:border-slate-700 transition";
    div.innerHTML = `
      <span class="font-mono text-[11px] text-slate-300">${aut}</span>
      <button onclick="triggerAutomation('${aut}')" class="px-2 py-1 rounded bg-slate-800 hover:bg-emerald-700 text-slate-300 hover:text-white text-[10px] font-mono transition">
        RUN
      </button>
    `;
    automationsGrid.appendChild(div);
  });
}

async function approveApproval(id) {
  try {
    const res = await fetch("/api/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, notes: "Approved via Web Command Center" })
    });
    if (res.ok) fetchState();
  } catch (err) {
    alert("Approval error: " + err.message);
  }
}

async function rejectApproval(id) {
  try {
    const res = await fetch("/api/reject", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, notes: "Rejected via Web Command Center" })
    });
    if (res.ok) fetchState();
  } catch (err) {
    alert("Rejection error: " + err.message);
  }
}

async function triggerAutomation(name) {
  try {
    const res = await fetch("/api/run-automation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name })
    });
    const data = await res.json();
    alert(`Automation '${name}' executed: Status ${data.status}`);
    fetchState();
  } catch (err) {
    alert("Automation trigger error: " + err.message);
  }
}

// Initial fetch and auto-refresh every 15 seconds
fetchState();
setInterval(fetchState, 15000);
