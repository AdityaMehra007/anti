#!/usr/bin/env python3
"""
NSA Ghidra Universal CLI
========================
Command-Line Interface for NSA Ghidra Autonomous Software Reverse Engineering Suite.

Usage:
    python ghidra_cli.py info
    python ghidra_cli.py analyze <binary_path> [--json]
    python ghidra_cli.py disasm <binary_path> [--addr ADDR] [--count N]
    python ghidra_cli.py decompile <binary_path> [--func NAME]
    python ghidra_cli.py pcode <binary_path> [--count N]
    python ghidra_cli.py strings <binary_path> [--min-len N] [--filter CAT]
    python ghidra_cli.py sections <binary_path>
    python ghidra_cli.py functions <binary_path>
    python ghidra_cli.py vulns <binary_path>
    python ghidra_cli.py entropy <binary_path>
    python ghidra_cli.py rop <binary_path>
    python ghidra_cli.py scripts
    python ghidra_cli.py run-script <script_path> <binary_path>
    python ghidra_cli.py do-everything [--binary PATH]
"""

import sys
import json
import argparse
import os
from ghidra_orchestrator import (
    GhidraConfig,
    GhidraOrchestrator,
    BinaryDissector
)


def print_banner():
    banner = r"""
  ____  _     _     _             ____  ____  _____ 
 / ___|| |__ (_) __| |_ __ __ _  / ___||  _ \| ____|
| |  _ | '_ \| |/ _` | '__/ _` | \___ \| |_) |  _|  
| |_| || | | | | (_| | | | (_| |  ___) |  _ <| |___ 
 \____||_| |_|_|\__,_|_|  \__,_| |____/|_| \_\_____|
   NSA SOFTWARE REVERSE ENGINEERING AUTONOMOUS SUITE
    """
    print(banner)


def cmd_info(args, orch: GhidraOrchestrator):
    info = orch.get_info()
    if args.json:
        print(json.dumps(info, indent=2))
        return
    print("\n[+] NSA Ghidra SRE Engine Telemetry:")
    print(f"  • Suite Name:       {info['name']}")
    print(f"  • Version:          {info['version']}")
    print(f"  • Upstream:         {info['upstream']}")
    print(f"  • Engine Mode:      {info['engine_mode']}")
    print(f"  • Decompiler:       {info['decompiler_version']}")
    print(f"  • P-Code Opcodes:   {info['pcode_operations_count']}")
    print("\n[+] Sleigh Target Architectures:")
    for proc in info["supported_processors"]:
        print(f"  - {proc['name']:<24} {proc['bits']}-bit | {proc['endian']:<6} | {proc['desc']}")
    print()


