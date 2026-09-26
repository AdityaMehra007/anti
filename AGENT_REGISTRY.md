# 👥 OMEGA ∞ — AGENT REGISTRY & GOVERNMENT MACHINERY
**Supreme Constitution**: [`OMEGA_CONSTITUTION.md`](OMEGA_CONSTITUTION.md) (Section 11 Multi-Agent Architecture & Section 12 Agent Contract)  

---

## 1. THE 9 OMEGA ∞ EXECUTIVE DEPARTMENTS

Every executive agent adheres strictly to Section 12 Agent Contracts:

| Department | Agent File | Key Role | Core Mission | Autonomy Gate |
|---|---|---|---|:---:|
| **Executive Directorate** | [`.agents/agents/omega-executive-director.md`](.agents/agents/omega-executive-director.md) | Master Orchestrator | End-to-end objective decomposition, multi-agent orchestration, Section 107 reporting | Level 4 |
| **Strategy** | [`.agents/agents/omega-strategy.md`](.agents/agents/omega-strategy.md) | Chief Strategy Officer | 13-metric opportunity scoring, moat architecture, competitive response simulations | Level 2 |
| **Research** | [`.agents/agents/omega-research.md`](.agents/agents/omega-research.md) | Head of Intelligence | Empirical investigation, primary source verification, fact vs. inference classification | Level 3 |
| **Product** | [`.agents/agents/omega-product.md`](.agents/agents/omega-product.md) | Product Architect & UX | 10 product questions, rapid MVP design, interactive dark-mode studios | Level 3 |
| **Engineering** | [`.agents/agents/omega-engineering.md`](.agents/agents/omega-engineering.md) | Chief Technology Officer | 16-step build engine, Ponytail minimalism, deep modules, 100% test pass gates | Level 4 |
| **Business & GTM** | [`.agents/agents/omega-business.md`](.agents/agents/omega-business.md) | VP Revenue & Operations | B2B lead generation, staged outreach (`omega_approvals.db`), SOP automation | Level 3 |
| **Finance** | [`.agents/agents/omega-finance.md`](.agents/agents/omega-finance.md) | Chief Financial Officer | Unit economics (CAC/LTV), cash flow, compute/token spend, capital allocation | Level 1 |
| **Security & Red Team** | [`.agents/agents/omega-security-redteam.md`](.agents/agents/omega-security-redteam.md) | CISO & Red Team Lead | 12 adversarial questions, secret protection, threat modeling, crisis containment | Level 2 |
| **Governance** | [`.agents/agents/omega-governance.md`](.agents/agents/omega-governance.md) | Head of Compliance & QA | Truthful execution enforcement (Section 78), single source of truth, reality audit | Level 2 |

---

## 2. THE ARCHETYPAL COUNCIL (SECTION 9)
For multi-perspective reasoning before major irreversible decisions:
- **THE SAGE**: Questions core premises and deep assumptions.
- **THE STRATEGIST**: Evaluates the whole board before making a move.
- **THE BUILDER**: Translates abstract ideas into tangible functional systems.
- **THE ENGINEER**: Enforces stability, performance, modularity, and error handling.
- **THE MERCHANT**: Analyzes customer demand, willingness to pay, and economics.
- **THE NEGOTIATOR**: Maximizes positive-sum outcomes and strategic leverage.
- **THE EXPLORER**: Detects untapped opportunities and emerging territories.
- **THE GUARDIAN**: Defends user privacy, secrets, data integrity, and ethical bounds.
- **THE SCIENTIST**: Demands verifiable empirical proof and falsifiable experiments.
- **THE PHILOSOPHER**: Models long-term ethical implications and moral boundaries.
- **THE INVESTOR**: Evaluates capital allocation and opportunity cost of resources.
- **THE OPERATOR**: Focuses on daily execution velocity, workflows, and bottleneck removal.
- **THE FUTURIST**: Builds 1-year to 50-year horizon scenarios.
- **THE ETHICIST**: Tests moral and societal boundaries.

---

## 3. THE STRATEGY COUNCIL (SECTION 10)
Simulates executive leadership perspectives for high-stakes decisions:
- **C-Suite**: CEO, COO, CFO, CTO, CMO, CRO, CISO.
- **Specialists**: Product Lead, Principal Engineer, Lead Designer, Data Scientist, Legal Counsel, Risk Officer.
- **External Perspectives**: Target Customer, Direct Competitor, Industry Regulator, Venture Investor, Frontline Employee.

---

## 4. THE 3,000 DOMAIN SPECIALIST SUBAGENTS
- Registered in `.agents/agents.json` and cataloged in `AGENTS_AND_SKILLS_MASTER_CATALOG.csv`.
- Mapped across 15 enterprise domains (200 agents per domain):
  1. AI Infrastructure & Operations
  2. Software Engineering, Cloud & DevOps
  3. B2B Sales & Revenue Generation
  4. Growth Marketing, SEO & Distribution
  5. Product Design, UX & Visual Systems
  6. Financial Engineering & Treasury
  7. Data Intelligence & Analytics
  8. Executive Strategy & Corporate Development
  9. Talent Acquisition & People Operations
  10. Security, Governance & Risk
  11. Event Operations & Brand Activations
  12. Global Supply Chain & EXIM Logistics
  13. Customer Success & Retention
  14. Generative AI & Agentic Workflows
  15. MCP Tool Connectors & Integrations

---

## 5. LOCAL MOE INFERENCE ENGINE (COLIBRÌ)
- **Core Engine**: `colibri/c/` — High-speed pure C inference engine streaming MoE weights directly from NVMe.
- **Serving Layer**: OpenAI-compatible HTTP Gateway (`openai_server.py`) serving local intelligence on `http://127.0.0.1:8080`.
- **Management**: `START_COLIBRI.bat` and `colibri_controller.py`.
