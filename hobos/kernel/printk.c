/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * printk.c - Kernel Formatted Output Driver
 */

#include <hobos/kernel.h>
#include <hobos/uart.h>
#include <stdarg.h>

static void print_num(uint64_t num, int base, bool sign, int width, char pad) {
    char buf[64];
    int i = 0;
    const char *digits = "0123456789abcdef";

    if (sign && (int64_t)num < 0) {
        uart_putc('-');
        num = (uint64_t)(-(int64_t)num);
        if (width > 0) width--;
    }

    if (num == 0) {
        buf[i++] = '0';
    } else {
        while (num > 0) {
            buf[i++] = digits[num % base];
            num /= base;
        }
    }

    while (width > i) {
        uart_putc(pad);
        width--;
    }

    while (i > 0) {
        uart_putc(buf[--i]);
    }
}

void vprintk(const char *fmt, va_list args) {
    while (*fmt) {
        if (*fmt == '%') {
            fmt++;
            char pad = ' ';
            int width = 0;

            if (*fmt == '0') {
                pad = '0';
                fmt++;
            }

            while (*fmt >= '0' && *fmt <= '9') {
                width = width * 10 + (*fmt - '0');
                fmt++;
            }

            switch (*fmt) {
                case 's': {
                    const char *s = va_arg(args, const char *);
                    uart_puts(s ? s : "(null)");
                    break;
                }
                case 'c': {
                    char c = (char)va_arg(args, int);
                    uart_putc(c);
                    break;
                }
                case 'd': {
                    int32_t d = va_arg(args, int32_t);
                    print_num((uint64_t)d, 10, true, width, pad);
                    break;
                }
                case 'u': {
                    uint32_t u = va_arg(args, uint32_t);
                    print_num(u, 10, false, width, pad);
                    break;
                }
                case 'x': {
                    uint32_t x = va_arg(args, uint32_t);
                    print_num(x, 16, false, width, pad);
                    break;
                }
                case 'l': {
                    fmt++;
                    if (*fmt == 'x' || *fmt == 'u' || *fmt == 'd') {
                        uint64_t lx = va_arg(args, uint64_t);
                        if (*fmt == 'x') {
                            print_num(lx, 16, false, width, pad);
                        } else if (*fmt == 'd') {
                            print_num(lx, 10, true, width, pad);
                        } else {
                            print_num(lx, 10, false, width, pad);
                        }
                    }
                    break;
                }
                case 'p': {
                    uint64_t p = va_arg(args, uint64_t);
                    uart_puts("0x");
                    print_num(p, 16, false, 16, '0');
                    break;
                }
                case '%': {
                    uart_putc('%');
                    break;
                }
                default:
                    uart_putc('%');
                    uart_putc(*fmt);
                    break;
            }
        } else {
            uart_putc(*fmt);
        }
        fmt++;
    }
}

void printk(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vprintk(fmt, args);
    va_end(args);
}
