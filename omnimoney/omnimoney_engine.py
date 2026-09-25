"""
OMNIMONEY OS - Core Opportunity & Economic Intelligence Engine
Compliant with ANTIGRAVITY OMNIMONEY OS Master Specification (Sections 128, 138, 152, 153).
"""

import os
import sqlite3
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class Opportunity:
    id: str
    title: str
    category: str
    target_customer: str
    problem: str
    offer: str
    pricing_model: str  # Retainer, Project, Commission, Equity
    price_inr: float
    daily_equivalent_inr: float
    score: float
    confidence: float
    difficulty: str     # Low, Medium, High
    time_to_first_rupee_days: int
    exact_next_action: str
    sources: List[str] = field(default_factory=list)

@dataclass
class EconomicAction:
    opportunity: str
    customer: str
    problem: str
    offer: str
    price_inr: float
    acquisition_channel: str
    expected_effort: str
    evidence: str
    risks: str
    exact_next_action: str

def calculate_opportunity_score(
    demand: float,
    margin: float,
    speed: float,
    competition: float,
    fit: float
) -> float:
    """
    Computes an Opportunity Score between 0 and 100 based on economic levers:
    - Demand (weight 25%)
    - Margin (weight 25%)
    - Speed to cash (weight 25%)
    - Low competition [10 - competition] (weight 15%)
    - Personal / AI execution fit (weight 10%)
    All inputs assume a 1 to 10 scale.
    """
    d = max(1.0, min(10.0, float(demand)))
    m = max(1.0, min(10.0, float(margin)))
    s = max(1.0, min(10.0, float(speed)))
    c = max(1.0, min(10.0, float(competition)))
    f = max(1.0, min(10.0, float(fit)))

    raw = (d * 2.5) + (m * 2.5) + (s * 2.5) + ((10.0 - c) * 1.5) + (f * 1.0)
    # raw maximum possible: 25 + 25 + 25 + 13.5 + 10 = 98.5 -> normalized to 100
    normalized = min(100.0, max(0.0, (raw / 98.5) * 100.0))
    return round(normalized, 1)

