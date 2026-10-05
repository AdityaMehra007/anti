// ARES-FINANCE Terminal Interactive Controller

let currentTicker = "NVDA";
let currentDossier = null;
let currentDcf = null;
let fcfChartInstance = null;
let geminiApiKey = localStorage.getItem("ARES_GEMINI_API_KEY") || "";

// AI Studio Assets
const AI_STUDIO_SYSTEM_PROMPT = `<identity>
You are "ARES-FINANCE" (Autonomous Research & Equity Synthesis), an Apex Institutional Financial Research Director and Chief Investment Strategist at a top-tier multi-strategy hedge fund.
You combine the forensic accounting rigor of Harry Markopolos, the economic moat analysis of Charlie Munger and Hamilton Helmer, the valuation precision of Aswath Damodaran, and the risk management architecture of Stanley Druckenmiller.

You operate with zero tolerance for "vibe-investing," financial fluff, or corporate PR spin. Every claim must be tied to verified primary filings (SEC 10-K, 10-Q, 8-K, proxy statements DEF 14A, statutory filings, earnings transcripts), audited statement line items, or verifiable macro datasets.
</identity>

<reality_laws_and_financial_axioms>
1. CASH IS REALITY, NET INCOME IS OPINION:
   - Accruals can be manipulated; Free Cash Flow (FCF) and cash conversion cycles rarely lie.
   - Always scrutinize working capital changes (DSO, DIO, DPO) for channel stuffing or supplier stretching.
2. STOCK-BASED COMPENSATION (SBC) IS A CASH OUTFLOW:
   - Treat SBC as a real economic expense. Never accept management's "Adjusted EBITDA" that strips out SBC without penalizing share count dilution in per-share valuation.
3. REVERSE DCF OVER BASE DCF:
   - Rather than projecting fantasy growth rates 10 years out, calculate the implied market expectations: "What revenue growth and terminal operating margin must this company hit to justify today's share price?" Then judge whether that expectation is feasible.
4. UNYIELDING FORENSIC SCRUTINY:
   - Scrutinize off-balance-sheet commitments, operating lease capitalized liabilities, pension underfunding, factoring of receivables, and related-party transactions.
5. PRIMARY SOURCE FIDELITY:
   - When figures diverge between Bloomberg/Yahoo Finance and the SEC 10-K footnote, the SEC footnote governs. Always cite filing period, Item, and footnote number.
</reality_laws_and_financial_axioms>

<core_analytical_engines>
### ENGINE 1: FORENSIC ACCOUNTING & EARNINGS QUALITY
- Beneish M-Score Calculation (8-variable model to detect probability of earnings manipulation):
  * DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA
- Altman Z-Score & Ohlson O-Score: Distance to default / insolvency risk.
- Sloan Accrual Ratio: Accruals = (Net Income - Operating Cash Flow) / Total Assets.
- Non-GAAP Reconciliation Audit: Bridge GAAP Operating Income to Adjusted EBITDA.

### ENGINE 2: STRATEGIC MOAT (7 POWERS FRAMEWORK)
Evaluate durable competitive advantage through Hamilton Helmer's 7 Powers:
1. Scale Economies | 2. Network Effects | 3. Counter-Positioning | 4. Switching Costs | 5. Branding | 6. Cornered Resource | 7. Process Power

### ENGINE 3: VALUATION & ASYMMETRIC EXPECTATIONS MODELING
- Unlevered 5-Year DCF with WACC & Mid-Year Convention.
- Reverse DCF: Solve for market implied terminal growth rate.
- Sensitivity Matrix: WACC vs. Terminal Growth Rate.
- Scenario Probability Trees (Base, Bull, Bear).

### ENGINE 4: EXECUTIVE INTEGRITY & TRANSCRIPT FORENSICS
- Form 4 Insider transaction flows vs. 10b5-1 plans.
- Capital Allocation Track Record (ROIC vs WACC spread).

### ENGINE 5: MACRO, LIQUIDITY & CROSS-ASSET OVERLAY
- Yield curve, SOFR, OAS credit spreads, and FX exposure.
</core_analytical_engines>

<mandatory_output_template>
# [TICKER: COMPANY NAME] — INSTITUTIONAL INVESTMENT MEMORANDUM
**Date:** [YYYY-MM-DD] | **Current Price:** [$X.XX] | **Target Price (12M):** [$X.XX]
**Recommendation:** [STRONG BUY / LONG / NEUTRAL / SHORT / STRONG SELL] | **Implied Return:** [+/-X.X%]
1. EXECUTIVE THESIS & ASYMMETRIC SETUP (Variant Perception, Catalysts)
2. FORENSIC FINANCIAL SCORECARD & EARNINGS QUALITY (Beneish M-Score, Altman Z, SBC dilution)
3. MOAT & COMPETITIVE ARCHITECTURE (7 Powers, Pricing Power)
4. VALUATION SUITE & EXPECTATIONS INVESTING (Reverse DCF, Sensitivity Matrix)
5. SCENARIOS & THESIS INVALIDATION RED LINES
</mandatory_output_template>`;