def cmd_analyze(args, orch: GhidraOrchestrator):
    path = args.binary
    if not os.path.exists(path):
        print(f"[-] Error: Binary not found at '{path}'")
        sys.exit(1)

    print(f"\n[*] Dissecting binary: {path}")
    report = orch.analyze_binary(path)

    if args.json:
        # Convert dataclass report to dict
        import dataclasses
        print(json.dumps(dataclasses.asdict(report), indent=2))
        return

    meta = report.metadata
    print("\n[+] Binary Header & Architecture Telemetry:")
    print(f"  • Format:           {meta.format} ({meta.architecture})")
    print(f"  • Endianness:       {meta.endianness}")
    print(f"  • File Size:        {meta.file_size_bytes:,} bytes")
    print(f"  • Entry Point:      0x{meta.entry_point_va:08x} (RVA: 0x{meta.entry_point_rva:08x})")
    print(f"  • Image Base:       0x{meta.image_base:08x}")
    print(f"  • Subsystem:        {meta.subsystem}")
    print(f"  • SHA-256:          {meta.hashes.get('sha256', '')}")

    print("\n[+] Exploit Mitigations Checklist:")
    mit = report.mitigations
    print(f"  • ASLR:             {'ENABLED' if mit.aslr else 'DISABLED'}")
    print(f"  • DEP / NX:         {'ENABLED' if mit.dep_nx else 'DISABLED'}")
    print(f"  • Stack Canary:     {'ENABLED' if mit.stack_canary else 'DISABLED'}")
    print(f"  • SafeSEH:          {'ENABLED' if mit.safe_seh else 'DISABLED'}")
    print(f"  • ControlFlowGuard: {'ENABLED' if mit.control_flow_guard else 'DISABLED'}")
    print(f"  • Security Score:   {mit.score_out_of_100}/100")

    print("\n[+] Memory Sections:")
    for sec in report.sections:
        warn = " [SUSPICIOUS/PACKED]" if sec.is_suspicious_or_packed else ""
        print(f"  - {sec.name:<10} VA: 0x{sec.virtual_address:08x} | Size: {sec.virtual_size:>7} | Entropy: {sec.entropy:>4.2f}/8.0 | {sec.characteristics_flags}{warn}")

    print(f"\n[+] Identified Functions: {len(report.functions)}")
    for fn in report.functions[:5]:
        print(f"  - {fn.name:<30} 0x{fn.address:08x} ({fn.calling_convention}) -> {fn.return_type}")

    print(f"\n[+] Vulnerabilities & Flaws Detected: {len(report.vulnerabilities)}")
    for v in report.vulnerabilities[:4]:
        print(f"  - [{v.severity}] {v.title} @ 0x{v.address:08x}")
        print(f"      Description: {v.description}")
        print(f"      Remedy:      {v.mitigation_remedy}")

    print(f"\n[+] Packer Analysis: {report.packer_detection['verdict']}")
    print(f"[*] Complete analysis completed in {report.analysis_time_seconds}s\n")


def cmd_disasm(args, orch: GhidraOrchestrator):
    path = args.binary
    addr = int(args.addr, 16) if args.addr else None
    count = args.count or 20

    instructions = orch.disassemble(path, address=addr, count=count)
    print(f"\n[+] Sleigh Instruction Disassembly ({path}):")
    print(f"{'Address':<12} {'Raw Bytes':<12} {'Instruction':<24} {'P-Code Micro-Operation'}")
    print("-" * 75)
    for i in instructions:
        pcode_repr = i.pcode_ops[0].to_string() if i.pcode_ops else ""
        print(f"0x{i.address:08x}   {i.raw_bytes_hex:<10}  {i.mnemonic} {i.operands:<16}  {pcode_repr}")
    print()


def cmd_decompile(args, orch: GhidraOrchestrator):
    path = args.binary
    func_name = args.func or "main"
    decomp = orch.decompile_function(path, func_name)
    print(f"\n[+] Ghidra Decompiler Output for '{func_name}':")
    print("-" * 65)
    print(decomp.pseudo_c_code)
    print("-" * 65)
    print(f"[+] Recovered Types: {decomp.recovered_types}\n")


def cmd_pcode(args, orch: GhidraOrchestrator):
    path = args.binary
    count = args.count or 25
    pcode_ops = orch.get_pcode(path, count=count)
    print(f"\n[+] Ghidra P-Code Intermediate Representation ({len(pcode_ops)} ops):")
    for op in pcode_ops:
        print(f"  {op['pcode_disassembly']}  [{op['instruction']}]")
    print()


def cmd_strings(args, orch: GhidraOrchestrator):
    path = args.binary
    min_len = args.min_len or 4
    cat_filter = args.filter
    strings = orch.extract_strings(path, min_len=min_len, category_filter=cat_filter)
    print(f"\n[+] Extracted Strings ({len(strings)} entries):")
    for s in strings[:40]:
        print(f"  0x{s.address:08x} [{s.encoding}] [{s.category:<14}] {s.value}")
    print()


