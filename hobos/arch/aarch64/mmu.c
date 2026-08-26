/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * mmu.c - Virtual Memory Management & 4-Level Page Table Translation
 */

#include <hobos/mm.h>
#include <hobos/kernel.h>
#include <hobos/uart.h>
#include <hobos/gic.h>
#include "asm_utils.h"

/* Early static page tables for kernel boot */
__attribute__((aligned(PAGE_SIZE))) uint64_t kernel_pgdir_l0[512];
__attribute__((aligned(PAGE_SIZE))) uint64_t kernel_pgdir_l1[512];
__attribute__((aligned(PAGE_SIZE))) uint64_t kernel_pgdir_l2[512];

void vmm_init(void) {
    printk("[MMU] Initializing 4-Level ARM64 Page Tables (4KB Granule, 48-bit VA)...\n");

    /* Clear L0, L1, L2 tables */
    for (int i = 0; i < 512; i++) {
        kernel_pgdir_l0[i] = 0;
        kernel_pgdir_l1[i] = 0;
        kernel_pgdir_l2[i] = 0;
    }

    /* Link L0 -> L1 */
    kernel_pgdir_l0[0] = ((uint64_t)kernel_pgdir_l1) | PTE_TABLE | PTE_VALID;

    /* Link L1 -> L2 */
    kernel_pgdir_l1[0] = ((uint64_t)kernel_pgdir_l2) | PTE_TABLE | PTE_VALID;

    /* Map 1GB of DRAM (0x40000000 to 0x80000000) using 2MB blocks */
    for (uint64_t paddr = DRAM_BASE; paddr < (DRAM_BASE + 0x20000000); paddr += 0x200000) {
        uint64_t idx = (paddr >> 21) & 0x1FF;
        kernel_pgdir_l2[idx] = paddr | PTE_BLOCK | PTE_VALID | PTE_AF | PTE_SH_INNER | PTE_ATTRINDX(ATTR_NORMAL_WB);
    }

    /* Map Device MMIO (UART0: 0x09000000, GIC: 0x08000000) */
    uint64_t dev_uart_idx = (UART0_BASE >> 21) & 0x1FF;
    kernel_pgdir_l2[dev_uart_idx] = UART0_BASE | PTE_BLOCK | PTE_VALID | PTE_AF | PTE_ATTRINDX(ATTR_DEVICE_nGnRnE);

    uint64_t dev_gic_idx = (GICD_BASE >> 21) & 0x1FF;
    kernel_pgdir_l2[dev_gic_idx] = GICD_BASE | PTE_BLOCK | PTE_VALID | PTE_AF | PTE_ATTRINDX(ATTR_DEVICE_nGnRnE);

    /* Setup MAIR_EL1 */
    uint64_t mair = (0x00ULL << (ATTR_DEVICE_nGnRnE * 8)) | /* Device-nGnRnE */
                    (0x44ULL << (ATTR_NORMAL_NC * 8))     | /* Normal Non-Cacheable */
                    (0xFFULL << (ATTR_NORMAL_WB * 8));      /* Normal Write-Back */
    set_mair_el1(mair);

    /* Setup TCR_EL1: T0SZ=16 (48-bit VA), TG0=0 (4KB), Inner/Outer WB Cacheable */
    uint64_t tcr = (16ULL << 0)   | /* T0SZ */
                   (0ULL  << 14)  | /* TG0: 4KB */
                   (3ULL  << 8)   | /* Outer Shareable */
                   (1ULL  << 10)  | /* Outer Cacheable */
                   (1ULL  << 12)  | /* Inner Cacheable */
                   (16ULL << 16)  | /* T1SZ */
                   (2ULL  << 30);   /* TG1: 4KB */
    set_tcr_el1(tcr);

    /* Set TTBR0_EL1 and TTBR1_EL1 */
    set_ttbr0_el1((uint64_t)kernel_pgdir_l0);
    set_ttbr1_el1((uint64_t)kernel_pgdir_l0);

    flush_tlb_all();

    /* Enable MMU and Caches in SCTLR_EL1 */
    uint64_t sctlr = get_sctlr_el1();
    sctlr |= (1 << 0);  /* M: Enable MMU */
    sctlr |= (1 << 2);  /* C: Enable Data Cache */
    sctlr |= (1 << 12); /* I: Enable Instruction Cache */
    set_sctlr_el1(sctlr);
    isb();

    printk("[MMU] Hardware MMU Enabled Successfully. Translation Active.\n");
}

int vmm_map_page(uint64_t *pgdir, vaddr_t vaddr, paddr_t paddr, uint64_t flags) {
    uint64_t l0_idx = (vaddr >> 39) & 0x1FF;
    uint64_t l1_idx = (vaddr >> 30) & 0x1FF;
    uint64_t l2_idx = (vaddr >> 21) & 0x1FF;
    uint64_t l3_idx = (vaddr >> 12) & 0x1FF;

    /* Traverse or allocate tables */
    if (!(pgdir[l0_idx] & PTE_VALID)) {
        void *tbl = alloc_page();
        if (!tbl) return -1;
        for (int i = 0; i < 512; i++) ((uint64_t *)tbl)[i] = 0;
        pgdir[l0_idx] = ((uint64_t)tbl) | PTE_TABLE | PTE_VALID;
    }

    uint64_t *l1_tbl = (uint64_t *)(pgdir[l0_idx] & ~0xFFFULL);
    if (!(l1_tbl[l1_idx] & PTE_VALID)) {
        void *tbl = alloc_page();
        if (!tbl) return -1;
        for (int i = 0; i < 512; i++) ((uint64_t *)tbl)[i] = 0;
        l1_tbl[l1_idx] = ((uint64_t)tbl) | PTE_TABLE | PTE_VALID;
    }

    uint64_t *l2_tbl = (uint64_t *)(l1_tbl[l1_idx] & ~0xFFFULL);
    if (!(l2_tbl[l2_idx] & PTE_VALID)) {
        void *tbl = alloc_page();
        if (!tbl) return -1;
        for (int i = 0; i < 512; i++) ((uint64_t *)tbl)[i] = 0;
        l2_tbl[l2_idx] = ((uint64_t)tbl) | PTE_TABLE | PTE_VALID;
    }

    uint64_t *l3_tbl = (uint64_t *)(l2_tbl[l2_idx] & ~0xFFFULL);
    l3_tbl[l3_idx] = paddr | PTE_PAGE | PTE_VALID | PTE_AF | flags;

    flush_tlb_all();
    return 0;
}
