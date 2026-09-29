"""
Sovereign Banking Core: Transaction Banking, Wholesale Liquidity & Trade Finance Engine.

Models the multi-trillion dollar plumbing of corporate payments and international trade:
1. Global Cash Pooling & Zero-Balance Sweeping (Multi-currency treasury)
2. Multilateral Intercompany Netting (Compresses gross transactions by up to 85%)
3. Trade Finance: Letters of Credit (UCP 600) & Supply Chain Finance / Reverse Factoring
4. SWIFT ISO 20022 Interbank Messaging (pacs.008, pacs.009, camt.053) & Nostro/Vostro double entry
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import time


@dataclass
class LetterOfCredit:
    lc_reference: str
    applicant_buyer: str
    beneficiary_seller: str
    issuing_bank: str
    advising_bank: str
    amount_usd: float
    expiry_date: str
    is_confirmed: bool = True
    is_transferable: bool = False
    governing_rules: str = "ICC UCP 600"
    issuance_fee_bps: float = 125.0  # 1.25% per annum


@dataclass
class ISO20022Message:
    message_id: str
    message_type: str  # pacs.008, pacs.009, camt.053
    instructing_agent_bic: str
    instructed_agent_bic: str
    debtor_account: str
    creditor_account: str
    interbank_settlement_amount: float
    currency: str
    settlement_timestamp_iso: str
    end_to_end_uetr: str  # Unique End-to-end Transaction Reference (UUID)


class GlobalCashManagementDesk:
    """
    Automates multi-entity liquidity pooling, zero-balance sweeping, and multilateral netting.
    """

    def execute_zero_balance_sweep(
        self,
        subsidiary_balances: Dict[str, float],
        target_operating_cushion: float = 5_000_000.0,
    ) -> Dict[str, Any]:
        """
        Sweeps excess cash from operating subsidiaries into central master treasury.
        """
        swept_amounts: Dict[str, float] = {}
        total_swept = 0.0

        for sub, bal in subsidiary_balances.items():
            if bal > target_operating_cushion:
                excess = bal - target_operating_cushion
                swept_amounts[sub] = excess
                total_swept += excess
            else:
                swept_amounts[sub] = 0.0

        return {
            "master_treasury_target": "OMEGA_GLOBAL_TREASURY_ACCOUNT",
            "total_liquidity_concentrated_usd": round(total_swept, 2),
            "individual_sweeps": {k: round(v, 2) for k, v in swept_amounts.items()},
            "status": "SWEEP_EXECUTED_EOD",
        }

    def execute_multilateral_netting(
        self,
        gross_obligations: List[Tuple[str, str, float]],  # (Debtor, Creditor, Amount)
    ) -> Dict[str, Any]:
        """
        Netting matrix eliminating redundant inter-company gross wire transfers.
        """
        gross_volume = sum(amt for _, _, amt in gross_obligations)
        net_balances: Dict[str, float] = {}

        for debtor, creditor, amt in gross_obligations:
            net_balances[debtor] = net_balances.get(debtor, 0.0) - amt
            net_balances[creditor] = net_balances.get(creditor, 0.0) + amt

        # Volume required to settle net
        net_settlement_volume = sum(abs(v) for v in net_balances.values()) / 2.0
        compression_ratio = ((gross_volume - net_settlement_volume) / gross_volume) * 100.0 if gross_volume > 0 else 0.0

        return {
            "gross_turnover_usd": round(gross_volume, 2),
            "net_clearing_volume_usd": round(net_settlement_volume, 2),
            "compression_efficiency_pct": round(compression_ratio, 2),
            "final_net_settlement_positions": {k: round(v, 2) for k, v in net_balances.items()},
        }


class TradeFinanceDesk:
    """
    Manages Letters of Credit, bills of exchange, and supplier reverse factoring.
    """

    def issue_confirmed_letter_of_credit(
        self,
        buyer: str,
        seller: str,
        amount_usd: float,
        tenor_days: int = 90,
    ) -> LetterOfCredit:
        lc_ref = f"LC_OMEGA_{time.time_ns()}"
        return LetterOfCredit(
            lc_reference=lc_ref,
            applicant_buyer=buyer,
            beneficiary_seller=seller,
            issuing_bank="Planetary_Continuum_Trade_Bank",
            advising_bank="Global_Allied_Correspondent_Bank",
            amount_usd=amount_usd,
            expiry_date=f"+{tenor_days}_days",
            is_confirmed=True,
            is_transferable=False,
            governing_rules="ICC UCP 600",
            issuance_fee_bps=125.0,
        )

    def calculate_reverse_factoring_early_payment(
        self,
        invoice_face_value_usd: float,
        days_to_maturity: int,
        buyer_credit_spread_pct: float = 1.10,
        sofr_base_rate_pct: float = 4.80,
    ) -> Dict[str, Any]:
        """
        Suppliers receive early payment discounted at the large buyer's superior credit rating.
        """
        annual_discount_rate = (sofr_base_rate_pct + buyer_credit_spread_pct) / 100.0
        discount_amount = invoice_face_value_usd * annual_discount_rate * (days_to_maturity / 360.0)
        net_early_cash_paid = invoice_face_value_usd - discount_amount

        return {
            "invoice_face_value_usd": invoice_face_value_usd,
            "days_accelerated": days_to_maturity,
            "financing_rate_pct": round((sofr_base_rate_pct + buyer_credit_spread_pct), 3),
            "early_payment_discount_usd": round(discount_amount, 2),
            "net_cash_delivered_to_supplier_usd": round(net_early_cash_paid, 2),
            "status": "APPROVED_SUPPLY_CHAIN_FINANCE",
        }


class WholesalePaymentRails:
    """
    High-value interbank clearing and ISO 20022 message orchestration.
    """

    def __init__(self):
        # Nostro/Vostro double-entry ledger {Account_Pair: Balance}
        self.nostro_vostro_accounts: Dict[str, float] = {
            "NOSTRO_CONTINUUM_AT_JPMORGAN_USD": 500_000_000.0,
            "VOSTRO_JPMORGAN_AT_CONTINUUM_USD": 500_000_000.0,
        }

    def generate_iso20022_pacs008(
        self,
        instructing_bic: str,
        instructed_bic: str,
        debtor_account: str,
        creditor_account: str,
        amount: float,
        currency: str = "USD",
    ) -> ISO20022Message:
        """
        Constructs ISO 20022 pacs.008 FI-to-FI Customer Credit Transfer.
        """
        tx_id = f"pacs008_{time.time_ns()}"
        uetr = hashlib.sha256(f"{tx_id}:{instructing_bic}:{creditor_account}".encode()).hexdigest()[:36]

        msg = ISO20022Message(
            message_id=tx_id,
            message_type="pacs.008.001.10",
            instructing_agent_bic=instructing_bic,
            instructed_agent_bic=instructed_bic,
            debtor_account=debtor_account,
            creditor_account=creditor_account,
            interbank_settlement_amount=amount,
            currency=currency,
            settlement_timestamp_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            end_to_end_uetr=uetr,
        )

        # Update Nostro / Vostro accounts
        self.nostro_vostro_accounts["NOSTRO_CONTINUUM_AT_JPMORGAN_USD"] -= amount
        self.nostro_vostro_accounts["VOSTRO_JPMORGAN_AT_CONTINUUM_USD"] += amount

        return msg
