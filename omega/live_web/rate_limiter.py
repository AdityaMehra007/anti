"""
CRAWL BUDGET & RATE LIMITING
Controls per-domain limits, backoff, and tracks financial & compute costs.
"""
import time
from typing import Dict, Optional
from dataclasses import dataclass, field

@dataclass
class CrawlBudget:
    max_pages: int = 100
    max_requests: int = 200
    max_cost_usd: float = 5.00
    max_time_seconds: float = 300.0
    pages_consumed: int = 0
    requests_consumed: int = 0
    cost_consumed_usd: float = 0.0
    start_time: float = field(default_factory=time.time)

    def is_exhausted(self) -> bool:
        if self.pages_consumed >= self.max_pages:
            return True
        if self.requests_consumed >= self.max_requests:
            return True
        if self.cost_consumed_usd >= self.max_cost_usd:
            return True
        if (time.time() - self.start_time) >= self.max_time_seconds:
            return True
        return False

    def record_request(self, pages: int = 1, cost_usd: float = 0.001):
        self.requests_consumed += 1
        self.pages_consumed += pages
        self.cost_consumed_usd += cost_usd

@dataclass
class DomainThrottle:
    domain: str
    last_request_time: float = 0.0
    min_interval_seconds: float = 0.5
    concurrency_limit: int = 3
    active_requests: int = 0

class RateLimiter:
    def __init__(self, default_interval: float = 0.5):
        self.default_interval = default_interval
        self._domain_throttles: Dict[str, DomainThrottle] = {}

    def get_throttle(self, domain: str) -> DomainThrottle:
        if domain not in self._domain_throttles:
            self._domain_throttles[domain] = DomainThrottle(
                domain=domain,
                min_interval_seconds=self.default_interval
            )
        return self._domain_throttles[domain]

    def acquire(self, domain: str) -> bool:
        throttle = self.get_throttle(domain)
        now = time.time()
        elapsed = now - throttle.last_request_time
        if elapsed < throttle.min_interval_seconds:
            time.sleep(throttle.min_interval_seconds - elapsed)
        throttle.last_request_time = time.time()
        throttle.active_requests += 1
        return True

    def release(self, domain: str):
        throttle = self.get_throttle(domain)
        if throttle.active_requests > 0:
            throttle.active_requests -= 1
