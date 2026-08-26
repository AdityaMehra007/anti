# 🔬 ARM64 / AArch64 Deep Dive Specification (Phase 2)

## 1. Exception Levels & State Machine
- **EL0**: Unprivileged userspace application execution.
- **EL1**: Privileged OS kernel execution (HobOS core).
- **EL2**: Hypervisor virtualization layer.
- **EL3**: Secure Monitor / TrustZone layer.

## 2. System Registers Managed
- `CurrentEL`: Evaluates boot privilege level (`(CurrentEL >> 2) & 3`).
- `SCTLR_EL1`: System Control Register controlling MMU (`M`), Data Cache (`C`), Instruction Cache (`I`).
- `TCR_EL1`: Translation Control Register setting translation table size (T0SZ=16 for 48-bit VA), page granule (TG0=4KB), and memory shareability.
- `MAIR_EL1`: Memory Attribute Indirection Register defining Device-nGnRnE (0x00) and Normal Write-Back (0xFF).
- `TTBR0_EL1` / `TTBR1_EL1`: Translation Table Base Registers for user and kernel halves.
- `VBAR_EL1`: Vector Base Address Register pointing to 2048-byte aligned exception vectors.

