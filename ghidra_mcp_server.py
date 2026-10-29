#!/usr/bin/env python3
"""
NSA Ghidra Autonomous MCP (Model Context Protocol) Server
=========================================================
Exposes NSA Ghidra Software Reverse Engineering (SRE) capabilities to AI agents,
subagents, and LLMs via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- ghidra_get_info
- ghidra_analyze_binary
- ghidra_disassemble
- ghidra_decompile_function
- ghidra_get_pcode
- ghidra_list_functions
- ghidra_get_xrefs
- ghidra_extract_strings
- ghidra_inspect_sections
- ghidra_audit_vulnerabilities
- ghidra_calculate_entropy
- ghidra_find_rop_gadgets
- ghidra_detect_crypto
- ghidra_list_scripts
- ghidra_run_headless_script
- ghidra_do_everything
"""

import sys
import json
import logging
import dataclasses
from typing import Any, Dict

from ghidra_orchestrator import (
    GhidraConfig,
    GhidraOrchestrator,
    BinaryDissector
)

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("ghidra_mcp")

orchestrator = GhidraOrchestrator()

TOOLS = [
    {
        "name": "ghidra_get_info",
        "description": "Get Ghidra engine details, supported Sleigh architectures (x86, x64, ARM, MIPS, RISC-V), and P-Code opcodes.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "ghidra_analyze_binary",
        "description": "Perform full automated software reverse engineering on a binary executable (PE/ELF/Mach-O/Raw).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Absolute or relative path to the binary executable"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_disassemble",
        "description": "Disassemble binary instructions starting at an entry point or address, with Ghidra P-Code micro-operations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"},
                "address": {"type": "string", "description": "Hex address to start disassembly (optional)"},
                "count": {"type": "integer", "description": "Number of instructions to disassemble", "default": 20}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_decompile_function",
        "description": "Decompile a function into structured pseudo-C with recovered variables, types, and control flow.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"},
                "function_name": {"type": "string", "description": "Function name (e.g. main) or hex address", "default": "main"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_get_pcode",
        "description": "Extract Ghidra's intermediate representation (P-Code) microcode translation sequence.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"},
                "count": {"type": "integer", "description": "Number of P-Code operations", "default": 25}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_list_functions",
        "description": "List identified functions with calling conventions, parameters, return types, and cyclomatic complexity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_get_xrefs",
        "description": "Extract cross-references and function call graph topology (callers and callees).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_extract_strings",
        "description": "Extract ASCII and UTF-16LE strings and classify them (URLs, IPs, FilePaths, RegistryKeys, Crypto).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"},
                "min_length": {"type": "integer", "description": "Minimum string length", "default": 4},
                "category": {"type": "string", "description": "Filter by category (URL, IP_Address, FilePath, RegistryKey, CryptoConstant, API_Name)"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_inspect_sections",
        "description": "Inspect memory sections, virtual offsets, raw sizes, permissions, and Shannon entropy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_audit_vulnerabilities",
        "description": "Audit binary for dangerous libc/Win32 APIs, missing DEP/ASLR mitigations, buffer overflows, and ROP gadgets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_calculate_entropy",
        "description": "Calculate binary Shannon entropy and perform packer/crypter detection (UPX, Themida, VMProtect).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_find_rop_gadgets",
        "description": "Scan executable sections for Return-Oriented Programming (ROP) gadgets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_detect_crypto",
        "description": "Search binary for cryptographic constants (AES Rijndael S-Box, SHA-256, MD5, RC4).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "ghidra_list_scripts",
        "description": "List available Ghidra SRE analysis scripts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "ghidra_run_headless_script",
        "description": "Execute a custom Ghidra headless or Python analysis script on a binary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_path": {"type": "string", "description": "Path to analysis script"},
                "binary_path": {"type": "string", "description": "Path to binary"}
            },
            "required": ["script_path", "binary_path"]
        }
    },
    {
        "name": "ghidra_do_everything",
        "description": "Execute the comprehensive 12-Phase Sovereign SRE Lifecycle and generate signed attestation manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Optional path to target binary"}
            }
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    """Dispatches tool execution to Ghidra orchestrator."""
    if name == "ghidra_get_info":
        return orchestrator.get_info()

    if name == "ghidra_analyze_binary":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        return dataclasses.asdict(report)

    if name == "ghidra_disassemble":
        addr = int(arguments["address"], 16) if "address" in arguments and arguments["address"] else None
        count = arguments.get("count", 20)
        instrs = orchestrator.disassemble(arguments["binary_path"], address=addr, count=count)
        return [dataclasses.asdict(i) for i in instrs]

    if name == "ghidra_decompile_function":
        fn_name = arguments.get("function_name", "main")
        decomp = orchestrator.decompile_function(arguments["binary_path"], fn_name)
        return dataclasses.asdict(decomp)

    if name == "ghidra_get_pcode":
        count = arguments.get("count", 25)
        return orchestrator.get_pcode(arguments["binary_path"], count=count)

    if name == "ghidra_list_functions":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        return [dataclasses.asdict(f) for f in report.functions]

    if name == "ghidra_get_xrefs":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        edges = []
        for fn in report.functions:
            for c in fn.callees:
                edges.append({"caller": fn.name, "callee": c})
        return {"call_graph_edges": edges, "functions_count": len(report.functions)}

    if name == "ghidra_extract_strings":
        min_len = arguments.get("min_length", 4)
        cat = arguments.get("category")
        strings = orchestrator.extract_strings(arguments["binary_path"], min_len=min_len, category_filter=cat)
        return [dataclasses.asdict(s) for s in strings]

    if name == "ghidra_inspect_sections":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        return [dataclasses.asdict(s) for s in report.sections]

    if name == "ghidra_audit_vulnerabilities":
        return orchestrator.audit_vulnerabilities(arguments["binary_path"])

    if name == "ghidra_calculate_entropy":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        return {
            "overall_entropy": report.overall_entropy,
            "packer_detection": report.packer_detection,
            "sections_entropy": [{"section": s.name, "entropy": s.entropy} for s in report.sections]
        }

    if name == "ghidra_find_rop_gadgets":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        return [dataclasses.asdict(g) for g in report.rop_gadgets]

    if name == "ghidra_detect_crypto":
        report = orchestrator.analyze_binary(arguments["binary_path"])
        crypto_findings = [dataclasses.asdict(v) for v in report.vulnerabilities if "CRYPTO" in v.rule_id]
        return {"crypto_primitives_found": len(crypto_findings), "findings": crypto_findings}

    if name == "ghidra_list_scripts":
        import os
        s_dir = os.path.abspath("ghidra/scripts")
        scripts = [f for f in os.listdir(s_dir) if f.endswith(".py")] if os.path.exists(s_dir) else []
        return {"registered_scripts": scripts}

    if name == "ghidra_run_headless_script":
        return orchestrator.run_script(arguments["script_path"], arguments["binary_path"])

    if name == "ghidra_do_everything":
        bin_path = arguments.get("binary_path")
        return orchestrator.do_everything(bin_path)

    raise ValueError(f"Unknown tool: {name}")


def main():
    """Stdio JSON-RPC loop for MCP."""
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

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "ghidra-autonomous-mcp", "version": "11.1.2"}
                }
            }
            print(json.dumps(resp), flush=True)

        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS}
            }
            print(json.dumps(resp), flush=True)

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_data = handle_tool_call(name, arguments)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(result_data, indent=2)}
                        ]
                    }
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": str(e)}
                }
            print(json.dumps(resp), flush=True)

        elif method == "notifications/initialized":
            pass

        else:
            if req_id is not None:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"}
                }
                print(json.dumps(resp), flush=True)


if __name__ == "__main__":
    main()
