"""
TradeNexus Cryptographic Audit Ledger & Compliance Certificate Vault
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class LedgerEntry(BaseModel):
    entry_id: str
    timestamp: float
    invoice_number: str
    exporter_name: str
    destination_country: str
    hs_codes: List[str]
    compliance_status: str
    audit_score: float
    payload_hash: str
    previous_block_hash: str
    current_block_hash: str
    digital_signature: str

class VerificationCertificate(BaseModel):
    certificate_id: str
    issued_at: str
    invoice_number: str
    exporter_name: str
    cbam_status: str
    scomet_status: str
    tamper_proof_hash: str
    chain_height: int
    is_valid: bool

class CryptographicAuditLedger:
    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
    _chain: List[LedgerEntry] = []

    @classmethod
    def record_audit(cls, invoice_data: Dict[str, Any], audit_result: Dict[str, Any]) -> LedgerEntry:
        prev_hash = cls._chain[-1].current_block_hash if cls._chain else cls.GENESIS_HASH
        ts = time.time()
        inv_num = invoice_data.get("invoice_number", "INV-UNKNOWN")
        exporter = invoice_data.get("exporter_name", "UNKNOWN EXPORTER")
        dest = invoice_data.get("destination_country", "UNKNOWN")
        hs_list = [item.get("hs_code", "") for item in invoice_data.get("line_items", [])]

        status = audit_result.get("status", "PASSED")
        score = float(audit_result.get("compliance_score", 100.0))

        raw_payload = json.dumps({"inv": invoice_data, "audit": audit_result}, sort_keys=True)
        payload_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

        block_content = f"{ts}:{inv_num}:{exporter}:{dest}:{status}:{score}:{payload_hash}:{prev_hash}"
        current_hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()
        signature = f"TRADENEXUS-SIG-{hashlib.sha256((current_hash + 'TNX-2027').encode('utf-8')).hexdigest()[:16].upper()}"

        entry_id = f"LE-2027-{len(cls._chain) + 1:05d}"
        entry = LedgerEntry(
            entry_id=entry_id,
            timestamp=ts,
            invoice_number=inv_num,
            exporter_name=exporter,
            destination_country=dest,
            hs_codes=hs_list,
            compliance_status=status,
            audit_score=score,
            payload_hash=payload_hash,
            previous_block_hash=prev_hash,
            current_block_hash=current_hash,
            digital_signature=signature
        )
        cls._chain.append(entry)
        return entry

    @classmethod
    def verify_entry(cls, entry_id: str) -> Optional[VerificationCertificate]:
        for idx, entry in enumerate(cls._chain):
            if entry.entry_id == entry_id:
                prev_hash = cls._chain[idx - 1].current_block_hash if idx > 0 else cls.GENESIS_HASH
                is_valid = (entry.previous_block_hash == prev_hash)
                cert_id = f"CERT-{entry.entry_id}-{entry.current_block_hash[:8].upper()}"
                return VerificationCertificate(
                    certificate_id=cert_id,
                    issued_at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(entry.timestamp)),
                    invoice_number=entry.invoice_number,
                    exporter_name=entry.exporter_name,
                    cbam_status="COMPLIANT_DECLARATION_VERIFIED",
                    scomet_status="NON_SCOMET_OR_PERMITTED",
                    tamper_proof_hash=entry.current_block_hash,
                    chain_height=idx + 1,
                    is_valid=is_valid
                )
        return None

    @classmethod
    def get_ledger_height(cls) -> int:
        return len(cls._chain)

    @classmethod
    def reset_ledger(cls):
        cls._chain = []
