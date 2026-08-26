/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * boot.S - Early ARM64 Bootloader & Initialization Entry
 */

.section ".text.boot"
.global _start

_start:
    /* Read CPU ID (MPIDR_EL1). If secondary core, put in low-power wait */
    mrs     x0, mpidr_el1
    and     x0, x0, #0xFF
    cbz     x0, primary_cpu

secondary_cpu_wait:
    wfe
    b       secondary_cpu_wait

primary_cpu:
    /* Check Current Exception Level */
    mrs     x0, CurrentEL
    lsr     x0, x0, #2
    cmp     x0, #3
    b.eq    drop_from_el3
    cmp     x0, #2
    b.eq    drop_from_el2
    b       init_el1

drop_from_el3:
    /* Configure SCR_EL3: NS=1, RW=1 (64-bit EL2), SMD=0 */
    mov     x0, #0x5B1
    msr     scr_el3, x0
    /* Target SPSR_EL3: Return to EL2h with all interrupts masked */
    mov     x0, #0x3C9
    msr     spsr_el3, x0
    adr     x0, drop_from_el2
    msr     elr_el3, x0
    eret

drop_from_el2:
    /* Configure HCR_EL2: RW=1 (64-bit EL1) */
    mov     x0, #(1 << 31)
    msr     hcr_el2, x0
    /* Configure CNTHCTL_EL2: Allow EL1 physical timer access */
    mov     x0, #0x3
    msr     cnthctl_el2, x0
    msr     cntvoff_el2, xzr
    /* Target SPSR_EL2: Return to EL1h with interrupts masked */
    mov     x0, #0x3C5
    msr     spsr_el2, x0
    adr     x0, init_el1
    msr     elr_el2, x0
    eret

init_el1:
    /* Set up stack pointer (SP_EL1) */
    adrp    x0, _boot_stack_top
    add     x0, x0, :lo12:_boot_stack_top
    mov     sp, x0

    /* Zero out BSS section */
    adrp    x0, __bss_start
    add     x0, x0, :lo12:__bss_start
    adrp    x1, __bss_end
    add     x1, x1, :lo12:__bss_end

zero_bss:
    cmp     x0, x1
    b.ge    jump_kmain
    str     xzr, [x0], #8
    b       zero_bss

jump_kmain:
    /* Jump into C kernel main */
    bl      kmain

halt:
    wfe
    b       halt

.section ".bss.boot"
.align 12
_boot_stack_bottom:
    .space 16384 /* 16KB early boot stack */
_boot_stack_top:
