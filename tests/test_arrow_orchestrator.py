"""
Tests for Apache Arrow Autonomous Columnar & Zero-Copy Orchestrator
===================================================================
Tests 64-byte aligned memory buffers, validity bitmaps, zero-copy slicing,
Arrow C Data Interface ABI structures, Acero vectorized compute, Arrow IPC streaming,
Feather V2 random access, Parquet columnar storage, and 12-phase sovereign lifecycle.
"""

import os
import pytest
from arrow_orchestrator import (
    ArrowOrchestrator,
    ArrowBuffer,
    ValidityBitmap,
    ArrowSchema,
    ArrowArray,
    PYARROW_AVAILABLE,
)


@pytest.fixture
def orchestrator():
    return ArrowOrchestrator()


def test_buffer_memory_alignment():
    buf = ArrowBuffer(b"TESTDATA" * 5, alignment=64)
    assert buf.size_bytes % 64 == 0
    assert len(buf.data) % 64 == 0
    assert "..." in buf.hex_preview(16)


def test_validity_bitmap_lsb_first():
    bitmap = ValidityBitmap(length=16, null_indices=[0, 3, 7])
    assert not bitmap.is_valid(0)
    assert bitmap.is_valid(1)
    assert bitmap.is_valid(2)
    assert not bitmap.is_valid(3)
    assert not bitmap.is_valid(7)
    assert bitmap.is_valid(8)
    assert bitmap.null_count == 3
    bitstr = bitmap.to_bitstring(8)
    assert bitstr.startswith("0110")


def test_runtime_telemetry(orchestrator):
    telemetry = orchestrator.get_telemetry()
    assert telemetry["system"] == "Apache Arrow Autonomous Columnar & Zero-Copy Engine"
    assert telemetry["memory_alignment_bytes"] == 64
    assert telemetry["total_registered_schemas"] >= 3
    assert telemetry["flight_endpoints"] >= 2


def test_schemas_registry(orchestrator):
    trades_schema = orchestrator.get_schema("financial_trades")
    assert trades_schema is not None
    assert trades_schema["name"] == "financial_trades"
    assert trades_schema["field_count"] == 8

    iot_schema = orchestrator.get_schema("iot_sensor_telemetry")
    assert iot_schema is not None
    assert iot_schema["name"] == "iot_sensor_telemetry"


def test_dataset_generation(orchestrator):
    trades = orchestrator.generate_trades_table(num_rows=1000)
    rows = trades.num_rows if hasattr(trades, "num_rows") else len(trades)
    assert rows == 1000

    iot = orchestrator.generate_iot_telemetry_table(num_rows=500)
    rows_iot = iot.num_rows if hasattr(iot, "num_rows") else len(iot)
    assert rows_iot == 500


def test_zero_copy_slicing(orchestrator):
    res = orchestrator.demonstrate_zero_copy_slicing(offset=50, length=200)
    assert res["slice_offset"] == 50
    assert res["slice_length"] == 200
    assert res["zero_copy_verified"] is True
    assert res["slice_duration_ns"] > 0


def test_c_data_interface_abi(orchestrator):
    c_res = orchestrator.run_c_data_interface_abi()
    assert c_res["abi_standard"] == "Arrow C Data Interface v1.0"
    assert c_res["format_code"] == "l"
    assert c_res["exported_length"] == 8
    assert c_res["exported_null_count"] == 1
    assert c_res["zero_copy_preserved"] is True


def test_acero_vectorized_compute(orchestrator):
    res = orchestrator.execute_vectorized_query(
        table_name="trades",
        filter_col="price",
        filter_op=">",
        filter_val=150.0,
        group_col="symbol",
    )
    assert "statistics" in res
    assert res["statistics"]["row_count_after"] > 0
    assert res["statistics"]["price_sum"] > 0
    assert res["statistics"]["price_mean"] > 0


def test_ipc_stream_export(orchestrator):
    res = orchestrator.export_ipc_stream(table_name="trades")
    assert "size_bytes" in res
    assert res["size_bytes"] > 0
    assert os.path.exists(res["file_path"])


def test_feather_export(orchestrator):
    res = orchestrator.export_feather_file(table_name="trades")
    assert "size_bytes" in res
    assert res["size_bytes"] > 0
    assert os.path.exists(res["file_path"])


def test_parquet_export(orchestrator):
    res = orchestrator.export_parquet(table_name="trades", compression="snappy")
    assert res["format"] == "Apache Parquet Columnar Storage"
    assert res["compressed_size_bytes"] > 0
    assert os.path.exists(res["file_path"])


def test_flight_catalog_and_get(orchestrator):
    cat = orchestrator.get_flight_catalog()
    assert cat["total_endpoints"] >= 2
    assert "/datasets/trades" in cat["endpoints"]

    flight_res = orchestrator.flight_do_get("/datasets/trades")
    assert flight_res["flight_status"] == "FLIGHT_STREAM_ACTIVE"
    assert flight_res["zero_copy_wire_transfer"] is True


def test_benchmark_runner(orchestrator):
    bench = orchestrator.run_benchmarks(num_rows=2000)
    assert "zero_copy_slicing" in bench
    assert "simd_vectorized_sum" in bench
    assert "simd_vectorized_filter" in bench
    assert "arrow_ipc_serialization" in bench
    assert "parquet_columnar_write" in bench


def test_12_phase_lifecycle(orchestrator):
    manifest = orchestrator.run_all_phases()
    assert manifest["total_phases_executed"] == 12
    assert "SOVEREIGN APACHE ARROW SUITE OPERATIONAL" in manifest["overall_status"]
    assert all(p["status"] == "PASSED" for p in manifest["phases"])
