/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * syscall.c - System Call Dispatcher & Pointer Validation Safety Checks
 */

#include <hobos/syscall.h>
#include <hobos/sched.h>
#include <hobos/vfs.h>
#include <hobos/uart.h>
#include <hobos/kernel.h>

static syscall_fn_t syscall_table[MAX_SYSCALLS];

int copy_from_user(void *dst, const void *src, size_t n) {
    uintptr_t uaddr = (uintptr_t)src;
    /* Check that source address is in userspace (< 0x0000800000000000) */
    if (uaddr >= 0xFFFF000000000000ULL || (uaddr + n) < uaddr) {
        return -1; /* Fault: attempt to read kernel space */
    }
    const char *s = (const char *)src;
    char *d = (char *)dst;
    for (size_t i = 0; i < n; i++) {
        d[i] = s[i];
    }
    return 0;
}

int copy_to_user(void *dst, const void *src, size_t n) {
    uintptr_t uaddr = (uintptr_t)dst;
    if (uaddr >= 0xFFFF000000000000ULL || (uaddr + n) < uaddr) {
        return -1; /* Fault: attempt to write to kernel space */
    }
    const char *s = (const char *)src;
    char *d = (char *)dst;
    for (size_t i = 0; i < n; i++) {
        d[i] = s[i];
    }
    return 0;
}

/* Syscall implementations */
static int64_t sys_yield(uint64_t a0, uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5) {
    (void)a0; (void)a1; (void)a2; (void)a3; (void)a4; (void)a5;
    schedule();
    return 0;
}

static int64_t sys_exit(uint64_t code, uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5) {
    (void)a1; (void)a2; (void)a3; (void)a4; (void)a5;
    task_exit((int)code);
    return 0;
}

static int64_t sys_write(uint64_t fd, uint64_t buf_ptr, uint64_t count, uint64_t a3, uint64_t a4, uint64_t a5) {
    (void)a3; (void)a4; (void)a5;
    if (fd == 1 || fd == 2) { /* stdout / stderr */
        char kbuf[256];
        size_t total = 0;
        while (total < count) {
            size_t chunk = MIN(count - total, sizeof(kbuf) - 1);
            if (copy_from_user(kbuf, (const void *)(buf_ptr + total), chunk) < 0) {
                return -1; /* EFAULT */
            }
            kbuf[chunk] = '\0';
            uart_puts(kbuf);
            total += chunk;
        }
        return total;
    }
    return vfs_write((int)fd, (const void *)buf_ptr, (size_t)count);
}

static int64_t sys_getpid(uint64_t a0, uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5) {
    (void)a0; (void)a1; (void)a2; (void)a3; (void)a4; (void)a5;
    return current_task ? current_task->pid : 0;
}

void syscall_init(void) {
    printk("[SYSCALL] Initializing AArch64 Syscall ABI Dispatch Table...\n");
    for (int i = 0; i < MAX_SYSCALLS; i++) {
        syscall_table[i] = NULL;
    }

    syscall_table[SYS_YIELD]  = sys_yield;
    syscall_table[SYS_EXIT]   = sys_exit;
    syscall_table[SYS_WRITE]  = sys_write;
    syscall_table[SYS_GETPID] = sys_getpid;
}

void handle_syscall(struct trap_frame *tf) {
    uint64_t syscall_nr = tf->x[8]; /* Syscall number passed in x8 */

    if (syscall_nr < MAX_SYSCALLS && syscall_table[syscall_nr]) {
        int64_t ret = syscall_table[syscall_nr](
            tf->x[0], tf->x[1], tf->x[2],
            tf->x[3], tf->x[4], tf->x[5]
        );
        tf->x[0] = (uint64_t)ret; /* Return value in x0 */
    } else {
        printk("[SYSCALL] Unknown syscall %lu called by PID %d.\n", syscall_nr, current_task ? current_task->pid : -1);
        tf->x[0] = (uint64_t)-1; /* ENOSYS */
    }
}