def cmd_sections(args, orch: GhidraOrchestrator):
    path = args.binary
    report = orch.analyze_binary(path)
    print(f"\n[+] Memory Map & Sections for {os.path.basename(path)}:")
    print(f"{'Name':<10} {'Virtual Addr':<14} {'Virt Size':<10} {'Raw Offset':<12} {'Raw Size':<10} {'Entropy':<8} {'Flags'}")
    print("-" * 80)
    for s in report.sections:
        print(f"{s.name:<10} 0x{s.virtual_address:08x}     {s.virtual_size:<10} 0x{s.raw_offset:08x}   {s.raw_size:<10} {s.entropy:<8.2f} {s.characteristics_flags}")
    print()


def cmd_functions(args, orch: GhidraOrchestrator):
    path = args.binary
    report = orch.analyze_binary(path)
    print(f"\n[+] Dissected Functions in {os.path.basename(path)} ({len(report.functions)} total):")
    print(f"{'Function Name':<30} {'Address':<14} {'Convention':<12} {'Return':<10} {'Complexity':<10}")
    print("-" * 80)
    for fn in report.functions:
        print(f"{fn.name:<30} 0x{fn.address:08x}     {fn.calling_convention:<12} {fn.return_type:<10} {fn.cyclomatic_complexity:<10}")
    print()


def cmd_vulns(args, orch: GhidraOrchestrator):
    path = args.binary
    audit = orch.audit_vulnerabilities(path)
    print(f"\n[+] SRE Vulnerability & Mitigation Audit: {audit['binary']}")
    print(f"  • Exploit Mitigations Security Score: {audit['mitigations_score']}/100")
    print(f"  • Security Findings: {audit['findings_count']}")
    for f in audit["findings"]:
        print(f"\n  [{f['severity']}] {f['rule_id']}: {f['title']}")
        print(f"    Target:      {f['function']} @ 0x{f['address']:08x}")
        print(f"    Evidence:    {f['evidence']}")
        print(f"    Remedy:      {f['mitigation_remedy']}")
    print()


def cmd_entropy(args, orch: GhidraOrchestrator):
    path = args.binary
    with open(path, "rb") as f:
        data = f.read()
    ent = BinaryDissector.calculate_entropy(data)
    print(f"\n[+] Shannon Entropy Analysis: {os.path.basename(path)}")
    print(f"  • Overall Entropy: {ent:.4f} / 8.0 bits per byte")
    bars = int(ent * 5)
    print(f"  • Density:         [{'#' * bars}{'.' * (40 - bars)}] ({int((ent / 8.0) * 100)}%)")
    if ent > 7.1:
        print("  • Assessment:      PACKED / ENCRYPTED / COMPRESSED PAYLOAD DETECTED")
    else:
        print("  • Assessment:      NORMAL NATIVE EXECUTABLE / LOW ENTROPY CODE")
    print()


def cmd_rop(args, orch: GhidraOrchestrator):
    path = args.binary
    report = orch.analyze_binary(path)
    print(f"\n[+] Return-Oriented Programming (ROP) Gadgets ({len(report.rop_gadgets)} found):")
    for g in report.rop_gadgets:
        gadget_str = " ; ".join(g.instructions)
        print(f"  0x{g.address:08x} [{g.raw_bytes:<8}] [{g.classification:<12}] {gadget_str}")
    print()


def cmd_scripts(args, orch: GhidraOrchestrator):
    scripts_dir = os.path.abspath("ghidra/scripts")
    print("\n[+] Registered Ghidra SRE Scripts:")
    if os.path.exists(scripts_dir):
        files = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
        for f in files:
            print(f"  - {f}")
    else:
        print("  (No script files found in ghidra/scripts)")
    print()


def cmd_run_script(args, orch: GhidraOrchestrator):
    res = orch.run_script(args.script, args.binary)
    print("\n[+] Script Execution Result:")
    print(json.dumps(res, indent=2))
    print()


