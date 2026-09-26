# TradeNexus AI: Master Risk Register & Mitigation Matrix

## 1. Risk Scoring Methodology

In compliance with **Part LXIV (Red Team Engine)** and **Part LXV (Resilience Engine)**:
Risks are ranked by `Composite Risk Score = Likelihood (1–5) × Impact (1–5)`.

---

## 2. Comprehensive Risk Matrix

| Risk ID | Risk Category | Description | Likelihood (1-5) | Impact (1-5) | Inherent Score | Existing Controls & Mitigations | Residual Score | Owner |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---:|:---:|
| **RSK-01** | **Regulatory** | EU extends CBAM reporting deadline or relaxes penalty enforcement, lowering exporter urgency. | 3 | 4 | **12** | Core beachhead covers general customs demurrage, HS classification, and US CBP rules—not dependent solely on CBAM. | **6 (MED)** | Strategy Lead |
| **RSK-02** | **Technical** | Model hallucination on complex dual-use chemical or precision mechanical HS code leads to customs penalty. | 2 | 5 | **10** | Deterministic rule engine overrides probabilistic LLMs; GRI rules hardcoded; mandatory human review when confidence < 80%. | **4 (LOW)** | Lead Architect |
| **RSK-03** | **Commercial** | Long sales cycles and procurement inertia among conservative traditional exporters. | 4 | 3 | **12** | Offer zero-risk pilot: "We audit 50 bills free; pay only if we find compliance errors or lost drawback cash." | **6 (MED)** | Growth Lead |
| **RSK-04** | **Platform** | ICEGATE changes EDI flatfile specification or blocks external automated parsing tools. | 2 | 4 | **8** | Maintain daily ICEGATE schema monitoring cron; direct integration with certified Customs House Agents. | **4 (LOW)** | Integration Eng |
| **RSK-05** | **Competition** | Flexport or Descartes launches self-serve ₹25k/mo tool tailored specifically to Indian mid-market exporters. | 2 | 4 | **8** | Enterprise giants cannot economically service ₹25k/mo accounts with heavy sales overhead; build deep local ERP hooks (Tally/Zoho). | **4 (LOW)** | Strategy Lead |
| **RSK-06** | **Operational** | Key person risk (sole founder capacity constraint during initial customer scaling). | 3 | 4 | **12** | Full operational SOPs documented; autonomous AI agent swarm handles 80% of routine workflows. | **6 (MED)** | Founder |
| **RSK-07** | **Financial** | Customer default on monthly SaaS invoices; negative cash flow from delayed receivables. | 2 | 3 | **6** | Annual upfront payment incentives (10-15% discount); credit card / automated auto-debit requirement for monthly plans. | **3 (LOW)** | Finance Lead |
| **RSK-08** | **Cybersecurity** | Exporter commercial invoice data leaked or compromised in multi-tenant database. | 1 | 5 | **5** | Strict tenant-level database isolation, AES-256 encryption at rest, TLS 1.3 in transit, zero credentials in code. | **2 (LOW)** | Security Lead |
