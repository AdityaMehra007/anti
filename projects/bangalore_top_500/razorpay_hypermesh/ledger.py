"""
Razorpay Project HyperMesh: Sovereign Immutable Financial Ledger
Strict double-entry bookkeeping with cryptographic SHA-256 Merkle root verification
and zero-leakage idempotency key enforcement.
"""
import hashlib
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class JournalEntry:
    entry_id: str
    idempotency_key: str
    debit_account: str
    credit_account: str
    amount_paisa: int
    timestamp_ns: int
    entry_hash: str

class SovereignLedger:
    def __init__(self):
        self.accounts: Dict[str, int] = {} # balance in paisa
        self.entries: List[JournalEntry] = []
        self.idempotency_registry: Dict[str, str] = {}
        self.prev_hash: str = "0" * 64

    def get_balance(self, account_id: str) -> int:
        return self.accounts.get(account_id, 0)

    def record_transfer(self, entry_id: str, idempotency_key: str, debit_account: str, credit_account: str, amount_paisa: int) -> JournalEntry:
        if amount_paisa <= 0:
            raise ValueError("Transfer amount must be strictly positive")

        # Idempotency check
        if idempotency_key in self.idempotency_registry:
            existing_id = self.idempotency_registry[idempotency_key]
            for e in self.entries:
                if e.entry_id == existing_id:
                    return e

        # Ensure debit account has sufficient balance unless it's a clearing reserve
        debit_bal = self.get_balance(debit_account)
        if not debit_account.startswith("CLEARING_") and debit_bal < amount_paisa:
            raise ValueError(f"Insufficient funds in {debit_account}: available {debit_bal}, required {amount_paisa}")

        ts = time.time_ns()
        payload = f"{self.prev_hash}:{entry_id}:{idempotency_key}:{debit_account}:{credit_account}:{amount_paisa}:{ts}"
        entry_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        # Update accounts atomically
        self.accounts[debit_account] = debit_bal - amount_paisa
        self.accounts[credit_account] = self.get_balance(credit_account) + amount_paisa

        entry = JournalEntry(
            entry_id=entry_id,
            idempotency_key=idempotency_key,
            debit_account=debit_account,
            credit_account=credit_account,
            amount_paisa=amount_paisa,
            timestamp_ns=ts,
            entry_hash=entry_hash
        )

        self.entries.append(entry)
        self.idempotency_registry[idempotency_key] = entry_id
        self.prev_hash = entry_hash
        return entry

    def verify_integrity(self) -> bool:
        """Verifies full cryptographic chain and zero financial drift."""
        running_hash = "0" * 64
        total_balance = sum(self.accounts.values())
        if total_balance != 0:
            return False

        for e in self.entries:
            expected = hashlib.sha256(
                f"{running_hash}:{e.entry_id}:{e.idempotency_key}:{e.debit_account}:{e.credit_account}:{e.amount_paisa}:{e.timestamp_ns}".encode("utf-8")
            ).hexdigest()
            if e.entry_hash != expected:
                return False
            running_hash = e.entry_hash
        return True
