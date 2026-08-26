# 📦 HobOS — Complete Project Inventory (Phase 0)

**Architecture:** ARMv8-A (AArch64)  
**Target Board:** QEMU `virt` Platform (`-M virt -cpu cortex-a53`)  
**Maturity Status:** Functional Research Kernel Baseline  

---

## 1. Directory Structure

```
hobos/
├── arch/aarch64/      # Architecture-specific assembly, vectors, MMU, GIC, timer
│   ├── boot.S         # Reset vector, EL3/EL2 -> EL1 drop, BSS zeroing, stack setup
│   ├── vectors.S      # 16-entry VBAR_EL1 exception table (sync, irq, fiq, serror)
│   ├── context.S      # Callee-saved context switch (cpu_switch_to)
│   ├── mmu.c          # 4-level page tables, TCR_EL1, MAIR_EL1, TTBR0/1_EL1
│   ├── gic.c          # GICv2 distributor & CPU interface management
│   ├── timer.c        # Architectural physical timer (CNTP_TVAL_EL0)
│   └── asm_utils.h    # Inline assembly system register accessors
├── kernel/            # Architecture-independent kernel core
│   ├── main.c         # kmain entry, subsystem init sequence
│   ├── printk.c       # Formatted string output (%s, %d, %x, %lx, %p)
│   ├── panic.c        # Kernel panic, register dump, stack trace
│   ├── task.c         # Process Control Block (PCB) allocation & management
│   ├── sched.c        # Preemptive priority round-robin scheduler
│   ├── syscall.c      # Syscall ABI dispatch table & user memory safety checks
│   └── sync.c         # Spinlocks, mutexes, atomic operations
├── mm/                # Memory Management
│   ├── buddy.c        # Physical page buddy allocator (orders 0..10)
│   └── slab.c         # Object cache allocator (kmalloc/kfree 16B..2048B)
├── drivers/           # Peripheral drivers
│   └── uart_pl011.c   # PrimeCell PL011 UART serial driver
├── fs/                # Filesystem layer
│   └── vfs.c          # Virtual File System abstraction & file descriptors
├── include/hobos/     # Public kernel headers (types, mm, sched, gic, uart, etc.)
├── tests/             # Automated unit & integration verification harnesses
├── Makefile           # Cross-compilation Makefile (aarch64-linux-gnu-gcc)
└── linker.ld          # Linker script placing kernel at 0x40080000
```

---

## 2. Component Dependency Map

```
                  ┌──────────────┐
                  │    boot.S    │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   kernel/    │
                  │    main.c    │
                  └──────┬───────┘
     ┌───────────┬───────┼───────────┬───────────┐
     ▼           ▼       ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│uart_pl  │ │  mmu.c  │ │ gic.c   │ │ buddy.c │ │ sched.c │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

