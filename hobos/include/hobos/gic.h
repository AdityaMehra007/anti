/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * gic.h - ARM Generic Interrupt Controller v2
 */

#ifndef _HOBOS_GIC_H_
#define _HOBOS_GIC_H_

#include <hobos/types.h>

/* QEMU virt board GICv2 MMIO base addresses */
#define GICD_BASE 0x08000000ULL /* Distributor */
#define GICC_BASE 0x08010000ULL /* CPU Interface */

/* Distributor Registers */
#define GICD_CTLR            (GICD_BASE + 0x000)
#define GICD_TYPER           (GICD_BASE + 0x004)
#define GICD_ISENABLER(n)    (GICD_BASE + 0x100 + ((n) * 4))
#define GICD_ICENABLER(n)    (GICD_BASE + 0x180 + ((n) * 4))
#define GICD_IPRIORITYR(n)   (GICD_BASE + 0x400 + ((n) * 4))
#define GICD_ITARGETSR(n)    (GICD_BASE + 0x800 + ((n) * 4))
#define GICD_ICFGR(n)        (GICD_BASE + 0xC00 + ((n) * 4))

/* CPU Interface Registers */
#define GICC_CTLR            (GICC_BASE + 0x000)
#define GICC_PMR             (GICC_BASE + 0x004)
#define GICC_IAR             (GICC_BASE + 0x00C)
#define GICC_EOIR            (GICC_BASE + 0x010)

/* Common IRQs on virt board */
#define IRQ_UART0            33
#define IRQ_ARCH_TIMER       27

typedef void (*irq_handler_t)(uint32_t irq, void *data);

void gic_init(void);
void gic_enable_irq(uint32_t irq);
void gic_disable_irq(uint32_t irq);
void register_irq_handler(uint32_t irq, irq_handler_t handler, void *data);
void gic_handle_irq(void);

#endif /* _HOBOS_GIC_H_ */
