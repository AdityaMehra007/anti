/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * vectors.S - AArch64 Exception Vector Table (VBAR_EL1)
 */

.macro save_all
    sub     sp, sp, #288
    stp     x0, x1,   [sp, #0]
    stp     x2, x3,   [sp, #16]
    stp     x4, x5,   [sp, #32]
    stp     x6, x7,   [sp, #48]
    stp     x8, x9,   [sp, #64]
    stp     x10, x11, [sp, #80]
    stp     x12, x13, [sp, #96]
    stp     x14, x15, [sp, #112]
    stp     x16, x17, [sp, #128]
    stp     x18, x19, [sp, #144]
    stp     x20, x21, [sp, #160]
    stp     x22, x23, [sp, #176]
    stp     x24, x25, [sp, #192]
    stp     x26, x27, [sp, #208]
    stp     x28, x29, [sp, #224]
    
    mrs     x21, sp_el0
    str     x30,      [sp, #240]
    str     x21,      [sp, #248]
    
    mrs     x22, elr_el1
    mrs     x23, spsr_el1
    mrs     x24, esr_el1
    mrs     x25, far_el1
    
    stp     x22, x23, [sp, #256]
    stp     x24, x25, [sp, #272]
.endm

.macro restore_all
    ldp     x22, x23, [sp, #256]
    ldp     x24, x25, [sp, #272]
    
    msr     elr_el1, x22
    msr     spsr_el1, x23
    
    ldr     x30,      [sp, #240]
    ldr     x21,      [sp, #248]
    msr     sp_el0, x21
    
    ldp     x0, x1,   [sp, #0]
    ldp     x2, x3,   [sp, #16]
    ldp     x4, x5,   [sp, #32]
    ldp     x6, x7,   [sp, #48]
    ldp     x8, x9,   [sp, #64]
    ldp     x10, x11, [sp, #80]
    ldp     x12, x13, [sp, #96]
    ldp     x14, x15, [sp, #112]
    ldp     x16, x17, [sp, #128]
    ldp     x18, x19, [sp, #144]
    ldp     x20, x21, [sp, #160]
    ldp     x22, x23, [sp, #176]
    ldp     x24, x25, [sp, #192]
    ldp     x26, x27, [sp, #208]
    ldp     x28, x29, [sp, #224]
    add     sp, sp, #288
.endm

.macro ventry label
    .align 7
    b \label
.endm

.section ".text.vectors"
.align 11
.global vector_table_el1

vector_table_el1:
    /* Current EL with SP0 */
    ventry el1_sp0_sync
    ventry el1_sp0_irq
    ventry el1_sp0_fiq
    ventry el1_sp0_serror

    /* Current EL with SPx */
    ventry el1_spx_sync
    ventry el1_spx_irq
    ventry el1_spx_fiq
    ventry el1_spx_serror

    /* Lower EL using AArch64 (Userspace EL0) */
    ventry el0_64_sync
    ventry el0_64_irq
    ventry el0_64_fiq
    ventry el0_64_serror

    /* Lower EL using AArch32 */
    ventry el0_32_sync
    ventry el0_32_irq
    ventry el0_32_fiq
    ventry el0_32_serror

el1_sp0_sync:
el1_sp0_irq:
el1_sp0_fiq:
el1_sp0_serror:
el1_spx_fiq:
el1_spx_serror:
el0_64_fiq:
el0_64_serror:
el0_32_sync:
el0_32_irq:
el0_32_fiq:
el0_32_serror:
    save_all
    mov     x0, sp
    bl      unhandled_exception
    restore_all
    eret

el1_spx_sync:
    save_all
    mov     x0, sp
    bl      handle_kernel_sync_exception
    restore_all
    eret

el1_spx_irq:
el0_64_irq:
    save_all
    mov     x0, sp
    bl      gic_handle_irq
    restore_all
    eret

el0_64_sync:
    save_all
    mov     x0, sp
    mrs     x1, esr_el1
    lsr     x2, x1, #26 /* EC field */
    cmp     x2, #0x15   /* EC = 0x15 -> SVC instruction from AArch64 */
    b.eq    invoke_syscall
    bl      handle_user_sync_exception
    restore_all
    eret

invoke_syscall:
    bl      handle_syscall
    restore_all
    eret
