"""
=============================================================================
INTERVIEW PREPARATION INTELLIGENCE ENGINE (STAR METHOD)
Ground-Truth Operational Interview Preparation for Bengaluru Target Roles
=============================================================================
"""

import os
from typing import Any

# Grounded facts about Aditya Mehra
CANDIDATE_FACTS = {
    "name": "Aditya Mehra",
    "education": "BBA in International Business, Dayananda Sagar University (2023–2026), GPA 8.2/10",
    "event_scale": "300+ live corporate and high-stakes events delivered across Bengaluru with 0 critical failures",
    "flagship_event": "AERO India 2025 at Yelahanka Air Force Station (VIP logistics, defense delegates, security protocol)",
    "robotics_ops": "Instawork AI Robotics & Computer Vision Data Operations (10,000+ spatial frames validated, zero drift)",
    "vendor_management": "Pencil Mark BD written commendation; managed 40+ vendor rate cards, negotiated 15-20% cost savings",
    "technical_skills": "Python, SQL, Advanced Excel (XLOOKUP, Pivot, Scenario Manager), Power BI, Process Optimization",
}

QUESTION_BANK = [
    {
        "id": "Q1_PRESSURE",
        "question": "Tell me about a time you managed high operational pressure with tight deadlines and zero room for error.",
        "category": "Operational Resilience & High Stakes",
        "star": {
            "situation": "During AERO India 2025 at Yelahanka Air Force Station, our operations unit managed protocol logistics, VIP movement schedules, and multi-agency coordination across defense and corporate delegations.",
            "task": "Maintain 100% on-time movement for international delegates across security-controlled flight lines with strict physical checkpoints and real-time schedule modifications.",
            "action": "I established a redundant communications tree with checkpoint leads, pre-cleared transport manifests 3 hours ahead of time, and built a contingency rerouting protocol for emergency flight-line delays.",
            "result": "Zero protocol breaches or missed delegate briefings across the multi-day aerospace summit, delivering seamless operational compliance under military-grade security conditions.",
        },
    },
    {
        "id": "Q2_CONFLICT_VENDOR",
        "question": "How do you handle a vendor or supplier who fails to deliver as per SLA or attempts price gouging?",
        "category": "Vendor & Supply Chain Management",
        "star": {
            "situation": "While delivering a 1,200-attendee corporate summit in Bengaluru, a key fabrication and audiovisual vendor attempted to levy unapproved 25% rush surcharges and delayed staging handover.",
            "task": "Enforce contractual rate card integrity, prevent unbudgeted cost overruns, and ensure the staging was fully commissioned 2 hours before attendee entry.",
            "action": "I benchmarked their itemized rate card against pre-agreed master SLAs, isolated the unsubstantiated line-item markups, and negotiated an immediate performance cure window with vendor leadership while deploying standby local backup technicians.",
            "result": "The vendor waived the Rs 1.8 Lakhs surcharge, staging was handed over with complete technical sign-off 45 minutes ahead of schedule, and gross event margin was preserved.",
        },
    },
    {
        "id": "Q3_PROCESS_IMPROVEMENT",
        "question": "Describe a scenario where you identified an operational inefficiency and solved it systematically.",
        "category": "Process Optimization & Data Analytics",
        "star": {
            "situation": "In multi-event operations across 40+ vendors, rate card quotes and stage commissioning checklists were handled manually via unstructured WhatsApp chats and disconnected paper logs.",
            "task": "Standardize procurement workflows, eliminate quotation discrepancies, and accelerate turnaround from 48 hours to same-day approval.",
            "action": "I built an automated Python and Excel-based quotation validation model that cross-checked vendor line items against historical market benchmarks and flagged >10% rate anomalies automatically.",
            "result": "Reduced invoice audit cycle time by 65%, eliminated quotation errors, and achieved an average 18% cost reduction across recurring equipment rentals.",
        },
    },
    {
        "id": "Q4_DATA_QUALITY",
        "question": "How do you ensure data accuracy and quality when managing high-volume repetitive operations?",
        "category": "AI & Dataset Operations",
        "star": {
            "situation": "During my engagement with Instawork on AI robotics vision data operations, our team processed thousands of spatial bounding box annotations for warehouse mobile robot navigation.",
            "task": "Maintain >99.5% geometric precision across multi-class object tags (pallets, forklifts, warehouse personnel) to prevent robotic obstacle collision risks.",
            "action": "I designed a deterministic validation checklist checking bounding coordinates, aspect ratios, and occlusion tags, running batch verification passes before sending annotation batches downstream.",
            "result": "Audited over 10,000 spatial frames with zero critical labeling drift, achieving top-tier QA velocity and benchmark accuracy.",
        },
    },
    {
        "id": "Q5_WHY_OPERATIONS",
        "question": "Why do you want to work in Business Operations or Supply Chain rather than traditional Sales or Marketing?",
        "category": "Career Alignment & Value Fit",
        "star": {
            "situation": "Throughout my BBA in International Business at Dayananda Sagar University and 300+ live operational deployments, I discovered that enterprise profitability is won or lost in execution, cost control, and logistics reliability.",
            "task": "Direct my career trajectory into analytical, high-leverage operations roles where metrics are objective, systems are scalable, and efficiency creates direct bottom-line impact.",
            "action": "I deliberately avoided speculative commission-driven telecalling to focus on supply chain economics, procurement negotiation, process mapping, and operational analytics tools (SQL, Python, Advanced Excel).",
            "result": "I bring proven execution discipline, cross-functional vendor negotiation capability, and a builder mindset that thrives on operational rigor and measurable efficiency.",
        },
    },
]