def cmd_do_everything(args, orch: GhidraOrchestrator):
    print("\n[*] Initiating OMEGA Sovereign 12-Phase NSA Ghidra Lifecycle...\n")
    res = orch.do_everything(args.binary)
    print("\n" + "=" * 70)
    print(f"STATUS: {res['overall_status']}")
    print(f"Execution ID:    {res['execution_id']}")
    print(f"Total Phases:    {res['total_phases_executed']}/12 PASSED")
    print(f"Elapsed Time:    {res['total_elapsed_seconds']}s")
    print("=" * 70)
    print("\nPhase Summary:")
    for p in res["phases"]:
        print(f"  Phase {p['phase']:>2}: {p['name']:<55} [{p['status']}] ({p['elapsed_seconds']}s)")
    print(f"\nAttestation manifest persisted at: omega/data/ghidra_do_everything_manifest.json\n")


def main():
    parser = argparse.ArgumentParser(description="NSA Ghidra Universal CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    # info
    p_info = subparsers.add_parser("info", help="Display Ghidra engine details")
    p_info.add_argument("--json", action="store_true", help="Output in JSON format")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Dissect binary and run full SRE analysis")
    p_analyze.add_argument("binary", help="Path to binary executable")
    p_analyze.add_argument("--json", action="store_true", help="Output in JSON format")

    # disasm
    p_disasm = subparsers.add_parser("disasm", help="Disassemble binary instructions")
    p_disasm.add_argument("binary", help="Path to binary executable")
    p_disasm.add_argument("--addr", help="Start address in hex (e.g. 0x140001000)")
    p_disasm.add_argument("--count", type=int, default=20, help="Number of instructions")

    # decompile
    p_decomp = subparsers.add_parser("decompile", help="Decompile function to pseudo-C")
    p_decomp.add_argument("binary", help="Path to binary executable")
    p_decomp.add_argument("--func", default="main", help="Function name or address")

    # pcode
    p_pcode = subparsers.add_parser("pcode", help="Extract Ghidra P-Code microcode")
    p_pcode.add_argument("binary", help="Path to binary executable")
    p_pcode.add_argument("--count", type=int, default=25, help="Number of P-Code ops")

    # strings
    p_strings = subparsers.add_parser("strings", help="Extract strings and IOCs")
    p_strings.add_argument("binary", help="Path to binary executable")
    p_strings.add_argument("--min-len", type=int, default=4, help="Minimum string length")
    p_strings.add_argument("--filter", help="Filter by category (URL, IP_Address, FilePath, etc.)")

    # sections
    p_sections = subparsers.add_parser("sections", help="Inspect memory sections & entropy")
    p_sections.add_argument("binary", help="Path to binary executable")

    # functions
    p_funcs = subparsers.add_parser("functions", help="List identified functions")
    p_funcs.add_argument("binary", help="Path to binary executable")

    # vulns
    p_vulns = subparsers.add_parser("vulns", help="Audit vulnerabilities and mitigations")
    p_vulns.add_argument("binary", help="Path to binary executable")

    # entropy
    p_ent = subparsers.add_parser("entropy", help="Calculate Shannon entropy")
    p_ent.add_argument("binary", help="Path to binary executable")

    # rop
    p_rop = subparsers.add_parser("rop", help="Extract ROP gadgets")
    p_rop.add_argument("binary", help="Path to binary executable")

    # scripts
    subparsers.add_parser("scripts", help="List available SRE analysis scripts")

    # run-script
    p_run = subparsers.add_parser("run-script", help="Run Ghidra SRE script")
    p_run.add_argument("script", help="Path to script")
    p_run.add_argument("binary", help="Path to binary")

    # do-everything
    p_do = subparsers.add_parser("do-everything", help="Run the master 12-phase sovereign lifecycle")
    p_do.add_argument("--binary", help="Optional path to target binary")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    orch = GhidraOrchestrator()

    commands = {
        "info": cmd_info,
        "analyze": cmd_analyze,
        "disasm": cmd_disasm,
        "decompile": cmd_decompile,
        "pcode": cmd_pcode,
        "strings": cmd_strings,
        "sections": cmd_sections,
        "functions": cmd_functions,
        "vulns": cmd_vulns,
        "entropy": cmd_entropy,
        "rop": cmd_rop,
        "scripts": cmd_scripts,
        "run-script": cmd_run_script,
        "do-everything": cmd_do_everything
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args, orch)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
