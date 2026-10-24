"""Tests for ApexFlow Circuit Breaker."""

import asyncio
import pytest
from projects.apex_enterprise_orchestrator.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenException,
    CircuitState,
)


def test_circuit_breaker_transitions_closed_to_open():
    async def run():
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=0.2, name="test_cb")
        assert cb.state == CircuitState.CLOSED

        async def faulty_operation():
            raise RuntimeError("Service down")

        # First 2 failures: circuit should stay CLOSED
        for _ in range(2):
            with pytest.raises(RuntimeError):
                await cb.call(faulty_operation)
            assert cb.state == CircuitState.CLOSED

        # 3rd failure trips the breaker to OPEN
        with pytest.raises(RuntimeError):
            await cb.call(faulty_operation)
        assert cb.state == CircuitState.OPEN

        # Subsequent call immediately rejected without running func
        with pytest.raises(CircuitBreakerOpenException):
            await cb.call(faulty_operation)

    asyncio.run(run())


def test_circuit_breaker_half_open_recovery():
    async def run():
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1, half_open_max_trials=1)

        async def faulty_op():
            raise ValueError("Flaky")

        async def healthy_op():
            return "SUCCESS"

        # Trip breaker
        for _ in range(2):
            with pytest.raises(ValueError):
                await cb.call(faulty_op)
        assert cb.state == CircuitState.OPEN

        # Sleep past recovery timeout
        await asyncio.sleep(0.12)
        assert cb.state == CircuitState.HALF_OPEN

        # Successful call heals circuit back to CLOSED
        res = await cb.call(healthy_op)
        assert res == "SUCCESS"
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    asyncio.run(run())

