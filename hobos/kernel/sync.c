/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * sync.c - Synchronization Primitives (Mutexes and Semaphores)
 */

#include <hobos/sync.h>
#include <hobos/sched.h>

void mutex_init(mutex_t *m) {
    spin_lock_init(&m->wait_lock);
    m->locked = false;
    m->owner = 0;
}

void mutex_lock(mutex_t *m) {
    while (1) {
        spin_lock(&m->wait_lock);
        if (!m->locked) {
            m->locked = true;
            m->owner = current_task ? current_task->pid : 0;
            spin_unlock(&m->wait_lock);
            return;
        }
        spin_unlock(&m->wait_lock);
        schedule(); /* Yield CPU while waiting */
    }
}

void mutex_unlock(mutex_t *m) {
    spin_lock(&m->wait_lock);
    m->locked = false;
    m->owner = 0;
    spin_unlock(&m->wait_lock);
}
