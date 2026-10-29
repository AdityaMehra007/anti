#!/usr/bin/env python3
r"""
Apache Arrow Autonomous MCP (Model Context Protocol) Server
============================================================
Exposes Apache Arrow Columnar & Zero-Copy Ecosystem capabilities to AI agents,
subagents, and LLMs via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- arrow_get_telemetry
- arrow_list_schemas
- arrow_create_dataset
- arrow_zero_copy_slice
- arrow_vectorized_compute
- arrow_c_data_interface
- arrow_export_ipc
- arrow_export_parquet
- arrow_flight_catalog
- arrow_flight_do_get
- arrow_run_benchmarks
- arrow_do_everything
"""

import sys
import json
import logging
from typing import Any, Dict

from arrow_orchestrator import ArrowOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("arrow_mcp")

orchestrator = ArrowOrchestrator()

TOOLS = [
    {
        "name": "arrow_get_telemetry",
        "description": "Get Apache Arrow runtime telemetry, SIMD acceleration, memory alignment, and feature matrix.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_list_schemas",
        "description": "List registered columnar schemas (financial trades, IoT telemetry, orderbooks, risk portfolios).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Optional schema name to inspect in detail"}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_create_dataset",
        "description": "Generate high-throughput columnar Arrow dataset in memory (trades or iot_telemetry).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dataset": {"type": "string", "enum": ["trades", "iot_telemetry"], "default": "trades"},
                "rows": {"type": "integer", "default": 25000}
            },
            "required": ["dataset"],
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_zero_copy_slice",
        "description": "Demonstrate O(1) zero-copy buffer slicing with raw memory address attestation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "offset": {"type": "integer", "default": 100},
                "length": {"type": "integer", "default": 500}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_vectorized_compute",
        "description": "Execute vectorized Acero relational query (filter, statistics, hash group-by aggregation).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "default": "trades"},
                "col": {"type": "string", "default": "price"},
                "op": {"type": "string", "enum": [">", ">=", "<", "<=", "=="], "default": ">"},
                "val": {"type": "number", "default": 200.0},
                "group": {"type": "string", "default": "symbol"}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_c_data_interface",
        "description": "Verify Arrow C Data Interface ABI export and re-import via ctypes ArrowSchema & ArrowArray.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_export_ipc",
        "description": "Serialize Arrow table to encapsulated IPC stream format (.arrows) with continuation headers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "default": "trades"},
                "filename": {"type": "string"}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_export_parquet",
        "description": "Convert Arrow table to compressed Apache Parquet columnar storage format.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "default": "trades"},
                "compression": {"type": "string", "enum": ["snappy", "zstd", "gzip", "none"], "default": "snappy"},
                "filename": {"type": "string"}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_flight_catalog",
        "description": "Inspect registered Arrow Flight RPC endpoints, tickets, and dataset descriptors.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_flight_do_get",
        "description": "Simulate Arrow Flight DoGet stream retrieval using opaque ticket token.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticket": {"type": "string", "description": "Ticket string or endpoint path"}
            },
            "required": ["ticket"],
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_run_benchmarks",
        "description": "Execute microsecond throughput benchmark suite (slicing, SIMD sum/filter, IPC, Parquet).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rows": {"type": "integer", "default": 50000}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "arrow_do_everything",
        "description": "Execute complete 12-Phase Sovereign Lifecycle verification and generate attested manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


def execute_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Dispatch tool name to orchestrator logic."""
    if name == "arrow_get_telemetry":
        return orchestrator.get_telemetry()
    elif name == "arrow_list_schemas":
        schema_name = arguments.get("name")
        if schema_name:
            return orchestrator.get_schema(schema_name) or {"error": f"Schema {schema_name} not found"}
        return orchestrator.schemas_cache
    elif name == "arrow_create_dataset":
        dataset = arguments.get("dataset", "trades")
        rows = int(arguments.get("rows", 25000))
        if dataset == "trades":
            t = orchestrator.generate_trades_table(num_rows=rows)
        else:
            t = orchestrator.generate_iot_telemetry_table(num_rows=rows)
        row_count = t.num_rows if hasattr(t, "num_rows") else len(t)
        return {"status": "SUCCESS", "dataset": dataset, "rows_created": row_count}
    elif name == "arrow_zero_copy_slice":
        return orchestrator.demonstrate_zero_copy_slicing(
            offset=int(arguments.get("offset", 100)),
            length=int(arguments.get("length", 500)),
        )
    elif name == "arrow_vectorized_compute":
        return orchestrator.execute_vectorized_query(
            table_name=arguments.get("table", "trades"),
            filter_col=arguments.get("col", "price"),
            filter_op=arguments.get("op", ">"),
            filter_val=float(arguments.get("val", 200.0)),
            group_col=arguments.get("group", "symbol"),
        )
    elif name == "arrow_c_data_interface":
        return orchestrator.run_c_data_interface_abi()
    elif name == "arrow_export_ipc":
        return orchestrator.export_ipc_stream(
            table_name=arguments.get("table", "trades"),
            filename=arguments.get("filename"),
        )
    elif name == "arrow_export_parquet":
        return orchestrator.export_parquet(
            table_name=arguments.get("table", "trades"),
            filename=arguments.get("filename"),
            compression=arguments.get("compression", "snappy"),
        )
    elif name == "arrow_flight_catalog":
        return orchestrator.get_flight_catalog()
    elif name == "arrow_flight_do_get":
        return orchestrator.flight_do_get(ticket=arguments.get("ticket", "/datasets/trades"))
    elif name == "arrow_run_benchmarks":
        return orchestrator.run_benchmarks(num_rows=int(arguments.get("rows", 50000)))
    elif name == "arrow_do_everything":
        return orchestrator.run_all_phases()
    else:
        raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    """JSON-RPC 2.0 stdio server loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "arrow-mcp-server",
                        "version": "1.0.0",
                    },
                },
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS},
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                result_data = execute_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_data, indent=2, default=str),
                            }
                        ]
                    },
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)},
                }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"},
            }

        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
