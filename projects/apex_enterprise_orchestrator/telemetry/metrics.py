"""
ApexFlow Enterprise Telemetry - High-Resolution Metrics Collector & Prometheus Exporter.
Tracks request rates, error ratios, latency percentiles (p50, p95, p99), and financial protection totals.
"""

import math
import time
from collections import deque
from threading import Lock, RLock
from typing import Dict, List, Optional


class MetricsRegistry:
    """
    Lock-free/thread-safe sliding window metrics collector.
    """

    _instance: Optional["MetricsRegistry"] = None
    _lock = Lock()

    def __new__(cls) -> "MetricsRegistry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, window_size: int = 5000):
        if getattr(self, "_initialized", False):
            return
        self.window_size = window_size
        self._latencies: deque = deque(maxlen=window_size)
        self._counters: Dict[str, int] = {
            "reconciliation_requests_total": 0,
            "reconciliation_matches_exact": 0,
            "reconciliation_discrepancies_total": 0,
            "circuit_breaker_trips_total": 0,
            "idempotency_cache_hits_total": 0,
            "pipeline_executions_total": 0,
        }
        self._gauges: Dict[str, float] = {
            "total_financial_exposure_prevented_inr": 0.0,
            "active_circuit_breakers": 0.0,
        }
        self._start_time = time.time()
        self._data_lock = RLock()
        self._initialized = True

    def increment(self, metric_name: str, count: int = 1) -> None:
        with self._data_lock:
            self._counters[metric_name] = self._counters.get(metric_name, 0) + count

    def set_gauge(self, metric_name: str, value: float) -> None:
        with self._data_lock:
            self._gauges[metric_name] = float(value)

    def add_gauge(self, metric_name: str, value: float) -> None:
        with self._data_lock:
            self._gauges[metric_name] = self._gauges.get(metric_name, 0.0) + float(value)

    def record_latency(self, duration_ms: float) -> None:
        with self._data_lock:
            self._latencies.append(duration_ms)

    def get_latency_percentiles(self) -> Dict[str, float]:
        with self._data_lock:
            if not self._latencies:
                return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "count": 0}

            sorted_lat = sorted(self._latencies)
            n = len(sorted_lat)

            def get_pct(p: float) -> float:
                idx = min(int(math.ceil(p * n)) - 1, n - 1)
                return round(sorted_lat[max(0, idx)], 3)

            return {
                "p50": get_pct(0.50),
                "p95": get_pct(0.95),
                "p99": get_pct(0.99),
                "min": round(sorted_lat[0], 3),
                "max": round(sorted_lat[-1], 3),
                "count": n,
            }

    def get_snapshot(self) -> Dict[str, any]:
        uptime_sec = round(time.time() - self._start_time, 2)
        with self._data_lock:
            return {
                "uptime_seconds": uptime_sec,
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "latencies_ms": self.get_latency_percentiles(),
            }

    def to_prometheus_format(self) -> str:
        """Renders standard Prometheus exposition format."""
        snapshot = self.get_snapshot()
        lines: List[str] = [
            "# HELP apexflow_uptime_seconds System uptime in seconds",
            "# TYPE apexflow_uptime_seconds gauge",
            f"apexflow_uptime_seconds {snapshot['uptime_seconds']}",
        ]

        for name, count in snapshot["counters"].items():
            lines.append(f"# HELP apexflow_{name} Counter metric")
            lines.append(f"# TYPE apexflow_{name} counter")
            lines.append(f"apexflow_{name} {count}")

        for name, val in snapshot["gauges"].items():
            lines.append(f"# HELP apexflow_{name} Gauge metric")
            lines.append(f"# TYPE apexflow_{name} gauge")
            lines.append(f"apexflow_{name} {val}")

        p = snapshot["latencies_ms"]
        lines.append("# HELP apexflow_reconciliation_duration_ms Latency percentiles in milliseconds")
        lines.append("# TYPE apexflow_reconciliation_duration_ms summary")
        lines.append(f'apexflow_reconciliation_duration_ms{{quantile="0.50"}} {p["p50"]}')
        lines.append(f'apexflow_reconciliation_duration_ms{{quantile="0.95"}} {p["p95"]}')
        lines.append(f'apexflow_reconciliation_duration_ms{{quantile="0.99"}} {p["p99"]}')
        lines.append(f"apexflow_reconciliation_duration_ms_count {p['count']}")

        return "\n".join(lines) + "\n"
