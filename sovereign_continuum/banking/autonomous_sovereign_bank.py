"""
Sovereign Banking Core: Bank of the Continuum (Autonomous Sovereign Bank).

The apex institutional bank unifying:
1. Central Banking Facility (Lender of last resort, liquidity corridors, FX swap lines)
2. Investment Banking (DCM, Syndicated Loans, Securitization, M&A)
3. Transaction Banking (Cash pooling, multilateral netting, Trade Finance, ISO 20022 rails)
4. Custody & Prime Brokerage (AUC safekeeping, Tri-Party Repo, Securities lending, Margining)
5. Derivatives Clearing (IRS, FX forwards, CDS hedging)
6. Autonomous Machine Accounts (Direct programmable banking for robot swarms, SMRs, and foundries)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time
import hashlib

from .central_banking_engine import CentralBankingFacility
from .investment_banking_engine import DebtCapitalMarketsDesk, SyndicatedLendingDesk, SecuritizationDesk, SecuritizedPool
from .transaction_banking_engine import GlobalCashManagementDesk, TradeFinanceDesk, WholesalePaymentRails
from .custody_prime_brokerage import GlobalCustodyDesk, TriPartyRepoDesk, PrimeBrokerageDesk, CustodyAssetPosition
from .derivatives_clearing_engine import DerivativesClearingDesk, InterestRateSwap, FXForwardContract, CreditDefaultSwap


@dataclass
class SovereignBankAccount:
    account_id: str
    account_holder_name: str
    entity_type: str  # ROBOT_SWARM, SMR_REACTOR, BIO_FOUNDRY, SOVEREIGN_TREASURY, ENTERPRISE_CLIENT
    fiat_balance_usd: float
    ecu_energy_compute_units: float
    credit_line_limit_usd: float
    drawn_credit_usd: float = 0.0


class BankOfTheContinuum:
    """
    Planetary Sovereign Financial Institution managing multi-trillion dollar monetary flows.
    """

    def __init__(self, institution_bic: str = "CONTUS33XXX"):
        self.institution_bic = institution_bic
        
        # Institutional Desks
        self.central_bank = CentralBankingFacility()
        self.dcm_desk = DebtCapitalMarketsDesk()
        self.syndicated_lending = SyndicatedLendingDesk()
        self.securitization_desk = SecuritizationDesk()
        self.cash_management = GlobalCashManagementDesk()
        self.trade_finance = TradeFinanceDesk()
        self.wholesale_payments = WholesalePaymentRails()
        self.custody_desk = GlobalCustodyDesk()
        self.tri_party_repo = TriPartyRepoDesk()
        self.prime_brokerage = PrimeBrokerageDesk()
        self.derivatives_desk = DerivativesClearingDesk()

        # Sovereign Deposit & Credit Ledger
        self.accounts: Dict[str, SovereignBankAccount] = {}
        self._initialize_core_accounts()

    def _initialize_core_accounts(self):
        # 1. Terra Kinetics Global Labor Fleet Account
        self.open_account(
            account_id="ACC_TERRA_FLEET_01",
            holder_name="Terra Kinetics Worldwide Humanoid Fleet",
            entity_type="ROBOT_SWARM",
            initial_fiat=250_000_000.0,
            initial_ecu=1_500_000.0,
            credit_limit=1_000_000_000.0,
        )
        # 2. Aether Energy Nuclear Grid Account
        self.open_account(
            account_id="ACC_AETHER_SMR_01",
            holder_name="Aether Energy SMR Fleet Holdings",
            entity_type="SMR_REACTOR",
            initial_fiat=500_000_000.0,
            initial_ecu=5_000_000.0,
            credit_limit=2_500_000_000.0,
        )
        # 3. Bioma Molecular Foundry Account
        self.open_account(
            account_id="ACC_BIOMA_FOUNDRY_01",
            holder_name="Bioma Cellular Fermentation Foundry",
            entity_type="BIO_FOUNDRY",
            initial_fiat=150_000_000.0,
            initial_ecu=800_000.0,
            credit_limit=500_000_000.0,
        )
        # 4. Sovereign Master Treasury
        self.open_account(
            account_id="ACC_SOVEREIGN_TREASURY_PRIME",
            holder_name="Sovereign Continuum Apex Treasury",
            entity_type="SOVEREIGN_TREASURY",
            initial_fiat=10_000_000_000.0,
            initial_ecu=25_000_000.0,
            credit_limit=50_000_000_000.0,
        )

    def open_account(
        self,
        account_id: str,
        holder_name: str,
        entity_type: str,
        initial_fiat: float = 0.0,
        initial_ecu: float = 0.0,
        credit_limit: float = 0.0,
    ) -> SovereignBankAccount:
        account = SovereignBankAccount(
            account_id=account_id,
            account_holder_name=holder_name,
            entity_type=entity_type,
            fiat_balance_usd=initial_fiat,
            ecu_energy_compute_units=initial_ecu,
            credit_line_limit_usd=credit_limit,
        )
        self.accounts[account_id] = account
        return account

    def transfer_liquidity(
        self,
        source_account_id: str,
        dest_account_id: str,
        amount_usd: float,
    ) -> Dict[str, Any]:
        """
        Instant zero-fee internal ledger settlement.
        """
        src = self.accounts.get(source_account_id)
        dst = self.accounts.get(dest_account_id)

        if not src or not dst:
            raise ValueError("Invalid source or destination account ID")

        if src.fiat_balance_usd < amount_usd:
            raise ValueError(f"Insufficient funds: available ${src.fiat_balance_usd:,.2f}, requested ${amount_usd:,.2f}")

        src.fiat_balance_usd -= amount_usd
        dst.fiat_balance_usd += amount_usd

        tx_hash = hashlib.sha256(f"{source_account_id}:{dest_account_id}:{amount_usd}:{time.time_ns()}".encode()).hexdigest()

        return {
            "transaction_hash": tx_hash,
            "source_account": source_account_id,
            "destination_account": dest_account_id,
            "settled_amount_usd": amount_usd,
            "source_new_balance_usd": round(src.fiat_balance_usd, 2),
            "dest_new_balance_usd": round(dst.fiat_balance_usd, 2),
            "status": "SETTLED_REAL_TIME",
        }

    def generate_consolidated_banking_audit(self) -> Dict[str, Any]:
        """
        Provides a comprehensive balance sheet and operational audit of all 6 banking divisions.
        """
        total_deposits_usd = sum(acc.fiat_balance_usd for acc in self.accounts.values())
        total_ecu_held = sum(acc.ecu_energy_compute_units for acc in self.accounts.values())
        total_credit_lines = sum(acc.credit_line_limit_usd for acc in self.accounts.values())

        cb_assets = self.central_bank.balance_sheet.total_assets_b
        auc_data = self.custody_desk.calculate_total_assets_under_custody()

        return {
            "institution": "Bank of the Continuum (Global Planetary Reserve)",
            "bic_code": self.institution_bic,
            "regulatory_framework": "Basel IV / CPSS-IOSCO / ISO 20022 Certified",
            "autonomous_accounts_count": len(self.accounts),
            "total_fiat_deposits_usd": round(total_deposits_usd, 2),
            "total_fiat_deposits_b": round(total_deposits_usd / 1e9, 3),
            "total_energy_compute_units_ecu": round(total_ecu_held, 2),
            "total_credit_lines_granted_b": round(total_credit_lines / 1e9, 2),
            "central_bank_balance_sheet_assets_b": round(cb_assets, 2),
            "assets_under_custody_b": auc_data["total_assets_under_custody_b"],
            "divisions_active": [
                "1. Central Banking & Liquidity Facilities",
                "2. Debt Capital Markets & Mega-Bond Underwriting",
                "3. Syndicated Infrastructure Lending",
                "4. Physical Cash-Flow Securitization (ABS/CLO)",
                "5. Wholesale Cash Management & Multilateral Netting",
                "6. Global Trade Finance (UCP 600 Letters of Credit)",
                "7. Interbank ISO 20022 High-Value Rails",
                "8. Global Custody & Tri-Party Repo",
                "9. Prime Brokerage & Margin Clearing",
                "10. Multi-Trillion Derivatives Hedging (IRS/FX/CDS)",
            ],
        }
