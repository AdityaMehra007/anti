"""Tests for ApexFlow Idempotency Ledger."""

import asyncio
import pytest
from projects.apex_enterprise_orchestrator.core.idempotency import IdempotencyLedger


def test_idempotency_cache_hit_and_deterministic_response():
    async def run():
        ledger = IdempotencyLedger(db_path=":memory:")
        payload = {"po_id": "PO-999", "amount": 54000.0}
        key = "IDEMP-KEY-1001"

        # 1. First attempt: not cached, reserved as PENDING
        is_cached, cached = await ledger.check_or_reserve(key=key, payload=payload)
        assert is_cached is False
        assert cached is None

        # 2. Record successful response
        expected_response = {"status": "APPROVED", "reconciliation_id": "REC-888"}
        await ledger.record_success(key=key, response=expected_response)

        # 3. Second identical attempt: cache hit, returns exact response
        is_cached2, cached2 = await ledger.check_or_reserve(key=key, payload=payload)
        assert is_cached2 is True
        assert cached2 == expected_response

    asyncio.run(run())


def test_idempotency_detects_payload_mutation():
    async def run():
        ledger = IdempotencyLedger(db_path=":memory:")
        key = "IDEMP-KEY-ATTACK"
        payload1 = {"user": "Alice", "amount": 100}
        payload2 = {"user": "Alice", "amount": 5000}

        await ledger.check_or_reserve(key=key, payload=payload1)
        await ledger.record_success(key=key, response={"status": "OK"})

        # Attempting to use same key with mutated payload raises ValueError
        with pytest.raises(ValueError, match="previously used with a different payload hash"):
            await ledger.check_or_reserve(key=key, payload=payload2)

    asyncio.run(run())