const AI_STUDIO_TOOLS_SCHEMA = JSON.stringify([
  {
    "name": "get_sec_filing_text",
    "description": "Fetches section text from SEC 10-K, 10-Q, or 8-K filings from EDGAR.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "ticker": { "type": "STRING" },
        "filing_type": { "type": "STRING" },
        "item_section": { "type": "STRING" },
        "year": { "type": "INTEGER" }
      },
      "required": ["ticker", "filing_type", "year"]
    }
  },
  {
    "name": "calculate_dcf_and_reverse_dcf",
    "description": "Calculates institutional unlevered DCF, Reverse DCF, and sensitivity matrix.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "current_share_price": { "type": "NUMBER" },
        "shares_outstanding": { "type": "NUMBER" },
        "net_debt": { "type": "NUMBER" },
        "starting_fcf": { "type": "NUMBER" },
        "wacc": { "type": "NUMBER" },
        "terminal_growth_rate": { "type": "NUMBER" }
      },
      "required": ["current_share_price", "shares_outstanding", "net_debt", "starting_fcf", "wacc", "terminal_growth_rate"]
    }
  }
], null, 2);

const AI_STUDIO_RESPONSE_SCHEMA = JSON.stringify({
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InstitutionalEquityResearchReport",
  "type": "object",
  "properties": {
    "ticker": { "type": "string" },
    "company_name": { "type": "string" },
    "recommendation": { "type": "string", "enum": ["STRONG_BUY", "LONG", "NEUTRAL", "SHORT", "STRONG_SELL"] },
    "current_price": { "type": "number" },
    "target_price_12m": { "type": "number" },
    "variant_perception": { "type": "string" },
    "moat_rating": { "type": "string", "enum": ["WIDE", "NARROW", "NONE"] },
    "powers_present": { "type": "array", "items": { "type": "string" } },
    "forensics": {
      "type": "object",
      "properties": {
        "beneish_m_score": { "type": "number" },
        "manipulation_risk": { "type": "string" },
        "altman_z_score": { "type": "number" },
        "sbc_to_revenue_percent": { "type": "number" }
      },
      "required": ["beneish_m_score", "manipulation_risk", "altman_z_score"]
    }
  },
  "required": ["ticker", "company_name", "recommendation", "current_price", "target_price_12m", "variant_perception", "forensics"]
}, null, 2);

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  initEventListeners();
  loadTickerData("NVDA");
});

function initEventListeners() {
  // Search
  document.getElementById("btnSearchTicker").addEventListener("click", () => {
    const ticker = document.getElementById("customTickerInput").value.trim().toUpperCase();
    if (ticker) loadTickerData(ticker);
  });
  document.getElementById("customTickerInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const ticker = e.target.value.trim().toUpperCase();
      if (ticker) loadTickerData(ticker);
    }
  });

  // Ribbon clicks
  document.querySelectorAll(".ribbon-item").forEach(item => {
    item.addEventListener("click", () => {
      document.querySelectorAll(".ribbon-item").forEach(i => i.classList.remove("selected"));
      item.classList.add("selected");
      loadTickerData(item.dataset.ticker);
    });
  });

  // DCF Sliders
  const waccSlider = document.getElementById("waccSlider");
  const tgrSlider = document.getElementById("tgrSlider");

  waccSlider.addEventListener("input", (e) => {
    document.getElementById("waccDisplayVal").innerText = `${(e.target.value * 100).toFixed(1)}%`;
    recalculateDCF();
  });

  tgrSlider.addEventListener("input", (e) => {
    document.getElementById("tgrDisplayVal").innerText = `${(e.target.value * 100).toFixed(1)}%`;
    recalculateDCF();
  });

  // Audit button
  document.getElementById("btnRunDeepAnalysis").addEventListener("click", runLiveAudit);

  // Copy & Print
  document.getElementById("btnCopyMemo").addEventListener("click", () => {
    const text = document.getElementById("memoBody").innerText;
    navigator.clipboard.writeText(text);
    alert("Memorandum copied to clipboard!");
  });

  document.getElementById("btnPrintMemo").addEventListener("click", () => {
    window.print();
  });

  // AI Studio Modal
  const aiStudioModal = document.getElementById("aiStudioModal");
  const exportArea = document.getElementById("aiStudioExportArea");

  document.getElementById("btnOpenAIStudioModal").addEventListener("click", () => {
    exportArea.value = AI_STUDIO_SYSTEM_PROMPT;
    aiStudioModal.style.display = "flex";
  });
  document.getElementById("btnCloseAIStudioModal").addEventListener("click", () => {
    aiStudioModal.style.display = "none";
  });

  document.getElementById("tabPrompt").addEventListener("click", (e) => {
    setActiveTab(e.target);
    exportArea.value = AI_STUDIO_SYSTEM_PROMPT;
  });
  document.getElementById("tabTools").addEventListener("click", (e) => {
    setActiveTab(e.target);
    exportArea.value = AI_STUDIO_TOOLS_SCHEMA;
  });
  document.getElementById("tabOutput").addEventListener("click", (e) => {
    setActiveTab(e.target);
    exportArea.value = AI_STUDIO_RESPONSE_SCHEMA;
  });
  document.getElementById("btnCopyExportText").addEventListener("click", () => {
    navigator.clipboard.writeText(exportArea.value);
    alert("Copied configuration to clipboard!");
  });

  // API Key Modal
  const apiKeyModal = document.getElementById("apiKeyModal");
  document.getElementById("btnApiKeyModal").addEventListener("click", () => {
    document.getElementById("geminiApiKeyInput").value = geminiApiKey;
    apiKeyModal.style.display = "flex";
  });
  document.getElementById("btnCloseApiKeyModal").addEventListener("click", () => {
    apiKeyModal.style.display = "none";
  });
  document.getElementById("btnSaveApiKey").addEventListener("click", () => {
    geminiApiKey = document.getElementById("geminiApiKeyInput").value.trim();
    localStorage.setItem("ARES_GEMINI_API_KEY", geminiApiKey);
    apiKeyModal.style.display = "none";
    alert("Gemini API Key saved locally.");
  });
}

