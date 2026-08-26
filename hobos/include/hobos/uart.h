/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * uart.h - ARM PrimeCell PL011 UART Driver
 */

#ifndef _HOBOS_UART_H_
#define _HOBOS_UART_H_

#include <hobos/types.h>

/* QEMU virt board PL011 UART0 base */
#define UART0_BASE 0x09000000ULL

/* PL011 Register Offsets */
#define UART_DR    (UART0_BASE + 0x000) /* Data Register */
#define UART_RSR   (UART0_BASE + 0x004) /* Receive Status Register */
#define UART_FR    (UART0_BASE + 0x018) /* Flag Register */
#define UART_IBRD  (UART0_BASE + 0x024) /* Integer Baud Rate */
#define UART_FBRD  (UART0_BASE + 0x028) /* Fractional Baud Rate */
#define UART_LCRH  (UART0_BASE + 0x02C) /* Line Control Register */
#define UART_CR    (UART0_BASE + 0x030) /* Control Register */
#define UART_IMSC  (UART0_BASE + 0x038) /* Interrupt Mask Set/Clear */
#define UART_ICR   (UART0_BASE + 0x044) /* Interrupt Clear Register */

/* Flag Register bits */
#define UART_FR_TXFF (1 << 5) /* Transmit FIFO full */
#define UART_FR_RXFE (1 << 4) /* Receive FIFO empty */
#define UART_FR_BUSY (1 << 3) /* UART busy */

void uart_init(void);
void uart_putc(char c);
void uart_puts(const char *str);
char uart_getc(void);
bool uart_has_char(void);

#endif /* _HOBOS_UART_H_ */
