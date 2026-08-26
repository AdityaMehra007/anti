/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * timer.c - ARM Generic Architectural Physical Timer
 */

#include <hobos/timer.h>
#include <hobos/gic.h>
#include <hobos/sched.h>
#include <hobos/kernel.h>
#include "asm_utils.h"

static volatile uint64_t system_ticks = 0;
static uint32_t timer_frequency = 0;

static inline uint32_t get_cntfrq(void) {
    uint32_t frq;
    asm volatile("mrs %0, cntfrq_el0" : "=r"(frq));
    return frq;
}

static inline void set_cntp_tval(uint32_t tval) {
    asm volatile("msr cntp_tval_el0, %0" :: "r"(tval) : "memory");
}

static inline void set_cntp_ctl(uint32_t ctl) {
    asm volatile("msr cntp_ctl_el0, %0" :: "r"(ctl) : "memory");
}

void timer_handler(uint32_t irq, void *data) {
    (void)irq;
    (void)data;
    
    system_ticks++;
    
    /* Re-arm timer for next tick interval (1/HZ sec) */
    set_cntp_tval(timer_frequency / HZ);

    /* Trigger scheduler tick */
    sched_tick();
}

void timer_init(void) {
    timer_frequency = get_cntfrq();
    printk("[TIMER] ARM Generic Timer Frequency: %u Hz (Tick Rate: %d Hz)\n", timer_frequency, HZ);

    /* Register timer IRQ 27 */
    register_irq_handler(IRQ_ARCH_TIMER, timer_handler, NULL);

    /* Set first interval and enable timer: IMASK=0, ENABLE=1 */
    set_cntp_tval(timer_frequency / HZ);
    set_cntp_ctl(1);

    printk("[TIMER] Architectural Physical Timer Started.\n");
}

uint64_t timer_get_ticks(void) {
    return system_ticks;
}

void timer_sleep_ms(uint64_t ms) {
    uint64_t target = system_ticks + (ms * HZ / 1000);
    while (system_ticks < target) {
        asm volatile("wfi");
    }
}