class InterviewPrepEngine:
    def __init__(self):
        self.candidate = CANDIDATE_FACTS
        self.questions = QUESTION_BANK

    def generate_company_playbook(
        self, company_name: str, target_role: str
    ) -> dict[str, Any]:
        """Generates tailored interview strategy for a specific target company and role."""
        return {
            "company": company_name,
            "role": target_role,
            "candidate_intro_30s": (
                f"I am Aditya Mehra, an operations-focused BBA in International Business candidate from "
                f"Dayananda Sagar University (Class of 2026, GPA 8.2). I have led ground execution across "
                f"300+ live operations in Bengaluru, including VIP defense logistics at AERO India 2025 and "
                f"computer vision data operations at Instawork. I specialize in vendor SLA enforcement, "
                f"cost optimization, and analytical process mapping to drive operational excellence at {company_name}."
            ),
            "tailored_answers": self.questions,
            "closing_questions_to_ask_interviewer": [
                f"What are the top operational bottlenecks or SLA challenges your team is actively optimizing this quarter at {company_name}?",
                "How does your department measure success for an entry-level Operations Analyst in the first 90 days?",
                "Which software tools and internal ERP systems will this role interface with daily?",
            ],
        }

    def export_playbook_markdown(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# BENGALURU CORPORATE INTERVIEW PREPARATION PLAYBOOK\n")
            f.write(
                "### Target: Business Operations, SCM, and Operations Analyst (Non-Sales)\n"
            )
            f.write(f"**Candidate:** Aditya Mehra | {self.candidate['education']}\n\n")
            f.write("---\n\n")
            f.write(
                "## 1. 30-Second Executive Pitch (The 'Tell Me About Yourself' Anchor)\n\n"
            )
            f.write(
                '> *"I am Aditya Mehra, an operations-focused BBA in International Business candidate from '
            )
            f.write(
                "Dayananda Sagar University (Class of 2026, GPA 8.2). Over the past three years, I have directed "
            )
            f.write(
                "on-ground execution across 300+ live operations in Bengaluru, from military-grade VIP movement at "
            )
            f.write(
                "AERO India 2025 to high-precision robotics vision dataset quality at Instawork. I bring tested vendor "
            )
            f.write(
                "negotiation skills, analytical process discipline (SQL/Python/Excel), and a relentless focus on bottom-line "
            )
            f.write('efficiency with zero appetite for cold-calling sales."*\n\n')
            f.write("---\n\n")
            f.write("## 2. High-Impact STAR Behavioral Interview Cases\n\n")

            for q in self.questions:
                f.write(f"### {q['id']}: {q['question']}\n")
                f.write(f"**Category:** `{q['category']}`\n\n")
                f.write(f"- **Situation (S):** {q['star']['situation']}\n")
                f.write(f"- **Task (T):** {q['star']['task']}\n")
                f.write(f"- **Action (A):** {q['star']['action']}\n")
                f.write(f"- **Result (R):** **{q['star']['result']}**\n\n")
                f.write("---\n\n")

            f.write(
                "## 3. High-Leverage Reverse Interview Questions (Questions to Ask the Hiring Manager)\n\n"
            )
            f.write(
                '1. *"What are the top 2 operational bottlenecks or SLA variances that this business unit is actively solving this quarter?"*\n'
            )
            f.write(
                '2. *"How does the team balance operational speed with data governance and audit compliance?"*\n'
            )
            f.write(
                '3. *"What does high performance look like for an Operations Associate in the first 90 days?"*\n'
            )


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "INTERVIEW_PLAYBOOK.md")
    engine = InterviewPrepEngine()
    engine.export_playbook_markdown(output_path)
    print(f"[OK] Generated Interview Playbook at: {output_path}")
