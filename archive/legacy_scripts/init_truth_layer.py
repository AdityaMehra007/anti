"""
Antigravity Autonomous Career Command Center - Candidate Truth Layer Initializer
Builds /career-hub/candidate/ JSON files with strict Evidence-ID traceability.
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(r"e:\anti\career-hub\candidate")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Candidate Profile
candidate_profile = {
    "candidate_id": "CAND-001",
    "first_name": "Aditya",
    "last_name": "Mehra",
    "full_name": "Aditya Mehra",
    "display_name": "Adi / Aditya",
    "email": "adityamehra799@gmail.com",
    "phone": "+91-7003456624",
    "linkedin_url": "https://www.linkedin.com/in/aditya-mehra-b8644b326",
    "location": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "work_authorization": "India Citizen"
    },
    "current_status": "BBA Student / Incoming Graduate (May 2026)",
    "headline": "Business Generalist | Operations Leadership | Business Development | International Business",
    "summary": "Business generalist with hands-on experience across event operations, client management, and business development, built alongside a full-time BBA in International Business from Dayananda Sagar University, Bangalore. Delivered 300+ events and brand activations for corporate clients like Tata Communications and Puma.",
    "years_experience": 8,
    "languages": [
        {"language": "Hindi", "proficiency": "Native"},
        {"language": "Punjabi", "proficiency": "Native"},
        {"language": "Bengali", "proficiency": "Proficient"},
        {"language": "English", "proficiency": "Fluent"},
        {"language": "French", "proficiency": "Conversational"}
    ]
}

# 2. Education Evidence
education = [
    {
        "evidence_id": "EDU-001",
        "institution": "Dayananda Sagar University",
        "degree": "Bachelor of Business Administration (BBA)",
        "specialization": "International Business",
        "location": "Bengaluru, India",
        "start_year": 2023,
        "graduation_date": "May 2026",
        "accreditation": "NAAC Accredited",
        "relevant_coursework": [
            "International Trade & Policy",
            "Global Marketing Strategy",
            "Business Management",
            "Financial Analysis",
            "Professional Communication",
            "Entrepreneurship"
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    }
]

# 3. Experience Evidence
experience_evidence = [
    {
        "evidence_id": "EXP-001",
        "role": "Event Coordinator",
        "organization": "TRILOGY: Indo-Jazz Instrumental Fusion",
        "venue": "Bangalore Club, Bangalore",
        "start_date": "Jan 2026",
        "end_date": "Jan 2026",
        "type": "Contract / Project",
        "key_achievements": [
            "Coordinated live performance headlined by Grammy Award winner Pt. Vishwa Mohan Bhatt alongside Amyt Datta and Pt. Subhen Chatterjee.",
            "Managed full artist logistics pipeline: travel, hospitality, technical riders, and scheduling.",
            "Delivered seamless 3-hour live delivery through real-time multi-party AV and venue coordination."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-002",
        "role": "Business Development Intern",
        "organization": "Pencil Mark Interior Solutions LLP",
        "location": "Bangalore, India",
        "start_date": "Jul 2025",
        "end_date": "Aug 2025",
        "type": "Internship",
        "key_achievements": [
            "Drove client outreach and lead generation campaigns, expanding firm's active pipeline.",
            "Managed 15+ concurrent client communication threads.",
            "Recognized with formal written management commendation at programme conclusion."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-003",
        "role": "AI Data Operations Intern",
        "organization": "Instawork Services India Pvt Ltd",
        "location": "Bangalore, India",
        "start_date": "Dec 2025",
        "end_date": "Dec 2025",
        "type": "Internship",
        "key_achievements": [
            "Contributed to national AI & Robotics data collection initiative structuring activity datasets for ML training pipelines.",
            "Maintained 100% on-time submission and quality compliance across data cycles."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-004",
        "role": "Exhibition Operations Lead",
        "organization": "Salt in My Coca (AERO India 2025)",
        "location": "Yelahanka Air Force Station, Bangalore",
        "start_date": "Feb 2025",
        "end_date": "Feb 2025",
        "type": "7-Day Deployment",
        "key_achievements": [
            "Managed full-week stall setup, brand presentation, product display, inventory, and visitor engagement at Asia's premier defense exposition.",
            "Interacted with international defense delegates, government officials, and 100,000+ visitors."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-005",
        "role": "Community Outreach Intern",
        "organization": "Campusquare Foundation Trust",
        "location": "Bangalore, India",
        "start_date": "Jun 2024",
        "end_date": "Jul 2024",
        "type": "Certified 4-Week Internship",
        "key_achievements": [
            "Delivered community awareness campaigns on educational access engaging underserved communities across Bangalore."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-006",
        "role": "Independent Event Director & Multi-Format Operations Lead",
        "organization": "Freelance Practice",
        "location": "Bangalore & Pan India",
        "start_date": "2019",
        "end_date": "Present",
        "type": "Independent Practice",
        "key_achievements": [
            "Delivered 300+ events across corporate activations, weddings, retail pop-ups, and exhibitions.",
            "Executed brand activations for HP, Intel, Razorpay, Tata Communications, VH1 Supersonic, Vector, Apollo Marketing.",
            "Achieved 15% per-event cost savings through vendor renegotiations and 30%+ repeat client rate."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-007",
        "role": "Co-Founder & Operations Manager",
        "organization": "Mehra's Kitchen",
        "location": "Bangalore, India",
        "start_date": "2025",
        "end_date": "2025",
        "type": "Entrepreneurship (Concluded)",
        "key_achievements": [
            "Developed business concept, menu, pricing, cost analysis, and unit economics model for home-based cloud kitchen.",
            "Operated physical food stall managing daily inventory, customer service, cash handling, and ingredient supply chain."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-008",
        "role": "Field Marketing Executive",
        "organization": "Clinic Health Hub",
        "location": "Bangalore, India",
        "start_date": "2020",
        "end_date": "2020",
        "type": "1-Month Project",
        "key_achievements": [
            "Executed targeted residential and commercial direct-response marketing across Bangalore neighborhoods."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    },
    {
        "evidence_id": "EXP-009",
        "role": "Operations & Sales Associate",
        "organization": "Family Business",
        "location": "Kolkata & Bangalore",
        "start_date": "2018",
        "end_date": "2020",
        "type": "Family Business",
        "key_achievements": [
            "Entered workforce at age 17 managing retail sales, inventory, supplier relations, and daily P&L.",
            "Coordinated strategic operational relocation from Kolkata to Bangalore."
        ],
        "verification_status": "VERIFIED_DOCUMENT"
    }
]

# 4. Certifications Evidence
certifications = [
    {
        "evidence_id": "CERT-001",
        "name": "Generative AI Mastermind",
        "issuer": "Outskill",
        "date": "Oct 2025",
        "verification_status": "VERIFIED_CERTIFICATE"
    },
    {
        "evidence_id": "CERT-002",
        "name": "AI Tools & ChatGPT for Business Productivity",
        "issuer": "be10x",
        "date": "Jan 2026",
        "verification_status": "VERIFIED_CERTIFICATE"
    },
    {
        "evidence_id": "CERT-003",
        "name": "Service Marketing: A Practical Approach",
        "issuer": "IIT Kharagpur / NPTEL / Swayam",
        "date": "Jan - Feb 2025",
        "verification_status": "VERIFIED_CERTIFICATE"
    },
    {
        "evidence_id": "CERT-004",
        "name": "Digital Marketing Professional Certificate",
        "issuer": "Google",
        "date": "2024",
        "verification_status": "VERIFIED_CERTIFICATE"
    }
]

# 5. Achievements Evidence
achievements = [
    {
        "evidence_id": "ACH-001",
        "title": "Outstanding Performance Commendation",
        "organization": "Pencil Mark Interior Solutions LLP",
        "date": "Aug 2025",
        "description": "Formally recognized with written management commendation for exceptional initiative and lead generation performance."
    },
    {
        "evidence_id": "ACH-002",
        "title": "NPTEL Certification",
        "organization": "IIT Kharagpur",
        "date": "Feb 2025",
        "description": "Completed certified service marketing program from premier technical institution."
    },
    {
        "evidence_id": "ACH-003",
        "title": "300+ Events Delivered",
        "organization": "Independent Practice",
        "date": "2019-2026",
        "description": "Delivered 300+ multi-format events over 6 years with 15% cost savings and 30%+ repeat client rate."
    }
]

# Write JSON files
def write_json(filename, data):
    path = BASE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Initialized Truth Layer: {filename}")

write_json("candidate_profile.json", candidate_profile)
write_json("education.json", education)
write_json("experience_evidence.json", experience_evidence)
write_json("certifications.json", certifications)
write_json("achievements.json", achievements)

print("Truth Layer initialization complete!")
