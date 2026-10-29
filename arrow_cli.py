#!/usr/bin/env python3
r"""
Apache Arrow Universal CLI
==========================
Autonomous command-line interface for Apache Arrow columnar engine,
zero-copy memory management, Acero vectorized compute, C Data Interface ABI,
Arrow Flight RPC, Parquet storage, and 12-phase sovereign lifecycle verification.
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Any, Dict

from arrow_orchestrator import ArrowOrchestrator, PYARROW_AVAILABLE, PYARROW_VERSION


def format_table_output(data: Any) -> None:
    """Print structured data as indented formatted JSON."""
    print(json.dumps(data, indent=2, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="arrow_cli",
        description="Apache Arrow Autonomous Columnar & Zero-Copy CLI (https://github.com/apache/arrow)",
    )
    parser.add_argument("--version", action="version", version=f"arrow_cli (PyArrow {PYARROW_VERSION})")
    parser.add_argument("--json", action="store_true", help="Force raw JSON output")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Display Arrow runtime architecture, SIMD status, and feature matrix")

    # schemas
    p_schemas = subparsers.add_parser("schemas", help="List registered columnar schemas or inspect schema details")
    p_schemas.add_argument("--name", type=str, default=None, help="Schema name to inspect")

    # create
    p_create = subparsers.add_parser("create", help="Generate synthetic columnar datasets (trades, iot_telemetry)")
    p_create.add_argument("--dataset", type=str, choices=["trades", "iot_telemetry"], default="trades", help="Dataset archetype")
    p_create.add_argument("--rows", type=int, default=25000, help="Number of rows to generate")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Deep inspection of columnar table buffers and validity bitmaps")
    p_inspect.add_argument("--table", type=str, default="trades", help="Table name to inspect")

    # slice
    p_slice = subparsers.add_parser("slice", help="Demonstrate zero-copy slicing with buffer pointer verification")
    p_slice.add_argument("--offset", type=int, default=100, help="Slice starting row offset")
    p_slice.add_argument("--length", type=int, default=500, help="Slice row length")

    # compute
    p_compute = subparsers.add_parser("compute", help="Execute vectorized Acero query (filter, aggregates, group-by)")
    p_compute.add_argument("--table", type=str, default="trades", help="Table name")
    p_compute.add_argument("--col", type=str, default="price", help="Column to filter")
    p_compute.add_argument("--op", type=str, default=">", choices=[">", ">=", "<", "<=", "=="], help="Comparison operator")
    p_compute.add_argument("--val", type=float, default=200.0, help="Filter threshold value")
    p_compute.add_argument("--group", type=str, default="symbol", help="Optional column to group by")

    # ipc
    p_ipc = subparsers.add_parser("ipc", help="Export Arrow table to encapsulated IPC stream format (.arrows)")
    p_ipc.add_argument("--table", type=str, default="trades", help="Table name")
    p_ipc.add_argument("--output", type=str, default=None, help="Output file name")

    # feather
    p_feather = subparsers.add_parser("feather", help="Export Arrow table to Feather / IPC file format (.arrow)")
    p_feather.add_argument("--table", type=str, default="trades", help="Table name")
    p_feather.add_argument("--output", type=str, default=None, help="Output file name")

    # parquet
    p_parquet = subparsers.add_parser("parquet", help="Convert Arrow table to compressed Apache Parquet format")
    p_parquet.add_argument("--table", type=str, default="trades", help="Table name")
    p_parquet.add_argument("--compression", type=str, choices=["snappy", "zstd", "gzip", "none"], default="snappy", help="Compression codec")
    p_parquet.add_argument("--output", type=str, default=None, help="Output file name")

    # c-data
    subparsers.add_parser("c-data", help="Verify Arrow C Data Interface ABI export and import roundtrip")

    # flight
    p_flight = subparsers.add_parser("flight", help="Inspect Arrow Flight RPC catalog and simulate ticket streaming")
    p_flight.add_argument("--ticket", type=str, default=None, help="Flight ticket token to stream")

    # benchmark
    p_bench = subparsers.add_parser("benchmark", help="Run high-precision microsecond throughput benchmark suite")
    p_bench.add_argument("--rows", type=int, default=100000, help="Number of rows for benchmark")

    # do-everything
    subparsers.add_parser("do-everything", help="Execute complete 12-Phase Sovereign Lifecycle verification")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    orchestrator = ArrowOrchestrator()

    if args.command == "info":
        res = orchestrator.get_telemetry()
        format_table_output(res)
        return 0

    elif args.command == "schemas":
        if args.name:
            res = orchestrator.get_schema(args.name)
            if not res:
                print(f"Error: Schema '{args.name}' not found.", file=sys.stderr)
                return 1
            format_table_output(res)
        else:
            format_table_output({
                "registered_schemas": list(orchestrator.schemas_cache.keys()),
                "schemas": orchestrator.schemas_cache,
            })
        return 0

    elif args.command == "create":
        if args.dataset == "trades":
            t = orchestrator.generate_trades_table(num_rows=args.rows)
            rows = t.num_rows if hasattr(t, "num_rows") else len(t)
            print(f"[OK] Generated 'trades' Arrow Table with {rows:,} rows.")
        else:
            t = orchestrator.generate_iot_telemetry_table(num_rows=args.rows)
            rows = t.num_rows if hasattr(t, "num_rows") else len(t)
            print(f"[OK] Generated 'iot_telemetry' Arrow Table with {rows:,} rows.")
        return 0

    elif args.command == "inspect":
        if args.table not in orchestrator.tables_cache:
            orchestrator.generate_trades_table(num_rows=1000)
        table = orchestrator.tables_cache.get(args.table)
        if hasattr(table, "schema"):
            schema_info = [{"name": f.name, "type": str(f.type), "nullable": f.nullable} for f in table.schema]
            res = {
                "table_name": args.table,
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "schema": schema_info,
                "memory_size_bytes": table.nbytes,
                "memory_size_kb": round(table.nbytes / 1024.0, 2),
            }
        else:
            res = {"table_name": args.table, "rows": len(table) if isinstance(table, list) else 0}
        format_table_output(res)
        return 0

    elif args.command == "slice":
        res = orchestrator.demonstrate_zero_copy_slicing(offset=args.offset, length=args.length)
        format_table_output(res)
        return 0

    elif args.command == "compute":
        res = orchestrator.execute_vectorized_query(
            table_name=args.table,
            filter_col=args.col,
            filter_op=args.op,
            filter_val=args.val,
            group_col=args.group,
        )
        format_table_output(res)
        return 0

    elif args.command == "ipc":
        res = orchestrator.export_ipc_stream(table_name=args.table, filename=args.output)
        format_table_output(res)
        return 0

    elif args.command == "feather":
        res = orchestrator.export_feather_file(table_name=args.table, filename=args.output)
        format_table_output(res)
        return 0

    elif args.command == "parquet":
        codec = args.compression if args.compression != "none" else None
        res = orchestrator.export_parquet(table_name=args.table, filename=args.output, compression=codec or "snappy")
        format_table_output(res)
        return 0

    elif args.command == "c-data":
        res = orchestrator.run_c_data_interface_abi()
        format_table_output(res)
        return 0

    elif args.command == "flight":
        if args.ticket:
            res = orchestrator.flight_do_get(args.ticket)
        else:
            res = orchestrator.get_flight_catalog()
        format_table_output(res)
        return 0

    elif args.command == "benchmark":
        print(f"Running microsecond benchmarks with {args.rows:,} rows...")
        res = orchestrator.run_benchmarks(num_rows=args.rows)
        format_table_output(res)
        return 0

    elif args.command == "do-everything":
        print("Executing Apache Arrow Sovereign 12-Phase Lifecycle Protocol...")
        res = orchestrator.run_all_phases()
        print(f"\nResult: {res['overall_status']}")
        print(f"Elapsed: {res['total_elapsed_seconds']}s")
        print(f"Phases Passed: {res['total_phases_executed']} / 12")
        print(f"Manifest written to: {os.path.join(orchestrator.manifest_dir, 'arrow_do_everything_manifest.json')}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