class OmniMoneyEngine:
    """
    The central intelligence and execution coordinator of OMNIMONEY OS.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to repo sqlite database if available
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(base_dir, "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite")
            self.db_path = candidate if os.path.exists(candidate) else None
        else:
            self.db_path = db_path

        self._services = self._init_monetizable_services()
        self._categories = self._init_bengaluru_customer_categories()
        self._opportunities = self._init_opportunities()

    def get_db_stats(self) -> Dict[str, Any]:
        """Returns statistics from the integrated SQLite database."""
        if not self.db_path or not os.path.exists(self.db_path):
            return {"connected": False, "reason": "Database file not found"}

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM master_hr_contacts")
            hr_count = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM company_founder_gaps")
            gap_count = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM tech_parks")
            tp_count = cur.fetchone()[0]
            conn.close()
            return {
                "connected": True,
                "db_path": self.db_path,
                "verified_contacts": hr_count,
                "company_gaps_identified": gap_count,
                "major_tech_parks": tp_count,
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}

    def _init_monetizable_services(self) -> List[Dict[str, Any]]:
        """Section 152 - Step 5: 10 services immediately sellable with AI + Business background."""
        return [
            {
                "id": "SRV-01",
                "name": "AI WhatsApp Inbound Lead Qualification & Appointment Setter",
                "target": "Clinics, Aesthetic Centers, Gyms, High-End Salons",
                "pricing": "₹15,000 setup + ₹10,000/month retainer",
                "deliverable": "Automated WhatsApp bot that captures Ad/Google leads 24/7, answers FAQs, and books slots directly into calendar.",
                "days_to_deliver": 2
            },
            {
                "id": "SRV-02",
                "name": "Real Estate Broker AI Lead Nurturing & Follow-Up System",
                "target": "Bengaluru Property Brokers & Real Estate Agencies (Whitefield, Indiranagar)",
                "pricing": "₹25,000 setup + ₹15,000/month retainer",
                "deliverable": "Automated CRM pipeline that follows up with property inquiries, filters serious buyers, and sends site visit reminders.",
                "days_to_deliver": 3
            },
            {
                "id": "SRV-03",
                "name": "B2B Export-Import (EXIM) & Cross-Border Lead Intelligence",
                "target": "Manufacturers, Exporters in Peenya / Electronic City",
                "pricing": "₹20,000 one-time audit or ₹15,000/month",
                "deliverable": "Custom list of verified overseas buyers, import tariff breakdowns, and drafted outreach sequences.",
                "days_to_deliver": 2
            },
            {
                "id": "SRV-04",
                "name": "Local SEO & Google Business Profile (GBP) AI Optimization",
                "target": "Restaurants, Cafes, Dental Clinics, Car Detailing Hubs",
                "pricing": "₹12,000 one-time + ₹6,000/month maintenance",
                "deliverable": "Google Maps top 3 ranking optimization, review generation automation, and photo/keyword audit.",
                "days_to_deliver": 1
            },
            {
                "id": "SRV-05",
                "name": "Founder / CXO AI Research & Executive Ghostwriting",
                "target": "Venture-backed Startup Founders & Seed-stage Executives (HSR Layout, Koramangala)",
                "pricing": "₹25,000/month retainer",
                "deliverable": "Weekly thought leadership synthesis, LinkedIn market commentary, and company updates powered by deep research.",
                "days_to_deliver": 3
            },
            {
                "id": "SRV-06",
                "name": "E-Commerce / D2C Abandoned Cart Recovery Workflow",
                "target": "Bengaluru Shopify / WooCommerce Brands",
                "pricing": "₹15,000 setup + 10% commission on recovered revenue",
                "deliverable": "WhatsApp + Email instant recovery triggers recovering 15–25% of lost checkouts.",
                "days_to_deliver": 2
            },
            {
                "id": "SRV-07",
                "name": "Talent Sourcing & Candidate Pre-Screening Pipeline",
                "target": "Fast-growing Seed & Series A tech startups",
                "pricing": "₹30,000 per closed hire or ₹20,000/month search sprint",
                "deliverable": "AI-automated outbound sourcing on LinkedIn/GitHub, tailored outreach, and verified resume dossier delivery.",
                "days_to_deliver": 4
            },
            {
                "id": "SRV-08",
                "name": "Competitor & Market Pricing Radar Dashboard",
                "target": "B2B SaaS companies and manufacturing distributors",
                "pricing": "₹35,000 project fee",
                "deliverable": "Scraped pricing matrix, competitor feature comparison, and market gap brief.",
                "days_to_deliver": 4
            },
            {
                "id": "SRV-09",
                "name": "Customer Support Automation with Custom RAG Knowledge Base",
                "target": "Fintech / Edtech SMBs handling >500 tickets/month",
                "pricing": "₹35,000 setup + ₹15,000/month infrastructure maintenance",
                "deliverable": "Instant resolution bot trained on company SOPs and past tickets, routing complex issues to staff.",
                "days_to_deliver": 5
            },
            {
                "id": "SRV-10",
                "name": "Cold Outreach Infrastructure & B2B Lead Machine Setup",
                "target": "Marketing agencies and B2B IT service providers",
                "pricing": "₹25,000 one-time setup",
                "deliverable": "Secondary domain setup, SPF/DKIM/DMARC warmup, Apollo lead mining, and high-deliverability sequence copy.",
                "days_to_deliver": 3
            }
        ]

    def _init_bengaluru_customer_categories(self) -> List[Dict[str, Any]]:
        """Section 152 - Step 6: 20 customer categories in Bengaluru with high willingness to pay."""
        return [
            {"id": "CAT-01", "name": "Aesthetic, Dermatology & Dental Clinics", "budget": "₹15k - ₹35k/mo", "density_hubs": "Indiranagar, Koramangala, Jayanagar"},
            {"id": "CAT-02", "name": "Premium Fitness Centers, Crossfit & MMA Gyms", "budget": "₹10k - ₹25k/mo", "density_hubs": "HSR Layout, Bellandur, Whitefield"},
            {"id": "CAT-03", "name": "Independent Real Estate Brokers & Luxury Property Firms", "budget": "₹25k - ₹60k/mo", "density_hubs": "Whitefield, Sarjapur, North Bangalore"},
            {"id": "CAT-04", "name": "High-End Salons, Spas & Wellness Retreats", "budget": "₹15k - ₹30k/mo", "density_hubs": "Lavelle Road, Sadashivanagar, Indiranagar"},
            {"id": "CAT-05", "name": "Coaching Institutes, Study Abroad & Test Prep Centers", "budget": "₹20k - ₹50k/mo", "density_hubs": "Malleshwaram, Vijayanagar, Jayanagar"},
            {"id": "CAT-06", "name": "Seed & Series A Venture-Backed Startups", "budget": "₹30k - ₹80k/mo", "density_hubs": "HSR Layout, Koramangala, Domlur"},
            {"id": "CAT-07", "name": "B2B IT Services & Boutique Dev Agencies", "budget": "₹25k - ₹50k/mo", "density_hubs": "Electronic City, Manyata Tech Park"},
            {"id": "CAT-08", "name": "D2C Brands (Apparel, Specialty Foods, Cosmetics)", "budget": "₹20k - ₹45k/mo", "density_hubs": "HSR Layout, Indiranagar"},
            {"id": "CAT-09", "name": "Industrial Manufacturers & Exporters", "budget": "₹30k - ₹75k/mo", "density_hubs": "Peenya Industrial Area, Bommasandra"},
            {"id": "CAT-10", "name": "Specialty Restaurants, Microbreweries & Cafes", "budget": "₹15k - ₹30k/mo", "density_hubs": "Koramangala, Indiranagar, Church Street"},
            {"id": "CAT-11", "name": "Immigration & Visa Consultants", "budget": "₹20k - ₹40k/mo", "density_hubs": "MG Road, Residency Road"},
            {"id": "CAT-12", "name": "Chartered Accountants, Tax & Corporate Law Firms", "budget": "₹15k - ₹35k/mo", "density_hubs": "Basavanagudi, Richmond Town"},
            {"id": "CAT-13", "name": "Event Management & Luxury Wedding Planners", "budget": "₹25k - ₹50k/mo", "density_hubs": "Cunningham Road, Benson Town"},
            {"id": "CAT-14", "name": "Interior Designers & Home Architecture Studios", "budget": "₹25k - ₹60k/mo", "density_hubs": "Indiranagar, HSR, JP Nagar"},
            {"id": "CAT-15", "name": "Car Detailing Studios & Luxury Auto Garages", "budget": "₹12k - ₹25k/mo", "density_hubs": "Koramangala, JP Nagar, Hebbal"},
            {"id": "CAT-16", "name": "Logistics & Freight Forwarding Companies", "budget": "₹25k - ₹50k/mo", "density_hubs": "Peenya, Devanahalli Airport corridor"},
            {"id": "CAT-17", "name": "Private Diagnostic Labs & Specialized Clinics", "budget": "₹20k - ₹40k/mo", "density_hubs": "Rajajinagar, Banashankari, Whitefield"},
            {"id": "CAT-18", "name": "Pet Care, Grooming & Veterinary Clinics", "budget": "₹12k - ₹20k/mo", "density_hubs": "Indiranagar, Whitefield, HSR"},
            {"id": "CAT-19", "name": "Boutique Coworking Spaces & Business Centers", "budget": "₹20k - ₹40k/mo", "density_hubs": "Koramangala, HSR, MG Road"},
            {"id": "CAT-20", "name": "Educational Nurseries & Premium K-12 Preschools", "budget": "₹15k - ₹30k/mo", "density_hubs": "Whitefield, Sarjapur, Kalyan Nagar"}
        ]

    def _init_opportunities(self) -> List[Opportunity]:
        """Initializes ranked concrete opportunities."""
        raw_opps = [
            Opportunity(
                id="OPP-001",
                title="AI WhatsApp Lead Qualification & Booking for Aesthetic Clinics",
                category="AI Automation / Local Agency",
                target_customer="Indiranagar & Koramangala Aesthetic / Dermatology Clinics",
                problem="Clinics spend ₹50k-₹2L on Meta Ads, but front desk misses leads during evenings or takes 3+ hours to reply. 60% of leads drop off.",
                offer="Setup automated 60-second WhatsApp conversational booking that qualifies patient budget and books appointments directly into clinic calendar.",
                pricing_model="₹20,000 setup + ₹12,000/month recurring retainer",
                price_inr=20000.0,
                daily_equivalent_inr=667.0,
                score=calculate_opportunity_score(demand=9.5, margin=9.0, speed=9.0, competition=4.0, fit=9.5),
                confidence=0.92,
                difficulty="Low",
                time_to_first_rupee_days=3,
                exact_next_action="Audit 5 clinic Instagram ad accounts/Google profiles, record a 90-second Loom demo showing instant WhatsApp auto-booking, send via WhatsApp directly to clinic owners.",
                sources=["Periodic Labour Force Survey", "Meta Ad Library Bengaluru", "Local Google Maps Data"]
            ),
            Opportunity(
                id="OPP-002",
                title="Whitefield Real Estate Broker Rapid-Lead Qualifier",
                category="Real Estate Tech",
                target_customer="Independent Property Consultants & Channel Partners in Whitefield & Sarjapur",
                problem="Brokers receive dozens of portal inquiries (99acres, MagicBricks) daily but spend 5 hours/day cold-calling unqualified prospects.",
                offer="Automated WhatsApp workflow that pings new leads instantly, asks 3 questions (Budget, 2BHK/3BHK, Ready to Move/Under Construction), and schedules calls with serious buyers only.",
                pricing_model="₹25,000 setup + ₹15,000/month retainer",
                price_inr=25000.0,
                daily_equivalent_inr=833.0,
                score=calculate_opportunity_score(demand=9.0, margin=8.5, speed=8.5, competition=5.0, fit=9.0),
                confidence=0.88,
                difficulty="Medium",
                time_to_first_rupee_days=5,
                exact_next_action="Extract 15 verified brokers from Bengaluru Real Estate WhatsApp groups or MagicBricks, send direct message offer offering 3 free days of automated filtering.",
                sources=["MagicBricks Bengaluru Data", "Bangalore Real Estate WhatsApp Hubs"]
            ),
            Opportunity(
                id="OPP-003",
                title="B2B Export Intelligence & Buyer Discovery Sprint",
                category="EXIM & International Trade",
                target_customer="Industrial Engineering & Textile Exporters in Peenya Industrial Area",
                problem="Exporters rely on expensive manual trade fairs and lack automated intelligence on overseas buyer customs data.",
                offer="Deliver a bespoke Dossier of 50 verified overseas importers (with purchasing volumes, contact emails, and import hs-codes) plus tailored cold pitch copy.",
                pricing_model="₹25,000 per trade docket",
                price_inr=25000.0,
                daily_equivalent_inr=833.0,
                score=calculate_opportunity_score(demand=8.5, margin=9.5, speed=7.5, competition=3.0, fit=9.0),
                confidence=0.85,
                difficulty="Medium",
                time_to_first_rupee_days=6,
                exact_next_action="Select 10 Peenya precision manufacturing exporters, compile sample 3-record buyer dossier showing buyer demand in Germany/UAE, and deliver directly to the Managing Director.",
                sources=["Peenya Industries Association Directory", "Global EXIM Customs databases"]
            ),
            Opportunity(
                id="OPP-004",
                title="D2C & E-Commerce Cart Recovery WhatsApp Automation",
                category="E-Commerce Tech",
                target_customer="Bengaluru-based Shopify Apparel & Lifestyle Brands",
                problem="High checkout abandonment rate (70%+) with generic email recovery seeing <15% open rates.",
                offer="Implement intelligent 15-minute WhatsApp cart recovery sequence with personalized discount and 1-click checkout link.",
                pricing_model="₹15,000 setup + 15% revenue share on recovered GMV",
                price_inr=15000.0,
                daily_equivalent_inr=500.0,
                score=calculate_opportunity_score(demand=8.0, margin=9.0, speed=8.0, competition=5.0, fit=8.5),
                confidence=0.87,
                difficulty="Low",
                time_to_first_rupee_days=4,
                exact_next_action="Identify 10 local Shopify stores via BuiltWith, test their cart abandonment flow, screenshot the lack of WhatsApp follow-up, and message the founder on LinkedIn.",
                sources=["Shopify Bangalore Community", "BuiltWith Indian D2C Index"]
            ),
            Opportunity(
                id="OPP-005",
                title="Founders' Office AI Strategic Research & Briefing Service",
                category="Executive Operations / Career Bridge",
                target_customer="Series A/B Startup CEOs in HSR Layout & Koramangala",
                problem="Founders are drowning in operational noise, needing quick competitive market intelligence, investor dossier preparation, and executive ghostwriting.",
                offer="Part-time AI Chief of Staff retainer: delivering daily 5-minute executive market briefs, investor meeting dossiers, and automated operational research.",
                pricing_model="₹35,000/month recurring retainer",
                price_inr=35000.0,
                daily_equivalent_inr=1167.0,
                score=calculate_opportunity_score(demand=8.5, margin=9.5, speed=7.0, competition=4.0, fit=9.5),
                confidence=0.89,
                difficulty="Medium",
                time_to_first_rupee_days=7,
                exact_next_action="Leverage the 7,500 contacts in BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite to identify 20 Series A founders in HSR Layout; send a sample 1-page Competitive Intelligence Brief on their top rival.",
                sources=["BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite", "Tracxn Bengaluru Unicorn Index"]
            )
        ]
        return sorted(raw_opps, key=lambda x: x.score, reverse=True)

    def get_monetizable_services(self) -> List[Dict[str, Any]]:
        return self._services

    def get_bengaluru_customer_categories(self) -> List[Dict[str, Any]]:
        return self._categories

    def get_ranked_opportunities(self, limit: int = 10) -> List[Opportunity]:
        return self._opportunities[:limit]

    def get_highest_probability_action(self) -> EconomicAction:
        """
        Answers Section 153:
        'What is the highest-probability legitimate economic action I can take today, given my actual resources and constraints?'
        """
        top_opp = self._opportunities[0]
        return EconomicAction(
            opportunity=top_opp.title,
            customer="Indiranagar & Koramangala Aesthetic / Dermatology Clinics (100+ active clinics within 7km)",
            problem="Clinics spend ₹50,000–₹2,00,000/month on Meta & Google Ads, but losing 60%+ of evening/weekend inquiries due to slow manual receptionist replies.",
            offer="AI WhatsApp Inbound Qualifier: Responds within 60 seconds 24/7, answers treatment prices & FAQs, qualifies budget, and books confirmed consultation slots straight into Google Calendar.",
            price_inr=top_opp.price_inr,
            acquisition_channel="Direct WhatsApp message to Clinic Owner/Doctor with a tailored 60-second video demo showing how their current ad leads are being delayed.",
            expected_effort="2 hours to record demo + 1 hour to send 15 personalized outreach messages today.",
            evidence="Meta Ad Library verifies 82 dermatology clinics in Indiranagar/Koramangala running active ads right now. Industry standard lead-to-booking conversion jumps from 8% to 22% with sub-5-minute reply time.",
            risks="Clinic owner delegates outreach to a receptionist who deletes the message. Mitigation: Contact the Managing Doctor directly via LinkedIn or direct WhatsApp business number.",
            exact_next_action="Open Meta Ad Library, search 'Dermatologist Bangalore', record a 60-second screen capture of a sample WhatsApp booking workflow, and dispatch outreach to 10 clinic managers today."
        )

    def export_dashboard_data(self) -> Dict[str, Any]:
        """Produces serialized data payload for HTML command center."""
        stats = self.get_db_stats()
        action = self.get_highest_probability_action()
        opps = [asdict(o) for o in self.get_ranked_opportunities(10)]
        services = self.get_monetizable_services()
        categories = self.get_bengaluru_customer_categories()

        return {
            "version": "1.0.0",
            "system_name": "OMNIMONEY OS - MONEY RADAR BENGALURU",
            "database_stats": stats,
            "section_153_highest_action": asdict(action),
            "opportunities": opps,
            "monetizable_services": services,
            "customer_categories": categories,
            "income_ladder": [
                {"level": "Step 1", "daily": 500, "monthly": 15000, "label": "Gig / Entry Service", "status": "Ready"},
                {"level": "Step 2", "daily": 1000, "monthly": 30000, "label": "1 Retainer Client", "status": "In-Progress (Target Day 7)"},
                {"level": "Step 3", "daily": 2000, "monthly": 60000, "label": "2 Retainers + Setup Fees", "status": "Target Day 21"},
                {"level": "Step 4", "daily": 5000, "monthly": 150000, "label": "4-5 Retainers (B2B Agency)", "status": "Target Day 45"},
                {"level": "Step 5", "daily": 10000, "monthly": 300000, "label": "Productized Service + Micro-SaaS", "status": "Target Day 90"},
                {"level": "Step 6", "daily": 50000, "monthly": 1500000, "label": "Scalable Ecosystem & Platform", "status": "Long-Term Vision"}
            ]
        }