function setActiveTab(btn) {
  document.querySelectorAll("#aiStudioModal .btn-pill").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

async function loadTickerData(ticker) {
  currentTicker = ticker.toUpperCase();
  try {
    const res = await fetch(`/api/dossier/${currentTicker}`);
    const data = await res.json();
    if (data.status === "SUCCESS") {
      currentDossier = data.data;
      currentDcf = data.dcf_model;
      renderDossier();
      runLiveAudit();
    }
  } catch (err) {
    console.error("Failed to load ticker data:", err);
  }
}

function renderDossier() {
  if (!currentDossier) return;
  const d = currentDossier;

  // Hero
  document.getElementById("heroTicker").innerText = d.ticker;
  document.getElementById("heroCompanyName").innerText = d.company_name;
  document.getElementById("heroSector").innerText = d.sector;
  document.getElementById("heroPrice").innerText = `$${d.current_price.toFixed(2)}`;
  document.getElementById("heroTargetPrice").innerText = `$${d.target_price_12m.toFixed(2)}`;
  
  const upside = (((d.target_price_12m - d.current_price) / d.current_price) * 100).toFixed(1);
  const upsideEl = document.getElementById("heroUpside");
  upsideEl.innerText = `${upside > 0 ? '+' : ''}${upside}%`;
  upsideEl.className = `stat-val ${upside >= 0 ? 'up' : 'down'}`;

  const recBadge = document.getElementById("heroRecBadge");
  recBadge.innerText = d.recommendation;
  recBadge.className = `badge-rec ${d.recommendation.replace(' ', '-')}`;

  document.getElementById("heroVariantText").innerText = d.thesis.variant_perception;

  // Forensics
  document.getElementById("beneishScoreVal").innerText = d.forensics.beneish_m_score.toFixed(2);
  const beneishRiskEl = document.getElementById("beneishRiskVal");
  beneishRiskEl.innerText = `${d.forensics.manipulation_risk} MANIPULATION RISK`;
  beneishRiskEl.className = `status ${d.forensics.manipulation_risk === 'LOW' ? 'up' : 'down'}`;

  document.getElementById("altmanScoreVal").innerText = d.forensics.altman_z_score.toFixed(2);
  document.getElementById("altmanZoneVal").innerText = d.forensics.altman_z_score > 3.0 ? "SAFE ZONE SOLVENCY" : "WATCH ZONE";
  
  document.getElementById("sbcRevVal").innerText = `${d.forensics.sbc_to_revenue_pct.toFixed(1)}%`;
  document.getElementById("sloanRatioVal").innerText = d.forensics.sloan_accrual_ratio.toFixed(3);

  // Red Flags
  const redFlagsList = document.getElementById("redFlagsList");
  redFlagsList.innerHTML = d.forensics.red_flags.map(f => `<li>${f}</li>`).join("");

  // Moat
  document.getElementById("moatRatingBadge").innerText = `${d.moat.rating} MOAT`;
  document.getElementById("pricingPowerVal").innerText = `${d.moat.pricing_power_score} / 10`;
  document.getElementById("grossMarginVal").innerText = `${d.moat.gross_margin_ltm.toFixed(1)}%`;

  const powersContainer = document.getElementById("powersContainer");
  powersContainer.innerHTML = d.moat.powers.map(p => `<span class="power-tag">⚡ ${p}</span>`).join("");

  // Sliders
  document.getElementById("waccSlider").value = d.wacc;
  document.getElementById("waccDisplayVal").innerText = `${(d.wacc * 100).toFixed(1)}%`;
  document.getElementById("tgrSlider").value = 0.025;
  document.getElementById("tgrDisplayVal").innerText = "2.5%";

  renderDCFOutputs(currentDcf);
}

function renderDCFOutputs(dcf) {
  if (!dcf) return;
  document.getElementById("modelFairValue").innerText = `$${dcf.fair_value_per_share.toFixed(2)}`;
  document.getElementById("reverseDcfTgr").innerText = `${dcf.reverse_dcf_implied_terminal_growth.toFixed(2)}%`;
  document.getElementById("tvShareVal").innerText = `${dcf.terminal_value_share_percent.toFixed(1)}%`;

  // Sensitivity Matrix
  const tbody = document.getElementById("sensitivityBody");
  tbody.innerHTML = dcf.sensitivity_matrix.map(row => {
    return `
      <tr>
        <td style="font-weight: 700; color: #fff;">${row.wacc}%</td>
        ${row.matrix.map(col => `
          <td class="${col.price >= dcf.current_price ? 'highlight' : ''}">$${col.price.toFixed(2)}</td>
        `).join("")}
      </tr>
    `;
  }).join("");

  // Chart
  renderChart(dcf.fcf_projections);
}

function renderChart(projections) {
  const ctx = document.getElementById("fcfChart").getContext("2d");
  const labels = projections.map(p => `Yr ${p.year} (+${p.growth}%)`);
  const data = projections.map(p => p.fcf);

  if (fcfChartInstance) {
    fcfChartInstance.destroy();
  }

  fcfChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Projected Unlevered FCF ($B)",
        data: data,
        backgroundColor: "rgba(56, 189, 248, 0.4)",
        borderColor: "#38bdf8",
        borderWidth: 2,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 11 } }
        }
      },
      scales: {
        x: {
          ticks: { color: "#64748b", font: { family: "JetBrains Mono" } },
          grid: { color: "rgba(255,255,255,0.05)" }
        },
        y: {
          ticks: { color: "#64748b", font: { family: "JetBrains Mono" } },
          grid: { color: "rgba(255,255,255,0.05)" }
        }
      }
    }
  });
}

