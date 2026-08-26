/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * kernel.h - Core kernel definitions, macros, and formatted output
 */

#ifndef _HOBOS_KERNEL_H_
#define _HOBOS_KERNEL_H_

#include <hobos/types.h>

#define KERNEL_NAME    "HobOS"
#define KERNEL_VERSION "1.0.0-ARM64"

#define ALIGN_UP(x, align)   (((x) + ((align) - 1)) & ~((align) - 1))
#define ALIGN_DOWN(x, align) ((x) & ~((align) - 1))

#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

/* Physical / Virtual Layout on QEMU virt board */
#define DRAM_BASE       0x40000000ULL
#define DRAM_SIZE       0x40000000ULL /* 1GB default */
#define KERNEL_VIRT_BASE 0xFFFF000000000000ULL
#define KERNEL_PHYS_BASE 0x40080000ULL

/* Function prototypes */
void printk(const char *fmt, ...);
void panic(const char *fmt, ...) __attribute__((noreturn));

#define assert(expr) \
    do { \
        if (!(expr)) { \
            panic("Assertion failed: %s at %s:%d\n", #expr, __FILE__, __LINE__); \
        } \
    } while (0)

static inline void dsb_sy(void) {
    asm volatile("dsb sy" ::: "memory");
}

static inline void dsb_ish(void) {
    asm volatile("dsb ish" ::: "memory");
}

static inline void isb(void) {
    asm volatile("isb" ::: "memory");
}

#endif /* _HOBOS_KERNEL_H_ */
