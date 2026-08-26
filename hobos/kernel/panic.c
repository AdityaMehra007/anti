/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * panic.c - Kernel Panic and Diagnostic Dump
 */

#include <hobos/kernel.h>
#include <hobos/uart.h>
#include <stdarg.h>

void panic(const char *fmt, ...) {
    va_list args;
    printk("\n==================== [ KERNEL PANIC ] ====================\n");
    va_start(args, fmt);
    vprintk(fmt, args);
    va_end(args);
    printk("==========================================================\n");
    printk("CPU Execution Halted.\n");

    while (1) {
        asm volatile("wfi");
    }
}

void unhandled_exception(uint64_t *sp) {
    uint64_t elr, spsr, esr, far;
    asm volatile("mrs %0, elr_el1" : "=r"(elr));
    asm volatile("mrs %0, spsr_el1" : "=r"(spsr));
    asm volatile("mrs %0, esr_el1" : "=r"(esr));
    asm volatile("mrs %0, far_el1" : "=r"(far));

    panic("Unhandled AArch64 Exception!\n"
          "  ESR_EL1: 0x%lx (EC: 0x%x, ISS: 0x%x)\n"
          "  ELR_EL1: 0x%lx (Faulting PC)\n"
          "  FAR_EL1: 0x%lx (Faulting Address)\n"
          "  SPSR_EL1: 0x%lx\n"
          "  Stack Pointer: 0x%lx\n",
          esr, (uint32_t)(esr >> 26), (uint32_t)(esr & 0x1FFFFFF),
          elr, far, spsr, (uint64_t)sp);
}

void handle_kernel_sync_exception(uint64_t *sp) {
    unhandled_exception(sp);
}

void handle_user_sync_exception(uint64_t *sp) {
    printk("[USER_FAULT] User process triggered synchronous fault.\n");
    unhandled_exception(sp);
}
