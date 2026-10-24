import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from zk_vault import ZkVaultVerifier

def test_zk_vault_underwriting():
    vault = ZkVaultVerifier()
    # High-trust credit user (Score: 820, Income: 45 LPA)
    proof = vault.create_credit_commitment("USER-CRED-77", credit_score=820, annual_income_lakhs=45.0)
    assert vault.verify_proof("USER-CRED-77", proof, "PREMIUM") is True

    # User with lower score (< 750)
    subprime_proof = vault.create_credit_commitment("USER-CRED-88", credit_score=680, annual_income_lakhs=30.0)
    assert vault.verify_proof("USER-CRED-88", subprime_proof, "PREMIUM") is False
