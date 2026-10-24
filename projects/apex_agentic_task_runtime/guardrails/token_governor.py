"""
ApexAgentic Runtime - Token & Cost Budget Governor.
Prevents runaway loops, token burnouts, and unauthorized API spend.
"""

import time
from dataclasses import dataclass
from threading import Lock
from typing import Dict, Optional


class BudgetExceededException(Exception):
    """Raised when token or currency budget is saturated."""
    pass


class RateLimitExceededException(Exception):
    """Raised when requests exceed configured RPM (requests per minute)."""
    pass


@dataclass
class ModelCostRates:
    input_cost_per_million: float
    output_cost_per_million: float


# Industry baseline pricing (USD per 1M tokens)
PRICING_TABLE: Dict[str, ModelCostRates] = {
    "gemini-2.5-flash": ModelCostRates(0.075, 0.30),
    "gemini-2.5-pro": ModelCostRates(1.25, 5.00),
    "claude-3-7-sonnet": ModelCostRates(3.00, 15.00),
    "gpt-4o": ModelCostRates(2.50, 10.00),
}


class TokenBudgetGovernor:
    """
    Enforces strict token budgets, cost limits, and request rate limiting per agent session.
    """

    def __init__(
        self,
        max_total_tokens: int = 100_000,
        max_cost_usd: float = 2.00,
        max_rpm: int = 60,
    ):
        self.max_total_tokens = max_total_tokens
        self.max_cost_usd = max_cost_usd
        self.max_rpm = max_rpm

        self.consumed_input_tokens = 0
        self.consumed_output_tokens = 0
        self.accumulated_cost_usd = 0.0
        self.request_timestamps = []
        self._lock = Lock()

    @property
    def total_tokens(self) -> int:
        with self._lock:
            return self.consumed_input_tokens + self.consumed_output_tokens

    @property
    def current_cost_usd(self) -> float:
        with self._lock:
            return round(self.accumulated_cost_usd, 5)

    def check_rate_limit(self) -> None:
        """Sliding-window RPM limiter."""
        now = time.time()
        with self._lock:
            # Prune timestamps older than 60 seconds
            self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 60.0]
            if len(self.request_timestamps) >= self.max_rpm:
                raise RateLimitExceededException(
                    f"Agent rate limit exceeded: {len(self.request_timestamps)} requests in last 60s (Max: {self.max_rpm})"
                )
            self.request_timestamps.append(now)

    def record_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        model_name: str = "gemini-2.5-flash",
    ) -> float:
        """
        Records token consumption and verifies budget invariants.
        Returns the incremental cost incurred in USD.
        """
        rates = PRICING_TABLE.get(model_name, ModelCostRates(1.0, 3.0))
        delta_cost = (
            (input_tokens / 1_000_000.0) * rates.input_cost_per_million
            + (output_tokens / 1_000_000.0) * rates.output_cost_per_million
        )

        with self._lock:
            new_total_tokens = self.consumed_input_tokens + self.consumed_output_tokens + input_tokens + output_tokens
            new_total_cost = self.accumulated_cost_usd + delta_cost

            if new_total_tokens > self.max_total_tokens:
                raise BudgetExceededException(
                    f"Token budget exceeded: {new_total_tokens} > {self.max_total_tokens}"
                )

            if new_total_cost > self.max_cost_usd:
                raise BudgetExceededException(
                    f"Cost budget exceeded: ${new_total_cost:.4f} > ${self.max_cost_usd:.2f}"
                )

            self.consumed_input_tokens += input_tokens
            self.consumed_output_tokens += output_tokens
            self.accumulated_cost_usd = new_total_cost

        return round(delta_cost, 6)

    def get_summary(self) -> Dict[str, any]:
        with self._lock:
            return {
                "input_tokens": self.consumed_input_tokens,
                "output_tokens": self.consumed_output_tokens,
                "total_tokens": self.consumed_input_tokens + self.consumed_output_tokens,
                "total_cost_usd": round(self.accumulated_cost_usd, 4),
                "budget_utilized_pct": round(
                    ((self.consumed_input_tokens + self.consumed_output_tokens) / self.max_total_tokens) * 100, 2
                ),
            }
