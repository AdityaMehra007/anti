"""
Global Trade, Incoterms 2020 & UCP 600 Documentary Credit Compliance Engine
Evaluates Letter of Credit (LC) presentation conformity and computes Indian Customs landed costs.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Tuple, Optional


@dataclass
class LetterOfCredit:
    lc_number: str
    issuing_bank: str
    beneficiary: str
    applicant: str
    lc_amount_usd: float
    tolerance_pct: float  # e.g., 5.0 for +/- 5% as per UCP 600 Article 30
    expiry_date: str      # YYYY-MM-DD
    latest_shipment_date: str # YYYY-MM-DD
    port_of_loading: str
    port_of_discharge: str
    incoterm: str         # FOB, CIF, CFR, EXW, DDP


@dataclass
class PresentationDocuments:
    doc_id: str
    lc_number: str
    commercial_invoice_amount_usd: float
    invoice_beneficiary: str
    bill_of_lading_number: str
    shipped_on_board_date: str # YYYY-MM-DD
    bol_port_of_loading: str
    bol_port_of_discharge: str
    is_clean_on_board: bool


@dataclass
class ComplianceResult:
    is_compliant: bool
    status: str # CLEAN_COMPLIANT, DISCREPANT, REJECTED
    discrepancies: List[str]
    max_permitted_drawdown: float
    min_permitted_drawdown: float
    audit_timestamp: str


@dataclass
class CustomsAssessment:
    shipment_id: str
    cif_value_inr: float
    basic_customs_duty_rate_pct: float
    bcd_amount_inr: float
    sws_amount_inr: float # Social Welfare Surcharge (10% of BCD)
    igst_rate_pct: float
    igst_amount_inr: float
    total_customs_duty_inr: float
    total_landed_cost_inr: float


class EximCustomsEngine:
    def __init__(self, inr_usd_fx_rate: float = 85.0):
        self.fx_rate = inr_usd_fx_rate

    def verify_ucp600_presentation(
        self, lc: LetterOfCredit, docs: PresentationDocuments, presentation_date: str
    ) -> ComplianceResult:
        """
        Audits presentation conformity against ICC UCP 600 Articles:
        - Art 14: Standard for Examination of Documents
        - Art 18: Commercial Invoice requirements & currency
        - Art 20: Bill of Lading requirements (clean on board, ports)
        - Art 30: Tolerance allowances (+/- 5%)
        """
        discrepancies = []
        d_pres = datetime.strptime(presentation_date, "%Y-%m-%d")
        d_exp = datetime.strptime(lc.expiry_date, "%Y-%m-%d")
        d_ship_latest = datetime.strptime(lc.latest_shipment_date, "%Y-%m-%d")
        d_shipped = datetime.strptime(docs.shipped_on_board_date, "%Y-%m-%d")

        # 1. Expiry Check (Art 14c: Must present on or before expiry)
        if d_pres > d_exp:
            discrepancies.append(f"Late Presentation: Presented on {presentation_date} after LC Expiry {lc.expiry_date}")

        # 2. Late Shipment Check (Art 14c / Art 20a: Shipped on board date vs latest shipment date)
        if d_shipped > d_ship_latest:
            discrepancies.append(f"Late Shipment: Shipped on {docs.shipped_on_board_date} past latest date {lc.latest_shipment_date}")

        # 3. 21-Day Presentation Rule (Art 14c: Documents must be presented within 21 days after shipment date)
        days_after_shipment = (d_pres - d_shipped).days
        if days_after_shipment > 21:
            discrepancies.append(f"Stale Documents: Presented {days_after_shipment} days after shipment (max 21 days allowed under UCP 600 Art 14c)")

        # 4. Beneficiary Exact Match (Art 18a: Commercial Invoice must appear to have been issued by beneficiary)
        if lc.beneficiary.strip().lower() != docs.invoice_beneficiary.strip().lower():
            discrepancies.append(f"Beneficiary Discrepancy: LC states '{lc.beneficiary}', Invoice issued by '{docs.invoice_beneficiary}'")

        # 5. Clean Bill of Lading (Art 27: Clean transport document)
        if not docs.is_clean_on_board:
            discrepancies.append("Claused Transport Document: Bill of Lading is not Clean on Board")

        # 6. Port Matching (Art 20a)
        if lc.port_of_loading.strip().lower() != docs.bol_port_of_loading.strip().lower():
            discrepancies.append(f"Port of Loading Mismatch: Expected '{lc.port_of_loading}', got '{docs.bol_port_of_loading}'")
        if lc.port_of_discharge.strip().lower() != docs.bol_port_of_discharge.strip().lower():
            discrepancies.append(f"Port of Discharge Mismatch: Expected '{lc.port_of_discharge}', got '{docs.bol_port_of_discharge}'")

        # 7. Amount & Tolerance Check (Art 30b: Tolerance +/- tolerance_pct)
        max_draw = lc.lc_amount_usd * (1.0 + (lc.tolerance_pct / 100.0))
        min_draw = lc.lc_amount_usd * (1.0 - (lc.tolerance_pct / 100.0))

        if docs.commercial_invoice_amount_usd > max_draw:
            discrepancies.append(f"Overdrawn LC: Invoice amount (${docs.commercial_invoice_amount_usd:,.2f}) exceeds max tolerance (${max_draw:,.2f})")
        elif docs.commercial_invoice_amount_usd < min_draw:
            discrepancies.append(f"Underdrawn LC: Invoice amount (${docs.commercial_invoice_amount_usd:,.2f}) below min tolerance (${min_draw:,.2f})")

        is_compliant = len(discrepancies) == 0
        status = "CLEAN_COMPLIANT" if is_compliant else "DISCREPANT"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return ComplianceResult(
            is_compliant=is_compliant,
            status=status,
            discrepancies=discrepancies,
            max_permitted_drawdown=max_draw,
            min_permitted_drawdown=min_draw,
            audit_timestamp=now_str
        )

    def calculate_indian_customs_duty(
        self,
        shipment_id: str,
        fob_value_usd: float,
        freight_usd: float,
        insurance_usd: float,
        bcd_rate_pct: float = 10.0,
        igst_rate_pct: float = 18.0
    ) -> CustomsAssessment:
        """
        Computes Landed Customs Duty under Indian Customs Act, 1962 (Section 14 Valuation):
        - Assessable CIF = (FOB + Freight + Insurance) * Exchange Rate
        - Basic Customs Duty (BCD) = CIF * bcd_rate_pct
        - Social Welfare Surcharge (SWS) = 10% of BCD (Finance Act, 2018)
        - IGST Base = Assessable CIF + BCD + SWS
        - IGST = IGST Base * igst_rate_pct
        - Total Landed Cost = Assessable CIF + BCD + SWS + IGST
        """
        cif_usd = fob_value_usd + freight_usd + insurance_usd
        cif_inr = cif_usd * self.fx_rate

        bcd_amount = cif_inr * (bcd_rate_pct / 100.0)
        sws_amount = bcd_amount * 0.10  # Standard 10% on BCD

        igst_base = cif_inr + bcd_amount + sws_amount
        igst_amount = igst_base * (igst_rate_pct / 100.0)

        total_duty = bcd_amount + sws_amount + igst_amount
        total_landed = cif_inr + total_duty

        return CustomsAssessment(
            shipment_id=shipment_id,
            cif_value_inr=round(cif_inr, 2),
            basic_customs_duty_rate_pct=bcd_rate_pct,
            bcd_amount_inr=round(bcd_amount, 2),
            sws_amount_inr=round(sws_amount, 2),
            igst_rate_pct=igst_rate_pct,
            igst_amount_inr=round(igst_amount, 2),
            total_customs_duty_inr=round(total_duty, 2),
            total_landed_cost_inr=round(total_landed, 2)
        )
