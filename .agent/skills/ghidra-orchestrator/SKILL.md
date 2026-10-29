---
name: ghidra-orchestrator
description: Autonomous SDK, CLI, and operational standard for NSA Ghidra Software Reverse Engineering (SRE) suite. Disassembles multi-architecture binaries (x86, x64, ARM, MIPS, RISC-V), generates Ghidra P-Code microcode, decompiles to pseudo-C, audits exploit mitigations, and identifies vulnerabilities.
---

# NSA Ghidra Autonomous SRE & Reverse Engineering Skill

Autonomous standard operating procedure and deep SDK for NSA Ghidra (https://github.com/NationalSecurityAgency/ghidra).

## Architecture & Primitives

1. **Dual-Mode Execution Architecture**:
   - **Live Ghidra Execution**: Direct execution via `support/analyzeHeadless` / `support/analyzeHeadless.bat` or PyGhidra. Automates program database creation (`.gpr` / `.rep`), headless script execution, and export of decompiled ASTs.
   - **Autonomous SRE Engine**: Self-contained pure-Python reverse engineering core supporting PE32/PE32+, ELF32/ELF64, Mach-O, and raw binary dissection, Shannon entropy calculation, x86/x64 and ARM disassembly, P-Code micro-operation translation, control flow graph pseudo-C decompilation, and vulnerability analysis.

2. **Core Capabilities**:
   - **Multi-Format Dissection**: Parses headers, memory sections, entry points, image bases, and import/export tables.
   - **Sleigh Multi-Architecture Disassembly**: Decodes opcodes and instructions across x86, x86_64, ARMv8, AArch64, MIPS, and RISC-V.
   - **P-Code Intermediate Representation (IR)**: Generates Ghidra's 78 canonical microcode operations (`COPY`, `LOAD`, `STORE`, `BRANCH`, `CBRANCH`, `CALL`, `INT_ADD`, `INT_SUB`, etc.).
   - **High-Fidelity Decompiler**: Reconstructs control flow graphs, recovers variable names, eliminates dead code, and synthesizes structured ANSI C pseudo-code.
   - **Vulnerability & Exploit Mitigations**:
     * Audits ASLR, DEP/NX, Stack Canaries (/GS), SafeSEH, and Control Flow Guard (CFG).
     * Scans for dangerous C runtime APIs (`strcpy`, `strcat`, `sprintf`, `gets`, `system`, `popen`, `WinExec`).
     * Identifies Return-Oriented Programming (ROP) gadgets (`pop reg; ret`, `mov [reg], reg; ret`, `syscall; ret`).
     * Detects cryptographic constant tables (AES S-Box, SHA-256 initial words, MD5, RC4).
     * Shannon entropy calculation per section to detect UPX, Themida, and custom cryptors/packers.
   - **Model Context Protocol (MCP)**: Exposes 16 tools over JSON-RPC 2.0 stdio (`ghidra_mcp_server.py`).

## Universal CLI Usage

```bash
# Query Ghidra engine telemetry and supported architectures
python ghidra_cli.py info

# Dissect binary and run full automated SRE analysis
python ghidra_cli.py analyze <binary_path>

# Disassemble instructions with P-Code micro-operations
python ghidra_cli.py disasm <binary_path> [--addr 0x140001000] [--count 25]

# Decompile function into structured pseudo-C
python ghidra_cli.py decompile <binary_path> [--func main]

# Extract Ghidra P-Code microcode sequence
python ghidra_cli.py pcode <binary_path> [--count 25]

# Extract ASCII/Unicode strings and classify IOCs
python ghidra_cli.py strings <binary_path> [--min-len 4] [--filter URL]

# Inspect memory sections and Shannon entropy
python ghidra_cli.py sections <binary_path>

# List functions, calling conventions, and complexity
python ghidra_cli.py functions <binary_path>

# Audit security vulnerabilities and exploit mitigations
python ghidra_cli.py vulns <binary_path>

# Scan for Return-Oriented Programming (ROP) gadgets
python ghidra_cli.py rop <binary_path>

# Calculate Shannon entropy and detect packers
python ghidra_cli.py entropy <binary_path>

# List registered SRE analysis scripts
python ghidra_cli.py scripts

# Run custom Ghidra headless script
python ghidra_cli.py run-script ghidra/scripts/find_dangerous_apis.py <binary_path>

# Execute master 12-phase sovereign lifecycle
python ghidra_cli.py do-everything
```

## Model Context Protocol (MCP) Server

Launch the MCP server via stdio:
```bash
python ghidra_mcp_server.py
```

Available MCP Tools:
- `ghidra_get_info`: Engine metadata, supported ISAs, and P-Code opcodes.
- `ghidra_analyze_binary`: Comprehensive SRE analysis report.
- `ghidra_disassemble`: Sleigh disassembly instructions.
- `ghidra_decompile_function`: High-level pseudo-C decompiler.
- `ghidra_get_pcode`: Ghidra microcode IR sequence.
- `ghidra_list_functions`: Recovered functions and calling conventions.
- `ghidra_get_xrefs`: Cross-references and call graph topology.
- `ghidra_extract_strings`: String intelligence with IOC categorizer.
- `ghidra_inspect_sections`: Memory sections and permissions.
- `ghidra_audit_vulnerabilities`: Vulnerability scan and exploit mitigations.
- `ghidra_calculate_entropy`: Shannon entropy and packer detection.
- `ghidra_find_rop_gadgets`: ROP gadget finder.
- `ghidra_detect_crypto`: Cryptographic primitive scanner.
- `ghidra_list_scripts`: Script catalog.
- `ghidra_run_headless_script`: Batch script executor.
- `ghidra_do_everything`: 12-phase lifecycle attestation.

## Local API Server & Mission Control Cockpit

Start the API server on port 8771:
```bash
python ghidra_api_server.py --port 8771
```
Open `http://localhost:8771/` to interact with the 10-tab Emerald Dragon Cockpit.
