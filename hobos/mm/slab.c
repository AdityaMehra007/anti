/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * slab.c - Fine-Grained Object Cache Allocator (kmalloc / kfree)
 */

#include <hobos/mm.h>
#include <hobos/kernel.h>
#include <hobos/sync.h>

#define SLAB_SIZES 8
static const size_t slab_sizes[SLAB_SIZES] = { 16, 32, 64, 128, 256, 512, 1024, 2048 };

struct slab_buf {
    struct slab_buf *next;
};

struct kmem_cache {
    size_t obj_size;
    spinlock_t lock;
    struct slab_buf *free_list;
    uint32_t total_allocs;
    uint32_t active_objs;
};

static struct kmem_cache caches[SLAB_SIZES];

void slab_init(void) {
    printk("[SLAB] Initializing Object Caches (16B to 2048B)...\n");
    for (int i = 0; i < SLAB_SIZES; i++) {
        caches[i].obj_size = slab_sizes[i];
        spin_lock_init(&caches[i].lock);
        caches[i].free_list = NULL;
        caches[i].total_allocs = 0;
        caches[i].active_objs = 0;
    }
}

static struct kmem_cache *get_cache_for_size(size_t size) {
    for (int i = 0; i < SLAB_SIZES; i++) {
        if (size <= slab_sizes[i]) {
            return &caches[i];
        }
    }
    return NULL;
}

void *kmalloc(size_t size) {
    if (size == 0) return NULL;

    /* If size exceeds max slab, fall back to page allocation */
    if (size > 2048) {
        uint32_t order = 0;
        while ((PAGE_SIZE << order) < (size + sizeof(size_t))) {
            order++;
        }
        struct page *p = alloc_pages(order);
        if (!p) return NULL;
        size_t *header = (size_t *)p->paddr;
        *header = (order << 16) | 0xFFFF; /* Mark as page allocated */
        return (void *)(header + 1);
    }

    struct kmem_cache *cache = get_cache_for_size(size);
    if (!cache) return NULL;

    spin_lock(&cache->lock);

    if (!cache->free_list) {
        /* Allocate a new page for objects */
        void *page = alloc_page();
        if (!page) {
            spin_unlock(&cache->lock);
            return NULL;
        }

        size_t num_objs = PAGE_SIZE / cache->obj_size;
        char *ptr = (char *)page;

        for (size_t i = 0; i < num_objs; i++) {
            struct slab_buf *buf = (struct slab_buf *)(ptr + (i * cache->obj_size));
            buf->next = cache->free_list;
            cache->free_list = buf;
        }
    }

    struct slab_buf *obj = cache->free_list;
    cache->free_list = obj->next;
    cache->active_objs++;
    cache->total_allocs++;

    spin_unlock(&cache->lock);
    return (void *)obj;
}

void kfree(void *ptr) {
    if (!ptr) return;

    /* Check if it was a direct page allocation */
    size_t *header = (size_t *)ptr - 1;
    if ((*header & 0xFFFF) == 0xFFFF) {
        uint32_t order = (*header >> 16) & 0xFFFF;
        paddr_t addr = (paddr_t)header;
        free_page((void *)addr);
        return;
    }

    /* Locate cache */
    for (int i = 0; i < SLAB_SIZES; i++) {
        struct kmem_cache *cache = &caches[i];
        spin_lock(&cache->lock);
        struct slab_buf *buf = (struct slab_buf *)ptr;
        buf->next = cache->free_list;
        cache->free_list = buf;
        if (cache->active_objs > 0) cache->active_objs--;
        spin_unlock(&cache->lock);
        return;
    }
}
