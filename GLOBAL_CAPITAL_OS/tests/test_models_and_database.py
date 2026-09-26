"""Tests for models and database integrity in GLOBAL CAPITAL OS."""

import pytest
from GLOBAL_CAPITAL_OS.core.config import settings
from GLOBAL_CAPITAL_OS.core.models import (
    CurrencyCode, AccountCategory, TransactionCategory,
    TransactionStatus, LegalCheckStatus
)
from GLOBAL_CAPITAL_OS.core.database import db


def test_database_initialization_and_seeding():
    """Verifies that the database initializes with the primary entity and bank accounts."""
    with db.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM entities")
        entity_count = cur.fetchone()[0]
        assert entity_count >= 1

        cur.execute("SELECT COUNT(*) FROM bank_accounts WHERE is_active = 1")
        account_count = cur.fetchone()[0]
        assert account_count >= 5  # Ops, Tax, Emergency, Growth, Wise

        cur.execute("SELECT id, currency, balance_inr FROM bank_accounts WHERE id = 'ACC-IN-OPS-01'")
        ops_account = cur.fetchone()
        assert ops_account is not None
        assert ops_account["currency"] == "INR"


def test_money_distinction_rules():
    """Enforces absolute reality rule: separate REVENUE, CASH, and DEBT."""
    with db.get_connection() as conn:
        cur = conn.cursor()
        # Debt facilities must never be inserted into revenue transactions
        cur.execute("""
            SELECT COUNT(*) FROM transactions WHERE category = 'REVENUE_CUSTOMER' AND description LIKE '%Debt%'
        """)
        assert cur.fetchone()[0] == 0

        # Verify tax reserve account exists and is segregated
        cur.execute("SELECT id, category FROM bank_accounts WHERE id = 'ACC-IN-TAX-01'")
        tax_acc = cur.fetchone()
        assert tax_acc["category"] == "TAX_RESERVE"
