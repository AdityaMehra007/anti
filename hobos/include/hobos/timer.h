/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * timer.h - ARM Generic Physical Timer (CNTP_TVAL_EL0, CNTP_CTL_EL0)
 */

#ifndef _HOBOS_TIMER_H_
#define _HOBOS_TIMER_H_

#include <hobos/types.h>

#define HZ 100 /* 100Hz scheduler tick (10ms) */

void timer_init(void);
void timer_handler(uint32_t irq, void *data);
uint64_t timer_get_ticks(void);
void timer_sleep_ms(uint64_t ms);

#endif /* _HOBOS_TIMER_H_ */
