---
name: arrow-orchestrator
description: Autonomous SDK, CLI, Acero vectorized compute engine, C Data Interface ABI bridge, Flight RPC, and 12-phase sovereign lifecycle standard for Apache Arrow (https://github.com/apache/arrow). Enables 64-byte aligned columnar in-memory buffers, zero-copy slicing, and high-performance cross-language data sharing.
---

# Apache Arrow Autonomous Columnar & Zero-Copy Skill

Autonomous standard operating procedure and deep orchestration SDK for Apache Arrow (https://github.com/apache/arrow).

## Architecture & Primitives

1. **Columnar In-Memory Architecture**:
   - **64-Byte Memory Alignment**: All buffers align to 64-byte cache lines for hardware SIMD vectorization (AVX2, AVX-512, and ARM NEON).
   - **LSB-First Validity Bitmaps**: Continuous bit arrays where bit 1 indicates a valid value and bit 0 indicates null. If `null_count == 0`, validity buffers can be eliminated to achieve zero-overhead bitmask storage.
   - **StringView / BinaryView Layout (Arrow 15+)**: 16-byte fixed-size view descriptors `(length: uint32, prefix: 4 bytes, buffer_index: uint32, offset: uint32)` or inline small strings (<= 12 bytes), eliminating pointer chasing and allowing instant prefix comparison in a single CPU instruction.

2. **Zero-Copy Slicing ($O(1)$ Complexity)**:
   - `table.slice(offset, length)` performs a pointer offset shift rather than copying memory bytes.
   - Preserves underlying buffer addresses (`orig_buf.address == sliced_buf.address`), enabling instant windowing and chunk processing across billions of records.

3. **Arrow C Data Interface ABI**:
   - Two ABI-stable structs:
     * `struct ArrowSchema`: Encodes column name, type format string (`'l'` for int64, `'f'` for float32, `'+s'` for struct), metadata, and child schemas.
     * `struct ArrowArray`: Exposes physical length, null count, slice offset, and an array of raw buffer memory pointers.
   - Bridges C++, Python, Rust, Go, DuckDB, and Polars inside the same process with zero memory copy and zero ABI fragility.

4. **Acero Vectorized Compute Engine**:
   - SIMD-accelerated relational operators: `filter`, `project`, `sum`, `mean`, `min`, `max`, `count`, `stddev`, and hash-based `value_counts` group-by aggregations.

5. **Arrow IPC Streaming & Feather Storage**:
   - Encapsulated stream format with 4-byte continuation tokens (`0xFFFFFFFF`), Flatbuffers metadata headers, 64-byte aligned body buffers, and 4-byte zero End-of-Stream (EOS) markers.
   - Feather V2 random-access files with metadata footers and ZSTD/LZ4 compression.

6. **Apache Parquet Columnar Compression**:
   - Converts in-memory Arrow tables to compressed Parquet files with column chunks, pages, dictionary encoding, and Snappy/Zstd compression codecs.

7. **Arrow Flight RPC & Flight SQL**:
   - High-throughput client-server framework built on gRPC exchanging Arrow IPC record batches directly over TCP without serialization/deserialization bottlenecks.

8. **Model Context Protocol (MCP) Server**:
   - Exposes 12 tools over JSON-RPC 2.0 stdio (`arrow_mcp_server.py`) for AI agents and LLMs.

---

## Universal CLI Usage

```bash
# Query Arrow runtime telemetry, SIMD acceleration, and features
python arrow_cli.py info

# Create synthetic high-volume columnar datasets
python arrow_cli.py create --dataset trades --rows 50000
python arrow_cli.py create --dataset iot_telemetry --rows 25000

# Inspect columnar tables, memory sizes, and schema definitions
python arrow_cli.py inspect --table trades

# Verify O(1) zero-copy buffer slicing
python arrow_cli.py slice --offset 100 --length 500

# Execute Acero SIMD compute query (filter, statistics, group-by)
python arrow_cli.py compute --table trades --col price --op ">" --val 200.0 --group symbol

# Verify Arrow C Data Interface ABI export/import via ctypes
python arrow_cli.py c-data

# Export Arrow table to streaming IPC format (.arrows)
python arrow_cli.py ipc --table trades

# Export Arrow table to Feather random-access file (.arrow)
python arrow_cli.py feather --table trades

# Export Arrow table to compressed Apache Parquet (.parquet)
python arrow_cli.py parquet --table trades --compression snappy

# Query Flight RPC catalog or stream records via ticket
python arrow_cli.py flight
python arrow_cli.py flight --ticket /datasets/trades

# Run microsecond throughput benchmark suite
python arrow_cli.py benchmark --rows 100000

# Execute complete 12-Phase Sovereign Lifecycle
python arrow_cli.py do-everything
```

---

## Python SDK Integration

```python
from arrow_orchestrator import ArrowOrchestrator

orchestrator = ArrowOrchestrator()

# 1. Generate columnar table
table = orchestrator.generate_trades_table(num_rows=50_000)

# 2. Zero-copy slice
slice_result = orchestrator.demonstrate_zero_copy_slicing(offset=100, length=500)
print("Zero copy verified:", slice_result["zero_copy_verified"])

# 3. Vectorized compute query
query_result = orchestrator.execute_vectorized_query(
    table_name="trades",
    filter_col="price",
    filter_op=">",
    filter_val=250.0,
    group_col="symbol"
)
print("Filtered rows:", query_result["statistics"]["row_count_after"])

# 4. C Data Interface roundtrip
c_abi = orchestrator.run_c_data_interface_abi()
print("C ABI Format:", c_abi["format_code"])

# 5. Full 12-Phase Verification
manifest = orchestrator.run_all_phases()
print("Sovereign status:", manifest["overall_status"])
```

---

## 12-Phase Sovereign Verification Standard

All Arrow deployments in this workspace must satisfy Section 101 of the OMEGA Constitution:
- **Phase 1**: Columnar In-Memory Layout & 64-Byte SIMD Alignment Verification
- **Phase 2**: Comprehensive Type System & Nested Schemas
- **Phase 3**: Zero-Copy Slicing & Memoryview Safety Validation
- **Phase 4**: Arrow C Data Interface ABI Conformance
- **Phase 5**: Acero & Vectorized Compute Engine
- **Phase 6**: Arrow IPC Streaming Serialization & Parsing
- **Phase 7**: Arrow IPC Random-Access File Format & Feather Integration
- **Phase 8**: Apache Parquet Columnar Storage & Compression Interop
- **Phase 9**: Arrow Flight RPC & Flight SQL Protocol Simulation
- **Phase 10**: Multi-Engine Zero-Copy Interop (NumPy & Pandas)
- **Phase 11**: High-Performance SIMD & Vectorized Throughput Micro-Benchmarking
- **Phase 12**: Autonomous Mission Control Cockpit, Local REST API Server & MCP Attestation
