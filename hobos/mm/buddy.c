/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * buddy.c - Physical Page Buddy Allocator (Power-of-Two Coalescing)
 */

#include <hobos/mm.h>
#include <hobos/kernel.h>
#include <hobos/sync.h>

static spinlock_t buddy_lock = SPINLOCK_INIT;

static struct {
    struct list_head free_list[MAX_ORDER + 1];
    uint32_t nr_free[MAX_ORDER + 1];
} free_areas;

static struct page *mem_map = NULL;
static paddr_t phys_start = 0;
static size_t total_pages = 0;

void mm_init(paddr_t start, size_t size) {
    printk("[BUDDY] Initializing Buddy Allocator from 0x%lx (Size: %lu MB)...\n", start, size / (1024 * 1024));

    phys_start = ALIGN_UP(start, PAGE_SIZE);
    total_pages = size / PAGE_SIZE;

    /* Initialize free lists */
    for (int o = 0; o <= MAX_ORDER; o++) {
        init_list_head(&free_areas.free_list[o]);
        free_areas.nr_free[o] = 0;
    }

    /* Allocate page array at start of physical memory */
    size_t mem_map_size = ALIGN_UP(total_pages * sizeof(struct page), PAGE_SIZE);
    mem_map = (struct page *)phys_start;
    phys_start += mem_map_size;
    total_pages -= (mem_map_size / PAGE_SIZE);

    /* Initialize page descriptors */
    for (size_t i = 0; i < total_pages; i++) {
        struct page *p = &mem_map[i];
        p->flags = PAGE_FLAG_FREE;
        p->order = 0;
        p->ref_count = 0;
        p->paddr = phys_start + (i * PAGE_SIZE);
        init_list_head(&p->list);
    }

    /* Add blocks to buddy allocator */
    size_t pfn = 0;
    while (pfn < total_pages) {
        uint32_t order = MAX_ORDER;
        while (order > 0 && (pfn + (1 << order) > total_pages || (pfn & ((1 << order) - 1)) != 0)) {
            order--;
        }
        struct page *p = &mem_map[pfn];
        p->order = order;
        list_add(&p->list, &free_areas.free_list[order]);
        free_areas.nr_free[order]++;
        pfn += (1 << order);
    }

    printk("[BUDDY] Total Physical Pages Managed: %lu (%lu KB)\n", total_pages, (total_pages * PAGE_SIZE) / 1024);
}

struct page *alloc_pages(uint32_t order) {
    if (order > MAX_ORDER) return NULL;

    spin_lock(&buddy_lock);

    for (uint32_t cur_order = order; cur_order <= MAX_ORDER; cur_order++) {
        if (!list_empty(&free_areas.free_list[cur_order])) {
            struct list_head *entry = free_areas.free_list[cur_order].next;
            list_del(entry);
            free_areas.nr_free[cur_order]--;

            struct page *page = list_entry(entry, struct page, list);

            /* Split higher-order blocks down to requested order */
            while (cur_order > order) {
                cur_order--;
                size_t buddy_pfn = ((page->paddr - phys_start) / PAGE_SIZE) + (1 << cur_order);
                struct page *buddy = &mem_map[buddy_pfn];
                buddy->order = cur_order;
                buddy->flags = PAGE_FLAG_FREE;
                list_add(&buddy->list, &free_areas.free_list[cur_order]);
                free_areas.nr_free[cur_order]++;
            }

            page->order = order;
            page->flags &= ~PAGE_FLAG_FREE;
            page->ref_count = 1;

            spin_unlock(&buddy_lock);
            return page;
        }
    }

    spin_unlock(&buddy_lock);
    return NULL;
}

void free_pages(struct page *page, uint32_t order) {
    if (!page || order > MAX_ORDER) return;

    spin_lock(&buddy_lock);

    size_t pfn = (page->paddr - phys_start) / PAGE_SIZE;

    /* Coalesce with buddies */
    while (order < MAX_ORDER) {
        size_t buddy_pfn = pfn ^ (1 << order);
        if (buddy_pfn >= total_pages) break;

        struct page *buddy = &mem_map[buddy_pfn];
        if (!(buddy->flags & PAGE_FLAG_FREE) || buddy->order != order) {
            break; /* Buddy is not free or not same order */
        }

        /* Remove buddy from free list */
        list_del(&buddy->list);
        free_areas.nr_free[order]++;

        /* Combined block */
        if (buddy_pfn < pfn) {
            pfn = buddy_pfn;
            page = buddy;
        }
        order++;
    }

    page->order = order;
    page->flags |= PAGE_FLAG_FREE;
    list_add(&page->list, &free_areas.free_list[order]);
    free_areas.nr_free[order]++;

    spin_unlock(&buddy_lock);
}

void *alloc_page(void) {
    struct page *p = alloc_pages(0);
    return p ? (void *)p->paddr : NULL;
}

void free_page(void *ptr) {
    if (!ptr) return;
    paddr_t addr = (paddr_t)ptr;
    size_t pfn = (addr - phys_start) / PAGE_SIZE;
    if (pfn < total_pages) {
        free_pages(&mem_map[pfn], 0);
    }
}
