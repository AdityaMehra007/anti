import json, uuid
from datetime import datetime

class SovereignCRM:
    '''Enterprise CRM, Lead Scoring, Invoicing & Churn Prediction Engine.'''
    def __init__(self):
        self.leads = []
        self.deals = []
        self.invoices = []

    def add_lead(self, company_name, contact_name, deal_size_inr, industry="Enterprise"):
        lead_id = f"LEAD-{uuid.uuid4().hex[:6]}"
        score = 85 if deal_size_inr >= 500000 else 65
        lead = {
            "id": lead_id,
            "company": company_name,
            "contact": contact_name,
            "deal_size_inr": deal_size_inr,
            "industry": industry,
            "lead_score": score,
            "stage": "QUALIFIED",
            "created_at": datetime.now().isoformat()
        }
        self.leads.append(lead)
        return lead

    def generate_invoice(self, lead_id, amount_inr, tax_rate=0.18):
        inv_id = f"INV-{uuid.uuid4().hex[:6]}"
        tax = amount_inr * tax_rate
        total = amount_inr + tax
        invoice = {
            "invoice_id": inv_id,
            "lead_id": lead_id,
            "subtotal_inr": amount_inr,
            "tax_inr": tax,
            "total_inr": total,
            "status": "ISSUED",
            "due_date": "30_DAYS_NET",
            "created_at": datetime.now().isoformat()
        }
        self.invoices.append(invoice)
        return invoice
