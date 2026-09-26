"""Compliance Agent - Regulatory & Cross-Border Legal Guardian.

Evaluates proposed actions against RBI Master Directions, FEMA,
Companies Act 2013 (Section 186), GST export rules (LUT), and Income Tax rules.
Emits 'PROFESSIONAL ADVISOR REVIEW REQUIRED' where mandated.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier, LegalCheckStatus, CurrencyCode


class ComplianceAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="ComplianceAgent",
            role_description="Regulatory compliance auditor ensuring complete adherence to Indian and international financial laws."
        )

    def evaluate_transaction_compliance(
        self,
        action_type: str,
        amount_inr: float,
        currency: str,
        counterparty_country: str,
        is_cross_border: bool = False
    ) -> dict[str, Any]:
        """Audits a proposed financial action against statutory compliance frameworks."""
        self.check_permission(ActionTier.ANALYZE)
        notes = []
        status = LegalCheckStatus.COMPLIANT

        # 1. Cross-Border Remittance Evaluation (RBI / FEMA)
        if is_cross_border:
            if currency != "INR":
                notes.append("RBI Inward Remittance: Software/services export must be backed by GST Letter of Undertaking (LUT) for zero-rated IGST.")
                notes.append("Banking Compliance: Verify electronic Foreign Inward Remittance Certificate (e-FIRC) and purpose code (P0802/P0807).")

            if action_type in ["OUTWARD_REMITTANCE", "FOREIGN_INVESTMENT", "FOREIGN_BORROWING"]:
                status = LegalCheckStatus.ADVISOR_REVIEW_REQUIRED
                notes.append("FEMA Overseas Investment / Borrowing: Outward remittances require Form 15CA/15CB tax certification and Authorized Dealer Bank routing.")
                notes.append("ECB Master Directions: Foreign debt is subject to eligible borrower/lender rules, all-in-cost ceilings, and strict end-use restrictions.")

        # 2. Corporate Investment & Loans (Companies Act 2013, Section 186)
        if action_type in ["LOAN_DISBURSEMENT", "CORPORATE_INVESTMENT", "EQUITY_PURCHASE"]:
            status = LegalCheckStatus.ADVISOR_REVIEW_REQUIRED
            notes.append("Companies Act Sec 186: Inter-corporate loans/investments cannot exceed 60% of paid-up capital + free reserves without Special Resolution.")
            notes.append("Separation of Funds: Founder personal money and company capital must remain strictly segregated. Direct loans to directors strictly regulated under Sec 185.")

        # 3. High Value Transaction Threshold (> ₹2,00,000)
        if amount_inr >= 200000.0:
            notes.append("Income Tax SFT Threshold: High-value transaction will be reported under SFT (Statement of Financial Transactions). Verified PAN/GST required.")
            if status == LegalCheckStatus.COMPLIANT:
                status = LegalCheckStatus.CONDITIONS_APPLY

        # 4. Anti-Money Laundering (AML) / Sanctions Check
        sanctioned_jurisdictions = ["NORTH_KOREA", "IRAN", "SYRIA", "RUSSIA_SANCTIONED_ENTITIES"]
        if counterparty_country.upper() in sanctioned_jurisdictions:
            status = LegalCheckStatus.PROHIBITED
            notes.append(f"FATF / RBI AML Violation: Transactions with {counterparty_country} are strictly prohibited.")

        result = {
            "status": status.value,
            "is_cross_border": is_cross_border,
            "compliance_notes": notes,
            "requires_cfa_ca_review": (status == LegalCheckStatus.ADVISOR_REVIEW_REQUIRED)
        }
        self.log_action("COMPLIANCE_EVALUATION_COMPLETED", {"action": action_type, "amount_inr": amount_inr, "result": result})
        return result


compliance_agent = ComplianceAgent()
