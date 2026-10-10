"""
OMNIVERSE INTERVIEW DEFENSE ENGINE
Generates comprehensive role-specific behavioral STAR answers,
technical defense packs, and situational handling strategies for
Aditya Mehra (BBA International Business).

Directives: OMEGA CONSTITUTION & ADI_OMNI_CODEX
"""

import os
import json
import datetime

OUTPUT_MD = r"e:\anti\OMNIVERSE_INTERVIEW_DEFENSE_COMPENDIUM.md"

INTERVIEW_PACKS = [
    {
        "role_archetype": "Global Operations & Trade Settlement Analyst",
        "target_companies": ["Deutsche Bank", "Goldman Sachs", "Morgan Stanley", "HSBC Global Services"],
        "core_focus": "Trade validation, clearing cycles, reconciliation, exception handling, and regulatory compliance.",
        "star_questions": [
            {
                "question": "Walk me through how you handle high-stakes operational exceptions when trade data doesn't reconcile.",
                "situation": "In an international trade settlement simulation involving multi-currency transactions and staggered value dates.",
                "task": "Identify discrepancies across counterparty trade confirmations, nostro accounts, and internal ledgers before market cut-off times.",
                "action": "Conducted systematic root-cause tracing by isolating currency conversion variances, value date timing mismatches, and fee deductions. Automated ledger reconciliation checks to catch recurring syntax errors.",
                "result": "Resolved 100% of out-of-balance breaks prior to market clearing deadlines, achieving zero-penalty settlement and establishing an audited exception ledger.",
                "defense_tip": "Emphasize zero panic, rigorous audit trail preservation, and strict SLA adherence."
            },
            {
                "question": "Why did you choose Operations rather than Front-Office Sales?",
                "situation": "Assessing career motivation and long-term commitment to operational excellence.",
                "task": "Articulate a genuine value alignment with high-volume enterprise execution and risk management.",
                "action": "Focused on how institutional stability, regulatory adherence, and bottom-line margin expansion depend entirely on flawless operational execution. Demonstrated that my BBA training in international trade instilled deep respect for process engineering over variable sales quotas.",
                "result": "Clear positioning as a reliable, long-term operational anchor who thrives on SLA precision and process scalability.",
                "defense_tip": "Position operations as the engine room of the bank that protects capital and ensures regulatory immunity."
            }
        ]
    },
    {
        "role_archetype": "Audit & Assurance Associate",
        "target_companies": ["KPMG India Services", "Deloitte US-India", "EY GDS", "PwC Acceleration Centers"],
        "core_focus": "Substantive testing, analytical procedures, internal controls, and documentation integrity.",
        "star_questions": [
            {
                "question": "How do you ensure audit documentation meets strict cross-border regulatory standards (e.g. Canadian or US standards)?",
                "situation": "Reviewing financial statements and internal controls for global clients across differing accounting jurisdictions.",
                "task": "Verify that audit working papers, vouching evidence, and management representations comply strictly with host-country regulatory frameworks.",
                "action": "Structured verification checklists cross-referencing IFRS and host-country GAAP guidelines. Performed dual-pass sampling on high-risk transaction ledgers to detect omissions or classification anomalies.",
                "result": "Zero audit deficiency findings during review cycles, ensuring clean audit file sign-offs and verified evidentiary compliance.",
                "defense_tip": "Highlight procedural skepticism, meticulous documentation, and cross-border regulatory awareness."
            }
        ]
    },
    {
        "role_archetype": "Supply Chain & Procurement Operations Specialist",
        "target_companies": ["Target India", "Flipkart", "Amazon India", "Cisco Systems", "Cargill"],
        "core_focus": "Vendor SLA management, inventory forecasting, purchase order execution, and logistics tracking.",
        "star_questions": [
            {
                "question": "Describe a scenario where a supplier failed to deliver on time. How did you maintain operational continuity?",
                "situation": "Managing multi-tier vendor shipments facing unexpected logistics delays and port congestion.",
                "task": "Maintain fulfillment velocity without incurring stockout penalties or severe expedited freight surcharges.",
                "action": "Analyzed safety stock buffers, activated secondary regional supplier agreements, and negotiated partial split shipments via multimodal routing.",
                "result": "Sustained a 99.2% on-time fulfillment rate, avoiding customer stockouts while containing shipping cost inflation within 3%.",
                "defense_tip": "Focus on proactive scenario planning, contract SLA enforcement, and data-driven inventory management."
            }
        ]
    },
    {
        "role_archetype": "Enterprise Business & Systems Analyst",
        "target_companies": ["Salesforce", "NTT DATA", "Sagility", "IBM India"],
        "core_focus": "Requirement gathering, process mapping, KPI reporting, and stakeholder coordination.",
        "star_questions": [
            {
                "question": "How do you translate complex business requirements into clear, actionable technical specifications?",
                "situation": "Collaborating with cross-functional teams to digitize manual reporting workflows.",
                "task": "Bridge the gap between executive business needs and technical system configurations.",
                "action": "Authored comprehensive Functional Requirement Documents (FRDs) and User Stories with explicit acceptance criteria. Mapped current-state vs future-state BPMN workflows to eliminate redundant data entry steps.",
                "result": "Reduced process turnaround time by 35% and achieved 100% user adoption during user acceptance testing (UAT).",
                "defense_tip": "Emphasize empathetic stakeholder communication, clear visual process modeling, and measurable business outcomes."
            }
        ]
    }
]


def generate_interview_defense_compendium():
    """Generates the master markdown defense compendium."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"""# OMNIVERSE INFINITY: Behavioral Interview Defense & STAR Compendium

**Target Candidate**: Aditya Mehra | BBA International Business  
**Generated On**: {now}  
**Framework**: Behavioral STAR (Situation, Task, Action, Result)  

---

"""

    for i, pack in enumerate(INTERVIEW_PACKS):
        md += f"""## Archetype {i+1}: {pack['role_archetype']}

- **Target Employers**: {', '.join(pack['target_companies'])}
- **Core Domain Focus**: {pack['core_focus']}

### STAR Defense Blueprint

"""
        for q_idx, q in enumerate(pack['star_questions']):
            md += f"""#### Question {q_idx+1}: *"{q['question']}"*

- **Situation:** {q['situation']}
- **Task:** {q['task']}
- **Action:** {q['action']}
- **Result:** {q['result']}
- **💡 Strategic Interview Tip:** {q['defense_tip']}

```text
Response Script:
"In my operations training, {q['situation']} My responsibility was to {q['task']}. To resolve this, I {q['action']}. Ultimately, this resulted in {q['result']}."
```

---
"""

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"[OMNIVERSE DEFENSE] Compendium generated at: {OUTPUT_MD}")
    return INTERVIEW_PACKS


if __name__ == "__main__":
    generate_interview_defense_compendium()
