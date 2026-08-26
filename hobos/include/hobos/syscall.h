/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * syscall.h - System call interface, ABI numbers, and dispatch table
 */

#ifndef _HOBOS_SYSCALL_H_
#define _HOBOS_SYSCALL_H_

#include <hobos/types.h>
#include <hobos/sched.h>

#define SYS_YIELD     0
#define SYS_EXIT      1
#define SYS_FORK      2
#define SYS_EXEC      3
#define SYS_READ      4
#define SYS_WRITE     5
#define SYS_OPEN      6
#define SYS_CLOSE     7
#define SYS_GETPID    8
#define SYS_MMAP      9
#define SYS_SLEEP     10
#define MAX_SYSCALLS  32

typedef int64_t (*syscall_fn_t)(uint64_t a0, uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5);

void syscall_init(void);
void handle_syscall(struct trap_frame *tf);

/* User copy safety functions */
int copy_from_user(void *dst, const void *src, size_t n);
int copy_to_user(void *dst, const void *src, size_t n);

#endif /* _HOBOS_SYSCALL_H_ */
