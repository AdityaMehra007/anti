"""
ApexFlow Enterprise Core - Circuit Breaker Pattern.
Thread-safe, async-capable state machine preventing cascade failures.
"""

import asyncio
import time
from enum import Enum
from typing import Any, Callable, Coroutine, Optional


class CircuitState(str, Enum):
    CLOSED = "CLOSED"      # Normal operation: requests pass through
    OPEN = "OPEN"          # Fault state: requests are blocked immediately
    HALF_OPEN = "HALF_OPEN"# Trial state: testing upstream availability


class CircuitBreakerOpenException(Exception):
    """Raised when an operation is attempted while circuit is OPEN."""
    def __init__(self, message: str = "Circuit breaker is OPEN. Upstream call rejected."):
        super().__init__(message)


class CircuitBreaker:
    """
    High-performance Circuit Breaker with exponential backoff and half-open probing.
    
    Invariants:
    - On consecutive failures >= failure_threshold -> transitions CLOSED to OPEN.
    - While OPEN, blocks execution until recovery_timeout seconds elapse.
    - Once recovery_timeout expires -> transitions to HALF_OPEN.
    - In HALF_OPEN, allows limited trial requests.
      - If trial succeeds -> transitions back to CLOSED and resets failures.
      - If trial fails -> immediately returns to OPEN.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 10.0,
        half_open_max_trials: int = 2,
        name: str = "default_circuit",
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_trials = half_open_max_trials

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._half_open_trials = 0
        self._lock: Optional[asyncio.Lock] = None

    @property
    def lock(self) -> asyncio.Lock:
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    @property
    def state(self) -> CircuitState:
        # Check if recovery timeout has elapsed while OPEN
        if self._state == CircuitState.OPEN:
            if time.monotonic() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_trials = 0
        return self._state

    @property
    def failure_count(self) -> int:
        return self._failure_count

    async def call(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        fallback: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None,
        **kwargs: Any,
    ) -> Any:
        """Executes the async function guarded by the circuit breaker."""
        async with self.lock:
            current_state = self.state

            if current_state == CircuitState.OPEN:
                if fallback:
                    return await fallback(*args, **kwargs)
                raise CircuitBreakerOpenException(
                    f"CircuitBreaker '{self.name}' is OPEN. Retry in "
                    f"{max(0.0, self.recovery_timeout - (time.monotonic() - self._last_failure_time)):.2f}s"
                )

            if current_state == CircuitState.HALF_OPEN:
                if self._half_open_trials >= self.half_open_max_trials:
                    if fallback:
                        return await fallback(*args, **kwargs)
                    raise CircuitBreakerOpenException(
                        f"CircuitBreaker '{self.name}' HALF_OPEN trial capacity saturated."
                    )
                self._half_open_trials += 1

        # Execute call outside lock to prevent blocking concurrent closed calls
        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result
        except Exception as exc:
            await self._record_failure()
            if fallback:
                return await fallback(*args, **kwargs)
            raise exc

    async def _record_success(self) -> None:
        async with self.lock:
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                self._half_open_trials = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0
            self._success_count += 1

    async def _record_failure(self) -> None:
        async with self.lock:
            self._failure_count += 1
            self._last_failure_time = time.monotonic()

            if self._state == CircuitState.HALF_OPEN:
                # Immediate trip back to OPEN
                self._state = CircuitState.OPEN
            elif self._state == CircuitState.CLOSED and self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
