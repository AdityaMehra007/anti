"""
Global EXIM & Cross-Border Supply Chain Engine
Performs Harmonized System (HS) customs duty computations, autonomous UCP 600 Letter of Credit
audits, strategic freight corridor routing, FX Forward trade hedging, and OFAC/UN sanctions screening.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Tuple


class Incoterm(Enum):
    EXW = "Ex Works"
    FOB = "Free on Board"
    CFR = "Cost and Freight"
    CIF = "Cost, Insurance and Freight"
    DDP = "Delivered Duty Paid"


@dataclass
class HSTariffRecord:
    hs_code: str
    description: str
    basic_customs_duty_pct: float
    social_welfare_surcharge_pct: float  # typically 10% of BCD
    igst_vat_pct: float
    anti_dumping_pct: float = 0.0


@dataclass
class TradeContract:
    contract_id: str
    exporter_name: str
    exporter_country: str
    importer_name: str
    importer_country: str
    hs_code: str
    incoterm: Incoterm
    cargo_quantity_units: int
    unit_price_usd: float
    freight_usd: float
    marine_insurance_usd: float
    settlement_currency: str = "USD"

    @property
    def fob_value_usd(self) -> float:
        return round(self.cargo_quantity_units * self.unit_price_usd, 2)

    @property
    def cif_value_usd(self) -> float:
        return round(self.fob_value_usd + self.freight_usd + self.marine_insurance_usd, 2)


@dataclass
class CustomsLandedCostBreakdown:
    cif_value_local: float
    basic_customs_duty_amount: float
    social_welfare_surcharge_amount: float
    anti_dumping_duty_amount: float
    assessable_value_for_tax: float
    igst_vat_amount: float
    total_customs_duties: float
    total_landed_cost: float
    effective_tariff_rate_pct: float


@dataclass
class LetterOfCreditSpec:
    lc_reference: str
    issuing_bank: str
    applicant: str
    beneficiary: str
    credit_amount_usd: float
    tolerance_pct: float       # e.g., 5.0 for +/- 5%
    expiry_date: str           # YYYY-MM-DD
    latest_shipment_date: str  # YYYY-MM-DD
    port_of_loading: str
    port_of_discharge: str


@dataclass
class ShippingDocuments:
    doc_reference: str
    invoice_number: str
    invoice_amount_usd: float
    invoice_beneficiary: str
    invoice_applicant: str
    bill_of_lading_no: str
    shipped_on_board_date: str # YYYY-MM-DD
    bol_port_of_loading: str
    bol_port_of_discharge: str
    is_clean_on_board: bool


class GlobalEximEngine:
    """Enterprise International Trade, Customs, and Trade Finance Compliance Engine."""

    # Pre-configured global tariff database
    HS_CATALOG: Dict[str, HSTariffRecord] = {
        "8471.50.00": HSTariffRecord(
            hs_code="8471.50.00",
            description="High-Performance Computing Units & AI Servers",
            basic_customs_duty_pct=0.0,
            social_welfare_surcharge_pct=0.0,
            igst_vat_pct=18.0,
            anti_dumping_pct=0.0
        ),
        "8542.31.00": HSTariffRecord(
            hs_code="8542.31.00",
            description="Advanced Processors and Controller ICs (Semiconductors)",
            basic_customs_duty_pct=0.0,
            social_welfare_surcharge_pct=0.0,
            igst_vat_pct=18.0,
            anti_dumping_pct=0.0
        ),
        "8703.80.00": HSTariffRecord(
            hs_code="8703.80.00",
            description="Electric Passenger Motor Vehicles",
            basic_customs_duty_pct=70.0,
            social_welfare_surcharge_pct=10.0, # 10% of BCD (7%)
            igst_vat_pct=28.0,
            anti_dumping_pct=0.0
        ),
        "2709.00.00": HSTariffRecord(
            hs_code="2709.00.00",
            description="Petroleum Oils and Crude Mineral Oil",
            basic_customs_duty_pct=2.5,
            social_welfare_surcharge_pct=10.0,
            igst_vat_pct=0.0, # Handled under excise
            anti_dumping_pct=0.0
        ),
        "8411.82.00": HSTariffRecord(
            hs_code="8411.82.00",
            description="Gas Turbines for Nuclear/Thermal Power Generation > 5000 kW",
            basic_customs_duty_pct=7.5,
            social_welfare_surcharge_pct=10.0,
            igst_vat_pct=18.0,
            anti_dumping_pct=0.0
        )
    }

    SANCTIONED_COUNTRIES = {"IRAN", "NORTH KOREA", "SYRIA", "RUSSIA_MILITARY_SECTOR", "CUBA"}
    SANCTIONED_ENTITIES = {
        "GLOBAL_SHADOW_SHIPPING_LTD",
        "BLACK_SEA_DARK_FLEET_CORP",
        "NORTH_STAR_BALLISTICS_INC",
        "RED_STAR_NUCLEAR_ENTERPRISES"
    }

    def __init__(self, fx_rate_to_local: float = 85.0, local_currency: str = "INR"):
        self.fx_rate = fx_rate_to_local
        self.local_currency = local_currency

    def compute_customs_landed_cost(self, contract: TradeContract) -> CustomsLandedCostBreakdown:
        tariff = self.HS_CATALOG.get(contract.hs_code)
        if not tariff:
            tariff = HSTariffRecord(
                hs_code=contract.hs_code,
                description="General Merchandise",
                basic_customs_duty_pct=10.0,
                social_welfare_surcharge_pct=10.0,
                igst_vat_pct=18.0
            )

        cif_local = contract.cif_value_usd * self.fx_rate

        # 1. Basic Customs Duty
        bcd = cif_local * (tariff.basic_customs_duty_pct / 100.0)

        # 2. SWS is % of BCD
        sws = bcd * (tariff.social_welfare_surcharge_pct / 100.0)

        # 3. Anti-Dumping
        add = cif_local * (tariff.anti_dumping_pct / 100.0)

        # 4. IGST/VAT assessed on CIF + BCD + SWS + ADD
        assessable_base = cif_local + bcd + sws + add
        igst = assessable_base * (tariff.igst_vat_pct / 100.0)

        total_duties = bcd + sws + add + igst
        total_landed = cif_local + total_duties
        effective_rate = (total_duties / cif_local) * 100.0 if cif_local > 0 else 0.0

        return CustomsLandedCostBreakdown(
            cif_value_local=round(cif_local, 2),
            basic_customs_duty_amount=round(bcd, 2),
            social_welfare_surcharge_amount=round(sws, 2),
            anti_dumping_duty_amount=round(add, 2),
            assessable_value_for_tax=round(assessable_base, 2),
            igst_vat_amount=round(igst, 2),
            total_customs_duties=round(total_duties, 2),
            total_landed_cost=round(total_landed, 2),
            effective_tariff_rate_pct=round(effective_rate, 2)
        )

    def audit_ucp600_presentation(
        self,
        lc: LetterOfCreditSpec,
        docs: ShippingDocuments,
        presentation_date: str
    ) -> Dict[str, any]:
        """
        Audits documentary presentation conformity against ICC UCP 600 rules:
        - Invoice Amount within tolerance (Art 30)
        - Clean on Board Bill of Lading (Art 20)
        - Ports alignment (Art 20)
        - Shipment date on or before latest shipment date (Art 14)
        - Presentation within 21 days of shipment (Art 14c)
        - Presentation on or before LC expiry date (Art 14)
        """
        discrepancies: List[str] = []

        # 1. Tolerance check
        min_allowed = lc.credit_amount_usd * (1.0 - (lc.tolerance_pct / 100.0))
        max_allowed = lc.credit_amount_usd * (1.0 + (lc.tolerance_pct / 100.0))
        if docs.invoice_amount_usd < min_allowed or docs.invoice_amount_usd > max_allowed:
            discrepancies.append(
                f"UCP 600 Art 30: Invoice amount ${docs.invoice_amount_usd:,.2f} outside allowed range "
                f"${min_allowed:,.2f} - ${max_allowed:,.2f} (tolerance +/-{lc.tolerance_pct}%)."
            )

        # 2. Beneficiary / Applicant match
        if docs.invoice_beneficiary.strip().lower() != lc.beneficiary.strip().lower():
            discrepancies.append(f"UCP 600 Art 18: Invoice beneficiary '{docs.invoice_beneficiary}' does not match LC beneficiary '{lc.beneficiary}'.")
        if docs.invoice_applicant.strip().lower() != lc.applicant.strip().lower():
            discrepancies.append(f"UCP 600 Art 18: Invoice applicant '{docs.invoice_applicant}' does not match LC applicant '{lc.applicant}'.")

        # 3. Clean Bill of Lading
        if not docs.is_clean_on_board:
            discrepancies.append("UCP 600 Art 20: Bill of Lading is claused / foul. Clean on Board required.")

        # 4. Port routing
        if docs.bol_port_of_loading.strip().lower() != lc.port_of_loading.strip().lower():
            discrepancies.append(f"UCP 600 Art 20: Port of loading '{docs.bol_port_of_loading}' does not match LC '{lc.port_of_loading}'.")
        if docs.bol_port_of_discharge.strip().lower() != lc.port_of_discharge.strip().lower():
            discrepancies.append(f"UCP 600 Art 20: Port of discharge '{docs.bol_port_of_discharge}' does not match LC '{lc.port_of_discharge}'.")

        # 5. Dates
        p_dt = datetime.strptime(presentation_date, "%Y-%m-%d")
        exp_dt = datetime.strptime(lc.expiry_date, "%Y-%m-%d")
        ship_dt = datetime.strptime(docs.shipped_on_board_date, "%Y-%m-%d")
        late_ship_dt = datetime.strptime(lc.latest_shipment_date, "%Y-%m-%d")

        if ship_dt > late_ship_dt:
            discrepancies.append(f"UCP 600 Art 14: Shipped on board date ({docs.shipped_on_board_date}) is after latest shipment date ({lc.latest_shipment_date}).")

        if p_dt > exp_dt:
            discrepancies.append(f"UCP 600 Art 14: Presentation date ({presentation_date}) is after LC expiry date ({lc.expiry_date}).")

        # 21-day presentation rule (Art 14c)
        days_after_shipment = (p_dt - ship_dt).days
        if days_after_shipment > 21:
            discrepancies.append(f"UCP 600 Art 14(c): Presentation made {days_after_shipment} days after shipment date (exceeds statutory 21-day limit).")

        is_compliant = (len(discrepancies) == 0)
        status = "CLEAN_COMPLIANT_FOR_PAYMENT" if is_compliant else "DISCREPANT_REJECTED"

        return {
            "lc_reference": lc.lc_reference,
            "status": status,
            "is_compliant": is_compliant,
            "discrepancies_count": len(discrepancies),
            "discrepancies": discrepancies,
            "payable_amount_usd": docs.invoice_amount_usd if is_compliant else 0.0
        }

    def price_fx_forward_hedge(
        self,
        spot_rate: float,
        domestic_rate_pct: float,
        foreign_rate_pct: float,
        tenor_days: int
    ) -> Dict[str, float]:
        """
        Computes Covered Interest Rate Parity (CIRP) Forward FX Rate:
        F = S * (1 + r_d * (t / 360)) / (1 + r_f * (t / 360))
        """
        t_factor = tenor_days / 360.0
        rd = domestic_rate_pct / 100.0
        rf = foreign_rate_pct / 100.0

        forward_rate = spot_rate * ((1.0 + rd * t_factor) / (1.0 + rf * t_factor))
        forward_points = (forward_rate - spot_rate) * 100.0  # In paise / pips

        return {
            "spot_rate": spot_rate,
            "forward_rate": round(forward_rate, 4),
            "forward_points": round(forward_points, 2),
            "annualized_cost_of_carry_pct": round((forward_rate / spot_rate - 1.0) * (365.0 / tenor_days) * 100.0, 3)
        }

    def screen_sanctions_and_embargo(
        self,
        exporter_name: str,
        exporter_country: str,
        importer_name: str,
        importer_country: str,
        cargo_description: str
    ) -> Dict[str, any]:
        """OFAC / UN Denied Parties and Embargo screening engine."""
        violations = []

        # Country check
        for c, label in [(exporter_country, "Exporter Country"), (importer_country, "Importer Country")]:
            clean_c = c.strip().upper()
            if clean_c in self.SANCTIONED_COUNTRIES:
                violations.append(f"Sanctions Breach: {label} '{clean_c}' is under comprehensive multilateral embargo.")

        # Entity check
        clean_exp = exporter_name.strip().upper().replace(" ", "_")
        clean_imp = importer_name.strip().upper().replace(" ", "_")
        if clean_exp in self.SANCTIONED_ENTITIES:
            violations.append(f"OFAC SDN Match: Exporter '{exporter_name}' is on the Specially Designated Nationals list.")
        if clean_imp in self.SANCTIONED_ENTITIES:
            violations.append(f"OFAC SDN Match: Importer '{importer_name}' is on the Specially Designated Nationals list.")

        # Dual-use keyword check
        dual_use_flags = ["CENTRIFUGE", "ENRICHED URANIUM", "WEAPONS GRADE", "MISSILE GUIDANCE"]
        for flag in dual_use_flags:
            if flag in cargo_description.upper():
                violations.append(f"ITAR/Dual-Use Prohibited Cargo Match: Keyword '{flag}' detected in cargo manifest.")

        passed = (len(violations) == 0)
        return {
            "cleared_for_export": passed,
            "risk_status": "CLEARED" if passed else "HALTED_SANCTION_VIOLATION",
            "violations_count": len(violations),
            "violations": violations
        }
