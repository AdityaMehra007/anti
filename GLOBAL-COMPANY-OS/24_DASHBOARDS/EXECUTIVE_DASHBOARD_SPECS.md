# TradeNexus AI: Executive Dashboard Architecture & Telemetry Specs

## 1. Executive Telemetry Overview

In compliance with **Part LVI (Founder Dashboard)** and **Part LXXIII (Automated Report Factory)**:
The Founder Dashboard must provide an unvarnished, real-time single source of truth separating facts from forecasts and hypotheses.

```
+-------------------------------------------------------------------------+
|                    FOUNDER COMMAND COCKPIT                              |
+-------------------+-------------------+-------------------+-------------+
| Cash Position     | Monthly Run-Rate  | Gross Margin      | Runway      |
| Lean Bootstrapped | ₹0 (Day 30: ₹85k) | 94.0%             | Infinite    |
+-------------------+-------------------+-------------------+-------------+
| Active Beachhead  | Pipeline Potential| Shipping Bills    | System State|
| TradeNexus AI     | ₹2,50,000         | Audited: 12 Live  | OPTIMAL     |
+-------------------------------------------------------------------------+
| BIGGEST BOTTLENECK: Closing Exporter Pilot Account #1 in Bangalore      |
| HIGHEST LEVERAGE ACTION: Dispatch 25 pre-computed compliance teardowns  |
+-------------------------------------------------------------------------+
```

---

## 2. Telemetry Ingestion Points & Alert Thresholds

| Metric | Source Component | Frequency | Alert Threshold (Red Flag) |
|:---|:---|:---:|:---|
| **API Error Rate** | FastAPI Middleware | Real-time | Errors > 1.0% over 5-minute rolling window |
| **Parsing Confidence** | `hs_engine.py` | Per-docket | Any docket line with confidence < 80% |
| **ICEGATE Latency** | `icegate_edi_generator.py`| Hourly | API response time > 5,000ms |
| **Lead Pipeline Health**| CRM / JSON store | Daily | Qualified leads in Stage 1 < 20 accounts |
| **Outbound Bounce Rate**| SMTP Dispatcher | Daily | Hard bounce rate > 3.0% (auto-halts queue) |
| **Cash Burn Rate** | Finance Ledger | Monthly | Unbudgeted burn > ₹25,000/month |