async function recalculateDCF() {
  if (!currentDossier) return;
  const wacc = parseFloat(document.getElementById("waccSlider").value);
  const tgr = parseFloat(document.getElementById("tgrSlider").value);

  try {
    const res = await fetch("/api/calculate/dcf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        current_price: currentDossier.current_price,
        shares_diluted: currentDossier.shares_diluted_b,
        net_debt: currentDossier.net_debt_b,
        starting_fcf: currentDossier.fcf_ltm_b,
        wacc: wacc,
        terminal_growth_rate: tgr,
        growth_rates: currentDossier.growth_profile
      })
    });
    const dcf = await res.json();
    currentDcf = dcf;
    renderDCFOutputs(dcf);
  } catch (err) {
    console.error("Recalculation error:", err);
  }
}

async function runLiveAudit() {
  const memoBody = document.getElementById("memoBody");
  memoBody.innerHTML = `
    <div style="text-align: center; padding: 40px; color: var(--accent-cyan); font-family: var(--font-mono);">
      <div style="font-size: 24px; margin-bottom: 10px;">⚡</div>
      <strong>SYNTHESIZING INSTITUTIONAL RESEARCH MEMORANDUM...</strong>
      <div style="font-size: 11px; color: var(--text-dim); margin-top: 6px;">Auditing SEC footnotes, Beneish variables & reverse DCF expectations.</div>
    </div>
  `;

  try {
    const res = await fetch("/api/analyze/live", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: currentTicker,
        gemini_api_key: geminiApiKey || null,
        agent_mode: "FULL_SYNTHESIS"
      })
    });
    const data = await res.json();
    if (data.memo_markdown) {
      memoBody.innerHTML = marked.parse(data.memo_markdown);
    }
  } catch (err) {
    memoBody.innerHTML = `<p style="color: var(--accent-rose);">Failed to generate memorandum: ${err.message}</p>`;
  }
}
