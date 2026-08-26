/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * types.h - Fundamental fixed-width type definitions
 */

#ifndef _HOBOS_TYPES_H_
#define _HOBOS_TYPES_H_

typedef unsigned char      uint8_t;
typedef unsigned short     uint16_t;
typedef unsigned int       uint32_t;
typedef unsigned long long uint64_t;

typedef signed char        int8_t;
typedef signed short       int16_t;
typedef signed int         int32_t;
typedef signed long long   int64_t;

typedef uint64_t           size_t;
typedef int64_t            ssize_t;
typedef uint64_t           uintptr_t;
typedef int64_t            intptr_t;
typedef uint64_t           paddr_t;
typedef uint64_t           vaddr_t;
typedef int32_t            pid_t;

#define NULL ((void *)0)

typedef enum {
    false = 0,
    true = 1
} bool;

#endif /* _HOBOS_TYPES_H_ */
