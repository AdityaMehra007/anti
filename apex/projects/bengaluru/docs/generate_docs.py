"""
APEX BENGALURU - Specification Documentation Generator
Generates all 17 authoritative technical specifications.
"""
from pathlib import Path

DOCS_DIR = Path(r"e:\anti\apex\projects\bengaluru\docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

specs = {
    "BENGALURU_ECOSYSTEM_ARCHITECTURE.md": """# 🏙️ BENGALURU ECOSYSTEM ARCHITECTURE
Unified multi-tier city architecture integrating 15 ecosystems: Startups, Technology, AI, GCCs, Enterprises, Talent, Investors, Research, Education, Infrastructure, Commercial, Policy, Real Estate, Deep-Tech, and Services.
- **Data Layer:** SQLite Normalized Relational Engine (`bengaluru.db`)
- **Intelligence Layer:** Signal Engine, Digital Twin, Dynamic Capability Discovery
- **Application Layer:** Career OS, Business Factory, GCC Automation Engine, Command Center""",

    "BENGALURU_DATA_MODEL.md": """# 🗄️ BENGALURU DATA MODEL
Schema specifications for normalized entities:
- `companies`, `gccs`, `startups`, `job_postings`, `skills_taxonomy`, `investors`, `funding_rounds`, `neighborhoods`, `intelligence_signals`, `policies_programs`, `time_series_metrics`, `user_career_pipeline`.""",

    "BENGALURU_KNOWLEDGE_GRAPH.md": """# 🌐 BENGALURU KNOWLEDGE GRAPH
Multi-relational graph connecting:
COMPANY ↔ GCC ↔ INDUSTRY ↔ ROLE ↔ SKILL ↔ TECH ↔ OFFICE ↔ LOCATION ↔ INVESTOR ↔ FOUNDER ↔ PRODUCT ↔ MARKET ↔ CUSTOMER ↔ EVENT ↔ UNIVERSITY ↔ RESEARCH ↔ POLICY.""",

    "BENGALURU_COMPANY_INTELLIGENCE.md": """# 🏢 BENGALURU COMPANY INTELLIGENCE
Tracking Tier-1 enterprises, MNCs, and GCCs in Bengaluru with multi-dimensional momentum scoring, verified headcount, and active tech stacks.""",

    "BENGALURU_STARTUP_INTELLIGENCE.md": """# 🚀 BENGALURU STARTUP INTELLIGENCE
Tracking 45+ Unicorns, DeepTech founders, funding rounds, cap tables, accelerator networks, and `STARTUP_MOMENTUM_SCORE`.""",

    "BENGALURU_GCC_INTELLIGENCE.md": """# 🏢 BENGALURU GCC INTELLIGENCE
Deep dive into 600+ Global Capability Centers (Walmart, Target, Goldman Sachs, Boeing, Mercedes-Benz) mapping AI mandates, product ownership, and engineering headcounts.""",

    "BENGALURU_JOB_INTELLIGENCE.md": """# 💼 BENGALURU JOB INTELLIGENCE
Job market mapping across ORR, Whitefield, Electronic City, and Manyata Tech Park with `ROLE_DEMAND_SCORE` and real salary benchmarks.""",

    "BENGALURU_SKILL_INTELLIGENCE.md": """# 🧠 BENGALURU SKILL INTELLIGENCE
Skill-demand heatmaps across Generative AI, LLM Workflows, SCM/Trade Analytics, Quantitative Modeling, and Enterprise Automation.""",

    "BENGALURU_INVESTOR_INTELLIGENCE.md": """# 💰 BENGALURU INVESTOR INTELLIGENCE
Venture capital and private equity intelligence mapping Peak XV Partners, Accel, Lightspeed, Matrix, and Blume Ventures.""",

    "BENGALURU_POLICY_INTELLIGENCE.md": """# 📜 BENGALURU POLICY INTELLIGENCE
Tracking Government of Karnataka schemes: ELEVATE 100 grants (₹50L), Karnataka GCC Policy 2024-2029, KDEM incentives, and power subsidies.""",

    "BENGALURU_OPPORTUNITY_ENGINE.md": """# ⚡ BENGALURU OPPORTUNITY ENGINE
Multi-variable opportunity ranking: DEMAND × ACCESSIBILITY × VALUE × TIMING × RECURRING POTENTIAL adjusted for RISK & COMPETITION.""",

    "BENGALURU_CAREER_OS.md": """# 🎯 APEX BENGALURU CAREER OS
Targeting engine for BBA / Tech graduates, skill gap analysis, resume optimization, interview intelligence, and recruiter networking.""",

    "BENGALURU_BUSINESS_OS.md": """# 🏭 BENGALURU BUSINESS OS & STARTUP BUILDER
Autonomous idea-to-revenue pipeline: DISCOVER ➔ VALIDATE ➔ BUILD ➔ PILOT ➔ SELL ➔ DELIVER ➔ MEASURE ➔ SCALE.""",

    "BENGALURU_CONTROL_TOWER.md": """# 🗼 BENGALURU CONTROL TOWER
Full-stack cyberpunk mission control dashboard with real-time Chart.js feeds, signal streams, and micro-market radars.""",

    "BENGALURU_SOURCE_GOVERNANCE.md": """# 📋 BENGALURU SOURCE GOVERNANCE
Strict evidence hierarchy: Govt Filings ➔ Company Press ➔ Official Portals ➔ Research Inst. Tagging claims as VERIFIED, OBSERVED, INFERRED.""",

    "BENGALURU_PRIVACY_SECURITY.md": """# 🛡️ BENGALURU PRIVACY & SECURITY
Zero surveillance policy, no unauthorized scraping, parameterized SQL execution, and full compliance with Digital Personal Data Protection Act (DPDPA).""",

    "BENGALURU_READINESS_REPORT.md": """# 📊 BENGALURU READINESS REPORT
Readiness scoring across MNCs, GCCs, and Startups with gap closure roadmaps for job seekers and entrepreneurs."""
}

for filename, content in specs.items():
    file_path = DOCS_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"[DOCS_GEN] Successfully generated {len(specs)} technical specification documents in: {DOCS_DIR}")
