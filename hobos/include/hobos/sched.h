/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * sched.h - Process Control Block (PCB), task context, and scheduler
 */

#ifndef _HOBOS_SCHED_H_
#define _HOBOS_SCHED_H_

#include <hobos/types.h>
#include <hobos/list.h>

#define KERNEL_STACK_SIZE 16384 /* 16KB kernel stack */
#define MAX_TASKS         256

typedef enum {
    TASK_STATE_UNUSED = 0,
    TASK_STATE_READY,
    TASK_STATE_RUNNING,
    TASK_STATE_BLOCKED,
    TASK_STATE_ZOMBIE
} task_state_t;

/* Callee-saved registers preserved across cpu_switch_to */
struct cpu_context {
    uint64_t x19;
    uint64_t x20;
    uint64_t x21;
    uint64_t x22;
    uint64_t x23;
    uint64_t x24;
    uint64_t x25;
    uint64_t x26;
    uint64_t x27;
    uint64_t x28;
    uint64_t fp; /* x29 */
    uint64_t sp;
    uint64_t pc; /* x30 / lr */
};

/* Complete user/kernel trap frame saved on exception entry */
struct trap_frame {
    uint64_t x[31];
    uint64_t sp;
    uint64_t elr_el1;
    uint64_t spsr_el1;
    uint64_t esr_el1;
    uint64_t far_el1;
};

/* Process Control Block (PCB) */
struct task_struct {
    struct cpu_context context;
    pid_t pid;
    task_state_t state;
    uint32_t priority;
    uint64_t time_slice;
    uint64_t total_ticks;
    
    char name[32];
    uint64_t *pgdir; /* Page directory physical address (TTBR0_EL1) */
    
    void *kernel_stack;
    void *user_stack;
    
    struct list_head run_list;
    struct list_head all_list;
};

/* Scheduler prototypes */
void sched_init(void);
struct task_struct *task_create(const char *name, void (*entry)(void), uint32_t priority, bool is_user);
void task_exit(int code);
void schedule(void);
void sched_tick(void);

extern struct task_struct *current_task;
void cpu_switch_to(struct task_struct *prev, struct task_struct *next);

#endif /* _HOBOS_SCHED_H_ */
