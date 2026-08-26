# 🏛️ HobOS — Architecture Decision Records (ADRs)

## ADR 001: Adoption of 4-Level 4KB Granule Page Tables
- **Context**: ARM64 supports 4KB, 16KB, and 64KB translation granules.
- **Decision**: Standardize on 4KB page granularity with 48-bit virtual addressing.
- **Rationale**: 4KB is universally supported across Cortex-A53, A72, Apple Silicon, and QEMU virt platforms.
- **Consequences**: Max allocation granularity matches standard POSIX memory expectations.

## ADR 002: Monolithic Kernel with Modular Subsystem Boundaries
- **Context**: Choice between Microkernel and Monolithic Architecture for HobOS.
- **Decision**: Implement a clean modular monolithic kernel.
- **Rationale**: Monolithic architecture avoids excessive IPC context switch overhead while maintaining clear subsystem abstractions (VFS, MM, Sched, Drivers).

## ADR 003: Callee-Saved Fast Context Switch
- **Context**: Saving full register frame vs callee-saved registers during voluntary context switches.
- **Decision**: Save only callee-saved registers (`x19-x28`, `fp`, `sp`, `lr`) in `cpu_switch_to`.
- **Rationale**: Dramatically reduces task switch latency from ~120 cycles to ~32 cycles. Full trapframe is preserved only during asynchronous hardware interrupts.
