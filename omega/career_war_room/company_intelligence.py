"""
COMPANY INTELLIGENCE ENGINE
Maintains normalized multi-tier company dossiers (Tier S, A, B, C) with Bangalore presence,
career URLs, hiring signals, and evidence verification.
"""
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from .database import war_room_db

@dataclass
class CompanyDossier:
    company_id: str
    name: str
    industry: str
    tier: str # TIER_S, TIER_A, TIER_B, TIER_C
    bangalore_office: str
    other_india_offices: str
    global_presence: str
    career_page_url: str
    active_hiring_signal: bool
    departments: List[str]
    estimated_career_value: float # 0.0 - 100.0
    source: str
    source_evidence: str
    verification_status: str = "VERIFIED" # VERIFIED, ESTIMATED, UNVERIFIED
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class CompanyIntelligenceEngine:
    def __init__(self):
        self.db = war_room_db
        self._seed_priority_companies()

    def _seed_priority_companies(self):
        seed_data = [
            CompanyDossier(
                company_id="COMP-AMZN",
                name="Amazon Global Operations / AWS",
                industry="E-Commerce, Cloud, Logistics, Supply Chain",
                tier="TIER_S",
                bangalore_office="Bagmane World Technology Centre / WTC Malleshwaram, Bengaluru",
                other_india_offices="Hyderabad, Chennai, Mumbai, Delhi NCR",
                global_presence="Seattle, WA, USA (Worldwide)",
                career_page_url="https://amazon.jobs/en/locations/bangalore-india",
                active_hiring_signal=True,
                departments=["Global Logistics", "Supply Chain Operations", "AWS Business Operations", "Merchant Services"],
                estimated_career_value=96.5,
                source="Official Amazon Jobs Portal",
                source_evidence="Active Bangalore job requisitions in Global Trade Compliance and Transportation Operations",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-MSFT",
                name="Microsoft India Development Centre (IDC)",
                industry="Enterprise Cloud, AI, Software",
                tier="TIER_S",
                bangalore_office="Prestige Ferns Galaxy / Outer Ring Road, Bengaluru",
                other_india_offices="Hyderabad, Noida, Pune, Mumbai",
                global_presence="Redmond, WA, USA (Global)",
                career_page_url="https://careers.microsoft.com/v2/global/en/locations/india/bangalore.html",
                active_hiring_signal=True,
                departments=["Cloud & Enterprise Operations", "Commercial Sales", "Business Strategy"],
                estimated_career_value=97.0,
                source="Microsoft Official Careers",
                source_evidence="Verified active campus & early-in-career requisitions",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-GOOG",
                name="Google India GCC",
                industry="Cloud, AI, Global Advertising & Business Ops",
                tier="TIER_S",
                bangalore_office="Bagmane Constellation Business Park / RMZ Infinity, Bengaluru",
                other_india_offices="Hyderabad, Mumbai, Gurugram",
                global_presence="Mountain View, CA, USA",
                career_page_url="https://www.google.com/about/careers/applications/jobs/results/?location=Bangalore%2C%20India",
                active_hiring_signal=True,
                departments=["Global Business Operations", "Customer Solutions", "Partner Operations"],
                estimated_career_value=98.0,
                source="Google Careers Official",
                source_evidence="Active Business Analyst and Global Strategy postings",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-MAERSK",
                name="A.P. Moller - Maersk Technology & Operations",
                industry="Integrated Container Logistics, Ocean Freight & Supply Chain",
                tier="TIER_S",
                bangalore_office="RMZ EcoWorld, Outer Ring Road, Bellandur, Bengaluru",
                other_india_offices="Mumbai, Chennai, Pune",
                global_presence="Copenhagen, Denmark",
                career_page_url="https://www.maersk.com/careers/search-jobs",
                active_hiring_signal=True,
                departments=["Global Trade Operations", "Supply Chain Management", "Customs Brokerage"],
                estimated_career_value=95.0,
                source="Maersk Careers Portal",
                source_evidence="Continuous hiring for International Logistics Specialists and Trade Analysts",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-SCHN",
                name="Schneider Electric Global Hub",
                industry="Energy Management, Industrial Automation, Supply Chain",
                tier="TIER_A",
                bangalore_office="Attibele Industrial Area & Bagmane Tech Park, Bengaluru",
                other_india_offices="Gurugram, Mumbai, Chennai, Hyderabad",
                global_presence="Rueil-Malmaison, France",
                career_page_url="https://www.se.com/in/en/about-us/careers/",
                active_hiring_signal=True,
                departments=["Global Supply Chain Excellence", "International Procurement", "Digital Energy Ops"],
                estimated_career_value=91.0,
                source="Schneider Official Careers",
                source_evidence="Active postings in Global Purchasing & Supply Chain Strategy",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-DHL",
                name="DHL Global Forwarding & Supply Chain",
                industry="Contract Logistics, Freight Forwarding, Global Trade",
                tier="TIER_A",
                bangalore_office="Electronic City & Airport Logistics Park, Devanahalli, Bengaluru",
                other_india_offices="Mumbai, Delhi, Chennai, Kolkata",
                global_presence="Bonn, Germany",
                career_page_url="https://careers.dhl.com/global/en",
                active_hiring_signal=True,
                departments=["Cross-Border Trade", "Air & Ocean Operations", "Key Account Management"],
                estimated_career_value=89.5,
                source="DHL Careers Official",
                source_evidence="Active India forwarding operations requisitions",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-ACCN",
                name="Accenture Solutions / Strategy & Operations",
                industry="Management Consulting, Global Delivery & Operations",
                tier="TIER_A",
                bangalore_office="IBC Knowledge Park & RMZ Ecospace, Bengaluru",
                other_india_offices="Mumbai, Gurugram, Hyderabad, Pune, Chennai",
                global_presence="Dublin, Ireland (Global)",
                career_page_url="https://www.accenture.com/in-en/careers",
                active_hiring_signal=True,
                departments=["Supply Chain & Operations Consulting", "Global Delivery", "Business Strategy"],
                estimated_career_value=90.0,
                source="Accenture Careers India",
                source_evidence="Active hiring for Business Operations Analyst and International Project Coordinators",
                verification_status="VERIFIED"
            ),
            CompanyDossier(
                company_id="COMP-TGT",
                name="Target in India (Target Enterprise Services GCC)",
                industry="Retail GCC, Merchandising, Supply Chain",
                tier="TIER_A",
                bangalore_office="Manyata Embassy Business Park, Hebbal, Bengaluru",
                other_india_offices="Bengaluru Dedicated Hub",
                global_presence="Minneapolis, MN, USA",
                career_page_url="https://india.target.com/careers",
                active_hiring_signal=True,
                departments=["Global Supply Chain", "Inventory Management", "Merchandising Operations"],
                estimated_career_value=92.0,
                source="Target India Official",
                source_evidence="Active GCC requisitions in Inventory Planning & Global Logistics",
                verification_status="VERIFIED"
            )
        ]
        
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            for c in seed_data:
                cur.execute("""
                INSERT OR REPLACE INTO companies (
                    company_id, name, industry, tier, bangalore_office, other_india_offices,
                    global_presence, career_page_url, active_hiring_signal, departments,
                    estimated_career_value, source, source_evidence, verification_status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    c.company_id, c.name, c.industry, c.tier, c.bangalore_office, c.other_india_offices,
                    c.global_presence, c.career_page_url, c.active_hiring_signal, json.dumps(c.departments),
                    c.estimated_career_value, c.source, c.source_evidence, c.verification_status,
                    c.created_at, c.updated_at
                ))
            conn.commit()

    def get_company(self, company_id: str) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM companies WHERE company_id = ?", (company_id,))
            row = cur.fetchone()
            if row:
                d = dict(row)
                d["departments"] = json.loads(d["departments"])
                return d
            return None

    def list_companies(self, tier: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            if tier:
                cur.execute("SELECT * FROM companies WHERE tier = ? ORDER BY estimated_career_value DESC", (tier,))
            else:
                cur.execute("SELECT * FROM companies ORDER BY estimated_career_value DESC")
            rows = cur.fetchall()
            results = []
            for r in rows:
                d = dict(r)
                d["departments"] = json.loads(d["departments"]) if d["departments"] else []
                results.append(d)
            return results

company_intelligence = CompanyIntelligenceEngine()
