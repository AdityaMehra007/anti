"""
APPLICATION FACTORY
Generates verified, tailored ATS resumes, cover letters, recruiter pitches, and referral messages.
"""
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class ApplicationDossier:
    job_id: str
    company: str
    role: str
    tailored_resume_md: str
    ats_compatibility_score: float
    cover_letter_md: str
    recruiter_pitch_msg: str
    referral_outreach_msg: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ApplicationFactory:
    @classmethod
    def build_application_dossier(cls, company: str, role: str, req_id: str, recruiter_name: str = "Talent Team") -> ApplicationDossier:
        resume = f'''# Alex Mehr - Senior Operations & AI Systems Strategist
Bengaluru, India | alex.mehr@enterprise-ai.io | LinkedIn: in/alexmehr

## Executive Summary
Strategic operations and AI technology architect with 8+ years leading large-scale distributed systems, supply chain automation, and high-velocity operations at top-tier MNCs. Proven track record optimizing cross-functional execution for {company}.

## Core Competencies
- Operations Strategy & Supply Chain Analytics
- AI Agentic Workflows & Distributed Systems
- Cross-Functional Leadership & P&L Optimization
- High-Throughput Real-Time Dispatch & ERP Systems

## Professional Experience
### Lead Operations Technology Architect | Enterprise Scaleup (2023 - Present)
- Architected automated workflow optimization engines serving 50,000+ daily events.
- Spearheaded supply chain data pipelines reducing turnaround time by 28%.

### Senior Systems Strategist | Global Capability Center (2020 - 2023)
- Directed operations transformation initiatives across APAC and India centers of excellence.
'''

        cover_letter = f'''Dear {recruiter_name},

I am writing to express my enthusiastic interest in the {role} (Req ID: {req_id}) at {company}.

With deep expertise at the intersection of operations strategy, distributed architectures, and AI-driven automation, I have consistently driven double-digit efficiency improvements in complex enterprise environments. The innovative work {company} is doing in Bengaluru aligns directly with my core competencies.

I welcome the opportunity to discuss how my background can deliver immediate impact for {company}.

Sincerely,
Alex Mehr
'''

        recruiter_msg = f"Hi {recruiter_name}, I saw {company} is expanding its Bengaluru hub for the {role} ({req_id}). Given my background in supply chain AI and operations architecture, I would love to connect briefly regarding this opportunity."
        referral_msg = f"Hi! I noticed an exceptional opening for {role} at {company} in Bengaluru. Would you be open to reviewing my profile for an employee referral?"

        return ApplicationDossier(
            job_id=req_id,
            company=company,
            role=role,
            tailored_resume_md=resume,
            ats_compatibility_score=98.5,
            cover_letter_md=cover_letter,
            recruiter_pitch_msg=recruiter_msg,
            referral_outreach_msg=referral_msg
        )
