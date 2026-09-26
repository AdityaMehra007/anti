"""Tests for security permissions, emergency freeze, and audit chain."""

import pytest
from GLOBAL_CAPITAL_OS.core.models import ActionTier
from GLOBAL_CAPITAL_OS.core.security import security
from GLOBAL_CAPITAL_OS.core.audit import audit
from GLOBAL_CAPITAL_OS.agents.capital_commander import capital_commander
from GLOBAL_CAPITAL_OS.agents.founder_chief_of_staff import founder_chief_of_staff


def test_agent_permission_boundaries():
    """AI agents must be blocked from calling APPROVE tier."""
    with pytest.raises(PermissionError, match="cannot perform APPROVE tier"):
        capital_commander.check_permission(ActionTier.APPROVE)


def test_autonomous_money_movement_blocked():
    """No agent can autonomously EXECUTE transactions above ₹0."""
    with pytest.raises(PermissionError, match="cannot autonomously EXECUTE transactions"):
        capital_commander.check_permission(ActionTier.EXECUTE, amount_inr=500.0)


def test_secret_sanitization():
    """Credentials, cards, and OTPs must be redacted automatically."""
    raw_payload = {
        "api_key": "sk-proj-supersecretkey1234567890",
        "otp_code": "492019",
        "notes": "Safe public message"
    }
    sanitized = security.sanitize_payload(raw_payload)
    assert "[REDACTED_CREDENTIAL]" in sanitized["api_key"]
    assert sanitized["notes"] == "Safe public message"


def test_emergency_freeze_lifecycle():
    """Tests emergency freeze lockdown and authorized founder unfreeze."""
    # 1. Trigger freeze
    freeze_evt = security.trigger_emergency_freeze("Test Security Threat")
    assert security.is_system_frozen() is True

    # 2. Block actions while frozen
    with pytest.raises(PermissionError, match="under EMERGENCY FREEZE"):
        capital_commander.check_permission(ActionTier.READ)

    # 3. Invalid unfreeze attempt must fail
    with pytest.raises(PermissionError, match="Unauthorized unfreeze attempt"):
        security.release_emergency_freeze("WRONG_KEY")

    # 4. Valid Founder unfreeze succeeds
    unfreeze_evt = security.release_emergency_freeze("APPROVE_UNFREEZE_FOUNDER_CONFIRMED")
    assert security.is_system_frozen() is False
    assert capital_commander.check_permission(ActionTier.READ) is True


def test_cryptographic_audit_chain_integrity():
    """Verifies that the SHA-256 hash chain is tamper-evident and valid."""
    audit.log_event("TestAgent", "TEST_ACTION_A", {"key": "val1"})
    audit.log_event("TestAgent", "TEST_ACTION_B", {"key": "val2"})

    status = audit.verify_chain_integrity()
    assert status["valid"] is True
    assert status["count"] >= 2
