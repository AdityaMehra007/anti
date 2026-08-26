# 💳 HobOS — Technical Debt & Architectural Backlog

## 1. Identified Backlog Items
1. **Secondary CPU Wakeup**: `arch/aarch64/boot.S` currently places secondary CPUs in a `wfe` loop. Need PSCI `CPU_ON` firmware call implementation.
2. **Dynamic Page Table Deallocation**: `mm/mmu.c` allocates L1/L2/L3 page tables on demand but does not yet reclaim empty intermediate page tables on unmap.
3. **Signal Handling**: Syscall interface does not yet implement POSIX signals (`SIGINT`, `SIGTERM`, `SIGSEGV`).
4. **Demand Paging**: Virtual memory currently maps memory eagerly rather than faulting in pages on demand via data aborts.

## 2. Remediation Priority
- Priority 1: Per-process `TTBR0_EL1` address space separation.
- Priority 2: VirtIO-Block device support for persistent storage.
- Priority 3: PSCI SMP multicore initialization.
