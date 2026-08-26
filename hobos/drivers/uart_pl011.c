/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * uart_pl011.c - ARM PrimeCell PL011 UART Driver Implementation
 */

#include <hobos/uart.h>
#include <hobos/gic.h>

#define REG(r) (*(volatile uint32_t *)(r))

static void uart_irq_handler(uint32_t irq, void *data) {
    (void)irq;
    (void)data;
    /* Clear RX/TX interrupts */
    REG(UART_ICR) = 0x7FF;
}

void uart_init(void) {
    /* Disable UART */
    REG(UART_CR) = 0;

    /* Set Baud Rate (Assuming 24MHz clock, 115200 baud: IBRD=13, FBRD=1) */
    REG(UART_IBRD) = 13;
    REG(UART_FBRD) = 1;

    /* 8 bits, 1 stop bit, no parity, FIFO enabled (WLEN = 3, FEN = 1) */
    REG(UART_LCRH) = (3 << 5) | (1 << 4);

    /* Mask all interrupts */
    REG(UART_IMSC) = 0;
    REG(UART_ICR) = 0x7FF;

    /* Enable UART, TX, RX (UARTEN=1, TXE=1, RXE=1) */
    REG(UART_CR) = (1 << 0) | (1 << 8) | (1 << 9);

    /* Register UART IRQ */
    register_irq_handler(IRQ_UART0, uart_irq_handler, NULL);
}

void uart_putc(char c) {
    /* Wait until transmit FIFO is not full */
    while (REG(UART_FR) & UART_FR_TXFF) {
        asm volatile("nop");
    }
    REG(UART_DR) = (uint32_t)c;
}

void uart_puts(const char *str) {
    if (!str) return;
    while (*str) {
        if (*str == '\n') {
            uart_putc('\r');
        }
        uart_putc(*str++);
    }
}

bool uart_has_char(void) {
    return !(REG(UART_FR) & UART_FR_RXFE);
}

char uart_getc(void) {
    while (!uart_has_char()) {
        asm volatile("wfi");
    }
    return (char)(REG(UART_DR) & 0xFF);
}
