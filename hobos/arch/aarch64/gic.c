/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * gic.c - ARM Generic Interrupt Controller v2 Driver
 */

#include <hobos/gic.h>
#include <hobos/kernel.h>

#define MMIO32(addr) (*(volatile uint32_t *)(addr))

static struct {
    irq_handler_t handler;
    void *data;
} irq_handlers[1024];

void gic_init(void) {
    printk("[GIC] Initializing GICv2 Interrupt Controller...\n");

    /* Disable Distributor while configuring */
    MMIO32(GICD_CTLR) = 0;

    /* Get number of interrupt lines */
    uint32_t typer = MMIO32(GICD_TYPER);
    uint32_t it_lines_number = typer & 0x1F;
    uint32_t max_irq = 32 * (it_lines_number + 1);

    /* Disable all interrupts, set priority to 0xA0, route all to CPU0 */
    for (uint32_t i = 0; i < max_irq; i += 32) {
        MMIO32(GICD_ICENABLER(i / 32)) = 0xFFFFFFFF;
    }

    for (uint32_t i = 0; i < max_irq; i += 4) {
        MMIO32(GICD_IPRIORITYR(i / 4)) = 0xA0A0A0A0;
        MMIO32(GICD_ITARGETSR(i / 4)) = 0x01010101; /* Target CPU0 */
    }

    /* Enable Distributor (Group 0 & Group 1) */
    MMIO32(GICD_CTLR) = 3;

    /* Configure CPU Interface: Priority Mask = 0xF0 (accept all lower priorities), Enable */
    MMIO32(GICC_PMR) = 0xF0;
    MMIO32(GICC_CTLR) = 3;

    printk("[GIC] GICv2 Enabled for %u Interrupt Lines.\n", max_irq);
}

void gic_enable_irq(uint32_t irq) {
    MMIO32(GICD_ISENABLER(irq / 32)) = (1 << (irq % 32));
}

void gic_disable_irq(uint32_t irq) {
    MMIO32(GICD_ICENABLER(irq / 32)) = (1 << (irq % 32));
}

void register_irq_handler(uint32_t irq, irq_handler_t handler, void *data) {
    if (irq < 1024) {
        irq_handlers[irq].handler = handler;
        irq_handlers[irq].data = data;
        gic_enable_irq(irq);
    }
}

void gic_handle_irq(void) {
    uint32_t iar = MMIO32(GICC_IAR);
    uint32_t irq = iar & 0x3FF;

    if (irq >= 1020) {
        /* Spurious interrupt */
        return;
    }

    if (irq_handlers[irq].handler) {
        irq_handlers[irq].handler(irq, irq_handlers[irq].data);
    }

    /* Acknowledge End-of-Interrupt */
    MMIO32(GICC_EOIR) = iar;
}
