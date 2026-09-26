"""
COMPANY INTELLIGENCE ENGINE v2
Maintains normalized multi-tier company dossiers (Tier S, Tier A, Tier B) across all 20 priority Bangalore hubs.
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
    tier: str # TIER_S, TIER_A, TIER_B
    bangalore_office: str
    other_india_offices: str
    global_presence: str
    career_page_url: str
    active_hiring_signal: bool
    departments: List[str]
    estimated_career_value: float
    source: str
    source_evidence: str
    verification_status: str = "VERIFIED"
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class CompanyIntelligenceEngine:
    def __init__(self):
        self.db = war_room_db
        self._seed_all_20_companies()

    def _seed_all_20_companies(self):
        seed_data = [
            CompanyDossier("COMP-AMZN", "Amazon Global Operations / AWS", "E-Commerce, Cloud, Supply Chain", "TIER_S", "Bagmane World Technology Centre / WTC Malleshwaram, Bengaluru", "Hyderabad, Chennai, Mumbai, Delhi", "Seattle, WA, USA", "https://amazon.jobs/en/locations/bangalore-india", True, ["Global Logistics", "Supply Chain Operations", "AWS Trade Compliance"], 98.0, "Amazon Official Jobs", "Active Bangalore Trade & Logistics reqs"),
            CompanyDossier("COMP-MSFT", "Microsoft India Development Centre", "Enterprise Cloud, AI, Software", "TIER_S", "Prestige Ferns Galaxy, Bellandur, Bengaluru", "Hyderabad, Noida, Pune", "Redmond, WA, USA", "https://careers.microsoft.com/v2/global/en/locations/india/bangalore.html", True, ["Cloud Business Operations", "Commercial Sales", "AI Operations"], 97.5, "Microsoft Careers", "Active early-career openings"),
            CompanyDossier("COMP-GOOG", "Google India GCC", "Cloud, AI, Global Advertising & Business Ops", "TIER_S", "Bagmane Constellation Business Park / RMZ Infinity, Bengaluru", "Hyderabad, Mumbai, Gurugram", "Mountain View, CA, USA", "https://www.google.com/about/careers/applications/jobs/results/?location=Bangalore%2C%20India", True, ["Global Business Operations", "Partner Solutions"], 98.5, "Google Careers", "Active Business Analyst postings"),
            CompanyDossier("COMP-MAERSK", "A.P. Moller - Maersk", "Integrated Container Logistics & Ocean Freight", "TIER_S", "RMZ EcoWorld, Outer Ring Road, Bellandur, Bengaluru", "Mumbai, Chennai, Pune", "Copenhagen, Denmark", "https://www.maersk.com/careers/search-jobs", True, ["Global Trade Operations", "Supply Chain Management", "Customs Brokerage"], 95.0, "Maersk Careers", "Continuous logistics specialist hiring"),
            CompanyDossier("COMP-GS", "Goldman Sachs Services", "Investment Banking & Financial Operations", "TIER_S", "Helios Business Park, Kadubeesanahalli, Bengaluru", "Mumbai, Hyderabad", "New York, NY, USA", "https://www.goldmansachs.com/careers", True, ["Global Operations", "Trade Settlement", "Risk Management"], 96.0, "Goldman Sachs Careers", "Active trade analyst requisitions"),
            CompanyDossier("COMP-JPMC", "JPMorgan Chase & Co. GBS", "Global Banking & Cross-Border Financial Operations", "TIER_S", "Prestige Tech Park, Marathahalli-Sarjapur ORR, Bengaluru", "Mumbai, Hyderabad", "New York, NY, USA", "https://jpmorganchase.com/careers", True, ["International Operations", "Trade Governance"], 95.5, "JPMC Official", "Active operations requisitions"),
            CompanyDossier("COMP-WMT", "Walmart Global Tech India", "Retail Tech, Global Sourcing & Supply Chain", "TIER_S", "Cessna Business Park, Kadubeesanahalli, Bengaluru", "Chennai, Gurugram", "Bentonville, AR, USA", "https://careers.walmart.com", True, ["Retail Operations", "Cross-Border Sourcing", "Supply Chain"], 94.5, "Walmart Careers", "Active Bangalore supply chain reqs"),
            CompanyDossier("COMP-CSCO", "Cisco Systems India", "Networking & Global Trade Logistics", "TIER_A", "Cisco Campus, SEZ, Sarjapur, Bengaluru", "Mumbai, Delhi, Chennai", "San Jose, CA, USA", "https://jobs.cisco.com", True, ["Global Logistics", "Export Compliance", "Carrier SLA"], 92.0, "Cisco Careers", "Active trade specialist openings"),
            CompanyDossier("COMP-SCHN", "Schneider Electric Global Hub", "Energy Management & Global Procurement", "TIER_A", "Bagmane Tech Park, CV Raman Nagar, Bengaluru", "Gurugram, Mumbai, Chennai", "Rueil-Malmaison, France", "https://www.se.com/in/en/about-us/careers/", True, ["Global Supply Chain Excellence", "International Procurement"], 91.0, "Schneider Careers", "Active supply chain planning reqs"),
            CompanyDossier("COMP-TGT", "Target in India GCC", "Retail Merchandising & Inventory Operations", "TIER_A", "Manyata Embassy Business Park, Hebbal, Bengaluru", "Dedicated Bengaluru Hub", "Minneapolis, MN, USA", "https://india.target.com/careers", True, ["Inventory Management", "Global Sourcing", "Supply Chain"], 92.5, "Target India Official", "Active GCC inventory analyst openings"),
            CompanyDossier("COMP-DHL", "DHL Global Forwarding", "Freight Forwarding & Contract Logistics", "TIER_A", "Electronic City & Airport Logistics Park, Bengaluru", "Mumbai, Delhi, Chennai", "Bonn, Germany", "https://careers.dhl.com/global/en", True, ["Air/Ocean Operations", "Customs Brokerage", "Trade Logistics"], 89.5, "DHL Careers", "Active forwarding coordinator openings"),
            CompanyDossier("COMP-ACCN", "Accenture Solutions", "Management Consulting & International Operations", "TIER_A", "IBC Knowledge Park & RMZ Ecospace, Bengaluru", "Mumbai, Gurugram, Hyderabad", "Dublin, Ireland", "https://www.accenture.com/in-en/careers", True, ["Operations Consulting", "Supply Chain Strategy"], 90.0, "Accenture India", "Active operations analyst reqs"),
            CompanyDossier("COMP-DELL", "Dell Technologies", "Technology Hardware & Global Supply Planning", "TIER_A", "Domlur Inner Ring Road & Bagmane Parin, Bengaluru", "Hyderabad, Gurugram", "Round Rock, TX, USA", "https://jobs.dell.com", True, ["Demand Planning", "Inbound Logistics", "Vendor Performance"], 90.5, "Dell Official", "Active supply chain planner openings"),
            CompanyDossier("COMP-BOSCH", "Bosch Global Technologies", "Automotive, Industrial & Sourcing Operations", "TIER_A", "Adugodi & Electronic City, Bengaluru", "Pune, Coimbatore, Chennai", "Gerlingen, Germany", "https://careers.smartrecruiters.com/BoschGroup", True, ["Strategic Sourcing", "Procurement Operations", "SAP MM"], 91.5, "Bosch Group", "Active procurement specialist reqs"),
            CompanyDossier("COMP-SHELL", "Shell Business Operations", "Energy Trade, Contracting & Procurement", "TIER_A", "Shell Technology Centre, RMZ Galleria, Yelahanka, Bengaluru", "Chennai, Mumbai", "London, UK", "https://jobs.shell.com", True, ["Commodity Trade Documentation", "Contracting & Procurement"], 92.0, "Shell Careers", "Active trade operations reqs"),
            CompanyDossier("COMP-STAN", "Standard Chartered GBS", "Trade Finance & Cross-Border Banking Operations", "TIER_A", "RMZ EcoSpace, Bellandur, Bengaluru", "Chennai, Mumbai", "London, UK", "https://scb.taleo.net", True, ["Trade Finance", "Letters of Credit", "Sanctions Screening"], 91.0, "Standard Chartered", "Active trade finance reqs"),
            CompanyDossier("COMP-UL", "Unilever Global Operations Hub", "FMCG Global Supply Chain & Customer Ops", "TIER_A", "Prestige Shantiniketan, Whitefield, Bengaluru", "Mumbai, Gurugram", "London, UK", "https://unilever.taleo.net", True, ["Customer Operations", "Export Logistics", "Supply Planning"], 92.0, "Unilever Careers", "Active supply chain associate reqs"),
            CompanyDossier("COMP-FDX", "FedEx Express India", "Express Transportation & Customs Clearance", "TIER_B", "KIA Airport Cargo Terminal, Devanahalli, Bengaluru", "Mumbai, Delhi, Chennai", "Memphis, TN, USA", "https://fedex.wd1.myworkdayjobs.com", True, ["Customs Clearance", "Air Cargo Operations", "Import Compliance"], 87.0, "FedEx Careers", "Active customs specialist reqs"),
            CompanyDossier("COMP-IBM", "IBM India", "Enterprise Tech, Procurement & Operations", "TIER_B", "Embassy Golf Links, Domlur, Bengaluru", "Hyderabad, Gurugram, Pune", "Armonk, NY, USA", "https://ibm.com/careers", True, ["Procurement Analytics", "Supplier Governance", "Process Automation"], 88.5, "IBM Careers", "Active procurement analyst reqs"),
            CompanyDossier("COMP-FK", "Flipkart (Walmart Group)", "E-Commerce Supply Chain & First/Last Mile Ops", "TIER_A", "Embassy Tech Village, Bellandur, Bengaluru", "Hyderabad, Mumbai, Gurugram", "Bengaluru, India", "https://flipkartcareers.com", True, ["Fulfilment Logistics", "Supply Chain Strategy", "Warehouse Analytics"], 92.5, "Flipkart Careers", "Active supply chain associate reqs")
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
                val = d.get("departments")
                if val:
                    try:
                        d["departments"] = json.loads(val)
                    except (json.JSONDecodeError, TypeError):
                        d["departments"] = [x.strip() for x in str(val).split(",") if x.strip()]
                else:
                    d["departments"] = []
                office = d.get("bangalore_office") or ""
                if "Bengaluru" not in office:
                    d["bangalore_office"] = f"{office}, Bengaluru".lstrip(", ") if office else "Bengaluru"
                results.append(d)
            return results

company_intelligence = CompanyIntelligenceEngine()
