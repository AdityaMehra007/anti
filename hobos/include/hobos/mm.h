/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * mm.h - Memory management, page allocator, buddy system, slab, VMM
 */

#ifndef _HOBOS_MM_H_
#define _HOBOS_MM_H_

#include <hobos/types.h>
#include <hobos/list.h>

#define PAGE_SHIFT        12
#define PAGE_SIZE         (1ULL << PAGE_SHIFT) /* 4KB */
#define PAGE_MASK         (~(PAGE_SIZE - 1))

#define MAX_ORDER         10 /* Max allocation block: 2^10 * 4KB = 4MB */

/* Page Table Attributes (ARMv8 4KB Granularity) */
#define PTE_VALID         (1ULL << 0)
#define PTE_TABLE         (1ULL << 1)
#define PTE_BLOCK         (0ULL << 1)
#define PTE_PAGE          (1ULL << 1)
#define PTE_USER          (1ULL << 6)
#define PTE_RO            (1ULL << 7)
#define PTE_RW            (0ULL << 7)
#define PTE_SH_INNER      (3ULL << 8)
#define PTE_AF            (1ULL << 10) /* Access Flag */
#define PTE_NG            (1ULL << 11) /* Non-Global */
#define PTE_PXN           (1ULL << 53) /* Privileged eXecute Never */
#define PTE_UXN           (1ULL << 54) /* User eXecute Never */

/* Memory Attribute Indices in MAIR_EL1 */
#define ATTR_DEVICE_nGnRnE 0
#define ATTR_NORMAL_NC     1
#define ATTR_NORMAL_WB     2
#define PTE_ATTRINDX(idx)  ((uint64_t)(idx) << 2)

/* Page descriptor */
struct page {
    uint32_t flags;
    uint32_t order;
    uint32_t ref_count;
    struct list_head list;
    paddr_t paddr;
};

#define PAGE_FLAG_FREE     (1 << 0)
#define PAGE_FLAG_RESERVED (1 << 1)
#define PAGE_FLAG_SLAB     (1 << 2)

/* Memory prototypes */
void mm_init(paddr_t mem_start, size_t mem_size);
struct page *alloc_pages(uint32_t order);
void free_pages(struct page *p, uint32_t order);

void *alloc_page(void);
void free_page(void *ptr);

void slab_init(void);
void *kmalloc(size_t size);
void kfree(void *ptr);

void vmm_init(void);
int vmm_map_page(uint64_t *pgdir, vaddr_t vaddr, paddr_t paddr, uint64_t flags);
int vmm_unmap_page(uint64_t *pgdir, vaddr_t vaddr);
paddr_t vmm_virt_to_phys(uint64_t *pgdir, vaddr_t vaddr);

#endif /* _HOBOS_MM_H_ */
