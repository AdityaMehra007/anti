/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * asm_utils.h - AArch64 System Register Accessors and Assembly Helpers
 */

#ifndef _HOBOS_ASM_UTILS_H_
#define _HOBOS_ASM_UTILS_H_

#include <hobos/types.h>

static inline uint32_t get_current_el(void) {
    uint64_t el;
    asm volatile("mrs %0, CurrentEL" : "=r"(el));
    return (uint32_t)((el >> 2) & 3);
}

static inline void set_vbar_el1(uint64_t vbar) {
    asm volatile("msr vbar_el1, %0" :: "r"(vbar) : "memory");
}

static inline void set_ttbr0_el1(uint64_t ttbr0) {
    asm volatile("msr ttbr0_el1, %0" :: "r"(ttbr0) : "memory");
}

static inline void set_ttbr1_el1(uint64_t ttbr1) {
    asm volatile("msr ttbr1_el1, %0" :: "r"(ttbr1) : "memory");
}

static inline void set_tcr_el1(uint64_t tcr) {
    asm volatile("msr tcr_el1, %0" :: "r"(tcr) : "memory");
}

static inline void set_mair_el1(uint64_t mair) {
    asm volatile("msr mair_el1, %0" :: "r"(mair) : "memory");
}

static inline uint64_t get_sctlr_el1(void) {
    uint64_t sctlr;
    asm volatile("mrs %0, sctlr_el1" : "=r"(sctlr));
    return sctlr;
}

static inline void set_sctlr_el1(uint64_t sctlr) {
    asm volatile("msr sctlr_el1, %0" :: "r"(sctlr) : "memory");
}

static inline void flush_tlb_all(void) {
    asm volatile("dsb ish\n tlbi vmalle1is\n dsb ish\n isb" ::: "memory");
}

static inline void enable_irq(void) {
    asm volatile("msr daifclr, #2" ::: "memory");
}

static inline void disable_irq(void) {
    asm volatile("msr daifset, #2" ::: "memory");
}

#endif /* _HOBOS_ASM_UTILS_H_ */
