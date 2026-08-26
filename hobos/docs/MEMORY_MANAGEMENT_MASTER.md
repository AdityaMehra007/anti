# 🧠 HobOS Memory Management Master (Phase 4)

## 1. Physical Page Buddy Allocator
- **Granularity**: 4KB (Order 0).
- **Max Order**: Order 10 (1024 pages = 4MB).
- **Page Descriptor**: `struct page` tracking `flags`, `order`, `ref_count`, and `paddr`.
- **Coalescing**: On `free_pages()`, buddies are indexed via XOR `pfn ^ (1 << order)` and merged up to Order 10.

## 2. Slab Object Allocator (`kmalloc` / `kfree`)
- **Tiers**: 16, 32, 64, 128, 256, 512, 1024, 2048 bytes.
- **Backing**: Dynamically allocates 4KB pages from the Buddy system and carves them into fixed-size object freelists protected by spinlocks.
- **Large Objects**: Allocations >2048 bytes bypass slab and allocate dedicated contiguous page blocks.

## 3. 4-Level Virtual Page Tables
- **Address Space**: 48-bit Virtual Addressing (256TB).
- **Levels**: L0 (512GB) -> L1 (1GB) -> L2 (2MB blocks) -> L3 (4KB pages).
- **Attributes**: `PTE_AF` (Access Flag), `PTE_SH_INNER` (Inner Shareable), `PTE_ATTRINDX` (MAIR index).

