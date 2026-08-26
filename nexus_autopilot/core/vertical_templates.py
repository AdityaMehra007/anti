"""
NEXUS AUTOPILOT - Industry Vertical Templates Engine
Provides pre-built workflow schemas, default fields, and automation rules for:
1. Distributors, 2. Agencies, 3. Event Businesses, 4. Clinics, 5. Contractors
"""
from typing import Dict, Any, List

class VerticalTemplatesEngine:
    def __init__(self):
        self.templates = {
            "DISTRIBUTOR": {
                "vertical_name": "Industrial & FMCG Distributors",
                "core_workflows": ["order_capture", "repeat_ordering", "quotations", "invoices", "payment_reminders", "credit_monitoring"],
                "default_line_items": [{"item": "Corrugated Boxes 3-Ply", "unit": "box", "hsn": "48191000", "default_rate": 420.0}],
                "payment_terms_days": 15,
                "credit_limit_inr": 500000.0,
                "risk_threshold_days": 10
            },
            "AGENCY": {
                "vertical_name": "B2B Marketing & Creative Agencies",
                "core_workflows": ["lead_capture", "proposals", "client_approvals", "retainer_invoicing", "milestone_billing"],
                "default_line_items": [{"item": "Monthly Performance Marketing Retainer", "unit": "month", "sac": "998311", "default_rate": 75000.0}],
                "payment_terms_days": 30,
                "credit_limit_inr": 200000.0,
                "risk_threshold_days": 15
            },
            "EVENT": {
                "vertical_name": "Event Organizers & Production Houses",
                "core_workflows": ["enquiry_capture", "requirement_extraction", "quotation_generation", "vendor_coordination", "advance_collection"],
                "default_line_items": [{"item": "Stage & AV Production Setup", "unit": "event", "sac": "998596", "default_rate": 150000.0}],
                "payment_terms_days": 7,
                "credit_limit_inr": 300000.0,
                "risk_threshold_days": 5
            },
            "CLINIC": {
                "vertical_name": "Clinics & Healthcare Centers",
                "core_workflows": ["enquiry_management", "appointment_workflows", "payment_requests", "invoices", "repeat_service_campaigns"],
                "default_line_items": [{"item": "Executive Health Consultation & Diagnostics", "unit": "session", "sac": "999312", "default_rate": 2500.0}],
                "payment_terms_days": 0, # Immediate / Advance
                "credit_limit_inr": 0.0,
                "risk_threshold_days": 3
            },
            "CONTRACTOR": {
                "vertical_name": "Infrastructure & Civil Contractors",
                "core_workflows": ["quotation", "work_orders", "milestone_invoices", "payment_collection", "expense_capture", "vendor_coordination"],
                "default_line_items": [{"item": "Milestone 1: Civil Foundation & Framework", "unit": "milestone", "sac": "995411", "default_rate": 500000.0}],
                "payment_terms_days": 21,
                "credit_limit_inr": 1000000.0,
                "risk_threshold_days": 14
            }
        }

    def get_template(self, industry_code: str) -> Dict[str, Any]:
        return self.templates.get(industry_code.upper(), self.templates["DISTRIBUTOR"])

if __name__ == "__main__":
    v = VerticalTemplatesEngine()
    print("[VERTICALS] Distributor Template Loaded:", v.get_template("DISTRIBUTOR")["vertical_name"])
