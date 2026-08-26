/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * main.c - Kernel Main Entry Point & Subsystem Initialization Sequence
 */

#include <hobos/kernel.h>
#include <hobos/types.h>
#include <hobos/uart.h>
#include <hobos/gic.h>
#include <hobos/timer.h>
#include <hobos/mm.h>
#include <hobos/sched.h>
#include <hobos/syscall.h>
#include <hobos/vfs.h>

extern void sched_add_task(struct task_struct *task);
extern void set_vbar_el1(uint64_t vbar);
extern char vector_table_el1[];

static void user_init_process(void) {
    printk("\n=======================================================\n");
    printk("       🌟 [HobOS USERSPACE INIT PROCESS STARTED] 🌟    \n");
    printk("=======================================================\n");
    printk("[USER] Running at EL0 with isolated stack and virtual address space.\n");
    printk("[USER] Invoking SYS_WRITE (stdout: fd 1)...\n");

    const char msg[] = "[USER] Hello from HobOS Userspace Process (PID 1)!\n";
    asm volatile(
        "mov x8, %0\n" /* SYS_WRITE */
        "mov x0, #1\n" /* stdout */
        "mov x1, %1\n"
        "mov x2, %2\n"
        "svc #0\n"
        :
        : "r"((uint64_t)SYS_WRITE), "r"((uint64_t)msg), "r"((uint64_t)sizeof(msg))
        : "x0", "x1", "x2", "x8"
    );

    printk("[USER] Userspace interactive shell operational.\n");

    while (1) {
        asm volatile("wfi");
    }
}

static void kernel_worker_task(void) {
    printk("[WORKER] Background kernel worker active. Processing task queues...\n");
    while (1) {
        timer_sleep_ms(500);
        printk("[HEARTBEAT] System Ticks: %lu | Active PID: %d\n", timer_get_ticks(), current_task ? current_task->pid : 0);
    }
}

void kmain(void) {
    /* 1. Early Serial Console */
    uart_init();
    printk("\n\n");
    printk("===============================================================\n");
    printk("    __  __      __   ____  _____\n");
    printk("   / / / /___  / /_ / __ \\/ ___/\n");
    printk("  / /_/ / __ \\/ __ \\/ / / /\\__ \\ \n");
    printk(" / __  / /_/ / /_/ / /_/ /___/ / \n");
    printk("/_/ /_/\\____/_.___/\\____//____/  v%s\n", KERNEL_VERSION);
    printk("ARMv8-A 64-bit Educational & Research Operating System Platform\n");
    printk("===============================================================\n\n");

    /* 2. Set Exception Vector Base (VBAR_EL1) */
    set_vbar_el1((uint64_t)vector_table_el1);
    printk("[BOOT] VBAR_EL1 Exception Vector Table Loaded at %p\n", vector_table_el1);

    /* 3. Physical Memory Allocation (Buddy System) */
    mm_init(DRAM_BASE + 0x1000000, 128 * 1024 * 1024); /* 128MB managed */

    /* 4. Slab / kmalloc Object Allocator */
    slab_init();

    /* 5. Virtual Memory & 4-Level Page Tables */
    vmm_init();

    /* 6. Generic Interrupt Controller (GICv2) */
    gic_init();

    /* 7. Architectural Physical Timer */
    timer_init();

    /* 8. Virtual File System */
    vfs_init();
    vfs_create_file("motd.txt", "Welcome to HobOS ARM64!", 25);

    /* 9. Syscall ABI Dispatcher */
    syscall_init();

    /* 10. Process Control & Preemptive Scheduler */
    sched_init();

    /* 11. Spawn Initial Tasks */
    struct task_struct *init_task = task_create("init", user_init_process, 10, true);
    sched_add_task(init_task);

    struct task_struct *worker_task = task_create("kworker", kernel_worker_task, 5, false);
    sched_add_task(worker_task);

    printk("[BOOT] All Core Subsystems Online. Entering Scheduler Loop...\n");

    /* Enable Interrupts and jump to scheduler */
    asm volatile("msr daifclr, #2" ::: "memory");
    schedule();

    /* Should never reach here */
    panic("Kernel execution reached end of kmain()!\n");
}
