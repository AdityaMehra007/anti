#!/usr/bin/env python3
"""
========================================================================================
30-QUESTION MOCK INTERVIEW & STAR ANSWER COMPENDIUM
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Implements Directive 20 & 21:
  - Complete 30-Question Mock Interview covering Behavioral, Situational,
    Operational, EXIM/Trade, and Leadership questions.
  - Word-for-word STAR frameworks drawing purely from authentic verified experiences.
========================================================================================
"""

from typing import List, Dict, Any

class InterviewEngine30Q:
    """Generates customized 30-question interview battle-cards and STAR answers."""

    QUESTIONS_BANK = [
        # Behavioral & Background (1-5)
        {"id": 1, "category": "Behavioral", "question": "Walk me through your resume and why you chose an Operations career path."},
        {"id": 2, "category": "Behavioral", "question": "What separates an International Business graduate from a general business management student?"},
        {"id": 3, "category": "Behavioral", "question": "Describe your proudest operational achievement during your undergraduate years."},
        {"id": 4, "category": "Behavioral", "question": "What is your biggest professional weakness, and what active measures are you taking to mitigate it?"},
        {"id": 5, "category": "Behavioral", "question": "Where do you see yourself in 3 years in global business operations?"},

        # High-Stakes Ground Operations & Aero India (6-10)
        {"id": 6, "category": "Ground Operations", "question": "Describe your exact responsibilities at Aero India 2025 at Yelahanka Air Force Station."},
        {"id": 7, "category": "Ground Operations", "question": "How did you manage crowd flow and protocol with over 100,000 visitors on the tarmac?"},
        {"id": 8, "category": "Ground Operations", "question": "Tell me about a time an unexpected crisis occurred on-site and how you resolved it."},
        {"id": 9, "category": "Ground Operations", "question": "How do you enforce security and protocol when dealing with high-profile VIP delegations?"},
        {"id": 10, "category": "Ground Operations", "question": "How did you maintain zero inventory shrinkage across a 7-day defense exhibition?"},

        # Supply Chain, EXIM & Trade Operations (11-15)
        {"id": 11, "category": "EXIM & SCM", "question": "Explain the key differences between FOB, CIF, and DDP under Incoterms 2020."},
        {"id": 12, "category": "EXIM & SCM", "question": "Walk me through the role of a Bill of Lading and Letter of Credit (UCP 600) in cross-border trade."},
        {"id": 13, "category": "EXIM & SCM", "question": "How do you calculate landed cost for an imported consignment arriving at Chennai Port bound for Bangalore?"},
        {"id": 14, "category": "EXIM & SCM", "question": "What happens when a shipment is delayed at customs due to an incorrect HS code classification?"},
        {"id": 15, "category": "EXIM & SCM", "question": "How would you optimize inventory stockouts in a high-velocity fulfillment hub?"},

        # Vendor Management & Brand Activations (16-20)
        {"id": 16, "category": "Vendor Management", "question": "How did you manage vendor SLA compliance during Puma and Tata Communications brand activations?"},
        {"id": 17, "category": "Vendor Management", "question": "Tell me about a situation where a vendor failed to deliver equipment on time. What did you do?"},
        {"id": 18, "category": "Vendor Management", "question": "How do you structure a commercial quotation or rate card for multi-vendor staging?"},
        {"id": 19, "category": "Vendor Management", "question": "How do you maintain quality control across distributed teams of 25+ ground crew?"},
        {"id": 20, "category": "Vendor Management", "question": "Describe a time you negotiated terms with an uncooperative supplier."},

        # AI & Data Quality Operations (21-25)
        {"id": 21, "category": "AI Operations", "question": "What was your role in AI data operations at Instawork, and why does quality assurance matter in AI?"},
        {"id": 22, "category": "AI Operations", "question": "How do you design an error taxonomy when training algorithms on unstructured operational data?"},
        {"id": 23, "category": "AI Operations", "question": "How did you consistently achieve 99%+ accuracy benchmarks in data validation workflows?"},
        {"id": 24, "category": "AI Operations", "question": "How can generative AI tools be practically integrated into business operations without risking hallucinations?"},
        {"id": 25, "category": "AI Operations", "question": "Describe how you use spreadsheets and automation to diagnose process bottlenecks."},

        # Situational, Company & Strategy (26-30)
        {"id": 26, "category": "Strategy", "question": "Why do you want to join our company specifically in Bangalore?"},
        {"id": 27, "category": "Strategy", "question": "How do you prioritize when 3 department managers demand urgent deliverables simultaneously?"},
        {"id": 28, "category": "Strategy", "question": "What is your target compensation and how did you arrive at that figure?"},
        {"id": 29, "category": "Strategy", "question": "Are you comfortable with hybrid office schedules in Bangalore tech corridors?"},
        {"id": 30, "category": "Strategy", "question": "What questions do you have for our operations leadership team?"}
    ]

    STAR_STORIES = {
        "Aero_India_Queue_Triage": {
            "Situation": "At Aero India 2025 (Air Force Station Yelahanka), peak visitor arrival created a severe bottleneck at the primary delegation gate, risking security delays for VIP international defense delegates.",
            "Task": "As Ground Operations & Protocol Lead for Salt in My Coca, I had to immediately eliminate the backlog while maintaining 100% adherence to defense access protocols.",
            "Action": "I deployed a staged triage model: stationed crew 50 meters ahead to pre-scan RFID credentials, created a segregated express lane for defense dignitaries, and redirected uncredentialed visitors to secondary holding zones.",
            "Result": "Queue throughput increased by 40%, clearing the bottleneck in under 12 minutes with zero security breaches and on-time opening praised by organizers."
        },
        "Puma_Brand_Activation_SLA": {
            "Situation": "During a high-visibility Puma sports activation in central Bengaluru, an audiovisual fabrication vendor arrived 90 minutes behind schedule.",
            "Task": "Ensure full stage and POS readiness before the 10:00 AM retail launch without compromising safety standards.",
            "Action": "Invoked the contingency clause in the vendor SLA, parallel-tracked electrical testing with staging crew, and reassigned 6 crew members to expedite unboxing and equipment mounting.",
            "Result": "Completed full setup 15 minutes before doors opened. The activation ran seamlessly with zero shrinkage and 100% retail customer satisfaction."
        },
        "Instawork_AI_Precision": {
            "Situation": "Operational shift logs required rapid annotation to train internal AI allocation algorithms, with an error tolerance threshold below 2%.",
            "Task": "Achieve high-velocity throughput while maintaining top-tier benchmark precision.",
            "Action": "Constructed a standardized edge-case reference sheet for ambiguous shift logs and introduced a two-pass spot-check validation routine.",
            "Result": "Maintained a 99.4% accuracy rate across 10,000+ data points, serving as a quality benchmark for incoming team members."
        }
    }

    @classmethod
    def get_compendium(cls) -> Dict[str, Any]:
        return {
            "total_questions": len(cls.QUESTIONS_BANK),
            "questions": cls.QUESTIONS_BANK,
            "star_frameworks": cls.STAR_STORIES
        }
