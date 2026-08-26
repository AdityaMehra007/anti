/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * sched.c - Priority Preemptive Round-Robin Scheduler
 */

#include <hobos/sched.h>
#include <hobos/kernel.h>
#include <hobos/sync.h>

struct task_struct *current_task = NULL;
static struct task_struct idle_task;

static LIST_HEAD(runqueue);
static spinlock_t sched_lock = SPINLOCK_INIT;

static void idle_thread_fn(void) {
    while (1) {
        asm volatile("wfi");
    }
}

void sched_init(void) {
    printk("[SCHED] Initializing Preemptive Task Scheduler...\n");
    init_list_head(&runqueue);

    /* Initialize Idle Task */
    idle_task.pid = 0;
    idle_task.state = TASK_STATE_RUNNING;
    idle_task.priority = 0;
    idle_task.time_slice = 1;
    char idle_name[] = "idle";
    for (int i = 0; i < 5; i++) idle_task.name[i] = idle_name[i];

    current_task = &idle_task;
}

void sched_add_task(struct task_struct *task) {
    if (!task) return;
    spin_lock(&sched_lock);
    task->state = TASK_STATE_READY;
    list_add_tail(&task->run_list, &runqueue);
    spin_unlock(&sched_lock);
}

void sched_tick(void) {
    if (!current_task || current_task == &idle_task) {
        schedule();
        return;
    }

    current_task->total_ticks++;

    if (current_task->time_slice > 0) {
        current_task->time_slice--;
    }

    if (current_task->time_slice == 0) {
        current_task->time_slice = 10; /* Reset slice */
        schedule();
    }
}

void schedule(void) {
    spin_lock(&sched_lock);

    struct task_struct *prev = current_task;
    struct task_struct *next = NULL;

    /* Re-queue prev if still ready/running */
    if (prev && prev != &idle_task && prev->state == TASK_STATE_RUNNING) {
        prev->state = TASK_STATE_READY;
        list_add_tail(&prev->run_list, &runqueue);
    }

    /* Pick next task from runqueue */
    if (!list_empty(&runqueue)) {
        struct list_head *entry = runqueue.next;
        list_del(entry);
        next = list_entry(entry, struct task_struct, run_list);
    } else {
        next = &idle_task;
    }

    next->state = TASK_STATE_RUNNING;
    current_task = next;

    spin_unlock(&sched_lock);

    if (prev != next) {
        cpu_switch_to(prev, next);
    }
}
