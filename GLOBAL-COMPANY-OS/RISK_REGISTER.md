# MASTER RISK REGISTER

| Risk ID | Category | Risk Description | Prob (1-5) | Impact (1-5) | Exposure | Trigger | Mitigation Strategy | Owner | Status |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---|:---|:---:|
| **RSK-001** | Regulatory | Government API changes on ICEGATE / DGFT portal | 3 | 4 | 12 | Portal schema migration notice | Maintain decoupled adapter layer; support manual export docket upload fallback | CTO Agent | ACTIVE |
| **RSK-002** | Product | AI model hallucination in HS tariff code classification | 2 | 5 | 10 | Tariff misclassification alert | Hard deterministic cross-validation against WCO tariff database + confidence score gating | QA Agent | ACTIVE |
| **RSK-003** | Sales | Long enterprise procurement cycles (>60 days) | 3 | 3 | 9 | Stalled prospect discussions | Target owners/managing directors directly with no-risk free compliance audit of past dockets | Sales Agent | ACTIVE |
| **RSK-004** | Operational | Founder cognitive overload across multi-agent duties | 3 | 4 | 12 | Task backlog > 10 items | Strict Company Commander filter enforcing Top 3 daily actions; automate background cron | Founder OS | ACTIVE |
| **RSK-005** | Financial | Delayed receivable payments from early Indian B2B clients | 4 | 3 | 12 | Invoice overdue > 15 days | 100% upfront payment for first pilot or automated credit-card recurring SaaS billing | Finance Agent | ACTIVE |
