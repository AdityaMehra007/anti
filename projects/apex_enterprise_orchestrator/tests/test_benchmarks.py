"""Benchmark & High-Throughput Stress Tests for ApexFlow Engine."""

import pytest
from projects.apex_enterprise_orchestrator.reconciliation.batch_runner import (
    BatchReconciliationEngine,
)


def test_high_throughput_batch_streaming():
    engine = BatchReconciliationEngine()
    test_volume = 5000

    stream = engine.generate_synthetic_stream(count=test_volume)
    assert len(stream) == test_volume

    report = engine.process_triplets(stream)

    # Verification criteria
    assert report["total_records"] == test_volume
    assert report["elapsed_seconds"] < 1.0  # Must process 5k records in under 1 second
    assert report["throughput_records_per_sec"] > 5000  # Minimum 5,000 recs/sec
    assert report["average_latency_ms"] < 0.2  # Under 200 microseconds per transaction
    assert report["total_exposure_prevented"] > 0.0

    # Ensure discrepancy catches
    assert report["verdict_counts"]["EXACT_MATCH"] > 0
    assert report["verdict_counts"]["QUANTITY_MISMATCH"] > 0
    assert report["verdict_counts"]["PRICE_MISMATCH"] > 0
    assert report["verdict_counts"]["MISSING_GRN"] > 0
