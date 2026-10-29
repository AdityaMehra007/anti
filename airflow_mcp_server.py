#!/usr/bin/env python3
"""
Apache Airflow Model Context Protocol (MCP) Server
=================================================
JSON-RPC 2.0 stdio server exposing 15 high-leverage Apache Airflow tools
for autonomous AI agents, multi-agent swarms, and LLMs.

Usage:
    python airflow_mcp_server.py
"""

from __future__ import annotations

import sys
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import asdict
from airflow_orchestrator import AirflowClient, AirflowConfig, AirflowOrchestrator

logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("airflow_mcp_server")

client = AirflowClient()


def get_tool_definitions() -> List[Dict[str, Any]]:
    return [
        {
            "name": "airflow_get_health",
            "description": "Check Apache Airflow system health, scheduler heartbeat, and metadb status.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_dags",
            "description": "List all registered Directed Acyclic Graphs (DAGs) with schedules, tags, and active status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "active_only": {"type": "boolean", "description": "Filter for active (unpaused) DAGs only"}
                },
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_get_dag_details",
            "description": "Retrieve comprehensive metadata for a specific DAG including tasks, operators, and topological order.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The unique identifier of the DAG"}
                },
                "required": ["dag_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_trigger_dag",
            "description": "Trigger a new execution run of a DAG with an optional configuration payload.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The unique identifier of the DAG"},
                    "conf": {"type": "object", "description": "JSON configuration payload passed to the DAG Run"}
                },
                "required": ["dag_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_toggle_dag_pause",
            "description": "Pause or unpause an Airflow DAG to control automated scheduling.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The DAG identifier"},
                    "is_paused": {"type": "boolean", "description": "True to pause, False to unpause (activate)"}
                },
                "required": ["dag_id", "is_paused"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_dag_runs",
            "description": "List historical and active DAG runs with execution dates, states, and durations.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The DAG identifier"}
                },
                "required": ["dag_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_task_instances",
            "description": "List task instances and execution states for a specific DAG run.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The DAG identifier"},
                    "run_id": {"type": "string", "description": "Optional specific run_id (defaults to latest)"}
                },
                "required": ["dag_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_get_task_log",
            "description": "Retrieve execution logs for an individual task instance attempt.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The DAG identifier"},
                    "run_id": {"type": "string", "description": "The DAG Run identifier"},
                    "task_id": {"type": "string", "description": "The Task identifier"}
                },
                "required": ["dag_id", "run_id", "task_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_get_xcom",
            "description": "Pull XCom metadata values pushed by a task instance for inter-task coordination.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "dag_id": {"type": "string", "description": "The DAG identifier"},
                    "task_id": {"type": "string", "description": "The Task identifier"},
                    "key": {"type": "string", "description": "Optional XCom key filter"}
                },
                "required": ["dag_id", "task_id"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_variables",
            "description": "List global Airflow configuration variables.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_set_variable",
            "description": "Set or update an Airflow configuration variable.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Variable key"},
                    "val": {"type": "string", "description": "Variable value"},
                    "description": {"type": "string", "description": "Description of the variable"}
                },
                "required": ["key", "val"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_connections",
            "description": "List configured external service connections (databases, cloud storage, webhooks).",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_list_pools",
            "description": "List concurrency pools, total slots, and current slot saturation.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_emit_dataset_event",
            "description": "Emit an update event to an Airflow Dataset / Asset URI to trigger data-driven consumer pipelines.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "uri": {"type": "string", "description": "The Dataset URI (e.g. s3://warehouse/sales/raw.parquet)"},
                    "source": {"type": "string", "description": "Origin task or agent producing the update"}
                },
                "required": ["uri"],
                "additionalProperties": False
            }
        },
        {
            "name": "airflow_audit_dags",
            "description": "Run static security, reliability, and concurrency audits on all registered DAGs.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    ]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "airflow_get_health":
        return client.get_health()

    elif name == "airflow_list_dags":
        dags = client.list_dags()
        if arguments.get("active_only"):
            dags = [d for d in dags if not d["is_paused"]]
        return dags

    elif name == "airflow_get_dag_details":
        dag_id = arguments["dag_id"]
        dag = client.get_dag(dag_id)
        dag["topological_order"] = client.mock_engine.topological_sort_dag(dag_id)
        return dag

    elif name == "airflow_trigger_dag":
        return client.trigger_dag(arguments["dag_id"], conf=arguments.get("conf", {}))

    elif name == "airflow_toggle_dag_pause":
        dag = client.mock_engine.toggle_dag_pause(arguments["dag_id"], arguments["is_paused"])
        return asdict(dag)

    elif name == "airflow_list_dag_runs":
        return client.list_dag_runs(arguments["dag_id"])

    elif name == "airflow_list_task_instances":
        runs = client.list_dag_runs(arguments["dag_id"])
        if not runs:
            return {"error": "No runs found for DAG"}
        run_id = arguments.get("run_id")
        target_run = runs[0]
        if run_id:
            for r in runs:
                if r["run_id"] == run_id:
                    target_run = r
                    break
        return target_run.get("task_instances", {})

    elif name == "airflow_get_task_log":
        dag_id = arguments["dag_id"]
        run_id = arguments["run_id"]
        task_id = arguments["task_id"]
        runs = client.list_dag_runs(dag_id)
        for r in runs:
            if r["run_id"] == run_id:
                ti = r.get("task_instances", {}).get(task_id)
                if ti:
                    return {"task_id": task_id, "state": ti["state"], "log": ti["log"]}
        return {"error": f"Task instance '{task_id}' in run '{run_id}' not found."}

    elif name == "airflow_get_xcom":
        dag_id = arguments["dag_id"]
        task_id = arguments["task_id"]
        key = arguments.get("key")
        entries = [asdict(x) for x in client.mock_engine.xcom_store if x.dag_id == dag_id and x.task_id == task_id]
        if key:
            entries = [x for x in entries if x["key"] == key]
        return entries

    elif name == "airflow_list_variables":
        return client.list_variables()

    elif name == "airflow_set_variable":
        return client.set_variable(arguments["key"], arguments["val"], description=arguments.get("description", ""))

    elif name == "airflow_list_connections":
        return client.list_connections()

    elif name == "airflow_list_pools":
        return client.list_pools()

    elif name == "airflow_emit_dataset_event":
        client.emit_dataset_event(arguments["uri"], source=arguments.get("source", "mcp_agent"))
        return {"status": "SUCCESS", "message": f"Dataset update event emitted for '{arguments['uri']}'"}

    elif name == "airflow_audit_dags":
        return client.mock_engine.audit_security_and_best_practices()

    else:
        raise ValueError(f"Unknown tool: '{name}'")


def main():
    """Main JSON-RPC 2.0 loop reading from stdin and writing to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "tools/list":
            res = {"tools": get_tool_definitions()}
            response = {"jsonrpc": "2.0", "id": req_id, "result": res}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                result = handle_tool_call(tool_name, tool_args)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(result, indent=2)}
                        ]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "airflow-mcp-server", "version": "1.0.0"}
            }
            response = {"jsonrpc": "2.0", "id": req_id, "result": res}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
