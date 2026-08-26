# 🏛️ HobOS Architecture Master Specification (Phase 1)

## Complete Boot-to-Userspace Lifecycle

```
POWER / RESET ON QEMU VIRT
          │
          ▼
   CPU RESET STATE (0x40080000)
          │
          ▼
   BOOT CODE (arch/aarch64/boot.S)
   - Read MPIDR_EL1 (Primary CPU vs Secondary Cores)
          │
          ▼
   EL INITIALIZATION
   - Check CurrentEL: If EL3 -> drop to EL2 -> drop to EL1h
   - Configure SCR_EL3, SPSR_EL3, HCR_EL2, SPSR_EL2
          │
          ▼
   STACK & BSS INITIALIZATION
   - Load SP_EL1 with _boot_stack_top (16KB)
   - Zero .bss section (__bss_start to __bss_end)
          │
          ▼
   EARLY CONSOLE (drivers/uart_pl011.c)
   - Configure IBRD=13, FBRD=1 (115200 baud at 24MHz)
   - Print HobOS banner & version
          │
          ▼
   EXCEPTION VECTOR BASE (VBAR_EL1)
   - Load vector_table_el1 into VBAR_EL1
          │
          ▼
   PHYSICAL MEMORY DISCOVERY & BUDDY (mm/buddy.c)
   - Manage 128MB DRAM in power-of-two page orders (0..10)
          │
          ▼
   SLAB OBJECT CACHE (mm/slab.c)
   - Initialize 16B to 2048B caches for kmalloc
          │
          ▼
   HARDWARE MMU & 4-LEVEL PAGE TABLES (arch/aarch64/mmu.c)
   - Setup MAIR_EL1 (Device, Normal-NC, Normal-WB)
   - Setup TCR_EL1 (48-bit VA, 4KB page granule)
   - Enable MMU, D-Cache, I-Cache in SCTLR_EL1
          │
          ▼
   INTERRUPT CONTROLLER (arch/aarch64/gic.c)
   - Configure GICv2 Distributor & CPU Interface
          │
          ▼
   ARCHITECTURAL TIMER (arch/aarch64/timer.c)
   - Read CNTFRQ_EL0, program CNTP_TVAL_EL0 for 100Hz tick
          │
          ▼
   PREEMPTIVE SCHEDULER (kernel/sched.c)
   - Initialize runqueue, idle task, PCB tables
          │
          ▼
   VFS & SYSCALL INTERFACE (kernel/syscall.c, fs/vfs.c)
   - Register SYS_YIELD, SYS_EXIT, SYS_WRITE, SYS_GETPID
          │
          ▼
   USERSPACE INIT PROCESS (PID 1)
   - Transition to EL0 with isolated stack and trapframe
   - Execute user shell via SVC #0
```

