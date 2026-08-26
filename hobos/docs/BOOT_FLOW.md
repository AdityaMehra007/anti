# 🚀 HobOS Boot Flow Analysis (Phase 3)

## Entry Point: `_start` in `arch/aarch64/boot.S`

```
Address: 0x40080000
Registers at Entry:
  x0: Device Tree Blob (DTB) physical address (passed by QEMU)
  x1-x3: Reserved (0)
  PSTATE: EL3 or EL2 (QEMU default)

Execution Sequence:
1. Core Filter: mpidr_el1 & 0xFF. Core 0 proceeds; cores 1-3 enter wfe loop.
2. EL Check: Checks CurrentEL.
   - If EL3: Sets scr_el3 = 0x5B1, spsr_el3 = 0x3C9, elr_el3 = drop_from_el2; eret.
   - If EL2: Sets hcr_el2 = (1<<31), cnthctl_el2 = 3, spsr_el2 = 0x3C5, elr_el2 = init_el1; eret.
3. Stack Setup: sp = _boot_stack_top (16KB stack in .bss.boot).
4. BSS Clear: Zeros memory from __bss_start to __bss_end.
5. C Entry: Calls kmain().
```

