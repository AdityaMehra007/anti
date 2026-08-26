/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * sync.h - Spinlocks, Mutexes, and Atomic Operations
 */

#ifndef _HOBOS_SYNC_H_
#define _HOBOS_SYNC_H_

#include <hobos/types.h>

typedef struct {
    volatile uint32_t lock;
} spinlock_t;

#define SPINLOCK_INIT { 0 }

static inline void spin_lock_init(spinlock_t *lock) {
    lock->lock = 0;
}

static inline void spin_lock(spinlock_t *lock) {
    uint32_t tmp;
    asm volatile(
        "1: ldaxr %w0, [%1]\n"
        "   cbnz  %w0, 1b\n"
        "   stxr  %w0, %w2, [%1]\n"
        "   cbnz  %w0, 1b\n"
        : "=&r"(tmp)
        : "r"(&lock->lock), "r"(1)
        : "memory"
    );
}

static inline void spin_unlock(spinlock_t *lock) {
    asm volatile(
        "stlr wzr, [%0]\n"
        :
        : "r"(&lock->lock)
        : "memory"
    );
}

typedef struct {
    spinlock_t wait_lock;
    bool locked;
    pid_t owner;
} mutex_t;

#define MUTEX_INIT { SPINLOCK_INIT, false, 0 }

void mutex_init(mutex_t *m);
void mutex_lock(mutex_t *m);
void mutex_unlock(mutex_t *m);

#endif /* _HOBOS_SYNC_H_ */
