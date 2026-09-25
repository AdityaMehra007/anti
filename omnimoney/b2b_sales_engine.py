"""
OMNIMONEY OS - B2B Sales & Daily Prospecting Engine
Handles high-ticket client acquisition, outreach generation, and CRM state machine.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Any, Optional
import datetime

class LeadStatus(str, Enum):
    NEW = "NEW"
    AUDIT_SENT = "AUDIT_SENT"
    CONTACTED = "CONTACTED"
    CALL_SCHEDULED = "CALL_SCHEDULED"
    WON = "WON"
    LOST = "LOST"

@dataclass
class Prospect:
    id: str
    business_name: str
    category: str
    location: str
    contact_person: str
    phone: str
    email: str
    website: str
    status: LeadStatus
    notes: str
    deal_value_inr: float
    last_activity: str

class B2BSalesEngine:
    """
    Manages cold prospecting pipelines, tailored outreach generation, and deal flow.
    """

    def __init__(self):
        self._prospects: List[Prospect] = self._init_seed_prospects()

    def _init_seed_prospects(self) -> List[Prospect]:
        now = datetime.date.today().isoformat()
        return [
            Prospect(
                id="LEAD-001",
                business_name="Aura Glow Skin & Laser Clinic",
                category="Aesthetic & Dermatology Clinic",
                location="Indiranagar 100ft Road, Bengaluru",
                contact_person="Dr. Sneha Rao (Medical Director)",
                phone="+91 98450 XXXXX",
                email="director@auraglowclinic.in",
                website="https://auraglowclinic.in",
                status=LeadStatus.NEW,
                notes="Currently running 4 active Meta ads for HydraFacial & Acne treatments. Response time to inquiry tested at 4.5 hours.",
                deal_value_inr=20000.0,
                last_activity=now
            ),
            Prospect(
                id="LEAD-002",
                business_name="Peak Form Crossfit & Wellness Hub",
                category="Fitness & Performance",
                location="HSR Layout Sector 4, Bengaluru",
                contact_person="Karthik N. (Co-Founder)",
                phone="+91 99001 XXXXX",
                email="karthik@peakformblr.com",
                website="https://peakformblr.com",
                status=LeadStatus.AUDIT_SENT,
                notes="Sent 60-second Loom showing instant free trial WhatsApp booking bot. WhatsApp opened.",
                deal_value_inr=15000.0,
                last_activity=now
            ),
            Prospect(
                id="LEAD-003",
                business_name="Whitefield Prime Realty Advisors",
                category="Real Estate Brokerage",
                location="Whitefield Main Road, Bengaluru",
                contact_person="Rajesh Varma (Principal Broker)",
                phone="+91 98860 XXXXX",
                email="rajesh@whitefieldprime.com",
                website="https://whitefieldprime.com",
                status=LeadStatus.CONTACTED,
                notes="Follow-up scheduled regarding filtering pre-launch villa leads in Hope Farm area.",
                deal_value_inr=25000.0,
                last_activity=now
            ),
            Prospect(
                id="LEAD-004",
                business_name="Precision Gear Dynamics Exporters",
                category="Industrial Manufacturing & EXIM",
                location="Peenya Industrial Area Phase 2, Bengaluru",
                contact_person="M. S. Sundaram (Managing Partner)",
                phone="+91 94480 XXXXX",
                email="exports@precisiongeardynamics.com",
                website="https://precisiongeardynamics.com",
                status=LeadStatus.NEW,
                notes="Exporting high-precision automotive components to EU. Target trade buyer dossier prepared for German distributor network.",
                deal_value_inr=25000.0,
                last_activity=now
            ),
            Prospect(
                id="LEAD-005",
                business_name="Green Leaf Dental Speciality Center",
                category="Dental Care",
                location="Koramangala 4th Block, Bengaluru",
                contact_person="Dr. Vikram Patel",
                phone="+91 97400 XXXXX",
                email="info@greenleafdental.in",
                website="https://greenleafdental.in",
                status=LeadStatus.CALL_SCHEDULED,
                notes="Demo call confirmed for tomorrow 4:30 PM to review automated Invisalign appointment setter.",
                deal_value_inr=20000.0,
                last_activity=now
            )
        ]

    def get_prospects(self) -> List[Prospect]:
        return self._prospects

    def update_status(self, lead_id: str, new_status: LeadStatus, notes: Optional[str] = None) -> bool:
        for p in self._prospects:
            if p.id == lead_id:
                p.status = new_status
                p.last_activity = datetime.date.today().isoformat()
                if notes:
                    p.notes = f"{p.notes} | {notes}"
                return True
        return False

    def get_pipeline_summary(self) -> Dict[str, Any]:
        total_pipeline_val = sum(p.deal_value_inr for p in self._prospects if p.status != LeadStatus.LOST)
        stage_counts = {status.value: 0 for status in LeadStatus}
        for p in self._prospects:
            stage_counts[p.status.value] += 1

        return {
            "total_leads": len(self._prospects),
            "pipeline_value_inr": total_pipeline_val,
            "won_revenue_inr": sum(p.deal_value_inr for p in self._prospects if p.status == LeadStatus.WON),
            "stages": stage_counts
        }

    def generate_outreach_script(self, template_type: str, prospect_name: str, business_name: str) -> str:
        """Generates hyper-tailored, zero-spam outreach copy."""
        if template_type == "whatsapp_clinic_audit":
            return (
                f"Hi {prospect_name}, quick observation from your Meta ads for {business_name} in Bengaluru.\n\n"
                f"I noticed patients clicking your ad in the evening wait 2–4 hours for appointment confirmation. "
                f"Most book with a nearby competitor within 15 minutes.\n\n"
                f"I built a 60-second AI WhatsApp scheduler that automatically answers treatment questions, checks doctor calendar availability, "
                f"and confirms booking slots instantly 24/7.\n\n"
                f"I recorded a 45-second screen demo showing how it works with {business_name}'s services. Can I send the link over here?"
            )
        elif template_type == "real_estate_broker":
            return (
                f"Hi {prospect_name}, saw your luxury property listings across Whitefield.\n\n"
                f"Most brokers tell us they waste 4+ hours a day calling portal leads who 'just wanted the price' or have no budget.\n\n"
                f"We set up an automated WhatsApp qualifier: as soon as a lead inquires on 99acres or your site, it asks 3 questions "
                f"(Budget, Timeline, Unit type) and only rings your phone when someone has ₹1.8Cr+ pre-qualified capital ready for a site visit.\n\n"
                f"Happy to set this up for you for 3 days completely free to show you the difference. Would tomorrow morning work for a quick 5-min walk-through?"
            )
        elif template_type == "exim_manufacturer":
            return (
                f"Respected {prospect_name},\n\n"
                f"We analyzed European customs clearance records for precision engineering components exported from Peenya.\n\n"
                f"We identified 18 tier-2 machinery distributors in Germany and Netherlands currently purchasing HS Code 8483 parts "
                f"who are diversifying supply away from China.\n\n"
                f"We have compiled a complete Trade Buyer Intelligence Sheet with verified procurement contacts and annual import volumes. "
                f"Would you like us to share the 1-page sample docket with your office?"
            )
        else:
            return (
                f"Hi {prospect_name}, wanted to share a custom AI workflow we built to help {business_name} capture more high-value clients."
            )
