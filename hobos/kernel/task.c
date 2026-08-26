/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * task.c - Process Control Block (PCB) Allocation and Task Management
 */

#include <hobos/sched.h>
#include <hobos/mm.h>
#include <hobos/kernel.h>
#include <hobos/sync.h>

static pid_t next_pid = 1;
static spinlock_t task_lock = SPINLOCK_INIT;

LIST_HEAD(all_tasks_head);

struct task_struct *task_create(const char *name, void (*entry)(void), uint32_t priority, bool is_user) {
    spin_lock(&task_lock);

    struct task_struct *t = (struct task_struct *)kmalloc(sizeof(struct task_struct));
    if (!t) {
        spin_unlock(&task_lock);
        return NULL;
    }

    t->pid = next_pid++;
    t->state = TASK_STATE_READY;
    t->priority = priority;
    t->time_slice = 10; /* 10 ticks default */
    t->total_ticks = 0;

    /* Copy name */
    int i = 0;
    while (name && name[i] && i < 31) {
        t->name[i] = name[i];
        i++;
    }
    t->name[i] = '\0';

    /* Allocate kernel stack */
    t->kernel_stack = kmalloc(KERNEL_STACK_SIZE);
    if (!t->kernel_stack) {
        kfree(t);
        spin_unlock(&task_lock);
        return NULL;
    }

    /* Clear context */
    char *ctx_bytes = (char *)&t->context;
    for (size_t b = 0; b < sizeof(struct cpu_context); b++) {
        ctx_bytes[b] = 0;
    }

    uint64_t sp_top = (uint64_t)t->kernel_stack + KERNEL_STACK_SIZE;

    if (is_user) {
        /* Allocate user stack */
        t->user_stack = kmalloc(PAGE_SIZE);
        /* Set up trapframe for eret into EL0 */
        t->context.sp = sp_top;
        t->context.pc = (uint64_t)entry;
    } else {
        t->user_stack = NULL;
        t->context.sp = sp_top;
        t->context.pc = (uint64_t)entry;
    }

    init_list_head(&t->run_list);
    list_add_tail(&t->all_list, &all_tasks_head);

    spin_unlock(&task_lock);
    return t;
}

void task_exit(int code) {
    (void)code;
    spin_lock(&task_lock);
    if (current_task) {
        current_task->state = TASK_STATE_ZOMBIE;
        printk("[TASK] Task '%s' (PID %d) terminated with code %d.\n", current_task->name, current_task->pid, code);
    }
    spin_unlock(&task_lock);
    schedule();
}
